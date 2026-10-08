#!/usr/bin/env python3
"""Executable contract for the standalone OpenCode BCREQ pilot."""

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


PACKAGE = Path(__file__).resolve().parents[2] / "dist/execution-package-opencode"
PROJECT = PACKAGE.parents[1]


class PackageTest(unittest.TestCase):
    def test_compiler_survives_autocrlf_checkout_of_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source"
            clone = Path(temporary) / "clone"
            target = source / "projects/ba-ai-process"
            (target / "build").mkdir(parents=True)
            shutil.copy2(PROJECT / "build/compile-opencode-package.py", target / "build")
            shutil.copytree(PROJECT / "build/common", target / "build/common")
            shutil.copytree(PROJECT / "build/adapters/opencode", target / "build/adapters/opencode")
            shutil.copytree(PACKAGE, target / "dist/execution-package-opencode")
            subprocess.run(["git", "init", "-q", str(source)], check=True)
            subprocess.run(["git", "-C", str(source), "add", "."], check=True)
            subprocess.run(["git", "-C", str(source), "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                            "commit", "-qm", "test source and package"], check=True)
            subprocess.run(["git", "-c", "core.autocrlf=true", "clone", "-q", str(source), str(clone)], check=True)
            result = subprocess.run([sys.executable, str(clone / "projects/ba-ai-process/build/compile-opencode-package.py"), "--check"],
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

    def test_opencode_runtime_files_do_not_break_integrity(self):
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "package"
            shutil.copytree(PACKAGE, package)
            # OpenCode installs its plugin SDK into .opencode at start-up.
            (package / ".opencode/node_modules/@opencode-ai/plugin").mkdir(parents=True)
            (package / ".opencode/node_modules/@opencode-ai/plugin/index.js").write_text("export {}\n")
            for name in ("package.json", "package-lock.json", "bun.lock"):
                (package / ".opencode" / name).write_text("{}\n")
            self.assertEqual(self.invoke(package, "check-package").returncode, 0)
            (package / ".opencode/commands/extra.md").write_text("extra\n")
            self.assertNotEqual(self.invoke(package, "check-package").returncode, 0)

    def test_permission_rules_deny_by_default(self):
        config = json.loads((PACKAGE / "opencode.json").read_text(encoding="utf-8"))
        permission = config["permission"]
        self.assertEqual(permission["*"], "deny")
        for tool in ("bash", "task", "skill", "webfetch", "websearch", "external_directory"):
            self.assertEqual(permission[tool], "deny", tool)
        self.assertEqual(permission["edit"]["*"], "deny")
        self.assertEqual(permission["edit"]["submissions/TASK-*.json"], "ask")
        self.assertEqual(config["agent"]["plan"]["permission"]["edit"], "deny")
        self.assertEqual(config["share"], "disabled")

    def hook(self, package, event):
        result = subprocess.run([sys.executable, str(package / "tools/opencode_hook.py")], input=json.dumps(event),
                                cwd=package, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_hook_policy(self):
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "Пилот с пробелом"
            shutil.copytree(PACKAGE, package)
            outside = str(Path(temporary) / "outside.json")
            directory = str(package)
            patch = "*** Begin Patch\n*** Add File: submissions/TASK-0002.json\n+{}\n*** End Patch"
            moved = "*** Begin Patch\r\n*** Update File: submissions/TASK-0002.json\r\n*** Move to: contracts/x.json\r\n*** End Patch"
            for tool, args, allowed in (
                ("read", {"filePath": "README.md"}, True),
                ("grep", {"pattern": "BCREQ"}, True),
                ("question", {"questions": []}, True),
                ("write", {"filePath": "submissions/TASK-0002.json", "content": "{}"}, True),
                ("write", {"filePath": str(package / "submissions/TASK-0002.json"), "content": "{}"}, True),
                ("edit", {"filePath": "submissions/TASK-12345.json"}, True),
                ("write", {"filePath": "submissions/TASK-abc.json"}, False),
                ("write", {"filePath": "submissions/nested/TASK-0002.json"}, False),
                ("write", {"filePath": "submissions/../contracts/c-working-bcreq.schema.json"}, False),
                ("edit", {"filePath": "opencode.json"}, False),
                ("edit", {"filePath": ".opencode/plugins/bcreq-guard.js"}, False),
                ("write", {"filePath": outside}, False),
                ("write", {}, False),
                ("apply_patch", {"patchText": patch}, True),
                ("apply_patch", {"patchText": moved}, False),
                ("apply_patch", {"patchText": "no envelope"}, False),
                ("bash", {"command": "echo unsafe"}, False),
                ("task", {"prompt": "x"}, False),
                ("webfetch", {"url": "https://example.invalid"}, False),
                ("kb-readonly_search_issues", {"jql": "project = BCREQ"}, True),
                ("kb-readonly_get_page", {"id": "1"}, True),
                ("kb-readonly_create_issue", {}, False),
                ("kb-readonly_search_and_update", {}, False),
                ("jira_search", {}, False),
                ("read_mcp_resource", {"server": "kb-readonly", "uri": "x"}, True),
                ("read_mcp_resource", {"server": "other", "uri": "x"}, False),
            ):
                verdict = self.hook(package, {"event": "tool.execute.before", "tool": tool, "args": args,
                                              "directory": directory})
                self.assertEqual(verdict["allow"], allowed, f"{tool} {args}: {verdict}")
            # OpenCode resolves relative paths against the directory where it was started.
            nested = self.hook(package, {"event": "tool.execute.before", "tool": "write",
                                         "args": {"filePath": "TASK-0002.json"}, "directory": str(package / "submissions")})
            self.assertTrue(nested["allow"], nested)
            self.assertFalse(self.hook(package, {"event": "unknown"})["allow"])
            (package / "tools/bcreq_pipeline.py").write_text("pass\n")
            tampered = self.hook(package, {"event": "tool.execute.before", "tool": "read", "args": {}, "directory": directory})
            self.assertFalse(tampered["allow"])
            self.assertIn("integrity", tampered["reason"])

    @unittest.skipUnless(shutil.which("node"), "Node.js runs the OpenCode plugin")
    def test_guard_plugin_cancels_blocked_calls(self):
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "Пилот с пробелом"
            shutil.copytree(PACKAGE, package)
            probe = Path(temporary) / "probe.mjs"
            probe.write_text("""
import { pathToFileURL } from "node:url"
const [plugin, directory] = process.argv.slice(2)
const { BcreqGuard } = await import(pathToFileURL(plugin).href)
const hooks = await BcreqGuard({ directory })
const results = []
for (const [tool, filePath] of [["write", "submissions/TASK-0002.json"], ["edit", "contracts/c-working-bcreq.schema.json"], ["bash", ""]]) {
  try {
    await hooks["tool.execute.before"]({ tool }, { args: { filePath, command: "echo" } })
    results.push("allowed")
  } catch (error) {
    results.push(error.message)
  }
}
console.log(JSON.stringify(results))
""", encoding="utf-8")
            result = subprocess.run(["node", str(probe), str(package / ".opencode/plugins/bcreq-guard.js"), str(package)],
                                    text=True, capture_output=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            allowed, edit, bash = json.loads(result.stdout)
            self.assertEqual(allowed, "allowed")
            self.assertEqual(edit, "BCREQ guard: OpenCode may write only submissions/TASK-ID.json")
            self.assertTrue(bash.startswith("BCREQ guard: "), bash)

    def command(self, package, *args, env=None):
        environment = {key: value for key, value in os.environ.items() if not key.startswith("OPENCODE_")}
        environment.update(env or {})
        return subprocess.run([sys.executable, str(package / "tools/opencode_command.py"), *args], cwd=package,
                              text=True, capture_output=True, env=environment, encoding="utf-8")

    def test_package_commands(self):
        for name in ("bcreq-check", "bcreq-start", "bcreq-gate"):
            text = (PACKAGE / ".opencode/commands" / f"{name}.md").read_text(encoding="utf-8")
            self.assertIn("agent: plan", text, name)
        start = (PACKAGE / ".opencode/commands/bcreq-start.md").read_text(encoding="utf-8")
        self.assertIn("$ARGUMENTS", start)
        self.assertNotIn("!`", start)
        gate = (PACKAGE / ".opencode/commands/bcreq-gate.md").read_text(encoding="utf-8")
        self.assertIn("!`python tools/opencode_command.py gate '$1'`", gate)
        # OpenCode on Windows drops the output of a !`...` block that exits with 1 (cross-spawn reports
        # ENOENT), so every command exits 0 and reports the result in its `exit code:` line.
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "Пилот с пробелом"
            shutil.copytree(PACKAGE, package)
            check = self.command(package, "check")
            self.assertEqual(check.returncode, 0, check.stdout)
            self.assertIn("package: PASS\nexit code: 0", check.stdout)
            for name in ("OPENCODE_PURE", "OPENCODE_DISABLE_PROJECT_CONFIG", "OPENCODE_PERMISSION",
                         "OPENCODE_CONFIG_CONTENT", "OPENCODE_DISABLE_DEFAULT_PLUGINS"):
                overridden = self.command(package, "check", env={name: "1"})
                self.assertEqual(overridden.returncode, 0, name)
                self.assertIn(f"ERROR: OpenCode protection overrides are set: {name}\nexit code: 1", overridden.stdout)
            for raw in ("x;y", "TASK-0002; echo pwned", "BCREQ-123", "TASK-12", ""):
                rejected = self.command(package, "gate", raw)
                self.assertEqual(rejected.returncode, 0, raw)
                self.assertIn("ERROR: task ID must match TASK-0001", rejected.stdout)
                self.assertIn("exit code: 1", rejected.stdout)
            missing = self.command(package, "gate", "TASK-0009")
            self.assertEqual(missing.returncode, 0)
            self.assertIn("exit code: 1", missing.stdout)
            self.assertNotIn("run TASK-0009", missing.stdout)
            self.assertFalse((package / "runs/TASK-0009").exists())
            shutil.copy2(package / "golden/TASK-0001.json", package / "submissions/TASK-0001.json")
            # cmd.exe keeps the single quotes of '$1'.
            passed = self.command(package, "gate", "'TASK-0001'")
            self.assertEqual(passed.returncode, 0, passed.stdout)
            self.assertIn("sealed: submissions/TASK-0001.json\nexit code: 0", passed.stdout)
            self.assertIn("TASK-0001: PASS\nexit code: 0", passed.stdout)
            # Sealing a sealed file changes nothing; on Windows the runner writes CRLF.
            self.assertEqual(json.loads((package / "submissions/TASK-0001.json").read_text(encoding="utf-8")),
                             json.loads((package / "golden/TASK-0001.json").read_text(encoding="utf-8")))
            # A Windows console code page: the runner reports the Cyrillic package path.
            rerun = self.command(package, "gate", "TASK-0001", env={"PYTHONIOENCODING": "cp1252"})
            self.assertIn("ERROR: run already exists", rerun.stdout, rerun.stdout + rerun.stderr)
            self.assertIn("exit code: 1", rerun.stdout, rerun.stdout + rerun.stderr)
            self.assertEqual(rerun.returncode, 0)
            self.assertEqual(self.command(package, "verify").returncode, 0)
            unknown = self.command(package, "unknown")
            self.assertEqual(unknown.returncode, 0)
            self.assertIn("exit code: 2", unknown.stdout)

    def test_git_bash_drive_path_normalization(self):
        spec = importlib.util.spec_from_file_location("run_task_windows", PACKAGE / "tools/run_task.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.normalize_windows_path("/c/Users/Иван Петров/bcreq-pilot/runtime/submissions/TASK-0002.json"),
                         "C:\\Users\\Иван Петров\\bcreq-pilot\\runtime\\submissions\\TASK-0002.json")

    def test_one_environment_boundary(self):
        other_clients = re.compile(r"\b(?:Cline|GigaCode|Qwen(?: Chat)?|Kilo Code|Roo Code)\b", re.I)
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

    def test_guide_links_resolve(self):
        def slug(heading):
            text = re.sub(r"`|\*|\[|\]\([^)]*\)", "", heading).strip().lower()
            return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")

        guides = PACKAGE / "docs/guides"
        expected = {"README.md", "01-junior-pilot.md", "02-install.md", "03-deploy-package.md", "04-smoke-test.md",
                    "05-commands-reference.md", "06-working-with-opencode.md"}
        self.assertEqual({path.name for path in guides.glob("*.md")}, expected)
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
                self.assertFalse(target.startswith(("/", "www.")), f"{path.name}: {target}")
                name, _, anchor = target.partition("#")
                name = name or path.name
                self.assertTrue((guides / name).is_file(), f"{path.name}: {target}")
                if anchor and name.endswith(".md"):
                    self.assertIn(anchor, anchors[name], f"{path.name}: {target}")

    def test_guide_real_task_flow(self):
        guide = (PACKAGE / "docs/guides/06-working-with-opencode.md").read_text(encoding="utf-8")
        for needle in ("/bcreq-start TASK-0002", "/bcreq-gate TASK-0002", "Allow once",
                       "Move-Item submissions\\TASK-0002.json runs\\TASK-0002\\working.json"):
            self.assertIn(needle, guide)
        reference = (PACKAGE / "docs/guides/05-commands-reference.md").read_text(encoding="utf-8")
        self.assertIn("python tools/run_task.py seal submissions/TASK-0002.json", reference)
        with tempfile.TemporaryDirectory() as temporary:
            package = Path(temporary) / "package"
            shutil.copytree(PACKAGE, package)
            data = json.loads((package / "golden/TASK-0001.json").read_text(encoding="utf-8"))
            data["evidence"][0]["locator"] = "https://jira.example.test/browse/BCREQ-123"
            data["evidence"][0]["excerpt"] = "Клиент должен выгружать журнал звонков."
            edited = json.dumps(data, ensure_ascii=False, indent=2)
            (package / "submissions/TASK-0002.json").write_text(edited, encoding="utf-8")
            unsealed = self.invoke(package, "run", "TASK-0002", "submissions/TASK-0002.json")
            self.assertNotEqual(unsealed.returncode, 0)
            self.assertIn("Working digest does not match", unsealed.stderr)
            (package / "submissions/TASK-0002.json").rename(package / "runs/TASK-0002/working.json")
            # The corrected draft gets a new TASK ID; /bcreq-gate seals it before the run.
            (package / "submissions/TASK-0003.json").write_text(edited, encoding="utf-8")
            accepted = self.command(package, "gate", "TASK-0003")
            self.assertEqual(accepted.returncode, 0, accepted.stdout)
            self.assertIn("TASK-0003: PASS", accepted.stdout)
            ci = self.invoke(package, "verify-ci")
            self.assertEqual(ci.returncode, 0, ci.stderr)
            self.assertIn("submissions/TASK-0003.json: PASS", ci.stdout)
            self.assertEqual(self.invoke(package, "check-package").returncode, 0)


if __name__ == "__main__":
    unittest.main()
