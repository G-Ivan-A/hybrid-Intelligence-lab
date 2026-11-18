#!/usr/bin/env python3
"""Pin floating spoke links to extracted BA sources onto ba-ai-metamodel (B-249).

A floating link names a branch (not a 40-hex SHA) of the Hub and a path that
the extraction moved: `projects/ba-ai-process/`, `research/mango/`,
`docs/ba-meta-model-overview.md` or one of the five BA tests in `tools/`.
After the Hub tombstone such a link answers 404. The rewrite keeps the same
object and points it at an immutable commit of the new repository:

  github.com/G-Ivan-A/hybrid-Intelligence-lab/<blob|tree|raw>/<ref>/<path>
    -> github.com/G-Ivan-A/ba-ai-metamodel/<blob|tree|raw>/<SHA>/<mapped path>
  raw.githubusercontent.com/G-Ivan-A/hybrid-Intelligence-lab/<ref>/<path>
    -> raw.githubusercontent.com/G-Ivan-A/ba-ai-metamodel/<SHA>/<mapped path>

where `projects/ba-ai-process/X` maps to `X` and other paths keep their
names (MAP of ba-instance-params.txt). SHA-pinned Hub links are untouched:
they still resolve against the archive revision.

Usage:
  pin-spoke-links.py --repo PATH --sha SHA [--check] [--verify-target PATH]

--check rewrites nothing and exits 1 when a floating link is left.
--verify-target checks every rewritten path exists at SHA in a local clone.
"""
import argparse
import re
import subprocess
import sys
from collections import Counter

SOURCES = (r"projects/ba-ai-process(?:/|(?=[\s)\]>'\"`]))|research/mango(?:/|(?=[\s)\]>'\"`]))"
           r"|docs/ba-meta-model-overview\.md"
           r"|tools/test-(?:execution-package|cline-package|opencode-package"
           r"|bcreq-working-release-pipeline|ba-meta-model-overview)\.sh")
LINK = re.compile(
    r"(?P<host>github\.com/G-Ivan-A/hybrid-Intelligence-lab/(?P<kind>blob|tree|raw)"
    r"|raw\.githubusercontent\.com/G-Ivan-A/hybrid-Intelligence-lab)"
    r"/(?P<ref>[^/\s)\]>'\"`]+)/(?P<path>(?:" + SOURCES + r")[^\s)\]>'\"`#?]*)",
    re.I)
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def mapped(path):
    prefix = "projects/ba-ai-process/"
    if path.startswith(prefix):
        return path[len(prefix):]
    return "" if path == "projects/ba-ai-process" else path


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--sha", required=True)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--verify-target")
    args = ap.parse_args()
    if not SHA40.match(args.sha):
        sys.exit("--sha must be a full 40-hex commit")

    floating, pinned, files = Counter(), 0, Counter()
    targets = set()
    undecodable = []
    for rel in git(args.repo, "ls-files", "-z").decode().split("\0"):
        if not rel:
            continue
        path = f"{args.repo}/{rel}"
        with open(path, "rb") as fh:
            data = fh.read()
        if b"\0" in data[:8192]:
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            if b"hybrid-Intelligence-lab" in data:
                undecodable.append(rel)
            continue

        def repl(m):
            nonlocal pinned
            if SHA40.match(m.group("ref").lower()):
                pinned += 1
                return m.group(0)
            new_path = mapped(m.group("path").rstrip(".,;:"))
            tail = m.group("path")[len(m.group("path").rstrip(".,;:")):]
            floating[m.group("path").rstrip(".,;:")] += 1
            files[rel] += 1
            targets.add(new_path)
            if m.group("kind"):
                host = f"github.com/G-Ivan-A/ba-ai-metamodel/{m.group('kind')}"
            else:
                host = "raw.githubusercontent.com/G-Ivan-A/ba-ai-metamodel"
            return f"{host}/{args.sha}/{new_path}{tail}"

        new = LINK.sub(repl, text)
        if new != text and not args.check:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)

    print(f"repo: {args.repo}")
    print(f"head: {git(args.repo, 'rev-parse', 'HEAD').decode().strip()}")
    print(f"pinned-hub-links-kept: {pinned}")
    print(f"floating-links: {sum(floating.values())} in {len(files)} file(s)")
    for p, n in sorted(floating.items()):
        print(f"target {p}: {n}")
    for rel, n in sorted(files.items()):
        print(f"file {rel}: {n}")
    for rel in undecodable:
        print(f"undecodable-with-hub-mention {rel}")
    missing = []
    if args.verify_target:
        for p in sorted(targets):
            spec = f"{args.sha}:{p}" if p else f"{args.sha}^{{tree}}"
            ok = subprocess.run(["git", "-C", args.verify_target, "cat-file", "-e", spec],
                                capture_output=True).returncode == 0
            print(f"exists {p or '.'} @ {args.sha[:7]}: {'yes' if ok else 'NO'}")
            if not ok:
                missing.append(p)
    if missing or undecodable or (args.check and floating):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
