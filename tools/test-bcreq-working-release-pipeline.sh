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
  rg -q --fixed-strings "$marker" "$rfc" || {
    echo "missing Working/Release pipeline marker: $marker" >&2
    exit 1
  }
done

if rg -n '\]\((?!https://|mailto:)' "$rfc" --pcre2; then
  echo "Working/Release pipeline RFC contains a non-absolute Markdown link" >&2
  exit 1
fi

echo "BCREQ Working/Release pipeline contract: OK"
