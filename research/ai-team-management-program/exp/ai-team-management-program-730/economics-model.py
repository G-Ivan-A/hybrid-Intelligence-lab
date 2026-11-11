#!/usr/bin/env python3
"""Экономическая модель MVP-программы «ИИ в работе с командой» (issues #730, #732).

Воспроизводимый расчёт для паспорта проекта
projects/ai-team-management-program/docs/passport/economics.md.

Все ставки — допущения (○) из отчёта
research/ai-team-management-program/2026-11-10-economics-market-benchmarks.md,
раздел 5.1, пересчитанные на итоговую архитектуру паспорта:
Модуль 0 (онлайн) + 4 очных модуля по 2 дня раз в месяц + межмодульная работа
+ онлайн-сессия через 60 дней после последнего модуля (оценка уровня 3).

Формула маржинальности (договорённость диалога к постановке):
    Маржа, % = (Цена − Себестоимость) / Цена × 100%
Разовые затраты на разработку (NRE) считаются отдельно от затрат на
проведение (Delivery). Цены — без НДС; НДС 22% добавляется сверху.
Лицензии ИИ-сервисов, альтернативные издержки времени участников и
интеграции с ERP/CRM в расчёт не входят (Д-7 постановки).

Итерация 2 (issue #732):
- Вариант 1 (полный): пять учебных кейсов К1–К5 вместо двух артефактов A/B —
  дороже практикум (наборы данных и шаблоны на 5 кейсов), цена NRE поднята
  с 4,5 до 4,8 млн ₽, чтобы первый поток сохранил порог НФТ-5 (маржа ≥ 30%).
- Вариант 2 («до 3 млн ₽»): цена заказа (разработка + один поток) не более
  3 млн ₽ без НДС, маржа не ниже 25%, архитектура программы не меняется
  (М0, 4 × 2 очных дня, 9 онлайн-сессий, оценка через 60 дней, 5 кейсов).
  Экономия — за счёт модели поставки: команда из пула стартапов и МСБ по
  ставкам ниже, «бережливая» разработка на готовой архитектуре паспорта,
  зал, питание, логистика куратора и проверка ИБ — силами заказчика.
  Разделы 11–15 журнала.

Запуск: python3 economics-model.py > economics-model.log
Зависимостей нет (только стандартная библиотека), сеть не используется.
"""

SCEN = ("min", "typ", "max")
SCEN_RU = {"min": "мин.", "typ": "типичное", "max": "макс."}

# ---------------------------------------------------------------- архитектура
IN_PERSON_DAYS = 8            # 4 модуля × 2 дня (Д-4)
AK_H_PER_DAY = 8              # академических часов в очный день
ONLINE_GROUP_SESSIONS = 9     # М0: 2; межмодульные: 2 × 3 периода; через 60 дней: 1
ONLINE_SESSION_H = 2          # астрономических часов на сессию
PROGRAM_MONTHS = 6            # подготовка потока (1) + М0..М4 (4) + оценка уровня 3 (1)
GUEST_SLOTS = 4               # гостевой эксперт: по полдня в каждом модуле
STAFF_ON_SITE = 4             # ведущий, ИИ-инженер, куратор, гость — в питании
INDIV_CONSULT_H_PER_P = 1.5   # индивидуальные онлайн-консультации на участника
CURATOR_FIXED_H = 100         # ≈ 20 ч в месяц × 5 месяцев (канал, напоминания, логистика заданий)
CURATOR_H_PER_P = 2           # проверка межмодульных заданий и артефакта по рубрике
EVAL_H = 40                   # отчёт Киркпатрик 1–3 + интервью Бринкерхоффа
CONTINGENCY = 0.10            # резерв на риски от прямых затрат Delivery

