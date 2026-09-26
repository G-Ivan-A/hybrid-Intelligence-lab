#!/usr/bin/env python3
"""Blocking workspace hook. The runner and CI remain authoritative."""

import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_task import ROOT, check_package


READ_TOOLS = {
    "read_file", "list_files", "search_files", "list_code_definition_names",
    "ask_followup_question", "attempt_completion", "access_mcp_resource", "use_mcp_tool",
}
WRITE_TOOLS = {"write_to_file", "replace_in_file"}


def decision(event: dict) -> dict:
    try:
        check_package()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        return {"cancel": True, "errorMessage": f"Package integrity check failed: {error}"}
    hook = event.get("hookName")
    if hook in {"TaskStart", "TaskResume"}:
        return {"cancel": False}
    if hook != "PreToolUse":
        return {"cancel": True, "errorMessage": "Unexpected hook event"}
    tool = event.get("preToolUse", {})
    name = tool.get("toolName")
    if name in READ_TOOLS:
        return {"cancel": False}
    if name not in WRITE_TOOLS:
        return {"cancel": True, "errorMessage": "Use the external runner for commands; this Cline tool is not approved for the pilot"}
    parameters = tool.get("parameters", {})
    raw = parameters.get("path", parameters.get("file_path"))
    if not isinstance(raw, str):
        return {"cancel": True, "errorMessage": "Write target is missing"}
    target = (ROOT / raw).resolve()
    try:
        relative = target.relative_to(ROOT / "submissions")
    except ValueError:
        return {"cancel": True, "errorMessage": "Cline may write only submissions/TASK-ID.json"}
    if len(relative.parts) != 1 or not re.fullmatch(r"TASK-[0-9]{4,}\.json", relative.name):
        return {"cancel": True, "errorMessage": "Cline may write only submissions/TASK-ID.json"}
    return {"cancel": False}


if __name__ == "__main__":
    try:
        event = json.load(sys.stdin)
        response = decision(event)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        response = {"cancel": True, "errorMessage": "Invalid hook input"}
    print(json.dumps(response))
