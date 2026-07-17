#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
adr="$repo_root/docs/adr/2026-07-adr-009-mango-repo-split.md"
plan="$repo_root/docs/analysis/2026-07-17-mango-artifacts-migration-plan.md"

if grep -Fq 'kb/processes/' "$adr" "$plan"; then
  echo "ERROR: obsolete kb/processes/ path remains in the Mango migration contract" >&2
  exit 1
fi

grep -Fq '| `kb/` (включая `processed/`, `sources/`, `fragments/`, `practices/`) | Операционная база знаний, обработанные данные и внутренние практики. |' "$adr"
grep -Fq 'Весь каталог `kb/` мигрирует в **Priv** как единое дерево' "$plan"
grep -Fq '| `kb/` (5 077; включая `processed/`, `sources/`, `fragments/`, `practices/`) | **Priv** | `kb/` | Перенос целиком as-is' "$plan"

if grep -Eq 'Q1 и Q2 фаундером|Q1 и Q2 сформулированы|Закрыть Q1 .* и Q2|Q1–Q4 остаются' "$plan"; then
  echo "ERROR: migration plan still describes resolved Q2 as open" >&2
  exit 1
fi

echo "Mango kb migration contract test passed."
