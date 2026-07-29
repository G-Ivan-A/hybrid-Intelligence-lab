#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

require_text() {
  local text="$1"
  grep -Fq -- "$text" pr-ops/backlog.md ||
    fail "backlog must contain: $text"
}

reject_text() {
  local text="$1"
  if grep -Fq -- "$text" pr-ops/backlog.md; then
    fail "backlog must not contain: $text"
  fi
}

b053_line="$(grep -F '| **B-053** |' pr-ops/backlog.md)"
[[ "$b053_line" == *'| DONE |'* ]] ||
  fail "B-053 must be DONE after merged PR #452"

b085_line="$(grep -F '| **B-085** |' pr-ops/backlog.md)"
[[ "$b085_line" == *'research/ai-education/retrieval/'* ]] ||
  fail "B-085 must point to the retrieval module"
[[ "$b085_line" == *'docs/rfc/2026-07-17-rfc-reference-research-pattern.md'* ]] ||
  fail "B-085 must point to the Reference Research Pattern RFC"
[[ "$b085_line" == *'Conceptual Framing'* ]] ||
  fail "B-085 must record the Conceptual Framing implementation"
[[ "$b085_line" == *'S = Decision(KB, Query, Constraints)'* ]] ||
  fail "B-085 must record the formal retrieval signature"

reject_text 'Результат: `research/education/2026-07-16-retrieval-strategies-survey.md`'
require_text '| **B-090** |'

printf 'Backlog current-state regression tests passed.\n'
