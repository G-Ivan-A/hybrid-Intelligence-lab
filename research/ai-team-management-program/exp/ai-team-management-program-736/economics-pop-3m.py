#!/usr/bin/env python3
"""Экономика трёхмесячной программы для пакета pop-3m (issue #736).

Воспроизводимый расчёт для
projects/ai-team-management-program/pop-3m/05-detailed-economics.md
и агрегатов в 01-project-summary.md того же каталога.

Правила расчёта (постановка #736 и диалог 11.11.2026):
- все суммы без НДС;
- ставки людей указаны гросс (до удержания НДФЛ 13%), сверху работодатель
  начисляет страховые взносы по единому тарифу 30%;
- помещение — внутренний ресурс Академии, 0 ₽;
- кофе-брейки: 20 участников + 4 человека команды, 6 очных дней, 2 перерыва
  в день;
- одна ставка на позицию, без диапазонов.
- Маржа (%) = (Цена − Себестоимость) / Цена × 100%.

Обоснование каждой ставки — в README.md этого каталога (раздел «Ставки»).
Запуск: python3 economics-pop-3m.py > economics-pop-3m.log
Зависимостей нет, сеть не используется.
"""

PAYROLL_TAX = 0.30          # единый тариф страховых взносов, доля от гросс
PARTICIPANTS = 20           # базовый поток
TEAM_AT_BREAKS = 4          # ведущий эксперт, ИИ-архитектор, куратор, спонсор
IN_PERSON_DAYS = 6          # недели 1, 6, 11 по 2 дня
PROGRAM_MONTHS = 3

# ------------------------------------------------------------------ ставки
RATE = {
    "lead_day": 100_000,        # ведущий эксперт, очный день 8 а.ч.
    "lead_online": 25_000,      # ведущий эксперт, живая онлайн-сессия 2 а.ч.
    "arch_day": 80_000,         # ИИ-архитектор, очный день или день разработки
    "arch_online": 20_000,      # ИИ-архитектор, живой практикум 2 а.ч.
    "arch_hour": 6_000,         # ИИ-архитектор, консультации сетов, час
    "curator_hour": 1_500,      # куратор (штат Академии), час
    "methodologist_hour": 1_500,  # методист, час
    "video_lecture": 25_000,    # запись и монтаж одной лекции (подрядчик-юрлицо)
    "coffee_break": 650,        # один кофе-брейк на человека
    "handouts": 2_500,          # раздаточные материалы на участника
    "justai_seat_month": 3_500,  # место в песочнице JustAI + токены LLM, мес.
}

# ------------------------------------------------------------ программа, а.ч.
WEEKS = [
    # (неделя, формат, а.ч. всего, из них теория)
    ("0", "онлайн", 3, 0),
    ("1", "очно", 16, 6),
    ("2", "онлайн", 5, 1), ("3", "онлайн", 5, 1), ("4", "онлайн", 5, 1),
    ("5", "онлайн", 5, 1),
    ("6", "очно", 16, 2),
    ("7", "онлайн", 5, 1), ("8", "онлайн", 5, 1), ("9", "онлайн", 5, 1),
    ("10", "онлайн", 5, 1),
    ("11", "очно", 16, 2),
]

# ----------------------------------------------------------------- NRE
NRE_PEOPLE = [
    # (статья, роль, количество, единица, ставка)
    ("Методология: программа 91 а.ч., рабочая тетрадь, шаблоны",
     "Методист", 200, "ч", RATE["methodologist_hour"]),
    ("Экспертиза: контент недель 1 и 7–10, 4 лекции, сценарий стресс-теста",
     "Ведущий эксперт", 6, "дн.", RATE["lead_day"]),
    ("Экспертиза: контент недель 2–6, 4 лекции, шаблоны агентов",
     "ИИ-архитектор", 5, "дн.", RATE["arch_day"]),
    ("Синтетические данные для 5 кейсов с разметкой зон",
     "ИИ-архитектор", 3, "дн.", RATE["arch_day"]),
    ("Настройка песочницы JustAI: пространства, агенты-шаблоны, база знаний",
     "ИИ-архитектор", 2, "дн.", RATE["arch_day"]),
]
NRE_VENDORS = [
    ("Запись и монтаж 8 лекций", "Видеостудия", 8, "лекц.", RATE["video_lecture"]),
]

