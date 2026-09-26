#!/usr/bin/env python3
"""Independent BCREQ gate and trace writer for the Cline package."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
IMMUTABLE_EXCEPTIONS = {"package-manifest.yaml"}
MUTABLE_ROOTS = {"runs", "submissions", "docs/kb", "meta-model", ".git", ".vscode"}
STEPS = ("validate-working", "compile", "validate-release")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_files() -> dict[str, Path]:
    result = {}
    for base, directories, filenames in os.walk(ROOT, followlinks=False):
        parent = Path(base)
        for name in directories:
            if (parent / name).is_symlink():
                raise ValueError(f"symlink in package: {(parent / name).relative_to(ROOT)}")
        directories[:] = [name for name in directories if name != "__pycache__"
                          and (parent / name).relative_to(ROOT).as_posix() not in MUTABLE_ROOTS]
        for name in filenames:
            path = parent / name
            rel = path.relative_to(ROOT).as_posix()
            if path.is_symlink():
                raise ValueError(f"symlink in package: {rel}")
            if rel not in IMMUTABLE_EXCEPTIONS:
                result[rel] = path
    return result


def check_package() -> str:
    manifest_path = ROOT / "package-manifest.yaml"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("manifest") != "execution-package-cline-vscode":
        raise ValueError("wrong package identity")
    if manifest.get("adapter", {}).get("name") != "cline-vscode":
        raise ValueError("wrong adapter")
    if not re.fullmatch(r"[0-9a-f]{40}", manifest.get("source", {}).get("revision", "")):
        raise ValueError("source revision must be a full commit SHA")
    if not manifest.get("inputs", {}).get("allowlist"):
        raise ValueError("missing source allowlist")
    if manifest.get("outputs", {}).get("hash_algorithm") != "sha256":
        raise ValueError("unsupported hash algorithm")
    route = json.loads((ROOT / "routes/pilot.json").read_text(encoding="utf-8"))
    if route.get("route_id") != "RG-BCREQ-v1/synthetic-working-release" or tuple(route.get("machine_steps", [])) != STEPS or route.get("human_gate") != "G-human":
        raise ValueError("pilot route differs from the runner")
    expected = manifest["outputs"].get("hashes", {})
    files = package_files()
    if set(files) != set(expected):
        raise ValueError(f"immutable file list differs: missing={sorted(set(expected)-set(files))}, extra={sorted(set(files)-set(expected))}")
    for rel, path in files.items():
        if sha256(path) != expected[rel]:
            raise ValueError(f"package hash mismatch: {rel}")
    for rel in ("runs/.gitkeep", "submissions/.gitkeep", "docs/kb/.gitkeep", "meta-model/.gitkeep"):
        if not (ROOT / rel).is_file():
            raise ValueError(f"missing runtime placeholder: {rel}")
    return sha256(manifest_path)


def trace_line(state: str, task_id: str, gate: str, package_hash: str, *, command: list[str] | None = None,
               exit_code: int | None = None, input_hash: str | None = None, output_hash: str | None = None,
               actor: str = "runner", detail: str = "") -> dict:
    return {
        "at": datetime.now(timezone.utc).isoformat(),
        "task_id": task_id,
        "route": "RG-BCREQ-v1/synthetic-working-release",
        "node": gate,
        "state": state,
        "recorded_by": "tools/run_task.py",
        "actor": actor,
        "package_sha256": package_hash,
        "gate_id": gate,
        "command": command,
        "exit_code": exit_code,
        "input_sha256": input_hash,
        "output_sha256": output_hash,
        "detail": detail,
    }


def run(task_id: str, candidate: Path, output: Path, package_hash: str) -> bool:
    if not re.fullmatch(r"TASK-[0-9]{4,}", task_id):
        raise ValueError("task ID must match TASK-0001")
    if not candidate.is_file() or candidate.is_symlink():
        raise ValueError("candidate must be a regular JSON file")
    if output.exists():
        raise ValueError(f"run already exists: {output}")
    output.mkdir(parents=True)
    trace_path = output / "trace.jsonl"
    pipeline = ROOT / "tools/bcreq_pipeline.py"
    commands = (
        [sys.executable, str(pipeline), "validate-working", str(candidate)],
        [sys.executable, str(pipeline), "compile", str(candidate), "--output", str(output)],
        [sys.executable, str(pipeline), "validate-release", str(candidate), "--release", str(output / "release.json"), "--manifest", str(output / "release-manifest.json")],
    )
    input_hash = sha256(candidate)
    ok = True
    with trace_path.open("w", encoding="utf-8") as trace:
        for gate, command in zip(STEPS, commands):
            if ok:
                result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
                output_hash = sha256(output / "release.json") if (output / "release.json").exists() else None
                line = trace_line("script_invoked", task_id, gate, package_hash, command=command,
                                  exit_code=result.returncode, input_hash=input_hash, output_hash=output_hash)
                ok = result.returncode == 0
                if not ok:
                    print(result.stderr or result.stdout or f"{gate} failed", file=sys.stderr)
            else:
                line = trace_line("step_skipped", task_id, gate, package_hash, input_hash=input_hash,
                                  detail="previous machine gate failed")
            trace.write(json.dumps(line, ensure_ascii=False) + "\n")
        trace.write(json.dumps(trace_line("contract_mode", task_id, "G-human", package_hash,
                                        input_hash=input_hash, actor="human", detail="semantic and publication review required; not credited as a machine gate"), ensure_ascii=False) + "\n")
    return ok


def verify_ci(package_hash: str) -> bool:
    candidates = [ROOT / "golden/TASK-0001.json"]
    submissions = ROOT / "submissions"
    for path in submissions.iterdir():
        if path.name == ".gitkeep":
            continue
        if not path.is_file() or path.is_symlink() or not re.fullmatch(r"TASK-[0-9]{4,}\.json", path.name):
            raise ValueError(f"unexpected submission: {path.name}")
        candidates.append(path)
    passed = True
    with tempfile.TemporaryDirectory() as temp:
        for index, candidate in enumerate(candidates):
            task_id = candidate.stem
            outcome = run(task_id, candidate, Path(temp) / f"run-{index}", package_hash)
            print(f"{candidate.relative_to(ROOT)}: {'PASS' if outcome else 'FAIL'}")
            passed &= outcome
    return passed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check-package", "run", "verify-ci"))
    parser.add_argument("task_id", nargs="?")
    parser.add_argument("candidate", nargs="?", type=Path)
    args = parser.parse_args()
    try:
        package_hash = check_package()
        if args.action == "check-package":
            print("package: PASS")
            return 0
        if args.action == "verify-ci":
            return 0 if verify_ci(package_hash) else 1
        if not args.task_id or not args.candidate:
            parser.error("run requires TASK-ID and candidate JSON")
        outcome = run(args.task_id, args.candidate.resolve(), ROOT / "runs" / args.task_id, package_hash)
        print(f"{args.task_id}: {'PASS' if outcome else 'FAIL'}")
        return 0 if outcome else 1
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
