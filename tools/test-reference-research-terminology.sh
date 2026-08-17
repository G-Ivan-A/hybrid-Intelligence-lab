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

grep -Eq '^\| Research Method \|.*Theory → Taxonomy → Decision Framework → Practice' "$glossary_file" ||
  fail "glossary must define Research Method with its canonical route"

grep -Eq '^\| Domain Methodology \|.*Conceptual Framing → Object Model → Decision Space' "$glossary_file" ||
  fail "glossary must define Domain Methodology with its canonical sequence"

grep -Fq '| Reference Research Pattern (RRP) |' "$glossary_file" ||
  fail "glossary must define Reference Research Pattern (RRP)"

grep -Eq '^\| Reference Research Pattern \(RRP\) \|.*Experimental' "$glossary_file" ||
  fail "glossary must keep the RRP pattern status Experimental"

# ADR-011, ограничение контекста 1: Analysis - отдельный тип артефакта, а не
# модель research. Зонтичный термин, ставящий его в один ряд с RRP, запрещён.
for forbidden in 'Модель исследования' 'Research Model' 'Discussion Paper'; do
  ! grep -Fq "$forbidden" "$glossary_file" ||
    fail "glossary must not legitimise a term still only proposed in ADR-011: $forbidden"
done

grep -Eq '^\| Analysis \|.*[Оо]тдельный тип артефакта' "$glossary_file" ||
  fail "glossary must describe Analysis as a separate artifact type, not a research model"

grep -Eq '^\| Analysis \|.*analysis-standard\.md.*docs/analysis/' "$glossary_file" ||
  fail "glossary must point Analysis at its own standard and home directory"

for term in 'Research Method' 'Domain Methodology' 'Reference Research Pattern (RRP)'; do
  awk -v term="$term" -F'|' '{ name=$2; gsub(/^ +| +$/, "", name); if (name == term) print $5 }' "$glossary_file" |
    grep -Eq 'research-standard\.md|rfc-reference-research-pattern\.md' ||
    fail "glossary term must cross-reference research-standard or the RRP RFC: $term"
done

grep -Fq 'Research Method ⟂ Domain Methodology' "$glossary_file" ||
  fail "glossary must relate Research Method and Domain Methodology as orthogonal layers"

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
