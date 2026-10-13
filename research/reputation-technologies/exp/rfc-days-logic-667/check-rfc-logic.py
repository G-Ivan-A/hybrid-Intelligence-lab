#!/usr/bin/env python3
"""Check the issue #667 RFC contract: appeal first, logical slide skeletons, 90-minute budget."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
NEW_RFC = DOMAIN / "2026-10-12-rfc-days-1-3-logic.md"
OLD_RFC = DOMAIN / "gra-research-program/presentation-rfc/2026-10-12-rfc-presentation-ux-days-1-3.md"
FOLDER_README = DOMAIN / "gra-research-program/presentation-rfc/README.md"
TECHNOGRAD = "https://technograd.moscow/event_page_new?669#programm_event"
APPENDIX = "## Приложение"
FIELDS = ("- **Зачем этот слайд?**", "- **Нарративная связь:**", "- **Формат и время:**")
IMAGE_MARKERS = re.compile(r"Qwen|Kandinsky|Midjourney|DALL|Stable Diffusion|промпт[а-я]* (?:для )?изображени|image prompt", re.I)
LOCAL_PROGRAM = re.compile(r"default\.txt|121026\.txt|user-attachments")
DAY = re.compile(r"^## День ([123])\. .+$", re.M)
PART = re.compile(r"^### (Вход|Основная часть|Финал)[^\n]*\(слайды (\d+)–(\d+)\)$", re.M)
SLIDE = re.compile(r"^#### Слайд (\d+)\. «.+»$", re.M)
MINUTES = re.compile(r"· (\d+(?:,\d)?) мин$", re.M)
RESERVE = re.compile(r"Резерв — (\d+(?:,\d)?) минут")


def number(value):
    return float(value.replace(",", "."))


def frontmatter(text):
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return dict(line.split(": ", 1) for line in match[1].splitlines()) if match else {}


def day_sections(text):
    matches = list(DAY.finditer(text))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        tail = re.search(r"^## (?!День)", text[match.end():end], re.M)
        yield match[1], text[match.start():match.end() + tail.start() if tail else end]


def validate(text, label):
    errors = []
    h2 = re.findall(r"^## (.+)$", text, re.M)
    if not h2 or h2[0] != "КРИТИЧЕСКАЯ АППЕЛЯЦИЯ":
        errors.append(f"{label}: first section must be «КРИТИЧЕСКАЯ АППЕЛЯЦИЯ»")
    if not any(title.startswith("Executive Summary") for title in h2):
        errors.append(f"{label}: Executive Summary missing")
    main = text.split(APPENDIX, 1)[0]
    if re.search(r"^\|", main, re.M):
        errors.append(f"{label}: table in the main structure (allowed only after «{APPENDIX}»)")
    if LOCAL_PROGRAM.search(text):
        errors.append(f"{label}: mentions a local course-program file")
    if TECHNOGRAD not in text:
        errors.append(f"{label}: Technograd program link missing")
    days = dict(day_sections(text))
    if sorted(days) != ["1", "2", "3"]:
        errors.append(f"{label}: expected sections for Days 1, 2, 3")
    for day, body in days.items():
        where = f"{label}/День {day}"
        if IMAGE_MARKERS.search(body):
            errors.append(f"{where}: image prompt in slide structure")
        slides = list(SLIDE.finditer(body))
        numbers = [int(m[1]) for m in slides]
        if numbers != list(range(1, len(numbers) + 1)):
            errors.append(f"{where}: slide numbers must run 1..N")
        if len(numbers) > 30:
            errors.append(f"{where}: {len(numbers)} slides exceed 30")
        parts = {m[1]: int(m[3]) - int(m[2]) + 1 for m in PART.finditer(body)}
        main_count = sum(int(m[3]) - int(m[2]) + 1 for m in PART.finditer(body) if m[1] == "Основная часть")
        if parts.get("Вход") != 5 or not 15 <= main_count <= 20 or not 1 <= parts.get("Финал", 0) <= 4:
            errors.append(f"{where}: expected 5 intro + 15–20 main + 1–4 final slides")
        if sum(parts.values()) - parts.get("Основная часть", 0) + main_count != len(numbers):
            errors.append(f"{where}: part ranges do not cover all slides")
        total = 0.0
        for i, slide in enumerate(slides):
            chunk = body[slide.end():slides[i + 1].start() if i + 1 < len(slides) else len(body)]
            for field in FIELDS:
                if field not in chunk:
                    errors.append(f"{where}/слайд {slide[1]}: missing {field}")
            minutes = MINUTES.search(chunk)
            total += number(minutes[1]) if minutes else 0
        reserve = RESERVE.search(body)
        if not reserve or abs(total + number(reserve[1]) - 90) > 0.01:
            errors.append(f"{where}: slide minutes {total:g} + reserve do not sum to 90")
        if len(re.findall(r"«🗳", body)) > 4:
            errors.append(f"{where}: more than 4 chat votes")
    return errors


def self_test(text):
    broken = {
        "appeal moved": text.replace("## КРИТИЧЕСКАЯ АППЕЛЯЦИЯ", "## Аппеляция", 1),
        "table in main": text.replace("## Как читать", "| a | b |\n\n## Как читать", 1),
        "image prompt": text.replace("- **Зачем этот слайд?** Задаёт рамку", "- **Зачем этот слайд?** Промпт Qwen. Задаёт рамку", 1),
        "field missing": text.replace("- **Нарративная связь:**", "- Связь:", 1),
        "local program": text.replace("## Источники", "## Источники\n\nСм. default.txt.", 1),
        "budget broken": text.replace("· 1 мин", "· 4 мин", 1),
        "slide removed": re.sub(r"#### Слайд 24\. [^\n]+\n", "", text, count=1),
        "technograd missing": text.replace(TECHNOGRAD, "https://example.org"),
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
            errors.append("self-test: rejected #665 RFC unexpectedly passes the #667 contract")
        errors += [f"self-test: mutation not rejected: {name}" for name in self_test(text)]
    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        raise SystemExit(1)
    print("PASS: appeal first; 3 days × ≤30 slides with 5 intro / 15–20 main / 1–4 final; 3 fields per slide; 90 minutes with reserve; no tables before appendix; no image prompts")
    if args.self_test:
        print("PASS: rejected #665 RFC fails the contract; 8 broken fixtures rejected")


if __name__ == "__main__":
    main()
