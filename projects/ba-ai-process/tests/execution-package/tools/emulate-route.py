#!/usr/bin/env python3
"""Deterministic RG-BCREQ-v1 emulator for mocks; never invokes an LLM or MCP."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re

import yaml


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    _, raw, _ = text.split("---", 2)
    return yaml.safe_load(raw) or {}


def _skill_index(package: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for path in sorted((package / ".gigacode/skills").glob("*/SKILL.md")):
        fields = _frontmatter(path)
        pack = fields.get("packs", "")
        if isinstance(pack, str) and "/" in pack:
            result[pack.split("/", 1)[1]] = path
    return result


def emulate(package: Path, fixture_path: Path, output_root: Path) -> dict:
    fixture = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))
    graph = yaml.safe_load((package / "routes/rg-bcreq-v1.yaml").read_text(encoding="utf-8"))
    task_id = fixture["task_id"]
    run_id = fixture["run_id"]
    if not re.fullmatch(r"TASK-[0-9]{4}", task_id):
        raise ValueError(f"invalid task id: {task_id}")

    nodes = {item["node"]: item for item in graph["nodes"]}
    edges = {(edge["from"], edge["to"]): edge for edge in graph["edges"]}
    skills = _skill_index(package)
    approved = set(fixture.get("human_approvals", []))
    pause_at = fixture.get("pause_at")
    task_root = output_root / task_id
    (task_root / "runs").mkdir(parents=True)
    (task_root / "evidence").mkdir()

    now = datetime.now(timezone.utc).isoformat()
    path = ["entry"]
    events = []
    current = "entry"
    seq = 0
    outcome = "in-progress"

    while current not in {"exit", "halt", "refuse"}:
        try:
            target = fixture["transitions"][current]
        except KeyError as error:
            raise ValueError(f"fixture has no deterministic transition from {current}") from error
        if (current, target) not in edges:
            raise ValueError(f"route forbids transition {current} -> {target}")
        path.append(target)
        seq += 1
        events.append(
            {
                "seq": seq,
                "event_type": "transition",
                "actor": "agent",
                "input_ref": current,
                "output_ref": target,
                "source_refs": [],
                "decision": edges[(current, target)]["condition"],
                "at": now,
            }
        )

        if target in nodes:
            node = nodes[target]
            if node["actor"] == "agent":
                skill = skills.get(node["skill"])
                if skill is None or not skill.is_file():
                    raise ValueError(f"{target} has no native skill for {node['skill']}")
                seq += 1
                events.append(
                    {
                        "seq": seq,
                        "event_type": "skill-invocation",
                        "actor": "agent",
                        "node": target,
                        "skill": skill.parent.name,
                        "input_ref": f"mock:{current}",
                        "output_ref": f"mock:{target}",
                        "source_refs": [],
                        "verdict": "pass",
                        "at": now,
                    }
                )
            if "G-human" in node["gates"] and target not in approved and target != pause_at:
                raise ValueError(f"fixture did not resolve human gate at {target}")
            if target == pause_at:
                if "G-human" not in node["gates"]:
                    raise ValueError(f"fixture may pause only at a human gate, got {target}")
                checkpoint = task_root / "evidence" / f"checkpoint-{target}.md"
                checkpoint.write_text(
                    "# Human checkpoint\n\n"
                    f"- Task: `{task_id}`\n"
                    f"- Node: `{target}`\n"
                    "- Decision: awaiting explicit human input\n",
                    encoding="utf-8",
                )
                seq += 1
                events.append(
                    {
                        "seq": seq,
                        "event_type": "artifact-write",
                        "actor": "agent",
                        "node": target,
                        "input_ref": f"mock:{target}",
                        "output_ref": f"evidence/{checkpoint.name}",
                        "source_refs": [],
                        "at": now,
                    }
                )
                seq += 1
                events.append(
                    {
                        "seq": seq,
                        "event_type": "gate",
                        "actor": "human",
                        "node": target,
                        "gate": "G-human",
                        "input_ref": f"evidence/{checkpoint.name}",
                        "output_ref": "pending:human-decision",
                        "source_refs": [],
                        "at": now,
                    }
                )
                outcome = "awaiting-human"
                current = target
                break
            if "G-human" in node["gates"]:
                seq += 1
                events.append(
                    {
                        "seq": seq,
                        "event_type": "gate",
                        "actor": "human",
                        "node": target,
                        "gate": "G-human",
                        "verdict": "pass",
                        "input_ref": f"mock:{target}",
                        "output_ref": f"approval:{target}",
                        "source_refs": [],
                        "at": now,
                    }
                )
        current = target

    if current == "exit":
        outcome = "completed"
        (task_root / "A-BCREQ.md").write_text(
            "# Mock A-BCREQ\n\nGenerated by deterministic route emulation.\n",
            encoding="utf-8",
        )
        seq += 1
        events.append(
            {
                "seq": seq,
                "event_type": "artifact-write",
                "actor": "agent",
                "input_ref": "mock:n12",
                "output_ref": "A-BCREQ.md",
                "source_refs": [],
                "at": now,
            }
        )
    elif current in {"halt", "refuse"}:
        outcome = "refused"

    task = {
        "schema_version": 1,
        "task_id": task_id,
        "route_id": graph["route_graph_id"],
        "active_run_id": run_id,
        "status": outcome,
    }
    run = {
        "run_id": run_id,
        "route_id": graph["route_graph_id"],
        "task_id": task_id,
        "started_at": now,
        "outcome": outcome,
        "events": events,
        "handover": {
            "objective": fixture["name"],
            "ssot_refs": ["routes/rg-bcreq-v1.yaml"],
            "process_version": graph["route_graph_id"],
            "current_node": current,
            "path": path,
            "decisions": [event["decision"] for event in events if "decision" in event],
            "gate_results": [event["verdict"] for event in events if "verdict" in event],
            "open_items": ["human decision required"] if outcome == "awaiting-human" else [],
            "artifact_refs": ["A-BCREQ.md"] if outcome == "completed" else [],
        },
    }
    (task_root / "task.yaml").write_text(yaml.safe_dump(task, sort_keys=False), encoding="utf-8")
    (task_root / "runs" / f"{run_id}.yaml").write_text(
        yaml.safe_dump(run, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    return {"outcome": outcome, "path": path, "task_root": task_root}
