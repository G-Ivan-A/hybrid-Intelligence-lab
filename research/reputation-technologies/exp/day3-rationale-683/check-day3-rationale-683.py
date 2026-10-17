#!/usr/bin/env python3
"""Check issue #683: the Day 3 rationale (document 1) follows RFC v0.3 and the deck and script approved in PR #682."""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
RATIONALE = DOMAIN / "2026-11-02-day3-rationale-and-method.md"
SCRIPT = DOMAIN / "2026-11-02-day3-lecturer-script.md"
# The NFR stop list of #671 and #681, applied to the whole rationale.
STOP = (("trigger word", re.compile(r"безопасн|разоблач|угроз|расследова|ловл[яиюе]", re.I)),
        ("risk rhetoric", re.compile(r"риск|вшив", re.I)),
        ("GRA formula", re.compile(r"формул(?!ир)|F\(t\)|\bH1\b", re.I)),
        ("provocation", re.compile(r"провок|провоц", re.I)),
        ("evaluative adjective", re.compile(r"честн|реалистичн|правдив", re.I)),
        ("incoming request", re.compile(r"запрос[а-я]* цен|прислал", re.I)),
        ("payments", re.compile(r"оплат|платёж|платеж|плат[ия]т|платил", re.I)),
        ("lawsuit analysis", re.compile(r"ФССП|дебитор|исполнительн[а-я]* производств", re.I)),
        ("old case 1", re.compile(r"(?<![\d.])(?:40|100) магазин", re.I)))
REQUIRED = ("более 100 оптовых", "5–8 торговых сетей за 3 месяца", "20 визиток", "25 магазинов",
            "компания действует, иски за годы работы есть", "гибко и одновременно аккуратно",
            "### Этика сбора: гибко и одновременно аккуратно", "Полезность для встречи", "| Полезн. |",
            "«не сейчас»", "звонком «Д»", "вопрос о сроках входа в матрицу", "web.archive.org",
            "381-ФЗ, 38-ФЗ, 98-ФЗ, 152-ФЗ, 259-ФЗ, 323-ФЗ", "ст. 152.2 ГК", "гармония или эклектика",
            "version: 0.3", "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/683")
# Headings other files link to must keep their anchors.
HEADINGS = ("### Кейс 1. B2B-производитель консервов: вход через тех, кто уже поставляет кандидату",
            "### Статус → действие или отказ", "### Разметка достоверности: собирать всё, решать по проверяемому",
            "### Текст промпта", "## Промпт-фильтр", "## Ограничения и допущения", "## Источники", "## Мост ко Дню 4",
            "## Главная мысль дня")
FENCE = re.compile(r"^```text\n(.*?)^```", re.S | re.M)


def prompt(text):
    i = text.find("### Текст промпта") if "### Текст промпта" in text else text.find("### А.2. Текст промпта")
    m = FENCE.search(text, i)
    return m.group(1).strip() if m else None


def check(text, script):
    errors = []
    for name, rx in STOP:
        for m in rx.finditer(text):
            errors.append(f"{name}: «{m.group(0)}» at line {text.count(chr(10), 0, m.start()) + 1}")
    harm = [m.start() for m in re.finditer(r"вред", text, re.I)]
    lines = {text.count("\n", 0, p) for p in harm}
    if len(lines) > 1 or (lines and "полезность для встречи" not in text.splitlines()[lines.pop()].lower()):
        errors.append("«вред» must appear in one paragraph only, translated into «полезность для встречи»")
    errors += [f"missing: {s}" for s in REQUIRED if s not in text]
    errors += [f"heading changed: {h}" for h in HEADINGS if not re.search("^" + re.escape(h) + "$", text, re.M)]
    if prompt(text) != prompt(script):
        errors.append("prompt text differs from section А.2 of the lecturer script")
    return errors


def self_test(text, script):
    assert not check(text, script), check(text, script)
    mutations = (("25 магазинов", "40 магазинов"), ("Полезность для встречи", "Возможный вред"),
                 ("гибко и одновременно аккуратно", "строго"), ("компания действует, иски за годы работы есть", "4 иска"),
                 ("## Источники", "## Литература"), ("ШАГ 0.", "ШАГ ноль."), ("«не сейчас»", "«нет»"))
    for a, b in mutations:
        assert a in text, a
        assert check(text.replace(a, b), script), f"mutation not caught: {a} -> {b}"
    for bad in ("риск", "F(t)", "оплата", "провокация", "прислал прайс", "ФССП"):
        assert check(text + "\n" + bad, script), f"stop word not caught: {bad}"
    print(f"self-test: {len(mutations) + 6} mutations caught")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    t, s = RATIONALE.read_text(encoding="utf-8"), SCRIPT.read_text(encoding="utf-8")
    if a.self_test:
        self_test(t, s)
    errs = check(t, s)
    for e in errs:
        print("FAIL", e)
    print("OK" if not errs else f"{len(errs)} problem(s)")
    sys.exit(1 if errs else 0)
