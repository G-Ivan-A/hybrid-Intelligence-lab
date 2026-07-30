#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

tmp_out="$(mktemp)"
tmp_err="$(mktemp)"

cleanup() {
  rm -rf governance website experiments mkdocs.yml "$tmp_out" "$tmp_err"
}
trap cleanup EXIT

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  if [[ -s "$tmp_out" ]]; then
    printf '\nstdout:\n' >&2
    cat "$tmp_out" >&2
  fi
  if [[ -s "$tmp_err" ]]; then
    printf '\nstderr:\n' >&2
    cat "$tmp_err" >&2
  fi
  exit 1
}

for legacy_path in governance website experiments mkdocs.yml; do
  if [[ -e "$legacy_path" ]]; then
    fail "cannot run legacy-path test while $legacy_path already exists"
  fi
done

mkdir governance website experiments
: > mkdocs.yml

if ./tools/validate-repository-structure.sh >"$tmp_out" 2>"$tmp_err"; then
  fail "expected repository structure validator to reject ADR-007 legacy root paths"
fi

for expected in \
  "forbidden legacy path present: governance" \
  "forbidden legacy path present: website" \
  "forbidden legacy path present: experiments" \
  "forbidden legacy path present: mkdocs.yml"; do
  if ! grep -Fq "$expected" "$tmp_err"; then
    fail "missing expected validator error: $expected"
  fi
done

cleanup
trap - EXIT

if grep -nE 'require_text[[:space:]]+"[^"]+"[[:space:]]+"governance/' tools/validate-repository-structure.sh; then
  fail "structure validator must not require migrated root governance/ paths"
fi

if grep -nF 'governance/rfc/' tools/validate-file-naming.sh; then
  fail "file-naming validator must not keep stale governance/rfc/ comments"
fi

for required_path in \
  "projects-sink" \
  "ai-governance" \
  "ai-rules" \
  "pr-ops" \
  "docs/rfc" \
  "docs/guides"; do
  if ! grep -Fq "\"$required_path\"" tools/validate-repository-structure.sh; then
    fail "structure validator must require ADR-007 path: $required_path"
  fi
done

backlog_file="pr-ops/backlog.md"

b053_line="$(grep -F '| **B-053** |' "$backlog_file")"
[[ "$b053_line" == *'| DONE |'* ]] ||
  fail "B-053 must be DONE after merged PR #452"

b085_line="$(grep -F '| **B-085** |' "$backlog_file")"
for expected in \
  "research/ai-education/retrieval/" \
  "docs/rfc/2026-07-17-rfc-reference-research-pattern.md" \
  "Conceptual Framing" \
  "S = Decision(KB, Query, Constraints)"; do
  if [[ "$b085_line" != *"$expected"* ]]; then
    fail "B-085 must contain current-state evidence: $expected"
  fi
done

if grep -Fq \
  'Результат: `research/education/2026-07-16-retrieval-strategies-survey.md`' \
  "$backlog_file"; then
  fail "B-085 must not name the superseded monolith as its result"
fi

grep -Fq '| **B-090** |' "$backlog_file" ||
  fail "B-090 must remain in the active backlog"

printf 'Post-migration validator regression tests passed.\n'
