#!/usr/bin/env python3
"""Check issue #699: the Couturier Constructor file of Day 4 v5 image prompts covers every slide of the v5 deck with Variant А
«Гармония» and Variant Б «Эклектика», each in [EN] and [RU]; 26 couturiers of the issue appear on exactly two slides each; cities
come from the pool of the issue plus Mumbai, at most twice, with neighbouring variants in different cultural zones and never three
European cities in a row; subject types and motions never repeat on neighbouring variants; every prompt keeps the proportion frame
in words, a real city, the couturier, two base colours on the clothing before the art object and the third one on it, gold #B89B5E
on the person, a moderate varied crowd in bokeh, a complex art object, at least three markers of the house, the season, and none of
the banned words; [RU] keeps the HEX codes, the Latin city and house names and the Art Deco term."""
import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOMAIN = ROOT / "research/reputation-technologies"
PROMPTS = DOMAIN / "2026-11-03-day4-image-prompts-v5-couturier-constructor.md"
DECK = DOMAIN / "2026-11-03-day4-presentation-gamma-v5.md"
FILES = (PROMPTS, DECK)
ISSUE = "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/699"
TITLE = "# День 4 · Промпты для изображений (Версия 5 · Couturier Constructor)"
VARIANTS = {"А": ("Гармония", "Always recognisable Art Deco in {city}.", "Всегда узнаваемое Ар-Деко в {loc}."),
            "Б": ("Эклектика", "Surreal-meets-classical eclecticism.", "Сюрреалистичная эклектика.")}
EN_START, RU_START = "Tall narrow vertical banner photograph", "Высокий вертикальный баннер"
BASE = ("#16181D", "#132A4A", "#0A4D3C", "#720E1E")
GOLD = "#B89B5E"
SEASONS = ("FW 2026/27", "SS 2027")
MAX_CHARS = 4000  # DALL-E 3 prompt limit; Midjourney and Nano Banana take more
MIN_WORDS = {"EN": 280, "RU": 240}
# Cultural zone of every city: the pool of §5.1 plus Mumbai (South Asia) to fill 54 variants with each city at most twice.
ZONE = {"Tokyo": "Восточная Азия", "Shanghai": "Восточная Азия", "Seoul": "Восточная Азия", "Mumbai": "Южная Азия",
        "Istanbul": "Западная Азия", "Dubai": "Западная Азия", "Cairo": "Северная Африка", "Marrakesh": "Северная Африка",
        "New York": "Северная Америка", "Buenos Aires": "Латинская Америка", "Mexico City": "Латинская Америка",
        "Rio de Janeiro": "Латинская Америка", "Stockholm": "Северная Европа", "Helsinki": "Северная Европа",
        "Oslo": "Северная Европа", "Copenhagen": "Северная Европа", "London": "Западная Европа", "Paris": "Западная Европа",
        "Amsterdam": "Западная Европа", "Brussels": "Западная Европа", "Berlin": "Центральная Европа",
        "Vienna": "Центральная Европа", "Prague": "Центральная Европа", "Lisbon": "Южная Европа", "Athens": "Южная Европа",
        "Rome": "Южная Европа", "Milan": "Южная Европа"}
# Locative of the city for the [RU] ending of Variant А.
LOCATIVE = {"Paris": "Париже", "Mexico City": "Мехико", "Stockholm": "Стокгольме", "Marrakesh": "Марракеше",
            "Amsterdam": "Амстердаме", "Seoul": "Сеуле", "Rome": "Риме", "Mumbai": "Мумбаи", "Berlin": "Берлине",
            "Rio de Janeiro": "Рио-де-Жанейро", "Tokyo": "Токио", "Athens": "Афинах", "London": "Лондоне", "Dubai": "Дубае",
            "Oslo": "Осло", "Milan": "Милане", "New York": "Нью-Йорке", "Brussels": "Брюсселе", "Cairo": "Каире",
            "Vienna": "Вене", "Helsinki": "Хельсинки", "Shanghai": "Шанхае", "Prague": "Праге", "Lisbon": "Лиссабоне",
            "Buenos Aires": "Буэнос-Айресе", "Istanbul": "Стамбуле", "Copenhagen": "Копенгагене"}
SUBJECT = {"W": ("one woman", "одна женщина"), "M": ("one man", "один мужчина"), "MF": ("a man and a woman", "мужчина и женщина"),
           "WW": ("two women", "две женщины"), "MM": ("two men", "двое мужчин")}
