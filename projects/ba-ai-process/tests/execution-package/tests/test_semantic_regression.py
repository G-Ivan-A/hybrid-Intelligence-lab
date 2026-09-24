#!/usr/bin/env python3
"""Regression cases from https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/613."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT.parents[1] / "dist/execution-package-gigacode-cli"
SPEC = importlib.util.spec_from_file_location("bcreq_pipeline", PACKAGE / "tools/bcreq_pipeline.py")
assert SPEC and SPEC.loader
PIPELINE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PIPELINE)


class SemanticRegressionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.working = json.loads((ROOT / "fixtures/working-valid.json").read_text(encoding="utf-8"))
        self.working["working_digest"] = PIPELINE.working_digest(self.working)

    def test_valid_baseline_compiles_byte_identically(self) -> None:
        self.assertEqual([], PIPELINE.validate_working(self.working, PACKAGE))
        first = PIPELINE.compile_release(self.working, PACKAGE)
        second = PIPELINE.compile_release(self.working, PACKAGE)
        self.assertEqual(PIPELINE.canonical(first), PIPELINE.canonical(second))
        self.assertEqual([], PIPELINE.validate_release(self.working, *first))
        release, manifest = first
        self.assertIn("BND-001", manifest["included_ids"])
        self.assertIn("UC-001", manifest["included_ids"])
        self.assertIn("CON-001", manifest["included_ids"])
        self.assertEqual("internal_only", next(item["policy"] for item in manifest["excluded"] if item["id"] == "SRC-001"))
        self.assertEqual("conditional", next(item["policy"] for item in manifest["excluded"] if item["id"] == "DELTA-002"))
        self.assertEqual("customer", release["audience"])

    def test_known_antipatterns_are_rejected(self) -> None:
        cases = {
            "EVID-01 unread claim": (lambda d: d["evidence"][0].update(retrieval_status="unread"), "EVID-01"),
            "REL-01 unlinked claim": (lambda d: d["claims"][0].update(goal_refs=[]), "REL-01"),
            "SCOPE-01 as-is FR": (lambda d: d["fr"][0].update(delta_ref="DELTA-002"), "SCOPE-01"),
            "FR-01 UI as FR": (lambda d: d["fr"][0].update(abstraction_level="L3"), "FR-01"),
            "FR-01 atomic UI wording": (lambda d: d["fr"][0].update(shall="The system shall show an export button."), "FR-01"),
            "NFR orphan": (lambda d: d["nfr"][0].update(applies_to_fr=["FR-999"]), "NFR-TRACE"),
            "constraint orphan": (lambda d: d["constraints"][0].update(applies_to_fr=["FR-999"]), "CON-TRACE"),
            "NFR invented target": (lambda d: d["nfr"][0].update(target_source_ref=""), "NFR-01"),
            "compatibility missing obligation": (lambda d: d["compatibility"].update(obligation_refs=[]), "COMP-01"),
            "external spec handed to P-08": (lambda d: d.update(work_type="external-spec", routing={"primary_axis": "industry", "rule": "external-spec", "decision": "confirmed", "decision_ref": "DEC-001"}), "ROUTE"),
            "invented TMF ID": (lambda d: d["industry_bindings"].append({"id": "IND-001", "tm_forum_binding": {"status": "resolved", "element_type": "API", "snapshot_ref": "unknown", "element_id": "TMF-999", "element_name": "Invented", "source_anchor": "none"}, "sid_context": {"status": "not-applicable", "element_type": None, "snapshot_ref": None, "element_id": None, "element_name": None, "source_anchor": None}, "local_product_binding_refs": ["PB-001"], "rationale": "test", "reviewed_by": "analyst"}), "TMF-01"),
        }
        for name, (mutate, code) in cases.items():
            with self.subTest(name=name):
                document = copy.deepcopy(self.working)
                mutate(document)
                document["working_digest"] = PIPELINE.working_digest(document)
                self.assertIn(code, " ".join(PIPELINE.validate_working(document, PACKAGE)))

    def test_release_reverse_trace_cannot_point_to_unknown_working_id(self) -> None:
        release, manifest = PIPELINE.compile_release(self.working, PACKAGE)
        manifest["fragments"][0]["working_ids"] = ["FR-999"]
        self.assertIn("RELEASE-TRACE", " ".join(PIPELINE.validate_release(self.working, release, manifest)))

    def test_tbd_and_open_question_block_release(self) -> None:
        document = copy.deepcopy(self.working)
        document["open_questions"] = [{"id": "OPEN-001", "text": "Agree target", "owner": "analyst", "status": "open"}]
        document["nfr"][0].update(target="TBD", target_source_ref="OPEN-001")
        document["working_digest"] = PIPELINE.working_digest(document)
        self.assertEqual([], PIPELINE.validate_working(document, PACKAGE))
        with self.assertRaisesRegex(ValueError, "unresolved questions"):
            PIPELINE.compile_release(document, PACKAGE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