# Контактные часы (для удельной цены): 8 дней × 8 ак. ч + онлайн 9 × 2 астр. ч
CONTACT_AK_H = IN_PERSON_DAYS * AK_H_PER_DAY + round(ONLINE_GROUP_SESSIONS * ONLINE_SESSION_H * 60 / 45)
CONTACT_ASTRO_H = IN_PERSON_DAYS * 6 + ONLINE_GROUP_SESSIONS * ONLINE_SESSION_H  # 6 астр. ч в очном дне
# Проектируемый контент: очные дни + 2 сессии Модуля 0. Остальные онлайн-сессии —
# консультации по межмодульной работе участников, отдельной разработки не требуют.
DESIGNED_ASTRO_H = IN_PERSON_DAYS * 6 + 2 * ONLINE_SESSION_H

# ---------------------------------------------------------------- ставки (○)
RATES = {
    "lead_day":       {"min": 30_000, "typ": 60_000, "max": 120_000},  # ведущий эксперт, ₽/день
    "eng_day":        {"min": 25_000, "typ": 40_000, "max": 80_000},   # ИИ-инженер практикума, ₽/день
    "guest_slot":     {"min": 30_000, "typ": 50_000, "max": 100_000},  # гостевой эксперт, полдня (○)
    "online_h":       {"min": 5_000,  "typ": 10_000, "max": 20_000},   # групповая онлайн-сессия, ₽/ч
    "consult_h":      {"min": 3_000,  "typ": 5_000,  "max": 10_000},   # индивидуальная консультация, ₽/ч (○)
    "curator_h":      {"min": 2_000,  "typ": 4_000,  "max": 7_000},    # куратор, ₽/ч
    "pm_month":       {"min": 40_000, "typ": 75_000, "max": 120_000},  # продюсер, ₽/мес при 30%
    "venue_day":      {"min": 14_400, "typ": 25_000, "max": 45_000},   # зал, ₽/день
    "catering_pd":    {"min": 1_500,  "typ": 2_500,  "max": 4_000},    # питание, ₽/чел.-день
    "handout_p":      {"min": 1_000,  "typ": 3_000,  "max": 6_000},    # раздатка, ₽/участник
    "eval_h":         {"min": 1_000,  "typ": 2_000,  "max": 3_000},    # аналитик оценки, ₽/ч (○)
    # NRE
    "dev_ratio":      {"min": 20,     "typ": 30,     "max": 43},       # ч разработки на 1 астр. ч контакта (Chapman ILT 43:1 — верх)
    "method_h":       {"min": 600,    "typ": 1_000,  "max": 1_500},    # методист, ₽/ч
    "lead_dev_days":  {"min": 8,      "typ": 10,     "max": 12},       # дни ведущего эксперта на содержание
    "practicum":      {"min": 400_000, "typ": 700_000, "max": 1_100_000},  # синтетические данные 3 типов подразделений, наборы 5 кейсов К1–К5 (#732; было 300/500/800 для A/B)
    "instruments":    {"min": 100_000, "typ": 200_000, "max": 350_000},  # диагностика, рубрики, анкеты, протокол уровня 3
    "infosec":        {"min": 100_000, "typ": 150_000, "max": 300_000},  # проверка стека и заданий, вторая реализация (НФТ-4, ГК-10)
    "pilot":          {"min": 150_000, "typ": 300_000, "max": 600_000},  # тестовый прогон фрагмента М1 на 5–8 участниках
    "pm_dev_months":  {"min": 2,      "typ": 2,      "max": 3},
}

# ---------------------------------------------------------------- цена (предложение исполнителя)
PRICE_NRE = 4_800_000          # разработка, единовременно, без НДС (#732: было 4,5 млн при 2 артефактах)
PRICE_COHORT_BASE = 5_500_000  # проведение потока до 20 участников включительно, без НДС
PRICE_EXTRA_P = 180_000        # за каждого участника сверх 20 (21–25)
MIN_BILLABLE = 20              # при наборе 15–19 счёт выставляется как за 20 (ГК-1)
VAT = 0.22


