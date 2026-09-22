#!/usr/bin/env bash
# Замер прослеживаемости мета-модели и пакета исполнения к модулям
# research/ai-education/. Вопрос: на какие модули исследования по созданию
# ИИ-агентов проектные артефакты ссылаются хотя бы один раз.
# Запуск: ./measure-research-coverage.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
TARGET="$ROOT/projects/ba-ai-process"
printf '%-42s %s\n' "модуль" "ссылок"
covered=0
total=0
for module in "$ROOT"/research/ai-education/*/; do
  name="$(basename "$module")"
  count="$({ grep -rn "ai-education/$name" "$TARGET" || true; } | wc -l | tr -d ' ')"
  printf '%-42s %s\n' "$name" "$count"
  total=$((total + 1))
  if [[ "$count" -gt 0 ]]; then covered=$((covered + 1)); fi
done
printf 'покрыто модулей: %s из %s\n' "$covered" "$total"
