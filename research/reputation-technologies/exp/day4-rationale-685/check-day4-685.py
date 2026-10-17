#!/usr/bin/env python3
"""Check issue #685: the Day 4 rationale and method lists slides 1–4 of block А and the 22 RFC v0.3 slides of block Б, each with a title of at most six words, two or three key theses and a logic comment, keeps the mandatory nodes and the hard constraints, and confirms all eight gate items."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
DOC = DOMAIN / "2026-11-03-day4-rationale-and-method.md"
FILES = (DOC,)
SOURCE = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/685"
REPO_BLOB = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
SLIDE = re.compile(r"^### Слайд (\d+)\. (.+)$", re.M)
LINK = re.compile(r"\]\(([^)\s]+)\)")
# Block А is slides 1–4; block Б keeps every RFC v0.3 slide after the cover and the route (2–4 and 6–24) as slides 5–26.
SLIDES = 26
TITLE_WORDS = 6
THESES = (2, 3)
THESES_HEAD = "**Ключевые тезисы:**"
LOGIC_HEAD = "**Логика и комментарий:**"
# The NFR stop list of #671, kept by #673, #677, #679 and #681: verbatim quotes (lines starting with «>»), link targets and code blocks are exempt.
TRIGGERS = re.compile(r"безопасн|разоблач|угроз|расследова|ловл[яиюе]", re.I)
DAY_TONE = re.compile(r"риск|вшив", re.I)
FORMULA = re.compile(r"формул(?!ир)|F\(t\)|\bH1\b", re.I)
PROVOCATION = re.compile(r"провок|провоц", re.I)
EVALUATIVE = re.compile(r"честн|реалистичн|правдив", re.I)
STOP_LISTS = (("trigger word", TRIGGERS), ("risk or «вшивость» rhetoric", DAY_TONE), ("GRA formula", FORMULA),
              ("provocation", PROVOCATION), ("evaluative adjective of #663", EVALUATIVE))
# #685: case 1 is proactive search only — no incoming request anywhere, quotes, links and code included.
RAW_INCOMING = re.compile(r"запрос[а-я]* цен|прислал|входящ", re.I)
PROACTIVE = "сам пишет сетям первым"
CASE = re.compile(r"более 100 оптовых")
OLD_CASE = re.compile(r"(?<![\d.])100 магазин|(?<![а-яё])сто магазин|(?<![\d.])40 магазин|сорок магазин", re.I)
STORES = "25 магазинов"
# #685: lawsuits are only an activity marker; no forensic reading and no conclusions about how the network pays.
PAYMENT = re.compile(r"оплат|платёж|платеж|плат[ия]т|платил", re.I)
NEGATION = re.compile(r"(?<![а-яё])(?:не|ни|нет|нельзя|без|вне)(?![а-яё])|запрещ", re.I)
FORENSIC = re.compile(r"форензик|предмет[а-я]* спор|сумм[а-я]* иск", re.I)
ACTIVITY = re.compile(r"(?:иск|судебн)[а-я]*[^.\n]{0,240}маркер[а-я]* активности|маркер[а-я]* активности[^.\n]{0,240}(?:иск|судебн)", re.I)
# #685: the program word is never a filter criterion; «полезность для встречи» is named as an adaptation of the Technograd term.
HARM = re.compile(r"вред", re.I)
USEFUL = "полезность для встречи"
ADAPTATION = re.compile(r"«полезность для встречи»[^\n]{0,200}адапт|адапт[^\n]{0,200}«полезность для встречи»", re.I)
# #685: the first step is not the global image strategy or a rebranding.
REBRAND = re.compile(r"[Гг]лобальная имиджевая стратегия[^.\n]{0,120}ребрендинг[^.\n]{0,160}вне задачи дня")
# Slides 1–4 of block А.
COVER = ("Имиджевые стратегии для действия", "Действую: выстраиваем первый контакт",
         "Управляйте данными о связях — и первый контакт станет вашим ходом")
LECTURER = ("`VERIFIED`", "`PARTIAL`", "«?»", "гармони", "эклектик", "+1")
COURSE_MAP = ("День 1 · Вижу — «Репутационный инжиниринг: ключевые составляющие»",
              "День 2 · Собираю — «Мониторинг ресурсов, работа с данными»",
              "День 3 · Выбираю — «Внутренние и внешние факторы влияния на развитие компании»",
              "День 4 · Действую — «Имиджевые стратегии для действия» (сегодня)",
              "Вижу → Собираю → Выбираю → **Действую**")
ROUTE = ("«Имидж как система данных» → «Все методики — гипотезы» → «Гармония vs Эклектика»",
         "карточка первого контакта на одну страницу")
# Mandatory nodes of block Б: slide number → phrases that slide must carry.
NODES = {
    9: ("Г4-1", "Согласованность", "недостоверность", "`PARTIAL`"),
    13: ("Все методики — гипотезы", "●", "◐", "○"),
    14: ("контрастов", "◐", "цветотипов", "○"),
    17: ("гармони", "подстрой"),
    19: ("полярности +1, малой дистанции и высокой массе", "гармония с одной контрастной деталью", "«?»", "−1"),
    21: ("Промпт-стратег", "обещает больше, чем подтверждают статусы Дня 2"),
    23: ("«Д» (`CONFLICT`", "короткий звонок, подстройка, вопрос о текущих процессах", "«С» (`VERIFIED`)",
         "просьба о знакомстве", "Коммерческий директор", "пилотной партии"),
    24: ("точка, статус, полярность, дистанция", "вид, стиль и канал", "первая фраза", "что записать после встречи",
         "Возврат к голосованию слайда 6"),
}
VOTE, TRIAL = "🗳", "🤖"
VOTES, TRIALS = {6, 18}, {21}
# The card of the artifact: every field the issue names, each a row of the card table.
CARD_FIELDS = ("Точка", "Статус данных", "Полярность", "Дистанция", "Вид шага", "Стиль", "Канал", "Первая фраза", "Что записать после")
CASE_COLUMNS = "| Поле | Дистрибьютор «Д» | Сопоставщик «С» | Коммерческий директор сети «Х» |"
SECTIONS = ("## Как читать этот документ", "## Аппеляции", "## Главная мысль дня", "## Цепочка «потому что → поэтому»",
            "## Правила дня", "## Гипотезы дня", "## Артефакт: карточка первого контакта", "## Нумерация: документ и RFC v0.3",
            "## Блок А. Вход (слайды 1–4)", "## Кейс 1: три первых шага", "## Промпт-стратег: текст для пробы",
            "## Поминутный тайминг и бюджет", "## Покрытие программы Технограда", "## Как меняется мышление слушателя",
            "## Метод: 90 минут для пассивной вечерней аудитории", "## Мост: после курса", "## Ограничения и допущения",
            "## Источники", "## Гейт-проверка")
TOTAL = "| **Итого** | 26 слайдов | **90** | 18:30–20:00 |"
SHARE = "61,5 минуты из 90, это 68%"
RFC = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-10-12-rfc-days-1-3-logic.md#день-4-действую-выстраиваем-первый-контакт"
PROGRAM = "https://technograd.moscow/event_page_new?669#programm_event"
GATE_ITEMS = 8


def frontmatter(text):
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return dict(line.split(": ", 1) for line in match[1].splitlines() if ": " in line) if match else {}


def plain(text):
    """Text without blockquotes and code: verbatim quotes of the program, the founder's appeals and the prompt keep their own words."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return "\n".join(line for line in text.splitlines() if not line.startswith(">"))


