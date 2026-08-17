#!/usr/bin/env bash
set -euo pipefail

# Reference Research Pattern, rule P2 (docs/rfc/2026-07-17-rfc-reference-research-pattern.md):
# the practice branch of a module must explicitly reference its own foundation.
# The rule lived only in the RFC and was therefore honoured in 3 of 8 modules —
# cross-validation reports for issue #505 and issue #506 showed that exactly what
# CI checks is what gets done. This validator makes P2 machine-checkable.
#
# Check is deliberately trivial (Anti-Inflation): at least one relative markdown
# link from the module's practice file (40-*.md) to a theory-branch file
# (10-*.md, 20-*.md, 30-*.md) in the same module directory. No AST parsing.
#
# Existing violations are grandfathered in BASELINE_VIOLATIONS: the modules are
# research text and issue #506 forbids editing them, so the deviation is recorded
# rather than silently fixed. The list is a ratchet — a new module must satisfy
# P2, and a baseline module that starts satisfying it must be removed from the
# list, otherwise this validator fails.

ROOT_DIR="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
cd "$ROOT_DIR"

SEARCH_ROOT="${RRP_SEARCH_ROOT:-research}"

# Modules that violated P2 before the rule became machine-checkable.
# Attribution and evidence: research/hub/2026-08-13-rrp-cross-validation-codex.md
# and research/hub/2026-08-13-rrp-cross-validation-claude-opus-4-8.md.
BASELINE_VIOLATIONS_DEFAULT=(
  "research/ai-education/evaluation"
  "research/ai-education/information-extraction-graph-modeling"
  "research/ai-education/observability"
  "research/ai-education/tool-use"
)

if [[ -n "${RRP_BASELINE_OVERRIDE-}" ]]; then
  # Test hook: whitespace-separated module paths, "none" for an empty baseline.
  if [[ "$RRP_BASELINE_OVERRIDE" == "none" ]]; then
    BASELINE_VIOLATIONS=()
  else
    read -r -a BASELINE_VIOLATIONS <<< "$RRP_BASELINE_OVERRIDE"
  fi
else
  BASELINE_VIOLATIONS=("${BASELINE_VIOLATIONS_DEFAULT[@]}")
fi

failures=0

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  failures=$((failures + 1))
}

warn() {
  printf 'WARNING: %s\n' "$1" >&2
}

is_baseline_violation() {
  local module="$1"
  local known

  for known in ${BASELINE_VIOLATIONS[@]+"${BASELINE_VIOLATIONS[@]}"}; do
    [[ "$module" == "$known" ]] && return 0
  done

  return 1
}

# A module declares itself by holding a 00-*.md entry point, the same signal
# validate-file-naming.sh uses to recognise a Reference Research Pattern module.
count_foundation_links() {
  local practice_file="$1"

  # grep exits 1 on no match, which is a legitimate result here, not an error.
  grep -cE '\]\((10|20|30)-[a-z0-9]+(-[a-z0-9]+)*\.md(#[^)]*)?\)' "$practice_file" || true
}

modules_checked=0

if [[ -d "$SEARCH_ROOT" ]]; then
  while IFS= read -r intro_file; do
    module="${intro_file%/*}"
    modules_checked=$((modules_checked + 1))

    practice_file=""
    while IFS= read -r candidate; do
      practice_file="$candidate"
      break
    done < <(find "$module" -maxdepth 1 -type f -name '40-*.md' | sort)

    if [[ -z "$practice_file" ]]; then
      # P1 lists a practice file among the six; a module without it has no
      # place for P2 to hold, so the gap is reported rather than skipped.
      fail "RRP module has no practice file (40-*.md), P2 cannot hold: $module"
      continue
    fi

    links="$(count_foundation_links "$practice_file")"

    if (( links > 0 )); then
      if is_baseline_violation "$module"; then
        fail "module now satisfies P2 and must be removed from BASELINE_VIOLATIONS in tools/validate-rrp-links.sh: $module"
      fi
      continue
    fi

    if is_baseline_violation "$module"; then
      warn "known P2 deviation (grandfathered, human decision pending): $practice_file has no markdown link to 10-/20-/30-*.md"
      continue
    fi

    fail "P2 violated: $practice_file has no markdown link to a theory-branch file (10-*.md, 20-*.md, 30-*.md) of its own module"
  done < <(find "$SEARCH_ROOT" -type f -name '00-*.md' | sort)
fi

if (( failures > 0 )); then
  printf 'RRP link validation failed with %d error(s).\n' "$failures" >&2
  exit 1
fi

printf 'RRP link validation passed (%d module(s) checked).\n' "$modules_checked"
