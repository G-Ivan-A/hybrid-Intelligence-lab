#!/usr/bin/env bash
# Бюджетный инвариант точки входа: ai-rules/agent-work-rules.md лежит на глубине 0
# от точки входа агента, поэтому его размер напрямую расходует рабочий бюджет
# контекста. Источники порогов: docs/rfc/2026-08-06-rfc-task-statement-architecture.md
# (§P.9, «Файл остаётся ниже ~8k токенов») и
# docs/adr/2026-09-adr-021-agent-collaboration-layer.md (§5: «9K — рекомендация,
# не блокер»; при превышении рекомендуется декомпозиция без вытеснения норм).
#
# Поведение (B-196):
#   - выше WARN_TOKENS (~7k)      — мягкое предупреждение, код 0;
#   - выше DECOMPOSE_TOKENS (~9k) — предупреждение с рекомендацией декомпозиции, код 0;
#   - целевой файл не найден      — ошибка, код 1 (fail-closed).
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_FILE="${TARGET_FILE:-$ROOT_DIR/ai-rules/agent-work-rules.md}"
# Байты на токен для смешанного ru/en Markdown; оценка, не точный токенайзер.
BYTES_PER_TOKEN="${BYTES_PER_TOKEN:-3.2}"
WARN_TOKENS="${WARN_TOKENS:-7000}"
# ERROR_TOKENS — прежнее имя переменной, принимается для обратной совместимости.
DECOMPOSE_TOKENS="${DECOMPOSE_TOKENS:-${ERROR_TOKENS:-9000}}"

if [[ ! -f "$TARGET_FILE" ]]; then
  printf 'ERROR: budget invariant target not found: %s\n' "$TARGET_FILE" >&2
  exit 1
fi

bytes="$(wc -c <"$TARGET_FILE" | tr -d '[:space:]')"
tokens="$(awk -v b="$bytes" -v r="$BYTES_PER_TOKEN" 'BEGIN { printf "%d", b / r }')"
rel_path="${TARGET_FILE#"$ROOT_DIR/"}"

printf '%s: %s bytes = ~%s tokens (warning %s, decomposition recommended above %s).\n' \
  "$rel_path" "$bytes" "$tokens" "$WARN_TOKENS" "$DECOMPOSE_TOKENS"

if (( tokens > DECOMPOSE_TOKENS )); then
  printf 'WARNING: %s exceeds the recommended budget of %s tokens (~%s); this is a recommendation, not a blocker (ADR-021 §5).\n' \
    "$rel_path" "$DECOMPOSE_TOKENS" "$tokens" >&2
  printf 'Рекомендуется декомпозиция: вынесите детали в отдельные канонические артефакты с явными маршрутами и оставьте в точке входа ссылку, не вытесняя действующие нормы.\n' >&2
elif (( tokens > WARN_TOKENS )); then
  printf 'WARNING: %s exceeds the soft budget of %s tokens (~%s).\n' \
    "$rel_path" "$WARN_TOKENS" "$tokens" >&2
fi

printf 'Agent work rules size check passed.\n'
