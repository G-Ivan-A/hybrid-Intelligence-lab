#!/usr/bin/env python3
"""Check issue #673: the three Day 2 files follow the Day 2 section of RFC v0.3 — 24 slides, peaceful collection, CONFLICT on matrix openness, GRA as guardrails."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
RFC = DOMAIN / "2026-10-12-rfc-days-1-3-logic.md"
RATIONALE = DOMAIN / "2026-10-30-day2-rationale-and-method.md"
PRESENTATION = DOMAIN / "2026-10-30-day2-presentation.md"
SCRIPT = DOMAIN / "2026-10-30-day2-lecturer-script.md"
FILES = (RATIONALE, PRESENTATION, SCRIPT)
SOURCE = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/673"
REPO_BLOB = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
CASE1_ANCHOR = "кейс-1-умные-холодные-продажи-conflict-по-открытости-матрицы-меняет-подготовку-к-встрече"
OLD_CASE1_ANCHOR = "кейс-1-b2b-производство-conflict-по-задержкам-оплат-меняет-стратегию-переговоров"
SLIDE = re.compile(r"^#### Слайд (\d+)\. «(.+)»$", re.M)
MINUTES = re.compile(r"· (\d+(?:,\d)?) мин$", re.M)
RESERVE = re.compile(r"Резерв — (\d+(?:,\d)?) минут")
LINK = re.compile(r"\]\(([^)\s]+)\)")
FIELDS = (
    "- **Главный вывод:**",
    "- **На слайде:**",
    "- **Связь:**",
    "- **Глубже — в ссылках:**",
    "- **Визуал:**",
    "- **Формат и время:**",
)
# The RFC #671 stop lists, applied to every Day 2 file: verbatim program quotes (lines starting with «>») and link targets are exempt.
TRIGGERS = re.compile(r"безопасн|разоблач|угроз|расследова|ловл[яиюе]", re.I)
DAY_TONE = re.compile(r"риск|вшив", re.I)
FORMULA = re.compile(r"формул(?!ир)|F\(t\)|\bH1\b", re.I)
INCOMING = re.compile(r"запрос[а-я]* цен|прислал[аи]? запрос|входящ[а-я]* запрос", re.I)
PROVOCATION = re.compile(r"провок|провоц", re.I)
HARM = re.compile(r"вред", re.I)
STOP_LISTS = (("trigger word", TRIGGERS), ("risk or «вшивость» rhetoric", DAY_TONE), ("GRA formula", FORMULA),
              ("incoming price request", INCOMING), ("provocation", PROVOCATION), ("«вред»", HARM))
# #673 item 2: payments are never the focus; any sentence about payments must be a prohibition.
PAYMENT = re.compile(r"оплат|платёж|платеж", re.I)
NEGATION = re.compile(r"(?<![а-яё])(?:не|ни|нет|нельзя|без|вне)(?![а-яё])|запрещ", re.I)
PAYMENT_CONFLICT = re.compile(r"CONFLICT`? по (?:задержкам )?оплат", re.I)
PAYMENT_BAN = re.compile(r"(?<![а-яё])не(?![а-яё])[^.\n]{0,160}платёжн[а-я]* дисциплин", re.I)
ACTIVITY = re.compile(r"иск[а-я]*[^.\n]{0,240}маркер[а-я]* активности|маркер[а-я]* активности[^.\n]{0,240}иск", re.I)
MATRIX_QUOTES = ("сеть ищет местных производителей", "матрица закрыта до весны")
ETHICS = {
    "open accounts allowed": re.compile(r"открыт[а-я]* (?:аккаунт|профил)", re.I),
    "public photos allowed": re.compile(r"фото в открытом доступе", re.I),
    "business phone in a personal contact book": re.compile(r"записн[а-я]* книжк", re.I),
    "hidden databases forbidden": re.compile(r"скрыт[а-я]* баз", re.I),
    "illegal parsing forbidden": re.compile(r"парсинг", re.I),
    "closed data forbidden": re.compile(r"закрыт[а-я]* (?:профил|данн)", re.I),
}
PROMPT_RULES = {
    "Wayback Machine": re.compile(r"web\.archive\.org"),
    "open web": re.compile(r"открыт[а-я]* веб", re.I),
    "mandatory search": re.compile(r"обязательн", re.I),
    "ЕГРЮЛ optional": re.compile(r"ЕГРЮЛ[^\n]{0,80}по желанию", re.I),
    "empty archive recorded as «снимков нет»": re.compile(r"снимков нет", re.I),
    "guardrails": re.compile(r"guardrail", re.I),
}
# #673 item 7: slides 1–10 form one «потому что → поэтому» chain; each link carries its own step.
CHAIN = {
    2: (r"без основани",),
    6: (r"объём", r"источник"),
    7: (r"уверенност", r"точност"),
    8: (r"9 независимых источник",),
    9: (r"провенанс",),
    10: (r"статус", r"встреч"),
}
VOTE, TRIAL = "🗳", "🤖"
VOTE_SLIDES, TRIAL_SLIDES = {3, 10}, {14}
SCRIPT_VOTE, SCRIPT_TRIAL = "[ГОЛОСОВАНИЕ В ЧАТ]", "[ПРОБА ПРОМПТА]"


def number(value):
    return float(value.replace(",", "."))


def frontmatter(text):
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    return dict(line.split(": ", 1) for line in match[1].splitlines() if ": " in line) if match else {}


def plain(text):
    """Text without blockquotes: verbatim quotes of the program and of the founder keep their own words."""
    return "\n".join(line for line in text.splitlines() if not line.startswith(">"))


def prose(text):
    """Plain text without link targets: headings of other files may keep their own words."""
    return re.sub(r"\]\([^)]*\)", "]", plain(text))


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


def broken_links(text, texts, only=None):
    """Repository links whose file or anchor is missing; texts overrides files under test."""
    cache = {}
    for url in sorted(set(LINK.findall(text))):
        if not url.startswith(REPO_BLOB):
            continue
        path, _, anchor = url[len(REPO_BLOB):].partition("#")
        target = ROOT / path
        if only and target not in only:
            continue
        if target not in texts and not target.is_file():
            yield f"{url}: file not found"
        elif anchor and target.suffix == ".md":
            if target not in cache:
                cache[target] = anchors(texts.get(target) or target.read_text(encoding="utf-8"))
            if anchor not in cache[target]:
                yield f"{url}: anchor not found"


def rfc_day2(rfc):
    start = rfc.find("## День 2.")
    end = rfc.find("\n## День 3.", start)
    return rfc[start:end] if start >= 0 and end > start else ""


def slides(text):
    matches = list(SLIDE.finditer(text))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        tail = re.search(r"^#{1,3} ", text[match.end():end], re.M)
        yield int(match[1]), match[2], text[match.end():match.end() + tail.start() if tail else end]


def field(chunk, name):
    match = re.search(re.escape(name) + r"[^\n]*(?:\n  [^\n]*)*", chunk)
    return match[0] if match else ""


def prompt_block(script):
    match = re.search(r"^### А\.2\. Текст промпта\n+```text\n(.*?)\n```", script, re.S | re.M)
    return match[1] if match else ""


def validate(texts, rfc):
    errors = []
    rationale, presentation, script = (texts[path] for path in FILES)
    day2 = rfc_day2(rfc)
    if not day2:
        return ["RFC: Day 2 section not found"]

    # 1. Shared contract of the three files.
    for path in FILES:
        text, name = texts[path], path.name
        if frontmatter(text).get("source", "").strip('"') != SOURCE:
            errors.append(f"{name}: frontmatter source is not issue #673")
        clean = prose(text)
        for label, pattern in STOP_LISTS:
            for match in sorted(set(pattern.findall(clean)))[:3]:
                errors.append(f"{name}: {label}: «{match}»")
        for quote in MATRIX_QUOTES:
            if quote not in clean:
                errors.append(f"{name}: matrix CONFLICT quote missing: «{quote}»")
        if PAYMENT_CONFLICT.search(clean):
            errors.append(f"{name}: case 1 CONFLICT is built on payments")
        for sentence in re.split(r"(?<=[.!?])\s+|\n", clean):
            if PAYMENT.search(sentence) and not NEGATION.search(sentence):
                errors.append(f"{name}: payments discussed without a prohibition: «{sentence.strip()[:90]}»")
                break
        if "guardrail" not in clean:
            errors.append(f"{name}: GRA is not presented as guardrails")
        relative = [url for url in LINK.findall(text) if not re.match(r"https?://", url)]
        if relative:
            errors.append(f"{name}: links are not full URLs: {relative[:3]}")
        errors += [f"{name}: {error}" for error in broken_links(text, texts)]

    # 2. Rationale: SSOT collection condition, guardrails, lawsuits as activity marker, case 1 on the matrix.
    condition = re.search(r"\*\*Условие сбора\.\*\* ([^\n]+?) Это этическая граница", day2)
    if not condition or condition[1] not in rationale:
        errors.append(f"{RATIONALE.name}: RFC collection condition is not quoted verbatim")
    if CASE1_ANCHOR not in anchors(rationale):
        errors.append(f"{RATIONALE.name}: case 1 heading on matrix openness missing")
    for word in ("масса", "дистанция", "полярность"):
        if word not in rationale.lower():
            errors.append(f"{RATIONALE.name}: guardrail question missing: {word}")
    for path in (RATIONALE, SCRIPT):
        text = prose(texts[path])
        if not ACTIVITY.search(text):
            errors.append(f"{path.name}: lawsuits are not read as an activity marker")
        if not PAYMENT_BAN.search(text):
            errors.append(f"{path.name}: no explicit ban on payment-discipline conclusions")
        for label, pattern in ETHICS.items():
            if not pattern.search(text):
                errors.append(f"{path.name}: ethics boundary missing: {label}")

    # 3. Presentation: 24 RFC slides with the same titles and minutes, six fields, chain, votes, budget.
    expected = [(n, title, MINUTES.findall(chunk)) for n, title, chunk in slides(day2)]
    actual = list(slides(presentation))
    if [n for n, _, _ in actual] != list(range(1, 25)):
        errors.append(f"{PRESENTATION.name}: slides are not 1–24: {[n for n, _, _ in actual][:40]}")
    for (n, title, minutes), (m, own_title, chunk) in zip(expected, actual):
        if n != m:
            break
        if own_title != title:
            errors.append(f"{PRESENTATION.name}: slide {n} title differs from RFC: «{own_title}»")
        if MINUTES.findall(chunk) != minutes:
            errors.append(f"{PRESENTATION.name}: slide {n} minutes differ from RFC: {MINUTES.findall(chunk)} vs {minutes}")
        for name in FIELDS:
            if name not in chunk:
                errors.append(f"{PRESENTATION.name}: slide {n} field missing: {name}")
        if not re.search(r"\]\(https://[^)\s]+\)", field(chunk, "- **Глубже — в ссылках:**")):
            errors.append(f"{PRESENTATION.name}: slide {n} has no full URL in «Глубже — в ссылках»")
        link = field(chunk, "- **Связь:**").lower()
        if n <= 10 and not ("потому что" in link and "поэтому" in link):
            errors.append(f"{PRESENTATION.name}: slide {n} link is not «потому что → поэтому»")
        for term in CHAIN.get(n, ()):
            if not re.search(term, link):
                errors.append(f"{PRESENTATION.name}: slide {n} chain step missing: {term}")
    votes = {n for n, title, _ in actual if VOTE in title}
    trials = {n for n, title, _ in actual if TRIAL in title}
    if votes != VOTE_SLIDES or trials != TRIAL_SLIDES:
        errors.append(f"{PRESENTATION.name}: votes {sorted(votes)} and prompt trials {sorted(trials)}, expected {sorted(VOTE_SLIDES)} and {sorted(TRIAL_SLIDES)}")
    minutes = sum(number(m) for _, _, chunk in actual for m in MINUTES.findall(chunk))
    reserve = RESERVE.search(presentation)
    if not reserve or minutes + number(reserve[1]) != 90:
        errors.append(f"{PRESENTATION.name}: slides {minutes:g} min + reserve {reserve[1] if reserve else '?'} ≠ 90")

    # 4. Lecturer script: every slide once and in order, 2 votes, 1 prompt trial, the prompt searches Wayback and the open web.
    markers = [int(n) for n in re.findall(r"`\[СЛАЙД (\d+)\]`", script)]
    if sorted(set(markers)) != list(range(1, 25)) or markers != sorted(markers):
        errors.append(f"{SCRIPT.name}: slide markers are not 1–24 in order: {sorted(set(markers))}")
    body = script.split("\n## Приложение", 1)[0]
    if body.count(SCRIPT_VOTE) != 2 or body.count(SCRIPT_TRIAL) != 1:
        errors.append(f"{SCRIPT.name}: {body.count(SCRIPT_VOTE)} votes and {body.count(SCRIPT_TRIAL)} prompt trials, expected 2 and 1")
    prompt = prompt_block(script)
    if not prompt:
        errors.append(f"{SCRIPT.name}: section «А.2. Текст промпта» with a text block missing")
    for label, pattern in PROMPT_RULES.items():
        if prompt and not pattern.search(prompt):
            errors.append(f"{SCRIPT.name}: Промпт-разведчик rule missing: {label}")
    if prompt and not (PAYMENT_BAN.search(prompt) and re.search(r"маркер[а-я]* активности", prompt)):
        errors.append(f"{SCRIPT.name}: Промпт-разведчик lets the model read lawsuits beyond an activity marker")
    if prompt and not (re.search(r"скрыт[а-я]* баз", prompt) and re.search(r"парсинг", prompt)):
        errors.append(f"{SCRIPT.name}: Промпт-разведчик has no ethics boundary")

    # 5. RFC side: the slide 10 link points to the rebuilt case 1, and RFC links into Day 2 resolve.
    if OLD_CASE1_ANCHOR in rfc or "описан через оплаты" in rfc:
        errors.append(f"{RFC.name}: slide 10 still points to the payment case 1")
    errors += [f"{RFC.name}: {error}" for error in broken_links(rfc, texts, only=set(FILES))]
    return errors


def mutate(texts, path, old, new, count=1):
    changed = dict(texts)
    changed[path] = texts[path].replace(old, new, count)
    return changed


def mutate_re(texts, path, pattern, new):
    changed = dict(texts)
    changed[path] = re.sub(pattern, new, texts[path], count=1, flags=re.M | re.S)
    return changed


def self_test(texts, rfc):
    p, r, s = PRESENTATION, RATIONALE, SCRIPT
    lead = "- **Главный вывод:** "
    broken = {
        "slide removed": mutate_re(texts, p, r"^#### Слайд 24\. [^\n]+\n", ""),
        "third vote": mutate(texts, p, "#### Слайд 4. «", "#### Слайд 4. «🗳 "),
        "second prompt trial": mutate(texts, p, "#### Слайд 6. «", "#### Слайд 6. «🤖 "),
        "title drift": mutate(texts, p, "«140 упоминаний сети", "«150 упоминаний сети"),
        "minutes drift": mutate(texts, p, "· 1 мин", "· 2 мин"),
        "reserve drift": mutate(texts, p, "Резерв — 10 минут", "Резерв — 5 минут"),
        "link field missing": mutate(texts, p, "- **Глубже — в ссылках:**", "- Ссылки:"),
        "link field without URL": mutate_re(texts, p, r"(- \*\*Глубже — в ссылках:\*\*)[^\n]*", r"\1 см. документ 1."),
        "chain without «потому что»": mutate_re(texts, p, r"(#### Слайд 7\..*?- \*\*Связь:\*\* )[Пп]отому что", r"\1Так как"),
        "chain step lost": mutate_re(texts, p, r"(#### Слайд 8\..*?- \*\*Связь:\*\*[^\n]*?)9 независимых источник", r"\1немного источник"),
        "formula in rationale": mutate(texts, r, "\n## ", "\nСила связи считается по формуле F(t).\n\n## "),
        "trigger word in script": mutate(texts, s, "\n## ", "\nЭто курс об экономической безопасности.\n\n## "),
        "«вшивость» in presentation": mutate(texts, p, lead, lead + "Проверка на вшивость. "),
        "payment CONFLICT": mutate(texts, r, "\n## ", "\nВ кейсе 1 главный `CONFLICT` по задержкам оплат.\n\n## "),
        "payment-discipline conclusion": mutate(texts, s, "\n## ", "\nИски показывают, как сеть платит поставщикам.\n\n## "),
        "incoming price request": mutate(texts, r, "\n## ", "\nСеть «Х» прислала запрос цен.\n\n## "),
        "matrix quote missing": mutate(texts, p, "матрица закрыта до весны", "ассортимент обновят", count=-1),
        "activity marker missing": mutate(texts, s, "маркер активности", "признак", count=-1),
        "payment ban missing": mutate_re(texts, r, r"(?<![а-яё])не(?![а-яё])([^.\n]{0,160}платёжн)", r"мы\1"),
        "hidden databases not forbidden": mutate(texts, r, "скрытые базы", "новые сводки", count=-1),
        "contact book missing": mutate(texts, s, "записную книжку", "таблицу", count=-1),
        "collection condition edited": mutate(texts, r, "без обхода входа", "с обходом входа"),
        "wayback missing in prompt": mutate(texts, s, "web.archive.org", "example.org", count=-1),
        "ЕГРЮЛ mandatory": mutate_re(texts, s, r"(ЕГРЮЛ[^\n]{0,80})по желанию", r"\1обязательно"),
        "broken anchor": mutate(texts, r, "## Мост ко Дню 3", "## Переход"),
        "case 1 still on payments": mutate(texts, r, "по открытости матрицы", "по задержкам оплат"),
        "script slide marker missing": mutate(texts, s, "`[СЛАЙД 12]`", ""),
        "third vote in script": mutate(texts, s, "`[СЛАЙД 4]`", "`[СЛАЙД 4]` " + SCRIPT_VOTE),
        "relative link": mutate(texts, p, "](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/", "](../"),
        "source not #673": mutate(texts, s, SOURCE, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/660"),
    }
    failed = [name for name, mutated in broken.items() if mutated == texts or not validate(mutated, rfc)]
    rfc_broken = {
        "RFC slide 10 on the old anchor": rfc.replace(CASE1_ANCHOR, OLD_CASE1_ANCHOR, 1),
    }
    failed += [name for name, mutated in rfc_broken.items() if mutated == rfc or not validate(texts, mutated)]
    return failed, len(broken) + len(rfc_broken)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="also prove the checker rejects broken fixtures")
    args = parser.parse_args()
    texts = {path: path.read_text(encoding="utf-8") for path in FILES}
    rfc = RFC.read_text(encoding="utf-8")
    errors = validate(texts, rfc)
    if args.self_test and not errors:
        failed, fixtures = self_test(texts, rfc)
        errors += [f"self-test: mutation not rejected: {name}" for name in failed]
    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        raise SystemExit(1)
    print("PASS: presentation has the 24 RFC v0.3 slides with RFC titles and minutes, 6 fields each, a full URL in «Глубже — в ссылках», 🗳 on slides 3 and 10, 🤖 on slide 14, 80 + 10 = 90 minutes")
    print("PASS: slides 1–10 form the «потому что → поэтому» chain: no grounds → volume, not source → confidence, not accuracy → 140 = 9 sources → provenance → status → meeting")
    print("PASS: three files: source #673, no formula, no trigger/risk/«вред»/provocation words, no incoming price request, payments only as a prohibition, matrix CONFLICT quotes, guardrails")
    print("PASS: rationale quotes the RFC collection condition; lawsuits are an activity marker with no payment-discipline conclusions; ethics allows open accounts, photos, a contact book and forbids hidden databases, parsing, closed data")
    print("PASS: script shows slides 1–24 in order with 2 votes and 1 prompt trial; Промпт-разведчик searches Wayback Machine and the open web, ЕГРЮЛ by choice; repository links and RFC anchors resolve")
    if args.self_test:
        print(f"PASS: {fixtures} broken fixtures rejected")


if __name__ == "__main__":
    main()
