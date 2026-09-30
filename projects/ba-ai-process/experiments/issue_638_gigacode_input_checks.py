#!/usr/bin/env python3
"""Experiment for issue #638: G-mach messages the GigaCode guides quote.

Checks, on a temp copy of the package: evidence files under runs/<TASK_ID>/
keep the gate green; a stray file in the package root breaks it; the
`--input` check of a confirmed A-IN (correct and wrong binding_digest); the
one-line digest command from docs/guides/05-commands-reference.md.
Runs the documented `python` commands, so it works unchanged on Windows 10/11
(issue #647). Requires PyYAML and jsonschema (pip install -r requirements.txt).
"""
import json, pathlib, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "tests/execution-package/tests"))
from issue_638_gigacode_smoke_flow_data import a_in  # noqa: E402
from test_guides import environment  # noqa: E402
# A redirected Windows console uses the ANSI code page, which has no Cyrillic;
# the log of this experiment is UTF-8 like every file of the package.
sys.stdout.reconfigure(encoding="utf-8")

SRC = pathlib.Path(__file__).resolve().parents[1] / "dist/execution-package-gigacode-cli"
work = pathlib.Path(tempfile.mkdtemp(prefix="gc-638-in-")) / "runtime"
shutil.copytree(SRC, work)
DIGEST = ("import json,hashlib,sys; p=json.load(open(sys.argv[1],encoding='utf-8-sig'))['products']; "
          "print('sha256:'+hashlib.sha256(json.dumps(p,ensure_ascii=False,sort_keys=True,"
          "separators=(',',':')).encode('utf-8')).hexdigest())")


codes = []


def sh(title: str, *command: str) -> None:
    result = subprocess.run([sys.executable, *command], cwd=work, capture_output=True,
                            encoding="utf-8", env=environment())
    shown = " ".join(["python", *(c if len(c) < 60 else "<digest one-liner>" for c in command)])
    output = (result.stdout + result.stderr).strip().replace(str(work.parent), "<tmp>")
    print(f"== {title}\n$ {shown}\n{output}\nexit={result.returncode}\n")
    codes.append(result.returncode)


sh("start", "tools/run-task.py", "start", "TASK-0001")
evidence = work / "runs/TASK-0001/evidence"
evidence.mkdir()
(evidence / "A-IN.json").write_text(json.dumps(a_in("TASK-0001", False), ensure_ascii=False, indent=2), encoding="utf-8")
confirmed = a_in("TASK-0001", True)
(evidence / "A-IN-confirmed.json").write_text(json.dumps(confirmed, ensure_ascii=False, indent=2), encoding="utf-8")
sh("gate with evidence under runs/", "tools/validate-package.py")
sh("digest one-liner", "-c", DIGEST, "runs/TASK-0001/evidence/A-IN-confirmed.json")
sh("check confirmed A-IN", "tools/validate-package.py", "--input", "runs/TASK-0001/evidence/A-IN-confirmed.json")
confirmed["product_attribution"]["binding_digest"] = "sha256:" + "0" * 64
(evidence / "A-IN-bad.json").write_text(json.dumps(confirmed), encoding="utf-8")
sh("check A-IN with wrong digest", "tools/validate-package.py", "--input", "runs/TASK-0001/evidence/A-IN-bad.json")
sh("check pending A-IN", "tools/validate-package.py", "--input", "runs/TASK-0001/evidence/A-IN.json")
(work / "A-IN.json").write_text("{}", encoding="utf-8")
sh("gate with stray file in package root", "tools/validate-package.py")
sh("start with stray file", "tools/run-task.py", "start", "TASK-0002")
# The guides promise: evidence keeps the gate green, bad inputs and stray files are refused.
sys.exit(0 if [code != 0 for code in codes] == [False] * 4 + [True] * 4 else f"unexpected exit codes: {codes}")
