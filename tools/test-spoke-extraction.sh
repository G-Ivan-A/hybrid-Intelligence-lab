#!/usr/bin/env bash
# Регрессионный тест tools/spoke-extraction.py (issue #717): на синтетическом
# git-репозитории «Хаба» доказывает, что перенос данных в спицу детерминирован
# и проверяем по хешу, а не по пересказу агентом:
#   * manifest закреплён за SHA и падает на плавающей ссылке, коллизии путей
#     и пустом правиле map;
#   * materialize не перезаписывает существующие файлы без --overwrite;
#   * verify ловит подмену байта, пропуск файла, лишний файл и смену режима;
#   * rewrite-links (L1/L2) переписывает только то, что должен, идемпотентен,
#     не трогает код, SHA-пермалинки и файлы, изменённые после импорта;
#   * history-paths находит исторические пути переименованного файла;
#   * sections переносит разделы Markdown (спринты бэклога) дословно и
#     обнаруживает изменённую строку.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL=(python3 -I "$ROOT_DIR/tools/spoke-extraction.py")
HUB_URL="https://hub.example/org/hub"
TARGET_URL="https://hub.example/org/spoke"

work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT
hub="$work_dir/hub"
failures=0

report() {
  local status="$1" name="$2"
  printf '%s %s\n' "$status" "$name"
  [[ "$status" == "FAIL" ]] && failures=$((failures + 1))
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

ext() { "${TOOL[@]}" --hub "$hub" "$@"; }

# ---------------------------------------------------------------- fixture Hub
git init -q -b main "$hub"
git -C "$hub" config user.email test@example.invalid
git -C "$hub" config user.name test
mkdir -p "$hub/projects/demo/docs" "$hub/projects/demo/build" "$hub/ops" "$hub/research/demo-old"
printf 'old body\n' >"$hub/research/demo-old/model.md"
git -C "$hub" add -A
git -C "$hub" commit -q -m "seed old path"
mkdir -p "$hub/projects/demo/model"
git -C "$hub" mv research/demo-old/model.md projects/demo/model/model.md
cat >"$hub/projects/demo/README.md" <<'EOF'
# Demo

See [model](model/model.md), [same dir](./docs/guide.md) and [repo model](../../ops/repo-model.md).
Folder [ops](../../ops/) and [missing](../../ops/none.md) and [anchor](#demo).
Absolute [guide](https://hub.example/org/hub/blob/main/projects/demo/docs/guide.md#top).
Pinned [guide](https://hub.example/org/hub/blob/0123456789012345678901234567890123456789/projects/demo/docs/guide.md).
Foreign [rule](https://hub.example/org/hub/blob/main/ops/repo-model.md).
Code `[x](../../ops/repo-model.md)` stays.

```md
[fenced](../../ops/repo-model.md)
```

[ref]: ../../ops/repo-model.md
EOF
cat >"$hub/projects/demo/docs/guide.md" <<'EOF'
# Guide

Back to [readme](../README.md).
EOF
cat >"$hub/projects/demo/build/compile.py" <<'EOF'
SOURCE = "https://hub.example/org/hub/blob/main/projects/demo/model/model.md"
ROOT = "projects/demo"
EOF
chmod +x "$hub/projects/demo/build/compile.py"
printf 'repo model\n' >"$hub/ops/repo-model.md"
git -C "$hub" add -A
git -C "$hub" commit -q -m "demo project"
sha="$(git -C "$hub" rev-parse HEAD)"
manifest="$work_dir/manifest.tsv"

# ---------------------------------------------------------------- manifest
run "manifest: 4 файла по правилу map" 0 "manifest: 4 files" -- \
  ext manifest --sha "$sha" --map projects/demo/= -o "$manifest"
run "manifest: строки blob и пути" 0 "100755" -- grep -P "\tbuild/compile.py\tprojects/demo/build/compile.py$" "$manifest"
run "manifest: детерминирован" 0 "" -- \
  bash -c "$(printf '%q ' "${TOOL[@]}") --hub $(printf '%q' "$hub") manifest --sha $sha --map projects/demo/= | cmp - $(printf '%q' "$manifest")"
run "manifest: плавающая ссылка отклонена" 2 "full 40-hex" -- ext manifest --sha main --map projects/demo/=
run "manifest: коллизия целевых путей" 2 "target collision" -- \
  ext manifest --sha "$sha" --map projects/demo/= --map ops/repo-model.md=docs/guide.md
run "manifest: правило без файлов" 2 "matches no file" -- \
  ext manifest --sha "$sha" --map projects/demo/= --map projects/absent/=absent/
run "manifest: exclude" 0 "manifest: 3 files" -- \
  ext manifest --sha "$sha" --map projects/demo/= --exclude projects/demo/README.md

# ---------------------------------------------------------------- materialize / verify
target="$work_dir/spoke"
run "materialize: запись" 0 "materialize: 4 files" -- ext materialize --manifest "$manifest" --target "$target"
run "verify: дословная копия" 0 '"ok": 4' -- ext verify --manifest "$manifest" --target "$target" --extra-scope ""
run "materialize: отказ без --overwrite" 1 "already exist" -- ext materialize --manifest "$manifest" --target "$target"
printf 'x' >>"$target/docs/guide.md"
run "verify: подмена байта" 1 '"docs/guide.md"' -- ext verify --manifest "$manifest" --target "$target"
run "materialize --overwrite: восстановление" 0 "" -- ext materialize --manifest "$manifest" --target "$target" --overwrite
chmod -x "$target/build/compile.py"
run "verify: смена режима" 1 '"mode_mismatch": [' -- ext verify --manifest "$manifest" --target "$target"
chmod +x "$target/build/compile.py"
printf 'stray\n' >"$target/stray.md"
run "verify: лишний файл в области" 1 '"stray.md"' -- ext verify --manifest "$manifest" --target "$target" --extra-scope ""
rm "$target/stray.md"
mv "$target/docs/guide.md" "$work_dir/guide.bak"
run "verify: пропущенный файл" 1 '"missing": [' -- ext verify --manifest "$manifest" --target "$target"
mv "$work_dir/guide.bak" "$target/docs/guide.md"

# ---------------------------------------------------------------- history
run "history-paths: исторический путь" 0 "research/demo-old/model.md" -- ext history-paths --manifest "$manifest"

# ---------------------------------------------------------------- rewrite-links
log="$work_dir/rewrite.jsonl"
run "rewrite-links: --check видит изменения" 1 "to change" -- \
  ext rewrite-links --manifest "$manifest" --target "$target" --hub-url "$HUB_URL" --target-url "$TARGET_URL" --check
run "rewrite-links: применение" 0 "2 file(s) changed" -- \
  ext rewrite-links --manifest "$manifest" --target "$target" --hub-url "$HUB_URL" --target-url "$TARGET_URL" --log "$log"
readme="$target/README.md"
expect_line() {
  local name="$1" text="$2" file="$3"
  if grep -qF -- "$text" "$file"; then report "PASS" "$name"; else report "FAIL" "$name (нет: $text)"; sed 's/^/    /' "$file"; fi
}
reject_line() {
  local name="$1" text="$2" file="$3"
  if grep -qF -- "$text" "$file"; then report "FAIL" "$name (осталось: $text)"; else report "PASS" "$name"; fi
}
expect_line "L1: ссылка внутри набора не изменена" "[model](model/model.md)" "$readme"
expect_line "L1: ./ внутри набора не изменена" "[same dir](./docs/guide.md)" "$readme"
expect_line "L1: файл вне набора -> пермалинк SHA" "[repo model]($HUB_URL/blob/$sha/ops/repo-model.md)" "$readme"
expect_line "L1: каталог вне набора -> tree SHA" "[ops]($HUB_URL/tree/$sha/ops)" "$readme"
expect_line "L1: несуществующая цель не изменена" "[missing](../../ops/none.md)" "$readme"
expect_line "L1: якорь не изменён" "[anchor](#demo)" "$readme"
expect_line "L1: reference definition" "[ref]: $HUB_URL/blob/$sha/ops/repo-model.md" "$readme"
expect_line "L1: inline code не изменён" '`[x](../../ops/repo-model.md)`' "$readme"
expect_line "L1: fenced code не изменён" "[fenced](../../ops/repo-model.md)" "$readme"
expect_line "L2: URL main внутри набора -> спица" "[guide]($TARGET_URL/blob/main/docs/guide.md#top)" "$readme"
expect_line "L2: SHA-пермалинк не изменён" "$HUB_URL/blob/0123456789012345678901234567890123456789/projects/demo/docs/guide.md" "$readme"
expect_line "L2: URL вне набора не изменён" "[rule]($HUB_URL/blob/main/ops/repo-model.md)" "$readme"
expect_line "L2: не-Markdown файл" "SOURCE = \"$TARGET_URL/blob/main/model/model.md\"" "$target/build/compile.py"
expect_line "L1: обратная ссылка внутри набора" "[readme](../README.md)" "$target/docs/guide.md"
expect_line "log: unresolved записан" '"kind": "unresolved"' "$log"
run "rewrite-links: идемпотентность (--check)" 0 "0 file(s) to change" -- \
  ext rewrite-links --manifest "$manifest" --target "$target" --hub-url "$HUB_URL" --target-url "$TARGET_URL" --check
run "verify --links: ожидаемое содержимое" 0 '"mode": "links"' -- \
  ext verify --manifest "$manifest" --target "$target" --links --hub-url "$HUB_URL" --target-url "$TARGET_URL"
run "verify без --links: файлы переписаны" 1 '"mismatch": [' -- ext verify --manifest "$manifest" --target "$target"
run "scan: остаток старого префикса" 0 'build/compile.py:2: projects/demo/' -- ext scan --manifest "$manifest" --target "$target"

# файл, изменённый после импорта, не перезаписывается
target2="$work_dir/spoke2"
ext materialize --manifest "$manifest" --target "$target2" >/dev/null 2>&1
printf 'local edit\n' >>"$target2/README.md"
run "rewrite-links: правка после импорта -> отказ" 1 "modified after import: README.md" -- \
  ext rewrite-links --manifest "$manifest" --target "$target2" --hub-url "$HUB_URL" --target-url "$TARGET_URL"
reject_line "rewrite-links: локальная правка сохранена" "$HUB_URL/blob/$sha/ops/repo-model.md" "$target2/README.md"

# ---------------------------------------------------------------- substitute
skel_manifest="$work_dir/skel.tsv"
printf 'name: {{project_name}} {{unknown_key}}\n' >"$hub/ops/skel.md"
git -C "$hub" add -A && git -C "$hub" commit -q -m skel
sha2="$(git -C "$hub" rev-parse HEAD)"
ext manifest --sha "$sha2" --map ops/skel.md=AGENTS.md -o "$skel_manifest" 2>/dev/null
run "materialize --substitute: остаток плейсхолдера" 0 "placeholder left: AGENTS.md: {{unknown_key}}" -- \
  ext materialize --manifest "$skel_manifest" --target "$work_dir/skel" --substitute project_name=demo-spoke
expect_line "materialize --substitute: подстановка" "name: demo-spoke {{unknown_key}}" "$work_dir/skel/AGENTS.md"

# ---------------------------------------------------------------- sections
cat >"$hub/ops/backlog.md" <<'EOB'
# Backlog

## Sprint 1: demo

| ID | Link |
| --- | --- |
| B-1 | [model](../projects/demo/model/model.md), [rule](repo-model.md) |

### Note

```md
## Sprint 9: not a heading inside code
```

## Sprint 2: other

| B-2 | other |
EOB
git -C "$hub" add -A && git -C "$hub" commit -q -m backlog
sha3="$(git -C "$hub" rev-parse HEAD)"
manifest3="$work_dir/manifest3.tsv"
ext manifest --sha "$sha3" --map projects/demo/= -o "$manifest3" 2>/dev/null
sections_out="$work_dir/sections.md"
run "sections: извлечение раздела с подразделом" 0 "sections: 1 from ops/backlog.md" -- \
  ext sections --sha "$sha3" --source ops/backlog.md --heading "## Sprint 1:" --manifest "$manifest3" \
  --target-path ops/backlog.md --hub-url "$HUB_URL" -o "$sections_out"
expect_line "sections: ссылка внутри набора -> путь спицы" "[model](../model/model.md)" "$sections_out"
expect_line "sections: ссылка вне набора -> пермалинк SHA" "[rule]($HUB_URL/blob/$sha3/ops/repo-model.md)" "$sections_out"
expect_line "sections: подраздел включён" "### Note" "$sections_out"
reject_line "sections: следующий раздел не включён" "B-2" "$sections_out"
run "sections: неоднозначный или отсутствующий заголовок" 2 "matches 0 headings" -- \
  ext sections --sha "$sha3" --source ops/backlog.md --heading "## Sprint 9:"
{ printf '# Spoke backlog\n\n'; cat "$sections_out"; } >"$work_dir/spoke-backlog.md"
run "sections --check: раздел присутствует" 0 "" -- \
  ext sections --sha "$sha3" --source ops/backlog.md --heading "## Sprint 1:" --manifest "$manifest3" \
  --target-path ops/backlog.md --hub-url "$HUB_URL" --check "$work_dir/spoke-backlog.md"
sed -i 's/| B-1 |/| B-1x |/' "$work_dir/spoke-backlog.md"
run "sections --check: изменённая строка" 1 "section absent or changed: ## Sprint 1:" -- \
  ext sections --sha "$sha3" --source ops/backlog.md --heading "## Sprint 1:" --manifest "$manifest3" \
  --target-path ops/backlog.md --hub-url "$HUB_URL" --check "$work_dir/spoke-backlog.md"

if (( failures > 0 )); then
  printf '\n%d проверок упало\n' "$failures" >&2
  exit 1
fi
printf '\nВсе проверки spoke-extraction прошли.\n'
