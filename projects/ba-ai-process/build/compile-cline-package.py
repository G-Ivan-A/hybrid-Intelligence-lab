#!/usr/bin/env python3
"""Compile the Cline pilot from common model inputs and one adapter."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


PROJECT = Path(__file__).resolve().parents[1]
COMMON = PROJECT / "build/common"
ADAPTER = PROJECT / "build/adapters/cline-vscode"
OUTPUT = PROJECT / "dist/execution-package-cline-vscode"
MUTABLE = {"runs", "submissions", "docs/kb", "meta-model"}


def source_files(source: Path):
    for path in sorted(source.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Source symlink is forbidden: {path}")
        if path.is_file() and "__pycache__" not in path.parts:
            yield path


def static_files(root: Path):
    return {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
        and not any(path.relative_to(root).as_posix().startswith(prefix + "/")
                    and path.name != ".gitkeep" for prefix in MUTABLE)
    }


def compile_into(root: Path, revision: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("source revision must be a full Git commit SHA")
    for source in (COMMON, ADAPTER):
        for path in source_files(source):
            relative = path.relative_to(source)
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    for path in (root / "contracts").glob("*.schema.json"):
        path.write_text(path.read_text(encoding="utf-8").replace(
            "build/common/contracts/", "dist/execution-package-cline-vscode/contracts/"), encoding="utf-8")
    for directory in MUTABLE:
        placeholder = root / directory / ".gitkeep"
        placeholder.parent.mkdir(parents=True, exist_ok=True)
        placeholder.touch()
    hashes = {
        rel: hashlib.sha256(path.read_bytes()).hexdigest()
        for rel, path in static_files(root).items()
        if rel != "package-manifest.yaml" and not any(rel.startswith(prefix + "/") for prefix in MUTABLE)
    }
    manifest = {
        "manifest": "execution-package-cline-vscode",
        "package_version": "0.1.0",
        "compiled_at": "2026-09-26",
        "source": {
            "repository": "https://github.com/G-Ivan-A/hybrid-Intelligence-lab",
            "revision": revision,
        },
        "adapter": {"name": "cline-vscode", "version": "0.1.0"},
        "inputs": {"allowlist": [
            "projects/ba-ai-process/build/common/",
            "projects/ba-ai-process/build/adapters/cline-vscode/",
        ]},
        "outputs": {"hash_algorithm": "sha256", "hashes": dict(sorted(hashes.items()))},
    }
    (root / "package-manifest.yaml").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    parser.add_argument("--source-revision")
    args = parser.parse_args()
    if args.write:
        revision = args.source_revision or subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    else:
        revision = json.loads((OUTPUT / "package-manifest.yaml").read_text(encoding="utf-8"))["source"]["revision"]
    with tempfile.TemporaryDirectory() as temporary:
        staged = Path(temporary) / "package"
        staged.mkdir()
        compile_into(staged, revision)
        expected = static_files(staged)
        if args.check:
            actual = static_files(OUTPUT)
            if set(expected) != set(actual):
                raise ValueError(f"Distribution file list differs: missing={sorted(set(expected)-set(actual))}, extra={sorted(set(actual)-set(expected))}")
            for rel, path in expected.items():
                if path.read_bytes() != actual[rel].read_bytes():
                    raise ValueError(f"Distribution differs from Source: {rel}")
                if rel.startswith(".clinerules/hooks/") and not (actual[rel].stat().st_mode & 0o111):
                    raise ValueError(f"Cline hook is not executable: {rel}")
            print("Cline package matches Source")
        else:
            for rel, path in expected.items():
                target = OUTPUT / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)
            print(f"Compiled Cline package from {revision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
