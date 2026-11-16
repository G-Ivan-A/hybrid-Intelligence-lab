#!/usr/bin/env bash
# Заморозка источников выноса проекта из Хаба (контракт выноса, шаг 0;
# B-243 Ш3.0, issue #738).
#
# Контракт ops/hub-project-extraction-contract.md проверяет заморозку только на
# стороне нового репозитория: агент этапа E1…E6 видит коммиты в источниках после
# `HUB_SHA` и останавливается. Эта проверка ставит тот же запрет на стороне Хаба,
# чтобы нарушение не попало в `main`, а не обнаруживалось этапом позже.
#
# Правило: ни один коммит из `HUB_SHA..REV` (достижим из REV, но не из
# HUB_SHA) не меняет пути-источники
# `MAP` из блока параметров выноса. Команда та же, что в шаге 0 контракта:
#   git log --oneline HUB_SHA..REV -- SOURCES
#
# Usage: check-extraction-freeze.sh PARAMS [REV]
#   PARAMS  файл с блоком extraction-params (строки `KEY: value`)
#   REV     проверяемая ревизия (по умолчанию HEAD)
#
# Снятие заморозки: PR надгробия (B-249) удаляет источники и в том же PR
# убирает шаг этой проверки из .github/workflows/validate.yml. Новый `HUB_SHA`
# выбирает только владелец; тогда меняется `HUB_SHA` в PARAMS и в задаче выноса.
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "usage: $0 PARAMS [REV]" >&2
  exit 2
fi
PARAMS="$1"
REV="${2:-HEAD}"

fail() {
  echo "::error::extraction freeze: $1" >&2
  exit 1
}

[[ -f "$PARAMS" ]] || fail "нет файла параметров $PARAMS"
param() { sed -n "s/^$1: //p" "$PARAMS"; }

HUB_SHA="$(param HUB_SHA)"
[[ "$HUB_SHA" =~ ^[0-9a-f]{40}$ ]] || fail "HUB_SHA в $PARAMS — не 40 hex: '$HUB_SHA'"

SOURCES=()
while IFS= read -r m; do
  [[ -n "$m" ]] && SOURCES+=("${m%%=*}")
done < <(param MAP)
[[ ${#SOURCES[@]} -gt 0 ]] || fail "в $PARAMS нет строк MAP"

git cat-file -e "$HUB_SHA^{commit}" 2>/dev/null \
  || fail "коммит HUB_SHA $HUB_SHA недоступен: нужен полный клон (actions/checkout с fetch-depth: 0)"
git rev-parse --verify --quiet "$REV^{commit}" >/dev/null || fail "ревизия $REV не найдена"
# Ветка от более старого main не содержит HUB_SHA. Диапазон HUB_SHA..REV тогда
# состоит из собственных коммитов ветки: именно они попадут в main после HUB_SHA.
if ! git merge-base --is-ancestor "$HUB_SHA" "$REV"; then
  echo "::notice::extraction freeze: $REV не содержит HUB_SHA $HUB_SHA; проверяются коммиты ветки вне истории HUB_SHA"
fi

changed="$(git log --oneline "$HUB_SHA..$REV" -- "${SOURCES[@]}")"
if [[ -n "$changed" ]]; then
  {
    echo "::error::extraction freeze: источники выноса изменены после HUB_SHA $HUB_SHA (параметры: $PARAMS)."
    echo "Коммиты, меняющие источники:"
    printf '%s\n' "$changed" | sed 's/^/  /'
    echo "Файлы:"
    git diff --name-only "$HUB_SHA" "$REV" -- "${SOURCES[@]}" | sed 's/^/  /'
    echo "Что делать: источники заморожены до надгробия в Хабе (B-249). Уберите эти"
    echo "коммиты из ветки PR и внесите правку в репозиторий-цель выноса. Revert-коммит"
    echo "не помогает: контракт останавливается на любом коммите в источниках после"
    echo "HUB_SHA. Если коммит уже в main, новый HUB_SHA выбирает владелец: он же"
    echo "обновляет HUB_SHA в $PARAMS и в задаче выноса, затем E1 повторяется."
  } >&2
  exit 1
fi

echo "extraction freeze OK: ${#SOURCES[@]} source path(s) unchanged in $HUB_SHA..$(git rev-parse --short "$REV")"
