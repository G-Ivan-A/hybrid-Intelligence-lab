#!/usr/bin/env python3
"""Fail-closed BCREQ Working validation and deterministic Release compilation.

The accepted source contracts are at
https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md
and
https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-working-release-pipeline.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def digest(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def working_digest(working: dict) -> str:
    return digest({key: value for key, value in working.items() if key != "working_digest"})


def _schema_errors(value: object, rule: dict, root: dict, path: str = "$value") -> list[str]:
    """Execute the draft-07 subset used by the self-contained Working schema."""
    if "$ref" in rule:
        target = root
        for part in rule["$ref"].removeprefix("#/").split("/"):
            target = target[part]
        return _schema_errors(value, target, root, path)
    errors: list[str] = []
    if "const" in rule and value != rule["const"]:
        errors.append(f"SCHEMA {path} differs from const")
    if "enum" in rule and value not in rule["enum"]:
        errors.append(f"SCHEMA {path} is outside enum")
    allowed = rule.get("type")
    if allowed:
        allowed = allowed if isinstance(allowed, list) else [allowed]
        valid = any({
            "object": lambda: isinstance(value, dict),
            "array": lambda: isinstance(value, list),
            "string": lambda: isinstance(value, str),
            "integer": lambda: isinstance(value, int) and not isinstance(value, bool),
            "boolean": lambda: isinstance(value, bool),
            "null": lambda: value is None,
        }[kind]() for kind in allowed)
        if not valid:
            return errors + [f"SCHEMA {path} has wrong type"]
    if isinstance(value, str):
        if len(value) < rule.get("minLength", 0):
            errors.append(f"SCHEMA {path} is empty")
        if "pattern" in rule and re.search(rule["pattern"], value) is None:
            errors.append(f"SCHEMA {path} has invalid format")
    if isinstance(value, list):
        if len(value) < rule.get("minItems", 0):
            errors.append(f"SCHEMA {path} has too few items")
        if "maxItems" in rule and len(value) > rule["maxItems"]:
            errors.append(f"SCHEMA {path} has too many items")
        if rule.get("uniqueItems") and len({canonical(item) for item in value}) != len(value):
            errors.append(f"SCHEMA {path} has duplicate items")
        if "items" in rule:
            for index, item in enumerate(value):
                errors.extend(_schema_errors(item, rule["items"], root, f"{path}[{index}]"))
    if isinstance(value, dict):
        for field in set(rule.get("required", [])) - set(value):
            errors.append(f"SCHEMA {path}.{field} is required")
        properties = rule.get("properties", {})
        for field, item in value.items():
            if field in properties:
                errors.extend(_schema_errors(item, properties[field], root, f"{path}.{field}"))
            elif rule.get("additionalProperties") is False:
                errors.append(f"SCHEMA {path}.{field} is not allowed")
    return errors


def _ids(items: object, key: str, prefix: str, errors: list[str], label: str) -> set[str]:
    if not isinstance(items, list):
        errors.append(f"SCHEMA {label} must be an array")
        return set()
    seen: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"SCHEMA {label}[{index}] must be an object")
            continue
        value = item.get(key)
        if not isinstance(value, str) or not re.fullmatch(prefix + r"-[0-9]{3}", value):
            errors.append(f"SCHEMA {label}[{index}].{key} has invalid typed ID")
        elif value in seen:
            errors.append(f"SCHEMA {label} duplicate ID {value}")
        else:
            seen.add(value)
    return seen


def _refs(item: dict, field: str, valid: set[str], errors: list[str], code: str,
          *, nonempty: bool = True) -> None:
    refs = item.get(field)
    if not isinstance(refs, list) or (nonempty and not refs) or any(
        not isinstance(ref, str) or ref not in valid for ref in refs
    ) or len(refs) != len(set(str(ref) for ref in refs)):
        errors.append(f"{code} {field} must contain unique existing IDs")


def _text(item: dict, field: str, errors: list[str], code: str) -> None:
    if not isinstance(item.get(field), str) or not item[field].strip():
        errors.append(f"{code} {field} is required")


def _taxonomy_paths(package: Path) -> set[tuple[str, str, str, str]]:
    data = json.loads((package / "taxonomy/mango-products.yaml").read_text(encoding="utf-8"))
    paths: set[tuple[str, str, str, str]] = set()
    for domain in data.get("domains", []):
        for capability in domain.get("capabilities", []):
            for feature in capability.get("features", []):
                for atomic in capability.get("atomic_functions", []):
                    paths.add((domain["id"], capability["id"], feature, atomic["id"]))
    return paths


def validate_working(working: object, package: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(working, dict):
        return ["SCHEMA Working must be an object"]
    schema = json.loads((package / "contracts/c-working-bcreq.schema.json").read_text(encoding="utf-8"))
    errors.extend(_schema_errors(working, schema, schema, "Working"))
    if any("wrong type" in error for error in errors):
        return errors
    missing = set(schema["required"]) - set(working)
    unknown = set(working) - set(schema["properties"])
    if missing or unknown:
        errors.append(f"SCHEMA Working missing={sorted(missing)} unknown={sorted(unknown)}")
    if working.get("schema_version") != 1 or working.get("artifact_class") != "A-BCREQ" or working.get("projection") != "working":
        errors.append("SCHEMA Working version or artifact class is invalid")
    if working.get("state") != "approved" or not re.fullmatch(r"WB-[0-9]{3}", str(working.get("working_baseline_id", ""))):
        errors.append("BASELINE Working must be approved with a typed baseline ID")
    if working.get("working_digest") != working_digest(working):
        errors.append("BASELINE Working digest does not match canonical content")

    work_type = working.get("work_type")
    axis = {"mango-change": "mango", "mango-kb": "mango", "industry-practice": "industry", "external-spec": "industry"}
    routing = working.get("routing") or {}
    if not isinstance(routing, dict):
        routing = {}
    if not isinstance(routing, dict) or work_type not in axis or routing.get("primary_axis") != axis.get(work_type) or routing.get("rule") != work_type or routing.get("decision") != "confirmed" or not routing.get("decision_ref"):
        errors.append("ROUTE primary axis must follow confirmed work type")
    if work_type == "external-spec":
        errors.append("ROUTE external-spec belongs to P-08, outside this BCREQ compiler")

    evidence = _ids(working.get("evidence"), "id", "SRC", errors, "evidence")
    _ids(working.get("terms"), "id", "TERM", errors, "terms")
    constraints = _ids(working.get("constraints"), "id", "CON", errors, "constraints")
    goals = _ids(working.get("goals"), "id", "GOAL", errors, "goals")
    tasks = _ids(working.get("tasks"), "id", "TASK", errors, "tasks")
    deltas = _ids(working.get("deltas"), "id", "DELTA", errors, "deltas")
    bindings = _ids(working.get("product_bindings"), "id", "PB", errors, "product_bindings")
    claims = _ids(working.get("claims"), "id", "CL", errors, "claims")
    stories = _ids(working.get("user_stories"), "id", "US", errors, "user_stories")
    fr = _ids(working.get("fr"), "requirement_id", "FR", errors, "fr")
    uc = _ids(working.get("uc"), "scenario_id", "UC", errors, "uc")
    nfr = _ids(working.get("nfr"), "requirement_id", "NFR", errors, "nfr")
    acceptance = _ids(working.get("acceptance"), "id", "AC", errors, "acceptance")
    design = _ids(working.get("design"), "id", "DES", errors, "design")
    edges = _ids(working.get("edge_cases"), "id", "EDGE", errors, "edge_cases")
    obligations = _ids(working.get("compatibility_obligations"), "id", "COMP", errors, "compatibility_obligations")
    questions = _ids(working.get("open_questions"), "id", "OPEN", errors, "open_questions")
    _ids(working.get("industry_bindings"), "id", "IND", errors, "industry_bindings")
    if not evidence or not goals or not tasks or not deltas or not bindings or not claims or not stories or not fr or not uc or not acceptance or not design:
        errors.append("PREFLIGHT and requirement registers cannot be empty")
    for source in working.get("evidence") or []:
        if not isinstance(source, dict):
            continue
        if source.get("retrieval_status") != "read" or not all(source.get(key) for key in ("locator", "anchor", "excerpt", "checksum")):
            errors.append("EVID-01 accepted evidence requires read status, anchor, excerpt and checksum")
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", str(source.get("checksum", ""))):
            errors.append("EVID-03 evidence checksum must be SHA-256")
        elif source.get("checksum") != "sha256:" + hashlib.sha256(str(source.get("excerpt", "")).encode("utf-8")).hexdigest():
            errors.append("EVID-03 evidence checksum does not match the retained excerpt")
    for field, names in (("terms", ("term", "definition")), ("constraints", ("text",))):
        for item in working.get(field) or []:
            if isinstance(item, dict):
                _refs(item, "source_refs", evidence, errors, "PREFLIGHT")
                for name in names:
                    _text(item, name, errors, "PREFLIGHT")
    for goal in working.get("goals") or []:
        if isinstance(goal, dict):
            _text(goal, "text", errors, "PREFLIGHT")
            _refs(goal, "source_refs", evidence, errors, "PREFLIGHT")
    for task in working.get("tasks") or []:
        if isinstance(task, dict):
            _text(task, "text", errors, "PREFLIGHT")
            _refs(task, "goal_refs", goals, errors, "PREFLIGHT")
    boundary = working.get("boundary") or {}
    if not isinstance(boundary, dict) or not re.fullmatch(r"BND-[0-9]{3}", str(boundary.get("id", ""))) or not boundary.get("system") or not boundary.get("in_scope") or not isinstance(boundary.get("out_of_scope"), list):
        errors.append("PREFLIGHT explicit system, in_scope and out_of_scope are required")
        if not isinstance(boundary, dict):
            boundary = {}
    delta_map = {d.get("id"): d for d in working.get("deltas") or [] if isinstance(d, dict)}
    for delta in delta_map.values():
        _refs(delta, "source_refs", evidence, errors, "SCOPE-01")
        for key in ("as_is", "requested_delta"):
            _text(delta, key, errors, "SCOPE-01")
        if delta.get("disposition") not in {"change", "as-is", "rejected"}:
            errors.append("SCOPE-01 delta disposition is invalid")
    taxonomy = _taxonomy_paths(package)
    for binding in working.get("product_bindings") or []:
        if not isinstance(binding, dict):
            continue
        path = tuple(binding.get(key) for key in ("domain", "capability", "feature", "atomic_function"))
        if any(not isinstance(part, str) for part in path) or path not in taxonomy:
            errors.append("PRODUCT local binding is not in the versioned taxonomy")
        _refs(binding, "source_refs", evidence, errors, "PRODUCT")

    claim_map = {c.get("id"): c for c in working.get("claims") or [] if isinstance(c, dict)}
    for claim in claim_map.values():
        for field, ids in (("source_refs", evidence), ("goal_refs", goals), ("task_refs", tasks), ("product_binding_refs", bindings)):
            _refs(claim, field, ids, errors, "REL-01")
        _text(claim, "candidate_statement", errors, "REL-01")
        _text(claim, "relevance_reason", errors, "REL-01")
        if claim.get("system_boundary") != boundary.get("system") or claim.get("delta_ref") not in deltas:
            errors.append("REL-01 claim lacks boundary or delta link")
        if claim.get("relevance_decision") not in {"accepted", "rejected", "hypothesis", "open"}:
            errors.append("REL-01 invalid claim relevance decision")
        if claim.get("abstraction_level") not in {"L1", "L2", "L3", "L4"} or claim.get("target_slot") not in {"S-FR", "S-SCENARIO", "S-SOLUTION", "S-AC", "S-SETTINGS", "S-UI", "S-INTEGRATION", "S-TRACE", "S-NFR", "S-LIMITS", "S-OPEN"}:
            errors.append("FR-01 claim level or slot is invalid")
    for story in working.get("user_stories") or []:
        if isinstance(story, dict):
            _text(story, "text", errors, "PREFLIGHT")

    fr_map = {r.get("requirement_id"): r for r in working.get("fr") or [] if isinstance(r, dict)}
    uc_map = {r.get("scenario_id"): r for r in working.get("uc") or [] if isinstance(r, dict)}
    for requirement in fr_map.values():
        claim = claim_map.get(requirement.get("claim_ref"), {})
        if claim.get("relevance_decision") != "accepted" or claim.get("target_slot") != "S-FR" or claim.get("abstraction_level") != "L1":
            errors.append("FR-01 FR requires an accepted L1 capability claim")
        if requirement.get("abstraction_level") != "L1" or requirement.get("system_subject") != boundary.get("system"):
            errors.append("FR-01 top-level FR must be an L1 target-system capability")
        _text(requirement, "shall", errors, "FR-01")
        if not re.search(r"\bshall\b|должн", str(requirement.get("shall", "")), re.I):
            errors.append("FR-01 FR must express an obligation")
        if re.search(r"\b(button|field|tab|checkbox|dropdown|endpoint|payload)\b|кнопк|вкладк|настройк", str(requirement.get("shall", "")), re.I):
            exception = requirement.get("ui_detail_exception") or {}
            if not all(exception.get(key) for key in ("reviewed_by", "rationale", "source_ref")) or exception.get("source_ref") not in evidence:
                errors.append("FR-01 atomic UI or implementation detail needs an explicit reviewed source exception")
        for field, ids in (("goal_refs", goals), ("task_refs", tasks), ("source_refs", evidence), ("user_story_refs", stories), ("product_binding_refs", bindings), ("scenario_refs", uc), ("acceptance_refs", acceptance)):
            _refs(requirement, field, ids, errors, "FR-TRACE")
        delta = delta_map.get(requirement.get("delta_ref"))
        if not delta or delta.get("disposition") != "change":
            errors.append("SCOPE-01 FR must trace to a confirmed requested delta")
    for scenario in uc_map.values():
        for key in ("actor", "trigger", "outcome"):
            _text(scenario, key, errors, "UC-01")
        if scenario.get("goal_ref") not in goals or not scenario.get("main_flow") or not isinstance(scenario.get("preconditions"), list) or not isinstance(scenario.get("alternatives"), list) or not isinstance(scenario.get("exceptions"), list):
            errors.append("UC-01 incomplete use case flow")
        for field, ids in (("requirement_refs", fr), ("nfr_refs", nfr), ("constraint_refs", constraints)):
            _refs(scenario, field, ids, errors, "UC-TRACE", nonempty=False)
        if not (scenario.get("requirement_refs") or scenario.get("nfr_refs") or scenario.get("constraint_refs")):
            errors.append("UC-TRACE scenario has no requirement owner")
        for ref in scenario.get("requirement_refs") or []:
            if scenario.get("scenario_id") not in fr_map.get(ref, {}).get("scenario_refs", []):
                errors.append("UC-TRACE FR and UC coverage is not bidirectional")
    for requirement in fr_map.values():
        for ref in requirement.get("scenario_refs") or []:
            if requirement.get("requirement_id") not in uc_map.get(ref, {}).get("requirement_refs", []):
                errors.append("UC-TRACE FR and UC coverage is not bidirectional")

    for item in working.get("nfr") or []:
        if not isinstance(item, dict):
            continue
        _refs(item, "applies_to_fr", fr, errors, "NFR-TRACE")
        _refs(item, "source_refs", evidence, errors, "NFR-01")
        for key in ("quality_attribute", "object", "condition", "measure", "target", "verification_method", "text"):
            _text(item, key, errors, "NFR-01")
        if item.get("target") == "TBD":
            if item.get("target_source_ref") not in questions:
                errors.append("NFR-01 TBD needs an owned open question")
        elif item.get("target_source_ref") not in evidence:
            errors.append("NFR-01 numeric target needs a source anchor")
    for item in working.get("constraints") or []:
        if isinstance(item, dict):
            _refs(item, "applies_to_fr", fr, errors, "CON-TRACE", nonempty=False)
    for item in working.get("acceptance") or []:
        if isinstance(item, dict):
            if item.get("fr_ref") not in fr:
                errors.append("FR-TRACE acceptance has unknown FR")
            _text(item, "text", errors, "FR-TRACE")
    for item in working.get("design") or []:
        if isinstance(item, dict):
            _refs(item, "fr_refs", fr, errors, "DESIGN")
            _refs(item, "scenario_refs", uc, errors, "DESIGN")
            _text(item, "text", errors, "DESIGN")
    for requirement in fr:
        if not any(requirement in item.get("fr_refs", []) for item in working.get("design") or [] if isinstance(item, dict)):
            errors.append(f"DESIGN {requirement} has no selected design")
    for edge in working.get("edge_cases") or []:
        if isinstance(edge, dict):
            _refs(edge, "requirement_refs", fr | nfr, errors, "EDGE")
            _text(edge, "expected_outcome", errors, "EDGE")
            if edge.get("verification_ref") not in acceptance:
                errors.append("EDGE edge case needs verification")

    compatibility = working.get("compatibility") or {}
    if not isinstance(compatibility, dict) or compatibility.get("requires_backward_compatibility") not in {True, False, "unknown"}:
        errors.append("COMP-01 compatibility decision is missing")
        compatibility = {}
    _text(compatibility, "rationale", errors, "COMP-01")
    _refs(compatibility, "source_refs", evidence, errors, "COMP-01")
    if not compatibility.get("affected_surfaces") or not isinstance(compatibility.get("affected_surfaces"), list):
        errors.append("COMP-01 affected surfaces must be examined")
    if compatibility.get("requires_backward_compatibility") is True:
        _refs(compatibility, "obligation_refs", obligations, errors, "COMP-01")
        if not compatibility.get("baseline_refs"):
            errors.append("COMP-01 true compatibility requires a baseline")
    elif compatibility.get("requires_backward_compatibility") == "unknown":
        if compatibility.get("question_ref") not in questions:
            errors.append("COMP-01 unknown compatibility requires an owned question")
        errors.append("COMP-01 unknown compatibility blocks baseline approval")
    elif compatibility.get("obligation_refs"):
        errors.append("COMP-01 false compatibility cannot claim obligations")
    for item in working.get("compatibility_obligations") or []:
        if not isinstance(item, dict):
            continue
        for field, ids in (("fr_refs", fr), ("scenario_refs", uc), ("edge_case_refs", edges), ("design_refs", design), ("verification_refs", acceptance)):
            _refs(item, field, ids, errors, "COMP-01")
        for key in ("baseline_ref", "preserved_behavior", "allowed_change"):
            _text(item, key, errors, "COMP-01")
        if item.get("baseline_ref") not in compatibility.get("baseline_refs", []):
            errors.append("COMP-01 obligation baseline not declared")
    for question in working.get("open_questions") or []:
        if isinstance(question, dict):
            if question.get("status") not in {"open", "resolved"} or not question.get("owner") or not question.get("text"):
                errors.append("PREFLIGHT open question needs owner, text and status")
    tmf_registry = json.loads((package / "taxonomy/tmf-snapshots.json").read_text(encoding="utf-8"))
    exact_bindings = {
        (item["axis"], item["element_type"], item["snapshot_ref"], item["element_id"], item["element_name"], item["source_anchor"])
        for item in tmf_registry.get("approved_bindings", [])
    }
    for binding in working.get("industry_bindings") or []:
        if not isinstance(binding, dict):
            errors.append("TMF-01 industry binding must be an object")
            continue
        _refs(binding, "local_product_binding_refs", bindings, errors, "TMF-01")
        for field in ("tm_forum_binding", "sid_context"):
            axis_binding = binding.get(field) or {}
            status = axis_binding.get("status")
            if field == "sid_context" and status == "escalated-to-sid":
                errors.append("TMF-01 SID context cannot escalate to itself")
            if status == "resolved":
                if not all(axis_binding.get(key) for key in ("element_type", "snapshot_ref", "element_id", "element_name", "source_anchor")) or not binding.get("reviewed_by"):
                    errors.append("TMF-01 resolved binding needs exact versioned ID, anchor and human review")
                elif (field, axis_binding["element_type"], axis_binding["snapshot_ref"], axis_binding["element_id"], axis_binding["element_name"], axis_binding["source_anchor"]) not in exact_bindings:
                    errors.append("TMF-01 exact ID is absent from approved typed snapshot registry")
            elif status in {"unresolved", "not-applicable", "escalated-to-sid"}:
                if axis_binding.get("element_id"):
                    errors.append("TMF-01 unresolved or escalated binding cannot carry a guessed ID")
            else:
                errors.append("TMF-01 invalid binding status")
        if not binding.get("rationale"):
            errors.append("TMF-01 binding rationale is required")
        if (binding.get("tm_forum_binding") or {}).get("status") == "escalated-to-sid" and (binding.get("sid_context") or {}).get("status") == "not-applicable":
            errors.append("TMF-01 escalation requires an applicable SID context")
    approval = working.get("approval") or {}
    semantic = working.get("semantic_review") or {}
    if not isinstance(semantic, dict) or semantic.get("status") != "passed" or not all(semantic.get(key) for key in ("reviewed_by", "rationale", "counterexample")):
        errors.append("SEMANTIC G-semantic review with rationale and counterexample is required")
    if not isinstance(approval, dict) or not approval.get("reviewed_by") or not approval.get("decision_ref"):
        errors.append("BASELINE human approval is required")
    return errors


def compile_release(working: dict, package: Path) -> tuple[dict, dict]:
    errors = validate_working(working, package)
    if errors:
        raise ValueError("; ".join(errors))
    if any(item.get("status") == "open" for item in working["open_questions"]):
        raise ValueError("RELEASE unresolved questions block publication")
    if any(item["target"] == "TBD" for item in working["nfr"]):
        raise ValueError("RELEASE TBD target blocks publication")
    profile = json.loads((package / "contracts/bcreq-client-v1.json").read_text(encoding="utf-8"))
    fragments: list[dict] = []
    def add(section: str, working_id: str, text: str) -> None:
        fragments.append({"fragment_id": f"RF-{len(fragments) + 1:03}", "section": section, "text": text, "working_ids": [working_id]})
    for item in working["terms"]:
        add("1", item["id"], f"{item['term']}: {item['definition']}")
    for item in working["goals"]:
        add("2", item["id"], item["text"])
    for item in working["user_stories"]:
        add("2", item["id"], item["text"])
    boundary = working["boundary"]
    add("2.3", boundary["id"], "In scope: " + "; ".join(boundary["in_scope"]) + ". Out of scope: " + "; ".join(boundary["out_of_scope"]))
    for item in working["deltas"]:
        if item["disposition"] == "change":
            add("2.3", item["id"], item["requested_delta"])
    for item in working["fr"]:
        add("3", item["requirement_id"], item["shall"])
    for item in working["design"]:
        add("4", item["id"], item["text"])
    for item in working["nfr"]:
        add("5", item["requirement_id"], item["text"])
    for item in working["constraints"]:
        add("6", item["id"], item["text"])
    for item in working["uc"]:
        if item.get("release_selected"):
            add("7", item["scenario_id"], item["trigger"] + ": " + "; ".join(item["main_flow"]) + ". Outcome: " + item["outcome"])
    for item in working["compatibility_obligations"]:
        add("7", item["id"], item["preserved_behavior"])
    included_ids = [fragment["working_ids"][0] for fragment in fragments]
    included = set(included_ids)
    entity_keys = {"fr": "requirement_id", "nfr": "requirement_id", "uc": "scenario_id"}
    excluded: list[dict] = []
    for field, policy in profile["entity_policies"].items():
        items = [working["boundary"]] if field == "boundary" else working[field]
        for item in items:
            entity_id = item[entity_keys.get(field, "id")]
            if entity_id in included:
                if policy == "internal_only":
                    raise ValueError(f"RELEASE internal-only entity was published: {entity_id}")
            elif policy == "required":
                raise ValueError(f"RELEASE required entity was omitted: {entity_id}")
            else:
                reason = "not-selected-for-client-profile" if field == "uc" else "not-a-confirmed-change" if field == "deltas" else "internal-working-evidence"
                excluded.append({"id": entity_id, "policy": policy, "reason": reason})
    release = {
        "schema_version": 1,
        "artifact_class": "A-BCREQ",
        "projection": "release",
        "release_id": "REL-" + working["working_baseline_id"].split("-", 1)[1],
        "working_baseline_id": working["working_baseline_id"],
        "release_profile": profile["profile_id"],
        "release_profile_version": profile["version"],
        "audience": profile["audience"],
        "sections": [{"id": section["id"], "heading": section["heading"], "fragments": [f for f in fragments if f["section"] == section["id"]]} for section in profile["sections"]],
    }
    release["release_digest"] = digest(release)
    manifest = {
        "release_id": release["release_id"],
        "working_baseline_id": working["working_baseline_id"],
        "working_digest": working["working_digest"],
        "release_profile": profile["profile_id"],
        "release_profile_version": profile["version"],
        "audience": profile["audience"],
        "included_ids": included_ids,
        "excluded": excluded,
        "fragments": [{"release_fragment": fragment["fragment_id"], "working_ids": fragment["working_ids"]} for fragment in fragments],
        "release_digest": release["release_digest"],
    }
    return release, manifest


def validate_release(working: dict, release: object, manifest: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(release, dict) or not isinstance(manifest, dict):
        return ["RELEASE document and manifest must be objects"]
    package = Path(__file__).resolve().parents[1]
    for value, filename, label in ((release, "c-release-bcreq.schema.json", "Release"), (manifest, "c-release-manifest.schema.json", "Manifest")):
        schema = json.loads((package / "contracts" / filename).read_text(encoding="utf-8"))
        errors.extend(_schema_errors(value, schema, schema, label))
    if errors:
        return errors
    field_ids = (("terms", "id"), ("goals", "id"), ("user_stories", "id"), ("deltas", "id"), ("fr", "requirement_id"), ("design", "id"), ("nfr", "requirement_id"), ("constraints", "id"), ("uc", "scenario_id"), ("compatibility_obligations", "id"))
    working_ids = {item[key] for field, key in field_ids for item in working.get(field, [])}
    working_ids.add(working.get("boundary", {}).get("id"))
    fragments = [fragment for section in release.get("sections", []) for fragment in section.get("fragments", [])]
    fragment_ids = {fragment.get("fragment_id") for fragment in fragments}
    if len(fragment_ids) != len(fragments):
        errors.append("RELEASE-TRACE fragment IDs are not unique")
    manifest_links = manifest.get("fragments") or []
    if {link.get("release_fragment") for link in manifest_links} != fragment_ids or len(manifest_links) != len(fragments):
        errors.append("RELEASE-TRACE manifest must link every fragment exactly once")
    for link in manifest_links:
        refs = link.get("working_ids")
        if not isinstance(refs, list) or not refs or any(ref not in working_ids for ref in refs):
            errors.append("RELEASE-TRACE reverse link points outside approved Working IDs")
    if manifest.get("included_ids") != [fragment.get("working_ids", [None])[0] for fragment in fragments]:
        errors.append("RELEASE-TRACE included IDs differ from fragments")
    if manifest.get("working_digest") != working_digest(working) or manifest.get("working_baseline_id") != working.get("working_baseline_id"):
        errors.append("RELEASE baseline provenance mismatch")
    if release.get("release_digest") != digest({key: value for key, value in release.items() if key != "release_digest"}) or manifest.get("release_digest") != release.get("release_digest"):
        errors.append("RELEASE digest mismatch")
    if release.get("release_id") != manifest.get("release_id") or release.get("release_profile") != manifest.get("release_profile"):
        errors.append("RELEASE profile or ID mismatch")
    fr_ids = {item["requirement_id"] for item in working.get("fr", [])}
    published = set(manifest.get("included_ids") or [])
    for item in working.get("nfr", []):
        if item["requirement_id"] in published and not set(item["applies_to_fr"]).issubset(published & fr_ids):
            errors.append("RELEASE NFR references unpublished FR")
    for item in working.get("constraints", []):
        if item["id"] in published and not set(item["applies_to_fr"]).issubset(published & fr_ids):
            errors.append("RELEASE constraint references unpublished FR")
    try:
        expected_release, expected_manifest = compile_release(working, Path(__file__).resolve().parents[1])
    except (ValueError, KeyError) as error:
        errors.append(f"RELEASE cannot compile from baseline: {error}")
    else:
        if release != expected_release or manifest != expected_manifest:
            errors.append("RELEASE output differs from deterministic approved projection")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("validate-working", "compile", "validate-release"))
    parser.add_argument("working", type=Path)
    parser.add_argument("--release", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    package = Path(__file__).resolve().parents[1]
    working = json.loads(args.working.read_text(encoding="utf-8"))
    if args.action == "validate-working":
        errors = validate_working(working, package)
    elif args.action == "compile":
        try:
            release, manifest = compile_release(working, package)
        except ValueError as error:
            errors = [str(error)]
        else:
            if args.output is None:
                parser.error("compile requires --output")
            args.output.mkdir(parents=True, exist_ok=True)
            (args.output / "release.json").write_bytes(canonical(release) + b"\n")
            (args.output / "release-manifest.json").write_bytes(canonical(manifest) + b"\n")
            errors = []
    else:
        if args.release is None or args.manifest is None:
            parser.error("validate-release requires --release and --manifest")
        release = json.loads(args.release.read_text(encoding="utf-8"))
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        errors = validate_release(working, release, manifest)
    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 1
    print("G-mach: BCREQ accepted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
