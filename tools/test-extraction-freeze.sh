#!/usr/bin/env bash
# Регрессионный тест tools/check-extraction-freeze.sh (B-243 Ш3.0, issue #738).
# На синтетическом git-репозитории доказывает:
#   * нет коммитов после HUB_SHA или они не трогают источники — проходит;
#   * коммит меняет файл в каталоге-источнике (`dir/=`), файл-источник или
#     удаляет источник — падение с ::error:: и списком коммитов;
#   * revert не снимает нарушение (контракт видит любой коммит в источниках);
#   * ветка без HUB_SHA в истории: проверяются её собственные коммиты;
#   * HUB_SHA не 40 hex, недоступен, нет строк MAP — падение;
#   * параметры выноса Хаба: заморозка держалась до надгробия B-249, которое
#     её снимает (первый коммит в источниках после HUB_SHA — коммит B-249).
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL="$ROOT_DIR/tools/check-extraction-freeze.sh"
HUB_PARAMS="$ROOT_DIR/research/hub/exp/ba-extraction-717/ba-instance-params.txt"

work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT
repo="$work_dir/repo"
failures=0

report() {
  printf '%s %s\n' "$1" "$2"
  [[ "$1" == "FAIL" ]] && failures=$((failures + 1))
  return 0
}

# run NAME EXPECTED_CODE EXPECTED_TEXT PARAMS [REV]
run() {
  local name="$1" expected_code="$2" expected_text="$3"
  shift 3
  local out code=0
  out="$(cd "$repo" && bash "$TOOL" "$@" 2>&1)" || code=$?
  if [[ "$code" != "$expected_code" ]]; then
    report FAIL "$name: exit $code, expected $expected_code"
    printf '%s\n' "$out" | sed 's/^/    /'
  elif [[ "$out" != *"$expected_text"* ]]; then
    report FAIL "$name: output lacks '$expected_text'"
    printf '%s\n' "$out" | sed 's/^/    /'
  else
    report PASS "$name"
  fi
}

commit() {
  git -C "$repo" add -A
  git -C "$repo" commit --quiet -m "$1"
}

git init --quiet -b main "$repo"
git -C "$repo" config user.email test@example.invalid
git -C "$repo" config user.name test
mkdir -p "$repo/projects/demo/core" "$repo/docs" "$repo/tools"
echo a > "$repo/projects/demo/core/model.md"
echo b > "$repo/docs/overview.md"
echo c > "$repo/tools/test-demo.sh"
echo d > "$repo/docs/other.md"
commit "pre"
PRE_SHA="$(git -C "$repo" rev-parse HEAD)"
echo k >> "$repo/projects/demo/core/model.md"
commit "base"
HUB_SHA="$(git -C "$repo" rev-parse HEAD)"

params="$work_dir/params.txt"
cat > "$params" <<EOF
HUB_REPO: owner/hub
HUB_SHA: $HUB_SHA
MAP: projects/demo/=
MAP: docs/overview.md=docs/overview.md
MAP: tools/test-demo.sh=tools/test-demo.sh
DIR: core | demo
STAGE:
EOF

run "no commits after HUB_SHA" 0 "extraction freeze OK: 3 source path(s)" "$params"

echo e >> "$repo/docs/other.md"
commit "unrelated change"
run "unrelated commit passes" 0 "extraction freeze OK" "$params"

git -C "$repo" branch before-source
echo f >> "$repo/projects/demo/core/model.md"
commit "edit nested file of a source directory"
run "nested file in source directory" 1 "edit nested file of a source directory" "$params"
run "error annotation" 1 "::error::extraction freeze" "$params"
run "changed file listed" 1 "projects/demo/core/model.md" "$params"

git -C "$repo" revert --quiet --no-edit HEAD >/dev/null
run "revert does not lift the freeze" 1 "edit nested file of a source directory" "$params"

git -C "$repo" checkout --quiet -b file-source before-source
echo g >> "$repo/docs/overview.md"
commit "edit single source file"
run "single source file" 1 "edit single source file" "$params"

