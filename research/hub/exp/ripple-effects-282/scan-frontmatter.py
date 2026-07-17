#!/usr/bin/env python3
"""Scan Markdown frontmatter for issue #284 decision support."""

from __future__ import annotations

import json
import subprocess
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = Path(__file__).resolve().parent
SCAN_DATE = date(2026, 6, 28).isoformat()
EXCLUDED_PATHS = {"research/hub/2026-06-28-ripple-effects-282-research.md"}
EXCLUDED_PREFIXES = ("research/hub/exp/ripple-effects-282/",)


def git_files() -> list[Path]:
    output = subprocess.check_output(["git", "ls-files", "*.md"], cwd=ROOT, text=True)
    paths = []
    for line in output.splitlines():
        relative = line.strip()
        if not relative:
            continue
        if relative in EXCLUDED_PATHS or relative.startswith(EXCLUDED_PREFIXES):
            continue
        paths.append(ROOT / relative)
    return paths


def path_class(path: str) -> str:
    if path.startswith("research/") or path.startswith("docs/analysis/"):
        return "knowledge"
    if path.startswith(
        (
            "governance/rfc/",
            "docs/adr/",
            "docs/rfc/",
            "standards/",
            "governance/",
            "templates/",
            "practices/",
        )
    ):
        return "governance"
    return "other"


def parse_frontmatter(path: Path) -> dict[str, str] | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    fields: dict[str, str] = {}
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            return fields
        if (
            not stripped
            or stripped.startswith("#")
            or ":" not in line
            or line.startswith((" ", "\t", "-"))
        ):
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key:
            fields[key] = value.strip().strip("'\"")
    return None


def sample_append(samples: dict[str, list[str]], key: str, value: str, limit: int = 8) -> None:
    if len(samples[key]) < limit:
        samples[key].append(value)


def build_report(data: dict) -> str:
    status_rows = "\n".join(
        f"| `{status}` | {count} |"
        for status, count in data["status_counts"].items()
    )
    field_rows = "\n".join(
        f"| `{field}` | {count} |"
        for field, count in data["field_counts"].items()
    )
    path_rows = "\n".join(
        f"| `{klass}` | {count} |"
        for klass, count in data["path_class_counts"].items()
    )
    extra_rows = "\n".join(
        f"| `{field}` | {count} |"
        for field, count in data["extra_field_counts"].items()
    )
    ai_samples = "\n".join(f"- `{path}`" for path in data["samples"]["ai_generated_paths"])
    deprecated_samples = "\n".join(
        f"- `{path}`" for path in data["samples"]["governance_canonical_paths"]
    )

    return f"""---
status: draft
version: 0.1
updated: {SCAN_DATE}
temperature: 0.1
---

# Frontmatter scan for issue 284

## Summary

| Metric | Count |
| --- | ---: |
| Tracked Markdown files | {data["markdown_files"]} |
| Files with frontmatter | {data["files_with_frontmatter"]} |
| Files without frontmatter | {data["files_without_frontmatter"]} |
| Files with `ai-generated` | {data["files_with_ai_generated"]} |
| Files with fields outside the four base fields | {data["files_with_extra_fields"]} |

The scan excludes this issue #284 research artifact and its experiment directory
so the counts describe the repository state that issue #282 would migrate.

## Status Values

| Status | Count |
| --- | ---: |
{status_rows}

## Path Classes

| Path class | Count |
| --- | ---: |
{path_rows}

## Frontmatter Fields

| Field | Count |
| --- | ---: |
{field_rows}

## Extra Fields

Fields outside `status`, `version`, `updated` and `temperature`:

| Field | Count |
| --- | ---: |
{extra_rows}

## Sample `ai-generated` Paths

{ai_samples}

## Sample Governance Files Currently Using `canonical`

{deprecated_samples}
"""


def main() -> None:
    base_fields = {"status", "version", "updated", "temperature"}
    markdown_files = git_files()
    status_counts: Counter[str] = Counter()
    field_counts: Counter[str] = Counter()
    extra_field_counts: Counter[str] = Counter()
    path_class_counts: Counter[str] = Counter()
    files_with_frontmatter = 0
    files_without_frontmatter = 0
    files_with_ai_generated = 0
    files_with_extra_fields = 0
    samples: dict[str, list[str]] = defaultdict(list)

    for file_path in markdown_files:
        relative = file_path.relative_to(ROOT).as_posix()
        fields = parse_frontmatter(file_path)
        if fields is None:
            files_without_frontmatter += 1
            sample_append(samples, "without_frontmatter_paths", relative)
            continue

        files_with_frontmatter += 1
        klass = path_class(relative)
        path_class_counts[klass] += 1

        for key in fields:
            field_counts[key] += 1
            if key not in base_fields:
                extra_field_counts[key] += 1

        if "status" in fields:
            status_counts[fields["status"]] += 1

        if "ai-generated" in fields:
            files_with_ai_generated += 1
            sample_append(samples, "ai_generated_paths", relative)

        if any(key not in base_fields for key in fields):
            files_with_extra_fields += 1
            sample_append(samples, "extra_field_paths", relative)

        if klass == "governance" and fields.get("status") == "canonical":
            sample_append(samples, "governance_canonical_paths", relative)

    data = {
        "scan_date": SCAN_DATE,
        "markdown_files": len(markdown_files),
        "files_with_frontmatter": files_with_frontmatter,
        "files_without_frontmatter": files_without_frontmatter,
        "files_with_ai_generated": files_with_ai_generated,
        "files_with_extra_fields": files_with_extra_fields,
        "excluded_paths": sorted(EXCLUDED_PATHS),
        "excluded_prefixes": list(EXCLUDED_PREFIXES),
        "status_counts": dict(status_counts.most_common()),
        "field_counts": dict(field_counts.most_common()),
        "extra_field_counts": dict(extra_field_counts.most_common()),
        "path_class_counts": dict(path_class_counts.most_common()),
        "samples": dict(samples),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "frontmatter-scan.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT_DIR / "2026-06-28-frontmatter-scan.md").write_text(
        build_report(data),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