MOTIONS = ("lookback", "profile-left", "profile-right", "diagonal-in", "diagonal-out", "pivot", "stairs", "facing", "toward",
           "crossing", "lead")
PAIR_MOTIONS = ("facing", "toward", "crossing", "lead")
# Country of the brand and at least three markers of its house DNA (§5.3), as [EN] and [RU] regular expressions.
HOUSES = {
    "Balenciaga": ("Испания · Франция",
                   r"exaggerated shoulder|hyperbolic shoulder|cocoon|architectural volume|hourglass|funnel neck|balloon|minimalist drama",
                   r"гиперболизированн\w* плеч|кокон|архитектурн\w* объём|песочн\w* час|воротник\w*-воронк|баллон|минималистичн\w* драм"),
    "Dior": ("Франция", r"Bar jacket|New Look|structured bodice|tulle|organza|floral|cannage|toile de Jouy",
             r"Bar|New Look|структурированн\w* (?:лиф|корсаж)|тюл|органз|цветочн|каннаж|туаль де Жуи"),
    "Chanel": ("Франция", r"tweed|chain|pearl|two-tone|slingback|camellia|quilted|2\.55|cardigan|braid trim",
               r"твид|цеп|жемчу|двухцветн|слингбэк|камели|стёган|кардиган|тесьм"),
    "Valentino": ("Италия", r"pink|lace|train|cape|Rockstud|taffeta", r"розов|кружев|шлейф|кейп|накидк|Rockstud|тафт"),
    "Prada": ("Италия", r"nylon|triangle logo|triangular logo|eyewear|glasses|proportion|intellectual minimalism|kitten heel|Saffiano",
              r"нейлон|треугольн|очк|пропорци|интеллектуальн\w* минимализм|kitten heel|сафьян"),
    "Loewe": ("Испания", r"leather|craft|Puzzle|organic|playful|raffia|basket|trompe-l'oeil|anagram|marquetry",
              r"кож|ремесл|пазл|Puzzle|органическ|игрив|рафи|тромплёй|анаграм|маркетри"),
    "Bottega Veneta": ("Италия", r"intrecciato|intarsia|monochrome|logo-free|without logos|quiet luxury|knot|Andiamo|Cassette",
                       r"intrecciato|интарси|монохром|без логотип|тих\w* роскош|узел|узл|Andiamo|Cassette"),
    "Saint Laurent": ("Франция", r"le smoking|tuxedo|strict black|jet black|stiletto|heel|rock-chic|satin lapel|pussy-bow|sheer|saharienne",
                      r"смокинг|строг\w* чёрн|шпильк|каблук|рок-шик|атласн\w* лацкан|бант|прозрачн|сафари"),
    "Celine": ("Франция", r"Parisian chic|straight line|slim|Triomphe|restraint|basics|Chelsea boot|bourgeois|Crombie",
               r"парижск\w* шик|прям\w* лини|слим|узк|Triomphe|сдержанн|базов|челси|буржуазн"),
    "Hermès": ("Франция", r"equestrian|horse|carré|silk scarf|cashmere|earth tone|saddle stitch|sellier|Kelly|Birkin|Clou de Selle|Chaîne d'Ancre|riding",
               r"конн|лошад|карре|платок|кашемир|землист|седельн\w* шов|Kelly|Birkin|Clou de Selle|Chaîne d'Ancre|верхов"),
    "Louis Vuitton": ("Франция", r"trunk|travel|Damier|Monogram|technical fabric|bright pattern|Keepall|Speedy|Petite Malle",
                      r"сундук|кофр|путешеств|Damier|Monogram|технологичн\w* ткан|ярк\w* узор|Keepall|Speedy|Petite Malle"),
    "Gucci": ("Италия", r"maximalis|vintage|print|bohemian|horsebit|Web stripe|Flora|bamboo|Jackie|Rosso Ancora",
              r"максимализм|винтаж|принт|богемн|Horsebit|Web|Flora|бамбук|Jackie|Rosso Ancora"),
    "Fendi": ("Италия", r"\bFF\b|Zucca|faux fur|eco-fur|Roman|duality|Baguette|Peekaboo|Selleria",
              r"\bFF\b|Zucca|эко-мех|искусственн\w* мех|римск|двойствен|Baguette|Peekaboo|Selleria"),
    "Versace": ("Италия", r"baroque|Barocco|Greek key|meander|Greca|Medusa|metallic|metal mesh|sensual|safety pin",
                r"барокко|меандр|Greca|Медуз|металлик|металлическ\w* сетк|чувствен|английск\w* булавк"),
    "Armani Privé": ("Италия", r"fluid|sheen|shimmer|lustre|soft shoulder|unstructured|evening grace|greige|crystal|velvet",
                     r"текуч|блеск|мерцани|мягк\w* плеч|вечерн\w* грац|грейдж|кристалл|бархат"),
    "Givenchy": ("Франция", r"gothic|clean line|archive|Hubert|Bettina|4G|padlock|Antigona|little black dress",
                 r"готич|чист\w* лини|архив|Bettina|4G|замок|замк|Antigona"),
    "Maison Margiela": ("Франция", r"deconstruct|white stitch|anonymity|anonymous|theatr|Tabi|Artisanal|bianchetto|Glam Slam",
                        r"деконструк|бел\w* стежк|аноним|театр|Tabi|Artisanal|bianchetto|Glam Slam"),
    "Rick Owens": ("США · Франция", r"floor-length|hood|post-apocalyptic|romanticism|Geobasket|Kiss boot|platform|dust|milk|chalk",
                   r"в пол|удлинённ|капюшон|постапокалипт|романтизм|Geobasket|платформ|пыльн|молочн|мелов"),
    "Thom Browne": ("США", r"shrunken|grey wool|grey flannel|grosgrain|cropped|four-bar|wingtip|brogue|Hector|collegiate|red lining",
                    r"укорочен|сер\w* (?:шерст|фланел)|репсов|grosgrain|четыр\w* полос|броги|Hector|колледж|красн\w* подкладк"),
    "Jil Sander": ("Германия", r"minimalis|pure colour|perfect fit|precise|poplin|gabardine|Tangle",
                   r"минимализм|чист\w* цвет|идеальн\w* посадк|поплин|габардин|Tangle"),
    "The Row": ("США", r"quiet|silence|cashmere|vicuña|double-faced|loose|relaxed|invisible luxury|Margaux|tonal|logo-free",
                r"тишин|тих|кашемир|викунь|двусторонн|свободн\w* кро|незаметн\w* роскош|Margaux|тон-в-тон|без логотип"),
    "Alaïa": ("Франция", r"knit|cut-out|laser-cut|sculpt|corset belt|fit-and-flare|ballet flat|Le Cœur",
              r"трикотаж|вырез|лазерн\w* перфорац|скульпт|корсетн\w* пояс|расклешён|балетк|Le Cœur"),
    "Schiaparelli": ("Франция", r"surreal|anatomical|ear-shaped|eye-shaped|keyhole|theatrical|shocking pink|trompe-l'oeil|padlock|lobster",
                     r"сюрреал|анатомическ|замочн\w* скважин|театраль|shocking pink|тромплёй|омар"),
    "Rabanne": ("Франция", r"metal|chainmail|disc|paillette|futuris|radian|1969", r"металл|кольчуг|диск|пайетк|футуризм|сияни|1969"),
    "Jacquemus": ("Франция", r"Provence|Provençal|mini|straw|lightness|airy|play|Chiquito|Bambino|linen",
                  r"Прованс|мини|солом|лёгк|игр|Chiquito|Bambino|лён|льнян"),
    "Coperni": ("Франция", r"technolog|spray-on|Fabrican|sci-fi|clean form|Swipe|aerogel",
                r"технолог|спрей|Fabrican|научн\w* фантастик|чист\w* форм|Swipe|аэрогел"),
}
BANNED = {
    "EN": r"business suit|\bsuits?\b|\boffices?\b|uniform|plain white walls|gloom|\bdark\b|\bshadows?\b|close-up|stock smile|"
          r"\bnight|\bstatues?\b|\bcubes?\b|\bspheres?\b|\bprisms?\b|\bcones?\b|\bpyramids?\b|\bmannequins?\b",
    "RU": r"делов\w* костюм|костюм|офис|униформ|школьн\w* форм|бел\w* стен|мрак|мрачн|тёмн|темн|\bтен(?:ь|и|ей|ям|ями|ях)\b|"
          r"крупн\w* план|стоков\w* улыб|\bноч|стату|\bкуб|\bсфер|призм|\bконус|пирамид|манекен",
}
GENERIC = {"EN": r"\b(?:drap\w*|pleat\w*)", "RU": r"драпир\w*|плиссе\w*|складк\w*"}
FRAME = {"EN": ("one continuous uninterrupted scene", "height far greater than width", "no panels and no borders", "high-key",
                "daylight", "tack-sharp", "serious", "Art Deco"),
         "RU": ("одной непрерывной сцены", "высота намного больше ширины", "без панелей и рамок", "high-key", "дневн", "резк",
                "серьёзн", "Ар-Деко")}
