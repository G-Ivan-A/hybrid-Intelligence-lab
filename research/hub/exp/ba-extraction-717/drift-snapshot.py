#!/usr/bin/env python3
"""Drift snapshot of a Hub project prepared for extraction, issue #717.

Prints a deterministic, sorted snapshot of everything the extraction
parameters (the `extraction-params` block, e.g. ba-instance-params.txt) depend
on, read at one Hub commit:

  sources  files under MAP sources, their digest and top-level target dirs
           (declared in DIR, part of the genome, or UNDECLARED)
  inbound  Hub files outside the sources that mention a source path
           (a superset of the files the tombstone task rewrites)
  ci       workflow jobs and steps that name a source path
           (declared in CI_STEP/CI_JOB, or UNDECLARED)
  backlog  ops/backlog.md sections that are declared in BACKLOG or mention
           a source path (declared, or mentions-source: decide whether it moves)
  spoke    for each --spoke working tree: links into the sources, split into
           SHA-pinned (survive the tombstone) and floating (break after it),
           and the Hub pins of compilation manifests
  target   with --target PATH: files of the target repository (stage E2
           accepts only README.md there)
  since    with --since BASE: commits and file changes in the sources

Drift between the pinned baseline and a candidate commit is the plain
`diff` of two snapshots; the `since` section lists the commits behind it.
Read-only: the script runs `git` commands and reads files, nothing else.

Usage:
  python3 -I drift-snapshot.py --params PARAMS --hub HUB_CLONE --ref REF \
      [--since BASE] [--target PATH] [--spoke NAME=PATH ...]
"""
import argparse
import hashlib
import re
import subprocess
import sys

FORMAT = "# drift-snapshot v1"
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True,
                          capture_output=True).stdout.decode("utf-8", "replace")


def read_params(path):
    params = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            key, sep, value = line.rstrip("\n").partition(": ")
            if sep and key.isupper():
                params.setdefault(key, []).append(value.strip())
    return params


def sources_of(params):
    maps = []
    for value in params.get("MAP", []):
        src, _, dst = value.partition("=")
        maps.append((src, dst))
    return maps


def pathspecs(maps):
    return [src.rstrip("/") for src, _ in maps]


def target_of(path, maps):
    for src, dst in maps:
        if src.endswith("/") and path.startswith(src):
            return dst + path[len(src):]
        if path == src:
            return dst
    return None


def section_sources(hub, ref, maps, params):
    rows = git(hub, "ls-tree", "-r", ref, "--", *pathspecs(maps)).splitlines()
    excluded = {e for e in params.get("EXCLUDE", []) if e}
    entries = []
    for row in rows:
        meta, path = row.split("\t", 1)
        mode, _kind, blob = meta.split()
        if path in excluded or any(path.startswith(e.rstrip("/") + "/") for e in excluded):
            continue
        entries.append((target_of(path, maps), blob, mode))
    entries.sort()
    digest = hashlib.sha256("".join(f"{m} {b} {t}\n" for t, b, m in entries).encode()).hexdigest()
    declared = {d.split("|", 1)[0].strip() for d in params.get("DIR", [])}
    genome = {line.split("\t", 1)[1] for line in
              git(hub, "ls-tree", ref, "templates/spoke/").splitlines()
              if line.split()[1] == "tree"}
    genome = {p[len("templates/spoke/"):] for p in genome} | {".github", "ops", "tools"}
    counts = {}
    for target, _blob, _mode in entries:
        if "/" in target:
            top = target.split("/", 1)[0]
            counts[top] = counts.get(top, 0) + 1
    out = ["## sources", f"files: {len(entries)}", f"digest: {digest}"]
    for top in sorted(counts):
        kind = "declared" if top in declared else "genome" if top in genome else "UNDECLARED"
        out.append(f"dir {top}: {counts[top]} {kind}")
    for top in sorted(declared - set(counts)):
        out.append(f"dir {top}: 0 declared-missing")
    return out


def mentions(text, specs):
    return any(spec in text for spec in specs)


def section_inbound(hub, ref, maps):
    specs = pathspecs(maps)
    args = ["grep", "-l", "-I", "-F"]
    for spec in specs:
        args += ["-e", spec]
    args += [ref, "--", "."] + [f":!{spec}" for spec in specs]
    try:
        files = git(hub, *args).splitlines()
    except subprocess.CalledProcessError:
        files = []
    files = sorted(f.split(":", 1)[1] for f in files)
    return ["## inbound", f"files: {len(files)}"] + files


def workflow_blocks(text):
    """Yield (job, step or None, block text) for a GitHub Actions workflow."""
    job, step, block, in_jobs = None, None, [], False
    for line in text.splitlines() + ["jobs-end:"]:
        top = re.match(r"^(\S[^:]*):", line)
        job_head = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line) if in_jobs else None
        step_head = re.match(r"^\s+- name:\s*(.+?)\s*$", line) if job else None
        if top or job_head or step_head:
            if job:
                yield job, step, "\n".join(block)
            block = []
            if top:
                in_jobs = top.group(1) == "jobs"
                job, step = None, None
            elif job_head:
                job, step = job_head.group(1), None
            else:
                step = step_head.group(1).strip("'\"")
        block.append(line)


