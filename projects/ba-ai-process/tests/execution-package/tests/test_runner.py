#!/usr/bin/env python3
"""Integration and negative tests for the local transition controller."""

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


PACKAGE = Path(__file__).resolve().parents[3] / "dist/execution-package-gigacode-cli"
SPEC = importlib.util.spec_from_file_location("run_task", PACKAGE / "tools/run-task.py")
assert SPEC and SPEC.loader
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def input_document(confirmed: bool) -> dict:
    products = [{
        "marker": "A", "domain": "platform", "capability": "platform-integration",
        "feature": "crm-connectors", "atomic_function": "crm-bidirectional-sync",
        "profile": "P-API", "owner": "platform-owner",
    }]
    digest = hashlib.sha256(json.dumps(products, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":")).encode()).hexdigest()
    return {
        "artifact_class": "A-IN", "state": "raw",
        "task": {"id": "TASK-9001", "title": "Test", "requested_by": "analyst"},
        "work_type": "mango-change",
        "routing": {"primary_axis": "mango", "rule": "mango-change",
                    "decision": "confirmed" if confirmed else "pending",
                    "decision_ref": "evidence/checkpoint-n0.md"},
        "products": products,
        "product_attribution": ({"status": "confirmed", "confirmed_by": "analyst",
                                 "confirmed_at": "2026-09-26T12:00:00Z",
                                 "decision_ref": "evidence/checkpoint-n0.md",
                                 "binding_digest": "sha256:" + digest}
                                if confirmed else {"status": "pending"}),
        "sources": [{"id": "SRC-01", "kind": "transcript", "tier": "ST-1-ATTACHED",
                     "locator": "test", "content": "test"}],
        "language": "ru",
    }


class RunnerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="gigacode-runner-")
        self.addCleanup(self.temp.cleanup)
        self.package = Path(self.temp.name) / "package"
        shutil.copytree(PACKAGE, self.package)
        self.raw = Path(self.temp.name) / "raw.json"
        self.confirmed = Path(self.temp.name) / "confirmed.json"
        self.raw.write_text(json.dumps(input_document(False)), encoding="utf-8")
        self.confirmed.write_text(json.dumps(input_document(True)), encoding="utf-8")
        self.runner("start", "TASK-9001", expected=0)

    def runner(self, *args: str, expected: int,
               approval: str | None = None) -> subprocess.CompletedProcess:
        command = [sys.executable, str(self.package / "tools/run-task.py"), *map(str, args)]
        if approval is None:
            result = subprocess.run(command, cwd=self.package, text=True, capture_output=True)
        else:
            master, slave = os.openpty()
            try:
                os.write(master, (approval + "\n").encode())
                result = subprocess.run(command, cwd=self.package, text=True, stdin=slave,
                                        capture_output=True)
            finally:
                os.close(slave)
                os.close(master)
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return result

    @staticmethod
    def approval(checkpoint: Path, node: str) -> str:
        digest = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
        return f"APPROVE TASK-9001:{node} sha256:{digest}"

    def trace(self) -> list[dict]:
        path = self.package / "runs/TASK-9001/trace.jsonl"
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

    def test_gate_invoked_before_each_transition(self) -> None:
        self.runner("advance", "TASK-9001", "--to", "n0", "--artifact", self.raw, expected=0)
        checkpoint = Path(self.temp.name) / "checkpoint.md"
        checkpoint.write_text("Approved by analyst", encoding="utf-8")
        self.runner("advance", "TASK-9001", "--to", "n1", "--artifact", self.confirmed,
                    "--checkpoint", checkpoint, expected=0,
                    approval=self.approval(checkpoint, "n0"))
        trace = self.trace()
        self.assertEqual([("entry", "n0"), ("n0", "n1")],
                         [(row["from"], row["to"]) for row in trace])
        self.assertTrue(all(row["script_invoked"] and row["exit_code"] == 0 for row in trace))
        self.assertTrue(all(row["recorded_by"] == "runner" for row in trace))
        self.assertEqual(["entry", "n0"], [row["node"] for row in trace])
        self.assertTrue(all(sum(row[key] is True for key in
                                ("script_invoked", "contract_mode", "step_skipped")) == 1
                            for row in trace))
        result = self.runner("metrics", "TASK-9001", expected=0)
        self.assertEqual(1.0, json.loads(result.stdout)["deterministic_share"])

    def test_skipped_edge_blocks_transition(self) -> None:
        self.runner("advance", "TASK-9001", "--to", "n1", "--artifact", self.raw,
                    expected=1)
        self.assertTrue(self.trace()[-1]["step_skipped"])
        self.assertEqual("entry", json.loads((self.package / "runs/TASK-9001/state.json")
                                             .read_text())["current"])

    def test_failed_gate_blocks_transition(self) -> None:
        with (self.package / "taxonomy/operations.yaml").open("a", encoding="utf-8") as handle:
            handle.write("\n# damaged compiled package\n")
        self.runner("advance", "TASK-9001", "--to", "n0", "--artifact", self.raw,
                    expected=1)
        row = self.trace()[-1]
        self.assertTrue(row["script_invoked"])
        self.assertNotEqual(0, row["exit_code"])
        result = self.runner("metrics", "TASK-9001", expected=0)
        self.assertEqual(0.0, json.loads(result.stdout)["deterministic_share"])
        self.assertEqual("entry", json.loads((self.package / "runs/TASK-9001/state.json")
                                             .read_text())["current"])

    def test_missing_human_checkpoint_blocks_transition(self) -> None:
        self.runner("advance", "TASK-9001", "--to", "n0", "--artifact", self.raw, expected=0)
        self.runner("advance", "TASK-9001", "--to", "n1", "--artifact", self.confirmed,
                    expected=1)
        self.assertEqual("n0", json.loads((self.package / "runs/TASK-9001/state.json")
                                          .read_text())["current"])

    def test_trace_deletion_is_detected(self) -> None:
        self.runner("advance", "TASK-9001", "--to", "n0", "--artifact", self.raw, expected=0)
        (self.package / "runs/TASK-9001/trace.jsonl").write_text("", encoding="utf-8")
        self.runner("advance", "TASK-9001", "--to", "n1", "--artifact", self.confirmed,
                    expected=1)

    def test_claimed_pass_without_gate_is_rejected(self) -> None:
        self.runner("advance", "TASK-9001", "--to", "n0", "--artifact", self.raw, expected=0)
        root = self.package / "runs/TASK-9001"
        row = self.trace()[0]
        row["script_invoked"] = False
        row["step_skipped"] = True
        row.pop("command")
        row.pop("exit_code")
        row.pop("event_digest")
        row["event_digest"] = "sha256:" + hashlib.sha256(
            json.dumps(row, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")).encode("utf-8")).hexdigest()
        (root / "trace.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")
        state = json.loads((root / "state.json").read_text(encoding="utf-8"))
        state["last_event_digest"] = row["event_digest"]
        (root / "state.json").write_text(json.dumps(state), encoding="utf-8")
        self.runner("metrics", "TASK-9001", expected=1)

    def test_wrong_predicate_blocks_transition(self) -> None:
        self.runner("advance", "TASK-9001", "--to", "n0", "--artifact", self.raw, expected=0)
        external = input_document(True)
        external["work_type"] = "external-spec"
        external["routing"].update(primary_axis="industry", rule="external-spec")
        path = Path(self.temp.name) / "external.json"
        path.write_text(json.dumps(external), encoding="utf-8")
        checkpoint = Path(self.temp.name) / "checkpoint.md"
        checkpoint.write_text("Approved by analyst", encoding="utf-8")
        self.runner("advance", "TASK-9001", "--to", "n1", "--artifact", path,
                    "--checkpoint", checkpoint, expected=1)
        self.assertTrue(self.trace()[-1]["step_skipped"])

    def test_resolved_blocker_uses_declared_core_field(self) -> None:
        self.assertEqual("n9", RUNNER.required_target(
            "n8", {"ambiguities": [{"severity": "blocker", "resolved_by": "SRC-01"}]}))
        self.assertEqual("n5", RUNNER.required_target(
            "n8", {"ambiguities": [{"severity": "blocker"}]}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
