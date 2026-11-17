#!/usr/bin/env bash
# Finite, offline integration and refusal tests for the issue-742 import package.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
GFR="${GFR:?set GFR to git-filter-repo 2.47.0}"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
git init --quiet -b main "$WORK/base"
git -C "$WORK/base" config user.name 'Extraction test'
git -C "$WORK/base" config user.email 'test@example.invalid'
printf '# aether-orbis-proxeneta\n[add]\n' > "$WORK/base/README.md"
git -C "$WORK/base" add README.md
git -C "$WORK/base" commit --quiet -m 'Destination fixture'
prepare() {
  python3 -I "$HERE/prepare-import.py" --filter-repo "$GFR" --target-base "$WORK/base" --out "$1"
}
prepare "$WORK/import" > "$WORK/prepare.log" 2>&1 || { cat "$WORK/prepare.log"; exit 1; }
python3 -I - "$WORK/import/summary.json" <<'PY'
import json, sys
s = json.load(open(sys.argv[1]))
assert s['files'] == 79 and s['backlog_rows'] == 28
assert len(s['ci_steps']) == 5 and s['local_checks'] == 'PASS'
assert 'unresolved' not in s['link_events'] and 'outside-repo' not in s['link_events']
PY
if prepare "$WORK/import" > "$WORK/refusal.log" 2>&1; then
  echo 'FAIL: accepted an existing output directory'; exit 1
fi
grep -Fq 'must be a new directory outside the Hub' "$WORK/refusal.log"
if prepare "$HERE/forbidden-output" > "$WORK/refusal.log" 2>&1; then
  echo 'FAIL: accepted output inside the Hub'; exit 1
fi
grep -Fq 'must be a new directory outside the Hub' "$WORK/refusal.log"
printf 'human work\n' > "$WORK/base/new.md"
if prepare "$WORK/rejected" > "$WORK/refusal.log" 2>&1; then
  echo 'FAIL: accepted a dirty destination'; exit 1
fi
grep -Fq 'uncommitted changes' "$WORK/refusal.log"
git -C "$WORK/base" add new.md
git -C "$WORK/base" commit --quiet -m 'New human work'
if prepare "$WORK/rejected" > "$WORK/refusal.log" 2>&1; then
  echo 'FAIL: accepted new destination content'; exit 1
fi
grep -Fq 'no longer README-only' "$WORK/refusal.log"
git -C "$WORK/base" rm --quiet new.md
printf '# New human README\n' > "$WORK/base/README.md"
git -C "$WORK/base" add README.md
git -C "$WORK/base" commit --quiet -m 'Human README on README-only destination'
if prepare "$WORK/rejected" > "$WORK/refusal.log" 2>&1; then
  echo 'FAIL: overwrote a changed README on a README-only destination'; exit 1
fi
grep -Fq 'README changed from the observed placeholder' "$WORK/refusal.log"
test ! -e "$WORK/rejected"
printf 'PASS: offline import, existing output, Hub output, dirty destination, changed destination, changed README\n'
