#!/usr/bin/env python3
"""Bounded arithmetic and state-contract probes, with manually labelled BA cases.

No network, LLM, runtime SDK, semantic classifier, or authentication service.
--write records results; --check verifies the committed deterministic evidence.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def ratio(numerator, denominator):
    return round(numerator / denominator, 6) if denominator else None


def metrics(case, gold):
    gold_ids = {f["id"] for f in gold}
    critical = {f["id"] for f in gold if f["critical"]}
    covered = set(case["covered"])
    require(covered <= gold_ids, "Unknown manually labelled fact")
    require(len(covered) == len(case["covered"]), "Duplicate gold mapping")
    tp, fp = len(covered), len(set(case["unsupported"]))
    return {
        "tp": tp,
        "fp": fp,
        "fn": len(gold_ids - covered),
        "completeness": ratio(tp, len(gold_ids)),
        "precision": ratio(tp, tp + fp),
        "critical_completeness": ratio(len(covered & critical), len(critical)),
        "contradictions": len(case["contradictions"]),
        "machine_pass": case["machine_pass"],
        "escalated": case["escalated"],
    }


def envelope_errors(envelope, current_sources):
    errors = []
    if envelope["source_version"] != current_sources:
        errors.append("stale-source")
    if envelope["payload_hash"] != digest(envelope["payload"]):
        errors.append("changed-payload")
    available = set(envelope["source_refs"])
    if any(not fact["source"] or fact["source"] not in available
           for fact in envelope["payload"]):
        errors.append("missing-evidence")
    return errors


def may_publish(envelope, approval, validation, principal):
    # principal is a trusted identity-service input, not an LLM-supplied field.
    return (
        not envelope_errors(envelope, "source-set@1")
        and principal == "ba-owner"
        and approval["actor"] == principal
        and approval["decision"] == "approve"
        and approval["hash"] == envelope["payload_hash"]
        and approval["revision"] == envelope["revision"]
        and validation["hash"] == envelope["payload_hash"]
        and validation["revision"] == envelope["revision"]
        and validation["pass"] is True
    )


def run():
    data = json.loads((ROOT / "cases.json").read_text())
    require(len(data["gold"]) == 8 and len(data["variants"]) == 4, "Bounded fixture size changed")
    gold = data["gold"]
    variants = {case["id"]: metrics(case, gold) for case in data["variants"]}
    probes = []

    def record(identifier, perspective, observation, condition):
        require(condition, identifier + ": unexpected observation")
        probes.append({"id": identifier, "perspective": perspective, "observation": observation})

    envelope = {
        "revision": 1,
        "source_version": "source-set@1",
        "source_refs": [f["source"] for f in gold],
        "payload": gold,
        "payload_hash": digest(gold),
    }
    restored = json.loads(json.dumps(envelope))
    record("H1-1", "architecture", "JSON round-trip retains all 8 facts and references",
           restored == envelope and not envelope_errors(restored, "source-set@1"))
    summary_ids = {"F1", "F3", "F4", "F5", "F7", "F8"}
    lost = sorted(f["id"] for f in gold if f["id"] not in summary_ids)
    record("H1-2", "human-governance", "Lossy summary omits F2 and F6",
           lost == ["F2", "F6"])
    record("H1-3", "operations", "Changed source revision invalidates old envelope",
           envelope_errors(envelope, "source-set@2") == ["stale-source"])
    missing = copy.deepcopy(envelope)
    missing["payload"][0]["source"] = ""
    missing["payload_hash"] = digest(missing["payload"])
    record("H1-4", "security", "Absent source pointer is rejected",
           envelope_errors(missing, "source-set@1") == ["missing-evidence"])
    semantic = copy.deepcopy(envelope)
    semantic["payload"][1]["text"] = "A manager may approve their own request."
    semantic["payload_hash"] = digest(semantic["payload"])
    record("H1-5", "human-governance", "Well-formed evidence pointer does not prove entailment",
           not envelope_errors(semantic, "source-set@1")
           and semantic["payload"][1]["text"] != gold[1]["text"])

    approval = {"actor": "ba-owner", "decision": "approve", "hash": digest(gold), "revision": 1}
    validation = {"pass": True, "hash": digest(gold), "revision": 1}
    record("H2-1", "architecture", "Matching owner, validation and revision permit publication",
           may_publish(envelope, approval, validation, "ba-owner"))
    changed = copy.deepcopy(envelope)
    changed["revision"] = 2
    record("H2-2", "operations", "An approval for revision 1 cannot publish revision 2",
           not may_publish(changed, approval, validation, "ba-owner"))
    changed_payload = copy.deepcopy(envelope)
    changed_payload["payload"] = gold[:-1]
    record("H2-3", "security", "Mutation without a new hash is detected",
           envelope_errors(changed_payload, "source-set@1") == ["changed-payload"]
           and not may_publish(changed_payload, approval, validation, "ba-owner"))
    record("H2-4", "human-governance", "An agent cannot act as the owner with a copied approval",
           not may_publish(envelope, approval, validation, "generator-agent"))
    ledger = {}

    def publish_once(key):
        if key not in ledger:
            ledger[key] = "REQ-001"
        return ledger[key]

    key = digest({"artifact": envelope["payload_hash"], "target": "tenant-A/requirements"})
    first = publish_once(key)
    second = publish_once(key)
    record("H2-5", "operations", "Two delivery attempts create one logical record in the toy ledger",
           first == second and len(ledger) == 1)

    complete, summary = variants["complete"], variants["fluent-summary"]
    verbose, abstention = variants["verbose"], variants["honest-abstention"]
    record("H3-1", "architecture", "100% schema-pass coexists with 75% completeness",
           summary["machine_pass"] and summary["completeness"] == 0.75)
    record("H3-2", "security", "100% completeness coexists with 66.6667% precision",
           verbose["completeness"] == 1 and verbose["precision"] == 0.666667)
    record("H3-3", "human-governance", "Omitted critical facts remain visible despite fluent output",
           summary["critical_completeness"] == 0 and summary["contradictions"] == 1)
    record("H3-4", "operations", "A justified abstention lowers pass rate and preserves precision",
           not abstention["machine_pass"] and abstention["precision"] == 1
           and abstention["escalated"])
    require(complete["completeness"] == 1 and complete["precision"] == 1, "Positive metric control")
    first_pass = sum(c["machine_pass"] for c in data["variants"])
    false_passes = sum(c["machine_pass"] and c["needs_escalation"] for c in data["variants"])
    needed = sum(c["needs_escalation"] for c in data["variants"])
    handled = sum(c["needs_escalation"] and c["escalated"] for c in data["variants"])
    escalated = sum(c["escalated"] for c in data["variants"])
    record("H3-5", "human-governance", "75% first-pass rate hides 2 false passes; escalation recall is 1/3",
           first_pass == 3 and false_passes == 2 and needed == 3 and handled == 1
           and escalated == 1)
    require(len(probes) == 15, "Exactly five independent probes per hypothesis")
    return {
        "kind": "deterministic synthetic measurement; no LLM or vendor benchmark",
        "fixture_sha256": hashlib.sha256((ROOT / "cases.json").read_bytes()).hexdigest(),
        "variants": variants,
        "aggregate": {
            "first_pass_rate": ratio(first_pass, 4),
            "false_pass_rate_among_passed": ratio(false_passes, first_pass),
            "human_escalation_rate": ratio(escalated, 4),
            "escalation_recall": ratio(handled, needed),
            "probes_passed": len(probes),
        },
        "probes": probes,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = run()
    target = ROOT / "results.json"
    if args.write:
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    else:
        require(result == json.loads(target.read_text()), "Recorded results differ; investigate before regenerating")
    print("15/15 synthetic probes passed; 4 labelled variants; committed results "
          + ("written" if args.write else "verified"))


if __name__ == "__main__":
    main()
