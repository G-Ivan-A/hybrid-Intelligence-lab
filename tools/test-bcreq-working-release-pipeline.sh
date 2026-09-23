#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
rfc="$repo_root/projects/ba-ai-process/docs/rfc/2026-09-bcreq-working-release-pipeline.md"

required_markers=(
  "working_baseline_id"
  "release_manifest"
  "requires_backward_compatibility"
  "applies_to_fr"
  "G-release"
  "2.3 «Задачи»"
  "Функциональный дизайн решения"
)

for marker in "${required_markers[@]}"; do
  grep -Fq -- "$marker" "$rfc" || {
    echo "missing Working/Release pipeline marker: $marker" >&2
    exit 1
  }
done

python3 - "$rfc" <<'PY'
import pathlib
import re
import sys

rfc = pathlib.Path(sys.argv[1])
violations = []
for line_number, line in enumerate(rfc.read_text(encoding="utf-8").splitlines(), start=1):
    for match in re.finditer(r"\]\(([^)]+)\)", line):
        target = match.group(1).split(maxsplit=1)[0]
        if not target.startswith(("https://", "mailto:")):
            violations.append(f"{rfc}:{line_number}: {target}")

if violations:
    print("\n".join(violations), file=sys.stderr)
    print(
        "Working/Release pipeline RFC contains a non-absolute Markdown link",
        file=sys.stderr,
    )
    raise SystemExit(1)
PY

echo "BCREQ Working/Release pipeline contract: OK"
