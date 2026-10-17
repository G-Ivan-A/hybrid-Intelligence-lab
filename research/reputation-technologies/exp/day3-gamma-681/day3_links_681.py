#!/usr/bin/env python3
"""List repository links into the Day 3 files of #681 whose anchor no longer resolves."""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/reputation-technologies/exp/day2-gamma-679"))
from importlib import import_module
anchors = import_module("check-day2-679").anchors
BLOB = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
TARGETS = [f"research/reputation-technologies/2026-11-02-day3-{n}.md" for n in
           ("lecturer-script", "presentation-gamma", "slide-standard-and-gate", "rationale-and-method")]
files = subprocess.run(["git", "ls-files", "*.md"], cwd=ROOT, capture_output=True, text=True).stdout.split()
cache = {}
bad = 0
for f in files:
    text = (ROOT / f).read_text(encoding="utf-8", errors="replace")
    for target in TARGETS:
        for anchor in re.findall(re.escape(BLOB + target) + r"#([^)\s>\"]+)", text):
            if target not in cache:
                path = ROOT / target
                cache[target] = anchors(path.read_text(encoding="utf-8")) if path.is_file() else set()
            if anchor not in cache[target]:
                bad += 1
                print(f"{f}: {target}#{anchor}")
print("broken:", bad)
