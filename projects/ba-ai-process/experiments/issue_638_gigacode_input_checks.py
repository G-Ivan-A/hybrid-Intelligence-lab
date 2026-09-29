#!/usr/bin/env python3
"""Experiment for issue #638: G-mach messages the GigaCode guides quote.

Checks, on a temp copy of the package: evidence files under runs/<TASK_ID>/
keep the gate green; a stray file in the package root breaks it; the
`--input` check of a confirmed A-IN (correct and wrong binding_digest); the
one-line digest command from docs/guides/05-commands-reference.md.
Requires PyYAML and jsonschema (pip install -r requirements.txt).
"""
import json, pathlib, shutil, subprocess, sys, tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from issue_638_gigacode_smoke_flow_data import a_in  # noqa: E402

SRC = pathlib.Path(__file__).resolve().parents[1] / "dist/execution-package-gigacode-cli"
work = pathlib.Path(tempfile.mkdtemp(prefix="gc-638-in-")) / "runtime"
shutil.copytree(SRC, work)
DIGEST = ("import json,hashlib,sys; p=json.load(open(sys.argv[1],encoding='utf-8'))['products']; "
          "print('sha256:'+hashlib.sha256(json.dumps(p,ensure_ascii=False,sort_keys=True,"
          "separators=(',',':')).encode('utf-8')).hexdigest())")


def sh(title: str, *command: str) -> None:
    result = subprocess.run(list(command), cwd=work, text=True, capture_output=True)
    shown = " ".join(c if len(c) < 60 else "<digest one-liner>" for c in command)
    print(f"== {title}\n$ {shown}\n{(result.stdout + result.stderr).strip()}\nexit={result.returncode}\n")


sh("start", "sh", "tools/run-task", "start", "TASK-0001")
evidence = work / "runs/TASK-0001/evidence"
evidence.mkdir()
(evidence / "A-IN.json").write_text(json.dumps(a_in("TASK-0001", False), ensure_ascii=False, indent=2), encoding="utf-8")
confirmed = a_in("TASK-0001", True)
(evidence / "A-IN-confirmed.json").write_text(json.dumps(confirmed, ensure_ascii=False, indent=2), encoding="utf-8")
sh("gate with evidence under runs/", "sh", "tools/validate-package.sh")
sh("digest one-liner", "python3", "-c", DIGEST, "runs/TASK-0001/evidence/A-IN-confirmed.json")
sh("check confirmed A-IN", "sh", "tools/validate-package.sh", "--input", "runs/TASK-0001/evidence/A-IN-confirmed.json")
confirmed["product_attribution"]["binding_digest"] = "sha256:" + "0" * 64
(evidence / "A-IN-bad.json").write_text(json.dumps(confirmed), encoding="utf-8")
sh("check A-IN with wrong digest", "sh", "tools/validate-package.sh", "--input", "runs/TASK-0001/evidence/A-IN-bad.json")
sh("check pending A-IN", "sh", "tools/validate-package.sh", "--input", "runs/TASK-0001/evidence/A-IN.json")
(work / "A-IN.json").write_text("{}", encoding="utf-8")
sh("gate with stray file in package root", "sh", "tools/validate-package.sh")
sh("start with stray file", "sh", "tools/run-task", "start", "TASK-0002")
