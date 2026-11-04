#!/usr/bin/env bash
#
# End-to-end test for the Smart Sync infrastructure (issue #207):
#   - tools/generate-manifest.py  (manifest generation + drift check)
#   - tools/sync-from-hub.sh      (--init, --report, --apply, --apply --force)
#
# Uses the real Hub repo as a --local source and a throwaway spoke workspace.
# No network access required.
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="${PYTHON:-python3}"
PASS=0
FAIL=0

ok()   { printf '  ✅ %s\n' "$1"; PASS=$((PASS+1)); }
bad()  { printf '  ❌ %s\n' "$1"; FAIL=$((FAIL+1)); }
check() { if eval "$2"; then ok "$1"; else bad "$1"; fi; }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "== 1. manifest generator =="
"$PY" "$REPO_ROOT/tools/generate-manifest.py" --check >/dev/null 2>&1 \
  && ok "manifest.json is in sync with templates/ tree" \
  || bad "manifest.json drift detected"

"$PY" "$REPO_ROOT/tools/generate-manifest.py" > "$WORK/manifest-stdout.json"
check "generated manifest is valid JSON" "$PY -c 'import json,sys; json.load(open(\"$WORK/manifest-stdout.json\"))'"
check "manifest lists the handover prompt artifact" \
  "grep -q 'htom-ai-session-handover-prompt' \"$WORK/manifest-stdout.json\""

echo "== 2. spoke workspace + --init (non-interactive via piped answers) =="
SPOKE="$WORK/spoke"
mkdir -p "$SPOKE"
cd "$SPOKE"
# answers: create=Y, name, type=2(Spoke), stack=5(all), phase=1(MVP)
printf 'Y\nmango_ba_prompts\n2\n5\n1\n' | \
  bash "$REPO_ROOT/tools/sync-from-hub.sh" --init --profile "$SPOKE/.hub-profile.json" \
       --hub "https://github.com/G-Ivan-A/hybrid-Intelligence-lab" >/dev/null
check ".hub-profile.json created" "[ -f \"$SPOKE/.hub-profile.json\" ]"
check "profile has project_name" "grep -q 'mango_ba_prompts' \"$SPOKE/.hub-profile.json\""
check "profile target_type=Spoke" "grep -q '\"Spoke\"' \"$SPOKE/.hub-profile.json\""
check "profile last_sync empty" "$PY -c 'import json; assert json.load(open(\"$SPOKE/.hub-profile.json\"))[\"last_sync\"]=={}'"

echo "== 3. --report against local Hub (everything new) =="
REPORT="$WORK/report.txt"
bash "$REPO_ROOT/tools/sync-from-hub.sh" --report --local "$REPO_ROOT" \
     --profile "$SPOKE/.hub-profile.json" > "$REPORT"
cat "$REPORT" | sed 's/^/    /'
check "report header present" "grep -q 'Hub Sync Report for' \"$REPORT\""
check "report lists updates section" "grep -q 'релевантные обновления' \"$REPORT\""
check "report shows Spoke template (spoke README)" "grep -q 'README.md' \"$REPORT\""
check "report does NOT leak HTOM-only AI_QUICK_RULES" "! grep -q 'AI_QUICK_RULES' \"$REPORT\""

echo "== 4. safe --apply (no local files yet → files written; no .hub-new) =="
bash "$REPO_ROOT/tools/sync-from-hub.sh" --apply --local "$REPO_ROOT" \
     --profile "$SPOKE/.hub-profile.json" > "$WORK/apply1.txt"
check "spoke README.md written" "[ -f \"$SPOKE/README.md\" ]"
check "ci.yml written to .github/workflows/" "[ -f \"$SPOKE/.github/workflows/ci.yml\" ]"
check "handover prompt written (Spoke target)" "[ -f \"$SPOKE/AI_SESSION_HANDOVER_PROMPT.md\" ]"
check "last_sync updated after apply" \
  "$PY -c 'import json; d=json.load(open(\"$SPOKE/.hub-profile.json\"))[\"last_sync\"]; assert d, d'"

echo "== 5. re-report after apply (now up to date) =="
bash "$REPO_ROOT/tools/sync-from-hub.sh" --report --local "$REPO_ROOT" \
     --profile "$SPOKE/.hub-profile.json" > "$WORK/report2.txt"
check "second report says synchronized" "grep -q 'синхронизировано' \"$WORK/report2.txt\""

echo "== 6. local edit + safe apply does NOT overwrite (creates .hub-new) =="
# Simulate a newer hub version by resetting last_sync for the spoke README.
$PY - "$SPOKE/.hub-profile.json" <<'PY'
import json, sys
p = sys.argv[1]
d = json.load(open(p, encoding="utf-8"))
d["last_sync"].pop("spoke-readme", None)
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
PY
printf '# LOCAL EDIT — do not lose me\n' > "$SPOKE/README.md"
bash "$REPO_ROOT/tools/sync-from-hub.sh" --apply --local "$REPO_ROOT" \
     --profile "$SPOKE/.hub-profile.json" > "$WORK/apply2.txt"
check "local README.md preserved (safe mode)" "grep -q 'LOCAL EDIT' \"$SPOKE/README.md\""
check ".hub-new.md created alongside" "[ -f \"$SPOKE/README.hub-new.md\" ]"

