#!/usr/bin/env bash
# Постусловие «непустой полезный дифф» на ярусе CI.
# Источник: docs/rfc/2026-08-06-rfc-task-statement-architecture.md
# (§"Implementation and Validation", шаг 1; §4.2 эмпирической валидации PR #462).
#
# Правило: pull request обязан содержать непустой дифф по содержательным путям.
# Дифф считается three-dot (от merge-base), чтобы проверка была устойчива к
# движению base-ветки и к merge-коммитам. Изменения исключительно в служебных
# файлах-заглушках не считаются полезными; тело самого PR в git не хранится и
# в дифф не попадает по определению.
#
# Escape-метка `no-diff-expected` пропускает проверку, но только если её
# поставил авторизованный пользователь (owner или admin репозитория).
#
# Переменные окружения:
#   BASE_REF                     — base-ветка PR (по умолчанию GITHUB_BASE_REF или main)
#   HEAD_REF                     — head-ревизия PR (по умолчанию HEAD)
#   PR_LABELS                    — метки PR через запятую или перевод строки
#   NO_DIFF_LABEL_ACTOR_ROLE     — роль поставившего метку: OWNER / ADMIN / прочее
#   NONEMPTY_DIFF_EXCLUDES       — доп. glob-шаблоны служебных путей через запятую
set -euo pipefail

ESCAPE_LABEL="no-diff-expected"
AUTHORIZED_ROLES_RE='^(OWNER|ADMIN)$'

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# NONEMPTY_DIFF_REPO позволяет проверять другой рабочий каталог (используется тестом).
cd "${NONEMPTY_DIFF_REPO:-$ROOT_DIR}"

base_ref="${BASE_REF:-${GITHUB_BASE_REF:-main}}"
head_ref="${HEAD_REF:-HEAD}"

# Служебные файлы-заглушки: их наличие в диффе не доказывает выполненную работу.
default_excludes=(
  "pull-request-bootstrap*"
  "*/pull-request-bootstrap*"
  ".github/PULL_REQUEST_TEMPLATE.md"
)

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

has_escape_label() {
  local labels="${PR_LABELS:-}"
  [[ -z "$labels" ]] && return 1
  local label
  while IFS= read -r label; do
    label="$(printf '%s' "$label" | tr -d '[:space:]')"
    [[ "$label" == "$ESCAPE_LABEL" ]] && return 0
  done < <(printf '%s\n' "$labels" | tr ',' '\n')
  return 1
}

resolve_base_commit() {
  local candidate
  for candidate in "$base_ref" "origin/$base_ref" "refs/remotes/origin/$base_ref"; do
    if git rev-parse --verify --quiet "$candidate^{commit}" >/dev/null; then
      printf '%s' "$candidate"
      return 0
    fi
  done
  return 1
}

is_excluded() {
  local path="$1" pattern
  for pattern in "${default_excludes[@]}"; do
    # shellcheck disable=SC2053 — glob-сопоставление намеренное
    [[ "$path" == $pattern ]] && return 0
  done
  if [[ -n "${NONEMPTY_DIFF_EXCLUDES:-}" ]]; then
    while IFS= read -r pattern; do
      pattern="$(printf '%s' "$pattern" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
      [[ -z "$pattern" ]] && continue
      # shellcheck disable=SC2053
      [[ "$path" == $pattern ]] && return 0
    done < <(printf '%s\n' "${NONEMPTY_DIFF_EXCLUDES}" | tr ',' '\n')
  fi
  return 1
}

if has_escape_label; then
  role="$(printf '%s' "${NO_DIFF_LABEL_ACTOR_ROLE:-}" | tr '[:lower:]' '[:upper:]' | tr -d '[:space:]')"
  if [[ "$role" =~ $AUTHORIZED_ROLES_RE ]]; then
    printf 'Метка %s поставлена авторизованным пользователем (%s): проверка диффа пропущена.\n' \
      "$ESCAPE_LABEL" "$role"
    exit 0
  fi
  fail "метка $ESCAPE_LABEL поставлена неавторизованным пользователем (роль: ${role:-неизвестна}); метку ставит только owner или admin"
fi

base_commit="$(resolve_base_commit)" || fail "base-ревизия '$base_ref' недоступна; нужен checkout с fetch-depth: 0"
git rev-parse --verify --quiet "$head_ref^{commit}" >/dev/null || fail "head-ревизия '$head_ref' недоступна"

merge_base="$(git merge-base "$base_commit" "$head_ref")" ||
  fail "не найден merge-base между '$base_ref' и '$head_ref'; нужен checkout с fetch-depth: 0"

mapfile -t changed_paths < <(git diff --name-only "$merge_base" "$head_ref")

meaningful=()
skipped=()
for path in "${changed_paths[@]}"; do
  [[ -z "$path" ]] && continue
  if is_excluded "$path"; then
    skipped+=("$path")
  else
    meaningful+=("$path")
  fi
done

if ((${#skipped[@]} > 0)); then
  printf 'Служебные пути, не считающиеся полезным диффом (%s):\n' "${#skipped[@]}"
  printf '  - %s\n' "${skipped[@]}"
fi

if ((${#meaningful[@]} == 0)); then
  printf 'ERROR: pull request не содержит полезного диффа относительно %s (merge-base %s).\n' \
    "$base_ref" "${merge_base:0:12}" >&2
  printf 'Постусловие непустого диффа: docs/rfc/2026-08-06-rfc-task-statement-architecture.md, шаг 1 внедрения.\n' >&2
  printf 'Если пустой PR намеренный, owner или admin ставит метку %s.\n' "$ESCAPE_LABEL" >&2
  exit 1
fi

printf 'Непустой дифф подтверждён: %s изменённых путей относительно %s (merge-base %s).\n' \
  "${#meaningful[@]}" "$base_ref" "${merge_base:0:12}"
printf '  - %s\n' "${meaningful[@]}"
printf 'Nonempty diff check passed.\n'
