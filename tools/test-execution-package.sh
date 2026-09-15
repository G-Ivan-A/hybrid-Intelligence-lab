#!/usr/bin/env bash
set -euo pipefail

# Regression tests for the execution package gate (issue #580).
#
# The package validator IS the machine gate G-mach, so a validator that only
# ever passes is indistinguishable from no gate at all (metric M-2). Every case
# below breaks one compilation rule in a throwaway copy of the package and
# asserts that the gate rejects it, plus one case asserting the intact package
# passes.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PACKAGE="projects/ba-gigacode-implementation/execution-package-mvp-bcreq"
VALIDATOR="$PACKAGE/tools/validate-package.py"

if ! python3 -c 'import yaml' 2>/dev/null; then
  printf 'SKIP: PyYAML is not installed, execution package tests cannot run.\n' >&2
  exit 0
fi

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

fixture() {
  # Fresh copy per case: mutations must not leak between cases.
  local target="$WORKDIR/$1"
  rm -rf "$target"
  mkdir -p "$target"
  cp -R "$ROOT_DIR/$PACKAGE/." "$target/"
  printf '%s\n' "$target"
}

expect_pass() {
  local target="$1" name="$2"
  if ! python3 "$ROOT_DIR/$VALIDATOR" "$target" >/dev/null 2>&1; then
    python3 "$ROOT_DIR/$VALIDATOR" "$target" >&2 || true
    fail "$name: gate rejected a package that must be accepted"
  fi
}

expect_reject() {
  local target="$1" name="$2" needle="$3"
  local output
  if output="$(python3 "$ROOT_DIR/$VALIDATOR" "$target" 2>&1)"; then
    fail "$name: gate accepted a package that must be rejected"
  fi
  if [[ "$output" != *"$needle"* ]]; then
    fail "$name: rejection reason does not mention $needle; got: $output"
  fi
}

# Case 1: the package as committed passes its own gate.
expect_pass "$ROOT_DIR/$PACKAGE" "intact package"

# Case 2: a route node pointing at a skill that was never compiled.
target="$(fixture missing-skill)"
rm -rf "$target/.agents/skills/core-assembly-contact-center"
expect_reject "$target" "missing skill" "SK-core-assembly"

# Case 3: a SKILL.md that lost a mandatory section.
target="$(fixture missing-section)"
python3 - "$target" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1], ".agents/skills/ambiguity-detection-contact-center/SKILL.md")
path.write_text(path.read_text(encoding="utf-8").replace("\n## Отказ\n", "\n## Прочее\n"), encoding="utf-8")
PY
expect_reject "$target" "missing skill section" "## Отказ"

# Case 4: an operation identifier outside the closed format.
target="$(fixture bad-operation-id)"
python3 - "$target" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1], "taxonomy/operations.yaml")
path.write_text(path.read_text(encoding="utf-8").replace("id: OP-EXT-01", "id: OP-FREE-01", 1), encoding="utf-8")
PY
expect_reject "$target" "operation id outside vocabulary" "OP-"

# Case 5: an edge pointing at a node that does not exist.
target="$(fixture dangling-edge)"
python3 - "$target" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1], "routes/rg-bcreq-v1.yaml")
text = path.read_text(encoding="utf-8")
anchor = "  - {from: n12, to: exit, condition: gate_passed}\n"
path.write_text(text.replace(anchor, anchor + "  - {from: n12, to: n99, condition: gate_passed}\n", 1), encoding="utf-8")
PY
expect_reject "$target" "dangling edge" "n99"

# Case 6: a golden case that leaves a slot neither filled nor explained.
target="$(fixture slot-gap)"
python3 - "$target" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1], "golden/cases.yaml")
path.write_text(path.read_text(encoding="utf-8").replace(", S-TRACE]", "]", 1), encoding="utf-8")
PY
expect_reject "$target" "unexplained empty slot" "S-TRACE"

# Case 7: a runtime artifact that reaches back into the hub.
target="$(fixture hub-reference)"
printf '\nсмотри ba-meta-model/20-taxonomy.md\n' >> "$WORKDIR/hub-reference/templates/bcreq-skeleton.md"
expect_reject "$target" "hub reference at runtime" "контракт 2"

# Case 8: an incomplete metric baseline.
target="$(fixture missing-metric)"
python3 - "$target" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1], "evaluation/metrics.yaml")
text = path.read_text(encoding="utf-8")
head, _, _ = text.partition("  - id: MP-6")
path.write_text(head, encoding="utf-8")
PY
expect_reject "$target" "incomplete metric baseline" "MP-6"

printf 'Execution package tests passed (8 case(s)).\n'
