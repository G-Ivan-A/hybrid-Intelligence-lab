#!/usr/bin/env python3
"""Инвентаризация research-практик в spoke-репозиториях для issue #499.

`scan-research.py` покрывает только корпус Хаба. Постановка issue #499 (уточнение
в комментарии PR #502) требует расширить область анализа на research-практики
проектов `mango_ba_prompts` и `clarify-engine-ai`. Эти репозитории не являются
подмодулями Хаба, поэтому снимок снимается через GitHub API (`gh api`), а не с
файловой системы.

Классификация формальная — только путь, имя файла и frontmatter:

* `module`   — каталог с точкой входа `00-*.md` (Reference Research Pattern);
* `hub-single` — `YYYY-MM-DD-name.md` (форма research-standard.md Хаба);
* `spoke-single` — `YYYY-MM-DD_<slug>_vN.md` с подчёркиваниями и/или суффиксом
  версии — наблюдаемая в spoke-репозиториях запись, не совпадающая ни с одной
  формой, нормированной Хабом;
* `undated`  — файл без даты в имени.

Содержательная интерпретация выполняется в родительском Analysis.

Использование:
    python3 research/hub/exp/research-methodology-validation-499/scan-spokes.py \
        --out research/hub/exp/research-methodology-validation-499/spoke-inventory.json
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import subprocess
from pathlib import Path

SPOKES = ["G-Ivan-A/mango_ba_prompts", "G-Ivan-A/clarify-engine-ai"]

# Каталоги, которые в spoke-репозиториях несут research/analysis-нагрузку.
RESEARCH_DIR_RE = re.compile(r"(^|/)(research|analysis)(/|$)")

HUB_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9.-]+\.md$")
SPOKE_DATED_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[_-].+\.md$")
VERSION_SUFFIX_RE = re.compile(r"_v(\d+)\.md$")
BACKLOG_ID_RE = re.compile(r"_(bl-\d+|b-\d+)_", re.IGNORECASE)
MODULE_FILE_RE = re.compile(r"^\d{2}-[a-z0-9-]+\.md$")


def gh_api(path: str) -> dict:
    out = subprocess.check_output(["gh", "api", path], text=True)
    return json.loads(out)


def default_sha(repo: str) -> str:
    return gh_api(f"repos/{repo}/commits?per_page=1")[0]["sha"]


def read_frontmatter(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return fields
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip().strip('"')
    return fields


def classify(path: str) -> str:
    name = path.rsplit("/", 1)[-1]
    if MODULE_FILE_RE.match(name):
        return "module-file"
    if HUB_DATED_RE.match(name):
        return "hub-single"
    if SPOKE_DATED_RE.match(name):
        return "spoke-single"
    return "undated"


def scan_repo(repo: str) -> dict:
    sha = default_sha(repo)
    tree = gh_api(f"repos/{repo}/git/trees/{sha}?recursive=1")["tree"]

    md_paths = [
        node["path"]
        for node in tree
        if node["type"] == "blob"
        and node["path"].endswith(".md")
        and RESEARCH_DIR_RE.search(node["path"].rsplit("/", 1)[0])
        and node["path"].rsplit("/", 1)[-1] != "README.md"
    ]

    # Исполняемая evidence base spoke-репозитория: код и тесты под research/.
    code_paths = sorted(
        node["path"]
        for node in tree
        if node["type"] == "blob"
        and not node["path"].endswith(".md")
        and RESEARCH_DIR_RE.search(node["path"].rsplit("/", 1)[0])
    )

    documents = []
    for path in sorted(md_paths):
        blob = gh_api(f"repos/{repo}/contents/{path}?ref={sha}")
        text = base64.b64decode(blob["content"]).decode("utf-8", errors="replace")
        frontmatter = read_frontmatter(text)
        name = path.rsplit("/", 1)[-1]
        version_match = VERSION_SUFFIX_RE.search(name)
        documents.append({
            "path": path,
            "kind": classify(path),
            "lines": len(text.splitlines()),
            "has_frontmatter": bool(frontmatter),
            "status": frontmatter.get("status", ""),
            "version_frontmatter": frontmatter.get("version", ""),
            "version_in_filename": version_match.group(1) if version_match else "",
            "backlog_id_in_filename": bool(BACKLOG_ID_RE.search(name)),
            "directory": path.rsplit("/", 1)[0],
        })

    kinds: dict[str, int] = {}
    for doc in documents:
        kinds[doc["kind"]] = kinds.get(doc["kind"], 0) + 1

    return {
        "repo": repo,
        "sha": sha,
        "documents": len(documents),
        "lines_total": sum(d["lines"] for d in documents),
        "kinds": dict(sorted(kinds.items())),
        "modules": sum(1 for d in documents if d["kind"] == "module-file"),
        "with_frontmatter": sum(1 for d in documents if d["has_frontmatter"]),
        "with_version_suffix": sum(1 for d in documents if d["version_in_filename"]),
        "with_backlog_id": sum(1 for d in documents if d["backlog_id_in_filename"]),
        "exp_containers": sorted({
            d["directory"] for d in documents if "/exp/" in d["path"] + "/"
        }),
        "research_code_files": code_paths,
        "directories": sorted({d["directory"] for d in documents}),
        "files": documents,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="путь для JSON-результата")
    args = parser.parse_args()

    repos = [scan_repo(repo) for repo in SPOKES]
    result = {
        "source_issue": "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/499",
        "summary": {
            "repos": len(repos),
            "documents_total": sum(r["documents"] for r in repos),
            "lines_total": sum(r["lines_total"] for r in repos),
            "modules_total": sum(r["modules"] for r in repos),
            "exp_containers_total": sum(len(r["exp_containers"]) for r in repos),
            "hub_form_documents": sum(
                sum(1 for f in r["files"] if f["kind"] == "hub-single") for r in repos
            ),
        },
        "repos": repos,
    }

    Path(args.out).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    s = result["summary"]
    print(f"repos scanned: {s['repos']}")
    for r in repos:
        print(f"  {r['repo']} @ {r['sha'][:7]}: {r['documents']} docs, "
              f"{r['lines_total']} lines, kinds={r['kinds']}, "
              f"frontmatter={r['with_frontmatter']}/{r['documents']}, "
              f"version-suffix={r['with_version_suffix']}, "
              f"backlog-id={r['with_backlog_id']}, "
              f"code files={len(r['research_code_files'])}")
    print(f"modules (Reference Research Pattern) in spokes: {s['modules_total']}")
    print(f"exp/ containers in spokes: {s['exp_containers_total']}")
    print(f"documents in hub dated form: {s['hub_form_documents']}")


if __name__ == "__main__":
    main()
