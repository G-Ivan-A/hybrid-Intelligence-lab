#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
module_dir="$root_dir/research/ai-education/tool-use"

required_files=(
  00-introduction.md
  10-theory.md
  20-taxonomy.md
  30-decision-framework.md
  40-practice-and-cases.md
  50-open-research.md
)

for file in "${required_files[@]}"; do
  test -f "$module_dir/$file" || {
    echo "missing Tool Use research module file: $file" >&2
    exit 1
  }
done

grep -Fq 'tool-use/00-introduction.md' "$root_dir/research/ai-education/README.md"
grep -Fq '/research/ai-education/tool-use/00-introduction.md' "$root_dir/pr-ops/artifact-map.md"
grep -Fq 'research/ai-education/tool-use/' "$root_dir/CHANGELOG.md"

echo "Tool Use research module structure is synchronized."