AGE = {"EN": r"aged (?:3\d|4\d|50)\b", "RU": r"(?:3\d|4\d|50) (?:лет|года)"}
CROWD = {"EN": (r"\bmoderate", r"\bvaried", r"bokeh", r"passers-by|crowd"),
         "RU": (r"умеренн", r"разнообразн", r"боке", r"прохож|массовк")}
OBJECT = {"EN": "art object", "RU": "арт-объект"}
GOLD_WORD = {"EN": f"Gold {GOLD}", "RU": f"Золото {GOLD}"}
ROW = re.compile(r"^\| (\d+) \| ([АБ]) \| ([^|·]+?) · ([^|]+?) \| ([^|]+?) \| ([^|]+?) \| ([^|]+?) \| (W|M|MF|WW|MM) \| ([a-z-]+) \| "
                 r"(#[0-9A-F]{6}), (#[0-9A-F]{6}) \| (#[0-9A-F]{6}) \| ([^|]+?) \| (FW 2026/27|SS 2027) \|$", re.M)
SECTION = re.compile(r"^## Слайд (\d+)\. (.+)$", re.M)
DECK_SLIDE = re.compile(r"^### Слайд (\d+)\. (.+)$", re.M)
GATE = "\n## Гейт-проверка\n"
DEVIATIONS = "\n## Отклонения от постановки\n"
EUROPE = {city for city, zone in ZONE.items() if zone.endswith("Европа")}


