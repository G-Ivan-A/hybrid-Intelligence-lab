#!/usr/bin/env python3
"""Check issue #691: the Day 4 Variant 3 deck shows exactly four image technologies as a map of hypotheses in the three-field
Gamma format, and the Variant 3 lecturer script speaks every slide in 150–180 words with bridges only between slides."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
GAMMA = DOMAIN / "2026-11-03-day4-presentation-gamma-v3.md"
SCRIPT = DOMAIN / "2026-11-03-day4-lecturer-script-v3.md"
FILES = (GAMMA, SCRIPT)
SOURCE = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/691"
REPO_BLOB = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
# Variant 3 is independent: its repository links lead only to the pair of v3 files and to this checker.
OWN_LINKS = ("research/reputation-technologies/2026-11-03-day4-presentation-gamma-v3.md",
             "research/reputation-technologies/2026-11-03-day4-lecturer-script-v3.md",
             "research/reputation-technologies/exp/day4-v3-691/")
EARLIER = re.compile(r"rationale-and-method|presentation-gamma\.md|lecturer-script\.md|crisis-mitigation|ai-interpretation")
SLIDE = re.compile(r"^### Слайд (\d+)\. (.+)$", re.M)
LINK = re.compile(r"\]\(([^)\s]+)\)")
WORD = re.compile(r"[0-9A-Za-zА-Яа-яЁё]+(?:-[0-9A-Za-zА-Яа-яЁё]+)*")
SENTENCE_END = re.compile(r"[.!?…](?=\s|$)")
# Ban 1 of #691: GRA terms never justify colour, texture or style.
GRA = re.compile(r"(?<![а-яё])масс[аыуеой]|дистанц|полярн|VERIFIED|PARTIAL|CONFLICT|\bGRA\b", re.I)
# Ban 2 of #691: no running case of the course.
CASE = re.compile(r"«[ХДС]»|дистрибьют|производител|консерв|(?<![а-яё])сет(?:ь|и|ей|ям|ями|ях)(?![а-яё])|оптов", re.I)
# Ban 3 of #691: the «потому что → поэтому» bridge lives only in the script, between slides.
BRIDGE = re.compile(r"потому что|поэтому", re.I)
BRIDGE_NAME = "«потому что → поэтому»"
GAMMA_FIELDS = ("SLIDE_TEXT", "IMAGE_PROMPT", "FOOTER_LINKS")
GAMMA_HEADER = "Введение в репутационный инжиниринг · Имиджевые стратегии для действия"
GAMMA_FOOTER = " · (Telegram) @gulienko @qwen-3.7plus @claudeopus-5.5 · Москва, 10.2026"
LABELS = ("Шапка", "Надзаголовок", "Заголовок", "Эпиграф", "Вводный абзац", "Карточка", "Карточка", "Карточка", "Вывод")
CARDS = ("01 · ТЕХНОЛОГИЯ — ", "02 · ВЕКТОР: ГАРМОНИЯ — ", "03 · ВЕКТОР: КОНТРАСТ/ЭКЛЕКТИКА — ")
TITLE_WORDS = 6
TECHNOLOGIES = ("Цвет", "Форма", "Стиль", "Аксессуары")
TECH_TITLE = re.compile(r"^Технология: (.+)$")
# The image rules of #691, word for word.
IMAGE_BASE = ("Luxurious art deco as the base, only a light touch of Bauhaus geometry and Neue Sachlichkeit clarity. "
              "Bright but contrasty light, crisp directional light, deep shadows, white and light-grey surfaces, deep blue and "
              "graphite accents, ONE thin gold or malachite accent. Vertical 9:16 composition. No readable text, no logos, no distortion.")
THEMES = ("architecture", "art", "fashion")
THEMES_RU = {"architecture": "архитектура", "art": "арт", "fashion": "мода"}
PEOPLE = re.compile(r"(?<!no )\b(?:man|woman|men|women|person|people|couple|model)\b", re.I)
AGE = re.compile(r"\b(?:around|about|aged) (\d\d)\b")
# The base rules of #691 are the only source for the Gamma prompt: every value is there, and no colour beyond the five given.
GAMMA_RULES = ("297×210 мм", "12 мм", "Space Grotesk, 28 pt", "IBM Plex Sans, 15 pt", "12 pt", "8 pt", "7 pt", "#FFFFFF",
               "#16181D", "#132A4A", "#E7E9EC", "#B89B5E", "малахит (глубокий зелёный)", "70×168 мм", "архитектура",
               "мода (люди 30–50 лет", "без офисов и стоковых улыбок", "Инфографика — только нативными средствами Gamma")
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")
ALLOWED_HEX = {"#FFFFFF", "#16181D", "#132A4A", "#E7E9EC", "#B89B5E"}
LAYOUT_ROW = re.compile(r"^\| (\d) \| ([^|]+) \| ([^|]+) \| (слева|справа) \| (золото #B89B5E|малахит) \|$", re.M)
# The gate of #691, item by item, ticked.
GATE = ("- [x] Я создал файлы с суффиксом `-v3.md`, полностью независимые от предыдущих вариантов рационале",
        "- [x] Я описал ровно 4 технологии: Цвет, Форма (композиция), Стиль, Аксессуары",
        "- [x] Каждая технология описана строго по структуре: Название → Базовый принцип → Вектор Гармонии → Вектор Контраста/Эклектики",
        "- [x] В описании технологий полностью отсутствуют упоминания GRA и сквозных кейсов",
        "- [x] Структура слайда строго соответствует 3-полевому формату",
        "- [x] Промпты для изображений соответствуют правилам")
GATE_HEADING = "\n## Гейт-проверка\n"
DECISIONS = "\n## Решения исполнителя в пределах постановки\n"
SCRIPT_MARK = re.compile(r"`\[СЛАЙД (\d+)\]`")
SPEECH_WORDS = (150, 180)
SLIDE_SECONDS = 72
SPEECH_MARKS = ("`[ПАУЗА]`", "`[ДЕМОНСТРАЦИЯ ЭКРАНА]`", "`[ПЛАН Б ДЛЯ МОЛЧАЛИВОГО ЧАТА]`")
SPHERES = {"финтех": re.compile(r"финтех", re.I), "luxury": re.compile(r"\bluxury\b", re.I), "deep-tech": re.compile(r"\bdeep-tech\b", re.I)}
SCENARIO, SCENARIO_END = "\n## Сценарий\n", "\n## Источники речи\n"
TOTAL = "| **Итого** | 6 слайдов | 00:00–07:12 | **7,2 мин** |"
# A speech that shares eight words in a row with the slide texts retells the slide instead of opening it.
NGRAM = 8


def frontmatter(text):
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return dict(line.split(": ", 1) for line in match[1].splitlines() if ": " in line) if match else {}


def prose(text):
    """Text without link targets: URLs keep their own words."""
    return re.sub(r"\]\([^)]*\)", "]", text)


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
    """Repository links whose file or anchor is missing, or that leave the pair of v3 files; texts overrides files under test."""
    cache = {}
    for url in sorted(set(LINK.findall(text))):
        if not url.startswith(REPO_BLOB):
            continue
        path, _, anchor = url[len(REPO_BLOB):].partition("#")
        target = ROOT / path
        if not path.startswith(OWN_LINKS):
            yield f"{url}: Variant 3 links outside its own files"
        elif not texts.get(target) and not target.is_file():
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


def section(text, heading, stop="\n## "):
    return text.split(heading, 1)[1].split(stop, 1)[0] if heading in text else ""


def sentences(text):
    return len(SENTENCE_END.findall(text.strip()))


def speeches(body):
    """Speech of each slide: from its `[СЛАЙД N]` mark to the next mark or the end of the scenario."""
    marks = list(SCRIPT_MARK.finditer(body))
    for i, match in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        yield int(match[1]), body[match.end():end]


def spoken(chunk):
    """What the lecturer says aloud: no headings, timing lines, stage directions in italics or bracket marks."""
    text = "\n".join(line for line in chunk.splitlines() if not line.startswith("#") and not line.startswith("*Тайминг"))
    text = re.sub(r"\*\[[^\]]*\]\*", " ", text)
    return re.sub(r"`\[[^\]]+\]`", " ", text)


def grams(text):
    words = [word.lower().replace("ё", "е") for word in WORD.findall(text)]
    return {tuple(words[i:i + NGRAM]) for i in range(len(words) - NGRAM + 1)}


def clock(seconds):
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def validate_slide_text(n, title, text):
    errors = []
    lines = text.splitlines()
    labels = []
    for line in lines:
        match = re.match(r"^- ([А-ЯЁа-яё ]+): \S", line)
        if not match:
            errors.append(f"slide {n}: [SLIDE_TEXT] line without a label: {line[:60]!r}")
            continue
        labels.append(match[1])
    if tuple(labels) != LABELS:
        errors.append(f"slide {n}: labels are {labels}, expected {list(LABELS)}")
    if errors:
        return errors
    value = {label: line.split(": ", 1)[1] for label, line in zip(labels, lines) if label != "Карточка"}
    cards = [line.split(": ", 1)[1] for label, line in zip(labels, lines) if label == "Карточка"]
    if value["Шапка"] != GAMMA_HEADER:
        errors.append(f"slide {n}: header is not «{GAMMA_HEADER}»")
    if value["Надзаголовок"] != value["Надзаголовок"].upper():
        errors.append(f"slide {n}: overline is not in capitals")
    if value["Заголовок"] != title:
        errors.append(f"slide {n}: title «{value['Заголовок']}» differs from the heading «{title}»")
    if len(WORD.findall(title)) > TITLE_WORDS:
        errors.append(f"slide {n}: title longer than {TITLE_WORDS} words")
    if not 1 <= sentences(value["Вводный абзац"]) <= 2:
        errors.append(f"slide {n}: intro paragraph is not 1–2 sentences")
    for card, prefix in zip(cards, CARDS):
        if not card.startswith(prefix):
            errors.append(f"slide {n}: card «{card[:40]}» does not start with «{prefix.strip()}»")
    tech = TECH_TITLE.match(title)
    if tech and cards[0].startswith(CARDS[0]):
        name, _, principle = cards[0][len(CARDS[0]):].partition(". ")
        if name != tech[1]:
            errors.append(f"slide {n}: card 01 does not name the technology «{tech[1]}»")
        if not principle.startswith("Традиционно") or not 1 <= sentences(principle) <= 2:
            errors.append(f"slide {n}: card 01 has no base principle of 1–2 sentences starting with «Традиционно»")
    return errors


def validate_image(n, prompt):
    errors = []
    theme = THEMES[(n - 1) % len(THEMES)]
    if not prompt.startswith(f"Theme: {theme}. "):
        errors.append(f"slide {n}: image prompt does not start with «Theme: {theme}.»")
    if IMAGE_BASE not in prompt:
        errors.append(f"slide {n}: image prompt lacks the base rules of #691 word for word")
    if re.search(r"[А-Яа-яЁё]", prompt):
        errors.append(f"slide {n}: image prompt is not in English")
    subject = prompt.replace(IMAGE_BASE, "")
    accent = "gold" if n % 2 else "malachite"
    other = "malachite" if n % 2 else "gold"
    if accent not in subject or other in subject:
        errors.append(f"slide {n}: image subject has no single {accent} accent")
    if "central part of the frame" not in prompt:
        errors.append(f"slide {n}: image prompt does not keep the subject in the centre for the 70×168 mm block")
    ages = [int(age) for age in AGE.findall(prompt)]
    if theme == "fashion":
        if not ages or any(not 30 <= age <= 50 for age in ages):
            errors.append(f"slide {n}: fashion photo without people aged 30–50")
        if "no office" not in prompt or not re.search(r"no smiles?\b", prompt):
            errors.append(f"slide {n}: fashion photo allows offices or stock smiles")
        if not re.search(r"\bsurreal editorial\b", prompt, re.I) or "unusual" not in prompt:
            errors.append(f"slide {n}: fashion photo is not a surreal editorial from an unusual angle")
    elif PEOPLE.search(prompt) or ages or "No people." not in prompt:
        errors.append(f"slide {n}: people outside a fashion photo")
    return errors


def validate_gamma(texts):
    errors = []
    text = texts[GAMMA]
    found = list(slides(text))
    numbers = [n for n, _, _ in found]
    if numbers != list(range(1, len(found) + 1)) or len(found) < len(TECHNOLOGIES):
        errors.append(f"deck: slides are numbered {numbers}")
    techs = [TECH_TITLE.match(title)[1] for _, title, _ in found if TECH_TITLE.match(title)]
    if tuple(techs) != TECHNOLOGIES:
        errors.append(f"deck: technology slides are {techs}, expected exactly {list(TECHNOLOGIES)}")
    for n, title, chunk in found:
        fields = tuple(re.findall(r"^\*\*\[([A-Z_]+)\]\*\*", chunk, re.M))
        if fields != GAMMA_FIELDS:
            errors.append(f"slide {n}: fields are {list(fields)}, expected {list(GAMMA_FIELDS)}")
            continue
        slide_text, prompt, footer = (gamma_field(chunk, name) for name in GAMMA_FIELDS)
        errors += validate_slide_text(n, title, slide_text)
        errors += validate_image(n, prompt)
        if "\n" in footer or not footer.startswith("Источники: [") or not footer.endswith(GAMMA_FOOTER):
            errors.append(f"slide {n}: footer is not one line «Источники: […](…)…{GAMMA_FOOTER}»")
        if any(not re.match(r"https?://", url) for url in LINK.findall(footer)):
            errors.append(f"slide {n}: footer source without a full URL")
        visible = prose(slide_text + "\n" + footer)
        for name, pattern in (("GRA term", GRA), ("running case", CASE), (f"bridge {BRIDGE_NAME}", BRIDGE)):
            hits = pattern.findall(visible)
            if hits:
                errors.append(f"slide {n}: {name} on the slide: {hits[:3]}")
    # The gate quotes the bans by name; everything else in the deck keeps them out.
    rest = prose(text.replace(section(text, GATE_HEADING), ""))
    for name, pattern in (("GRA term", GRA), ("running case", CASE)):
        hits = pattern.findall(rest)
        if hits:
            errors.append(f"deck: {name} outside the gate: {hits[:3]}")
    prompt = code_block(text, "### Промпт для генерации в Gamma")
    if prompt is None:
        errors.append("deck: Gamma prompt block missing")
    else:
        errors += [f"deck: Gamma prompt lacks «{rule}»" for rule in GAMMA_RULES if rule not in prompt]
        if not re.search(rf"Не меняй количество слайдов", prompt) or f"{len(found)} слайдов" not in prompt:
            errors.append("deck: Gamma prompt does not fix the number of slides")
    invented = sorted(set(HEX.findall(text)) - ALLOWED_HEX)
    if invented:
        errors.append(f"deck: colours outside the base rules of #691: {invented}")
    rows = LAYOUT_ROW.findall(text)
    if [int(row[0]) for row in rows] != numbers:
        errors.append("deck: photo layout table does not list every slide")
    for row, (n, title, _) in zip(rows, found):
        theme = THEMES_RU[THEMES[(n - 1) % len(THEMES)]]
        side, accent = ("слева", "золото #B89B5E") if n % 2 else ("справа", "малахит")
        if (row[1].strip(), row[2].strip(), row[3], row[4]) != (title, theme, side, accent):
            errors.append(f"deck: photo layout row {n} is not «{title} | {theme} | {side} | {accent}»")
    gate = section(text, GATE_HEADING)
    ticked = [line for line in gate.splitlines() if line.startswith("- [")]
    if len(ticked) != len(GATE) or any(not line.startswith(item) for line, item in zip(ticked, GATE)):
        errors.append("deck: gate check is not the six ticked items of #691 in order")
    if DECISIONS not in text:
        errors.append("deck: section on the decisions within the brief is missing")
    return errors


def validate_script(texts):
    errors = []
    text, deck = texts[SCRIPT], texts[GAMMA]
    titles = {n: title for n, title, _ in slides(deck)}
    body = section(text, SCENARIO, SCENARIO_END)
    if not body or SCENARIO_END not in text:
        return ["script: sections «Сценарий» and «Источники речи» missing"]
    if {n: title for n, title, _ in slides(body)} != titles:
        errors.append("script: slide headings differ from the deck")
    found = list(speeches(body))
    if [n for n, _ in found] != list(titles):
        errors.append(f"script: slide marks are {[n for n, _ in found]}, expected {list(titles)}")
    if TOTAL not in text or "## Тайминг и План Б" not in text:
        errors.append(f"script: timing table without «{TOTAL}»")
    slide_grams = set()
    for _, _, chunk in slides(deck):
        slide_grams |= grams(gamma_field(chunk, "SLIDE_TEXT") or "")
    last = max(titles, default=0)
    for n, speech in found:
        start, end = clock((n - 1) * SLIDE_SECONDS), clock(n * SLIDE_SECONDS)
        if f"*[{start}]* `[СЛАЙД {n}]`" not in body or f"*Тайминг: 1,2 мин ({start}–{end})" not in body:
            errors.append(f"script: slide {n} is not timed 1,2 мин from {start} to {end}")
        words = len(WORD.findall(spoken(speech)))
        if not SPEECH_WORDS[0] <= words <= SPEECH_WORDS[1]:
            errors.append(f"script: slide {n} speech has {words} words, expected {SPEECH_WORDS[0]}–{SPEECH_WORDS[1]}")
        for mark in SPEECH_MARKS:
            if speech.count(mark) != 1:
                errors.append(f"script: slide {n} has {speech.count(mark)} marks {mark}, expected one")
        if not re.search(r"`\[ДЕМОНСТРАЦИЯ ЭКРАНА\]` \*\[Откройте [^\]]*из подвала", speech):
            errors.append(f"script: slide {n} demonstration does not open a source from the footer")
        if not re.search(r"`\[ПЛАН Б ДЛЯ МОЛЧАЛИВОГО ЧАТА\]` \*\[[^\]]+\]\*", speech):
            errors.append(f"script: slide {n} Plan Б has no instruction")
        for sphere, pattern in SPHERES.items():
            if not pattern.search(spoken(speech)):
                errors.append(f"script: slide {n} speech has no {sphere} example")
        said = spoken(speech)
        paragraphs = [p.strip() for p in said.split("\n\n") if p.strip()]
        bridges = BRIDGE.findall(speech)
        if n < last:
            ending = paragraphs[-1] if paragraphs else ""
            if [b.lower() for b in bridges] != ["потому что", "поэтому"] or not re.match(r"Потому что [^\n]+, поэтому ", ending):
                errors.append(f"script: slide {n} does not end with exactly one bridge {BRIDGE_NAME} to slide {n + 1}")
        elif bridges:
            errors.append(f"script: slide {n} is the last one, yet has a bridge {BRIDGE_NAME}")
        copied = grams(said) & slide_grams
        if copied:
            errors.append(f"script: slide {n} speech copies the slides: «{' '.join(sorted(copied)[0])}»")
    outside = prose(text.replace(body, "")).replace(BRIDGE_NAME, "")
    if BRIDGE.search(outside):
        errors.append(f"script: {BRIDGE_NAME} outside the speeches")
    for name, pattern in (("GRA term", GRA), ("running case", CASE)):
        hits = pattern.findall(prose(text))
        if hits:
            errors.append(f"script: {name}: {hits[:3]}")
    return errors


def validate(texts):
    missing = [path for path in FILES if not texts[path]]
    errors = [f"{path.name}: file not found" for path in missing]
    if missing:
        return errors
    for path in FILES:
        text, name = texts[path], path.name
        if frontmatter(text).get("source", "").strip('"') != SOURCE:
            errors.append(f"{name}: frontmatter source is not issue #691")
        relative = [url for url in LINK.findall(text) if not re.match(r"https?://", url)]
        if relative:
            errors.append(f"{name}: links are not full URLs: {relative[:3]}")
        if EARLIER.search(text):
            errors.append(f"{name}: names an earlier variant: {EARLIER.findall(text)[:3]}")
        if "<!--" in text:
            errors.append(f"{name}: draft HTML comment")
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
    blob = REPO_BLOB + "research/reputation-technologies/"
    broken = {
        "deck file missing": mutate_re(texts, g, r".*", "", count=1),
        "fifth technology": mutate_re(texts, g, r"^(### Слайд 6\. |- Заголовок: )Выбор вектора — тоже гипотеза$", r"\1Технология: Голос", count=2),
        "technology slide removed": mutate_re(texts, g, r"^### Слайд 5\. .*?(?=^### Слайд 6\.)", ""),
        "technologies out of order": mutate_re(texts, g, r"^(### Слайд 2\. |- Заголовок: )Технология: Цвет$", r"\1Технология: Стиль", count=2),
        "fourth field on a slide": mutate(texts, g, "**[IMAGE_PROMPT]**", "**[SPEAKER_NOTES]**\nРечь.\n\n**[IMAGE_PROMPT]**"),
        "deck field missing": mutate(texts, g, "**[FOOTER_LINKS]**", "**Ссылки**"),
        "common header lost": mutate(texts, g, "- Шапка: " + GAMMA_HEADER, "- Шапка: Введение в репутационный инжиниринг"),
        "unlabeled line on a slide": mutate(texts, g, "- Вывод: ", "Без метки.\n- Вывод: "),
        "indented sub-line in a card": mutate(texts, g, "\n- Карточка: 02", "\n  - подпункт карточки\n- Карточка: 02"),
        "overline not in capitals": mutate(texts, g, "- Надзаголовок: ТЕХНОЛОГИЯ 1 ИЗ 4 · ЦВЕТ", "- Надзаголовок: Технология 1 из 4 · цвет"),
        "title longer than six words": mutate_re(texts, g, r"^(### Слайд 1\. |- Заголовок: )Карта гипотез, а не инструкция$", r"\1Карта гипотез, а вовсе не жёсткая инструкция", count=2),
        "intro paragraph of three sentences": mutate(texts, g, "- Вводный абзац: ", "- Вводный абзац: Раз. Два. ", count=1),
        "harmony card missing": mutate(texts, g, "02 · ВЕКТОР: ГАРМОНИЯ — Палитра", "02 · ВЕКТОР: АДАПТАЦИЯ — Палитра"),
        "cards out of order": mutate_re(texts, g, r"(### Слайд 3\..*?- Карточка: )02 · ВЕКТОР: ГАРМОНИЯ(.*?- Карточка: )03 · ВЕКТОР: КОНТРАСТ/ЭКЛЕКТИКА", r"\g<1>03 · ВЕКТОР: КОНТРАСТ/ЭКЛЕКТИКА\g<2>02 · ВЕКТОР: ГАРМОНИЯ"),
        "base principle not traditional": mutate(texts, g, "01 · ТЕХНОЛОГИЯ — Форма. Традиционно", "01 · ТЕХНОЛОГИЯ — Форма. Мы советуем"),
        "card 01 names another technology": mutate(texts, g, "01 · ТЕХНОЛОГИЯ — Стиль. ", "01 · ТЕХНОЛОГИЯ — Эстетика. "),
        "GRA term on a slide": mutate(texts, g, "- Вывод: Цвет не сообщает", "- Вывод: Полярность решает. Цвет не сообщает"),
        "data status on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: Статус PARTIAL. "),
        "«масса» in the deck": mutate(texts, g, "## Как читать", "Палитру выбирает масса.\n\n## Как читать"),
        "running case on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: Как у сети «Х». "),
        "distributor in the deck": mutate(texts, g, "## Как читать", "Пример дистрибьютора.\n\n## Как читать"),
        "bridge on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: Потому что цвет заметен, поэтому он первый. "),
        "image prompt in Russian": mutate_re(texts, g, r"(\*\*\[IMAGE_PROMPT\]\*\*\nTheme: [a-z]+\. )", r"\1Фото. "),
        "base image rules edited": mutate(texts, g, "Vertical 9:16 composition.", "Horizontal 16:9 composition."),
        "themes not alternating": mutate(texts, g, "Theme: art. An abstract sculpture", "Theme: architecture. An abstract sculpture"),
        "two accents on a photo": mutate(texts, g, "with one thin malachite edge", "with one thin malachite edge and a gold edge"),
        "subject not kept in the centre": mutate(texts, g, " Keep the main subject in the central part of the frame.", "", count=1),
        "person too young": mutate(texts, g, "a woman around 40", "a woman around 22"),
        "stock smile allowed": mutate(texts, g, "no smile, no office", "warm smile"),
        "people outside a fashion photo": mutate(texts, g, "Theme: architecture. Close-up", "Theme: architecture. A woman around 40 near a close-up"),
        "footer without Telegram": mutate(texts, g, "(Telegram) @gulienko", "@gulienko"),
        "footer without «Источники:»": mutate_re(texts, g, r"(\*\*\[FOOTER_LINKS\]\*\*\n)Источники: ", r"\1"),
        "invented malachite hex": mutate(texts, g, "малахит (глубокий зелёный)", "малахит (глубокий зелёный) #0B6E4F"),
        "Gamma prompt lacks a rule": mutate(texts, g, "Space Grotesk, 28 pt", "Space Grotesk"),
        "photo side not alternating": mutate(texts, g, "| 2 | Технология: Цвет | арт | справа |", "| 2 | Технология: Цвет | арт | слева |"),
        "gate item unticked": mutate(texts, g, "- [x] Я описал ровно 4", "- [ ] Я описал ровно 4"),
        "decisions section lost": mutate(texts, g, DECISIONS, "\n## Заметки\n"),
        "link to an earlier rationale": mutate(texts, g, "## Как читать", f"См. [обоснование]({blob}2026-11-03-day4-rationale-and-method-v2.md).\n\n## Как читать"),
        "relative link": mutate(texts, g, "](" + blob, "](../", count=1),
        "broken anchor": mutate(texts, s, "#источники-и-уровень-опоры", "#источники"),
        "source not #691": mutate(texts, g, SOURCE, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/689"),
        "script file missing": mutate_re(texts, s, r".*", "", count=1),
        "script slide mark missing": mutate(texts, s, "`[СЛАЙД 3]`", "СЛАЙД 3"),
        "script heading differs from the deck": mutate(texts, s, "### Слайд 4. Технология: Стиль", "### Слайд 4. Стиль"),
        "slide not at 1,2 minutes": mutate(texts, s, "*[02:24]* `[СЛАЙД 3]`", "*[02:40]* `[СЛАЙД 3]`"),
        "timing total lost": mutate(texts, s, TOTAL, "| **Итого** | 6 слайдов | 00:00–10:00 | **10 мин** |"),
        "short speech": mutate_re(texts, s, r"(`\[СЛАЙД 2\]`\n).*?(?=\n`\[ДЕМОНСТРАЦИЯ ЭКРАНА\]`)", r"\1\nЦвет — гипотеза.\n"),
        "long speech": mutate(texts, s, "`[СЛАЙД 5]`", "`[СЛАЙД 5]`\n\n" + "Деталь в luxury держит образ. " * 6),
        "pause mark missing": mutate_re(texts, s, r"(`\[СЛАЙД 3\]`.*?) `\[ПАУЗА\]`", r"\1"),
        "demonstration mark missing": mutate_re(texts, s, r"(`\[СЛАЙД 4\]`.*?)`\[ДЕМОНСТРАЦИЯ ЭКРАНА\]` ", r"\1"),
        "Plan Б mark missing": mutate_re(texts, s, r"(`\[СЛАЙД 6\]`.*?)`\[ПЛАН Б ДЛЯ МОЛЧАЛИВОГО ЧАТА\]` ", r"\1"),
        "speech without a bridge": mutate_re(texts, s, r"Потому что ([^\n]*), поэтому начинаем с технологии цвета\.", r"Итак: \1, и начинаем с технологии цвета."),
        "second bridge inside a speech": mutate(texts, s, "Значит, перед нами эвристика", "Поэтому перед нами эвристика"),
        "bridge after the last slide": mutate(texts, s, "*[07:12. Конец блока", "Потому что карта собрана, поэтому блок закончен.\n\n*[07:12. Конец блока"),
        "bridge outside the speeches": mutate(texts, s, "\n## Перед эфиром", "\nПоэтому блок короткий.\n\n## Перед эфиром"),
        "speech without a deep-tech example": mutate_re(texts, s, r"(`\[СЛАЙД 3\]`.*?)deep-tech(.*?`\[СЛАЙД 4\]`)", r"\1инженерной\2", count=0),
        "speech retells the slide": mutate(texts, s, "Это исследование полезно своей границей.", "Небольшие изменения костюма подняли оценки по всем качествам, кроме надёжности, и это важно."),
        "running case in the speech": mutate(texts, s, "Представьте три встречи.", "Представьте сеть «Х» и три встречи."),
        "GRA term in the speech": mutate(texts, s, "Теперь два режима.", "Теперь два режима, их выбирает дистанция."),
        "draft comment in the script": mutate(texts, s, "\n## Перед эфиром", "\n<!-- дописать -->\n\n## Перед эфиром"),
        "source not #691 in the script": mutate(texts, s, SOURCE, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/689", count=-1),
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
    slides_count = len(list(slides(texts[GAMMA])))
    print(f"PASS: deck has {slides_count} slides, exactly four of them «Технология: …» in the order {', '.join(TECHNOLOGIES)}; every slide has only the fields [SLIDE_TEXT], [IMAGE_PROMPT], [FOOTER_LINKS]")
    print(f"PASS: every slide line has a label in the order {' → '.join(dict.fromkeys(LABELS))}; header «{GAMMA_HEADER}», overline in capitals, titles of at most {TITLE_WORDS} words, intro of 1–2 sentences")
    print("PASS: cards 01 · ТЕХНОЛОГИЯ → 02 · ВЕКТОР: ГАРМОНИЯ → 03 · ВЕКТОР: КОНТРАСТ/ЭКЛЕКТИКА; card 01 of each technology names it and gives a traditional base principle of 1–2 sentences")
    print(f"PASS: no GRA term and no running case in the deck outside the gate or anywhere in the script; no bridge {BRIDGE_NAME} on the slides")
    print("PASS: image prompts are English, carry the base rules of #691 word for word, alternate architecture → art → fashion and gold → malachite, keep the subject in the centre; people aged 30–50 only in fashion photos, without offices or smiles")
    print("PASS: footers are one line «Источники: …» with full URLs, Telegram and «Москва, 10.2026»; the Gamma prompt carries every base rule and no colour beyond them; photo layout alternates left and right; the six gate items are ticked")
    print(f"PASS: script marks `[СЛАЙД 1]`…`[СЛАЙД {slides_count}]` at 1,2 minutes each, every speech {SPEECH_WORDS[0]}–{SPEECH_WORDS[1]} words with `[ПАУЗА]`, `[ДЕМОНСТРАЦИЯ ЭКРАНА]` of a footer source and `[ПЛАН Б ДЛЯ МОЛЧАЛИВОГО ЧАТА]`, examples from fintech, luxury and deep-tech and no {NGRAM}-word copy of the slides")
    print(f"PASS: one bridge {BRIDGE_NAME} closes each speech 1–{slides_count - 1} and leads to the next slide; none on the last slide or outside the speeches")
    print("PASS: Variant 3 links only to its own files and names no earlier variant; repository links resolve")
    if args.self_test:
        print(f"PASS: {fixtures} broken fixtures rejected")


if __name__ == "__main__":
    main()
