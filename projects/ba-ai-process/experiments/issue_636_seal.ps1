# Experiment for issue #636: PowerShell form of the guide commands
# (sealing via here-string piped to "python -", moving a failed draft).
# Run from the package root: pwsh -NoProfile -File <this file>
$ErrorActionPreference = 'Continue'
python -c "import json;w=json.load(open('golden/TASK-0001.json',encoding='utf-8'));w['evidence'][0]['excerpt']='Клиент должен выгружать журнал звонков.';w['evidence'][0]['locator']='https://jira.example.test/browse/BCREQ-123';json.dump(w,open('submissions/TASK-0002.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)"
python tools/run_task.py run TASK-0002 submissions/TASK-0002.json
"exit=$LASTEXITCODE"
Move-Item submissions\TASK-0002.json runs\TASK-0002\working.json
Copy-Item runs\TASK-0002\working.json submissions\TASK-0003.json
@'
import hashlib, json, sys
sys.path.insert(0, "tools")
import bcreq_pipeline
path = sys.argv[1]
working = json.load(open(path, encoding="utf-8"))
for item in working.get("evidence", []):
    item["checksum"] = "sha256:" + hashlib.sha256(item["excerpt"].encode("utf-8")).hexdigest()
working["working_digest"] = bcreq_pipeline.working_digest(working)
open(path, "w", encoding="utf-8").write(json.dumps(working, ensure_ascii=False, indent=2) + "\n")
print("sealed:", path)
'@ | python - submissions/TASK-0003.json
"exit=$LASTEXITCODE"
python tools/run_task.py run TASK-0003 submissions/TASK-0003.json
"exit=$LASTEXITCODE"
python tools/run_task.py verify-ci
"exit=$LASTEXITCODE"
python tools/run_task.py check-package
