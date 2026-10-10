#!/usr/bin/env python3
"""Check that absolute repo links with #anchors point to existing headings (GitHub slug rules)."""
import re, sys, pathlib
ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
PREFIX = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
def slug(h):
    h = h.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")
def anchors(path):
    out, in_code = set(), False
    for line in path.read_text().splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if not in_code and re.match(r"^#{1,6} ", line):
            out.add(slug(re.sub(r"^#+ ", "", line)))
    return out
bad = 0
for f in sys.argv[2:]:
    text = pathlib.Path(f).read_text()
    for m in re.finditer(r"\]\((" + re.escape(PREFIX) + r"[^)#]+)(#[^)]*)?\)", text):
        target = ROOT / m.group(1)[len(PREFIX):]
        if not target.exists():
            print(f"{f}: missing file {target}"); bad += 1; continue
        if m.group(2) and m.group(2)[1:] not in anchors(target):
            print(f"{f}: missing anchor {m.group(2)} in {target.name}"); bad += 1
print("bad:", bad); sys.exit(1 if bad else 0)
