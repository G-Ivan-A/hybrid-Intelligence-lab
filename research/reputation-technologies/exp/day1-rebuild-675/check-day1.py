#!/usr/bin/env python3
"""Check issue #675: the three Day 1 files follow the Day 1 section of RFC v0.3 («Умные холодные продажи», GRA as guardrails, 24 slides); the Gamma deck moved to the #677 checker exp/day1-rebuild-677/check-day1-677.py."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
RFC = DOMAIN / "2026-10-12-rfc-days-1-3-logic.md"
RATIONALE = DOMAIN / "2026-10-07-day1-rationale-and-method-653.md"
PRESENTATION = DOMAIN / "2026-10-07-day1-presentation-653.md"
SCRIPT = DOMAIN / "2026-10-07-day1-lecturer-script-653.md"
FILES = (RATIONALE, PRESENTATION, SCRIPT)
SOURCE = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/675"
REPO_BLOB = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
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
# The NFR stop list of the #671 task, applied to every Day 1 file: verbatim program quotes (lines starting with «>») and link targets are exempt.
TRIGGERS = re.compile(r"безопасн|разоблач|угроз|расследова|ловл[яиюе]", re.I)
DAY_TONE = re.compile(r"риск|вшив", re.I)
FORMULA = re.compile(r"формул(?!ир)|F\(t\)|\bH1\b", re.I)
PROVOCATION = re.compile(r"провок|провоц", re.I)
STOP_LISTS = (("trigger word", TRIGGERS), ("risk or «вшивость» rhetoric", DAY_TONE), ("GRA formula", FORMULA),
              ("provocation", PROVOCATION))
# DoD of #671: a plain grep finds neither the incoming price request nor «прислал» anywhere in the files, quotes and links included.
RAW_INCOMING = re.compile(r"запрос[а-я]* цен|прислал", re.I)
# Lawsuits stay one activity marker; payments are never discussed except as a prohibition.
PAYMENT = re.compile(r"оплат|платёж|платеж|плат[ия]т|платил", re.I)
NEGATION = re.compile(r"(?<![а-яё])(?:не|ни|нет|нельзя|без|вне)(?![а-яё])|запрещ", re.I)
PAYMENT_BAN = re.compile(r"(?<![а-яё])не(?![а-яё])[^.\n]{0,160}платёжн[а-я]* дисциплин", re.I)
ACTIVITY = re.compile(r"иск[а-я]*[^.\n]{0,240}маркер[а-я]* активности|маркер[а-я]* активности[^.\n]{0,240}иск", re.I)
CASE = {
    "about 100 stores": re.compile(r"100 магазин"),
    "goal of 5–8 partner networks": re.compile(r"5–8 сет"),
    "in 3 months": re.compile(r"3 месяц"),
    "20 business cards": re.compile(r"20 визит"),
    "3–5 networks written to first": re.compile(r"3–5 сет"),
    "decision makers (ЛПР)": re.compile(r"ЛПР"),
    "network «Х» of 25 stores": re.compile(r"25 магазин"),
}
NODES = {
    "commercial director": re.compile(r"коммерческ[а-я]* директор", re.I),
    "category manager": re.compile(r"категорийн[а-я]* менеджер", re.I),
    "purchasing department": re.compile(r"служб[а-я]* закупок", re.I),
    "network representative from the exhibition": re.compile(r"представител[а-я]* сети[^.\n]{0,80}выставк", re.I),
    "co-supplier «С»": re.compile(r"сопоставщик[а-я]* «С»", re.I),
    "distributor «Д»": re.compile(r"дистрибьютор[а-я]* «Д»", re.I),
    "other suppliers of the network": re.compile(r"други[а-я]* поставщик[а-я]* сети", re.I),
    "industry association": re.compile(r"отраслев[а-я]* ассоциаци", re.I),
}
MARKERS = {
    "«Поставщикам» page": re.compile(r"«Поставщикам»"),
    "store openings and category-manager vacancies": re.compile(r"открыти[а-я]* магазин[^.\n]{0,40}ваканси", re.I),
    "page history in the web archive": re.compile(r"истори[а-я]* страниц[^.\n]{0,80}(?:веб-архив|Wayback)", re.I),
    "words of network representatives at the exhibition and in industry media": re.compile(r"слов[а-я]* представител[а-я]* сети[^.\n]{0,80}отраслев[а-я]* СМИ", re.I),
}
ETHICS = {
    "«гибко и одновременно аккуратно»": re.compile(r"гибко и одновременно аккуратно", re.I),
    "open accounts allowed": re.compile(r"открыт[а-я]* (?:аккаунт|профил)", re.I),
    "public photos allowed": re.compile(r"фото в открытом доступе", re.I),
    "business phone in a personal contact book": re.compile(r"записн[а-я]* книжк", re.I),
    "hidden databases forbidden": re.compile(r"скрыт[а-я]* баз", re.I),
    "leaked dumps forbidden": re.compile(r"«слит[а-я]*»", re.I),
    "illegal parsing forbidden": re.compile(r"парсинг", re.I),
    "closed data forbidden": re.compile(r"закрыт[а-я]* (?:профил|данн)", re.I),
}
SOURCES = {
    "Wayback Machine": re.compile(r"web\.archive\.org"),
    "open web": re.compile(r"открыт[а-я]* веб", re.I),
    "mandatory search": re.compile(r"обязательн", re.I),
    "ЕГРЮЛ optional": re.compile(r"ЕГРЮЛ[^\n]{0,80}по желанию", re.I),
}
PROMPT_RULES = dict(SOURCES, **{
    "empty archive recorded as «снимков нет»": re.compile(r"снимков нет", re.I),
    "guardrails": re.compile(r"guardrail", re.I),
    "question of mass": re.compile(r"масс[аеуы]", re.I),
    "question of distance": re.compile(r"дистанци", re.I),
    "question of polarity": re.compile(r"полярност", re.I),
    "«?» when there are no data": re.compile(r"«\?»"),
})
PAIR = {
    "harmony": re.compile(r"гармони", re.I),
    "eclecticism": re.compile(r"эклектик", re.I),
    "«свой, но заметный»": re.compile(r"свой, но заметный", re.I),
    "eclecticism as competent contrast": re.compile(r"грамотн[а-я]* контраст", re.I),
    "visual channels": re.compile(r"сайт[^.\n]{0,60}блог", re.I),
}
# Headings of the rationale that other files of the repository link to (grep of #675): they must survive the rewrite.
INBOUND_ANCHORS = (
    "источники", "связь-с-днями-24", "почему-переходить-от-образа-к-связям-нужно-сейчас", "сквозные-кейсы",
    "рабочие-определения-дня-1", "кейс-3-массажист-эксперт-рекомендации-вместо-рекламы",
    "кейс-1-приоритетный-производитель-консервов-досье-или-карта-связей",
    "итог-блока-2-как-контуры-складываются-в-единое-восприятие-бренда",
    "целевое-действие-найти-12-соисследователей", "свой-кейс-и-промпт-фреймер-дня-1", "поминутный-тайминг",
    "кейс-2-deep-tech-стартап-инвесторы-и-направление-потока", "главная-мысль-дня",
)
# #675 item 4: slides 1–10 form one «потому что → поэтому» chain (RFC «Проверка воротами»); each link carries its own step.
CHAIN = {
    1: (r"задач",),
    2: (r"20 визит", r"3–5"),
    3: (r"ответит",),
    4: (r"решает", r"отчёт"),
    5: (r"старая оптика",),
    6: (r"узк", r"круг"),
    7: (r"посредник", r"ИИ"),
    8: (r"связ",),
    9: (r"капитал",),
    10: (r"guardrail",),
}
VOTE, TRIAL = "🗳", "🤖"
VOTE_SLIDES, TRIAL_SLIDES = {3, 12}, {14}
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
        if not texts.get(target) and not target.is_file():
            yield f"{url}: file not found"
        elif anchor and target.suffix == ".md":
            if target not in cache:
                cache[target] = anchors(texts.get(target) or target.read_text(encoding="utf-8"))
            if anchor not in cache[target]:
                yield f"{url}: anchor not found"


def rfc_day1(rfc):
    start = rfc.find("## День 1.")
    end = rfc.find("\n## День 2.", start)
    return rfc[start:end] if start >= 0 and end > start else ""


def rfc_chain(rfc):
    start = rfc.find("## Проверка воротами")
    return re.findall(r"^(\d+)\. ", rfc[start:rfc.find("\nДля остальных дней", start)], re.M) if start >= 0 else []


def slides(text, pattern=SLIDE):
    matches = list(pattern.finditer(text))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        tail = re.search(r"^#{1,3} ", text[match.end():end], re.M)
        yield int(match[1]), match[2], text[match.end():match.end() + tail.start() if tail else end]


def field(chunk, name):
    match = re.search(re.escape(name) + r"[^\n]*(?:\n  [^\n]*)*", chunk)
    return match[0] if match else ""


def words(text):
    return len([token for token in text.split() if re.search(r"\w", token)])


def section(text, heading):
    match = re.search(r"^## " + re.escape(heading) + r"[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return match[1] if match else ""


def prompt_block(script):
    match = re.search(r"^### А\.2\. Текст промпта\n+```text\n(.*?)\n```", script, re.S | re.M)
    return match[1] if match else ""


def shared(path, text, texts, clean):
    """Contract shared by the three Day 1 files and the Gamma deck."""
    errors, name = [], path.name
    if frontmatter(text).get("source", "").strip('"') != SOURCE:
        errors.append(f"{name}: frontmatter source is not issue #675")
    for label, pattern in STOP_LISTS:
        for match in sorted(set(pattern.findall(clean)))[:3]:
            errors.append(f"{name}: {label}: «{match}»")
    for match in sorted(set(RAW_INCOMING.findall(text)))[:3]:
        errors.append(f"{name}: incoming price request plot: «{match}»")
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
    return errors


def validate(texts, rfc):
    errors = []
    rationale, presentation, script = (texts[path] for path in FILES)
    day1 = rfc_day1(rfc)
    if not day1:
        return ["RFC: Day 1 section not found"]
    missing = [path for path in FILES if not texts[path]]
    errors += [f"{path.name}: file not found" for path in missing]
    if missing:
        return errors

    # 1. Shared contract of the three files.
    for path in FILES:
        clean = prose(texts[path])
        errors += shared(path, texts[path], texts, clean)
        for label, pattern in CASE.items():
            if not pattern.search(clean):
                errors.append(f"{path.name}: case 1 «Умные холодные продажи» fact missing: {label}")

    # 2. Rationale: chain, nodes, markers, ethics, sources, harmony/eclecticism, inbound anchors, #675 section.
    clean = prose(rationale)
    own = anchors(rationale)
    for anchor in INBOUND_ANCHORS:
        if anchor not in own:
            errors.append(f"{RATIONALE.name}: heading linked from other files is gone: #{anchor}")
    chain = section(rationale, "Цепочка «потому что → поэтому»")
    items = re.findall(r"^(\d+)\. ([^\n]+)", chain, re.M)
    if [int(n) for n, _ in items] != list(range(1, 11)) or len(rfc_chain(rfc)) != 10:
        errors.append(f"{RATIONALE.name}: section «Цепочка «потому что → поэтому»» does not list slides 1–10")
    for n, line in items:
        terms = CHAIN.get(int(n), ())
        if not ("потому что" in line.lower() and "поэтому" in line.lower()) or not all(re.search(t, line) for t in terms):
            errors.append(f"{RATIONALE.name}: chain link {n} is not «потому что → поэтому» with its step")
    if not section(rationale, "Изменения версии 0.4 (issue #675)"):
        errors.append(f"{RATIONALE.name}: section «Изменения версии 0.4 (issue #675)» missing")
    budget = re.search(r"\*\*Бюджет Дня 1\.\*\* [^\n]+", day1)
    if not budget or budget[0] not in rationale:
        errors.append(f"{RATIONALE.name}: RFC budget of Day 1 is not quoted verbatim")
    for group, patterns in (("node", NODES), ("openness marker", MARKERS), ("source rule", SOURCES), ("harmony / eclecticism", PAIR)):
        for label, pattern in patterns.items():
            if not pattern.search(clean if group != "source rule" else rationale):
                errors.append(f"{RATIONALE.name}: {group} missing: {label}")
    for word in ("масса", "дистанция", "полярность"):
        if word not in clean.lower():
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

    # 3. Presentation: 24 RFC slides with the same titles and minutes, six fields, chain, nodes, markers, votes, budget, image prompts after the slides.
    expected = [(n, title, MINUTES.findall(chunk)) for n, title, chunk in slides(day1)]
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
        link = field(chunk, "- **Связь:**")
        if n <= 10 and not ("потому что" in link.lower() and "поэтому" in link.lower()):
            errors.append(f"{PRESENTATION.name}: slide {n} link is not «потому что → поэтому»")
        for term in CHAIN.get(n, ()):
            if not re.search(term, link):
                errors.append(f"{PRESENTATION.name}: slide {n} chain step missing: {term}")
        for group, number_, patterns in (("node", 11, NODES), ("openness marker", 13, MARKERS)):
            for label, pattern in patterns.items() if n == number_ else ():
                if not pattern.search(prose(chunk)):
                    errors.append(f"{PRESENTATION.name}: slide {n} {group} missing: {label}")
    votes = {n for n, title, _ in actual if VOTE in title}
    trials = {n for n, title, _ in actual if TRIAL in title}
    if votes != VOTE_SLIDES or trials != TRIAL_SLIDES:
        errors.append(f"{PRESENTATION.name}: votes {sorted(votes)} and prompt trials {sorted(trials)}, expected {sorted(VOTE_SLIDES)} and {sorted(TRIAL_SLIDES)}")
    minutes = sum(number(m) for _, _, chunk in actual for m in MINUTES.findall(chunk))
    reserve = RESERVE.search(presentation)
    if not reserve or minutes + number(reserve[1]) != 90:
        errors.append(f"{PRESENTATION.name}: slides {minutes:g} min + reserve {reserve[1] if reserve else '?'} ≠ 90")
    last = presentation.find("#### Слайд 24.")
    images = presentation.find("\n## Промпты для изображений")
    if last < 0 or images < last:
        errors.append(f"{PRESENTATION.name}: image prompts are not a separate section after the slides")

    # 4. Lecturer script: every slide once and in order, the chain spoken on slides 1–10, 2 votes, 1 prompt trial, the Промпт-фреймер, FAQ.
    markers = [int(n) for n in re.findall(r"`\[СЛАЙД (\d+)\]`", script)]
    if sorted(set(markers)) != list(range(1, 25)) or markers != sorted(markers):
        errors.append(f"{SCRIPT.name}: slide markers are not 1–24 in order: {sorted(set(markers))}")
    body = script.split("\n## Приложение", 1)[0]
    if body.count(SCRIPT_VOTE) != 2 or body.count(SCRIPT_TRIAL) != 1:
        errors.append(f"{SCRIPT.name}: {body.count(SCRIPT_VOTE)} votes and {body.count(SCRIPT_TRIAL)} prompt trials, expected 2 and 1")
    spoken = re.split(r"`\[СЛАЙД (\d+)\]`", body)
    for n in range(1, 11):
        segment = "".join(spoken[i + 1] for i in range(1, len(spoken) - 1, 2) if spoken[i] == str(n))
        if "поэтому" not in segment.lower():
            errors.append(f"{SCRIPT.name}: slide {n}: the «потому что → поэтому» link is not spoken")
    prompt = prompt_block(script)
    if not prompt:
        errors.append(f"{SCRIPT.name}: section «А.2. Текст промпта» with a text block missing")
    for label, pattern in PROMPT_RULES.items():
        if prompt and not pattern.search(prompt):
            errors.append(f"{SCRIPT.name}: Промпт-фреймер rule missing: {label}")
    if prompt and not (PAYMENT_BAN.search(prompt) and re.search(r"маркер[а-я]* активности", prompt)):
        errors.append(f"{SCRIPT.name}: Промпт-фреймер lets the model read lawsuits beyond an activity marker")
    if prompt and not (re.search(r"скрыт[а-я]* баз", prompt) and re.search(r"парсинг", prompt)):
        errors.append(f"{SCRIPT.name}: Промпт-фреймер has no ethics boundary")
    if not re.search(r"^## Приложение В\. Короткие ответы на частые вопросы", script, re.M):
        errors.append(f"{SCRIPT.name}: FAQ appendix missing")

    # 5. The RFC side.
    errors += [f"{RFC.name}: {error}" for error in broken_links(rfc, texts, only=set(FILES))]
    return errors


def mutate(texts, path, old, new, count=1):
    changed = dict(texts)
    changed[path] = texts[path].replace(old, new, count)
    return changed


def mutate_re(texts, path, pattern, new, count=1):
    changed = dict(texts)
    changed[path] = re.sub(pattern, new, texts[path], count=count, flags=re.M | re.S)
    return changed


def self_test(texts, rfc):
    p, r, s = PRESENTATION, RATIONALE, SCRIPT
    lead = "- **Главный вывод:** "
    broken = {
        "slide removed": mutate_re(texts, p, r"^#### Слайд 24\. [^\n]+\n", ""),
        "third vote": mutate(texts, p, "#### Слайд 4. «", "#### Слайд 4. «🗳 "),
        "second prompt trial": mutate(texts, p, "#### Слайд 6. «", "#### Слайд 6. «🤖 "),
        "title drift": mutate(texts, p, "«20 визиток с выставки", "«30 визиток с выставки"),
        "minutes drift": mutate(texts, p, "· 1 мин", "· 2 мин"),
        "reserve drift": mutate(texts, p, "Резерв — 10 минут", "Резерв — 5 минут"),
        "link field missing": mutate(texts, p, "- **Глубже — в ссылках:**", "- Ссылки:"),
        "link field without URL": mutate_re(texts, p, r"(- \*\*Глубже — в ссылках:\*\*)[^\n]*", r"\1 см. документ 1."),
        "chain without «потому что»": mutate_re(texts, p, r"(#### Слайд 7\..*?- \*\*Связь:\*\* )[Пп]отому что", r"\1Так как"),
        "chain step lost": mutate_re(texts, p, r"(#### Слайд 9\..*?- \*\*Связь:\*\*[^\n]*?)капитал", r"\1ресурс", count=0),
        "node missing on slide 11": mutate_re(texts, p, r"(#### Слайд 11\..*?)служб[а-я]* закупок(.*?#### Слайд 12)", r"\1отдел\2"),
        "marker missing on slide 13": mutate_re(texts, p, r"#### Слайд 13\..*?(?=#### Слайд 14)", lambda m: m[0].replace("«Поставщикам»", "о закупках")),
        "image prompts inside the slides": mutate(texts, p, "\n## Промпты для изображений", "\n## Иллюстрации"),
        "formula in rationale": mutate(texts, r, "\n## ", "\nСила связи считается по формуле F(t).\n\n## "),
        "H1 in presentation": mutate(texts, p, lead, lead + "Гипотеза H1. "),
        "trigger word in script": mutate(texts, s, "\n## ", "\nЭто курс об экономической безопасности.\n\n## "),
        "«вшивость» in presentation": mutate(texts, p, lead, lead + "Проверка на вшивость. "),
        "risk rhetoric in script": mutate(texts, s, "\n## ", "\nКаждый новый партнёр — это риск.\n\n## "),
        "incoming price request": mutate(texts, r, "\n## ", "\nСеть «Х» прислала запрос цен.\n\n## "),
        "price request even in a quote": mutate(texts, s, "\n## ", "\n> Сеть сделала запрос цен.\n\n## "),
        "payment-discipline conclusion": mutate(texts, s, "\n## ", "\nИски показывают, как сеть платит поставщикам.\n\n## "),
        "activity marker missing": mutate(texts, s, "маркер активности", "признак", count=-1),
        "payment ban missing": mutate_re(texts, r, r"платёжн[а-я]* дисциплин[а-я]*", "надёжности", count=0),
        "case goal lost": mutate(texts, s, "5–8 сет", "много сет", count=-1),
        "hidden databases not forbidden": mutate_re(texts, r, r"скрыт[а-я]* баз[а-я]*", "новые сводки", count=0),
        "leaked dumps not forbidden": mutate_re(texts, s, r"«слит[а-я]*»", "свежие", count=0),
        "flexible and careful lost": mutate_re(texts, r, r"(?i)гибко и одновременно аккуратно", "строго", count=0),
        "contact book missing": mutate(texts, s, "записную книжку", "таблицу", count=-1),
        "eclecticism missing": mutate(texts, r, "свой, но заметный", "яркий", count=-1),
        "chain section lost": mutate(texts, r, "## Цепочка «потому что → поэтому»", "## Логика слайдов"),
        "inbound anchor lost": mutate(texts, r, "## Поминутный тайминг", "## Тайминг"),
        "wayback missing in prompt": mutate(texts, s, "web.archive.org", "example.org", count=-1),
        "ЕГРЮЛ mandatory": mutate_re(texts, s, r"(ЕГРЮЛ[^\n]{0,80})по желанию", r"\1обязательно", count=0),
        "«?» missing in prompt": mutate_re(texts, s, r"(### А\.2\. Текст промпта.*?)«\?»(.*?)```", r"\1?\2```"),
        "chain not spoken": mutate_re(texts, s, r"(`\[СЛАЙД 6\]`.*?)поэтому(.*?`\[СЛАЙД 7\]`)", r"\1и\2", count=0),
        "FAQ missing": mutate(texts, s, "## Приложение В. Короткие ответы на частые вопросы", "## Приложение В. Заметки"),
        "script slide marker missing": mutate(texts, s, "`[СЛАЙД 12]`", ""),
        "third vote in script": mutate(texts, s, "`[СЛАЙД 4]`", "`[СЛАЙД 4]` " + SCRIPT_VOTE),
        "relative link": mutate(texts, p, "](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/", "](../"),
        "source not #675": mutate(texts, s, SOURCE, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/653"),
    }
    failed = [name for name, mutated in broken.items() if mutated == texts or not validate(mutated, rfc)]
    rfc_broken = {
        "RFC Day 1 title changed": rfc.replace("«Что изучить после эфира: кейсы, промпт, свой кейс»", "«Что изучить после эфира»", 1),
    }
    failed += [name for name, mutated in rfc_broken.items() if mutated == rfc or not validate(texts, mutated)]
    return failed, len(broken) + len(rfc_broken)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="also prove the checker rejects broken fixtures")
    args = parser.parse_args()
    texts = {path: path.read_text(encoding="utf-8") if path.is_file() else "" for path in FILES}
    rfc = RFC.read_text(encoding="utf-8")
    errors = validate(texts, rfc)
    if args.self_test and not errors:
        failed, fixtures = self_test(texts, rfc)
        errors += [f"self-test: mutation not rejected: {name}" for name in failed]
    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        raise SystemExit(1)
    print("PASS: presentation has the 24 RFC v0.3 slides with RFC titles and minutes, 6 fields each, a full URL in «Глубже — в ссылках», 🗳 on slides 3 and 12, 🤖 on slide 14, 80 + 10 = 90 minutes, image prompts after the slides")
    print("PASS: slides 1–10 form the «потому что → поэтому» chain in the rationale, on the slides and in the lecturer's speech: task → 20 cards, 3–5 networks → will it answer → who decides → old optics → narrow circles → intermediaries and AI → links → capital → guardrails")
    print("PASS: three files: source #675, case «Умные холодные продажи» (100 stores, 5–8 networks in 3 months, 20 cards, 3–5 networks and their ЛПР, «Х» of 25 stores), no formula/F(t)/H1, no trigger/risk/«вшивость»/provocation words, no «запрос цен» or «прислал» even in quotes, payments only as a prohibition, guardrails")
    print("PASS: rationale keeps the 13 linked headings, the RFC budget, 8 nodes, 4 openness markers, Wayback and the open web mandatory, ЕГРЮЛ by choice, harmony/eclecticism «свой, но заметный», ethics «гибко и одновременно аккуратно»; lawsuits are one activity marker with no payment-discipline conclusions")
    print("PASS: script shows slides 1–24 in order and speaks the chain, 2 votes and 1 prompt trial; Промпт-фреймер asks the three guardrail questions, puts «?», searches Wayback Machine and the open web, ЕГРЮЛ by choice; FAQ present")
    print("PASS: repository links of the three files and RFC links to them resolve; the Gamma deck is checked by exp/day1-rebuild-677/check-day1-677.py")
    if args.self_test:
        print(f"PASS: {fixtures} broken fixtures rejected")


if __name__ == "__main__":
    main()
