#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

failures=0

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  failures=$((failures + 1))
}

require_dir() {
  local path="$1"
  [[ -d "$path" ]] || fail "missing directory: $path"
}

require_file() {
  local path="$1"
  [[ -f "$path" ]] || fail "missing file: $path"
}

reject_path() {
  local path="$1"
  [[ ! -e "$path" ]] || fail "legacy path should not exist: $path"
}

required_directories=(
  "docs/concept"
  "docs/governance"
  "education"
  "education/ba-prompt-engineering"
  "experiments"
  "frameworks"
  "meta"
  "projects"
  "research"
  "research/mango"
  "standards"
  "tests"
)

required_files=(
  "AI_GOVERNANCE.md"
  "PRODUCT_VISION.md"
  "README.md"
  "docs/concept/repository-structure.md"
  "docs/concept/vision-standard.md"
  "docs/governance/hybrid-team-collaboration.md"
  "education/README.md"
  "education/ba-prompt-engineering/DELIVERABLES.md"
  "education/ba-prompt-engineering/course-structure.md"
  "education/ba-prompt-engineering/presentation-content.md"
  "education/ba-prompt-engineering/presentation-structure.md"
  "education/ba-prompt-engineering/teacher-scenario.md"
  "experiments/tz-corpus/README.md"
  "frameworks/README.md"
  "meta/README.md"
  "projects/README.md"
  "research/README.md"
  "research/mango/README.md"
  "research/mango/classification.md"
  "research/mango/classification-tz.md"
  "research/mango/requirements-flow.md"
  "standards/README.md"
)

legacy_root_paths=(
  ".gitkeep"
  "DELIVERABLES.md"
  "course-structure.md"
  "presentation-content.md"
  "presentation-structure.md"
  "teacher-scenario.md"
)

for dir in "${required_directories[@]}"; do
  require_dir "$dir"
done

for file in "${required_files[@]}"; do
  require_file "$file"
done

for path in "${legacy_root_paths[@]}"; do
  reject_path "$path"
done

if [[ -f README.md ]]; then
  grep -q "PRODUCT_VISION.md" README.md || fail "README.md must link PRODUCT_VISION.md"
  grep -q "AI_GOVERNANCE.md" README.md || fail "README.md must link AI_GOVERNANCE.md"
fi

if [[ -f AI_GOVERNANCE.md ]]; then
  grep -q "Founder & PO" AI_GOVERNANCE.md || fail "AI_GOVERNANCE.md must define Founder & PO role"
  grep -q "Команда C" AI_GOVERNANCE.md || fail "AI_GOVERNANCE.md must define support team role"
fi

if [[ -f docs/concept/repository-structure.md ]]; then
  grep -q "ru/en" docs/concept/repository-structure.md || fail "repository structure must define bilingual ru/en policy"
  grep -q "Hub-and-Spoke" docs/concept/repository-structure.md || fail "repository structure must document Hub-and-Spoke option"
fi

if [[ "$failures" -gt 0 ]]; then
  printf '\nRepository structure validation failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'Repository structure validation passed.\n'
