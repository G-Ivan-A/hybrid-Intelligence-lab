#!/usr/bin/env python3
"""Check issue #689: the analysis of the AI interpretation failure quotes Variant 1 line by line and explains the proverb, Variant 2 is a clean catalog of image technologies without GRA, the RFC fixes the generated deck with one lecturer phrase and a few word swaps, Variant 1 stays byte for byte as PR #686 accepted it, and all gate items are confirmed."""
import argparse
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
V1 = DOMAIN / "2026-11-03-day4-rationale-and-method.md"
V2 = DOMAIN / "2026-11-03-day4-rationale-and-method-v2.md"
ANALYSIS = DOMAIN / "2026-11-03-day4-ai-interpretation-analysis.md"
RFC = DOMAIN / "2026-11-03-day4-crisis-mitigation-rfc.md"
NEW = (ANALYSIS, V2, RFC)
FILES = (V1,) + NEW
SOURCE = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/689"
REPO_BLOB = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
# The deck of #688 is not in main yet: it is linked by a permalink to the commit the slides were generated from.
DECK = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9d1fc9f0dc17924f04abb5c53260edcc97e897f9/research/reputation-technologies/2026-11-03-day4-presentation-gamma.md"
LINK = re.compile(r"\]\(([^)\s]+)\)")
# #689: Variant 1 stays unchanged — the git blob hash of the file PR #686 merged into main (54dcc91).
V1_BLOB = "6bae8fc84fc1d5d9d8b483f24aa3473a6768b54e"
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
            "На Дне 4 лектор не применяет GRA к себе для выбора стиля")
V2_GATE = 6

# Analysis: the four parts of direction 1, the proverb and quotes of Variant 1 checked against its lines.
PROVERB = "Заставь дурака молиться, он и лоб расшибет"
ANALYSIS_SECTIONS = ("## Источник разбора", "## Граница, которую нарушил ИИ", "## 1. Суммаризация проблемы",
                     "## 2. Конкретные примеры провала", "## 3. Корневая причина",
                     f"## 4. «{PROVERB}»: что это значит для ИИ-агента", "## 5. Что исправлено", "## Гейт-проверка")
ROW_QUOTE = re.compile(r"^\| строка (\d+)[^|\n]*\| «(.+)» \| [^|\n]+ \|$", re.M)
ITEM_QUOTE = re.compile(r"^(?:- )?[Сс]трока (\d+)[^:\n]*: [^«\n]*«(.+)»", re.M)
QUOTES = 20
ANALYSIS_GATE = 7
NO_DIALOG = "Файл диалога: неприменимо"

# RFC: the four parts of direction 3, the founder's phrase verbatim and the P0 word swap on slide 19.
RFC_SECTIONS = ("## 1. Диагноз", "## 2. Решение для сценария лектора: одна фраза на слайде 17",
                "## 3. Решение для презентации: точечные замены в `[SLIDE_TEXT]`", "### P0. Обязательно: две замены на слайде 19",
                "## 4. Вывод", "## Гейт-проверка Файла 3")
PHRASE = ("> Коллеги, важное разграничение. GRA помогла нам собрать данные о том, КОМУ писать. Но то, КАК мы выглядим "
          "и звучим в этом письме, — это отдельная область: имидж-технологии. GRA не диктует цвет вашего галстука. "
          "Статус VERIFIED не определяет стиль письма. Данные собирает GRA, но решение о подаче принимает человек "
          "на основе отдельной экспертизы.")
SLIDE_17 = "**Слайд 17 колоды «Гармония: говорить языком точки»**"
P0_TITLE = "| P0-1 | 19 | Заголовок | Стратегию выбирают полярность, дистанция, масса | **Правило выбора стиля** |"
P0_ROW = re.compile(r"^\| P0-\d+ \| ", re.M)
P0_ROWS = 2
SWAP_ROW = re.compile(r"^\| (P\d-\d+) \| (\d+) \| [^|\n]+ \| ([^|\n]+) \| ([^|\n]+) \|$", re.M)
DIAGNOSIS = ("26 слайдов сгенерированы в Gamma", "Менять структуру колоды — порядок и число слайдов, вёрстку, изображения — нельзя")
CONCLUSION = ("кредиты Gamma", "Новой генерации нет", "В эфире", "В тексте слайда 19")
RFC_GATE = 6


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


