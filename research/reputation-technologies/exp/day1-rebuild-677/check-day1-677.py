#!/usr/bin/env python3
"""Check issue #677: the Day 1 Gamma deck is readable slide by slide (Контекст → Цель → Действие), the lecturer's speech lives in a separate script, the lecturer research and the gate document are in place."""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
GAMMA = DOMAIN / "2026-10-14-day1-presentation-gamma.md"
SCRIPT = DOMAIN / "2026-10-14-day1-lecturer-script.md"
RESEARCH = DOMAIN / "2026-10-14-day1-lecturer-gra-research.md"
STANDARD = DOMAIN / "2026-10-15-day1-slide-standard-and-gate-677.md"
FILES = (GAMMA, SCRIPT, RESEARCH, STANDARD)
SOURCE = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/677"
REPO_BLOB = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/"
SLIDE = re.compile(r"^### Слайд (\d+)\. (.+)$", re.M)
LINK = re.compile(r"\]\(([^)\s]+)\)")
# The NFR stop list of #671, kept by #675 and #677 for the deck and the script: verbatim quotes (lines starting with «>») and link targets are exempt.
TRIGGERS = re.compile(r"безопасн|разоблач|угроз|расследова|ловл[яиюе]", re.I)
DAY_TONE = re.compile(r"риск|вшив", re.I)
FORMULA = re.compile(r"формул(?!ир)|F\(t\)|\bH1\b", re.I)
PROVOCATION = re.compile(r"провок|провоц", re.I)
STOP_LISTS = (("trigger word", TRIGGERS), ("risk or «вшивость» rhetoric", DAY_TONE), ("GRA formula", FORMULA),
              ("provocation", PROVOCATION))
