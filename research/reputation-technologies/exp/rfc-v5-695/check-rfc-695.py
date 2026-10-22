#!/usr/bin/env python3
"""Check issue #695: the RFC of point diffs against the Day 4 deck v4 — every «Было» quotes its permalinked v4 line word for
word, the rows apply cleanly, and the resulting deck v5 passes the gate of #693 with the rules of #695: the wording of the NIA,
no ВШСДТ and Школа Туркенич, no blogs and no shortened links, GRA status profiles equal to the taxonomy with the context phrase
on every PARTIAL and CONFLICT, image prompts under the visual rule of #695 quoted word for word in section 3."""
import argparse
import hashlib
import re
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
V4_CHECK = DOMAIN / "exp/day4-v4-693/check-day4-693.py"
RFC = DOMAIN / "2026-11-03-rfc-presentation-update-v5.md"
TAXONOMY = DOMAIN / "image-technologies/20-taxonomy.md"
ISSUE_695 = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/695"
COMMIT = "f3af657b88884d00d37d795d645287188a245ffa"
# The deck v4 is quoted, not regenerated: the file must stay the one of commit f3af657.
V4_SHA256 = "27dc031a1a4de678d15574c8fb3ef6835b0a0d169c4764d498fd10ae165263db"
PERMALINK = f"https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/{COMMIT}/research/reputation-technologies/2026-11-03-day4-presentation-gamma-v4.md?plain=1#L"
HEADINGS = ("\n## 1. Обоснование\n", "\n## 2. Таблица замен (Diffs)\n", "\n## 3. Визуальные правила\n")
TABLE_HEAD = "| № | Слайд | Поле | Было (v4, дословно) | Стало (v5) | Обоснование |"
FIELDS = ("[SLIDE_TEXT]", "[IMAGE_PROMPT]", "[FOOTER_LINKS]", "### Заголовок слайда")
# The visual rule of #695, word for word.
VISUAL_RULE = ("Если меняются промпты, они должны строго соответствовать: haute couture 2026-2027, навеянные идеей ар-деко, 2-3 "
               "базовых цвета (графит #16181D, глубокий синий #132A4A, изумруд #0A4D3C, рубин #720E1E) + 1 золотой акцент #B89B5E, "
               "вертикаль 1:2.4, без текста на изображении.")
# The wording #695 prescribes for the technologies of the NIA and the phrase it attaches to every PARTIAL or CONFLICT profile.
NIA = 'Технологии, используемые в НИА "Гид по стилю" (на базе которых впоследствии образовался ряд профильных школ)'
NIA_SLIDES = (5, 10, 14, 16, 20)
CONTEXT = "Механизм восприятия реален, но направление и сила зависят от контекста, что требует проверки глазом и опытом."
# Slides of technologies and their taxonomy cards: the profile on the slide is the sum of the profiles of its cards.
CARDS = {4: ("1.3",), 5: ("1.9",), 6: ("1.5",), 9: ("2.2",), 10: ("2.14", "2.15"), 11: ("2.8",), 14: ("3.8",), 15: ("3.9",),
         17: ("3.2",), 20: ("4.9",), 21: ("4.1",), 22: ("4.7",)}
STATUSES = ("VERIFIED", "PARTIAL", "CONFLICT", "?")
COUNT = re.compile(r"(\d+) [`«]?(VERIFIED|PARTIAL|CONFLICT|\?)[`»]?")
# #695: ВШСДТ and Школа Туркенич stay in the module, the NIA is named without its authors, Маменко was a course page (a blog-like
# source); none of them reaches the deck v5 or the «Стало» column.
BANNED_V5 = ("ВШСДТ", "Туркенич", "Меньшиков", "Маменко")
# Replaced technologies and the misspelling «Ваттерман» survive only as quotes in the decisions section.
BANNED_SLIDES = ("Ваттерман", "Джексон", "Jackson", "Моллой", "Molloy", "Jewelrygram")
# Blogs, personal journals, file libraries, school pages and encyclopedias replaced by primary sources, and link shorteners.
BANNED_URLS = ("livejournal.", "jewelrygram.", "koob.ru", "style-school.com", "styleschool.ru", "tatyana-mamenko.", "wikipedia.org",
               "bit.ly", "goo.gl", "tinyurl.", "clck.ru", "vk.cc", "ow.ly", "is.gd", "cutt.ly", "t.co/")
