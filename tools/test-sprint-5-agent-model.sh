#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

require_text() {
  local path="$1"
  local text="$2"
  grep -Fq -- "$text" "$path" || fail "$path must contain: $text"
}

require_text ".github/ISSUE_TEMPLATE/task.yml" "- hybrid"
require_text "tools/test-operating-mode-contract.sh" "expected_modes"

stress_test="ai-rules/adversarial-stress-testing.md"
[[ -f "$stress_test" ]] || fail "missing stress-test procedure: $stress_test"
require_text "$stress_test" "✅ держит"
require_text "$stress_test" "⚠️ держит с оговоркой"
require_text "$stress_test" "❌ вскрывает границу"
require_text "$stress_test" "не менее пяти"
require_text "$stress_test" "pr-ops/backlog.md"

security_checklist="ai-governance/agent-security-checklist.md"
[[ -f "$security_checklist" ]] || fail "missing agent security checklist: $security_checklist"
for risk in LLM01 LLM02 LLM03 LLM04 LLM05 LLM06 LLM07 LLM08 LLM09 LLM10; do
  require_text "$security_checklist" "$risk"
done
require_text "$security_checklist" "SAIF"
require_text "$security_checklist" "Rule 6"
require_text "$security_checklist" "Человек > Команда Q > Исполнитель"
require_text "$security_checklist" "Readback"
require_text "$security_checklist" "Rule 5"
require_text "$security_checklist" "token budget"

require_text "pr-ops/artifact-map.md" "/ai-rules/adversarial-stress-testing.md"
require_text "pr-ops/artifact-map.md" "/ai-governance/agent-security-checklist.md"
require_text "pr-ops/backlog.md" "| **B-064** |"
require_text "pr-ops/backlog.md" "| **B-065** |"
require_text "pr-ops/backlog.md" "| **B-066** |"
require_text "pr-ops/backlog.md" "[#406](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/406)"

printf 'Sprint 5 agent-model regression tests passed.\n'
