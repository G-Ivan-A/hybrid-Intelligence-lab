#!/usr/bin/env python3
"""Generate templates/manifest.json from the templates/ tree.

The manifest is the Smart Sync template registry consumed by
``tools/sync-from-hub.sh``. It is **auto-generated** and must never be edited
by hand (see issue #207). Sync-policy metadata that cannot be inferred from the
file tree (target_type, stack, min_phase, criticality, tags, description) is
read from the hand-maintained ``templates/sync-metadata.json`` registry; the
manifest itself is always produced by this script.

Usage:
    tools/generate-manifest.py            # print manifest to stdout
    tools/generate-manifest.py --write    # (re)write templates/manifest.json
    tools/generate-manifest.py --check     # exit 1 if manifest is out of date

``--check`` compares only the structural content (manifest_version + templates)
and ignores ``last_updated`` so a date-only difference never reports drift.
"""

from __future__ import annotations

import argparse
import datetime
import fnmatch
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(ROOT, "templates")
META_FILE = os.path.join(TEMPLATES_DIR, "sync-metadata.json")
OUT_FILE = os.path.join(TEMPLATES_DIR, "manifest.json")

ENTRY_FIELDS = (
    "id",
    "path",
    "version",
    "target_type",
    "stack",
    "min_phase",
    "criticality",
    "tags",
    "description",
)


def load_metadata() -> dict:
    with open(META_FILE, encoding="utf-8") as handle:
        return json.load(handle)


def slugify(name: str) -> str:
    base = os.path.splitext(name)[0]
    slug = re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")
    return slug or base.lower()


def normalize_version(value: str) -> str:
    value = str(value).strip().strip('"').strip("'")
    parts = value.split(".")
    while len(parts) < 3:
        parts.append("0")
    return ".".join(parts[:3])


def frontmatter_version(path: str) -> str | None:
    try:
        with open(path, encoding="utf-8") as handle:
            first = handle.readline()
            if first.strip() != "---":
                return None
            for line in handle:
                if line.strip() == "---":
                    return None
                match = re.match(r"\s*version:\s*(.+)\s*$", line)
                if match:
                    return normalize_version(match.group(1))
    except (OSError, UnicodeDecodeError):
        return None
    return None


def heuristic_target_type(rel_path: str) -> list[str]:
    if "/htom/" in rel_path:
        return ["HTOM"]
    if "/spoke/" in rel_path:
        return ["Spoke"]
    return ["HTOM", "Spoke"]


def is_excluded(rel_path: str, patterns: list[str]) -> bool:
    base = os.path.basename(rel_path)
    for pattern in patterns:
        if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(base, pattern):
            return True
    return False


def collect_files(exclude: list[str]) -> list[str]:
    found = []
    for dirpath, _dirnames, filenames in os.walk(TEMPLATES_DIR):
        for name in filenames:
            abs_path = os.path.join(dirpath, name)
            rel_path = os.path.relpath(abs_path, ROOT).replace(os.sep, "/")
            if is_excluded(rel_path, exclude):
                continue
            found.append(rel_path)
    return sorted(found)


def build_entry(rel_path: str, meta: dict) -> dict:
    defaults = meta.get("defaults", {})
    override = meta.get("overrides", {}).get(rel_path, {})

    version = (
        override.get("version")
        or frontmatter_version(os.path.join(ROOT, rel_path))
        or defaults.get("version", "1.0.0")
    )

    entry = {
        "id": override.get("id", slugify(os.path.basename(rel_path))),
        "path": rel_path,
        "version": normalize_version(version),
        "target_type": override.get("target_type", heuristic_target_type(rel_path)),
        "stack": override.get("stack", defaults.get("stack", ["all"])),
        "min_phase": override.get("min_phase", defaults.get("min_phase", 0)),
        "criticality": override.get(
            "criticality", defaults.get("criticality", "RECOMMENDED")
        ),
        "tags": override.get("tags", defaults.get("tags", [])),
        "description": override.get("description", ""),
    }
    return {field: entry[field] for field in ENTRY_FIELDS}


def build_manifest(meta: dict, today: str) -> dict:
    exclude = meta.get("exclude", [])
    templates = [build_entry(rel, meta) for rel in collect_files(exclude)]
    return {
        "manifest_version": meta.get("manifest_version", "1.0"),
        "last_updated": today,
        "templates": templates,
    }


def structural(manifest: dict) -> dict:
    return {
        "manifest_version": manifest.get("manifest_version"),
        "templates": manifest.get("templates"),
    }


def dump(manifest: dict) -> str:
    return json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write templates/manifest.json")
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if manifest.json differs structurally from the templates tree",
    )
    parser.add_argument(
        "--date",
        default=datetime.date.today().isoformat(),
        help="value for last_updated (default: today)",
    )
    args = parser.parse_args()

    meta = load_metadata()
    manifest = build_manifest(meta, args.date)

    if args.check:
        if not os.path.exists(OUT_FILE):
            print("manifest.json is missing; run with --write", file=sys.stderr)
            return 1
        with open(OUT_FILE, encoding="utf-8") as handle:
            current = json.load(handle)
        if structural(current) != structural(manifest):
            print("manifest.json is out of date; run tools/generate-manifest.py --write", file=sys.stderr)
            return 1
        print("manifest.json is up to date.")
        return 0

    if args.write:
        # Preserve the existing last_updated when only the date would change,
        # so re-running --write does not create date-only churn.
        if os.path.exists(OUT_FILE):
            with open(OUT_FILE, encoding="utf-8") as handle:
                current = json.load(handle)
            if structural(current) == structural(manifest):
                manifest["last_updated"] = current.get("last_updated", args.date)
        with open(OUT_FILE, "w", encoding="utf-8") as handle:
            handle.write(dump(manifest))
        print(f"Wrote {os.path.relpath(OUT_FILE, ROOT)} ({len(manifest['templates'])} templates).")
        return 0

    sys.stdout.write(dump(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