# ---------------------------------------------------------------- OPEX
CONSULT_WEEKS = 8
CONSULT_HOURS_PER_WEEK = 4
CURATOR_HOURS = 12 * 6 + IN_PERSON_DAYS * 8   # 12 недель по 6 ч + очные дни

OPEX_PEOPLE = [
    ("Ведущий эксперт: очные дни (неделя 1 — 2 дня, неделя 11 — 1 день)",
     "Ведущий эксперт", 3, "дн.", RATE["lead_day"]),
    ("Ведущий эксперт: живые сессии недель 7–10",
     "Ведущий эксперт", 4, "сесс.", RATE["lead_online"]),
    ("ИИ-архитектор: очные дни (неделя 1 — 1, неделя 6 — 2, неделя 11 — 2)",
     "ИИ-архитектор", 5, "дн.", RATE["arch_day"]),
    ("ИИ-архитектор: живые практикумы недель 2–5",
     "ИИ-архитектор", 4, "сесс.", RATE["arch_online"]),
    ("ИИ-архитектор: консультации сетов, недели 2–5 и 7–10",
     "ИИ-архитектор", CONSULT_WEEKS * CONSULT_HOURS_PER_WEEK, "ч", RATE["arch_hour"]),
    ("Куратор: ритм, LMS, напоминания, очные дни",
     "Куратор", CURATOR_HOURS, "ч", RATE["curator_hour"]),
]
COFFEE_UNITS = (PARTICIPANTS + TEAM_AT_BREAKS) * IN_PERSON_DAYS * 2
OPEX_OTHER = [
    ("Кофе-брейки: 24 чел. × 6 дн. × 2", "Кейтеринг", COFFEE_UNITS, "порц.",
     RATE["coffee_break"]),
    ("Раздаточные материалы и сертификаты", "Типография", PARTICIPANTS, "компл.",
     RATE["handouts"]),
    ("Песочница JustAI и токены LLM: 24 места × 3 мес.", "JustAI",
     (PARTICIPANTS + TEAM_AT_BREAKS) * PROGRAM_MONTHS, "место-мес.",
     RATE["justai_seat_month"]),
    ("Помещение — ресурс Академии", "Академия", IN_PERSON_DAYS, "дн.", 0),
    ("Корпоративная LMS — ресурс Академии", "Академия", 1, "поток", 0),
]

PRICE_NRE = 3_400_000
PRICE_FLOW = 3_500_000
PRICE_EXTRA_PARTICIPANT = 140_000

# Рыночный ориентир цены потока: ₽ за а.ч. на участника
# (research/ai-team-management-program/2026-11-10-economics-market-benchmarks.md,
# раздел 2.1, строка «₽ за ак. ч на участника»: типичное ~2 800, минимум 1 140):
MARKET_IN_PERSON_RUB_PER_AH = 2_800   # очные короткие программы
MARKET_ONLINE_RUB_PER_AH = 1_140      # онлайн-программы


def fmt(x: float) -> str:
    return f"{x:,.0f}".replace(",", " ")


def block(title, rows, taxed):
    gross = 0
    print(f"## {title}")
    for item, who, qty, unit, rate in rows:
        total = qty * rate
        gross += total
        print(f"- {item} | {who} | {qty} {unit} × {fmt(rate)} ₽ = {fmt(total)} ₽")
    tax = round(gross * PAYROLL_TAX) if taxed else 0
    if taxed:
        print(f"  Итого гросс: {fmt(gross)} ₽; страховые взносы 30%: {fmt(tax)} ₽; "
              f"с взносами: {fmt(gross + tax)} ₽")
    else:
        print(f"  Итого: {fmt(gross)} ₽")
    return gross + tax


