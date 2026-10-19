#!/usr/bin/env python3
"""Check issue #687: the Day 4 Gamma deck has 26 self-sufficient slides with three fields each, and the lecturer script speaks every slide in 150–180 words with a bridge, Plan Б and the timing of the approved Day 4 rationale."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
GAMMA = DOMAIN / "2026-11-03-day4-presentation-gamma.md"
SCRIPT = DOMAIN / "2026-11-03-day4-lecturer-script.md"
RATIONALE = DOMAIN / "2026-11-03-day4-rationale-and-method.md"
FILES = (GAMMA, SCRIPT)
SOURCE = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/687"
REPO_BLOB = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
SLIDE = re.compile(r"^### Слайд (\d+)\. (.+)$", re.M)
LINK = re.compile(r"\]\(([^)\s]+)\)")
WORD = re.compile(r"[0-9A-Za-zА-Яа-яЁё]+(?:-[0-9A-Za-zА-Яа-яЁё]+)*")
# The NFR stop list of #671, kept by #673, #677, #679, #681 and #685: verbatim quotes (lines starting with «>»), link targets and code blocks of the script are exempt.
TRIGGERS = re.compile(r"безопасн|разоблач|угроз|расследова|ловл[яиюе]", re.I)
DAY_TONE = re.compile(r"риск|вшив", re.I)
FORMULA = re.compile(r"формул(?!ир)|F\(t\)|\bH1\b", re.I)
PROVOCATION = re.compile(r"провок|провоц", re.I)
# #663: no evaluative adjectives about data or people.
EVALUATIVE = re.compile(r"честн|реалистичн|правдив", re.I)
# RFC v0.3, decision 2 on the appeals of v0.2: the program word is read as «полезность для встречи»; on Day 4 it stays off both files.
HARM = re.compile(r"вред", re.I)
STOP_LISTS = (("trigger word", TRIGGERS), ("risk or «вшивость» rhetoric", DAY_TONE), ("GRA formula", FORMULA),
              ("provocation", PROVOCATION), ("evaluative adjective of #663", EVALUATIVE),
              ("program word «вред» instead of «полезность для встречи»", HARM))
# #681 and #685: case 1 is proactive search only — neither an incoming price request nor «прислал» anywhere, quotes, links and code included.
RAW_INCOMING = re.compile(r"запрос[а-я]* цен|прислал", re.I)
PROACTIVE = "сам пишет сетям первым"
# The «Сверьте с юристом» item names the norms of the first contact: people's data and images, trade secrets, advertising and the supply contract.
LAWS = ("152-ФЗ", "152.2 ГК РФ", "98-ФЗ", "38-ФЗ", "381-ФЗ")
# #687: the slide count is fixed by the rationale, and no file may ask to cut or cap the number of slides.
SLIDE_LIMIT = re.compile(r"(?:сократ|урез|ограничь|не больше|не более|максимум)[^.\n]{0,40}слайд", re.I)
# Lawsuits stay one activity marker; payments are never discussed except as a prohibition.
PAYMENT = re.compile(r"оплат|платёж|платеж|плат[ия]т|платил", re.I)
NEGATION = re.compile(r"(?<![а-яё])(?:не|ни|нет|нельзя|без|вне)(?![а-яё])|запрещ", re.I)
ACTIVITY = re.compile(r"(?:иск|судебн)[а-я]*[^.\n]{0,240}маркер[а-я]* активности|маркер[а-я]* активности[^.\n]{0,240}(?:иск|судебн)", re.I)
# Case 1 as #677 fixed it on Day 1: over 100 wholesale buyers, not «100 магазинов»; the network «Х» of RFC v0.3 has 25 stores, not the 40 of #663.
CASE = re.compile(r"более 100 оптовых")
OLD_CASE = re.compile(r"(?<![\d.])100 магазин|(?<![а-яё])сто магазин|(?<![\d.])40 магазин|сорок магазин", re.I)
GAMMA_FIELDS = ("SLIDE_TEXT", "IMAGE_PROMPT", "FOOTER_LINKS")
GAMMA_SLIDES = 26
GAMMA_HEADER = "Введение в репутационный инжиниринг · Имиджевые стратегии для действия"
GAMMA_FOOTER = "· (Telegram) @gulienko @qwen-3.7plus @claudeopus-5.5 · Москва, 10.2026"
# #687: the slides carry no air date, time, format or day counter; only the city and the month stay in the footer.
AIR_TIME = re.compile(r"(?<![\d.])\d{1,2}[.:]\d{2}(?![\d.])|онлайн|День 4 из 4|10–11\.2026|\d{1,2} ноябр|03\.11", re.I)
TITLE_WORDS = 6
# Titles of the approved rationale of #685 that carry the logic of the day: consistency, styles as hypotheses, the style rule,
# −1 polarity, the AI review and the card of first contact.
TITLES = {
    5: "Три точки — три первых шага",
    7: "Вопрос вечера: ради второго шага",
    9: "Согласованность строит доверие",
    13: "Все методики — гипотезы",
    19: "Стратегию выбирают полярность, дистанция, масса",
    20: "При −1 контраст разрушает доверие",
    22: "Где ИИ пообещал лишнее",
    23: "Кейс 1: три разных шага",
    24: "Карточка первого контакта",
    25: "Вижу → Действую: что записать",
}
# Slide 3 repeats the course map of Days 1–3 line by line, with Day 4 marked as today.
COURSE_MAP = ("  - День 1 · Вижу — Репутационный инжиниринг: ключевые составляющие.",
              "  - День 2 · Собираю — Мониторинг ресурсов, работа с данными.",
              "  - День 3 · Выбираю — Внутренние и внешние факторы влияния на развитие компании.",
              "  - День 4 · Действую — Имиджевые стратегии для действия (СЕГОДНЯ).")
STATUSES = ("VERIFIED", "PARTIAL", "«?»")
# Контекст → Цель → Действие on every slide, as in the Day 1 standard of #677.
FRAME = {
    "intro paragraph": re.compile(r"^- Вводный абзац: \S", re.M),
    "«КОНТЕКСТ» card": re.compile(r"^- Карточка: \d\d · КОНТЕКСТ — \S", re.M),
    "«ЦЕЛЬ», «ПРОБЛЕМА», «ВОПРОС» or «ГРАНИЦЫ» card": re.compile(r"^- Карточка: \d\d · (?:ЦЕЛЬ|ПРОБЛЕМА|ВОПРОС|ГРАНИЦЫ) — \S", re.M),
    "«РЕШЕНИЕ» or «ДЕЙСТВИЕ» card": re.compile(r"^- Карточка: \d\d · (?:РЕШЕНИЕ|ДЕЙСТВИЕ) — \S", re.M),
    "conclusion": re.compile(r"^- Вывод: \S", re.M),
}
LABEL = re.compile(r"^(?:- (?:Шапка|Надзаголовок|Заголовок|Подзаголовок|Эпиграф|Вводный абзац|Карточка|Вывод): \S|  - \S)")
CARD_ORDER = re.compile(r"^- Карточка: \d\d · ([А-ЯЁ]+) —", re.M)
CARD_RANK = {"КОНТЕКСТ": 0, "ЦЕЛЬ": 1, "ПРОБЛЕМА": 1, "ВОПРОС": 1, "ГРАНИЦЫ": 1, "РЕШЕНИЕ": 2, "ДЕЙСТВИЕ": 2}
PEOPLE = re.compile(r"(?<!no )\b(?:man|woman|men|women|person|people|couple)\b", re.I)
AGE = re.compile(r"aged (\d\d)–(\d\d)")
VOTE, TRIAL = "🗳", "🤖"
GAMMA_VOTES, GAMMA_TRIALS = {6, 18}, {21}
SCRIPT_MARK = re.compile(r"`\[СЛАЙД (\d+)\]`")
SPEECH_WORDS = (150, 180)
# A speech that shares eight words in a row with the slide texts retells the slide instead of opening it.
NGRAM = 8
SPEECH_MARKS = ("[ПАУЗА]", "[ДЕМОНСТРАЦИЯ ЭКРАНА]", "[ЮМОР/РАЗРЯДКА]")
RESERVE = "\n## 19:53"
# The minute-by-minute timing of the rationale of #685: block А 5, entry 8, stop 1 17,5, stop 2 14, stop 3 30, finale 9, reserve 6,5.
TIMING = ("## 18:30–18:35. Блок А", "*[18:30]* `[СЛАЙД 1]`", "*[18:35]* `[СЛАЙД 5]`", "*[18:43]* `[СЛАЙД 8]`",
          "*[19:00:30]* `[СЛАЙД 13]`", "*[19:14:30]* `[СЛАЙД 17]`", "*[19:28]* `[СЛАЙД 21]`", "*[19:44:30]* `[СЛАЙД 24]`",
          "## 19:53:30–20:00. Резерв", "Резерв — 6,5 минуты, с 19:53:30 до 20:00", "## Тайминг и План Б",
          "| **Итого** | 26 слайдов | 18:30–20:00 | **90** |")
TABLE_ROW = re.compile(r"^\| [^|\n]+ \| (?:\d+–\d+|—) \| [\d:]+–[\d:]+ \| (\d+(?:,\d)?) \|$", re.M)
PLAN_B = ("**План Б: чат молчит.**", "**План Б: эфир начался позже.**", "**План Б: у слушателей нет ИИ под рукой.**")
APPENDIX = ("## Приложение А. Промпт-стратег для слушателей", "### А.1. Как пользоваться", "### А.2. Текст промпта",
            "### А.3. Карточка коммерческого директора сети «Х»", "## Приложение Б. Три карточки кейса 1 и ответ ИИ для разбора",
            "### Б.1. Карточка дистрибьютора «Д»", "### Б.2. Карточка сопоставщика «С»",
            "### Б.3. Карточка коммерческого директора сети «Х»", "### Б.4. Образец ответа ИИ с ошибками для слайда 22",
            "## Приложение В. Короткие ответы на частые вопросы")
# The card of first contact of the rationale: who and what is known, the step, the record after the meeting.
CARD_FIELDS = ("Точка:", "Статус данных:", "Полярность:", "Дистанция:", "Вид шага:", "Стиль:", "Канал:", "Первая фраза:",
               "Полезное для встречи:", "Что записать после:")
# The kind of step follows the status of the data: CONFLICT → conversation, PARTIAL → reversible step, VERIFIED → offer or introduction.
CARD_STEPS = {"Б.1": "CONFLICT → разговор", "Б.2": "VERIFIED → предложение или знакомство", "Б.3": "PARTIAL → обратимый шаг"}
HYPOTHESES = ("Г4-1", "Г4-2", "Г4-3")


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


def code_block(text, heading):
    """The first ```text block after a heading, or None."""
    part = text.split(heading, 1)
    match = re.search(r"```text\n(.*?)```", part[1], re.S) if len(part) == 2 else None
    return match[1] if match else None


def section(text, heading, stop):
    return text.split(heading, 1)[-1].split(stop, 1)[0] if heading in text else ""


def speeches(body):
    """Speech of each slide: from its `[СЛАЙД N]` mark to the next mark, the reserve or the end of the speech part."""
    marks = list(SCRIPT_MARK.finditer(body))
    for i, match in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        yield int(match[1]), body[match.end():end].split(RESERVE, 1)[0]


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
    return errors


def validate_gamma(texts):
    errors, text, name = [], texts[GAMMA], GAMMA.name
    clean = prose(text)
    errors += stop_words(name, text, clean)
    if not ACTIVITY.search(clean):
        errors.append(f"{name}: lawsuits are not described as an activity marker")
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
        if image and (re.search(r"[а-яё]", image, re.I) or not re.search(r"gold|brass", image, re.I)
                      or not re.search(r"malachite", image, re.I) or not re.search(r"monochrome", image, re.I)
                      or "16:9" not in image or "no readable text" not in image.lower()):
            errors.append(f"{name}: slide {n} image prompt is not English, monochrome with a malachite and gold accent, 16:9 and without readable text")
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
            errors.append(f"{name}: slide {n} is not «{title}» (approved rationale of #685)")
    rationale = texts.get(RATIONALE) or ""
    expected = [(int(n), title) for n, title in SLIDE.findall(rationale)]
    if expected and [(n, title) for n, title, _ in deck] != expected:
        errors.append(f"{name}: slide titles differ from the approved rationale of #685")
    chunks = {n: prose(gamma_field(chunk, "SLIDE_TEXT") or "") for n, _, chunk in deck}
    for status in STATUSES:
        if status not in chunks.get(2, ""):
            errors.append(f"{name}: slide 2 does not show the status {status}")
    for line in COURSE_MAP:
        if line not in chunks.get(3, "").splitlines():
            errors.append(f"{name}: slide 3 lost the course map line «{line.strip()[:60]}»")
    votes = {n for n, title, _ in deck if VOTE in title}
    trials = {n for n, title, _ in deck if TRIAL in title}
    if votes != GAMMA_VOTES or trials != GAMMA_TRIALS:
        errors.append(f"{name}: votes {sorted(votes)} and prompt trials {sorted(trials)}, expected {sorted(GAMMA_VOTES)} and {sorted(GAMMA_TRIALS)}")
    return errors


def validate_script(texts):
    errors, text, name = [], texts[SCRIPT], SCRIPT.name
    clean = prose(re.sub(r"```.*?```", "", text, flags=re.S))
    errors += stop_words(name, text, clean)
    if not ACTIVITY.search(clean):
        errors.append(f"{name}: lawsuits are not described as an activity marker")
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
    total = sum(float(minutes.replace(",", ".")) for minutes in TABLE_ROW.findall(text))
    if total != 90:
        errors.append(f"{name}: timing table blocks add up to {total:g} minutes, not 90")
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
    for hypothesis in HYPOTHESES:
        if hypothesis not in body:
            errors.append(f"{name}: hypothesis {hypothesis} is not named in the speech")
    for heading in APPENDIX:
        if not re.search(r"^" + re.escape(heading) + r"$", text, re.M):
            errors.append(f"{name}: appendix heading missing: «{heading}»")
    prompt, approved = code_block(text, "### А.2. Текст промпта"), code_block(texts.get(RATIONALE) or "", "## Промпт-стратег: текст для пробы")
    if not prompt or prompt != approved:
        errors.append(f"{name}: section А.2 is not the Промпт-стратег of the approved rationale word for word")
    for key, step in CARD_STEPS.items():
        card = code_block(text, f"### {key}. ") or ""
        missing = [field for field in CARD_FIELDS if not re.search(r"^" + re.escape(field), card, re.M)]
        if missing:
            errors.append(f"{name}: card {key} misses the fields {', '.join(missing)}")
        if step not in card:
            errors.append(f"{name}: card {key} does not derive the kind of step from the status: «{step}»")
    if "надёжный поставщик федеральных сетей" not in (code_block(text, "### Б.4. ") or ""):
        errors.append(f"{name}: the flawed AI answer of Б.4 lost the over-promise «надёжный поставщик федеральных сетей»")
    key = section(text, "### Б.4. ", "## Приложение В.")
    if not {"1", "2", "3", "4"} <= set(re.findall(r"^\| (\d) \|", key, re.M)):
        errors.append(f"{name}: the key of Б.4 does not list the four errors of slide 22")
    lawyer = re.search(r"^\d+\. Сверьте с юристом.*$", text, re.M)
    missing = [law for law in LAWS if not lawyer or not re.search(r"(?<!\d)" + re.escape(law), lawyer[0])]
    if missing:
        errors.append(f"{name}: the «Сверьте с юристом» item misses {', '.join(missing)}")
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
            errors.append(f"{name}: frontmatter source is not issue #687")
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
    broken = {
        "deck file missing": mutate_re(texts, g, r".*", "", count=1),
        "deck slide removed": mutate_re(texts, g, r"^### Слайд 26\. .*?(?=^## |\Z)", ""),
        "speaker notes back in the deck": mutate(texts, g, "**[IMAGE_PROMPT]**", "**[SPEAKER_NOTES]**\nРечь.\n\n**[IMAGE_PROMPT]**"),
        "fourth field on a slide": mutate(texts, g, "**[IMAGE_PROMPT]**", "**[LAYOUT]**\nДве колонки.\n\n**[IMAGE_PROMPT]**"),
        "deck field missing": mutate(texts, g, "**[FOOTER_LINKS]**", "**Ссылки**"),
        "common header lost": mutate(texts, g, "- Шапка: " + GAMMA_HEADER, "- Шапка: Введение в репутационный инжиниринг"),
        "unlabeled line on a slide": mutate(texts, g, "- Вывод: ", "Без метки.\n- Вывод: "),
        "title longer than six words": mutate_re(texts, g, r"^(### Слайд 10\. |- Заголовок: )Свой, но заметный$", r"\1Свой, но заметный для каждой выбранной точки", count=2),
        "title differs from the rationale": mutate_re(texts, g, r"^(### Слайд 16\. |- Заголовок: )Продуманный гибрид вместо шаблона$", r"\1Гибрид вместо шаблона", count=2),
        "air time in a footer": mutate(texts, g, "· Москва, 10.2026", "· онлайн, 18:30 · Москва, 10.2026"),
        "air date on the cover": mutate(texts, g, "- Надзаголовок: ДЕНЬ 4 · ДЕЙСТВУЮ", "- Надзаголовок: ДЕНЬ 4 · ДЕЙСТВУЮ · 3 ноября"),
        "day counter on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: День 4 из 4. "),
        "Telegram lost in a footer": mutate(texts, g, "(Telegram) @gulienko", "@gulienko"),
        "footer without «Источники:»": mutate_re(texts, g, r"(\*\*\[FOOTER_LINKS\]\*\*\n)Источники: ", r"\1"),
        "relative link": mutate(texts, g, "](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/", "](../"),
        "broken anchor": mutate(texts, g, "#приложение-а-промпт-стратег-для-слушателей", "#приложение-а", count=-1),
        "slide 2 status lost": mutate_re(texts, g, r"(### Слайд 2\.)(.*?)(?=^### Слайд 3\.)", lambda m: m[1] + m[2].replace("PARTIAL", "частично")),
        "slide 3 day theme edited": mutate(texts, g, COURSE_MAP[3], "  - День 4 · Действую — Стратегии."),
        "style rule slide dropped": mutate_re(texts, g, r"^(### Слайд 19\. |- Заголовок: )Стратегию выбирают полярность, дистанция, масса$", r"\1Как выбрать стиль", count=2),
        "«вред» on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: Критерий — возможный вред. "),
        "КОНТЕКСТ card missing": mutate_re(texts, g, r"(### Слайд 15\..*?)· КОНТЕКСТ —", r"\1· ФОН —"),
        "goal card missing": mutate_re(texts, g, r"(### Слайд 20\..*?)· (?:ЦЕЛЬ|ПРОБЛЕМА|ВОПРОС|ГРАНИЦЫ) —", r"\1· ИТОГ —"),
        "action card missing": mutate_re(texts, g, r"(### Слайд 24\..*?)· (?:РЕШЕНИЕ|ДЕЙСТВИЕ) —", r"\1· ИТОГ —"),
        "cards out of order": mutate_re(texts, g, r"(### Слайд 10\..*?- Карточка: 01 · )КОНТЕКСТ(.*?- Карточка: 03 · )(?:РЕШЕНИЕ|ДЕЙСТВИЕ)", r"\1ДЕЙСТВИЕ\2КОНТЕКСТ"),
        "intro paragraph missing": mutate_re(texts, g, r"(### Слайд 25\..*?)- Вводный абзац: [^\n]*\n", r"\1"),
        "conclusion missing": mutate_re(texts, g, r"(### Слайд 3\..*?)- Вывод: [^\n]*\n", r"\1"),
        "third vote": mutate_re(texts, g, r"^(### Слайд 10\. |- Заголовок: )(Свой, но заметный)$", r"\1🗳 \2", count=2),
        "trial removed": mutate_re(texts, g, r"^(### Слайд 21\. |- Заголовок: )🤖 ", r"\1", count=2),
        "«100 магазинов» case": mutate(texts, g, "более 100 оптовых покупателей", "около 100 магазинов", count=-1),
        "40 stores of #663": mutate(texts, g, "- Вывод: ", "- Вывод: Сеть на 40 магазинов. "),
        "incoming request instead of proactive search": mutate(texts, g, PROACTIVE, "отвечает на письма сетей", count=-1),
        "lawsuits beyond an activity marker": mutate_re(texts, g, r"маркер([а-я]*) активности", r"признак\1", count=0),
        "formula on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: Стиль считается по формуле F(t). "),
        "risk word on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: Эклектика — это риск. "),
        "incoming price request": mutate(texts, g, "- Вывод: ", "- Вывод: Сеть «Х» прислала запрос цен. "),
        "payment-discipline conclusion": mutate(texts, g, "- Вывод: ", "- Вывод: Иски показывают, как сеть платит поставщикам. "),
        "appeal to the number of slides": mutate(texts, g, "- Вывод: ", "- Вывод: Сократите колоду до 20 слайдов. "),
        "image prompt in Russian": mutate_re(texts, g, r"(\*\*\[IMAGE_PROMPT\]\*\*[^\n]*\n)", r"\1Иллюстрация. "),
        "image prompt in color": mutate(texts, g, "monochrome", "full color", count=-1),
        "malachite accent lost": mutate_re(texts, g, r"(\*\*\[IMAGE_PROMPT\]\*\*\n)([^\n]*)", lambda m: m[1] + m[2].replace("malachite", "emerald")),
        "person too young": mutate(texts, g, "a man aged 40–50", "a man aged 20–25"),
        "people outside a fashion photo": mutate_re(texts, g, r"(\*\*\[IMAGE_PROMPT\]\*\*[^\n]*\n)(?!Fashion)", r"\1A man at a desk. "),
        "footnote without source": mutate(texts, g, "- Вывод: ", "- Вывод: Цитата ^[9]. "),
        "source not #687": mutate(texts, g, SOURCE, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/685"),
        "script file missing": mutate_re(texts, s, r".*", "", count=1),
        "script slide mark missing": mutate(texts, s, "`[СЛАЙД 3]`", "СЛАЙД 3"),
        "script slide marks out of order": mutate(texts, s, "`[СЛАЙД 21]`", "`[СЛАЙД 22]`"),
        "short speech": mutate_re(texts, s, r"(`\[СЛАЙД 12\]`).*?(?=^### Слайд 13\.)", r"\1\n\nКоротко: потому что идея спорная, поэтому идём дальше.\n\n"),
        "long speech": mutate(texts, s, "`[СЛАЙД 14]`", "`[СЛАЙД 14]`\n\n" + "Цвет помогает выделить одну деталь письма. " * 6),
        "speech without a bridge": mutate_re(texts, s, r"`\[СЛАЙД 14\]`.*?`\[СЛАЙД 15\]`", lambda m: re.sub(r"[Пп]оэтому", "значит", m[0])),
        "speech retells the slide": mutate(texts, s, "Поэтому и в письме, и на странице фактов о федеральных сетях мы молчим.", "Поэтому фразы о федеральных сетях нет ни в письме, ни на странице фактов."),
        "slide 2 speech without statuses": mutate_re(texts, s, r"(`\[СЛАЙД 2\]`.*?)VERIFIED(.*?`\[СЛАЙД 3\]`)", r"\1подтверждено\2", count=0),
        "slide 5 not at 18:35": mutate(texts, s, "*[18:35]* `[СЛАЙД 5]`", "*[18:37]* `[СЛАЙД 5]`"),
        "stop 3 not at 19:14:30": mutate(texts, s, "*[19:14:30]* `[СЛАЙД 17]`", "*[19:16]* `[СЛАЙД 17]`"),
        "reserve not 19:53:30–20:00": mutate(texts, s, "Резерв — 6,5 минуты, с 19:53:30 до 20:00", "Резерв — 10 минут, с 19:50 до 20:00"),
        "timing table not 90 minutes": mutate(texts, s, "| 8–12 | 18:43–19:00:30 | 17,5 |", "| 8–12 | 18:43–19:00:30 | 19,5 |"),
        "timing section lost": mutate(texts, s, "## Тайминг и План Б", "## Тайминг"),
        "silent chat plan lost": mutate(texts, s, "**План Б: чат молчит.**", "**Если тихо.**"),
        "vote moved off slide 18": mutate_re(texts, s, r"(`\[СЛАЙД 18\]`.*?)`\[ГОЛОСОВАНИЕ В ЧАТ\]` ", r"\1"),
        "second trial": mutate(texts, s, "`[СЛАЙД 23]`", "`[СЛАЙД 23]`\n\n`[ПРОБА ПРОМПТА]`"),
        "План Б lost on slide 21": mutate_re(texts, s, r"(`\[СЛАЙД 21\]`.*?)План Б(.*?`\[СЛАЙД 22\]`)", r"\1запасной ход\2", count=0),
        "mark removed": mutate(texts, s, "[ЮМОР/РАЗРЯДКА]", "", count=-1),
        "hypothesis Г4-3 not named": mutate(texts, s, "Г4-3", "гипотеза дня", count=-1),
        "appendix Б.4 lost": mutate(texts, s, "### Б.4. Образец ответа ИИ с ошибками для слайда 22", "### Б.4. Ответ ИИ"),
        "prompt edited": mutate(texts, s, "Открытую эклектику предлагай только при полярности +1", "Открытую эклектику предлагай при полярности +1"),
        "card field lost": mutate_re(texts, s, r"(### Б\.3\..*?)^Дистанция:", r"\1Расстояние:"),
        "card step not from the status": mutate(texts, s, "(CONFLICT → разговор)", "(по вкусу)"),
        "flawed answer without the over-promise": mutate_re(texts, s, r"(### Б\.4\..*?)«Мы — надёжный поставщик федеральных сетей", r"\1«Мы — сильный поставщик"),
        "key row removed": mutate_re(texts, s, r"(### Б\.4\..*?)^\| [2-4] \|[^\n]*\n", r"\1", count=1),
        "«вред» in the script": mutate(texts, s, "\n## Перед эфиром", "\nКритерий программы — возможный вред.\n\n## Перед эфиром"),
        "«100 магазинов» in the speech": mutate(texts, s, "более 100 оптовых покупателей", "сто магазинов", count=-1),
        "evaluative adjective in the speech": mutate(texts, s, "\n## Перед эфиром", "\nКарточка получилась честной.\n\n## Перед эфиром"),
        "lawyer item misses 98-ФЗ": mutate(texts, s, "98-ФЗ о коммерческой тайне", "закон о коммерческой тайне"),
        "risk rhetoric in the speech": mutate(texts, s, "\n## Перед эфиром", "\nКаждое письмо директору — это риск.\n\n## Перед эфиром"),
        "lawsuits not an activity marker in the script": mutate_re(texts, s, r"маркер([а-я]*) активности", r"признак\1", count=0),
        "incoming request in a card": mutate(texts, s, "```text\nКАРТОЧКА ТОЧКИ", "```text\nСеть прислала запрос цен.\nКАРТОЧКА ТОЧКИ"),
        "draft comment in the script": mutate(texts, s, "\n## Перед эфиром", "\n<!-- дописать -->\n\n## Перед эфиром"),
        "source not #687 in the script": mutate(texts, s, SOURCE, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/685", count=-1),
    }
    failed = [name for name, mutated in broken.items() if mutated == texts or not validate(mutated)]
    return failed, len(broken)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="also prove the checker rejects broken fixtures")
    args = parser.parse_args()
    texts = {path: path.read_text(encoding="utf-8") if path.is_file() else "" for path in FILES + (RATIONALE,)}
    errors = validate(texts)
    if args.self_test and not errors:
        failed, fixtures = self_test(texts)
        errors += [f"self-test: mutation not rejected: {name}" for name in failed]
    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        raise SystemExit(1)
    print(f"PASS: deck has {GAMMA_SLIDES} slides with exactly the fields [SLIDE_TEXT], [IMAGE_PROMPT], [FOOTER_LINKS], the common header «{GAMMA_HEADER}» and titles of at most {TITLE_WORDS} words, the same as in the approved rationale of #685")
    print("PASS: every slide line has a label; every slide has an intro paragraph and the cards Контекст → Цель/Проблема → Решение/Действие with a conclusion")
    print("PASS: slide 2 shows VERIFIED, PARTIAL and «?», slide 3 keeps the course map with Day 4 as today; votes on 6 and 18, prompt trial on 21")
    print("PASS: footers are «Источники: …» with full URLs, Telegram and «Москва, 10.2026», no air date, time, format or day counter; image prompts are English, monochrome, 16:9, with a malachite and gold accent and no readable text, people aged 30–50 only in fashion photos")
    print("PASS: case 1 is proactive with over 100 wholesale buyers, lawsuits stay an activity marker; no «вред», formula/F(t)/H1, trigger, risk, provocation, evaluative adjective, price request, payment talk or slide-count appeal")
    print(f"PASS: script marks `[СЛАЙД 1]`…`[СЛАЙД {GAMMA_SLIDES}]` in order, every speech {SPEECH_WORDS[0]}–{SPEECH_WORDS[1]} words with a «потому что → поэтому» bridge and no {NGRAM}-word copy of the slides; 90-minute timing of the rationale, Plan Б on 6, 18 and 21, all three speech marks, Г4-1…Г4-3 named")
    print("PASS: «Сверьте с юристом» names 152-ФЗ, ст. 152.2 ГК РФ, 98-ФЗ, 38-ФЗ and 381-ФЗ; appendix А carries the Промпт-стратег of the rationale word for word and the director card, Б the three cards of first contact with the step derived from the status and the flawed AI answer with its key, В short answers; repository links resolve")
    if args.self_test:
        print(f"PASS: {fixtures} broken fixtures rejected")


if __name__ == "__main__":
    main()