# ---------------------------------------------------------------- вариант 2 (#732)
# Ставки «бережливого» профиля. Все — допущения (○): ставки практиков из
# компаний МСБ и стартапов не опубликованы; ориентир — нижняя граница ставок
# варианта 1 (отчёт об экономике рынка, раздел 5.1) и отказ от премии
# «топ-эксперта». Нефинансовая мотивация экспертов НЕ моделируется: гости
# получают оплату, бесплатное участие не закладывается.
LEAN = {
    "lead_day":       {"min": 30_000, "typ": 35_000, "max": 50_000},   # ведущий-практик из МСБ, ₽/день
    "eng_day":        {"min": 20_000, "typ": 22_000, "max": 30_000},   # ИИ-инженер практикума, ₽/день
    "guest_slot":     {"min": 20_000, "typ": 25_000, "max": 35_000},   # основатель/техлид стартапа, полдня
    "online_h":       {"min": 5_000,  "typ": 6_000,  "max": 8_000},    # групповая онлайн-сессия, ₽/ч
    "consult_h":      {"min": 2_500,  "typ": 3_000,  "max": 4_000},    # индивидуальная консультация, ₽/ч
    "curator_h":      {"min": 2_000,  "typ": 2_500,  "max": 3_500},    # проверка заданий по рубрике, ₽/ч
    "pm_month":       {"min": 30_000, "typ": 40_000, "max": 50_000},   # продюсер при 30%, ₽/мес
    "eval_h":         {"min": 1_000,  "typ": 1_500,  "max": 2_000},    # аналитик оценки, ₽/ч
    "handout_p":      {"min": 500,    "typ": 1_000,  "max": 1_500},    # раздатка (в основном электронная), ₽/уч.
    # NRE: архитектура, рубрика, кейсы и модули уже спроектированы в паспорте,
    # поэтому коэффициент разработки ниже «с нуля» (Chapman 43:1 — верх варианта 1).
    "dev_ratio":      {"min": 8,      "typ": 10,     "max": 14},
    "method_h":       {"min": 600,    "typ": 700,    "max": 900},
    "lead_dev_days":  {"min": 3,      "typ": 4,      "max": 6},
    "practicum":      {"min": 150_000, "typ": 200_000, "max": 300_000},  # один синтетический набор данных, 5 кейсов на общем шаблоне
    "instruments":    {"min": 50_000, "typ": 80_000, "max": 120_000},   # рубрика и анкеты паспорта, без отдельной разработки диагностики
    "infosec":        {"min": 40_000, "typ": 60_000, "max": 100_000},   # самопроверка исполнителя; ревью ИБ — силами заказчика
    "pm_dev_months":  {"min": 1,      "typ": 1.5,    "max": 2},
}
LEAN_EVAL_H = 30               # оценка уровней 1–3 по сокращённому протоколу
LEAN_CURATOR_H_PER_P = 2       # проверка заданий и карты внедрения; логистика — куратор заказчика
PRICE_V2 = 3_000_000           # заказ целиком: разработка + один поток до 25 участников, без НДС
V2_MARGIN_MIN = 25.0


def nre_items_v2(s):
    r = {k: v[s] for k, v in LEAN.items()}
    return [
        ("Адаптация методики на готовой архитектуре паспорта ({} астр. ч × {} ч/ч × ставка методиста)".format(DESIGNED_ASTRO_H, r["dev_ratio"]),
         DESIGNED_ASTRO_H * r["dev_ratio"] * r["method_h"]),
        ("Экспертиза содержания ведущим-практиком ({} дн.)".format(r["lead_dev_days"]), r["lead_dev_days"] * r["lead_day"]),
        ("Практикум: один синтетический набор данных подразделения, 5 кейсов на общем шаблоне карты внедрения", r["practicum"]),
        ("Инструменты оценки: рубрика и анкеты паспорта без отдельной диагностики", r["instruments"]),
        ("Самопроверка стека и заданий (ревью ИБ — силами заказчика)", r["infosec"]),
        ("Пилот: не проводится, ретро после М1 вместо пилота", 0),
        ("Продюсер на этапе разработки ({} мес.)".format(r["pm_dev_months"]), r["pm_dev_months"] * r["pm_month"]),
    ]


