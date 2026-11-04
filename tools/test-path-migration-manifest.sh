#!/usr/bin/env bash
# Регрессионный тест tools/path-migration-manifest.py (RFC #721 Ш4.2, issue #725).
# На синтетическом git-репозитории доказывает, что manifest redirect
# (ADR-022) разрешает историческую ссылку только на путь из манифеста и что
# проверка манифеста падает, когда он расходится с деревом или с коммитом архива:
#   * путь из манифеста разрешается, путь вне манифеста — нет;
#   * пропущенный путь, повтор, строка без адреса или с двумя адресами;
#   * удалённый по мандату путь в коммите архива, путь на теге вне коммита
#     архива, чужой тег в адресе, отсутствующий локальный адрес;
#   * файл, оставшийся под выведенным префиксом; надгробие без сигнала выбытия;
#   * недоступный archive_commit (squash или rebase вместо merge-коммита);
#   * тег, указывающий не на archive_commit.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL=(python3 -I "$ROOT_DIR/tools/path-migration-manifest.py")
SPOKE="https://github.com/example/spoke/blob/0123456789abcdef0123456789abcdef01234567"
HUB="https://github.com/example/hub"
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

pmm() { "${TOOL[@]}" --root "$repo" "$@"; }
g() { git -C "$repo" "$@"; }

# ------------------------------------------------------------ fixture
git init -q -b main "$repo"
g config user.email test@example.invalid
g config user.name test
mkdir -p "$repo/research/old/sub" "$repo/research/kept" "$repo/docs"
for f in a b pii keep; do printf '# %s\n' "$f" >"$repo/research/old/$f.md"; done
printf '# c\n' >"$repo/research/old/sub/c.md"
printf '# old index\n' >"$repo/research/old/README.md"
printf 'See [a](../research/old/a.md) and [c](../research/old/sub/c.md).\n' >"$repo/docs/hist.md"
g add -A
g commit -q -m seed
seed="$(g rev-parse HEAD)"

