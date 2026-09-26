#!/usr/bin/env python3
"""Local, fail-closed transition controller for RG-BCREQ-v1.

The operator runs this program after preparing a node artifact. The agent may
write artifacts, but only this program updates the authoritative route state.
"""

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

try:
    import jsonschema
    import yaml
except ImportError:
    sys.stderr.write("ERROR: install pinned dependencies with pip install -r requirements.txt\n")
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parent.parent
GRAPH = ROOT / "routes/rg-bcreq-v1.yaml"
TERMINAL = {"exit", "halt", "refuse", "handoff-p08"}
TASK_RE = re.compile(r"TASK-[0-9]{4}\Z")


class Refused(Exception):
    pass


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def file_digest(path: Path) -> str:
    return digest(path.read_bytes())


def canonical(value: dict) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def read_document(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Refused("artifact must contain an object")
    return value


def schema_check(name: str, value: dict) -> None:
    schema = json.loads((ROOT / "contracts" / name).read_text(encoding="utf-8"))
    jsonschema.Draft7Validator(schema).validate(value)


def task_root(task_id: str) -> Path:
    if not TASK_RE.fullmatch(task_id):
        raise Refused("task id must have form TASK-NNNN")
    return ROOT / "runs" / task_id


def graph_data() -> dict:
    graph = read_document(GRAPH)
    if graph.get("route_graph_id") != "RG-BCREQ-v1":
        raise Refused("unexpected route graph")
    return graph


def gate(extra: list[str]) -> tuple[list[str], int, str]:
    command = [sys.executable, str(ROOT / "tools/validate-package.py"), str(ROOT), *extra]
    try:
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    except OSError as error:
        raise Refused(f"gate could not start: {error}") from error
    output = (result.stdout + result.stderr).strip()
    return command, result.returncode, output


def load_state(root: Path) -> tuple[dict, list[dict]]:
    state_path = root / "state.json"
    trace_path = root / "trace.jsonl"
    if not state_path.is_file() or not trace_path.is_file():
        raise Refused("runner state or trace is missing")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    if state.get("route_digest") != file_digest(GRAPH):
        raise Refused("route changed after task start")
    rows = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines()]
    if len(rows) != state.get("next_seq", 1) - 1:
        raise Refused("trace length differs from runner state")
    previous = None
    current = "entry"
    for index, row in enumerate(rows, start=1):
        if row.get("seq") != index or row.get("previous_digest") != previous:
            raise Refused("trace sequence or digest chain is broken")
        if sum(row.get(key) is True for key in
               ("script_invoked", "contract_mode", "step_skipped")) != 1:
            raise Refused("trace must contain exactly one step state")
        recorded = row.get("recorded_by")
        if recorded != "runner" or row.get("from") != current or row.get("node") != current:
            raise Refused("trace recorder or route position is invalid")
        if row.get("script_invoked") and (not row.get("command") or not isinstance(row.get("exit_code"), int)):
            raise Refused("script invocation has no command or exit code")
        if row.get("status") == "pass":
            if not row.get("script_invoked") or row.get("exit_code") != 0:
                raise Refused("transition has no successful gate")
            current = row.get("to")
        else:
            if row.get("status") != "reject" or not row.get("reason"):
                raise Refused("rejected step lacks reason")
        previous = row.get("event_digest")
        unsigned = {key: value for key, value in row.items() if key != "event_digest"}
        if previous != digest(canonical(unsigned)):
            raise Refused("trace event digest mismatch")
    if current != state.get("current") or previous != state.get("last_event_digest"):
        raise Refused("runner state differs from trace")
    return state, rows


def save_state(root: Path, state: dict) -> None:
    temporary = root / "state.json.tmp"
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, root / "state.json")


