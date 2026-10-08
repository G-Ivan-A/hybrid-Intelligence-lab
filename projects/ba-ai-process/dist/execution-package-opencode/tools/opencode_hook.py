#!/usr/bin/env python3
"""Blocking policy for the OpenCode guard plugin. The runner and CI remain authoritative."""

import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_task import ROOT, check_package, host_path


READ_TOOLS = {"read", "glob", "grep", "list", "todowrite", "todoread", "question", "invalid"}
WRITE_TOOLS = {"write", "edit"}
MCP_RESOURCE_TOOLS = {"list_mcp_resources", "list_mcp_resource_templates", "read_mcp_resource"}
# The approved read-only corporate connection is configured by the analyst under this server name.
KB_SERVER = "kb-readonly"
READ_MCP_VERBS = {"get", "list", "search", "read", "fetch", "query"}
WRITE_MCP_VERBS = {"create", "update", "delete", "write", "edit", "add", "remove", "set", "post", "put",
                   "patch", "move", "transition", "comment", "upload", "assign", "merge", "send"}
TARGET_RULE = "OpenCode may write only submissions/TASK-ID.json"


def allow() -> dict:
    return {"allow": True}


def deny(reason: str) -> dict:
    return {"allow": False, "reason": reason}


def submission_target(raw, base: Path) -> dict:
    if not isinstance(raw, str) or not raw:
        return deny("Write target is missing")
    target = (base / host_path(raw)).resolve()
    try:
        relative = target.relative_to((ROOT / "submissions").resolve())
    except ValueError:
        return deny(TARGET_RULE)
    if len(relative.parts) != 1 or not re.fullmatch(r"TASK-[0-9]{4,}\.json", relative.name):
        return deny(TARGET_RULE)
    return allow()


def patch_targets(text) -> list:
    """Every file named by an apply_patch envelope, including move destinations."""
    if not isinstance(text, str):
        return [None]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    found = re.findall(r"^\*\*\* (?:(?:Add|Update|Delete) File|Move to):(.*)$", text, re.MULTILINE)
    return [item.strip() for item in found] or [None]


def mcp_decision(name: str, args: dict) -> dict:
    if name in MCP_RESOURCE_TOOLS:
        if args.get("server") == KB_SERVER:
            return allow()
        return deny(f"MCP resources are read only from the server named {KB_SERVER}")
    if not name.startswith(KB_SERVER + "_"):
        return deny("This OpenCode tool is not approved for the pilot; the analyst runs commands")
    words = set(re.split(r"[_\-]+", name[len(KB_SERVER) + 1:].lower()))
    if words & READ_MCP_VERBS and not words & WRITE_MCP_VERBS:
        return allow()
    return deny(f"Only read operations of {KB_SERVER} are approved for the pilot")


def decision(event: dict) -> dict:
    try:
        check_package()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        return deny(f"Package integrity check failed: {error}")
    hook = event.get("event")
    if hook == "session.check":
        return allow()
    if hook != "tool.execute.before":
        return deny("Unexpected hook event")
    name = event.get("tool")
    args = event.get("args")
    if not isinstance(name, str) or not isinstance(args, dict):
        return deny("Invalid tool call")
    if name in READ_TOOLS:
        return allow()
    # OpenCode resolves relative paths against the directory where it was started.
    base = host_path(event["directory"]) if isinstance(event.get("directory"), str) else ROOT
    if name in WRITE_TOOLS:
        return submission_target(args.get("filePath"), base)
    if name == "apply_patch":
        for raw in patch_targets(args.get("patchText")):
            verdict = submission_target(raw, base)
            if not verdict["allow"]:
                return verdict
        return allow()
    return mcp_decision(name, args)


if __name__ == "__main__":
    try:
        event = json.load(sys.stdin)
        response = decision(event) if isinstance(event, dict) else deny("Invalid hook input")
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        response = deny("Invalid hook input")
    print(json.dumps(response))
