#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

failures=0

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  failures=$((failures + 1))
}

assert_file() {
  local path="$1"
  [[ -f "$ROOT_DIR/$path" ]] || fail "required integration artifact is missing: $path"
}

# The compatibility cycle for the pr-ops/ -> ops/ migration is over (issue #585):
# the deprecated pointer must be gone, not merely reduced to a single README.md.
assert_removed_legacy_directory() {
  local path="$1"
  [[ ! -e "$ROOT_DIR/$path" ]] || fail "legacy compatibility directory must be removed after the sync cycle: $path"
}

expect_validator_failure() {
  local name="$1"
  local repo="$2"
  local expected="$3"
  local output="$TMP_DIR/${name}.log"
  if "$ROOT_DIR/tools/validate-agents-bootstrap.sh" "$repo" >"$output" 2>&1; then
    fail "$name: validator unexpectedly passed"
    return
  fi
  if ! grep -Fq -- "$expected" "$output"; then
    fail "$name: validator failed for the wrong reason (expected: $expected)"
  fi
}

assert_file "AGENTS.md"
assert_file ".hub-profile.json"
assert_file "ai-rules/agent-work-routing.md"
assert_file "standards/agents-md-bootstrap-standard.md"
assert_file "templates/htom/AGENTS.md"
assert_file "templates/htom/.hub-profile.json"
assert_file "templates/spoke/AGENTS.md"
assert_file "templates/spoke/.hub-profile.json"
assert_file "projects-sink/agents-md/README.md"
assert_file "projects-sink/agents-md/synchronization-rules.md"
assert_file "projects-sink/agents-md/templates/project-agents-md-template.md"
assert_removed_legacy_directory "pr-ops"

if ! "$ROOT_DIR/tools/validate-repository-structure.sh" \
  >"$TMP_DIR/repository-structure.log" 2>&1; then
  fail "repository structure validator rejects the integrated bootstrap or path migration"
fi

if [[ -f "$ROOT_DIR/AGENTS.md" && -f "$ROOT_DIR/.hub-profile.json" ]]; then
  missing_agents="$TMP_DIR/missing-agents"
  mkdir -p "$missing_agents"
  cp "$ROOT_DIR/.hub-profile.json" "$missing_agents/.hub-profile.json"
  expect_validator_failure "missing-agents" "$missing_agents" "missing file: AGENTS.md"

  missing_profile="$TMP_DIR/missing-profile"
  mkdir -p "$missing_profile"
  cp "$ROOT_DIR/AGENTS.md" "$missing_profile/AGENTS.md"
  expect_validator_failure "missing-profile" "$missing_profile" "missing file: .hub-profile.json"

  environment_mismatch="$TMP_DIR/environment-mismatch"
  mkdir -p "$environment_mismatch"
  cp "$ROOT_DIR/AGENTS.md" "$environment_mismatch/AGENTS.md"
  cp "$ROOT_DIR/.hub-profile.json" "$environment_mismatch/.hub-profile.json"
  python3 - "$environment_mismatch/.hub-profile.json" <<'PY'
import json
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as source:
    profile = json.load(source)
profile["environment"] = "gigacode"
with open(path, "w", encoding="utf-8") as target:
    json.dump(profile, target, ensure_ascii=False, indent=2)
    target.write("\n")
PY
  expect_validator_failure \
    "environment-mismatch" \
    "$environment_mismatch" \
    "AGENTS.md environment must match .hub-profile.json"

  declared_directories="$TMP_DIR/declared-directories"
  mkdir -p "$declared_directories"
  cp "$ROOT_DIR/AGENTS.md" "$declared_directories/AGENTS.md"
  cp "$ROOT_DIR/.hub-profile.json" "$declared_directories/.hub-profile.json"
  mkdir "$declared_directories/plans" "$declared_directories/tasks"
  python3 - "$declared_directories/.hub-profile.json" <<'PY'
import json
import sys

path = sys.argv[1]
with open(path, encoding="utf-8") as source:
    profile = json.load(source)
profile["project_specific_directories"] = [
    {"path": "plans", "reason": "Project-local planning artifacts"},
    {"path": "tasks", "reason": "Project-local task artifacts"},
]
with open(path, "w", encoding="utf-8") as target:
    json.dump(profile, target, ensure_ascii=False, indent=2)
    target.write("\n")
PY
  if ! "$ROOT_DIR/tools/validate-agents-bootstrap.sh" "$declared_directories" \
    >"$TMP_DIR/declared-directories.log" 2>&1; then
    fail "generic directory declarations rejected plans/ or tasks/"
  fi
