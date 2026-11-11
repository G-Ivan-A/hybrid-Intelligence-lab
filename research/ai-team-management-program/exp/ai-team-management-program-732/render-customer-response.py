#!/usr/bin/env python3
"""Вёрстка резюме проекта (ответа заказчику) на две страницы A4 (issues #732, #734).

Читает резюме проекта — по умолчанию оба варианта
projects/ai-team-management-program/docs/passport/project-summary-6m.md и
project-summary-3m.md, либо файлы из аргументов командной строки, —
переводит ограниченное подмножество Markdown (заголовки, абзацы, жирный шрифт,
ссылки, маркированные и нумерованные списки, таблицы) в HTML с A4-вёрсткой и
печатает его в PDF через headless Chrome. Затем считает страницы PDF и
завершается с ошибкой, если их больше двух. Итерация 3 (#734) добавила
проверку пункта 14 чек-листа шаблона резюме: в тексте нет утверждений об
отрасли заказчика и о «нет аналитики», которых нет в запросе.

Запуск (из корня репозитория):
    python3 -I research/ai-team-management-program/exp/ai-team-management-program-732/render-customer-response.py
Переменная CHROME задаёт путь к браузеру (по умолчанию google-chrome).
Флаг --html-only только пишет HTML во временный каталог (без PDF).
Пример для одного файла:
    python3 -I .../render-customer-response.py projects/ai-team-management-program/docs/passport/project-summary-3m.md
"""
import html
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[4]
PASSPORT = ROOT / "projects" / "ai-team-management-program" / "docs" / "passport"
DEFAULT_SOURCES = [PASSPORT / "project-summary-6m.md", PASSPORT / "project-summary-3m.md"]
# Пункт 14 чек-листа шаблона резюме (#734): запрет утверждений о заказчике,
# которых нет в запросе. Отрасль заказчика не названа — слово «банк» в резюме
# недопустимо; «аналитики … нет» — пример додумывания проблемы из итерации 2.
FORBIDDEN = [
    (r"(?i)\bбанк", "отрасль, которой нет в запросе заказчика"),
    (r"(?i)аналитик\w*[^.]{0,60}\bнет\b", "утверждение об отсутствии аналитики у заказчика"),
]
MAX_PAGES = 2
MAX_WORDS = 900  # 700–900 слов: рекомендация отчёта 2026-11-11-multi-case-design-and-proposal-format-evidence.md, §2.2.3
TABLE_PT = "12pt"  # ГОСТ Р 7.0.97-2025 рекомендует 12–14 pt; 11 pt — отклонение

CSS = """
@page { size: A4; margin: 20mm 15mm 20mm 20mm; }
* { box-sizing: border-box; }
body { font-family: "PT Sans", "Liberation Sans", Arial, sans-serif;
       font-size: 12pt; line-height: 1.1; color: #1a1a1a; margin: 0; }
h1 { font-size: 14pt; margin: 0 0 1mm 0; color: #0b3d63; }
h2 { font-size: 13pt; margin: 2.4mm 0 0.8mm 0; color: #0b3d63;
     border-bottom: 0.4pt solid #0b3d63; padding-bottom: 0.3mm; }
p { margin: 0 0 1.2mm 0; text-align: justify; hyphens: auto; }
p.sub { color: #555; margin-bottom: 1.6mm; }
table { border-collapse: collapse; width: 100%; margin: 0.6mm 0 1.4mm 0;
        page-break-inside: avoid; font-size: TABLE_PT; }
th, td { border: 0.4pt solid #9aa9b5; padding: 0.4mm 1.2mm; vertical-align: top;
         text-align: left; }
th { background: #e8eff5; font-weight: bold; }
ul, ol { margin: 0 0 1.2mm 0; padding-left: 5mm; }
li { margin: 0 0 0.3mm 0; }
a { color: #0b3d63; text-decoration: none; }
"""


def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t


def convert(md):
    md = re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.S)
    lines = md.splitlines()
    out, i, first_par = [], 0, True
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("# "):
            out.append("<h1>{}</h1>".format(inline(line[2:])))
            i += 1
            continue
        if line.startswith("## "):
            out.append("<h2>{}</h2>".format(inline(line[3:])))
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(re.fullmatch(r":?-+:?", c) for c in r)]
            t = ["<table><tr>" + "".join("<th>{}</th>".format(inline(c)) for c in head) + "</tr>"]
            for r in body:
                t.append("<tr>" + "".join("<td>{}</td>".format(inline(c)) for c in r) + "</tr>")
            out.append("".join(t) + "</table>")
            continue
        m = re.match(r"^(- |\d+\. )", line)
        if m:
            tag = "ul" if line.startswith("- ") else "ol"
            items = []
            while i < len(lines) and lines[i].strip():
                if re.match(r"^(- |\d+\. )", lines[i]):
                    items.append(re.sub(r"^(- |\d+\. )", "", lines[i]))
                else:
                    items[-1] += " " + lines[i].strip()
                i += 1
            out.append("<{0}>{1}</{0}>".format(tag, "".join("<li>{}</li>".format(inline(x)) for x in items)))
            continue
        par = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "|", "- ")) \
                and not re.match(r"^\d+\. ", lines[i]):
            par.append(lines[i].strip())
            i += 1
        cls = ' class="sub"' if first_par else ""
        first_par = False
        out.append("<p{}>{}</p>".format(cls, inline(" ".join(par))))
    return out


def count_words(md):
    body = re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.S)
    return len(re.findall(r"[0-9A-Za-zА-Яа-яЁё][0-9A-Za-zА-Яа-яЁё,\-–]*", body))


def count_pages(pdf_bytes):
    return len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", pdf_bytes))


def render(src, html_only):
    pdf = src.with_suffix(".pdf")
    md = src.read_text(encoding="utf-8")
    if re.search(r"\{N_[A-Z]+\}", md):
        sys.exit("{}: остались незаполненные подстановки {{N_...}}.".format(src.name))
    body_md = re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.S)
    for pattern, why in FORBIDDEN:
        hit = re.search(pattern, body_md)
        if hit:
            sys.exit("{}: {} — «{}».".format(src.name, why, hit.group(0)))
    words = count_words(md)
    body = "\n".join(convert(md))
    doc = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
           "<title>Резюме проекта</title><style>{}</style></head><body>{}</body></html>").format(
               CSS.replace("TABLE_PT", TABLE_PT), body)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="project-summary-"))
    page = tmp / (src.stem + ".html")
    page.write_text(doc, encoding="utf-8")
    if html_only:
        print(page)
        return
    chrome = os.environ.get("CHROME") or shutil.which("google-chrome") or shutil.which("chromium")
    if not chrome:
        sys.exit("Не найден браузер Chrome/Chromium для печати PDF.")
    out = tmp / "out.pdf"
    subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
                    "--no-pdf-header-footer", "--print-to-pdf={}".format(out), page.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    data = out.read_bytes()
    pages = count_pages(data)
    pdf.write_bytes(data)
    print("PDF: {} — страниц: {}, слов: {}".format(pdf.relative_to(ROOT), pages, words))
    if words > MAX_WORDS:
        sys.exit("{}: длиннее {} слов — сократите текст.".format(src.name, MAX_WORDS))
    if pages > MAX_PAGES:
        sys.exit("{}: длиннее {} страниц A4 — сократите текст.".format(src.name, MAX_PAGES))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sources = [pathlib.Path(a).resolve() for a in args] or DEFAULT_SOURCES
    for src in sources:
        render(src, "--html-only" in sys.argv)


if __name__ == "__main__":
    main()
