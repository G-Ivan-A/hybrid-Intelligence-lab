#!/usr/bin/env python3
"""Reading-consistency matrix of ecosystem repositories against Hub homes (issue #715).

Usage: python3 -I research/hub/exp/hub-governance-roadmap-715/spoke-consistency-matrix.py <hub_dir> <spoke_dir>...
Reads files only; never executes spoke content.
"""
import json, os, sys, glob

CHECKS = [
    ("AGENTS.md", lambda r: os.path.isfile(f"{r}/AGENTS.md")),
    (".hub-profile.json", lambda r: os.path.isfile(f"{r}/.hub-profile.json")),
    ("profile.archetype", lambda r: prof(r).get("archetype")),
    ("profile.environment", lambda r: prof(r).get("environment")),
    ("profile.last_sync", lambda r: (prof(r).get("last_sync") or {}).get("date") if isinstance(prof(r).get("last_sync"), dict) else prof(r).get("last_sync")),
    ("last_sync pin key", lambda r: pin_key(prof(r))),
    ("ops/backlog.md", lambda r: os.path.isfile(f"{r}/ops/backlog.md")),
    ("other backlog", lambda r: ",".join(sorted(os.path.relpath(p, r) for p in glob.glob(f"{r}/**/*[Bb][Aa][Cc][Kk][Ll][Oo][Gg]*.md", recursive=True) if "/ops/backlog.md" not in p and "/.git/" not in p)[:3]) or "-"),
    ("pr-ops (legacy ops home)", lambda r: os.path.isdir(f"{r}/pr-ops")),
    ("docs/README.md", lambda r: os.path.isfile(f"{r}/docs/README.md")),
    ("docs/vision.md", lambda r: os.path.isfile(f"{r}/docs/vision.md")),
    ("docs/concept.md", lambda r: os.path.isfile(f"{r}/docs/concept.md")),
    ("docs/adr/", lambda r: os.path.isdir(f"{r}/docs/adr")),
    ("docs/contracts/ (forbidden)", lambda r: os.path.isdir(f"{r}/docs/contracts")),
    ("ai-rules/", lambda r: os.path.isdir(f"{r}/ai-rules")),
    ("root AI_*.md", lambda r: ",".join(sorted(os.path.basename(p) for p in glob.glob(f"{r}/AI_*.md"))) or "-"),
    ("issue tpl task.md", lambda r: os.path.isfile(f"{r}/.github/ISSUE_TEMPLATE/task.md")),
    ("issue tpl task-creative.md", lambda r: os.path.isfile(f"{r}/.github/ISSUE_TEMPLATE/task-creative.md")),
    ("CI workflow", lambda r: len(glob.glob(f"{r}/.github/workflows/*.y*ml"))),
    ("sync tool", lambda r: ",".join(sorted(os.path.relpath(p, r) for p in glob.glob(f"{r}/**/*sync*hub*", recursive=True) + glob.glob(f"{r}/**/*import*hub*", recursive=True) if "/.git/" not in p)) or "-"),
]

_cache = {}
def prof(r):
    if r not in _cache:
        try:
            _cache[r] = json.load(open(f"{r}/.hub-profile.json", encoding="utf-8"))
        except Exception:
            _cache[r] = {}
    return _cache[r]

def pin_key(p):
    """Which field (if any) pins the Hub source of the last sync."""
    ls = p.get("last_sync")
    if not isinstance(ls, dict) or not ls:
        return None
    for k in ("hub_sha", "hub_commit"):
        if k in ls:
            return k
    return "per-template versions"

repos = sys.argv[1:]
names = [os.path.basename(os.path.abspath(r)) for r in repos]
print("| Check | " + " | ".join(names) + " |")
print("| --- |" + " --- |" * len(names))
for label, fn in CHECKS:
    vals = []
    for r in repos:
        v = fn(r)
        vals.append("✅" if v is True else "❌" if v in (False, None, 0) else str(v))
    print(f"| {label} | " + " | ".join(vals) + " |")
