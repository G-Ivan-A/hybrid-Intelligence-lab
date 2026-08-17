#!/usr/bin/env bash
# Постусловие «иммутабельность исторических документов» на ярусе CI.
# Источник: docs/analysis/2026-08-11-sequential-task-contract-ambiguity-analysis.md
# (пробел: нет механической защиты RFC/ADR от переписывания в PR внедрения).
#
# Правило: pull request не изменяет и не удаляет существующие файлы в
# `docs/rfc/` и `docs/adr/`. Разрешено только добавление новых файлов.
# Историческое решение фиксирует состояние на момент принятия; если решение
# устарело, добавляется новый RFC/ADR, а не переписывается старый.
#
# Дифф считается three-dot (от merge-base), как в `validate-nonempty-diff.sh`,
# чтобы проверка была устойчива к движению base-ветки и к merge-коммитам.
#
# Allowlist: изменение существующего файла допускается, если после изменения он
# является совместимым редиректом — во frontmatter стоит `status: deprecated`
# или `status: superseded`, тело короче порога и содержит markdown-ссылку на
# актуальный артефакт. Такой файл сохраняет входящие ссылки живыми, не
# переписывая содержательное историческое решение. Дополнительные пути
# исключаются glob-шаблонами через HISTORICAL_IMMUTABLE_ALLOWLIST.
#
# Второе исключение — документ до decision gate: иммутабельность защищает
# «решение на момент принятия», а запись со статусом `draft` или `proposed`
# такого момента ещё не имеет (см. docs/adr/README.md: переходы
# `draft → proposed → accepted`, перевод в `accepted` требует human review).
# Правка допускается, только если запись была pre-decision и в base-ревизии:
# понизить статус уже принятого решения и тем обойти проверку нельзя.
#
# Переменные окружения:
#   BASE_REF                        — base-ветка PR (по умолчанию GITHUB_BASE_REF или main)
#   HEAD_REF                        — head-ревизия PR (по умолчанию HEAD)
#   HISTORICAL_IMMUTABLE_PATHS      — защищаемые префиксы через запятую
#                                     (по умолчанию docs/rfc/,docs/adr/)
#   HISTORICAL_IMMUTABLE_ALLOWLIST  — glob-шаблоны путей-исключений через запятую
#   HISTORICAL_IMMUTABLE_REPO       — рабочий каталог проверки (используется тестом)
set -euo pipefail

# Порог «короткого тела»: совместимый редирект — это заглушка со ссылкой,
# а не переписанный документ.
DEPRECATED_REDIRECT_MAX_BODY_LINES=40

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${HISTORICAL_IMMUTABLE_REPO:-$ROOT_DIR}"

base_ref="${BASE_REF:-${GITHUB_BASE_REF:-main}}"
head_ref="${HEAD_REF:-HEAD}"

IFS=',' read -r -a protected_prefixes <<<"${HISTORICAL_IMMUTABLE_PATHS:-docs/rfc/,docs/adr/}"

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
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

is_protected() {
  local path="$1" prefix
  for prefix in "${protected_prefixes[@]}"; do
    prefix="$(printf '%s' "$prefix" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
    [[ -z "$prefix" ]] && continue
    [[ "$path" == "$prefix"* ]] && return 0
  done
  return 1
}

is_allowlisted_path() {
  local path="$1" pattern
  [[ -z "${HISTORICAL_IMMUTABLE_ALLOWLIST:-}" ]] && return 1
  while IFS= read -r pattern; do
    pattern="$(printf '%s' "$pattern" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
    [[ -z "$pattern" ]] && continue
    # shellcheck disable=SC2053 — glob-сопоставление намеренное
    [[ "$path" == $pattern ]] && return 0
  done < <(printf '%s\n' "${HISTORICAL_IMMUTABLE_ALLOWLIST}" | tr ',' '\n')
  return 1
}

# Статус из frontmatter указанной ревизии; пустая строка, если его нет.
frontmatter_status() {
  local rev="$1" path="$2" content
  content="$(git show "$rev:$path" 2>/dev/null)" || return 0
  [[ "$(printf '%s\n' "$content" | head -n 1)" == "---" ]] || return 0
  printf '%s\n' "$content" | sed -n '2,/^---$/p' |
    sed -n 's/^status:[[:space:]]*\([a-zA-Z-]*\).*/\1/p' | head -n 1
}

# Документ до decision gate: статус draft|proposed и в base, и в head.
is_pre_decision_record() {
  local path="$1" base_status head_status
  base_status="$(frontmatter_status "$merge_base" "$path")"
  [[ "$base_status" == "draft" || "$base_status" == "proposed" ]] || return 1
  head_status="$(frontmatter_status "$head_ref" "$path")"
  [[ "$head_status" == "draft" || "$head_status" == "proposed" ||
    "$head_status" == "accepted" ]] || return 1
  return 0
}

