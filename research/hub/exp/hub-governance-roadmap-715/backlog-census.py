#!/usr/bin/env python3
"""Census of ops/backlog.md rows for issue #715 RFC: status per sprint, IDs, stale signals."""
import re, sys, collections, json
path = sys.argv[1] if len(sys.argv) > 1 else "ops/backlog.md"
sprint = None
rows = []
for line in open(path, encoding="utf-8"):
    m = re.match(r"^## (.+)", line)
    if m:
        sprint = m.group(1).strip()
        continue
    if line.startswith("| **B-") or re.match(r"^\| B-\d", line):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rid = re.sub(r"[*`]", "", cells[0])
        status = re.sub(r"[*`]", "", cells[4]) if len(cells) > 4 else "?"
        rows.append({"id": rid, "sprint": sprint, "title": cells[1][:90], "prio": cells[2], "status": status, "issue": cells[5][:60] if len(cells) > 5 else ""})
by_sprint = collections.OrderedDict()
for r in rows:
    by_sprint.setdefault(r["sprint"], collections.Counter())[r["status"].split()[0] if r["status"] else "?"] += 1
total = collections.Counter(r["status"].split()[0] for r in rows)
ids = collections.Counter(r["id"] for r in rows)
print("rows", len(rows), "unique ids", len(ids))
print("statuses", dict(total))
print("duplicate ids", {k: v for k, v in ids.items() if v > 1})
for s, c in by_sprint.items():
    print(f"{s[:70]:70} {dict(c)}")
if "--rows" in sys.argv:
    for r in rows:
        print(json.dumps(r, ensure_ascii=False))
