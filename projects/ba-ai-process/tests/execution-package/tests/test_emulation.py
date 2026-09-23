#!/usr/bin/env python3
"""Executable assertions for the deterministic execution-package emulator."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import yaml


TESTS_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = TESTS_ROOT.parents[1]
PACKAGE = SOURCE_ROOT / "dist/execution-package-gigacode-cli"
SPEC = importlib.util.spec_from_file_location("emulate_route", TESTS_ROOT / "tools/emulate-route.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
VALIDATOR_SPEC = importlib.util.spec_from_file_location(
    "validate_package", PACKAGE / "tools/validate-package.py"
)
assert VALIDATOR_SPEC and VALIDATOR_SPEC.loader
VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(VALIDATOR)


class RouteEmulationTest(unittest.TestCase):
    def test_product_attribution_is_the_first_mandatory_human_gate(self) -> None:
        graph = yaml.safe_load(
            (PACKAGE / "routes/rg-bcreq-v1.yaml").read_text(encoding="utf-8")
        )
        entry_targets = [
            edge["to"]
            for edge in graph["edges"]
            if edge["from"] == "entry" and edge["to"] != "refuse"
        ]
        self.assertEqual(["n0"], entry_targets)
        node = next(item for item in graph["nodes"] if item["node"] == "n0")
        self.assertEqual("SK-product-attribution", node["skill"])
        self.assertEqual("A-IN", node["output"])
        self.assertIn("G-human", node["gates"])

    def test_input_contract_uses_taxonomy_paths_and_explicit_confirmation(self) -> None:
        schema = json.loads(
            (PACKAGE / "contracts/c-in.schema.json").read_text(encoding="utf-8")
        )
        self.assertIn("product_attribution", schema["required"])
        product = schema["properties"]["products"]["items"]
        self.assertTrue(
            {"domain", "capability", "feature", "atomic_function", "profile", "owner"}
            .issubset(product["required"])
        )
        self.assertNotIn("product_class", product["properties"])
        status = schema["properties"]["product_attribution"]["properties"]["status"]
        self.assertEqual(["pending", "confirmed", "rejected"], status["enum"])

    def test_runtime_skills_have_no_contact_center_binding(self) -> None:
        for skill in (PACKAGE / ".gigacode/skills").glob("*/SKILL.md"):
            self.assertNotIn("contact-center", skill.parent.name)
            fields = MODULE._frontmatter(skill)
            self.assertNotEqual("contact-center", fields.get("product_class"))

    def test_validator_resolves_non_contact_center_product_from_taxonomy(self) -> None:
        products = [
            {
                "marker": "A",
                "domain": "platform",
                "capability": "platform-integration",
                "feature": "crm-connectors",
                "atomic_function": "crm-bidirectional-sync",
                "profile": "P-API",
                "owner": "platform-owner",
            }
        ]
        document = {
            "products": products,
            "product_attribution": {
                "status": "confirmed",
                "confirmed_by": "analyst@example.test",
                "confirmed_at": "2026-09-23T12:00:00Z",
                "decision_ref": "evidence/checkpoint-n0.md",
                "binding_digest": VALIDATOR.canonical_product_digest(products),
            },
        }
        mango = json.loads((PACKAGE / "taxonomy/mango-products.yaml").read_text(encoding="utf-8"))
        routing = yaml.safe_load((PACKAGE / "taxonomy/products.yaml").read_text(encoding="utf-8"))
        self.assertEqual([], VALIDATOR.product_binding_errors(document, mango, routing))

        document["products"][0]["capability"] = "not-in-platform"
        errors = VALIDATOR.product_binding_errors(document, mango, routing)
        self.assertTrue(any("не принадлежит domain" in message for message in errors))
        self.assertTrue(any("binding_digest" in message for message in errors))

    def assert_run_matches_declared_shape(self, run_path: Path) -> None:
        schema = yaml.safe_load((PACKAGE / "contracts/c-rk.schema.json").read_text(encoding="utf-8"))
        run = yaml.safe_load(run_path.read_text(encoding="utf-8"))
        self.assertTrue(set(schema["required"]).issubset(run))
        self.assertTrue(set(run).issubset(schema["properties"]))
        event_schema = schema["properties"]["events"]["items"]
        for event in run["events"]:
            self.assertTrue(set(event_schema["required"]).issubset(event))
            self.assertTrue(set(event).issubset(event_schema["properties"]))
        handover_schema = schema["properties"]["handover"]
        self.assertTrue(set(handover_schema["required"]).issubset(run["handover"]))
        self.assertTrue(set(run["handover"]).issubset(handover_schema["properties"]))

    def assert_scenario(self, name: str) -> None:
        fixture = TESTS_ROOT / "fixtures" / f"{name}.yaml"
        expected = yaml.safe_load((TESTS_ROOT / "assertions" / f"{name}.yaml").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory(prefix="bcreq-emulation-") as directory:
            result = MODULE.emulate(PACKAGE, fixture, Path(directory))
            self.assertEqual(expected["outcome"], result["outcome"])
            self.assertEqual(expected["path"], result["path"])
            for rel in expected["required_files"]:
                self.assertTrue((result["task_root"] / rel).is_file(), rel)
            run_path = result["task_root"] / "runs" / "RUN-0001.yaml"
            self.assert_run_matches_declared_shape(run_path)
            run = yaml.safe_load(run_path.read_text(encoding="utf-8"))
            task = yaml.safe_load((result["task_root"] / "task.yaml").read_text(encoding="utf-8"))
            self.assertEqual("confirmed", run["product_attribution"]["status"])
            self.assertEqual(task["products"], run["products"])
            self.assertEqual(task["product_attribution"], run["product_attribution"])
            event_types = {event["event_type"] for event in run["events"]}
            self.assertTrue(set(expected["required_event_types"]).issubset(event_types))

    def test_straight_through_route(self) -> None:
        self.assert_scenario("straight-through")

    def test_human_gate_persists_markdown_checkpoint(self) -> None:
        self.assert_scenario("human-gate")


if __name__ == "__main__":
    unittest.main(verbosity=2)