def plan(body):
    """Rows of the distribution table: one per variant, in the order of the slides."""
    keys = ("slide", "variant", "house", "designer", "country", "city", "zone", "type", "motion", "cloth1", "cloth2", "object",
            "object_type", "season")
    rows = [dict(zip(keys, match.groups())) for match in ROW.finditer(body)]
    for row in rows:
        row["slide"] = int(row["slide"])
    return rows


def sections(body):
    """Each `## Слайд N. Title` section up to the next one or the gate."""
    marks = list(SECTION.finditer(body))
    end_all = body.find(GATE) if GATE in body else len(body)
    for i, match in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else end_all
        yield int(match[1]), match[2].strip(), body[match.end():end]


def variants(section):
    """Variant heading, [EN] prompt and [RU] prompt of Variants А and Б of a slide section."""
    found = {}
    for match in re.finditer(r"^### Вариант ([АБ]): (\S+) \(([^\n]+)\)\n\*\*\[EN\]\*\*\n`([^`\n]+)`\n\n\*\*\[RU\]\*\*\n`([^`\n]+)`$",
                             section, re.M):
        found[match[1]] = {"label": match[2], "heading": match[3], "EN": match[4], "RU": match[5]}
    return found


def markers(house, lang, prompt):
    """Distinct markers of the house DNA named in the prompt."""
    pattern = HOUSES[house][1 if lang == "EN" else 2]
    return {match.group(0).lower() for match in re.finditer(pattern, prompt)}