# The case starts with the producer's own first letter: neither an incoming price request nor «прислал» anywhere, quotes and links included.
RAW_INCOMING = re.compile(r"запрос[а-я]* цен|прислал", re.I)
# #677: the founder asked for a full deck, so neither file may ask to cut or cap the number of slides.
SLIDE_LIMIT = re.compile(r"(?:сократ|урез|ограничь|не больше|не более|максимум)[^.\n]{0,40}слайд", re.I)
# Gamma page 7 quoted without changes and the founder's slide 9 title keep their own words; nothing else is exempt.
GAMMA_VERBATIM = (
    "Важны прозрачность отчетности, устойчивость риск-модели и отсутствие регуляторных скрытых угроз.",
    "GRA как guardrails (ограничители) для ИИ, а не формула",
)
# Lawsuits stay one activity marker; payments are never discussed except as a prohibition.
PAYMENT = re.compile(r"оплат|платёж|платеж|плат[ия]т|платил", re.I)
NEGATION = re.compile(r"(?<![а-яё])(?:не|ни|нет|нельзя|без|вне)(?![а-яё])|запрещ", re.I)
PAYMENT_BAN = re.compile(r"(?<![а-яё])(?:не|без)(?![а-яё])[^.\n]{0,160}платёжн[а-я]* дисциплин", re.I)
ACTIVITY = re.compile(r"(?:иск|судебн)[а-я]*[^.\n]{0,240}маркер[а-я]* активности|маркер[а-я]* активности[^.\n]{0,240}(?:иск|судебн)", re.I)
# Case 1 «Умные холодные продажи» as the founder fixed it in #677: the producer already works with networks and has over 100 wholesale buyers.
CASE = {
    "over 100 wholesale buyers": re.compile(r"более 100 оптовых"),
    "goal of 5–8 partner networks": re.compile(r"5–8 сет"),
    "in 3 months": re.compile(r"3 месяц"),
    "20 business cards": re.compile(r"20 визит"),
    "3–5 networks written to first": re.compile(r"3–5 сет"),
    "decision makers (ЛПР)": re.compile(r"ЛПР"),
    "network «Х» of 25 stores": re.compile(r"25 магазин"),
    "the producer writes first": re.compile(r"пишет первым|написать им первыми"),
}
OLD_CASE = re.compile(r"100 магазин")
NODES = {
    "commercial director": re.compile(r"коммерческ[а-я]* директор", re.I),
    "category manager": re.compile(r"категорийн[а-я]* менеджер", re.I),
    "purchasing": re.compile(r"закуп", re.I),
    "network representative": re.compile(r"представител[а-я]* сети", re.I),
    "co-supplier «С»": re.compile(r"сопоставщик[а-я]* «С»", re.I),
    "distributor «Д»": re.compile(r"дистрибьютор[а-я]* «Д»", re.I),
    "other suppliers of the network": re.compile(r"други[а-я]* поставщик", re.I),
    "industry association": re.compile(r"отраслев[а-я]* ассоциаци", re.I),
}
MARKERS = {
    "«Поставщикам» page": re.compile(r"«Поставщикам»"),
    "vacancies": re.compile(r"ваканси", re.I),
    "web archive": re.compile(r"архив", re.I),
    "lawsuits as an activity marker": ACTIVITY,
    "no payment-discipline conclusions": PAYMENT_BAN,
}
ETHICS = {
    "«гибко и одновременно аккуратно»": re.compile(r"гибко и одновременно аккуратно", re.I),
    "open accounts allowed": re.compile(r"открыт[а-я]* (?:аккаунт|профил)", re.I),
    "public photos allowed": re.compile(r"фото", re.I),
    "business phone in a personal contact book": re.compile(r"записн[а-я]* книжк", re.I),
    "hidden databases forbidden": re.compile(r"скрыт[а-я]* баз", re.I),
    "leaked dumps forbidden": re.compile(r"«слит[а-я]*»", re.I),
    "illegal parsing forbidden": re.compile(r"парсинг", re.I),
}
PROMPT_RULES = {
    "Wayback Machine": re.compile(r"web\.archive\.org"),
    "open web": re.compile(r"открыт[а-я]* веб", re.I),
    "mandatory search": re.compile(r"обязательн", re.I),
    "ЕГРЮЛ optional": re.compile(r"ЕГРЮЛ[^\n]{0,80}по желанию", re.I),
    "empty archive recorded as «снимков нет»": re.compile(r"снимков нет", re.I),
    "guardrails": re.compile(r"guardrail", re.I),
    "question of mass": re.compile(r"масс[аеуы]", re.I),
    "question of distance": re.compile(r"дистанци", re.I),
    "question of polarity": re.compile(r"полярност", re.I),
    "«?» when there are no data": re.compile(r"«\?»"),
    "lawsuits as an activity marker": re.compile(r"маркер[а-я]* активности", re.I),
    "no payment-discipline conclusions": PAYMENT_BAN,
    "hidden databases forbidden": re.compile(r"скрыт[а-я]* баз", re.I),
    "illegal parsing forbidden": re.compile(r"парсинг", re.I),
    "case with over 100 wholesale buyers": CASE["over 100 wholesale buyers"],
}
GAMMA_FIELDS = ("SLIDE_TEXT", "IMAGE_PROMPT", "FOOTER_LINKS")
GAMMA_SLIDES = 33
# The founder fixed titles 1, 2 and 9–11 in #675; #677 keeps them.
GAMMA_TITLES = {
    1: "Введение: от вероятностного мониторинга влияния к имиджу",
    2: "Лектор: профессиональная оптика и границы метода",
    9: "От теории к практике МСП: GRA как guardrails (ограничители) для ИИ, а не формула",
    10: "Четыре дня: Вижу → Собираю → Выбираю → Действую",
    11: "Маршрут вечера: цель дня и вход в работу",
}
# Slides 3–8 repeat Gamma pages 2, 3, 4, 6, 7, 9 without changes; pages 5 and 8 are left out.
GAMMA_PAGES = {
    3: ("АРХИТЕКТУРА ВОСПРИЯТИЯ", "Репутация — это система сигналов", "Доверие складывается из сигналов, а не из деклараций",
        "КОНТУР 01", "Медиа и инфополе", "КОНТУР 02", "Стейкхолдеры и общество", "КОНТУР 03", "Рынки и инвесторы",
        "КОНТУР 04", "Поведение и культура"),
    4: ("ПРИНЦИП СООТВЕТСТВИЯ", "Обещаемое должно совпадать с подтверждаемым",
        "Нельзя обещать больше, чем способна подтвердить практика", "ЧТО МЫ ОБЕЩАЕМ", "Ясный вектор",
        "ЧЕМ ПОДТВЕРЖДАЕМ", "Твёрдая база"),
    5: ("МЕТОДОЛОГИЯ ЦИКЛА", "Три контура управления репутацией", "Цикл работает, только когда каждый этап подтверждён",
        "ЭТАП 01", "Диагностика", "ЭТАП 02", "Настройка", "ЭТАП 03", "Доказательство"),
    6: ("НАКОПЛЕНИЕ ДОВЕРИЯ", "Сильная позиция собирается из повторяемых сигналов",
        "Повторяемость сильнее разовых громких кампаний", "Единый смысловой центр", "Синхронный язык каналов",
        "Проверяемые действия", "Ритм подтверждений"),
    7: ("ФОКУСИРОВКА СООБЩЕНИЙ", "Карта стейкхолдеров показывает, где нужна точность",
        "Одно сообщение — разные критерии проверки", "ГРУППА 01 · ИНВЕСТОРЫ И СОВЕТ", "ГРУППА 02 · КЛИЕНТЫ И ПОЛЬЗОВАТЕЛИ",
        "ГРУППА 03 · РЕГУЛЯТОРЫ И ОТРАСЛЬ", "ГРУППА 04 · КОМАНДА И РЫНОК ТРУДА"),
    8: ("МЕТРИКИ УСТОЙЧИВОСТИ", "Измерять нужно не шум, а устойчивость доверия", "Ценен не шум, а устойчивое доверие",
        "ВЫВОД АНАЛИТИКИ", "Охваты не равны лояльности"),
}
GAMMA_EXCLUDED = ("АНАЛИЗ УЯЗВИМОСТЕЙ", "ПРЕВЕНТИВНЫЙ КОНТРОЛЬ", "безопасными полями")
GAMMA_HEADER = "Введение в репутационный инжиниринг · Репутационный инжиниринг: ключевые составляющие"
GAMMA_FOOTER = "· (Telegram) @gulienko @qwen-3.7plus @claudeopus-5.5 · Москва, 10.2026"
# #677: the slides carry no air time, no format and no day counter; only the city and the month stay in the footer.
AIR_TIME = re.compile(r"(?<![\d.])\d{1,2}[.:]\d{2}(?![\d.])|онлайн|День 1 из 4|10–11\.2026|\d{1,2} октябр", re.I)
SLOGAN = "Управляйте данными о связях — или стратегию за вас выберет случай"
INDICES_QUOTE = "Помните слайд с индексами?"
# Контекст → Цель → Действие: every slide written for #677 (all but the verbatim Gamma pages) explains itself without the lecturer.
FRAME = {
    "intro paragraph": re.compile(r"^- Вводный абзац: \S", re.M),
    "«КОНТЕКСТ» card": re.compile(r"^- Карточка: \d\d · КОНТЕКСТ — \S", re.M),
    "«ЦЕЛЬ», «ПРОБЛЕМА», «ВОПРОС» or «ГРАНИЦЫ» card": re.compile(r"^- Карточка: \d\d · (?:ЦЕЛЬ|ПРОБЛЕМА|ВОПРОС|ГРАНИЦЫ) — \S", re.M),
    "«РЕШЕНИЕ» or «ДЕЙСТВИЕ» card": re.compile(r"^- Карточка: \d\d · (?:РЕШЕНИЕ|ДЕЙСТВИЕ) — \S", re.M),
    "conclusion": re.compile(r"^- Вывод: \S", re.M),
}
CASE_LABEL = "УЧЕБНЫЙ КЕЙС"
VOTE, TRIAL = "🗳", "🤖"
GAMMA_VOTES, GAMMA_TRIALS = {13, 22}, {24}
SPEECH_WORDS = (150, 180)
SPEECH_MARKS = ("[ПАУЗА]", "[ДЕМОНСТРАЦИЯ ЭКРАНА]", "[ЮМОР/РАЗРЯДКА]")
MARKS_MIN = 3
NGRAM = 8
SCRIPT_SECTIONS = ("Как читать сценарий", "Перед эфиром", "Тайминг и План Б", "Речь к слайдам",
                   "Приложение А. Промпт-фреймер для чата")
