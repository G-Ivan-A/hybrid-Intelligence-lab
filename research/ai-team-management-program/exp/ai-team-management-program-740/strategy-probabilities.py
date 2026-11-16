#!/usr/bin/env python3
"""Модель вероятностей стратегий продвижения (issue #740).

Каждая стратегия — воронка за горизонт 12 месяцев:

    p_попытки = p_встреча * p_предложение * p_договор
    P(>=1 платного договора) = 1 - (1 - p_попытки) ** n

Все параметры заданы треугольными диапазонами (низ, мода, верх). Метод
Монте-Карло с фиксированным зерном даёт медиану и P10/P90. Выход детерминирован
и сверяется в CI с strategy-probabilities.log:

    python3 -I strategy-probabilities.py | diff - strategy-probabilities.log

Источник каждого диапазона — в поле `src`. Отметка GRA показывает силу
основания: ● — базовая ставка из открытого источника, ◐ — перенос ставки из
смежной практики или вторичный источник, ○ — экспертная оценка исполнителя без
внешней ставки. Модель субъективна: она нужна, чтобы сравнивать стратегии
между собой и знать, какие параметры проверять первыми. Абсолютные цифры не
прогноз.

Только стандартная библиотека Python.
"""

import random
import statistics

SEED = 740
RUNS = 20000
HORIZON_MONTHS = 12

# Ссылки на отчёты итерации 5 (research/ai-team-management-program/).
S4 = "2026-11-16-specialist-positioning-ru-us-cn.md"
S5 = "2026-11-16-network-building-shuttle-diplomacy-evidence.md"
S6 = "2026-11-16-university-codevelopment-project-selection.md"
S7 = "2026-11-16-vendor-education-mechanisms-formats-evidence.md"
S2 = "2026-11-16-vendor-education-russia.md"
S3 = "2026-11-16-vendor-education-china.md"

# Параметр: (низ, мода, верх, отметка GRA, источник).
STRATEGIES = {
    "RU-A": {
        "title": "Курсы и круглые столы Технограда -> проекты с вендорами и корпорациями",
        "market": "RU",
        "n": (12, 24, 40, "○", "лиц, принимающих решения, в год: 4-8 мероприятий по 3-5 ЛПР; оценка исполнителя"),
        "p_meeting": (0.10, 0.20, 0.35, "◐", S5 + ": тёплый контакт после мероприятия"),
        "p_proposal": (0.20, 0.35, 0.50, "◐", S5 + ": переход встреча -> КП в B2B-консалтинге"),
        "p_contract": (0.15, 0.25, 0.40, "◐", S5 + ": доля выигранных КП (win rate)"),
    },
    "RU-B": {
        "title": "Совместная ДПО-программа с вузом и вендором-спонсором",
        "market": "RU",
        "n": (2, 4, 6, "○", "вузов в переговорах; оценка исполнителя"),
        "p_meeting": (0.30, 0.50, 0.70, "◐", S6 + ": вуз принимает предложение ДПО (гипотеза issue)"),
        "p_proposal": (0.20, 0.35, 0.55, "◐", S2 + ": вендор соглашается софинансировать программу"),
        "p_contract": (0.30, 0.50, 0.70, "○", "платный пилот при согласии обеих сторон; оценка исполнителя"),
    },
    "RU-C": {
        "title": "Прямое предложение вендорам: проектирование клиентской академии",
        "market": "RU",
        "n": (15, 30, 50, "○", "вендоров в адресном списке; оценка исполнителя"),
        "p_meeting": (0.03, 0.08, 0.15, "◐", S5 + ": ответ на холодное B2B-обращение"),
        "p_proposal": (0.20, 0.35, 0.50, "◐", S5 + ": переход встреча -> КП"),
        "p_contract": (0.10, 0.20, 0.35, "◐", S5 + ": win rate КП"),
    },
    "CN-A": {
        "title": "Китай: российско-китайские вузовские каналы и китайские компании в РФ",
        "market": "CN",
        "n": (3, 8, 15, "○", "контактов в год; оценка исполнителя"),
        "p_meeting": (0.05, 0.12, 0.25, "◐", S3 + ": барьеры языка и гуаньси"),
        "p_proposal": (0.10, 0.25, 0.40, "○", "оценка исполнителя"),
        "p_contract": (0.05, 0.15, 0.30, "◐", S3 + ": локализация вендорских программ"),
    },
    "US-A": {
        "title": "США: удалённые проекты и публичная экспертиза при санкционных ограничениях",
        "market": "US",
        "n": (5, 15, 30, "○", "откликов и контактов в год; оценка исполнителя"),
        "p_meeting": (0.01, 0.04, 0.10, "◐", S4 + ": санкции, платежи, визы"),
        "p_proposal": (0.10, 0.25, 0.40, "○", "оценка исполнителя"),
        "p_contract": (0.05, 0.15, 0.30, "○", "оценка исполнителя"),
    },
}

