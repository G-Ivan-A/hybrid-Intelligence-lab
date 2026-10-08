#!/usr/bin/env python3
"""Drive a real OpenCode binary against a compiled package and a scripted mock model.

Usage: python issue_652_opencode_e2e.py PACKAGE_DIR [--opencode PATH] [--keep]

Checks, on a disposable Git runtime copy of the package:
1. the guard plugin loads and blocks writes outside submissions/TASK-ID.json;
2. the declarative rules hide or deny tools (bash, edits of package files, Plan agent writes);
3. /bcreq-check and /bcreq-gate run the runner and give its output to the model.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


HERE = Path(__file__).resolve().parent


class Mock:
    def __init__(self, work: Path, name: str, script: list):
        self.log = work / f"{name}.log.jsonl"
        script_path = work / f"{name}.script.json"
        script_path.write_text(json.dumps(script, ensure_ascii=False), encoding="utf-8")
        port_file = work / f"{name}.port"
        self.process = subprocess.Popen([sys.executable, str(HERE / "issue_652_mock_openai.py"), str(script_path),
                                         str(self.log), "--port-file", str(port_file)])
        for _ in range(100):
            if port_file.exists() and port_file.read_text():
                break
            time.sleep(0.1)
        self.port = int(port_file.read_text())

    def requests(self) -> list:
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def stop(self):
        self.process.terminate()
        self.process.wait(10)


def environment(work: Path, port: int) -> dict:
    home = work / "home"
    for name in ("config", "data", "cache", "state"):
        (home / name).mkdir(parents=True, exist_ok=True)
    config = work / f"provider-{port}.json"
    config.write_text(json.dumps({
        "$schema": "https://opencode.ai/config.json",
        "model": "mock/mock-model",
        "provider": {"mock": {
            "npm": "@ai-sdk/openai-compatible", "name": "Mock",
            "options": {"baseURL": f"http://127.0.0.1:{port}/v1", "apiKey": "mock"},
            "models": {"mock-model": {"name": "Mock", "tool_call": True,
                                      "limit": {"context": 100000, "output": 4000}}},
        }},
    }), encoding="utf-8")
    env = {key: value for key, value in os.environ.items() if not key.startswith("OPENCODE_")}
    env.update({
        "HOME": str(home), "USERPROFILE": str(home),
        "XDG_CONFIG_HOME": str(home / "config"), "XDG_DATA_HOME": str(home / "data"),
        "XDG_CACHE_HOME": str(home / "cache"), "XDG_STATE_HOME": str(home / "state"),
        "OPENCODE_CONFIG": str(config), "OPENCODE_DISABLE_MODELS_FETCH": "1",
        "OPENCODE_DISABLE_AUTOUPDATE": "1", "OPENCODE_DISABLE_LSP_DOWNLOAD": "1",
    })
    return env


def opencode(binary: str, package: Path, env: dict, arguments: list, log: Path) -> int:
    command = [binary, "run", "--format", "json", *arguments]
    # `opencode run` takes its project directory from PWD before the process cwd.
    with log.open("w", encoding="utf-8") as output:
        result = subprocess.run(command, cwd=package, env={**env, "PWD": str(package)}, stdout=output, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL, timeout=300)
    return result.returncode


def tool_results(requests: list) -> dict:
    """Map tool call ids to the text OpenCode returned to the model."""
    results = {}
    for request in requests:
        for message in request["messages"]:
            if message.get("role") == "tool":
                content = message.get("content")
                if isinstance(content, list):
                    content = " ".join(part.get("text", "") for part in content if isinstance(part, dict))
                results[message.get("tool_call_id")] = content or ""
    return results


def user_text(requests: list) -> str:
    texts = []
    for request in requests:
        for message in request["messages"]:
            if message.get("role") == "user":
                content = message.get("content")
                if isinstance(content, list):
                    content = " ".join(part.get("text", "") for part in content if isinstance(part, dict))
                texts.append(content or "")
    return "\n".join(texts)


def probe(binary: str, package: Path, work: Path):
    """Trace which shell runs the !`...` blocks of a command and what argv it passes."""
    command = package / ".opencode/commands/probe.md"
    command.write_text(
        "---\ndescription: probe\n---\n"
        "A !`echo shell=[$BASH_VERSION] [%COMSPEC%] [$PSVersionTable]`\n"
        "B !`python -c \"import sys, os; print('argv', sys.argv[1:], os.getcwd())\" '$1'`\n"
        "C !`python -c \"import sys; print('argv-dq', sys.argv[1:])\" \"$1\"`\n"
        "D !`python tools/opencode_command.py gate '$1'`\n"
        "E !`python -c \"print('exit-1'); raise SystemExit(1)\"`\n", encoding="utf-8")
    for label, arguments in (("plain", ["TASK-0002"]), ("semicolon", ["TASK-0002;", "echo", "probe"]),
                             ("redirect", ["TASK-0002", ">", "probe1.txt"]),
                             ("both", ["TASK-0002;", "echo", "probe", ">", "probe2.txt"]),
                             ("pwned", ["TASK-0002;", "echo", "pwned", ">", "probe3.txt"])):
        mock = Mock(work, f"probe-{label}", [{"text": "ok"}])
        try:
            opencode(binary, package, environment(work, mock.port), ["--command", "probe", *arguments],
                     work / f"probe-{label}.out")
        finally:
            mock.stop()
        text = user_text(mock.requests())
        print(f"  probe {label}: {ascii(text[text.find('A '):][:1200])}")
        created = sorted(str(path.relative_to(work)) for path in work.rglob("probe[0-9]*"))
        print(f"  probe {label} files: {created}")
    command.unlink()
    print(f"  SHELL={os.environ.get('SHELL')!r} COMSPEC={os.environ.get('COMSPEC')!r}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--opencode", default=shutil.which("opencode") or "opencode")
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args()
    work = Path(tempfile.mkdtemp(prefix="opencode-e2e-"))
    package = work / "runtime"
    shutil.copytree(args.package, package)
    for command in (["init", "-q"], ["add", "-A"],
                    ["-c", "user.name=e2e", "-c", "user.email=e2e@example.invalid", "commit", "-qm", "runtime"]):
        subprocess.run(["git", *command], cwd=package, check=True)
    golden = (package / "golden/TASK-0001.json").read_text(encoding="utf-8")
    outside = str(work / "outside.json")
    failures = []

    def expect(condition: bool, message: str):
        print(("PASS " if condition else "FAIL ") + message)
        if not condition:
            failures.append(message)

    build_script = [
        {"tool": "write", "args": {"filePath": "submissions/TASK-0002.json", "content": golden}},
        {"tool": "write", "args": {"filePath": "submissions/TASK-abc.json", "content": "{}"}},
        {"tool": "edit", "args": {"filePath": "opencode.json", "oldString": "\"deny\"", "newString": "\"allow\""}},
        {"tool": "write", "args": {"filePath": outside, "content": "{}"}},
        {"tool": "bash", "args": {"command": "echo pwned > pwned.txt", "description": "probe"}},
        {"tool": "read", "args": {"filePath": "routes/pilot.json"}},
        {"text": "Черновик записан."},
    ]
    mock = Mock(work, "build", build_script)
    try:
        env = environment(work, mock.port)
        code = opencode(args.opencode, package, env, ["--auto", "Пиши черновик"], work / "build.out")
    finally:
        mock.stop()
    requests = mock.requests()
    results = tool_results(requests)
    print(f"build run exit code {code}; {len(requests)} model requests")
    for call, text in sorted(results.items()):
        print(f"  {call}: {text[:160]!r}")
    tools = next((request["tools"] for request in requests if request["tools"]), [])
    print(f"  tools offered to the model: {sorted(tools)}")
    expect((package / "submissions/TASK-0002.json").is_file(), "write to submissions/TASK-0002.json is allowed")
    expect(not (package / "submissions/TASK-abc.json").exists(), "write to submissions/TASK-abc.json is blocked")
    expect("BCREQ guard" in results.get("call_1", ""), "the guard plugin reports the blocked write")
    expect('"*": "deny"' in (package / "opencode.json").read_text(encoding="utf-8"), "opencode.json is not edited")
    expect(not Path(outside).exists(), "write outside the package is blocked")
    expect(not (package / "pwned.txt").exists() and "bash" not in tools, "bash is hidden and does not run")
    expect("pilot" in results.get("call_5", "").lower(), "read of a package file is allowed")

    plan_script = [
        {"tool": "write", "args": {"filePath": "submissions/TASK-0004.json", "content": golden}},
        {"text": "ok"},
    ]
    mock = Mock(work, "plan", plan_script)
    try:
        env = environment(work, mock.port)
        opencode(args.opencode, package, env, ["--auto", "--agent", "plan", "Пиши черновик"], work / "plan.out")
    finally:
        mock.stop()
    plan_tools = next((request["tools"] for request in mock.requests() if request["tools"]), [])
    print(f"  plan agent tools: {sorted(plan_tools)}")
    expect(not (package / "submissions/TASK-0004.json").exists(), "the Plan agent cannot write a draft")

    for name, arguments, needle in (
        ("check", ["--command", "bcreq-check"], "package: PASS"),
        ("gate", ["--command", "bcreq-gate", "TASK-0002"], "TASK-0002: PASS"),
        ("gate-bad", ["--command", "bcreq-gate", "TASK-0002;", "echo", "pwned", ">", "pwned2.txt"], "task ID must match"),
        ("gate-again", ["--command", "bcreq-gate", "TASK-0002"], "ERROR: run already exists"),
    ):
        mock = Mock(work, name, [{"text": "ok"}])
        try:
            env = environment(work, mock.port)
            opencode(args.opencode, package, env, arguments, work / f"{name}.out")
        finally:
            mock.stop()
        text = user_text(mock.requests())
        expect(needle in text, f"/{arguments[1]} gives the model the runner output ({needle})")
        if needle not in text:
            output = (work / f"{name}.out").read_text(encoding="utf-8", errors="replace")
            print(f"  model requests: {len(mock.requests())}; runner block: {ascii(text[text.find(chr(96) * 3):][:1500])}")
            print(f"  OpenCode output: {ascii(output[-3000:])}")
            probe(args.opencode, package, work)
    expect((package / "runs/TASK-0002/release.json").is_file(), "/bcreq-gate writes runs/TASK-0002/release.json")
    # cmd.exe would keep the single quotes and redirect into a file named pwned2.txt'
    expect(not any(package.glob("pwned2*")), "/bcreq-gate does not run text after the TASK ID")
    check = subprocess.run([sys.executable, "tools/run_task.py", "check-package"], cwd=package,
                           capture_output=True, text=True)
    expect(check.returncode == 0, f"package integrity after OpenCode start-up: {check.stdout.strip() or check.stderr.strip()}")
    status = subprocess.run(["git", "status", "--porcelain", "--ignored"], cwd=package, capture_output=True, text=True).stdout
    print("git status after the runs:\n" + status)
    if args.keep:
        print(f"work directory kept: {work}")
    else:
        shutil.rmtree(work, ignore_errors=True)
    print("E2E: " + ("PASS" if not failures else f"FAIL ({len(failures)})"))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
