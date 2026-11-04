#!/usr/bin/env python3
"""Перепись ссылок живых файлов Хаба на домен GRA по манифесту (issue #725, B-279).

Usage:
    python3 -I rewrite-live-links.py <hub> <file>...

Источник адресов — манифест надгробия `research/reputation-technologies/README.md`
(его строит `tombstone-manifest.py`). Переписываются ссылки на плавающую ветку
(`blob|tree/<ветка>/research/reputation-technologies/...`) и относительные ссылки,
которые ведут внутрь домена; SHA-ссылки — уже закреплённые адреса — не трогаются.

* путь из манифеста с адресом в спице или на теге — этот адрес (якорь сохраняется);
* удалённый по мандату путь — SHA-ссылка на последнюю версию `48ebe52`;
* путь с локальным адресом — относительная ссылка на новый путь в Хабе;
* корень домена — репозиторий спицы; каталог внутри домена — тот же каталог на теге.

Ссылка на файл с персональными данными (Q-4) — ошибка: её нельзя переписать
ни на тег, ни на SHA. Печатает число замен по каждому файлу.
"""

from __future__ import annotations

import os
import re
import sys

DOMAIN = "research/reputation-technologies"
HUB_URL = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab"
SPOKE_URL = "https://github.com/G-Ivan-A/aether-orbis-gra"
TAG = "archive/reputation-technologies-2026-11"
PIN = "48ebe5230be87ca5bf8a08b385e296a2987e9958"
MANIFEST = f"{DOMAIN}/README.md"
ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|([^|]*)\|(.*)\|\s*$")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
FLOAT_RE = re.compile(re.escape(HUB_URL) + r"/(?:blob|tree)/(?![0-9a-f]{7,40}/)[\w.-]+/(" + re.escape(DOMAIN) + r"(?:/[^)\s#]*)?)(#[^)\s]*)?")
REL_RE = re.compile(r"\]\(((?:\.\./|\./)*[\w./-]*reputation-technologies[^)\s#]*)(#[^)\s]*)?\)")


def load(hub: str) -> dict[str, tuple[str, str]]:
    table: dict[str, tuple[str, str]] = {}
    with open(os.path.join(hub, MANIFEST), encoding="utf-8") as fh:
        for line in fh:
            m = ROW_RE.match(line.rstrip("\n"))
            if not m or not m.group(1).startswith(DOMAIN + "/"):
                continue
            path, label, cell = m.group(1), m.group(2).strip(), m.group(3)
            link = LINK_RE.search(cell)
            if "персональные данные" in label:
                table[path] = ("pii", "")
            elif link is None:
                table[path] = ("deleted", f"{HUB_URL}/blob/{PIN}/{path}")
            elif link.group(1).startswith("https://"):
                table[path] = ("url", link.group(1))
            else:
                table[path] = ("local", os.path.normpath(os.path.join(DOMAIN, link.group(1))))
    return table


def address(table: dict, path: str, source: str) -> str:
    path = path.rstrip("/")
    if path == DOMAIN:
        return SPOKE_URL
    if path in table:
        kind, target = table[path]
        if kind == "pii":
            raise SystemExit(f"{source}: ссылка на файл с персональными данными {path}")
        if kind == "local":
            return os.path.relpath(target, os.path.dirname(source))
        return target
    if any(p.startswith(path + "/") for p in table):
        return f"{HUB_URL}/tree/{TAG}/{path}"
    raise SystemExit(f"{source}: путь {path} не найден в манифесте")


def rewrite(hub: str, table: dict, source: str) -> int:
    full = os.path.join(hub, source)
    with open(full, encoding="utf-8") as fh:
        text = fh.read()
    count = 0

    def floating(m: re.Match) -> str:
        nonlocal count
        count += 1
        return address(table, m.group(1), source) + (m.group(2) or "")

    def relative(m: re.Match) -> str:
        nonlocal count
        resolved = os.path.normpath(os.path.join(os.path.dirname(source), m.group(1)))
        if resolved != DOMAIN and not resolved.startswith(DOMAIN + "/"):
            return m.group(0)
        count += 1
        return f"]({address(table, resolved, source)}{m.group(2) or ''})"

    text = FLOAT_RE.sub(floating, text)
    text = REL_RE.sub(relative, text)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"{source}: {count} ссылок переписано")
    return count


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    hub = argv[1]
    table = load(hub)
    total = sum(rewrite(hub, table, source) for source in argv[2:])
    print(f"итого: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