STAGES = ("p_meeting", "p_proposal", "p_contract")

PORTFOLIOS = {
    "RU-A+RU-B": ("RU-A", "RU-B"),
    "RU-A+RU-B+RU-C": ("RU-A", "RU-B", "RU-C"),
    "все пять": tuple(STRATEGIES),
}


def tri(rng, spec):
    low, mode, high = spec[0], spec[1], spec[2]
    return rng.triangular(low, high, mode)


def draw(rng, strat):
    """Один прогон: вернуть (P(>=1 договора), ожидаемое число договоров)."""
    n = round(tri(rng, strat["n"]))
    p = 1.0
    for stage in STAGES:
        p *= tri(rng, strat[stage])
    return 1 - (1 - p) ** n, n * p


def simulate(rng):
    """Совместные прогоны всех стратегий: портфель считается внутри прогона."""
    probs = {k: [] for k in STRATEGIES}
    expected = {k: [] for k in STRATEGIES}
    for _ in range(RUNS):
        for key, strat in STRATEGIES.items():
            pr, ex = draw(rng, strat)
            probs[key].append(pr)
            expected[key].append(ex)
    return probs, expected


def quantiles(xs):
    qs = statistics.quantiles(xs, n=10, method="inclusive")
    return qs[0], statistics.median(xs), qs[-1]


def point(strat, override=None):
    """Детерминированная оценка по модам; override = (параметр, индекс границы)."""
    vals = {k: strat[k][1] for k in ("n",) + STAGES}
    if override:
        key, idx = override
        vals[key] = strat[key][idx]
    p = vals["p_meeting"] * vals["p_proposal"] * vals["p_contract"]
    return 1 - (1 - p) ** round(vals["n"])


def main():
    rng = random.Random(SEED)
    print(f"# Модель вероятностей стратегий #740: seed={SEED}, runs={RUNS}, горизонт={HORIZON_MONTHS} мес.")
    print()
    print("## Параметры")
    for key, strat in STRATEGIES.items():
        print(f"{key} [{strat['market']}] {strat['title']}")
        for param in ("n",) + STAGES:
            low, mode, high, mark, src = strat[param]
            print(f"  {param:<10} {low:>6} {mode:>6} {high:>6}  {mark}  {src}")
    print()
    print("## P(>=1 платного договора за горизонт): P10 / медиана / P90; E[договоров]")
    probs, expected = simulate(rng)
    for key in STRATEGIES:
        p10, med, p90 = quantiles(probs[key])
        print(f"{key:<6} {p10:.3f} / {med:.3f} / {p90:.3f}   E={statistics.mean(expected[key]):.2f}")
    print()
    print("## Портфель: 1 - prod(1 - P_i) в каждом прогоне; P10 / медиана / P90")
    print("# Независимость стратегий -- верхняя граница: их связывает одно время исполнителя.")
    for name, keys in PORTFOLIOS.items():
        joint = []
        for i in range(RUNS):
            q = 1.0
            for k in keys:
                q *= 1 - probs[k][i]
            joint.append(1 - q)
        p10, med, p90 = quantiles(joint)
        print(f"{name:<16} {p10:.3f} / {med:.3f} / {p90:.3f}")
    print()
    print("## Чувствительность по модам: P при параметре на нижней / верхней границе")
    for key, strat in STRATEGIES.items():
        base = point(strat)
        swings = []
        for param in ("n",) + STAGES:
            lo, hi = point(strat, (param, 0)), point(strat, (param, 2))
            swings.append((hi - lo, param, lo, hi))
        swings.sort(reverse=True)
        top = swings[0]
        print(f"{key}  база={base:.3f}; главный параметр {top[1]}: {top[2]:.3f} .. {top[3]:.3f}")


if __name__ == "__main__":
    main()
