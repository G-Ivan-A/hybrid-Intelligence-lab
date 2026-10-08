#!/usr/bin/env python3
"""Analyst-started actions for OpenCode slash commands; the output is shown to the model."""

from __future__ import annotations

import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "run_task.py"
# OpenCode settings that switch off or replace the package protections (`opencode --pure` sets OPENCODE_PURE).
OVERRIDES = ("OPENCODE_PURE", "OPENCODE_DISABLE_PROJECT_CONFIG", "OPENCODE_PERMISSION",
             "OPENCODE_CONFIG_CONTENT", "OPENCODE_DISABLE_DEFAULT_PLUGINS")


def runner(*arguments: str) -> int:
    result = subprocess.run([sys.executable, str(RUNNER), *arguments], cwd=ROOT, text=True,
                            encoding="utf-8", errors="replace",
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    print(f"$ python tools/run_task.py {' '.join(arguments)}")
    print(result.stdout.rstrip() or "(no output)")
    print(f"exit code: {result.returncode}")
    return result.returncode


def check() -> int:
    found = [name for name in OVERRIDES if os.environ.get(name)]
    if found:
        print(f"ERROR: OpenCode protection overrides are set: {', '.join(found)}")
        print("exit code: 1")
        return 1
    return runner("check-package")


def gate(raw: str) -> int:
    # cmd.exe keeps the quotes that PowerShell and Git Bash remove from '$1'.
    task_id = raw.strip().strip("'\"")
    if not re.fullmatch(r"TASK-[0-9]{4,}", task_id):
        print(f"ERROR: task ID must match TASK-0001, got {raw!r}")
        print("exit code: 1")
        return 1
    candidate = f"submissions/{task_id}.json"
    if runner("seal", candidate) != 0:
        return 1
    return runner("run", task_id, candidate)


def main(argv: list[str]) -> int:
    # The runner writes UTF-8; a Windows console code page must not break the output for OpenCode.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(argv) == 1 and argv[0] == "check":
        return check()
    if len(argv) == 1 and argv[0] == "verify":
        return runner("verify-ci")
    if len(argv) == 2 and argv[0] == "gate":
        return gate(argv[1])
    print("usage: opencode_command.py check | verify | gate TASK-ID")
    print("exit code: 2")
    return 2


if __name__ == "__main__":
    main(sys.argv[1:])
    # OpenCode on Windows drops the output of a !`...` block that exits with 1 (cross-spawn reports
    # ENOENT); the result is the printed `exit code:` line.
    raise SystemExit(0)
