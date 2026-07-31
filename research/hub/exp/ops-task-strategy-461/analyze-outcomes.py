#!/usr/bin/env python3
"""Direction 1: what distinguishes productive PRs from non-productive ones.

Reads `corpus-metrics.json` (produced by `collect-evidence.py`) and answers:

1. How often does the ecosystem actually fail, and in what shape?
2. Do *detailed* task statements produce better outcomes than short ones?
3. Do *decision contracts* (verification / escalation / autonomy / non-empty
   rules) behave differently from plain specification detail?

All statistics are computed with the standard library only: an exact Fisher
test for the 2x2 contingency questions, and a seeded permutation test for the
rank comparisons. The failure class is small (10 PRs), so every result is
reported with its n and treated as descriptive unless the exact test says
otherwise.

Usage:
    python3 analyze-outcomes.py
"""

from __future__ import annotations

import json
import math
import pathlib
import random
import statistics

HERE = pathlib.Path(__file__).resolve().parent
SEED = 20260731
PERMUTATIONS = 20000

PRODUCTIVE = {"merged"}
NON_PRODUCTIVE = {"empty-merge", "abandoned"}


# --- statistics -------------------------------------------------------------

def fisher_exact(a: int, b: int, c: int, d: int) -> float:
    """Two-sided Fisher exact p-value for the table [[a, b], [c, d]]."""
    row1, row2 = a + b, c + d
    col1 = a + c
    total = row1 + row2

    def prob(x: int) -> float:
        return (
            math.comb(row1, x)
            * math.comb(row2, col1 - x)
            / math.comb(total, col1)
        )

    observed = prob(a)
    lo = max(0, col1 - row2)
    hi = min(row1, col1)
    # Sum every table at most as likely as the observed one (with a tolerance
    # for float noise), which is the standard two-sided construction.
    return min(1.0, sum(
        p for x in range(lo, hi + 1)
        if (p := prob(x)) <= observed * (1 + 1e-9)
    ))


def permutation_diff_in_means(
    group_a: list[float], group_b: list[float], seed: int = SEED
) -> dict:
    """Two-sided permutation test on the difference of means."""
    if not group_a or not group_b:
        return {"n_a": len(group_a), "n_b": len(group_b), "p_value": None}
    observed = statistics.fmean(group_a) - statistics.fmean(group_b)
    pool = group_a + group_b
    n_a = len(group_a)
    rng = random.Random(seed)
    extreme = 0
    for _ in range(PERMUTATIONS):
        rng.shuffle(pool)
        diff = statistics.fmean(pool[:n_a]) - statistics.fmean(pool[n_a:])
        if abs(diff) >= abs(observed) - 1e-12:
            extreme += 1
    return {
        "n_a": n_a,
        "n_b": len(group_b),
        "mean_a": round(statistics.fmean(group_a), 3),
        "mean_b": round(statistics.fmean(group_b), 3),
        "observed_diff": round(observed, 3),
        "permutations": PERMUTATIONS,
        "p_value": round((extreme + 1) / (PERMUTATIONS + 1), 4),
    }


