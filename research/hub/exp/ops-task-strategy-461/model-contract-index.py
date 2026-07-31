#!/usr/bin/env python3
"""Direction 3: model the contract index and measure where it earns its keep.

The hypothesis proposes an entry point carrying decision contracts. This script
does not argue about it; it implements the contract set as an executable checker
and replays it over the real corpus of 475 issues and 479 pull requests to see
what it would have caught and what it would have cost.

Two placements of the same contract are modelled, because they behave nothing
alike:

  issue-time gate      Refuse to start a task whose statement lacks the decision
                       contracts. Cheap to state, but every issue it flags is a
                       human interruption, so its cost is the false-positive
                       count on the 468 tasks that finished fine.

  pull-request-time    Check the mechanical postcondition instead of the prose
  postcondition        precondition: a PR closing an issue must carry a non-empty
                       diff. It cannot be satisfied by wording, only by work.

The comparison is the finding. A precondition on prose and a postcondition on
artifacts aim at the same failure and differ by an order of magnitude in cost.

Usage:
    python3 model-contract-index.py
"""

from __future__ import annotations

import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

# Outcomes that represent work that did not land. `open` is excluded: it has not
# failed yet, and counting a pending PR as a failure would flatter any detector.
NON_PRODUCTIVE = {"empty-merge", "abandoned"}

CONTRACT_CLAUSES = ["verification_rule", "escalation_rule",
                    "autonomy_rule", "nonempty_rule"]


def wilson_ci(successes: int, total: int, z: float = 1.96) -> list[float]:
    """Wilson score interval — honest at the small counts this corpus has."""
    if total == 0:
        return [0.0, 0.0]
    phat = successes / total
    denom = 1 + z * z / total
    centre = (phat + z * z / (2 * total)) / denom
    margin = (z * ((phat * (1 - phat) / total
                    + z * z / (4 * total * total)) ** 0.5)) / denom
    return [round(max(0.0, centre - margin), 4),
            round(min(1.0, centre + margin), 4)]


def load() -> tuple[list[dict], dict]:
    """Flatten the corpus into PR records joined to their issue's spec."""
    metrics = json.loads((HERE / "corpus-metrics.json").read_text())
    joined = []
    specs: dict[tuple[str, int], dict] = {}
    for repo, data in metrics["repos"].items():
        for issue in data["issues"]:
            specs[(repo, issue["number"])] = issue["spec"]
        for pr in data["prs"]:
            spec = specs.get((repo, pr.get("issue_number")))
            joined.append({
                "repo": repo,
                "pr": pr["number"],
                "issue": pr.get("issue_number"),
                "outcome": pr["outcome"],
                "churn": pr.get("additions", 0) + pr.get("deletions", 0),
                "changed_files": pr.get("changed_files"),
                "spec": spec,
                "features": set(spec["features"]) if spec else set(),
                "detail_score": spec["detail_score"] if spec else None,
            })
    return joined, metrics


def gate_at_issue_time(records: list[dict], required: list[str]) -> dict:
    """Flag any linked task whose statement lacks every required clause.

    Modelled as fail-closed: the gate stops the task unless the contract is
    stated. Records without a linked issue are skipped rather than assumed
    compliant — an unlinked PR is a different defect, measured elsewhere.
    """
    scored = [r for r in records if r["spec"] is not None
              and r["outcome"] != "open"]
    flagged = [r for r in scored
               if not any(c in r["features"] for c in required)]
    failures = [r for r in scored if r["outcome"] in NON_PRODUCTIVE]
    caught = [r for r in flagged if r["outcome"] in NON_PRODUCTIVE]
    false_positives = [r for r in flagged
                       if r["outcome"] not in NON_PRODUCTIVE]

    return {
        "required_any_of": required,
        "evaluated": len(scored),
        "flagged": len(flagged),
        "flag_rate": round(len(flagged) / len(scored), 4) if scored else None,
        "failures_total": len(failures),
        "failures_caught": len(caught),
        "recall": round(len(caught) / len(failures), 4) if failures else None,
        "false_positives": len(false_positives),
        "precision": (round(len(caught) / len(flagged), 4)
                      if flagged else None),
        "precision_ci95": wilson_ci(len(caught), len(flagged)),
        "human_interruptions_per_failure_caught": (
            round(len(false_positives) / len(caught), 1) if caught else None),
    }


def postcondition_at_pr_time(records: list[dict]) -> dict:
    """Flag a merged PR that closes an issue but changes nothing.

    This is not a judgement about the task statement. It is arithmetic on the
    diff, so it has no opinion to be wrong about: a merged PR with zero changed
    files did not deliver the work its issue described.
    """
    merged = [r for r in records if r["outcome"] in {"merged", "empty-merge"}]
    flagged = [r for r in merged if r["outcome"] == "empty-merge"]
    empty_merges = len(flagged)

    # False positives would be genuinely empty-but-correct merges. Every empty
    # merge in this corpus is listed so a human can check that claim rather than
    # take it on trust.
    return {
        "rule": "a merged PR closing an issue must change at least one file",
        "evaluated": len(merged),
        "flagged": empty_merges,
        "flag_rate": round(empty_merges / len(merged), 4) if merged else None,
        "false_positives_by_construction": 0,
        "flagged_prs": [
            {"repo": r["repo"], "pr": r["pr"], "issue": r["issue"],
             "changed_files": r["changed_files"], "churn": r["churn"],
             "detail_score": r["detail_score"],
             "contracts_present": sorted(
                 c for c in CONTRACT_CLAUSES if c in r["features"])}
            for r in sorted(flagged, key=lambda r: r["pr"])
        ],
        "share_of_all_non_productive": None,
    }


