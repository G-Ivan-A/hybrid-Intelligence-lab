#!/usr/bin/env python3
"""Experiment for issue #638: run the powershell blocks of docs/guides/04-smoke-test.md verbatim.

Copies the package to a temporary folder under a user profile with a space and
Cyrillic letters, extracts every ```powershell block from the training-run guide
in document order and runs it in PowerShell in the package folder. Blocks that
pass --checkpoint get the APPROVE line through a terminal, exactly as a person
would type it. The block that deletes the task runs last, followed by a new
start, to show that the training run can repeat. Ported to Windows 10/11 for
issue #647: set GUIDE_SHELL to powershell or pwsh; Windows also needs pywinpty.
Requires PyYAML and jsonschema (pip install -r requirements.txt).
"""
import pathlib, shutil, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tests/execution-package/tests"))
from test_guides import GuideShell, environment, guide_shell, powershell_blocks  # noqa: E402

SRC = HERE.parent / "dist/execution-package-gigacode-cli"
GUIDE = SRC / "docs/guides/04-smoke-test.md"
shell = guide_shell()
if not shell:
    sys.exit("no PowerShell: set GUIDE_SHELL or install powershell/pwsh")
root = pathlib.Path(tempfile.mkdtemp(prefix="gc-638-smoke-"))
home = root / "Иван Петров"
work = home / "bcreq-pilot" / "runtime"
shutil.copytree(SRC, work)
console = GuideShell(shell, root, environment(USERPROFILE=str(home)))
blocks = powershell_blocks(GUIDE)


def run(block: str) -> int:
    print(f"PS> {block.splitlines()[0]}" + (" …" if block.count("\n") > 1 else ""))
    code, output = console.run(work, block)
    output = output.replace("\r\n", "\n").strip().replace(str(root), "<tmp>")
    print(output + ("\n" if output else "") + f"exit={code}\n")
    return code


print(f"== {len(blocks)} powershell blocks in {GUIDE.relative_to(HERE.parent).as_posix()}\n")
codes = [run(block) for block in blocks]
print("== evidence:", sorted(p.name for p in (work / "runs/TASK-0001/evidence").iterdir())
      if (work / "runs/TASK-0001/evidence").is_dir() else "absent (removed by the last block)")
codes.append(run(blocks[0]))
print("== all blocks exit 0:", all(code == 0 for code in codes))
shutil.rmtree(root)
