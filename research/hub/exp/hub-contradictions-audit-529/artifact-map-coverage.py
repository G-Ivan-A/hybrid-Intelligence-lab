#!/usr/bin/env python3
"""Сверка pr-ops/artifact-map.md с фактическим деревом Хаба (issue #529, контракт 2).

Первая колонка таблицы artifact-map содержит путь вида `/path/to/file`.
Скрипт печатает:
  MISSING — путь зарегистрирован в карте, но файла/каталога в репозитории нет;
  UNREGISTERED — отслеживаемый git'ом markdown-файл, которого нет в карте.
"""
import re, subprocess
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                          cwd=Path(__file__).resolve().parent, capture_output=True,
                          text=True, check=True).stdout.strip())
ROW = re.compile(r'^\|\s*`(/[^`]+)`\s*\|')

registered = []
for line in (ROOT / "pr-ops/artifact-map.md").read_text(encoding="utf-8").splitlines():
    m = ROW.match(line)
    if m:
        registered.append(m.group(1).lstrip("/"))

missing = [p for p in registered if not (ROOT / p).exists()]
regset = {p.rstrip("/") for p in registered}

tracked = subprocess.run(["git", "ls-files", "*.md"], cwd=ROOT, capture_output=True,
                         text=True, check=True).stdout.split()
unregistered = [f for f in tracked if f not in regset]

print("== MISSING (в карте есть, в репозитории нет) ==")
for p in missing:
    print(" ", p)
print(f"\n== UNREGISTERED ({len(unregistered)} из {len(tracked)} md-файлов) ==")
for f in unregistered:
    print(" ", f)
