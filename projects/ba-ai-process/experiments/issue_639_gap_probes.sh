#!/usr/bin/env bash
# Experiment for issue #639: empirical probes behind the expectation-gap audit.
# Runs on a temporary copy of the Cline package; the repository is not modified.
set -u
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../dist/execution-package-cline-vscode" && pwd)"
W=$(mktemp -d)/runtime
cp -r "$SRC" "$W"
cd "$W"
seal() {
python3 - "$1" <<'PY'
import json, sys, hashlib
sys.path.insert(0, "tools")
import bcreq_pipeline as p
path = sys.argv[1]
w = json.load(open(path, encoding="utf-8"))
for s in w.get("evidence", []):
    s["checksum"] = "sha256:" + hashlib.sha256(s["excerpt"].encode("utf-8")).hexdigest()
w["working_digest"] = p.working_digest(w)
open(path, "w", encoding="utf-8").write(json.dumps(w, ensure_ascii=False, indent=2) + "\n")
PY
}
edit() {  # edit <file> <python statements operating on w>
python3 - "$1" "$2" <<'PY'
import json, sys
path, code = sys.argv[1], sys.argv[2]
w = json.load(open("golden/TASK-0001.json", encoding="utf-8"))
exec(code)
json.dump(w, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
PY
}
echo "== P1. baseline: check-package and verify-ci"
python3 tools/run_task.py check-package; python3 tools/run_task.py verify-ci; echo "exit=$?"

echo "== P2. semantic_review removed (G-semantic before G-mach), sealed"
edit submissions/TASK-0101.json 'del w["semantic_review"]'; seal submissions/TASK-0101.json
python3 tools/bcreq_pipeline.py validate-working submissions/TASK-0101.json; echo "exit=$?"

echo "== P3. semantic_review self-declared by the agent, sealed"
edit submissions/TASK-0102.json 'w["semantic_review"].update(reviewed_by="cline-agent", rationale="ok", counterexample="none")'
seal submissions/TASK-0102.json
python3 tools/bcreq_pipeline.py validate-working submissions/TASK-0102.json; echo "exit=$?"

echo "== P4. fabricated evidence (non-existent locator, invented excerpt), sealed"
edit submissions/TASK-0103.json 'w["evidence"][0].update(locator="https://nonexistent.invalid/page/42", excerpt="Выдуманная цитата, которой нет ни в одном источнике.")'
seal submissions/TASK-0103.json
python3 tools/run_task.py run TASK-0103 submissions/TASK-0103.json; echo "exit=$?"

echo "== P5. determinism: compile twice, compare bytes"
python3 tools/bcreq_pipeline.py compile golden/TASK-0001.json --output /tmp/i639-a >/dev/null
python3 tools/bcreq_pipeline.py compile golden/TASK-0001.json --output /tmp/i639-b >/dev/null
cmp /tmp/i639-a/release.json /tmp/i639-b/release.json && echo "identical release.json"

echo "== P6. release format: line count, size, headings"
wc -l -c < /tmp/i639-a/release.json
python3 -c "
import json; r=json.load(open('/tmp/i639-a/release.json',encoding='utf-8'))
print('top-level keys:', sorted(r)[:12])
secs=r.get('sections') or []
print('section titles:', [(s.get('heading'), len(s.get('fragments') or [])) for s in secs][:12] if isinstance(secs,list) else type(secs))"

echo "== P7. failed run: is the error text kept in the trace?"
python3 tools/run_task.py run TASK-0104 submissions/TASK-0101.json 2>/tmp/i639-stderr.txt; echo "exit=$?"
echo "stderr:"; cat /tmp/i639-stderr.txt
echo "trace:"; python3 -c "
import json
for l in open('runs/TASK-0104/trace.jsonl',encoding='utf-8'):
    d=json.loads(l); print(d['node'],d['state'],d.get('exit_code'),d.get('detail'))"
echo "rerun same ID:"; python3 tools/run_task.py run TASK-0104 submissions/TASK-0101.json; echo "exit=$?"

echo "== P8. hook decisions for selected Cline tools"
for t in read_file use_mcp_tool plan_mode_respond execute_command browser_action new_task; do
  printf '%-20s ' "$t"
  echo "{\"hookName\":\"PreToolUse\",\"preToolUse\":{\"toolName\":\"$t\",\"parameters\":{}}}" | python3 tools/cline_hook.py
done
printf '%-20s ' "write ../AGENTS.md"
echo '{"hookName":"PreToolUse","preToolUse":{"toolName":"write_to_file","parameters":{"path":"AGENTS.md"}}}' | python3 tools/cline_hook.py
printf '%-20s ' "write submissions"
echo '{"hookName":"PreToolUse","preToolUse":{"toolName":"write_to_file","parameters":{"path":"submissions/TASK-0200.json"}}}' | python3 tools/cline_hook.py

echo "== P9. which package files reference the process menu / meta-model"
ls meta-model; ls routes; grep -c route_id routes/*.json
