#!/usr/bin/env python3
"""Check issue #681: the Day 3 Gamma deck has 33 self-sufficient slides with three fields each, the lecturer script speaks every slide in 150–180 words with a bridge and Plan Б, and the gate file confirms all ten gate items."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
GAMMA = DOMAIN / "2026-11-02-day3-presentation-gamma.md"
SCRIPT = DOMAIN / "2026-11-02-day3-lecturer-script.md"
GATE = DOMAIN / "2026-11-02-day3-slide-standard-and-gate.md"
FILES = (GAMMA, SCRIPT, GATE)
SOURCE = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/681"
REPO_BLOB = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
SLIDE = re.compile(r"^### Слайд (\d+)\. (.+)$", re.M)
LINK = re.compile(r"\]\(([^)\s]+)\)")
WORD = re.compile(r"[0-9A-Za-zА-Яа-яЁё]+(?:-[0-9A-Za-zА-Яа-яЁё]+)*")
# The NFR stop list of #671, kept by #673, #677, #679 and #681: verbatim quotes (lines starting with «>»), link targets and code blocks of the script are exempt.
TRIGGERS = re.compile(r"безопасн|разоблач|угроз|расследова|ловл[яиюе]", re.I)
DAY_TONE = re.compile(r"риск|вшив", re.I)
FORMULA = re.compile(r"формул(?!ир)|F\(t\)|\bH1\b", re.I)
PROVOCATION = re.compile(r"провок|провоц", re.I)
# #663 (exp/day3-filter-663/check-day3.sh): no evaluative adjectives about data or people.
EVALUATIVE = re.compile(r"честн|реалистичн|правдив", re.I)
STOP_LISTS = (("trigger word", TRIGGERS), ("risk or «вшивость» rhetoric", DAY_TONE), ("GRA formula", FORMULA),
              ("provocation", PROVOCATION), ("evaluative adjective of #663", EVALUATIVE))
# #681: case 1 is proactive search only — neither an incoming price request nor «прислал» anywhere, quotes, links and code included.
RAW_INCOMING = re.compile(r"запрос[а-я]* цен|прислал", re.I)
PROACTIVE = "сам пишет сетям первым"
# #663: the lecturer's «Сверьте с юристом» item covers every law of the «Правовые нормы» line of document 1 (rationale and method).
LAWS = ("381-ФЗ", "38-ФЗ", "98-ФЗ", "152-ФЗ", "259-ФЗ", "323-ФЗ")
# #681: the slide count is not capped, so no file may ask to cut or cap the number of slides.
SLIDE_LIMIT = re.compile(r"(?:сократ|урез|ограничь|не больше|не более|максимум)[^.\n]{0,40}слайд", re.I)
# Lawsuits stay one activity marker; payments are never discussed except as a prohibition.
PAYMENT = re.compile(r"оплат|платёж|платеж|плат[ия]т|платил", re.I)
NEGATION = re.compile(r"(?<![а-яё])(?:не|ни|нет|нельзя|без|вне)(?![а-яё])|запрещ", re.I)
ACTIVITY = re.compile(r"(?:иск|судебн)[а-я]*[^.\n]{0,240}маркер[а-я]* активности|маркер[а-я]* активности[^.\n]{0,240}(?:иск|судебн)", re.I)
# Case 1 as #677 fixed it on Day 1: over 100 wholesale buyers, not «100 магазинов»; the network «Х» of RFC v0.3 has 25 stores, not the 40 of #663.
CASE = re.compile(r"более 100 оптовых")
OLD_CASE = re.compile(r"(?<![\d.])100 магазин|(?<![а-яё])сто магазин|(?<![\d.])40 магазин|сорок магазин", re.I)
# RFC v0.3, decision 2 on the appeals of v0.2: the fourth filter question is «полезность для встречи»; the program word stays off the slides
# and is named in the script only in a paragraph that reads it as «полезность для встречи».
HARM = re.compile(r"вред", re.I)
USEFUL = "полезность для встречи"
GAMMA_FIELDS = ("SLIDE_TEXT", "IMAGE_PROMPT", "FOOTER_LINKS")
GAMMA_SLIDES = 33
GAMMA_HEADER = "Введение в репутационный инжиниринг · Внутренние и внешние факторы влияния"
GAMMA_FOOTER = "· (Telegram) @gulienko @qwen-3.7plus @claudeopus-5.5 · Москва, 10.2026"
# #681: the slides carry no air date, time, format or day counter; only the city and the month stay in the footer.
AIR_TIME = re.compile(r"(?<![\d.])\d{1,2}[.:]\d{2}(?![\d.])|онлайн|День 3 из 4|10–11\.2026|\d{1,2} ноябр|02\.11", re.I)
TITLE_WORDS = 6
# Slides that carry the RFC v0.3 logic #681 names: the bridge from the Day 2 registry, the 20 business cards on two slides,
# point of influence versus audience, the polarity change and the ethics of meeting preparation.
TITLES = {
    6: "Статусы Дня 2 становятся критериями",
    7: "20 визиток: кому первые письма?",
    8: "Сеть «Х»: десять узлов, два-три разговора",
    17: "Четыре вопроса фильтра",
    21: "Точка влияния — не аудитория",
    22: "Смена полярности: сигнал, а не спам",
    25: "20 визиток после фильтра",
    30: "Подготовка к встрече, а не слежка",
}
FILTER = ("1. Доступность", "2. Значимость", "3. Качество", "4. Полезность для встречи")
# Slide 3 repeats the course map of Days 1–2 line by line, with Day 3 marked as today.
COURSE_MAP = ("  - День 1 · Вижу — Репутационный инжиниринг: ключевые составляющие.",
              "  - День 2 · Собираю — Мониторинг ресурсов, работа с данными.",
              "  - День 3 · Выбираю — Внутренние и внешние факторы влияния на развитие компании (СЕГОДНЯ).",
              "  - День 4 · Действую — Имиджевые стратегии для действия.")
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
GAMMA_VOTES, GAMMA_TRIALS = {9, 18}, {23}
SCRIPT_MARK = re.compile(r"`\[СЛАЙД (\d+)\]`")
SPEECH_WORDS = (150, 180)
# A speech that shares eight words in a row with the slide texts retells the slide instead of opening it.
NGRAM = 8
SPEECH_MARKS = ("[ПАУЗА]", "[ДЕМОНСТРАЦИЯ ЭКРАНА]", "[ЮМОР/РАЗРЯДКА]")
TIMING = ("## 18:30–18:37. Вводный блок", "*[18:30]* `[СЛАЙД 1]`", "*[18:37]* `[СЛАЙД 5]`",
          "## 19:50–20:00. Резерв", "Резерв — 10 минут, с 19:50 до 20:00", "## Тайминг и План Б", "| **Итого** | 33 слайда | 18:30–20:00 | **90** |")
# The Plan Б format of the Day 2 script of #679: two named plans in the timing section and one inside each interactive speech.
PLAN_B = ("**План Б: чат молчит.**", "**План Б: эфир начался позже.**", "**План Б: у слушателей нет ИИ под рукой.**")
APPENDIX = ("## Приложение А. Промпт-фильтр для слушателей", "### А.2. Текст промпта", "### А.3. Бриф кейса 1: сеть «Х»",
            "### Б.1. Десять узлов вокруг сети «Х»", "### Б.2. 20 визиток с выставки",
            "### Б.3. Выход ИИ с ошибками: образец для слайда 24", "## Приложение В. Короткие ответы на частые вопросы")
PROMPT_STEPS = ("В1. ДОСТУПНОСТЬ", "В2. ЗНАЧИМОСТЬ", "В3. КАЧЕСТВО", "В4. ПОЛЕЗНОСТЬ ДЛЯ ВСТРЕЧИ")
CARDS = 20
GATE_SECTIONS = ("## 1. ", "## 2. ", "## 3. ", "## 4. ", "## 5. ", "## 6. ", "## 7. Гейт-проверка", "## 8. Как запустить проверку")
GATE_ITEMS = 10


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
    """Speech of each slide: from its `[СЛАЙД N]` mark to the next mark, the reserve or the end of the speech part."""
    marks = list(SCRIPT_MARK.finditer(body))
    for i, match in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        yield int(match[1]), body[match.end():end].split("\n## 19:50", 1)[0]


def spoken(chunk):
    """What the lecturer says aloud: no headings, timing lines, stage directions in italics or bracket marks."""
    text = "\n".join(line for line in chunk.splitlines() if not line.startswith("#") and not line.startswith("*Тайминг"))
    text = re.sub(r"\*\[[^\]]*\]\*", " ", text)
    text = re.sub(r"`\[[^\]]+\]`", " ", text)
    return re.sub(r"^---$", " ", text, flags=re.M)


def grams(text):
    words = [word.lower().replace("ё", "е") for word in WORD.findall(text)]
    return {tuple(words[i:i + NGRAM]) for i in range(len(words) - NGRAM + 1)}


def stop_words(name, text, clean):
    """Stop lists of the deck and the script; clean is the prose without quotes, link targets and code."""
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
        errors.append(f"{name}: case 1 still counts «100 магазинов» or the 40 stores of #663")
    if not CASE.search(text):
        errors.append(f"{name}: case 1 does not say «более 100 оптовых покупателей»")
    if PROACTIVE not in clean:
        errors.append(f"{name}: case 1 does not say the producer «{PROACTIVE}»")
    if not ACTIVITY.search(clean):
        errors.append(f"{name}: lawsuits are not described as an activity marker")
    return errors


def validate_gamma(texts):
    errors, text, name = [], texts[GAMMA], GAMMA.name
    clean = prose(text)
    errors += stop_words(name, text, clean)
    for match in sorted(set(HARM.findall(clean)))[:1]:
        errors.append(f"{name}: the program word «{match}» is on the slides instead of «{USEFUL}»")
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
        if screen and f"- Шапка: {GAMMA_HEADER}" not in screen.splitlines():
            errors.append(f"{name}: slide {n} has no common header")
        if screen and f"- Заголовок: {title}" not in screen.splitlines():
            errors.append(f"{name}: slide {n} on-screen title differs from the heading")
        words = [word for word in title.replace(VOTE, " ").replace(TRIAL, " ").split() if re.search(r"\w", word)]
        if len(words) > TITLE_WORDS:
            errors.append(f"{name}: slide {n} title has {len(words)} words, more than {TITLE_WORDS}")
        unlabeled = [line for line in screen.splitlines() if line.strip() and not LABEL.match(line)]
        if unlabeled:
            errors.append(f"{name}: slide {n} line has no label: «{unlabeled[0][:60]}»")
        for found in sorted(set(AIR_TIME.findall(screen + "\n" + footer)))[:2]:
            errors.append(f"{name}: slide {n} shows air time, date, format or day counter: «{found}»")
        for label, pattern in FRAME.items():
            if not pattern.search(screen):
                errors.append(f"{name}: slide {n} has no {label} (Контекст → Цель → Действие)")
        ranks = [CARD_RANK.get(card, -1) for card in CARD_ORDER.findall(screen)]
        if ranks != sorted(ranks) or -1 in ranks:
            errors.append(f"{name}: slide {n} cards are not in the order Контекст → Цель/Проблема → Решение/Действие")
        if image and (re.search(r"[а-яё]", image, re.I) or not re.search(r"gold|amber|brass", image, re.I)
                      or not re.search(r"monochrome", image, re.I)
                      or "16:9" not in image or "no readable text" not in image.lower()):
            errors.append(f"{name}: slide {n} image prompt is not English, monochrome with a gold accent, 16:9 and without readable text")
        if image and PEOPLE.search(image):
            ages = AGE.findall(image)
            if "Fashion" not in image or not ages or any(int(a) < 30 or int(b) > 50 for a, b in ages):
                errors.append(f"{name}: slide {n} shows people outside a fashion photo of people aged 30–50")
        if footer and not (footer.startswith("Источники: ") and re.search(r"\]\(https://[^)\s]+\)", footer)
                           and footer.endswith(GAMMA_FOOTER)):
            errors.append(f"{name}: slide {n} footer is not «Источники: …» with full URLs ending with «{GAMMA_FOOTER}»")
        for mark in sorted(set(re.findall(r"\^\[\d+\]", screen))):
            if mark not in footer:
                errors.append(f"{name}: slide {n} footnote {mark} has no source in [FOOTER_LINKS]")
    titles = {n: title for n, title, _ in deck}
    for n, title in TITLES.items():
        if titles.get(n, "").replace(f"{VOTE} ", "").replace(f"{TRIAL} ", "") != title:
            errors.append(f"{name}: slide {n} is not «{title}» (RFC v0.3 logic of #681)")
    chunks = {n: prose(gamma_field(chunk, "SLIDE_TEXT") or "") for n, _, chunk in deck}
    for status in STATUSES:
        if status not in chunks.get(2, ""):
            errors.append(f"{name}: slide 2 does not show the status {status}")
    for line in COURSE_MAP:
        if line not in chunks.get(3, "").splitlines():
            errors.append(f"{name}: slide 3 lost the course map line «{line.strip()[:60]}»")
    positions = [chunks.get(17, "").find(question) for question in FILTER]
    if -1 in positions or positions != sorted(positions):
        errors.append(f"{name}: slide 17 does not list the four filter questions in order: {', '.join(FILTER)}")
    votes = {n for n, title, _ in deck if VOTE in title}
    trials = {n for n, title, _ in deck if TRIAL in title}
    if votes != GAMMA_VOTES or trials != GAMMA_TRIALS:
        errors.append(f"{name}: votes {sorted(votes)} and prompt trials {sorted(trials)}, expected {sorted(GAMMA_VOTES)} and {sorted(GAMMA_TRIALS)}")
    return errors


def validate_script(texts):
    errors, text, name = [], texts[SCRIPT], SCRIPT.name
    clean = prose(re.sub(r"```.*?```", "", text, flags=re.S))
    errors += stop_words(name, text, clean)
    for paragraph in clean.splitlines():
        if HARM.search(paragraph) and USEFUL not in paragraph.lower():
            errors.append(f"{name}: the program word «вред» without its reading as «{USEFUL}» in the same paragraph: «{paragraph.strip()[:90]}»")
            break
    body = text.split("\n## Приложение", 1)[0]
    speech = dict(speeches(body))
    order = [int(n) for n in SCRIPT_MARK.findall(body)]
    if order != list(range(1, GAMMA_SLIDES + 1)):
        errors.append(f"{name}: slide marks are not `[СЛАЙД 1]`…`[СЛАЙД {GAMMA_SLIDES}]` in order: {order[:40]}")
    deck = "\n".join(gamma_field(chunk, "SLIDE_TEXT") or "" for _, _, chunk in slides(texts[GAMMA]))
    deck_grams = grams(deck)
    low, high = SPEECH_WORDS
    for n, chunk in sorted(speech.items()):
        words = spoken(chunk)
        count = len(WORD.findall(words))
        if not low <= count <= high:
            errors.append(f"{name}: slide {n} speech has {count} words, not {low}–{high}")
        if "потому что" not in words.lower() or "поэтому" not in words.lower():
            errors.append(f"{name}: slide {n} speech has no «потому что → поэтому» bridge")
        copied = grams(words) & deck_grams
        if copied:
            errors.append(f"{name}: slide {n} speech retells the slide text: «{' '.join(sorted(copied)[0])}»")
    for status in ("VERIFIED", "PARTIAL"):
        if status not in speech.get(2, ""):
            errors.append(f"{name}: the slide 2 speech does not name a {status} fact")
    for phrase in TIMING + PLAN_B:
        if phrase not in text:
            errors.append(f"{name}: timing anchor missing: «{phrase}»")
    table = re.findall(r"^\| [^|\n]+ \| (?:\d+–\d+|—) \| \d\d:\d\d–\d\d:\d\d \| (\d+) \|$", text, re.M)
    if sum(int(minutes) for minutes in table) != 90:
        errors.append(f"{name}: timing table blocks add up to {sum(int(m) for m in table)} minutes, not 90")
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
    for heading in APPENDIX:
        if not re.search(r"^" + re.escape(heading) + r"$", text, re.M):
            errors.append(f"{name}: appendix heading missing: «{heading}»")
    prompt = text.split("### А.2. Текст промпта", 1)[-1].split("### А.3.", 1)[0]
    positions = [prompt.find(step) for step in PROMPT_STEPS]
    if -1 in positions or positions != sorted(positions):
        errors.append(f"{name}: the Промпт-фильтр does not ask the four questions in order: {', '.join(PROMPT_STEPS)}")
    lawyer = re.search(r"^\d+\. Сверьте с юристом.*$", text, re.M)
    missing = [law for law in LAWS if not lawyer or not re.search(r"(?<!\d)" + law, lawyer[0])]
    if missing:
        errors.append(f"{name}: the «Сверьте с юристом» item misses {', '.join(missing)}")
    cards = text.split("### Б.2. 20 визиток с выставки", 1)[-1].split("### Б.3.", 1)[0]
    if len(re.findall(r"^\| \d+ \|", cards, re.M)) != CARDS:
        errors.append(f"{name}: section Б.2 does not list {CARDS} business cards")
    return errors


def validate_gate(texts):
    errors, text, name = [], texts[GATE], GATE.name
    for heading in GATE_SECTIONS:
        if not re.search(r"^" + re.escape(heading), text, re.M):
            errors.append(f"{name}: section «{heading.strip()}» missing")
    gate = text.split("## 7. Гейт-проверка", 1)[-1].split("## 8.", 1)[0]
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
            errors.append(f"{name}: frontmatter source is not issue #681")
        relative = [url for url in LINK.findall(text) if not re.match(r"https?://", url)]
        if relative:
            errors.append(f"{name}: links are not full URLs: {relative[:3]}")
        errors += [f"{name}: {error}" for error in broken_links(text, texts)]
    errors += validate_gamma(texts)
    errors += validate_script(texts)
    errors += validate_gate(texts)
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
    g, s, t = GAMMA, SCRIPT, GATE
    broken = {
        "deck file missing": mutate_re(texts, g, r".*", "", count=1),
        "deck back to 30 slides": mutate_re(texts, g, r"^### Слайд 31\. .*?(?=^## |\Z)", ""),
        "deck slide removed": mutate_re(texts, g, r"^### Слайд 33\. .*?(?=^## |\Z)", ""),
        "speaker notes back in the deck": mutate(texts, g, "**[IMAGE_PROMPT]**", "**[SPEAKER_NOTES]**\nРечь.\n\n**[IMAGE_PROMPT]**"),
        "fourth field on a slide": mutate(texts, g, "**[IMAGE_PROMPT]**", "**[LAYOUT]**\nДве колонки.\n\n**[IMAGE_PROMPT]**"),
        "deck field missing": mutate(texts, g, "**[FOOTER_LINKS]**", "**Ссылки**"),
        "common header lost": mutate(texts, g, "- Шапка: " + GAMMA_HEADER, "- Шапка: Введение в репутационный инжиниринг"),
        "unlabeled line on a slide": mutate(texts, g, "- Вывод: ", "Без метки.\n- Вывод: "),
        "title longer than six words": mutate_re(texts, g, r"^(### Слайд 10\. |- Заголовок: )Вопрос вечера: с кем начать\?$", r"\1Вопрос вечера: с кем же нам начать партнёрство?", count=2),
        "air time in a footer": mutate(texts, g, "· Москва, 10.2026", "· онлайн, 18:30 · Москва, 10.2026"),
        "air date on the cover": mutate(texts, g, "- Надзаголовок: ДЕНЬ 3 · ВЫБИРАЮ", "- Надзаголовок: ДЕНЬ 3 · ВЫБИРАЮ · 2 ноября"),
        "day counter on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: День 3 из 4. "),
        "20:00 on a slide": mutate(texts, g, "К концу вечера у вас будут", "К 20:00 у вас будут"),
        "Telegram lost in a footer": mutate(texts, g, "(Telegram) @gulienko", "@gulienko"),
        "footer without «Источники:»": mutate_re(texts, g, r"(\*\*\[FOOTER_LINKS\]\*\*\n)Источники: ", r"\1"),
        "relative link": mutate(texts, g, "](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/", "](../"),
        "broken anchor": mutate(texts, g, "#день-3-выбираю-фильтруем-узлы-для-действия", "#день-3", count=-1),
        "slide 2 status lost": mutate_re(texts, g, r"(### Слайд 2\.)(.*?)(?=^### Слайд 3\.)", lambda m: m[1] + m[2].replace("PARTIAL", "частично")),
        "slide 3 day theme edited": mutate(texts, g, COURSE_MAP[3], "  - День 4 · Действую — Стратегии."),
        "slide 17 filter out of order": mutate(texts, g, "  - 1. Доступность", "  - 5. Доступность"),
        "polarity slide dropped": mutate_re(texts, g, r"^(### Слайд 22\. |- Заголовок: )Смена полярности: сигнал, а не спам$", r"\1Сигнал вместо спама", count=2),
        "20 business cards slide dropped": mutate_re(texts, g, r"^(### Слайд 25\. |- Заголовок: )20 визиток после фильтра$", r"\1Итог по визиткам", count=2),
        "«вред» back on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: Четвёртый критерий — возможный вред. "),
        "КОНТЕКСТ card missing": mutate_re(texts, g, r"(### Слайд 15\..*?)· КОНТЕКСТ —", r"\1· ФОН —"),
        "goal card missing": mutate_re(texts, g, r"(### Слайд 20\..*?)· (?:ЦЕЛЬ|ПРОБЛЕМА|ВОПРОС|ГРАНИЦЫ) —", r"\1· ИТОГ —"),
        "action card missing": mutate_re(texts, g, r"(### Слайд 26\..*?)· (?:РЕШЕНИЕ|ДЕЙСТВИЕ) —", r"\1· ИТОГ —"),
        "cards out of order": mutate_re(texts, g, r"(### Слайд 10\..*?- Карточка: 01 · )КОНТЕКСТ(.*?- Карточка: 03 · )(?:РЕШЕНИЕ|ДЕЙСТВИЕ)", r"\1ДЕЙСТВИЕ\2КОНТЕКСТ"),
        "intro paragraph missing": mutate_re(texts, g, r"(### Слайд 27\..*?)- Вводный абзац: [^\n]*\n", r"\1"),
        "conclusion missing": mutate_re(texts, g, r"(### Слайд 3\..*?)- Вывод: [^\n]*\n", r"\1"),
        "third vote": mutate_re(texts, g, r"^(### Слайд 15\. |- Заголовок: )(Посредник ценнее громкого узла)$", r"\1🗳 \2", count=2),
        "trial removed": mutate_re(texts, g, r"^(### Слайд 23\. |- Заголовок: )🤖 ", r"\1", count=2),
        "«100 магазинов» case": mutate(texts, g, "более 100 оптовых покупателей", "около 100 магазинов"),
        "40 stores of #663": mutate(texts, g, "- Вывод: ", "- Вывод: Сеть на 40 магазинов. "),
        "incoming request instead of proactive search": mutate(texts, g, PROACTIVE, "отвечает на письма сетей", count=-1),
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
        "source not #681": mutate(texts, g, SOURCE, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/663"),
        "script file missing": mutate_re(texts, s, r".*", "", count=1),
        "script slide mark missing": mutate(texts, s, "`[СЛАЙД 3]`", "СЛАЙД 3"),
        "script slide marks out of order": mutate(texts, s, "`[СЛАЙД 21]`", "`[СЛАЙД 22]`"),
        "short speech": mutate_re(texts, s, r"(`\[СЛАЙД 12\]`).*?(?=^### Слайд 13\.)", r"\1\n\nКоротко: потому что определение широкое, поэтому идём дальше.\n\n"),
        "speech without a bridge": mutate_re(texts, s, r"(`\[СЛАЙД 14\]`.*?)[Пп]оэтому(.*?`\[СЛАЙД 15\]`)", r"\1Значит\2", count=0),
        "speech retells the slide": mutate(texts, s, "`[СЛАЙД 6]`", "`[СЛАЙД 6]` Статус перестаёт быть цветной меткой и становится критерием отсева."),
        "slide 2 speech without statuses": mutate_re(texts, s, r"(`\[СЛАЙД 2\]`.*?)VERIFIED(.*?`\[СЛАЙД 3\]`)", r"\1подтверждено\2", count=0),
        "slide 5 not at 18:37": mutate(texts, s, "*[18:37]* `[СЛАЙД 5]`", "*[18:36]* `[СЛАЙД 5]`"),
        "reserve not 19:50–20:00": mutate(texts, s, "Резерв — 10 минут, с 19:50 до 20:00", "Резерв — 4 минуты, с 19:56 до 20:00"),
        "timing table not 90 minutes": mutate(texts, s, "| 1–4 | 18:30–18:37 | 7 |", "| 1–4 | 18:30–18:37 | 9 |"),
        "timing section lost": mutate(texts, s, "## Тайминг и План Б", "## Тайминг"),
        "silent chat plan lost": mutate(texts, s, "**План Б: чат молчит.**", "**Если тихо.**"),
        "vote moved off slide 18": mutate_re(texts, s, r"(`\[СЛАЙД 18\]`.*?)`\[ГОЛОСОВАНИЕ В ЧАТ\]` ", r"\1"),
        "План Б lost on slide 23": mutate_re(texts, s, r"(`\[СЛАЙД 23\]`.*?)План Б(.*?`\[СЛАЙД 24\]`)", r"\1запасной ход\2", count=0),
        "mark removed": mutate(texts, s, "[ЮМОР/РАЗРЯДКА]", "", count=-1),
        "appendix Б.3 lost": mutate(texts, s, "### Б.3. Выход ИИ с ошибками: образец для слайда 24", "### Б.3. Выход ИИ"),
        "prompt questions out of order": mutate(texts, s, "В1. ДОСТУПНОСТЬ", "В5. ДОСТУПНОСТЬ"),
        "business card removed": mutate_re(texts, s, r"(### Б\.2\..*?)^\| 20 \|[^\n]*\n", r"\1"),
        "«вред» without «полезность»": mutate(texts, s, "\n## Перед эфиром", "\nКритерий программы — возможный вред.\n\n## Перед эфиром"),
        "«100 магазинов» in the speech": mutate(texts, s, "более 100 оптовых покупателей", "сто магазинов", count=-1),
        "evaluative adjective in the speech": mutate(texts, s, "\n## Перед эфиром", "\nРеестр получился честным.\n\n## Перед эфиром"),
        "lawyer item misses 381-ФЗ": mutate(texts, s, "для кейса 1 — 381-ФЗ (ст. 9)", "для кейса 1 — закон о торговле"),
        "risk rhetoric in the speech": mutate(texts, s, "\n## Перед эфиром", "\nКаждый новый партнёр — это риск.\n\n## Перед эфиром"),
        "incoming request in the prompt": mutate(texts, s, "```text\n", "```text\nСеть прислала запрос цен.\n"),
        "source not #681 in the script": mutate(texts, s, SOURCE, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/663", count=-1),
        "gate file missing": mutate_re(texts, t, r".*", "", count=1),
        "gate item open": mutate(texts, t, "- [x] ", "- [ ] "),
        "gate item removed": mutate_re(texts, t, r"^- \[x\] [^\n]*\n", ""),
        "gate section removed": mutate(texts, t, "## 8. Как запустить проверку", "## Запуск"),
        "draft comment in the gate": mutate(texts, t, "## 8. Как запустить проверку", "<!-- дописать -->\n\n## 8. Как запустить проверку"),
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
    print(f"PASS: deck has {GAMMA_SLIDES} slides with exactly the fields [SLIDE_TEXT], [IMAGE_PROMPT], [FOOTER_LINKS], the common header «{GAMMA_HEADER}» and titles of at most {TITLE_WORDS} words")
    print("PASS: every slide line has a label; every slide has an intro paragraph and the cards Контекст → Цель/Проблема → Решение/Действие with a conclusion")
    print("PASS: slide 2 shows VERIFIED, PARTIAL and «?», slide 3 keeps the course map, slide 17 asks the four filter questions in order; votes on 9 and 18, prompt trial on 23")
    print("PASS: RFC v0.3 logic on screen: Day 2 statuses as criteria (6), 20 business cards (7, 25), point of influence versus audience (21), polarity change (22), meeting preparation (30)")
    print("PASS: footers are «Источники: …» with full URLs, Telegram and «Москва, 10.2026», no air date, time, format or day counter; image prompts are English, monochrome, 16:9, with a gold accent and no readable text, people aged 30–50 only in fashion photos")
    print("PASS: case 1 is proactive with over 100 wholesale buyers, lawsuits stay an activity marker, «вред» only as the program word read as «полезность для встречи»; no formula/F(t)/H1, trigger, risk, provocation, evaluative adjective, price request, payment talk or slide-count appeal")
    print(f"PASS: script marks `[СЛАЙД 1]`…`[СЛАЙД {GAMMA_SLIDES}]` in order, every speech {SPEECH_WORDS[0]}–{SPEECH_WORDS[1]} words with a «потому что → поэтому» bridge and no {NGRAM}-word copy of the slides; 90-minute timing, Plan Б on 9, 18 and 23, all three speech marks")
    print(f"PASS: «Сверьте с юристом» names all six laws; appendices А (Промпт-фильтр with В1–В4 in order), Б (ten nodes, {CARDS} business cards, flawed AI output) and В; gate file has sections 1–8 and {GATE_ITEMS} confirmed items; repository links resolve")
    if args.self_test:
        print(f"PASS: {fixtures} broken fixtures rejected")


if __name__ == "__main__":
    main()
