#!/usr/bin/env bash
# Регрессионный тест tools/archive-tags.py (RFC #721 Ш4.3, issue #725, Q-5 и Q-6).
# На синтетическом git-репозитории доказывает:
#   * plan: тега нет — create; тег на archive_commit — ok; тег на другом
#     коммите — падение (тег архива не переписывается); archive_commit
#     недоступен или не предок HEAD (squash/rebase) — падение;
#   * ruleset-check: эталон .github/rulesets/archive-tags.json защищает тег;
#     нет ruleset, ruleset выключен, цель branch, нет правила deletion или
#     update, тег исключён шаблоном — падение; правила из двух ruleset и ~ALL
#     засчитываются.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL=(python3 -I "$ROOT_DIR/tools/archive-tags.py")
REFERENCE="$ROOT_DIR/.github/rulesets/archive-tags.json"
TAG="archive/old-2026-11"

work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT
repo="$work_dir/repo"
failures=0

report() {
  printf '%s %s\n' "$1" "$2"
  [[ "$1" == "FAIL" ]] && failures=$((failures + 1))
  return 0
}

# run NAME EXPECTED_CODE EXPECTED_TEXT -- command...
run() {
  local name="$1" expected="$2" text="$3"
  shift 4
  set +e
  "$@" >"$work_dir/out.log" 2>&1
  local code=$?
  set -e
  if [[ "$code" != "$expected" ]]; then
    report "FAIL" "$name (код $code, ожидался $expected)"
    sed 's/^/    /' "$work_dir/out.log"
  elif [[ -n "$text" ]] && ! grep -qF -- "$text" "$work_dir/out.log"; then
    report "FAIL" "$name (нет ожидаемого текста: $text)"
    sed 's/^/    /' "$work_dir/out.log"
  else
    report "PASS" "$name"
  fi
}

g() { git -C "$repo" "$@"; }
plan() { "${TOOL[@]}" --root "$repo" plan; }
profile() {
  printf '{"path_migrations": [{"from": "research/old/", "to": "https://example.invalid/spoke", "manifest": "research/old/README.md", "archive": "%s", "archive_commit": "%s"}]}\n' "$TAG" "$1" >"$repo/.hub-profile.json"
}

# ------------------------------------------------------------ fixture
git init -q -b main "$repo"
g config user.email test@example.invalid
g config user.name test
printf 'seed\n' >"$repo/seed.md"
g add -A
g commit -q -m seed
seed="$(g rev-parse HEAD)"
printf 'alpha\n' >"$repo/alpha.md"
g add -A
g commit -q -m alpha
alpha="$(g rev-parse HEAD)"
profile "$alpha"
g add -A
g commit -q -m beta
# Ветка, не влитая в HEAD: так выглядит α после squash или rebase.
g checkout -q -b side "$seed"
printf 'side\n' >"$repo/side.md"
g add -A
g commit -q -m side
side="$(g rev-parse HEAD)"
g checkout -q main

# ------------------------------------------------------------ plan
run "plan: тега нет — create" 0 "create	$TAG	$alpha" -- plan
g tag -a "$TAG" -m archive "$alpha"
run "plan: тег на archive_commit — ok" 0 "ok	$TAG	$alpha" -- plan
g tag -d "$TAG" >/dev/null
g tag -a "$TAG" -m archive "$seed"
run "plan: тег на другом коммите — падение" 1 "не переписывается" -- plan
g tag -d "$TAG" >/dev/null
profile "fedcba9876543210fedcba9876543210fedcba98"
run "plan: archive_commit недоступен — падение" 1 "нужен merge-коммит" -- plan
profile "$side"
run "plan: archive_commit не предок HEAD — падение" 1 "не предок HEAD" -- plan
profile "$alpha"
run "plan: фикстура восстановлена" 0 "create" -- plan

# ------------------------------------------------------------ ruleset-check
check() { "${TOOL[@]}" ruleset-check "$work_dir/rulesets.json" "$TAG"; }
rulesets() { printf '%s\n' "$1" >"$work_dir/rulesets.json"; }
ruleset() {  # TARGET ENFORCEMENT INCLUDE EXCLUDE RULES
  printf '{"name": "r", "target": "%s", "enforcement": "%s", "conditions": {"ref_name": {"include": [%s], "exclude": [%s]}}, "rules": [%s]}' "$1" "$2" "$3" "$4" "$5"
}
both='{"type": "update"}, {"type": "deletion"}'

rulesets "[$(cat "$REFERENCE")]"
run "ruleset: эталон archive-tags.json защищает тег" 0 "OK refs/tags/$TAG" -- check
rulesets "[]"
run "ruleset: нет ruleset — падение" 1 "update, deletion" -- check
rulesets "[$(ruleset tag disabled '"refs/tags/archive/*"' '' "$both")]"
run "ruleset: выключен — падение" 1 "FAIL" -- check
rulesets "[$(ruleset tag evaluate '"refs/tags/archive/*"' '' "$both")]"
run "ruleset: режим evaluate — падение" 1 "FAIL" -- check
rulesets "[$(ruleset branch active '"refs/tags/archive/*"' '' "$both")]"
run "ruleset: цель branch — падение" 1 "FAIL" -- check
rulesets "[$(ruleset tag active '"refs/tags/archive/*"' '' '{"type": "update"}')]"
run "ruleset: нет правила deletion — падение" 1 "правилами deletion" -- check
rulesets "[$(ruleset tag active '"refs/tags/archive/*"' '' '{"type": "deletion"}')]"
run "ruleset: нет правила update — падение" 1 "правилами update" -- check
rulesets "[$(ruleset tag active '"refs/tags/archive/*"' '"refs/tags/archive/old-*"' "$both")]"
run "ruleset: тег исключён шаблоном — падение" 1 "FAIL" -- check
rulesets "[$(ruleset tag active '"refs/tags/release/*"' '' "$both")]"
run "ruleset: другой шаблон — падение" 1 "FAIL" -- check
rulesets "[$(ruleset tag active '"refs/tags/archive/*"' '' '{"type": "update"}'), $(ruleset tag active '"~ALL"' '' '{"type": "deletion"}')]"
run "ruleset: правила из двух ruleset и ~ALL" 0 "OK" -- check

run "message: аннотация ссылается на RFC и манифест" 0 "манифест redirect" -- "${TOOL[@]}" message "$TAG" "$alpha"

if ((failures > 0)); then
  printf '\n%d test(s) failed\n' "$failures" >&2
  exit 1
fi
printf '\nAll archive tag tests passed.\n'