def section(text, head, end=None):
    """Body of a section from its heading to the next heading of the same level, or to end."""
    if head not in text:
        return ""
    body = text.split(head, 1)[1]
    if end:
        return body.split(end, 1)[0]
    level = head.split(" ", 1)[0]
    return re.split(r"^" + level + r" ", body, maxsplit=1, flags=re.M)[0]


def gate(name, text, head, expected):
    body = section(text, head)
    done, open_items = re.findall(r"^- \[x\] ", body, re.M), re.findall(r"^- \[ \] ", body, re.M)
    if len(done) != expected or open_items:
        return [f"{name}: gate has {len(done)} confirmed and {len(open_items)} open items, expected {expected} confirmed"]
    return []


def sections(name, text, heads):
    return [f"{name}: section «{head}» missing" for head in heads if not re.search(r"^" + re.escape(head) + r"$", text, re.M)]


def plain(text):
    return text.replace("**", "").replace("*", "")


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
    deviation = section(text, "## Отклонение от постановки")
    if not DEVIATION.search(deviation):
        errors.append(f"{name}: the deviation from the condition examples is not in the founder's format")
    lecturer = section(text, "## Лектор на Дне 4")
    for phrase in LECTURER:
        if phrase not in lecturer:
            errors.append(f"{name}: the lecturer section lost «{phrase[:60]}»")
    errors += gate(name, text, "## Гейт-проверка Файла 1", V2_GATE)
    return errors


def validate_analysis(text, v1):
    errors, name = sections(ANALYSIS.name, text, ANALYSIS_SECTIONS), ANALYSIS.name
    lines = plain(v1).splitlines()
    quotes = [(int(m[1]), m[2]) for pattern in (ROW_QUOTE, ITEM_QUOTE) for m in pattern.finditer(section(text, "## 2. Конкретные примеры провала"))]
    if len(quotes) < QUOTES:
        errors.append(f"{name}: {len(quotes)} quotes of Variant 1 with line numbers, expected at least {QUOTES}")
    for number, quote in quotes:
        line = lines[number - 1] if 0 < number <= len(lines) else ""
        parts = [part.strip() for part in plain(quote).split("…") if part.strip()]
        if not parts or any(part not in line for part in parts):
            errors.append(f"{name}: the quote of line {number} is not in Variant 1: «{quote[:60]}»")
    if not DEVIATION.search(section(text, "## Источник разбора")):
        errors.append(f"{name}: the missing dialog file has no deviation in the founder's format")
    for phrase in ("потому что → поэтому", "масса", "дистанция", "полярность"):
        if phrase not in section(text, "## 2. Конкретные примеры провала").lower():
            errors.append(f"{name}: the examples do not show «{phrase}»")
    proverb = section(text, f"## 4. «{PROVERB}»: что это значит для ИИ-агента")
    if len(re.findall(r"^\d\. \*\*", proverb, re.M)) < 3 or "| Расшибленный лоб |" not in proverb:
        errors.append(f"{name}: the proverb is not applied to the agent: roles table and at least three mechanisms")
    if NO_DIALOG not in section(text, "## Гейт-проверка"):
        errors.append(f"{name}: gate item 7 does not say the dialog file was not applicable")
    errors += gate(name, text, "## Гейт-проверка", ANALYSIS_GATE)
    return errors