RESEARCH_SECTIONS = ("Шаг 4. Итоговый промпт", "Шаг 5. Полный результат поиска", "Шаг 6. Выжимка и разбор по GRA")
RESEARCH_TERMS = ("VERIFIED", "PARTIAL", "CONFLICT", "масса", "дистанция", "полярность")
GATE = ("Мета-анализ.", "Исследование лектора.", "Презентация.", "Сценарий.", "Контекст → Цель → Действие.",
        "Слайды 3–8 вербатим.", "Кейс 1, GRA и иски.", "Подвал.", "Без апелляций к числу слайдов.")
STANDARD_PHRASES = ("«Слайды 1-4, 6-7, 9: взять из PDF Gamma вербатим»", "**Признание.**", INDICES_QUOTE, SLOGAN,
                    "check-day1-677.py --self-test")


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


def slides(text):
    matches = list(SLIDE.finditer(text))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        tail = re.search(r"^#{1,3} ", text[match.end():end], re.M)
        yield int(match[1]), match[2], text[match.end():match.end() + tail.start() if tail else end]


def gamma_field(chunk, name):
    match = re.search(r"\*\*\[" + name + r"\]\*\*[^\n]*\n(.*?)(?=\n\*\*\[[A-Z_]+\]\*\*|\Z)", chunk, re.S)
    return match[1].strip() if match else None


