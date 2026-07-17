#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESEARCH_ROOT="${RESEARCH_ROOT:-$ROOT_DIR/research}"
failures=0

[[ -d "$RESEARCH_ROOT" ]] || {
  printf 'Evidence structure validation passed.\n'
  exit 0
}

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  failures=$((failures + 1))
}

while IFS= read -r path; do
  fail "legacy experiment directory: ${path#"$ROOT_DIR/"} (use research/<domain>/exp/<issue-slug>/)"
done < <(find "$RESEARCH_ROOT" -type d -name 'exp-*' -print | sort)

while IFS= read -r path; do
  fail "forbidden outputs directory: ${path#"$ROOT_DIR/"} (keep evidence flat inside exp/<issue-slug>/)"
done < <(find "$RESEARCH_ROOT" -type d -name outputs -print | sort)

while IFS= read -r experiment; do
  readme="$experiment/README.md"
  if [[ ! -f "$readme" ]]; then
    fail "experiment must contain README.md: ${experiment#"$ROOT_DIR/"}"
    continue
  fi
  if ! grep -Eq '\]\((\.\./\.\./|\.\./\.\./\.\./\.\./docs/(analysis|audit|report)/)[0-9]{4}-[0-9]{2}-[0-9]{2}-[^)#]+\.md(#[^)]+)?\)' "$readme"; then
    fail "experiment README must link to a parent dated research report: ${readme#"$ROOT_DIR/"}"
  fi
done < <(find "$RESEARCH_ROOT" -type d -mindepth 3 -maxdepth 3 -path '*/exp/*' -print | sort)

if (( failures > 0 )); then
  printf 'Evidence structure validation failed with %d error(s).\n' "$failures" >&2
  exit 1
fi

printf 'Evidence structure validation passed.\n'
