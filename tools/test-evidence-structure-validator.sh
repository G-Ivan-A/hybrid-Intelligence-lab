#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

tmp_root="$(mktemp -d)"
trap 'rm -rf "$tmp_root"' EXIT

expect_fail() {
  local label="$1"
  local expected="$2"

  if RESEARCH_ROOT="$tmp_root/research" ./tools/validate-evidence-structure.sh >"$tmp_root/out" 2>"$tmp_root/err"; then
    printf 'Expected failure for %s, got pass.\n' "$label" >&2
    exit 1
  fi

  if ! grep -Fq "$expected" "$tmp_root/err"; then
    printf 'Expected failure for %s to contain %s.\n' "$label" "$expected" >&2
    sed -n '1,200p' "$tmp_root/err" >&2
    exit 1
  fi
}

mkdir -p "$tmp_root/research/hub/exp-legacy-123"
expect_fail "legacy exp sibling" "legacy experiment directory"
rm -rf "$tmp_root/research"

mkdir -p "$tmp_root/research/hub/exp/example-123/outputs"
expect_fail "outputs directory" "forbidden outputs directory"
rm -rf "$tmp_root/research"

mkdir -p "$tmp_root/research/hub/exp/example-123"
printf '%s\n' '# Evidence' > "$tmp_root/research/hub/exp/example-123/README.md"
expect_fail "missing parent report link" "must link to a parent dated research report"
rm -rf "$tmp_root/research"

mkdir -p "$tmp_root/research/hub/exp/example-123"
printf '%s\n' '[Parent](../../2026-07-17-example.md)' > "$tmp_root/research/hub/exp/example-123/README.md"
RESEARCH_ROOT="$tmp_root/research" ./tools/validate-evidence-structure.sh >/dev/null

rm -rf "$tmp_root/research"
mkdir -p "$tmp_root/research/hub/exp/example-123/data"
printf '%s\n' '[Parent](../../../../docs/analysis/2026-07-17-example.md)' > "$tmp_root/research/hub/exp/example-123/README.md"
RESEARCH_ROOT="$tmp_root/research" ./tools/validate-evidence-structure.sh >/dev/null

printf 'Evidence structure validator regression tests passed.\n'