fi

GENERAL_LAYER_SECTIONS=(hard_rules forbidden guidelines hybrid_work)
REQUIRED_SECTIONS=(scope hard_rules forbidden guidelines hybrid_work project_specific_rules routing artifact_homes issue_levels missing_tags context_scope validation models escalation)

assert_sections() {
  local path="$1"
  local section
  for section in "${REQUIRED_SECTIONS[@]}"; do
    grep -Fq "<$section>" "$ROOT_DIR/$path" \
      || fail "$path is missing the required section <$section>"
    grep -Fq "</$section>" "$ROOT_DIR/$path" \
      || fail "$path is missing the closing tag </$section>"
  done
}

for agents_path in AGENTS.md templates/htom/AGENTS.md templates/spoke/AGENTS.md; do
  assert_sections "$agents_path"
done

# The Hub-specific research-boundary rule must live in the project layer only, and
# must not be shipped into spokes through the general layer of a template.
if ! sed -n '/<project_specific_rules>/,/<\/project_specific_rules>/p' "$ROOT_DIR/AGENTS.md" \
  | grep -q 'expands the considered boundary'; then
  fail "the Hub research-boundary rule must live inside <project_specific_rules> of AGENTS.md"
fi
for template in templates/htom/AGENTS.md templates/spoke/AGENTS.md; do
  if grep -q 'expands the considered boundary' "$ROOT_DIR/$template"; then
    fail "$template must not ship the Hub-specific research-boundary rule"
  fi
  if ! sed -n '/<project_specific_rules>/,/<\/project_specific_rules>/p' "$ROOT_DIR/$template" \
    | grep -q 'REQUIRED: define the rules of THIS project here'; then
    fail "$template must reserve <project_specific_rules> with an explicit placeholder"
  fi
done

# The size threshold is normed in the structure standard, not restated in the entrypoint.
for agents_path in AGENTS.md templates/htom/AGENTS.md templates/spoke/AGENTS.md; do
  if grep -Eq '4K tokens|8K tokens|4,000|8,000' "$ROOT_DIR/$agents_path"; then
    fail "$agents_path must not restate the size thresholds; they belong to the structure standard"
  fi
done
if ! grep -Fq "4,000 estimated tokens" "$ROOT_DIR/standards/agents-md-bootstrap-standard.md"; then
  fail "standards/agents-md-bootstrap-standard.md must norm the size thresholds"
fi

# A dropped general-layer section is a validator failure, not a silent pass.
if [[ -f "$ROOT_DIR/AGENTS.md" && -f "$ROOT_DIR/.hub-profile.json" ]]; then
  for section in "${GENERAL_LAYER_SECTIONS[@]}"; do
    dropped="$TMP_DIR/dropped-$section"
    mkdir -p "$dropped"
    cp "$ROOT_DIR/.hub-profile.json" "$dropped/.hub-profile.json"
    sed "/^<$section>$/,/^<\/$section>$/d" "$ROOT_DIR/AGENTS.md" >"$dropped/AGENTS.md"
    # The open tag is also mentioned in the prose of <scope>, so the closing tag is
    # the signal that the section body itself is gone.
    expect_validator_failure \
      "dropped-$section" \
      "$dropped" \
      "AGENTS.md missing section: </$section>"
  done
fi

if [[ -d "$ROOT_DIR/ops" ]]; then
  if git -C "$ROOT_DIR" grep -n 'pr-ops/' -- . \
    ':(exclude)CHANGELOG.md' \
    ':(exclude)docs/superpowers/plans/2026-09-09-agents-md-physical-integration.md' \
    ':(exclude)docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md' \
    ':(exclude)docs/rfc/2026-09-03-rfc-agents-md-root-contract.md' \
    ':(exclude).hub-profile.json' \
    ':(exclude)tools/test-agents-md-integration.sh' \
    ':(exclude)tools/test-historical-immutable.sh' \
    ':(exclude)tools/test-post-migration-validator.sh' \
    ':(exclude)tools/validate-repository-structure.sh' \
    ':(exclude)ops/backlog.md' \
    ':(exclude)ops/artifact-map.md' \
    >"$TMP_DIR/stale-pr-ops.log"; then
    fail "active tracked files still contain stale pr-ops/ references"
  fi
fi

if ((failures > 0)); then
  printf '\nAGENTS.md integration regression tests failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'AGENTS.md integration regression tests passed.\n'
