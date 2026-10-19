#!/usr/bin/env python3
"""Check issue #689: the analysis assesses Days 1–4 against the founder's dialog with quotes checked line by line, Variant 2 is a clean catalog of image technologies without GRA, the RFC proposes Days 1–3 first, ONE lecturer phrase and word swaps, deck v2 of Day 4 is rebuilt from the untouched deck v1, the register of findings matches its source lines, the first variants stay byte for byte, the dialog file is deleted and all gate items are confirmed."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
DOMAIN = ROOT / "research/reputation-technologies"
V1 = DOMAIN / "2026-11-03-day4-rationale-and-method.md"
DECK1 = DOMAIN / "2026-11-03-day4-presentation-gamma.md"
V2 = DOMAIN / "2026-11-03-day4-rationale-and-method-v2.md"
ANALYSIS = DOMAIN / "2026-11-03-day4-ai-interpretation-analysis.md"
RFC = DOMAIN / "2026-11-03-day4-crisis-mitigation-rfc.md"
DECK2 = DOMAIN / "2026-11-03-day4-presentation-gamma-v2.md"
FINDINGS = HERE / "findings-days-1-4-689.json"
BUILD = HERE / "build_deck_v2_689.py"
DIALOG = DOMAIN / "2026-10-19-founder-dialog-689.txt"
NEW = (ANALYSIS, V2, RFC, DECK2)
FILES = (V1, DECK1) + NEW + (FINDINGS,)
SOURCE = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/689"
REPO_BLOB = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
LINK = re.compile(r"\]\(([^)\s]+)\)")
# #689 and the founder's comment on PR #690: the first variants stay unchanged — git blob hashes of the files in main.
FIRST_VARIANTS = {V1: "6bae8fc84fc1d5d9d8b483f24aa3473a6768b54e", DECK1: "19df63d29dba90a77f7736efdf08bc7163fc2e6a"}
# Quotes link to the commit that added the founder's dialog: the dialog file is deleted later, the commit keeps it.
SHA = "16415e90abc2d6489ed0ea9582236a3af15bb648"
PERMALINK = re.compile(r"\[([^\]\n]+):(\d+)\]\(https://github\.com/G-Ivan-A/hybrid-Intelligence-lab/blob/" + SHA
                       + r"/research/reputation-technologies/([^?)#\s]+)\?plain=1#L(\d+)\)")
LABELS = {
    "диалог": "2026-10-19-founder-dialog-689.txt",
    "колода Д1": "2026-10-14-day1-presentation-gamma.md",
    "сценарий Д1": "2026-10-14-day1-lecturer-script.md",
    "обоснование Д1": "2026-10-07-day1-rationale-and-method-653.md",
    "разбор лектора Д1": "2026-10-14-day1-lecturer-gra-research.md",
    "колода Д2": "2026-10-30-day2-presentation-gamma.md",
    "черновик колоды Д2": "2026-10-30-day2-presentation.md",
    "сценарий Д2": "2026-10-30-day2-lecturer-script.md",
    "обоснование Д2": "2026-10-30-day2-rationale-and-method.md",
    "колода Д3": "2026-11-02-day3-presentation-gamma.md",
    "черновик колоды Д3": "2026-11-02-day3-presentation.md",
    "сценарий Д3": "2026-11-02-day3-lecturer-script.md",
    "обоснование Д3": "2026-11-02-day3-rationale-and-method.md",
    "стандарт Д3": "2026-11-02-day3-slide-standard-and-gate.md",
    "вариант 1": V1.name,
    "колода Д4 в1": DECK1.name,
    "сценарий Д4": "2026-11-03-day4-lecturer-script.md",
    "RFC v0.3": "2026-10-12-rfc-days-1-3-logic.md",
}
# The founder's deviation format.
DEVIATION = re.compile(r"Я предлагаю скорректировать \[[^\]\n]+\], потому что вариант \[[^\]\n]+\] эффективнее решает задачу \[[^\]\n]+\]")

# Variant 2: a catalog of cards, four fields each, no GRA and no narrative bridge inside the catalog.
CATALOG_HEAD, CATALOG_END = "## Перечень имидж-технологий", "## Технологии на слайдах колоды"
CARD = re.compile(r"^#### (\d+)\. (.+)$", re.M)
CARD_FIELDS = ("- **Название:** ", "- **Суть:** ", "- **Условие применения:** Если ", "- **Визуальный маркер:** ")
CARDS = 21
GRA_WORDS = re.compile(r"масс[аыуеой]|дистанц|полярн|статус|VERIFIED|PARTIAL|CONFLICT|\bGRA\b", re.I)
BRIDGE = re.compile(r"потому что|поэтому", re.I)
V2_SECTIONS = ("## Как читать", "## Граница: что этот перечень не делает", "## Отклонение от постановки",
               "## Лектор на Дне 4", CATALOG_HEAD, CATALOG_END, "## Гейт-проверка Файла 1")
LECTURER = ("На Дне 1 лектор согласился с одним: GRA полезна, чтобы собрать и описать открытые данные о нём самом",
            "На Дне 4 лектор вообще не применяет к себе ни GRA, ни статусы данных")
V2_GATE = 6

# Analysis: the four parts of direction 1 for all four days, the proverb, quotes checked against their lines.
PROVERB = "Заставь дурака молиться, он и лоб расшибет"
EXAMPLES = "## 2. Конкретные примеры провала: День 4"
DAYS = "## 3. Независимая оценка по дням"
DAY_HEADS = ("### 3.1. День 1", "### 3.2. День 2", "### 3.3. День 3", "### 3.4. День 4")
PROVERB_HEAD = f"## 5. «{PROVERB}»: что это значит для ИИ-агента"
ANALYSIS_SECTIONS = ("## Источник разбора", "## Граница: что делает каждая модель", "## 1. Суммаризация проблемы",
                     EXAMPLES, DAYS, "## 4. Корневая причина", PROVERB_HEAD, "### 5.1. Интерпретация для агента",
                     "### 5.2. Наложение на Вариант 1", "### 5.3. Наложение на Дни 1–3", "## Гейт-проверка")
V1_QUOTES = 20
DAY_QUOTES = 3
# The seven gate items of the issue, by their key words.
ANALYSIS_GATE = ("Я полностью прочитал прикреплённый файл диалога и усвоил границы применения GRA", "Я создал Файл 2",
                 "Я создал Файл 1", "Я создал Файл 3", "Я не трогал и не удалял исходный файл `2026-11-03-day4-rationale-and-method.md` (Вариант 1)",
                 "Все 3 файла созданы в каталоге `research/reputation-technologies/`", "Я удалил прикреплённый файл с диалогом")

# RFC: Days 1–3 first, Day 4 deck v2 instead of edits, the founder's phrase verbatim once, the slide 19 title swap.
DAY4 = "## День 4: колода вариант 2 вместо правок"
PHRASE_HEAD = "### Фраза в сценарий лектора: слайд 17"
PROMPT_HEAD = "### Промпт-стратег: исправленное правило 2"
RFC_SECTIONS = ("## Диагноз", "## Как править слайды в Gamma", "### Отклонение: где замена длиннее 1–2 слов",
                "## День 3: слайд-мост 32 — первым", "## День 1: замены или генерация с нуля",
                "### Вариант: сгенерировать колоду Дня 1 с нуля", "## День 2: по желанию", "## RFC v0.3: каркас курса",
                DAY4, PHRASE_HEAD, "### Правки сценария Дня 4", PROMPT_HEAD, "## Порядок действий", "## Вывод",
                "## Гейт-проверка Файла 3")
DAYS_1_3 = ("## День 3: слайд-мост 32 — первым", "## День 1: замены или генерация с нуля", "## День 2: по желанию")
PHRASE = ("> Коллеги, важное разграничение. GRA помогла нам собрать данные о том, КОМУ писать. Но то, КАК мы выглядим "
          "и звучим в этом письме, — это отдельная область: имидж-технологии. GRA не диктует цвет вашего галстука. "
          "Статус VERIFIED не определяет стиль письма. Данные собирает GRA, но решение о подаче принимает человек "
          "на основе отдельной экспертизы.")
SLIDE_17 = "речь к слайду 17 «Гармония: говорить языком точки»"
TITLE_SWAP = re.compile(r"^\| Д4-\d+ \| 19 \| Заголовок \| \[колода Д4 в1:\d+\]\([^)]+\) «Стратегию выбирают полярность, дистанция, масса» \| Правило выбора стиля \|$", re.M)
STEPS = ("День 3", "День 1", "День 2", "День 4", "RFC v0.3")
CRITICAL_SLIDES = ("Д3-G-01", "Д3-G-02", "Д3-G-03")
CONTRACT = "Ничего из этого RFC не применяется без согласования."
DIAGNOSIS = ("Колоды созданы в Gamma", "Менять структуру колод — порядок и число слайдов, вёрстку, изображения — нельзя",
             "**День 4.** В Gamma не генерировался")
CONCLUSION = ("кредиты Gamma", "Новой генерации нет", "в эфире", "«Правило выбора стиля»")
RULE_2 = "2. Данные о связи — массу, дистанцию, полярность и статусы — используй только для описания ситуации, не для выбора стиля."
RFC_GATE = 6
ROW = re.compile(r"^\| (?:Д\d|RFC)-.*\|$", re.M)
SWAP_CELL = re.compile(r"^\[[^\]]+\]\([^)]+\) «(.*)»$")

# Deck v2: rebuilt from deck v1, same slides, slide 19 titled «Правило выбора стиля».
SLIDE = re.compile(r"^### Слайд (\d+)\.", re.M)
DECK2_TITLE = ("### Слайд 19. Правило выбора стиля", "- Заголовок: Правило выбора стиля")
DECK2_GONE = "Стратегию выбирают"
FINDINGS_COUNT, OK_COUNT = 228, 65


def frontmatter(text):
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return dict(line.split(": ", 1) for line in match[1].splitlines() if ": " in line) if match else {}


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


SOURCE_LINES = {}


def source_lines(name):
    """Lines of a file at the commit the quotes link to; CI checks out the full history."""
    if name not in SOURCE_LINES:
        result = subprocess.run(["git", "-C", str(ROOT), "show", f"{SHA}:research/reputation-technologies/{name}"],
                                capture_output=True, text=True)
        SOURCE_LINES[name] = result.stdout.split("\n") if result.returncode == 0 else None
    return SOURCE_LINES[name]


def quote_after(text, start):
    """The «quote» right after a permalink, with nested «» kept."""
    if not text.startswith(" «", start):
        return None
    depth, i = 1, start + 2
    for j in range(i, len(text)):
        depth += {"«": 1, "»": -1}.get(text[j], 0)
        if depth == 0:
            return text[i:j]
    return None


def in_line(quote, line):
    """Every piece of a quote between «…» stands in the line, in order."""
    pos, pieces = 0, [piece.strip() for piece in quote.split("…") if piece.strip()]
    for piece in pieces:
        pos = line.find(piece, pos)
        if pos < 0:
            return False
        pos += len(piece)
    return bool(pieces)


def permalinks(name, text):
    """Check every permalink: label matches file and line, the quote after it stands in that line at commit SHA."""
    errors, count = [], 0
    for match in PERMALINK.finditer(text):
        count += 1
        label, number, path, anchor = match[1], int(match[2]), match[3], int(match[4])
        if LABELS.get(label) != path or number != anchor:
            errors.append(f"{name}: permalink [{label}:{number}] points to {path}#L{anchor}")
            continue
        lines = source_lines(path)
        if lines is None:
            errors.append(f"{name}: cannot read {path} at commit {SHA[:7]}: checkout the full history (fetch-depth: 0)")
            continue
        quote = quote_after(text, match.end())
        if quote is None:
            errors.append(f"{name}: permalink [{label}:{number}] has no «quote» after it")
        elif not 0 < number <= len(lines) or not in_line(quote, lines[number - 1]):
            errors.append(f"{name}: the quote of [{label}:{number}] is not in that line: «{quote[:60]}»")
    return errors, count


def section(text, head, end=None):
    """Body of a section from its heading to the next heading of the same or higher level, or to end."""
    match = re.search(r"^" + re.escape(head) + r".*$", text, re.M)
    if not match:
        return ""
    body = text[match.end():]
    if end:
        return body.split(end, 1)[0]
    level = len(head.split(" ", 1)[0])
    return re.split(r"^#{1,%d} " % level, body, maxsplit=1, flags=re.M)[0]


def gate(name, text, head, expected):
    body = section(text, head)
    done, open_items = re.findall(r"^- \[x\] (.*)$", body, re.M), re.findall(r"^- \[ \] ", body, re.M)
    count = expected if isinstance(expected, int) else len(expected)
    if len(done) != count or open_items:
        return [f"{name}: gate has {len(done)} confirmed and {len(open_items)} open items, expected {count} confirmed"]
    if not isinstance(expected, int):
        return [f"{name}: gate item {i} does not start with «{item}»" for i, (item, line) in enumerate(zip(expected, done), 1)
                if not line.startswith(item)]
    return []


def sections(name, text, heads):
    return [f"{name}: section «{head}» missing" for head in heads if not re.search(r"^" + re.escape(head) + r"$", text, re.M)]


def validate_v2(text):
    errors, name = sections(V2.name, text, V2_SECTIONS), V2.name
    catalog = section(text, CATALOG_HEAD, CATALOG_END)
    for match in sorted(set(m.lower() for m in GRA_WORDS.findall(catalog)))[:3]:
        errors.append(f"{name}: the catalog of image technologies uses GRA or data labels: «{match}»")
    for match in sorted(set(m.lower() for m in BRIDGE.findall(catalog)))[:2]:
        errors.append(f"{name}: a narrative bridge inside the catalog: «{match}»")
    cards = list(CARD.finditer(catalog))
    if [int(m[1]) for m in cards] != list(range(1, CARDS + 1)):
        errors.append(f"{name}: catalog cards are not 1–{CARDS}: {[int(m[1]) for m in cards]}")
    for i, match in enumerate(cards):
        end = cards[i + 1].start() if i + 1 < len(cards) else len(catalog)
        body = re.split(r"^#{1,3} ", catalog[match.end():end], maxsplit=1, flags=re.M)[0]
        lines = [line for line in body.splitlines() if line.startswith("- ")]
        if len(lines) != len(CARD_FIELDS) or any(not line.startswith(field) for line, field in zip(lines, CARD_FIELDS)):
            errors.append(f"{name}: card {match[1]} is not Название, Суть, Условие применения «Если …», Визуальный маркер")
        elif " применяем " not in lines[2]:
            errors.append(f"{name}: card {match[1]} condition is not a direct rule «Если …, применяем …»")
    if not DEVIATION.search(section(text, "## Отклонение от постановки")):
        errors.append(f"{name}: the deviation from the condition examples is not in the founder's format")
    lecturer = section(text, "## Лектор на Дне 4")
    for phrase in LECTURER:
        if phrase not in lecturer:
            errors.append(f"{name}: the lecturer section lost «{phrase[:60]}»")
    errors += gate(name, text, "## Гейт-проверка Файла 1", V2_GATE)
    return errors


def validate_analysis(text, findings):
    errors, name = sections(ANALYSIS.name, text, ANALYSIS_SECTIONS), ANALYSIS.name
    examples = section(text, EXAMPLES)
    quotes = len(re.findall(r"\[вариант 1:\d+\]\(", examples))
    if quotes < V1_QUOTES:
        errors.append(f"{name}: {quotes} permalinked quotes of Variant 1 in the examples, expected at least {V1_QUOTES}")
    for phrase in ("потому что → поэтому", "масса", "дистанция", "полярность"):
        if phrase not in examples.lower():
            errors.append(f"{name}: the examples do not show «{phrase}»")
    for head in DAY_HEADS:
        count = len(PERMALINK.findall(section(text, head)))
        if count < DAY_QUOTES:
            errors.append(f"{name}: «{head}» has {count} permalinked quotes, expected at least {DAY_QUOTES}")
    proverb = section(text, "### 5.1. Интерпретация для агента")
    if len(re.findall(r"^\d\. \*\*", proverb, re.M)) < 3 or "| Расшибленный лоб |" not in proverb:
        errors.append(f"{name}: the proverb is not applied to the agent: roles table and at least three mechanisms")
    if "| Расшибленный лоб |" not in section(text, "### 5.2. Наложение на Вариант 1"):
        errors.append(f"{name}: the proverb is not laid over Variant 1")
    if findings:
        total = f"Все {len(findings['findings'])} найденных нарушений и {len(findings['ok'])} верных интерпретаций"
        if total not in text:
            errors.append(f"{name}: the summary does not match the register: «{total}» missing")
    errors += gate(name, text, "## Гейт-проверка", ANALYSIS_GATE)
    return errors


def cells(row):
    return [cell.strip() for cell in row.strip("|").split(" | ")]


def validate_rfc(text, findings, deck2):
    errors, name = sections(RFC.name, text, RFC_SECTIONS), RFC.name
    if CONTRACT not in text.split("## Диагноз", 1)[0]:
        errors.append(f"{name}: the intro does not say nothing is applied without the founder's agreement")
    positions = [text.find("\n" + head + "\n") for head in DAYS_1_3 + (DAY4,)]
    if -1 not in positions and max(positions[:-1]) > positions[-1]:
        errors.append(f"{name}: Days 1–3 do not come before Day 4")
    steps = re.findall(r"^\d\. \*\*(День \d|RFC v0\.3)\.\*\*", section(text, "## Порядок действий"), re.M)
    if steps != list(STEPS):
        errors.append(f"{name}: the order of actions is not Days 3, 1, 2, then Day 4: {steps}")
    for phrase in DIAGNOSIS:
        if phrase not in section(text, "## Диагноз"):
            errors.append(f"{name}: the diagnosis lost «{phrase[:60]}»")
    if not DEVIATION.search(section(text, "### Отклонение: где замена длиннее 1–2 слов")):
        errors.append(f"{name}: the longer swaps are not a deviation in the founder's format")
    phrase = section(text, PHRASE_HEAD)
    if PHRASE not in phrase:
        errors.append(f"{name}: the founder's phrase is not quoted verbatim in «{PHRASE_HEAD}»")
    if text.count("Коллеги, важное разграничение.") != 1:
        errors.append(f"{name}: the lecturer gets not exactly ONE phrase")
    if SLIDE_17 not in phrase:
        errors.append(f"{name}: the phrase is not placed in the speech to deck slide 17")
    if not TITLE_SWAP.search(section(text, DAY4)):
        errors.append(f"{name}: Day 4 does not swap the slide 19 title for «Правило выбора стиля»")
    day3 = section(text, DAYS_1_3[0])
    for item in CRITICAL_SLIDES:
        if f"| {item} | 32 |" not in day3:
            errors.append(f"{name}: Day 3 lost the critical slide 32 swap {item}")
    rule = re.search(r"```text\n(.*?)```", section(text, PROMPT_HEAD), re.S)
    if not rule or not rule[1].startswith(RULE_2) or "при полярности +1" in rule[1]:
        errors.append(f"{name}: the corrected prompt rule 2 is missing or still ties eclecticism to polarity")
    known = {item["id"]: item for item in findings["findings"]} if findings else {}
    rows = 0
    for match in ROW.finditer(text):
        row = cells(match[0])
        swap = next((i for i, cell in enumerate(row[:-1]) if SWAP_CELL.match(cell)), None)
        if not re.match(r"(Д\d|RFC)-", row[0]) or swap is None:
            continue
        old, new = SWAP_CELL.match(row[swap])[1], row[swap + 1]
        if old == new:
            errors.append(f"{name}: swap {row[0]} changes nothing")
        elif row[0] in known:
            rows += 1
            if (old, new) != (known[row[0]]["was"], known[row[0]]["now"]):
                errors.append(f"{name}: row {row[0]} does not match the register: «{new[:60]}»")
        elif re.match(r"Д4-\d+$", row[0]) and new not in deck2:
            errors.append(f"{name}: Day 4 swap {row[0]} is not in deck v2: «{new[:60]}»")
    if known and rows < 100:
        errors.append(f"{name}: {rows} rows match the register, expected at least 100")
    for phrase in CONCLUSION:
        if phrase not in section(text, "## Вывод"):
            errors.append(f"{name}: the conclusion lost «{phrase}»")
    errors += gate(name, text, "## Гейт-проверка Файла 3", RFC_GATE)
    return errors


BUILT = {}


def build_deck2(deck1):
    """Deck v2 as build_deck_v2_689.py builds it from the given deck v1."""
    if deck1 not in BUILT:
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / DECK1.name).write_text(deck1, encoding="utf-8")
            result = subprocess.run([sys.executable, "-I", str(BUILD), tmp], capture_output=True, text=True)
            out = Path(tmp) / DECK2.name
            BUILT[deck1] = out.read_text(encoding="utf-8") if result.returncode == 0 and out.is_file() else None
    return BUILT[deck1]


def validate_deck2(text, deck1):
    errors, name = [], DECK2.name
    if SLIDE.findall(text) != SLIDE.findall(deck1):
        errors.append(f"{name}: slides differ from deck v1: {SLIDE.findall(text)[:5]}…")
    for phrase in DECK2_TITLE:
        if phrase not in text:
            errors.append(f"{name}: slide 19 is not titled «Правило выбора стиля»: «{phrase}» missing")
    if DECK2_GONE in text:
        errors.append(f"{name}: «{DECK2_GONE}» is still on the slides")
    if build_deck2(deck1) != text:
        errors.append(f"{name}: differs from what {BUILD.name} builds from deck v1")
    return errors


def validate_findings(findings):
    errors, name = [], FINDINGS.name
    if findings.get("source_commit") != SHA:
        errors.append(f"{name}: source_commit is not {SHA[:7]}")
    items, ok = findings.get("findings", []), findings.get("ok", [])
    if len(items) != FINDINGS_COUNT or len(ok) != OK_COUNT:
        errors.append(f"{name}: {len(items)} findings and {len(ok)} correct interpretations, expected {FINDINGS_COUNT} and {OK_COUNT}")
    ids = [item["id"] for item in items]
    if len(set(ids)) != len(ids):
        errors.append(f"{name}: finding ids repeat")
    for item in items + ok:
        lines = source_lines(item["file"])
        where = f"{item.get('id', 'ok')} {item['file']}:{item['line']}"
        if lines is None:
            errors.append(f"{name}: cannot read {item['file']} at commit {SHA[:7]}")
        elif not 0 < item["line"] <= len(lines) or not in_line(item["quote"], lines[item["line"] - 1]):
            errors.append(f"{name}: {where}: the quote is not in that line")
        elif "was" in item and (item["was"] not in lines[item["line"] - 1] or item["was"] == item["now"]):
            errors.append(f"{name}: {where}: «was» is not in the line or equals «now»")
        if "id" in item and (any(kind not in findings["types"] for kind in item["type"].split(",")) or item["severity"] not in findings["severity"]):
            errors.append(f"{name}: {where}: unknown type or severity")
    return errors


def blob(text):
    data = text.encode("utf-8")
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def validate(texts):
    validate.permalinks = 0
    missing = [path for path in FILES if not texts[path]]
    errors = [f"{path.name}: file not found" for path in missing]
    if missing:
        return errors
    for path, expected in FIRST_VARIANTS.items():
        if blob(texts[path]) != expected:
            errors.append(f"{path.name}: the first variant changed: blob {blob(texts[path])}, expected {expected}")
    if texts.get(DIALOG):
        errors.append(f"{DIALOG.name}: the dialog file is not deleted after the three files were committed")
    try:
        findings = json.loads(texts[FINDINGS])
    except ValueError as error:
        errors.append(f"{FINDINGS.name}: not JSON: {error}")
        findings = None
    count = 0
    for path in NEW:
        text, name = texts[path], path.name
        if frontmatter(text).get("source", "").strip('"') != SOURCE:
            errors.append(f"{name}: frontmatter source is not issue #689")
        relative = [url for url in LINK.findall(text) if not re.match(r"https?://", url)]
        if relative:
            errors.append(f"{name}: links are not full URLs: {relative[:3]}")
        errors += [f"{name}: {error}" for error in broken_links(text, texts)]
        if "<!--" in text:
            errors.append(f"{name}: a draft comment is left in the file")
        if path != DECK2:
            found, number = permalinks(name, text)
            errors += found
            count += number
    if findings:
        errors += validate_findings(findings)
    errors += validate_analysis(texts[ANALYSIS], findings)
    errors += validate_v2(texts[V2])
    errors += validate_rfc(texts[RFC], findings, texts[DECK2])
    errors += validate_deck2(texts[DECK2], texts[DECK1])
    validate.permalinks = count
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
    a, v, r, d, f = ANALYSIS, V2, RFC, DECK2, FINDINGS
    dialog = dict(texts)
    dialog[DIALOG] = "1. запрещего перегенерировать\n"
    broken = {
        "RFC missing": mutate_re(texts, r, r".*", "", count=1),
        "dialog file kept": dialog,
        "Variant 1 edited": mutate(texts, V1, "Стратегию выбирают полярность, дистанция, масса", "Правило выбора стиля"),
        "Variant 1 deleted": mutate_re(texts, V1, r".*", "", count=1),
        "deck v1 edited": mutate(texts, DECK1, "Стратегию выбирают полярность, дистанция, масса", "Правило выбора стиля"),
        "source is another issue": mutate(texts, v, 'source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/689"', 'source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/685"'),
        "relative link": mutate(texts, a, "](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/", "](../"),
        "broken anchor": mutate(texts, r, "#нумерация-документ-и-rfc-v03", "#нумерация"),
        "draft comment left": mutate(texts, r, "## Вывод", "<!-- TODO -->\n## Вывод"),
        "permalink quote altered": mutate(texts, a, "«Стратегию выбирают полярность, дистанция, масса", "«Стратегию выбирают имидж-технологии"),
        "permalink line shifted": mutate_re(texts, a, r"\[вариант 1:394\]\((.*?)#L394\)", r"[вариант 1:395](\1#L395)"),
        "permalink label mismatch": mutate_re(texts, r, r"\[сценарий Д4:424\]\((.*?)#L424\)", r"[сценарий Д4:424](\1#L426)"),
        "permalink to another file": mutate(texts, r, "[колода Д3:866](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/" + SHA + "/research/reputation-technologies/2026-11-02-day3-presentation-gamma.md",
                                            "[колода Д3:866](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/" + SHA + "/research/reputation-technologies/2026-11-02-day3-presentation.md"),
        "dialog quote altered": mutate(texts, a, "«GRA запрещено применять к имидж-технологиям»", "«GRA можно применять к имидж-технологиям»"),
        "mass justifies style in the catalog": mutate(texts, v, "- **Условие применения:** Если готовим любой первый контакт", "- **Условие применения:** Если масса аудитории высокая и готовим любой первый контакт"),
        "polarity in a visual marker": mutate(texts, v, "- **Визуальный маркер:** Графит и белый", "- **Визуальный маркер:** При полярности «?» графит и белый"),
        "status label in the catalog": mutate(texts, v, "- **Суть:** Образ соответствует роли", "- **Суть:** Образ со статусом VERIFIED соответствует роли"),
        "GRA in the catalog": mutate(texts, v, "- **Суть:** Образ соответствует роли", "- **Суть:** Образ по GRA соответствует роли"),
        "narrative bridge in the catalog": mutate(texts, v, "- **Суть:** Образ соответствует роли", "- **Суть:** Потому что образ соответствует роли"),
        "card field lost": mutate_re(texts, v, r"(#### 3\. [^\n]+\n\n(?:- [^\n]+\n){1})- \*\*Суть:\*\* [^\n]+\n", r"\1"),
        "condition not a direct rule": mutate(texts, v, "- **Условие применения:** Если готовим", "- **Условие применения:** Когда готовим"),
        "condition without «применяем»": mutate_re(texts, v, r"(#### 4\. [^\n]+\n\n(?:- [^\n]+\n){2}- \*\*Условие применения:\*\* [^\n]*?) применяем ", r"\1 берём "),
        "card removed": mutate_re(texts, v, r"^#### 21\. .*?(?=^## )", ""),
        "cards out of order": mutate(texts, v, "#### 8. ", "#### 9. "),
        "Variant 2 deviation not in format": mutate(texts, v, "эффективнее решает задачу [отделить", "лучше [отделить"),
        "lecturer applies statuses to himself": mutate(texts, v, "На Дне 4 лектор вообще не применяет к себе ни GRA, ни статусы данных", "На Дне 4 лектор не применяет к себе GRA, но берёт статусы данных"),
        "Variant 2 gate item open": mutate(texts, v, "- [x] Только перечень", "- [ ] Только перечень"),
        "analysis quotes of Variant 1 cut": mutate_re(texts, a, r"^### 2\.1\. .*?(?=^### 2\.3\.)", ""),
        "a day not assessed": mutate(texts, a, "### 3.2. День 2", "### 3.2. Второй день"),
        "analysis section lost": mutate(texts, a, "## 4. Корневая причина", "## 4. Причины"),
        "proverb not applied": mutate(texts, a, "| Расшибленный лоб | Разрушенный смысл", "| Итог | Разрушенный смысл"),
        "proverb not laid over Variant 1": mutate_re(texts, a, r"^### 5\.2\. .*?(?=^### 5\.3\.)", "### 5.2. Наложение на Вариант 1\n\n"),
        "summary disagrees with the register": mutate(texts, a, "Все 228 найденных нарушений", "Все 227 найденных нарушений"),
        "analysis gate item lost": mutate_re(texts, a, r"^- \[x\] Все 3 файла[^\n]*\n", ""),
        "dialog deletion not confirmed": mutate(texts, a, "- [x] Я удалил прикреплённый файл с диалогом", "- [x] Файл диалога оставлен"),
        "contract lost": mutate(texts, r, CONTRACT, "Замены можно применять сразу."),
        "Day 4 before Days 1–3": mutate_re(texts, r, r"^(## День 3: слайд-мост 32 — первым\n.*?)(^## День 4: колода вариант 2 вместо правок\n.*?)(?=^## Порядок действий)", r"\2\1"),
        "Day 4 first in the order of actions": mutate_re(texts, r, r"^1\. \*\*День 3\.\*\*(.*?)^4\. \*\*День 4\.\*\*([^\n]*)", r"1. **День 4.**\2\n2. **День 3.**\1", count=1),
        "diagnosis lost": mutate(texts, r, "Менять структуру колод — порядок и число слайдов, вёрстку, изображения — нельзя", "Колоды можно перегенерировать"),
        "longer swaps not a deviation": mutate(texts, r, "Я предлагаю скорректировать [Ограничение «точечная правка 1–2 слов»]", "Можно расширить [Ограничение «точечная правка 1–2 слов»]"),
        "phrase reworded": mutate(texts, r, "GRA не диктует цвет вашего галстука.", "GRA не выбирает галстук."),
        "second phrase": mutate(texts, r, "**Время.**", "> Коллеги, важное разграничение. Ещё одна фраза.\n\n**Время.**"),
        "phrase moved off slide 17": mutate(texts, r, SLIDE_17, "речь к слайду 19 «Правило выбора стиля»"),
        "slide 19 title kept": mutate(texts, r, "| Заголовок | [колода Д4 в1:559]", "| Подзаголовок | [колода Д4 в1:559]"),
        "Day 3 critical swap dropped": mutate_re(texts, r, r"^\| Д3-G-02 \|[^\n]*\n", ""),
        "row disagrees with the register": mutate(texts, r, "| Точки выбраны: гармония или эклектика? |", "| Гармония или эклектика? |"),
        "swap changes nothing": mutate(texts, r, "«МЕТОД КУРСА, ПРИМЕНЁННЫЙ К ЛЕКТОРУ» | ЛЕКТОР ВЕЧЕРА |", "«МЕТОД КУРСА, ПРИМЕНЁННЫЙ К ЛЕКТОРУ» | МЕТОД КУРСА, ПРИМЕНЁННЫЙ К ЛЕКТОРУ |"),
        "Day 4 swap not in deck v2": mutate(texts, r, "» | ЛЕКТОР ВЕЧЕРА |", "» | ЛЕКТОР КУРСА |"),
        "prompt rule 2 kept polarity": mutate(texts, r, RULE_2, "2. Открытую эклектику предлагай только при полярности +1, малой дистанции и высокой массе говорящего."),
        "conclusion lost": mutate(texts, r, "Новой генерации нет", "Нужна новая генерация"),
        "RFC gate item open": mutate(texts, r, "- [x] Диагноз", "- [ ] Диагноз"),
        "deck v2 edited by hand": mutate_re(texts, d, r"^(### Слайд 20\. [^\n]*)$", r"\1 (правка)"),
        "deck v2 keeps the GRA title": mutate(texts, d, "- Заголовок: Правило выбора стиля", "- Заголовок: Стратегию выбирают полярность, дистанция, масса"),
        "deck v2 slide dropped": mutate_re(texts, d, r"^### Слайд 25\..*?(?=^### Слайд 26\.)", ""),
        "register quote altered": mutate(texts, f, '"quote": "Управляйте данными о связях', '"quote": "Управляйте связями'),
        "register line shifted": mutate(texts, f, '"line": 100,\n   "place": "слайд 1 ', '"line": 101,\n   "place": "слайд 1 '),
        "register finding dropped": mutate_re(texts, f, r'\{\s*"id": "Д1-D1".*?\},\s*', ""),
        "register swap changes nothing": mutate(texts, f, '"now": "карту связей нарисует случай"', '"now": "стратегию за вас выберет случай"'),
    }
    failed = [name for name, mutated in broken.items() if mutated == texts or not validate(mutated)]
    return failed, len(broken)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="also prove the checker rejects broken fixtures")
    args = parser.parse_args()
    texts = {path: path.read_text(encoding="utf-8") if path.is_file() else "" for path in FILES + (DIALOG,)}
    errors = validate(texts)
    count = validate.permalinks
    if args.self_test and not errors:
        failed, fixtures = self_test(texts)
        errors += [f"self-test: mutation not rejected: {name}" for name in failed]
    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        raise SystemExit(1)
    print(f"PASS: Variant 1 and deck v1 are unchanged; the dialog file is deleted; the new files cite issue #689, use full URLs and their repository links resolve")
    print(f"PASS: {count} permalinked quotes match their lines at commit {SHA[:7]}; the register holds {FINDINGS_COUNT} findings and {OK_COUNT} correct interpretations, each quote in its line")
    print(f"PASS: the analysis has the summary, at least {V1_QUOTES} quotes of Variant 1, all four days assessed, the root cause and the proverb applied to the agent and laid over Variant 1; gate has {len(ANALYSIS_GATE)} confirmed items")
    print(f"PASS: Variant 2 lists {CARDS} cards of Название, Суть, Условие применения «Если …, применяем …», Визуальный маркер; no mass, distance, polarity, statuses, GRA or «потому что → поэтому» in the catalog; the lecturer applies neither GRA nor statuses to himself; gate has {V2_GATE} confirmed items")
    print(f"PASS: the RFC puts Days 1–3 before Day 4 in its sections and its order of actions, keeps the contract, quotes ONE verbatim phrase for slide 17, swaps the slide 19 title for «Правило выбора стиля», every swap matches the register; gate has {RFC_GATE} confirmed items")
    print(f"PASS: deck v2 is exactly what {BUILD.name} builds from deck v1, keeps its slides and titles slide 19 «Правило выбора стиля»")
    if args.self_test:
        print(f"PASS: {fixtures} broken fixtures rejected")


if __name__ == "__main__":
    main()
