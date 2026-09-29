#!/usr/bin/env python3
"""Executable contract for the BA guide cluster of the GigaCode package.

The guides target Windows 10/11 only, so every command block is a ```powershell
block and is executed here by Windows PowerShell 5.1 (`powershell`) or PowerShell 7
(`pwsh`). Set GUIDE_SHELL to choose the shell; CI sets it so a missing shell fails.
"""

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
import time
import unittest


PACKAGE = Path(__file__).resolve().parents[3] / "dist/execution-package-gigacode-cli"
PACKAGE_PATH = "projects/ba-ai-process/dist/execution-package-gigacode-cli"
GUIDES = PACKAGE / "docs/guides"
FIXTURE = Path(__file__).resolve().parents[1] / "fixtures/working-valid.json"
LAB_URL = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab.git"
KB_URL = "https://github.com/G-Ivan-A/mango-ba-ai-runtime-cli.git"
APPROVAL = re.compile(r"Type exactly: (APPROVE \S+ sha256:[0-9a-f]{64})")
ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b[=>]")
TIMEOUT = 300

# Runs a guide block statement by statement, as a person types it at the prompt, and
# stops at the first cmdlet error or non-zero exit code of a native command. Native
# stderr (git progress, pip notices) is not an error, exactly as in a console window.
HARNESS = r"""param([string]$BlockPath, [switch]$ParseOnly)
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$text = [IO.File]::ReadAllText($BlockPath, [Text.Encoding]::UTF8)
$tokens = $null
$parseErrors = $null
$ast = [Management.Automation.Language.Parser]::ParseInput($text, [ref]$tokens, [ref]$parseErrors)
if ($parseErrors) {
    $parseErrors | ForEach-Object { [Console]::Error.WriteLine("PARSE: " + $_.Message) }
    exit 90
}
if ($ParseOnly) { exit 0 }
foreach ($statement in $ast.EndBlock.Statements) {
    $global:LASTEXITCODE = 0
    $before = $Error.Count
    . ([scriptblock]::Create($statement.Extent.Text)) | Out-Host
    $new = $Error.Count - $before
    $failed = @($Error | Select-Object -First $new |
        Where-Object { $_.FullyQualifiedErrorId -notlike 'NativeCommandError*' })
    if ($failed.Count -gt 0) {
        $failed | ForEach-Object { [Console]::Error.WriteLine("ERROR: " + $_) }
        exit 91
    }
    if ($LASTEXITCODE) { exit $LASTEXITCODE }
}
exit 0
"""


def guide_shell() -> str | None:
    configured = os.environ.get("GUIDE_SHELL")
    if configured:
        return configured
    return shutil.which("powershell") or shutil.which("pwsh")


def powershell_blocks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return ["".join(line[len(match.group(1)):] for line in match.group(2).splitlines(True))
            for match in re.finditer(r"^( *)```powershell\n(.*?)^\1```", text, re.M | re.S)]


def environment(**extra: str) -> dict[str, str]:
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8", **extra)
    env["PATH"] = f"{Path(sys.executable).parent}{os.pathsep}{env['PATH']}"
    return env


def interactive(argv: list[str], cwd: Path, env: dict[str, str]) -> tuple[int, str]:
    """Runs a command in a terminal and types the APPROVE line the runner asks for."""
    if os.name == "nt":
        import winpty  # pywinpty: the Windows console gives the runner a real terminal.

        process = winpty.PtyProcess.spawn(argv, cwd=str(cwd), env=env, dimensions=(24, 500))
        output, answered = "", False
        deadline = time.monotonic() + TIMEOUT
        while time.monotonic() < deadline:
            try:
                output += process.read(4096)
            except EOFError:
                break
            found = APPROVAL.search(ANSI.sub("", output))
            if found and not answered:
                process.write(found.group(1) + "\r\n")
                answered = True
        while process.isalive() and time.monotonic() < deadline:
            time.sleep(0.1)
        return process.exitstatus if process.exitstatus is not None else -1, ANSI.sub("", output)

    import select

    master, slave = os.openpty()
    process = subprocess.Popen(argv, cwd=cwd, env=env, stdin=slave, stdout=slave, stderr=slave,
                               start_new_session=True)
    os.close(slave)
    chunks, answered = b"", False
    deadline = time.monotonic() + TIMEOUT
    try:
        while time.monotonic() < deadline:
            ready, _, _ = select.select([master], [], [], 0.5)
            if not ready:
                if process.poll() is not None:
                    break
                continue
            try:
                data = os.read(master, 4096)
            except OSError:
                break
            if not data:
                break
            chunks += data
            found = APPROVAL.search(ANSI.sub("", chunks.decode("utf-8", "replace")))
            if found and not answered:
                os.write(master, (found.group(1) + "\r").encode())
                answered = True
    finally:
        os.close(master)
    return process.wait(timeout=TIMEOUT), ANSI.sub("", chunks.decode("utf-8", "replace"))


