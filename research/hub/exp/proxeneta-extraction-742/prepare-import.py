#!/usr/bin/env python3
"""Prepare an OFFLINE import; never push, merge, delete Hub sources or change visibility.

Requires git-filter-repo 2.47.0 and a local clone of the destination repository.
All imported bytes and link transformations use the pinned Hub extraction tool.
"""
import argparse
import collections
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
HUB = HERE.parents[3]
TARGET_URL = "https://github.com/G-Ivan-A/aether-orbis-proxeneta"
BRANCH = "issue-742-ecf948625d8a"
DAY = "2026-11-17"


def run(*args, cwd=HUB, capture=False):
    result = subprocess.run(list(map(str, args)), cwd=cwd, check=True,
                            stdout=subprocess.PIPE if capture else None, text=True)
    return result.stdout if capture else None


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-base", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True, help="new directory outside the Hub")
    parser.add_argument("--filter-repo", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    if out.is_relative_to(HUB) or out.exists():
        parser.error("--out must be a new directory outside the Hub")
    params = collections.defaultdict(list)
    for line in (HERE / "extraction-params.txt").read_text().splitlines():
        key, value = line.split(":", 1)
        params[key].append(value.strip())
    sha = params["HUB_SHA"][0]
    hub_url = "https://github.com/" + params["HUB_REPO"][0]
    run("git", "merge-base", "--is-ancestor", sha, "origin/main")
    run("bash", "tools/check-extraction-freeze.sh", HERE / "extraction-params.txt")
    # Match the observed, empty destination. Refuse to overwrite new human work.
    base = args.target_base.resolve()
    if run("git", "status", "--porcelain", cwd=base, capture=True).strip():
        parser.error("destination base has uncommitted changes")
    if run("git", "ls-tree", "-r", "--name-only", "HEAD", cwd=base, capture=True) != "README.md\n":
        parser.error("destination is no longer README-only; reconcile before import")
    if run("git", "show", "HEAD:README.md", cwd=base, capture=True) != "# aether-orbis-proxeneta\n[add]\n":
        parser.error("destination README changed from the observed placeholder; reconcile before import")
    out.mkdir()
    tool = out / "spoke-extraction.py"
    tool.write_text(run("git", "show", f"{sha}:tools/spoke-extraction.py", capture=True))

    def x(*argv, capture=False):
        return run(sys.executable, "-I", tool, "--hub", HUB, *argv, capture=capture)

    maps = [item for value in params["MAP"] for item in ("--map", value)]
    manifest = out / "manifest.tsv"
    x("manifest", "--sha", sha, *maps, "-o", manifest)
    if manifest.read_bytes() != (HERE / "manifest.tsv").read_bytes():
        raise RuntimeError("checked-in manifest drift")
    target = out / "target"
    run("git", "clone", "--quiet", "--no-local", base, target)
    run("git", "switch", "--quiet", "-c", BRANCH, cwd=target)
    run("git", "config", "user.name", "Codex local preparation", cwd=target)
    run("git", "config", "user.email", "codex-local@example.invalid", cwd=target)
    # A local clone's origin is a filesystem path; no credential or remote write is needed.
    genome = out / "genome.tsv"
    x("manifest", "--sha", sha, "--map", "templates/spoke/=",
      "--map", "templates/htom/.github/ISSUE_TEMPLATE/=.github/ISSUE_TEMPLATE/",
      "--map", "templates/htom/tools/validate-agents-bootstrap.sh=tools/validate-agents-bootstrap.sh",
      "--exclude", "templates/spoke/README.md", "-o", genome)
    def targets(path):
        return {line.split("\t")[2] for line in path.read_text().splitlines() if not line.startswith("#")}
    if targets(genome) & targets(manifest):
        raise RuntimeError("genome/import collision")
    x("materialize", "--manifest", genome, "--target", target,
      "--substitute", "project_name=aether-orbis-proxeneta", "--substitute", f"hub_url={hub_url}",
      "--substitute", f"date={DAY}")
    profile = json.loads((target / ".hub-profile.json").read_text())
    profile["project_specific_directories"] = [dict(zip(("path", "reason"), map(str.strip, row.split("|", 1))))
                                               for row in params["DIR"]]
    profile["last_sync"] = {"hub_sha": sha, "date": DAY, "scope": "genome",
                            "tool": "tools/spoke-extraction.py@" + sha[:12]}
    write_json(target / ".hub-profile.json", profile)
    evid = target / "docs" / "import" / ("hub-" + sha[:12])
    evid.mkdir(parents=True)
    for path in (manifest, genome):
        (evid / path.name).write_bytes(path.read_bytes())
    run("bash", "tools/validate-agents-bootstrap.sh", target, cwd=target)
    agents = target / "AGENTS.md"
    text = agents.read_text()
    text = re.sub(r"^<project_specific_rules>.*?^</project_specific_rules>", """<project_specific_rules>
1. Strategy, market research and income-trajectory evidence belong only in this repository after PRIVATE visibility is verified. Do not publish these artifacts or new commercial data in the Hub.
2. Preserve the imported project and research paths; reusable Hub rules remain linked by absolute URLs.
3. Agents may optimise execution inside the task; widening the product boundary requires an explicit owner decision. Synthetic reference data must be labelled and kept with the producing experiment.
</project_specific_rules>""", text, flags=re.S | re.M)
    agents.write_text(text)
    run("git", "add", ".", cwd=target)
    run("git", "commit", "--quiet", "-m", "E1: initialize spoke genome", cwd=target)

    history = x("history-paths", "--manifest", manifest, capture=True)
    (evid / "history.txt").write_text(history)
    paths = out / "paths.txt"
    paths.write_text("\n".join(sorted(set(history.splitlines() + [m.split("=", 1)[0] for m in params["MAP"]]))) + "\n")
    filtered = out / "filtered"
    # Fetch the immutable commit: Actions checks out PRs detached, without a local main.
    run("git", "init", "--quiet", "-b", "main", filtered)
    run("git", "fetch", "--quiet", HUB, sha, cwd=filtered)
    run("git", "reset", "--quiet", "--hard", sha, cwd=filtered)
    run(args.filter_repo.resolve(), "--force", "--preserve-commit-hashes", "--paths-from-file", paths,
        "--message-callback", "return re.sub(rb'(?<![\\w/.-])#(\\d+)', rb'G-Ivan-A/hybrid-Intelligence-lab#\\1', message)", cwd=filtered)
    (evid / "verify-filtered.json").write_text(x("verify", "--manifest", manifest, "--target", filtered, "--extra-scope", "", capture=True))
    run("git", "fetch", "--quiet", filtered, "main:refs/hub-import/main", cwd=target)
    run("git", "merge", "--allow-unrelated-histories", "--no-ff", "--no-edit", "-m", f"import: {hub_url}@{sha} with history", "refs/hub-import/main", cwd=target)
    (evid / "verify-import.json").write_text(x("verify", "--manifest", manifest, "--target", target, capture=True))
    (evid / "commit-map.txt").write_bytes((filtered / ".git/filter-repo/commit-map").read_bytes())
    (evid / "commit-count.txt").write_text(run("git", "rev-list", "--count", "HEAD", cwd=filtered, capture=True))

    links = ("--manifest", manifest, "--target", target, "--hub-url", hub_url, "--target-url", TARGET_URL)
    x("rewrite-links", *links, "--log", evid / "rewrite-links.jsonl")
    x("rewrite-links", *links, "--check", capture=True)
    (evid / "verify-links.json").write_text(x("verify", *links, "--links", capture=True))
    (evid / "scan-after.txt").write_text(x("scan", "--manifest", manifest, "--target", target, capture=True))
    # Preserve directory depth: all five Python entrypoints then keep their ROOT calculation.
    workflow = run("git", "show", f"{sha}:.github/workflows/validate.yml", capture=True)
    blocks = re.split(r"(?=^      - name: )", workflow, flags=re.M)
    wanted = [step.split(" / ", 1)[1] for step in params["CI_STEP"]]
    selected = [block for block in blocks if block.splitlines()[0].removeprefix("      - name: ") in wanted]
    if len(selected) != len(wanted):
        raise RuntimeError("CI step selection incomplete")
    ci = """name: ci
on:
  push:
  pull_request:
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - name: Validate genome
        run: bash tools/validate-agents-bootstrap.sh .
      - name: Validate file naming
        run: ./tools/validate-file-naming.sh
"""
    (target / ".github/workflows/ci.yml").write_text(ci + "".join(selected))
    headings = [item for h in params["BACKLOG"] for item in ("--heading", h)]
    sections_args = ("--sha", sha, "--source", "ops/backlog.md", "--manifest", manifest,
                     "--target-path", "ops/backlog.md", "--hub-url", hub_url, "--target-url", TARGET_URL, *headings)
    (target / "ops").mkdir(exist_ok=True)
    (target / "ops/backlog.md").write_text(f"---\nstatus: draft\nversion: 0.1\nupdated: {DAY}\ntemperature: 0.1\n---\n\n# Бэклог\n\nИсточник: {hub_url}/blob/{sha}/ops/backlog.md; ID сохранены.\n\n" + x("sections", *sections_args, capture=True))
    x("sections", *sections_args, "--check", target / "ops/backlog.md")
    ids = re.findall(r"^\| \*\*(B-\d+)\*\*", (target / "ops/backlog.md").read_text(), re.M)
    (evid / "backlog-ids.txt").write_text("\n".join(ids) + "\n")
    readme = HERE / "spoke-readme.txt"
    (target / "README.md").write_bytes(readme.read_bytes())
    (target / "LICENSE").write_text(run("git", "show", f"{sha}:LICENSE", capture=True))
    # Imported decisions remain historical. A new decision records this import without rewriting them.
    adr = target / "docs/adr/2026-11-adr-001-hub-import.md"
    adr.parent.mkdir(parents=True, exist_ok=True)
    adr.write_text(f"---\nstatus: proposed\nversion: 0.1\nupdated: {DAY}\ntemperature: 0.1\ndecision-type: architecture\n---\n\n# ADR-001: импорт из Хаба\n\n## Context\n\nIssue {hub_url}/issues/742; контракт {hub_url}/blob/{sha}/ops/hub-project-extraction-contract.md.\n\n## Decision\n\nПроект и исследования переносятся с сохранением путей из `{sha}`.\nИстория обработана git-filter-repo 2.47.0; карта коммитов и хеши файлов — в `../import/hub-{sha[:12]}/`.\nИмпорт локальный; приёмка, удалённый CI, приватность и очистка Хаба ещё не подтверждены.\n\n## Consequences\n\nЛицензия исходного вклада сохранена. Новые закрытые данные хранятся только после проверки PRIVATE.\nСлияние должно сохранить историю (merge commit).\n")
    final = x("verify", *links, "--links", capture=True)
    (evid / "verify-final.json").write_text(final)
    run("bash", "tools/validate-agents-bootstrap.sh", target, cwd=target)
    run("./tools/validate-file-naming.sh", cwd=target)
    for block in selected:
        command = block.split("        run:", 1)[1].strip()
        if command.startswith("|"):
            command = "\n".join(line[10:] for line in command.splitlines()[1:])
        run("bash", "-e", "-o", "pipefail", "-c", command, cwd=target)
    events = collections.Counter(json.loads(line)["kind"] for line in (evid / "rewrite-links.jsonl").read_text().splitlines())
    summary = {"hub_sha": sha, "files": len(targets(manifest)), "history_commits": int((evid / "commit-count.txt").read_text()),
               "link_events": dict(sorted(events.items())), "backlog_rows": len(ids), "ci_steps": wanted,
               "local_checks": "PASS", "remote_import": "NOT VERIFIED (offline preparation)",
               "visibility": "NOT VERIFIED (offline preparation)", "hub_cleanup": "NOT PERFORMED (remote E6 required)"}
    write_json(evid / "summary.json", summary)
    (evid / "README.md").write_text(f"---\nstatus: draft\nversion: 0.1\nupdated: {DAY}\ntemperature: 0.1\n---\n\n# Локальный импорт `{sha}`\n\nКонтракт: {hub_url}/blob/{sha}/ops/hub-project-extraction-contract.md.\n\nE1–E6 проверены локально; удалённая приёмка НЕ выполнена.\nМанифесты, карта истории, журнал ссылок, проверки и ID бэклога — в этом каталоге.\nСчётчики и блокеры — `summary.json`. Импортированные файлы после E3 совпадают с `verify-final.json`; адаптированных файлов проекта нет.\n")
    run("git", "add", ".", cwd=target)
    run("git", "commit", "--quiet", "-m", "Prepare E2–E6: history, links, CI and backlog (local verification only)", cwd=target)
    run("git", "bundle", "create", out / "proxeneta.bundle", BRANCH, cwd=target)
    write_json(out / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
