"""Shared A-IN builder for the issue #638 GigaCode experiments."""
import hashlib, json


def a_in(task: str, confirmed: bool) -> dict:
    products = [{"marker": "A", "domain": "platform", "capability": "platform-integration",
                 "feature": "crm-connectors", "atomic_function": "crm-bidirectional-sync",
                 "profile": "P-API", "owner": "platform-owner"}]
    digest = hashlib.sha256(json.dumps(products, ensure_ascii=False, sort_keys=True,
                                       separators=(",", ":")).encode()).hexdigest()
    return {"artifact_class": "A-IN", "state": "raw",
            "task": {"id": task, "title": "Smoke", "requested_by": "analyst"},
            "work_type": "mango-change",
            "routing": {"primary_axis": "mango", "rule": "mango-change",
                        "decision": "confirmed" if confirmed else "pending",
                        "decision_ref": "evidence/checkpoint-n0.md"},
            "products": products,
            "product_attribution": ({"status": "confirmed", "confirmed_by": "analyst",
                                     "confirmed_at": "2026-09-29T12:00:00Z",
                                     "decision_ref": "evidence/checkpoint-n0.md",
                                     "binding_digest": "sha256:" + digest}
                                    if confirmed else {"status": "pending"}),
            "sources": [{"id": "SRC-01", "kind": "transcript", "tier": "ST-1-ATTACHED",
                         "locator": "smoke", "content": "smoke"}],
            "language": "ru"}
