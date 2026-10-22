#!/usr/bin/env python3
"""Check issue #697: the Day 4 deck v5 passes the gate of #693 with the rules of #695 and the #697 image tail, quotes the wording of
the NIA on every slide of the «Гид по стилю» technologies, puts the status line and the context phrase in the conclusion of every
technology slide and the wordings of the PDF reference in the conclusions of the legend and of the axes; the lecturer script v5
speaks every slide in 150–180 words, closes it with one «потому что → поэтому» bridge to the next slide, never copies eight words of
the slides in a row and has a Plan Б for a silent chat with a line to say on every slide."""
import argparse
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
RFC_CHECK = DOMAIN / "exp/rfc-v5-695/check-rfc-695.py"
DECK = DOMAIN / "2026-11-03-day4-presentation-gamma-v5.md"
SCRIPT = DOMAIN / "2026-11-03-day4-lecturer-script-v5.md"
ISSUE = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/697"


def load_rfc_check():
    """check-rfc-695 and its patched check-day4-693; the tail of the image prompts becomes the one of #697."""
    spec = importlib.util.spec_from_file_location("check_rfc_695", RFC_CHECK)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    check = module.CHECK
    old = r"Vertical 1:2\.4 composition, main subject in the central part of the frame\. No text, no letters, no logos, no office scenes, no stock smiles\.$"
    new = (r"Vertical 1:2\.4 composition, editorial photography, main subject in the central part of the frame\. "
           r"No readable text, no logos, no distortion, no office scenes, no stock smiles\.$")
    if check.IMAGE_TAIL.pattern.count(old) != 1:
        raise SystemExit("check-day4-693.py or check-rfc-695.py changed: the image tail of #695 is not found")
    check.IMAGE_TAIL = re.compile(check.IMAGE_TAIL.pattern.replace(old, new), check.IMAGE_TAIL.flags)
    return module, check


RFC, C = load_rfc_check()
FILES = (DECK, SCRIPT) + C.MODULE_FILES
NIA = RFC.NIA
CONTEXT = RFC.CONTEXT
# #697: the wording of the NIA on every slide that names the technologies of «Гид по стилю», not only on the five of #695.
NIA_SLIDES = (3, 5, 10, 12, 14, 16, 18, 20, 23, 25, 26, 27)
NIA_MENTION = re.compile(r"НИА|Гид[а-я]* по стилю", re.I)
# Technology slides: the conclusion carries «Статусы проверки: …» and the context phrase.
TECH_SLIDES = (4, 5, 6, 9, 10, 11, 14, 15, 16, 17, 20, 21, 22)
STYLE_DIRECTIONS = (16, "3.1", 1)  # slide, taxonomy card, extra «?» for the analogy of Russian names
# The wordings of the PDF reference of #697 in the conclusion of the legend and of the analytic markers of each axis, and the source
# of each conclusion in the footer of its slide.
PDF_WORDINGS = {
    3: ("Выбор режима — гипотеза о реакции аудитории, а не правило.", "https://doi.org/10.1177/0146167291175001"),
    8: ("Цвет не сообщает характер — ни ваш, ни чужой. Палитра — гипотеза о первом впечатлении.", "https://doi.org/10.1177/1474704918802412"),
    13: ("Иллюзии формы реальны, но слабы, а правило «вертикаль стройнит» в экспериментах иногда работает наоборот.", "https://doi.org/10.1068/i0405"),
    19: ("Гипотеза теории нарушения ожиданий: позитивно прочитанное отступление выигрывает у нормы", "https://doi.org/10.1080/03637758809376158"),
    24: ("деталь меняет впечатление, но не гарантирует доверия", "https://doi.org/10.1108/13612021311305128"),
}
# #697: no technology is attributed to one author as a personal invention.
INVENTION = re.compile(r"изобрёл|изобрел|изобрела|изобретени|придумал|личн[а-я]* (?:изобретени|открыти|методик)|авторск[а-я]* (?:технологи|метод|систем)", re.I)
BRIDGE = re.compile(r"потому что|поэтому", re.I)
BRIDGE_NAME = "«потому что → поэтому»"
GATE_697 = "\n## Гейт-проверка issue #697\n"
DECISIONS_697 = "\n## Решения исполнителя по issue #697\n"
DEVIATIONS_697 = 2
SCRIPT_LINK = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-11-03-day4-lecturer-script-v5.md"
# Script rules: 1,2 minutes and 150–180 words of speech per slide, the rhythm marks of #697, no eight words of the slides in a row.
SCRIPT_MARK = re.compile(r"`\[СЛАЙД (\d+)\]`")
SPEECH_WORDS = (150, 180)
SLIDE_SECONDS = 72
SPEECH_MARKS = ("`[ПАУЗА]`", "`[ДЕМОНСТРАЦИЯ ЭКРАНА]`", "`[ПЛАН Б ДЛЯ МОЛЧАЛИВОГО ЧАТА]`")
HUMOR = "`[ЮМОР/РАЗРЯДКА]`"
HUMOR_MIN = 9
PLAN_B = re.compile(r"`\[ПЛАН Б ДЛЯ МОЛЧАЛИВОГО ЧАТА\]` \*\[Скажите: «[^\]]+»\.?\]\*")
DEMO = re.compile(r"`\[ДЕМОНСТРАЦИЯ ЭКРАНА\]` \*\[Откройте [^\]]*из подвала")
INTERACTIVE = {"голосование": re.compile(r"[Гг]олосование: "), "проба промпта": re.compile(r"Проба промпта: "),
               "вопрос": re.compile(r"[Вв]опрос в чат: |Напишите в чат: ")}
