#!/usr/bin/env python3
"""Replay the Hub's course self-checks against the spoke's copies (issue #721).

Question: if the Hub drops its 19 course CI steps, does it lose a guard that
still protects the course's *current* text, which now lives in the spoke?
Each check is run twice, in two detached git worktrees of the Hub at HEAD:

  hub    — the Hub domain as it is at HEAD (baseline; must pass like CI does);
  spoke  — the same tree, but every file moved to the spoke (inventory column
           `moved_to`) is replaced by the spoke's version of that file.

A check that passes on `hub` and fails on `spoke` guards text the spoke has
changed (by design: the spoke drops self-check sections on import, spoke
ADR-001 point 5). A check that passes on both still holds for the spoke copy.

Only Hub check scripts (trusted, tracked in this repository) are executed. Spoke
files are copied as data and never executed. Every check runs `python3 -I`
with a 120 s timeout and a 512 MiB address-space limit.

Usage:
  python3 -I spoke-guard-replay.py <hub-root> <spoke-root> <inventory.tsv> [--keep]
"""
from __future__ import annotations

import csv
import re
import resource
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DOMAIN = "research/reputation-technologies"
STEP_RE = re.compile(r"\n      - name: ")
SCRIPT_RE = re.compile(r"python3 (?:-I )?(research/reputation-technologies/\S+\.py)([^\n]*)")


def limit() -> None:
    resource.setrlimit(resource.RLIMIT_AS, (512 << 20, 512 << 20))


def course_steps(workflow: Path) -> list[tuple[str, list[str]]]:
    steps = []
    for block in STEP_RE.split(workflow.read_text(encoding="utf-8"))[1:]:
        name = block.split("\n", 1)[0].strip()
        commands = [m.group(1) + m.group(2) for m in SCRIPT_RE.finditer(block)]
        if commands:
            steps.append((name, commands))
    return steps


def build_tree(hub: Path, tmp: Path) -> Path:
    """Detached worktree at HEAD: the checks read files outside the domain and
    the Hub's git history (e.g. #689 reads a file at a past commit)."""
    subprocess.run(["git", "-C", str(hub), "worktree", "add", "-q", "--detach", str(tmp), "HEAD"],
                   check=True)
    return tmp


def overlay_spoke(root: Path, spoke: Path, inventory: Path) -> list[str]:
    replaced = []
    with inventory.open(encoding="utf-8") as source:
        for row in csv.DictReader(source, delimiter="\t"):
            unit, moved = row["unit"], row["moved_to"]
            if moved == "-" or unit.endswith("/"):
                continue  # containers are evidence, the spoke keeps one derived file
            src = spoke / moved
            if src.is_file():
                shutil.copyfile(src, root / DOMAIN / unit)
                replaced.append(unit)
    return replaced


def run(root: Path, command: str) -> tuple[int, str]:
    script, *args = command.split()
    proc = subprocess.run(
        [sys.executable, "-I", script, *args],
        cwd=root, capture_output=True, text=True, timeout=120, preexec_fn=limit,
    )
    tail = (proc.stdout + proc.stderr).strip().splitlines()
    return proc.returncode, tail[-1][:160] if tail else ""


def main() -> int:
    hub, spoke, inventory = (Path(a).resolve() for a in sys.argv[1:4])
    keep = "--keep" in sys.argv[4:]
    steps = course_steps(hub / ".github/workflows/validate.yml")
    tmp = Path(tempfile.mkdtemp(prefix="gra-replay-"))
    try:
        hub_root = build_tree(hub, tmp / "hub")
        spoke_root = build_tree(hub, tmp / "spoke")
        replaced = overlay_spoke(spoke_root, spoke, inventory)
        print(f"course steps: {len(steps)}; files replaced by spoke copies: {len(replaced)}")
        counts = {"both-pass": 0, "spoke-fails": 0, "hub-fails": 0}
        print("step | hub | spoke | last line on spoke")
        for name, commands in steps:
            hub_rc = max(run(hub_root, c)[0] for c in commands)
            spoke_results = [run(spoke_root, c) for c in commands]
            spoke_rc = max(rc for rc, _ in spoke_results)
            note = next((line for rc, line in spoke_results if rc), "")
            if hub_rc:
                counts["hub-fails"] += 1
            elif spoke_rc:
                counts["spoke-fails"] += 1
            else:
                counts["both-pass"] += 1
            print(f"{name[:72]} | {'ok' if not hub_rc else 'FAIL'} | "
                  f"{'ok' if not spoke_rc else 'FAIL'} | {note}")
        print("summary: " + ", ".join(f"{k} {v}" for k, v in counts.items()))
    finally:
        if keep:
            print(f"kept: {tmp}", file=sys.stderr)
        else:
            for tree in (tmp / "hub", tmp / "spoke"):
                subprocess.run(["git", "-C", str(hub), "worktree", "remove", "--force", str(tree)],
                               check=False)
            shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
