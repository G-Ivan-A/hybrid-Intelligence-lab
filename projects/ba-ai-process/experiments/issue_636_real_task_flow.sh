#!/usr/bin/env bash
# Experiment for issue #636: can a modified (non-golden) task reach PASS,
# what happens on rerun, and how verify-ci treats failed drafts in submissions/.
set -u
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/../dist/execution-package-cline-vscode" && pwd)"
W=$(mktemp -d)/runtime
cp -r "$SRC" "$W"
cd "$W"
echo "== 1. check-package"; python3 tools/run_task.py check-package
echo "== 2. edited draft without sealing"
python3 - <<'PY'
import json
w=json.load(open("golden/TASK-0001.json",encoding="utf-8"))
w["evidence"][0]["locator"]="https://jira.example.test/browse/BCREQ-123"
w["evidence"][0]["excerpt"]="Клиент должен выгружать журнал звонков."
w["goals"][0]["text"]="Клиенты получают отчёты"
json.dump(w,open("submissions/TASK-0002.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
PY
python3 tools/run_task.py run TASK-0002 submissions/TASK-0002.json; echo "exit=$?"
echo "== 3. rerun same ID"; python3 tools/run_task.py run TASK-0002 submissions/TASK-0002.json; echo "exit=$?"
echo "== 4. verify-ci with failed draft in submissions/"; python3 tools/run_task.py verify-ci; echo "exit=$?"
echo "== 5. seal (stdin script) and run under new ID"
cp submissions/TASK-0002.json submissions/TASK-0003.json
python3 - submissions/TASK-0003.json <<'PY'
import json, sys, hashlib
sys.path.insert(0, "tools")
import bcreq_pipeline as p
path = sys.argv[1]
w = json.load(open(path, encoding="utf-8"))
for s in w.get("evidence", []):
    s["checksum"] = "sha256:" + hashlib.sha256(s["excerpt"].encode("utf-8")).hexdigest()
w["working_digest"] = p.working_digest(w)
open(path, "w", encoding="utf-8").write(json.dumps(w, ensure_ascii=False, indent=2) + "\n")
print("sealed:", path)
PY
python3 tools/run_task.py run TASK-0003 submissions/TASK-0003.json; echo "exit=$?"
echo "== 6. move failed draft out of submissions/, then verify-ci"
mv submissions/TASK-0002.json runs/TASK-0002/working.json
python3 tools/run_task.py check-package; python3 tools/run_task.py verify-ci; echo "exit=$?"
echo "== 7. bad file name in submissions/"
cp submissions/TASK-0003.json submissions/BCREQ-123.json
python3 tools/run_task.py verify-ci; echo "exit=$?"; rm submissions/BCREQ-123.json
echo "== 8. ID rules"; python3 tools/run_task.py run BCREQ-123 submissions/TASK-0003.json; echo "exit=$?"
echo "== 9. trace of TASK-0002"; python3 -c "
import json
for l in open('runs/TASK-0002/trace.jsonl',encoding='utf-8'):
    d=json.loads(l); print(d['node'],d['state'],d['exit_code'],d['detail'])"
ls runs/TASK-0003
