#!/usr/bin/env python3
"""Inventory of research/reputation-technologies/ for the GRA extraction cleanup (issue #721).

Usage:
    python3 -I research/hub/exp/gra-extraction-cleanup-721/gra-inventory.py <hub_dir> <spoke_dir> [--tsv OUT]

<hub_dir>   — the Hub working tree (git is called only here, read-only).
<spoke_dir> — a clone of aether-orbis-gra. Untrusted data: files are only read,
              nothing from the spoke is imported or executed.

The script answers measurable questions only; dispositions are a deterministic
function of the measured facts plus the explicit SEMANTIC table below, whose
every row quotes the reason recorded by the spoke migration inventory
(docs/analysis/2026-11-01-migration-inventory.md in the spoke) or the Hub file
frontmatter. Set GRA_INVENTORY_DEBUG=1 to trace every reference match.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

DOMAIN = "research/reputation-technologies/"
HUB_URL = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab"
DEBUG = os.environ.get("GRA_INVENTORY_DEBUG") == "1"
TEXT_EXT = (".md", ".py", ".sh", ".yml", ".yaml", ".json", ".txt", ".log", ".tsv", ".csv")
DECISION_HOMES = ("docs/adr/", "docs/rfc/", "docs/audit/", "docs/analysis/", "docs/report/")
SOURCE_RE = re.compile(r'^source:\s*"?' + re.escape(HUB_URL) + r'/(blob|tree)/([0-9a-f]{7,40})/(' + re.escape(DOMAIN) + r'[^"\s]*)"?\s*$', re.M)
SPOKE_REF_RE = re.compile(re.escape(HUB_URL) + r'/(blob|tree)/([^/\s)"]+)/(' + re.escape(DOMAIN) + r'[^)\s"#?]*)')
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
# Absolute mention of the domain path (with or without a trailing slash).
ABS_REF_RE = re.compile(r"(?<![\w-])" + re.escape(DOMAIN.rstrip("/")) + r"(/[^\s)\]\"'`#?<>|,;]*)?")
# Relative Markdown link target: ](target) .
MD_LINK_RE = re.compile(r"\]\(([^)\s#?]+)")

# Semantic classes that cannot be measured. Key: path relative to DOMAIN
# (a trailing "/" means a directory prefix). Value: (class, reason quote).
SEMANTIC: dict[str, tuple[str, str]] = {
    "2026-10-14-day1-lecturer-gra-research.md": (
        "pii", "Исследование открытых данных о конкретном человеке (лекторе): персональные данные не тиражируются"),
    "gra-research-program/presentation-rfc/": ("decision", "RFC отклонён (`rejected`)"),
    "2026-11-03-day4-ai-interpretation-analysis.md": (
        "decision", "Разбор провала интерпретации ИИ (рабочий документ задачи); урок 2 в history.md спицы"),
    "2026-11-03-day4-crisis-mitigation-rfc.md": (
        "decision", "План замен в днях 1–3, `draft`, не применён без согласования автора"),
    "2026-11-03-rfc-presentation-update-v5.md": (
        "decision", "Описание изменений колоды v4 → v5 (рабочий документ задачи)"),
    "2026-11-03-day4-presentation-gamma.md": (
        "decision", "Вариант 1 — исторический документ провала интерпретации"),
    "2026-06-29-partner-attraction-strategy.ru.md": (
        "global-candidate", "ADR-001 спицы, п. 6: «Глобальные исследования (например, стратегия привлечения партнёров ...) остаются в Хабе»; тема файла — партнёры курса (issue #292), то есть проектная"),
    "2026-09-24-introductory-course-options-610.md": (
        "decision", "Сравнение вариантов курса до выбора программы"),
    "2026-09-30-course-sources-and-presentations-650.md": (
        "global-candidate", "Инвентарь спицы: «Исследование источников курса (глобальное исследование)»; `scope: reputation-technologies-course-deepening`; коды `[650:X]` курса ведут на него"),
    "2026-10-07-day1-lecturer-script-653.md": ("superseded", "Ранние версии дня 1, заменены версиями 14.10"),
    "2026-10-07-day1-presentation-653.md": ("superseded", "Ранние версии дня 1, заменены версиями 14.10"),
    "2026-10-13-day1-rebuild-task-671.md": ("superseded", "Постановка задачи"),
    "2026-10-30-day2-presentation.md": ("superseded", "Предыдущий формат колод, заменён версиями для Gamma"),
    "2026-11-02-day3-presentation.md": ("superseded", "Предыдущий формат колод, заменён версиями для Gamma"),
    "2026-11-03-day4-presentation-gamma-v2.md": ("superseded", "Варианты 1–4 дня 4"),
    "2026-11-03-day4-presentation-gamma-v3.md": ("superseded", "Варианты 1–4 дня 4"),
    "2026-11-03-day4-presentation-gamma-v4.md": ("superseded", "Варианты 1–4 дня 4"),
    "2026-11-03-day4-lecturer-script.md": ("superseded", "Варианты 1–4 дня 4"),
    "2026-11-03-day4-lecturer-script-v3.md": ("superseded", "Варианты 1–4 дня 4"),
    "2026-11-03-day4-rationale-and-method.md": ("superseded", "Варианты 1–4 дня 4"),
    "2026-11-03-day4-rationale-and-method-v2.md": ("superseded", "Варианты 1–4 дня 4"),
    "README.md": ("index", "Индекс Хаба с историей задач; заменён документами L1–L4"),
    "exp/quotes-711/": (
        "provenance", "Сборщик и проверка текущего списка цитат (CI `build_quotes_711.py --check`): провенанс документа, который доимпортируется"),
    "exp/": ("evidence", "Эксперименты и проверки задач"),
}


def debug(msg: str) -> None:
    if DEBUG:
        print(f"[inventory] {msg}", file=sys.stderr)


def git(hub: str, *args: str, check: bool = True) -> str:
    res = subprocess.run(["git", "-C", hub, *args], capture_output=True, text=True)
    if check and res.returncode != 0:
        raise SystemExit(f"git {' '.join(args)}: {res.stderr.strip()}")
    return res.stdout if res.returncode == 0 else ""


def blob(hub: str, rev: str, path: str) -> str:
    return git(hub, "rev-parse", "--verify", "--quiet", f"{rev}:{path}", check=False).strip()


def semantic(rel: str) -> tuple[str, str]:
    if rel in SEMANTIC:
        return SEMANTIC[rel]
    for key, val in SEMANTIC.items():
        if key.endswith("/") and rel.startswith(key):
            return val
    return ("current", "")


def unit_of(rel: str) -> str:
    """exp/<container>/... is one unit; every other file is its own unit."""
    parts = rel.split("/")
    return "/".join(parts[:2]) + "/" if parts[0] == "exp" and len(parts) > 2 else rel


def domain_targets(path: str, text: str) -> list[str]:
    """Domain paths a Hub file points at: absolute mentions plus relative links resolved from its directory."""
    out = []
    for m in ABS_REF_RE.finditer(text):
        out.append(DOMAIN + (m.group(1) or "/").lstrip("/"))
    if path.endswith(".md"):
        base = os.path.dirname(path)
        for target in MD_LINK_RE.findall(text):
            if "://" in target or target.startswith(("mailto:", "/")):
                continue
            resolved = os.path.normpath(os.path.join(base, target)).replace(os.sep, "/")
            if (resolved + "/").startswith(DOMAIN) and DOMAIN.rstrip("/") not in target:
                out.append(resolved + ("/" if resolved + "/" == DOMAIN else ""))
    return out


def read_text(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except (UnicodeDecodeError, OSError):
        return ""


def walk_text(root: str, skip_prefix: str = "") -> dict[str, str]:
    out = {}
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in files:
            if not name.endswith(TEXT_EXT):
                continue
            full = os.path.join(base, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if skip_prefix and rel.startswith(skip_prefix):
                continue
            out[rel] = read_text(full)
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    hub, spoke = argv[1], argv[2]
    tsv_out = argv[argv.index("--tsv") + 1] if "--tsv" in argv else None
    head = git(hub, "rev-parse", "HEAD").strip()
    profile = json.loads(read_text(os.path.join(spoke, ".hub-profile.json")) or "{}")
    last_sync = profile.get("last_sync") or {}
    snapshot = last_sync.get("hub_commit") or last_sync.get("hub_sha") or ""
    if not SHA_RE.match(snapshot):
        raise SystemExit("spoke .hub-profile.json has no last_sync hub commit")
    spoke_head = ""
    head_file = os.path.join(spoke, ".git", "HEAD")
    if os.path.isfile(head_file):
        ref = read_text(head_file).strip()
        if ref.startswith("ref: "):
            spoke_head = read_text(os.path.join(spoke, ".git", ref[5:])).strip()
            if not spoke_head:
                packed = read_text(os.path.join(spoke, ".git", "packed-refs"))
                m = re.search(r"^([0-9a-f]{40}) " + re.escape(ref[5:]) + "$", packed, re.M)
                spoke_head = m.group(1) if m else ""
        else:
            spoke_head = ref

    files = [p for p in git(hub, "ls-files", "--", DOMAIN).splitlines() if p]
    snap_files = set(git(hub, "ls-tree", "-r", "--name-only", snapshot, "--", DOMAIN).splitlines())

    # 1. Moves recorded by the spoke itself: frontmatter `source:` permalinks.
    spoke_text = walk_text(spoke)
    moved: dict[str, tuple[str, str]] = {}
    for spath, text in spoke_text.items():
        for kind, sha, hpath in SOURCE_RE.findall(text[:2000]):
            if kind == "blob":
                moved[hpath] = (spath, sha)

    # 2. Spoke references to Hub domain paths: pinned (SHA) or floating (branch).
    spoke_refs: dict[str, Counter] = defaultdict(Counter)
    for spath, text in spoke_text.items():
        for kind, rev, hpath in SPOKE_REF_RE.findall(text):
            hpath = hpath.rstrip("/.,;")
            key = "pinned" if SHA_RE.match(rev) else "floating"
            spoke_refs[hpath][key] += 1
            debug(f"spoke {spath} -> {rev}:{hpath} ({key})")

    # 3. Hub references from outside the domain.
    hub_text = {p: read_text(os.path.join(hub, p)) for p in git(hub, "ls-files").splitlines()
                if p.endswith(TEXT_EXT) and not p.startswith(DOMAIN)}
    validate_yml = hub_text.get(".github/workflows/validate.yml", "")
    hub_targets = {f: domain_targets(f, t) for f, t in hub_text.items()}
    hub_targets = {f: v for f, v in hub_targets.items() if v}

    units: dict[str, list[str]] = defaultdict(list)
    for p in files:
        units[unit_of(p[len(DOMAIN):])].append(p)

    rows = []
    for unit, paths in sorted(units.items()):
        rel_paths = [p[len(DOMAIN):] for p in paths]
        needle = DOMAIN + unit
        ext_refs = sorted(f for f, v in hub_targets.items()
                          if any(t == needle or t.startswith(needle) for t in v))
        decision_refs = [f for f in ext_refs if f.startswith(DECISION_HOMES)]
        changelog_ref = "CHANGELOG.md" in ext_refs
        registry_refs = [f for f in ext_refs if f in (
            "ops/artifact-map.md", "tools/validate-repository-structure.sh", "CHANGELOG.md",
            "ops/backlog.md", "research/README.md")]
        ci = needle in validate_yml
        sref = Counter()
        for hp, c in spoke_refs.items():
            if hp == needle.rstrip("/") or hp.startswith(needle):
                sref.update(c)
        moved_to = sorted({moved[p][0] for p in paths if p in moved})
        stale = [p for p in paths if p in moved and blob(hub, moved[p][1], p) != blob(hub, head, p)]
        new = [p for p in paths if p not in snap_files]
        cls, reason = semantic(rel_paths[0])
        # Disposition: first matching rule wins.
        if moved_to and len(moved_to) == len(paths) and not stale:
            rule, disp = "R1 перенесён, байты Хаба не менялись после source", "TOMBSTONE"
        elif stale:
            rule, disp = "R2 перенесён, но изменён в Хабе после source", "REIMPORT"
        elif new and cls in ("current",):
            rule, disp = "R3 создан в Хабе после снимка спицы", "REIMPORT"
        elif cls == "pii":
            rule, disp = "R4 персональные данные", "PII"
        elif cls == "index":
            rule, disp = "R5 индекс домена", "README-TOMBSTONE"
        elif cls == "global-candidate":
            rule, disp = "R6 кандидат в глобальные исследования: спица называет глобальным, тема проектная", "OWNER-Q"
        elif cls == "decision":
            rule, disp = "R7 запись решения или урока", "ARCHIVE"
        elif cls == "provenance":
            rule, disp = "R7a провенанс текущего документа спицы", "ARCHIVE"
        elif cls in ("superseded", "evidence") and (decision_refs or sref["floating"]):
            rule, disp = "R8 заменён/доказательство, но есть входящие ссылки записей решений или плавающие ссылки спицы", "ARCHIVE"
        elif cls in ("superseded", "evidence"):
            rule, disp = "R9 заменён/доказательство без входящих ссылок записей решений", "DELETE"
        else:
            rule, disp = "R10 не классифицирован", "OWNER-Q"
        if moved_to and len(moved_to) < len(paths) and disp in ("DELETE", "ARCHIVE"):
            rule += "; часть файлов перенесена"
        rows.append({
            "unit": unit, "files": len(paths), "class": cls, "moved_to": ";".join(moved_to) or "-",
            "stale": len(stale), "new_after_snapshot": len(new), "ci_step": "yes" if ci else "-",
            "hub_ext_refs": len(ext_refs), "decision_refs": len(decision_refs),
            "registry_refs": len(registry_refs), "changelog_ref": "yes" if changelog_ref else "-",
            "spoke_pinned": sref["pinned"],
            "spoke_floating": sref["floating"], "rule": rule, "disposition": disp,
            "reason": reason or "-", "decision_ref_files": ",".join(decision_refs) or "-",
        })

    cols = list(rows[0].keys())
    if tsv_out:
        with open(tsv_out, "w", encoding="utf-8") as fh:
            fh.write("\t".join(cols) + "\n")
            for r in rows:
                fh.write("\t".join(str(r[c]) for c in cols) + "\n")

    total = sum(r["files"] for r in rows)
    print(f"hub HEAD: {head}")
    print(f"spoke HEAD: {spoke_head or 'unknown'}")
    print(f"spoke snapshot (last_sync.hub_commit): {snapshot}")
    print(f"domain files at HEAD: {len(files)} (units: {len(rows)}; sum check: {total})")
    print(f"domain files in snapshot: {len(snap_files)}; added after snapshot: {len(set(files) - snap_files)}; removed after snapshot: {len(snap_files - set(files))}")
    print(f"spoke files with source: permalink to the domain: {len(moved)}")
    print()
    print("files by disposition:")
    by = Counter()
    for r in rows:
        by[r["disposition"]] += r["files"]
    for k, v in sorted(by.items()):
        print(f"  {k}: {v} files, {sum(1 for r in rows if r['disposition'] == k)} units")
    print()
    print("units with a CI step in .github/workflows/validate.yml:", sum(1 for r in rows if r["ci_step"] == "yes"))
    print("spoke references to the domain: pinned", sum(r["spoke_pinned"] for r in rows),
          "floating", sum(r["spoke_floating"] for r in rows))
    print()
    print("re-import list (rule R2/R3):")
    for r in rows:
        if r["disposition"] == "REIMPORT":
            print(f"  {r['unit']} ({r['files']} files; stale {r['stale']}; new {r['new_after_snapshot']})")
    print()
    hist = [r for r in rows if r["changelog_ref"] == "yes" or r["decision_refs"]]
    print("units referenced from historical records (CHANGELOG.md or docs/{adr,rfc,audit,analysis,report}/):"
          f" {len(hist)} of {len(rows)} units, {sum(r['files'] for r in hist)} files")
    print("  artifact-deprecation-standard, Deletion Rules, forbidden #1: such a path may not be deleted"
          " unless its address is replaced by a compatibility redirect")
    print()
    print("units blocked by floating spoke links (must be pinned in the spoke before the Hub moves them):")
    for r in rows:
        if r["spoke_floating"] and r["disposition"] != "TOMBSTONE":
            print(f"  {r['unit']}: {r['spoke_floating']} floating -> {r['disposition']}")
    for r in rows:
        if r["spoke_floating"] and r["disposition"] == "TOMBSTONE":
            print(f"  {r['unit']}: {r['spoke_floating']} floating -> TOMBSTONE")
    print()
    print("Hub files outside the domain that reference it:")
    print("  (count = absolute mentions + relative Markdown links resolved into the domain;"
          " a bare mention of the domain root counts too)")
    for f, v in sorted(hub_targets.items()):
        print(f"  {f}: {len(v)}")
    print(f"  total files: {len(hub_targets)}")
    print()
    bare_name = DOMAIN.rstrip("/").rsplit("/", 1)[1] + "/"
    bare = sorted(f for f, t in hub_text.items() if f not in hub_targets and bare_name in t)
    print(f"Hub files outside the domain with only a bare `{bare_name}` mention (tree diagrams, tables; no link):")
    for f in bare:
        print(f"  {f}: {hub_text[f].count(bare_name)}")
    print(f"  total files: {len(bare)}")
    print()
    print("per-unit table:")
    short = ["unit", "files", "class", "stale", "new_after_snapshot", "ci_step", "changelog_ref", "decision_refs", "spoke_floating", "disposition"]
    print("  " + " | ".join(short))
    for r in rows:
        print("  " + " | ".join(str(r[c]) for c in short))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
