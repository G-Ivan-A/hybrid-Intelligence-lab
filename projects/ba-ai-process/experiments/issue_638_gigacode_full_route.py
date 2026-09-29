#!/usr/bin/env python3
"""Experiment for issue #638: walk RG-BCREQ-v1 from entry to exit with the runner.

Checks the operator commands that docs/guides/06-working-with-gigacode.md and
05-commands-reference.md describe: every artifact lives in runs/<TASK>/evidence/,
every G-human node gets a checkpoint and a typed APPROVE line, and the Working is
sealed with the POSIX heredoc from the guide before validate-working, compile,
validate-release and the n12/n13 transitions. Requires PyYAML and jsonschema
(pip install -r requirements.txt) and python3 on PATH for the sealing snippet.
"""
import hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent / "dist/execution-package-gigacode-cli"
FIXTURE = HERE.parent / "tests/execution-package/fixtures/working-valid.json"
work = pathlib.Path(tempfile.mkdtemp(prefix="gc-638-route-")) / "runtime"
shutil.copytree(SRC, work)
sys.path.insert(0, str(HERE))
from issue_638_gigacode_smoke_flow_data import a_in  # noqa: E402

TASK = "TASK-0002"
EV = pathlib.Path("runs") / TASK / "evidence"
SEAL = f"""python3 - {EV}/working.json <<'EOF'
import hashlib, json, sys
sys.path.insert(0, "tools")
import bcreq_pipeline
path = sys.argv[1]
working = json.load(open(path, encoding="utf-8"))
for item in working.get("evidence", []):
    item["checksum"] = "sha256:" + hashlib.sha256(item["excerpt"].encode("utf-8")).hexdigest()
working["working_digest"] = bcreq_pipeline.working_digest(working)
open(path, "w", encoding="utf-8").write(json.dumps(working, ensure_ascii=False, indent=2) + "\\n")
print("sealed:", path)
EOF
"""


def show(title: str, command: list[str] | str, stdin=subprocess.DEVNULL, shell=False) -> int:
    shown = command if isinstance(command, str) else " ".join(command)
    print(f"== {title}\n$ {shown.splitlines()[0]}")
    result = subprocess.run(command, cwd=work, text=True, capture_output=True,
                            stdin=stdin, shell=shell)
    print((result.stdout + result.stderr).strip().replace(str(work.parent), "<tmp>"))
    print(f"exit={result.returncode}\n")
    return result.returncode


def runner(title: str, *args: str, checkpoint: str | None = None) -> int:
    command = [sys.executable, "tools/run-task.py", *args]
    if checkpoint is None:
        return show(title, command)
    command += ["--checkpoint", checkpoint]
    source = json.loads((work / "runs" / TASK / "state.json").read_text())["current"]
    digest = hashlib.sha256((work / checkpoint).read_bytes()).hexdigest()
    master, slave = os.openpty()
    os.write(master, f"APPROVE {TASK}:{source} sha256:{digest}\n".encode())
    try:
        return show(title, command, stdin=slave)
    finally:
        os.close(slave); os.close(master)


def write(name: str, value) -> str:
    path = work / EV / name
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")
    return str(EV / name)


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
assert show("seal Working (sh heredoc)", ["sh", "-c", SEAL]) == 0
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
print("== runs tree:", sorted(str(p.relative_to(work)) for p in (work / "runs").rglob("*") if p.is_file()))