def check_prompt(where, lang, prompt, row):
    errors = []
    start = EN_START if lang == "EN" else RU_START
    ending = VARIANTS[row["variant"]][1 if lang == "EN" else 2].format(city=row["city"], loc=LOCATIVE.get(row["city"], "?"))
    if not prompt.startswith(start):
        errors.append(f"{where}: does not start with «{start}»")
    if not prompt.endswith(ending):
        errors.append(f"{where}: does not end with «{ending}»")
    for phrase in FRAME[lang]:
        if phrase.lower() not in prompt.lower():
            errors.append(f"{where}: frame element «{phrase}» missing")
    if not re.search(AGE[lang], prompt):
        errors.append(f"{where}: age 30–50 of the models not stated")
    city = f"Real {row['city']}," if lang == "EN" else f"({row['city']})"
    if city not in prompt:
        errors.append(f"{where}: city «{city}» of the table missing")
    if row["house"] not in prompt:
        errors.append(f"{where}: couturier {row['house']} not named")
    if row["season"] not in prompt:
        errors.append(f"{where}: season {row['season']} not named")
    subject = SUBJECT[row["type"]][0 if lang == "EN" else 1]
    if subject not in prompt.lower():
        errors.append(f"{where}: subject «{subject}» of type {row['type']} missing")
    hexes = set(re.findall(r"#[0-9A-F]{6}", prompt))
    expected = {row["cloth1"], row["cloth2"], row["object"], GOLD}
    if hexes != expected:
        errors.append(f"{where}: HEX codes {sorted(hexes)} differ from the table {sorted(expected)}")
    anchor = prompt.find(OBJECT[lang])
    if anchor < 0:
        errors.append(f"{where}: no «{OBJECT[lang]}»")
    else:
        for code in (row["cloth1"], row["cloth2"], GOLD_WORD[lang]):
            if not 0 <= prompt.find(code) < anchor:
                errors.append(f"{where}: {code} not on the person before the «{OBJECT[lang]}»")
        if prompt.find(row["object"]) < anchor:
            errors.append(f"{where}: object colour {row['object']} not after the «{OBJECT[lang]}»")
    for pattern in CROWD[lang]:
        if not re.search(pattern, prompt, re.I):
            errors.append(f"{where}: crowd element /{pattern}/ missing")
    banned = re.search(BANNED[lang], prompt, re.I)
    if banned:
        errors.append(f"{where}: banned word «{banned.group(0)}»")
    for sentence in re.split(r"(?<=[.;:])\s", prompt):
        generic = re.search(GENERIC[lang], sentence, re.I)
        if generic and row["house"] not in sentence:
            errors.append(f"{where}: generic «{generic.group(0)}» not tied to {row['house']} in the same sentence")
    found = markers(row["house"], lang, prompt)
    if len(found) < 3:
        errors.append(f"{where}: {len(found)} markers of {row['house']} ({', '.join(sorted(found))}), need at least 3")
    if len(prompt) > MAX_CHARS:
        errors.append(f"{where}: {len(prompt)} characters, more than {MAX_CHARS}")
    if len(prompt.split()) < MIN_WORDS[lang]:
        errors.append(f"{where}: {len(prompt.split())} words, fewer than {MIN_WORDS[lang]}")
    return errors


def named(row, before, after):
    """House with its designer, or the house alone when the designer carries its name (Rick Owens, Thom Browne)."""
    return row["house"] if row["designer"] == row["house"] else f"{row['house']}{before}{row['designer']}{after}"


def check_slide(n, title, section, rows, deck_title):
    """Gate, interpretation, both variants and their four prompts of one slide against its rows of the table."""
    errors = []
    if title != deck_title:
        errors.append(f"slide {n}: title «{title}» differs from the deck v5 «{deck_title}»")
    gate = re.search(r"^\*\*Кутюрье-гейт:\*\* (.+)$", section, re.M)
    expected = "; ".join(f"{r['variant']} — {named(r, ' (', ')')}, {r['country']}" for r in rows)
    if not gate or gate[1] != expected:
        errors.append(f"slide {n}: gate line is not «{expected}»")
    interpretation = re.search(r"^\*\*Интерпретация:\*\* (.+)$", section, re.M)
    if not interpretation or len(re.findall(r"[.!?](?:\s|$)", interpretation[1])) != 1:
        errors.append(f"slide {n}: interpretation is not one sentence")
    found = variants(section)
    for row in rows:
        v = row["variant"]
        if v not in found:
            errors.append(f"slide {n}: Variant {v} with [EN] and [RU] code spans not found")
            continue
        if found[v]["label"] != VARIANTS[v][0] or found[v]["heading"] != named(row, " — ", ""):
            errors.append(f"slide {n}: heading of Variant {v} is not «{VARIANTS[v][0]} ({named(row, ' — ', '')})»")
        for lang in ("EN", "RU"):
            errors += check_prompt(f"slide {n}{v} [{lang}]", lang, found[v][lang], row)
    if not section.rstrip().endswith("\n---"):
        errors.append(f"slide {n}: no `---` after the slide")
    return errors