def words(text):
    return len([token for token in text.split() if re.search(r"\w", token)])


def tokens(text):
    return re.findall(r"\w+", text.lower())


def ngrams(text):
    found = tokens(text)
    return {tuple(found[i:i + NGRAM]) for i in range(len(found) - NGRAM + 1)}


def heading(text, title):
    return re.search(r"^## " + re.escape(title) + r"\s*$", text, re.M) is not None


def prompt_block(script):
    match = re.search(r"^### А\.2\. Текст промпта\n+```text\n(.*?)\n```", script, re.S | re.M)
    return match[1] if match else ""


def stop_words(name, text, clean):
    """Stop lists of the deck and the script; clean is the prose with verbatim Gamma wording removed."""
    errors = []
    for label, pattern in STOP_LISTS:
        for match in sorted(set(pattern.findall(clean)))[:3]:
            errors.append(f"{name}: {label}: «{match}»")
    for match in sorted(set(RAW_INCOMING.findall(text)))[:3]:
        errors.append(f"{name}: incoming price request plot: «{match}»")
    for match in SLIDE_LIMIT.findall(clean)[:1]:
        errors.append(f"{name}: appeal to the number of slides: «{match}»")
    for sentence in re.split(r"(?<=[.!?])\s+|\n", clean):
        if PAYMENT.search(sentence) and not NEGATION.search(sentence):
            errors.append(f"{name}: payments discussed without a prohibition: «{sentence.strip()[:90]}»")
            break
    if OLD_CASE.search(clean):
        errors.append(f"{name}: case 1 still counts «100 магазинов» instead of over 100 wholesale buyers")
    return errors


def exempt(text):
    clean = prose(text)
    for phrase in GAMMA_VERBATIM:
        clean = clean.replace(phrase, "")
    return clean


