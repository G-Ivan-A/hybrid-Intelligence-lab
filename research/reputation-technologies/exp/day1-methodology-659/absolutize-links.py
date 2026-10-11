#!/usr/bin/env python3
"""Rewrite relative markdown links to absolute GitHub URLs on the main branch.

Usage: python3 -I absolutize-links.py <repo-root> <file.md> [...]

Only file links are rewritten. In-page anchors (#...), http(s) and mailto
links stay as they are. The link target must exist in the working tree,
otherwise the script reports it and leaves the link untouched.
"""
import os
import re
import sys

BASE = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
LINK = re.compile(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)")


def main(argv):
    root = os.path.abspath(argv[1])
    missing = 0
    for path in argv[2:]:
        text = open(path, encoding="utf-8").read()
        folder = os.path.dirname(os.path.abspath(path))

        def repl(match):
            nonlocal missing
            target = match.group(1)
            file_part, _, anchor = target.partition("#")
            resolved = os.path.normpath(os.path.join(folder, file_part))
            if not os.path.exists(resolved):
                print(f"missing: {path}: {target}")
                missing += 1
                return match.group(0)
            url = BASE + os.path.relpath(resolved, root).replace(os.sep, "/")
            return "](" + url + ("#" + anchor if anchor else "") + ")"

        new = LINK.sub(repl, text)
        if new != text:
            open(path, "w", encoding="utf-8").write(new)
            print(f"rewritten: {path}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
