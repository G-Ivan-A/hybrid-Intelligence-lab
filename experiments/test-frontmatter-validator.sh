#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

tmp_dirs=()
cleanup() {
  local dir
  for dir in "${tmp_dirs[@]}"; do
    rm -rf "$dir"
  done
}
trap cleanup EXIT

make_tmp_dir() {
  local __resultvar="$1"
  local parent="$2"
  local dir
  dir="$(mktemp -d "$parent/.frontmatter-test.XXXXXX")"
  tmp_dirs+=("$dir")
  printf -v "$__resultvar" '%s' "$dir"
}

write_doc() {
  local path="$1"
  local frontmatter="$2"

  {
    printf '%s\n' '---'
    printf '%s\n' "$frontmatter"
    printf '%s\n' '---'
    printf '%s\n' '# Fixture'
  } > "$path"
}

expect_pass() {
  local label="$1"
  local path="$2"

  if ! ./tools/validate-frontmatter.sh "$path" > /tmp/frontmatter-test.out 2> /tmp/frontmatter-test.err; then
    printf 'Expected pass for %s, got failure:\n' "$label" >&2
    cat /tmp/frontmatter-test.err >&2
    exit 1
  fi
}

expect_fail() {
  local label="$1"
  local path="$2"
  local expected="$3"

  if ./tools/validate-frontmatter.sh "$path" > /tmp/frontmatter-test.out 2> /tmp/frontmatter-test.err; then
    printf 'Expected failure for %s, got pass.\n' "$label" >&2
    exit 1
  fi

  if ! grep -Fq "$expected" /tmp/frontmatter-test.err; then
    printf 'Expected failure for %s to contain:\n%s\nActual stderr:\n' "$label" "$expected" >&2
    cat /tmp/frontmatter-test.err >&2
    exit 1
  fi
}

make_tmp_dir knowledge_dir research
make_tmp_dir governance_dir standards
make_tmp_dir adr_dir docs/adr
make_tmp_dir rfc_dir governance/rfc

write_doc "$knowledge_dir/valid.md" "status: reviewed
version: 1.0
updated: 2026-06-28
temperature: 0.1"
expect_pass "valid knowledge status" "$knowledge_dir/valid.md"

write_doc "$governance_dir/valid.md" "status: accepted
version: 1.0
updated: 2026-06-28
temperature: 0.1
owner: Governance"
expect_pass "valid governance status and owner" "$governance_dir/valid.md"

write_doc "$knowledge_dir/invalid-status.md" "status: accepted
version: 1.0
updated: 2026-06-28
temperature: 0.1"
expect_fail "knowledge vocabulary" "$knowledge_dir/invalid-status.md" "invalid knowledge status 'accepted'"

write_doc "$governance_dir/invalid-status.md" "status: canonical
version: 1.0
updated: 2026-06-28
temperature: 0.1
owner: Governance"
expect_fail "governance vocabulary" "$governance_dir/invalid-status.md" "invalid governance status 'canonical'"

write_doc "$governance_dir/missing-owner.md" "status: accepted
version: 1.0
updated: 2026-06-28
temperature: 0.1"
expect_fail "governance owner" "$governance_dir/missing-owner.md" "missing required frontmatter field for governance artifact: owner"

write_doc "$adr_dir/missing-decision-type.md" "status: accepted
version: 1.0
updated: 2026-06-28
temperature: 0.1
owner: Governance"
expect_fail "ADR decision type" "$adr_dir/missing-decision-type.md" "missing required frontmatter field for ADR artifact: decision-type"

write_doc "$rfc_dir/missing-rfc-scope.md" "status: proposed
version: 1.0
updated: 2026-06-28
temperature: 0.1
owner: Governance"
expect_fail "RFC scope" "$rfc_dir/missing-rfc-scope.md" "missing required frontmatter field for RFC artifact: rfc-scope"

write_doc "$knowledge_dir/ai-generated.md" "status: reviewed
version: 1.0
updated: 2026-06-28
temperature: 0.1
ai-generated: true"
expect_fail "ai-generated ban" "$knowledge_dir/ai-generated.md" "frontmatter field is forbidden: ai-generated"

write_doc "$knowledge_dir/unknown-field.md" "status: reviewed
version: 1.0
updated: 2026-06-28
temperature: 0.1
unexpected: value"
expect_fail "approved field list" "$knowledge_dir/unknown-field.md" "frontmatter field is not approved for this document class: unexpected"

printf 'Frontmatter validator regression tests passed.\n'
