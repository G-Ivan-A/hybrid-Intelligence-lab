#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

tmp_out="$(mktemp)"
tmp_err="$(mktemp)"

cleanup() {
  rm -rf governance website experiments pr-ops mkdocs.yml "$tmp_out" "$tmp_err"
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

for legacy_path in governance website experiments pr-ops mkdocs.yml; do
  if [[ -e "$legacy_path" ]]; then
    fail "cannot run legacy-path test while $legacy_path already exists"
  fi
done

if ! ./tools/validate-repository-structure.sh >"$tmp_out" 2>"$tmp_err"; then
  fail "structure validator must accept the current tracked repository before testing legacy paths"
fi

mkdir governance website experiments pr-ops
: > mkdocs.yml

if ./tools/validate-repository-structure.sh >"$tmp_out" 2>"$tmp_err"; then
  fail "expected repository structure validator to reject ADR-007 legacy root paths"
fi

for expected in \
  "forbidden legacy path present: governance" \
  "forbidden legacy path present: website" \
  "forbidden legacy path present: experiments" \
  "forbidden legacy path present: pr-ops" \
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

if grep -Fq '"pr-ops/README.md"' tools/validate-repository-structure.sh; then
  fail "structure validator must not keep the retired pr-ops compatibility pointer exception"
fi

if [[ -e "pr-ops" ]]; then
  fail "legacy pr-ops/ directory must be removed after the compatibility cycle"
fi

for required_path in \
  "projects-sink" \
  "ai-governance" \
  "ai-rules" \
  "ops" \
  "docs/rfc" \
  "docs/guides"; do
  if ! grep -Fq "\"$required_path\"" tools/validate-repository-structure.sh; then
    fail "structure validator must require ADR-007 path: $required_path"
  fi
done

backlog_file="ops/backlog.md"

# B-053 was DONE after merged PR #452 and its sprint (Спринт 3) is archived by
# issue #583. The regression to guard is resurrection of the archived task, not
# its status.
if grep -Fq '| **B-053** |' "$backlog_file"; then
  fail "B-053 must stay archived after issue #583 (Спринт 3 removed from the active backlog)"
fi

# Спринты 14–21 и 24–28 (B-173 included) moved to ba-ai-metamodel by B-247 and
# were removed from the Hub by the B-249 tombstone (issue #738). B-173 stays the
# declared trigger for B-068 and B-070, so the Hub must point to the spoke backlog
# instead of resurrecting the rows.
grep -Fq '## Спринты 14–21, 24–28: Перенесены в ba-ai-metamodel' "$backlog_file" ||
  fail "moved BA sprints must keep a pointer to the ba-ai-metamodel backlog"

if grep -Fq '| **B-173** |' "$backlog_file"; then
  fail "B-173 lives in the ba-ai-metamodel backlog after B-249 (issue #738)"
fi

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

if grep -Fq '| **B-090** |' "$backlog_file"; then
  fail "B-090 must stay archived after issue #747"
fi

duplicate_ids="$(sed -nE 's/^\| \*\*(B-[0-9]+)\*\* \|.*/\1/p' "$backlog_file" | sort | uniq -d)"
if [[ -n "$duplicate_ids" ]]; then
  fail "active Hub backlog contains duplicate IDs: $duplicate_ids"
fi

if ! awk -F ' [|] ' '
  /^\| \*\*B-[0-9]+\*\* \| / && toupper($5) == "TODO" && $5 != "TODO" {
    print "Noncanonical TODO status on line " NR ": " $1
    invalid = 1
  }
  END { exit invalid }
' "$backlog_file"; then
  fail "active Hub backlog must spell TODO in uppercase"
fi

printf 'Post-migration validator regression tests passed.\n'