# Influences the visual rule of #695 removes from the image prompts, the Gamma prompt and the photo table.
REMOVED_INFLUENCES = re.compile(r"Bauhaus|Neue Sachlichkeit|New York|Beijing|Баухауз|Нью-Йорк|Пекин|пекинск", re.I)
DEVIATIONS_695 = 7
# The wording of a deviation in #695; a bracket may hold a link, the first one may be followed by a qualifier.
DEVIATION = re.compile(r"Я предлагаю скорректировать \[.+?\][^\[\n]*?, потому что вариант \[.+?\] эффективнее решает задачу \[.+?\]\.")
ROW = re.compile(r"^\| (G-01|V5-\d{3}|S-\d{3}) \| (.*) \|$", re.M)
CELL_SPLIT = re.compile(r"(?<!\\) \| ")
BYLO = re.compile(r"^\[v4:L(\d+)\]\(" + re.escape(PERMALINK) + r"(\d+)\) «(.*)»$", re.S)
STALO = re.compile(r"^«(.*)»$", re.S)


def load_v4_check():
    """check-day4-693 with the rules of #695: GRA statuses are allowed, «консервативность» is not a case, the mandatory
    technologies are the ones of #695, the prompt tail is the visual rule of #695, slide 16 names the NIA without ВШСДТ."""
    source = V4_CHECK.read_text(encoding="utf-8")
    for old, new in (
            ('"ВШСДТ" not in overline or "«ГИД ПО СТИЛЮ»" not in overline', '"ВШСДТ" in overline or "«ГИД ПО СТИЛЮ»" not in overline'),
            ("does not name ВШСДТ and «Гид по стилю»", "names ВШСДТ or does not name «Гид по стилю»"),
            (r're.search(r"Опора П\b.*\bА\b", conclusion)', r're.search(r"Опора [КП]\b.*\bА\b", conclusion)')):
        if source.count(old) != 1:
            raise SystemExit(f"check-day4-693.py changed: «{old}» occurs {source.count(old)} times")
        source = source.replace(old, new)
    check = types.ModuleType("check_day4_695")
    check.__file__ = str(V4_CHECK)
    exec(compile(source, str(V4_CHECK), "exec"), check.__dict__)
    patterns = ((check.GRA, "|VERIFIED|PARTIAL|CONFLICT", ""), (check.CASE, "|консерв|", "|консерв(?!атив)|"),
                (check.IMAGE_TAIL, r"inspired by New York and Beijing, strictly subordinate to a luxurious art deco base "
                                   r"with a light touch of Bauhaus and Neue Sachlichkeit\.", r"inspired by the idea of art deco\."))
    compiled = []
    for pattern, old, new in patterns:
        if pattern.pattern.count(old) != 1:
            raise SystemExit(f"check-day4-693.py changed: «{old}» not in {pattern.pattern[:40]}")
        compiled.append(re.compile(pattern.pattern.replace(old, new), pattern.flags))
    check.GRA, check.CASE, check.IMAGE_TAIL = compiled
    check.MANDATORY = {"ЦВЕТ": ("Й. ИТТЕН", "ВАТЕРМАН", "ЦИНГЕЛЬ"),
                       "ФОРМА": ("БЕЛЯЕВА-ЭКЗЕМПЛЯРСКАЯ", "«ГИД ПО СТИЛЮ»"),
                       "СТИЛЬ": ("«ГИД ПО СТИЛЮ»", "ТРУБЕЦКОВА"),
                       "АКСЕССУАРЫ": ("«ГИД ПО СТИЛЮ»",)}
    removed = ("Нью-Йорком и Пекином", "Баухауз", "Neue Sachlichkeit")
    check.GAMMA_RULES = tuple(rule for rule in check.GAMMA_RULES if rule not in removed) + ("навеянная идеей ар-деко",)
    return check


