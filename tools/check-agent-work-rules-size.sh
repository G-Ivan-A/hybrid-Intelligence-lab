#!/usr/bin/env bash
# Бюджетный инвариант точки входа: ai-rules/agent-work-rules.md лежит на глубине 0
# от точки входа агента, поэтому его размер напрямую расходует рабочий бюджет
# контекста. Источник порогов: docs/rfc/2026-08-06-rfc-task-statement-architecture.md
# (§P.9, «Файл остаётся ниже ~8k токенов»).
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_FILE="${TARGET_FILE:-$ROOT_DIR/ai-rules/agent-work-rules.md}"
# Байты на токен для смешанного ru/en Markdown; оценка, не точный токенайзер.
BYTES_PER_TOKEN="${BYTES_PER_TOKEN:-3.2}"
WARN_TOKENS="${WARN_TOKENS:-7000}"
ERROR_TOKENS="${ERROR_TOKENS:-9000}"

if [[ ! -f "$TARGET_FILE" ]]; then
  printf 'ERROR: budget invariant target not found: %s\n' "$TARGET_FILE" >&2
  exit 1
fi

bytes="$(wc -c <"$TARGET_FILE" | tr -d '[:space:]')"
tokens="$(awk -v b="$bytes" -v r="$BYTES_PER_TOKEN" 'BEGIN { printf "%d", b / r }')"
rel_path="${TARGET_FILE#"$ROOT_DIR/"}"

printf '%s: %s bytes = ~%s tokens (warning %s, error %s).\n' \
  "$rel_path" "$bytes" "$tokens" "$WARN_TOKENS" "$ERROR_TOKENS"

if (( tokens > ERROR_TOKENS )); then
  printf 'ERROR: %s exceeds the hard budget of %s tokens (~%s).\n' \
    "$rel_path" "$ERROR_TOKENS" "$tokens" >&2
  printf 'Вынесите детали в отдельный артефакт и оставьте в точке входа ссылку.\n' >&2
  exit 1
fi

if (( tokens > WARN_TOKENS )); then
  printf 'WARNING: %s exceeds the soft budget of %s tokens (~%s).\n' \
    "$rel_path" "$WARN_TOKENS" "$tokens" >&2
fi

printf 'Agent work rules size check passed.\n'
