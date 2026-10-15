#!/usr/bin/env python3
"""Check issue #679: the Day 2 Gamma deck has 28 slides (four new intro slides plus the old slides 1–24 as 5–28) with three fields each, and the lecturer script speaks all 28 slides on the 6 + 84 minute timing."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
GAMMA = DOMAIN / "2026-10-30-day2-presentation-gamma.md"
SCRIPT = DOMAIN / "2026-10-30-day2-lecturer-script.md"
FILES = (GAMMA, SCRIPT)
SOURCE = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/679"
REPO_BLOB = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
SLIDE = re.compile(r"^### Слайд (\d+)\. (.+)$", re.M)
LINK = re.compile(r"\]\(([^)\s]+)\)")
# The NFR stop list of #671, kept by #673, #677 and #679 for the deck and the script: verbatim quotes (lines starting with «>») and link targets are exempt.
TRIGGERS = re.compile(r"безопасн|разоблач|угроз|расследова|ловл[яиюе]", re.I)
DAY_TONE = re.compile(r"риск|вшив", re.I)
FORMULA = re.compile(r"формул(?!ир)|F\(t\)|\bH1\b", re.I)
PROVOCATION = re.compile(r"провок|провоц", re.I)
STOP_LISTS = (("trigger word", TRIGGERS), ("risk or «вшивость» rhetoric", DAY_TONE), ("GRA formula", FORMULA),
              ("provocation", PROVOCATION))
# The case starts with the producer's own first letter: neither an incoming price request nor «прислал» anywhere, quotes and links included.
RAW_INCOMING = re.compile(r"запрос[а-я]* цен|прислал", re.I)
# #679: the founder asked for 28 slides, so neither file may ask to cut or cap the number of slides.
SLIDE_LIMIT = re.compile(r"(?:сократ|урез|ограничь|не больше|не более|максимум)[^.\n]{0,40}слайд", re.I)
# Lawsuits stay one activity marker; payments are never discussed except as a prohibition.
PAYMENT = re.compile(r"оплат|платёж|платеж|плат[ия]т|платил", re.I)
NEGATION = re.compile(r"(?<![а-яё])(?:не|ни|нет|нельзя|без|вне)(?![а-яё])|запрещ", re.I)
ACTIVITY = re.compile(r"(?:иск|судебн)[а-я]*[^.\n]{0,240}маркер[а-я]* активности|маркер[а-я]* активности[^.\n]{0,240}(?:иск|судебн)", re.I)
# Case 1 as #677 fixed it on Day 1: the producer has over 100 wholesale buyers, not «100 магазинов».
CASE = re.compile(r"более 100 оптовых")
OLD_CASE = re.compile(r"(?<![\d.])100 магазин|(?<![а-яё])сто магазин", re.I)
GAMMA_FIELDS = ("SLIDE_TEXT", "IMAGE_PROMPT", "FOOTER_LINKS")
GAMMA_SLIDES = 28
GAMMA_HEADER = "Введение в репутационный инжиниринг · Мониторинг ресурсов, работа с данными"
OLD_HEADER = "День 2: Собираю"
GAMMA_FOOTER = "· (Telegram) @gulienko @qwen-3.7plus @claudeopus-5.5 · Москва, 10.2026"
# #679: the slides carry no air date, time, format or day counter; only the city and the month stay in the footer.
AIR_TIME = re.compile(r"(?<![\d.])\d{1,2}[.:]\d{2}(?![\d.])|онлайн|День 2 из 4|10–11\.2026|\d{1,2} октябр", re.I)
# The two «20:00» the slides need are the goal of the evening, not the air time.
AIR_EXEMPT = {1: "К 20:00 у вас будет", 9: "к 20:00"}
# Slides 1–4 are the founder's text from #679; slide 4 keeps the 🤖 of the trial that the issue text lost.
VERBATIM = {
    1: ("- Надзаголовок: ДЕНЬ 2 · СОБИРАЮ",
        "- Заголовок: Мониторинг ресурсов, работа с данными",
        "- Подзаголовок: Собираю: проверяем основания связей",
        "- Эпиграф: «На чём держится каждая стрелка карты, которую мы нарисовали вчера?»",
        "- Вводный абзац: Второй шаг цепочки. Сегодня мы мирно собираем то, что можно узнать о будущем партнёре по открытым данным, и записываем, на чём держится каждое утверждение. Работа с данными нужна ради подготовки к партнёрству, а не ради отчёта.",
        "- Карточка: 01 · КОНТЕКСТ — Вчера мы увидели карту связей. У половины стрелок пока нет основания.",
        "- Карточка: 02 · ЦЕЛЬ — Научиться проверять провенанс (происхождение) данных и присваивать им статусы.",
        "- Карточка: 03 · ДЕЙСТВИЕ — К 20:00 у вас будет реестр утверждений кейса 1 со статусами и планом первого контакта."),
    2: ("- Надзаголовок: МЕТОД КУРСА, ПРИМЕНЁННЫЙ К ЛЕКТОРУ",
        "- Заголовок: Лектор: проверяем основания утверждений",
        "- Эпиграф: «Сначала метод проверяют на себе, потом — на партнёре»",
        "- Вводный абзац: Вчера мы собрали данные о лекторе по открытым источникам. Сегодня применяем к ним механику Дня 2: оцениваем не громкость регалий, а происхождение и статус каждого утверждения.",
        "- Карточка: 01 · КОНТЕКСТ — Что подтверждают открытые данные",
        "  - ● факт (VERIFIED): экс-генеральный директор АНО ДПО «Высшая школа стилистики, дизайна и технологий» (подтверждено реестром и сайтом школы).",
        "  - ◐ интерпретация (PARTIAL): эксперт по имидж-технологиям, бизнес-аналитик (подтверждено сайтом школы и GitHub, но нет независимых статей).",
        "  - «?» (данных нет): продюсер серии изданий по деловому дресс-коду (названий изданий в открытых данных не найдено).",
        "- Карточка: 02 · ЦЕЛЬ — Три вопроса к связи «слушатель — лектор»",
        "  - Масса ◐ средняя: опыт руководства подтверждён, независимого признания GRA пока нет.",
        "  - Дистанция ● короткая: открытый канал Telegram @gulienko и эфир курса.",
        "  - Полярность «?»: до проверки метода на вашем кейсе.",
        "- Карточка: 03 · ДЕЙСТВИЕ — Границы метода",
        "  - Ничего не вычисляем. Берём только открытые источники. Решение принимает человек, а «?» снимает тот, кто проверил.",
        "- Вывод: Полный журнал поиска и разбор по GRA — по ссылке в подвале."),
    3: ("- Надзаголовок: КАРТА КУРСА",
        "- Заголовок: Четыре дня: Вижу → Собираю → Выбираю → Действую",
        "- Эпиграф: «Сначала увидеть связи, потом собрать данные, выбрать и действовать»",
        "- Вводный абзац: Курс построен как один управленческий цикл на одном сквозном кейсе. Каждый вечер добавляет к карте связей новый слой и опирается на результат предыдущего.",
        "- Карточка: 01 · КОНТЕКСТ — Четыре вечера, 8 часов",
        "  - Темы дней взяты из программы курса на Технограде. Сегодня подсвечен второй шаг.",
        "- Карточка: 02 · ЦЕЛЬ — Реестр с проверенными основаниями",
        "  - К финалу курса у каждого слушателя — не просто карта, а реестр утверждений со статусами и план первого контакта.",
        "- Карточка: 03 · ДЕЙСТВИЕ — Четыре шага",
        "  - День 1 · Вижу — Репутационный инжиниринг: ключевые составляющие.",
        "  - День 2 · Собираю — Мониторинг ресурсов, работа с данными (СЕГОДНЯ).",
        "  - День 3 · Выбираю — Внутренние и внешние факторы влияния на развитие компании.",
        "  - День 4 · Действую — Имиджевые стратегии для действия.",
        "- Вывод: Сегодня учимся собирать данные и проверять их основания, а не просто считать упоминания."),
    4: ("- Надзаголовок: МАРШРУТ ВЕЧЕРА",
        "- Заголовок: Маршрут вечера: от упоминания к основанию",
        "- Эпиграф: «Один кейс, три остановки, один реестр»",
        "- Вводный абзац: Программа дня на Технограде задаёт три блока. Все три блока разбираем на одном учебном кейсе — сети «Х», которую мы выбрали вчера.",
        "- Карточка: 01 · КОНТЕКСТ — Тема дня",
        "  - Мониторинг ресурсов, работа с данными. Данные с проверенным происхождением. Как можно структурировать их по статусам.",
        "- Карточка: 02 · ЦЕЛЬ — Результат вечера",
        "  - Реестр утверждений кейса 1: утверждение, источник, дата, статус (VERIFIED, PARTIAL, CONFLICT) и то, что статус меняет в первом контакте.",
        "- Карточка: 03 · ДЕЙСТВИЕ — Три остановки",
        "  - Остановка 1 · От упоминания к основанию (Провенанс и статусы).",
        "  - Остановка 2 · ИИ как помощник в первичной сортировке (Промпт-разведчик).",
        "  - Остановка 3 · Что считать первым: «почему» или «сколько» (Качественные vs Количественные данные).",
        "- Вывод: Вход в работу — учебный кейс 1 «Умные холодные продажи»: 2 голосования 🗳 и 1 проба промпта 🤖."),
}
STATUSES = ("VERIFIED", "PARTIAL", "«?»")
# Контекст → Цель → Действие on every slide, as in the Day 1 standard of #677.
FRAME = {
    "intro paragraph": re.compile(r"^- Вводный абзац: \S", re.M),
    "«КОНТЕКСТ» card": re.compile(r"^- Карточка: \d\d · КОНТЕКСТ — \S", re.M),
    "«ЦЕЛЬ», «ПРОБЛЕМА», «ВОПРОС» or «ГРАНИЦЫ» card": re.compile(r"^- Карточка: \d\d · (?:ЦЕЛЬ|ПРОБЛЕМА|ВОПРОС|ГРАНИЦЫ) — \S", re.M),
    "«РЕШЕНИЕ» or «ДЕЙСТВИЕ» card": re.compile(r"^- Карточка: \d\d · (?:РЕШЕНИЕ|ДЕЙСТВИЕ) — \S", re.M),
    "conclusion": re.compile(r"^- Вывод: \S", re.M),
}
# Every line of the slide text starts with a label; sub-items of a card are indented.
LABEL = re.compile(r"^(?:- (?:Шапка|Надзаголовок|Заголовок|Подзаголовок|Эпиграф|Вводный абзац|Карточка|Вывод): \S|  - \S)")
CARD_ORDER = re.compile(r"^- Карточка: \d\d · ([А-ЯЁ]+) —", re.M)
CARD_RANK = {"КОНТЕКСТ": 0, "ЦЕЛЬ": 1, "ПРОБЛЕМА": 1, "ВОПРОС": 1, "ГРАНИЦЫ": 1, "РЕШЕНИЕ": 2, "ДЕЙСТВИЕ": 2}
PEOPLE = re.compile(r"(?<!no )\b(?:man|woman|men|women|person|people|couple)\b", re.I)
AGE = re.compile(r"aged (\d\d)–(\d\d)")
VOTE, TRIAL = "🗳", "🤖"
GAMMA_VOTES, GAMMA_TRIALS = {7, 14}, {18}
SCRIPT_MARK = re.compile(r"`\[СЛАЙД (\d+)\]`")
SLIDE2_QUOTE = ("Вчера мы собирали данные обо мне. Сегодня давайте посмотрим на них глазами Дня 2. "
                "Вот что имеет статус VERIFIED, а вот где PARTIAL...")
SPEECH_MARKS = ("[ПАУЗА]", "[ДЕМОНСТРАЦИЯ ЭКРАНА]", "[ЮМОР/РАЗРЯДКА]")
TIMING = ("## 18:30–18:36. Вводный блок", "*[18:30]* `[СЛАЙД 1]`", "*[18:36]* `[СЛАЙД 5]`",
          "## 19:56–20:00. Резерв", "Резерв — 4 минуты, с 19:56 до 20:00", "## Тайминг и План Б", "| **Итого** | 28 слайдов | 18:30–20:00 | **90** |")
PLAN_B = ("**План Б: чат молчит.**", "**План Б: эфир начался позже.**")


def frontmatter(text):
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return dict(line.split(": ", 1) for line in match[1].splitlines() if ": " in line) if match else {}


def plain(text):
    """Text without blockquotes: verbatim quotes of the program and of the founder keep their own words."""
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


def gamma_field(chunk, name):
    match = re.search(r"\*\*\[" + name + r"\]\*\*[^\n]*\n(.*?)(?=\n\*\*\[[A-Z_]+\]\*\*|\Z)", chunk, re.S)
    return match[1].strip() if match else None


def speeches(body):
    """Speech of each slide: from its `[СЛАЙД N]` mark to the next mark or the end of the speech part."""
    marks = list(SCRIPT_MARK.finditer(body))
    for i, match in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        yield int(match[1]), body[match.end():end]


def stop_words(name, text, clean):
    """Stop lists of the deck and the script; clean is the prose without quotes and link targets."""
    errors = []
    for label, pattern in STOP_LISTS:
        for match in sorted(set(pattern.findall(clean)))[:3]:
            errors.append(f"{name}: {label}: «{match}»")
    for match in sorted(set(RAW_INCOMING.findall(text)))[:3]:
        errors.append(f"{name}: incoming price request plot: «{match}»")
    for match in SLIDE_LIMIT.findall(clean)[:1]:
        errors.append(f"{name}: appeal to the number of slides: «{match}»")
    for sentence in re.split(r"(?<=[.!?])\s+|\n", clean):
        if PAYMENT.search(sentence) and not NEGATION.search(sentence):
            errors.append(f"{name}: payments discussed without a prohibition: «{sentence.strip()[:90]}»")
            break
    if OLD_CASE.search(clean):
        errors.append(f"{name}: case 1 still counts «100 магазинов» instead of over 100 wholesale buyers")
    if OLD_HEADER in text:
        errors.append(f"{name}: old header «{OLD_HEADER}» present")
    return errors


def validate_gamma(texts):
    errors, text, name = [], texts[GAMMA], GAMMA.name
    errors += stop_words(name, text, prose(text))
    if "SPEAKER_NOTES" in text:
        errors.append(f"{name}: speaker notes are back in the deck")
    if "## Как читать" not in text:
        errors.append(f"{name}: section «Как читать» missing")
    deck = list(slides(text))
    if [n for n, _, _ in deck] != list(range(1, GAMMA_SLIDES + 1)):
        errors.append(f"{name}: slides are not 1–{GAMMA_SLIDES}: {[n for n, _, _ in deck][:40]}")
    for n, title, chunk in deck:
        values = {key: gamma_field(chunk, key) for key in GAMMA_FIELDS}
        for key, value in values.items():
            if not value:
                errors.append(f"{name}: slide {n} field missing or empty: [{key}]")
        if len(re.findall(r"^\*\*\[[A-Z_]+\]\*\*", chunk, re.M)) != len(GAMMA_FIELDS):
            errors.append(f"{name}: slide {n} does not have exactly the fields {', '.join(GAMMA_FIELDS)}")
        screen, image, footer = (values[key] or "" for key in GAMMA_FIELDS)
        if screen and f"- Шапка: {GAMMA_HEADER}" not in screen:
            errors.append(f"{name}: slide {n} has no common header")
        if screen and f"- Заголовок: {title}" not in screen and f"- Подзаголовок: {title}" not in screen:
            errors.append(f"{name}: slide {n} on-screen title differs from the heading")
        unlabeled = [line for line in screen.splitlines() if line.strip() and not LABEL.match(line)]
        if unlabeled:
            errors.append(f"{name}: slide {n} line has no label: «{unlabeled[0][:60]}»")
        shown = screen.replace(AIR_EXEMPT.get(n, "\0"), "") + "\n" + footer
        for found in sorted(set(AIR_TIME.findall(shown)))[:2]:
            errors.append(f"{name}: slide {n} shows air time, format or day counter: «{found}»")
        for label, pattern in FRAME.items():
            if not pattern.search(screen):
                errors.append(f"{name}: slide {n} has no {label} (Контекст → Цель → Действие)")
        ranks = [CARD_RANK.get(card, -1) for card in CARD_ORDER.findall(screen)]
        if ranks != sorted(ranks) or -1 in ranks:
            errors.append(f"{name}: slide {n} cards are not in the order Контекст → Цель/Проблема → Решение/Действие")
        for line in VERBATIM.get(n, ()):
            if line not in screen.splitlines():
                errors.append(f"{name}: slide {n} lost the founder's text: «{line[:70]}»")
        if image and (re.search(r"[а-яё]", image, re.I) or not re.search(r"gold|amber", image, re.I)
                      or not re.search(r"monochrome", image, re.I)
                      or "16:9" not in image or "no readable text" not in image.lower()):
            errors.append(f"{name}: slide {n} image prompt is not English, monochrome with a gold accent, 16:9 and without readable text")
        if image and PEOPLE.search(image):
            ages = AGE.findall(image)
            if "Fashion" not in image or not ages or any(int(a) < 30 or int(b) > 50 for a, b in ages):
                errors.append(f"{name}: slide {n} shows people outside a fashion photo of people aged 30–50")
        if footer and not (re.search(r"\]\(https://[^)\s]+\)", footer) and footer.endswith(GAMMA_FOOTER)):
            errors.append(f"{name}: slide {n} footer has no full URL or does not end with «{GAMMA_FOOTER}»")
        for mark in sorted(set(re.findall(r"\^\[\d+\]", screen))):
            if mark not in footer:
                errors.append(f"{name}: slide {n} footnote {mark} has no source in [FOOTER_LINKS]")
    chunks = {n: prose(gamma_field(chunk, "SLIDE_TEXT") or "") for n, _, chunk in deck}
    for status in STATUSES:
        if status not in chunks.get(2, ""):
            errors.append(f"{name}: slide 2 does not show the status {status}")
    if not CASE.search(text):
        errors.append(f"{name}: case 1 does not say «более 100 оптовых покупателей»")
    if not ACTIVITY.search(prose(text)):
        errors.append(f"{name}: lawsuits are not described as an activity marker")
    votes = {n for n, title, _ in deck if VOTE in title}
    trials = {n for n, title, _ in deck if TRIAL in title}
    if votes != GAMMA_VOTES or trials != GAMMA_TRIALS:
        errors.append(f"{name}: votes {sorted(votes)} and prompt trials {sorted(trials)}, expected {sorted(GAMMA_VOTES)} and {sorted(GAMMA_TRIALS)}")
    return errors


def validate_script(texts):
    errors, text, name = [], texts[SCRIPT], SCRIPT.name
    clean = prose(re.sub(r"```.*?```", "", text, flags=re.S))
    errors += stop_words(name, text, clean)
    body = text.split("\n## Приложение", 1)[0]
    speech = dict(speeches(body))
    order = [int(n) for n in SCRIPT_MARK.findall(body)]
    if order != list(range(1, GAMMA_SLIDES + 1)):
        errors.append(f"{name}: slide marks are not `[СЛАЙД 1]`…`[СЛАЙД {GAMMA_SLIDES}]` in order: {order[:40]}")
    if SLIDE2_QUOTE not in speech.get(2, ""):
        errors.append(f"{name}: the slide 2 speech does not say «{SLIDE2_QUOTE[:50]}…»")
    for status in ("VERIFIED", "PARTIAL"):
        if status not in speech.get(2, "").replace(SLIDE2_QUOTE, ""):
            errors.append(f"{name}: the slide 2 speech does not name a {status} fact")
    for phrase in TIMING + PLAN_B:
        if phrase not in text:
            errors.append(f"{name}: timing anchor missing: «{phrase}»")
    for mark in SPEECH_MARKS:
        if mark not in body:
            errors.append(f"{name}: mark {mark} missing")
    for mark, expected in (("[ГОЛОСОВАНИЕ В ЧАТ]", GAMMA_VOTES), ("[ПРОБА ПРОМПТА]", GAMMA_TRIALS)):
        found = {n for n, chunk in speech.items() if mark in chunk}
        if found != expected or body.count(f"`{mark}`") != len(expected):
            errors.append(f"{name}: `{mark}` on slides {sorted(found)}, expected once on each of {sorted(expected)}")
    plan_b = {n for n, chunk in speech.items() if "План Б" in chunk}
    if not GAMMA_VOTES | GAMMA_TRIALS <= plan_b:
        errors.append(f"{name}: no «План Б» in the speeches of slides {sorted((GAMMA_VOTES | GAMMA_TRIALS) - plan_b)}")
    if not CASE.search(text):
        errors.append(f"{name}: case 1 does not say «более 100 оптовых покупателей»")
    return errors


def validate(texts):
    missing = [path for path in FILES if not texts[path]]
    errors = [f"{path.name}: file not found" for path in missing]
    if missing:
        return errors
    for path in FILES:
        text, name = texts[path], path.name
        if frontmatter(text).get("source", "").strip('"') != SOURCE:
            errors.append(f"{name}: frontmatter source is not issue #679")
        relative = [url for url in LINK.findall(text) if not re.match(r"https?://", url)]
        if relative:
            errors.append(f"{name}: links are not full URLs: {relative[:3]}")
        errors += [f"{name}: {error}" for error in broken_links(text, texts)]
    errors += validate_gamma(texts)
    errors += validate_script(texts)
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
    g, s = GAMMA, SCRIPT
    speech = r"(## 18:30–18:36.*?)"
    broken = {
        "deck file missing": mutate_re(texts, g, r".*", "", count=1),
        "deck back to 24 slides": mutate_re(texts, g, r"^### Слайд 1\. .*?(?=^### Слайд 5\. )", ""),
        "deck slide removed": mutate_re(texts, g, r"^### Слайд 28\. .*?(?=^## |\Z)", ""),
        "speaker notes back in the deck": mutate(texts, g, "**[IMAGE_PROMPT]**", "**[SPEAKER_NOTES]**\nРечь.\n\n**[IMAGE_PROMPT]**"),
        "fourth field on a slide": mutate(texts, g, "**[IMAGE_PROMPT]**", "**[LAYOUT]**\nДве колонки.\n\n**[IMAGE_PROMPT]**"),
        "deck field missing": mutate(texts, g, "**[FOOTER_LINKS]**", "**Ссылки**"),
        "common header lost": mutate(texts, g, "- Шапка: " + GAMMA_HEADER, "- Шапка: Введение в репутационный инжиниринг"),
        "old «День 2: Собираю» header": mutate(texts, g, "- Шапка: " + GAMMA_HEADER, "- Шапка: Введение в репутационный инжиниринг · День 2: Собираю", count=-1),
        "unlabeled line on a slide": mutate(texts, g, "- Вывод: ", "Без метки.\n- Вывод: "),
        "air time in a footer": mutate(texts, g, "· Москва, 10.2026", "· онлайн, 18:30 · Москва, 10.2026"),
        "air date on the cover": mutate(texts, g, "- Надзаголовок: ДЕНЬ 2 · СОБИРАЮ", "- Надзаголовок: ДЕНЬ 2 · СОБИРАЮ · 30 октября"),
        "day counter on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: День 2 из 4. "),
        "20:00 outside the exempt goal": mutate_re(texts, g, r"(### Слайд 12\..*?- Вывод: )", r"\g<1>До 20:00 успеем. "),
        "Telegram lost in a footer": mutate(texts, g, "(Telegram) @gulienko", "@gulienko"),
        "relative link": mutate(texts, g, "](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/", "](../"),
        "broken anchor": mutate(texts, g, "#а2-текст-промпта", "#промпт", count=-1),
        "slide 1 epigraph edited": mutate(texts, g, "которую мы нарисовали вчера?»", "которую мы видели?»"),
        "slide 2 status line edited": mutate(texts, g, "  - ◐ интерпретация (PARTIAL): эксперт", "  - ◐ интерпретация: эксперт"),
        "slide 2 VERIFIED lost": mutate(texts, g, "● факт (VERIFIED)", "● факт", count=-1),
        "slide 3 day theme edited": mutate(texts, g, "  - День 4 · Действую — Имиджевые стратегии для действия.", "  - День 4 · Действую — Стратегии."),
        "slide 4 stop removed": mutate_re(texts, g, r"^  - Остановка 2 · [^\n]*\n", ""),
        "slide 4 trial emoji lost": mutate(texts, g, "1 проба промпта 🤖.", "1 проба промпта ."),
        "КОНТЕКСТ card missing": mutate_re(texts, g, r"(### Слайд 15\..*?)· КОНТЕКСТ —", r"\1· ФОН —"),
        "goal card missing": mutate_re(texts, g, r"(### Слайд 20\..*?)· (?:ЦЕЛЬ|ПРОБЛЕМА|ВОПРОС|ГРАНИЦЫ) —", r"\1· ИТОГ —"),
        "action card missing": mutate_re(texts, g, r"(### Слайд 26\..*?)· (?:РЕШЕНИЕ|ДЕЙСТВИЕ) —", r"\1· ИТОГ —"),
        "cards out of order": mutate_re(texts, g, r"(### Слайд 10\..*?- Карточка: 01 · )КОНТЕКСТ(.*?- Карточка: 03 · )(?:РЕШЕНИЕ|ДЕЙСТВИЕ)", r"\1ДЕЙСТВИЕ\2КОНТЕКСТ"),
        "intro paragraph missing": mutate_re(texts, g, r"(### Слайд 27\..*?)- Вводный абзац: [^\n]*\n", r"\1"),
        "conclusion missing": mutate_re(texts, g, r"(### Слайд 3\..*?)- Вывод: [^\n]*\n", r"\1"),
        "third vote": mutate_re(texts, g, r"^### Слайд 15\. ", "### Слайд 15. 🗳 "),
        "trial on the old slide 14": mutate_re(texts, g, r"^### Слайд 18\. 🤖 ", "### Слайд 18. "),
        "«100 магазинов» case": mutate(texts, g, "более 100 оптовых покупателей", "около 100 магазинов"),
        "lawsuits beyond an activity marker": mutate_re(texts, g, r"маркер([а-я]*) активности", r"признак\1", count=0),
        "formula on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: Сила связи считается по формуле F(t). "),
        "risk word on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: Новый поставщик — это риск. "),
        "incoming price request": mutate(texts, g, "- Вывод: ", "- Вывод: Сеть «Х» прислала запрос цен. "),
        "payment-discipline conclusion": mutate(texts, g, "- Вывод: ", "- Вывод: Иски показывают, как сеть платит поставщикам. "),
        "appeal to the number of slides": mutate(texts, g, "- Вывод: ", "- Вывод: Сократите колоду до 24 слайдов. "),
        "image prompt in Russian": mutate_re(texts, g, r"(\*\*\[IMAGE_PROMPT\]\*\*[^\n]*\n)", r"\1Иллюстрация. "),
        "image prompt in color": mutate(texts, g, "monochrome", "full color", count=-1),
        "person too young": mutate(texts, g, "a man aged 40–50", "a man aged 20–25"),
        "people outside a fashion photo": mutate_re(texts, g, r"(\*\*\[IMAGE_PROMPT\]\*\*[^\n]*\n)(?!Fashion)", r"\1A man at a desk. "),
        "footnote without source": mutate(texts, g, "- Вывод: ", "- Вывод: Цитата ^[9]. "),
        "source not #679": mutate(texts, g, SOURCE, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/673"),
        "script file missing": mutate_re(texts, s, r".*", "", count=1),
        "script slide mark missing": mutate(texts, s, "`[СЛАЙД 3]`", "СЛАЙД 3"),
        "script slide marks out of order": mutate(texts, s, "`[СЛАЙД 21]`", "`[СЛАЙД 22]`"),
        "script still starts at the old slide 1": mutate_re(texts, s, r"^## 18:30–18:36\..*?(?=^## 18:36–18:47)", ""),
        "slide 2 quote edited": mutate(texts, s, "глазами Дня 2", "глазами второго дня"),
        "slide 2 quote moved to slide 3": mutate_re(texts, s, speech + r"(" + re.escape(SLIDE2_QUOTE) + r")(.*?`\[СЛАЙД 3\]`)", r"\1\3 \2"),
        "slide 5 not at 18:36": mutate(texts, s, "*[18:36]* `[СЛАЙД 5]`", "*[18:30]* `[СЛАЙД 5]`"),
        "reserve not 19:56–20:00": mutate(texts, s, "## 19:56–20:00. Резерв", "## 19:50–20:00. Резерв"),
        "reserve not 4 minutes": mutate(texts, s, "Резерв — 4 минуты", "Резерв — 10 минут"),
        "timing section lost": mutate(texts, s, "## Тайминг и План Б", "## Тайминг"),
        "silent chat plan lost": mutate(texts, s, "**План Б: чат молчит.**", "**Если тихо.**"),
        "vote moved off slide 14": mutate_re(texts, s, r"(`\[СЛАЙД 14\]`.*?)`\[ГОЛОСОВАНИЕ В ЧАТ\]` ", r"\1"),
        "trial on the old slide": mutate_re(texts, s, r"(`\[СЛАЙД 1)8(\]`.*?`\[СЛАЙД 1)9(\]`)", r"\g<1>9\g<2>8\3"),
        "mark removed": mutate(texts, s, "[ЮМОР/РАЗРЯДКА]", "", count=-1),
        "План Б lost on slide 7": mutate_re(texts, s, r"(`\[СЛАЙД 7\]`.*?)План Б(.*?`\[СЛАЙД 8\]`)", r"\1запасной ход\2", count=0),
        "«100 магазинов» in the speech": mutate(texts, s, "более ста оптовых покупателей", "сто магазинов"),
        "risk rhetoric in the speech": mutate(texts, s, "\n## Перед эфиром", "\nКаждый новый партнёр — это риск.\n\n## Перед эфиром"),
        "appeal to slides in the speech": mutate(texts, s, "сведите рассказ на слайдах", "сократите рассказ на слайдах"),
        "source not #679 in the script": mutate(texts, s, SOURCE, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/673", count=-1),
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
    print(f"PASS: deck has {GAMMA_SLIDES} slides with exactly the fields [SLIDE_TEXT], [IMAGE_PROMPT], [FOOTER_LINKS], the common header «{GAMMA_HEADER}» and no «{OLD_HEADER}»")
    print("PASS: slides 1–4 keep the founder's text of #679 line by line; slide 2 shows VERIFIED, PARTIAL and «?»; votes on 7 and 14, prompt trial on 18")
    print("PASS: every slide line has a label; every slide has an intro paragraph and the cards Контекст → Цель/Проблема → Решение/Действие with a conclusion")
    print("PASS: footers carry full URLs, Telegram and «Москва, 10.2026» with no air date, time, format or day counter; image prompts are English, monochrome, 16:9, gold or amber, without readable text, people aged 30–50 only in fashion photos")
    print("PASS: case 1 has over 100 wholesale buyers, lawsuits stay an activity marker; no formula/F(t)/H1, trigger, risk, provocation, price request or slide-count appeal in the deck and the script")
    print(f"PASS: script marks `[СЛАЙД 1]`…`[СЛАЙД {GAMMA_SLIDES}]` in order, the slide 2 quote, the 6-minute intro, slide 5 at 18:36, the 4-minute reserve 19:56–20:00, votes on 7 and 14 and the trial on 18 with План Б, all three speech marks; repository links resolve")
    if args.self_test:
        print(f"PASS: {fixtures} broken fixtures rejected")


if __name__ == "__main__":
    main()
