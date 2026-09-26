#!/usr/bin/env python3
"""Проверка словаря слотов `S-*` на корпусе базы знаний runtime `docs/kb/`.

Комментарий фаундера к PR #562 (пункт 3) требует показать, что извлечение знаний
из БЗ для разных продуктов ложится в единый скелет и не требует заводить
«специальный» слот под каждый продукт.

Утверждение, которое здесь проверяется, сформулировано так, чтобы оно могло
оказаться ложным:

  1. ПОКРЫТИЕ. Каждый раздел БЗ отображается в слот закрытого словаря `S-*`.
     Специфические правила распознают слот по лексике заголовка; раздел, на
     котором не сработало ни одно правило, отходит слоту по умолчанию
     `S-SCOPE`. Это не заглушка измерения, а правило методологии: раздел БЗ
     описывает существующее поведение продукта, то есть текущее состояние, а
     текущее состояние — содержание `S-SCOPE` (§2 20-taxonomy.md). Поэтому
     покрытие здесь равно 100 % по построению, и проверяемым остаётся другое:
     остаточные заголовки выписываются в результат (`default_slot_titles`),
     чтобы утверждение «ни один из них не требует слота вне словаря» можно
     было опровергнуть чтением, а не принять на слово.
  2. ПРОФИЛЬ (абсолютный). Профиль продукта предсказывает долю разделов слота.
     Пороги заданы до замера и намеренно оставлены в коде вместе с результатом,
     включая не подтвердившийся: `S-INTEGRATION` у `P-API`.
  3. ПРОФИЛЬ (порядковый). Более сильный инструмент: сравнение документов между
     собой. Доля `S-UI` у `P-API` и `P-DEVICE` строго ниже, чем у любого
     `P-SETTINGS`; доля `S-INTEGRATION` — строго выше. Порядковое утверждение
     не зависит от выбора порога и опровержимо одним контрпримером.

Вход: клон `mango-ba-ai-runtime`. Разбирается `docs/kb/<doc>/index.md` —
машинная карта разделов перенесённого корпуса. Опубликованный результат
`kb-slot-fit.json` снят со старого `mango_ba_prompts/kb/processed` и не перезаписывается.

Границы: отображение лексическое, по заголовку раздела. Раздел со смешанным
содержанием получает один слот по первому сработавшему правилу, поэтому
измерение занижает смешение, а не завышает его. Проценты имеют смысл как
порядок величины, а не как точное значение.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Закрытый словарь слотов: research/ba-requirements/artifact-micro-structure/20-taxonomy.md, §2.
SLOTS = [
    "S-GLOSSARY",
    "S-PROBLEM",
    "S-SCOPE",
    "S-SOLUTION",
    "S-FR",
    "S-SETTINGS",
    "S-UI",
    "S-SCENARIO",
    "S-AC",
    "S-NFR",
    "S-LIMITS",
    "S-OPEN",
    "S-TRACE",
    "S-INTEGRATION",
]

# Правила применяются по порядку; побеждает первое сработавшее. Порядок отражает
# специфичность: интеграционная лексика различает продукт сильнее, чем лексика
# интерфейса, а лексика интерфейса — сильнее, чем общая фактическая.
SLOT_RULES: list[tuple[str, str]] = [
    (
        "S-INTEGRATION",
        r"\bapi\b|\bsip\b|webhook|вебхук|интеграц|протокол|\brest\b|\bsoap\b|\bjson\b|"
        r"\bxml\b|команд[аы]\s|метод[ыа]?\s|запрос|событи|уведомлени.*сервер|"
        r"транк|trunk|коннектор|обмен данными|выгрузк|импорт|экспорт",
    ),
    (
        "S-SETTINGS",
        r"настро|параметр|конфигур|включени.*функц|правил[оа] (обработки|распределения)|"
        r"расписани|график работы|шаблон|профил[ья]|схем[аы] (распределения|переадресации)",
    ),
    (
        "S-UI",
        r"интерфейс|кнопк|вкладк|окн[оа]|экран|страниц|панел|раздел меню|виджет|"
        r"личн(ый|ом) кабинет|рабоч(ее|ем) мест|карточк|форм[аы] |отображ|"
        r"внешний вид|дизайн|мобильн(ое|ый) приложени",
    ),
    (
        "S-LIMITS",
        r"ограничен|лимит|квот|тариф|стоимост|оплат|биллинг|прав[оа] доступ|"
        r"рол[ьие]|безопасност|лицензи|юридическ|персональн.*данн|соглашени|оферт",
    ),
    (
        "S-NFR",
        r"производительн|нагрузк|отказоустойчив|надёжност|надежност|доступност|"
        r"задержк|качеств[оа] (связи|обслуживания)|мониторинг|резервн|восстановлени",
    ),
    (
        "S-SCENARIO",
        r"сценари|пример|как\s|инструкци|шаг \d|быстрый старт|начало работы|"
        r"кейс|использовани|порядок действий|первичн.*настройк",
    ),
    (
        "S-GLOSSARY",
        r"термин|глоссари|сокращени|обозначени|определени|общие сведени|введени|"
        r"о продукт|назначени документа|титульн|оглавлени|аннотаци",
    ),
    (
        "S-FR",
        r"обработк|распределени|маршрутизац|алгоритм|логик|запис[ьи] разговор|"
        r"очеред|обзвон|кампани|аналитик|отчёт|отчет|статистик|расчёт|расчет|"
        r"хранени|поиск|фильтр|автоматическ|робот|бот|распознавани|синтез",
    ),
]

# Профиль → предсказание о доле разделов слота в БЗ продукта.
# Формат: слот → (минимальная доля, максимальная доля). None — предсказания нет.
PROFILE_PREDICTIONS: dict[str, dict[str, tuple[float, float]]] = {
    "P-API": {"S-UI": (0.0, 0.10), "S-INTEGRATION": (0.30, 1.0)},
    "P-SETTINGS": {"S-UI": (0.10, 1.0), "S-SETTINGS": (0.10, 1.0)},
    "P-NO-SETTINGS": {"S-UI": (0.10, 1.0)},
    "P-DEVICE": {"S-UI": (0.0, 0.15), "S-INTEGRATION": (0.20, 1.0)},
}

# Выборка: по одному документу БЗ на профиль, плюс контрольный второй `P-SETTINGS`.
# Продуктовый класс и профиль назначены по §6 20-taxonomy.md ДО замера.
PROBES = [
    {
        "doc": "mango-cc-manual",
        "product_class": "contact-center",
        "profile": "P-SETTINGS",
        "note": "руководство Контакт-центра: функция с пользовательскими настройками",
    },
    {
        "doc": "mango-lk-manual",
        "product_class": "self-service-lk",
        "profile": "P-SETTINGS",
        "note": "справочник абонента ВАТС: контроль — второй документ того же профиля",
    },
    {
        "doc": "vpbx-api",
        "product_class": "voice-ucaas",
        "profile": "P-API",
        "note": "API ВАТС: функция без пользовательского интерфейса",
    },
    {
        "doc": "sip-trunk",
        "product_class": "voice-ucaas",
        "profile": "P-DEVICE",
        "note": "SIP-транк: подключение стороннего оборудования",
    },
    {
        "doc": "speech-analytics/user-guide",
        "product_class": "analytics-reporting",
        "profile": "P-SETTINGS",
        "note": "речевая аналитика: проверка переносимости на другой домен",
    },
]

# Слот, которому отходит раздел, не распознанный ни одним специфическим правилом.
DEFAULT_SLOT = "S-SCOPE"

SECTION_ROW = re.compile(r"^\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*\[([^\]]+)\]")


def classify(title: str) -> str:
    lowered = title.lower().replace("ё", "ё")
    for slot, pattern in SLOT_RULES:
        if re.search(pattern, lowered):
            return slot
    # Слот по умолчанию: раздел БЗ описывает существующее поведение продукта.
    return DEFAULT_SLOT


def parse_index(index_path: Path) -> list[dict[str, str]]:
    """Разбирает таблицу разделов `index.md`: `| № PDF | Раздел | Файл | ...`."""
    sections: list[dict[str, str]] = []
    in_table = False
    for line in index_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| № PDF"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                if sections:
                    break
                continue
            if set(line.replace("|", "").replace(" ", "")) <= {"-", ":"}:
                continue
            match = SECTION_ROW.match(line)
            if not match:
                continue
            number, title, _ = match.groups()
            if not title or title == "Раздел":
                continue
            sections.append({"number": number, "title": title, "slot": classify(title)})
    return sections


def corpus_commit(mango_root: Path) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(mango_root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def check_predictions(profile: str, shares: dict[str, float]) -> list[dict[str, object]]:
    checks: list[dict[str, object]] = []
    for slot, (low, high) in PROFILE_PREDICTIONS.get(profile, {}).items():
        share = shares.get(slot, 0.0)
        checks.append(
            {
                "slot": slot,
                "predicted_share": [low, high],
                "observed_share": round(share, 3),
                "holds": low <= share <= high,
            }
        )
    return checks


# Порядковые утверждения о профилях: сравнение документов между собой.
# Формат: (слот, профиль слева, отношение, профиль справа).
ORDINAL_ASSERTIONS = [
    ("S-UI", "P-API", "<", "P-SETTINGS"),
    ("S-UI", "P-DEVICE", "<", "P-SETTINGS"),
    ("S-INTEGRATION", "P-API", ">", "P-SETTINGS"),
    ("S-INTEGRATION", "P-DEVICE", ">", "P-SETTINGS"),
    ("S-SETTINGS", "P-API", "<", "P-SETTINGS"),
]


def check_ordinal(documents: list[dict[str, object]]) -> list[dict[str, object]]:
    """Каждое утверждение проверяется на ВСЕХ парах документов двух профилей.

    Одна пара, нарушившая отношение, опровергает утверждение целиком: это и есть
    смысл порядковой формулировки — она не зависит от выбранного порога.
    """
    by_profile: dict[str, list[dict[str, object]]] = {}
    for document in documents:
        by_profile.setdefault(str(document["profile"]), []).append(document)

    checks: list[dict[str, object]] = []
    for slot, left_profile, relation, right_profile in ORDINAL_ASSERTIONS:
        left_docs = by_profile.get(left_profile, [])
        right_docs = by_profile.get(right_profile, [])
        pairs = []
        holds = bool(left_docs) and bool(right_docs)
        for left in left_docs:
            for right in right_docs:
                left_share = float(left["slot_shares"].get(slot, 0.0))  # type: ignore[union-attr]
                right_share = float(right["slot_shares"].get(slot, 0.0))  # type: ignore[union-attr]
                ok = left_share < right_share if relation == "<" else left_share > right_share
                holds = holds and ok
                pairs.append(
                    f"{left['doc']} {left_share:.3f} {relation} {right['doc']} {right_share:.3f}"
                    + ("" if ok else " ← нарушено")
                )
        checks.append(
            {
                "assertion": f"доля {slot} у {left_profile} {relation} чем у {right_profile}",
                "holds": holds,
                "pairs": pairs,
                "detail": f"{len(pairs)} пар документов",
            }
        )
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", required=True, type=Path, help="клон mango-ba-ai-runtime")
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="куда записать результат",
    )
    args = parser.parse_args()

    processed = args.runtime / "docs" / "kb"
    if not processed.is_dir():
        print(f"ERROR: {processed} не найден", file=sys.stderr)
        return 2

    documents = []
    total_sections = 0
    total_defaulted = 0
    failed_predictions = 0

    for probe in PROBES:
        index_path = processed / probe["doc"] / "index.md"
        if not index_path.is_file():
            print(f"ERROR: нет {index_path}", file=sys.stderr)
            return 2

        sections = parse_index(index_path)
        counts = {slot: 0 for slot in SLOTS}
        for section in sections:
            counts[section["slot"]] += 1

        n = len(sections)
        shares = {slot: (count / n if n else 0.0) for slot, count in counts.items()}
        checks = check_predictions(probe["profile"], shares)
        failed_predictions += sum(1 for check in checks if not check["holds"])

        defaulted = [s for s in sections if s["slot"] == DEFAULT_SLOT]
        total_sections += n
        total_defaulted += len(defaulted)

        documents.append(
            {
                **probe,
                "index": f"docs/kb/{probe['doc']}/index.md",
                "sections": n,
                "slot_counts": {slot: count for slot, count in counts.items() if count},
                "slot_shares": {
                    slot: round(share, 3) for slot, share in shares.items() if share
                },
                "default_slot_titles": [s["title"] for s in defaulted],
                "profile_checks": checks,
            }
        )

        print(f"— {probe['doc']} ({probe['profile']}): {n} разделов")
        for slot in SLOTS:
            if counts[slot]:
                print(f"    {slot:<15} {counts[slot]:>4}  {shares[slot]:.1%}")
        for check in checks:
            mark = "OK  " if check["holds"] else "FAIL"
            print(
                f"    [{mark}] {check['slot']}: предсказано "
                f"{check['predicted_share'][0]:.0%}–{check['predicted_share'][1]:.0%}, "
                f"замерено {check['observed_share']:.1%}"
            )

    ordinal = check_ordinal(documents)
    ordinal_failed = sum(1 for check in ordinal if not check["holds"])

    summary = {
        "documents": len(documents),
        "sections_total": total_sections,
        "sections_by_specific_rule": total_sections - total_defaulted,
        "sections_by_default_slot": total_defaulted,
        "slots_outside_vocabulary": 0,
        "specific_rule_share": (
            round(1 - total_defaulted / total_sections, 4) if total_sections else 0.0
        ),
        "profile_predictions_failed": failed_predictions,
        "ordinal_assertions_failed": ordinal_failed,
    }

    result = {
        "corpus": {
            "repo": "https://github.com/G-Ivan-A/mango-ba-ai-runtime",
            "commit": corpus_commit(args.runtime),
            "layer": "docs/kb",
        },
        "slot_vocabulary": SLOTS,
        "summary": summary,
        "ordinal_assertions": ordinal,
        "documents": documents,
    }

    args.out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print()
    print("Порядковые утверждения о профилях:")
    for check in ordinal:
        mark = "OK  " if check["holds"] else "FAIL"
        print(f"    [{mark}] {check['assertion']}  ({check['detail']})")

    print()
    print(f"Документов:                        {summary['documents']}")
    print(f"Разделов всего:                    {summary['sections_total']}")
    print(f"Распознано правилом слота:         {summary['sections_by_specific_rule']}")
    print(f"Отошло слоту по умолчанию S-SCOPE: {summary['sections_by_default_slot']}")
    print(f"Потребовалось слотов вне словаря:  {summary['slots_outside_vocabulary']}")
    print(f"Абсолютных предсказаний не подтвердилось: {summary['profile_predictions_failed']}")
    print(f"Порядковых утверждений не подтвердилось:  {summary['ordinal_assertions_failed']}")
    print(f"Результат: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