def check_plan(rows):
    """Distribution rules of §4, §5.1, §5.2 and §7 over the table."""
    errors = []
    order = [(n, v) for n in range(1, 28) for v in "АБ"]
    if [(r["slide"], r["variant"]) for r in rows] != order:
        return ["table: rows are not slides 1–27 with Variants А and Б in order"]
    slides = defaultdict(set)
    for r in rows:
        if r["house"] not in HOUSES:
            errors.append(f"table: {r['house']} is not one of the 26 couturiers")
            continue
        slides[r["house"]].add(r["slide"])
        if r["country"] != HOUSES[r["house"]][0]:
            errors.append(f"table: country of {r['house']} is not {HOUSES[r['house']][0]}")
        if ZONE.get(r["city"]) != r["zone"]:
            errors.append(f"table: zone of {r['city']} is not {ZONE.get(r['city'], 'a city of the pool')}")
        if r["motion"] not in MOTIONS or (r["motion"] in PAIR_MOTIONS and r["type"] in ("W", "M")):
            errors.append(f"table: motion {r['motion']} of {r['slide']}{r['variant']} not allowed for {r['type']}")
        if len({r["cloth1"], r["cloth2"], r["object"]}) != 3 or not {r["cloth1"], r["cloth2"], r["object"]} <= set(BASE):
            errors.append(f"table: colours of {r['slide']}{r['variant']} are not three different base colours")
    missing = set(HOUSES) - set(slides)
    if missing:
        errors.append(f"table: couturiers without a slide: {', '.join(sorted(missing))}")
    for house, numbers in slides.items():
        if len(numbers) != 2:
            errors.append(f"table: {house} on slides {sorted(numbers)}, not on exactly two")
    for city, count in Counter(r["city"] for r in rows).items():
        if count > 2:
            errors.append(f"table: {city} used {count} times")
    for a, b in zip(rows, rows[1:]):
        where = f"{a['slide']}{a['variant']}→{b['slide']}{b['variant']}"
        if a["slide"] == b["slide"] and a["city"] == b["city"]:
            errors.append(f"table: one city in both variants of slide {a['slide']}")
        for key in ("zone", "type", "motion", "object_type"):
            if a[key] == b[key]:
                errors.append(f"table: {key} «{a[key]}» repeats on {where}")
    for a, b, c in zip(rows, rows[1:], rows[2:]):
        if {a["city"], b["city"], c["city"]} <= EUROPE:
            errors.append(f"table: three European cities in a row from {a['slide']}{a['variant']}")
    return errors


def validate(texts):
    body, deck = texts[PROMPTS], texts[DECK]
    if not body:
        return [f"{PROMPTS.relative_to(ROOT)} is missing"]
    errors = []
    head = body.split("\n---\n", 1)[0]
    if f'source: "{ISSUE}"' not in head:
        errors.append(f"frontmatter source is not {ISSUE}")
    if f"\n{TITLE}\n" not in body:
        errors.append(f"title «{TITLE}» missing")
    rows = plan(body)
    errors += check_plan(rows)
    deck_titles = {int(n): title.strip() for n, title in DECK_SLIDE.findall(deck)}
    seen = []
    for n, title, section in sections(body):
        seen.append(n)
        errors += check_slide(n, title, section, [r for r in rows if r["slide"] == n], deck_titles.get(n, "?"))
    if seen != sorted(deck_titles) or len(seen) != 27:
        errors.append(f"slide sections {seen} are not the 27 slides of the deck v5")
    for name in (GATE, DEVIATIONS):
        if name not in body:
            errors.append(f"section «{name.strip()}» missing")
    gate = body.split(GATE, 1)[1].split("\n## ", 1)[0] if GATE in body else ""
    if "- [ ] " in gate or gate.count("- [x] ") < 6:
        errors.append("gate checklist of §7 is not ticked: six items with `- [x]` expected")
    return errors


def mutate(texts, path, old, new, count=1):
    changed = dict(texts)
    changed[path] = texts[path].replace(old, new, count)
    return changed


def mutate_re(texts, path, pattern, new, count=1):
    changed = dict(texts)
    changed[path] = re.sub(pattern, new, texts[path], count=count, flags=re.M | re.S)
    return changed


def prompt(texts, n, v, lang, pattern, new, every=False):
    """Fixture: the first match of pattern in one prompt of slide n replaced, or every match of it with every=True."""
    tag = re.escape(f"**[{lang}]**")
    changed = mutate_re(texts, PROMPTS, rf"(^## Слайд {n}\..*?^### Вариант {v}:.*?{tag}\n`[^`\n]*?){pattern}", rf"\g<1>{new}")
    while every and changed[PROMPTS] != texts[PROMPTS]:
        texts, changed = changed, prompt(changed, n, v, lang, pattern, new)
    return changed


