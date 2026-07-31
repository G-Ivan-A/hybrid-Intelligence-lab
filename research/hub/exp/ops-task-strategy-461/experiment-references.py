#!/usr/bin/env python3
"""Direction 2, experiment A: does a longer task statement stay resolvable?

A short task says little; a detailed one names paths, artifacts and versions.
Every named path is a promise the executor will try to follow. This experiment
measures how often that promise holds, resolving each reference against the Hub
tree **as it stood on the day the task was written** (not against today's tree,
which several migrations have since reshaped).

Metrics per task statement:
    refs_total        distinct repository paths named in the issue body
    refs_unresolved   those that did not exist at issue creation time
    unresolved_rate   refs_unresolved / refs_total

Only `hybrid-Intelligence-lab` is measured: it is the repository whose full
history is available locally, and resolving references against a remote tree per
issue would cost one API call per path. This limit is stated in the output.

Usage:
    python3 experiment-references.py [--repo-root PATH]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import statistics

HERE = pathlib.Path(__file__).resolve().parent
TARGET_REPO = "G-Ivan-A/hybrid-Intelligence-lab"

# A reference is a repository-looking path: at least one slash and either a
# known text extension or a trailing slash for a directory.
REF_RE = re.compile(
    r"(?<![\w.-])"
    r"((?:\./)?(?:[\w.-]+/)+(?:[\w.-]+\.(?:md|py|sh|ya?ml|json|txt|cfg|toml))?)"
)

# Prose in both languages is full of slashes ("Research/Analysis", "R/A/A",
# "human/AI"). Requiring the first segment to be a real top-level entry of the
# Hub tree at that moment removes them, and also removes references that point
# into the sibling repositories (`kb/`, `governance/BACKLOG.md`) rather than
# here. Those cross-repo references are counted separately as out of scope
# instead of being scored as broken Hub links.

def run(args: list[str], cwd: pathlib.Path) -> str:
    proc = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                          check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"{' '.join(args)}: {proc.stderr.strip()}")
    return proc.stdout


def tree_at(root: pathlib.Path, iso_date: str, cache: dict) -> set[str] | None:
    """Set of tracked paths on the default branch as of `iso_date`."""
    day = iso_date[:10]
    if day in cache:
        return cache[day]
    commit = run(
        ["git", "rev-list", "-1", f"--before={day}T23:59:59Z", "main"], root
    ).strip()
    if not commit:
        cache[day] = None
        return None
    listing = run(["git", "ls-tree", "-r", "--name-only", commit], root)
    paths = set(listing.split())
    # Directories are referenced too; add every prefix so `research/hub/` counts
    # as resolvable when files live under it.
    dirs = set()
    for path in paths:
        parts = path.split("/")
        for i in range(1, len(parts)):
            dirs.add("/".join(parts[:i]) + "/")
    cache[day] = paths | dirs
    return cache[day]


# `docs/report/YYYY-MM-DD-name.md` and `docs/adr/NNN-name.md` are the naming
# convention being quoted, not a file anyone expects to open.
PLACEHOLDER_RE = re.compile(r"YYYY|MM-DD|NNN|<[^>]+>|\{[^}]+\}")


def top_level(tree: set[str]) -> set[str]:
    """Top-level directory and file names present in a tree listing."""
    names = set()
    for path in tree:
        head = path.split("/", 1)[0]
        names.add(head)
    return names


def extract_refs(body: str, tree: set[str]) -> tuple[list[str], list[str]]:
    """Return (in-scope Hub references, out-of-scope candidates)."""
    roots = top_level(tree)
    in_scope, out_of_scope = set(), set()
    for match in REF_RE.finditer(body or ""):
        ref = match.group(1).strip()
        if ref.startswith("./"):
            ref = ref[2:]
        if not ref or "/" not in ref or PLACEHOLDER_RE.search(ref):
            continue
        if ref.split("/", 1)[0] in roots:
            in_scope.add(ref)
        else:
            out_of_scope.add(ref)
    return sorted(in_scope), sorted(out_of_scope)


SEED = 20260731
PERMUTATIONS = 20000


def permutation_diff_in_means(a: list[float], b: list[float]) -> dict:
    """Two-sided permutation test on the difference of means."""
    observed = statistics.fmean(a) - statistics.fmean(b)
    pool = a + b
    split = len(a)
    state = SEED
    extreme = 0
    for _ in range(PERMUTATIONS):
        # Deterministic Fisher-Yates: the seed is fixed so the p-value is
        # reproducible from the committed code alone.
        shuffled = pool[:]
        for i in range(len(shuffled) - 1, 0, -1):
            state = (1103515245 * state + 12345) % (1 << 31)
            j = state % (i + 1)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        diff = (statistics.fmean(shuffled[:split])
                - statistics.fmean(shuffled[split:]))
        if abs(diff) >= abs(observed) - 1e-12:
            extreme += 1
    return {
        "mean_a": round(statistics.fmean(a), 4),
        "mean_b": round(statistics.fmean(b), 4),
        "observed_diff": round(observed, 4),
        "p_value": round((extreme + 1) / (PERMUTATIONS + 1), 4),
        "n_a": len(a),
        "n_b": len(b),
    }


def temporal_control(records: list[dict]) -> dict:
    """Unresolved rate is an era property before it is a detail property.

    The Hub restructured itself during 2026-06 (`governance/` folded into
    `pr-ops/`, research artifacts renamed date-first). Task statements written
    in that window cite paths that the restructure invalidated days later, so
    comparing detail groups without holding the month fixed measures the
    migration, not the specification style. Detailed issues cluster in July and
    short ones in May-June, which is exactly the shape that would manufacture a
    spurious result.
    """
    by_month: dict[str, list[dict]] = {}
    for rec in records:
        by_month.setdefault(rec["created_at"][:7], []).append(rec)

    months = []
    within = []
    for month in sorted(by_month):
        subset = by_month[month]
        months.append({
            "month": month,
            "n": len(subset),
            "mean_refs": round(
                statistics.fmean(r["refs_total"] for r in subset), 2),
            "mean_unresolved_rate": round(
                statistics.fmean(r["unresolved_rate"] for r in subset), 3),
        })
        low = [r["unresolved_rate"] for r in subset
               if (r["detail_score"] or 0) <= 4]
        high = [r["unresolved_rate"] for r in subset
                if (r["detail_score"] or 0) >= 5]
        if len(low) >= 5 and len(high) >= 5:
            test = permutation_diff_in_means(high, low)
            test["month"] = month
            test["comparison"] = "detail>=5 minus detail<=4, unresolved rate"
            within.append(test)

    return {
        "note": temporal_control.__doc__.strip(),
        "by_month": months,
        "within_month_detail_split": within,
        "detail_group_months": {
            label: sorted(
                r["created_at"] for r in records
                if predicate(r["detail_score"] or 0)
            )[len([r for r in records if predicate(r["detail_score"] or 0)]) // 2]
            for label, predicate in (
                ("short (<=3) median date", lambda d: d <= 3),
                ("medium (4-5) median date", lambda d: 3 < d < 6),
                ("detailed (>=6) median date", lambda d: d >= 6),
            )
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=str(HERE.parents[3]))
    parser.add_argument(
        "--cache", default="/tmp/ops-task-strategy-461-cache",
        help="issue cache written by collect-evidence.py",
    )
    args = parser.parse_args()

    root = pathlib.Path(args.repo_root).resolve()
    cache_file = (
        pathlib.Path(args.cache)
        / f"{TARGET_REPO.replace('/', '_')}.issue.json"
    )
    if not cache_file.exists():
        raise SystemExit(
            f"missing {cache_file}; run collect-evidence.py first"
        )
    issues = json.loads(cache_file.read_text())
    metrics = json.loads((HERE / "corpus-metrics.json").read_text())
    spec_by_number = {
        i["number"]: i["spec"] for i in metrics["repos"][TARGET_REPO]["issues"]
    }
    outcome_by_issue = {
        pr["issue_number"]: pr["outcome"]
        for pr in metrics["repos"][TARGET_REPO]["prs"]
        if pr.get("issue_number")
    }

    tree_cache: dict = {}
    records = []
    for issue in issues:
        body = issue.get("body") or ""
        tree = tree_at(root, issue["createdAt"], tree_cache)
        if tree is None:
            continue
        refs, out_of_scope = extract_refs(body, tree)
        if not refs:
            continue
        unresolved = [r for r in refs if r not in tree]
        spec = spec_by_number.get(issue["number"], {})
        records.append({
            "issue": issue["number"],
            "title": issue["title"][:90],
            "created_at": issue["createdAt"][:10],
            "outcome": outcome_by_issue.get(issue["number"]),
            "detail_score": spec.get("detail_score"),
            "contract_score": spec.get("contract_score"),
            "length_chars": spec.get("length_chars"),
            "refs_total": len(refs),
            "refs_out_of_scope": len(out_of_scope),
            "refs_unresolved": len(unresolved),
            "unresolved_rate": round(len(unresolved) / len(refs), 3),
            "unresolved_sample": unresolved[:8],
        })

    def summarise(subset: list[dict], label: str) -> dict:
        if not subset:
            return {"label": label, "n": 0}
        return {
            "label": label,
            "n": len(subset),
            "median_refs": statistics.median(r["refs_total"] for r in subset),
            "mean_refs": round(
                statistics.fmean(r["refs_total"] for r in subset), 2),
            "mean_unresolved": round(
                statistics.fmean(r["refs_unresolved"] for r in subset), 2),
            "mean_unresolved_rate": round(
                statistics.fmean(r["unresolved_rate"] for r in subset), 3),
            "share_with_any_unresolved": round(
                sum(1 for r in subset if r["refs_unresolved"]) / len(subset), 3),
        }

    detailed = [r for r in records if (r["detail_score"] or 0) >= 6]
    short = [r for r in records if (r["detail_score"] or 0) <= 3]
    mid = [r for r in records if 3 < (r["detail_score"] or 0) < 6]
    failed = [r for r in records
              if r["outcome"] in {"empty-merge", "abandoned"}]

    report = {
        "experiment": "reference resolvability vs specification detail",
        "repo": TARGET_REPO,
        "limitation": (
            "Hub only: full local git history makes point-in-time resolution "
            "possible without one API call per referenced path. Clarify and "
            "Mango are not measured here."
        ),
        "issues_with_references": len(records),
        "groups": [
            summarise(short, "detail_score <= 3 (short)"),
            summarise(mid, "detail_score 4-5 (medium)"),
            summarise(detailed, "detail_score >= 6 (detailed)"),
            summarise(failed, "non-productive outcome"),
            summarise(records, "all"),
        ],
        "temporal_control": temporal_control(records),
        "correlation_refs_vs_detail": None,
        "worst_offenders": sorted(
            records, key=lambda r: (-r["refs_unresolved"], r["issue"])
        )[:15],
        "records": sorted(records, key=lambda r: r["issue"]),
    }

    xs = [float(r["detail_score"] or 0) for r in records]
    ys = [float(r["refs_total"]) for r in records]
    if len(xs) >= 3:
        report["correlation_refs_vs_detail"] = {
            "pearson_detail_vs_refs": round(statistics.correlation(xs, ys), 4),
            "n": len(xs),
        }

    out = HERE / "experiment-references.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    for group in report["groups"]:
        if group["n"]:
            print(f"{group['label']:32s} n={group['n']:3d} "
                  f"refs~{group['mean_refs']:6.2f} "
                  f"unresolved~{group['mean_unresolved']:5.2f} "
                  f"rate={group['mean_unresolved_rate']:.3f} "
                  f"any={group['share_with_any_unresolved']:.3f}")
    print()
    for month in report["temporal_control"]["by_month"]:
        print(f"{month['month']} n={month['n']:3d} "
              f"refs~{month['mean_refs']:5.2f} "
              f"unresolved_rate~{month['mean_unresolved_rate']:.3f}")
    for test in report["temporal_control"]["within_month_detail_split"]:
        print(f"{test['month']} within-month detail>=5 ({test['n_a']}) "
              f"{test['mean_a']:.3f} vs detail<=4 ({test['n_b']}) "
              f"{test['mean_b']:.3f}  p={test['p_value']}")
    print()
    print(f"corr(detail, refs) = {report['correlation_refs_vs_detail']}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
