#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

# Regression tests for the GigaCode CLI execution package gate (issues #580,
# #593, #599, and #603).
#
# The package validator IS the machine gate G-mach, so a validator that only
# ever passes is indistinguishable from no gate at all (metric M-2). The
# Source-layout checks stay here; the gate cases live in the cross-platform
# tests/test_package_gate.py so that they also run on Windows (issue #647).

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PROJECT="projects/ba-ai-process"
PACKAGE="$PROJECT/dist/execution-package-gigacode-cli"
PROJECT_TESTS="$PROJECT/tests/execution-package"
DECISION="$PROJECT/decisions/2026-09-adr-017-ba-ai-process-source-distribution.md"
PRODUCT_TAXONOMY="$PROJECT/ba-meta-model/product-taxonomy"
PRODUCT_TAXONOMY_COMPILER="$PROJECT/build/compiler/compile-product-taxonomies.py"

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

for required in \
  ba-meta-model \
  meta-model-guides \
  decisions \
  docs/rfc \
  experiments \
  tests/execution-package \
  dist/execution-package-gigacode-cli; do
  [[ -d "$PROJECT/$required" ]] || fail "missing target module: $PROJECT/$required"
done

[[ ! -e projects/ba-gigacode-implementation ]] || \
  fail "legacy project root remains: projects/ba-gigacode-implementation"

[[ -f "$DECISION" ]] || fail "accepted project decision is missing: $DECISION"
grep -Fq 'status: accepted' "$DECISION" || fail "ADR-017 must be accepted"

for obsolete in \
  ba-process-taxonomy \
  ba-operation-taxonomy \
  execution-package-mvp-bcreq; do
  [[ ! -e "$PROJECT/$obsolete" ]] || fail "obsolete flat-layout path remains: $PROJECT/$obsolete"
done

for placeholder in docs/kb/.gitkeep meta-model/.gitkeep; do
  [[ -f "$PACKAGE/$placeholder" ]] || fail "missing copy-time placeholder: $PACKAGE/$placeholder"
done

[[ -d "$PACKAGE/.gigacode/skills" ]] || fail "missing native GigaCode skill directory"
[[ ! -e "$PACKAGE/.agents" ]] || fail "legacy .agents tree must not remain in the CLI package"

for taxonomy in mango-products.yaml telecom-products.yaml; do
  [[ -f "$PRODUCT_TAXONOMY/$taxonomy" ]] || \
    fail "missing Source product taxonomy: $PRODUCT_TAXONOMY/$taxonomy"
  [[ -f "$PACKAGE/taxonomy/$taxonomy" ]] || \
    fail "missing Distribution product taxonomy: $PACKAGE/taxonomy/$taxonomy"
  cmp -s "$PRODUCT_TAXONOMY/$taxonomy" "$PACKAGE/taxonomy/$taxonomy" || \
    fail "Source and Distribution product taxonomies drifted: $taxonomy"
done

python3 "$PRODUCT_TAXONOMY_COMPILER" --check || \
  fail "product taxonomy compiler check failed"

if ! python3 -c 'import yaml' 2>/dev/null; then
  printf 'SKIP: PyYAML is not installed, package content tests cannot run.\n' >&2
  exit 0
fi

# The 26 G-mach cases and the BCREQ compilation regression live in Python so
# that the same suite runs on Windows 10/11 without bash (issue #647).
python3 "$PROJECT_TESTS/tests/test_package_gate.py"
# The project-level emulator exercises route traversal and human-gate pauses
# without invoking an LLM or writing into the committed package.
python3 "$PROJECT_TESTS/tests/test_emulation.py"
python3 "$PROJECT_TESTS/tests/test_semantic_regression.py"
python3 "$PROJECT_TESTS/tests/test_runner.py"
python3 "$PROJECT_TESTS/tests/test_guides.py"

printf 'Execution package tests passed (26 package cases + route emulation + runner negatives + BA guides + BCREQ regression and compilation).\n'