CHECK = load_v4_check()
GAMMA = CHECK.GAMMA
FILES = CHECK.FILES + (RFC,)


def parse_rows(rfc):
    """Rows of section 2 as dicts, or errors."""
    errors, rows = [], []
    table = CHECK.section(rfc, HEADINGS[1])
    if table.count(TABLE_HEAD) != 2:
        errors.append(f"RFC: section 2 does not have the two tables with the header «{TABLE_HEAD}»")
    for match in ROW.finditer(table):
        cells = [cell.replace("\\|", "|") for cell in CELL_SPLIT.split(match[2])]
        if len(cells) != 5:
            errors.append(f"RFC {match[1]}: {len(cells) + 1} cells, expected 6")
            continue
        slide, field, bylo, stalo, reason = cells
        old, new = BYLO.match(bylo), STALO.match(stalo)
        if not old or not new:
            errors.append(f"RFC {match[1]}: «Было» is not «[v4:Ln](permalink of line n) «quote»» or «Стало» is not ««text»»")
            continue
        if old[1] != old[2]:
            errors.append(f"RFC {match[1]}: label v4:L{old[1]} and permalink #L{old[2]} differ")
        if not reason.strip():
            errors.append(f"RFC {match[1]}: no reason")
        rows.append({"id": match[1], "slide": slide, "field": field, "line": int(old[1]), "old": old[3], "new": new[1],
                     "reason": reason})
    ids = [row["id"] for row in rows]
    points = sum(i.startswith("V5-") for i in ids)
    expected = ["G-01"] + [f"V5-{i:03d}" for i in range(1, points + 1)] + [f"S-{i:03d}" for i in range(1, len(ids) - points)]
    if ids != expected:
        errors.append("RFC: rows are not G-01, V5-001… and S-001… numbered in order")
    if not rows:
        errors.append("RFC: no rows in section 2")
    return errors, rows


def locate(lines, n):
    """Slide number and field of v4 line n, or (None, None) outside the slides."""
    slide, field = None, None
    for line in lines[:n]:
        if line.startswith("## Источники и уровень опоры"):
            return None, None
        match = re.match(r"^### Слайд (\d+)\. ", line)
        if match:
            slide, field = int(match[1]), "### Заголовок слайда"
        match = re.match(r"^\*\*\[([A-Z_]+)\]\*\*", line)
        if match and slide:
            field = f"[{match[1]}]"
    return slide, field


def apply_rows(v4, rows):
    """Deck v5: the point rows applied to their v4 lines right to left, then G-01 in every prompt; errors if a quote is off."""
    errors, lines = [], v4.split("\n")
    result, by_line = list(lines), {}
    for row in rows:
        if row["id"] == "G-01":
            continue
        n = row["line"]
        if not 1 <= n <= len(lines) or lines[n - 1].count(row["old"]) != 1:
            errors.append(f"RFC {row['id']}: «Было» is not quoted once from v4 line {n}: «{row['old'][:60]}»")
            continue
        slide, field = locate(lines, n)
        field_ok = row["field"].startswith(field) if field else not row["field"].startswith(FIELDS)
        if str(slide or "—") != row["slide"] or not field_ok:
            errors.append(f"RFC {row['id']}: slide «{row['slide']}» and field «{row['field']}» do not match v4 line {n}")
        by_line.setdefault(n, []).append((lines[n - 1].index(row["old"]), row["old"], row["new"], row["id"]))
    for n, edits in by_line.items():
        edits.sort()
        for (a, old_a, _, id_a), (b, _, _, id_b) in zip(edits, edits[1:]):
            if a + len(old_a) > b:
                errors.append(f"RFC {id_a} and {id_b}: fragments of v4 line {n} overlap")
        text = lines[n - 1]
        for start, old, new, _ in reversed(edits):
            text = text[:start] + new + text[start + len(old):]
        result[n - 1] = text
    v5 = "\n".join(result)
    tail = [row for row in rows if row["id"] == "G-01"]
    if len(tail) != 1 or tail[0]["slide"] != "1–27" or tail[0]["field"] != "[IMAGE_PROMPT]":
        errors.append("RFC: no row G-01 for the tail of the 27 image prompts")
    elif v5.count(tail[0]["old"]) != CHECK.SLIDES or tail[0]["old"] not in lines[tail[0]["line"] - 1]:
        errors.append(f"RFC G-01: «Было» does not occur in each of the {CHECK.SLIDES} prompts after the point rows")
    else:
        v5 = v5.replace(tail[0]["old"], tail[0]["new"])
    return errors, v5