def margin(price, cost):
    return (price - cost) / price * 100


def main():
    total_ah = sum(w[2] for w in WEEKS)
    in_person_ah = sum(w[2] for w in WEEKS if w[1] == "очно")
    online_ah = total_ah - in_person_ah
    theory_ah = sum(w[3] for w in WEEKS)
    print("# Программа")
    print(f"Всего {total_ah} а.ч.: очно {in_person_ah}, онлайн {online_ah}")
    print(f"Теория {theory_ah} а.ч. ({theory_ah / total_ah * 100:.0f}%), практика "
          f"{total_ah - theory_ah} а.ч. ({(total_ah - theory_ah) / total_ah * 100:.0f}%)")
    assert total_ah == 91 and in_person_ah == 48, "раскладка часов изменилась"
    assert all(3 <= w[2] <= 6 for w in WEEKS if w[1] == "онлайн"), "онлайн-блок вне 3–6 а.ч."
    assert all(w[2] == 16 for w in WEEKS if w[1] == "очно"), "очный блок не 16 а.ч."
    print()

    nre = block("NRE — люди", NRE_PEOPLE, True)
    nre += block("NRE — подрядчики", NRE_VENDORS, False)
    print(f"NRE итого: {fmt(nre)} ₽")
    print()

    opex = block("OPEX — люди", OPEX_PEOPLE, True)
    opex += block("OPEX — прочее", OPEX_OTHER, False)
    print(f"OPEX потока (20 участников) итого: {fmt(opex)} ₽")
    print()

    cogs = nre + opex
    price = PRICE_NRE + PRICE_FLOW
    print("# Цена и маржа")
    print(f"Разработка: себестоимость {fmt(nre)} ₽; цена {fmt(PRICE_NRE)} ₽; "
          f"маржа {margin(PRICE_NRE, nre):.1f}%")
    print(f"Поток: себестоимость {fmt(opex)} ₽; цена {fmt(PRICE_FLOW)} ₽; "
          f"маржа {margin(PRICE_FLOW, opex):.1f}%")
    print(f"Первый поток целиком: себестоимость {fmt(cogs)} ₽; цена {fmt(price)} ₽; "
          f"маржа {margin(price, cogs):.1f}%")
    print(f"Цена потока на участника: {fmt(PRICE_FLOW / PARTICIPANTS)} ₽; "
          f"за а.ч. на участника: {fmt(PRICE_FLOW / PARTICIPANTS / total_ah)} ₽")
    market = (in_person_ah * MARKET_IN_PERSON_RUB_PER_AH
              + online_ah * MARKET_ONLINE_RUB_PER_AH)
    print(f"Рыночный ориентир на участника: {in_person_ah} × "
          f"{fmt(MARKET_IN_PERSON_RUB_PER_AH)} + {online_ah} × "
          f"{fmt(MARKET_ONLINE_RUB_PER_AH)} = {fmt(market)} ₽")

    extra_cost = (IN_PERSON_DAYS * 2 * RATE["coffee_break"] + RATE["handouts"]
                  + PROGRAM_MONTHS * RATE["justai_seat_month"])
    print(f"Участник 21–25: переменная себестоимость {fmt(extra_cost)} ₽; "
          f"цена {fmt(PRICE_EXTRA_PARTICIPANT)} ₽; "
          f"маржа {margin(PRICE_EXTRA_PARTICIPANT, extra_cost):.1f}%")
    flow25_cost = opex + 5 * extra_cost
    flow25_price = PRICE_FLOW + 5 * PRICE_EXTRA_PARTICIPANT
    print(f"Поток 25 участников: себестоимость {fmt(flow25_cost)} ₽; цена "
          f"{fmt(flow25_price)} ₽; маржа {margin(flow25_price, flow25_cost):.1f}%")


if __name__ == "__main__":
    main()