def prose(text):
    """Plain text without link targets: headings of other files may keep their own words."""
    return re.sub(r"\]\([^)]*\)", "]", plain(text))


def anchors(text):
    """GitHub-style heading anchors of a Markdown text."""
    seen, result = {}, set()
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    for match in re.finditer(r"^#{1,6} (.+?)\s*#*$", text, re.M):
        title = re.sub(r"`|\*\*|\[([^\]]*)\]\([^)]*\)", lambda m: m[1] or "", match[1])
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        result.add(slug if count == 0 else f"{slug}-{count}")
    return result


def broken_links(text, texts):
    """Repository links whose file or anchor is missing; texts overrides files under test."""
    cache = {}
    for url in sorted(set(LINK.findall(text))):
        if not url.startswith(REPO_BLOB):
            continue
        path, _, anchor = url[len(REPO_BLOB):].partition("#")
        target = ROOT / path
        if not texts.get(target) and not target.is_file():
            yield f"{url}: file not found"
        elif anchor and target.suffix == ".md":
            if target not in cache:
                cache[target] = anchors(texts.get(target) or target.read_text(encoding="utf-8"))
            if anchor not in cache[target]:
                yield f"{url}: anchor not found"


def slides(text):
    matches = list(SLIDE.finditer(text))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        tail = re.search(r"^#{1,3} ", text[match.end():end], re.M)
        yield int(match[1]), match[2], text[match.end():match.end() + tail.start() if tail else end]


