#!/usr/bin/env python3
"""Collect the PR/issue corpus for issue #461 (ops task-strategy validation).

Fetches pull requests and issues from the three ecosystem repositories named in
the issue SSOT, derives per-PR outcome labels and per-issue specification
features, and writes a compact evidence file (`corpus-metrics.json`).

Full bodies are NOT committed: they are large and partly redundant with GitHub.
Reproducibility is provided by this script plus the recorded `collected_at`
timestamp and per-repo item counts.

Usage:
    python3 collect_evidence.py [--cache DIR] [--offline]

Requires the authenticated `gh` CLI.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import datetime

REPOS = [
    "G-Ivan-A/hybrid-Intelligence-lab",
    "G-Ivan-A/clarify-engine-ai",
    "G-Ivan-A/mango_ba_prompts",
]

PR_FIELDS = (
    "number,title,state,createdAt,mergedAt,closedAt,additions,deletions,"
    "changedFiles,author,body,closingIssuesReferences"
)
ISSUE_FIELDS = "number,title,state,createdAt,closedAt,body,author"

PR_LIMIT = 250
ISSUE_LIMIT = 1000

# Commit headlines are fetched per PR over REST rather than in the list query:
# nesting `commits` inside a 250-PR GraphQL page exceeds GitHub's 500k-node
# ceiling. To keep the request count bounded we fetch them ONLY for outcomes
# where commit shape is diagnostic (see `needs_commit_shape`). PRs merged with a
# real diff therefore carry no `commit_count`/`has_revert` fields, and the
# analysis must not treat their absence as `false`.

HERE = pathlib.Path(__file__).resolve().parent

# --- specification features -------------------------------------------------
# Each feature is a coarse, deterministic signal that a task author either did
# or did not put into the issue text. Patterns cover the Russian and English
# wording actually used across the three repositories.

SPEC_FEATURES: dict[str, str] = {
    # WHAT: the substance of the task
    "goal": r"(^|\n)\s*#{1,4}?\s*.{0,6}(ЦЕЛЬ|GOAL|Objective)\b|\*\*Ц[еЕ]ль\*\*|(^|\n)Цель[.:]",
    "context": r"(^|\n)\s*#{1,4}?\s*.{0,6}(КОНТЕКСТ|CONTEXT)\b|\*\*Контекст\*\*|(^|\n)Контекст[.:]",
    "dod": r"Definition of Done|(^|\n)\s*#{1,4}?\s*.{0,6}DoD\b|(^|\n)DoD[.:]|Acceptance Criteria|Критерии\s+при[её]мки",
    "sources": r"(^|\n)\s*#{1,4}?\s*.{0,6}(ИСТОЧНИКИ|SOURCES|SSOT|Single Source of Truth)\b",
    "steps": r"(^|\n)\s*#{1,4}?\s*.{0,6}(ЭТАП|Этап|ТРЕБОВАНИЯ К ИСПОЛНИТЕЛЮ|TODO|Шаги|Steps|План работ)",
    # BOUNDS: what the executor may not do
    "constraints": r"(^|\n)\s*#{1,4}?\s*.{0,6}(ОГРАНИЧЕНИЯ|CONSTRAINTS|Forbidden|Запрещено)\b|❌",
    "operating_mode": r"Operating Mode|Режим(\s+выполнения)?[:\s]*[`*]*(Structured|Creative|Research|Education|Hybrid)",
    "validation": r"validate-|валидатор|Validation\b|локальн\w+ проверк",
    # DECISION CONTRACTS: how the executor resolves uncertainty at runtime
    "verification_rule": (
        r"подтверд\w+\s+(факт|по репозиторию)|сверь|сверить|проверь по репозиторию|"
        r"если факт не подтвержда|не выдумыв|не придумыв|verify against|do not invent"
    ),
    "escalation_rule": (
        r"зафиксир\w+\s+(расхождение|блокировк|конфликт|gap)|запрос\w+\s+guidance|"
        r"задай вопрос|уточни у|escalat|ask (the )?(founder|maintainer|human)|"
        r"вынеси в отч[её]т|отрази в отч[её]те"
    ),
    "autonomy_rule": (
        r"НЕ\s+стопор|не стопорит|без ожидания (approval|апрув)|не жди (approval|апрув)|"
        r"не дожидайся|самостоятельно (определ|выбир|реш)|исполнитель\s+самостоятельно|"
        r"do not wait for approval|proceed without"
    ),
    "nonempty_rule": (
        r"пуст\w*\s+(мерж|merge|revert|PR|diff)|ненулев\w+\s+diff|non-empty diff|"
        r"внести правки реально|не мержить ноль"
    ),
}

SPEC_COMPILED = {k: re.compile(v, re.I | re.M) for k, v in SPEC_FEATURES.items()}

# Groups used by the analysis: "specification detail" vs "decision contracts".
DETAIL_FEATURES = [
    "goal", "context", "dod", "sources", "steps",
    "constraints", "operating_mode", "validation",
]
CONTRACT_FEATURES = [
    "verification_rule", "escalation_rule", "autonomy_rule", "nonempty_rule",
]

LINK_RE = re.compile(r"(?:Fixes|Closes|Resolves)\s+\S*?#(\d+)", re.I)
REVERT_RE = re.compile(r"^Revert\b", re.I)
SCAFFOLD_RE = re.compile(r"^Initial commit with task details", re.I)


def run_gh(args: list[str]) -> str:
    proc = subprocess.run(
        ["gh", *args], capture_output=True, text=True, check=False
    )
    if proc.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def fetch(repo: str, kind: str, fields: str, cache: pathlib.Path,
          offline: bool, limit: int) -> list[dict]:
    slug = repo.replace("/", "_")
    path = cache / f"{slug}.{kind}.json"
    if offline:
        if not path.exists():
            raise SystemExit(f"offline mode: missing cache file {path}")
        return json.loads(path.read_text())
    raw = run_gh([
        kind, "list", "--repo", repo, "--state", "all",
        "--limit", str(limit), "--json", fields,
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(raw)
    return json.loads(raw)


def linked_issue(pr: dict) -> int | None:
    """Issue number this PR closes, from the GitHub link or the body text."""
    refs = pr.get("closingIssuesReferences") or []
    if refs:
        return refs[0].get("number")
    match = LINK_RE.search(pr.get("body") or "")
    return int(match.group(1)) if match else None


def classify_outcome(pr: dict) -> str:
    """Coarse outcome label for a pull request.

    empty-merge     merged but changed nothing in the base branch
    merged          merged with a real diff
    abandoned       closed without merge
    open            still open
    """
    if pr["state"] == "OPEN":
        return "open"
    if pr["state"] == "CLOSED":
        return "abandoned"
    if pr.get("changedFiles", 0) == 0 or (
        pr.get("additions", 0) == 0 and pr.get("deletions", 0) == 0
    ):
        return "empty-merge"
    return "merged"


def needs_commit_shape(outcome: str) -> bool:
    """Commit shape is only diagnostic for non-productive outcomes."""
    return outcome in {"empty-merge", "abandoned", "open"}


def fetch_commit_shape(repo: str, number: int, cache: pathlib.Path,
                       offline: bool) -> dict:
    """Detect the scaffold+revert signature of a stalled solver session."""
    path = cache / f"{repo.replace('/', '_')}.commits.{number}.json"
    if offline:
        if not path.exists():
            return {}
        raw = path.read_text()
    else:
        raw = run_gh(["api", f"repos/{repo}/pulls/{number}/commits",
                      "--paginate"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(raw)
    commits = json.loads(raw)
    messages = [
        (c.get("commit", {}).get("message") or "").strip().splitlines()[0]
        for c in commits
    ]
    return {
        "commit_count": len(messages),
        "has_revert": any(REVERT_RE.match(m) for m in messages),
        "has_scaffold": any(SCAFFOLD_RE.match(m) for m in messages),
        "headlines": messages[:12],
    }


def spec_features(body: str | None, title: str | None = None) -> dict:
    """Compact specification profile of one task statement.

    `features` lists only the signals that fired; absence means the pattern did
    not match. Storing the hit list rather than a full boolean map keeps the
    committed evidence file an order of magnitude smaller.
    """
    text = f"{title or ''}\n{body or ''}"
    hits = [name for name, rx in SPEC_COMPILED.items() if rx.search(text)]
    return {
        "features": hits,
        "length_chars": len(body or ""),
        "heading_count": len(re.findall(r"^#{1,6}\s", body or "", re.M)),
        "checkbox_count": len(
            re.findall(r"^\s*[-*]\s*\[[ xX]\]", body or "", re.M)
        ),
        "detail_score": sum(1 for f in DETAIL_FEATURES if f in hits),
        "contract_score": sum(1 for f in CONTRACT_FEATURES if f in hits),
    }


def dump_compact(corpus: dict) -> str:
    """Serialize with one PR/issue record per line.

    Standard `indent=2` inflates ~950 small records to half a megabyte. Keeping
    each record on its own line stays diff-friendly and review-friendly while
    cutting the file to a size in line with the other `exp/` evidence files.
    """
    def rows(items: list[dict]) -> str:
        body = ",\n".join(
            "      " + json.dumps(item, ensure_ascii=False, sort_keys=True)
            for item in items
        )
        return f"[\n{body}\n    ]" if items else "[]"

    head = {k: v for k, v in corpus.items() if k != "repos"}
    parts = [json.dumps(head, ensure_ascii=False, indent=2)[:-2].rstrip() + ","]
    parts.append('  "repos": {')
    repo_blocks = []
    for repo, data in corpus["repos"].items():
        repo_blocks.append(
            f'    {json.dumps(repo)}: {{\n'
            f'      "pr_count": {data["pr_count"]},\n'
            f'      "issue_count": {data["issue_count"]},\n'
            f'      "prs": {rows(data["prs"])},\n'
            f'      "issues": {rows(data["issues"])}\n'
            f'    }}'
        )
    parts.append(",\n".join(repo_blocks))
    parts.append("  }\n}\n")
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", default="/tmp/ops-task-strategy-461-cache")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--out", default=str(HERE / "corpus-metrics.json"))
    args = parser.parse_args()

    cache = pathlib.Path(args.cache)
    corpus: dict = {
        "collected_at": datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat(),
        "source_issue": "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/461",
        "feature_definitions": SPEC_FEATURES,
        "detail_features": DETAIL_FEATURES,
        "contract_features": CONTRACT_FEATURES,
        "repos": {},
    }

    for repo in REPOS:
        prs = fetch(repo, "pr", PR_FIELDS, cache, args.offline, PR_LIMIT)
        issues = fetch(repo, "issue", ISSUE_FIELDS, cache, args.offline, ISSUE_LIMIT)
        issue_by_number = {i["number"]: i for i in issues}

        pr_records = []
        for pr in prs:
            num = linked_issue(pr)
            issue = issue_by_number.get(num) if num else None
            record = {
                "number": pr["number"],
                "title": pr["title"],
                "outcome": classify_outcome(pr),
                "additions": pr.get("additions", 0),
                "deletions": pr.get("deletions", 0),
                "changed_files": pr.get("changedFiles", 0),
                "created_at": pr.get("createdAt"),
                "merged_at": pr.get("mergedAt"),
                "issue_number": num,
                "issue_found": issue is not None,
            }
            if needs_commit_shape(record["outcome"]):
                record.update(
                    fetch_commit_shape(repo, pr["number"], cache, args.offline)
                )
            # Spec features are stored once, on the issue record; PRs join to
            # them by `issue_number`. Duplicating them here would roughly
            # double the evidence file for no extra information.
            pr_records.append(record)

        corpus["repos"][repo] = {
            "pr_count": len(prs),
            "issue_count": len(issues),
            "prs": sorted(pr_records, key=lambda r: r["number"]),
            "issues": [
                {
                    "number": i["number"],
                    "title": i["title"],
                    "state": i["state"],
                    "created_at": i.get("createdAt"),
                    "spec": spec_features(i.get("body"), i["title"]),
                }
                for i in sorted(issues, key=lambda i: i["number"])
            ],
        }
        print(
            f"{repo}: {len(prs)} PRs, {len(issues)} issues, "
            f"{sum(1 for r in pr_records if r['outcome'] == 'empty-merge')} empty merges",
            file=sys.stderr,
        )

    out = pathlib.Path(args.out)
    out.write_text(dump_compact(corpus))
    print(f"wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
