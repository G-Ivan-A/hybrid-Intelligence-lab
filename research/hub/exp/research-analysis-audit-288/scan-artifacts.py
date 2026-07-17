#!/usr/bin/env python3
"""Scan Research/Analysis/Audit candidate artifacts for issue #288."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path


SCAN_DATE = date(2026, 6, 28).isoformat()
HUB_BASELINE_SHA = "1a2a9cdfb37ab7e689b143d94623923ade65e33a"
TEXT_EXTENSIONS = {".md", ".markdown", ".html", ".txt"}
SELF_PATHS = {
    "research/hub/2026-06-28-research-analysis-audit-inventory.md",
}
SELF_PREFIXES = (
    "research/hub/exp/research-analysis-audit-288/",
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
    return path == "research/README.md" or path.startswith(("research/", "docs/"))


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


def classify(path: str, fields: dict[str, str], title: str, text: str) -> tuple[str, str, str]:
    lower_path = path.lower()
    lower_title = title.lower()
    lower_type = fields.get("type", "").lower()
    name = Path(path).name.lower()
    signal = " ".join((lower_path, lower_title, lower_type))
    content_sample = text[:4000].lower()

    proposal_named = (
        lower_title.startswith(("rfc:", "proposal:", "предложение:"))
        or lower_type in {"rfc", "proposed", "proposal"}
        or re.search(r"(^|/)\d{4}-\d{2}-\d{2}-rfc-", lower_path) is not None
        or re.search(r"(^|/)rfc[-_/]", lower_path) is not None
    )

    if name in {".gitkeep"}:
        return "Other", "structure-placeholder", "placeholder file, not a knowledge artifact"

    if lower_path.startswith("docs/adr/") or "/adr/" in lower_path:
        return "Other", "decision-record", "ADR/decision record rather than Research/Analysis/Audit"

    if "decision-record" in lower_type:
        return "Other", "decision-record", "decision record rather than Research/Analysis/Audit"

    if (
        "/standards/" in lower_path
        or lower_path.startswith("standards/")
        or "classification-standard" in lower_type
        or re.search(r"(^|[-_/])standard($|[-_/])", lower_path) is not None
    ):
        return "Other", "standard", "standard/reference material rather than R/A/A"

    if name == "readme.md":
        return "Other", "navigation", "README/navigation file rather than a standalone R/A/A artifact"

    if "/screenshots/" in lower_path:
        return "Other", "visual-evidence", "screenshot evidence, not a standalone R/A/A document"

    if "/user_guide/" in lower_path or "/runbooks/" in lower_path or "/guides/" in lower_path:
        return "Other", "guide", "guide/runbook material rather than R/A/A"

    if "/backlog/" in lower_path or "backlog" in lower_title:
        return "Other", "planning", "backlog/planning artifact rather than R/A/A"

    if lower_path.startswith("docs/") and not lower_path.startswith(
        ("docs/analysis/", "docs/audit/", "docs/research/", "docs/reviews/")
    ) and has_any(
        signal,
        (
            "concept",
            "концепц",
            "vision",
            "ecosystem-map",
            "taxonomy",
            "crosswalk",
            "reference",
            "template",
        ),
    ):
        return "Other", "reference-or-concept", "product, taxonomy, concept, or template documentation"

    if proposal_named:
        if "research" in lower_type or (
            lower_path.startswith("research/")
            and (
                has_any(content_sample[:800], ("режим", "research", "исследован"))
                or has_any(signal, ("external-tree-summary", "source tree summary"))
            )
        ):
            return "Research", "proposal-adjacent-research", "research document preparing future RFC/ADR decisions"
        return "Other", "proposal", "RFC/proposal artifact, not one of the three target artifact types"

    if has_any(
        signal,
        (
            "аудит",
            "audit",
            "verification",
            "верификац",
            "проверка",
            "validation",
            "валид",
            "conformance",
            "compliance",
            "consistency",
            "discrepanc",
            "smoke",
            "triage",
            "convergence-test",
            "contract-test",
            "post-implementation",
            "human-review",
        ),
    ):
        return "Audit", "conformance-check", "checks state against a norm, contract, checklist, or expected behavior"

    if lower_path.startswith("docs/audit/"):
        return "Audit", "audit-location", "audit location with no stronger contrary signal"

    if lower_path.startswith("docs/project-summaries/") or (
        lower_path.startswith("docs/analysis/") and has_any(signal, ("kickoff", "execution-report", "report", "review"))
    ):
        return "Analysis", "local-context-analysis", "examines local context, execution state, or existing artifacts"

    if "external-analysis" in lower_type or has_any(
        signal + " " + content_sample[:1200],
        (
            "research",
            "исследован",
            "industry",
            "market",
            "external source",
            "international practice",
            "variants",
            "вариант",
            "гипотез",
            "hypothesis",
            "comparative",
        ),
    ):
        return "Research", "knowledge-generation", "generates or compares new knowledge, hypotheses, variants, or evidence base"

    if has_any(
        signal,
        ("analysis", "анализ", "internal-analysis", "report", "отчет", "отчёт", "summary", "сводка", "inventory", "инвентар", "roadmap", "matrix"),
    ):
        return "Analysis", "local-context-analysis", "examines local context, execution state, or existing artifacts"

    if lower_path.startswith(("research/", "docs/research/")):
        return "Research", "research-location", "research location with no stronger contrary signal"

    if lower_path.startswith("docs/analysis/"):
        return "Analysis", "analysis-location", "analysis location with no stronger contrary signal"

    if lower_path.startswith("docs/audit/"):
        return "Audit", "audit-location", "audit location with no stronger contrary signal"

    if lower_path.startswith("docs/"):
        return "Other", "documentation", "product, navigation, reference, or auxiliary documentation"

    return "Other", "unclassified", "outside the three target artifact types"


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

    actual_type, subtype, rationale = classify(path, fields, title, text)
    folder = "/".join(path.split("/")[:2]) if "/" in path else path
    if path.startswith("docs/analysis/"):
        scan_bucket = "docs/analysis"
    elif path.startswith("docs/audit/"):
        scan_bucket = "docs/audit"
    elif path.startswith("docs/reports/"):
        scan_bucket = "docs/reports"
    elif path.startswith(("research/", "docs/research/")):
        scan_bucket = "research"
    elif path.startswith("docs/"):
        scan_bucket = "docs"
    else:
        scan_bucket = folder

    return {
        "repo": repo.key,
        "repo_label": repo.label,
        "path": path,
        "scan_bucket": scan_bucket,
        "extension": extension or "[none]",
        "text_like": text_like,
        "title": title,
        "frontmatter_type": fields.get("type", ""),
        "frontmatter_status": fields.get("status", ""),
        "actual_type": actual_type,
        "subtype": subtype,
        "rationale": rationale,
        "line_count": line_count,
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
        "# Research/Analysis/Audit artifact classification matrix",
        "",
        "Generated for issue #288. Classification is heuristic and evidence-oriented:",
        "path is only a signal; title, frontmatter and early content are used to detect",
        "audit/report/research/proposal signals. The written research report performs",
        "the final human-readable synthesis. The issue #288 report and experiment",
        "directory are excluded from the Hub scan so reruns preserve the baseline.",
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
            "| Repo | Research | Analysis | Audit | Other | Total text artifacts | Non-text docs artifacts |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )

    for key in ("hub", "mango", "clarify"):
        repo_records = grouped[key]
        counts = Counter(record["actual_type"] for record in repo_records if record["text_like"])
        non_text = sum(1 for record in repo_records if not record["text_like"])
        total_text = sum(1 for record in repo_records if record["text_like"])
        lines.append(
            f"| {repo_meta[key]['label']} | {counts['Research']} | {counts['Analysis']} | "
            f"{counts['Audit']} | {counts['Other']} | {total_text} | {non_text} |"
        )

    for key in ("hub", "mango", "clarify"):
        lines.extend(
            [
                "",
                f"## {repo_meta[key]['label']}",
                "",
                "| Path | Bucket | Actual type | Subtype | Source signal | Title |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for record in sorted(grouped[key], key=lambda item: item["path"]):
            if not record["text_like"]:
                continue
            title = record["title"].replace("|", "\\|") or "-"
            source_signal = record["frontmatter_type"] or record["frontmatter_status"] or "-"
            lines.append(
                f"| `{record['path']}` | `{record['scan_bucket']}` | {record['actual_type']} | "
                f"{record['subtype']} | `{source_signal}` | {title} |"
            )

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub-root", default=".", help="Path to hybrid-Intelligence-lab checkout")
    parser.add_argument(
        "--hub-baseline-sha",
        default=HUB_BASELINE_SHA,
        help="Hub baseline SHA recorded in outputs; issue #288 deliverables are excluded from the scan.",
    )
    parser.add_argument("--mango-root", required=True, help="Path to mango_ba_prompts checkout")
    parser.add_argument("--clarify-root", required=True, help="Path to clarify-engine-ai checkout")
    parser.add_argument(
        "--out-dir",
        default="research/hub/exp/research-analysis-audit-288",
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
            "sha": args.hub_baseline_sha if spec.key == "hub" else repo_sha(spec.root),
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
        "scope": ["research/**", "docs/**"],
        "repo_meta": repo_meta,
        "records": records,
    }
    (out_dir / "artifact-classification.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out_dir / "2026-06-28-artifact-classification-matrix.md").write_text(
        markdown_matrix(records, repo_meta),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