def delivery_items_v2(s, n, client_in_kind=True):
    r = {k: v[s] for k, v in LEAN.items()}
    items = [
        ("Ведущий-практик, {} очных дней".format(IN_PERSON_DAYS), IN_PERSON_DAYS * r["lead_day"]),
        ("ИИ-инженер практикума, {} очных дней".format(IN_PERSON_DAYS), IN_PERSON_DAYS * r["eng_day"]),
        ("Гости из пула стартапов и МСБ, {} × полдня".format(GUEST_SLOTS), GUEST_SLOTS * r["guest_slot"]),
        ("Групповые онлайн-сессии, {} × {} ч".format(ONLINE_GROUP_SESSIONS, ONLINE_SESSION_H),
         ONLINE_GROUP_SESSIONS * ONLINE_SESSION_H * r["online_h"]),
        ("Индивидуальные онлайн-консультации, {} ч × {} уч.".format(INDIV_CONSULT_H_PER_P, n),
         INDIV_CONSULT_H_PER_P * n * r["consult_h"]),
        ("Проверка заданий и карт внедрения, {} ч × {} уч.".format(LEAN_CURATOR_H_PER_P, n),
         LEAN_CURATOR_H_PER_P * n * r["curator_h"]),
        ("Продюсер/PM, {} мес. × 30% занятости".format(PROGRAM_MONTHS), PROGRAM_MONTHS * r["pm_month"]),
        ("Оценка Киркпатрик 1–3 по сокращённому протоколу, {} ч".format(LEAN_EVAL_H), LEAN_EVAL_H * r["eval_h"]),
        ("Раздатка, {} уч.".format(n), n * r["handout_p"]),
    ]
    if not client_in_kind:
        # заказчик не берёт на себя зал, питание и логистику куратора:
        # статьи по ставкам варианта 1 (типичным для выбранного сценария)
        v = {k: RATES[k][s] for k in ("venue_day", "catering_pd", "curator_h")}
        items += [
            ("Зал, {} дней (ставка варианта 1)".format(IN_PERSON_DAYS), IN_PERSON_DAYS * v["venue_day"]),
            ("Питание, {} дней × ({} уч. + {} ведущих)".format(IN_PERSON_DAYS, n, STAFF_ON_SITE),
             IN_PERSON_DAYS * (n + STAFF_ON_SITE) * v["catering_pd"]),
            ("Логистика куратора, {} ч".format(CURATOR_FIXED_H), CURATOR_FIXED_H * v["curator_h"]),
        ]
    direct = sum(v for _, v in items)
    items.append(("Резерв на риски {:.0%} от прямых затрат".format(CONTINGENCY), direct * CONTINGENCY))
    return items


def nre_items(s):
    r = {k: v[s] for k, v in RATES.items()}
    return [
        ("Методическая разработка (проектируемый контент {} астр. ч × {} ч/ч × ставка методиста)".format(DESIGNED_ASTRO_H, r["dev_ratio"]),
         DESIGNED_ASTRO_H * r["dev_ratio"] * r["method_h"]),
        ("Экспертиза содержания ведущим экспертом ({} дней)".format(r["lead_dev_days"]), r["lead_dev_days"] * r["lead_day"]),
        ("Практикум: синтетические данные 3 типов подразделений, наборы 5 кейсов К1–К5, шаблон карты внедрения, библиотека промптов", r["practicum"]),
        ("Инструменты оценки: входная диагностика, рубрика демо-дня, анкеты, протокол уровня 3", r["instruments"]),
        ("Проверка стека и заданий с ИБ, вторая реализация каждого задания", r["infosec"]),
        ("Пилот фрагмента М1 и доработка", r["pilot"]),
        ("Продюсер на этапе разработки ({} мес.)".format(r["pm_dev_months"]), r["pm_dev_months"] * r["pm_month"]),
    ]