def validate_rfc(text):
    errors, name = sections(RFC.name, text, RFC_SECTIONS), RFC.name
    for phrase in DIAGNOSIS:
        if phrase not in section(text, "## 1. Диагноз"):
            errors.append(f"{name}: the diagnosis lost «{phrase[:60]}»")
    lecturer = section(text, "## 2. Решение для сценария лектора: одна фраза на слайде 17")
    if PHRASE not in lecturer:
        errors.append(f"{name}: the founder's phrase is not quoted verbatim in the lecturer section")
    if text.count("Коллеги, важное разграничение.") != 1:
        errors.append(f"{name}: the lecturer gets not exactly ONE phrase")
    if SLIDE_17 not in lecturer:
        errors.append(f"{name}: the phrase is not placed on deck slide 17")
    if P0_TITLE not in text:
        errors.append(f"{name}: P0 does not swap the slide 19 title for «Правило выбора стиля»")
    p0 = section(text, "### P0. Обязательно: две замены на слайде 19")
    if len(P0_ROW.findall(p0)) != P0_ROWS:
        errors.append(f"{name}: P0 has {len(P0_ROW.findall(p0))} swaps, expected {P0_ROWS}")
    if not DEVIATION.search(section(text, "### Отклонение: необязательный список P1")):
        errors.append(f"{name}: the optional P1 list is not a deviation in the founder's format")
    for swap, slide, old, new in SWAP_ROW.findall(text):
        if old.strip() == new.strip():
            errors.append(f"{name}: swap {swap} on slide {slide} changes nothing")
    if f"]({DECK})" not in text:
        errors.append(f"{name}: the deck permalink of #688 is missing")
    for phrase in CONCLUSION:
        if phrase not in section(text, "## 4. Вывод"):
            errors.append(f"{name}: the conclusion lost «{phrase}»")
    errors += gate(name, text, "## Гейт-проверка Файла 3", RFC_GATE)
    return errors


