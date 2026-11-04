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

# Model-specific rules files (B-116, issue #727): only a thin generated pointer to
# AGENTS.md passes; a copy of the rules fails.
if [[ -f "$ROOT_DIR/AGENTS.md" && -f "$ROOT_DIR/.hub-profile.json" ]]; then
  adapter_repo() {
    local repo="$TMP_DIR/adapter-$1"
    mkdir -p "$repo"
    cp "$ROOT_DIR/AGENTS.md" "$ROOT_DIR/.hub-profile.json" "$repo/"
    printf '%s\n' "$repo"
  }
  thin_pointer='<!-- Generated adapter: do not edit; rules live in AGENTS.md. -->
@AGENTS.md'

  repo="$(adapter_repo thin-pointer)"
  mkdir -p "$repo/.github" "$repo/.cursor/rules"
  printf '%s\n' "$thin_pointer" > "$repo/CLAUDE.md"
  printf '%s\n' "$thin_pointer" > "$repo/.github/copilot-instructions.md"
  printf '%s\n' "$thin_pointer" > "$repo/.cursor/rules/agents.mdc"
  if ! "$ROOT_DIR/tools/validate-agents-bootstrap.sh" "$repo" >"$TMP_DIR/adapter-thin-pointer.log" 2>&1; then
    fail "thin generated pointers to AGENTS.md were rejected"
  fi

  repo="$(adapter_repo copied-rules)"
  cp "$ROOT_DIR/AGENTS.md" "$repo/CLAUDE.md"
  expect_validator_failure "adapter-copied-rules" "$repo" \
    "CLAUDE.md: model-specific rules file copies AGENTS.md sections"

  repo="$(adapter_repo copied-cursor-rules)"
  mkdir -p "$repo/.cursor/rules"
  { printf '%s\n' "$thin_pointer"; sed -n '/<hard_rules>/,/<\/hard_rules>/p' "$ROOT_DIR/AGENTS.md"; } \
    > "$repo/.cursor/rules/agents.mdc"
  expect_validator_failure "adapter-copied-cursor-rules" "$repo" \
    ".cursor/rules/agents.mdc: model-specific rules file copies AGENTS.md sections <hard_rules>"

  repo="$(adapter_repo no-pointer)"
  printf '# Gemini rules (generated)\n\nAlways answer in English.\n' > "$repo/GEMINI.md"
  expect_validator_failure "adapter-no-pointer" "$repo" \
    "GEMINI.md: model-specific rules file must be a thin pointer to AGENTS.md"

  repo="$(adapter_repo not-generated)"
  printf 'Read AGENTS.md first.\n' > "$repo/.cursorrules"
  expect_validator_failure "adapter-not-generated" "$repo" \
    ".cursorrules: model-specific rules file must identify itself as a generated adapter"

  repo="$(adapter_repo too-long)"
  { printf '%s\n' "$thin_pointer"; for i in $(seq 1 25); do printf 'Rule %s.\n' "$i"; done; } > "$repo/.windsurfrules"
  expect_validator_failure "adapter-too-long" "$repo" \
    ".windsurfrules: model-specific rules file has 27 non-empty lines"
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
  | grep 'expands the considered boundary' >/dev/null; then
  fail "the Hub research-boundary rule must live inside <project_specific_rules> of AGENTS.md"
fi
for template in templates/htom/AGENTS.md templates/spoke/AGENTS.md; do
  if grep -q 'expands the considered boundary' "$ROOT_DIR/$template"; then
    fail "$template must not ship the Hub-specific research-boundary rule"
  fi
  if ! sed -n '/<project_specific_rules>/,/<\/project_specific_rules>/p' "$ROOT_DIR/$template" \
    | grep 'REQUIRED: define the rules of THIS project here' >/dev/null; then
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
    ':(exclude)docs/analysis/2026-11-02-mango-ba-prompts-hub-practice-transfer-check.md' \
    ':(exclude)docs/analysis/2026-11-02-aether-orbis-gra-hub-practice-transfer-check.md' \
    ':(exclude)research/hub/exp/hub-governance-roadmap-715/spoke-consistency-matrix.log' \
    ':(exclude)docs/adr/2026-11-adr-022-hub-archive-and-extraction-redirect.md' \
    ':(exclude)docs/analysis/2026-11-04-gra-extraction-completeness-check.md' \
    ':(exclude)docs/rfc/2026-11-04-rfc-gra-extraction-completion-and-hub-cleanup.md' \
    ':(exclude)research/hub/exp/gra-extraction-cleanup-721/README.md' \
    ':(exclude)research/hub/exp/gra-extraction-cleanup-721/permalink-probe.log' \
    ':(exclude)research/hub/exp/independent-tech-debt-727/issue-statement-sweep.log' \
    >"$TMP_DIR/stale-pr-ops.log"; then
    fail "active tracked files still contain stale pr-ops/ references"
  fi
fi

if ((failures > 0)); then
  printf '\nAGENTS.md integration regression tests failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'AGENTS.md integration regression tests passed.\n'