def delivery_items(s, n, venue_by_client=False):
    r = {k: v[s] for k, v in RATES.items()}
    items = [
        ("Ведущий эксперт, {} очных дней".format(IN_PERSON_DAYS), IN_PERSON_DAYS * r["lead_day"]),
        ("ИИ-инженер практикума, {} очных дней".format(IN_PERSON_DAYS), IN_PERSON_DAYS * r["eng_day"]),
        ("Гостевые эксперты из пула кандидатов, {} × полдня".format(GUEST_SLOTS), GUEST_SLOTS * r["guest_slot"]),
        ("Групповые онлайн-сессии, {} × {} ч".format(ONLINE_GROUP_SESSIONS, ONLINE_SESSION_H),
         ONLINE_GROUP_SESSIONS * ONLINE_SESSION_H * r["online_h"]),
        ("Индивидуальные онлайн-консультации, {} ч × {} уч.".format(INDIV_CONSULT_H_PER_P, n),
         INDIV_CONSULT_H_PER_P * n * r["consult_h"]),
        ("Куратор: {} ч + {} ч × {} уч.".format(CURATOR_FIXED_H, CURATOR_H_PER_P, n),
         (CURATOR_FIXED_H + CURATOR_H_PER_P * n) * r["curator_h"]),
        ("Продюсер/PM, {} мес. × 30% занятости".format(PROGRAM_MONTHS), PROGRAM_MONTHS * r["pm_month"]),
        ("Оценка Киркпатрик 1–3 и интервью успешных случаев, {} ч".format(EVAL_H), EVAL_H * r["eval_h"]),
        ("Раздатка, {} уч.".format(n), n * r["handout_p"]),
    ]
    if not venue_by_client:
        items += [
            ("Зал, {} дней".format(IN_PERSON_DAYS), IN_PERSON_DAYS * r["venue_day"]),
            ("Питание, {} дней × ({} уч. + {} ведущих)".format(IN_PERSON_DAYS, n, STAFF_ON_SITE),
             IN_PERSON_DAYS * (n + STAFF_ON_SITE) * r["catering_pd"]),
        ]
    direct = sum(v for _, v in items)
    items.append(("Резерв на риски {:.0%} от прямых затрат".format(CONTINGENCY), direct * CONTINGENCY))
    return items


def total(items):
    return sum(v for _, v in items)


def price_cohort(n):
    billable = max(n, MIN_BILLABLE)
    return PRICE_COHORT_BASE + max(0, billable - 20) * PRICE_EXTRA_P


def margin(price, cost):
    return (price - cost) / price * 100


def mln(x):
    return "{:,.2f}".format(x / 1e6).replace(",", " ")


def rub(x):
    return "{:,.0f}".format(x).replace(",", " ")


def table_items(title, fn):
    print("### " + title + "\n")
    print("| Статья | " + " | ".join(SCEN_RU[s] for s in SCEN) + " |")
    print("|---|" + "---:|" * len(SCEN))
    rows = {s: fn(s) for s in SCEN}
    for i, (name, _) in enumerate(rows["typ"]):
        print("| {} | {} |".format(name, " | ".join(rub(rows[s][i][1]) for s in SCEN)))
    print("| **Итого** | {} |".format(" | ".join("**" + rub(total(rows[s])) + "**" for s in SCEN)))
    print()
    return {s: total(rows[s]) for s in SCEN}


