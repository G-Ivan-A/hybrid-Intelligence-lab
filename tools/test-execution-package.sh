#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

# Regression tests for the GigaCode CLI execution package gate (issues #580,
# #593, #599, and #603).
#
# The package validator IS the machine gate G-mach, so a validator that only
# ever passes is indistinguishable from no gate at all (metric M-2). Every case
# below breaks one compilation rule in a throwaway copy of the package and
# asserts that the gate rejects it, plus one case asserting the intact package
# passes.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PROJECT="projects/ba-ai-process"
PACKAGE="$PROJECT/dist/execution-package-gigacode-cli"
PROJECT_TESTS="$PROJECT/tests/execution-package"
DECISION="$PROJECT/decisions/2026-09-adr-017-ba-ai-process-source-distribution.md"
VALIDATOR="$PACKAGE/tools/validate-package.py"
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

# Python may create bytecode during a standalone G-mach invocation. It is a
# transient runtime file, not an immutable compiled package output.
target="$(fixture generated-bytecode)"
mkdir -p "$target/tools/__pycache__"
printf 'generated' > "$target/tools/__pycache__/bcreq_pipeline.cpython-314.pyc"
expect_pass "$target" "generated Python bytecode"

# Case 2: a route node pointing at a skill that was never compiled.
target="$(fixture missing-skill)"
rm -rf "$target/.gigacode/skills/core-assembly"
expect_reject "$target" "missing skill" "SK-core-assembly"

# Case 3: a SKILL.md that lost a mandatory section.
target="$(fixture missing-section)"
python3 - "$target" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1], ".gigacode/skills/ambiguity-detection/SKILL.md")
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
anchor = next(line + "\n" for line in text.splitlines() if line.startswith("  - {from: n13, to: exit,"))
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

# Case 9: the retired discovery path must fail closed if reintroduced.
target="$(fixture legacy-skill-tree)"
mkdir -p "$target/.agents/skills"
expect_reject "$target" "legacy skill tree" ".agents"

# Case 10: debug orchestration is part of the copyable envelope, not optional prose.
target="$(fixture missing-debug-orchestrator)"
rm -rf "$target/.gigacode/skills/ba-debug-orchestrator"
expect_reject "$target" "missing debug orchestrator" "ba-debug-orchestrator"

# Case 11: a machine rejection may not trigger a hidden corrective retry.
target="$(fixture corrective-retry)"
python3 - "$target" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1], "routes/rg-bcreq-v1.yaml")
path.write_text(path.read_text(encoding="utf-8").replace("corrective_attempts: 0", "corrective_attempts: 1", 1), encoding="utf-8")
PY
expect_reject "$target" "automatic corrective retry" "автоматические корректирующие попытки"

# Case 12: local KB and Confluence are complementary, not a sequential fallback.
target="$(fixture sequential-sources)"
python3 - "$target" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1], "taxonomy/source-tiers.yaml")
path.write_text(path.read_text(encoding="utf-8").replace("collection_mode: complementary", "collection_mode: sequential", 1), encoding="utf-8")
PY
expect_reject "$target" "sequential source fallback" "обязаны дополнять друг друга"

# Case 13: route orchestrators must never be selected implicitly by the model.
target="$(fixture implicit-dispatcher)"
python3 - "$target" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1], ".gigacode/skills/rg-bcreq-v1-dispatcher/SKILL.md")
path.write_text(path.read_text(encoding="utf-8").replace("disable-model-invocation: true", "disable-model-invocation: false", 1), encoding="utf-8")
PY
expect_reject "$target" "implicitly invoked dispatcher" "disable-model-invocation: true"

# Case 14: the executable run template and its C-RK schema cannot drift apart.
target="$(fixture run-template-drift)"
python3 - "$target" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1], "routes/run-sheet-template.yaml")
path.write_text(path.read_text(encoding="utf-8").replace("  artifact_refs: []", "  artifact_refs: []\n  undeclared_field: true", 1), encoding="utf-8")
PY
expect_reject "$target" "run template schema drift" "handover содержит поля вне C-RK"

# Cases 15-19: every prohibited Source artifact class is rejected independently.
target="$(fixture source-rationale)"
mkdir -p "$target/docs/rfc"
printf '%s\n' '# RFC must stay in Source' > "$target/docs/rfc/example.md"
expect_reject "$target" "source rationale in distribution" "запрещённый Source-артефакт"

target="$(fixture source-rrp)"
printf '%s\n' '# RRP must stay in Source' > "$target/00-introduction.md"
expect_reject "$target" "RRP in distribution" "запрещённый Source-артефакт"

target="$(fixture source-adr)"
mkdir -p "$target/decisions"
printf '%s\n' '# ADR must stay in Source' > "$target/decisions/2026-09-adr-999-example.md"
expect_reject "$target" "ADR in distribution" "запрещённый Source-артефакт"

target="$(fixture source-backlog)"
printf '%s\n' '# Backlog must stay in Source' > "$target/backlog.md"
expect_reject "$target" "backlog in distribution" "запрещённый Source-артефакт"

target="$(fixture feedback-inbox)"
mkdir -p "$target/feedback/inbox/test/instance"
printf '%s\n' 'report: must-stay-in-source' > "$target/feedback/inbox/test/instance/report.yaml"
expect_reject "$target" "feedback inbox in distribution" "запрещённый Source-артефакт"

