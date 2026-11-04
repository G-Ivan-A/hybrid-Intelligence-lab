#!/usr/bin/env python3
"""Генератор надгробия research/reputation-technologies/README.md (issue #725, B-278).

Usage:
    python3 -I tombstone-manifest.py <hub> <spoke> <inventory.tsv> <out.md>

Для каждого файла домена в дереве Хаба строит одну строку манифеста
(формат `tools/path-migration-manifest.py`):

* файл, перенесённый в спицу (frontmatter `source:` копии в спице указывает на
  этот путь Хаба, байты не менялись после `source`), — SHA-ссылка на спицу;
* иначе — по диспозиции единицы из `gra-inventory.tsv` (решения Q-1…Q-5):
  ARCHIVE и OWNER-Q #650 — путь на теге `archive/reputation-technologies-2026-11`,
  DELETE (мандат Q-2) и PII (Q-4) — «удалён; последняя версия — `48ebe52`»,
  OWNER-Q #292 — относительная ссылка на `research/education/` (Q-3).

Спица читается как данные: файлы и `git cat-file`, её код не исполняется.
Генератор падает, если хоть один файл остался без адреса.
"""

from __future__ import annotations

import csv
import os
import re
import subprocess
import sys
from collections import Counter

DOMAIN = "research/reputation-technologies/"
HUB_URL = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab"
SPOKE_URL = "https://github.com/G-Ivan-A/aether-orbis-gra"
TAG = "archive/reputation-technologies-2026-11"
PIN = "48ebe52"
PARTNER = "2026-06-29-partner-attraction-strategy.ru.md"
SOURCES_650 = "2026-09-30-course-sources-and-presentations-650.md"
SOURCE_RE = re.compile(r'^source:\s*"?' + re.escape(HUB_URL) + r'/blob/([0-9a-f]{7,40})/(' + re.escape(DOMAIN) + r'[^"\s]*)"?\s*$', re.M)
TEXT_EXT = (".md", ".py", ".sh", ".yml", ".yaml", ".json", ".txt", ".log", ".tsv", ".csv")


def git(root: str, *args: str) -> str:
    res = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit(f"git {' '.join(args)}: {res.stderr.strip()}")
    return res.stdout


def blob(root: str, rev: str, path: str) -> str:
    res = subprocess.run(["git", "-C", root, "rev-parse", "--verify", "--quiet", f"{rev}:{path}"],
                         capture_output=True, text=True)
    return res.stdout.strip()


def unit_of(rel: str) -> str:
    parts = rel.split("/")
    return "/".join(parts[:2]) + "/" if parts[0] == "exp" and len(parts) > 2 else rel


