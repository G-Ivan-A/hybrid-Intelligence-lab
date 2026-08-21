#!/usr/bin/env python3
"""Проверка относительных markdown-ссылок Хаба (issue #529, контракт 2).

Читает все отслеживаемые git'ом *.md и сообщает ссылки на несуществующие пути.
Внешние ссылки (http/https/mailto) и якоря (#...) пропускаются.
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                          cwd=Path(__file__).resolve().parent, capture_output=True,
                          text=True, check=True).stdout.strip())
LINK = re.compile(r'\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')

files = subprocess.run(["git", "ls-files", "*.md"], cwd=ROOT, capture_output=True,
                       text=True, check=True).stdout.split()
broken = []
for rel in files:
    path = ROOT / rel
    for num, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for target in LINK.findall(line):
            if target.startswith(("http://", "https://", "mailto:", "#", "<")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            if not (path.parent / clean).exists():
                broken.append((rel, num, target))

for rel, num, target in broken:
    print(f"{rel}:{num}: {target}")
print(f"\nBROKEN={len(broken)} FILES={len(files)}", file=sys.stderr)
