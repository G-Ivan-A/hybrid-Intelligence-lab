#!/usr/bin/env python3
"""Inventory semantic evidence in a mango_ba_prompts runs snapshot.

The script is intentionally read-only. It records whether a run contains a
local transcript or declares an external JSON chat export; it does not fetch
attachments or copy source conversations into this repository.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PROCESS_RE = re.compile(r"^process:\s*(.+)$", re.MULTILINE)
CHAT_URL_RE = re.compile(
    r"https://github\.com/user-attachments/files/\d+/\S*chat\S*\.json",
    re.IGNORECASE,
)


def classify(run: Path) -> tuple[str, str, str, str]:
    metadata_path = run / "metadata.yaml"
    metadata = metadata_path.read_text(encoding="utf-8")
    process_match = PROCESS_RE.search(metadata)
    process = process_match.group(1).strip() if process_match else "unknown"
    local_transcript = any(
        path.is_file()
        for path in run.rglob("*")
        if "transcript" in path.name.lower() or "chat" in path.name.lower()
    )
    chat_urls = sorted(set(CHAT_URL_RE.findall(metadata)))
    if local_transcript:
        evidence = "local-transcript"
    elif chat_urls:
        evidence = "external-chat-export"
    else:
        evidence = "no-semantic-transcript"
    return run.name, process, evidence, " ".join(chat_urls)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("runs", type=Path, help="Path to runs/<year>")
    args = parser.parse_args()
    runs = sorted(path for path in args.runs.glob("RUN-*") if path.is_dir())
    print("run_id\tprocess\tevidence\tchat_export")
    for row in map(classify, runs):
        print("\t".join(row))


if __name__ == "__main__":
    main()
