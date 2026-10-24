#!/usr/bin/env python3
"""Gate check of the course handout file of issue #700: one file, schedule, unified template blocks, Day 4 constraints, footprint audit."""
import argparse
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
HANDOUT = DOMAIN / "2026-10-24-handout-materials-master-prompt-registry-days-1-4.md"
DECKS = {
    1: DOMAIN / "2026-10-14-day1-presentation-gamma.md",
    2: DOMAIN / "2026-10-30-day2-presentation-gamma.md",
    3: DOMAIN / "2026-11-02-day3-presentation-gamma.md",
    4: DOMAIN / "2026-11-03-day4-presentation-gamma-v5.md",
}
FILES = (HANDOUT, *DECKS.values())

spec = importlib.util.spec_from_file_location("check699", DOMAIN / "exp/day4-image-prompts-v5-699/check-day4-image-prompts-699.py")
check699 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check699)
HOUSES, BANNED, GENERIC = check699.HOUSES, check699.BANNED, check699.GENERIC

REPO_URL = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab"
TITLE = "# Раздаточные материалы курса · Master Prompt Registry · Дни 1–4"
FRONTMATTER = ("status", "version", "updated", "temperature", "source", "scope", "method", "related_issues")
TASKS = {"1.1": 1, "2.1": 2, "2.2": 2, "3.1": 3, "4.1": 4, "4.2": 4}
LLMS = ("Claude", "GPT", "Gemini", "GigaChat")
GENERATORS = ("Midjourney", "Nano Banana", "DALL-E")
HEADERS = ("# ROLE", "# CONTEXT", "# INPUT DATA", "# TASK", "# OUTPUT FORMAT")
COMMENT = ("Почему шаблон работает", "Типичные ошибки новичков", "Как адаптировать INPUT DATA")
SCHEDULE_SLIDES = {1: (24, 25, 33), 2: (18, 19, 27), 3: (23, 24, 25, 32, 33), 4: (6, 12, 18, 23, 26, 27)}
VARIABLES = ("[CITY]", "[DESIGNER_DNA]", "[BASE_COLOR_1]", "[BASE_COLOR_2]", "[ART_OBJECT_TYPE]")
INSTRUCTION = "Выберите дизайнера из списка 26 мировых домов (Balenciaga, Dior...) и определите его ДНК для заполнения переменной."
CONSTRAINTS = ("Vertical Banner ~1:2.4", "High-key Light", "No Office/Business Suit", "Gold Accent Mandatory")
IMAGE_FRAME = ("about 1 to 2.4", "no panels and no borders", "high-key", "Gold #B89B5E", "worn on the person", "Art Deco")
PLATFORMS = ("VK", "LinkedIn", "Facebook", "Instagram", "Telegram channels", "Habr", "VC.ru")
LIVELIB = "https://www.livelib.ru/book/1000245012-dresskod-dlya-delovyh-muzhchin-audiokniga-cd-ivan-gulienko"
DEVIATION = re.compile(r"^- Я предлагаю скорректировать .+, потому что вариант .+ лучше подходит для автономного использования слушателем", re.M)