def main():
    print("# Вывод economics-model.py\n")
    print("Контактные часы: {} очных дней × {} ак. ч + {} онлайн-сессий × {} ч = {} ак. ч ({} астр. ч).\n".format(
        IN_PERSON_DAYS, AK_H_PER_DAY, ONLINE_GROUP_SESSIONS, ONLINE_SESSION_H, CONTACT_AK_H, CONTACT_ASTRO_H))
    print("Формула: Маржа, % = (Цена − Себестоимость) / Цена × 100%. Цены без НДС.\n")

    nre = table_items("1. Разовые затраты на разработку (NRE), ₽", nre_items)
    deliv22 = table_items("2. Затраты на проведение одного потока (Delivery), группа 22, ₽",
                          lambda s: delivery_items(s, 22))

    print("### 3. Цена, предложенная заказчику (без НДС)\n")
    print("| Позиция | Цена, ₽ | С НДС 22%, ₽ |")
    print("|---|---:|---:|")
    print("| Разработка программы (NRE), единовременно | {} | {} |".format(rub(PRICE_NRE), rub(PRICE_NRE * (1 + VAT))))
    for n in (20, 22, 25):
        p = price_cohort(n)
        print("| Проведение потока, {} участников | {} | {} |".format(n, rub(p), rub(p * (1 + VAT))))
    print("\nПравило: базовая цена потока — до 20 участников; {} ₽ за каждого участника с 21-го по 25-го; "
          "при наборе менее 20 счёт выставляется как за 20.\n".format(rub(PRICE_EXTRA_P)))

    print("### 4. Маржинальность NRE\n")
    print("| Сценарий | Себестоимость NRE, ₽ | Маржа NRE, % |")
    print("|---|---:|---:|")
    for s in SCEN:
        print("| {} | {} | {:.1f} |".format(SCEN_RU[s], rub(nre[s]), margin(PRICE_NRE, nre[s])))
    print()

    print("### 5. Маржинальность проведения по размеру группы\n")
    print("| Участников | Цена потока, ₽ | Себестоимость мин. / тип. / макс., ₽ | Маржа мин. / тип. / макс., % | Цена на участника, ₽ | ₽ за ак. ч на участника |")
    print("|---:|---:|---|---|---:|---:|")
    for n in (20, 22, 25):
        p = price_cohort(n)
        c = {s: total(delivery_items(s, n)) for s in SCEN}
        print("| {} | {} | {} | {} | {} | {} |".format(
            n, rub(p), " / ".join(mln(c[s]) for s in SCEN) + " млн",
            " / ".join("{:.1f}".format(margin(p, c[s])) for s in SCEN),
            rub(p / n), rub(p / n / CONTACT_AK_H)))
    print()

    print("### 6. Первый поток целиком (NRE + проведение), группа 20 — порог НФТ-5\n")
    print("| Сценарий | Цена, ₽ | Себестоимость, ₽ | Маржа, % | Цена для маржи 30%, ₽ |")
    print("|---|---:|---:|---:|---:|")
    for s in SCEN:
        p = PRICE_NRE + price_cohort(20)
        c = nre[s] + total(delivery_items(s, 20))
        print("| {} | {} | {} | {:.1f} | {} |".format(SCEN_RU[s], rub(p), rub(c), margin(p, c), rub(c / 0.7)))
    print()

    print("### 7. Альтернатива: NRE не выставляется отдельно, а амортизируется в цене потока\n")
    print("Цена потока при амортизации = базовая цена потока + цена NRE / K запусков (группа 20, типичные затраты).\n")
    print("| K запусков | Цена потока, ₽ | Себестоимость (Delivery + NRE/K), ₽ | Маржа, % |")
    print("|---:|---:|---:|---:|")
    for k in (1, 2, 3, 5):
        p = price_cohort(20) + PRICE_NRE / k
        c = total(delivery_items("typ", 20)) + nre["typ"] / k
        print("| {} | {} | {} | {:.1f} |".format(k, rub(p), rub(c), margin(p, c)))
    print()

    print("### 8. Граничный случай ГК-1: набор 15–19 участников (типичные затраты)\n")
    print("| Участников | Без правила минимального счёта: цена, ₽ | Маржа, % | С правилом «как за 20»: маржа, % |")
    print("|---:|---:|---:|---:|")
    for n in (15, 17, 19):
        c = total(delivery_items("typ", n))
        p_prop = PRICE_COHORT_BASE / 20 * n
        print("| {} | {} | {:.1f} | {:.1f} |".format(n, rub(p_prop), margin(p_prop, c), margin(price_cohort(n), c)))
    c20 = total(delivery_items("typ", 20))
    per_p = PRICE_COHORT_BASE / 20
    # фиксированная и переменная части затрат
    c0 = total(delivery_items("typ", 0))
    var = (c20 - c0) / 20
    be = c0 / (per_p - var)
    n30 = c0 / (per_p * 0.7 - var)
    print("\nПри пропорциональной цене {} ₽ за участника: постоянные затраты потока {} ₽, переменные {} ₽ на участника; "
          "безубыточность — {:.1f} участника, маржа 30% — от {:.1f} участника.\n".format(
              rub(per_p), rub(c0), rub(var), be, n30))

    print("### 9. Чувствительность: площадка и питание за счёт заказчика (группа 20)\n")
    print("| Сценарий | Себестоимость без зала и питания, ₽ | Маржа при той же цене, % | Цена при сохранении маржи типичного сценария, ₽ |")
    print("|---|---:|---:|---:|")
    m_typ = margin(price_cohort(20), total(delivery_items("typ", 20)))
    for s in SCEN:
        c = total(delivery_items(s, 20, venue_by_client=True))
        print("| {} | {} | {:.1f} | {} |".format(SCEN_RU[s], rub(c), margin(price_cohort(20), c), rub(c / (1 - m_typ / 100))))
    print()

    print("### 10. Сверка с рынком (цена за участника, группа 22)\n")
    p22 = price_cohort(22) / 22
    print("- Цена проведения на участника: {} ₽; за очный день (с сопровождением): {} ₽.".format(rub(p22), rub(p22 / IN_PERSON_DAYS)))
    print("- С долей NRE (один поток): {} ₽ на участника.".format(rub((price_cohort(22) + PRICE_NRE) / 22)))
    print("- Ориентиры отчёта о бизнес-школах: очный день массового сегмента 23–65 тыс. ₽, премиум 52–111 тыс. ₽ на участника.")
    print("- Медиана коротких программ ДПО ≈ 926 ₽ за ак. ч (отчёт об экономике рынка); у нас {} ₽ за ак. ч — "
          "премия за закрытую группу, практикум на данных подразделения и межмодульное сопровождение.".format(
              rub(p22 / CONTACT_AK_H)))
    print()
    main_v2(nre)


