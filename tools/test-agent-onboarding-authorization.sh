#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

files=(
  README.md
  ai-rules/agent-onboarding-protocol.md
  ai-rules/agent-work-rules.md
  standards/glossary.md
  standards/session-handover-standard.md
  templates/htom/AI_SESSION_HANDOVER_PROMPT.md
  templates/htom/README.md
)

forbidden='стоп до апрува|до апрува человека|до моего апрува|до явного апрува|approve / поехали|останавливается до апрува'

if grep -Eni "$forbidden" "${files[@]}"; then
  echo "ERROR: active onboarding contracts still require separate approval" >&2
  exit 1
fi

grep -Fq 'Readback' ai-rules/agent-onboarding-protocol.md
grep -Fq 'Мерж PR = согласование результата' ai-rules/agent-onboarding-protocol.md
grep -Fq 'Комментарий без мержа = возврат в работу' ai-rules/agent-onboarding-protocol.md
grep -Fq 'новая задача на' ai-rules/agent-onboarding-protocol.md
grep -Fq 'исправление' ai-rules/agent-onboarding-protocol.md
grep -Fq 'непустой дифф' ai-rules/agent-onboarding-protocol.md

grep -Fq 'Мерж PR = согласование результата' templates/htom/AI_SESSION_HANDOVER_PROMPT.md
grep -Fq 'непустой дифф' templates/htom/AI_SESSION_HANDOVER_PROMPT.md

echo "Agent onboarding authorization contract test passed."
