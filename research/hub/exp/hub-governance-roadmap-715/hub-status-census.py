#!/usr/bin/env python3
"""Frontmatter status census of Hub markdown by top-level area (issue #715).
Prints count of files per (area, status) and lists draft/proposed files older than a cutoff."""
import os, re, sys, collections, subprocess
cutoff = sys.argv[1] if len(sys.argv) > 1 else "2026-09-01"
areas = collections.defaultdict(collections.Counter)
old_open = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in (".git", "experiments", "node_modules")]
    for f in files:
        if not f.endswith(".md"):
            continue
        p = os.path.join(root, f)[2:]
        parts = p.split("/")
        area = "/".join(parts[:2]) if parts[0] in ("docs", "research", "projects") and len(parts) > 2 else parts[0] if len(parts) > 1 else "(root)"
        txt = open(p, encoding="utf-8", errors="replace").read(1500)
        m = re.match(r"---\n(.*?)\n---", txt, re.S)
        st = "none"; upd = ""
        if m:
            s = re.search(r"^status:\s*(\S+)", m.group(1), re.M); st = s.group(1).strip('"') if s else "none"
            u = re.search(r"^updated:\s*(\S+)", m.group(1), re.M); upd = u.group(1).strip('"') if u else ""
        areas[area][st] += 1
        if st in ("draft", "proposed", "review", "reviewed") and upd and upd < cutoff and "/exp/" not in p:
            old_open.append((upd, st, p, area))
for a in sorted(areas):
    print(f"{a:45} {sum(areas[a].values()):4}  {dict(areas[a])}")
print(f"\nopen-status (draft/proposed/review) docs not updated since {cutoff}, excluding exp/: {len(old_open)}")
for a, n in collections.Counter(x[3] for x in old_open).most_common():
    print(f"  {n:4}  {a}")
if "--list" in sys.argv:
    for x in sorted(old_open):
        print(*x[:3])