def main_v2(nre_v1):
    print("## Вариант 2: цена заказа не более {} ₽ без НДС, маржа не ниже {:.0f}% (#732)\n".format(
        rub(PRICE_V2), V2_MARGIN_MIN))
    print("Архитектура программы та же: М0, {} очных дней, {} онлайн-сессий, {} гостевых слота, оценка через 60 дней, "
          "5 кейсов. Цена {} ₽ — фиксированная за разработку и один поток до 25 участников.\n".format(
              IN_PERSON_DAYS, ONLINE_GROUP_SESSIONS, GUEST_SLOTS, rub(PRICE_V2)))
    nre2 = table_items("11. Вариант 2: разработка (NRE), бережливый профиль, ₽", nre_items_v2)
    table_items("12. Вариант 2: проведение, группа 20, зал, питание, логистика и ревью ИБ — у заказчика, ₽",
                lambda s: delivery_items_v2(s, 20))

    print("### 13. Вариант 2: маржа заказа целиком (NRE + один поток) по размеру группы\n")
    print("| Участников | Цена, ₽ | Себестоимость мин. / тип. / макс., ₽ | Маржа мин. / тип. / макс., % | Порог {:.0f}% в типичном |".format(V2_MARGIN_MIN))
    print("|---:|---:|---|---|---|")
    for n in (20, 22, 25):
        c = {s: nre2[s] + total(delivery_items_v2(s, n)) for s in SCEN}
        m = {s: margin(PRICE_V2, c[s]) for s in SCEN}
        print("| {} | {} | {} | {} | {} |".format(
            n, rub(PRICE_V2), " / ".join(mln(c[s]) for s in SCEN) + " млн",
            " / ".join("{:.1f}".format(m[s]) for s in SCEN), "выполнен" if m["typ"] >= V2_MARGIN_MIN else "НЕ выполнен"))
    c_max_cost = PRICE_V2 * (1 - V2_MARGIN_MIN / 100)
    print("\nПредел себестоимости при цене {} ₽ и марже {:.0f}%: {} ₽.\n".format(rub(PRICE_V2), V2_MARGIN_MIN, rub(c_max_cost)))

    print("### 14. Вариант 2: граничные случаи (группа 20, типичные ставки)\n")
    print("| Случай | Цена без НДС, ₽ | Себестоимость, ₽ | Маржа, % | Цена для маржи {:.0f}%, ₽ |".format(V2_MARGIN_MIN))
    print("|---|---:|---:|---:|---:|")
    base = nre2["typ"] + total(delivery_items_v2("typ", 20))
    no_kind = nre2["typ"] + total(delivery_items_v2("typ", 20, client_in_kind=False))
    p_vat = PRICE_V2 / (1 + VAT)
    v1_rates_lean_scope = nre_v1["typ"] + total(delivery_items("typ", 20))
    cases = [
        ("Базовый: заказчик даёт зал, питание, логистику, ревью ИБ", PRICE_V2, base),
        ("Заказчик не даёт зал, питание и логистику куратора", PRICE_V2, no_kind),
        ("3 млн ₽ — с НДС 22% (цена без НДС ниже)", p_vat, base),
        ("Ставки и объём работ варианта 1 при цене 3 млн ₽", PRICE_V2, v1_rates_lean_scope),
    ]
    for name, p, c in cases:
        print("| {} | {} | {} | {:.1f} | {} |".format(name, rub(p), rub(c), margin(p, c), rub(c / (1 - V2_MARGIN_MIN / 100))))
    print()
    # сколько нужно снять с себестоимости, если 3 млн — с НДС
    gap_vat = base - p_vat * (1 - V2_MARGIN_MIN / 100)
    print("Если 3 млн ₽ включают НДС, для маржи {:.0f}% себестоимость нужно снизить ещё на {} ₽ — "
          "в рамках неизменной архитектуры резервов нет (см. economics.md).\n".format(V2_MARGIN_MIN, rub(gap_vat)))

    print("### 15. Сравнение вариантов (группа 20, типичные ставки)\n")
    v1_price = PRICE_NRE + price_cohort(20)
    v1_cost = nre_v1["typ"] + total(delivery_items("typ", 20))
    print("| Показатель | Вариант 1 (полный) | Вариант 2 (до 3 млн ₽) |")
    print("|---|---:|---:|")
    print("| Цена заказа (NRE + один поток), без НДС, ₽ | {} | {} |".format(rub(v1_price), rub(PRICE_V2)))
    print("| То же с НДС 22%, ₽ | {} | {} |".format(rub(v1_price * (1 + VAT)), rub(PRICE_V2 * (1 + VAT))))
    print("| Себестоимость NRE, ₽ | {} | {} |".format(rub(nre_v1["typ"]), rub(nre2["typ"])))
    print("| Себестоимость проведения, ₽ | {} | {} |".format(rub(total(delivery_items("typ", 20))), rub(total(delivery_items_v2("typ", 20)))))
    print("| Маржа заказа, % | {:.1f} | {:.1f} |".format(margin(v1_price, v1_cost), margin(PRICE_V2, base)))
    print("| Цена на участника, ₽ | {} | {} |".format(rub(v1_price / 20), rub(PRICE_V2 / 20)))
    print("| Второй и следующие потоки, цена без НДС, ₽ | {} | от {} (только проведение, маржа {:.0f}%) |".format(
        rub(price_cohort(20)), rub(total(delivery_items_v2("typ", 20)) / (1 - V2_MARGIN_MIN / 100)), V2_MARGIN_MIN))


if __name__ == "__main__":
    main()