# α: удаление по мандату и PII, перенос keep.md внутри репозитория, надгробие.
g rm -q research/old/b.md research/old/pii.md
g mv research/old/keep.md research/kept/keep.md
write_tombstone() {
  cat >"$repo/research/old/README.md" <<EOF
---
status: deprecated
version: 1.0
---

# Old — выведен из дерева

| Прежний путь | Диспозиция | Адрес |
| --- | --- | --- |
| \`research/old/a.md\` | архив | [тег]($HUB/blob/$TAG/research/old/a.md) |
| \`research/old/b.md\` | удалён по мандату | удалён; последняя версия — \`${seed:0:7}\` |
| \`research/old/pii.md\` | удалён (PII) | удалён; последняя версия — \`${seed:0:7}\` |
| \`research/old/keep.md\` | перенесён в Хаб | [новый путь](../kept/keep.md) |
| \`research/old/sub/c.md\` | в спице | [спица]($SPOKE/sub/c.md) |
EOF
}
write_tombstone
g add -A
g commit -q -m alpha
alpha="$(g rev-parse HEAD)"

# β: остальные файлы уходят из дерева, запись path_migrations.
g rm -q research/old/a.md research/old/sub/c.md
write_profile() {
  local commit="$1"
  cat >"$repo/.hub-profile.json" <<EOF
{
  "path_migrations": [
    {"from": "research/old/keep.md", "to": "research/kept/keep.md", "issue": "x"},
    {"from": "research/old/", "to": "https://github.com/example/spoke", "manifest": "research/old/README.md",
     "archive": "$TAG", "archive_commit": "$commit", "issue": "x"}
  ]
}
EOF
}
write_profile "$alpha"
g add -A
g commit -q -m beta

reset_fixture() {
  write_tombstone
  write_profile "$alpha"
  rm -f "$repo/research/old/left.md"
  g tag -d "$TAG" >/dev/null 2>&1 || true
}

# mutate_row SED_EXPR — правит строку манифеста в рабочем дереве.
mutate_row() { sed -i "$1" "$repo/research/old/README.md"; }

# ------------------------------------------------------------ resolve
run "resolve: путь из манифеста разрешается" 0 "" -- pmm resolve research/old/a.md
run "resolve: путь с ../ нормализуется" 0 "" -- pmm resolve docs/../research/old/sub/c.md
run "resolve: файловая миграция внутри Хаба" 0 "" -- pmm resolve research/old/keep.md
run "resolve: путь вне манифеста не разрешается" 1 "" -- pmm resolve research/old/zzz.md
run "resolve: путь вне префикса не разрешается" 1 "" -- pmm resolve research/other/a.md

# ------------------------------------------------------------ check
run "check: полный манифест проходит" 0 "passed (1 manifest" -- pmm check

mutate_row '/sub\/c.md/d'
run "check: пропущенный путь" 1 "research/old/sub/c.md нет в манифесте" -- pmm check
reset_fixture

mutate_row '/`research\/old\/a.md`/p'
run "check: повтор строки" 1 "повторяет строку" -- pmm check
reset_fixture

mutate_row 's#| \[спица\](.*) |#| в спице |#'
run "check: строка без адреса" 1 "нужен ровно один адрес, найдено 0" -- pmm check
reset_fixture

mutate_row "s#\(| \`research/old/pii.md\` .*\) |\$#\1 [тег]($HUB/blob/$TAG/research/old/pii.md) |#"
run "check: два адреса в строке" 1 "нужен ровно один адрес, найдено 2" -- pmm check
reset_fixture

mutate_row "s#\[тег\]($HUB/blob/$TAG/research/old/a.md)#удалён; последняя версия — \`${seed:0:7}\`#"
run "check: удалённый путь попал в коммит архива" 1 "отмечен удалённым, но попал в archive_commit" -- pmm check
reset_fixture

mutate_row "s#удалён; последняя версия — \`${seed:0:7}\` |\$#[тег]($HUB/blob/$TAG/research/old/pii.md) |#"
run "check: адрес на теге для пути вне коммита архива" 1 "research/old/b.md адресован на тег" -- pmm check
reset_fixture

mutate_row "s#$TAG/research/old/a.md#archive/other-2026-11/research/old/a.md#"
run "check: чужой тег в адресе" 1 "не совпадает с archive" -- pmm check
reset_fixture

mutate_row "s#$TAG/research/old/a.md#$TAG/research/old/b.md#"
run "check: путь на теге не совпадает со строкой" 1 "не совпадает с прежним путём" -- pmm check
reset_fixture

mutate_row 's#(../kept/keep.md)#(../kept/missing.md)#'
run "check: локальный адрес не существует" 1 "не существует" -- pmm check
reset_fixture

printf '# left\n' >"$repo/research/old/left.md"
run "check: файл остался под префиксом" 1 "research/old/left.md остался в дереве" -- pmm check
reset_fixture

sed -i 's/^status: deprecated/status: active/' "$repo/research/old/README.md"
run "check: надгробие без сигнала выбытия" 1 "status deprecated или superseded" -- pmm check
reset_fixture

write_profile "fedcba9876543210fedcba9876543210fedcba98"
run "check: archive_commit недоступен" 1 "недоступен" -- pmm check
reset_fixture

g tag -a "$TAG" -m archive "$seed"
run "check: тег не на archive_commit" 1 "а не на archive_commit" -- pmm check
reset_fixture

g tag -a "$TAG" -m archive "$alpha"
run "check: тег на archive_commit проходит" 0 "passed" -- pmm check
reset_fixture

run "check: фикстура восстановлена" 0 "passed" -- pmm check

if ((failures > 0)); then
  printf '\n%d test(s) failed\n' "$failures" >&2
  exit 1
fi
printf '\nAll path migration manifest tests passed.\n'