def profile(text):
    counts = dict.fromkeys(STATUSES, 0)
    for number, name in COUNT.findall(text):
        counts[name] += int(number)
    return counts


def taxonomy_profiles(taxonomy):
    result = {}
    for match in re.finditer(r"^### Технология (\d+\.\d+)\. .*?\n(.*?)(?=^### |\Z)", taxonomy, re.M | re.S):
        line = re.search(r"^\*\*Профиль статусов:\*\* (.*)$", match[2], re.M)
        if line:
            result[match[1]] = line[1]
    return result


def validate_v5(v5, texts):
    """Rules of #695 on the deck v5 beyond the gate of #693."""
    errors, chunks = [], {n: chunk for n, _, chunk in CHECK.slides(v5)}
    if ISSUE_695 not in [item.strip() for item in CHECK.frontmatter(v5).get("source", "").strip('"').split(";")]:
        errors.append("v5: frontmatter source does not name issue #695")
    for n in NIA_SLIDES:
        if NIA not in chunks.get(n, ""):
            errors.append(f"v5 slide {n}: wording of the NIA of #695 is not quoted word for word")
    errors += [f"v5: names «{name}»" for name in BANNED_V5 if name.casefold() in v5.casefold()]
    slides_part = v5.split(CHECK.DECISIONS, 1)[0].casefold()
    errors += [f"v5: «{name}» outside the decisions section" for name in BANNED_SLIDES if name.casefold() in slides_part]
    for url in dict.fromkeys(CHECK.LINK.findall(v5)):
        if not url.startswith("https://") or any(fragment in url for fragment in BANNED_URLS):
            errors.append(f"v5: link is not a full https URL of a primary source: {url}")
    prompts = [CHECK.gamma_field(chunk, "IMAGE_PROMPT") or "" for chunk in chunks.values()]
    gamma = CHECK.code_block(v5, "### Промпт для генерации в Gamma") or ""
    photos = "\n".join(row[2] for row in CHECK.LAYOUT_ROW.findall(v5))
    hits = REMOVED_INFLUENCES.findall("\n".join(prompts) + gamma + photos)
    if hits:
        errors.append(f"v5: image rules still carry influences removed by #695: {hits[:3]}")
    tax = taxonomy_profiles(texts[TAXONOMY])
    for card, line in tax.items():
        if re.search(r"PARTIAL|CONFLICT", line) and CONTEXT not in line:
            errors.append(f"taxonomy card {card}: PARTIAL or CONFLICT profile without the context phrase of #695")
    for line in v5.split("\n"):
        status = re.search(r"Статусы проверки: ([^.]*)\.( |$)", line)
        if re.search(r"PARTIAL|CONFLICT", line) and (not status or f"{status[0].rstrip()} {CONTEXT}" not in line):
            errors.append(f"v5: PARTIAL or CONFLICT without «Статусы проверки: ….» and the context phrase: «{line[:60]}»")
    for n, cards in CARDS.items():
        conclusion = re.search(r"^- Вывод: .*Статусы проверки: ([^.]*)\.", chunks.get(n, ""), re.M)
        expected = {name: sum(profile(tax.get(card, "").split(".")[0])[name] for card in cards) for name in STATUSES}
        if not conclusion or profile(conclusion[1]) != expected:
            errors.append(f"v5 slide {n}: status profile differs from taxonomy cards {', '.join(cards)}: {expected}")
    return errors


