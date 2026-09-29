#!/usr/bin/env python3
"""Experiment for issue #638: capture real GigaCode CLI package runner output.

Copies the compiled package to a temp dir and walks the operator steps that the
docs/guides cluster describes: gate, start, entry -> n0, n0 -> n1 (with and
without checkpoint, non-interactive and interactive approval), metrics and
typical refusals. The approval is typed into a real terminal (pywinpty on
Windows, issue #647). Requires PyYAML and jsonschema (pip install -r requirements.txt).
"""
import hashlib, json, pathlib, shutil, subprocess, sys, tempfile

SRC = pathlib.Path(__file__).resolve().parents[1] / "dist/execution-package-gigacode-cli"
work = pathlib.Path(tempfile.mkdtemp(prefix="gc-638-")) / "runtime"
shutil.copytree(SRC, work)
inputs = work.parent / "inputs"
inputs.mkdir()
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "tests/execution-package/tests"))
from issue_638_gigacode_smoke_flow_data import a_in  # noqa: E402
from test_guides import environment, interactive  # noqa: E402
# A redirected Windows console uses the ANSI code page, which has no Cyrillic;
# the log of this experiment is UTF-8 like every file of the package.
sys.stdout.reconfigure(encoding="utf-8")


codes = []


def run(title: str, *args: str, approval: str | None = None) -> None:
    command = [sys.executable, "tools/run-task.py", *args]
    print(f"== {title}\nPS> python tools/run-task.py {' '.join(args)}".replace(str(work.parent), "<tmp>"))
    if approval is None:
        result = subprocess.run(command, cwd=work, capture_output=True, encoding="utf-8",
                                env=environment(), stdin=subprocess.DEVNULL)
        code, output = result.returncode, result.stdout + result.stderr
    else:
        code, output = interactive(command, work, environment())
        assert approval in output, f"runner asked for another approval line:\n{output}"
    print(output.replace("\r\n", "\n").strip().replace(str(work.parent), "<tmp>"))
    print(f"exit={code}\n")
    codes.append(code)


gate = subprocess.run([sys.executable, "tools/validate-package.py", "."], cwd=work,
                      capture_output=True, encoding="utf-8", env=environment())
print(f"== gate\n{(gate.stdout + gate.stderr).strip()}\nexit={gate.returncode}\n")

for task in ("TASK-0001", "TASK-0002"):
    (inputs / f"{task}-A-IN.json").write_text(json.dumps(a_in(task, False)), encoding="utf-8")
    (inputs / f"{task}-A-IN-confirmed.json").write_text(json.dumps(a_in(task, True)), encoding="utf-8")
checkpoint = inputs / "checkpoint-n0.md"
checkpoint.write_text("Цепочка platform → platform-integration → crm-connectors → "
                      "crm-bidirectional-sync подтверждена.\n", encoding="utf-8")
approval = f"APPROVE TASK-0001:n0 sha256:{hashlib.sha256(checkpoint.read_bytes()).hexdigest()}"

run("start", "start", "TASK-0001")
run("metrics before steps", "metrics", "TASK-0001")
run("start again", "start", "TASK-0001")
run("bad id", "start", "task-1")
run("entry -> n0", "advance", "TASK-0001", "--to", "n0", "--artifact", str(inputs / "TASK-0001-A-IN.json"))
run("n0 -> n1 without checkpoint", "advance", "TASK-0001", "--to", "n1",
    "--artifact", str(inputs / "TASK-0001-A-IN-confirmed.json"))
print("== state after refusal:", json.loads((work / "runs/TASK-0001/state.json").read_text(encoding="utf-8"))["status"], "\n")

run("start second task", "start", "TASK-0002")
run("second: entry -> n0", "advance", "TASK-0002", "--to", "n0", "--artifact", str(inputs / "TASK-0002-A-IN.json"))
run("second: wrong edge n0 -> n2", "advance", "TASK-0002", "--to", "n2",
    "--artifact", str(inputs / "TASK-0002-A-IN-confirmed.json"))

run("start third task", "start", "TASK-0003")
(inputs / "TASK-0003-A-IN.json").write_text(json.dumps(a_in("TASK-0003", False)), encoding="utf-8")
(inputs / "TASK-0003-A-IN-confirmed.json").write_text(json.dumps(a_in("TASK-0003", True)), encoding="utf-8")
run("third: entry -> n0", "advance", "TASK-0003", "--to", "n0", "--artifact", str(inputs / "TASK-0003-A-IN.json"))
run("third: n0 -> n1 non-interactive", "advance", "TASK-0003", "--to", "n1",
    "--artifact", str(inputs / "TASK-0003-A-IN-confirmed.json"), "--checkpoint", str(checkpoint))

run("start fourth task", "start", "TASK-0004")
(inputs / "TASK-0004-A-IN.json").write_text(json.dumps(a_in("TASK-0004", False)), encoding="utf-8")
(inputs / "TASK-0004-A-IN-confirmed.json").write_text(json.dumps(a_in("TASK-0004", True)), encoding="utf-8")
approval4 = approval.replace("TASK-0001", "TASK-0004")
run("fourth: entry -> n0", "advance", "TASK-0004", "--to", "n0", "--artifact", str(inputs / "TASK-0004-A-IN.json"))
run("fourth: n0 -> n1 interactive approval", "advance", "TASK-0004", "--to", "n1",
    "--artifact", str(inputs / "TASK-0004-A-IN-confirmed.json"), "--checkpoint", str(checkpoint),
    approval=approval4)
run("fourth: metrics", "metrics", "TASK-0004")
print("== trace row keys:", sorted(json.loads((work / "runs/TASK-0004/trace.jsonl")
                                              .read_text(encoding="utf-8").splitlines()[-1])))
print("== runs/:", sorted(p.name for p in (work / "runs").iterdir()))
# Refusals the guides document: repeated start, bad id, missing checkpoint, wrong edge, no console.
refused = [1 if code else 0 for code in codes]
sys.exit(0 if gate.returncode == 0 and refused == [0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
         else f"unexpected exit codes: gate {gate.returncode}, runner {codes}")
