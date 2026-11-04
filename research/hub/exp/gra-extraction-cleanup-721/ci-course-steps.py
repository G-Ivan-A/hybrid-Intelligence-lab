#!/usr/bin/env python3
"""CI cost of the course self-checks in the Hub validate job (issue #721).

Usage:
    python3 -I research/hub/exp/gra-extraction-cleanup-721/ci-course-steps.py <validate.yml> <jobs.jsonl>

<jobs.jsonl> — one JSON object per job, saved from
`gh api repos/G-Ivan-A/hybrid-Intelligence-lab/actions/runs/<id>/jobs --jq '.jobs[] | {name, started_at, completed_at, steps: [.steps[] | {name, started_at, completed_at}]}'`.
A step counts as a course step when its `run:` block in validate.yml mentions
research/reputation-technologies/. GitHub reports step times with 1 s resolution and may truncate long step
names (for example "Check Day 1 deck, lecturer script and gate of"), so a job
step matches a declared step when the declared name starts with it.
"""
import json
import re
import sys
from datetime import datetime

DOMAIN = "research/reputation-technologies/"


def ts(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def course_steps(yml_text):
    names, current, body = set(), None, []
    for line in yml_text.splitlines() + ["      - name: __end__"]:
        m = re.match(r"^\s*- name:\s*(.+?)\s*$", line)
        if m:
            if current and DOMAIN in "\n".join(body):
                names.add(current)
            current, body = m.group(1), []
        else:
            body.append(line)
    return names


def main(argv):
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    names = course_steps(open(argv[1], encoding="utf-8").read())
    print(f"course steps declared in validate.yml: {len(names)}")
    for line in open(argv[2], encoding="utf-8"):
        job = json.loads(line)
        total = (ts(job["completed_at"]) - ts(job["started_at"])).total_seconds()
        hit = [
            s for s in job["steps"]
            if s["started_at"] and s["completed_at"]
            and any(n == s["name"] or n.startswith(s["name"].rstrip() + " ") for n in names)
        ]
        if not hit:
            continue
        sec = sum((ts(s["completed_at"]) - ts(s["started_at"])).total_seconds() for s in hit)
        print(f"job {job['name']}: {total:.0f} s total; course steps run: {len(hit)}; course seconds: {sec:.0f} ({100 * sec / total:.0f}%)")
        for s in hit:
            print(f"  {(ts(s['completed_at']) - ts(s['started_at'])).total_seconds():>4.0f} s  {s['name']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
