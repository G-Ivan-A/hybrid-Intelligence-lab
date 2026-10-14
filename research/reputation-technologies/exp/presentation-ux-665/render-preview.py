#!/usr/bin/env python3
"""Render representative dense slides from the actual Markdown, without AI images."""
import argparse
import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
# The "after" view reads the current file, except Day 2: it was rebuilt on RFC v0.3 in #673,
# so its #665 layout is taken from the last commit before #673.
SELECTED = [
    (1, "2026-10-07-day1-presentation-653.md", "7", None),
    (2, "2026-10-30-day2-presentation.md", "10", "16e2577"),
    (3, "2026-11-02-day3-presentation.md", "13", None),
]


def diagram(day):
    labels = {
        1: [("Масса", "Ресурсы · позиция", "Сеть · реп. капитал"),
            ("Дистанция", "Срок контакта", "Рабочий канал"),
            ("Полярность", "Знак + / − / ?", "От кого → к кому")],
        2: [("VERIFIED", "Основание есть", "Дата и контекст"),
            ("PARTIAL", "Недостаточно", "Причина → проверка"),
            ("CONFLICT", "Версии расходятся", "Обе версии отдельно")],
        3: [("1. Доступность", "Канал и срок", ""),
            ("2. Значимость", "Действие под задачу", ""),
            ("3. Качество", "Источник и статус", ""),
            ("4. Вред", "Возможное вето", "")],
    }[day]
    cards = []
    for i, lines in enumerate(labels):
        y = 20 + i * 140
        border = "#a94843" if day == 3 and i == 3 else "#ae6500"
        dash = ' stroke-dasharray="9 6"' if day == 2 and i == 1 else ""
        cards.append(f'<rect x="12" y="{y}" width="586" height="116" rx="16" fill="#faf7ef" stroke="{border}" stroke-width="3"{dash}/>')
        for j, label in enumerate(lines):
            if label:
                cards.append(f'<text x="40" y="{y + 37 + j * 31}" font-size="{29 if j == 0 else 25}" font-weight="{700 if j == 0 else 400}" fill="#24313b">{html.escape(label)}</text>')
        if day == 3 and i < len(labels) - 1:
            cards.append(f'<path d="M305 {y + 118} v18 m-7 -7 l7 7 l7 -7" fill="none" stroke="#24313b" stroke-width="3"/>')
    return '<svg role="img" aria-label="Рабочая схема по спецификации слайда" viewBox="0 0 610 590">' + "".join(cards) + "</svg>"


def slide(day, name, key, pinned, before):
    path = DOMAIN / name
    ref = "6428ade" if before else pinned
    text = subprocess.check_output(["git", "show", f"{ref}:{path.relative_to(ROOT)}"], cwd=ROOT, text=True) if ref else path.read_text()
    match = re.search(rf'^\*\*Слайд {key}\. (.+?)\*\*\n(.*?)(?=^\*\*Слайд |^## Промпты|^### Завершение)', text, re.M | re.S)
    title, body = match.groups()
    paragraph = re.search(r'^- Раскрытие тезисов: (.+)$', body, re.M)
    conclusion = re.search(r'^- (?:Сдвиг|Главный вывод \(как меняется мышление\)): (.+)$', body, re.M)
    bullets = []
    notes = []
    for line in body.splitlines():
        if line.startswith("- ") and not any(line.startswith("- " + field) for field in (
            "Визуал:", "Сдвиг:", "Главный вывод", "Раскрытие тезисов:", "Альтернативный промпт")):
            line = re.sub(r'\*\*|`', '', line[2:])
            line = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', line)
            if line.startswith(("Внизу мелко:", "Значок:")):
                notes.append('<p>' + html.escape(line) + '</p>')
            elif not line.startswith(("Три бирки по центру:", "Четыре строки:")):
                bullets.append('<li>' + html.escape(line) + '</li>')
    context = '<div class="context"><p>' + html.escape(paragraph[1]) + '</p></div>' if paragraph else ''
    return f'''<article class="slide" data-day="{day}" data-slide="{key}">
<div class="eyebrow">День {day} · слайд {key} · {'до #665' if before else 'после #665'}</div>
<h1>{html.escape(title)}</h1>
<div class="body"><section class="text"><ul>{''.join(bullets)}</ul>{context}</section>
<aside class="{'with-notes' if notes else ''}">{diagram(day)}<div class="notes">{''.join(notes)}</div></aside></div>
<footer><b>{'Сдвиг' if before else 'Главный вывод (как меняется мышление)'}</b><span>{html.escape(conclusion[1])}</span></footer>
</article>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    css = '''*{box-sizing:border-box}body{margin:0;background:#dce1e5;font-family:Arial,sans-serif;color:#24313b}
    .slide{width:1920px;height:1080px;padding:50px 64px;background:#fffdf7;display:flex;flex-direction:column;border-bottom:12px solid #dce1e5}
    .eyebrow{font-size:24px;letter-spacing:2px;color:#57636d;margin-bottom:15px}
    h1{font-size:49px;line-height:1.14;margin:0 0 30px;font-weight:700}
    .body{display:grid;grid-template-columns:1.75fr 1fr;gap:54px;flex:1;min-height:0}
    .text{min-height:0;overflow:hidden}ul{padding-left:32px;margin:0 0 24px;font-size:32px;line-height:1.25}li{margin-bottom:12px}
    .context{border-left:6px solid #ae6500;padding-left:24px}.context p{font-size:32px;line-height:1.3;margin:0}
    aside svg{width:100%;max-height:590px}.with-notes svg{height:380px}.notes p{font-size:24px;line-height:1.3;margin:8px 0}.caption{font-size:24px;line-height:1.3;color:#57636d;margin:10px 0}
    footer{margin-top:26px;border-top:2px solid #ccc5b9;padding-top:20px;display:grid;grid-template-columns:470px 1fr;gap:30px;font-size:28px;line-height:1.25}
    footer b{color:#854c00}'''
    document = '<!doctype html><html lang="ru"><meta charset="utf-8"><title>Прототип слайдов #665</title><style>' + css + '</style><body>'
    document += ''.join(slide(d, n, k, p, args.before) for d, n, k, p in SELECTED)
    document += '</body></html>'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(document)
    print(args.output)


if __name__ == "__main__":
    main()
