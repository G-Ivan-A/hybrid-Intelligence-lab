#!/usr/bin/env python3
"""Exact gate-convergence model and source/stress-test checks for issue #757.

No network, LLM, vendor SDK or randomness. Probabilities are exact fractions.
--write records results.json; --check recomputes and compares with the record.
"""

import argparse
import hashlib
import json
import re
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SURVEY = ROOT.parent.parent / "2026-11-28-digital-employee-methodology-survey.md"
SELF_REPO = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab"
JUDGES = 3
DEFECT_RATE = F(1, 5)
FALSE_ALARM = F(1, 10)
MISS_RATES = {"optimistic": F(1, 5), "agreeable": F(3, 4)}
COMMON_MODE = [F(0), F(3, 10), F(3, 5), F(9, 10)]
POLICIES = ("single", "majority", "unanimous_or_escalate")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def show(value):
    """Exact fraction plus a rounded decimal for readers."""
    return {"exact": f"{value.numerator}/{value.denominator}", "approx": round(float(value), 4)}


def pass_count(n, p_pass, rho):
    """P(k of n judges pass) under a common-mode mixture.

    With probability rho the whole panel shares one verdict (common mode);
    otherwise judges are conditionally independent with pass probability p_pass.
    """
    dist = [F(0)] * (n + 1)
    dist[n] += rho * p_pass
    dist[0] += rho * (1 - p_pass)
    for k in range(n + 1):
        dist[k] += (1 - rho) * comb(n, k) * p_pass ** k * (1 - p_pass) ** (n - k)
    require(sum(dist) == 1, "Distribution must sum to 1")
    return dist


def decide(policy, k, n):
    """Return 'pass', 'fail' or 'escalate' for k passing votes of n."""
    if policy == "single":
        return "pass" if k == n else "fail"
    if policy == "majority":
        return "pass" if 2 * k > n else "fail"
    if policy == "unanimous_or_escalate":
        if k == n:
            return "pass"
        return "fail" if k == 0 else "escalate"
    raise ValueError(policy)


def gate_metrics(policy, miss, rho, false_alarm=FALSE_ALARM):
    n = 1 if policy == "single" else JUDGES
    bad = pass_count(n, miss, rho)
    good = pass_count(n, 1 - false_alarm, rho)
    out = {"defective": {"pass": F(0), "fail": F(0), "escalate": F(0)},
           "good": {"pass": F(0), "fail": F(0), "escalate": F(0)}}
    for k in range(n + 1):
        out["defective"][decide(policy, k, n)] += bad[k]
        out["good"][decide(policy, k, n)] += good[k]
    # A human reviewer of escalations is assumed perfect: an upper bound on benefit.
    auto_false_pass = DEFECT_RATE * out["defective"]["pass"]
    auto_false_reject = (1 - DEFECT_RATE) * out["good"]["fail"]
    escalation = DEFECT_RATE * out["defective"]["escalate"] + (1 - DEFECT_RATE) * out["good"]["escalate"]
    accepted = DEFECT_RATE * out["defective"]["pass"] + (1 - DEFECT_RATE) * out["good"]["pass"]
    return {
        "defect_pass_probability": out["defective"]["pass"],
        "false_pass_share_of_all_items": auto_false_pass,
        "defective_share_among_auto_accepted": auto_false_pass / accepted,
        "good_rejected_share_of_all_items": auto_false_reject,
        "human_escalation_rate": escalation,
    }


def gate_model():
    table = []
    for (label, miss), rho, policy in product(MISS_RATES.items(), COMMON_MODE, POLICIES):
        m = gate_metrics(policy, miss, rho)
        table.append({"miss_scenario": label, "miss_rate": show(miss), "common_mode": show(rho),
                      "policy": policy, **{key: show(value) for key, value in m.items()}})
    return table