def own_text(rfc):
    """The RFC without its «Было» cells: the quotes of v4 keep the names and links #695 removes."""
    def drop(match):
        cells = CELL_SPLIT.split(match[2])
        return f"| {match[1]} | " + " | ".join(cells[:2] + cells[3:]) + " |"
    return ROW.sub(drop, rfc)


def validate_rfc(rfc, rows, texts):
    errors, own = [], own_text(rfc)
    if ISSUE_695 not in CHECK.frontmatter(rfc).get("source", ""):
        errors.append("RFC: frontmatter source is not issue #695")
    positions = [rfc.find(heading) for heading in HEADINGS]
    if -1 in positions or positions != sorted(positions):
        errors.append("RFC: sections «1. Обоснование», «2. Таблица замен (Diffs)», «3. Визуальные правила» missing or out of order")
    if VISUAL_RULE not in CHECK.section(rfc, HEADINGS[2]):
        errors.append("RFC: section 3 does not quote the visual rule of #695 word for word")
    reasoning = CHECK.section(rfc, HEADINGS[0])
    stated = DEVIATION.findall(reasoning)
    if len(stated) < DEVIATIONS_695:
        errors.append(f"RFC: section 1 does not state the {DEVIATIONS_695} deviations of #695 in the wording of the issue")
    errors += [f"RFC: deviation differs from the module: «{text[:60]}»" for text in stated if text not in texts[CHECK.OPEN_FILE]]
    tax = taxonomy_profiles(texts[TAXONOMY])
    table = section_table(reasoning, "### Этап 2")
    for n, cards in CARDS.items():
        expected = [sum(profile(tax.get(card, "").split(".")[0])[name] for card in cards) for name in STATUSES]
        got = table.get(n)
        if got != expected:
            errors.append(f"RFC: stage 2 table row of slide {n} is {got}, taxonomy gives {expected}")
    new = "\n".join(row["new"] for row in rows)
    errors += [f"RFC «Стало»: names «{name}»" for name in BANNED_V5 if name.casefold() in new.casefold()]
    errors += [f"RFC «Стало»: link is not a full https URL of a primary source: {url}" for url in dict.fromkeys(CHECK.LINK.findall(new))
               if not url.startswith("https://") or any(fragment in url for fragment in BANNED_URLS)]
    if "меньшиков" in own.casefold():
        errors.append("RFC: names an author of the NIA handbook outside the quotes of v4")
    hits = re.findall(r"(?<![а-яё])масс(?:а|ы|у|е|ой)?(?![а-яё])|дистанц|полярн", CHECK.prose(new), re.I)
    if hits:
        errors.append(f"RFC «Стало»: term of the course data-collection model: {hits[:3]}")
    loose = [url for url in CHECK.LINK.findall(own) if not url.startswith("https://") or any(f in url for f in BANNED_URLS)]
    if loose:
        errors.append(f"RFC: links outside the quotes of v4 are not full https URLs of primary sources: {loose[:3]}")
    errors += [f"RFC: {error}" for error in CHECK.broken_links(rfc, texts)]
    gate = CHECK.section(rfc, "\n## Гейт-проверка\n")
    if not re.search(r"^- \[x\] ", gate, re.M) or re.search(r"^- \[ \] ", gate, re.M):
        errors.append("RFC: gate check items are not all ticked")
    return errors


def section_table(text, heading):
    """Rows «| slide | … | V | P | C | ? |» of the table after heading: slide → four sums."""
    rows = {}
    for line in CHECK.section(text, heading, stop="\n### ").splitlines():
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == 6 and cells[0].isdigit():
            rows[int(cells[0])] = [sum(int(x) for x in re.findall(r"\d+", cell)) for cell in cells[2:]]
    return rows