def blob(text):
    data = text.encode("utf-8")
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def validate(texts):
    missing = [path for path in FILES if not texts[path]]
    errors = [f"{path.name}: file not found" for path in missing]
    if missing:
        return errors
    if blob(texts[V1]) != V1_BLOB:
        errors.append(f"{V1.name}: Variant 1 changed: blob {blob(texts[V1])}, expected {V1_BLOB}")
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
    errors += validate_analysis(texts[ANALYSIS], texts[V1])
    errors += validate_v2(texts[V2])
    errors += validate_rfc(texts[RFC])
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
    a, v, r = ANALYSIS, V2, RFC
    broken = {
        "RFC missing": mutate_re(texts, r, r".*", "", count=1),
        "Variant 1 edited": mutate(texts, V1, "Стратегию выбирают полярность, дистанция, масса", "Правило выбора стиля"),
        "Variant 1 deleted": mutate_re(texts, V1, r".*", "", count=1),
        "source is another issue": mutate(texts, v, 'source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/689"', 'source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/685"'),
        "relative link": mutate(texts, a, "](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/", "](../"),
        "broken anchor": mutate(texts, r, "#нумерация-документ-и-rfc-v03", "#нумерация"),
        "draft comment left": mutate(texts, r, "## 4. Вывод", "<!-- TODO -->\n## 4. Вывод"),
        "mass justifies style in the catalog": mutate(texts, v, "- **Условие применения:** Если готовим любой первый контакт", "- **Условие применения:** Если масса аудитории высокая и готовим любой первый контакт"),
        "polarity in a visual marker": mutate(texts, v, "- **Визуальный маркер:** Графит и белый", "- **Визуальный маркер:** При полярности «?» графит и белый"),
        "status label in the catalog": mutate(texts, v, "- **Суть:** Образ соответствует роли", "- **Суть:** Образ со статусом VERIFIED соответствует роли"),
        "GRA in the catalog": mutate(texts, v, "#### 10. Деталь дела", "#### 10. Деталь дела по GRA"),
        "narrative bridge in the catalog": mutate(texts, v, "- **Суть:** Образ соответствует роли", "- **Суть:** Потому что образ соответствует роли"),
        "card field lost": mutate_re(texts, v, r"(#### 3\. [^\n]+\n\n(?:- [^\n]+\n){1})- \*\*Суть:\*\* [^\n]+\n", r"\1"),
        "condition not a direct rule": mutate(texts, v, "- **Условие применения:** Если готовим", "- **Условие применения:** Когда готовим"),
        "condition without «применяем»": mutate_re(texts, v, r"(#### 4\. [^\n]+\n\n(?:- [^\n]+\n){2}- \*\*Условие применения:\*\* [^\n]*?) применяем ", r"\1 берём "),
        "card removed": mutate_re(texts, v, r"^#### 21\. .*?(?=^## )", ""),
        "cards out of order": mutate(texts, v, "#### 8. ", "#### 9. "),
        "Variant 2 deviation not in format": mutate(texts, v, "эффективнее решает задачу [отделить", "лучше [отделить"),
        "lecturer applies GRA to himself": mutate(texts, v, "На Дне 4 лектор не применяет GRA к себе для выбора стиля", "На Дне 4 лектор применяет GRA к себе для выбора стиля"),
        "Variant 2 gate item open": mutate(texts, v, "- [x] Только перечень", "- [ ] Только перечень"),
        "analysis quote not in Variant 1": mutate(texts, a, "«Стратегию выбирают полярность, дистанция, масса» | Центральный", "«Стратегию выбирают имидж-технологии» | Центральный"),
        "analysis line number wrong": mutate(texts, a, "| строка 394, слайд 11 |", "| строка 395, слайд 11 |"),
        "analysis quotes cut": mutate_re(texts, a, r"^### 2\.2\. .*?(?=^### 2\.3\.)", ""),
        "analysis section lost": mutate(texts, a, "## 3. Корневая причина", "## 3. Причины"),
        "proverb not applied": mutate(texts, a, "| Расшибленный лоб |", "| Итог |"),
        "dialog deviation lost": mutate(texts, a, "Я предлагаю скорректировать [требование «единственный источник", "Предлагаю поменять [требование «единственный источник"),
        "dialog claimed deleted": mutate(texts, a, "Файл диалога: неприменимо", "Файл диалога удалён"),
        "analysis gate item lost": mutate_re(texts, a, r"^- \[x\] Все 3 файла[^\n]*\n", ""),
        "phrase reworded": mutate(texts, r, "GRA не диктует цвет вашего галстука.", "GRA не выбирает галстук."),
        "second phrase": mutate(texts, r, "### Время", "> Коллеги, важное разграничение. Ещё одна фраза.\n\n### Время"),
        "phrase moved off slide 17": mutate(texts, r, SLIDE_17, "**Слайд 19 колоды «Правило выбора стиля»**"),
        "slide 19 title kept": mutate(texts, r, "| **Правило выбора стиля** |", "| Стратегию выбирают полярность, дистанция, масса |"),
        "P0 grown to three swaps": mutate(texts, r, "\n\nПервая фраза вводного абзаца", "\n| P0-3 | 19 | Эпиграф | «Право на контраст зарабатывается вкладом» | «Контраст по ситуации» |\n\nПервая фраза вводного абзаца"),
        "swap changes nothing": mutate(texts, r, "| 02 · ВОПРОС | 02 · ДАННЫЕ |", "| 02 · ВОПРОС | 02 · ВОПРОС |"),
        "P1 deviation not in format": mutate(texts, r, "Я предлагаю скорректировать [Ограничение «указать 1–2 слова", "Можно расширить [Ограничение «указать 1–2 слова"),
        "diagnosis lost": mutate(texts, r, "Менять структуру колоды — порядок и число слайдов, вёрстку, изображения — нельзя", "Колоду можно перегенерировать"),
        "deck permalink lost": mutate(texts, r, DECK, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/688", count=1),
        "conclusion lost": mutate(texts, r, "Новой генерации нет", "Нужна новая генерация"),
        "RFC gate item open": mutate(texts, r, "- [x] Диагноз", "- [ ] Диагноз"),
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
    print(f"PASS: Variant 1 is unchanged (blob {V1_BLOB}); the three new files cite issue #689, use full URLs and their repository links resolve")
    print(f"PASS: the analysis has the summary, examples, root cause and the proverb applied to the agent; every quote of Variant 1 matches its line; the missing dialog is a deviation; gate has {ANALYSIS_GATE} confirmed items")
    print(f"PASS: Variant 2 lists {CARDS} cards of Название, Суть, Условие применения «Если …, применяем …», Визуальный маркер; no mass, distance, polarity, statuses, GRA or «потому что → поэтому» in the catalog; the lecturer does not apply GRA to himself; gate has {V2_GATE} confirmed items")
    print(f"PASS: the RFC keeps the deck structure, gives ONE verbatim phrase on deck slide 17, swaps the slide 19 title for «Правило выбора стиля» in {P0_ROWS} P0 swaps, files P1 as a deviation, links the deck permalink; gate has {RFC_GATE} confirmed items")
    if args.self_test:
        print(f"PASS: {fixtures} broken fixtures rejected")


if __name__ == "__main__":
    main()
