#!/usr/bin/env python3
"""Experiment for issue #638: rewrite outputs.hashes of the GigaCode package manifest.

The GigaCode package is edited directly in dist/, so after moving junior-guide.md
into docs/guides/ the immutable-output list must be rebuilt. The script walks the
package with the same exclusions as tools/validate-package.py, recomputes SHA-256
for every file and replaces only the `outputs.hashes` block, keeping the rest of
package-manifest.yaml byte-for-byte. Prints added, removed and changed paths.
"""
import hashlib, os, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent / "dist/execution-package-gigacode-cli"
MANIFEST = ROOT / "package-manifest.yaml"
MUTABLE = ("docs/kb/", "golden/candidates/", "meta-model/", "runs/")

actual = {}
for current, _dirs, files in os.walk(ROOT):
    for name in files:
        rel = os.path.relpath(os.path.join(current, name), ROOT).replace(os.sep, "/")
        if rel in {"package-manifest.yaml", ".gigacode/settings.json"} or rel.startswith(MUTABLE):
            continue
        if "/__pycache__/" in f"/{rel}" and rel.endswith(".pyc"):
            continue
        actual[rel] = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()

text = MANIFEST.read_text(encoding="utf-8")
block = re.search(r"^  hashes:\n((?:    .+\n)+)", text, re.M)
old = dict(line.strip().split(": ", 1) for line in block.group(1).splitlines())
new_block = "".join(f"    {rel}: {actual[rel]}\n" for rel in sorted(actual))
MANIFEST.write_text(text[:block.start(1)] + new_block + text[block.end(1):], encoding="utf-8")

print("added:", sorted(set(actual) - set(old)))
print("removed:", sorted(set(old) - set(actual)))
print("changed:", sorted(rel for rel in set(actual) & set(old) if actual[rel] != old[rel]))