class GuideShell:
    def __init__(self, shell: str, workdir: Path, env: dict[str, str]) -> None:
        self.shell, self.workdir, self.env, self.count = shell, workdir, env, 0
        self.harness = workdir / "run-guide-block.ps1"
        self.harness.write_text(HARNESS, encoding="utf-8")

    def run(self, cwd: Path, block: str, parse_only: bool = False) -> tuple[int, str]:
        self.count += 1
        path = self.workdir / f"block-{self.count}.ps1"
        path.write_text(block, encoding="utf-8-sig")
        argv = [self.shell, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                "-File", str(self.harness), str(path), *(["-ParseOnly"] if parse_only else [])]
        if "--checkpoint" in block and not parse_only:
            return interactive(argv, cwd, self.env)
        result = subprocess.run(argv, cwd=cwd, env=self.env, stdin=subprocess.DEVNULL,
                                capture_output=True, encoding="utf-8", errors="replace",
                                timeout=TIMEOUT)
        return result.returncode, result.stdout + result.stderr


def git(*args: str, cwd: Path) -> None:
    subprocess.run(["git", "-c", "user.name=guide", "-c", "user.email=guide@example.invalid",
                    *args], cwd=cwd, check=True, capture_output=True, timeout=TIMEOUT)


class StaticGuideTest(unittest.TestCase):
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

    def test_package_docs_are_windows_only(self) -> None:
        # Windows 10/11 is the only target: no POSIX shells, paths or other platforms.
        forbidden = {
            "POSIX shell block": re.compile(r"^ *```(?:sh|bash|shell|console|zsh)\s*$", re.M),
            "POSIX home path": re.compile(r"(?<![\w$])~/"),
            "POSIX absolute path": re.compile(r"/home/|/usr/|/bin/"),
            "python3 command": re.compile(r"\bpython3\b"),
            "sh wrapper call": re.compile(r"\bsh tools/"),
            "venv activation": re.compile(r"venv/bin|bin/activate"),
            "heredoc": re.compile(r"<<'?EOF"),
            "non-target OS": re.compile(r"\b(?:Linux|WSL|macOS|Ubuntu|Debian)\b"),
        }
        documents = [*GUIDES.glob("*.md"), PACKAGE / "README.md", PACKAGE / "AGENTS.md",
                     *(PACKAGE / ".gigacode/skills").glob("*/SKILL.md")]
        for path in documents:
            text = path.read_text(encoding="utf-8")
            for label, pattern in forbidden.items():
                found = pattern.search(text)
                self.assertIsNone(found, f"{path.relative_to(PACKAGE)}: {label}: "
                                         f"{found and text[max(0, found.start() - 40):found.end() + 40]!r}")
        for path in GUIDES.glob("*.md"):
            if path.name not in ("README.md", "01-junior-pilot.md"):
                self.assertTrue(powershell_blocks(path), f"{path.name} has no PowerShell commands")

    def test_documented_refusals_exist_in_runner(self) -> None:
        runner = (PACKAGE / "tools/run-task.py").read_text(encoding="utf-8")
        guide = (GUIDES / "06-working-with-gigacode.md").read_text(encoding="utf-8")
        messages = re.findall(r"`BLOCKED: ([^`]+)`", guide)
        self.assertGreater(len(messages), 10)
        for message in messages:
            stem = re.split(r" n?\d|: …| …", message)[0]
            self.assertTrue(stem in runner, f"{message!r} is not a runner refusal")