echo "== 7. --apply --force overwrites local file =="
$PY - "$SPOKE/.hub-profile.json" <<'PY'
import json, sys
p = sys.argv[1]
d = json.load(open(p, encoding="utf-8"))
d["last_sync"].pop("spoke-readme", None)
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
PY
printf '# LOCAL EDIT 2\n' > "$SPOKE/README.md"
bash "$REPO_ROOT/tools/sync-from-hub.sh" --apply --force --local "$REPO_ROOT" \
     --profile "$SPOKE/.hub-profile.json" > "$WORK/apply3.txt"
check "force overwrote local README.md" "! grep -q 'LOCAL EDIT 2' \"$SPOKE/README.md\""

echo "== 8. HTOM bootstrap renders Hybrid as the default Operating Mode (B-197, ADR-021 K-1) =="
# mode_default_ok FILE — файл называет Hybrid режимом по умолчанию и не
# объявляет Structured неявным умолчанием (переносы строк схлопываются).
mode_default_ok() {
  "$PY" - "$1" <<'PY'
import re, sys
text = re.sub(r"\s+", " ", open(sys.argv[1], encoding="utf-8").read())
bad = re.search(r"по умолчанию\W{0,3}\s*structured|structured\W{0,3}\s*(mode\s+)?(\|\s*)?по умолчанию", text, re.I)
good = re.search(r"по умолчанию — Hybrid|Hybrid mode \(по умолчанию\)|\| Hybrid \| По умолчанию|`Hybrid` \(по умолчанию\)", text)
sys.exit(0 if good and not bad else 1)
PY
}
HTOM_INIT="$WORK/htom-init"
cp -R "$REPO_ROOT/templates/htom" "$HTOM_INIT"
bash "$HTOM_INIT/init.sh" -n "Demo HTOM" -d "Bootstrap test" \
     -u "https://github.com/G-Ivan-A/hybrid-Intelligence-lab" --yes >/dev/null
check "init.sh removed itself after bootstrap" "[ ! -f \"$HTOM_INIT/init.sh\" ]"
check "init.sh: no {{date}} placeholder left in handover prompt" \
  "! grep -q '{{date}}' \"$HTOM_INIT/AI_SESSION_HANDOVER_PROMPT.md\""
for rel in AI_SESSION_HANDOVER_PROMPT.md AI_GOVERNANCE.md .github/ISSUE_TEMPLATE/task.md; do
  check "init.sh: $rel names Hybrid as default mode" "mode_default_ok \"$HTOM_INIT/$rel\""
done
# B-115 (issue #727): геном доставляет пять уровней постановки, плейсхолдеры подставлены.
for level in "Уровень 1. User Story" "Уровень 2. ФТ к системе" "Уровень 3. НФТ к системе" \
             "Уровень 4. Задача исполнителю" "Уровень 5. Ограничения процесса"; do
  check "init.sh: task.md renders '## $level'" \
    "grep -qx '## $level' \"$HTOM_INIT/.github/ISSUE_TEMPLATE/task.md\""
done
check "init.sh: task.md has no {{project_name}} / {{date}} placeholder left" \
  "! grep -q '{{project_name}}\\|{{date}}' \"$HTOM_INIT/.github/ISSUE_TEMPLATE/task.md\""
check "init.sh: AGENTS.md defaults an omitted mode to Hybrid" \
  "grep -q 'an omitted mode defaults to Hybrid' \"$HTOM_INIT/AGENTS.md\""
check "bootstrapped HTOM team passes its own structure validator" \
  "(cd \"$HTOM_INIT\" && bash tools/validate-repository-structure.sh >/dev/null 2>&1)"

HTOM_SYNC="$WORK/htom-sync"
mkdir -p "$HTOM_SYNC"
cd "$HTOM_SYNC"
# answers: create=Y, name, type=1(HTOM), stack=5(all), phase=1(MVP)
printf 'Y\ndemo-htom\n1\n5\n1\n' | \
  bash "$REPO_ROOT/tools/sync-from-hub.sh" --init --profile "$HTOM_SYNC/.hub-profile.json" \
       --hub "https://github.com/G-Ivan-A/hybrid-Intelligence-lab" >/dev/null
check "HTOM profile target_type=HTOM" "grep -q '\"HTOM\"' \"$HTOM_SYNC/.hub-profile.json\""
bash "$REPO_ROOT/tools/sync-from-hub.sh" --apply --local "$REPO_ROOT" \
     --profile "$HTOM_SYNC/.hub-profile.json" > "$WORK/apply-htom.txt"
for rel in AI_SESSION_HANDOVER_PROMPT.md AI_GOVERNANCE.md .github/ISSUE_TEMPLATE/task.md; do
  check "smart sync (HTOM): $rel names Hybrid as default mode" "mode_default_ok \"$HTOM_SYNC/$rel\""
done
check "smart sync (Spoke): handover prompt names Hybrid as default mode" \
  "mode_default_ok \"$SPOKE/AI_SESSION_HANDOVER_PROMPT.md\""
cd "$REPO_ROOT"

echo ""
echo "Passed: $PASS  Failed: $FAIL"
[ "$FAIL" -eq 0 ]
