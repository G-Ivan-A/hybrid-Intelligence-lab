#!/usr/bin/env python3
"""Проверка пакета projects/ai-team-management-program/pop-3m (issue #736).

Машинно проверяет критерии приёмки и запреты постановки:
- ровно 5 файлов с заданными именами;
- резюме не длиннее 5000 знаков с пробелами;
- запрещённые служебные слова и инструменты, кроме JustAI;
- 5 уровней паспорта, ни один не объединён;
- недельная раскладка 0–11 с а.ч., сумма 91, онлайн 3–6 а.ч., очно 16 а.ч.;
- 4 кандидата строго по шаблону, метки GRA ●●●◐, примечание о кураторе;
- RFC: структура сайта, workflow GitHub Actions, промпт, критерии приёмки;
- экономика: без диапазонов ставок, взносы 30%, помещение 0 ₽, кофе-брейки,
  формула маржи, итоги совпадают с economics-pop-3m.log;
- группа строго 20–25 человек, сеты 4–5 человек;
- блок КРИК-ГЕЙТ в рабочем README.

Запуск из корня репозитория:
  python3 research/ai-team-management-program/exp/ai-team-management-program-736/check-pop-3m.py
Код выхода 0 — все проверки пройдены.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
POP = ROOT / "projects/ai-team-management-program/pop-3m"
EXP = Path(__file__).resolve().parent
FILES = [
    "01-project-summary.md",
    "02-project-passport.md",
    "03-appendix.md",
    "04-rfc-site-presentation.md",
    "05-detailed-economics.md",
]
FORBIDDEN_WORDS = [
    r"draft", r"version", r"issue", r"черновик", r"исполнитель предлагает",
    r"мы считаем",
]
FORBIDDEN_TOOLS = [
    r"ChatGPT", r"OpenAI", r"\bGPT", r"Claude", r"Anthropic", r"Gemini",
    r"Яндекс", r"Yandex", r"GigaChat", r"ГигаЧат", r"Алиса", r"DeepSeek",
    r"Llama", r"Mistral", r"Qwen", r"Copilot", r"Perplexity", r"Microsoft",
    r"Google", r"Notion", r"Miro", r"Zapier", r"\bn8n\b", r"Power ?BI",
    r"Tableau", r"Excel", r"Bitrix", r"Битрикс", r"Telegram", r"Slack",
]
GOAL = ("Трансформация стиля управления 25 руководителей за счет внедрения "
        "ИИ-агентов для автоматизации рутины и создания прототипов аналитических "
        "дашбордов, с соблюдением корпоративных стандартов работы с данными")
ZONES = ("Руководитель обучается классифицировать данные (зелёная, жёлтая, "
         "красная зона) и осознанно выбирать модель в интерфейсе JustAI в "
         "зависимости от уровня риска")

errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


def flat(text):
    """Склеивает переносы строк и убирает markdown-выделение для поиска фраз."""
    return re.sub(r"\s+", " ", text.replace("**", "")).replace("ё", "е").lower()


def main():
    present = sorted(p.name for p in POP.iterdir())
    check(present == FILES, f"в pop-3m должны быть ровно 5 файлов, есть: {present}")
    text = {name: (POP / name).read_text(encoding="utf-8") for name in FILES
            if (POP / name).exists()}

    # Общие запреты
    for name, body in text.items():
        for word in FORBIDDEN_WORDS:
            for m in re.finditer(word, body, re.I):
                check(False, f"{name}: запрещённое слово «{m.group(0)}»")
        for tool in FORBIDDEN_TOOLS:
            for m in re.finditer(tool, body, re.I):
                check(False, f"{name}: упомянут инструмент или вендор «{m.group(0)}»")
        check(not body.startswith("---"), f"{name}: служебный frontmatter в артефакте")
        for m in re.finditer(r"(\d+)\s*[–-]\s*(\d+)\s+(человек|участник)", body):
            # допустимы только группа 20–25 и сет 4–5
            check((m.group(1), m.group(2)) in {("20", "25"), ("4", "5")},
                  f"{name}: размер группы «{m.group(0)}» вне 20–25 и сета вне 4–5")
        for m in re.finditer(r"сет\w*\s+(?:из|по)\s+(\d+)\s*[–-]\s*(\d+)", body):
            check((m.group(1), m.group(2)) == ("4", "5"),
                  f"{name}: размер сета «{m.group(0)}» вне 4–5")

    # Файл 1
    s1 = text.get(FILES[0], "")
    check(len(s1) <= 5000, f"01: {len(s1)} знаков, лимит 5000")
    check(flat(GOAL) in flat(s1), "01: бизнес-цель не дословно")
    check(flat(ZONES) in flat(s1), "01: формулировка зон данных не дословно")
    for week in ["Неделя 0", "Неделя 1 ", "Недели 2–5", "Неделя 6", "Недели 7–10",
                 "Неделя 11", "стресс-тест"]:
        check(week in s1, f"01: нет блока «{week.strip()}»")
    for role in ["Ведущий эксперт", "ИИ-архитектор", "Куратор"]:
        check(role in s1, f"01: нет роли {role}")
    for term in ["NRE", "OPEX", "Итого первый поток", "Маржа"]:
        check(term in s1, f"01: нет экономического агрегата {term}")

    # Файл 2
    s2 = text.get(FILES[1], "")
    levels = re.findall(r"^## Уровень (\d)\. (.+)$", s2, re.M)
    check([n for n, _ in levels] == ["1", "2", "3", "4", "5"],
          f"02: уровни паспорта {levels}, нужны 1–5 по отдельности")
    check(flat(ZONES) in flat(s2), "02: формулировка зон данных не дословно")
    rows = re.findall(r"^\| (\d+) \| (Онлайн|Очно, 2 дня) \| (\d+) \|", s2, re.M)
    check([int(r[0]) for r in rows] == list(range(12)), "02: недели не 0–11")
    check(sum(int(r[2]) for r in rows) == 91, "02: сумма а.ч. не 91")
    for week, fmt, ah in rows:
        ah = int(ah)
        if fmt == "Онлайн":
            check(3 <= ah <= 6, f"02: онлайн-неделя {week} — {ah} а.ч. вне 3–6")
        else:
            check(ah == 16, f"02: очная неделя {week} — {ah} а.ч., нужно 16")
    lectures = re.findall(r"Лекция «[^»]+»", s2)
    check(len(lectures) == 7, f"02: тем лекций {len(lectures)}, нужно 7 (недели 2–5 и 7–9)")
    check("Стресс-тест" in s2, "02: нет стресс-теста")
    for term in ["L1", "L2", "L3", "L4", "CSAT", "NPS", "20%", "80%", "Blended",
                 "не более 2 очных дней в месяц", "LMS", "песочница JustAI".lower()]:
        check(term.lower() in s2.lower(), f"02: нет «{term}»")

    # Файл 3
    s3 = text.get(FILES[2], "")
    for sec in ["## [1]", "## [2]", "## [3]", "## [4]"]:
        check(sec in s3, f"03: нет раздела {sec}")
    cand = re.findall(
        r"^(Ведущий эксперт [12]|ИИ-архитектор [12]): ([А-ЯЁ][а-яё]+ [А-ЯЁ]\.(?:[А-ЯЁ]\.)?)"
        r" \| ([^|\n]+) \| ([^|\n]+) \| Метка GRA: ([●◐])$", s3, re.M)
    check([c[0] for c in cand] == ["Ведущий эксперт 1", "Ведущий эксперт 2",
                                   "ИИ-архитектор 1", "ИИ-архитектор 2"],
          f"03: кандидаты не по шаблону: {[c[0] for c in cand]}")
    check([c[4] for c in cand] == ["●", "●", "●", "◐"], "03: метки GRA не ●●●◐")
    check(len(cand) == 4 and "Just AI" in cand[2][2], "03: ИИ-архитектор 1 не из JustAI")
    check("Куратор — штатная роль Академии, внешний подбор кандидатов не требуется"
          in s3, "03: нет примечания о кураторе")
    for term in ["66 дней", "Lacerenza", "Lally", "Карта страхов", "Зона гения",
                 "RACI", "Стресс-тест", "когнитивн".capitalize()]:
        check(term.lower() in s3.lower(), f"03: нет «{term}»")

    # Файл 4
    s4 = text.get(FILES[3], "")
    for term in ["Лендинг", "Интерактивный таймлайн", "Наша команда",
                 "Запросить детальный бюджет", "branches: [main]",
                 "actions/jekyll-build-pages", "actions/deploy-pages",
                 "actions/upload-pages-artifact", "## 5. Промпт для инициализации",
                 "Критерии приёмки RFC", "id-token: write"]:
        check(term in s4, f"04: нет «{term}»")

    # Файл 5
    s5 = text.get(FILES[4], "")
    for m in re.finditer(r"\d[\d ]*\s*[–-]\s*\d[\d ]*\s*₽", s5):
        check(False, f"05: диапазон ставки «{m.group(0)}»")
    check("~" not in s5 and "≈" not in s5, "05: приблизительные значения")
    for term in ["без НДС", "Страховые взносы 30%", "Помещение", "0 ₽ — внутренний ресурс Академии",
                 "Кофе-брейки", "20 участников + 4 человека команды, 6 очных дней",
                 "## 1. NRE", "## 2. OPEX", "## 3. Себестоимость (COGS)",
                 "## 4. Цена для заказчика", "## 5. Маржинальность",
                 "Маржа (%) = (Цена − Себестоимость) / Цена × 100%",
                 "Методология", "Экспертиза", "Синтетические данные",
                 "Настройка песочницы", "Ведущий эксперт", "ИИ-архитектор",
                 "Куратор", "Раздаточные материалы"]:
        check(term in s5, f"05: нет «{term}»")

    # Согласованность с моделью
    log = (EXP / "economics-pop-3m.log").read_text(encoding="utf-8")
    totals = {
        "NRE": re.search(r"NRE итого: ([\d ]+) ₽", log).group(1),
        "OPEX": re.search(r"OPEX потока \(20 участников\) итого: ([\d ]+) ₽", log).group(1),
    }
    for line in re.findall(r"^(?:Разработка|Поток|Первый поток целиком|Участник 21–25|"
                           r"Поток 25 участников): .+$", log, re.M):
        nums = re.findall(r"(\d[\d ]*\d) ₽", line)
        pct = re.search(r"маржа ([\d.]+)%", line).group(1).replace(".", ",")
        for n in nums:
            check(n in s5, f"05: нет суммы {n} из строки модели «{line}»")
        check(pct + "%" in s5, f"05: нет маржи {pct}% из строки модели «{line}»")
    for key, val in totals.items():
        check(f"**{val}**" in s5, f"05: итог {key} {val} не совпадает с моделью")
    for amount in re.findall(r"= ([\d ]+) ₽$", log, re.M):
        check(amount in s5, f"05: строка модели {amount} ₽ отсутствует")

    def mln(v):
        return f"{int(v.replace(' ', '')) / 1e6:.2f}".replace(".", ",") + " млн ₽"

    first = re.search(r"Первый поток целиком: себестоимость ([\d ]+) ₽; цена ([\d ]+) ₽; "
                      r"маржа ([\d.]+)%", log)
    for v in [totals["NRE"], totals["OPEX"], first.group(1), first.group(2)]:
        check(mln(v) in s1, f"01: агрегат {mln(v)} не совпадает с моделью")
    check(first.group(3).replace(".", ",") + "%" in s1, "01: маржа первого потока")

    # КРИК-ГЕЙТ
    readme = (EXP / "README.md").read_text(encoding="utf-8")
    check("--- ПРОВЕРКА КРИК-ГЕЙТ ---" in readme, "README: нет блока КРИК-ГЕЙТ")
    check("КРИК-ГЕЙТ ПРОЙДЕН. Ошибок не выявлено." in readme,
          "README: нет итогового вердикта КРИК-ГЕЙТ")

    if errors:
        print("pop-3m: найдено ошибок:", len(errors))
        for e in errors:
            print(" -", e)
        return 1
    print(f"pop-3m: все проверки пройдены; 01 — {len(s1)} знаков; "
          f"кандидатов {len(cand)}; недель {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