def validate_gamma(texts):
    errors, text, name = [], texts[GAMMA], GAMMA.name
    clean = exempt(text)
    errors += stop_words(name, text, clean)
    for phrase in (GAMMA_HEADER, SLOGAN, CASE_LABEL):
        if phrase not in text:
            errors.append(f"{name}: required phrase missing: «{phrase}»")
    for phrase in GAMMA_EXCLUDED + ("SPEAKER_NOTES",):
        if phrase in text:
            errors.append(f"{name}: excluded wording present: «{phrase}»")
    if "## Как читать" not in text:
        errors.append(f"{name}: section «Как читать» missing")
    deck = list(slides(text))
    if [n for n, _, _ in deck] != list(range(1, GAMMA_SLIDES + 1)):
        errors.append(f"{name}: slides are not 1–{GAMMA_SLIDES}: {[n for n, _, _ in deck][:40]}")
    for n, title, chunk in deck:
        if n in GAMMA_TITLES and title != GAMMA_TITLES[n]:
            errors.append(f"{name}: slide {n} title is not the founder's: «{title}»")
        if n > 11 and words(title.replace(VOTE, "").replace(TRIAL, "")) > 6:
            errors.append(f"{name}: slide {n} title longer than 6 words: «{title}»")
        values = {key: gamma_field(chunk, key) for key in GAMMA_FIELDS}
        for key, value in values.items():
            if not value:
                errors.append(f"{name}: slide {n} field missing or empty: [{key}]")
        screen, image, footer = (values[key] or "" for key in GAMMA_FIELDS)
        if screen and f"- Шапка: {GAMMA_HEADER}" not in screen:
            errors.append(f"{name}: slide {n} has no common header")
        if screen and f"- Заголовок: {title}" not in screen and f"- Подзаголовок: {title}" not in screen:
            errors.append(f"{name}: slide {n} on-screen title differs from the heading")
        for found in sorted(set(AIR_TIME.findall(screen + "\n" + footer)))[:2]:
            errors.append(f"{name}: slide {n} shows air time or format: «{found}»")
        if n not in GAMMA_PAGES:
            for label, pattern in FRAME.items():
                if not pattern.search(screen):
                    errors.append(f"{name}: slide {n} has no {label} (Контекст → Цель → Действие)")
        for phrase in GAMMA_PAGES.get(n, ()):
            if phrase not in screen:
                errors.append(f"{name}: slide {n} lost Gamma wording: «{phrase}»")
        if image and (re.search(r"[а-яё]", image, re.I) or not re.search(r"gold|amber", image, re.I)
                      or "16:9" not in image or "no readable text" not in image.lower()):
            errors.append(f"{name}: slide {n} image prompt is not English with a gold accent, 16:9 and no readable text")
        if footer and not (re.search(r"\]\(https://[^)\s]+\)", footer) and footer.endswith(GAMMA_FOOTER)):
            errors.append(f"{name}: slide {n} footer has no full URL or does not end with «{GAMMA_FOOTER}»")
        for mark in sorted(set(re.findall(r"\^\[\d+\]", screen))):
            if mark not in footer:
                errors.append(f"{name}: slide {n} footnote {mark} has no source in [FOOTER_LINKS]")
    chunks = {n: prose(chunk) for n, _, chunk in deck}
    for n, group, patterns in ((12, "case fact", CASE), (20, "node", NODES), (23, "openness marker", MARKERS),
                               (33, "ethics boundary", ETHICS)):
        for label, pattern in patterns.items():
            if not pattern.search(chunks.get(n, "")):
                errors.append(f"{name}: slide {n} {group} missing: {label}")
    for n in (12, 13, 20, 23, 24):
        if CASE_LABEL not in chunks.get(n, ""):
            errors.append(f"{name}: slide {n} of case 1 is not marked «{CASE_LABEL}»")
    if "guardrail" not in chunks.get(9, ""):
        errors.append(f"{name}: slide 9 does not present GRA as guardrails")
    votes = {n for n, title, _ in deck if VOTE in title}
    trials = {n for n, title, _ in deck if TRIAL in title}
    if votes != GAMMA_VOTES or trials != GAMMA_TRIALS:
        errors.append(f"{name}: votes {sorted(votes)} and prompt trials {sorted(trials)}, expected {sorted(GAMMA_VOTES)} and {sorted(GAMMA_TRIALS)}")
    return errors


def validate_script(texts):
    errors, text, name = [], texts[SCRIPT], SCRIPT.name
    clean = exempt(re.sub(r"```.*?```", "", text, flags=re.S))
    errors += stop_words(name, text, clean)
    for title in SCRIPT_SECTIONS:
        if not heading(text, title):
            errors.append(f"{name}: section «{title}» missing")
    deck = {n: (title, gamma_field(chunk, "SLIDE_TEXT") or "") for n, title, chunk in slides(texts[GAMMA])}
    screen = ngrams(" ".join(value for _, value in deck.values()))
    body = text.split("\n## Приложение", 1)[0]
    speech = list(slides(body))
    if [n for n, _, _ in speech] != list(range(1, GAMMA_SLIDES + 1)):
        errors.append(f"{name}: speeches are not 1–{GAMMA_SLIDES}: {[n for n, _, _ in speech][:40]}")
    for n, title, chunk in speech:
        if deck.get(n, ("",))[0] != title:
            errors.append(f"{name}: slide {n} title differs from the deck: «{title}»")
        spoken = re.sub(r"\[[^\]]*\]", " ", chunk)
        if not SPEECH_WORDS[0] <= words(spoken) <= SPEECH_WORDS[1]:
            errors.append(f"{name}: slide {n} speech has {words(spoken)} words, expected {SPEECH_WORDS[0]}–{SPEECH_WORDS[1]}")
        if not ("потому что" in chunk.lower() and "поэтому" in chunk.lower()):
            errors.append(f"{name}: slide {n} speech has no «потому что… поэтому…» bridge")
        copied = ngrams(spoken) & screen
        if copied:
            errors.append(f"{name}: slide {n} speech repeats the slide text: «{' '.join(sorted(copied)[0])}»")
        if n == 8 and INDICES_QUOTE not in chunk:
            errors.append(f"{name}: the indices quote is not spoken on slide 8")
    for mark in SPEECH_MARKS:
        if body.count(mark) < MARKS_MIN:
            errors.append(f"{name}: mark {mark} used {body.count(mark)} times, expected at least {MARKS_MIN}")
    plan_b = {n for n, _, chunk in speech if "План Б" in chunk}
    if not GAMMA_VOTES | GAMMA_TRIALS <= plan_b:
        errors.append(f"{name}: no «План Б» in the speeches of slides {sorted(GAMMA_VOTES | GAMMA_TRIALS - plan_b)}")
    prompt = prompt_block(text)
    if not prompt:
        errors.append(f"{name}: section «А.2. Текст промпта» with a text block missing")
    for label, pattern in PROMPT_RULES.items():
        if prompt and not pattern.search(prompt):
            errors.append(f"{name}: Промпт-фреймер rule missing: {label}")
    return errors


