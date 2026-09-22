#!/usr/bin/env python3
"""Executable assertions for the deterministic execution-package emulator."""

from __future__ import annotations

import importlib.util
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


class RouteEmulationTest(unittest.TestCase):
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
            event_types = {event["event_type"] for event in run["events"]}
            self.assertTrue(set(expected["required_event_types"]).issubset(event_types))

    def test_straight_through_route(self) -> None:
        self.assert_scenario("straight-through")

    def test_human_gate_persists_markdown_checkpoint(self) -> None:
        self.assert_scenario("human-gate")


if __name__ == "__main__":
    unittest.main(verbosity=2)