def section_ci(hub, ref, maps, params):
    specs = pathspecs(maps)
    try:
        text = git(hub, "show", f"{ref}:.github/workflows/validate.yml")
    except subprocess.CalledProcessError:
        text = ""
    steps_declared = set(params.get("CI_STEP", []))
    jobs_declared = set(params.get("CI_JOB", []))
    found_steps, found_jobs = set(), set()
    for job, step, block in workflow_blocks(text):
        if mentions(block, specs):
            found_jobs.add(job)
            if step is not None:
                found_steps.add(f"{job} / {step}")
        if step is not None and f"{job} / {step}" in steps_declared:
            found_steps.add(f"{job} / {step}")
    out = ["## ci"]
    for job in sorted(found_jobs | (jobs_declared & {j for j, _s, _b in workflow_blocks(text)})):
        out.append(f"job {job}: {'declared' if job in jobs_declared else 'step-level'}")
    for step in sorted(found_steps):
        job = step.split(" / ", 1)[0]
        kind = "declared" if step in steps_declared or job in jobs_declared else "UNDECLARED"
        out.append(f"step {step}: {kind}")
    all_steps = {f"{j} / {s}" for j, s, _b in workflow_blocks(text) if s is not None}
    all_jobs = {j for j, _s, _b in workflow_blocks(text)}
    for step in sorted(steps_declared - all_steps):
        out.append(f"step {step}: declared-missing")
    for job in sorted(jobs_declared - all_jobs):
        out.append(f"job {job}: declared-missing")
    return out


def section_backlog(hub, ref, maps, params):
    specs = pathspecs(maps)
    try:
        text = git(hub, "show", f"{ref}:ops/backlog.md")
    except subprocess.CalledProcessError:
        text = ""
    declared = params.get("BACKLOG", [])
    sections, heading, body = [], None, []
    for line in text.splitlines() + ["## "]:
        if line.startswith("## "):
            if heading is not None:
                sections.append((heading, "\n".join(body)))
            heading, body = line, []
        else:
            body.append(line)
    out = ["## backlog"]
    seen = set()
    for heading, body in sections:
        prefix = next((d for d in declared if heading.startswith(d)), None)
        rows = len(re.findall(r"^\| \*\*B-\d+\*\*", body, re.M))
        if prefix:
            seen.add(prefix)
            out.append(f"section {heading}: declared rows={rows}")
        elif mentions(body, specs):
            out.append(f"section {heading}: mentions-source rows={rows}")
    for prefix in declared:
        if prefix not in seen:
            out.append(f"section {prefix}: declared-missing")
    return out


def section_spoke(name, path, maps):
    alt = "|".join(re.escape(spec) for spec in pathspecs(maps))
    link = re.compile(r"(?:github\.com/G-Ivan-A/hybrid-Intelligence-lab/(?:blob|tree|raw)"
                      r"|raw\.githubusercontent\.com/G-Ivan-A/hybrid-Intelligence-lab)"
                      rf"/([^/\s)\]>'\"]+)/(?:{alt})", re.I)
    head = git(path, "rev-parse", "HEAD").strip()
    pinned, floating, pins = 0, {}, []
    for rel in sorted(git(path, "ls-files", "-z").split("\0")):
        if not rel:
            continue
        try:
            with open(f"{path}/{rel}", "rb") as fh:
                data = fh.read()
        except OSError:
            continue
        if b"\0" in data[:8192]:
            continue
        text = data.decode("utf-8", "replace")
        for ref in link.findall(text):
            if SHA40.match(ref.lower()):
                pinned += 1
            else:
                floating[rel] = floating.get(rel, 0) + 1
        if rel.endswith("compilation-manifest.yaml"):
            for line in text.splitlines():
                if re.match(r"^hub_commit:\s*\S", line):
                    pins.append(f"pin {rel}: {line.split(':', 1)[1].strip()}")
    out = [f"## spoke {name}", f"head: {head}", f"pinned-links: {pinned}",
           f"floating-links: {sum(floating.values())} in {len(floating)} file(s)"]
    out += [f"floating {rel}: {count}" for rel, count in sorted(floating.items())]
    return out + pins


def section_target(path):
    files = sorted(f for f in git(path, "ls-files", "-z").split("\0") if f)
    verdict = "ok" if files in ([], ["README.md"]) else "NOT-EMPTY"
    return (["## target", f"head: {git(path, 'rev-parse', 'HEAD').strip()}",
             f"files: {len(files)} {verdict}"] + files)


def section_since(hub, base, ref, maps):
    specs = pathspecs(maps)
    commits = git(hub, "log", "--no-merges", "--abbrev=12", "--format=%h %ad %s", "--date=short",
                  f"{base}..{ref}", "--", *specs).splitlines()
    changed = git(hub, "diff", "--name-status", base, ref, "--", *specs).splitlines()
    return ([f"## since {base}", f"commits: {len(commits)}"] + commits +
            [f"changed: {len(changed)}"] + changed)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--params", required=True)
    parser.add_argument("--hub", required=True, help="Hub git repository")
    parser.add_argument("--ref", required=True, help="Hub commit to snapshot")
    parser.add_argument("--since", help="baseline Hub commit for the since section")
    parser.add_argument("--target", help="working tree of the target repository")
    parser.add_argument("--spoke", action="append", default=[], metavar="NAME=PATH",
                        help="working tree of an ecosystem repository")
    args = parser.parse_args()
    params = read_params(args.params)
    maps = sources_of(params)
    if not maps:
        sys.exit("drift-snapshot: no MAP lines in the parameter block")
    ref = git(args.hub, "rev-parse", "--verify", f"{args.ref}^{{commit}}").strip()
    out = [FORMAT, f"hub_ref: {ref}"]
    out += section_sources(args.hub, ref, maps, params)
    out += section_inbound(args.hub, ref, maps)
    out += section_ci(args.hub, ref, maps, params)
    out += section_backlog(args.hub, ref, maps, params)
    if args.target:
        out += section_target(args.target)
    for spec in args.spoke:
        name, _, path = spec.partition("=")
        out += section_spoke(name, path, maps)
    if args.since:
        out += section_since(args.hub, args.since, ref, maps)
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
