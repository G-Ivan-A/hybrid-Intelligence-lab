#!/usr/bin/env python3
"""Инвентаризация research-корпуса Хаба для issue #499.

Скрипт сканирует `research/` и разделяет корпус на два наблюдаемых класса формы:

* `module` — каталог, объявляющий себя модулем наличием точки входа `00-*.md`
  (форма Reference Research Pattern, RFC 2026-07-17);
* `single` — одиночный датированный research-файл `YYYY-MM-DD-name.md`
  (форма RFC «Структура research», 2026-06-30).

Классификация формальная: она опирается только на структуру дерева, frontmatter
и git history. Содержательная интерпретация (какая форма чему соответствует)
выполняется в родительском Analysis и в скрипт не заносится.

Использование:
    python3 research/hub/exp/research-methodology-validation-499/scan-research.py \
        --out research/hub/exp/research-methodology-validation-499/research-inventory.json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
RESEARCH_ROOT = REPO_ROOT / "research"

SELF_PREFIX = "research/hub/exp/research-methodology-validation-499/"

# Файлы модуля Reference Research Pattern: префикс кратен десяти (P1 RFC).
MODULE_FILE_RE = re.compile(r"^(\d{2})-[a-z0-9-]+\.md$")
DATED_FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-[a-z0-9.-]+\.md$")
ISSUE_RE = re.compile(r"issues/(\d+)")

# Канонический состав модуля по P1 RFC 2026-07-17.
CANONICAL_MODULE_PREFIXES = ["00", "10", "20", "30", "40", "50"]


def run_git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(REPO_ROOT), *args], text=True)


def read_frontmatter(path: Path) -> dict[str, str]:
    """Плоский разбор frontmatter: только скалярные поля верхнего уровня."""
    fields: dict[str, str] = {}
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return fields
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", line)
        if match:
            key, value = match.group(1), match.group(2).strip().strip('"')
            fields[key] = value
    return fields


def read_issue_refs(path: Path) -> list[str]:
    """Все номера issue, упомянутые в файле (frontmatter + тело)."""
    text = path.read_text(encoding="utf-8")
    return sorted(set(ISSUE_RE.findall(text)), key=int)


def first_commit(path: str) -> dict[str, str]:
    out = run_git(
        "log", "--diff-filter=A", "--follow", "--format=%h|%ad|%s",
        "--date=short", "--", path,
    ).splitlines()
    if not out:
        return {"sha": "", "date": "", "subject": ""}
    sha, date, subject = out[-1].split("|", 2)
    return {"sha": sha, "date": date, "subject": subject}


def last_commit(path: str) -> dict[str, str]:
    out = run_git("log", "-1", "--format=%h|%ad|%s", "--date=short", "--", path).splitlines()
    if not out:
        return {"sha": "", "date": "", "subject": ""}
    sha, date, subject = out[0].split("|", 2)
    return {"sha": sha, "date": date, "subject": subject}


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def collect_modules() -> list[dict]:
    modules: list[dict] = []
    for entry_point in sorted(RESEARCH_ROOT.rglob("00-*.md")):
        module_dir = entry_point.parent
        rel_dir = module_dir.relative_to(REPO_ROOT).as_posix()
        files = []
        extra_files = []
        for md in sorted(module_dir.glob("*.md")):
            rel = md.relative_to(REPO_ROOT).as_posix()
            record = {
                "path": rel,
                "lines": line_count(md),
                "frontmatter": read_frontmatter(md),
                "issues": read_issue_refs(md),
            }
            if MODULE_FILE_RE.match(md.name):
                files.append(record)
            else:
                extra_files.append(record)

        prefixes = [md["path"].rsplit("/", 1)[-1][:2] for md in files]
        entry_rel = entry_point.relative_to(REPO_ROOT).as_posix()
        modules.append({
            "kind": "module",
            "path": rel_dir,
            "domain": module_dir.name,
            "module_files": len(files),
            "extra_files": [f["path"] for f in extra_files],
            "prefixes": prefixes,
            "canonical_six": prefixes == CANONICAL_MODULE_PREFIXES,
            "total_lines": sum(f["lines"] for f in files),
            "total_lines_with_extra": sum(f["lines"] for f in files + extra_files),
            "statuses": sorted({f["frontmatter"].get("status", "") for f in files}),
            "updated": sorted({f["frontmatter"].get("updated", "") for f in files}),
            "methods": sorted({f["frontmatter"].get("method", "") for f in files if f["frontmatter"].get("method")}),
            "issues": sorted({i for f in files + extra_files for i in f["issues"]}, key=int),
            "created": first_commit(entry_rel),
            "last_touched": last_commit(rel_dir),
            "files": files + extra_files,
        })
    return modules


def collect_singles(module_dirs: set[str]) -> list[dict]:
    singles: list[dict] = []
    for md in sorted(RESEARCH_ROOT.rglob("*.md")):
        rel = md.relative_to(REPO_ROOT).as_posix()
        if rel.startswith(SELF_PREFIX):
            continue
        if md.name == "README.md":
            continue
        parent = md.parent.relative_to(REPO_ROOT).as_posix()
        if parent in module_dirs and MODULE_FILE_RE.match(md.name):
            continue
        if "/exp/" in rel:
            continue
        frontmatter = read_frontmatter(md)
        dated = DATED_FILE_RE.match(md.name)
        singles.append({
            "kind": "single",
            "path": rel,
            "domain": parent.split("/", 1)[1] if "/" in parent else parent,
            "in_module_dir": parent in module_dirs,
            "date_first_name": bool(dated),
            "name_date": dated.group(1) if dated else "",
            "lines": line_count(md),
            "status": frontmatter.get("status", ""),
            "version": frontmatter.get("version", ""),
            "updated": frontmatter.get("updated", ""),
            "type": frontmatter.get("type", ""),
            "method": frontmatter.get("method", ""),
            "scope": frontmatter.get("scope", ""),
            "source": frontmatter.get("source", ""),
            "issues": read_issue_refs(md),
            "created": first_commit(rel),
            "last_touched": last_commit(rel),
        })
    return singles


def collect_experiments() -> list[dict]:
    experiments = []
    for exp_dir in sorted(RESEARCH_ROOT.rglob("exp/*")):
        if not exp_dir.is_dir():
            continue
        rel = exp_dir.relative_to(REPO_ROOT).as_posix()
        if rel.startswith(SELF_PREFIX.rstrip("/")):
            continue
        files = sorted(p.relative_to(REPO_ROOT).as_posix() for p in exp_dir.rglob("*") if p.is_file())
        experiments.append({
            "path": rel,
            "files": len(files),
            "scripts": len([f for f in files if f.endswith(".py")]),
            "datasets": len([f for f in files if f.endswith(".json")]),
            "logs": len([f for f in files if f.endswith(".log")]),
            "created": first_commit(rel),
        })
    return experiments


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="путь для JSON-результата")
    args = parser.parse_args()

    modules = collect_modules()
    module_dirs = {m["path"] for m in modules}
    singles = collect_singles(module_dirs)
    experiments = collect_experiments()

    by_domain = Counter(s["path"].split("/")[1] for s in singles)
    result = {
        "repo_sha": run_git("rev-parse", "HEAD").strip(),
        "source_issue": "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/499",
        "summary": {
            "modules": len(modules),
            "modules_canonical_six": sum(1 for m in modules if m["canonical_six"]),
            "modules_with_extra_files": sum(1 for m in modules if m["extra_files"]),
            "module_files_total": sum(m["module_files"] for m in modules),
            "module_lines_total": sum(m["total_lines"] for m in modules),
            "singles": len(singles),
            "singles_lines_total": sum(s["lines"] for s in singles),
            "singles_not_date_first": [s["path"] for s in singles if not s["date_first_name"]],
            "singles_by_domain": dict(sorted(by_domain.items())),
            "hub_singles": sum(1 for s in singles if s["path"].startswith("research/hub/")),
            "experiments": len(experiments),
            "experiments_with_scripts": sum(1 for e in experiments if e["scripts"]),
        },
        "modules": modules,
        "singles": singles,
        "experiments": experiments,
    }

    out_path = Path(args.out)
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    s = result["summary"]
    print(f"repo sha: {result['repo_sha']}")
    print(f"modules: {s['modules']} (canonical six files: {s['modules_canonical_six']}, "
          f"with extra files: {s['modules_with_extra_files']})")
    print(f"module files: {s['module_files_total']}, lines: {s['module_lines_total']}")
    print(f"singles: {s['singles']}, lines: {s['singles_lines_total']}, hub singles: {s['hub_singles']}")
    print(f"singles without date-first name: {s['singles_not_date_first']}")
    print(f"singles by domain: {s['singles_by_domain']}")
    print(f"experiments: {s['experiments']} (with scripts: {s['experiments_with_scripts']})")


if __name__ == "__main__":
    main()
