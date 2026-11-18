#!/usr/bin/env python3
"""Надгробия Хаба после выноса метамодели БА в ba-ai-metamodel (B-249, Ш3.6, issue #738).

Генерирует manifest redirect по стандарту выбытия для двух выведенных
префиксов и совместимый редирект для одиночного файла:

  projects/ba-ai-process/README.md   манифест префикса projects/ba-ai-process/
  research/mango/README.md           манифест префикса research/mango/
  docs/ba-meta-model-overview.md     совместимый редирект (одиночный путь)

Каждый прежний путь под префиксом в коммите архива (HUB_SHA параметров) и в
его первом родителе получает одну строку с SHA-ссылкой на тот же файл в
ba-ai-metamodel на коммите приёмки E6. Путь в спице выводится строками MAP
параметров выноса. Наличие каждого целевого пути проверяется по клону спицы.

Usage:
  python3 -I tombstone.py --hub HUB_CLONE --spoke SPOKE_CLONE --spoke-sha SHA [--check]

Без --check файлы записываются в рабочее дерево HUB_CLONE; с --check код 1,
если хоть один файл отличается от сгенерированного. Только git и чтение файлов.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARAMS = HERE / "ba-instance-params.txt"
SPOKE_URL = "https://github.com/G-Ivan-A/ba-ai-metamodel"
HUB_URL = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab"
UPDATED = "2026-11-17"
SHA40 = re.compile(r"^[0-9a-f]{40}$")

PREFIXES = {
    "projects/ba-ai-process/": {
        "version": "2.0",
        "title": "BA AI Process — вынесен в ba-ai-metamodel",
        "slug": "ba-ai-process-2026-11",
        "what": "Исходник метамодели БА (ядро, сборщики, решения, пакеты исполнения, руководства, тесты)",
        "depth": "../..",
    },
    "research/mango/": {
        "version": "2.0",
        "title": "Research: MANGO OFFICE — вынесен в ba-ai-metamodel",
        "slug": "mango-research-2026-11",
        "what": "Исследования эталонной реализации MANGO OFFICE (классификация, flow требований, онтология)",
        "depth": "../..",
    },
}
SINGLE = "docs/ba-meta-model-overview.md"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout


def read_params():
    params = {}
    for line in PARAMS.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.partition(": ")
        if sep and key.isupper():
            params.setdefault(key, []).append(value.strip())
    return params


def target_of(path, maps):
    for src, dst in maps:
        if src.endswith("/") and path.startswith(src):
            return dst + path[len(src):]
        if path == src:
            return dst
    return None


def paths_under(hub, commit, prefix):
    out = git(hub, "ls-tree", "-r", "--name-only", commit, "--", prefix.rstrip("/"))
    return {line for line in out.splitlines() if line}


def tombstone(prefix, meta, rows, hub_sha, spoke_sha):
    manifest = prefix + "README.md"
    depth = meta["depth"]
    readme_target = f"{SPOKE_URL}/blob/{spoke_sha}/{rows.pop(manifest)}"
    lines = [
        "---",
        "status: superseded",
        f"version: {meta['version']}",
        f"updated: {UPDATED}",
        "temperature: 0.1",
        "---",
        "",
        f"# {meta['title']}",
        "",
        "> **Historical compatibility path. Do not use as an active artifact.**",
        f"> **Замена:** спица [`G-Ivan-A/ba-ai-metamodel`]({SPOKE_URL}) — единственный источник (SSOT)",
        "> метамодели БА; задачи ведутся в её бэклоге без перенумерации ID.",
        f"> **Причина:** {meta['what']} вынесены из Хаба с историей",
        f"> по [контракту выноса]({depth}/ops/hub-project-extraction-contract.md)",
        f"> (B-243…B-249, [issue #738]({HUB_URL}/issues/738)).",
        "",
        f"Приёмка E1–E6 — на коммите спицы `{spoke_sha}`",
        f"([PR #2–#7]({SPOKE_URL}/pulls?q=is%3Apr+is%3Amerged)); дословность импорта —",
        f"по [карте коммитов]({SPOKE_URL}/blob/{spoke_sha}/docs/import/hub-54face1618f7/commit-map.txt)",
        f"и [журналу проверки]({depth}/research/hub/exp/ba-extraction-717/README.md).",
        "",
        "Здесь — только манифест redirect по",
        f"[стандарту выбытия]({depth}/standards/artifact-deprecation-standard.md#manifest-redirect):",
        f"куда ушёл каждый прежний путь под `{prefix}`. Ссылки исторических документов на",
        "эти пути валидатор разрешает по этой таблице",
        f"(`path_migrations` в [`.hub-profile.json`]({depth}/.hub-profile.json)).",
        "",
        f"- **Архивная ревизия Хаба** — `{hub_sha}`: последний коммит, где набор",
        f"  лежит целиком (источники заморожены на нём с B-243). Тег `archive/{meta['slug']}`",
        "  объявлен для workflow `archive-tag`; пока тег не подтверждён, ревизия",
        "  доступна по SHA. История Хаба не переписывается.",
        f"- **Прежний README** — [в спице]({readme_target}).",
        f"- **Актуальная версия** любого файла — по тому же пути на `main` спицы.",
        "",
        "## Манифест",
        "",
        "| Прежний путь | Диспозиция | Адрес |",
        "| --- | --- | --- |",
    ]
    for path in sorted(rows):
        dst = rows[path]
        lines.append(f"| `{path}` | перенесён в спицу | [{dst}]({SPOKE_URL}/blob/{spoke_sha}/{dst}) |")
    return "\n".join(lines) + "\n"


def single_stub(dst, spoke_sha):
    return "\n".join([
        "---",
        "status: superseded",
        "version: 0.2",
        f"updated: {UPDATED}",
        "temperature: 0.1",
        "---",
        "",
        "# Мета-модель БА: обзор для стейкхолдеров — вынесен в ba-ai-metamodel",
        "",
        "> **Historical compatibility path. Do not use as an active artifact.**",
        f"> **Замена:** [{dst} в спице `ba-ai-metamodel`]({SPOKE_URL}/blob/{spoke_sha}/{dst}).",
        "> **Причина:** метамодель БА вынесена из Хаба с историей",
        f"> (B-249, [issue #738]({HUB_URL}/issues/738)); актуальная версия — по тому же пути на `main` спицы.",
        "",
        "Каталог выноса и манифесты прежних путей —",
        "[`projects/ba-ai-process/README.md`](../projects/ba-ai-process/README.md) и",
        "[`research/mango/README.md`](../research/mango/README.md).",
        "",
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--hub", default=".", help="клон Хаба (рабочее дерево)")
    parser.add_argument("--spoke", required=True, help="клон ba-ai-metamodel")
    parser.add_argument("--spoke-sha", required=True, help="коммит приёмки E6 в спице")
    parser.add_argument("--check", action="store_true", help="сравнить, не записывая")
    args = parser.parse_args()
    if not SHA40.match(args.spoke_sha):
        sys.exit("tombstone: --spoke-sha должен быть полным SHA")
    params = read_params()
    hub_sha = params["HUB_SHA"][0]
    maps = [tuple(m.split("=", 1)) for m in params["MAP"]]
    spoke_paths = set(git(args.spoke, "ls-tree", "-r", "--name-only", args.spoke_sha).splitlines())
    parent = git(args.hub, "rev-parse", f"{hub_sha}^1").strip()
    outputs, errors = {}, []
    for prefix, meta in PREFIXES.items():
        paths = paths_under(args.hub, hub_sha, prefix) | paths_under(args.hub, parent, prefix)
        rows = {}
        for path in paths:
            dst = target_of(path, maps)
            if dst is None or dst not in spoke_paths:
                errors.append(f"{path}: нет цели {dst} в спице на {args.spoke_sha[:12]}")
            rows[path] = dst
        outputs[prefix + "README.md"] = tombstone(prefix, meta, rows, hub_sha, args.spoke_sha)
    dst = target_of(SINGLE, maps)
    if dst not in spoke_paths:
        errors.append(f"{SINGLE}: нет цели {dst} в спице")
    outputs[SINGLE] = single_stub(dst, args.spoke_sha)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    status = 0
    for rel, text in outputs.items():
        path = Path(args.hub) / rel
        if args.check:
            current = path.read_text(encoding="utf-8") if path.exists() else None
            if current != text:
                print(f"DIFF {rel}")
                status = 1
            else:
                print(f"ok {rel}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            print(f"wrote {rel}: {text.count(chr(10) + '| `')} row(s)")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
