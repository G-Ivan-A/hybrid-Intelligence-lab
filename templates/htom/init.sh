#!/usr/bin/env bash
#
# init.sh — инициализация HTOM-команды из «ДНК-шаблона» Хаба `hybrid-Intelligence-lab`.
#
# Креативное улучшение UX инициализации: один запуск заменяет плейсхолдеры во
# всех файлах шаблона и проставляет дату, чтобы новая HTOM-команда рождалась уже
# «правильной», без ручного поиска {{...}} по дереву.
#
# Заменяемые плейсхолдеры:
#   {{project_name}}         — имя проекта
#   {{hub_url}}              — ссылка на Хаб (источник истины)
#   {{date}}                 — текущая дата (YYYY-MM-DD), автоген
# Заполняемые поля:
#   README description       — одно-двухстрочное описание проекта
#
# Использование:
#   ./init.sh                                  # интерактивно (спросит значения)
#   ./init.sh --name "My HTOM Team"            # частично через флаги
#   ./init.sh -n "My HTOM Team" -d "..." -u "URL" --yes   # неинтерактивно (для CI)
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

DEFAULT_HUB_URL="https://github.com/G-Ivan-A/hybrid-Intelligence-lab"

project_name=""
project_description=""
hub_url=""
assume_yes=0

usage() {
  sed -n '2,28p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -n|--name)        project_name="${2:-}"; shift 2;;
    -d|--description) project_description="${2:-}"; shift 2;;
    -u|--hub-url)     hub_url="${2:-}"; shift 2;;
    -y|--yes)         assume_yes=1; shift;;
    -h|--help)        usage; exit 0;;
    *) printf 'Unknown argument: %s\n' "$1" >&2; usage; exit 2;;
  esac
done

prompt_if_empty() {
  # $1 = current value (by name), $2 = prompt text, $3 = default
  local current="$1" text="$2" default="$3" answer=""
  if [[ -n "$current" ]]; then
    printf '%s' "$current"
    return 0
  fi
  if [[ "$assume_yes" -eq 1 || ! -t 0 ]]; then
    printf '%s' "$default"
    return 0
  fi
  if [[ -n "$default" ]]; then
    read -r -p "$text [$default]: " answer
    printf '%s' "${answer:-$default}"
  else
    read -r -p "$text: " answer
    printf '%s' "$answer"
  fi
}

project_name="$(prompt_if_empty "$project_name" "Имя проекта (project_name)" "")"
if [[ -z "$project_name" ]]; then
  printf 'FAIL: project_name обязателен.\n' >&2
  exit 1
fi
project_description="$(prompt_if_empty "$project_description" "Краткое описание проекта" "TODO: добавьте описание проекта.")"
hub_url="$(prompt_if_empty "$hub_url" "URL Хаба" "$DEFAULT_HUB_URL")"
today="$(date +%F)"

# Экранирование значений для использования в правой части sed (разделитель «|»).
sed_escape() {
  printf '%s' "$1" | sed -e 's/[\\&|]/\\&/g'
}
esc_name="$(sed_escape "$project_name")"
esc_desc="$(sed_escape "$project_description")"
esc_hub="$(sed_escape "$hub_url")"
esc_date="$(sed_escape "$today")"

# Портабельная in-place замена (без sed -i: работает и на GNU, и на BSD/macOS).
replace_in_file() {
  local file="$1" tmp
  tmp="$(mktemp)"
  sed \
    -e "s|{{project_name}}|$esc_name|g" \
    -e "s|TODO: добавьте краткое описание проекта после инициализации\\.|$esc_desc|g" \
    -e "s|{{hub_url}}|$esc_hub|g" \
    -e "s|{{date}}|$esc_date|g" \
    "$file" > "$tmp"
  cat "$tmp" > "$file"
  rm -f "$tmp"
}

changed=0
while IFS= read -r file; do
  if grep -Iq '{{[a-z_]*}}' "$file" 2>/dev/null; then
    replace_in_file "$file"
    printf '  • %s\n' "$file"
    changed=$((changed + 1))
  fi
done < <(find . -type f \
  -not -path './.git/*' \
  -not -name 'init.sh' \
  | sort)

printf '\n✅ Инициализирована HTOM-команда «%s» (%d файл(ов) обновлено, дата %s).\n' \
  "$project_name" "$changed" "$today"
printf '   Хаб: %s\n' "$hub_url"

# init.sh — одноразовый: после инициализации он не нужен в HTOM-команде.
remove_self() {
  rm -f "$SCRIPT_DIR/init.sh"
  printf '   init.sh удалён (одноразовый скрипт инициализации).\n'
}

if [[ "$assume_yes" -eq 1 ]]; then
  remove_self
elif [[ -t 0 ]]; then
  read -r -p "Удалить init.sh (он одноразовый)? [Y/n]: " ans
  case "${ans:-Y}" in
    [Nn]*) printf '   init.sh оставлен.\n';;
    *)     remove_self;;
  esac
fi

printf '\nДалее: запустите ./tools/validate-repository-structure.sh\n'
