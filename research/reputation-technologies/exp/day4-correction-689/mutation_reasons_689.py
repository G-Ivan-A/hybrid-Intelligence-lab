#!/usr/bin/env python3
"""Print the first error each self-test mutation of check-day4-689.py triggers: shows every mutation is rejected for its own reason."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("check", Path(__file__).with_name("check-day4-689.py"))
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
texts = {path: path.read_text(encoding="utf-8") for path in check.FILES}
source = Path(check.__file__).read_text(encoding="utf-8")
broken_src = source.split("    broken = {", 1)[1].split("\n    }\n", 1)[0]
a, v, r, V1 = check.ANALYSIS, check.V2, check.RFC, check.V1
mutate, mutate_re = check.mutate, check.mutate_re
SLIDE_17, DECK = check.SLIDE_17, check.DECK
broken = eval("{" + broken_src + "}")
for name, mutated in broken.items():
    errors = check.validate(mutated) if mutated != texts else ["(no change)"]
    print(f"{name}: {errors[0] if errors else 'NOT REJECTED'}")
