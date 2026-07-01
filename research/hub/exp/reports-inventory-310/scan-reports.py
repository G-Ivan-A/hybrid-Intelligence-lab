#!/usr/bin/env python3
"""Scan report-like artifacts for issue #310.

The scan is intentionally heuristic. It identifies report-like candidates by
path, title and frontmatter, then the written analysis document performs the
final interpretation.
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


SCAN_DATE = date(2026, 7, 1).isoformat()
TEXT_EXTENSIONS = {".md", ".markdown", ".txt", ".html"}
SELF_PATHS = {
    "docs/analysis/2026-07-01-reports-artifacts-inventory.md",
}
SELF_PREFIXES = (
    "research/hub/exp/reports-inventory-310/",
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

    return path.startswith(("reports/", "docs/", "research/", "governance/"))


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


def bucket(path: str) -> str:
    if path.startswith("reports/"):
        return "reports"
    for prefix in (
        "docs/report/",
        "docs/reports/",
        "docs/analysis/",
        "docs/audit/",
        "docs/reviews/",
        "docs/project-summaries/",
        "governance/rfc/",
        "research/",
        "governance/",
    ):
        if path.startswith(prefix):
            return prefix.rstrip("/")
    return path.split("/", 1)[0]


def classify_report(path: str, fields: dict[str, str], title: str, text: str) -> dict[str, str | bool]:
    lower_path = path.lower()
    name = Path(path).name.lower()
    source_signal = " ".join(
        (
            lower_path,
            title.lower(),
            fields.get("type", "").lower(),
            fields.get("status", "").lower(),
        )
    )
    name_title_type = " ".join((name, title.lower(), fields.get("type", "").lower()))

    if name == "readme.md":
        return {
            "is_report_candidate": False,
            "subtype": "navigation",
            "relation": "not-report",
            "confidence": "high",
            "rationale": "README/navigation artifact.",
        }

    if lower_path.startswith(("docs/adr/", "governance/rfc/")) or "/adr/" in lower_path:
        return {
            "is_report_candidate": False,
            "subtype": "decision-or-proposal",
            "relation": "not-report",
            "confidence": "high",
            "rationale": "Decision/proposal artifact, not a Report candidate.",
        }

    proposal_named = (
        title.lower().startswith(("rfc:", "proposal:", "предложение:"))
        or fields.get("type", "").lower() in {"rfc", "proposal", "proposed"}
        or re.search(r"(^|/)\d{4}-\d{2}-\d{2}-rfc-", lower_path) is not None
        or re.search(r"(^|/)rfc[-_/]", lower_path) is not None
    )
    if proposal_named:
        return {
            "is_report_candidate": False,
            "subtype": "decision-or-proposal",
            "relation": "not-report",
            "confidence": "high",
            "rationale": "RFC/proposal artifact, not a Report candidate.",
        }

    if lower_path.startswith("standards/") or "/standards/" in lower_path:
        return {
            "is_report_candidate": False,
            "subtype": "standard",
            "relation": "not-report",
            "confidence": "high",
            "rationale": "Standard/reference artifact, not a Report candidate.",
        }

    if lower_path.startswith("docs/backlog/") or "backlog" in name_title_type:
        return {
            "is_report_candidate": False,
            "subtype": "planning",
            "relation": "not-report",
            "confidence": "high",
            "rationale": "Backlog/planning artifact, not a Report candidate.",
        }

    if "template" in name_title_type:
        return {
            "is_report_candidate": False,
            "subtype": "template",
            "relation": "not-report",
            "confidence": "high",
            "rationale": "Template artifact, not an existing Report candidate.",
        }

    if "validator" in name_title_type and not lower_path.startswith(("reports/", "docs/report/", "docs/reports/")):
        return {
            "is_report_candidate": False,
            "subtype": "validator",
            "relation": "not-report",
            "confidence": "high",
            "rationale": "Validator/tooling documentation, not a Report candidate.",
        }

    if "reports-industry-norms-and-standardization-scope" in lower_path:
        return {
            "is_report_candidate": False,
            "subtype": "research",
            "relation": "not-report",
            "confidence": "high",
            "rationale": "Reports standardization research is context for issue #310, not a Report artifact candidate.",
        }

    report_path = lower_path.startswith(("reports/", "docs/report/", "docs/reports/"))
    project_summary_path = lower_path.startswith("docs/project-summaries/")
    audit_terms = (
        "audit",
        "аудит",
        "verification",
        "верификац",
        "validation",
        "валид",
        "conformance",
        "compliance",
        "smoke",
        "e2e",
        "post-implementation",
        "consistency",
        "contract-test",
        "approval-contract-test",
        "human-review",
        "code-review",
        "сходимост",
        "convergence-test",
    )
    statistics_terms = (
        "statistics",
        "statistic",
        "stats",
        "metrics",
        "metric",
        "метрик",
        "статистик",
        "dashboard",
        "scan",
        "matrix",
        "inventory",
        "инвентар",
        "counts",
        "classification matrix",
        "frontmatter-scan",
        "tree-summary",
    )
    report_terms = (
        "отчет",
        "отчёт",
        "summary",
        "сводк",
        "execution-report",
        "-report",
        "_report",
        " report",
        "self-report",
        "retrospective",
        "ретроспектив",
        "hypothesis-analysis",
        "context-summary",
        "project summary",
        "digest",
    )

    if project_summary_path:
        return {
            "is_report_candidate": True,
            "subtype": "report",
            "relation": "standalone-report",
            "confidence": "high",
            "rationale": "Project summary is a standalone context report.",
        }

    audit_signal = lower_path.startswith("docs/audit/") or has_any(name_title_type, audit_terms)
    statistics_signal = has_any(name_title_type, statistics_terms)
    report_signal = report_path or has_any(name_title_type, report_terms)

    if not (report_path or audit_signal or statistics_signal or report_signal):
        return {
            "is_report_candidate": False,
            "subtype": "not-report",
            "relation": "not-report",
            "confidence": "medium",
            "rationale": "No report/audit/statistics signal in path, title or frontmatter.",
        }

    if lower_path.startswith("docs/audit/"):
        subtype = "audit"
        relation = "output-for-audit"
        rationale = "Audit/verification/compliance signal: report-like output of an audit or validation process."
    elif statistics_signal:
        subtype = "statistics"
        relation = "output-for-analysis"
        rationale = "Inventory, scan, matrix, metrics or registry signal: report-like statistical output."
    elif audit_signal:
        subtype = "audit"
        relation = "output-for-audit"
        rationale = "Audit/verification/compliance signal: report-like output of an audit or validation process."
    else:
        subtype = "report"
        relation = "standalone-report"
        rationale = "General report/summary/retrospective signal."

    if lower_path.startswith("docs/analysis/") and relation == "standalone-report":
        relation = "output-for-analysis"
        rationale = "General report signal inside docs/analysis: likely output of local analysis/execution work."
    elif lower_path.startswith("research/") and (
        relation == "standalone-report" or statistics_signal
    ):
        relation = "output-for-analysis"
        rationale = "Report-like signal inside research corpus: output/evidence for analysis or research."
    elif lower_path.startswith("docs/project-summaries/"):
        relation = "standalone-report"
        rationale = "Project summary is a standalone context report."

    confidence = "high" if report_path or lower_path.startswith("docs/audit/") else "medium"

    return {
        "is_report_candidate": True,
        "subtype": subtype,
        "relation": relation,
        "confidence": confidence,
        "rationale": rationale,
    }


def canonical_hint(path: str, subtype: str, relation: str) -> str:
    if path.startswith("docs/report/"):
        return "already canonical docs/report path"
    if path.startswith(("docs/reports/", "reports/")):
        return "noncanonical report-like path; target docs/report"
    if relation == "output-for-audit":
        return "future Report/Audit boundary decision before moving"
    if subtype == "statistics":
        return "candidate for docs/report statistics profile after standard"
    return "candidate for docs/report general report profile after standard"


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

    classification = classify_report(path, fields, title, text) if text_like else {
        "is_report_candidate": False,
        "subtype": "non-text",
        "relation": "not-report",
        "confidence": "high",
        "rationale": "Non-text artifact.",
    }

    return {
        "repo": repo.key,
        "repo_label": repo.label,
        "path": path,
        "bucket": bucket(path),
        "extension": extension or "[none]",
        "text_like": text_like,
        "title": title,
        "frontmatter_type": fields.get("type", ""),
        "frontmatter_status": fields.get("status", ""),
        "line_count": line_count,
        **classification,
        "canonical_hint": canonical_hint(
            path,
            str(classification["subtype"]),
            str(classification["relation"]),
        ),
    }


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
        "# Reports artifact candidate matrix",
        "",
        "Generated for issue #310. Classification is heuristic and evidence-oriented:",
        "path is only a signal; title and frontmatter are used to detect",
        "audit, general report and statistical report candidates. The written analysis",
        "document performs the final human-readable synthesis and recommendations.",
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
            "## Summary",
            "",
            "| Repo | Scanned text | Candidates | Audit | Report | Statistics | Output for audit | Output for analysis | Standalone |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for key in ("hub", "mango", "clarify"):
        repo_records = grouped[key]
        text_records = [record for record in repo_records if record["text_like"]]
        candidates = [record for record in text_records if record["is_report_candidate"]]
        subtype_counts = Counter(record["subtype"] for record in candidates)
        relation_counts = Counter(record["relation"] for record in candidates)
        lines.append(
            f"| {repo_meta[key]['label']} | {len(text_records)} | {len(candidates)} | "
            f"{subtype_counts['audit']} | {subtype_counts['report']} | {subtype_counts['statistics']} | "
            f"{relation_counts['output-for-audit']} | {relation_counts['output-for-analysis']} | "
            f"{relation_counts['standalone-report']} |"
        )

    lines.extend(
        [
            "",
            "## Current Path Buckets",
            "",
            "| Repo | Bucket | Candidates |",
            "| --- | --- | ---: |",
        ]
    )
    for key in ("hub", "mango", "clarify"):
        candidates = [
            record for record in grouped[key]
            if record["text_like"] and record["is_report_candidate"]
        ]
        bucket_counts = Counter(record["bucket"] for record in candidates)
        for bucket_name, count in sorted(bucket_counts.items()):
            lines.append(f"| {repo_meta[key]['label']} | `{bucket_name}` | {count} |")

    for key in ("hub", "mango", "clarify"):
        lines.extend(
            [
                "",
                f"## {repo_meta[key]['label']}",
                "",
                "| Path | Bucket | Subtype | Relation | Hint | Title |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        candidates = [
            record for record in grouped[key]
            if record["text_like"] and record["is_report_candidate"]
        ]
        for record in sorted(candidates, key=lambda item: item["path"]):
            title = str(record["title"]).replace("|", "\\|") or "-"
            lines.append(
                f"| `{record['path']}` | `{record['bucket']}` | {record['subtype']} | "
                f"{record['relation']} | {record['canonical_hint']} | {title} |"
            )

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub-root", default=".", help="Path to hybrid-Intelligence-lab checkout")
    parser.add_argument("--mango-root", required=True, help="Path to mango_ba_prompts checkout")
    parser.add_argument("--clarify-root", required=True, help="Path to clarify-engine-ai checkout")
    parser.add_argument(
        "--out-dir",
        default="research/hub/exp/reports-inventory-310",
        help="Output directory relative to hub root unless absolute",
    )
    args = parser.parse_args()

    hub_root = Path(args.hub_root).resolve()
    specs = [
        RepoSpec("hub", "Hub / hybrid-Intelligence-lab", hub_root, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab"),
        RepoSpec("mango", "Mango / mango_ba_prompts", Path(args.mango_root).resolve(), "https://github.com/G-Ivan-A/mango_ba_prompts"),
        RepoSpec("clarify", "Clarify / clarify-engine-ai", Path(args.clarify_root).resolve(), "https://github.com/G-Ivan-A/clarify-engine-ai"),
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
            "reports/**",
            "docs/report*/**",
            "docs/analysis/**",
            "docs/audit/**",
            "docs/reviews/**",
            "docs/project-summaries/**",
            "research/**",
            "governance/**",
        ],
        "repo_meta": repo_meta,
        "records": records,
    }
    (out_dir / "reports-inventory.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out_dir / "2026-07-01-reports-artifact-matrix.md").write_text(
        markdown_matrix(records, repo_meta),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