def gate_probes():
    probes = []

    def record(identifier, perspective, observation, condition):
        require(condition, identifier + ": unexpected observation")
        probes.append({"id": identifier, "perspective": perspective, "observation": observation})

    opt, agr = MISS_RATES["optimistic"], MISS_RATES["agreeable"]
    single = gate_metrics("single", opt, F(0))["defect_pass_probability"]
    unanimous = gate_metrics("unanimous_or_escalate", opt, F(0))["defect_pass_probability"]
    record("G-1", "architecture",
           "Independent judges (rho=0): unanimity lowers defect pass from 1/5 to 1/125",
           single == F(1, 5) and unanimous == F(1, 125))
    full = gate_metrics("unanimous_or_escalate", opt, F(1))["defect_pass_probability"]
    record("G-2", "architecture",
           "Full common mode (rho=1): a 3-judge panel is exactly as weak as one judge",
           full == single)
    high = gate_metrics("unanimous_or_escalate", opt, F(9, 10))["defect_pass_probability"]
    record("G-3", "operations",
           "rho=9/10 keeps defect pass at 113/625 (~0.18), close to a single judge",
           high == F(9, 10) * opt + F(1, 10) * opt ** 3 and high == F(113, 625))
    agreeable = gate_metrics("unanimous_or_escalate", agr, F(0))["defect_pass_probability"]
    record("G-4", "security",
           "Agreeable judges (miss 3/4) pass 27/64 of defects even when unanimous and independent",
           agreeable == F(27, 64))
    maj_opt = gate_metrics("majority", opt, F(0))
    una_opt = gate_metrics("unanimous_or_escalate", opt, F(0))
    record("G-5", "human-governance",
           "Unanimity-or-escalate buys lower false pass with a measurable human load",
           una_opt["false_pass_share_of_all_items"] < maj_opt["false_pass_share_of_all_items"]
           and una_opt["human_escalation_rate"] > 0)
    maj_agr = gate_metrics("majority", agr, F(0))["defect_pass_probability"]
    record("G-6", "security",
           "Reverse Condorcet: with miss 3/4 an independent majority passes 27/32 of defects, worse than one judge",
           maj_agr == F(27, 32) and maj_agr > agr)
    # Smallest human-labelled sample estimating a judge miss rate within +-0.1 at ~95%
    # (normal approximation, worst case p=1/2, z=1.96).
    z, half_width = F(196, 100), F(1, 10)
    needed = z * z * F(1, 4) / (half_width * half_width)
    sample = -(-needed.numerator // needed.denominator)
    record("G-7", "operations",
           "Calibrating a miss rate to +-0.1 needs at least 97 labelled defective items",
           sample == 97)
    # Zero misses observed on n defective items bounds the panel miss rate below p at 95%
    # only when (1 - p)^n <= 1/20 (exact form of the "rule of three", n ~ 3/p).
    def zero_miss_sample(p):
        n, survive = 0, F(1)
        while survive > F(1, 20):
            n, survive = n + 1, survive * (1 - p)
        return n
    panel_1, panel_5 = zero_miss_sample(F(1, 100)), zero_miss_sample(F(1, 20))
    record("G-8", "operations",
           "Showing a panel misses <=1% (<=5%) of defects with zero observed misses needs 299 (59) "
           "labelled defective items; 97 only calibrates one judge",
           panel_1 == 299 and panel_5 == 59 and panel_1 > sample)
    # Unanimous-or-escalate defect pass is linear in rho: rho*p + (1-rho)*p^3. The largest
    # tolerable common mode for a target pass rate follows from that line, not from a fixed 0.6.
    target = F(1, 10)
    rho_star = (target - opt ** 3) / (opt - opt ** 3)
    record("G-9", "architecture",
           "For optimistic judges and a 1/10 target defect pass the tolerable common mode is rho <= 23/48 (~0.48)",
           rho_star == F(23, 48)
           and gate_metrics("unanimous_or_escalate", opt, rho_star)["defect_pass_probability"] == target)
    # Defect pass never depends on the false-alarm rate; that rate only moves escalations.
    alt = F(1, 25)
    record("G-10", "security",
           "Reverse Condorcet does not depend on the false-alarm rate (27/32 at 1/10 and 1/25); "
           "it holds only for identical independent judges with miss > 1/2",
           gate_metrics("majority", agr, F(0), alt)["defect_pass_probability"] == maj_agr
           and gate_metrics("majority", F(2, 5), F(0))["defect_pass_probability"] < F(2, 5))
    return probes, sample


GATE_ROW = re.compile(r"^\|\s*(оптимистичный|соглашательский)\s*\|\s*([\d,]+)\s*\|"
                      r"\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|\s*$")
SCENARIO = {"оптимистичный": "optimistic", "соглашательский": "agreeable"}


def table_checks(text):
    """The hand-written gate table in the survey must match the model to three decimals."""
    rows = 0
    for line in text.splitlines():
        match = GATE_ROW.match(line.strip())
        if not match:
            continue
        label, rho, *cells = match.groups()
        miss, rho = MISS_RATES[SCENARIO[label]], F(rho.replace(",", "."))
        model = [gate_metrics(p, miss, rho)["defect_pass_probability"] for p in POLICIES]
        model.append(gate_metrics("unanimous_or_escalate", miss, rho)["human_escalation_rate"])
        expected = [f"{float(v):.3f}".replace(".", ",") for v in model]
        require(cells == expected, f"Survey gate row {label} rho={rho} {cells} != model {expected}")
        rows += 1
    require(rows >= 6, "Survey gate table (section 5.2) not found")
    return rows


STRESS_ROW = re.compile(r"^\|\s*(H\d+)-(\d+)\s*\|.*\|\s*(✅|⚠️|❌)[^|]*\|\s*$")
URL = re.compile(r"https?://[^\s)>\]\"'`]+")
BRACKET = re.compile(r"\[([^\]\[]+)\](?!\()")
SOURCE_ID = re.compile(r"\b([ABCDEX]\d{2}[a-z]?)\b")


def survey_checks(sources):
    text = SURVEY.read_text(encoding="utf-8")
    counts = {}
    for line in text.splitlines():
        match = STRESS_ROW.match(line.strip())
        if match:
            verdicts = counts.setdefault(match.group(1), {"✅": 0, "⚠️": 0, "❌": 0})
            verdicts[match.group(3)] += 1
    require(counts, "No stress-test rows found in the survey")
    for hypothesis, verdicts in counts.items():
        require(sum(verdicts.values()) >= 5, hypothesis + ": fewer than five stress tests")
    known = {s["url"].rstrip("/") for s in sources}
    urls = sorted({u.rstrip(".,;:").rstrip("/") for u in URL.findall(text)})
    external = [u for u in urls if not u.startswith(SELF_REPO)]
    missing = [u for u in external if u not in known]
    require(not missing, "Survey URLs absent from sources.json: " + ", ".join(missing))
    require(sorted(counts, key=lambda h: int(h[1:])) == [f"H{i}" for i in range(1, 9)],
            "Expected stress tests for founder hypotheses H1-H8")
    registered = {s["id"] for s in sources} | {a for s in sources for a in s.get("aliases", [])}
    cited = {i for group in BRACKET.findall(text) for i in SOURCE_ID.findall(group)}
    unknown = sorted(cited - registered)
    require(not unknown, "Cited source ids absent from sources.json: " + ", ".join(unknown))
    return {
        "gate_table_rows_matching_model": table_checks(text),
        "stress_tests": {h: counts[h] for h in sorted(counts, key=lambda h: int(h[1:]))},
        "stress_tests_total": sum(sum(v.values()) for v in counts.values()),
        "external_urls_in_survey": len(external),
        "external_urls_missing_from_sources": 0,
        "cited_source_ids": len(cited),
        "cited_source_ids_unknown": 0,
        "registered_sources_not_cited": sorted(
            s["id"] for s in sources if not ({s["id"], *s.get("aliases", [])} & cited)),
    }


def source_checks():
    path = ROOT / "sources.json"
    sources = json.loads(path.read_text(encoding="utf-8"))
    ids = [s["id"] for s in sources]
    require(len(ids) == len(set(ids)), "Duplicate source id")
    urls = [s["url"].rstrip("/") for s in sources]
    require(len(urls) == len(set(urls)), "Duplicate source URL")
    for s in sources:
        require(s["url"].startswith("https://"), s["id"] + ": URL must be https")
        require(s["quotes"] and all(q.strip() for q in s["quotes"]), s["id"] + ": empty quotes")
        require(isinstance(s["verified"], bool), s["id"] + ": verified must be boolean")
        require(s["stance"] in {"supports", "contradicts", "conditional", "context"},
                s["id"] + ": unknown stance")
    stance = {}
    for s in sources:
        stance[s["stance"]] = stance.get(s["stance"], 0) + 1
    summary = {
        "sources_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "sources": len(sources),
        "verified": sum(s["verified"] for s in sources),
        "unverified": [s["id"] for s in sources if not s["verified"]],
        "by_stance": dict(sorted(stance.items())),
    }
    return sources, summary


def run():
    sources, source_summary = source_checks()
    probes, sample = gate_probes()
    return {
        "kind": "deterministic analytic model and document checks; no LLM, no benchmark",
        "assumptions": {
            "judges": JUDGES,
            "defect_rate": show(DEFECT_RATE),
            "false_alarm_rate": show(FALSE_ALARM),
            "miss_rates": {k: show(v) for k, v in MISS_RATES.items()},
            "common_mode_values": [show(v) for v in COMMON_MODE],
            "human_review_of_escalations": "assumed perfect (upper bound on gate benefit)",
        },
        "gate_model": gate_model(),
        "probes": probes,
        "calibration_sample_min": sample,
        "sources": source_summary,
        "survey": survey_checks(sources),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = run()
    target = ROOT / "results.json"
    if args.write:
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        require(result == json.loads(target.read_text(encoding="utf-8")),
                "Recorded results differ; investigate before regenerating")
    survey = result["survey"]
    print(f"{len(result['probes'])}/{len(result['probes'])} gate probes passed; {result['sources']['sources']} sources "
          f"({result['sources']['verified']} verified); {survey['stress_tests_total']} stress tests "
          f"across {len(survey['stress_tests'])} hypotheses; results "
          + ("written" if args.write else "verified"))


if __name__ == "__main__":
    main()