def spoke_moves(spoke: str) -> dict[str, str]:
    moved: dict[str, str] = {}
    for base, dirs, files in os.walk(spoke):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in files:
            if not name.endswith(TEXT_EXT):
                continue
            full = os.path.join(base, name)
            try:
                with open(full, encoding="utf-8") as fh:
                    head = fh.read(2000)
            except (UnicodeDecodeError, OSError):
                continue
            for sha, hpath in SOURCE_RE.findall(head):
                spath = os.path.relpath(full, spoke).replace(os.sep, "/")
                if hpath in moved and moved[hpath][0] != spath:
                    raise SystemExit(f"{hpath}: две копии в спице — {moved[hpath][0]} и {spath}")
                moved[hpath] = (spath, sha)
    return moved


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(__doc__, file=sys.stderr)
        return 2
    hub, spoke, tsv, out = argv[1:]
    spoke_sha = git(spoke, "rev-parse", "HEAD").strip()
    head = git(hub, "rev-parse", "HEAD").strip()
    with open(tsv, encoding="utf-8") as fh:
        disposition = {r["unit"]: r["disposition"] for r in csv.DictReader(fh, delimiter="\t")}
    files = [p for p in git(hub, "ls-tree", "-r", "--name-only", "HEAD", "--", DOMAIN).splitlines() if p]
    moved = spoke_moves(spoke)
    rows, counts, errors = [], Counter(), []
    for path in sorted(files):
        rel = path[len(DOMAIN):]
        if rel == "README.md":
            continue
        unit = unit_of(rel)
        disp = disposition.get(unit)
        if disp is None:
            errors.append(f"{path}: единицы {unit} нет в инвентаре")
            continue
        if disp in ("DELETE", "PII"):
            if path in moved:
                errors.append(f"{path}: удаляется ({disp}), но есть копия в спице {moved[path][0]}")
            label = "удалён по мандату (Q-2)" if disp == "DELETE" else "удалён: персональные данные (Q-4), в тег не входит"
            rows.append((path, label, f"удалён; последняя версия — `{PIN}`"))
            counts[label] += 1
        elif path in moved:
            spath, source_sha = moved[path]
            if blob(hub, source_sha, path) != blob(hub, head, path):
                errors.append(f"{path}: копия {spath} снята с {source_sha[:7]}, байты Хаба после неё менялись")
                continue
            if not os.path.isfile(os.path.join(spoke, spath)):
                errors.append(f"{path}: файла {spath} нет в спице")
                continue
            label = "перенесён в спицу"
            rows.append((path, label, f"[{spath}]({SPOKE_URL}/blob/{spoke_sha}/{spath})"))
            counts[label] += 1
        elif rel == PARTNER:
            label = "перенесён в Хаб: глобальное исследование (Q-3)"
            rows.append((path, label, f"[research/education/{PARTNER}](../education/{PARTNER})"))
            counts[label] += 1
        elif disp == "ARCHIVE" or rel == SOURCES_650:
            label = "архив: тег" if disp == "ARCHIVE" else "архив: тег; перенос в спицу — GRA-003 (Q-3)"
            rows.append((path, label, f"[тег]({HUB_URL}/blob/{TAG}/{path})"))
            counts[label] += 1
        else:
            errors.append(f"{path}: диспозиция {disp} без адреса")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    summary = "\n".join(f"| {label} | {n} |" for label, n in sorted(counts.items()))
    table = "\n".join(f"| `{p}` | {label} | {address} |" for p, label, address in rows)
    text = f"""---
status: superseded
version: 2.0
updated: 2026-11-04
temperature: 0.1
---

# Research: Reputation Technologies (GRA) — выведен из Хаба

> **Historical compatibility path. Do not use as an active artifact.** Домен
> репутационных технологий (GRA) и курса «Технограда» выведен из дерева Хаба.
> **Замена:** спица [`G-Ivan-A/aether-orbis-gra`]({SPOKE_URL}); задачи курса
> ведутся только в её бэклоге (исключение A-4 снято). **Причина:** домен
> перенесён в спицу, а Хаб хранит только глобальные исследования и методологию.
> **Решение:** [RFC #721](../../docs/rfc/2026-11-04-rfc-gra-extraction-completion-and-hub-cleanup.md),
> [ADR-022](../../docs/adr/2026-11-adr-022-hub-archive-and-extraction-redirect.md),
> [issue #725]({HUB_URL}/issues/725) (ответы владельца Q-1…Q-6).

Здесь — только манифест redirect по
[стандарту выбытия](../../standards/artifact-deprecation-standard.md#manifest-redirect):
куда ушёл каждый прежний путь под `{DOMAIN}`. Ссылки исторических документов на
эти пути валидатор разрешает по этой таблице
(`path_migrations` в [`.hub-profile.json`](../../.hub-profile.json)).

## Где теперь содержимое

- **Перенесённое в спицу** — SHA-ссылка на копию в спице на коммите
  `{spoke_sha[:7]}`; актуальная версия — по тому же пути на `main` спицы.
- **Архив** — аннотированный тег
  [`{TAG}`]({HUB_URL}/tree/{TAG}/{DOMAIN}): коммит Хаба, где домен лежит целиком,
  без удалённого по мандату и без персональных данных.
- **Удалённое** — рабочие черновики R9 по мандату Q-2 и файл с персональными
  данными по Q-4. В тег не входят; история git не переписана, последняя версия —
  коммит `{PIN}`.
- **Стратегия партнёров (#292)** — осталась в Хабе как глобальное исследование:
  [research/education/{PARTNER}](../education/{PARTNER}).

| Диспозиция | Файлов |
| --- | --- |
{summary}
| **Итого** | **{len(rows)}** |

## Манифест

| Прежний путь | Диспозиция | Адрес |
| --- | --- | --- |
{table}
"""
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"tombstone: {len(rows)} rows; " + "; ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
