#!/usr/bin/env bash
set -euo pipefail
shopt -s extglob

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

warnings=0

required_fields=(
  "status"
  "version"
  "updated"
  "ai-generated"
)

warn() {
  local path="$1"
  local line="$2"
  local message="$3"

  printf '%s:%s: WARN: %s\n' "$path" "$line" "$message" >&2
  warnings=$((warnings + 1))
}

trim_value() {
  local value="$1"

  value="${value%%#*}"
  value="${value//$'\r'/}"
  value="${value##+([[:space:]])}"
  value="${value%%+([[:space:]])}"

  if [[ "$value" =~ ^\"(.*)\"$ ]]; then
    value="${BASH_REMATCH[1]}"
  elif [[ "$value" =~ ^\'(.*)\'$ ]]; then
    value="${BASH_REMATCH[1]}"
  fi

  printf '%s' "$value"
}

is_required_field() {
  local key="$1"

  case "$key" in
    status | version | updated | ai-generated)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

validate_field() {
  local path="$1"
  local field="$2"
  local line="$3"
  local value="$4"

  case "$field" in
    status)
      case "$value" in
        draft | reviewed | published | superseded | canonical)
          ;;
        *)
          warn "$path" "$line" "invalid status '$value' (expected one of: draft, reviewed, published, superseded, canonical)"
          ;;
      esac
      ;;
    version)
      if [[ ! "$value" =~ ^[0-9]+\.[0-9]+(\.[0-9]+)?$ ]]; then
        warn "$path" "$line" "invalid version '$value' (expected SemVer X.Y or X.Y.Z)"
      fi
      ;;
    updated)
      if [[ ! "$value" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        warn "$path" "$line" "invalid updated '$value' (expected ISO8601 date YYYY-MM-DD)"
      fi
      ;;
    ai-generated)
      case "$value" in
        true | false)
          ;;
        *)
          warn "$path" "$line" "invalid ai-generated '$value' (expected true or false)"
          ;;
      esac
      ;;
  esac
}

validate_file() {
  local path="$1"
  local line=""
  local line_no=0
  local closed=0
  declare -A values=()
  declare -A lines=()

  if [[ ! "$path" == *.md ]]; then
    warn "$path" 1 "not a markdown file"
    return
  fi

  if [[ ! -f "$path" ]]; then
    warn "$path" 1 "file does not exist"
    return
  fi

  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    line_no=$((line_no + 1))

    if [[ "$line_no" -eq 1 ]]; then
      if [[ "$line" != "---" ]]; then
        warn "$path" 1 "missing frontmatter block"
        return
      fi
      continue
    fi

    if [[ "$line" == "---" ]]; then
      closed=1
      break
    fi

    if [[ "$line" =~ ^[[:space:]]*([A-Za-z0-9_-]+)[[:space:]]*:(.*)$ ]]; then
      local key="${BASH_REMATCH[1]}"
      local raw_value="${BASH_REMATCH[2]}"

      if is_required_field "$key" && [[ -z "${lines[$key]+set}" ]]; then
        lines["$key"]="$line_no"
        values["$key"]="$(trim_value "$raw_value")"
      fi
    fi
  done < "$path"

  if [[ "$line_no" -eq 0 ]]; then
    warn "$path" 1 "missing frontmatter block"
    return
  fi

  if [[ "$closed" -eq 0 ]]; then
    warn "$path" 1 "frontmatter block is not closed"
    return
  fi

  local field
  for field in "${required_fields[@]}"; do
    if [[ -z "${lines[$field]+set}" ]]; then
      warn "$path" 1 "missing required frontmatter field: $field"
      continue
    fi

    validate_field "$path" "$field" "${lines[$field]}" "${values[$field]}"
  done
}

collect_files() {
  local target="$1"

  if [[ -d "$target" ]]; then
    find "$target" -type f -name '*.md' | sort
  else
    printf '%s\n' "$target"
  fi
}

main() {
  local targets=("$@")

  if [[ "${#targets[@]}" -eq 0 ]]; then
    targets=(".")
  fi

  local target
  while IFS= read -r target; do
    validate_file "$target"
  done < <(
    for target in "${targets[@]}"; do
      if [[ -d "$target" ]]; then
        collect_files "$target"
      elif [[ -e "$target" ]]; then
        collect_files "$target"
      else
        printf '%s\n' "$target"
      fi
    done
  )

  if [[ "$warnings" -gt 0 ]]; then
    printf 'Frontmatter validation completed with %d warning(s).\n' "$warnings" >&2
  else
    printf 'Frontmatter validation passed.\n'
  fi

  exit 0
}

main "$@"
