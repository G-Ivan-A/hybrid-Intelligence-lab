#!/usr/bin/env bash
set -euo pipefail

# Regression tests for tools/validate-rrp-links.sh (Reference Research Pattern, rule P2).
# Each case builds a throwaway module fixture and asserts the validator's verdict,
# so the tests prove both directions: the check fires on a missing link and passes
# when the link is there.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

VALIDATOR="$ROOT_DIR/tools/validate-rrp-links.sh"

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

make_module() {
  local module="$1"
  local practice_body="$2"

  mkdir -p "$module"
  printf '# Introduction\n' > "$module/00-introduction.md"
  printf '# Theory\n' > "$module/10-theory.md"
  printf '# Taxonomy\n' > "$module/20-taxonomy.md"
  printf '# Decision framework\n' > "$module/30-decision-framework.md"
  printf '%s\n' "$practice_body" > "$module/40-practice-and-cases.md"
  printf '# Open research\n' > "$module/50-open-research.md"
}

run_validator() {
  local baseline="$1"

  RRP_SEARCH_ROOT=research RRP_BASELINE_OVERRIDE="$baseline" \
    bash "$VALIDATOR" "$WORKDIR"
}

# Case 1: practice file links to theory — P2 satisfied.
rm -rf "$WORKDIR/research"
make_module "$WORKDIR/research/ai-education/linked" \
  '# Practice

Основание практики — [теория](10-theory.md).'

if ! output="$(run_validator none 2>&1)"; then
  printf '%s\n' "$output" >&2
  fail "validator must pass when the practice file links to its foundation"
fi

# Case 2: practice file mentions the file name without a link — insufficient.
rm -rf "$WORKDIR/research"
make_module "$WORKDIR/research/ai-education/unlinked" \
  '# Practice

Основание описано в 10-theory.md, но ссылки нет.'

if output="$(run_validator none 2>&1)"; then
  printf '%s\n' "$output" >&2
  fail "validator must fail when the practice file has no markdown link to the theory branch"
fi

grep -Fq 'P2 violated' <<< "$output" ||
  fail "failure message must name the violated rule, got: $output"

# Case 3: a link to 20-*.md or 30-*.md counts as the foundation too.
for target in 20-taxonomy 30-decision-framework; do
  rm -rf "$WORKDIR/research"
  make_module "$WORKDIR/research/ai-education/linked-$target" \
    "# Practice

См. [основание]($target.md#раздел)."

  if ! output="$(run_validator none 2>&1)"; then
    printf '%s\n' "$output" >&2
    fail "validator must accept a link to $target.md as the practice foundation"
  fi
done

# Case 4: a known violation stays a warning while it is in the baseline.
rm -rf "$WORKDIR/research"
make_module "$WORKDIR/research/ai-education/grandfathered" \
  '# Practice

Ссылок на основание нет.'

if ! output="$(run_validator "research/ai-education/grandfathered" 2>&1)"; then
  printf '%s\n' "$output" >&2
  fail "baseline module must not break the build"
fi

grep -Fq 'known P2 deviation' <<< "$output" ||
  fail "baseline module must still be reported as a warning, got: $output"

# Case 5: ratchet — a baseline module that now satisfies P2 must leave the list.
rm -rf "$WORKDIR/research"
make_module "$WORKDIR/research/ai-education/grandfathered" \
  '# Practice

Основание практики — [теория](10-theory.md).'

if output="$(run_validator "research/ai-education/grandfathered" 2>&1)"; then
  printf '%s\n' "$output" >&2
  fail "validator must demand removal from the baseline once the module satisfies P2"
fi

grep -Fq 'BASELINE_VIOLATIONS' <<< "$output" ||
  fail "ratchet message must point at the baseline list, got: $output"

# Case 6: a module without a practice file is reported, not silently skipped.
rm -rf "$WORKDIR/research"
make_module "$WORKDIR/research/ai-education/no-practice" '# Practice'
rm "$WORKDIR/research/ai-education/no-practice/40-practice-and-cases.md"

if output="$(run_validator none 2>&1)"; then
  printf '%s\n' "$output" >&2
  fail "validator must report an RRP module without a practice file"
fi

grep -Fq 'no practice file' <<< "$output" ||
  fail "missing practice file must be named explicitly, got: $output"

# Case 7: the real repository corpus passes with its documented baseline.
if ! output="$(bash "$VALIDATOR" 2>&1)"; then
  printf '%s\n' "$output" >&2
  fail "repository corpus must pass with the documented baseline"
fi

printf 'RRP link validator regression tests passed.\n'
