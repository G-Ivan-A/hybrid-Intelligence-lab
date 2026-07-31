#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

rfc_file="docs/rfc/2026-07-17-rfc-reference-research-pattern.md"
glossary_file="standards/glossary.md"

grep -Fq 'Theory → Taxonomy → Decision Framework → Practice' "$rfc_file" ||
  fail "RFC must define the canonical Research Method sequence"

grep -Fq 'Conceptual Framing → Object Model → Decision Space' "$rfc_file" ||
  fail "RFC must define the canonical Domain Methodology sequence"

grep -Eq '^\| Conceptual Framing \|' "$glossary_file" ||
  fail "glossary must define Conceptual Framing"

grep -Eq '^\| Mental Model \|.*[Dd]eprecated' "$glossary_file" ||
  fail "glossary must mark Mental Model as deprecated"

unexpected_matches="$({
  rg -n -i 'mental[ -]model|mental_model' \
    --glob '*.md' \
    --glob '!tools/**' \
    --glob '!pr-ops/backlog.md' \
    --glob '!standards/glossary.md' \
    --glob '!research/ai-education/retrieval/10-theory.md' \
    . || true
})"

if [[ -n "$unexpected_matches" ]]; then
  printf '%s\n' "$unexpected_matches" >&2
  fail "deprecated Mental Model term remains outside documented compatibility references"
fi

printf 'Reference research terminology regression tests passed.\n'
