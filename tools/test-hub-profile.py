#!/usr/bin/env python3
"""Acceptance tests for the ADR-024 profile schema and CLI."""

import json
import runpy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
CLI = TOOLS / "validate-hub-profile.py"
FIXTURES = TOOLS / "fixtures" / "hub-profile"
SCHEMA = json.loads((TOOLS / "hub-profile.schema.json").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=Draft202012Validator.FORMAT_CHECKER)
validate_profile = runpy.run_path(str(CLI))["validate_profile"]
E1 = json.loads((FIXTURES / "e1.json").read_text(encoding="utf-8"))
PATH_DECLARATION = {
    "path": "ops/backlog.md",
    "reason": "Decision on the project backlog",
    "declared_by": "owner",
    "issue": "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/752#issuecomment-1",
}
SECTION_DECLARATION = {
    "section": "AGENTS.md#project_specific_rules",
    "reason": "Decision on a project section",
    "declared_by": "project",
    "issue": "https://github.com/example/spoke/issues/1",
}


class HubProfileTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.profile_path = Path(temp.name) / ".hub-profile.json"

    def check_file(self, path, *, require_pin=False, cli=False):
        before = path.read_bytes()
        if cli:
            command = [sys.executable, str(CLI)]
            if require_pin:
                command.append("--require-pin")
            if path.name != ".hub-profile.json":
                command.append(path.name)
            run = subprocess.run(command, cwd=path.parent, capture_output=True, text=True)
            self.assertEqual(run.stderr, "")
            result, code = json.loads(run.stdout), run.returncode
        else:
            result, code = validate_profile(path, VALIDATOR, require_pin)
        self.assertEqual(path.read_bytes(), before)
        return result, code

    def check_profile(self, profile, *, require_pin=False):
        self.profile_path.write_text(json.dumps(profile), encoding="utf-8")
        return self.check_file(self.profile_path, require_pin=require_pin)

    def test_initial_templates(self):
        Draft202012Validator.check_schema(SCHEMA)
        for template, archetype in (("htom", "D"), ("spoke", "B")):
            with self.subTest(template=template):
                path = ROOT / "templates" / template / ".hub-profile.json"
                profile = json.loads(path.read_bytes())
                self.assertEqual(profile["archetype"], archetype)
                self.assertNotIn("last_sync", profile)
                self.assertEqual(profile["deviations"], [])
                VALIDATOR.validate(profile)
                initial, code = self.check_file(path, cli=True)
                self.assertEqual(code, 0)
                self.assertEqual(initial["pin_status"], "initial")
                self.assertEqual(initial["diagnostics"], [])
                self.assertEqual(initial["deviations"], [])
                self.assertFalse(initial["drift_ready"])
                drift, code = self.check_file(path, require_pin=True, cli=True)
                self.assertEqual(code, 1)
                self.assertIsNone(drift["last_sync"])
                self.assertEqual(drift["diagnostics"][0]["code"], "first_sync_required")

    def test_pinned_e1_snapshot(self):
        VALIDATOR.validate(E1)
        result, code = self.check_file(FIXTURES / "e1.json", require_pin=True, cli=True)
        self.assertEqual(code, 0)
        self.assertTrue(result["drift_ready"])
        self.assertEqual(result["pin_status"], "pinned")
        self.assertEqual(result["last_sync"], E1["last_sync"])
        self.assertEqual(result["last_sync"]["tool"], "tools/spoke-extraction.py@54face1618f7")
        self.assertEqual(result["deviations"], [])
        self.assertEqual(result["diagnostics"], [])

    def test_legacy_snapshots(self):
        # Mango additionally lacks the archetype required by the bootstrap contract.
        for fixture, exit_code, missing in (
            ("gra.json", 1, {"hub_sha", "tool"}),
            ("mango.json", 2, {"scope", "tool"}),
        ):
            with self.subTest(fixture=fixture):
                path = FIXTURES / fixture
                result, code = self.check_file(path, require_pin=True, cli=True)
                self.assertEqual(code, exit_code)
                self.assertEqual(result["pin_status"], "migration_required")
                self.assertFalse(result["drift_ready"])
                self.assertIsNone(result["last_sync"])
                migration = [
                    diagnostic for diagnostic in result["diagnostics"]
                    if diagnostic["code"] == "pin_migration_required"
                ]
                for field in missing:
                    self.assertTrue(any(field in item["message"] for item in migration))
        _, code = self.check_file(FIXTURES / "gra.json")
        self.assertEqual(code, 0)

    def test_bad_pin_fields(self):
        for field, value in (
            ("hub_sha", "54face1618f7"), ("hub_sha", "g" * 40),
            ("date", "2026-02-29"), ("date", "20261116"),
            ("scope", None), ("scope", " \t"),
            ("tool", None), ("tool", "spoke-extraction"),
            ("tool", "spoke-extraction@main"), ("tool", "spoke-extraction@^1.2.0"),
        ):
            with self.subTest(field=field, value=value):
                pin = E1["last_sync"].copy()
                if value is None:
                    del pin[field]
                else:
                    pin[field] = value
                result, code = self.check_profile(dict(E1, last_sync=pin), require_pin=True)
                self.assertEqual(code, 1)
                self.assertEqual(result["pin_status"], "migration_required")
                self.assertFalse(result["drift_ready"])
                self.assertIsNone(result["last_sync"])
                self.assertTrue(all(
                    item["code"] == "pin_migration_required" for item in result["diagnostics"]
                ))

    def test_empty_or_wrong_type_pin_requires_migration(self):
        for pin in ({}, None, []):
            with self.subTest(pin=pin):
                result, code = self.check_profile(dict(E1, last_sync=pin), require_pin=True)
                self.assertEqual(code, 1)
                self.assertEqual(result["pin_status"], "migration_required")
                self.assertIsNone(result["last_sync"])

    def test_exact_release_and_leap_day(self):
        pin = dict(E1["last_sync"], date="2024-02-29", tool="hub-sync@v1.2.3-rc.1+build.7")
        result, code = self.check_profile(dict(E1, last_sync=pin), require_pin=True)
        self.assertEqual(code, 0)
        self.assertEqual(result["last_sync"], pin)

    def test_declaration_candidates_and_missing_array(self):
        declarations = [PATH_DECLARATION, SECTION_DECLARATION]
        result, code = self.check_profile(dict(E1, deviations=declarations), require_pin=True)
        self.assertEqual(code, 0)
        self.assertEqual(result["deviations"], declarations)
        self.assertEqual(self.check_profile(E1), self.check_profile(dict(E1, deviations=[])))

    def test_bad_declarations_are_excluded(self):
        bad_declarations = [
            {key: value for key, value in PATH_DECLARATION.items() if key != omitted}
            for omitted in PATH_DECLARATION
        ] + [
            dict(PATH_DECLARATION, reason=" \t"),
            dict(PATH_DECLARATION, declared_by="admin"),
            dict(PATH_DECLARATION, path="ops/*.md"),
            dict(PATH_DECLARATION, path="../ops/backlog.md"),
            dict(PATH_DECLARATION, path="/ops/backlog.md"),
            dict(PATH_DECLARATION, issue="#752"),
            dict(PATH_DECLARATION, issue="https://github.com/example/spoke/pull/1"),
            dict(PATH_DECLARATION, issue="https://github.com/example/spoke/issues/1\n"),
            dict(PATH_DECLARATION, section="AGENTS.md#project_specific_rules"),
            dict(SECTION_DECLARATION, section=" "),
            "ops/backlog.md",
        ]
        for invalid in bad_declarations:
            with self.subTest(declaration=invalid):
                profile = dict(E1, deviations=[invalid, SECTION_DECLARATION])
                result, code = self.check_profile(profile, require_pin=True)
                self.assertEqual(code, 2)
                self.assertEqual(result["pin_status"], "pinned")
                self.assertFalse(result["drift_ready"])
                self.assertEqual(result["deviations"], [SECTION_DECLARATION])
                self.assertTrue(any(
                    item["code"] == "deviation_invalid" and item["path"][:2] == ["deviations", 0]
                    for item in result["diagnostics"]
                ))
        result, code = self.check_profile(dict(E1, deviations={}))
        self.assertEqual(code, 2)
        self.assertEqual(result["deviations"], [])
        self.assertEqual(result["diagnostics"][0]["path"], ["deviations"])

    def test_base_profile_compatibility(self):
        for archetype in ("A", "B", "C", "D"):
            with self.subTest(archetype=archetype):
                profile = {
                    "profile_version": "1.0",
                    "archetype": archetype,
                    "environment": "gigacode",
                    "secondary_environments": ["local", "serverless"],
                    "project_specific_directories": [
                        {"path": "docs/custom/", "reason": "Project artifacts", "decision": "#1"}
                    ],
                    "sync_history": [{"hub_commit": "32b5fa5"}],
                    "project_data": {"field": 123},
                }
                result, code = self.check_profile(profile)
                self.assertEqual(code, 0)
                self.assertEqual(result["deviations"], [])
        self.assertEqual(self.check_profile({"archetype": "B"})[1], 0)
        self.assertEqual(self.check_file(ROOT / ".hub-profile.json", cli=True)[1], 0)

    def test_invalid_base_fields(self):
        for fields in (
            {"archetype": "Z"},
            {"environment": "unknown"},
            {"secondary_environments": ["unknown"]},
            {"project_specific_directories": [{"path": "docs/custom/"}]},
            {"project_specific_directories": [{"path": "docs/custom/", "reason": " "}]},
            {"project_specific_directories": [{"path": "../custom", "reason": "Project"}]},
            {"project_specific_directories": [{"path": "/custom", "reason": "Project"}]},
        ):
            with self.subTest(fields=fields):
                result, code = self.check_profile(dict(E1, **fields))
                self.assertEqual(code, 2)
                self.assertFalse(result["drift_ready"])
                self.assertEqual(result["diagnostics"][0]["code"], "profile_invalid")

    def test_invalid_input_has_no_pin_or_declarations(self):
        for content in (b"{", b"[]", b'{"archetype":"B","last_sync":{},"last_sync":null}', b"\xff"):
            with self.subTest(content=content):
                self.profile_path.write_bytes(content)
                result, code = self.check_file(self.profile_path)
                self.assertEqual(code, 2)
                self.assertEqual(result["pin_status"], "unavailable")
                self.assertEqual(result["deviations"], [])
                self.assertEqual(result["diagnostics"][0]["code"], "profile_invalid")


if __name__ == "__main__":
    unittest.main()