def fields(chunk):
    """Theses and logic comment of a slide in the exact format of #685: theses heading, bullets, logic heading, comment."""
    match = re.match(r"\n\n" + re.escape(THESES_HEAD) + r"\n((?:- [^\n]+\n)+)\n" + re.escape(LOGIC_HEAD) + r"\n(.+)", chunk, re.S)
    if not match:
        return None, None
    return re.findall(r"^- (.+)$", match[1], re.M), match[2].strip()


def stop_words(name, text, clean):
    errors = []
    for label, pattern in STOP_LISTS:
        for match in sorted(set(pattern.findall(clean)))[:3]:
            errors.append(f"{name}: {label}: «{match}»")
    for match in sorted(set(RAW_INCOMING.findall(text)))[:3]:
        errors.append(f"{name}: incoming request plot: «{match}»")
    for match in sorted(set(PAYMENT.findall(text)))[:1]:
        errors.append(f"{name}: payment discipline discussed: «{match}»")
    for match in sorted(set(HARM.findall(text)))[:1]:
        errors.append(f"{name}: the program word «{match}» is used instead of «{USEFUL}»")
    if not ADAPTATION.search(clean):
        errors.append(f"{name}: «{USEFUL}» is not named as an adaptation of the program term")
    if OLD_CASE.search(clean):
        errors.append(f"{name}: case 1 still counts «100 магазинов» or the 40 stores of #663")
    for phrase, label in ((PROACTIVE, "the producer"), (STORES, "the network «Х» has")):
        if phrase not in clean:
            errors.append(f"{name}: case 1 does not say {label} «{phrase}»")
    if not CASE.search(clean):
        errors.append(f"{name}: case 1 does not say «более 100 оптовых покупателей»")
    if not ACTIVITY.search(clean):
        errors.append(f"{name}: lawsuits are not described as an activity marker")
    for sentence in re.split(r"(?<=[.!?])\s+|\n", clean):
        if FORENSIC.search(sentence) and not NEGATION.search(sentence):
            errors.append(f"{name}: lawsuits read forensically: «{sentence.strip()[:90]}»")
            break
    if not REBRAND.search(clean):
        errors.append(f"{name}: no sentence puts the global image strategy and rebranding outside the task of the day")
    return errors


