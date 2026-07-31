#!/usr/bin/env python3
"""Direction 3, experiment B: what does an entry point actually cost to read?

The hypothesis under test proposes a "repo entry point" — an index carrying
decision contracts that the agent reads before acting. An index is only useful
if following it terminates inside a context budget. This experiment walks the
Markdown link graph outward from each candidate entry point and measures the
transitive closure: how many files an agent reaches, how many bytes and
approximate tokens that is, and how deep it has to go.

Two numbers decide whether an index helps or merely adds a hop:

    closure_bytes   everything reachable by following links — the worst case for
                    an agent that reads what it is pointed at
    depth_profile   bytes gained per hop — where the budget is actually spent

A closure that exceeds a working context means the entry point cannot be
"just read"; it must instead carry the decision rules inline, so that depth 0
alone is sufficient to act. That distinction is the practical finding.

Token estimate: bytes / 3.2, a conservative ratio for mixed Russian and English
Markdown (Russian Cyrillic costs more tokens per byte than English). It is an
order-of-magnitude figure, labelled as such in the output, not a measurement.

Usage:
    python3 experiment-closure.py [--repo-root PATH]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import urllib.parse

HERE = pathlib.Path(__file__).resolve().parent

# Markdown inline links and bare reference definitions. Anchors, external URLs
# and mailto targets are dropped: they cost the agent nothing inside the repo.
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

BYTES_PER_TOKEN = 3.2

# Templates ship with unrendered placeholders (`{{hub_url}}`). They are not
# broken links, they are parameters, and counting them as breakage would inflate
# the only number in this experiment that looks like a defect.
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}|<[^>]+>")

# A working budget for one agent session. The question an index must answer is
# not "how big is the repository" but "how far can the agent follow links before
# the budget is gone".
CONTEXT_BUDGETS = [50_000, 200_000, 1_000_000]

# Candidates are the documents that today claim, explicitly or by convention, to
# be where an agent starts. Comparing them shows whether the repository already
# has an entry point and what it costs.
CANDIDATES = [
    "ai-rules/agent-onboarding-protocol.md",
    "ai-rules/agent-work-rules.md",
    "GOVERNANCE.md",
    "CONTRIBUTING.md",
    "README.md",
]


def is_internal(target: str) -> bool:
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return False
    return True


def resolve(source: pathlib.Path, target: str,
            root: pathlib.Path) -> pathlib.Path | None:
    """Resolve a link relative to its source file, staying inside the repo."""
    target = urllib.parse.unquote(target.split("#", 1)[0]).strip()
    if not target:
        return None
    candidate = (root / target[1:] if target.startswith("/")
                 else source.parent / target)
    try:
        resolved = candidate.resolve()
        resolved.relative_to(root)
    except (ValueError, OSError):
        return None
    return resolved


def walk(root: pathlib.Path, entry: str) -> dict:
    """Breadth-first closure of Markdown links reachable from `entry`."""
    start = (root / entry).resolve()
    if not start.exists():
        return {"entry": entry, "exists": False}

    seen = {start: 0}
    broken: list[str] = []
    non_markdown: set[pathlib.Path] = set()
    frontier = [start]
    depth = 0

    while frontier:
        nxt = []
        for path in frontier:
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for match in LINK_RE.finditer(text):
                target = match.group(1)
                if not is_internal(target):
                    continue
                if PLACEHOLDER_RE.search(target):
                    continue
                resolved = resolve(path, target, root)
                if resolved is None:
                    continue
                if not resolved.exists():
                    broken.append(
                        f"{path.relative_to(root)} -> {target}")
                    continue
                if resolved.suffix.lower() != ".md":
                    # Scripts and data are reachable but an agent reads them on
                    # demand, not as part of onboarding; counted separately.
                    non_markdown.add(resolved)
                    continue
                if resolved not in seen:
                    seen[resolved] = depth + 1
                    nxt.append(resolved)
        frontier = nxt
        depth += 1

    by_depth: dict[int, dict] = {}
    for path, level in seen.items():
        bucket = by_depth.setdefault(level, {"files": 0, "bytes": 0})
        bucket["files"] += 1
        bucket["bytes"] += path.stat().st_size

    total_bytes = sum(b["bytes"] for b in by_depth.values())
    cumulative = 0
    profile = []
    for level in sorted(by_depth):
        cumulative += by_depth[level]["bytes"]
        profile.append({
            "depth": level,
            "files": by_depth[level]["files"],
            "bytes": by_depth[level]["bytes"],
            "cumulative_bytes": cumulative,
            "cumulative_tokens_approx": round(cumulative / BYTES_PER_TOKEN),
        })

    # How far can an agent follow links before each budget is exhausted?
    affordable = {}
    for budget in CONTEXT_BUDGETS:
        reachable = [p["depth"] for p in profile
                     if p["cumulative_tokens_approx"] <= budget]
        affordable[str(budget)] = max(reachable) if reachable else None

    return {
        "entry": entry,
        "exists": True,
        "affordable_depth_by_budget": affordable,
        "closure_files": len(seen),
        "closure_bytes": total_bytes,
        "closure_tokens_approx": round(total_bytes / BYTES_PER_TOKEN),
        "max_depth": max(seen.values()),
        "entry_bytes": start.stat().st_size,
        "entry_tokens_approx": round(start.stat().st_size / BYTES_PER_TOKEN),
        "non_markdown_reachable": len(non_markdown),
        "broken_links": sorted(set(broken)),
        "depth_profile": profile,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=str(HERE.parents[3]))
    args = parser.parse_args()
    root = pathlib.Path(args.repo_root).resolve()

    tracked_md = sorted(root.rglob("*.md"))
    tracked_md = [p for p in tracked_md if ".git/" not in str(p)]
    repo_bytes = sum(p.stat().st_size for p in tracked_md)

    results = [walk(root, entry) for entry in CANDIDATES]

    report = {
        "experiment": "entry-point link closure and context budget",
        "token_estimate": (
            f"bytes / {BYTES_PER_TOKEN}, order-of-magnitude only; Cyrillic "
            "Markdown tokenises less efficiently than English"
        ),
        "repository": {
            "markdown_files": len(tracked_md),
            "markdown_bytes": repo_bytes,
            "markdown_tokens_approx": round(repo_bytes / BYTES_PER_TOKEN),
        },
        "entry_points": results,
    }

    out = HERE / "experiment-closure.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    print(f"repository markdown: {len(tracked_md)} files, "
          f"{repo_bytes / 1024:.0f} KiB, "
          f"~{report['repository']['markdown_tokens_approx']} tokens")
    print()
    for res in results:
        if not res["exists"]:
            print(f"{res['entry']:45s} MISSING")
            continue
        print(f"{res['entry']:45s} entry~{res['entry_tokens_approx']:6d}tok  "
              f"closure {res['closure_files']:3d} files "
              f"~{res['closure_tokens_approx']:6d}tok  "
              f"depth={res['max_depth']}  broken={len(res['broken_links'])}  "
              f"affordable_depth@200k="
              f"{res['affordable_depth_by_budget']['200000']}")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
