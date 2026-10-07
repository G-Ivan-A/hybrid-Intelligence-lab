#!/usr/bin/env python3
"""Executable contract for the standalone Cline BCREQ pilot."""

import json
import hashlib
import importlib.util
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[2] / "dist/execution-package-cline-vscode"


class PackageTest(unittest.TestCase):
    def test_compiler_survives_autocrlf_checkout_of_source(self):
        project = PACKAGE.parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source"
            clone = Path(temporary) / "clone"
            target = source / "projects/ba-ai-process"
            (target / "build").mkdir(parents=True)
            shutil.copy2(project / "build/compile-cline-package.py", target / "build")
            shutil.copytree(project / "build/common", target / "build/common")
            shutil.copytree(project / "build/adapters/cline-vscode", target / "build/adapters/cline-vscode")
            shutil.copytree(PACKAGE, target / "dist/execution-package-cline-vscode")
            subprocess.run(["git", "init", "-q", str(source)], check=True)
            subprocess.run(["git", "-C", str(source), "add", "."], check=True)
            subprocess.run(["git", "-C", str(source), "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                            "commit", "-qm", "test source and package"], check=True)
            subprocess.run(["git", "-c", "core.autocrlf=true", "clone", "-q", str(source), str(clone)], check=True)
            result = subprocess.run([sys.executable, str(clone / "projects/ba-ai-process/build/compile-cline-package.py"), "--check"],
                                    cwd=clone, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_git_checkout_preserves_manifest_bytes_with_autocrlf(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source"
            clone = Path(temporary) / "clone"
            shutil.copytree(PACKAGE, source)
            subprocess.run(["git", "init", "-q", str(source)], check=True)
            subprocess.run(["git", "-C", str(source), "add", "."], check=True)
            subprocess.run(["git", "-C", str(source), "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                            "commit", "-qm", "test package"], check=True)
            subprocess.run(["git", "-c", "core.autocrlf=true", "clone", "-q", str(source), str(clone)], check=True)
            check = self.invoke(clone, "check-package")
            self.assertEqual(check.returncode, 0, check.stderr)

    def test_windows_hook_entrypoints_and_v4_tools(self):
        for name in ("TaskStart", "TaskResume", "PreToolUse"):
            hook = PACKAGE / ".clinerules/hooks" / f"{name}.ps1"
            self.assertTrue(hook.is_file(), str(hook))
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "package"
            shutil.copytree(PACKAGE, package)
            hook = package / "tools/cline_hook.py"
            for name, parameters, allowed in (
                ("read_files", {"files": [{"path": str(package / "README.md")}]}, True),
                ("ask_question", {"question": "Continue?"}, True),
                ("editor", {"path": str(package / "submissions/TASK-0002.json")}, True),
                ("editor", {"path": str(package / "contracts/c-working-bcreq.schema.json")}, False),
                ("run_commands", {"commands": ["echo unsafe"]}, False),
                ("apply_patch", {"input": "*** Begin Patch"}, False),
            ):
                payload = {"hookName": "PreToolUse", "preToolUse": {"toolName": name, "parameters": parameters}}
                result = subprocess.run([sys.executable, str(hook)], input=json.dumps(payload), cwd=package,
                                        text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["cancel"], not allowed, name)

    def test_git_bash_drive_path_normalization(self):
        spec = importlib.util.spec_from_file_location("run_task_windows", PACKAGE / "tools/run_task.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.normalize_windows_path("/c/Users/Иван Петров/bcreq-pilot/runtime/submissions/TASK-0002.json"),
                         "C:\\Users\\Иван Петров\\bcreq-pilot\\runtime\\submissions\\TASK-0002.json")
        if os.name == "nt":
            with tempfile.TemporaryDirectory() as temporary:
                package = Path(temporary) / "Пилот с пробелом"
                shutil.copytree(PACKAGE, package)
                candidate = package / "golden/TASK-0001.json"
                git_bash_path = "/" + candidate.drive[0].lower() + candidate.as_posix()[2:]
                result = self.invoke(package, "run", "TASK-0001", git_bash_path)
                self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(os.name == "nt", "PowerShell hook runs in Windows CI")
    def test_windows_powershell_hook(self):
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "Пилот с пробелом"
            shutil.copytree(PACKAGE, package)
            hook = package / ".clinerules/hooks/PreToolUse.ps1"
            for path, blocked in (("submissions/TASK-0002.json", False), ("contracts/c-working-bcreq.schema.json", True)):
                payload = {"hookName": "PreToolUse", "preToolUse": {"toolName": "editor", "parameters": {"path": str(package / path)}}}
                result = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(hook)],
                                        input=json.dumps(payload, ensure_ascii=False), cwd=package,
                                        text=True, capture_output=True, encoding="utf-8")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["cancel"], blocked, result.stdout)

    @unittest.skipUnless(os.name == "nt", "PowerShell hook runs in Windows CI")
    def test_windows_hook_falls_back_to_py_launcher(self):
        # Without "Add python.exe to PATH" the name python is the Microsoft Store alias (exit 9009)
        # and only the py launcher starts Python.
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "Пилот с пробелом"
            shutil.copytree(PACKAGE, package)
            fake = Path(temporary) / "fake"
            fake.mkdir()
            (fake / "python.cmd").write_text("@exit /b 9009\r\n", encoding="ascii")
            hook = package / ".clinerules/hooks/PreToolUse.ps1"
            env = dict(os.environ, PATH=os.pathsep.join((str(fake), os.environ["PATH"])))
            for launcher, path, cancel in (
                (f'@"{sys.executable}" %2\r\n', "submissions/TASK-0002.json", False),
                (f'@"{sys.executable}" %2\r\n', "contracts/c-working-bcreq.schema.json", True),
                ("@exit /b 9009\r\n", "submissions/TASK-0002.json", True),
            ):
                (fake / "py.cmd").write_text(launcher, encoding="ascii")
                payload = {"hookName": "PreToolUse", "preToolUse": {"toolName": "editor", "parameters": {"path": str(package / path)}}}
                result = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                                         "-File", str(hook)], input=json.dumps(payload, ensure_ascii=False), cwd=package,
                                        env=env, text=True, capture_output=True, encoding="utf-8")
                self.assertEqual(result.returncode, 0, result.stderr)
                response = json.loads(result.stdout)
                self.assertEqual(response["cancel"], cancel, result.stdout)
                if launcher.startswith("@exit"):
                    self.assertIn("Windows hook failed", response["errorMessage"])

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
            blocked = subprocess.run([sys.executable, str(package / ".clinerules/hooks/PreToolUse")], input=json.dumps(payload), cwd=package, text=True, capture_output=True)
            self.assertEqual(blocked.returncode, 0, blocked.stderr)
            self.assertTrue(json.loads(blocked.stdout)["cancel"])
            payload["preToolUse"]["parameters"]["path"] = "submissions/TASK-0002.json"
            allowed = subprocess.run([sys.executable, str(package / ".clinerules/hooks/PreToolUse")], input=json.dumps(payload), cwd=package, text=True, capture_output=True)
            self.assertFalse(json.loads(allowed.stdout)["cancel"])
            payload["preToolUse"]["parameters"]["path"] = "submissions/../contracts/c-working-bcreq.schema.json"
            traversal = subprocess.run([sys.executable, str(package / ".clinerules/hooks/PreToolUse")], input=json.dumps(payload), cwd=package, text=True, capture_output=True)
            self.assertTrue(json.loads(traversal.stdout)["cancel"])
            payload["preToolUse"]["toolName"] = "execute_command"
            shell = subprocess.run([sys.executable, str(package / ".clinerules/hooks/PreToolUse")], input=json.dumps(payload), cwd=package, text=True, capture_output=True)
            self.assertTrue(json.loads(shell.stdout)["cancel"])
            (package / "tools/bcreq_pipeline.py").write_text("pass\n")
            check = self.invoke(package, "check-package")
            self.assertNotEqual(check.returncode, 0)

    def test_guide_links_resolve(self):
        # Source guides link to each other relatively; the compiler pins every link of the
        # package to the Source revision, so a copied package has only absolute URLs (#644).
        def slug(heading):
            text = re.sub(r"`|\*|\[|\]\([^)]*\)", "", heading).strip().lower()
            return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")

        def anchors(path):
            text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
            return {slug(item) for item in re.findall(r"^#{1,6}\s+(.*)$", text, re.M)} | set(
                re.findall(r'<a id="([^"]+)"', text))

        def links(path):
            text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
            return re.findall(r"\]\(([^)\s]+)\)", text)

        source = PACKAGE.parents[1] / "build"
        for path in (source / "adapters/cline-vscode/docs/guides").glob("*.md"):
            for target in links(path):
                if target.startswith(("http://", "https://")):
                    continue
                name, _, anchor = target.partition("#")
                linked = (path.parent / name).resolve() if name else path
                self.assertTrue(linked.exists(), f"{path.name}: {target}")
                if anchor:
                    self.assertIn(anchor, anchors(linked), f"{path.name}: {target}")

        manifest = json.loads((PACKAGE / "package-manifest.yaml").read_text(encoding="utf-8"))
        pinned = (f"{manifest['source']['repository']}/blob/{manifest['source']['revision']}"
                  "/projects/ba-ai-process/build/")
        checked = 0
        for path in PACKAGE.rglob("*.md"):
            if "docs/kb" in path.relative_to(PACKAGE).as_posix():
                continue
            for target in links(path):
                self.assertRegex(target, r"^https?://", f"{path.relative_to(PACKAGE)}: {target}")
                if not target.startswith(pinned):
                    continue
                checked += 1
                location, _, anchor = target[len(pinned):].partition("#")
                self.assertTrue((source / location).is_file(), f"{path.name}: {target}")
                inside = location.removeprefix("adapters/cline-vscode/").removeprefix("common/")
                self.assertTrue((PACKAGE / inside).is_file(), f"{path.name}: {target}")
                if anchor:
                    self.assertIn(anchor, anchors(PACKAGE / inside), f"{path.name}: {target}")
        self.assertGreater(checked, 50)

    def test_guide_real_task_flow(self):
        guide = (PACKAGE / "docs/guides/05-commands-reference.md").read_text(encoding="utf-8")
        self.assertIn("python tools/run_task.py seal submissions/TASK-0002.json", guide)
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
            sealed = self.invoke(package, "seal", "submissions/TASK-0003.json")
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
