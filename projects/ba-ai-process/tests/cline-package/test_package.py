#!/usr/bin/env python3
"""Executable contract for the standalone Cline BCREQ pilot."""

import json
import hashlib
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[2] / "dist/execution-package-cline-vscode"


class PackageTest(unittest.TestCase):
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

    def test_guide_links_resolve(self):
        def slug(heading):
            text = re.sub(r"`|\*|\[|\]\([^)]*\)", "", heading).strip().lower()
            return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")

        guides = PACKAGE / "docs/guides"
        anchors = {}
        for path in guides.glob("*.md"):
            text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
            anchors[path.name] = {slug(item) for item in re.findall(r"^#{1,6}\s+(.*)$", text, re.M)}
            anchors[path.name] |= set(re.findall(r'<a id="([^"]+)"', text))
        for path in guides.glob("*.md"):
            text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
            for target in re.findall(r"\]\(([^)\s]+)\)", text):
                if target.startswith(("http://", "https://")):
                    continue
                name, _, anchor = target.partition("#")
                name = name or path.name
                self.assertTrue((guides / name).is_file(), f"{path.name}: {target}")
                if anchor and name.endswith(".md"):
                    self.assertIn(anchor, anchors[name], f"{path.name}: {target}")

    def test_guide_real_task_flow(self):
        guide = (PACKAGE / "docs/guides/05-commands-reference.md").read_text(encoding="utf-8")
        seal = re.search(r"^ *@'\n(.*?)\n *'@ \| python - ", guide, re.S | re.M)
        self.assertIsNotNone(seal, "sealing command is missing from the guide")
        seal_script = "\n".join(line[2:] for line in seal.group(1).splitlines())
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "package"
            shutil.copytree(PACKAGE, package)
            data = json.loads((package / "golden/TASK-0001.json").read_text(encoding="utf-8"))
            data["evidence"][0]["locator"] = "https://jira.example.test/browse/BCREQ-123"
            data["evidence"][0]["excerpt"] = "Клиент должен выгружать журнал звонков."
            edited = json.dumps(data, ensure_ascii=False, indent=2)
            (package / "submissions/TASK-0002.json").write_text(edited, encoding="utf-8")
            (package / "submissions/TASK-0003.json").write_text(edited, encoding="utf-8")
            unsealed = self.invoke(package, "run", "TASK-0002", "submissions/TASK-0002.json")
            self.assertNotEqual(unsealed.returncode, 0)
            self.assertIn("Working digest does not match", unsealed.stderr)
            rerun = self.invoke(package, "run", "TASK-0002", "submissions/TASK-0002.json")
            self.assertIn("run already exists", rerun.stderr)
            sealed = subprocess.run([sys.executable, "-", "submissions/TASK-0003.json"], input=seal_script,
                                    cwd=package, text=True, capture_output=True)
            self.assertEqual(sealed.returncode, 0, sealed.stderr)
            self.assertIn("sealed: submissions/TASK-0003.json", sealed.stdout)
            accepted = self.invoke(package, "run", "TASK-0003", "submissions/TASK-0003.json")
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            self.assertNotEqual(self.invoke(package, "verify-ci").returncode, 0)
            (package / "submissions/TASK-0002.json").rename(package / "runs/TASK-0002/working.json")
            ci = self.invoke(package, "verify-ci")
            self.assertEqual(ci.returncode, 0, ci.stderr)
            self.assertIn("submissions/TASK-0003.json: PASS", ci.stdout)
            self.assertEqual(self.invoke(package, "check-package").returncode, 0)


if __name__ == "__main__":
    unittest.main()
