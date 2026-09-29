#!/usr/bin/env python3
"""Experiment for issue #638: walk RG-BCREQ-v1 from entry to exit with the runner.

Checks the operator commands that docs/guides/06-working-with-gigacode.md and
05-commands-reference.md describe: every artifact lives in runs/<TASK>/evidence/,
every G-human node gets a checkpoint and a typed APPROVE line, and the Working is
sealed with the PowerShell block from 05-commands-reference.md before
validate-working, compile, validate-release and the n12/n13 transitions. Ported to
Windows 10/11 for issue #647: set GUIDE_SHELL to powershell or pwsh; Windows also
needs pywinpty. Requires PyYAML and jsonschema (pip install -r requirements.txt).
"""
import json, pathlib, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent / "dist/execution-package-gigacode-cli"
FIXTURE = HERE.parent / "tests/execution-package/fixtures/working-valid.json"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "tests/execution-package/tests"))
from issue_638_gigacode_smoke_flow_data import a_in  # noqa: E402
from test_guides import (GuideShell, environment, guide_shell, interactive,  # noqa: E402
                         powershell_blocks)

shell = guide_shell()
if not shell:
    sys.exit("no PowerShell: set GUIDE_SHELL or install powershell/pwsh")
root = pathlib.Path(tempfile.mkdtemp(prefix="gc-638-route-"))
work = root / "Иван Петров" / "bcreq-pilot" / "runtime"
shutil.copytree(SRC, work)
console = GuideShell(shell, root, environment())

TASK = "TASK-0002"
EV = f"runs/{TASK}/evidence"
SEAL = next(block for block in powershell_blocks(SRC / "docs/guides/05-commands-reference.md")
            if block.startswith("@'") and f"| python - {EV}/working.json" in block)


def shown(command: list[str]) -> str:
    return " ".join(["python", *command[1:]])


def show(title: str, command: list[str]) -> int:
    print(f"== {title}\n$ {shown(command)}")
    result = subprocess.run(command, cwd=work, capture_output=True, encoding="utf-8",
                            env=environment(), stdin=subprocess.DEVNULL)
    return report(result.returncode, result.stdout + result.stderr)


def report(code: int, output: str) -> int:
    print(output.replace("\r\n", "\n").strip().replace(str(root), "<tmp>"))
    print(f"exit={code}\n")
    return code


def runner(title: str, *args: str, checkpoint: str | None = None) -> int:
    command = [sys.executable, "tools/run-task.py", *args]
    if checkpoint is None:
        return show(title, command)
    command += ["--checkpoint", checkpoint]
    print(f"== {title}\n$ {shown(command)}")
    return report(*interactive(command, work, environment()))


def write(name: str, value) -> str:
    path = work / EV / name
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")
    return f"{EV}/{name}"


def checkpoint(node: str) -> str:
    return write(f"checkpoint-{node}.md", f"# Human checkpoint {node}\n\nРешение человека: одобрено.\n")


assert runner("start", "start", TASK) == 0
(work / EV).mkdir()
confirmed = a_in(TASK, True)
core = {"artifact_class": "A-CORE", "state": "validated", "task_id": TASK,
        "products": confirmed["products"], "product_attribution": confirmed["product_attribution"],
        "entities": [], "actors": [], "constraints": [], "metrics": [], "ambiguities": [],
        "statements": [{"id": "ST-01", "text": "Синхронизация контактов", "slot": "S-FR",
                        "atomic": True, "source_ref": {"source_id": "SRC-01",
                                                       "locator": "smoke", "quote": "smoke"}}]}
steps = [
    ("n0", write("A-IN.json", a_in(TASK, False)), None),
    ("n1", write("A-IN-confirmed.json", confirmed), checkpoint("n0")),
    ("n2", write("normalized-text.md", "Нормализованный текст\n"), None),
    ("n3", write("marked-elements.md", "Размеченные элементы\n"), None),
    ("n4", write("ambiguities.md", "Неоднозначности\n"), None),
    ("n9", write("A-CORE.json", core), checkpoint("n4")),
    ("n10", write("problem-statement.md", "Проблема\n"), None),
    ("n10a", write("value-hypothesis.md", "Гипотеза ценности\n"), None),
    ("n11", write("preflight.json", {"preflight_registers": {"valid": True}}), checkpoint("n10a")),
    ("n12", write("bcreq-items.md", "Элементы BCREQ\n"), None),
]
for target, artifact, human in steps:
    assert runner(f"advance -> {target}", "advance", TASK, "--to", target,
                  "--artifact", artifact, checkpoint=human) == 0, target

shutil.copy(FIXTURE, work / EV / "working.json")
pipe = [sys.executable, "tools/bcreq_pipeline.py"]
show("validate-working before sealing", pipe + ["validate-working", f"{EV}/working.json"])
print(f"== seal Working (PowerShell block from 05)\nPS> {SEAL.splitlines()[-1]}")
assert report(*console.run(work, SEAL)) == 0
assert show("validate-working after sealing", pipe + ["validate-working", f"{EV}/working.json"]) == 0
assert runner("advance n12 -> n13", "advance", TASK, "--to", "n13",
              "--artifact", f"{EV}/working.json", checkpoint=checkpoint("n12")) == 0
release = f"runs/{TASK}/release"
assert show("compile", pipe + ["compile", f"{EV}/working.json", "--output", release]) == 0
assert show("validate-release", pipe + ["validate-release", f"{EV}/working.json",
                                        "--release", f"{release}/release.json",
                                        "--manifest", f"{release}/release-manifest.json"]) == 0
assert runner("advance n13 -> exit", "advance", TASK, "--to", "exit",
              "--artifact", f"{release}/release.json", "--working", f"{EV}/working.json",
              "--manifest", f"{release}/release-manifest.json", checkpoint=checkpoint("n13")) == 0
runner("metrics", "metrics", TASK)
runner("advance after exit", "advance", TASK, "--to", "n0", "--artifact", f"{EV}/A-IN.json")
show("gate after full route", [sys.executable, "tools/validate-package.py", "."])
print("== runs tree:", sorted(p.relative_to(work).as_posix() for p in (work / "runs").rglob("*")
                             if p.is_file()))
shutil.rmtree(root)
