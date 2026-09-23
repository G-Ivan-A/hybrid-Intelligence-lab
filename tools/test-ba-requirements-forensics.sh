#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
analysis="$repo_root/projects/ba-ai-process/docs/analysis/2026-09-23-requirements-run-forensics.md"
rfc="$repo_root/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md"
structure_validator="$repo_root/tools/validate-repository-structure.sh"

required_analysis_markers=(
  "FR-INV-01"
  "UC-INV-01"
  "NFR-INV-01"
  "TMF-INV-01"
  "RUN-0001"
  "RUN-0067"
  "BCREQ-UNKNOWN / RUN-0001"
)

for marker in "${required_analysis_markers[@]}"; do
  rg -q --fixed-strings "$marker" "$analysis" || {
    echo "missing analysis marker: $marker" >&2
    exit 1
  }
done

required_rfc_markers=(
  "tm_forum_snapshot_id"
  "tm_forum_capability_id"
  "FR-INV-01"
  "UC-INV-01"
  "NFR-INV-01"
)

for marker in "${required_rfc_markers[@]}"; do
  rg -q --fixed-strings "$marker" "$rfc" || {
    echo "missing RFC marker: $marker" >&2
    exit 1
  }
done

rg -q --fixed-strings '"projects/ba-ai-process/docs/analysis"' "$structure_validator" || {
  echo "project analysis home is missing from the structure contract" >&2
  exit 1
}

if rg -n '\]\((?!https://|mailto:)' "$analysis" --pcre2; then
  echo "analysis contains a non-absolute Markdown link" >&2
  exit 1
fi

echo "BA requirements forensics contract: OK"
