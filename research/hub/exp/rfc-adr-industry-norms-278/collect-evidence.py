#!/usr/bin/env python3
"""Collect reproducible RFC/ADR evidence for issue #278.

The script intentionally stores only source metadata, paths and small extracted
headings/status fields. It does not mirror external repositories.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class RepoSource:
    repo: str
    archetype: str
    label: str
    lens: str


RFC_SOURCES = [
    RepoSource("rust-lang/rfcs", "A", "Rust RFCs", "rfc"),
    RepoSource("kubernetes/enhancements", "A", "Kubernetes KEPs", "rfc"),
    RepoSource("open-telemetry/oteps", "A", "OpenTelemetry OTEPs", "rfc"),
    RepoSource("cncf/toc", "A", "CNCF TOC proposals", "rfc"),
    RepoSource("nodejs/TSC", "A", "Node.js TSC proposals/governance", "rfc"),
    RepoSource("python/peps", "A", "Python PEPs", "rfc"),
    RepoSource("golang/proposal", "A", "Go proposals", "rfc"),
    RepoSource("tc39/proposals", "A", "TC39 proposals", "rfc"),
    RepoSource("WICG/proposals", "A", "WICG proposals", "rfc"),
    RepoSource("ethereum/EIPs", "A", "Ethereum EIPs", "rfc"),
    RepoSource("bitcoin/bips", "A", "Bitcoin BIPs", "rfc"),
    RepoSource("whatwg/html", "A", "WHATWG HTML governance/spec", "rfc"),
    RepoSource("langchain-ai/langchain", "B", "LangChain", "rfc"),
    RepoSource("langchain-ai/langgraph", "B", "LangGraph", "rfc"),
    RepoSource("microsoft/promptflow", "B", "Microsoft Promptflow", "rfc"),
    RepoSource("promptfoo/promptfoo", "B", "Promptfoo", "rfc"),
    RepoSource("guidance-ai/guidance", "B", "Guidance", "rfc"),
    RepoSource("openai/openai-cookbook", "B", "OpenAI Cookbook", "rfc"),
    RepoSource("anthropics/claude-cookbooks", "B", "Anthropic Claude Cookbooks", "rfc"),
    RepoSource("microsoft/generative-ai-for-beginners", "B", "Generative AI for Beginners", "rfc"),
    RepoSource("deepset-ai/haystack", "B", "Haystack", "rfc"),
    RepoSource("run-llama/llama_index", "B", "LlamaIndex", "rfc"),
    RepoSource("crewAIInc/crewAI", "B", "CrewAI", "rfc"),
    RepoSource("stanfordnlp/dspy", "B", "DSPy", "rfc"),
    RepoSource("supabase/supabase", "C", "Supabase", "rfc"),
    RepoSource("calcom/cal.com", "C", "Cal.com", "rfc"),
    RepoSource("directus/directus", "C", "Directus", "rfc"),
    RepoSource("strapi/strapi", "C", "Strapi", "rfc"),
    RepoSource("grafana/grafana", "C", "Grafana", "rfc"),
    RepoSource("n8n-io/n8n", "C", "n8n", "rfc"),
    RepoSource("mattermost/mattermost", "C", "Mattermost", "rfc"),
    RepoSource("hashicorp/terraform", "C", "Terraform", "rfc"),
    RepoSource("backstage/backstage", "C", "Backstage", "rfc"),
    RepoSource("elastic/kibana", "C", "Kibana", "rfc"),
    RepoSource("home-assistant/core", "C", "Home Assistant Core", "rfc"),
    RepoSource("penpot/penpot", "C", "Penpot", "rfc"),
    RepoSource("freeCodeCamp/freeCodeCamp", "D", "freeCodeCamp", "rfc"),
    RepoSource("mdn/content", "D", "MDN Content", "rfc"),
    RepoSource("TheAlgorithms/Python", "D", "The Algorithms Python", "rfc"),
    RepoSource("ossu/computer-science", "D", "OSSU Computer Science", "rfc"),
    RepoSource("codecrafters-io/build-your-own-x", "D", "Build Your Own X", "rfc"),
    RepoSource("exercism/v3", "D", "Exercism v3", "rfc"),
    RepoSource("kubernetes/website", "D", "Kubernetes Website", "rfc"),
    RepoSource("github/docs", "D", "GitHub Docs", "rfc"),
    RepoSource("facebook/react", "D", "React docs/project", "rfc"),
    RepoSource("django/djangoproject.com", "D", "Django project website", "rfc"),
    RepoSource("microsoft/Web-Dev-For-Beginners", "D", "Web Dev for Beginners", "rfc"),
]

ADR_SOURCES = [
    RepoSource("adr/madr", "standard", "MADR", "adr"),
    RepoSource("npryce/adr-tools", "standard", "adr-tools", "adr"),
    RepoSource("joelparkerhenderson/architecture-decision-record", "standard", "ADR examples catalog", "adr"),
    RepoSource("rust-lang/rfcs", "A", "Rust accepted RFCs as decision records", "adr"),
    RepoSource("kubernetes/enhancements", "A", "Kubernetes KEPs as decision records", "adr"),
    RepoSource("open-telemetry/oteps", "A", "OpenTelemetry OTEPs as decision records", "adr"),
    RepoSource("cncf/toc", "A", "CNCF TOC governance decisions", "adr"),
    RepoSource("nodejs/TSC", "A", "Node.js TSC decisions", "adr"),
    RepoSource("python/peps", "A", "Python PEPs as accepted decisions", "adr"),
    RepoSource("golang/proposal", "A", "Go proposal decisions", "adr"),
    RepoSource("tc39/proposals", "A", "TC39 proposals as standards decisions", "adr"),
    RepoSource("WICG/proposals", "A", "WICG proposals as standards decisions", "adr"),
    RepoSource("ethereum/EIPs", "A", "Ethereum EIPs as accepted decisions", "adr"),
    RepoSource("bitcoin/bips", "A", "Bitcoin BIPs as accepted decisions", "adr"),
    RepoSource("open-telemetry/community", "A", "OpenTelemetry community governance", "adr"),
    RepoSource("langchain-ai/langchain", "B", "LangChain", "adr"),
    RepoSource("langchain-ai/langgraph", "B", "LangGraph", "adr"),
    RepoSource("microsoft/promptflow", "B", "Microsoft Promptflow", "adr"),
    RepoSource("promptfoo/promptfoo", "B", "Promptfoo", "adr"),
    RepoSource("guidance-ai/guidance", "B", "Guidance", "adr"),
    RepoSource("openai/openai-cookbook", "B", "OpenAI Cookbook", "adr"),
    RepoSource("anthropics/claude-cookbooks", "B", "Anthropic Claude Cookbooks", "adr"),
    RepoSource("deepset-ai/haystack", "B", "Haystack", "adr"),
    RepoSource("run-llama/llama_index", "B", "LlamaIndex", "adr"),
    RepoSource("crewAIInc/crewAI", "B", "CrewAI", "adr"),
    RepoSource("stanfordnlp/dspy", "B", "DSPy", "adr"),
    RepoSource("supabase/supabase", "C", "Supabase", "adr"),
    RepoSource("calcom/cal.com", "C", "Cal.com", "adr"),
    RepoSource("directus/directus", "C", "Directus", "adr"),
    RepoSource("strapi/strapi", "C", "Strapi", "adr"),
    RepoSource("grafana/grafana", "C", "Grafana", "adr"),
    RepoSource("n8n-io/n8n", "C", "n8n", "adr"),
    RepoSource("mattermost/mattermost", "C", "Mattermost", "adr"),
    RepoSource("hashicorp/terraform", "C", "Terraform", "adr"),
    RepoSource("backstage/backstage", "C", "Backstage", "adr"),
    RepoSource("elastic/kibana", "C", "Kibana", "adr"),
    RepoSource("home-assistant/architecture", "C", "Home Assistant Architecture", "adr"),
    RepoSource("penpot/penpot", "C", "Penpot", "adr"),
    RepoSource("freeCodeCamp/freeCodeCamp", "D", "freeCodeCamp", "adr"),
    RepoSource("mdn/content", "D", "MDN Content", "adr"),
    RepoSource("TheAlgorithms/Python", "D", "The Algorithms Python", "adr"),
    RepoSource("ossu/computer-science", "D", "OSSU Computer Science", "adr"),
    RepoSource("exercism/v3", "D", "Exercism v3", "adr"),
    RepoSource("kubernetes/website", "D", "Kubernetes Website", "adr"),
    RepoSource("github/docs", "D", "GitHub Docs", "adr"),
    RepoSource("microsoft/generative-ai-for-beginners", "D", "Generative AI for Beginners", "adr"),
    RepoSource("microsoft/Web-Dev-For-Beginners", "D", "Web Dev for Beginners", "adr"),
    RepoSource("django/djangoproject.com", "D", "Django project website", "adr"),
]


RFC_PATH_RE = re.compile(
    r"(^|/)(rfcs?|proposals?|enhancements?|keps?|oteps?|peps?|eips?|bips?|"
    r"governance|design-docs?|decision-records?)(/|$)|"
    r"(^|/)([0-9]{3,5}|rfc|proposal|kep|otep|pep|eip|bip)[-_].*\.md$",
    re.IGNORECASE,
)
ADR_PATH_RE = re.compile(
    r"(^|/)(adrs?|decision-records?|decisions?|architecture/decisions?|"
    r"docs/architecture|architecture)(/|$)|"
    r"(^|/)([0-9]{3,5}|adr)[-_].*\.md$",
    re.IGNORECASE,
)
HEADING_RE = re.compile(
    r"^(# .+|status:\s*.+|Status:\s*.+|## Status.*|"
    r"## (?:Context|Decision|Consequences|Контекст|Решение|Последствия).*)$",
    re.MULTILINE,
)


def gh_token() -> str | None:
    try:
        token = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return token or None


def github_json(url: str, token: str | None, retries: int = 3) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "issue-278-evidence-collector",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code in {403, 429, 500, 502, 503, 504} and attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue
            raise


def github_text(url: str, token: str | None) -> str:
    headers = {
        "Accept": "application/vnd.github.raw",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "issue-278-evidence-collector",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def repo_tree(repo: str, token: str | None) -> dict:
    meta = github_json(f"https://api.github.com/repos/{repo}", token)
    branch = meta["default_branch"]
    tree = github_json(
        f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1",
        token,
    )
    return {
        "repo": repo,
        "default_branch": branch,
        "html_url": meta.get("html_url"),
        "description": meta.get("description"),
        "archived": meta.get("archived"),
        "tree_truncated": tree.get("truncated"),
        "paths": [
            item["path"]
            for item in tree.get("tree", [])
            if item.get("type") == "blob"
        ],
    }


def sample_headings(repo: str, branch: str, paths: Iterable[str], token: str | None) -> dict[str, list[str]]:
    samples: dict[str, list[str]] = {}
    for path in list(paths)[:5]:
        if not path.lower().endswith((".md", ".mdx", ".txt", ".rst")):
            continue
        url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={branch}"
        try:
            text = github_text(url, token)
        except Exception as exc:  # pragma: no cover - diagnostic path
            samples[path] = [f"ERROR: {exc}"]
            continue
        samples[path] = [line.strip() for line in HEADING_RE.findall(text[:12000])]
        if not samples[path]:
            first_lines = [line.strip() for line in text.splitlines()[:8] if line.strip()]
            samples[path] = first_lines[:4]
    return samples


def summarize_repo(source: RepoSource, token: str | None) -> dict:
    try:
        tree = repo_tree(source.repo, token)
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {
            "repo": source.repo,
            "archetype": source.archetype,
            "label": source.label,
            "lens": source.lens,
            "error": str(exc),
        }

    matcher = RFC_PATH_RE if source.lens == "rfc" else ADR_PATH_RE
    matches = [path for path in tree["paths"] if matcher.search(path)]
    # Keep the evidence compact but deterministic.
    matches = sorted(matches, key=lambda value: (len(value), value.lower()))[:80]
    return {
        "repo": source.repo,
        "archetype": source.archetype,
        "label": source.label,
        "lens": source.lens,
        "default_branch": tree["default_branch"],
        "html_url": tree["html_url"],
        "description": tree["description"],
        "archived": tree["archived"],
        "tree_truncated": tree["tree_truncated"],
        "match_count_capped": len(matches),
        "sample_paths": matches[:25],
        "sample_headings": sample_headings(
            source.repo,
            tree["default_branch"],
            matches,
            token,
        ),
    }


def markdown_table(rows: list[dict], lens: str) -> str:
    title = f"{lens.upper()} external source tree summary"
    lines = [
        evidence_frontmatter(f"{lens}-external-tree-summary", date.today().isoformat()),
        f"# {title}",
        "",
        "| Archetype | Repository | Evidence paths found | Sample paths |",
        "| --- | --- | ---: | --- |",
    ]
    for row in rows:
        paths = row.get("sample_paths") or []
        sample = "<br>".join(f"`{path}`" for path in paths[:5]) if paths else "no path signal found"
        repo = row["repo"]
        url = row.get("html_url") or f"https://github.com/{repo}"
        count = row.get("match_count_capped", 0)
        if row.get("error"):
            sample = f"ERROR: {row['error']}"
        lines.append(
            f"| {row['archetype']} | [{repo}]({url}) | {count} | {sample} |"
        )
    lines.append("")
    return "\n".join(lines)


def evidence_frontmatter(slug: str, updated: str) -> str:
    return "\n".join(
        [
            "---",
            "status: draft",
            "version: 0.1",
            f"updated: {updated}",
            "temperature: 0.1",
            f"type: {slug}",
            "scope: evidence",
            "---",
            "",
        ]
    )


def frontmatter_status(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    match = re.search(r"^status:\s*([^\n]+)", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def first_heading(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    match = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    return match.group(1).strip() if match else path.stem


def local_audit(mango_path: Path | None) -> dict:
    repos = [
        ("hybrid-Intelligence-lab", ROOT),
    ]
    if mango_path and mango_path.exists():
        repos.append(("mango_ba_prompts", mango_path))

    result = {}
    for name, base in repos:
        files = []
        for rel in [
            "governance/rfc",
            "docs/rfc",
            "docs/adr",
            "standards/decisions",
            "docs/analysis",
        ]:
            folder = base / rel
            if not folder.exists():
                continue
            for path in sorted(folder.rglob("*.md")):
                if ".git" in path.parts:
                    continue
                files.append(
                    {
                        "path": path.relative_to(base).as_posix(),
                        "status": frontmatter_status(path),
                        "heading": first_heading(path),
                        "bytes": path.stat().st_size,
                    }
                )
        result[name] = files
    return result


def local_audit_markdown(audit: dict) -> str:
    lines = [
        evidence_frontmatter("local-rfc-adr-audit", date.today().isoformat()),
        "# Local ecosystem RFC/ADR audit",
        "",
        "| Repository | Path | Status | Heading |",
        "| --- | --- | --- | --- |",
    ]
    for repo, files in audit.items():
        for row in files:
            path = row["path"]
            if not (
                path.startswith("governance/rfc/")
                or path.startswith("docs/rfc/")
                or path.startswith("docs/adr/")
                or path.startswith("standards/decisions/")
            ):
                continue
            lines.append(
                f"| {repo} | `{path}` | `{row['status'] or '-'}"
                f"` | {row['heading']} |"
            )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mango-path",
        default="/tmp/mango_ba_prompts_issue278",
        help="local clone of G-Ivan-A/mango_ba_prompts",
    )
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    token = gh_token()
    if not token:
        print("WARN: no gh auth token found; unauthenticated GitHub API may rate-limit", file=sys.stderr)

    rfc_rows = [summarize_repo(source, token) for source in RFC_SOURCES]
    adr_rows = [summarize_repo(source, token) for source in ADR_SOURCES]
    audit = local_audit(Path(args.mango_path))

    (OUT_DIR / "rfc-external-tree-summary.json").write_text(
        json.dumps(rfc_rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT_DIR / "adr-external-tree-summary.json").write_text(
        json.dumps(adr_rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT_DIR / "local-rfc-adr-audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT_DIR / f"{date.today().isoformat()}-rfc-external-tree-summary.md").write_text(
        markdown_table(rfc_rows, "rfc"),
        encoding="utf-8",
    )
    (OUT_DIR / f"{date.today().isoformat()}-adr-external-tree-summary.md").write_text(
        markdown_table(adr_rows, "adr"),
        encoding="utf-8",
    )
    (OUT_DIR / f"{date.today().isoformat()}-local-rfc-adr-audit.md").write_text(
        local_audit_markdown(audit),
        encoding="utf-8",
    )

    print(f"Wrote evidence outputs to {OUT_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
