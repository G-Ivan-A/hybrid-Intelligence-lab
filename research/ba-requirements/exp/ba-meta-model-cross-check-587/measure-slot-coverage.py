#!/usr/bin/env python3
"""Замер покрытия закрытого скелета A-BCREQ реальными артефактами БА.

Вопрос замера: даёт ли действующая практика БА воспроизводимый скелет и
какие слоты закрытого скелета `templates/bcreq-skeleton.md` в ней не
возникают вовсе. Ответ нужен задаче #587 как основание вердикта
«реинжиниринг сейчас / коррекция в опытной эксплуатации».

Вход  — historical-structure.yaml (подписи разделов реальных прогонов).
Выход — slot-coverage.json и печатный отчёт.

Запуск: python3 measure-slot-coverage.py
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKELETON = ROOT / (
    "projects/ba-gigacode-implementation/execution-package-mvp-bcreq/"
    "templates/bcreq-skeleton.md"
)

# Подпись слота → нормализованные лексемы, по которым слот опознаётся в
# произвольном заголовке БА. Словарь синонимов закрыт намеренно: он часть
# замера, а не догадка по смыслу.
SLOT_MARKERS = {
    "S-GLOSSARY": ["термин", "глоссар", "определени"],
    "S-PROBLEM": ["проблем", "цель", "задач"],
    "S-SCOPE": ["текущее состояние", "дельт", "границ"],
    "S-SOLUTION": ["описание решения", "разрабатываемого решения"],
    "S-FR": ["функциональные требования"],
    "S-SETTINGS": ["пользовательские настройки", "настройки"],
    "S-UI": ["ui", "интерфейс"],
    "S-SCENARIO": ["сценари", "use case", "юзкейс"],
    "S-AC": ["критерии приёмки", "критерии приемки", "приёмк", "приемк"],
    "S-NFR": ["нефункциональн"],
    "S-LIMITS": ["ограничен"],
    "S-OPEN": ["открытые вопрос"],
    "S-TRACE": ["прослеживаем", "трассируем"],
    "S-INTEGRATION": ["внешние интерфейс", "интеграц"],
}


def skeleton_slots() -> list[str]:
    """Читает состав слотов из самого скелета, а не из копии в скрипте."""
    text = SKELETON.read_text(encoding="utf-8")
    slots = re.findall(r"<!--\s*(S-[A-Z]+)", text)
    ordered: list[str] = []
    for slot in slots:
        if slot not in ordered:
            ordered.append(slot)
    return ordered


def load_runs() -> dict:
    """Минимальный разбор YAML замера: внешние зависимости не нужны."""
    data = {"runs": []}
    current = None
    for raw in (HERE / "historical-structure.yaml").read_text(
        encoding="utf-8"
    ).splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - run_id:"):
            current = {"run_id": line.split(":", 1)[1].strip(), "headings": []}
            data["runs"].append(current)
        elif current is not None and line.startswith("      - "):
            current["headings"].append(line.split("- ", 1)[1].strip().strip('"'))
        elif current is not None and line.startswith("    "):
            key, _, value = line.strip().partition(":")
            if key != "headings":
                current[key] = value.strip().strip('"')
    return data


def match_slots(heading: str) -> list[str]:
    low = heading.lower()
    # «Нефункциональные требования» содержит «функциональные требования»
    # как подстроку: без этой отсечки S-NFR ложно засчитывался бы и как S-FR.
    if "нефункциональн" in low:
        low_fr = low.replace("нефункциональные требования", " ")
    else:
        low_fr = low
    hit = []
    for slot, markers in SLOT_MARKERS.items():
        haystack = low_fr if slot == "S-FR" else low
        if any(marker in haystack for marker in markers):
            hit.append(slot)
    # «Ограничения» внутри «Особенности реализации» не должны давать S-SCOPE:
    # маркер «границ» ловит только явную границу изменения.
    return hit


def main() -> int:
    slots = skeleton_slots()
    if len(slots) != 14:
        print(f"ERROR: скелет дал {len(slots)} слотов вместо 14", file=sys.stderr)
        return 1

    runs = load_runs()["runs"]
    report = {"skeleton_slots": slots, "runs": [], "aggregate": {}}
    signatures = set()
    never_seen = set(slots)

    for run in runs:
        present, merged, unmapped = [], [], []
        for heading in run["headings"]:
            hit = match_slots(heading)
            if not hit:
                unmapped.append(heading)
                continue
            if len(hit) > 1:
                merged.append({"heading": heading, "slots": hit})
            for slot in hit:
                if slot not in present:
                    present.append(slot)
        never_seen -= set(present)
        signature = tuple(sorted(present))
        signatures.add(signature)
        report["runs"].append(
            {
                "run_id": run["run_id"],
                "task": run.get("task", ""),
                "locator": run.get("locator", ""),
                "headings_count": len(run["headings"]),
                "slots_present": present,
                "slots_missing": [s for s in slots if s not in present],
                "merged_headings": merged,
                "unmapped_headings": unmapped,
                "coverage": round(len(present) / len(slots), 3),
            }
        )

    report["aggregate"] = {
        "runs": len(runs),
        "distinct_skeletons": len(signatures),
        # M-1: доля прогонов, давших один и тот же состав разделов.
        "m1_structural_reproducibility": round(
            (len(runs) - len(signatures) + 1) / len(runs), 3
        )
        if len(signatures) < len(runs)
        else 0.0,
        "slots_never_present": sorted(never_seen),
        "runs_with_merged_headings": sum(
            1 for r in report["runs"] if r["merged_headings"]
        ),
    }

    (HERE / "slot-coverage.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"слотов в скелете: {len(slots)}")
    for r in report["runs"]:
        print(
            f"{r['run_id']}: разделов {r['headings_count']}, "
            f"покрытие {r['coverage']}, "
            f"слитых заголовков {len(r['merged_headings'])}"
        )
        for m in r["merged_headings"]:
            print(f"    слит: «{m['heading']}» → {', '.join(m['slots'])}")
    agg = report["aggregate"]
    print(
        f"прогонов {agg['runs']}, различных скелетов {agg['distinct_skeletons']}, "
        f"M-1 = {agg['m1_structural_reproducibility']}"
    )
    print("слоты, не встретившиеся ни разу: " + ", ".join(agg["slots_never_present"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