TABLE_ROW = re.compile(r"^\| (\d+) \| ([^|]+) \| (\d\d:\d\d)–(\d\d:\d\d) \| ([^|]+) \| \[[^\]]+\]\((https://[^)\s]+)\) \|$", re.M)
SCENARIO, SCENARIO_END = "\n## Сценарий\n", "\n## Источники речи\n"
TOTAL = "| **Итого** | 27 слайдов | 00:00–32:24 | 27 интерактивов | **32,4 мин** |"
END_MARK = "*[32:24. Конец блока имидж-технологий.]*"
ASSEMBLY = (25, 26, 27)
NGRAM = 8
WORD = C.WORD


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


def conclusion(chunk):
    match = re.search(r"^- Вывод: (.*)$", C.gamma_field(chunk, "SLIDE_TEXT") or "", re.M)
    return match[1] if match else ""


def validate_deck(texts):
    """Rules of #697 on the deck v5 beyond the gate of #693 and the rules of #695."""
    deck, errors = texts[DECK], []
    found = {n: chunk for n, _, chunk in C.slides(deck)}
    if ISSUE not in [item.strip() for item in C.frontmatter(deck).get("source", "").strip('"').split(";")]:
        errors.append("deck: frontmatter source does not name issue #697")
    for n, chunk in found.items():
        text = C.gamma_field(chunk, "SLIDE_TEXT") or ""
        if (n in NIA_SLIDES or NIA_MENTION.search(text)) and NIA not in text:
            errors.append(f"deck slide {n}: names the technologies of «Гид по стилю» without the wording of the NIA")
        if BRIDGE.search(C.prose(text)):
            errors.append(f"deck slide {n}: bridge {BRIDGE_NAME} on the slide")
    for n in TECH_SLIDES:
        line = conclusion(found.get(n, ""))
        if not re.search(r"Статусы проверки: [^.]+\.", line) or CONTEXT not in line:
            errors.append(f"deck slide {n}: conclusion without «Статусы проверки: ….» and the context phrase")
    n, card, analogies = STYLE_DIRECTIONS
    tax = RFC.taxonomy_profiles(texts[RFC.TAXONOMY])
    expected = RFC.profile(tax.get(card, "").split(".")[0])
    expected["?"] += analogies
    status = re.search(r"Статусы проверки: ([^.]*)\.", conclusion(found.get(n, "")))
    if not status or RFC.profile(status[1]) != expected:
        errors.append(f"deck slide {n}: status profile is not card {card} plus {analogies} «?» for the analogy: {expected}")
    for n, (wording, source) in PDF_WORDINGS.items():
        chunk = found.get(n, "")
        if wording not in conclusion(chunk):
            errors.append(f"deck slide {n}: conclusion does not carry the wording of the PDF reference «{wording[:50]}…»")
        if source not in (C.gamma_field(chunk, "FOOTER_LINKS") or ""):
            errors.append(f"deck slide {n}: footer does not name the source of the conclusion {source}")
    hits = INVENTION.findall(C.prose("\n".join(chunk for chunk in found.values())))
    if hits:
        errors.append(f"deck: slide attributes a technology as a personal invention: {hits[:3]}")
    gate = C.section(deck, GATE_697)
    if not gate or not re.search(r"^- \[x\] ", gate, re.M) or re.search(r"^- \[ \] ", gate, re.M):
        errors.append("deck: gate check of #697 missing or not all ticked")
    decisions = C.section(deck, DECISIONS_697)
    if len(RFC.DEVIATION.findall(decisions)) < DEVIATIONS_697:
        errors.append(f"deck: decisions of #697 do not state {DEVIATIONS_697} deviations in the wording of the issue")
    if SCRIPT_LINK not in deck:
        errors.append("deck: no link to the lecturer script v5")
    return errors