def slug(heading):
    """GitHub anchor of a Markdown heading: lower case, punctuation and emoji dropped, spaces to hyphens."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def anchors(text):
    seen, result = {}, set()
    for heading in re.findall(r"^#{1,6} (.+)$", re.sub(r"^```.*?^```", "", text, flags=re.M | re.S), re.M):
        base = slug(heading)
        result.add(base if base not in seen else f"{base}-{seen[base]}")
        seen[base] = seen.get(base, 0) + 1
    return result


def deck_topic(text):
    match = re.search(r"^- Шапка: Введение в репутационный инжиниринг · (.+)$", text, re.M)
    return match.group(1).strip() if match else None


def section(text, start, end_pattern):
    index = text.find(start)
    if index < 0:
        return None
    rest = text[index + len(start):]
    match = re.search(end_pattern, rest, re.M)
    return rest[:match.start()] if match else rest


def first_code(block):
    match = re.search(r"^```text\n(.*?)^```", block, re.M | re.S)
    return match.group(1) if match else None


def check_template(task, day, topic, prompt):
    errors, where = [], f"task {task} prompt"
    positions = [prompt.find(f"\n{header}\n") if i else (0 if prompt.startswith(f"{header}\n") else -1) for i, header in enumerate(HEADERS)]
    for header, position in zip(HEADERS, positions):
        if position < 0:
            errors.append(f"{where}: header «{header}» missing")
    if all(p >= 0 for p in positions) and positions != sorted(positions):
        errors.append(f"{where}: headers are not in the order {' → '.join(HEADERS)}")
    if not re.search(r"^# ROLE\nYou are a Senior \S", prompt, re.M):
        errors.append(f"{where}: # ROLE does not start with «You are a Senior …»")
    context = section(prompt, "# CONTEXT\n", r"^# ") or ""
    for line in ("- Course: Introduction to Reputation Engineering.", f"- Day: {day}. Topic: {topic}.", "- Methodology: ", "- Constraints:"):
        if line not in context:
            errors.append(f"{where}: CONTEXT line «{line.strip()}» missing")
    if not re.search(r"\[[^\]]+\]", section(prompt, "# INPUT DATA\n", r"^# ") or ""):
        errors.append(f"{where}: INPUT DATA has no [FIELD] to replace")
    return errors


def validate(texts):
    errors = []
    text = texts[HANDOUT]
    if not text:
        return [f"{HANDOUT.relative_to(ROOT)} is missing"]
    frontmatter = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not frontmatter:
        errors.append("frontmatter missing")
    else:
        keys = re.findall(r"^([a-z_]+):", frontmatter.group(1), re.M)
        for key in FRONTMATTER:
            if key not in keys:
                errors.append(f"frontmatter: key «{key}» missing")
        if "ai-generated" in frontmatter.group(1):
            errors.append("frontmatter: «ai-generated» is not allowed")
        if f'source: "{REPO_URL}/issues/700"' not in frontmatter.group(1):
            errors.append("frontmatter: source is not issue #700")
    if f"\n{TITLE}\n" not in text:
        errors.append(f"title is not «{TITLE}»: the name must say these are handout materials")
    if "## Как пользоваться" not in text:
        errors.append("section «## Как пользоваться» missing")

    schedule = section(text, "## Когда что раздавать\n", r"^## ")
    if schedule is None:
        errors.append("section «## Когда что раздавать» missing")
    else:
        rows = [row for row in schedule.splitlines() if re.match(r"\| \d \|", row)]
        for day, slides in SCHEDULE_SLIDES.items():
            day_rows = " ".join(row for row in rows if row.startswith(f"| {day} |"))
            if not day_rows:
                errors.append(f"schedule: no row for Day {day}")
            for slide in slides:
                if not re.search(rf"[Сс]лайд\w*[^|]*?\b{slide}\b", day_rows):
                    errors.append(f"schedule: Day {day} has no row for slide {slide}")

    days = re.findall(r"^## День (\d)\. Тема: (.+)$", text, re.M)
    if [int(day) for day, _ in days] != [1, 2, 3, 4]:
        errors.append(f"day headings are {[day for day, _ in days]}, expected 1, 2, 3, 4 in order")
    topics = {int(day): topic.strip() for day, topic in days}
    for day, deck in DECKS.items():
        expected = deck_topic(texts[deck])
        if expected is None:
            errors.append(f"{deck.relative_to(ROOT)}: no «Шапка» line with the day topic")
        elif topics.get(day) != expected:
            errors.append(f"Day {day} topic «{topics.get(day)}» differs from the deck header «{expected}»")

    tasks = re.findall(r"^### Задача (\d\.\d): .+$", text, re.M)
    if tasks != list(TASKS):
        errors.append(f"tasks are {tasks}, expected {list(TASKS)}")
    for task, day in TASKS.items():
        block = section(text, f"### Задача {task}: ", r"^### Задача |^## ")
        if block is None:
            continue
        goal = re.search(r"^\*\*Цель:\*\* (.+)$", block, re.M)
        if not goal or not goal.group(1).startswith("Сгенерировать "):
            errors.append(f"task {task}: «**Цель:** Сгенерировать …» missing")
        tool = re.search(r"^\*\*Инструмент:\*\* (.+)$", block, re.M)
        names = GENERATORS + LLMS if task == "4.2" else LLMS
        if not tool:
            errors.append(f"task {task}: «**Инструмент:**» missing")
        else:
            for name in names:
                if name not in tool.group(1):
                    errors.append(f"task {task}: tool line does not name {name}")
        for heading in ("#### 📋 Шаблон промпта (Copy-Paste)", "#### 💡 Пример использования", "#### 🔁 Разбор ошибок", "#### ⚠️ Комментарий для лектора/слушателя"):
            if heading not in block:
                errors.append(f"task {task}: «{heading}» missing")
        example = section(block, "#### 💡 Пример использования", r"^#### ") or ""
        if "**Вход:**" not in example or "**Ожидаемый выход" not in example:
            errors.append(f"task {task}: example has no «Вход» and «Ожидаемый выход»")
        comment = section(block, "#### ⚠️ Комментарий для лектора/слушателя", r"^#### |^---") or ""
        for item in COMMENT:
            if f"**{item}" not in comment:
                errors.append(f"task {task}: comment item «{item}» missing")
        prompt = first_code(section(block, "#### 📋 Шаблон промпта (Copy-Paste)", r"^#### ") or "")
        if prompt is None:
            errors.append(f"task {task}: no ```text block after «📋 Шаблон промпта»")
        elif task != "4.2":
            errors += check_template(task, day, topics.get(day), prompt)
        if task == "2.2" and prompt:
            for platform in PLATFORMS:
                if platform not in prompt:
                    errors.append(f"task 2.2 prompt: platform {platform} missing from the fan-out search")
            if "Не ограничивайся академическими базами" not in prompt or "Не найдено легально — Gap" not in prompt:
                errors.append("task 2.2 prompt: rules «not only academic bases» and «Gap» missing")
            if "LiveLib" not in prompt or "аудиокнига" not in prompt:
                errors.append("task 2.2 prompt: book catalogs in all formats (LiveLib, аудиокнига) missing")
            if LIVELIB not in block:
                errors.append("task 2.2 example: the LiveLib book card missed by the Day 1 prompt is not shown")
        if task == "4.1" and prompt:
            for word in ("ЦВЕТ", "ФОРМА", "СТИЛЬ", "АКСЕССУАРЫ", "ГАРМОНИЯ", "ЭКЛЕКТИКА", "Hypothesis Map (Harmony vs Eclecticism)"):
                if word not in prompt:
                    errors.append(f"task 4.1 prompt: «{word}» missing")
        if task == "4.2":
            errors += check_image(block, prompt)
    for day in (1, 2, 3, 4):
        if not re.search(rf"^#### 📝 Домашнее задание Дня {day}", text, re.M):
            errors.append(f"homework of Day {day} missing")

    for target in re.findall(r"\]\((#[^)]+)\)", text):
        if target[1:] not in anchors(text):
            errors.append(f"anchor link {target} leads to no heading")
    for target in re.findall(r"\]\(([^)#]+)\)", text):
        if not target.startswith("https://"):
            errors.append(f"link {target} is not absolute: students have no access to the repository tree")
        elif target.startswith(f"{REPO_URL}/blob/main/"):
            if not (ROOT / target.removeprefix(f"{REPO_URL}/blob/main/")).is_file():
                errors.append(f"link {target} leads to no file")
    day4 = sorted(DOMAIN.glob("2026-11-03-day4-presentation-gamma-v*.md"), key=lambda path: int(path.stem.rsplit("-v", 1)[1]))
    if f"{REPO_URL}/blob/main/research/reputation-technologies/{day4[-1].name}" not in text:
        errors.append(f"latest Day 4 deck {day4[-1].name} is not linked")
    for stale in re.findall(r"2026-11-03-day4-presentation-gamma(?:-v\d)?\.md", text):
        if stale != day4[-1].name:
            errors.append(f"link to a stale Day 4 deck {stale}")

    deviations = section(text, "## Отклонения от постановки\n", r"^## ")
    if deviations is None or not DEVIATION.search(deviations):
        errors.append("section «## Отклонения от постановки» with the required wording missing")
    elif len(re.findall(r"^- ", deviations, re.M)) != len(DEVIATION.findall(deviations)):
        errors.append("deviation not in the form «Я предлагаю скорректировать …, потому что вариант … лучше подходит …»")
    gaps = section(text, "## Gaps\n", r"^## ")
    if gaps is None or "`Gap`" not in gaps or "`2.txt`" not in gaps:
        errors.append("section «## Gaps» with the unavailable 2.txt missing")
    return errors


def check_image(block, prompt):
    errors = []
    if INSTRUCTION not in block:
        errors.append("task 4.2: instruction «Выберите дизайнера из списка 26 мировых домов …» missing")
    if prompt is None:
        return errors
    for variable in VARIABLES:
        if variable not in prompt:
            errors.append(f"task 4.2 prompt: variable {variable} missing")
    for phrase in IMAGE_FRAME:
        if phrase not in prompt:
            errors.append(f"task 4.2 prompt: frame element «{phrase}» missing")
    for name, pattern in (("banned", BANNED["EN"]), ("generic", GENERIC["EN"])):
        found = sorted({match.group(0).lower() for match in re.finditer(pattern, prompt, re.I)})
        if found:
            errors.append(f"task 4.2 prompt: {name} words {found}")
    if re.search(r"[А-Яа-яЁё]", prompt):
        errors.append("task 4.2 prompt: Cyrillic in the English generator prompt")
    if len(prompt) > 4000:
        errors.append(f"task 4.2 prompt: {len(prompt)} characters, more than the DALL-E 3 limit of 4000")
    for constraint in CONSTRAINTS:
        if not re.search(rf"^- \[ \] \*\*{re.escape(constraint)}\*\*", block, re.M):
            errors.append(f"task 4.2: hard constraint «{constraint}» missing from the checklist")
    if "--ar 5:12" not in block:
        errors.append("task 4.2: Midjourney ratio --ar 5:12 missing")
    rows = {match.group(2).strip(): match.group(3) for match in re.finditer(r"^\| (\d+) \| ([^|·]+?) · [^|]+\| ([^|]+) \|$", block, re.M)}
    for house, (_, markers, _) in HOUSES.items():
        if house not in rows:
            errors.append(f"task 4.2: house {house} missing from the 26-house table")
            continue
        found = {match.group(0).lower() for match in re.finditer(markers, rows[house])}
        if len(found) < 3:
            errors.append(f"task 4.2: house {house} has {len(found)} DNA markers of #699, at least 3 needed")
        for name, pattern in (("banned", BANNED["EN"]), ("generic", GENERIC["EN"])):
            if re.search(pattern, rows[house], re.I):
                errors.append(f"task 4.2: house {house} DNA has {name} words")
    if len(rows) != len(HOUSES):
        errors.append(f"task 4.2: house table has {len(rows)} rows, expected {len(HOUSES)}")
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
    h = HANDOUT
    broken = {
        "handout missing": mutate(texts, h, texts[h], ""),
        "ai-generated in frontmatter": mutate(texts, h, "status: draft", "status: draft\nai-generated: true"),
        "frontmatter without method": mutate_re(texts, h, r"^method: [^\n]+\n", ""),
        "title without handout": mutate(texts, h, "# Раздаточные материалы курса ·", "# Курс ·"),
        "no schedule": mutate(texts, h, "## Когда что раздавать", "## Расписание"),
        "schedule without Day 2 homework slide": mutate(texts, h, "| 2 | Слайд 27, домашнее задание |", "| 2 | Домашнее задание |"),
        "schedule without Day 4": mutate_re(texts, h, r"^\| 4 \|.*?\n(?=\n)", ""),
        "day topic differs from deck": mutate(texts, h, "## День 2. Тема: Мониторинг ресурсов, работа с данными", "## День 2. Тема: Мониторинг"),
        "Day 3 missing": mutate(texts, h, "## День 3. Тема:", "## Третий день. Тема:"),
        "task 2.2 missing": mutate(texts, h, "### Задача 2.2: ", "### Аудит: "),
        "goal not generate": mutate(texts, h, "**Цель:** Сгенерировать черновик карты", "**Цель:** Черновик карты"),
        "tool without GigaChat": mutate(texts, h, "(Claude, GPT, Gemini, GigaChat). Лучше", "(Claude, GPT, Gemini). Лучше"),
        "4.2 tool without Nano Banana": mutate(texts, h, "**Инструмент:** Midjourney, Nano Banana (Gemini), DALL-E 3.", "**Инструмент:** Midjourney, DALL-E 3."),
        "no prompt block": mutate(texts, h, "#### 📋 Шаблон промпта (Copy-Paste)\n\n```text\n# ROLE\nYou are a Senior OSINT", "#### 📋 Шаблон промпта (Copy-Paste)\n\n```\n# ROLE\nYou are a Senior OSINT"),
        "OUTPUT FORMAT missing": mutate(texts, h, "# OUTPUT FORMAT\n1. Первая строка", "ВЫХОД\n1. Первая строка"),
        "TASK header renamed": mutate(texts, h, "# TASK\n1. Найди открытые сведения", "# TASKS\n1. Найди открытые сведения"),
        "headers out of order": mutate_re(texts, h, r"(# CONTEXT\n.*?)(# INPUT DATA\n.*?)(# TASK\n1\. Найди)", r"\2\1\3"),
        "role not senior": mutate(texts, h, "You are a Senior Partnership Strategist", "You are a Partnership Strategist"),
        "context day wrong": mutate(texts, h, "- Day: 3. Topic:", "- Day: 2. Topic:"),
        "context without methodology": mutate(texts, h, "- Methodology: GRA", "- Method: GRA"),
        "input without fields": mutate_re(texts, h, r"(# INPUT DATA\nКого проверяем: )\[[^\n]+\n(Варианты написания: )\[[^\n]+\n(Что уже известно: )\[[^\n]+\n(Зачем проверяем: )\[[^\n]+", r"\1—\n\2—\n\3—\n\4—"),
        "no example input": mutate(texts, h, "**Вход:** в INPUT DATA вставлены [бриф М2.1]", "Вставлены [бриф М2.1]"),
        "no error review": mutate(texts, h, "#### 🔁 Разбор ошибок 4.1", "#### Ошибки 4.1"),
        "comment without adaptation": mutate(texts, h, "- **Как адаптировать INPUT DATA.** Вставьте свою задачу", "- Вставьте свою задачу"),
        "no Day 3 homework": mutate(texts, h, "#### 📝 Домашнее задание Дня 3", "#### Задание"),
        "footprint without Habr": mutate(texts, h, "   - медиа: Habr, VC.ru,", "   - медиа: VC.ru,"),
        "footprint without Gap": mutate(texts, h, "Не найдено легально — Gap:", "Не найдено легально — пометь:"),
        "footprint only academic": mutate(texts, h, "  1. Не ограничивайся академическими базами: проверь соцсети, медиа и книжные каталоги.\n", ""),
        "LiveLib example missing": mutate(texts, h, LIVELIB, "https://www.livelib.ru/", 2),
        "4.1 without eclecticism": mutate(texts, h, "КОНТРАСТ / ЭКЛЕКТИКА", "КОНТРАСТ"),
        "image instruction changed": mutate(texts, h, INSTRUCTION, "Выберите дизайнера из списка домов."),
        "variable missing": mutate(texts, h, "the lower garment in [BASE_COLOR_2]", "the lower garment in forest green"),
        "business suit in image prompt": mutate(texts, h, "no text and no lettering. Always", "no text, no business suit. Always"),
        "dark scene in image prompt": mutate(texts, h, "clean even light with luminous fill", "dark moody light with deep shadows"),
        "gold dropped": mutate(texts, h, "Gold #B89B5E jewellery and embroidery worn on the person", "Jewellery"),
        "ratio dropped": mutate(texts, h, "about 1 to 2.4, ", ""),
        "constraint missing": mutate(texts, h, "- [ ] **Gold Accent Mandatory**", "- [ ] **Gold accent**"),
        "house missing": mutate_re(texts, h, r"^\| 26 \| Coperni ·.*?\n", ""),
        "house DNA too thin": mutate(texts, h, "| intrecciato weave, quiet luxury, Knot clutch, Andiamo bag |", "| woven leather |"),
        "house DNA with uniform": mutate(texts, h, "collegiate tailoring |", "school uniform |"),
        "broken anchor": mutate(texts, h, "(#материал-м32-20-визиток-с-выставки)", "(#материал-м32-визитки)"),
        "relative link": mutate(texts, h, "[конструкторе промптов Дня 4 v5](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-11-03-day4-image-prompts-v5-couturier-constructor.md)", "[конструкторе промптов Дня 4 v5](2026-11-03-day4-image-prompts-v5-couturier-constructor.md)"),
        "stale Day 4 deck": mutate(texts, h, "2026-11-03-day4-presentation-gamma-v5.md)", "2026-11-03-day4-presentation-gamma-v4.md)"),
        "dead repo link": mutate(texts, h, "2026-10-12-rfc-days-1-3-logic.md", "2026-10-12-rfc-days-1-4-logic.md"),
        "deviation free wording": mutate(texts, h, "- Я предлагаю скорректировать набор задач Дня 2, потому что", "- Добавлен шаблон 2.2, потому что"),
        "gaps without 2.txt": mutate(texts, h, "файл `2.txt`", "файл диалога"),
        "deck header lost": mutate(texts, DECKS[4], "- Шапка: Введение в репутационный инжиниринг ·", "- Шапка:", -1),
    }
    failed = [name for name, mutated in broken.items() if mutated == texts or not validate(mutated)]
    return failed, len(broken)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="also check that broken fixtures are rejected")
    args = parser.parse_args()
    texts = {path: path.read_text(encoding="utf-8") if path.is_file() else "" for path in FILES}
    errors = validate(texts)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        sys.exit(1)
    print(f"PASS: {HANDOUT.relative_to(ROOT)} — {len(TASKS)} templates in one file, schedule of 4 days, unified blocks, links to the latest decks")
    print(f"PASS: image template — {len(VARIABLES)} variables, {len(CONSTRAINTS)} hard constraints, {len(HOUSES)} houses with DNA markers of #699, no banned words")
    print(f"PASS: footprint audit — {len(PLATFORMS)} platforms, Gap rule, LiveLib book card")
    if args.self_test:
        failed, total = self_test(texts)
        for name in failed:
            print(f"FAIL: broken fixture not rejected: {name}")
        if failed:
            sys.exit(1)
        print(f"PASS: {total} broken fixtures rejected")


if __name__ == "__main__":
    main()
