#!/usr/bin/env python3
"""Scan Analysis-adjacent artifacts for issue #342.

The scan is intentionally heuristic. It classifies the requested corpus by
actual artifact role, then the written analysis document performs the final
interpretation and modernization recommendations.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path


SCAN_DATE = date(2026, 7, 2).isoformat()
TEXT_EXTENSIONS = {".md", ".markdown", ".txt", ".html"}
SELF_PATHS = {
    "docs/analysis/2026-07-02-analysis-artifacts-inventory.md",
}
SELF_PREFIXES = (
    "research/hub/exp/analysis-inventory-342/",
)


@dataclass(frozen=True)
class RepoSpec:
    key: str
    label: str
    root: Path
    url: str


def run_git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True)


def tracked_files(root: Path) -> list[str]:
    return [line for line in run_git(root, "ls-files").splitlines() if line.strip()]


def repo_sha(root: Path) -> str:
    return run_git(root, "rev-parse", "HEAD").strip()


def in_scope(path: str) -> bool:
    if path in SELF_PATHS or path.startswith(SELF_PREFIXES):
        return False

    return path.startswith(
        (
            "docs/analysis/",
            "docs/report/",
            "docs/reports/",
            "docs/audit/",
            "research/",
            "governance/",
        )
    )


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    fields: dict[str, str] = {}
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            return fields
        if not stripped or stripped.startswith("#") or ":" not in line:
            continue
        if line.startswith((" ", "\t", "-")):
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip("'\"")
    return {}


def first_heading(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def has_any(blob: str, terms: tuple[str, ...]) -> bool:
    return any(term in blob for term in terms)


def current_bucket(path: str) -> str:
    for prefix in (
        "docs/analysis/",
        "docs/report/",
        "docs/reports/",
        "docs/audit/",
        "governance/rfc/",
        "governance/",
        "research/",
    ):
        if path.startswith(prefix):
            return prefix.rstrip("/")
    return path.split("/", 1)[0]


def is_rfc_signal(lower_path: str, lower_title: str, lower_type: str) -> bool:
    return (
        lower_type in {"rfc", "proposal", "proposed"}
        or lower_title.startswith(("rfc:", "proposal:", "предложение:"))
        or re.search(r"(^|/)\d{4}-\d{2}-\d{2}-rfc-", lower_path) is not None
        or re.search(r"(^|/)rfc[-_/]", lower_path) is not None
    )


def is_audit_signal(lower_path: str, lower_title: str, lower_type: str, signal: str) -> bool:
    name = Path(lower_path).name
    if lower_path.startswith("docs/audit/"):
        return True
    if "research-analysis-audit" in lower_path:
        return False
    if lower_type in {"audit", "convergence-test", "validation-note"}:
        return True
    if lower_title.startswith(("audit:", "аудит")):
        return True
    if re.search(r"(^|[-_/])audit($|[-_/\\.])", name) is not None:
        return True
    return has_any(
        signal,
        (
            "verification",
            "верификац",
            "validation",
            "валид",
            "conformance",
            "compliance",
            "contract-test",
            "approval-contract-test",
            "convergence-test",
            "сходимост",
            "smoke",
            "e2e",
            "triage",
            "code-review",
            "human-review",
            "post-implementation",
        ),
    )


def is_research_signal(signal: str, content_sample: str) -> bool:
    return has_any(
        signal + " " + content_sample[:1600],
        (
            "research",
            "исследован",
            "industry",
            "market",
            "external",
            "source-backed",
            "international",
            "benchmark",
            "variants",
            "вариант",
            "hypothesis",
            "гипотез",
            "norms",
            "standardization-scope",
            "knowledge-generation",
            "empirical",
            "эмпир",
        ),
    )


def classify(path: str, fields: dict[str, str], title: str, text: str) -> tuple[str, str, str]:
    lower_path = path.lower()
    name = Path(path).name.lower()
    lower_title = title.lower()
    lower_type = fields.get("type", "").lower()
    lower_status = fields.get("status", "").lower()
    signal = " ".join((lower_path, lower_title, lower_type, lower_status))
    content_sample = text[:6000].lower()

    if name == ".gitkeep":
        return "Other", "structure-placeholder", "placeholder file, not a knowledge artifact"

    if name == "readme.md":
        return "Other", "navigation", "README/navigation file"

    if lower_path.startswith(("docs/adr/", "governance/adr/")) or "/adr/" in lower_path:
        return "ADR", "decision-record", "ADR/decision record"

    if lower_path.startswith(("docs/report/", "docs/reports/")):
        return "Report", "report-location", "report path with no stronger contrary signal"

    if lower_path.startswith(("governance/rfc/", "docs/rfc/")):
        return "RFC", "proposal", "RFC/proposal path"

    if lower_path.startswith("research/") and lower_type.endswith("-research"):
        return "Research", "knowledge-generation", "frontmatter marks a research artifact"

    if is_rfc_signal(lower_path, lower_title, lower_type):
        return "RFC", "proposal", "frontmatter, title, or path marks a proposal/RFC"

    if is_audit_signal(lower_path, lower_title, lower_type, signal):
        return "Audit", "conformance-check", "checks state against a norm, contract, checklist, or expected behavior"

    if lower_path.startswith("docs/audit/"):
        return "Audit", "audit-location", "audit path with no stronger contrary signal"

    if lower_path.startswith("docs/analysis/"):
        if has_any(signal, ("execution-report", "sprint", "kickoff", "report_template", "отчет", "отчёт")):
            return "Report", "analysis-path-report", "descriptive execution/report artifact under docs/analysis"
        if lower_type in {"research-inventory"} or has_any(
            signal,
            (
                "artifact-chain-hypothesis-research",
                "runs-observability-research",
                "telecom-vendors",
                "ba-processes-industry",
                "industry-inventory",
            ),
        ):
            return "Research", "knowledge-generation", "docs/analysis artifact generates external or hypothesis-driven knowledge"
        return "Analysis", "local-context-analysis", "docs/analysis artifact examines local/internal context without a conformance-check stance"

    if lower_path.startswith("governance/") and not lower_path.startswith("governance/rfc/"):
        if has_any(signal, ("session-digests", "sync-matrix", "digest", "matrix", "summary", "report")):
            return "Report", "governance-report", "governance log, matrix, digest, or report"
        if is_rfc_signal(lower_path, lower_title, lower_type):
            return "RFC", "proposal", "governance proposal outside the RFC directory"
        return "Other", "reference-or-governance", "governance reference, contract, policy, registry, or planning artifact"

    if lower_path.startswith("research/") and has_any(
        signal,
        (
            "retrospective",
            "ретроспектив",
            "summary",
            "сводк",
            "executive-summary",
            "run.log",
            "test1-",
            "test2-",
            "test3-",
            "test4-",
            "test5-",
        ),
    ):
        return "Report", "research-evidence-report", "report-like evidence or summary inside research corpus"

    if lower_path.startswith("research/") and lower_type == "internal-analysis":
        return "Analysis", "local-context-analysis", "research-path document explicitly marked internal analysis"

    if lower_path.startswith("research/") and "analysis" in name and not is_research_signal(signal, content_sample):
        return "Analysis", "analysis-under-research", "analysis-named local-context artifact under research"

    if lower_path.startswith("research/") or lower_type == "external-analysis" or is_research_signal(signal, content_sample):
        return "Research", "knowledge-generation", "generates or compares knowledge, hypotheses, variants, or evidence beyond one local state"

    analysis_signals = (
        "analysis",
        "анализ",
        "internal-analysis",
        "inventory",
        "инвентар",
        "matrix",
        "roadmap",
        "comparison",
        "сравнен",
        "local",
        "repo-state",
        "context",
        "контекст",
        "mapping",
        "classification",
        "классификац",
    )
    if lower_path.startswith("docs/analysis/") or has_any(signal, analysis_signals):
        return "Analysis", "local-context-analysis", "examines local/internal context without a conformance-check stance"

    if has_any(
        signal,
        (
            "digest",
            "summary",
            "report",
            "отчет",
            "отчёт",
            "log",
        ),
    ):
        return "Report", "general-report", "descriptive report/log/summary artifact"

    if has_any(
        signal,
        (
            "standard",
            "template",
            "contract",
            "policy",
            "manifest",
            "registry",
            "backlog",
            "map",
            "protocol",
            "process",
            "prompt",
            "guide",
        ),
    ):
        return "Other", "reference-or-governance", "reference, contract, policy, template, registry, or planning artifact"

    return "Other", "unclassified", "no strong Analysis/Research/Audit/Report/RFC/ADR signal"


def relation_to_analysis(path: str, actual_type: str) -> str:
    in_analysis_path = path.startswith("docs/analysis/")
    analysis_named = "analysis" in Path(path).name.lower()

    if actual_type == "Analysis":
        return "actual-analysis" if in_analysis_path else "analysis-outside-analysis-path"
    if in_analysis_path:
        return f"masked-{actual_type.lower()}-in-analysis-path"
    if analysis_named:
        return f"analysis-named-{actual_type.lower()}"
    return "adjacent-not-analysis"


def canonical_hint(path: str, actual_type: str, relation: str) -> str:
    if actual_type == "Analysis":
        if path.startswith("docs/analysis/"):
            return "already in target Analysis path; future standard should modernize metadata/sections"
        return "candidate for docs/analysis or explicit Analysis metadata after standard"
    if actual_type == "Research":
        return "keep under Research routing unless future Analysis standard cites it as upstream evidence"
    if actual_type == "Audit":
        return "route by future Audit standard; do not absorb into Analysis"
    if actual_type == "Report":
        return "route by Reports standard / docs/report profile, not Analysis"
    if actual_type == "RFC":
        return "keep as proposal/RFC; Analysis can cite it as downstream or upstream context"
    if actual_type == "ADR":
        return "keep as decision record; not an Analysis candidate"
    return "no B-028 move candidate unless a future standard names it"


def artifact_record(repo: RepoSpec, path: str) -> dict:
    file_path = repo.root / path
    extension = file_path.suffix.lower()
    text_like = extension in TEXT_EXTENSIONS

    fields: dict[str, str] = {}
    title = ""
    line_count = None
    if text_like and file_path.is_file():
        text = read_text(file_path)
        fields = parse_frontmatter(text)
        title = first_heading(text)
        line_count = len(text.splitlines())
    else:
        text = ""

    actual_type, subtype, rationale = (
        classify(path, fields, title, text)
        if text_like
        else ("Other", "non-text", "non-text artifact")
    )
    relation = relation_to_analysis(path, actual_type)

    return {
        "repo": repo.key,
        "repo_label": repo.label,
        "path": path,
        "current_bucket": current_bucket(path),
        "extension": extension or "[none]",
        "text_like": text_like,
        "title": title,
        "frontmatter_type": fields.get("type", ""),
        "frontmatter_status": fields.get("status", ""),
        "actual_type": actual_type,
        "subtype": subtype,
        "relation_to_analysis": relation,
        "canonical_hint": canonical_hint(path, actual_type, relation),
        "rationale": rationale,
        "line_count": line_count,
    }


def md_escape(value: object) -> str:
    text = str(value) if value not in {None, ""} else "-"
    return text.replace("|", "\\|").replace("\n", " ")


def markdown_matrix(records: list[dict], repo_meta: dict[str, dict]) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        grouped[record["repo"]].append(record)

    lines = [
        "---",
        "status: draft",
        "version: 0.1",
        f"updated: {SCAN_DATE}",
        "temperature: 0.1",
        "---",
        "",
        "# Analysis artifact candidate matrix",
        "",
        "Generated for issue #342. Classification is heuristic and evidence-oriented:",
        "the requested corpus is scanned by path, then path, filename, title,",
        "frontmatter and early content signals classify each text artifact by actual",
        "role: Research / Analysis / Audit / Report / RFC / ADR / Other. The written",
        "analysis document performs the final synthesis and recommendations.",
        "",
        "## Repository snapshots",
        "",
        "| Repo | URL | SHA |",
        "| --- | --- | --- |",
    ]

    for key in ("hub", "mango", "clarify"):
        meta = repo_meta[key]
        lines.append(f"| {meta['label']} | {meta['url']} | `{meta['sha']}` |")

    lines.extend(
        [
            "",
            "## Summary by actual type",
            "",
            "| Repo | Scanned text | Research | Analysis | Audit | Report | RFC | ADR | Other | Non-text |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    actual_types = ("Research", "Analysis", "Audit", "Report", "RFC", "ADR", "Other")
    for key in ("hub", "mango", "clarify"):
        repo_records = grouped[key]
        text_records = [record for record in repo_records if record["text_like"]]
        counts = Counter(record["actual_type"] for record in text_records)
        non_text = sum(1 for record in repo_records if not record["text_like"])
        count_cells = " | ".join(str(counts[item]) for item in actual_types)
        lines.append(
            f"| {repo_meta[key]['label']} | {len(text_records)} | {count_cells} | {non_text} |"
        )

    lines.extend(
        [
            "",
            "## Analysis relation summary",
            "",
            "| Repo | Relation | Count |",
            "| --- | --- | ---: |",
        ]
    )
    for key in ("hub", "mango", "clarify"):
        text_records = [record for record in grouped[key] if record["text_like"]]
        relation_counts = Counter(record["relation_to_analysis"] for record in text_records)
        for relation, count in sorted(relation_counts.items()):
            lines.append(f"| {repo_meta[key]['label']} | `{relation}` | {count} |")

    lines.extend(
        [
            "",
            "## Current path buckets",
            "",
            "| Repo | Bucket | Text artifacts | Research | Analysis | Audit | Report | RFC | Other |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for key in ("hub", "mango", "clarify"):
        text_records = [record for record in grouped[key] if record["text_like"]]
        buckets: dict[str, list[dict]] = defaultdict(list)
        for record in text_records:
            buckets[record["current_bucket"]].append(record)
        for bucket_name in sorted(buckets):
            bucket_records = buckets[bucket_name]
            counts = Counter(record["actual_type"] for record in bucket_records)
            lines.append(
                f"| {repo_meta[key]['label']} | `{bucket_name}` | {len(bucket_records)} | "
                f"{counts['Research']} | {counts['Analysis']} | {counts['Audit']} | "
                f"{counts['Report']} | {counts['RFC']} | {counts['Other']} |"
            )

    masked = [
        record
        for record in records
        if record["text_like"] and str(record["relation_to_analysis"]).startswith("masked-")
    ]
    lines.extend(
        [
            "",
            "## Masked artifacts in `docs/analysis/`",
            "",
            "| Repo | Path | Actual type | Subtype | Rationale |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for record in sorted(masked, key=lambda item: (item["repo"], item["path"])):
        lines.append(
            f"| {record['repo_label']} | `{record['path']}` | {record['actual_type']} | "
            f"{record['subtype']} | {md_escape(record['rationale'])} |"
        )

    for key in ("hub", "mango", "clarify"):
        lines.extend(
            [
                "",
                f"## {repo_meta[key]['label']}",
                "",
                "| Path | Bucket | Actual type | Relation | Hint | Title |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for record in sorted(grouped[key], key=lambda item: item["path"]):
            if not record["text_like"]:
                continue
            lines.append(
                f"| `{record['path']}` | `{record['current_bucket']}` | "
                f"{record['actual_type']} | `{record['relation_to_analysis']}` | "
                f"{md_escape(record['canonical_hint'])} | {md_escape(record['title'])} |"
            )

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub-root", default=".", help="Path to hybrid-Intelligence-lab checkout")
    parser.add_argument("--mango-root", required=True, help="Path to mango_ba_prompts checkout")
    parser.add_argument("--clarify-root", required=True, help="Path to clarify-engine-ai checkout")
    parser.add_argument(
        "--out-dir",
        default="research/hub/exp/analysis-inventory-342",
        help="Output directory relative to hub root unless absolute",
    )
    args = parser.parse_args()

    hub_root = Path(args.hub_root).resolve()
    specs = [
        RepoSpec(
            "hub",
            "Hub / hybrid-Intelligence-lab",
            hub_root,
            "https://github.com/G-Ivan-A/hybrid-Intelligence-lab",
        ),
        RepoSpec(
            "mango",
            "Mango / mango_ba_prompts",
            Path(args.mango_root).resolve(),
            "https://github.com/G-Ivan-A/mango_ba_prompts",
        ),
        RepoSpec(
            "clarify",
            "Clarify / clarify-engine-ai",
            Path(args.clarify_root).resolve(),
            "https://github.com/G-Ivan-A/clarify-engine-ai",
        ),
    ]

    records: list[dict] = []
    repo_meta: dict[str, dict] = {}
    for spec in specs:
        repo_meta[spec.key] = {
            "label": spec.label,
            "root": str(spec.root),
            "url": spec.url,
            "sha": repo_sha(spec.root),
        }
        for path in tracked_files(spec.root):
            if in_scope(path):
                records.append(artifact_record(spec, path))

    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = hub_root / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "scan_date": SCAN_DATE,
        "scope": [
            "docs/analysis/**",
            "docs/report/**",
            "docs/reports/**",
            "docs/audit/**",
            "research/**",
            "governance/**",
        ],
        "repo_meta": repo_meta,
        "records": records,
    }
    (out_dir / "analysis-inventory.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out_dir / "2026-07-02-analysis-artifact-matrix.md").write_text(
        markdown_matrix(records, repo_meta),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