class PowerShellGuideTest(unittest.TestCase):
    def setUp(self) -> None:
        shell = guide_shell()
        if not shell:
            self.skipTest("no PowerShell: set GUIDE_SHELL or install powershell/pwsh")
        self.temporary = tempfile.TemporaryDirectory(prefix="gigacode-guide-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.package = self.root / "runtime"
        shutil.copytree(PACKAGE, self.package)
        self.shell = GuideShell(shell, self.root, environment(USERPROFILE=str(self.home)))

    def run_blocks(self, cwd: Path, blocks: list[str]) -> str:
        outputs = []
        for block in blocks:
            code, output = self.shell.run(cwd, block)
            self.assertEqual(code, 0, f"{block}\n{output}")
            outputs.append(output)
        return "".join(outputs)

    def test_harness_stops_at_first_failed_statement(self) -> None:
        code, output = self.shell.run(self.root, "Get-Item missing-file\nWrite-Output reached")
        self.assertEqual(code, 91, output)
        self.assertNotIn("reached", output)
        code, output = self.shell.run(self.root, 'python -c "import sys; sys.exit(3)"\n'
                                                 "Write-Output reached")
        self.assertEqual(code, 3, output)
        self.assertNotIn("reached", output)
        code, output = self.shell.run(self.root, 'python -c "import sys; sys.stderr.write(\'note\')"\n'
                                                 "Write-Output reached")
        self.assertEqual(code, 0, output)
        self.assertIn("reached", output)
        code, output = self.shell.run(self.root, "python - <<EOF\nprint(1)\nEOF\n", parse_only=True)
        self.assertEqual(code, 90, output)

    def test_every_documented_block_parses(self) -> None:
        # Reference blocks with <placeholders> cannot run verbatim, but must be valid PowerShell.
        documents = [*sorted(GUIDES.glob("*.md")), PACKAGE / "README.md"]
        checked = 0
        for path in documents:
            for block in powershell_blocks(path):
                text = re.sub(r"<[^>\n]+>", "placeholder", block)
                code, output = self.shell.run(self.root, text, parse_only=True)
                self.assertEqual(code, 0, f"{path.name}:\n{block}\n{output}")
                checked += 1
        self.assertGreater(checked, 30)

    def test_smoke_guide_runs_verbatim(self) -> None:
        guide = GUIDES / "04-smoke-test.md"
        output = self.run_blocks(self.package, powershell_blocks(guide))
        text = guide.read_text(encoding="utf-8")
        for expected in ("TASK-0001: started at entry; next transition requires G-mach",
                         "TASK-0001: entry -> n0; G-mach exit 0; trace seq 1",
                         "TASK-0001: n0 -> n1; G-mach exit 0; trace seq 2"):
            self.assertIn(expected, text)
            self.assertIn(expected, output)
        metrics = re.search(r'^ *(\{"current": "n1".*\})$', text, re.M)
        self.assertIsNotNone(metrics, "metrics output is missing from the guide")
        self.assertIn(metrics.group(1), output)
        self.assertFalse((self.package / "runs/TASK-0001").exists(), "last block must reset the run")

    def test_deploy_guide_runs_verbatim(self) -> None:
        # The public repositories are replaced by local clones of the same layout, so the
        # test deploys this revision of the package and needs no network.
        lab = self.root / "lab"
        shutil.copytree(PACKAGE, lab / PACKAGE_PATH)
        kb = self.root / "kb"
        article = kb / "docs/kb/vpbx-api/sections/02-osnovnye-svedeniya.md"
        article.parent.mkdir(parents=True)
        article.write_text("# Основные сведения\n\nУчебная статья.\n", encoding="utf-8")
        for repository in (lab, kb):
            git("init", "-q", cwd=repository)
            git("add", "-A", cwd=repository)
            git("commit", "-q", "-m", "fixture", cwd=repository)
        blocks = []
        for block in powershell_blocks(GUIDES / "03-deploy-package.md"):
            if re.search(r"<[^>\n]+>|^(?:gigacode|notepad)\b", block, re.M):
                continue  # Needs a real address, token, GigaCode or a window.
            blocks.append(block.replace(LAB_URL, lab.as_uri()).replace(KB_URL, kb.as_uri()))
        self.assertTrue(any(lab.as_uri() in block for block in blocks))
        self.assertTrue(any(kb.as_uri() in block for block in blocks))
        # A person does these steps in one PowerShell window, so Set-Location carries over.
        output = self.run_blocks(self.home, ["\n".join(blocks)])
        runtime = self.home / "bcreq-pilot/runtime"
        for name in (".gigacode", ".gitattributes", ".gitignore", "AGENTS.md", "tools"):
            self.assertTrue((runtime / name).exists(), f"deploy lost {name}")
        self.assertTrue((runtime / "docs/kb/vpbx-api/02-osnovnye-svedeniya.md").is_file())
        self.assertGreaterEqual(output.count("G-mach: пакет принят"), 2, output)
        settings = [block for block in powershell_blocks(GUIDES / "03-deploy-package.md")
                    if "settings.example.json" in block]
        self.assertEqual(len(settings), 1)
        self.run_blocks(runtime, [settings[0].splitlines()[0]])
        self.assertTrue((runtime / ".gigacode/settings.json").is_file())
        self.assertIn("G-mach: пакет принят",
                      self.run_blocks(runtime, ["python tools/validate-package.py"]))

        # Updating (05, variant B) overwrites package files, keeps runs, KB and settings.
        update = [block for block in powershell_blocks(GUIDES / "05-commands-reference.md")
                  if "git -C source-lab pull" in block]
        self.assertEqual(len(update), 1)
        (runtime / "runs/TASK-0009").mkdir()
        (runtime / "runs/TASK-0009/state.json").write_text("{}", encoding="utf-8")
        skill = next((runtime / ".gigacode/skills").glob("*/SKILL.md"))
        skill.unlink()
        (runtime / "AGENTS.md").write_text("outdated", encoding="utf-8")
        output = self.run_blocks(self.home, [update[0]])
        self.assertIn("G-mach: пакет принят", output)
        self.assertTrue(skill.is_file(), "update must copy hidden .gigacode")
        self.assertTrue((runtime / "runs/TASK-0009/state.json").is_file())
        self.assertTrue((runtime / ".gigacode/settings.json").is_file())
        self.assertTrue((runtime / "docs/kb/vpbx-api/02-osnovnye-svedeniya.md").is_file())

    def test_documented_binding_digest(self) -> None:
        guide = (GUIDES / "05-commands-reference.md").read_text(encoding="utf-8")
        block = next(block for block in powershell_blocks(GUIDES / "05-commands-reference.md")
                     if block.startswith("python -c") and "hashlib" in block)
        confirmed = [block for block in powershell_blocks(GUIDES / "04-smoke-test.md")
                     if "A-IN-confirmed.json" in block and "Set-Content" in block]
        evidence = self.package / "runs/TASK-0002/evidence"
        evidence.mkdir(parents=True)
        self.run_blocks(self.package, [confirmed[0].replace("TASK-0001", "TASK-0002")])
        output = self.run_blocks(self.package, [block])
        expected = "sha256:af9fe155106dfbcbecd1ae1fb7a05c2b28781a2ada6b499c2e1d828172e2de0b"
        self.assertIn(expected, output)
        self.assertIn("hashlib", guide)

    def test_documented_sealing_command(self) -> None:
        seal = next(block for block in powershell_blocks(GUIDES / "05-commands-reference.md")
                    if block.startswith("@'")
                    and "| python - runs/TASK-0002/evidence/working.json" in block)
        evidence = self.package / "runs/TASK-0002/evidence"
        evidence.mkdir(parents=True)
        validate = [sys.executable, "tools/bcreq_pipeline.py", "validate-working",
                    "runs/TASK-0002/evidence/working.json"]
        # Windows PowerShell 5.1 and Notepad may save working.json with a UTF-8 BOM.
        for encoding in ("utf-8", "utf-8-sig"):
            with self.subTest(encoding=encoding):
                (evidence / "working.json").write_text(FIXTURE.read_text(encoding="utf-8"),
                                                       encoding=encoding)
                before = subprocess.run(validate, cwd=self.package, text=True,
                                        capture_output=True)
                self.assertNotEqual(before.returncode, 0)
                output = self.run_blocks(self.package, [seal])
                self.assertIn("sealed: runs/TASK-0002/evidence/working.json", output)
                after = subprocess.run(validate, cwd=self.package, text=True,
                                       capture_output=True, env=environment())
                self.assertEqual(after.returncode, 0, after.stdout + after.stderr)
                self.assertIn("G-mach: BCREQ accepted", after.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
