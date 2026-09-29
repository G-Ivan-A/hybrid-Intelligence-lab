#!/usr/bin/env python3
"""Executable contract for the BA guide cluster of the GigaCode package."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[3] / "dist/execution-package-gigacode-cli"
GUIDES = PACKAGE / "docs/guides"
FIXTURE = Path(__file__).resolve().parents[1] / "fixtures/working-valid.json"
ENV = dict(os.environ, PATH=f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}")


def sh_blocks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return ["".join(line[len(match.group(1)):] for line in match.group(2).splitlines(True))
            for match in re.finditer(r"^( *)```sh\n(.*?)^\1```", text, re.M | re.S)]


def run_block(package: Path, block: str) -> subprocess.CompletedProcess:
    """Runs a guide block as a person would; APPROVE is typed into a pseudo terminal."""
    found = re.search(r"advance (TASK-\d{4}) .*--checkpoint (\S+)", block)
    if not found:
        return subprocess.run(["sh", "-c", block], cwd=package, env=ENV, text=True,
                              capture_output=True, stdin=subprocess.DEVNULL)
    state = json.loads((package / "runs" / found.group(1) / "state.json").read_text(encoding="utf-8"))
    digest = hashlib.sha256((package / found.group(2)).read_bytes()).hexdigest()
    master, slave = os.openpty()
    try:
        os.write(master, f"APPROVE {found.group(1)}:{state['current']} sha256:{digest}\n".encode())
        return subprocess.run(["sh", "-c", block], cwd=package, env=ENV, text=True,
                              capture_output=True, stdin=slave)
    finally:
        os.close(slave)
        os.close(master)


class GuideTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.package = Path(self.temporary.name) / "runtime"
        shutil.copytree(PACKAGE, self.package)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_cluster_matches_cline_layout(self) -> None:
        names = sorted(path.name for path in GUIDES.glob("*.md"))
        self.assertEqual(names, ["01-junior-pilot.md", "02-install.md", "03-deploy-package.md",
                                 "04-smoke-test.md", "05-commands-reference.md",
                                 "06-working-with-gigacode.md", "README.md"])
        self.assertFalse((PACKAGE / "junior-guide.md").exists())

    def test_guide_links_resolve(self) -> None:
        def slug(heading: str) -> str:
            text = re.sub(r"`|\*|\[|\]\([^)]*\)", "", heading).strip().lower()
            return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")

        anchors = {}
        for path in GUIDES.glob("*.md"):
            text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
            anchors[path.name] = {slug(item) for item in re.findall(r"^#{1,6}\s+(.*)$", text, re.M)}
            anchors[path.name] |= set(re.findall(r'<a id="([^"]+)"', text))
        for path in GUIDES.glob("*.md"):
            text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
            for target in re.findall(r"\]\(([^)\s]+)\)", text):
                if target.startswith(("http://", "https://")):
                    continue
                name, _, anchor = target.partition("#")
                resolved = (path.parent / (name or path.name)).resolve()
                self.assertTrue(resolved.is_file(), f"{path.name}: {target}")
                if anchor and resolved.parent == GUIDES.resolve():
                    self.assertIn(anchor, anchors[resolved.name], f"{path.name}: {target}")

    def test_smoke_guide_runs_verbatim(self) -> None:
        guide = GUIDES / "04-smoke-test.md"
        outputs = []
        for block in sh_blocks(guide):
            result = run_block(self.package, block)
            self.assertEqual(result.returncode, 0, f"{block}\n{result.stdout}{result.stderr}")
            outputs.append(result.stdout)
        text = guide.read_text(encoding="utf-8")
        for expected in ("TASK-0001: started at entry; next transition requires G-mach",
                         "TASK-0001: entry -> n0; G-mach exit 0; trace seq 1",
                         "TASK-0001: n0 -> n1; G-mach exit 0; trace seq 2"):
            self.assertIn(expected, text)
            self.assertIn(expected, "".join(outputs))
        metrics = re.search(r'^ *(\{"current": "n1".*\})$', text, re.M)
        self.assertIsNotNone(metrics, "metrics output is missing from the guide")
        self.assertIn(metrics.group(1), "".join(outputs))
        self.assertFalse((self.package / "runs/TASK-0001").exists(), "last block must reset the run")

    def test_documented_sealing_command(self) -> None:
        seal = next(block for block in sh_blocks(GUIDES / "05-commands-reference.md")
                    if block.startswith("python3 - runs/TASK-0002/evidence/working.json <<'EOF'"))
        evidence = self.package / "runs/TASK-0002/evidence"
        evidence.mkdir(parents=True)
        shutil.copy(FIXTURE, evidence / "working.json")
        validate = [sys.executable, "tools/bcreq_pipeline.py", "validate-working",
                    "runs/TASK-0002/evidence/working.json"]
        before = subprocess.run(validate, cwd=self.package, text=True, capture_output=True)
        self.assertNotEqual(before.returncode, 0)
        sealed = subprocess.run(["sh", "-c", seal], cwd=self.package, env=ENV, text=True,
                                capture_output=True)
        self.assertEqual(sealed.returncode, 0, sealed.stderr)
        self.assertIn("sealed: runs/TASK-0002/evidence/working.json", sealed.stdout)
        after = subprocess.run(validate, cwd=self.package, text=True, capture_output=True)
        self.assertEqual(after.returncode, 0, after.stdout + after.stderr)
        self.assertIn("G-mach: BCREQ accepted", after.stdout)

    def test_documented_refusals_exist_in_runner(self) -> None:
        runner = (PACKAGE / "tools/run-task.py").read_text(encoding="utf-8")
        guide = (GUIDES / "06-working-with-gigacode.md").read_text(encoding="utf-8")
        messages = re.findall(r"`BLOCKED: ([^`]+)`", guide)
        self.assertGreater(len(messages), 10)
        for message in messages:
            stem = re.split(r" n?\d|: …| …", message)[0]
            self.assertTrue(stem in runner, f"{message!r} is not a runner refusal")


if __name__ == "__main__":
    unittest.main()