def append_event(root: Path, state: dict, event: dict) -> None:
    event.update({"seq": state["next_seq"], "task_id": state["task_id"],
                  "ts": datetime.now(timezone.utc).isoformat(),
                  "recorded_by": "runner", "previous_digest": state["last_event_digest"]})
    event["event_digest"] = digest(canonical(event))
    with (root / "trace.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    state["next_seq"] += 1
    state["last_event_digest"] = event["event_digest"]
    if event["status"] == "pass":
        state["current"] = event["to"]
        state["status"] = "completed" if event["to"] == "exit" else "active"
    else:
        state["status"] = "blocked"
    save_state(root, state)


def required_target(source: str, artifact: dict | None) -> str | None:
    if source == "entry":
        return "n0"
    if source == "n0":
        assert artifact is not None
        if artifact.get("work_type") == "external-spec":
            return "handoff-p08"
        return "n1"
    if source in {"n4", "n8"}:
        assert artifact is not None
        ambiguities = artifact.get("ambiguities")
        if not isinstance(ambiguities, list):
            raise Refused("branch requires ambiguities array")
        blockers = [item for item in ambiguities if isinstance(item, dict)
                    and item.get("severity") == "blocker"
                    and (source == "n4" or not item.get("resolved_by"))]
        return "n5" if blockers else "n9"
    if source == "n7":
        assert artifact is not None
        answers = artifact.get("answers")
        if not isinstance(answers, list):
            raise Refused("branch requires answers array")
        return "n8" if answers else "halt"
    if source == "n10a":
        assert artifact is not None
        registers = artifact.get("preflight_registers")
        if not isinstance(registers, dict) or not isinstance(registers.get("valid"), bool):
            raise Refused("branch requires preflight_registers.valid")
        return "n11" if registers["valid"] else "halt"
    if source == "n12":
        assert artifact is not None
        if artifact.get("state") != "approved" or not artifact.get("working_digest"):
            raise Refused("Working baseline is not approved")
        return "n13"
    if source == "n13":
        return "exit"
    return None  # The graph has one gate_passed edge from this node.


def advance(args: argparse.Namespace) -> None:
    root = task_root(args.task_id)
    lock = root / ".runner-lock"
    try:
        lock.mkdir()
    except FileExistsError as error:
        raise Refused("another runner command is active or its lock needs review") from error
    try:
        state, _rows = load_state(root)
        if state["status"] != "active" or state["current"] in TERMINAL:
            raise Refused("task is blocked or finished")
        graph = graph_data()
        source = state["current"]
        nodes = {item["node"]: item for item in graph["nodes"]}
        edges = [edge for edge in graph["edges"] if edge["from"] == source]
        event = {"node": source, "from": source, "to": args.to, "gate": "G-mach",
                 "script_invoked": False, "contract_mode": False,
                 "step_skipped": True, "status": "reject"}
        try:
            matching = [edge for edge in edges if edge["to"] == args.to]
            if len(matching) != 1:
                raise Refused("transition is absent from the route")
            artifact_path = Path(args.artifact).resolve()
            if not artifact_path.is_file():
                raise Refused("node artifact is missing")
            if artifact_path.stat().st_size == 0:
                raise Refused("node artifact is empty")
            artifact = read_document(artifact_path) if source in {
                "entry", "n0", "n4", "n5", "n6", "n7", "n8", "n10a", "n12", "n13"
            } else None
            if source in {"entry", "n0"}:
                schema_check("c-in.schema.json", artifact)
                if artifact["task"]["id"] != args.task_id:
                    raise Refused("A-IN belongs to another task")
            if source == "n0" and artifact["product_attribution"]["status"] != "confirmed":
                raise Refused("n0 requires confirmed product attribution")
            if source in {"n4", "n8"}:
                schema_check("c-core.schema.json", artifact)
            if source in {"n5", "n6"}:
                schema_check("c-quest.schema.json", artifact)
            if source == "n12":
                schema_check("c-working-bcreq.schema.json", artifact)
            if source == "n13":
                schema_check("c-release-bcreq.schema.json", artifact)
            expected = required_target(source, artifact)
            if expected is not None and args.to != expected:
                raise Refused(f"predicate selects {expected}, not {args.to}")
            if expected is None and len(edges) != 1:
                raise Refused("route has ambiguous gate_passed edges")
            event["output_digest"] = file_digest(artifact_path)
            event["output_ref"] = str(artifact_path)
            support_paths = []
            checkpoint = None
            if source in nodes and "G-human" in nodes[source]["gates"]:
                if not args.checkpoint:
                    raise Refused("human gate requires checkpoint")
                checkpoint = Path(args.checkpoint).resolve()
                if not checkpoint.is_file() or not checkpoint.read_text(encoding="utf-8").strip():
                    raise Refused("human checkpoint is missing or empty")
                event["checkpoint_ref"] = str(checkpoint)
                event["checkpoint_digest"] = file_digest(checkpoint)
            extra = []
            if source == "n0":
                extra = ["--input", str(artifact_path)]
            elif source == "n12":
                extra = ["--working", str(artifact_path)]
            elif source == "n13":
                if not args.working or not args.manifest:
                    raise Refused("Release gate requires --working and --manifest")
                support_paths = [Path(args.working).resolve(), Path(args.manifest).resolve()]
                event["support_digests"] = {str(path): file_digest(path) for path in support_paths}
                extra = ["--working", str(support_paths[0]),
                         "--release", str(artifact_path),
                         "--manifest", str(support_paths[1])]
            command, code, output = gate(extra)
            event.update({"script_invoked": True, "step_skipped": False,
                          "command": command, "exit_code": code,
                          "gate_output": output[-2000:]})
            if code != 0:
                raise Refused(f"G-mach exited {code}: {output[-300:]}")
            if checkpoint is not None:
                if not sys.stdin.isatty():
                    raise Refused("human gate requires an interactive terminal")
                challenge = f"APPROVE {args.task_id}:{source} {event['checkpoint_digest']}"
                print(f"Review {checkpoint}\nType exactly: {challenge}", flush=True)
                try:
                    answer = input().strip()
                except (EOFError, KeyboardInterrupt) as error:
                    raise Refused("human gate was not approved") from error
                if answer != challenge:
                    raise Refused("human gate was not approved")
            if file_digest(GRAPH) != state["route_digest"] or file_digest(artifact_path) != event["output_digest"]:
                raise Refused("route or node artifact changed during gate")
            if checkpoint is not None and file_digest(checkpoint) != event["checkpoint_digest"]:
                raise Refused("human checkpoint changed during gate")
            if any(file_digest(path) != event["support_digests"][str(path)] for path in support_paths):
                raise Refused("Release input changed during gate")
            event["status"] = "pass"
            event["reason"] = ""
        except (Refused, jsonschema.ValidationError, OSError, ValueError, KeyError) as error:
            event["reason"] = str(error)
            append_event(root, state, event)
            raise Refused(str(error)) from error
        append_event(root, state, event)
        print(f"{args.task_id}: {source} -> {args.to}; G-mach exit 0; trace seq {event['seq']}")
    finally:
        lock.rmdir()


def start(args: argparse.Namespace) -> None:
    root = task_root(args.task_id)
    if root.exists():
        raise Refused("task already exists; use a new task id")
    graph_data()
    command, code, output = gate([])
    if code != 0:
        raise Refused(f"package preflight failed: {output[-300:]}")
    root.mkdir()
    (root / "trace.jsonl").touch()
    save_state(root, {"task_id": args.task_id, "route_id": "RG-BCREQ-v1",
                      "route_digest": file_digest(GRAPH), "current": "entry",
                      "status": "active", "next_seq": 1,
                      "last_event_digest": None,
                      "preflight_command": command})
    print(f"{args.task_id}: started at entry; next transition requires G-mach")


def metrics(args: argparse.Namespace) -> None:
    state, rows = load_state(task_root(args.task_id))
    expected = len(rows)
    deterministic = sum(row["script_invoked"] and row.get("exit_code") == 0
                        and row["recorded_by"] == "runner" for row in rows)
    result = {"task_id": args.task_id, "current": state["current"],
              "status": state["status"], "expected_steps": expected,
              "deterministic_steps": deterministic,
              "deterministic_share": deterministic / expected if expected else None}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    begin = sub.add_parser("start", help="create a task after package preflight")
    begin.add_argument("task_id")
    step = sub.add_parser("advance", help="run gate and attempt one route transition")
    step.add_argument("task_id")
    step.add_argument("--to", required=True)
    step.add_argument("--artifact", required=True)
    step.add_argument("--checkpoint")
    step.add_argument("--working")
    step.add_argument("--manifest")
    report = sub.add_parser("metrics", help="report deterministic step share")
    report.add_argument("task_id")
    args = parser.parse_args()
    try:
        {"start": start, "advance": advance, "metrics": metrics}[args.action](args)
    except (Refused, OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as error:
        sys.stderr.write(f"BLOCKED: {error}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
