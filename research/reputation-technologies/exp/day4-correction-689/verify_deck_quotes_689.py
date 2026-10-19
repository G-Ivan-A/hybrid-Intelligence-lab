#!/usr/bin/env python3
"""Check that every swap row of the RFC quotes its «Было» verbatim from the linked line at commit 16415e9, and report how much each swap changes the length of the text: a longer line may not fit the Gamma card it sits in.

Run from any directory; git history must include commit 16415e9."""
import importlib.util
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location("check", Path(__file__).with_name("check-day4-689.py"))
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
text = check.RFC.read_text(encoding="utf-8")
LIMIT = 1.3  # a swap more than 30 % longer than the old text is flagged for a look in Gamma
errors, longer = 0, []
for match in check.ROW.finditer(text):
    row = check.cells(match[0])
    swap = next((i for i, cell in enumerate(row[:-1]) if check.SWAP_CELL.match(cell)), None)
    if swap is None:
        continue
    link = check.PERMALINK.match(row[swap])
    old, new = check.SWAP_CELL.match(row[swap])[1], row[swap + 1]
    lines = check.source_lines(link[3])
    found = lines is not None and check.in_line(old, lines[int(link[4]) - 1])
    errors += not found
    if len(new) > LIMIT * len(old):
        longer.append(row[0])
    print(f"{'PASS' if found else 'FAIL'}: {row[0]} {link[1]}:{link[2]}: {len(old)} → {len(new)} characters ({len(new) - len(old):+d})")
print(f"{'PASS' if not errors else 'FAIL'}: {errors} swaps not found verbatim; {len(longer)} swaps are more than {round((LIMIT - 1) * 100)} % longer: {', '.join(longer) or 'none'}")
raise SystemExit(1 if errors else 0)
