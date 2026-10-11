#!/usr/bin/env bash
# Scan the reputation-technologies domain for wording that contradicts the
# GRA research model (issue #659). Lines that explicitly mark a historical
# wording ("до правки #659") or quote the forbidden phrase as forbidden are
# allowed. Exit code 1 if anything is found.
set -euo pipefail
ROOT="${1:-.}"
DOMAIN="$ROOT/research/reputation-technologies"

patterns=(
  'выросла из гравитационной модели'
  'GRA выросла'
  'обратн[аоя][йя]? доверию'
  'обратная величина доверия'
  'inverse of trust'
  'открыт[аоу][яюй] исследовательск[аоу][яюй] программ'
  'unifies the \*\*Gravity Model'
  'Grounded in the Gravity Model'
  'Научные основания: \*\*Gravity Model'
)

hits=0
for p in "${patterns[@]}"; do
  while IFS= read -r line; do
    case "$line" in
      *"до правки #659"*|*"Исправлено"*|*"Запрещ"*|*"запрещ"*|*"«GRA выросла"*|*"было:"*|*"Было"*) continue ;;
    esac
    echo "$line"
    hits=$((hits + 1))
  done < <(grep -rnE --include='*.md' "$p" "$DOMAIN" --exclude-dir=exp || true)
done

while IFS= read -r line; do
  echo "relative link: $line"
  hits=$((hits + 1))
done < <(grep -rnoP --include='*.md' '\]\((?!https?://|#|mailto:)[^)]+\)' "$DOMAIN" --exclude-dir=exp || true)

echo "hits: $hits"
[[ "$hits" -eq 0 ]]