def swap(texts, first, second):
    """Fixture: two rows of the table exchange their cities, so each city is still used twice."""
    for (n, v, city, zone), (_, _, other, other_zone) in ((first, second), (second, first)):
        texts = mutate_re(texts, PROMPTS, rf"^(\| {n} \| {v} \| [^\n]*?\| ){re.escape(city)} \| {zone} \|", rf"\1{other} | {other_zone} |")
    return texts


# A [RU] prompt that keeps every rule of the file but is far shorter than MIN_WORDS: the fixture of the length check.
SHORT_RU = ("Высокий вертикальный баннер, фотография одной непрерывной сцены, высота намного больше ширины, без панелей и рамок. "
            "Реальный Буэнос-Айрес (Buenos Aires), дом Комеги в духе Ар-Деко, яркий high-key дневной свет SS 2027. "
            "Мужчина и женщина 47 и 38 лет, в резком фокусе, серьёзные лица, идут навстречу. "
            "Кутюр Chanel: на ней твидовый жакет цвета чернил #16181D с тесьмой, на нём кардиган глубокого синего #132A4A, "
            "сумка на цепочке. Золото #B89B5E — жемчужные пуговицы на героях. "
            "Умеренная массовка разнообразных прохожих в боке. "
            "Между ними арт-объект: стёганая камелия бутылочно-зелёного #0A4D3C. Сюрреалистичная эклектика.")


