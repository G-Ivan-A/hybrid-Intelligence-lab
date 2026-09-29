#!/usr/bin/env python3
"""Experiment for issue #638: run the sh blocks of docs/guides/04-smoke-test.md verbatim.

Copies the package to a temporary folder, extracts every ```sh block from the
training-run guide in document order and runs it with `sh -c` in the package
folder. Blocks that pass --checkpoint get the APPROVE line through a pseudo
terminal, exactly as a person would type it. The block that deletes the task
runs last, followed by a new start, to show that the training run can repeat.
Requires PyYAML and jsonschema (pip install -r requirements.txt).
"""
import hashlib, os, pathlib, re, shutil, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent / "dist/execution-package-gigacode-cli"
GUIDE = SRC / "docs/guides/04-smoke-test.md"
work = pathlib.Path(tempfile.mkdtemp(prefix="gc-638-smoke-")) / "runtime"
shutil.copytree(SRC, work)
env = dict(os.environ, PATH=f"{pathlib.Path(sys.executable).parent}:{os.environ['PATH']}")

blocks = []
for match in re.finditer(r"^( *)```sh\n(.*?)^\1```", GUIDE.read_text(encoding="utf-8"), re.M | re.S):
    indent = len(match.group(1))
    blocks.append("".join(line[indent:] for line in match.group(2).splitlines(True)))


def run(block: str) -> int:
    print(f"$ {block.splitlines()[0]}" + (" …" if block.count("\n") > 1 else ""))
    stdin = subprocess.DEVNULL
    master = slave = None
    found = re.search(r"advance (TASK-\d{4}) .*--checkpoint (\S+)", block)
    if found:
        state = (work / "runs" / found.group(1) / "state.json").read_text()
        source = re.search(r'"current": "([^"]+)"', state).group(1)
        digest = hashlib.sha256((work / found.group(2)).read_bytes()).hexdigest()
        master, slave = os.openpty()
        os.write(master, f"APPROVE {found.group(1)}:{source} sha256:{digest}\n".encode())
        stdin = slave
    result = subprocess.run(["sh", "-c", block], cwd=work, env=env, text=True,
                            capture_output=True, stdin=stdin)
    if slave is not None:
        os.close(slave); os.close(master)
    output = (result.stdout + result.stderr).strip().replace(str(work.parent), "<tmp>")
    print(output + ("\n" if output else "") + f"exit={result.returncode}\n")
    return result.returncode


print(f"== {len(blocks)} sh blocks in {GUIDE.relative_to(HERE.parent)}\n")
codes = [run(block) for block in blocks]
print("== evidence:", sorted(p.name for p in (work / "runs/TASK-0001/evidence").iterdir())
      if (work / "runs/TASK-0001/evidence").is_dir() else "absent (removed by the last block)")
codes.append(run(blocks[0]))
print("== all blocks exit 0:", all(code == 0 for code in codes))
shutil.rmtree(work.parent)