# Case 20: an immutable compiled output cannot drift from package provenance.
target="$(fixture output-drift)"
printf '\n# uncompiled edit\n' >> "$target/templates/bcreq-skeleton.md"
expect_reject "$target" "immutable output drift" "SHA-256 не совпадает"

# Case 21: every MANGO capability must retain one industry mapping.
target="$(fixture missing-industry-mapping)"
python3 - "$target" <<'PY'
import pathlib
import sys

import yaml

path = pathlib.Path(sys.argv[1], "taxonomy/telecom-products.yaml")
data = yaml.safe_load(path.read_text(encoding="utf-8"))
data["mappings"].pop()
path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
PY
expect_reject "$target" "missing industry mapping" "нет отраслевого соответствия"

# Case 22: the product-attribution Human Gate must remain the first work node.
target="$(fixture bypass-product-gate)"
python3 - "$target" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1], "routes/rg-bcreq-v1.yaml")
path.write_text(path.read_text(encoding="utf-8").replace("from: entry, to: n0", "from: entry, to: n1", 1), encoding="utf-8")
PY
expect_reject "$target" "bypassed product gate" "n0 обязан быть единственным"

# Case 23: no runtime skill may restore a static domain binding.
target="$(fixture static-product-class)"
python3 - "$target" <<'PY'
import sys, pathlib
path = pathlib.Path(sys.argv[1], ".gigacode/skills/context-extraction/SKILL.md")
path.write_text(path.read_text(encoding="utf-8").replace("packs:", "product_class: contact-center\npacks:", 1), encoding="utf-8")
PY
expect_reject "$target" "static skill product class" "статическая product_class запрещена"

# Case 24: downstream contracts must preserve the confirmed context.
target="$(fixture dropped-product-context)"
python3 - "$target" <<'PY'
import json
import pathlib
import sys
path = pathlib.Path(sys.argv[1], "contracts/c-quest.schema.json")
data = json.loads(path.read_text(encoding="utf-8"))
data["required"].remove("product_attribution")
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
expect_reject "$target" "dropped downstream product context" "привязка не является обязательной"

# Case 25: the optional A-IN gate resolves values dynamically from the MANGO taxonomy.
python3 - "$ROOT_DIR/$PACKAGE" "$WORKDIR/confirmed-a-in.yaml" <<'PY'
import hashlib
import json
import pathlib
import sys
products = [{
    "marker": "A",
    "domain": "platform",
    "capability": "platform-integration",
    "feature": "crm-connectors",
    "atomic_function": "crm-bidirectional-sync",
    "profile": "P-API",
    "owner": "platform-owner",
}]
digest = "sha256:" + hashlib.sha256(
    json.dumps(products, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
).hexdigest()
document = {
    "work_type": "mango-change",
    "routing": {"primary_axis": "mango", "rule": "mango-change", "decision": "confirmed", "decision_ref": "evidence/checkpoint-n0.md"},
    "products": products,
    "product_attribution": {
        "status": "confirmed",
        "confirmed_by": "analyst@example.test",
        "confirmed_at": "2026-09-23T12:00:00Z",
        "decision_ref": "evidence/checkpoint-n0.md",
        "binding_digest": digest,
    },
}
pathlib.Path(sys.argv[2]).write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
if ! python3 "$ROOT_DIR/$VALIDATOR" "$ROOT_DIR/$PACKAGE" --input "$WORKDIR/confirmed-a-in.yaml" >/dev/null 2>&1; then
  fail "confirmed non-contact-center A-IN: gate rejected a valid taxonomy path"
fi
python3 - "$WORKDIR/confirmed-a-in.yaml" <<'PY'
import json
import pathlib
import sys
path = pathlib.Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))
data["products"][0]["capability"] = "not-in-platform"
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
if output="$(python3 "$ROOT_DIR/$VALIDATOR" "$ROOT_DIR/$PACKAGE" --input "$WORKDIR/confirmed-a-in.yaml" 2>&1)"; then
  fail "invalid product chain: gate accepted a capability outside its domain"
fi
[[ "$output" == *"не принадлежит domain"* ]] || fail "invalid product chain: wrong rejection: $output"

# The project-level emulator exercises route traversal and human-gate pauses
# without invoking an LLM or writing into the committed package.
python3 "$PROJECT_TESTS/tests/test_emulation.py"
python3 "$PROJECT_TESTS/tests/test_semantic_regression.py"

python3 - "$PACKAGE" "$PROJECT_TESTS/fixtures/working-valid.json" "$WORKDIR/working.json" <<'PY'
import importlib.util
import json
from pathlib import Path
import sys
package, fixture, target = map(Path, sys.argv[1:])
spec = importlib.util.spec_from_file_location("bcreq_pipeline", package / "tools/bcreq_pipeline.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
working = json.loads(fixture.read_text(encoding="utf-8"))
working["working_digest"] = module.working_digest(working)
target.write_bytes(module.canonical(working) + b"\n")
PY
python3 "$VALIDATOR" "$PACKAGE" --working "$WORKDIR/working.json" >/dev/null
python3 "$PACKAGE/tools/bcreq_pipeline.py" compile "$WORKDIR/working.json" --output "$WORKDIR/release" >/dev/null
python3 "$VALIDATOR" "$PACKAGE" --working "$WORKDIR/working.json" --release "$WORKDIR/release/release.json" --manifest "$WORKDIR/release/release-manifest.json" >/dev/null

printf 'Execution package tests passed (26 package cases + route emulation + BCREQ regression and compilation).\n'
