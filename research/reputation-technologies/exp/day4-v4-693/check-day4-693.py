#!/usr/bin/env python3
"""Check issue #693: the Day 4 Variant 4 deck is a map of hypotheses built on the image-technologies research module — four axes
of three technologies each, an interpretation and four analytic markers per axis, three assembly slides on the course cases —
in the three-field Gamma format with haute couture image prompts."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
GAMMA = DOMAIN / "2026-11-03-day4-presentation-gamma-v4.md"
MODULE = DOMAIN / "image-technologies"
MODULE_FILES = tuple(MODULE / name for name in ("00-introduction.md", "10-theory.md", "20-taxonomy.md",
                                                "30-decision-framework.md", "40-practice-and-cases.md", "50-open-research.md"))
INTRO_FILE, OPEN_FILE = MODULE_FILES[0], MODULE_FILES[5]
FILES = (GAMMA,) + MODULE_FILES
SOURCE = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/693"
REPO_BLOB = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
DECK_PATH = "research/reputation-technologies/2026-11-03-day4-presentation-gamma-v4.md"
# The deck cites the module files it is built on: cards from the taxonomy, vectors and markers from the decision framework,
# assembly from the practice file.
DECK_BASIS = ("image-technologies/00-introduction.md", "image-technologies/20-taxonomy.md",
              "image-technologies/30-decision-framework.md", "image-technologies/40-practice-and-cases.md")
SLIDE = re.compile(r"^### Слайд (\d+)\. (.+)$", re.M)
LINK = re.compile(r"\]\(([^)\s]+)\)")
WORD = re.compile(r"[0-9A-Za-zА-Яа-яЁё]+(?:-[0-9A-Za-zА-Яа-яЁё]+)*")
# A dot after a single capital is an initial («Н. Туркенич»), not the end of a sentence.
SENTENCE_END = re.compile(r"(?<!\b[А-ЯЁA-Z])[.!?…](?=\s|$)")
# Ban 1 of #693: the data-collection model of the course and its terms never describe image technologies.
GRA = re.compile(r"(?<![а-яё])масс(?:а|ы|у|е|ой|ам|ами|ах)?(?![а-яё])|дистанц|полярн|VERIFIED|PARTIAL|CONFLICT|\bGRA\b", re.I)
# Ban 2 of #693: the running cases of the course appear only on the three assembly slides.
CASE = re.compile(r"«[ХДС]»|дистрибьют|производител|консерв|(?<![а-яё])сет(?:ь|и|ей|ям|ями|ях)(?![а-яё])|оптов", re.I)
GAMMA_FIELDS = ("SLIDE_TEXT", "IMAGE_PROMPT", "FOOTER_LINKS")
GAMMA_HEADER = "Введение в репутационный инжиниринг · Имиджевые стратегии для действия"
GAMMA_FOOTER = " · (Telegram) @gulienko @qwen-3.7plus @claudeopus-5.5 · Москва, 10.2026"
TITLE_WORDS = 6
SLIDES = 27
CARD = re.compile(r"^(\d\d) · ([^a-zа-яё—]+?) — \S")
# Axis: overline name, genitive in «на оси …», technology slides, interpretation slide, markers slide.
AXES = (("ЦВЕТ", "цвета", (4, 5, 6), 7, 8),
        ("ФОРМА", "формы", (9, 10, 11), 12, 13),
        ("СТИЛЬ", "стиля", (14, 15, 17), 18, 19),
        ("АКСЕССУАРЫ", "аксессуаров", (20, 21, 22), 23, 24))
STYLES_SLIDE = 16
INTRO_SLIDES, LEGEND_SLIDE, ASSEMBLY = (1, 2), 3, (25, 26, 27)
TECH_CARDS = ("ДЛЯ ЧЕГО", "ИСПОЛЬЗУЮТ", "В ЧЁМ СУТЬ")
VECTOR_WORDS = re.compile(r"вектор|гармони|эклектик", re.I)
INTERPRETATION_CARDS = ("ГАРМОНИЯ/КЛАССИЦИЗМ", "КОНТРАСТ/ЭКЛЕКТИКА")
SYNTHESIS = ("ОБОБЩЕНИЕ", "КОНКУРИРУЮЩИЕ ПОДХОДЫ")
MARKER_CARDS = ("СВОИ ОСОБЕННОСТИ", "КОНТЕКСТ: СУБЪЕКТЫ, ОБЪЕКТЫ, МОТИВАЦИИ", "ИНФОПОЛЕ КОММУНИКАЦИИ", "МОДА СЕЗОНА")
ASSEMBLY_CARDS = ("ЦВЕТ", "ФОРМА", "СТИЛЬ", "АКСЕССУАРЫ")
# Each of the six styles names its lines (straight, curved, angular) and scale, and an art association.
STYLE_LINES = re.compile(r"лини|прям|изгиб|угл|масштаб", re.I)
STYLES = ("ДРАМА", "КЛАССИКА", "НАТУРАЛЬНЫЙ", "РОМАНТИЗМ", "НАИВНАЯ РОМАНТИКА", "СПОРТ")
# The facets of the image named by #693 for the introduction.
FACETS = ("причёска", "походка", "речь", "почерк", "мимика", "синтаксис", "стиль жизни")
# Technologies #693 makes mandatory, found in the overline of a technology slide of their axis.
MANDATORY = {"ЦВЕТ": ("Й. ИТТЕН", "ВАТТЕРМАН", "ЦИНГЕЛЬ"),
             "ФОРМА": ("БЕЛЯЕВА-ЭКЗЕМПЛЯРСКАЯ", "«ГИД ПО СТИЛЮ»"),
             "СТИЛЬ": ("ВШСДТ",),
             "АКСЕССУАРЫ": ("ВШСДТ",)}
LEVEL = re.compile(r"Опора [ЭКПА]\b")
# Image rules of #693.
BASE_HEX = {"#16181D": "graphite", "#132A4A": "deep blue", "#0A4D3C": "emerald", "#720E1E": "ruby"}
GOLD = "#B89B5E"
IMAGE_TAIL = re.compile(r" Haute couture 2026–2027, inspired by New York and Beijing, strictly subordinate to a luxurious art deco base "
                        r"with a light touch of Bauhaus and Neue Sachlichkeit\. Palette strictly limited to (.+?) with ONE gold accent "
                        r"#B89B5E\. Vertical 1:2\.4 composition, main subject in the central part of the frame\. No text, no letters, "
                        r"no logos, no office scenes, no stock smiles\.$")
COLOR_WORDS = re.compile(r"\b(?:white|black|red|pink|orange|yellow|purple|violet|beige|brown|silver|turquoise|pastel|neon|cream|ivory|grey|gray)\b", re.I)
HEX = re.compile(r"#[0-9A-Fa-f]{6}\b")
ALLOWED_HEX = {"#FFFFFF", "#E7E9EC", GOLD} | set(BASE_HEX)
GAMMA_RULES = ("297×210 мм", "12 мм", "Space Grotesk, 28 pt", "IBM Plex Sans, 15 pt", "12 pt", "8 pt", "7 pt", "#FFFFFF",
               "#16181D", "#132A4A", "#E7E9EC", "золото #B89B5E", "изумруд #0A4D3C", "рубина #720E1E", "70×168 мм", "1:2.4",
               "Haute Couture", "2026–2027", "Нью-Йорком и Пекином", "ар-деко", "Баухауз", "Neue Sachlichkeit",
               "один золотой акцент #B89B5E", "30–50 лет", "без офисных сцен и стоковых улыбок", "три — в один ряд",
               "четыре — сеткой 2×2", "шесть — сеткой 3×2", "Инфографика — только нативными средствами Gamma")
LAYOUT_ROW = re.compile(r"^\| (\d+) \| ([^|]+) \| ([^|]+) \| (слева|справа) \| (золото #B89B5E|изумруд #0A4D3C) \|$", re.M)
# The gate of #693, item by item, ticked.
GATE = ("- [x] Исследование по контракту RRP создано в отдельном модуле",
        "- [x] На каждой из четырёх осей — три технологии; обязательные включены",
        "- [x] Тезис «цвет не сообщает характер, а является гипотезой о первом впечатлении» проверен",
        "- [x] Введение — слайды 1–2, легенда карты — слайд 3",
        "- [x] Каждая технология описана как «Ось — метод — автор», «Для чего», «Используют», «В чём суть»; векторов на карточке технологии нет",
        "- [x] На каждую ось — слайд интерпретации через гармонию и контраст и слайд из четырёх аналитических маркеров",
        "- [x] Сборка — слайды 25–27 на трёх кейсах курса; на других слайдах кейсов нет",
        "- [x] Модель сбора данных курса и её термины к имидж-технологиям не применяются",
        "- [x] Каждый слайд — ровно три поля",
        "- [x] Промпты изображений: только высокая мода 2026–2027")
GATE_HEADING = "\n## Гейт-проверка\n"
DECISIONS = "\n## Решения исполнителя в пределах постановки\n"
# The deviation rule of #693, word for word.
DEVIATION = re.compile(r"Я предлагаю скорректировать \[[^\]]+\], потому что вариант \[[^\]]+\] эффективнее решает задачу \[[^\]]+\]")
DEVIATIONS = 4


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
    """Repository links whose file or anchor is missing; texts overrides files under test."""
    cache = {}
    for url in sorted(set(LINK.findall(text))):
        if not url.startswith(REPO_BLOB):
            continue
        path, _, anchor = url[len(REPO_BLOB):].partition("#")
        target = ROOT / path
        if not texts.get(target) and not target.exists():
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


def kind(n):
    """Role of slide n in the deck and, for an axis slide, the axis."""
    if n in INTRO_SLIDES:
        return "intro", None
    if n == LEGEND_SLIDE:
        return "legend", None
    if n in ASSEMBLY:
        return "assembly", None
    if n == STYLES_SLIDE:
        return "styles", AXES[2]
    for axis in AXES:
        if n in axis[2]:
            return "technology", axis
        if n == axis[3]:
            return "interpretation", axis
        if n == axis[4]:
            return "markers", axis
    return None, None


def parse_slide_text(n, text):
    """Labelled values of [SLIDE_TEXT] and the list of cards, or errors."""
    errors, labels, values, cards = [], [], {}, []
    for line in text.splitlines():
        match = re.match(r"^- ([А-ЯЁа-яё ]+): (\S.*)$", line)
        if not match:
            errors.append(f"slide {n}: [SLIDE_TEXT] line without a label: {line[:60]!r}")
            continue
        labels.append(match[1])
        if match[1] == "Карточка":
            cards.append(match[2])
        else:
            values[match[1]] = match[2]
    order = [label for i, label in enumerate(labels) if label != "Карточка" or labels[i - 1] != "Карточка"]
    if order != ["Шапка", "Надзаголовок", "Заголовок", "Эпиграф", "Вводный абзац", "Карточка", "Вывод"]:
        errors.append(f"slide {n}: labels are {labels}, expected Шапка → Надзаголовок → Заголовок → Эпиграф → Вводный абзац → Карточка… → Вывод")
    return errors, values, cards


def expect_cards(n, cards, names):
    """Cards numbered 01… with the given captions, in order; a caption may be a tuple of alternatives."""
    got = [CARD.match(card) for card in cards]
    if len(cards) != len(names):
        return [f"slide {n}: {len(cards)} cards, expected {len(names)}"]
    errors = []
    for i, (match, name) in enumerate(zip(got, names), 1):
        allowed = name if isinstance(name, tuple) else (name,)
        if not match or match[1] != f"{i:02d}" or match[2] not in allowed:
            errors.append(f"slide {n}: card {i:02d} is «{cards[i - 1][:50]}», expected «{i:02d} · {' | '.join(allowed)} — …»")
    return errors


def validate_slide_text(n, title, text):
    errors, value, cards = parse_slide_text(n, text)
    if errors:
        return errors
    role, axis = kind(n)
    overline, intro, conclusion = value["Надзаголовок"], value["Вводный абзац"], value["Вывод"]
    if value["Шапка"] != GAMMA_HEADER:
        errors.append(f"slide {n}: header is not «{GAMMA_HEADER}»")
    if overline != overline.upper():
        errors.append(f"slide {n}: overline is not in capitals")
    if value["Заголовок"] != title:
        errors.append(f"slide {n}: title «{value['Заголовок']}» differs from the heading «{title}»")
    if len(WORD.findall(title)) > TITLE_WORDS:
        errors.append(f"slide {n}: title longer than {TITLE_WORDS} words")
    if not re.match(r"^«.+». — \S", value["Эпиграф"]):
        errors.append(f"slide {n}: epigraph is not «quote». — author")
    if not 1 <= sentences(intro) <= 2:
        errors.append(f"slide {n}: intro paragraph is not 1–2 sentences")
    for card in cards:
        if not CARD.match(card):
            errors.append(f"slide {n}: card «{card[:40]}» is not «NN · CAPTION — text»")
    if role == "intro" and n == 1:
        missing = [facet for facet in FACETS if facet not in intro.lower()]
        if missing:
            errors.append(f"slide {n}: introduction does not name the facets of the image {missing}")
    elif role == "intro":
        errors += expect_cards(n, cards, ("ОПОРА Э: ЭКСПЕРИМЕНТ", "ОПОРА К: КНИГА ИЛИ ПРОГРАММА", "ОПОРА П: ПРАКТИКА", "ОПОРА А: АНАЛОГИЯ"))
    elif role == "legend":
        if "может собираться по четырём осям" not in intro or "гипотеза" not in intro:
            errors.append(f"slide {n}: legend does not say the image may be built on four axes and the vector is a hypothesis")
        errors += expect_cards(n, cards, tuple(a[0] for a in AXES) + ("ВЕКТОР: ГАРМОНИЯ/КЛАССИЦИЗМ", "ВЕКТОР: КОНТРАСТ/ЭКЛЕКТИКА"))
    elif role == "technology":
        name, genitive, techs = axis[0], axis[1], axis[2]
        if not re.match(rf"^{name} — [^—]+ — [^—]+$", overline):
            errors.append(f"slide {n}: overline is not «{name} — МЕТОД — АВТОР»")
        if not intro.startswith(f"Технология {techs.index(n) + 1} из {len(techs)} на оси {genitive}"):
            errors.append(f"slide {n}: intro does not start with «Технология {techs.index(n) + 1} из {len(techs)} на оси {genitive}»")
        errors += expect_cards(n, cards, TECH_CARDS)
        if VECTOR_WORDS.search(text):
            errors.append(f"slide {n}: technology card carries a vector: {VECTOR_WORDS.findall(text)[:3]}")
        if not LEVEL.search(conclusion):
            errors.append(f"slide {n}: conclusion does not name the support level «Опора Э/К/П/А»")
    elif role == "styles":
        if not overline.startswith("СТИЛЬ — ") or "ВШСДТ" not in overline or "«ГИД ПО СТИЛЮ»" not in overline:
            errors.append(f"slide {n}: overline of the six styles does not name ВШСДТ and «Гид по стилю»")
        errors += expect_cards(n, cards, STYLES)
        errors += [f"slide {n}: style card without lines or an art association: «{card[:30]}»" for card in cards
                   if not re.search(r"ассоциация[^—]* — \S", card) or not STYLE_LINES.search(card)]
        if not re.search(r"Опора П\b.*\bА\b", conclusion):
            errors.append(f"slide {n}: conclusion does not mark the art parallels as an analogy (А)")
    elif role == "interpretation":
        if overline != f"{axis[0]} · ИНТЕРПРЕТАЦИЯ":
            errors.append(f"slide {n}: overline is not «{axis[0]} · ИНТЕРПРЕТАЦИЯ»")
        errors += expect_cards(n, cards, INTERPRETATION_CARDS + (SYNTHESIS,))
    elif role == "markers":
        if overline != f"{axis[0]} · УПРАВЛЕНЧЕСКИЕ ВЫВОДЫ":
            errors.append(f"slide {n}: overline is not «{axis[0]} · УПРАВЛЕНЧЕСКИЕ ВЫВОДЫ»")
        errors += expect_cards(n, cards, MARKER_CARDS)
        if n == AXES[0][4] and "цвет не сообщает характер" not in intro:
            errors.append(f"slide {n}: the checked colour thesis is missing from the intro")
    elif role == "assembly":
        i = ASSEMBLY.index(n) + 1
        if overline != f"СБОРКА · СЦЕНАРИЙ {i} ИЗ {len(ASSEMBLY)} · КЕЙС КУРСА":
            errors.append(f"slide {n}: overline is not «СБОРКА · СЦЕНАРИЙ {i} ИЗ {len(ASSEMBLY)} · КЕЙС КУРСА»")
        errors += expect_cards(n, cards, ASSEMBLY_CARDS)
        errors += [f"slide {n}: assembly card without a hypothesis: «{card[:30]}»" for card in cards if "гипотеза — " not in card]
        if not conclusion.startswith("Вектор — ") or "Проверка — " not in conclusion:
            errors.append(f"slide {n}: conclusion does not give «Вектор — …» and «Проверка — …»")
    else:
        errors.append(f"slide {n}: no role in the deck")
    return errors


def validate_image(n, prompt):
    errors = []
    if re.search(r"[А-Яа-яЁё]", prompt):
        errors.append(f"slide {n}: image prompt is not in English")
    tail = IMAGE_TAIL.search(prompt)
    if not tail:
        return errors + [f"slide {n}: image prompt does not end with the image rules of #693 word for word"]
    concept, palette = prompt[:tail.start()], tail[1]
    colours = HEX.findall(palette)
    expected = " and ".join(f"{BASE_HEX.get(h, '?')} {h}" for h in colours) if len(colours) == 2 else \
        f"{BASE_HEX.get(colours[0], '?')} {colours[0]}, " + " and ".join(f"{BASE_HEX.get(h, '?')} {h}" for h in colours[1:]) \
        if len(colours) == 3 else None
    if expected is None or palette != expected or len(set(colours)) != len(colours) or not set(colours) <= set(BASE_HEX):
        errors.append(f"slide {n}: palette «{palette}» is not 2–3 named base colours of #693")
    if prompt.count(GOLD) != 1 or HEX.findall(concept):
        errors.append(f"slide {n}: image prompt has a colour code outside the palette or more than one gold accent")
    if "the single gold accent" not in concept:
        errors.append(f"slide {n}: image concept does not name its single gold accent")
    if COLOR_WORDS.search(concept):
        errors.append(f"slide {n}: image concept names a colour outside the palette: {COLOR_WORDS.findall(concept)[:3]}")
    ages = [int(age) for age in re.findall(r"\b(\d\d)\b", concept)]
    if "aged" not in concept or not ages or any(not 30 <= age <= 50 for age in ages):
        errors.append(f"slide {n}: image without people aged 30–50")
    if not re.search(r"\bcalm\b", concept, re.I) or not re.search(r"\bserious\b", concept, re.I):
        errors.append(f"slide {n}: image concept is not calm and serious")
    if "couture" not in concept.lower():
        errors.append(f"slide {n}: image concept is not haute couture")
    return errors


def validate_gamma(texts):
    errors = []
    text = texts[GAMMA]
    found = list(slides(text))
    numbers = [n for n, _, _ in found]
    if numbers != list(range(1, SLIDES + 1)):
        errors.append(f"deck: slides are numbered {numbers}, expected 1–{SLIDES}")
    overlines = {}
    for n, title, chunk in found:
        fields = tuple(re.findall(r"^\*\*\[([A-Z_]+)\]\*\*", chunk, re.M))
        if fields != GAMMA_FIELDS:
            errors.append(f"slide {n}: fields are {list(fields)}, expected {list(GAMMA_FIELDS)}")
            continue
        slide_text, prompt, footer = (gamma_field(chunk, name) for name in GAMMA_FIELDS)
        errors += validate_slide_text(n, title, slide_text)
        overlines[n] = (re.search(r"^- Надзаголовок: (.*)$", slide_text, re.M) or [None, ""])[1]
        errors += validate_image(n, prompt)
        if "\n" in footer or not footer.startswith("Источники: [") or not footer.endswith(GAMMA_FOOTER):
            errors.append(f"slide {n}: footer is not one line «Источники: […](…)…{GAMMA_FOOTER}»")
        if any(not re.match(r"https?://", url) for url in LINK.findall(footer)):
            errors.append(f"slide {n}: footer source without a full URL")
        visible = prose(slide_text + "\n" + footer)
        if n not in ASSEMBLY and CASE.search(visible):
            errors.append(f"slide {n}: running case outside the assembly slides: {CASE.findall(visible)[:3]}")
        if n in ASSEMBLY and f"40-practice-and-cases.md#кейс-{ASSEMBLY.index(n) + 1}-" not in footer:
            errors.append(f"slide {n}: assembly footer does not cite case {ASSEMBLY.index(n) + 1} of the course")
    for name, techs, _, _ in ((a[0], a[2], a[3], a[4]) for a in AXES):
        named = " ".join(overlines.get(n, "") for n in techs + ((STYLES_SLIDE,) if name == "СТИЛЬ" else ()))
        missing = [tech for tech in MANDATORY[name] if tech not in named]
        if missing:
            errors.append(f"deck: mandatory technologies of axis {name} missing: {missing}")
    accessories = "\n".join(chunk for n, _, chunk in found if n in AXES[3][2])
    if "«в тон»" not in accessories:
        errors.append("deck: accessories technologies do not reject the «в тон» rule")
    hits = GRA.findall(prose(text))
    if hits:
        errors.append(f"deck: term of the course data-collection model: {hits[:3]}")
    outside = prose(SLIDE.split(text, 1)[0] + text[text.find("\n## Источники и уровень опоры"):])
    if CASE.search(outside):
        errors.append(f"deck: running case outside the assembly slides: {CASE.findall(outside)[:3]}")
    prompt = code_block(text, "### Промпт для генерации в Gamma")
    if prompt is None:
        errors.append("deck: Gamma prompt block missing")
    else:
        errors += [f"deck: Gamma prompt lacks «{rule}»" for rule in GAMMA_RULES if rule not in prompt]
        if "Не меняй количество слайдов" not in prompt or f"Создай презентацию из {SLIDES} слайдов" not in prompt:
            errors.append("deck: Gamma prompt does not fix the number of slides")
    invented = sorted(set(HEX.findall(text)) - ALLOWED_HEX)
    if invented:
        errors.append(f"deck: colours outside the rules of #693: {invented}")
    rows = LAYOUT_ROW.findall(text)
    if [int(row[0]) for row in rows] != numbers:
        errors.append("deck: photo layout table does not list every slide")
    for row, (n, title, _) in zip(rows, found):
        side, accent = ("слева", "золото #B89B5E") if n % 2 else ("справа", "изумруд #0A4D3C")
        if (row[1].strip(), row[3], row[4]) != (title, side, accent):
            errors.append(f"deck: photo layout row {n} is not «{title} | … | {side} | {accent}»")
    gate = section(text, GATE_HEADING)
    ticked = [line for line in gate.splitlines() if line.startswith("- [")]
    if len(ticked) != len(GATE) or any(not line.startswith(item) for line, item in zip(ticked, GATE)):
        errors.append(f"deck: gate check is not the {len(GATE)} ticked items of #693 in order")
    decisions = section(text, DECISIONS)
    stated = DEVIATION.findall(decisions)
    if DECISIONS not in text or len(stated) < DEVIATIONS:
        errors.append(f"deck: decisions do not state {DEVIATIONS} deviations in the wording of #693")
    open_text = texts[OPEN_FILE]
    for deviation in stated:
        if deviation not in open_text:
            errors.append(f"deck: deviation differs from the module: «{deviation[:60]}»")
    for basis in DECK_BASIS:
        if f"{REPO_BLOB}research/reputation-technologies/{basis}" not in text:
            errors.append(f"deck: does not link the module file {basis} it is built on")
    if f"{REPO_BLOB}{DECK_PATH}" not in texts[INTRO_FILE]:
        errors.append("module: introduction does not link the v4 deck")
    return errors


def validate(texts):
    missing = [path for path in FILES if not texts[path]]
    errors = [f"{path.name}: file not found" for path in missing]
    if missing:
        return errors
    for path in FILES:
        text, name = texts[path], path.name
        if frontmatter(text).get("source", "").strip('"') != SOURCE:
            errors.append(f"{name}: frontmatter source is not issue #693")
        if "<!--" in text:
            errors.append(f"{name}: draft HTML comment")
        errors += [f"{name}: {error}" for error in broken_links(text, texts)]
    relative = [url for url in LINK.findall(texts[GAMMA]) if not re.match(r"https?://", url)]
    if relative:
        errors.append(f"{GAMMA.name}: links are not full URLs: {relative[:3]}")
    errors += validate_gamma(texts)
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
    g = GAMMA
    blob = REPO_BLOB + "research/reputation-technologies/"
    broken = {
        "deck file missing": mutate_re(texts, g, r".*", "", count=1),
        "module file missing": mutate_re(texts, MODULE_FILES[2], r".*", "", count=1),
        "slide removed": mutate_re(texts, g, r"^### Слайд 27\. .*?(?=^## Источники)", ""),
        "slides out of order": mutate(texts, g, "### Слайд 5. ", "### Слайд 6. "),
        "fourth field on a slide": mutate(texts, g, "**[IMAGE_PROMPT]**", "**[SPEAKER_NOTES]**\nРечь.\n\n**[IMAGE_PROMPT]**"),
        "field missing": mutate(texts, g, "**[FOOTER_LINKS]**", "**Ссылки**"),
        "common header lost": mutate(texts, g, "- Шапка: " + GAMMA_HEADER, "- Шапка: Введение в репутационный инжиниринг"),
        "unlabeled line on a slide": mutate(texts, g, "- Вывод: ", "Без метки.\n- Вывод: "),
        "labels out of order": mutate_re(texts, g, r"^(- Эпиграф: .*)\n(- Вводный абзац: .*)$", r"\2\n\1"),
        "overline not in capitals": mutate(texts, g, "- Надзаголовок: ЛЕГЕНДА КАРТЫ", "- Надзаголовок: Легенда карты"),
        "title differs from the heading": mutate(texts, g, "- Заголовок: Карта гипотез: четыре оси", "- Заголовок: Карта гипотез"),
        "title longer than six words": mutate_re(texts, g, r"^(### Слайд 1\. |- Заголовок: )Образ шире четырёх осей$", r"\1Образ гораздо шире любых четырёх осей карты", count=2),
        "epigraph without author": mutate_re(texts, g, r"^(- Эпиграф: «[^\n]*»)\. — [^\n]*$", r"\1"),
        "intro paragraph of three sentences": mutate(texts, g, "- Вводный абзац: ", "- Вводный абзац: Раз. Два. "),
        "facet of the image missing": mutate(texts, g, "мимика, синтаксис и стиль жизни", "мимика и стиль жизни"),
        "legend without «может»": mutate(texts, g, "Образ может собираться по четырём осям", "Образ собирается по четырём осям"),
        "technology overline without author": mutate(texts, g, "- Надзаголовок: ЦВЕТ — СОЧЕТАНИЯ И КОНТРАСТЫ ЦВЕТА — Й. ИТТЕН", "- Надзаголовок: ЦВЕТ · СОЧЕТАНИЯ И КОНТРАСТЫ ЦВЕТА"),
        "mandatory Itten missing": mutate(texts, g, "— Й. ИТТЕН", "— ИОГАННЕС"),
        "mandatory Беляева-Экземплярская missing": mutate(texts, g, "С. Н. БЕЛЯЕВА-ЭКЗЕМПЛЯРСКАЯ\n", "КЛАССИКА МОДЕЛИРОВАНИЯ\n"),
        "«в тон» not rejected": mutate(texts, g, "отвергает подбор «в тон» одежде", "уточняет подбор одежде"),
        "technology numbered wrong": mutate(texts, g, "Технология 2 из 3 на оси формы", "Технология 4 из 4 на оси формы"),
        "technology card renamed": mutate(texts, g, "02 · ИСПОЛЬЗУЮТ — Художники", "02 · ПРИМЕНЕНИЕ — Художники"),
        "vector on a technology card": mutate(texts, g, "- Вывод: Опора К — книга-первоисточник. Иттен", "- Вывод: Вектор гармонии. Опора К — книга-первоисточник. Иттен"),
        "support level missing": mutate(texts, g, "- Вывод: Опора П — широкая практика.", "- Вывод: Широкая практика."),
        "style missing": mutate(texts, g, "- Карточка: 06 · СПОРТ — ", "- Карточка: 06 · ГРАНЖ — "),
        "style without art association": mutate(texts, g, "ассоциация — функционализм и Баухауз", "как в спорте"),
        "art parallels not marked as analogy": mutate(texts, g, "А — искусствоведческие параллели", "искусствоведческие параллели"),
        "interpretation card missing": mutate(texts, g, "- Карточка: 02 · КОНТРАСТ/ЭКЛЕКТИКА — Один названный контраст.", "- Карточка: 02 · АКЦЕНТ — Один названный контраст."),
        "interpretation without synthesis": mutate(texts, g, "- Карточка: 03 · ОБОБЩЕНИЕ — База плюс", "- Карточка: 03 · ИТОГ — База плюс"),
        "marker missing": mutate(texts, g, "- Карточка: 03 · ИНФОПОЛЕ КОММУНИКАЦИИ — Проверка носителя.", "- Карточка: 03 · КАНАЛ — Проверка носителя."),
        "markers out of order": mutate_re(texts, g, r"(### Слайд 13\..*?- Карточка: )01 · СВОИ ОСОБЕННОСТИ(.*?- Карточка: )02 · КОНТЕКСТ: СУБЪЕКТЫ, ОБЪЕКТЫ, МОТИВАЦИИ", r"\g<1>01 · КОНТЕКСТ: СУБЪЕКТЫ, ОБЪЕКТЫ, МОТИВАЦИИ\g<2>02 · СВОИ ОСОБЕННОСТИ"),
        "colour thesis lost": mutate(texts, g, "Тезис проверен и уточнён: цвет не сообщает характер,", "Тезис проверен и уточнён: цвет сообщает характер,"),
        "assembly without hypothesis": mutate(texts, g, "; гипотеза — спокойная палитра", "; спокойная палитра"),
        "assembly without check": mutate(texts, g, "Проверка — разговор идёт", "Разговор идёт"),
        "assembly without case link": mutate(texts, g, "#кейс-2-deep-tech-стартап-инвесторы-и-направление-потока", "#кейс-1-b2b-производитель-консервов-надёжные-оптовые-партнёры"),
        "case on a technology slide": mutate(texts, g, "- Вывод: Опора Э — рецензируемые публикации", "- Вывод: Как у производителя консервов. Опора Э — рецензируемые публикации"),
        "case in the reading guide": mutate(texts, g, "Сборка 1: закупщик региональной розницы | торговый", "Сборка 1: закупщик региональной розницы, оптовый | торговый"),
        "GRA term on a slide": mutate(texts, g, "- Вывод: Тема шире колоды.", "- Вывод: Полярность решает. Тема шире колоды."),
        "«масса» in the deck": mutate(texts, g, "## Как читать", "Палитру выбирает масса.\n\n## Как читать"),
        "GRA named in the gate": mutate(texts, g, "- [x] Модель сбора данных курса", "- [x] Модель GRA и модель сбора данных курса"),
        "image prompt in Russian": mutate(texts, g, "A woman aged 40 walks", "Женщина aged 40 walks"),
        "image rules edited": mutate(texts, g, "Vertical 1:2.4 composition", "Vertical 9:16 composition"),
        "fifth base colour in a palette": mutate(texts, g, "Palette strictly limited to graphite #16181D and deep blue #132A4A with", "Palette strictly limited to graphite #16181D, deep blue #132A4A, emerald #0A4D3C and ruby #720E1E with"),
        "one colour in a palette": mutate(texts, g, "Palette strictly limited to graphite #16181D and deep blue #132A4A with", "Palette strictly limited to graphite #16181D with"),
        "palette colour misnamed": mutate(texts, g, "Palette strictly limited to graphite #16181D and deep blue #132A4A with", "Palette strictly limited to graphite #16181D and emerald #132A4A with"),
        "second gold in a concept": mutate(texts, g, "the single gold accent is a thin inlaid line", "the gold #B89B5E accent is a thin inlaid line"),
        "colour outside the palette": mutate(texts, g, "a floor-length couture coat", "a floor-length white couture coat"),
        "person too young": mutate(texts, g, "A woman aged 40 walks", "A woman aged 22 walks"),
        "stock smile in a concept": mutate(texts, g, "calm, serious face carry", "smiling face carry"),
        "concept without couture": mutate(texts, g, "pins a draped haute couture toile", "pins a draped toile"),
        "footer without Telegram": mutate(texts, g, "(Telegram) @gulienko", "@gulienko"),
        "footer without «Источники:»": mutate_re(texts, g, r"(\*\*\[FOOTER_LINKS\]\*\*\n)Источники: ", r"\1"),
        "footer with a relative link": mutate(texts, g, "[Willis, Todorov, 2006](https://pubmed", "[Willis, Todorov, 2006](../pubmed"),
        "invented hex": mutate(texts, g, "\n## Как читать\n", "\nФон слайда — #F4F1EA.\n\n## Как читать\n"),
        "Gamma prompt lacks a rule": mutate(texts, g, "Space Grotesk, 28 pt", "Space Grotesk"),
        "Gamma prompt slide count": mutate(texts, g, "Создай презентацию из 27 слайдов", "Создай презентацию из 25 слайдов"),
        "photo side not alternating": mutate(texts, g, "| 2 | Технология — метод с опорой | кутюрье закалывает макет на манекене | справа |", "| 2 | Технология — метод с опорой | кутюрье закалывает макет на манекене | слева |"),
        "accent not alternating": mutate(texts, g, "| слева | золото #B89B5E |", "| слева | изумруд #0A4D3C |"),
        "gate item unticked": mutate(texts, g, "- [x] Каждый слайд — ровно три поля", "- [ ] Каждый слайд — ровно три поля"),
        "deviation wording broken": mutate(texts, g, "эффективнее решает задачу [единого визуального языка колоды v4]", "лучше [единого визуального языка колоды v4]"),
        "deviation differs from the module": mutate(texts, g, "эффективнее решает задачу [методологической чистоты]", "эффективнее решает задачу [чистоты метода]"),
        "decisions section lost": mutate(texts, g, DECISIONS, "\n## Заметки\n"),
        "deck does not cite the taxonomy": mutate(texts, g, blob + "image-technologies/20-taxonomy.md", blob + "image-technologies/00-introduction.md", count=-1),
        "module does not link the deck": mutate(texts, INTRO_FILE, REPO_BLOB + DECK_PATH, REPO_BLOB + "research/reputation-technologies/README.md", count=-1),
        "broken anchor": mutate(texts, g, "10-theory.md#3-проверка-тезиса-о-цвете", "10-theory.md#3-тезис-о-цвете"),
        "broken file link": mutate(texts, g, blob + "image-technologies/30-decision-framework.md", blob + "image-technologies/30-framework.md"),
        "source not #693": mutate(texts, g, SOURCE, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/691"),
        "module source not #693": mutate(texts, MODULE_FILES[3], SOURCE, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/691"),
        "draft comment": mutate(texts, g, "\n## Слайды\n", "\n<!-- дописать -->\n\n## Слайды\n"),
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
    print(f"PASS: deck has {SLIDES} slides — introduction 1–2, legend 3, four axes of three technologies with an interpretation and four markers each, six styles on slide {STYLES_SLIDE}, assembly {ASSEMBLY[0]}–{ASSEMBLY[-1]}; every slide has only the fields [SLIDE_TEXT], [IMAGE_PROMPT], [FOOTER_LINKS]")
    print(f"PASS: every slide line has a label in the order Шапка → Надзаголовок → Заголовок → Эпиграф → Вводный абзац → Карточка → Вывод; header «{GAMMA_HEADER}», overline in capitals, titles of at most {TITLE_WORDS} words, intro of 1–2 sentences")
    print("PASS: technology slides are «ОСЬ — МЕТОД — АВТОР» with cards ДЛЯ ЧЕГО → ИСПОЛЬЗУЮТ → В ЧЁМ СУТЬ, no vector and a support level; mandatory technologies of #693 are present and the «в тон» rule is rejected")
    print("PASS: interpretation slides are ГАРМОНИЯ/КЛАССИЦИЗМ → КОНТРАСТ/ЭКЛЕКТИКА → ОБОБЩЕНИЕ or КОНКУРИРУЮЩИЕ ПОДХОДЫ; marker slides are the four management conclusions of #693; the colour thesis is checked on slide 8")
    print("PASS: no term of the course data-collection model anywhere in the deck; running cases only on the assembly slides, each with a hypothesis per axis, a vector, a check and a link to its case")
    print("PASS: image prompts are English haute couture 2026–2027 with the rules of #693 word for word, a palette of 2–3 named base colours and one gold accent, people aged 30–50, calm and serious")
    print("PASS: footers are one line «Источники: …» with full URLs; the Gamma prompt carries every rule; photo side and accent alternate; the gate items are ticked; the deviations follow the wording of #693 and match the module")
    print("PASS: the deck links the module files it is built on and the module links the deck; frontmatter source is #693; repository links and anchors resolve")
    if args.self_test:
        print(f"PASS: {fixtures} broken fixtures rejected")


if __name__ == "__main__":
    main()
