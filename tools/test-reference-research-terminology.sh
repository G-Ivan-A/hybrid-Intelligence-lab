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

# ADR-011 (accepted, D6): критерий «>= 3 независимых домена» закрыт восемью
# модулями RRP, статус паттерна повышен Experimental -> Validated. Ratchet:
# понизить статус обратно правкой глоссария нельзя.
grep -Eq '^\| Reference Research Pattern \(RRP\) \|.*Validated' "$glossary_file" ||
  fail "glossary must record the RRP pattern status Validated (ADR-011, D6)"

! grep -Eq '^\| Reference Research Pattern \(RRP\) \|.*Experimental' "$glossary_file" ||
  fail "glossary must not keep the superseded RRP status Experimental"

# ADR-011, ограничение контекста 1: Analysis - отдельный тип артефакта, а не
# модель research. Зонтичный термин, ставящий его в один ряд с RRP, запрещён.
for forbidden in 'Модель исследования' 'Research Model'; do
  ! grep -Fq "$forbidden" "$glossary_file" ||
    fail "glossary must not introduce an umbrella term over Analysis and RRP: $forbidden"
done

# ADR-011 accepted -> модель M3 легитимна и обязана быть определена в глоссарии.
grep -Fq '| Discussion Paper / Survey |' "$glossary_file" ||
  fail "glossary must define Discussion Paper / Survey (ADR-011, D2)"

# L3: стандарт research обязан содержать модели и Decision Tree выбора модели
# (ADR-011, D5 / B-104), иначе исполнителю нечем маршрутизировать задачу.
standard_file="standards/research-standard.md"

grep -Fq '## Три модели research-артефакта' "$standard_file" ||
  fail "research standard must describe the three research artifact models"

grep -Fq '## Gate выбора модели исследования' "$standard_file" ||
  fail "research standard must contain the research model selection gate"

grep -Fq 'research_model' "$standard_file" ||
  fail "research standard must define routing for an unset research_model contract parameter"

! grep -Eq '^\| \*\*M2\. Reference Research Pattern \(RRP\)\*\* \|.*Experimental' "$standard_file" ||
  fail "research standard must not describe RRP as Experimental after ADR-011 D6"

grep -Eq '^\| Analysis \|.*[Оо]тдельный тип артефакта' "$glossary_file" ||
  fail "glossary must describe Analysis as a separate artifact type, not a research model"

grep -Eq '^\| Analysis \|.*analysis-standard\.md.*docs/analysis/' "$glossary_file" ||
  fail "glossary must point Analysis at its own standard and home directory"

for term in 'Research Method' 'Domain Methodology' 'Reference Research Pattern (RRP)' 'Discussion Paper / Survey'; do
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