def ranks(values: list[float]) -> list[float]:
    """Average ranks, ties shared."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        shared = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[order[k]] = shared
        i = j + 1
    return out


def spearman(xs: list[float], ys: list[float], seed: int = SEED) -> dict:
    """Spearman rho with a seeded permutation p-value."""
    if len(xs) < 3:
        return {"n": len(xs), "rho": None, "p_value": None}
    rx, ry = ranks(xs), ranks(ys)
    rho = statistics.correlation(rx, ry)
    rng = random.Random(seed)
    shuffled = list(ry)
    extreme = 0
    for _ in range(PERMUTATIONS):
        rng.shuffle(shuffled)
        if abs(statistics.correlation(rx, shuffled)) >= abs(rho) - 1e-12:
            extreme += 1
    return {
        "n": len(xs),
        "rho": round(rho, 4),
        "permutations": PERMUTATIONS,
        "p_value": round((extreme + 1) / (PERMUTATIONS + 1), 4),
    }


def wilson_ci(successes: int, n: int, z: float = 1.96) -> list[float]:
    """Wilson score interval - stays sane for the small, near-zero-rate counts
    this corpus produces, where the normal approximation does not."""
    if n == 0:
        return [0.0, 1.0]
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return [round(max(0.0, centre - half), 4), round(min(1.0, centre + half), 4)]


def min_detectable_share_gap(n_fail: int, n_prod: int) -> dict:
    """Smallest failure-group share that an exact test could separate from a
    given success-group share, at the sizes this corpus actually has."""
    out = {}
    for base in (0.02, 0.05, 0.10, 0.20):
        c = round(base * n_prod)
        needed = None
        for a in range(0, n_fail + 1):
            if fisher_exact(a, n_fail - a, c, n_prod - c) < 0.05:
                needed = round(a / n_fail, 2)
                break
        out[f"success_share_{base}"] = needed
    return out


# --- corpus helpers ---------------------------------------------------------

def load() -> dict:
    return json.loads((HERE / "corpus-metrics.json").read_text())


def joined(corpus: dict) -> list[dict]:
    """PR records joined to the specification profile of their linked issue."""
    rows = []
    for repo, data in corpus["repos"].items():
        specs = {i["number"]: i for i in data["issues"]}
        for pr in data["prs"]:
            issue = specs.get(pr.get("issue_number"))
            if issue is None:
                continue
            rows.append({
                "repo": repo,
                "pr": pr["number"],
                "pr_title": pr["title"],
                "outcome": pr["outcome"],
                "churn": pr["additions"] + pr["deletions"],
                "changed_files": pr["changed_files"],
                "commit_count": pr.get("commit_count"),
                "has_revert": pr.get("has_revert"),
                "issue": issue["number"],
                "issue_title": issue["title"],
                **{k: v for k, v in issue["spec"].items()},
            })
    return rows


def main() -> int:
    corpus = load()
    rows = joined(corpus)
    detail_features = corpus["detail_features"]
    contract_features = corpus["contract_features"]

    report: dict = {
        "source": "corpus-metrics.json",
        "collected_at": corpus["collected_at"],
        "seed": SEED,
    }

    # --- 1. outcome base rates ---------------------------------------------
    per_repo = {}
    for repo, data in corpus["repos"].items():
        counts: dict[str, int] = {}
        for pr in data["prs"]:
            counts[pr["outcome"]] = counts.get(pr["outcome"], 0) + 1
        per_repo[repo] = counts
    totals: dict[str, int] = {}
    for counts in per_repo.values():
        for k, v in counts.items():
            totals[k] = totals.get(k, 0) + v
    report["outcomes"] = {
        "per_repo": per_repo,
        "total": totals,
        "linked_to_issue": len(rows),
        "unlinked_prs": sum(len(d["prs"]) for d in corpus["repos"].values())
        - len(rows),
    }

    # --- 2. the failure set, in full ---------------------------------------
    failures = [r for r in rows if r["outcome"] in NON_PRODUCTIVE]
    unlinked_failures = [
        {"repo": repo, "pr": pr["number"], "title": pr["title"],
         "outcome": pr["outcome"], "headlines": pr.get("headlines")}
        for repo, data in corpus["repos"].items()
        for pr in data["prs"]
        if pr["outcome"] in NON_PRODUCTIVE and pr.get("issue_number") is None
    ]
    report["failure_cases"] = {
        "linked": sorted(
            (
                {
                    "repo": r["repo"], "pr": r["pr"], "issue": r["issue"],
                    "outcome": r["outcome"], "issue_title": r["issue_title"],
                    "detail_score": r["detail_score"],
                    "contract_score": r["contract_score"],
                    "length_chars": r["length_chars"],
                    "features": r["features"],
                    "commit_count": r["commit_count"],
                    "has_revert": r["has_revert"],
                }
                for r in failures
            ),
            key=lambda r: (r["repo"], r["pr"]),
        ),
        "unlinked": unlinked_failures,
    }

    # --- 3. detail vs outcome ----------------------------------------------
    prod = [r for r in rows if r["outcome"] in PRODUCTIVE]
    report["detail_vs_outcome"] = {
        "detail_score": permutation_diff_in_means(
            [r["detail_score"] for r in failures],
            [r["detail_score"] for r in prod],
        ),
        "length_chars": permutation_diff_in_means(
            [float(r["length_chars"]) for r in failures],
            [float(r["length_chars"]) for r in prod],
        ),
        "contract_score": permutation_diff_in_means(
            [r["contract_score"] for r in failures],
            [r["contract_score"] for r in prod],
        ),
        "note": (
            "group_a = non-productive (empty-merge + abandoned), "
            "group_b = merged with a real diff"
        ),
    }

    # --- 4. per-feature association with a non-productive outcome ----------
    feature_table = {}
    for feature in detail_features + contract_features:
        a = sum(1 for r in failures if feature in r["features"])
        b = len(failures) - a
        c = sum(1 for r in prod if feature in r["features"])
        d = len(prod) - c
        feature_table[feature] = {
            "kind": "contract" if feature in contract_features else "detail",
            "failures_with": a,
            "failures_without": b,
            "productive_with": c,
            "productive_without": d,
            "rate_failures": round(a / len(failures), 3) if failures else None,
            "rate_productive": round(c / len(prod), 3) if prod else None,
            "fisher_p": round(fisher_exact(a, b, c, d), 4),
        }
    report["feature_association"] = feature_table

    # --- 5. does more detail buy more delivered work? ----------------------
    merged = [r for r in prod if r["churn"] > 0]
    report["detail_vs_delivered_work"] = {
        "detail_score_vs_churn": spearman(
            [float(r["detail_score"]) for r in merged],
            [math.log10(r["churn"]) for r in merged],
        ),
        "length_vs_churn": spearman(
            [float(r["length_chars"]) for r in merged],
            [math.log10(r["churn"]) for r in merged],
        ),
        "note": "churn = additions + deletions of the merged PR, log10 scale",
    }

    # --- 6. how rare are decision contracts in practice? -------------------
    all_issues = [
        i for data in corpus["repos"].values() for i in data["issues"]
    ]
    report["contract_prevalence"] = {
        "issues_total": len(all_issues),
        "per_feature": {
            f: {
                "count": sum(1 for i in all_issues if f in i["spec"]["features"]),
                "share": round(
                    sum(1 for i in all_issues if f in i["spec"]["features"])
                    / len(all_issues), 3
                ),
            }
            for f in contract_features + detail_features
        },
        "issues_with_zero_contracts": sum(
            1 for i in all_issues if i["spec"]["contract_score"] == 0
        ),
        "issues_with_full_detail_zero_contracts": sum(
            1 for i in all_issues
            if i["spec"]["detail_score"] >= 6 and i["spec"]["contract_score"] == 0
        ),
    }

    # --- 7. quadrant view: detail x decision contracts ---------------------
    # The failure set is too small for a per-feature model, but the quadrant
    # split is the hypothesis the issue actually asks about.
    def quadrant(row: dict) -> str:
        high = "detail-high" if row["detail_score"] >= 6 else "detail-low"
        has = "contract-present" if row["contract_score"] >= 1 else "contract-absent"
        return f"{high}/{has}"

    quads: dict[str, dict] = {}
    for row in rows:
        if row["outcome"] not in PRODUCTIVE | NON_PRODUCTIVE:
            continue
        q = quads.setdefault(quadrant(row), {"n": 0, "failures": 0, "prs": []})
        q["n"] += 1
        if row["outcome"] in NON_PRODUCTIVE:
            q["failures"] += 1
            q["prs"].append(row["pr"])
    for q in quads.values():
        q["failure_rate"] = round(q["failures"] / q["n"], 4)
        q["failure_rate_ci95"] = wilson_ci(q["failures"], q["n"])
    report["quadrants"] = quads

    # --- 8. what this corpus can and cannot resolve ------------------------
    n_fail = len(failures)
    n_total = len(rows)
    report["power"] = {
        "failures": n_fail,
        "linked_prs": n_total,
        "failure_rate": round(n_fail / n_total, 4),
        "failure_rate_ci95": wilson_ci(n_fail, n_total),
        "min_detectable_share_gap": min_detectable_share_gap(n_fail, len(prod)),
        "caveat": (
            "With 10 non-productive PRs the corpus can only reveal large "
            "differences. A feature present in, say, half the failures and a "
            "tenth of the successes would be detectable; anything subtler "
            "would not be. Non-significant results here mean 'not resolved by "
            "this corpus', not 'no effect'."
        ),
    }

    out = HERE / "analysis-outcomes.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    # --- console summary ---------------------------------------------------
    print(f"outcomes: {totals}")
    print(f"linked PR->issue: {len(rows)} "
          f"(unlinked {report['outcomes']['unlinked_prs']})")
    print(f"failure set: {len(failures)} linked, {len(unlinked_failures)} unlinked")
    for key, res in report["detail_vs_outcome"].items():
        if isinstance(res, dict):
            print(f"  {key}: failures {res['mean_a']} vs merged {res['mean_b']} "
                  f"(p={res['p_value']}, n={res['n_a']}/{res['n_b']})")
    print("feature association (p < 0.2 shown):")
    for f, t in sorted(feature_table.items(), key=lambda kv: kv[1]["fisher_p"]):
        if t["fisher_p"] < 0.2:
            print(f"  [{t['kind']}] {f}: failures {t['rate_failures']} vs "
                  f"productive {t['rate_productive']} (p={t['fisher_p']})")
    print(f"detail_score vs churn: {report['detail_vs_delivered_work']['detail_score_vs_churn']}")
    print("quadrants (failure rate):")
    for q, v in sorted(quads.items()):
        print(f"  {q:34s} n={v['n']:3d} failures={v['failures']} "
              f"rate={v['failure_rate']} ci95={v['failure_rate_ci95']}")
    print(f"power: {report['power']['failure_rate']} "
          f"ci95={report['power']['failure_rate_ci95']} "
          f"mde={report['power']['min_detectable_share_gap']}")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