def validate(texts):
    missing = [path for path in FILES if not texts[path]]
    errors = [f"{path.name}: file not found" for path in missing]
    if missing:
        return errors
    for path in FILES:
        text, name = texts[path], path.name
        if frontmatter(text).get("source", "").strip('"') != SOURCE:
            errors.append(f"{name}: frontmatter source is not issue #677")
        relative = [url for url in LINK.findall(text) if not re.match(r"https?://", url)]
        if relative:
            errors.append(f"{name}: links are not full URLs: {relative[:3]}")
        errors += [f"{name}: {error}" for error in broken_links(text, texts)]
    errors += validate_gamma(texts)
    errors += validate_script(texts)
    research = texts[RESEARCH]
    for title in RESEARCH_SECTIONS:
        if not heading(research, title):
            errors.append(f"{RESEARCH.name}: section «{title}» missing")
    for term in RESEARCH_TERMS:
        if term not in research:
            errors.append(f"{RESEARCH.name}: term missing: {term}")
    standard = texts[STANDARD]
    for item in GATE:
        if f"- [x] **{item}**" not in standard:
            errors.append(f"{STANDARD.name}: gate rule missing or not checked: «{item}»")
    for phrase in STANDARD_PHRASES:
        if phrase not in standard:
            errors.append(f"{STANDARD.name}: required phrase missing: «{phrase}»")
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
    g, s, r, d = GAMMA, SCRIPT, RESEARCH, STANDARD
    speech8 = r"(## Речь к слайдам.*?### Слайд 8\. [^\n]+\n)"
    broken = {
        "deck file missing": mutate_re(texts, g, r".*", "", count=1),
        "deck slide removed": mutate_re(texts, g, r"^### Слайд 33\. .*?(?=^## |\Z)", ""),
        "speaker notes back in the deck": mutate(texts, g, "**[IMAGE_PROMPT]**", "**[SPEAKER_NOTES]**\nРечь.\n\n**[IMAGE_PROMPT]**"),
        "deck field missing": mutate(texts, g, "**[FOOTER_LINKS]**", "**Ссылки**"),
        "common header lost": mutate(texts, g, "- Шапка: " + GAMMA_HEADER, "- Шапка: Репутационный инжиниринг"),
        "air time in a footer": mutate(texts, g, "· Москва, 10.2026", "· онлайн, 20:00 · Москва, 10.2026"),
        "day counter on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: День 1 из 4. "),
        "old footer dates": mutate(texts, g, "Москва, 10.2026", "Москва, 10–11.2026", count=-1),
        "Telegram lost in a footer": mutate(texts, g, "(Telegram) @gulienko", "@gulienko"),
        "Gamma page text edited": mutate(texts, g, "Репутация — это система сигналов", "Репутация — это сигналы", count=-1),
        "Gamma excluded page added": mutate(texts, g, "\n## Слайды", "\nАНАЛИЗ УЯЗВИМОСТЕЙ\n\n## Слайды"),
        "founder title edited": mutate(texts, g, "### Слайд 10. Четыре дня", "### Слайд 10. Пять дней"),
        "slogan lost": mutate(texts, g, SLOGAN, "Репутацией управляет тот, кто громче говорит", count=-1),
        "third vote": mutate_re(texts, g, r"^### Слайд 14\. ", "### Слайд 14. 🗳 "),
        "long title": mutate_re(texts, g, r"^(### Слайд 30\. )([^\n]+)", r"\1\2 и ещё много лишних слов"),
        "КОНТЕКСТ card missing": mutate_re(texts, g, r"(### Слайд 15\..*?)· КОНТЕКСТ —", r"\1· ФОН —"),
        "goal card missing": mutate_re(texts, g, r"(### Слайд 1\..*?)· (?:ЦЕЛЬ|ПРОБЛЕМА|ВОПРОС|ГРАНИЦЫ) —", r"\1· ИТОГ —"),
        "action card missing": mutate_re(texts, g, r"(### Слайд 26\..*?)· (?:РЕШЕНИЕ|ДЕЙСТВИЕ) —", r"\1· ИТОГ —"),
        "intro paragraph missing": mutate_re(texts, g, r"(### Слайд 31\..*?)- Вводный абзац: [^\n]*\n", r"\1"),
        "conclusion missing": mutate_re(texts, g, r"(### Слайд 2\..*?)- Вывод: [^\n]*\n", r"\1"),
        "case label lost": mutate_re(texts, g, r"(### Слайд 20\..*?)УЧЕБНЫЙ КЕЙС", r"\1КЕЙС"),
        "producer no longer writes first": mutate_re(texts, g, r"^### Слайд 12\..*?(?=^### Слайд 13)", lambda m: re.sub(r"пишет первым|написать им первыми", "ждёт письма", m[0])),
        "«100 магазинов» case": mutate(texts, g, "более 100 оптовых покупателей", "около 100 магазинов"),
        "node missing on slide 20": mutate_re(texts, g, r"^### Слайд 20\..*?(?=^### Слайд 21)", lambda m: re.sub(r"(?i)дистрибьютор[а-я]* «Д»", "партнёр", m[0])),
        "lawsuits beyond an activity marker": mutate_re(texts, g, r"(### Слайд 23\..*?)маркер[а-я]* активности", r"\1признак"),
        "ethics boundary missing": mutate_re(texts, g, r"(### Слайд 33\..*?)парсинг", r"\1сбор"),
        "formula on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: Сила связи считается по формуле F(t). "),
        "H1 on a slide": mutate(texts, g, "- Вывод: ", "- Вывод: Гипотеза H1. "),
        "risk word outside the verbatim page": mutate(texts, g, "- Вывод: ", "- Вывод: Новый поставщик — это риск. "),
        "incoming price request": mutate(texts, g, "- Вывод: ", "- Вывод: Сеть «Х» прислала запрос цен. "),
        "payment-discipline conclusion": mutate(texts, g, "- Вывод: ", "- Вывод: Иски показывают, как сеть платит поставщикам. "),
        "appeal to the number of slides": mutate(texts, g, "- Вывод: ", "- Вывод: Сократите колоду до 10 слайдов. "),
        "image prompt in Russian": mutate_re(texts, g, r"(\*\*\[IMAGE_PROMPT\]\*\*[^\n]*\n)", r"\1Иллюстрация. "),
        "footnote without source": mutate(texts, g, "- Вывод: ", "- Вывод: Цитата ^[9]. "),
        "script file missing": mutate_re(texts, s, r".*", "", count=1),
        "speech removed": mutate_re(texts, s, r"^### Слайд 33\. .*?(?=^## )", ""),
        "speech title differs": mutate_re(texts, s, r"^### Слайд 14\. [^\n]+", "### Слайд 14. Кто решает"),
        "speech too short": mutate_re(texts, s, r"(### Слайд 5\. [^\n]+\n\n)[^\n]+\n", r"\1"),
        "speech too long": mutate_re(texts, s, r"(### Слайд 6\. [^\n]+\n)", r"\1" + "слово " * 40 + "\n"),
        "bridge removed": mutate_re(texts, s, r"(### Слайд 20\..*?)[Пп]оэтому(.*?### Слайд 21)", r"\1и\2", count=0),
        "mark removed": mutate(texts, s, "[ДЕМОНСТРАЦИЯ ЭКРАНА]", "", count=-1),
        "План Б lost on slide 22": mutate_re(texts, s, r"(## Речь к слайдам.*?### Слайд 22\..*?)План Б(.*?### Слайд 23)", r"\1запасной ход\2", count=0),
        "indices quote lost": mutate_re(texts, s, speech8 + r"(.*?)«Помните слайд с индексами\?»", r"\1\2«Помните индексы?»"),
        "slide text copied into the speech": mutate_re(texts, s, r"(### Слайд 13\. [^\n]+\n\n)",
                                                       r"\1Производитель выбрал сеть «Х» и готовит первое письмо категорийному менеджеру. "),
        "timing section lost": mutate(texts, s, "## Тайминг и План Б", "## Тайминг"),
        "prompt Wayback lost": mutate(texts, s, "web.archive.org", "example.org", count=-1),
        "prompt payment ban lost": mutate_re(texts, s, r"платёжн[а-я]* дисциплин[а-я]*", "надёжности", count=0),
        "risk rhetoric in the speech": mutate(texts, s, "\n## Перед эфиром", "\nКаждый новый партнёр — это риск.\n\n## Перед эфиром"),
        "price request even in a quote": mutate(texts, s, "\n## Перед эфиром", "\n> Сеть сделала запрос цен.\n\n## Перед эфиром"),
        "research file missing": mutate_re(texts, r, r".*", "", count=1),
        "research search result lost": mutate(texts, r, "## Шаг 5. Полный результат поиска", "## Шаг 5. Результат"),
        "research GRA breakdown lost": mutate(texts, r, "полярность", "знак", count=-1),
        "standard file missing": mutate_re(texts, d, r".*", "", count=1),
        "gate rule removed": mutate_re(texts, d, r"^- \[x\] \*\*Кейс 1, GRA и иски\.\*\*[^\n]*\n", ""),
        "gate rule unchecked": mutate(texts, d, "- [x] **Подвал.**", "- [ ] **Подвал.**"),
        "distortion statement lost": mutate(texts, d, "«Слайды 1-4, 6-7, 9: взять из PDF Gamma вербатим»", "«слайды из PDF»"),
        "acknowledgement lost": mutate(texts, d, "**Признание.**", "**Итог.**"),
        "relative link": mutate(texts, g, "](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/", "](../"),
        "broken anchor": mutate(texts, g, "#тайминг-и-план-б", "#тайминг", count=-1),
        "source not #677": mutate(texts, s, SOURCE, "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/675"),
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
    print(f"PASS: deck has {GAMMA_SLIDES} slides with three fields (no speaker notes), the common header, founder titles 1, 2, 9–11, Gamma pages 2, 3, 4, 6, 7, 9 unchanged on slides 3–8, the slogan, votes 13 and 22, trial 24")
    print("PASS: every new slide has an intro paragraph, a «КОНТЕКСТ» card, a goal / problem / question / limits card, a solution / action card and a conclusion (Контекст → Цель → Действие)")
    print("PASS: footers carry full URLs, Telegram and «Москва, 10.2026» with no air time, format or day counter; image prompts are English, 16:9, gold, without readable text")
    print("PASS: case 1 is marked «УЧЕБНЫЙ КЕЙС», the producer has over 100 wholesale buyers and writes first; 8 nodes on slide 20, openness markers and lawsuits as an activity marker on slide 23, ethics on slide 33; no formula/F(t)/H1, trigger, risk, provocation, price request or slide-count appeal")
    print(f"PASS: script speaks slides 1–{GAMMA_SLIDES} under the deck titles in {SPEECH_WORDS[0]}–{SPEECH_WORDS[1]} words with a «потому что → поэтому» bridge, no {NGRAM}-word repeat of the slide text, each mark at least {MARKS_MIN} times, План Б on 13, 22, 24, the indices quote on slide 8 and the full Промпт-фреймер")
    print("PASS: lecturer research keeps the final prompt, the full search result and the GRA breakdown; the gate document lists the nine checked rules, the distortion and the acknowledgement; repository links resolve")
    if args.self_test:
        print(f"PASS: {fixtures} broken fixtures rejected")


if __name__ == "__main__":
    main()
