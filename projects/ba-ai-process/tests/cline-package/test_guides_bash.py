#!/usr/bin/env python3
"""Executable contract for the guides of the Cline package (issue #644).

The analyst works on Windows 10/11 x64 with Git installed and runs commands in Git Bash,
the terminal profile VS Code detects next to Git. Every command block of the guides is a
```bash block and is executed here verbatim by Git Bash on Windows CI and by bash
elsewhere. Set GUIDE_BASH to choose the shell; CI sets it so a missing shell fails.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[2] / "dist/execution-package-cline-vscode"
PACKAGE_PATH = "projects/ba-ai-process/dist/execution-package-cline-vscode"
GUIDES = PACKAGE / "docs/guides"
LAB_URL = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab.git"
KB_URL = "https://github.com/G-Ivan-A/mango-ba-ai-runtime.git"
PLACEHOLDER = re.compile(r"<[^>\n]+>")
TIMEOUT = 300


def guide_bash() -> str | None:
    configured = os.environ.get("GUIDE_BASH")
    if configured:
        return configured
    if os.name != "nt":
        return shutil.which("bash")
    # C:\Windows\System32\bash.exe is WSL, not Git Bash: take bash.exe of the installed Git.
    git = shutil.which("git")
    for parent in Path(git).resolve().parents if git else ():
        if (parent / "bin/bash.exe").is_file() and (parent / "usr/bin").is_dir():
            return str(parent / "bin/bash.exe")
    return None


def bash_blocks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return ["".join(line[len(match.group(1)):] for line in match.group(2).splitlines(True))
            for match in re.finditer(r"^( *)```bash\n(.*?)^\1```", text, re.M | re.S)]


def git(*args: str, cwd: Path) -> None:
    subprocess.run(["git", "-c", "user.name=guide", "-c", "user.email=guide@example.invalid",
                    "-c", "core.autocrlf=false", *args], cwd=cwd, check=True, capture_output=True,
                   timeout=TIMEOUT)


class StaticGuideTest(unittest.TestCase):
    def test_guides_are_git_bash_instructions(self) -> None:
        powershell = {
            "PowerShell block": re.compile(r"^ *```(?:powershell|pwsh|ps1)\s*$", re.M),
            "PowerShell cmdlet": re.compile(r"\b(?:New|Copy|Move|Remove|Get|Set)-(?:Item|ChildItem|Location|Content)\b"),
            "PowerShell variable": re.compile(r"\$env:"),
            "PowerShell prompt": re.compile(r"\bPS C:"),
        }
        documents = [*sorted(GUIDES.glob("*.md")), PACKAGE / "README.md", PACKAGE / "AGENTS.md",
                     PACKAGE / ".clinerules/01-package.md"]
        for path in documents:
            text = path.read_text(encoding="utf-8")
            for label, pattern in powershell.items():
                found = pattern.search(text)
                self.assertIsNone(found, f"{path.relative_to(PACKAGE)}: {label}: "
                                         f"{found and text[max(0, found.start() - 40):found.end() + 40]!r}")
        for path in GUIDES.glob("*.md"):
            if path.name not in ("README.md", "01-junior-pilot.md"):
                self.assertTrue(bash_blocks(path), f"{path.name} has no Git Bash commands")
        for path in (PACKAGE / "AGENTS.md", PACKAGE / ".clinerules/01-package.md"):
            self.assertIn("Git Bash", path.read_text(encoding="utf-8"), path.name)

    def test_blocks_use_only_what_git_bash_provides(self) -> None:
        # Git for Windows has no python3 (the name may start the Microsoft Store), no sudo or
        # package manager, and POSIX example paths do not exist on the analyst's computer.
        forbidden = re.compile(r"\bpython3\b|\bsudo\b|\bapt(?:-get)?\b|/tmp/|/path/to|/home/|\\")
        for path in [*sorted(GUIDES.glob("*.md")), PACKAGE / "README.md"]:
            for block in bash_blocks(path):
                found = forbidden.search(block)
                self.assertIsNone(found, f"{path.name}: {block!r}")


class GitBashGuideTest(unittest.TestCase):
    def setUp(self) -> None:
        self.bash = guide_bash()
        if not self.bash:
            self.skipTest("no Git Bash: set GUIDE_BASH or install Git for Windows")
        self.temporary = tempfile.TemporaryDirectory(prefix="cline-guide-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        # A Windows account name often has a space and Cyrillic letters.
        self.home = self.root / "Иван Петров"
        self.home.mkdir()
        tools = self.root / "tools"
        tools.mkdir()
        if os.name != "nt":
            # "Add python.exe to PATH" gives the command name python, not python3.
            (tools / "python").symlink_to(sys.executable)
        self.env = dict(os.environ, HOME=str(self.home), USERPROFILE=str(self.home),
                        PYTHONIOENCODING="utf-8",
                        # Git for Windows installs with core.autocrlf=true by default.
                        GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="core.autocrlf", GIT_CONFIG_VALUE_0="true")
        self.env["PATH"] = os.pathsep.join((str(tools), str(Path(sys.executable).parent), self.env["PATH"]))
        self.count = 0

    def run_block(self, cwd: Path, block: str, parse_only: bool = False) -> tuple[int, str]:
        self.count += 1
        script = self.root / f"block-{self.count}.sh"
        script.write_text(block, encoding="utf-8", newline="\n")
        argv = [self.bash, "--noprofile", "--norc", *(["-n"] if parse_only else ["-e"]), script.as_posix()]
        result = subprocess.run(argv, cwd=cwd, env=self.env, stdin=subprocess.DEVNULL, capture_output=True,
                                encoding="utf-8", errors="replace", timeout=TIMEOUT)
        return result.returncode, result.stdout + result.stderr

    def run_blocks(self, cwd: Path, blocks: list[str]) -> str:
        outputs = []
        for block in blocks:
            code, output = self.run_block(cwd, block)
            self.assertEqual(code, 0, f"{block}\n{output}")
            outputs.append(output)
        return "".join(outputs)

    def deploy(self) -> Path:
        # The public repositories are replaced by local repositories of the same layout,
        # so the test deploys this revision of the package and needs no network.
        lab = self.root / "lab"
        shutil.copytree(PACKAGE, lab / PACKAGE_PATH)
        kb = self.root / "kb"
        (kb / "docs/kb/sip-trunk").mkdir(parents=True)
        (kb / "docs/kb/.gitkeep").write_text("", encoding="utf-8")
        (kb / "docs/kb/README.md").write_text("# База знаний\n", encoding="utf-8")
        (kb / "docs/kb/MAP.json").write_text("{}\n", encoding="utf-8")
        (kb / "docs/kb/sip-trunk/overview.md").write_text("# SIP-транк\n", encoding="utf-8")
        for repository in (lab, kb):
            git("init", "-q", cwd=repository)
            git("add", "-A", cwd=repository)
            git("commit", "-q", "-m", "fixture", cwd=repository)
        guide = (GUIDES / "03-deploy-package.md").read_text(encoding="utf-8")
        before_open, _, _ = guide.partition("## Откройте пакет в VS Code")
        deploy = [block for block in bash_blocks(GUIDES / "03-deploy-package.md")
                  if block in before_open and not PLACEHOLDER.search(block)]
        script = "\n".join(deploy).replace(LAB_URL, lab.as_uri()).replace(KB_URL, kb.as_uri())
        self.assertIn(lab.as_uri(), script)
        self.assertIn(kb.as_uri(), script)
        # The analyst types these blocks in one terminal opened at the home folder, so cd carries over.
        output = self.run_blocks(self.home, [script])
        runtime = self.home / "bcreq-pilot/runtime"
        for name in (".clinerules", ".github", ".gitattributes", ".gitignore", "AGENTS.md", "tools", "docs/kb/.gitkeep",
                     "docs/kb/MAP.json", "docs/kb/sip-trunk/overview.md"):
            self.assertTrue((runtime / name).exists(), f"deploy lost {name}")
            if not name.startswith("docs/kb/"):
                self.assertIn(name.split("/")[0], output, "the ls -a check must show the package")
        return runtime

    def test_every_documented_block_parses(self) -> None:
        checked = 0
        for path in [*sorted(GUIDES.glob("*.md")), PACKAGE / "README.md"]:
            for block in bash_blocks(path):
                code, output = self.run_block(self.root, PLACEHOLDER.sub("placeholder", block), parse_only=True)
                self.assertEqual(code, 0, f"{path.name}:\n{block}\n{output}")
                checked += 1
        self.assertGreater(checked, 12)

    def test_install_check_runs_verbatim(self) -> None:
        block, = [block for block in bash_blocks(GUIDES / "02-install.md") if "git --version" in block]
        if not shutil.which("code"):
            block = "\n".join(line for line in block.splitlines() if not line.startswith("code "))
        output = self.run_blocks(self.home, [block])
        self.assertRegex(output, r"git version 2\.")
        self.assertRegex(output, r"Python 3\.(?:1[1-9]|[2-9]\d)")

    def test_deploy_and_smoke_guides_run_verbatim(self) -> None:
        runtime = self.deploy()
        # VS Code opens the terminal of the runtime folder in that folder.
        after_open = (GUIDES / "03-deploy-package.md").read_text(encoding="utf-8").partition(
            "## Откройте пакет в VS Code")[2]
        checks = [block for block in bash_blocks(GUIDES / "03-deploy-package.md") if block in after_open]
        self.assertIn("package: PASS", self.run_blocks(runtime, checks))
        output = self.run_blocks(runtime, bash_blocks(GUIDES / "04-smoke-test.md"))
        self.assertEqual(output.count("TASK-0001: PASS"), 2, output)
        self.assertTrue((runtime / "runs/TASK-0001/release.json").is_file())
        self.assertTrue((runtime / "golden/TASK-0001.json").is_file())

    def test_real_task_commands_run_verbatim(self) -> None:
        runtime = self.deploy()
        commands = GUIDES / "05-commands-reference.md"
        working = GUIDES / "06-working-with-cline.md"
        # Cline writes the analyst's draft; the guide does the rest.
        data = json.loads((runtime / "golden/TASK-0001.json").read_text(encoding="utf-8"))
        data["evidence"][0]["locator"] = "https://jira.example.test/browse/BCREQ-123"
        data["evidence"][0]["excerpt"] = "Клиент должен выгружать журнал звонков."
        (runtime / "submissions/TASK-0002.json").write_text(json.dumps(data, ensure_ascii=False, indent=2),
                                                             encoding="utf-8")
        seal, = [block for block in bash_blocks(commands) if " seal " in block]
        self.assertIn("sealed: submissions/TASK-0002.json", self.run_blocks(runtime, [seal]))
        run, = [block for block in bash_blocks(working) if " run TASK-0002 " in block]
        self.assertIn("TASK-0002: PASS", self.run_blocks(runtime, [run]))
        debug = [block for block in bash_blocks(commands) if "bcreq-pilot/debug" in block]
        self.assertEqual(len(debug), 2, debug)
        output = self.run_blocks(runtime, debug)
        self.assertEqual(output.count("G-mach: BCREQ accepted"), 3, output)
        self.assertTrue((self.home / "bcreq-pilot/debug/TASK-0002/release-manifest.json").is_file())
        move, = [block for block in bash_blocks(working) if block.startswith("mv ")]
        self.assertEqual([move], [block for block in bash_blocks(commands) if block.startswith("mv ")])
        self.run_blocks(runtime, [move])
        self.assertTrue((runtime / "runs/TASK-0002/working.json").is_file())
        self.assertFalse((runtime / "submissions/TASK-0002.json").exists())
        self.assertIn("golden/TASK-0001.json: PASS", self.run_blocks(runtime, ["python tools/run_task.py verify-ci"]))
        self.assertIn("package: PASS", self.run_blocks(runtime, ["python tools/run_task.py check-package"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