git -C "$repo" checkout --quiet -b delete-source before-source
git -C "$repo" rm --quiet tools/test-demo.sh
commit "delete a source test"
run "deleted source" 1 "delete a source test" "$params"

git -C "$repo" checkout --quiet before-source
run "explicit REV before the violation" 0 "extraction freeze OK" "$params" before-source
run "explicit REV with the violation" 1 "delete a source test" "$params" delete-source

sed "s/^HUB_SHA: .*/HUB_SHA: ${HUB_SHA:0:12}/" "$params" > "$work_dir/short.txt"
run "short HUB_SHA" 1 "не 40 hex" "$work_dir/short.txt"

sed "s/^HUB_SHA: .*/HUB_SHA: $(printf '0%.0s' {1..40})/" "$params" > "$work_dir/missing.txt"
run "unavailable HUB_SHA" 1 "fetch-depth: 0" "$work_dir/missing.txt"

# Ветка от коммита до HUB_SHA: проверяются только её собственные коммиты.
git -C "$repo" checkout --quiet -b old-clean "$PRE_SHA"
echo i > "$repo/unrelated.md"
commit "old branch, unrelated change"
git -C "$repo" checkout --quiet -b old-dirty "$PRE_SHA"
echo j >> "$repo/projects/demo/core/model.md"
commit "old branch edits a source"
git -C "$repo" checkout --quiet before-source
run "branch without HUB_SHA: notice" 0 "::notice::extraction freeze" "$params" old-clean
run "branch without HUB_SHA, unrelated change" 0 "extraction freeze OK" "$params" old-clean
run "branch without HUB_SHA edits a source" 1 "old branch edits a source" "$params" old-dirty

grep -v '^MAP:' "$params" > "$work_dir/nomap.txt"
run "no MAP lines" 1 "нет строк MAP" "$work_dir/nomap.txt"
run "missing params file" 1 "нет файла параметров" "$work_dir/absent.txt"

# Параметры выноса Хаба: проверка на самом репозитории, если в нём есть история.
# Заморозку снимает надгробие B-249: первый коммит после HUB_SHA, меняющий
# источники, должен быть коммитом B-249, а до его родителя заморозка держалась.
hub_sha="$(sed -n 's/^HUB_SHA: //p' "$HUB_PARAMS")"
if git -C "$ROOT_DIR" cat-file -e "$hub_sha^{commit}" 2>/dev/null; then
  mapfile -t hub_sources < <(sed -n 's/^MAP: \([^=]*\)=.*/\1/p' "$HUB_PARAMS")
  tombstone="$(git -C "$ROOT_DIR" log --reverse --format=%H "$hub_sha..HEAD" -- "${hub_sources[@]}" | head -n 1)"
  if [[ -z "$tombstone" ]]; then
    rev="HEAD"
    label="Hub BA extraction params (freeze active)"
  elif git -C "$ROOT_DIR" log -1 --format=%s "$tombstone" | grep -q 'B-249'; then
    rev="$tombstone^"
    label="Hub BA extraction params (freeze held until tombstone ${tombstone:0:7})"
  else
    rev=""
    report FAIL "Hub BA extraction params: first source change ${tombstone:0:7} is not the B-249 tombstone"
    git -C "$ROOT_DIR" log -1 --format='    %h %s' "$tombstone"
  fi
  if [[ -n "$rev" ]]; then
    if out="$(cd "$ROOT_DIR" && bash "$TOOL" "$HUB_PARAMS" "$rev" 2>&1)"; then
      report PASS "$label: $out"
    else
      report FAIL "$label"
      printf '%s\n' "$out" | sed 's/^/    /'
    fi
  fi
else
  report SKIP "Hub BA extraction params: HUB_SHA not in this clone (shallow?)"
fi

if [[ "$failures" -gt 0 ]]; then
  echo "test-extraction-freeze: $failures failure(s)" >&2
  exit 1
fi
echo "test-extraction-freeze: all scenarios passed"
