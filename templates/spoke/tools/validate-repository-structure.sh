#!/usr/bin/env bash
#
# Минимальный валидатор структуры spoke-проекта («иммунная система» генома).
# Проверяет наличие базовых артефактов «ДНК-шаблона» и ловит самовольный рост
# дерева до того, как он превратится в хаос. Запускать из корня спока:
#
#   ./tools/validate-repository-structure.sh
#
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

failures=0
warnings=0

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  failures=$((failures + 1))
}

warn() {
  printf 'WARN: %s\n' "$1" >&2
  warnings=$((warnings + 1))
}

require_dir() {
  [[ -d "$1" ]] || fail "missing directory: $1"
}

require_file() {
  [[ -f "$1" ]] || fail "missing file: $1"
}

required_directories=(
  "docs/adr"
  "docs/audit"
  ".github/ISSUE_TEMPLATE"
  "tools"
)

required_files=(
  "AI_GOVERNANCE.md"
  "AI_QUICK_RULES.md"
  "AI_HANDOVER_PROMPT.md"
  "README.md"
  "CONTRIBUTING.md"
  "CHANGELOG.md"
  "docs/adr/.gitkeep"
  "docs/audit/.gitkeep"
  ".github/ISSUE_TEMPLATE/task.md"
  "tools/validate-repository-structure.sh"
)

for dir in "${required_directories[@]}"; do
  require_dir "$dir"
done

for file in "${required_files[@]}"; do
  require_file "$file"
done

# AI_GOVERNANCE.md обязателен в корне каждого спока (жёсткое ограничение Хаба).
require_file "AI_GOVERNANCE.md"

# Handover Prompt должен оставаться параметризованным ({{REPO_NAME}}), чтобы
# «доверенность» переносилась в любой спок без правок (см. AI_HANDOVER_PROMPT.md).
if [[ -f "AI_HANDOVER_PROMPT.md" ]] && ! grep -Fq '{{REPO_NAME}}' "AI_HANDOVER_PROMPT.md"; then
  fail "AI_HANDOVER_PROMPT.md must keep the {{REPO_NAME}} placeholder"
fi

# Negative check: research/ по умолчанию не создаётся в споке. Фундаментальные
# знания живут в research/ Хаба. Если папка появилась — это должно быть
# осознанным решением, зафиксированным как ADR (см. AI_QUICK_RULES.md).
if [[ -d "research" ]]; then
  warn "research/ найдена в споке: по умолчанию её быть не должно. Зафиксируйте отклонение как ADR в docs/adr/ или вынесите знания в research/ Хаба."
fi

# Незаменённые плейсхолдеры шаблона: подсказка запустить init (если он ещё есть).
# Паттерн — регулярка, а не точный токен, чтобы init.sh не переписал эту проверку.
if grep -RIlq '{{[a-z_][a-z_]*}}' . --include='*.md' 2>/dev/null; then
  warn "найдены незаменённые плейсхолдеры шаблона ({{...}}): запустите ./init.sh для инициализации спока."
fi

if [[ "$warnings" -gt 0 ]]; then
  printf '\n%d warning(s) — не блокируют, но требуют внимания.\n' "$warnings" >&2
fi

if [[ "$failures" -gt 0 ]]; then
  printf '\nSpoke structure validation failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'Spoke structure validation passed.\n'
