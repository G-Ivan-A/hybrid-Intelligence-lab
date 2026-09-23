#!/usr/bin/env python3
"""Compile reviewed MANGO and telecom product taxonomies into runtime YAML.

The reviewed classification remains the evidence-bearing source. This compiler
creates two operational projections and writes byte-identical copies to Source
and Distribution. It intentionally does not infer or enrich any classification.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PROJECT_ROOT = REPOSITORY_ROOT / "projects/ba-ai-process"
CLASSIFICATION = REPOSITORY_ROOT / "research/mango/2026-05-22-classification.md"
SOURCE_TAXONOMY = PROJECT_ROOT / "ba-meta-model/product-taxonomy"
DIST_TAXONOMY = PROJECT_ROOT / "dist/execution-package-gigacode-cli/taxonomy"
SOURCE_REVISION = "3a7306d66011186d42f5017b89a9cc051226fe32"
SOURCE_URL = (
    "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/"
    f"{SOURCE_REVISION}/research/mango/2026-05-22-classification.md"
)
ISSUE_URL = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/601"

STATUS_MAP = {
    "Есть": "present",
    "Есть (сквозной слой)": "present-cross-cutting",
    "Частично": "partial",
    "Не выявлено": "not-observed",
    "Вне SaaS-ядра": "outside-saas-core",
}


def split_values(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_mango(lines: list[str]) -> tuple[list[dict], dict[str, dict]]:
    domains: list[dict] = []
    by_path: dict[str, dict] = {}
    domain: dict | None = None
    capability: dict | None = None
    in_product_layer = False

    for line in lines:
        if line == "## 📊 Product Layer":
            in_product_layer = True
            continue
        if line == "## 🛒 Commercial Layer":
            break
        if not in_product_layer:
            continue

        domain_match = re.fullmatch(r"### 📦 Domain: ([a-z0-9-]+)", line)
        if domain_match:
            domain = {"id": domain_match.group(1), "name": "", "capabilities": []}
            domains.append(domain)
            capability = None
            continue
        if line == "### 🧩 Кросс-доменные возможности (platform)":
            domain = {
                "id": "platform",
                "name": "Кросс-доменные возможности",
                "capabilities": [],
            }
            domains.append(domain)
            capability = None
            continue
        if domain is None:
            continue

        name_match = re.fullmatch(r"\*\*Name\*\*: (.+)", line)
        if name_match and not domain["name"]:
            domain["name"] = name_match.group(1)
            continue

        capability_match = re.fullmatch(
            r"#### 🔹 Capability: ([a-z0-9-]+) \((.+)\)(?: — R[0-9.]+, новый)?",
            line,
        )
        if capability_match:
            capability = {
                "id": capability_match.group(1),
                "name": capability_match.group(2),
                "features": [],
                "atomic_functions": [],
                "related_commercial_fields": [],
            }
            domain["capabilities"].append(capability)
            continue
        if capability is None:
            continue

        if line.startswith("- **Features**: "):
            capability["features"] = split_values(line.removeprefix("- **Features**: "))
            continue
        atomic_match = re.fullmatch(r"  - `([a-z0-9-]+)` \(params: (.+)\)", line)
        if atomic_match:
            capability["atomic_functions"].append(
                {
                    "id": atomic_match.group(1),
                    "parameters": split_values(atomic_match.group(2)),
                }
            )
            continue
        if line.startswith("- **related_commercial_fields**: "):
            capability["related_commercial_fields"] = split_values(
                line.removeprefix("- **related_commercial_fields**: ")
            )
            continue
        status_match = re.fullmatch(r"- \*\*Mango status\*\*: (.+) · \*\*row\*\*: ([0-9]+)", line)
        if status_match:
            source_status = status_match.group(1)
            if source_status not in STATUS_MAP:
                raise ValueError(f"unknown MANGO status: {source_status}")
            capability["status"] = STATUS_MAP[source_status]
            capability["source_row"] = int(status_match.group(2))
            path = f"{domain['id']}/{capability['id']}"
            if path in by_path:
                raise ValueError(f"duplicate MANGO capability: {path}")
            by_path[path] = capability

    if len(domains) != 8 or len(by_path) != 42:
        raise ValueError(f"expected 8 domains and 42 capabilities, got {len(domains)} and {len(by_path)}")
    for item in domains:
        if not item["name"] or not item["capabilities"]:
            raise ValueError(f"incomplete MANGO domain: {item['id']}")
        for entry in item["capabilities"]:
            if not entry["features"] or not entry["atomic_functions"]:
                raise ValueError(f"incomplete MANGO capability: {item['id']}/{entry['id']}")
    return domains, by_path


def parse_industry(lines: list[str], by_path: dict[str, dict]) -> list[dict]:
    mappings: list[dict] = []
    in_table = False
    for line in lines:
        if line == "## Сравнительная таблица международной классификации":
            in_table = True
            continue
        if line == "## Сравнительная таблица к российским стандартам":
            break
        if not in_table or not line.startswith("|"):
            continue
        columns = [item.strip() for item in line.strip().strip("|").split("|")]
        if len(columns) != 7 or not columns[0].isdigit():
            continue
        row = int(columns[0])
        path = columns[2].replace(" → ", "/")
        if path not in by_path:
            raise ValueError(f"industry row {row} references unknown MANGO capability: {path}")
        if by_path[path]["source_row"] != row:
            raise ValueError(f"industry row mismatch for {path}")
        mappings.append(
            {
                "source_row": row,
                "mango_capability": path,
                "product_or_service": columns[1],
                "tm_forum": columns[4],
                "unspsc": columns[5],
                "babok": columns[6],
            }
        )
    if len(mappings) != 42:
        raise ValueError(f"expected 42 industry mappings, got {len(mappings)}")
    return mappings


def provenance() -> dict:
    return {
        "compiled_from": SOURCE_URL,
        "source_revision": SOURCE_REVISION,
        "copied_for": ISSUE_URL,
        "compiled_on": "2026-09-23",
    }


def render_documents() -> dict[str, str]:
    lines = CLASSIFICATION.read_text(encoding="utf-8").splitlines()
    domains, by_path = parse_mango(lines)
    mappings = parse_industry(lines, by_path)

    mango = {
        "generated_by": "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/build/compiler/compile-product-taxonomies.py",
        "taxonomy": "mango-products",
        "closed": True,
        "version": "3.0",
        "scope": "mango-only",
        "provenance": provenance(),
        "levels": ["Domain", "Capability", "Feature", "Atomic Function"],
        "binding_level": "Atomic Function",
        "domains": domains,
    }
    telecom = {
        "generated_by": "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/build/compiler/compile-product-taxonomies.py",
        "taxonomy": "telecom-products",
        "closed": True,
        "version": "3.0",
        "scope": "it-telecom",
        "provenance": provenance(),
        "frameworks": [
            {
                "id": "tm-forum",
                "role": "telecom-domain-and-capability-context",
                "url": "https://www.tmforum.org/oda/",
            },
            {
                "id": "unspsc",
                "role": "international-product-and-service-classification",
                "url": "https://www.ungm.org/Public/UNSPSC",
            },
            {
                "id": "babok-v3",
                "role": "business-analysis-perspective",
                "url": "https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/",
            },
        ],
        "mappings": mappings,
    }

    return {
        "mango-products.yaml": json.dumps(mango, ensure_ascii=False, indent=2) + "\n",
        "telecom-products.yaml": json.dumps(telecom, ensure_ascii=False, indent=2) + "\n",
    }


def check(outputs: dict[str, str]) -> int:
    errors: list[str] = []
    for filename, expected in outputs.items():
        for root in (SOURCE_TAXONOMY, DIST_TAXONOMY):
            path = root / filename
            if not path.is_file():
                errors.append(f"missing generated taxonomy: {path.relative_to(REPOSITORY_ROOT)}")
            elif path.read_text(encoding="utf-8") != expected:
                errors.append(f"generated taxonomy drift: {path.relative_to(REPOSITORY_ROOT)}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Product taxonomy compilation check passed (2 Source snapshots + 2 Distribution copies).")
    return 0


def write(outputs: dict[str, str]) -> None:
    SOURCE_TAXONOMY.mkdir(parents=True, exist_ok=True)
    DIST_TAXONOMY.mkdir(parents=True, exist_ok=True)
    for filename, content in outputs.items():
        (SOURCE_TAXONOMY / filename).write_text(content, encoding="utf-8")
        (DIST_TAXONOMY / filename).write_text(content, encoding="utf-8")
    print("Compiled 2 Source product taxonomies and 2 byte-identical Distribution copies.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = render_documents()
    if args.check:
        return check(outputs)
    write(outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
