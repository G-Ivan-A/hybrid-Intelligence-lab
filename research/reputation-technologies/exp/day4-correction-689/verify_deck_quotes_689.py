#!/usr/bin/env python3
"""Check that every «Было» cell of the RFC swap tables is verbatim [SLIDE_TEXT] of its slide in the #688 deck at commit 9d1fc9f, and report how the line length changes.

The deck is not in main yet, so this check is not part of CI: it reads the deck from git (`git fetch origin pull/688/head` first) or from a file passed as an argument."""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("check", Path(__file__).with_name("check-day4-689.py"))
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
COMMIT = "9d1fc9f0dc17924f04abb5c53260edcc97e897f9"
PATH = "research/reputation-technologies/2026-11-03-day4-presentation-gamma.md"
if len(sys.argv) > 1:
    deck = Path(sys.argv[1]).read_text(encoding="utf-8")
else:
    deck = subprocess.run(["git", "-C", str(check.ROOT), "show", f"{COMMIT}:{PATH}"], capture_output=True, text=True, check=True).stdout
slides = {int(m[1]): m[2] for m in re.finditer(r"^### Слайд (\d+)\..*?\n\*\*\[SLIDE_TEXT\]\*\*\n(.*?)\n\*\*\[IMAGE_PROMPT\]\*\*", deck, re.M | re.S)}
text = check.RFC.read_text(encoding="utf-8")
errors = 0
for swap, slide, old, new in check.SWAP_ROW.findall(text):
    old, new = old.replace("**", "").strip(), new.replace("**", "").strip()
    body = slides.get(int(slide), "")
    parts = [part.strip(" :") for part in old.split("…") if part.strip(" :")]
    found = bool(parts) and all(part in body for part in parts)
    errors += not found
    print(f"{'PASS' if found else 'FAIL'}: {swap} slide {slide}: {len(old)} → {len(new)} characters ({len(new) - len(old):+d})")
print(f"{'PASS' if not errors else 'FAIL'}: {len(slides)} deck slides read, {errors} swaps not found verbatim")
raise SystemExit(1 if errors else 0)
