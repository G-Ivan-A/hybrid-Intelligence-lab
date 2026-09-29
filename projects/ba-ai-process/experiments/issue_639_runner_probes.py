#!/usr/bin/env python3
"""Experiment for issue #639: what the GigaCode transition controller does and does not check.

P10 walks a temporary copy of the GigaCode package to n1 with a valid A-IN and a
human checkpoint, then offers arbitrary text as the n1, n2 and n3 artifacts.
P11 lists edge conditions that stay YAML strings and are never evaluated.
The repository is not modified. Requires PyYAML and jsonschema.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import yaml

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent / "dist/execution-package-gigacode-cli"
TESTS = HERE.parent / "tests/execution-package/tests"
sys.path.insert(0, str(TESTS))
from test_runner import input_document  # noqa: E402  (reuse the canonical fixture)


def run(package: Path, *args: str, approval: str | None = None) -> subprocess.CompletedProcess:
    command = [sys.executable, str(package / "tools/run-task.py"), *map(str, args)]
    if approval is None:
        return subprocess.run(command, cwd=package, text=True, capture_output=True)
    master, slave = os.openpty()
    try:
        os.write(master, (approval + "\n").encode())
        return subprocess.run(command, cwd=package, text=True, stdin=slave, capture_output=True)
    finally:
        os.close(slave)
        os.close(master)


def show(label: str, result: subprocess.CompletedProcess) -> None:
    text = (result.stdout + result.stderr).strip().splitlines()
    print(f"{label}: exit={result.returncode} :: {text[-1] if text else ''}")


def p10() -> None:
    print("== P10. arbitrary text as n1/n2/n3 artifacts after a confirmed n0")
    temp = Path(tempfile.mkdtemp(prefix="issue639-runner-"))
    package = temp / "package"
    shutil.copytree(PACKAGE, package)
    a_in = temp / "a-in.json"
    a_in.write_text(json.dumps(input_document(True)), encoding="utf-8")
    checkpoint = temp / "checkpoint-n0.md"
    checkpoint.write_text("BA confirmed work type, axis and MANGO chain.\n", encoding="utf-8")
    show("start", run(package, "start", "TASK-9001"))
    show("entry->n0", run(package, "advance", "TASK-9001", "--to", "n0", "--artifact", a_in))
    challenge = ("APPROVE TASK-9001:n0 sha256:"
                 + hashlib.sha256(checkpoint.read_bytes()).hexdigest())
    show("n0->n1", run(package, "advance", "TASK-9001", "--to", "n1", "--artifact", a_in,
                       "--checkpoint", checkpoint, approval=challenge))
    for source, target in (("n1", "n2"), ("n2", "n3"), ("n3", "n4")):
        junk = temp / f"{source}.txt"
        junk.write_text("lorem ipsum, not a normalized transcript\n", encoding="utf-8")
        show(f"{source}->{target} with junk", run(package, "advance", "TASK-9001", "--to", target,
                                                  "--artifact", junk))
    show("metrics", run(package, "metrics", "TASK-9001"))
    shutil.rmtree(temp)


def p11() -> None:
    print("== P11. edge conditions in routes/rg-bcreq-v1.yaml vs the runner")
    graph = yaml.safe_load((PACKAGE / "routes/rg-bcreq-v1.yaml").read_text(encoding="utf-8"))
    runner_src = (PACKAGE / "tools/run-task.py").read_text(encoding="utf-8")
    spec = importlib.util.spec_from_file_location("run_task", PACKAGE / "tools/run-task.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    evaluates = "eval(" in runner_src or "edge[\"condition\"]" in runner_src \
        or "edge.get(\"condition\")" in runner_src
    print(f"runner reads edge.condition strings: {evaluates}")
    parsed = [e for e in graph["edges"] if e.get("condition") not in (None, "gate_passed")]
    print(f"edges with a non-trivial predicate in YAML: {len(parsed)}")
    hardcoded = [s for s in ("entry", "n0", "n4", "n7", "n8", "n10a", "n12", "n13")
                 if f'"{s}"' in runner_src or f"'{s}'" in runner_src]
    print(f"sources with a hand-written branch in required_target(): {hardcoded}")
    print("n0->n1 YAML predicate:", next(e["condition"] for e in graph["edges"]
                                          if e["from"] == "n0" and e["to"] == "n1"))


if __name__ == "__main__":
    p10()
    p11()
