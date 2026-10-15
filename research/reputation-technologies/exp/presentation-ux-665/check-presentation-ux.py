#!/usr/bin/env python3
"""Check editorial coverage and preserve the approved pre-665 slide assets."""
import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
BASE = "6428ade"
# Day 2 was rebuilt on RFC v0.3 in #673 (24 slides); its layout is checked by exp/day2-rebuild-673/check-day2.py.
# Day 1 was rebuilt on RFC v0.3 in #675 (24 slides); its layout is checked by exp/day1-rebuild-675/check-day1.py.
DECKS = (
    "2026-11-02-day3-presentation.md",
)
RFC = DOMAIN / "gra-research-program/presentation-rfc/2026-10-12-rfc-presentation-ux-days-1-3.md"
SLIDE = re.compile(r"^\*\*Слайд ([ВЗ]?\d+)\. (.+?)\*\*$", re.M)


def slides(text):
    section = text.split("## Слайды\n", 1)[1].split("## Промпты для изображений", 1)[0]
    matches = list(SLIDE.finditer(section))
    return {m[1]: (m[2], section[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(section)])
            for i, m in enumerate(matches)}


def validate(text, original, label):
    errors = []
    current, previous = slides(text), slides(original)
    expected = [f"В{i}" for i in range(1, 7)] + [str(i) for i in range(1, 31)] + ["З1"]
    if list(current) != expected or len(SLIDE.findall(text)) != 37:
        errors.append(f"{label}: expected 6 opening + 30 original + 1 closing slides")
    for key, (title, body) in current.items():
        for field in ("Раскрытие тезисов:", "Главный вывод (как меняется мышление):", "Альтернативный промпт Qwen/Kandinsky:"):
            if field not in body:
                errors.append(f"{label}/{key}: missing {field}")
        paragraph = re.search(r"- Раскрытие тезисов: (.+)", body)
        if paragraph and len(paragraph[1].split()) < 25:
            errors.append(f"{label}/{key}: explanation too short to carry context")
        if not re.search(r"- Визуал:", body):
            errors.append(f"{label}/{key}: missing visual specification")
    for key, (title, body) in previous.items():
        if key not in current or current[key][0] != title:
            errors.append(f"{label}/{key}: original title changed")
            continue
        for visual in re.findall(r"^- Визуал: .+$", body, re.M):
            if visual not in current[key][1]:
                errors.append(f"{label}/{key}: original visual changed")
        for line in re.findall(r"^- .+$", body, re.M):
            preserved = line.replace("Сдвиг", "Главный вывод (как меняется мышление)").replace("сдвиг мышления", "главный вывод").replace("сдвиг", "изменение мышления")
            if preserved not in current[key][1]:
                errors.append(f"{label}/{key}: original thesis or instruction changed")
    old_prompts = re.findall(r"```text\n(.*?)\n```", original, re.S)
    new_prompts = re.findall(r"```text\n(.*?)\n```", text, re.S)
    for prompt in old_prompts:
        if prompt not in new_prompts:
            errors.append(f"{label}: original fenced image prompt changed")
    if "Сдвиг" in text or "сдвиг" in text:
        errors.append(f"{label}: old conclusion label remains")
    if len(re.findall(r"^\| [ИП][ОП][12] \|", text, re.M)) != 8:
        errors.append(f"{label}: expected 8 tools (2 open + 2 paid in each of 2 categories)")
    if "Имиджевые стратегии для действия" not in text:
        errors.append(f"{label}: approved Day 4 title missing")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    all_errors = []
    for name in DECKS:
        path = DOMAIN / name
        original = subprocess.check_output(["git", "show", f"{BASE}:{path.relative_to(ROOT)}"], cwd=ROOT, text=True)
        text = path.read_text()
        errors = validate(text, original, name)
        all_errors.extend(errors)
        if args.self_test and not errors:
            mutations = [
                text.replace("Раскрытие тезисов:", "Deleted:", 1),
                text.replace("Альтернативный промпт Qwen/Kandinsky:", "Deleted:", 1),
                text.replace("**Слайд В1.", "**Слайд В7.", 1),
                text.replace(f"**Слайд 1. {slides(original)['1'][0]}**", "**Слайд 1. Changed original title**", 1),
                text.replace("Имиджевые стратегии для действия", "Changed Day 4"),
            ]
            prompt = re.findall(r"```text\n(.*?)\n```", original, re.S)[0]
            mutations.append(text.replace(prompt, "Changed original prompt", 1))
            thesis = re.findall(r"^- .+$", slides(original)["2"][1], re.M)[0]
            mutations.append(text.replace(thesis, "- Deleted original thesis", 1))
            title, body = slides(text)["В1"]
            header = f"**Слайд В1. {title}**"
            mutations.append(text.replace(header, header + body + header, 1))
            for index, changed in enumerate(mutations, 1):
                if not validate(changed, original, name):
                    all_errors.append(f"{name}: mutation {index} escaped detection")
    if RFC.exists():
        rows = re.findall(r"^\| Д([123]) / ([ВЗ]?\d+) \|", RFC.read_text(), re.M)
        expected = {(str(d), k) for d in range(1, 4) for k in [f"В{i}" for i in range(1, 7)] + [str(i) for i in range(1, 31)] + ["З1"]}
        if len(rows) != 111 or set(rows) != expected:
            all_errors.append("RFC: incomplete or duplicate per-slide profile review")
    else:
        all_errors.append("RFC: review missing")
    if all_errors:
        print("\n".join(f"FAIL {error}" for error in all_errors))
        return 1
    print("PASS: 37 slides of Day 3; original titles, theses, visual specifications and image prompts preserved; 8 tool entries; 111 review rows")
    if args.self_test:
        print("PASS: 8 destructive mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
