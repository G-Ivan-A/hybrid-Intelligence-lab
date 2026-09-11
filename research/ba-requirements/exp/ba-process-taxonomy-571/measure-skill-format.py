#!/usr/bin/env python3
"""Замер гипотезы фаундера о природе навыка и формате контракта (issue #571).

Комментарий фаундера к PR #572 выдвинул две гипотезы, которые нельзя принять
или отвергнуть по тексту — их нужно измерить.

H1. «Подпроцесс требует формата stepwise, операция — формата oneshot».
    Проверяется на историческом корпусе спицы mango_ba_prompts: 24 промпта
    несут режим в имени файла (`-oneshot`, `-stepwise`, `-legacy`), то есть
    автор корпуса уже разметил формат руками. Если гипотеза верна, режим
    обязан отделяться каким-то признаком самого контракта, а не только именем.

    Скрипт измеряет три признака каждого промпта:
      handoff — точки возврата управления актору внутри прогона
                («Жди ответа», «ВОПРОС К ПОЛЬЗОВАТЕЛЮ» и подобные);
      stages  — объявленные шаги («ШАГ N») и маркеры внутреннего алгоритма;
      outputs — сколько разных классов результата промпт обязуется выдать.

H2. «Операция эквивалентна навыку формата oneshot», то есть oneshot ⇒ атомарность.
    Проверяется на тех же промптах: если oneshot-промпты содержат внутренний
    упорядоченный алгоритм или обещают более одного класса выхода, то oneshot
    атомарности не означает и обратная импликация ложна.

H3. Есть ли в новом каталоге L3 навык, состоящий ровно из одной операции,
    и какие операции переиспользуются достаточно, чтобы иметь смысл в форме
    самостоятельного навыка. Считается по таблице разложения навыков
    ba-operation-taxonomy/20-taxonomy.md §4.

Интерпретация — в датированном отчёте
research/ba-requirements/2026-09-10-skill-granularity-format-facts.md.

Использование:
    python3 measure-skill-format.py --mango /tmp/mango --hub ../../../.. \
        --json skill-format.json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Точка возврата управления актору внутри прогона: контракт не может
# продолжиться, пока актор не ответил.
HANDOFF_MARKERS = (
    "жди ответа",
    "жди подтверждения",
    "вопрос к пользователю",
    "дождись ответа",
    "спроси у пользователя",
    "запроси подтверждение",
    "жду ответа",
)

# Маркеры внутреннего упорядоченного алгоритма: контракт состоит более чем из
# одного действия, даже если управление актору не возвращается.
STAGE_MARKERS = (
    "алгоритм",
    "порядок действий",
    "как работаем",
    "этап",
    "сначала",
    "затем",
    "после этого",
)

STEP_RE = re.compile(r"^\s*(?:ШАГ|Шаг)\s*\d+", re.MULTILINE)

# Классы результата, которые промпт может пообещать. Ключ — класс, значение —
# лексические признаки его объявления в тексте промпта.
OUTPUT_CLASSES = {
    "requirements": ("функциональные требования", "раздел 4", "нумерованный список"),
    "report": ("отчет валидации", "отчёт валидации", "отчет", "отчёт"),
    "questions": ("уточняющих вопрос", "уточняющие вопрос", "список вопросов"),
    "scenarios": ("сценари",),
    "glossary": ("глоссари",),
    "matrix": ("матриц",),
}

MODES = ("oneshot", "stepwise", "legacy")


def commit(path: Path) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def count_markers(text: str, markers: tuple[str, ...]) -> int:
    low = text.lower()
    return sum(low.count(marker) for marker in markers)


def measure_prompts(mango: Path) -> dict:
    prompts_dir = mango / "prompts"
    if not prompts_dir.is_dir():
        raise SystemExit(f"нет каталога промптов: {prompts_dir}")

    items = []
    for path in sorted(prompts_dir.glob("*.md")):
        mode = next((m for m in MODES if path.stem.endswith(f"-{m}")), None)
        if mode is None:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        low = text.lower()
        outputs = sorted(
            name for name, marks in OUTPUT_CLASSES.items()
            if any(mark in low for mark in marks)
        )
        items.append({
            "file": f"prompts/{path.name}",
            "mode": mode,
            "handoff": count_markers(text, HANDOFF_MARKERS),
            "declared_steps": len(STEP_RE.findall(text)),
            "stage_markers": count_markers(text, STAGE_MARKERS),
            "output_classes": outputs,
            "words": len(text.split()),
        })

    by_mode = {m: [i for i in items if i["mode"] == m] for m in MODES}
    summary = {
        m: {
            "prompts": len(group),
            "with_handoff": sum(1 for i in group if i["handoff"] > 0),
            "with_internal_order": sum(
                1 for i in group if i["declared_steps"] > 0 or i["stage_markers"] > 0
            ),
            "multi_output": sum(1 for i in group if len(i["output_classes"]) > 1),
        }
        for m, group in by_mode.items()
    }
    return {"items": items, "by_mode": summary}


SKILL_ROW_RE = re.compile(
    r"^\|\s*`(SK-[a-z0-9-]+)`\s*\|\s*`(P-\d+)`\s*\|\s*(.+?)\s*\|\s*$", re.MULTILINE
)
OP_RE = re.compile(r"`([a-z][a-z0-9-]+)`")


def measure_catalogue(hub: Path) -> dict:
    source = hub / "projects/ba-gigacode-implementation/ba-operation-taxonomy/20-taxonomy.md"
    text = source.read_text(encoding="utf-8")
    skills = {}
    for name, process, cell in SKILL_ROW_RE.findall(text):
        ops = OP_RE.findall(cell)
        if ops:
            skills[name] = {"process": process, "operations": ops}

    reuse: dict[str, list[str]] = {}
    for name, item in skills.items():
        for op in item["operations"]:
            reuse.setdefault(op, []).append(name)

    single = sorted(n for n, i in skills.items() if len(i["operations"]) == 1)
    # Кандидат в навык-операцию: операция вызывается из трёх и более навыков,
    # то есть её переиспользование выражено не одним владельцем.
    candidates = sorted(
        (op for op, users in reuse.items() if len(users) >= 3),
        key=lambda op: (-len(reuse[op]), op),
    )
    return {
        "skills": len(skills),
        "operations": len(reuse),
        "single_operation_skills": single,
        "min_operations_per_skill": min((len(i["operations"]) for i in skills.values()), default=0),
        "max_operations_per_skill": max((len(i["operations"]) for i in skills.values()), default=0),
        "reuse": {op: len(users) for op, users in sorted(reuse.items())},
        "reuse_candidates": [{"operation": op, "callers": len(reuse[op])} for op in candidates],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mango", required=True, help="клон спицы mango_ba_prompts")
    parser.add_argument("--hub", default="../../../..", help="корень Хаба")
    parser.add_argument("--json", default="skill-format.json")
    args = parser.parse_args()

    mango, hub = Path(args.mango).resolve(), Path(args.hub).resolve()
    prompts = measure_prompts(mango)
    catalogue = measure_catalogue(hub)

    one, step, legacy = (prompts["by_mode"][m] for m in MODES)
    # H1 подтверждается, если признак handoff разделяет режимы без пересечения.
    h1 = (
        step["with_handoff"] == step["prompts"]
        and one["with_handoff"] == 0
        and legacy["with_handoff"] == 0
    )
    # H2 опровергается, если oneshot-промпты несут внутренний порядок.
    h2_refuted = one["with_internal_order"] == one["prompts"]

    result = {
        "measured_at": "2026-09-10",
        "source_issue": "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571",
        "corpus": {"mango": commit(mango), "hub": commit(hub)},
        "prompts": prompts,
        "catalogue": catalogue,
        "verdicts": {
            "H1_handoff_separates_modes": h1,
            "H2_oneshot_implies_atomic_refuted": h2_refuted,
            "H3_single_operation_skills": len(catalogue["single_operation_skills"]),
        },
    }
    Path(args.json).write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    for mode in MODES:
        s = prompts["by_mode"][mode]
        print(
            f"{mode}: промптов {s['prompts']}, с точкой возврата управления "
            f"{s['with_handoff']}, с внутренним порядком {s['with_internal_order']}, "
            f"с более чем одним классом выхода {s['multi_output']}"
        )
    print(
        f"каталог L3: навыков {catalogue['skills']}, операций {catalogue['operations']}, "
        f"навыков из одной операции {len(catalogue['single_operation_skills'])}, "
        f"операций на навык {catalogue['min_operations_per_skill']}–"
        f"{catalogue['max_operations_per_skill']}"
    )
    print(
        "кандидаты в навык-операцию (вызывается из трёх и более навыков): "
        + ", ".join(
            f"{c['operation']} ({c['callers']})" for c in catalogue["reuse_candidates"]
        )
    )
    print(f"H1 (точка возврата отделяет stepwise от oneshot): {'да' if h1 else 'нет'}")
    print(f"H2 (oneshot ⇒ атомарность) опровергнута: {'да' if h2_refuted else 'нет'}")
    return 0 if h1 and h2_refuted else 1


if __name__ == "__main__":
    sys.exit(main())
