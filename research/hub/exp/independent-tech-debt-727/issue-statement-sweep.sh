#!/usr/bin/env bash
# Ретро-прогон гейта постановки tools/validate-issue-statement.sh (B-116 (d))
# по последним issue Хаба и по «нулевому пациенту» mango#353.
# Только чтение: `gh issue list/view` и локальный запуск гейта; ничего не публикует.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
GATE="$ROOT_DIR/tools/validate-issue-statement.sh"
LIMIT="${SWEEP_LIMIT:-150}"
work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT

printf '# issue-statement sweep: hub HEAD %s, limit %s\n' "$(git -C "$ROOT_DIR" rev-parse --short HEAD)" "$LIMIT"

gh issue list --repo G-Ivan-A/hybrid-Intelligence-lab --state all --limit "$LIMIT" \
  --json number,body >"$work_dir/issues.json"
python3 -I - "$work_dir" <<'PY'
import json, sys
work = sys.argv[1]
for item in json.load(open(f"{work}/issues.json", encoding="utf-8")):
    with open(f"{work}/{item['number']}.md", "w", encoding="utf-8") as handle:
        handle.write(item["body"] or "")
PY

ok=0
red=0
for body in $(ls "$work_dir"/*.md | sort -V); do
  number="$(basename "$body" .md)"
  if out="$(bash "$GATE" "$body" 2>&1)"; then
    ok=$((ok + 1))
  else
    red=$((red + 1))
    printf '## hub#%s\n' "$number"
    printf '%s\n' "$out" | grep -a 'FAIL' | sed -E 's/^issue-statement: FAIL (line [0-9]+) \(«([^»]*)»\): path ([^ ]+) (is forbidden|uses top-level directory [^ ]+ moved|creates top-level directory [^ ]+).*/  \1 [\2] \3: \4/'
  fi
done
printf 'hub issues: %s checked, %s OK, %s red\n' "$((ok + red))" "$ok" "$red"

printf '## mango#353 (нулевой пациент F7, путь предписан в «Готово, когда»)\n'
gh issue view 353 --repo G-Ivan-A/mango_ba_prompts --json body -q .body >"$work_dir/m353.md"
if bash "$GATE" "$work_dir/m353.md" >"$work_dir/m353.log" 2>&1; then
  printf 'mango#353: OK (gate missed patient zero)\n'
else
  grep -a 'FAIL' "$work_dir/m353.log" | sed -E 's/^issue-statement: FAIL (line [0-9]+) \(«([^»]*)»\): path ([^ ]+) (is forbidden|creates top-level directory [^ ]+).*/  \1 [\2] \3: \4/'
  printf 'mango#353: red (patient zero caught)\n'
fi
