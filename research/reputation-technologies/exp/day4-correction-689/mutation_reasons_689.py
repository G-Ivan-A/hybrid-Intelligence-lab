#!/usr/bin/env python3
"""Print the first error each self-test mutation of check-day4-689.py triggers: shows every mutation is rejected for its own reason.

Pass --no-dialog to mask the dialog file while it is still in the tree, before the final commit deletes it."""
import importlib.util
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("check", Path(__file__).with_name("check-day4-689.py"))
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
texts = {path: path.read_text(encoding="utf-8") if path.is_file() else "" for path in check.FILES + (check.DIALOG,)}
if "--no-dialog" in sys.argv:
    texts[check.DIALOG] = ""
base = check.validate(texts)
if base:
    raise SystemExit("\n".join(f"FAIL: {error}" for error in base))
real_validate = check.validate
reasons = {}


def first_error(mutated):
    errors = real_validate(mutated)
    reasons[len(reasons)] = errors[0] if errors else "NOT REJECTED"
    return errors


check.validate = lambda mutated: first_error(mutated) if mutated != texts else (reasons.__setitem__(len(reasons), "(no change)") or [])
failed, fixtures = check.self_test(texts)
source = Path(check.__file__).read_text(encoding="utf-8")
names = [line.split('": ', 1)[0].strip().strip('"') for line in source.split("    broken = {", 1)[1].split("\n    }\n", 1)[0].splitlines()
         if line.startswith('        "')]
for name, reason in zip(names, reasons.values()):
    print(f"{name}: {reason}")
raise SystemExit(1 if failed else 0)