def validate_doc(texts):
    errors, text, name = [], texts[DOC], DOC.name
    clean = prose(text)
    errors += stop_words(name, text, clean)
    for heading in SECTIONS:
        if not re.search(r"^" + re.escape(heading) + r"$", text, re.M):
            errors.append(f"{name}: section «{heading}» missing")
    for url in (RFC, PROGRAM):
        if f"]({url})" not in text:
            errors.append(f"{name}: SSOT link missing: {url}")
    deck = list(slides(text))
    if [n for n, _, _ in deck] != list(range(1, SLIDES + 1)):
        errors.append(f"{name}: slides are not 1–{SLIDES}: {[n for n, _, _ in deck][:40]}")
    body = {}
    low, high = THESES
    for n, title, chunk in deck:
        words = [word for word in title.replace(VOTE, " ").replace(TRIAL, " ").split() if re.search(r"\w", word)]
        if len(words) > TITLE_WORDS:
            errors.append(f"{name}: slide {n} title has {len(words)} words, more than {TITLE_WORDS}")
        theses, logic = fields(chunk)
        if theses is None:
            errors.append(f"{name}: slide {n} is not «{THESES_HEAD}» with bullets, then «{LOGIC_HEAD}» with a comment")
            continue
        if not low <= len(theses) <= high:
            errors.append(f"{name}: slide {n} has {len(theses)} key theses, not {low}–{high}")
        if "*Потому что → поэтому.* Потому что" not in logic or "поэтому" not in logic:
            errors.append(f"{name}: slide {n} logic comment has no «потому что → поэтому» bridge")
        for part in ("*Почему здесь.*", "*Методологическая задача.*", "*GRA и кейс 1.*", "*Формат и время:*"):
            if part not in logic:
                errors.append(f"{name}: slide {n} logic comment has no {part}")
        body[n] = prose(chunk)
    for phrase in COVER:
        if phrase not in body.get(1, ""):
            errors.append(f"{name}: slide 1 does not carry «{phrase}»")
    for phrase in LECTURER:
        if phrase not in body.get(2, ""):
            errors.append(f"{name}: slide 2 does not carry «{phrase}»")
    for phrase in COURSE_MAP:
        if phrase not in body.get(3, ""):
            errors.append(f"{name}: slide 3 lost the course map line «{phrase[:60]}»")
    for phrase in ROUTE:
        if phrase not in body.get(4, ""):
            errors.append(f"{name}: slide 4 does not carry «{phrase}»")
    for n, phrases in NODES.items():
        for phrase in phrases:
            if phrase not in body.get(n, ""):
                errors.append(f"{name}: slide {n} lost the mandatory node «{phrase}»")
    votes = {n for n, title, _ in deck if VOTE in title}
    trials = {n for n, title, _ in deck if TRIAL in title}
    if votes != VOTES or trials != TRIALS:
        errors.append(f"{name}: votes {sorted(votes)} and prompt trials {sorted(trials)}, expected {sorted(VOTES)} and {sorted(TRIALS)}")
    card = text.split("## Артефакт: карточка первого контакта", 1)[-1].split("\n## ", 1)[0]
    for field in CARD_FIELDS:
        if not re.search(r"^\| " + re.escape(field) + r" ", card, re.M):
            errors.append(f"{name}: the first-contact card has no field «{field}»")
    case = text.split("## Кейс 1: три первых шага", 1)[-1].split("\n## ", 1)[0]
    if CASE_COLUMNS not in case:
        errors.append(f"{name}: case 1 does not lay out three steps for «Д», «С» and the commercial director")
    for field in CARD_FIELDS[1:]:
        row = re.search(r"^\| " + re.escape(field) + r" \|(.+)\|$", case, re.M)
        cells = [cell.strip() for cell in row[1].split("|")] if row else []
        if len(cells) != 3 or len(set(cells)) != 3:
            errors.append(f"{name}: case 1 row «{field}» does not give three different values")
    for phrase in (TOTAL, SHARE):
        if phrase not in text:
            errors.append(f"{name}: timing anchor missing: «{phrase}»")
    gate = text.split("## Гейт-проверка", 1)[-1]
    done, open_items = re.findall(r"^- \[x\] ", gate, re.M), re.findall(r"^- \[ \] ", gate, re.M)
    if len(done) != GATE_ITEMS or open_items:
        errors.append(f"{name}: gate has {len(done)} confirmed and {len(open_items)} open items, expected {GATE_ITEMS} confirmed")
    if "<!--" in text:
        errors.append(f"{name}: a draft comment is left in the file")
    return errors


def validate(texts):
    missing = [path for path in FILES if not texts[path]]
    errors = [f"{path.name}: file not found" for path in missing]
    if missing:
        return errors
    for path in FILES:
        text, name = texts[path], path.name
        if frontmatter(text).get("source", "").strip('"') != SOURCE:
            errors.append(f"{name}: frontmatter source is not issue #685")
        relative = [url for url in LINK.findall(text) if not re.match(r"https?://", url)]
        if relative:
            errors.append(f"{name}: links are not full URLs: {relative[:3]}")
        errors += [f"{name}: {error}" for error in broken_links(text, texts)]
    errors += validate_doc(texts)
    return errors


def mutate(texts, path, old, new, count=1):
    changed = dict(texts)
    changed[path] = texts[path].replace(old, new, count)
    return changed


def mutate_re(texts, path, pattern, new, count=1):
    changed = dict(texts)
    changed[path] = re.sub(pattern, new, texts[path], count=count, flags=re.M | re.S)
    return changed


