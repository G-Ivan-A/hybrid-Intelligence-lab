#!/usr/bin/env python3
"""Check relative links and #anchors in Cline guides (GitHub slug rules)."""
import re, sys, pathlib

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else
    pathlib.Path(__file__).resolve().parents[1] / "build/adapters/cline-vscode/docs/guides")

def slug(text):
    text = re.sub(r"`|\*|\[|\]\([^)]*\)", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")

def anchors(path):
    result, seen = set(), {}
    in_code = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"#{1,6}\s+(.*)", line)
        if m:
            s = slug(m.group(1))
            n = seen.get(s, 0)
            result.add(s if n == 0 else f"{s}-{n}")
            seen[s] = n + 1
        result.update(re.findall(r'<a id="([^"]+)"', line))
    return result

errors = 0
for md in sorted(root.glob("*.md")):
    text = md.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    for target in re.findall(r"\]\(([^)\s]+)\)", text):
        if re.match(r"https?:", target):
            continue
        file_part, _, anchor = target.partition("#")
        dest = (md.parent / file_part) if file_part else md
        if not dest.exists():
            print(f"{md.name}: missing file {target}"); errors += 1; continue
        if anchor and dest.suffix == ".md" and anchor not in anchors(dest):
            print(f"{md.name}: missing anchor {target}"); errors += 1
print("errors:", errors)
sys.exit(1 if errors else 0)