def validate(texts):
    rfc, v4 = texts[RFC], texts[GAMMA]
    if not rfc or not v4:
        return [f"{path.name}: file not found" for path in (RFC, GAMMA) if not texts[path]]
    errors = []
    if hashlib.sha256(v4.encode("utf-8")).hexdigest() != V4_SHA256:
        errors.append(f"{GAMMA.name}: deck v4 differs from commit {COMMIT[:7]} — the RFC quotes it, it is not regenerated")
    row_errors, rows = parse_rows(rfc)
    errors += row_errors
    apply_errors, v5 = apply_rows(v4, rows)
    errors += apply_errors
    v5_texts = dict(texts)
    v5_texts[GAMMA] = v5
    errors += [f"v5: {error}" for error in CHECK.validate(v5_texts)]
    errors += validate_v5(v5, texts)
    errors += validate_rfc(rfc, rows, texts)
    return errors


mutate, mutate_re = CHECK.mutate, CHECK.mutate_re


def row(texts, row_id, pattern, new):
    """Fixture: the first match of pattern in table row row_id replaced; «Было» precedes «Стало» in the row."""
    return mutate_re(texts, RFC, rf"^(\| {row_id} \|[^\n]*?){pattern}", rf"\g<1>{new}")


def card(texts, number, pattern, new):
    """Fixture: the first match of pattern in the status profile of taxonomy card number replaced."""
    return mutate_re(texts, TAXONOMY, rf"(^### Технология {re.escape(number)}\. .*?^\*\*Профиль статусов:\*\* [^\n]*?){pattern}",
                     rf"\g<1>{new}")