def zero_diff_at_close(records: list[dict]) -> dict:
    """The same arithmetic widened from merges to every closed pull request.

    Six of the ten non-productive pull requests changed no file at all — four
    merged empty, two closed empty. Widening the check from `merged` to `closed`
    therefore raises coverage by half again. Unlike the merge-time variant this
    one is not free of false positives: a task can be cancelled deliberately,
    and a deliberately cancelled task also closes with an empty diff. The check
    cannot tell the two apart, so it is a signal for review, not a gate.
    """
    closed = [r for r in records if r["outcome"] != "open"]
    flagged = [r for r in closed if not r["churn"] and not r["changed_files"]]
    return {
        "rule": "a closed PR linked to an issue changed no file",
        "caveat": zero_diff_at_close.__doc__.strip().split("\n\n")[-1],
        "evaluated": len(closed),
        "flagged": len(flagged),
        "flag_rate": round(len(flagged) / len(closed), 4) if closed else None,
        "cases": [
            {"repo": r["repo"], "pr": r["pr"], "issue": r["issue"],
             "outcome": r["outcome"], "detail_score": r["detail_score"]}
            for r in sorted(flagged, key=lambda r: r["pr"])
        ],
    }


def abandonment_shape(records: list[dict]) -> dict:
    """What the postcondition cannot see: work that never reached a merge."""
    abandoned = [r for r in records if r["outcome"] == "abandoned"]
    return {
        "abandoned": len(abandoned),
        "note": (
            "A PR-time postcondition only fires on merges. Abandoned pull "
            "requests close without merging, so they pass every artifact check "
            "by never producing an artifact. This is the residual the "
            "postcondition does not address and the reason it is a floor, not "
            "a complete answer."
        ),
        "cases": [
            {"repo": r["repo"], "pr": r["pr"], "issue": r["issue"],
             "churn": r["churn"], "detail_score": r["detail_score"],
             "contracts_present": sorted(
                 c for c in CONTRACT_CLAUSES if c in r["features"])}
            for r in sorted(abandoned, key=lambda r: r["pr"])
        ],
    }


def coverage_cost(records: list[dict]) -> dict:
    """How much of today's practice each candidate gate would interrupt."""
    scored = [r for r in records if r["spec"] is not None
              and r["outcome"] != "open"]
    rows = []
    for clause in CONTRACT_CLAUSES + ["any_contract"]:
        if clause == "any_contract":
            present = [r for r in scored if r["features"] & set(CONTRACT_CLAUSES)]
        else:
            present = [r for r in scored if clause in r["features"]]
        rows.append({
            "clause": clause,
            "present_in": len(present),
            "share_of_corpus": round(len(present) / len(scored), 4),
            "would_interrupt": len(scored) - len(present),
        })
    return {"evaluated": len(scored), "clauses": rows}


def main() -> int:
    records, _ = load()

    gates = [
        gate_at_issue_time(records, ["nonempty_rule"]),
        gate_at_issue_time(records, ["autonomy_rule", "escalation_rule"]),
        gate_at_issue_time(records, CONTRACT_CLAUSES),
    ]
    postcondition = postcondition_at_pr_time(records)
    widened = zero_diff_at_close(records)
    residual = abandonment_shape(records)

    non_productive = sum(
        1 for r in records if r["outcome"] in NON_PRODUCTIVE)
    postcondition["share_of_all_non_productive"] = (
        round(postcondition["flagged"] / non_productive, 4)
        if non_productive else None)

    report = {
        "model": "contract index — issue-time gate vs PR-time postcondition",
        "corpus": {
            "pull_requests": len(records),
            "non_productive": non_productive,
        },
        "issue_time_gates": gates,
        "pr_time_postcondition": postcondition,
        "pr_time_zero_diff_at_close": widened,
        "residual_not_covered": residual,
        "adoption_cost": coverage_cost(records),
        "conclusion_inputs": {
            "why_gates_are_expensive": (
                "Decision contracts appear in a small minority of task "
                "statements, so a fail-closed precondition on their presence "
                "flags most of the corpus. Its recall on real failures is high "
                "only because it flags nearly everything, which is not "
                "detection."
            ),
            "why_the_postcondition_is_cheap": (
                "It fires on an arithmetic property of the delivered diff, "
                "needs no wording in the task, and cannot misread prose."
            ),
        },
    }

    out = HERE / "model-contract-index.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    print(f"corpus: {len(records)} PRs, {non_productive} non-productive\n")
    print("issue-time gates (fail-closed on missing contract):")
    for gate in gates:
        print(f"  require any of {'+'.join(gate['required_any_of']):55s}")
        print(f"    flags {gate['flagged']:3d}/{gate['evaluated']} "
              f"({gate['flag_rate']:.1%})  recall={gate['recall']}  "
              f"precision={gate['precision']}  "
              f"interruptions per catch="
              f"{gate['human_interruptions_per_failure_caught']}")
    print("\nPR-time postcondition (non-empty diff):")
    print(f"  flags {postcondition['flagged']}/{postcondition['evaluated']} "
          f"({postcondition['flag_rate']:.2%})  "
          f"false positives={postcondition['false_positives_by_construction']}"
          f"  covers {postcondition['share_of_all_non_productive']:.0%} of "
          f"non-productive PRs")
    widened_share = widened["flagged"] / non_productive
    print(f"\nPR-time zero diff at close (merged or closed):")
    print(f"  flags {widened['flagged']}/{widened['evaluated']} "
          f"({widened['flag_rate']:.2%})  covers {widened_share:.0%} of "
          f"non-productive PRs, but cannot distinguish a cancelled task")
    print(f"\nresidual: {residual['abandoned']} abandoned PRs no artifact "
          f"check can see")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
