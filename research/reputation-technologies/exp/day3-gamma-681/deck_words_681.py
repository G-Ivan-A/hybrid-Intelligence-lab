#!/usr/bin/env python3
"""Count the words of each slide text in Gamma decks: the labels and the common header are not counted (meta-analysis of #681)."""
import re
import statistics
import sys
from pathlib import Path

LABEL = re.compile(r"^\s*-\s*(?:Шапка|Надзаголовок|Заголовок|Подзаголовок|Эпиграф|Вводный абзац|Карточка|Вывод):\s*")


def words(text):
    return len([token for token in text.split() if re.search(r"\w", token)])


def slide_words(path):
    body = Path(path).read_text(encoding="utf-8").split("\n## Слайды", 1)[1]
    counts = []
    for chunk in re.split(r"\n### Слайд \d+\.", body)[1:]:
        text = chunk.split("**[SLIDE_TEXT]**", 1)[1].split("**[IMAGE_PROMPT]**", 1)[0]
        counts.append(sum(words(LABEL.sub("", line)) for line in text.splitlines() if not re.match(r"^\s*-\s*Шапка:", line)))
    return counts


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: deck_words_681.py DECK.md [DECK.md ...]")
    for path in sys.argv[1:]:
        counts = slide_words(path)
        print(f"{Path(path).name}: {len(counts)} slides, median {statistics.median(counts)}, min {min(counts)}, max {max(counts)}, "
              f"slides 1–4 median {statistics.median(counts[:4])}")
        print("  " + " ".join(str(count) for count in counts))


if __name__ == "__main__":
    main()