def self_test(texts):
    p = PROMPTS
    broken = {
        "prompts missing": mutate_re(texts, p, r".*", "", count=1),
        "source without #699": mutate(texts, p, f'source: "{ISSUE}"', 'source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/697"'),
        "title of the issue changed": mutate(texts, p, TITLE, "# День 4 · Промпты для изображений"),
        "slide title differs from the deck": mutate(texts, p, "## Слайд 6. Цвет: шкала образов Кобаяси", "## Слайд 6. Цвет: шкала Кобаяси"),
        "slide 27 dropped": mutate_re(texts, p, r"^## Слайд 27\..*?(?=\n## Гейт-проверка\n)", ""),
        "gate line without the country": mutate_re(texts, p, r"(^## Слайд 3\..*?\*\*Кутюрье-гейт:\*\* [^\n]*?), Франция", r"\1"),
        "interpretation of two sentences": mutate_re(texts, p, r"(^## Слайд 4\..*?\*\*Интерпретация:\*\* [^\n]*)$", r"\1 Ещё одно."),
        "variant heading without the designer": mutate_re(texts, p, r"^(### Вариант Б: Эклектика \()[^\n]*?\)$", r"\1Gucci)"),
        "[RU] prompt dropped": mutate_re(texts, p, r"(^## Слайд 9\..*?)\*\*\[RU\]\*\*\n`[^`\n]*`", r"\1"),
        "proportions not in words": prompt(texts, 2, "А", "EN", "height far greater than width", "tall format"),
        "RU proportions not in words": prompt(texts, 2, "Б", "RU", "высота намного больше ширины", "высокий формат"),
        "EN start changed": prompt(texts, 5, "А", "EN", "Tall narrow vertical banner photograph", "Vertical photograph"),
        "RU start changed": prompt(texts, 5, "Б", "RU", "Высокий вертикальный баннер", "Вертикальный кадр"),
        "Variant А ending without the city": prompt(texts, 7, "А", "EN", r"Always recognisable Art Deco in [A-Za-z ]+\.(?=`)", "Always recognisable Art Deco."),
        "Variant А RU ending without the city": prompt(texts, 7, "А", "RU", r"Всегда узнаваемое Ар-Деко в [^`\s]+\.(?=`)", "Всегда узнаваемое Ар-Деко."),
        "Variant Б ending changed": prompt(texts, 8, "Б", "EN", r"Surreal-meets-classical eclecticism\.(?=`)", "Eclecticism."),
        "Variant Б RU ending changed": prompt(texts, 8, "Б", "RU", r"Сюрреалистичная эклектика\.(?=`)", "Эклектика."),
        "city of the table missing": prompt(texts, 10, "А", "EN", r"Real Cairo,", "Real city,", every=True),
        "Latin city missing in RU": prompt(texts, 10, "Б", "RU", r"\(Vienna\)", "", every=True),
        "couturier not named": prompt(texts, 11, "А", "EN", r"Jil Sander", "the house", every=True),
        "season not named": prompt(texts, 12, "А", "RU", r"FW 2026/27", "этого сезона", every=True),
        "subject type changed": prompt(texts, 13, "Б", "EN", r"(?i:two men)", "two people", every=True),
        "age of the models dropped": prompt(texts, 14, "А", "EN", r"aged (?:3\d|4\d|50)\b", "of any age", every=True),
        "fourth base colour": prompt(texts, 15, "А", "EN", r"(#[0-9A-F]{6})", r"\1 and #0A4D3C"),
        "clothing colours after the art object": prompt(texts, 16, "А", "EN", r"Tall narrow vertical banner photograph",
                                                         "Tall narrow vertical banner photograph of an art object"),
        "gold dropped": prompt(texts, 17, "А", "EN", r"Gold #B89B5E", "Brass", every=True),
        "RU gold dropped": prompt(texts, 17, "Б", "RU", r"Золото #B89B5E", "Латунь", every=True),
        "crowd not moderate": prompt(texts, 18, "А", "EN", r"(?i:\bmoderate)", "dense", every=True),
        "crowd without bokeh": prompt(texts, 18, "Б", "RU", r"боке", "резкости", every=True),
        "uniform in a prompt": prompt(texts, 19, "А", "EN", r"Couture by", "Uniform couture by"),
        "office in a RU prompt": prompt(texts, 19, "Б", "RU", r"Кутюр", "Офисный кутюр"),
        "statue as the art object": prompt(texts, 20, "А", "EN", r"art object", "art object, a classical statue,"),
        "night scene": prompt(texts, 20, "Б", "EN", r"daylight", "daylight fading into night"),
        "generic draping": prompt(texts, 21, "А", "EN", r"\. ", ". Generic draping. "),
        "too few house markers": prompt(texts, 22, "А", "EN", f"(?:{HOUSES['Fendi'][1]})", "detail", every=True),
        "too long for DALL-E 3": prompt(texts, 23, "А", "EN", r"Couture by", "Couture by " + "very " * 900),
        "shortened prompt": prompt(texts, 24, "Б", "RU", r"Высокий[^`\n]*", SHORT_RU),
        "house on a third slide": mutate_re(texts, p, r"^(\| 25 \| А \| )Saint Laurent · Anthony Vaccarello \| Франция", r"\1Celine · Hedi Slimane | Франция"),
        "zone repeats": swap(texts, (22, "Б", "Seoul", "Восточная Азия"), (25, "А", "Istanbul", "Западная Азия")),
        "three European cities in a row": swap(texts, (1, "Б", "Mexico City", "Латинская Америка"), (21, "А", "Vienna", "Центральная Европа")),
        "subject type repeats": mutate_re(texts, p, r"^(\| 2 \| А \| [^\n]*?\| )M \|", r"\1WW |"),
        "pair motion for one model": mutate_re(texts, p, r"^(\| 1 \| А \| [^\n]*?\| W \| )diagonal-in \|", r"\1facing |"),
        "gate unticked": mutate_re(texts, p, r"(^## Гейт-проверка\n.*?)- \[x\] ", r"\1- [ ] "),
        "deviations dropped": mutate(texts, p, DEVIATIONS, "\n## Заметки\n"),
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
    rows = plan(texts[PROMPTS])
    print(f"PASS: 27 slides of the deck v5 with Variant А «Гармония» and Variant Б «Эклектика», [EN] and [RU] each: {len(rows) * 2} prompts")
    print(f"PASS: {len(HOUSES)} couturiers on exactly two slides each; {len({r['city'] for r in rows})} cities at most twice, neighbouring "
          "variants in different cultural zones, never three European cities in a row; subject types, motions and art objects never "
          "repeat on neighbouring variants")
    print(f"PASS: every prompt keeps the proportion frame in words, a real city, the couturier, two base colours on the person before "
          f"the art object and the third on it, gold {GOLD} on the person, a moderate varied crowd in bokeh, the season, at least three "
          f"markers of the house, no banned word, at most {MAX_CHARS} characters")
    print("PASS: [RU] keeps HEX codes, Latin city and house names and «Ар-Деко»; gate checklist of §7 ticked; deviations listed")
    if args.self_test:
        print(f"PASS: {fixtures} broken fixtures rejected")


if __name__ == "__main__":
    main()
