#!/usr/bin/env python3
"""Print the first error each self-test mutation of check-day3-681.py raises, to see that it is rejected for the intended reason."""
import importlib.util
import re
from pathlib import Path

PATH = Path(__file__).resolve().parent / "check-day3-681.py"
spec = importlib.util.spec_from_file_location("check", PATH)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
texts = {path: path.read_text(encoding="utf-8") for path in check.FILES}
original, captured = check.validate, []
check.validate = lambda mutated: (captured.append(original(mutated)) or captured[-1])
names = re.findall(r'^        "([^"]+)": mutate', PATH.read_text(encoding="utf-8"), re.M)
check.self_test(texts)
for name, errors in zip(names, captured):
    print(f"{name} -> {errors[0][:150] if errors else 'NOT REJECTED'}")
