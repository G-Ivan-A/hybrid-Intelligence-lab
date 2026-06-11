#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

SITE_DIR="${1:-site}"

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

require_file() {
  local path="$1"
  [[ -f "$path" ]] || fail "missing generated site file: $path"
}

tracked_html="$(git ls-files '*.html' | while IFS= read -r path; do
  [[ ! -e "$path" ]] || printf '%s\n' "$path"
done)"
if [[ -n "$tracked_html" ]]; then
  printf '%s\n' "$tracked_html" >&2
  fail "generated HTML files must not be tracked in main"
fi

DISABLE_MKDOCS_2_WARNING=true mkdocs build --site-dir "$SITE_DIR"

require_file "$SITE_DIR/index.html"
require_file "$SITE_DIR/guides/index.html"
require_file "$SITE_DIR/research/index.html"
require_file "$SITE_DIR/search/search_index.json"
require_file "$SITE_DIR/stylesheets/extra.css"

[[ ! -e "$SITE_DIR/governance" ]] || fail "governance/ must not be published"
[[ ! -e "$SITE_DIR/standards" ]] || fail "standards/ must not be published"

grep -Fq 'class="md-search"' "$SITE_DIR/index.html" || fail "search UI is missing from generated HTML"
grep -Fq "md-sidebar" "$SITE_DIR/index.html" || fail "sidebar navigation is missing from generated HTML"
grep -Fq "word-break: break-word" "$SITE_DIR/stylesheets/extra.css" || fail "responsive table wrapping CSS is missing"

printf 'MkDocs site validation passed.\n'
