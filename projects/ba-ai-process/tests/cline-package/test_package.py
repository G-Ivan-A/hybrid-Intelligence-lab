#!/usr/bin/env python3
"""Executable contract for the standalone Cline BCREQ pilot."""

import json
import hashlib
import importlib.util
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


PACKAGE = Path(__file__).resolve().parents[2] / "dist/execution-package-cline-vscode"


class PackageTest(unittest.TestCase):
    def test_run_uses_one_working_snapshot_across_all_gates(self):
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "package"
            shutil.copytree(PACKAGE, package)
            candidate = package / "submissions/TASK-0002.json"
            original = json.loads((package / "golden/TASK-0001.json").read_text())
            candidate.write_text(json.dumps(original))
            original_hash = hashlib.sha256(candidate.read_bytes()).hexdigest()

            spec = importlib.util.spec_from_file_location("pilot_runner", package / "tools/run_task.py")
            runner = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(runner)
            real_run = subprocess.run

            def change_candidate_after_validation(command, **kwargs):
                result = real_run(command, **kwargs)
                if command[2] == "validate-working" and result.returncode == 0:
                    changed = json.loads(candidate.read_text())
                    changed["goals"][0]["text"] = "A different approved goal"
                    changed["working_digest"] = "sha256:" + hashlib.sha256(json.dumps(
                        {key: value for key, value in changed.items() if key != "working_digest"},
                        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                    ).encode()).hexdigest()
                    candidate.write_text(json.dumps(changed))
                return result

            with mock.patch.object(runner.subprocess, "run", side_effect=change_candidate_after_validation):
                self.assertTrue(runner.run("TASK-0002", candidate, package / "runs/TASK-0002", runner.check_package()))

            trace = [json.loads(line) for line in (package / "runs/TASK-0002/trace.jsonl").read_text().splitlines()]
            release_manifest = json.loads((package / "runs/TASK-0002/release-manifest.json").read_text())
            self.assertNotEqual(hashlib.sha256(candidate.read_bytes()).hexdigest(), original_hash)
            self.assertEqual(release_manifest["working_digest"], original["working_digest"])
            self.assertTrue(all(item["input_sha256"] == original_hash for item in trace))

    def test_changed_working_snapshot_stops_the_route(self):
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "package"
            shutil.copytree(PACKAGE, package)
            spec = importlib.util.spec_from_file_location("pilot_runner", package / "tools/run_task.py")
            runner = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(runner)
            output = package / "runs/TASK-0003"
            real_run = subprocess.run

            def change_snapshot_after_validation(command, **kwargs):
                result = real_run(command, **kwargs)
                if command[2] == "validate-working" and result.returncode == 0:
                    (output / "working.json").write_text("{}")
                return result

            with mock.patch.object(runner.subprocess, "run", side_effect=change_snapshot_after_validation):
                self.assertFalse(runner.run("TASK-0003", package / "golden/TASK-0001.json", output, runner.check_package()))

            trace = [json.loads(line) for line in (output / "trace.jsonl").read_text().splitlines()]
            self.assertEqual([item["state"] for item in trace[:3]], ["script_invoked", "step_skipped", "step_skipped"])
            self.assertEqual(trace[0]["detail"], "working snapshot changed")
            self.assertFalse((output / "release.json").exists())

    def test_one_environment_boundary(self):
        other_clients = re.compile(r"\b(?:GigaCode|Qwen(?: Chat)?|OpenCode|Kilo Code|Roo Code)\b", re.I)
        for path in PACKAGE.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                self.assertIsNone(other_clients.search(path.read_text(encoding="utf-8")), str(path))

    def invoke(self, package, *args):
        return subprocess.run(
            [sys.executable, str(package / "tools/run_task.py"), *map(str, args)],
            cwd=package,
            text=True,
            capture_output=True,
        )

    def test_pilot_and_fail_closed_trace(self):
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "package"
            shutil.copytree(PACKAGE, package)
            (package / ".git").mkdir()
            (package / ".git/config").write_text("local git state")
            good = package / "golden/TASK-0001.json"
            success = self.invoke(package, "run", "TASK-0001", good)
            self.assertEqual(success.returncode, 0, success.stderr)
            trace = [json.loads(line) for line in (package / "runs/TASK-0001/trace.jsonl").read_text().splitlines()]
            self.assertEqual([item["state"] for item in trace], ["script_invoked"] * 3 + ["contract_mode"])
            self.assertTrue(all(item["package_sha256"] and item["task_id"] == "TASK-0001" for item in trace))
            self.assertTrue((package / "runs/TASK-0001/release.json").exists())

            broken = package / "submissions/TASK-0002.json"
            data = json.loads(good.read_text())
            data["fr"] = []
            data["working_digest"] = "sha256:" + hashlib.sha256(json.dumps(
                {key: value for key, value in data.items() if key != "working_digest"},
                ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            ).encode()).hexdigest()
            broken.write_text(json.dumps(data))
            rejected = self.invoke(package, "run", "TASK-0002", broken)
            self.assertNotEqual(rejected.returncode, 0)
            trace = [json.loads(line) for line in (package / "runs/TASK-0002/trace.jsonl").read_text().splitlines()]
            self.assertEqual([item["state"] for item in trace], ["script_invoked", "step_skipped", "step_skipped", "contract_mode"])
            self.assertNotEqual(trace[0]["exit_code"], 0)
            self.assertFalse((package / "runs/TASK-0002/release.json").exists())
            ci = self.invoke(package, "verify-ci")
            self.assertNotEqual(ci.returncode, 0)
            self.assertIn("submissions/TASK-0002.json: FAIL", ci.stdout)

    def test_manifest_tamper_and_hook(self):
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "package"
            shutil.copytree(PACKAGE, package)
            payload = {"hookName": "PreToolUse", "preToolUse": {"toolName": "write_to_file", "parameters": {"path": "contracts/c-working-bcreq.schema.json"}}}
            blocked = subprocess.run([str(package / ".clinerules/hooks/PreToolUse")], input=json.dumps(payload), cwd=package, text=True, capture_output=True)
            self.assertEqual(blocked.returncode, 0, blocked.stderr)
            self.assertTrue(json.loads(blocked.stdout)["cancel"])
            payload["preToolUse"]["parameters"]["path"] = "submissions/TASK-0002.json"
            allowed = subprocess.run([str(package / ".clinerules/hooks/PreToolUse")], input=json.dumps(payload), cwd=package, text=True, capture_output=True)
            self.assertFalse(json.loads(allowed.stdout)["cancel"])
            payload["preToolUse"]["parameters"]["path"] = "submissions/../contracts/c-working-bcreq.schema.json"
            traversal = subprocess.run([str(package / ".clinerules/hooks/PreToolUse")], input=json.dumps(payload), cwd=package, text=True, capture_output=True)
            self.assertTrue(json.loads(traversal.stdout)["cancel"])
            payload["preToolUse"]["toolName"] = "execute_command"
            shell = subprocess.run([str(package / ".clinerules/hooks/PreToolUse")], input=json.dumps(payload), cwd=package, text=True, capture_output=True)
            self.assertTrue(json.loads(shell.stdout)["cancel"])
            (package / "tools/bcreq_pipeline.py").write_text("pass\n")
            check = self.invoke(package, "check-package")
            self.assertNotEqual(check.returncode, 0)


if __name__ == "__main__":
    unittest.main()