# Совместимый редирект: deprecated/superseded frontmatter + короткое тело со ссылкой.
is_compatibility_redirect() {
  local path="$1" content status body
  content="$(git show "$head_ref:$path" 2>/dev/null)" || return 1
  [[ "$(printf '%s\n' "$content" | head -n 1)" == "---" ]] || return 1

  status="$(printf '%s\n' "$content" | sed -n '2,/^---$/p' |
    sed -n 's/^status:[[:space:]]*\([a-zA-Z-]*\).*/\1/p' | head -n 1)"
  [[ "$status" == "deprecated" || "$status" == "superseded" ]] || return 1

  body="$(printf '%s\n' "$content" | sed -n '2,$p' | sed -n '/^---$/,$p' | tail -n +2)"
  local body_lines
  body_lines="$(printf '%s\n' "$body" | grep -c '[^[:space:]]' || true)"
  ((body_lines <= DEPRECATED_REDIRECT_MAX_BODY_LINES)) || return 1

  printf '%s\n' "$body" | grep -q '](' || return 1
  return 0
}

base_commit="$(resolve_base_commit)" || fail "base-ревизия '$base_ref' недоступна; нужен checkout с fetch-depth: 0"
git rev-parse --verify --quiet "$head_ref^{commit}" >/dev/null || fail "head-ревизия '$head_ref' недоступна"

merge_base="$(git merge-base "$base_commit" "$head_ref")" ||
  fail "не найден merge-base между '$base_ref' и '$head_ref'; нужен checkout с fetch-depth: 0"

violations=()
added=()
allowed=()

while IFS=$'\t' read -r status path rename_target; do
  [[ -z "${status:-}" || -z "${path:-}" ]] && continue
  # Для переименований git печатает старый и новый путь; проверяются оба.
  local_paths=("$path")
  [[ -n "${rename_target:-}" ]] && local_paths+=("$rename_target")

  for candidate in "${local_paths[@]}"; do
    is_protected "$candidate" || continue
    case "${status:0:1}" in
      A)
        added+=("$candidate")
        ;;
      M)
        if is_allowlisted_path "$candidate"; then
          allowed+=("$candidate (явный allowlist)")
        elif is_pre_decision_record "$candidate"; then
          allowed+=("$candidate (запись до decision gate)")
        elif is_compatibility_redirect "$candidate"; then
          allowed+=("$candidate (совместимый редирект)")
        else
          violations+=("$candidate — изменение существующего исторического документа")
        fi
        ;;
      D)
        if is_allowlisted_path "$candidate"; then
          allowed+=("$candidate (явный allowlist)")
        else
          violations+=("$candidate — удаление существующего исторического документа")
        fi
        ;;
      R)
        if is_allowlisted_path "$candidate"; then
          allowed+=("$candidate (явный allowlist)")
        else
          violations+=("$candidate — переименование существующего исторического документа")
        fi
        ;;
      *)
        if is_allowlisted_path "$candidate"; then
          allowed+=("$candidate (явный allowlist)")
        else
          violations+=("$candidate — изменение существующего исторического документа (статус $status)")
        fi
        ;;
    esac
  done
done < <(git diff --name-status -M "$merge_base" "$head_ref")

if ((${#added[@]} > 0)); then
  printf 'Добавленные исторические документы (%s):\n' "${#added[@]}"
  printf '  + %s\n' "${added[@]}"
fi

if ((${#allowed[@]} > 0)); then
  printf 'Разрешённые изменения (%s):\n' "${#allowed[@]}"
  printf '  ~ %s\n' "${allowed[@]}"
fi

if ((${#violations[@]} > 0)); then
  printf 'ERROR: pull request изменяет исторические документы (%s):\n' "${#violations[@]}" >&2
  printf '  - %s\n' "${violations[@]}" >&2
  printf 'Исторические документы иммутабельны: RFC/ADR фиксируют решение на момент принятия.\n' >&2
  printf 'Устаревшее решение заменяется НОВЫМ RFC/ADR, а старый файл не переписывается.\n' >&2
  printf 'Исключение — совместимый редирект: frontmatter status: deprecated|superseded,\n' >&2
  printf 'тело не длиннее %s непустых строк и содержит ссылку на актуальный артефакт.\n' \
    "$DEPRECATED_REDIRECT_MAX_BODY_LINES" >&2
  printf 'Второе исключение — запись до decision gate: status draft|proposed в base-ревизии.\n' >&2
  exit 1
fi

printf 'Иммутабельность исторических документов подтверждена относительно %s (merge-base %s).\n' \
  "$base_ref" "${merge_base:0:12}"
printf 'Historical immutability check passed.\n'
