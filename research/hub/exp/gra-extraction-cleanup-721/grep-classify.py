#!/usr/bin/env python3
"""Классификация упоминаний выведенного домена GRA в дереве Хаба (issue #725, B-284).

Usage:
    python3 -I grep-classify.py <hub>

Критерий Ш6.2 RFC #721: `git grep research/reputation-technologies` находит
только надгробие, `path_migrations` и исторические записи. Адрес на теге архива
или по SHA — закреплённая ссылка на прежний путь, а не живой путь в дереве;
он тоже допустим. Каждое вхождение получает класс:

* `tombstone` — само надгробие или упоминание пути, который есть в дереве:
  надгробия `.../README.md` или префикса домена, где оно лежит;
* `path_migrations` — `.hub-profile.json`;
* `history` — исторические записи: `docs/{analysis,rfc,adr,audit,report}/`,
  `CHANGELOG.md`, `ops/backlog.md`, evidence-контейнеры `*/exp/*`;
* `pinned` — вхождение внутри URL `blob|tree/<sha>/` или `blob|tree/archive/*/`;
* `live` — всё прочее: путь под доменом, которого нет в дереве, вне
  закреплённого URL. Ошибка.

Печатает сводку по классам и каждое `live`-вхождение; код 1, если они есть.
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter

DOMAIN = "research/reputation-technologies"
TOMBSTONE = f"{DOMAIN}/README.md"
HISTORY = re.compile(r"^(docs/(analysis|rfc|adr|audit|report)/|CHANGELOG\.md$|ops/backlog\.md$|.*/exp/)")
PINNED = re.compile(r"https://github\.com/[\w.-]+/[\w.-]+/(?:blob|tree)/(?:[0-9a-f]{7,40}|archive/[\w.-]+)/" + re.escape(DOMAIN) + r"[^\s)\"'`>|]*")
TOKEN = re.compile(re.escape(DOMAIN) + r"[\w./#-]*")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    hub = argv[1]
    out = subprocess.run(["git", "-C", hub, "grep", "-n", "-I", "-F", DOMAIN],
                         capture_output=True, text=True).stdout
    tree = set(subprocess.run(["git", "-C", hub, "ls-files"], capture_output=True, text=True).stdout.split())
    dirs = {p.rsplit("/", i)[0] for p in tree for i in range(1, p.count("/") + 1)}
    counts: Counter = Counter()
    files: dict[str, set] = {}
    live = []
    for line in out.splitlines():
        path, lineno, text = line.split(":", 2)
        if path == TOMBSTONE:
            kind = ["tombstone"]
        elif path == ".hub-profile.json":
            kind = ["path_migrations"]
        elif HISTORY.match(path):
            kind = ["history"]
        else:
            kind = ["pinned"] * len(PINNED.findall(text))
            for token in TOKEN.findall(PINNED.sub("", text)):
                target = token.split("#")[0].rstrip("/.")
                if target in tree or target in dirs:
                    kind.append("tombstone")
                else:
                    kind.append("live")
                    live.append(f"{path}:{lineno}: {token}")
        for k in kind:
            counts[k] += 1
            files.setdefault(k, set()).add(path)
    print("класс\tвхождений\tфайлов")
    for k in ("tombstone", "path_migrations", "history", "pinned", "live"):
        print(f"{k}\t{counts[k]}\t{len(files.get(k, ()))}")
    for item in live:
        print(f"LIVE {item}")
    return 1 if live else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
