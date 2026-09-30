#!/usr/bin/env python3
"""Regression tests for the GigaCode CLI execution package gate G-mach.

The package validator IS the machine gate G-mach, so a validator that only ever
passes is indistinguishable from no gate at all (metric M-2). Every case breaks
one compilation rule in a throwaway copy of the package and asserts that the gate
rejects it with the expected reason; the intact package must pass. The cases were
ported from tools/test-execution-package.sh (issues #580, #593, #599, #603) so
that they run unchanged on Windows 10/11 (issue #647).
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml


PROJECT = Path(__file__).resolve().parents[3]
PACKAGE = PROJECT / "dist/execution-package-gigacode-cli"
VALIDATOR = PACKAGE / "tools/validate-package.py"
FIXTURE = Path(__file__).resolve().parents[1] / "fixtures/working-valid.json"
SOURCE_REJECTION = "запрещённый Source-артефакт"


def gate(package: Path, *extra: str) -> subprocess.CompletedProcess:
    # A Windows pipe uses the ANSI code page, which cannot encode G-mach messages.
    environment = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run([sys.executable, str(VALIDATOR), str(package), *extra],
                          capture_output=True, encoding="utf-8", env=environment)


def edit(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{path.name}: {old!r} is absent, the case would test nothing"
    # newline="\n": Windows text mode would turn the whole file into CRLF otherwise.
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append(path: Path, text: str) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def add_dangling_edge(root: Path) -> None:
    path = root / "routes/rg-bcreq-v1.yaml"
    anchor = next(line + "\n" for line in path.read_text(encoding="utf-8").splitlines()
                  if line.startswith("  - {from: n13, to: exit,"))
    edit(path, anchor, anchor + "  - {from: n12, to: n99, condition: gate_passed}\n")


def drop_last_metric(root: Path) -> None:
    path = root / "evaluation/metrics.yaml"
    head, separator, _ = path.read_text(encoding="utf-8").partition("  - id: MP-6")
    assert separator, "metrics.yaml has no MP-6"
    write(path, head)


def drop_industry_mapping(root: Path) -> None:
    path = root / "taxonomy/telecom-products.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data["mappings"].pop()
    write(path, yaml.safe_dump(data, allow_unicode=True, sort_keys=False))


def drop_downstream_context(root: Path) -> None:
    path = root / "contracts/c-quest.schema.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["required"].remove("product_attribution")
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


# (case, mutation of a package copy, text the rejection must contain)
REJECTIONS = [
    ("missing skill", lambda root: shutil.rmtree(root / ".gigacode/skills/core-assembly"),
     "SK-core-assembly"),
    ("missing skill section", lambda root: edit(
        root / ".gigacode/skills/ambiguity-detection/SKILL.md", "\n## Отказ\n", "\n## Прочее\n"),
     "## Отказ"),
    ("operation id outside vocabulary", lambda root: edit(
        root / "taxonomy/operations.yaml", "id: OP-EXT-01", "id: OP-FREE-01"), "OP-"),
    ("dangling edge", add_dangling_edge, "n99"),
    ("unexplained empty slot", lambda root: edit(root / "golden/cases.yaml", ", S-TRACE]", "]"),
     "S-TRACE"),
    ("hub reference at runtime", lambda root: append(
        root / "templates/bcreq-skeleton.md", "\nсмотри ba-meta-model/20-taxonomy.md\n"),
     "контракт 2"),
    ("incomplete metric baseline", drop_last_metric, "MP-6"),
    ("legacy skill tree", lambda root: (root / ".agents/skills").mkdir(parents=True), ".agents"),
    ("missing debug orchestrator",
     lambda root: shutil.rmtree(root / ".gigacode/skills/ba-debug-orchestrator"),
     "ba-debug-orchestrator"),
    ("automatic corrective retry", lambda root: edit(
        root / "routes/rg-bcreq-v1.yaml", "corrective_attempts: 0", "corrective_attempts: 1"),
     "автоматические корректирующие попытки"),
    ("sequential source fallback", lambda root: edit(
        root / "taxonomy/source-tiers.yaml", "collection_mode: complementary",
        "collection_mode: sequential"), "обязаны дополнять друг друга"),
    ("implicitly invoked dispatcher", lambda root: edit(
        root / ".gigacode/skills/rg-bcreq-v1-dispatcher/SKILL.md",
        "disable-model-invocation: true", "disable-model-invocation: false"),
     "disable-model-invocation: true"),
    ("run template schema drift", lambda root: edit(
        root / "routes/run-sheet-template.yaml", "  artifact_refs: []",
        "  artifact_refs: []\n  undeclared_field: true"), "handover содержит поля вне C-RK"),
    ("source rationale in distribution", lambda root: write(
        root / "docs/rfc/example.md", "# RFC must stay in Source\n"), SOURCE_REJECTION),
    ("RRP in distribution", lambda root: write(
        root / "00-introduction.md", "# RRP must stay in Source\n"), SOURCE_REJECTION),
    ("ADR in distribution", lambda root: write(
        root / "decisions/2026-09-adr-999-example.md", "# ADR must stay in Source\n"),
     SOURCE_REJECTION),
    ("backlog in distribution", lambda root: write(
        root / "backlog.md", "# Backlog must stay in Source\n"), SOURCE_REJECTION),
    ("feedback inbox in distribution", lambda root: write(
        root / "feedback/inbox/test/instance/report.yaml", "report: must-stay-in-source\n"),
     SOURCE_REJECTION),
    ("immutable output drift", lambda root: append(
        root / "templates/bcreq-skeleton.md", "\n# uncompiled edit\n"), "SHA-256 не совпадает"),
    ("missing industry mapping", drop_industry_mapping, "нет отраслевого соответствия"),
    ("bypassed product gate", lambda root: edit(
        root / "routes/rg-bcreq-v1.yaml", "from: entry, to: n0", "from: entry, to: n1"),
     "n0 обязан быть единственным"),
    ("static skill product class", lambda root: edit(
        root / ".gigacode/skills/context-extraction/SKILL.md", "packs:",
        "product_class: contact-center\npacks:"), "статическая product_class запрещена"),
    ("dropped downstream product context", drop_downstream_context,
     "привязка не является обязательной"),
]


def confirmed_input() -> dict:
    products = [{
        "marker": "A", "domain": "platform", "capability": "platform-integration",
        "feature": "crm-connectors", "atomic_function": "crm-bidirectional-sync",
        "profile": "P-API", "owner": "platform-owner",
    }]
    digest = hashlib.sha256(json.dumps(products, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":")).encode("utf-8")).hexdigest()
    return {
        "work_type": "mango-change",
        "routing": {"primary_axis": "mango", "rule": "mango-change", "decision": "confirmed",
                    "decision_ref": "evidence/checkpoint-n0.md"},
        "products": products,
        "product_attribution": {
            "status": "confirmed", "confirmed_by": "analyst@example.test",
            "confirmed_at": "2026-09-23T12:00:00Z", "decision_ref": "evidence/checkpoint-n0.md",
            "binding_digest": "sha256:" + digest,
        },
    }


class PackageGateTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="gigacode-gate-")
        self.addCleanup(temporary.cleanup)
        self.workdir = Path(temporary.name)

    def fixture(self, name: str) -> Path:
        # Fresh copy per case: mutations must not leak between cases.
        target = self.workdir / name.replace(" ", "-")
        shutil.copytree(PACKAGE, target)
        return target

    def assertAccepted(self, package: Path, *extra: str) -> None:
        result = gate(package, *extra)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assertRejected(self, package: Path, needle: str, *extra: str) -> None:
        result = gate(package, *extra)
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, "gate accepted a package that must be rejected")
        self.assertIn(needle, output)

    def test_intact_package_passes(self) -> None:
        self.assertAccepted(PACKAGE)

    def test_generated_bytecode_is_not_a_package_output(self) -> None:
        # Python may create bytecode during a standalone G-mach invocation.
        target = self.fixture("generated-bytecode")
        write(target / "tools/__pycache__/bcreq_pipeline.cpython-314.pyc", "generated")
        self.assertAccepted(target)

    def test_broken_rule_is_rejected(self) -> None:
        for name, mutate, needle in REJECTIONS:
            with self.subTest(name):
                target = self.fixture(name)
                mutate(target)
                self.assertRejected(target, needle)

    def test_input_chain_resolves_from_mango_taxonomy(self) -> None:
        document = confirmed_input()
        path = self.workdir / "confirmed-a-in.yaml"
        write(path, json.dumps(document, ensure_ascii=False, indent=2) + "\n")
        self.assertAccepted(PACKAGE, "--input", str(path))
        document["products"][0]["capability"] = "not-in-platform"
        write(path, json.dumps(document, ensure_ascii=False, indent=2) + "\n")
        self.assertRejected(PACKAGE, "не принадлежит domain", "--input", str(path))

    def test_working_compiles_to_accepted_release(self) -> None:
        spec = importlib.util.spec_from_file_location("bcreq_pipeline",
                                                      PACKAGE / "tools/bcreq_pipeline.py")
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        working = json.loads(FIXTURE.read_text(encoding="utf-8"))
        working["working_digest"] = module.working_digest(working)
        path = self.workdir / "working.json"
        path.write_bytes(module.canonical(working) + b"\n")
        self.assertAccepted(PACKAGE, "--working", str(path))
        release = self.workdir / "release"
        compiled = subprocess.run([sys.executable, str(PACKAGE / "tools/bcreq_pipeline.py"),
                                   "compile", str(path), "--output", str(release)],
                                  capture_output=True, encoding="utf-8",
                                  env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        self.assertEqual(compiled.returncode, 0, compiled.stdout + compiled.stderr)
        self.assertAccepted(PACKAGE, "--working", str(path),
                            "--release", str(release / "release.json"),
                            "--manifest", str(release / "release-manifest.json"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
