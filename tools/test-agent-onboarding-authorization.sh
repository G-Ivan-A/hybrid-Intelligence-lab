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

require_text() {
  local file="$1"
  local expected="$2"
  if ! grep -Fq "$expected" "$file"; then
    echo "ERROR: $file must contain: $expected" >&2
    exit 1
  fi
}

if grep -Eni "$forbidden" "${files[@]}"; then
  echo "ERROR: active onboarding contracts still require separate approval" >&2
  exit 1
fi

require_text ai-rules/agent-onboarding-protocol.md 'Readback'
require_text ai-rules/agent-onboarding-protocol.md 'Мерж PR = согласование результата'
require_text ai-rules/agent-onboarding-protocol.md 'Комментарий без мержа = возврат в работу'
require_text ai-rules/agent-onboarding-protocol.md 'новая задача на'
require_text ai-rules/agent-onboarding-protocol.md 'исправление'
require_text ai-rules/agent-onboarding-protocol.md 'непустой дифф'

require_text templates/htom/AI_SESSION_HANDOVER_PROMPT.md 'Мерж PR = согласование результата'
require_text templates/htom/AI_SESSION_HANDOVER_PROMPT.md 'Непустой дифф'

echo "Agent onboarding authorization contract test passed."