def validate_script(texts):
    text, deck, errors = texts[SCRIPT], texts[DECK], []
    name = SCRIPT.name
    if C.frontmatter(text).get("source", "").strip('"') != ISSUE:
        errors.append(f"{name}: frontmatter source is not issue #697")
    for url in dict.fromkeys(C.LINK.findall(text)):
        if not url.startswith("https://") or any(fragment in url for fragment in RFC.BANNED_URLS):
            errors.append(f"{name}: link is not a full https URL of a primary source: {url}")
    errors += [f"{name}: {error}" for error in C.broken_links(text, texts)]
    errors += [f"{name}: names «{banned}»" for banned in RFC.BANNED_V5 + RFC.BANNED_SLIDES if banned.casefold() in text.casefold()]
    if "<!--" in text:
        errors.append(f"{name}: draft HTML comment")
    titles = {n: title for n, title, _ in C.slides(deck)}
    footers = {n: C.gamma_field(chunk, "FOOTER_LINKS") or "" for n, _, chunk in C.slides(deck)}
    body = C.section(text, SCENARIO, SCENARIO_END)
    if not body or SCENARIO_END not in text:
        return errors + ["script: sections «Сценарий» and «Источники речи» missing"]
    if {n: title for n, title, _ in C.slides(body)} != titles:
        errors.append("script: slide headings differ from the deck")
    found = dict(speeches(body))
    if list(found) != list(titles):
        errors.append(f"script: slide marks are {list(found)}, expected {list(titles)}")
    if TOTAL not in text or "\n## Тайминг и План Б\n" not in text:
        errors.append(f"script: timing table without «{TOTAL}»")
    rows = {int(row[0]): row for row in TABLE_ROW.findall(C.section(text, "\n## Тайминг и План Б\n"))}
    if list(rows) != list(titles):
        errors.append(f"script: timing table rows are {list(rows)}, expected {list(titles)}")
    slide_grams = set()
    for _, _, chunk in C.slides(deck):
        slide_grams |= grams(C.gamma_field(chunk, "SLIDE_TEXT") or "")
    last = max(titles, default=0)
    humor = 0
    for n, speech in found.items():
        start, end = clock((n - 1) * SLIDE_SECONDS), clock(n * SLIDE_SECONDS)
        if f"*[{start}]* `[СЛАЙД {n}]`" not in body or f"*Тайминг: 1,2 мин ({start}–{end})" not in body:
            errors.append(f"script: slide {n} is not timed 1,2 мин from {start} to {end}")
        row = rows.get(n)
        if row and (row[1].strip() != titles.get(n) or (row[2], row[3]) != (start, end) or row[5] not in footers.get(n, "")):
            errors.append(f"script: timing row {n} is not «{titles.get(n)} | {start}–{end}» with a source from the footer of the slide")
        said = spoken(speech)
        words = len(WORD.findall(said))
        if not SPEECH_WORDS[0] <= words <= SPEECH_WORDS[1]:
            errors.append(f"script: slide {n} speech has {words} words, expected {SPEECH_WORDS[0]}–{SPEECH_WORDS[1]}")
        for mark in SPEECH_MARKS:
            if speech.count(mark) != 1:
                errors.append(f"script: slide {n} has {speech.count(mark)} marks {mark}, expected one")
        if speech.count(HUMOR) > 1:
            errors.append(f"script: slide {n} has {speech.count(HUMOR)} marks {HUMOR}, expected at most one")
        humor += speech.count(HUMOR)
        if not DEMO.search(speech):
            errors.append(f"script: slide {n} demonstration does not open a source from the footer")
        kinds = [kind for kind, pattern in INTERACTIVE.items() if pattern.search(said)]
        if row and kinds[:1] != [row[4].strip()]:
            errors.append(f"script: slide {n} interaction is {kinds}, the timing table says «{row[4].strip()}»")
        if not PLAN_B.search(speech):
            errors.append(f"script: slide {n} Plan Б has no line to say «Скажите: «…»»")
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
        if n not in ASSEMBLY and C.CASE.search(C.prose(speech)):
            errors.append(f"script: slide {n} speech names a case of the course: {C.CASE.findall(C.prose(speech))[:3]}")
    if humor < HUMOR_MIN:
        errors.append(f"script: {humor} marks {HUMOR}, expected at least {HUMOR_MIN}")
    if not body.rstrip().endswith(END_MARK):
        errors.append(f"script: scenario does not end with «{END_MARK}»")
    outside = C.prose(text.replace(body, "")).replace(BRIDGE_NAME, "")
    if BRIDGE.search(outside):
        errors.append(f"script: {BRIDGE_NAME} outside the speeches")
    rest = text.replace(body, "")
    hits = [hit for hit in C.CASE.findall(C.prose(rest))]
    if hits:
        errors.append(f"script: case of the course outside the assembly speeches: {hits[:3]}")
    hits = C.GRA.findall(C.prose(text)) + re.findall(r"VERIFIED|PARTIAL|CONFLICT|\bGRA\b", text)
    if hits:
        errors.append(f"script: term of the course data-collection model: {hits[:3]}")
    hits = INVENTION.findall(C.prose(text))
    if hits:
        errors.append(f"script: technology attributed as a personal invention: {hits[:3]}")
    return errors


