#!/usr/bin/env python3
"""Check the RFC contract of issues #667 and #669: appeal first, four logical day skeletons, 90-minute budget, partnership tone."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
NEW_RFC = DOMAIN / "2026-10-12-rfc-days-1-3-logic.md"
OLD_RFC = DOMAIN / "gra-research-program/presentation-rfc/2026-10-12-rfc-presentation-ux-days-1-3.md"
FOLDER_README = DOMAIN / "gra-research-program/presentation-rfc/README.md"
TECHNOGRAD = "https://technograd.moscow/event_page_new?669#programm_event"
REPO_BLOB = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
APPENDIX = "## Приложение"
PRINCIPLE = "Просто в эфире, глубоко в ссылках"
APPEAL = "АППЕЛЯЦИЯ: Требование"
FIELDS = ("- **Когнитивный сдвиг:**", "- **Нарративная связь:**", "- **Глубже — в ссылках:**", "- **Формат и время:**")
IMAGE_MARKERS = re.compile(r"Qwen|Kandinsky|Midjourney|DALL|Stable Diffusion|промпт[а-я]* (?:для )?изображени|image prompt", re.I)
LOCAL_PROGRAM = re.compile(r"default\.txt|121026\.txt|user-attachments")
# #669 DoD: no investigation rhetoric outside verbatim quotes (blockquotes).
TRIGGERS = re.compile(r"безопасн|разоблач|угроз|расследова|ловл[яиюе]", re.I)
HARM = re.compile(r"вред", re.I)
DAY = re.compile(r"^## День ([1-4])\. .+$", re.M)
PART = re.compile(r"^### (Вход|Основная часть|Финал)[^\n]*\(слайды (\d+)–(\d+)\)$", re.M)
SLIDE = re.compile(r"^#### Слайд (\d+)\. «.+»$", re.M)
MINUTES = re.compile(r"· (\d+(?:,\d)?) мин$", re.M)
RESERVE = re.compile(r"Резерв — (\d+(?:,\d)?) минут")
LINK = re.compile(r"\]\((https://[^)\s]+)\)")
DAY3_MENTION = re.compile(r"Д(?:ень|ня|ню|не|нём|нем) 3")

FOUNDER_QUOTES = (
    'Между "посредник врет" и "давайте измерим связь по трем осям" - такое ощущение, что мы пытаемся поймать исследуемый объект на противоречиях и зафиксировать это. НО посыл курса другой - давайте МИРНО посмотрим на то, какую информацию мы можем собрать (в том числе с использованием ИИ) и проанализировать (с использованием ИИ). Для увеличения вероятности детерминированного результата нам надо задать модель, которой и является исследуемый GRA. Мы не пытаемся что-то доказать. Мы не пытаемся заниматься экономической безопасностью. Мы не пытаемся планировать действия в жесткой конкурентной борьбе. Пока, в этой итерации/курсе. На первом этапе мы смотрим, что можно узнать и как это интерпретировать и записать для накопления статистики и дальнейшего применения в анализе. Пока на простом уровне',
    'Поэтому целесообразно упростить "подачу курса", сократить количество убеждений и доказательств (но дать много ссылок в тексте на ресурсы, кейсы, промпты, которые они могут изучить отдельно от лекции). И рассматривать курс именно с позитивной позиции, что мы подбираем "партнеров" и на 4-й день планируем определенную грань - как визуально выстроить коммуникацию. Нет цели разработать идеальные всесторонние стратегии. Давайте проще и понятнее ЦА на этом первом этапе (первом прогоне курса)',
    'Вред - предлагаю не рассматривать (см. выше), предлагаю рассматривать как: из полученной (собранной) информации выделить "полезное" для подготовки встречи (4 день)',
    'Про цифры - они сейчас не критичны. Количество исков за длительный период существования бизнеса говорит о том, что он работает. Далее надо смотреть от кого (например налоговые или физики или юрики) - но это уже углубленный экономической безопасности анализ, вне рамок нашей задачи. Потому можно смотреть что они есть и от кого, коротко суммировать результаты и продолжает или нет действовать компания ... пока на очень простом информативном уровне',
)


def number(value):
    return float(value.replace(",", "."))


def frontmatter(text):
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return dict(line.split(": ", 1) for line in match[1].splitlines()) if match else {}


def plain(text):
    """Text without blockquotes: verbatim quotes of the founder and of the program may keep their own words."""
    return "\n".join(line for line in text.splitlines() if not line.startswith(">"))


def anchors(path):
    """GitHub-style heading anchors of a Markdown file."""
    seen, result = {}, set()
    text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
    for match in re.finditer(r"^#{1,6} (.+?)\s*#*$", text, re.M):
        title = re.sub(r"`|\*\*|\[([^\]]*)\]\([^)]*\)", lambda m: m[1] or "", match[1])
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        result.add(slug if count == 0 else f"{slug}-{count}")
    return result


def broken_links(text):
    cache = {}
    for url in sorted(set(LINK.findall(text))):
        if not url.startswith(REPO_BLOB):
            continue
        path, _, anchor = url[len(REPO_BLOB):].partition("#")
        target = ROOT / path
        if not target.is_file():
            yield f"{url}: file not found"
        elif anchor and target.suffix == ".md":
            if target not in cache:
                cache[target] = anchors(target)
            if anchor not in cache[target]:
                yield f"{url}: anchor not found"


def day_sections(text):
    matches = list(DAY.finditer(text))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        tail = re.search(r"^## (?!День)", text[match.end():end], re.M)
        yield match[1], text[match.start():match.end() + tail.start() if tail else end]


def field(chunk, name):
    match = re.search(re.escape(name) + r"[^\n]*(?:\n  [^\n]*)*", chunk)
    return match[0] if match else ""


def validate(text, label):
    errors = []
    h2 = re.findall(r"^## (.+)$", text, re.M)
    if not h2 or h2[0] != "КРИТИЧЕСКАЯ АППЕЛЯЦИЯ":
        errors.append(f"{label}: first section must be «КРИТИЧЕСКАЯ АППЕЛЯЦИЯ»")
    elif APPEAL not in text.split("\n## ", 2)[1]:
        errors.append(f"{label}: appeal section has no «{APPEAL} …» statement")
    if not any(title.startswith("Executive Summary") for title in h2):
        errors.append(f"{label}: Executive Summary missing")
    main = text.split(APPENDIX, 1)[0]
    if re.search(r"^\|", main, re.M):
        errors.append(f"{label}: table in the main structure (allowed only after «{APPENDIX}»)")
    if LOCAL_PROGRAM.search(text):
        errors.append(f"{label}: mentions a local course-program file")
    if TECHNOGRAD not in text:
        errors.append(f"{label}: Technograd program link missing")
    if PRINCIPLE not in text:
        errors.append(f"{label}: principle «{PRINCIPLE}» not stated")
    for quote in FOUNDER_QUOTES:
        if f"> «{quote}»" not in text:
            errors.append(f"{label}: founder quote missing or shortened: «{quote[:40]}…»")
    for match in TRIGGERS.finditer(plain(text)):
        errors.append(f"{label}: trigger word outside a verbatim quote: «{match[0]}»")
    errors += [f"{label}: broken link {problem}" for problem in broken_links(text)]
    days = dict(day_sections(text))
    if sorted(days) != ["1", "2", "3", "4"]:
        errors.append(f"{label}: expected sections for Days 1, 2, 3, 4")
    for day, body in days.items():
        where = f"{label}/День {day}"
        if IMAGE_MARKERS.search(body):
            errors.append(f"{where}: image prompt in slide structure")
        if HARM.search(plain(body)):
            errors.append(f"{where}: «вред» outside a verbatim program quote")
        slides = list(SLIDE.finditer(body))
        numbers = [int(m[1]) for m in slides]
        if numbers != list(range(1, len(numbers) + 1)):
            errors.append(f"{where}: slide numbers must run 1..N")
        if not 22 <= len(numbers) <= 26:
            errors.append(f"{where}: {len(numbers)} slides, expected about 24 (22–26)")
        parts = {m[1]: int(m[3]) - int(m[2]) + 1 for m in PART.finditer(body)}
        main_count = sum(int(m[3]) - int(m[2]) + 1 for m in PART.finditer(body) if m[1] == "Основная часть")
        if parts.get("Вход") != 5 or not 15 <= main_count <= 20 or not 1 <= parts.get("Финал", 0) <= 4:
            errors.append(f"{where}: expected 5 intro + 15–20 main + 1–4 final slides")
        if sum(parts.values()) - parts.get("Основная часть", 0) + main_count != len(numbers):
            errors.append(f"{where}: part ranges do not cover all slides")
        total = 0.0
        for i, slide in enumerate(slides):
            chunk = body[slide.end():slides[i + 1].start() if i + 1 < len(slides) else len(body)]
            for name in FIELDS:
                if name not in chunk:
                    errors.append(f"{where}/слайд {slide[1]}: missing {name}")
            if not LINK.search(field(chunk, FIELDS[2])):
                errors.append(f"{where}/слайд {slide[1]}: no self-study link")
            if day == "4" and not DAY3_MENTION.search(field(chunk, FIELDS[1])):
                errors.append(f"{where}/слайд {slide[1]}: narrative link does not name the Day 3 result")
            minutes = MINUTES.search(chunk)
            total += number(minutes[1]) if minutes else 0
        reserve = RESERVE.search(body)
        if not reserve or abs(total + number(reserve[1]) - 90) > 0.01:
            errors.append(f"{where}: slide minutes {total:g} + reserve do not sum to 90")
        votes, trials = len(re.findall(r"«🗳", body)), len(re.findall(r"«🤖", body))
        if votes > 2:
            errors.append(f"{where}: {votes} chat votes, at most 2 allowed")
        if trials != 1:
            errors.append(f"{where}: {trials} prompt trials, exactly 1 expected")
    filter_slides = [m[0] for m in SLIDE.finditer(days.get("3", "")) if "фильтр" in m[0].lower()]
    if not any("полезност" in title for title in filter_slides):
        errors.append(f"{label}/День 3: filter slide has no «полезность для встречи»")
    if not re.search(r"маркер активности", plain(days.get("1", ""))):
        errors.append(f"{label}/День 1: case 1 lawsuits are not described as an activity marker")
    return errors


def self_test(text):
    broken = {
        "appeal moved": text.replace("## КРИТИЧЕСКАЯ АППЕЛЯЦИЯ", "## Аппеляция", 1),
        "table in main": text.replace("## Как читать", "| a | b |\n\n## Как читать", 1),
        "image prompt": text.replace("- **Когнитивный сдвиг:** ", "- **Когнитивный сдвиг:** Промпт Qwen. ", 1),
        "field missing": text.replace("- **Нарративная связь:**", "- Связь:", 1),
        "link field missing": text.replace("- **Глубже — в ссылках:**", "- Ссылки:", 1),
        "broken anchor": text.replace("#главная-мысль-дня", "#нет-такого-раздела", 1),
        "local program": text.replace("## Источники", "## Источники\n\nСм. default.txt.", 1),
        "budget broken": text.replace("· 1 мин", "· 4 мин", 1),
        "slide removed": re.sub(r"#### Слайд 24\. [^\n]+\n", "", text, count=1),
        "technograd missing": text.replace(TECHNOGRAD, "https://example.org"),
        "day 4 missing": text.replace("## День 4.", "## Итог 4.", 1),
        "third vote": text.replace("#### Слайд 4. «", "#### Слайд 4. «🗳 ", 1),
        "second prompt trial": text.replace("#### Слайд 6. «", "#### Слайд 6. «🤖 ", 1),
        "trigger word": text.replace("## Как читать", "Курс учит экономической безопасности.\n\n## Как читать", 1),
        "harm in filter": re.sub(r"(#### Слайд \d+\. «[^»\n]*?)полезность для встречи", r"\1возможный вред", text, count=1),
        "founder quote shortened": text.replace("Пока на простом уровне", "", 1),
        "activity marker missing": text.replace("маркер активности", "признак"),
        "principle missing": text.replace(PRINCIPLE, "Просто"),
    }
    return [name for name, mutated in broken.items() if not validate(mutated, name)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="also prove the checker rejects the rejected RFC and broken fixtures")
    args = parser.parse_args()
    text = NEW_RFC.read_text(encoding="utf-8")
    errors = validate(text, NEW_RFC.name)
    if frontmatter(FOLDER_README.read_text(encoding="utf-8")).get("status") != "rejected":
        errors.append("presentation-rfc/README.md: folder not marked rejected")
    if frontmatter(OLD_RFC.read_text(encoding="utf-8")).get("status") != "rejected":
        errors.append(f"{OLD_RFC.name}: status is not rejected")
    if args.self_test:
        if not validate(OLD_RFC.read_text(encoding="utf-8"), OLD_RFC.name):
            errors.append("self-test: rejected #665 RFC unexpectedly passes the contract")
        failed = self_test(text)
        errors += [f"self-test: mutation not rejected: {name}" for name in failed]
    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        raise SystemExit(1)
    print("PASS: appeal first; 4 days × 22–26 slides with 5 intro / 15–20 main / 1–4 final; 4 fields per slide with a self-study link; 90 minutes with reserve")
    print("PASS: ≤2 chat votes and 1 prompt trial per day; Day 4 narrative tied to Day 3; Day 3 filter by usefulness for the meeting; case 1 lawsuits as an activity marker")
    print("PASS: founder quotes verbatim; no trigger words outside quotes; repository links and anchors resolve; no tables before appendix; no image prompts")
    if args.self_test:
        print("PASS: rejected #665 RFC fails the contract; 18 broken fixtures rejected")


if __name__ == "__main__":
    main()