def self_test(texts):
    d = DOC
    broken = {
        "file missing": mutate_re(texts, d, r".*", "", count=1),
        "source is another issue": mutate(texts, d, 'source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/685"', 'source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/681"'),
        "last slide removed": mutate_re(texts, d, r"^### Слайд 26\. .*?(?=^## )", ""),
        "block Б capped at slide 24": mutate_re(texts, d, r"^### Слайд 25\. .*?(?=^## Кейс 1)", ""),
        "slides out of order": mutate(texts, d, "### Слайд 8. ", "### Слайд 9. "),
        "title longer than six words": mutate(texts, d, "### Слайд 10. Свой, но заметный", "### Слайд 10. Свой, но заметный для каждого будущего партнёра"),
        "theses heading renamed": mutate(texts, d, THESES_HEAD, "**Тезисы:**"),
        "logic heading renamed": mutate(texts, d, LOGIC_HEAD, "**Комментарий:**"),
        "one key thesis only": mutate_re(texts, d, r"(### Слайд 7\. [^\n]+\n\n\*\*Ключевые тезисы:\*\*\n- [^\n]+\n)- [^\n]+\n", r"\1"),
        "four key theses": mutate_re(texts, d, r"(### Слайд 5\. [^\n]+\n\n\*\*Ключевые тезисы:\*\*\n)", r"\1- Лишний тезис.\n"),
        "bridge lost": mutate_re(texts, d, r"(### Слайд 12\..*?)\*Потому что → поэтому\.\*", r"\1*Мостик.*"),
        "logic part lost": mutate_re(texts, d, r"(### Слайд 15\..*?)\*GRA и кейс 1\.\*", r"\1*Кейс.*"),
        "cover subtitle lost": mutate(texts, d, "подзаголовок — «Действую: выстраиваем первый контакт»", "подзаголовок — «Первый контакт»"),
        "cover slogan lost": mutate(texts, d, "Слоган дня: «Управляйте данными о связях — и первый контакт станет вашим ходом».", "Слоган дня: «Действуйте»."),
        "lecturer statuses lost": mutate_re(texts, d, r"(### Слайд 2\.)(.*?)(?=^### Слайд 3\.)", lambda m: m[1] + m[2].replace("`PARTIAL`", "частично")),
        "course map: Day 4 not today": mutate(texts, d, "«Имиджевые стратегии для действия» (сегодня)", "«Имиджевые стратегии для действия»"),
        "route without the card": mutate(texts, d, "Артефакт к 20:00 — карточка первого контакта на одну страницу", "Артефакт к 20:00 — план"),
        "Г4-1 lost": mutate(texts, d, "Гипотеза Г4-1 ○: шаг", "Гипотеза ○: шаг"),
        "color types not a hypothesis": mutate(texts, d, "цветотипов не имеют рецензируемой проверки ○", "цветотипов работают ●"),
        "eclectic rule lost": mutate(texts, d, "открытая эклектика — только при полярности +1, малой дистанции и высокой массе говорящего.", "открытая эклектика — когда хочется."),
        "prompt trial without the Day 2 check": mutate(texts, d, "найти, где ИИ обещает больше, чем подтверждают статусы Дня 2", "оценить ответ ИИ"),
        "«Д» step lost": mutate(texts, d, "короткий звонок, подстройка, вопрос о текущих процессах", "письмо"),
        "case 1 steps identical": mutate_re(texts, d, r"^\| Вид шага \| разговор \| просьба о знакомстве \| [^|\n]+ \|$", "| Вид шага | разговор | разговор | разговор |"),
        "card field lost": mutate(texts, d, "| Первая фраза | одна фраза", "| Фраза | одна фраза"),
        "no return to the vote": mutate(texts, d, "Возврат к голосованию слайда 6", "Итог"),
        "third vote": mutate(texts, d, "### Слайд 11. ", f"### Слайд 11. {VOTE} "),
        "prompt trial moved": mutate(texts, d, f"### Слайд 21. {TRIAL} ", "### Слайд 21. "),
        "GRA formula": mutate(texts, d, "На Дне 4 нет математики", "На Дне 4 есть формула F(t)"),
        "H1 named": mutate(texts, d, "На Дне 4 нет математики", "На Дне 4 проверяем H1"),
        "incoming request plot": mutate(texts, d, "ни одна сеть к нему не обращалась", "сеть прислала ему входящий запрос цен"),
        "not proactive": mutate(texts, d, PROACTIVE, "ждёт сети", count=-1),
        "«вред» as a criterion": mutate(texts, d, "| Что записать после | был ли второй шаг", "| Что записать после | какой вред"),
        "«вред» in a quote": mutate(texts, d, "> 1. АППЕЛЯЦИЯ:", "> Четвёртый вопрос — вред.\n> 1. АППЕЛЯЦИЯ:"),
        "adaptation note lost": mutate_re(texts, d, r"адапт[а-я]*", "название", count=0),
        "payment discipline": mutate(texts, d, "Иски за годы работы — только маркер активности сети", "Иски показывают, как сеть платит поставщикам"),
        "lawsuits as forensics": mutate(texts, d, "Иски за годы работы — только маркер активности сети: компания действует и ведёт дела.", "Иски за годы работы разбираем по предметам споров и суммам исков."),
        "rebranding mixed in": mutate(texts, d, "Глобальная имиджевая стратегия компании, ребрендинг, смена логотипа и фирменного стиля — вне задачи дня.", "Первый шаг начинается с ребрендинга."),
        "old case store count": mutate(texts, d, "Сеть «Х» на 25 магазинов не", "Сеть «Х» на 40 магазинов не"),
        "wholesale buyers lost": mutate(texts, d, "более 100 оптовых", "многих оптовых", count=-1),
        "trigger word": mutate(texts, d, "Не судим людей по внешности", "Безопасность встречи"),
        "risk rhetoric outside a quote": mutate(texts, d, "## Главная мысль дня\n", "## Главная мысль дня\n\nПервый шаг снижает риск.\n"),
        "provocation outside a quote": mutate(texts, d, "## Главная мысль дня\n", "## Главная мысль дня\n\nПровокация не нужна.\n"),
        "evaluative adjective": mutate(texts, d, "Прямой ответ — отчасти да", "Честный ответ — отчасти да"),
        "relative link": mutate(texts, d, "](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/", "](../"),
        "broken anchor": mutate(texts, d, "#день-4-действую-выстраиваем-первый-контакт", "#день-4", count=-1),
        "missing file link": mutate(texts, d, "2026-10-30-day2-rationale-and-method.md#", "2026-10-30-day2-rationale.md#"),
        "SSOT program link lost": mutate(texts, d, PROGRAM, "https://technograd.moscow/", count=-1),
        "section lost": mutate(texts, d, "## Ограничения и допущения", "## Прочее"),
        "timing total changed": mutate(texts, d, TOTAL, "| **Итого** | 26 слайдов | **95** | 18:30–20:05 |"),
        "gate item open": mutate(texts, d, "- [x] Описан артефакт", "- [ ] Описан артефакт"),
        "gate item lost": mutate_re(texts, d, r"^- \[x\] Описан артефакт[^\n]*\n", ""),
        "draft comment left": mutate(texts, d, "## Гейт-проверка", "<!-- TODO -->\n## Гейт-проверка"),
    }
    failed = [name for name, mutated in broken.items() if mutated == texts or not validate(mutated)]
    return failed, len(broken)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="also prove the checker rejects broken fixtures")
    args = parser.parse_args()
    texts = {path: path.read_text(encoding="utf-8") if path.is_file() else "" for path in FILES}
    errors = validate(texts)
    if args.self_test and not errors:
        failed, fixtures = self_test(texts)
        errors += [f"self-test: mutation not rejected: {name}" for name in failed]
    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        raise SystemExit(1)
    print(f"PASS: {SLIDES} slides in order — block А 1–4 and block Б 5–{SLIDES} with every RFC v0.3 slide; titles of at most {TITLE_WORDS} words")
    print(f"PASS: every slide is «{THESES_HEAD}» with {THESES[0]}–{THESES[1]} bullets and «{LOGIC_HEAD}» with why here, a «потому что → поэтому» bridge, the method task, GRA and case 1, format and time")
    print("PASS: slide 1 carries the program title, subtitle and slogan; slide 2 the lecturer's VERIFIED, PARTIAL and «?» with harmony or eclectic; slide 3 the course map with Действую today; slide 4 the three stops and the one-page card")
    print("PASS: mandatory nodes: Г4-1 (9), ●/◐/○ for methods (13), contrasts ◐ and color types ○ (14), the eclectic rule +1, small distance, high mass (19), Промпт-стратег against the Day 2 statuses (21), three different steps of case 1 (23), the card and the return to the vote (24); votes on 6 and 18, prompt trial on 21")
    print("PASS: the card lists point, status, polarity, distance, kind, style, channel, first phrase and what to record; case 1 gives «Д», «С» and the commercial director three different values in every row")
    print("PASS: case 1 is proactive with over 100 wholesale buyers and a network of 25 stores; lawsuits stay an activity marker without forensic reading; «полезность для встречи» is named as an adaptation; rebranding is outside the day; no formula/F(t)/H1, «вред», payment talk, incoming request, trigger, risk, provocation or evaluative adjective")
    print(f"PASS: all sections present, timing totals 90 minutes with 68% image technologies, SSOT links present, gate has {GATE_ITEMS} confirmed items, repository links resolve")
    if args.self_test:
        print(f"PASS: {fixtures} broken fixtures rejected")


if __name__ == "__main__":
    main()