def validate(texts):
    missing = [path for path in (DECK, SCRIPT) if not texts[path]]
    if missing:
        return [f"{path.name}: file not found" for path in missing]
    gate_texts = dict(texts)
    gate_texts[C.GAMMA] = texts[DECK]
    errors = [f"gate #693/#695: {error}" for error in C.validate(gate_texts) + RFC.validate_v5(texts[DECK], texts)]
    return errors + validate_deck(texts) + validate_script(texts)


mutate, mutate_re = C.mutate, C.mutate_re


def speech(texts, n, pattern, new):
    """Fixture: the first match of pattern in the speech of slide n replaced."""
    return mutate_re(texts, SCRIPT, rf"(`\[СЛАЙД {n}\]`(?:(?!`\[СЛАЙД ).)*?){pattern}", rf"\g<1>{new}")


def self_test(texts):
    d, s = DECK, SCRIPT
    broken = {
        "deck missing": mutate_re(texts, d, r".*", "", count=1),
        "script missing": mutate_re(texts, s, r".*", "", count=1),
        "deck source without #697": mutate(texts, d, "; https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/697\"", '"'),
        "prompt tail of #695 kept": mutate(texts, d, "No readable text, no logos, no distortion, no office scenes", "No text, no letters, no logos, no office scenes"),
        "editorial photography dropped": mutate(texts, d, "Vertical 1:2.4 composition, editorial photography, ", "Vertical 1:2.4 composition, "),
        "Bauhaus back in a prompt": mutate(texts, d, "inspired by the idea of art deco.", "inspired by the idea of art deco and Bauhaus."),
        "NIA wording dropped on slide 12": mutate_re(texts, d, r"(### Слайд 12\..*?)" + re.escape(NIA), r"\1Технологии НИА"),
        "NIA wording dropped on slide 27": mutate_re(texts, d, r"(### Слайд 27\..*?)" + re.escape(NIA), r"\1Технологии НИА"),
        "NIA wording edited on slide 5": mutate_re(texts, d, r"(### Слайд 5\..*?)на базе которых впоследствии", r"\1на базе которых"),
        "status line dropped on slide 4": mutate_re(texts, d, r"(### Слайд 4\..*?- Вывод: [^\n]*?) Статусы проверки: [^.]*\.", r"\1"),
        "context phrase dropped on slide 15": mutate_re(texts, d, r"(### Слайд 15\..*?- Вывод: [^\n]*?) " + re.escape(CONTEXT), r"\1"),
        "slide 16 profile edited": mutate(texts, d, "1 PARTIAL, 2 «?» по шкале Маккимзи", "1 PARTIAL, 1 «?» по шкале Маккимзи"),
        "slide 6 profile differs from taxonomy": mutate_re(texts, d, r"(### Слайд 6\..*?Статусы проверки: )1 VERIFIED", r"\g<1>2 VERIFIED"),
        "legend wording of the PDF lost": mutate(texts, d, "Выбор режима — гипотеза о реакции аудитории, а не правило.", "Выбор режима — дело вкуса."),
        "colour wording of the PDF lost": mutate(texts, d, "Цвет не сообщает характер — ни ваш, ни чужой.", "Цвет сообщает характер."),
        "form wording of the PDF lost": mutate(texts, d, "в экспериментах иногда работает наоборот", "работает всегда"),
        "style wording of the PDF lost": mutate(texts, d, "позитивно прочитанное отступление выигрывает у нормы", "отступление выигрывает у нормы"),
        "accessories wording of the PDF lost": mutate(texts, d, "деталь меняет впечатление, но не гарантирует доверия", "деталь гарантирует доверие"),
        "source of the style conclusion dropped": mutate_re(texts, d, r"(### Слайд 19\..*?\*\*\[FOOTER_LINKS\]\*\*\n[^\n]*?)\[Burgoon, Hale, 1988\]\(https://doi.org/10.1080/03637758809376158\)", r"\1Burgoon, Hale, 1988"),
        "bridge on a slide": mutate(texts, d, "- Вывод: Тема шире колоды.", "- Вывод: Тема шире колоды, поэтому нужны оси."),
        "personal invention on a slide": mutate(texts, d, "- Вывод: Опора К — книга-первоисточник. Иттен", "- Вывод: Опора К — книга-первоисточник. Иттен изобрёл метод, и Иттен"),
        "case on a technology slide": mutate(texts, d, "- Вывод: Тема шире колоды.", "- Вывод: Тема шире колоды, как у дистрибьютора."),
        "GRA term justifies a choice": mutate(texts, d, "- Вывод: Тема шире колоды.", "- Вывод: Тема шире колоды, а выбор задаёт полярность."),
        "ВШСДТ back in the deck": mutate(texts, d, "четыре стиля «Гида по стилю» и коэффициент", "четыре стиля ВШСДТ и коэффициент"),
        "shortened link in the deck": mutate(texts, d, "(https://doi.org/10.1002/col.5080060210)", "(https://bit.ly/3kXy)"),
        "gate of #697 unticked": mutate_re(texts, d, r"(## Гейт-проверка issue #697.*?)- \[x\] ", r"\1- [ ] "),
        "deviation of #697 reworded": mutate_re(texts, d, r"(## Решения исполнителя по issue #697.*?)потому что вариант", r"\1так как вариант"),
        "deck does not link the script": mutate(texts, d, SCRIPT_LINK, SCRIPT_LINK.replace("-v5.md", "-v3.md"), count=-1),
        "script source not #697": mutate(texts, s, f'source: "{ISSUE}"', 'source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/695"'),
        "script slide mark missing": mutate(texts, s, "`[СЛАЙД 9]`", "СЛАЙД 9"),
        "script heading differs from the deck": mutate(texts, s, "### Слайд 6. Цвет: шкала образов Кобаяси", "### Слайд 6. Цвет: шкала Кобаяси"),
        "slide not at 1,2 minutes": mutate(texts, s, "*[13:12]* `[СЛАЙД 12]`", "*[13:30]* `[СЛАЙД 12]`"),
        "timing total lost": mutate(texts, s, TOTAL, "| **Итого** | 27 слайдов | 00:00–40:00 | **40 мин** |"),
        "timing row with a source not in the footer": mutate(texts, s, "| [Kobayashi, 1981](https://doi.org/10.1002/col.5080060210) |", "| [Kobayashi, 1981](https://doi.org/10.1002/col.0000000000) |"),
        "timing row says question, speech votes": mutate(texts, s, "| 07:12–08:24 | голосование |", "| 07:12–08:24 | вопрос |"),
        "short speech": speech(texts, 2, r"Дальше вопрос доверия:[^\n]*\n\n", ""),
        "long speech": speech(texts, 5, r"Вторая технология цвета идёт от человека\.", "Вторая технология цвета идёт от человека. " + "Это важно для образа. " * 6),
        "pause mark missing": speech(texts, 3, r" `\[ПАУЗА\]`", ""),
        "demonstration mark missing": speech(texts, 4, r"`\[ДЕМОНСТРАЦИЯ ЭКРАНА\]` ", ""),
        "demonstration not from the footer": speech(texts, 4, r"Откройте книгу Иттена в архиве из подвала слайда", "Откройте любую книгу об Иттене"),
        "Plan Б without a line on a vote slide": speech(texts, 7, r"\*\[Скажите: «Представьте финансового директора[^\]]*\]\*", "*[Подождите ещё.]*"),
        "Plan Б missing on a prompt trial": speech(texts, 18, r"`\[ПЛАН Б ДЛЯ МОЛЧАЛИВОГО ЧАТА\]` \*\[[^\]]*\]\*\n\n", ""),
        "two humour marks in a speech": speech(texts, 5, r"`\[ЮМОР/РАЗРЯДКА\]` Да,", "`[ЮМОР/РАЗРЯДКА]` `[ЮМОР/РАЗРЯДКА]` Да,"),
        "humour marks dropped": mutate(texts, s, "`[ЮМОР/РАЗРЯДКА]` ", "", count=-1),
        "speech without a bridge": speech(texts, 10, r"Потому что тип фигуры по справочнику служит впечатлению, а индустрии нужна точная посадка, поэтому",
                                          "Тип фигуры по справочнику служит впечатлению, а индустрии нужна точная посадка, и"),
        "second bridge inside a speech": speech(texts, 11, "Метод живой:", "Поэтому метод живой:"),
        "bridge after the last slide": mutate(texts, s, "На этом блок имидж-технологий закончен.", "Потому что карта собрана, поэтому блок закончен."),
        "bridge outside the speeches": mutate(texts, s, "\n## Перед эфиром\n", "\nПоэтому блок длинный.\n\n## Перед эфиром\n"),
        "speech retells the slide": speech(texts, 8, "Цвет двигает впечатление на миллиметры, а не на километры.",
                                           "Цвет не сообщает характер — ни ваш, ни чужой. Палитра — гипотеза о первом впечатлении."),
        "case of the course in a technology speech": speech(texts, 15, "Механизм понятен любому,", "Механизм понятен дистрибьютору «Д» и любому,"),
        "GRA term in a speech": speech(texts, 7, "Соединяем три технологии.", "Соединяем три технологии, а выбор задаёт дистанция."),
        "status code in a speech": speech(texts, 4, "сколько утверждений подтверждено,", "сколько утверждений VERIFIED,"),
        "personal invention in a speech": speech(texts, 17, "Кибби — западный соперник,", "Кибби придумал этот метод, это западный соперник,"),
        "Туркенич in the script": speech(texts, 14, "Ось стиля начинаем", "Как у Школы Туркенич, ось стиля начинаем"),
        "shortened link in the script": mutate(texts, s, "(https://doi.org/10.1177/0146167291175001)", "(https://bit.ly/3brewer)"),
        "broken anchor in the script": mutate(texts, s, "#источники-и-уровень-опоры", "#источники"),
        "end mark lost": mutate(texts, s, END_MARK, "*[Конец.]*"),
    }
    failed = [name for name, mutated in broken.items() if mutated == texts or not validate(mutated)]
    return failed, len(broken)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="also prove the checker rejects broken fixtures")
    args = parser.parse_args()
    texts = {path: path.read_text(encoding="utf-8") if path.is_file() else "" for path in FILES + (RFC.TAXONOMY,)}
    errors = validate(texts)
    if args.self_test and not errors:
        failed, fixtures = self_test(texts)
        errors += [f"self-test: mutation not rejected: {name}" for name in failed]
    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        raise SystemExit(1)
    count = len(list(C.slides(texts[DECK])))
    print(f"PASS: deck v5 passes the gate of #693 with the rules of #695 and the image tail of #697; {count} slides, three fields each")
    print(f"PASS: the wording of the NIA stands word for word on every slide of the «Гид по стилю» technologies: {', '.join(map(str, NIA_SLIDES))}")
    print(f"PASS: the conclusion of every technology slide ({', '.join(map(str, TECH_SLIDES))}) carries «Статусы проверки: …» and the context "
          "phrase; profiles equal the taxonomy, slide 16 — card 3.1 plus one «?» for the analogy")
    print(f"PASS: conclusions of slides {', '.join(map(str, PDF_WORDINGS))} carry the wordings of the PDF reference with their sources in the "
          "footer; no bridge on the slides, no case outside the assembly slides, no technology as a personal invention")
    print(f"PASS: gate of #697 ticked, {DEVIATIONS_697} deviations in the wording of the issue, the deck links the lecturer script v5")
    print(f"PASS: script marks `[СЛАЙД 1]`…`[СЛАЙД {count}]` at 1,2 minutes each, {SPEECH_WORDS[0]}–{SPEECH_WORDS[1]} spoken words per slide, "
          "timing table with the interaction and a footer source of each slide")
    print(f"PASS: every speech has one `[ПАУЗА]`, one `[ДЕМОНСТРАЦИЯ ЭКРАНА]` of a footer source and a `[ПЛАН Б ДЛЯ МОЛЧАЛИВОГО ЧАТА]` "
          f"with a line to say; at most one {HUMOR} per speech, at least {HUMOR_MIN} in total")
    print(f"PASS: one bridge {BRIDGE_NAME} closes each speech 1–{count - 1}; none on the last slide or outside the speeches; no "
          f"{NGRAM}-word copy of the slides; no case outside speeches 25–27, no term of the data-collection model, full https links")
    if args.self_test:
        print(f"PASS: {fixtures} broken fixtures rejected")


if __name__ == "__main__":
    main()