def self_test(texts):
    r = RFC
    broken = {
        "RFC missing": mutate_re(texts, r, r".*", "", count=1),
        "deck v4 edited": mutate(texts, GAMMA, "Создай презентацию", "Создай, пожалуйста, презентацию"),
        "«Было» not quoted from its line": row(texts, "V5-001", "«Strict frontal", "«Stern frontal"),
        "«Было» line number wrong": row(texts, "V5-001", r"\[v4:L169\]\((\S+?#L)169\)", r"[v4:L170](\g<2>170)"),
        "label and permalink differ": row(texts, "V5-001", r"\[v4:L169\]\((\S+?#L)169\)", r"[v4:L169](\g<2>168)"),
        "permalink not of commit f3af657": row(texts, "V5-001", COMMIT, "main"),
        "«Было» without quote marks": row(texts, "V5-001", "«Strict frontal Neue Sachlichkeit framing»", "Strict frontal Neue Sachlichkeit framing"),
        "row removed, Джексон stays": mutate_re(texts, r, r"^\| V5-019 \|[^\n]*\n", ""),
        "row duplicated": mutate_re(texts, r, r"^(\| V5-001 \|[^\n]*)$", r"\1\n\1"),
        "rows out of order": mutate_re(texts, r, r"^\| V5-001 \|", "| V5-100 |"),
        "row with five cells": row(texts, "V5-001", r" \| Визуальное правило #695[^\n]*", ""),
        "row without reason": row(texts, "V5-001", r"Визуальное правило #695[^\n]*", " |"),
        "slide column wrong": mutate_re(texts, r, r"^\| V5-001 \| 2 \|", "| V5-001 | 3 |"),
        "field column wrong": mutate_re(texts, r, r"^\| V5-001 \| 2 \| \[IMAGE_PROMPT\]", "| V5-001 | 2 | [FOOTER_LINKS]"),
        "service row given a slide": mutate_re(texts, r, r"^\| S-001 \| — \|", "| S-001 | 1 |"),
        "table header without «Обоснование»": mutate(texts, r, TABLE_HEAD, TABLE_HEAD.replace(" Обоснование |", " Причина |")),
        "G-01 missing": mutate_re(texts, r, r"^\| G-01 \|[^\n]*\n", ""),
        "G-01 brings Bauhaus back": row(texts, "G-01", "» \\| «Haute couture 2026–2027, inspired by the idea of art deco.»",
                                        "» | «Haute couture 2026–2027, inspired by the idea of art deco and Bauhaus.»"),
        "prompt keeps Neue Sachlichkeit": row(texts, "V5-001", "» \\| «Strict frontal framing»", "» | «Strict frontal Neue Sachlichkeit framing»"),
        "Gamma prompt keeps New York": row(texts, "S-022", "» \\| «навеянная", "» | «вдохновлённая Нью-Йорком, навеянная"),
        "ВШСДТ in «Стало»": row(texts, "V5-048", "» \\| «Стиль: четыре стиля", "» | «Стиль: ВШСДТ, четыре стиля"),
        "Туркенич in a card of slide 6": row(texts, "V5-023", "» \\| «Дизайн одежды", "» | «По Туркенич, дизайн одежды"),
        "ТУРКЕНИЧ in «Стало»": row(texts, "V5-038", "— «ГИД ПО СТИЛЮ»»", "— «ГИД ПО СТИЛЮ», ШКОЛА СТИЛЯ Н. ТУРКЕНИЧ»"),
        "NIA author named": mutate(texts, r, "Имена авторов справочника не воспроизводятся.", "Справочник составила Е. Меньшикова."),
        "Ваттерман on a slide": row(texts, "V5-009", "» \\| «Ватерман»", "» | «Ваттерман»"),
        "Ваттерман in «Как читать»": row(texts, "S-011", "» \\| «Ватерман»", "» | «Ваттерман»"),
        "Кобаяси replaced by Джексон in «Как читать»": row(texts, "S-012", "шкала образов Кобаяси»", "сезонные цветотипы Джексон»"),
        "shortened link in «Стало»": row(texts, "V5-028", r"\(https://doi.org/10.1002/col.5080060210\)", "(https://bit.ly/3kXy)"),
        "http link in «Стало»": row(texts, "V5-028", r"\(https://doi.org/10.1002/col.5080060210\)", "(http://doi.org/10.1002/col.5080060210)"),
        "blog link in «Стало»": row(texts, "V5-028", r"\(https://doi.org/10.1002/col.5080060210\)", "(https://make-your-style.livejournal.com/297987.html)"),
        "blog link in the reasoning": mutate(texts, r, "](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md#исключённые-источники)",
                                             "](https://make-your-style.livejournal.com/297987.html)"),
        "NIA wording edited": row(texts, "V5-014", "на базе которых впоследствии", "на базе которых"),
        "NIA wording dropped": mutate(texts, r, NIA, "Технологии НИА", count=-1),
        "context phrase dropped": row(texts, "V5-007", " " + re.escape(CONTEXT), ""),
        "profile differs from taxonomy": row(texts, "V5-007", "Статусы проверки: 2 VERIFIED", "Статусы проверки: 3 VERIFIED"),
        "taxonomy profile changed": card(texts, "2.2", "3 `VERIFIED`", "2 `VERIFIED`"),
        "taxonomy PARTIAL without context": card(texts, "1.5", " " + re.escape(CONTEXT), ""),
        "stage 2 table differs": mutate(texts, r, "| 9 | Беляева-Экземплярская, карточка 2.2 | 3 |", "| 9 | Беляева-Экземплярская, карточка 2.2 | 2 |"),
        "GRA term in «Стало»": row(texts, "V5-022", "Метод идёт от задуманного впечатления", "Метод идёт от полярности впечатления"),
        "case on a technology slide": row(texts, "V5-022", "Метод идёт от задуманного впечатления", "Метод идёт от впечатления производителя"),
        "mandatory Трубецкова dropped": row(texts, "V5-[0-9]{3}", "И. ТРУБЕЦКОВА, Н. НАЙДЕНСКАЯ", "Н. НАЙДЕНСКАЯ"),
        "visual rule edited": mutate(texts, r, "вертикаль 1:2.4, без текста на изображении.", "вертикаль 9:16, без текста на изображении."),
        "visual rules section missing": mutate(texts, r, HEADINGS[2], "\n## 3. Изображения\n"),
        "reasoning section missing": mutate(texts, r, HEADINGS[0], "\n## 1. Контекст\n"),
        "sections out of order": mutate(mutate(mutate(texts, r, HEADINGS[0], "\n## swap\n"), r, HEADINGS[2], HEADINGS[0]), r,
                                        "\n## swap\n", HEADINGS[2]),
        "deviation differs from the module": mutate(texts, r, "эффективнее решает задачу [точной атрибуции]", "эффективнее решает задачу [атрибуции]"),
        "deviation wording broken": mutate(texts, r, "потому что вариант [снять блоги", "так как вариант [снять блоги"),
        "RFC source not #695": mutate(texts, r, f'source: "{ISSUE_695}"', 'source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/693"'),
        "RFC broken anchor": mutate(texts, r, "#подтверждение-pdf-кодекс-стиля-проанализирован-полностью", "#подтверждение-pdf"),
        "RFC links a missing file": mutate(texts, r, "/exp/rfc-v5-695/check-rfc-695.py)", "/exp/rfc-v5-695/check.py)"),
        "RFC relative link": mutate(texts, r, "](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md#исключённые-источники)",
                                    "](image-technologies/20-taxonomy.md#исключённые-источники)"),
        "RFC gate item unticked": mutate(texts, r, "- [x] Колода v4 не перегенерирована", "- [ ] Колода v4 не перегенерирована"),
        "v5 source without #695": row(texts, "S-003", "; https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/695\"»", '"»'),
    }
    failed = [name for name, mutated in broken.items() if not validate(mutated) or mutated == texts]
    return failed, len(broken)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="also prove the checker rejects broken fixtures")
    parser.add_argument("--write-v5", type=Path, help="write the deck v5 that the RFC produces to this path")
    args = parser.parse_args()
    texts = {path: path.read_text(encoding="utf-8") if path.is_file() else "" for path in FILES}
    errors = validate(texts)
    if args.write_v5 and texts[RFC]:
        args.write_v5.write_text(apply_rows(texts[GAMMA], parse_rows(texts[RFC])[1])[1], encoding="utf-8")
    if args.self_test and not errors:
        failed, fixtures = self_test(texts)
        errors += [f"self-test: mutation not rejected: {name}" for name in failed]
    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        raise SystemExit(1)
    rows = parse_rows(texts[RFC])[1]
    print(f"PASS: RFC has sections «1. Обоснование», «2. Таблица замен (Diffs)», «3. Визуальные правила»; {len(rows)} rows, each «Было» "
          f"quoted word for word from its permalinked line of the deck v4 (commit {COMMIT[:7]}, unchanged), slide and field match the line")
    print(f"PASS: the rows apply without overlaps and G-01 replaces the tail of all {CHECK.SLIDES} image prompts; the deck v5 passes the "
          "gate of #693 with the rules of #695")
    print(f"PASS: deck v5 quotes the wording of the NIA on slides {', '.join(map(str, NIA_SLIDES))}; no ВШСДТ, Школа Туркенич, authors of the "
          "NIA or blogs; every link is a full https URL without shorteners")
    print("PASS: status profiles on the technology slides and in the stage 2 table equal the taxonomy; every PARTIAL and CONFLICT carries "
          "the context phrase of #695")
    print("PASS: section 3 quotes the visual rule of #695 word for word; no New York, Beijing, Bauhaus or Neue Sachlichkeit in the image "
          f"prompts, the Gamma prompt and the photo table; section 1 states the {DEVIATIONS_695} deviations as in the module")
    if args.self_test:
        print(f"PASS: {fixtures} broken fixtures rejected")


if __name__ == "__main__":
    main()
