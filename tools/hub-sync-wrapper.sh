#!/usr/bin/env bash
# hub-sync-wrapper.sh — reference spoke wrapper for the canonical Hub sync
# (B-239, ADR-024 I-4).
#
# A spoke wrapper only passes parameters and the exit status to the single
# Hub tool tools/hub-sync.py. It must not copy files, resolve revisions or
# write the profile itself. Copy this file into a spoke as is.
#
# Environment:
#   HUB_SYNC_HUB   local clone of the Hub (required unless --hub is passed)
#   HUB_SYNC_TOOL  path to hub-sync.py (default: $HUB_SYNC_HUB/tools/hub-sync.py)
#   PYTHON         interpreter (default: python3)
#
# Usage:
#   HUB_SYNC_HUB=../hybrid-Intelligence-lab tools/hub-sync-wrapper.sh \
#     sync --ref <hub-sha-or-tag> --scope genome
set -euo pipefail

tool="${HUB_SYNC_TOOL:-}"
if [ -z "$tool" ]; then
  if [ -z "${HUB_SYNC_HUB:-}" ]; then
    echo "hub-sync-wrapper: set HUB_SYNC_HUB to a local clone of the Hub or HUB_SYNC_TOOL to tools/hub-sync.py" >&2
    exit 2
  fi
  tool="$HUB_SYNC_HUB/tools/hub-sync.py"
fi

exec "${PYTHON:-python3}" "$tool" "$@"
