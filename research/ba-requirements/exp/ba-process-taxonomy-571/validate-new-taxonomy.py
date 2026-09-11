#!/usr/bin/env python3
"""Проверка новой таксономии процессов и операций на синтетических кейсах.

Словари не дублируются в коде: они читаются прямо из модулей исследования,
поэтому расхождение текста и проверки невозможно по построению. Эталоны берутся
из 2026-09-10-synthetic-cases.md.

Режим --legacy воспроизводит дефект до исправления: те же кейсы проверяются
против прежнего словаря девяти процессов и тринадцати операций и не должны в
нём выражаться. Успех в этом режиме означает, что дефект воспроизведён.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PROCESS_MODULE = "projects/ba-gigacode-implementation/ba-process-taxonomy/20-taxonomy.md"
OPERATION_MODULE = "projects/ba-gigacode-implementation/ba-operation-taxonomy/20-taxonomy.md"
CASES = "research/ba-requirements/exp/ba-process-taxonomy-571/2026-09-10-synthetic-cases.md"

# Прежние словари спицы (docs/taxonomy.md §2 и §3) — предмет режима --legacy.
LEGACY_PROCESSES = (
    "fr-generation",
    "fr-validation",
    "tender-analysis",
    "uc-us-modeling",
    "uml-bpmn-visualization",
    "po-pm-support",
    "statistics",
    "impact-analysis",
    "risk-analysis",
)
LEGACY_OPERATIONS = (
    "ingestion",
    "understanding",
    "validation",
    "modeling",
    "solution_design",
    "documentation",
    "quality",
    "research",
    "governance",
    "impact_analysis",
    "reverse_requirements",
    "risk_analysis",
    "release_readiness",
)

CODE = re.compile(r"`([^`]+)`")
PROCESS_CODE = re.compile(r"^P-\d{2}$")
SKILL_CODE = re.compile(r"^SK-[a-z0-9]+(-[a-z0-9]+)*$")
OPERATION_CODE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)+$")
TIER = re.compile(r"^G[1-7]$")


def read(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"нет файла: {path}")
    return path.read_text(encoding="utf-8")


def rows(text: str) -> list[list[str]]:
    """Все строки markdown-таблиц файла как списки ячеек."""
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|") or set(s) <= set("| -:"):
            continue
        out.append([c.strip() for c in s.strip("|").split("|")])
    return out


def section(text: str, start: str, end: str) -> str:
    """Фрагмент между двумя заголовками; end может отсутствовать."""
    i = text.find(start)
    if i < 0:
        raise SystemExit(f"нет раздела {start!r}")
    j = text.find(end, i + len(start))
    return text[i:] if j < 0 else text[i:j]


def first_code(cell: str) -> str | None:
    m = CODE.search(cell)
    return m.group(1) if m else None


def all_codes(cell: str) -> list[str]:
    return CODE.findall(cell)


def parse_processes(text: str) -> dict[str, dict]:
    """§4: коды L2, целевой выход, критерий завершения."""
    out: dict[str, dict] = {}
    for cells in rows(section(text, "## 4. `L2`", "## 5.")):
        code = first_code(cells[0]) if cells else None
        if not code or not PROCESS_CODE.match(code):
            continue
        out[code] = {
            "name": first_code(cells[1]) or cells[1],
            "l1": first_code(cells[2]) if len(cells) > 2 else None,
            "output": cells[5] if len(cells) > 5 else "",
            "completion": cells[6] if len(cells) > 6 else "",
        }
    return out


def parse_skills(text: str) -> dict[str, dict]:
    """§5: навык → процесс, ярус."""
    out: dict[str, dict] = {}
    for cells in rows(section(text, "## 5. `L3`", "## 6.")):
        code = first_code(cells[0]) if cells else None
        if not code or not SKILL_CODE.match(code):
            continue
        out[code] = {
            "process": first_code(cells[1]) if len(cells) > 1 else None,
            "tier": first_code(cells[4]) if len(cells) > 4 else None,
        }
    return out


def parse_operations(text: str) -> dict[str, dict]:
    """§2: каталог операций; поля контракта берутся из колонок таблицы."""
    out: dict[str, dict] = {}
    body = section(text, "## 2. Каталог", "## 3. Сводка")
    current_class = None
    class_by_heading = {
        "### 2.1": "extract",
        "### 2.2": "transform",
        "### 2.3": "generate",
        "### 2.4": "check",
        "### 2.5": "assess",
    }
    for line in body.splitlines():
        s = line.strip()
        for prefix, name in class_by_heading.items():
            if s.startswith(prefix):
                current_class = name
        if not s.startswith("|") or set(s) <= set("| -:"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        code = first_code(cells[0])
        if not code or not OPERATION_CODE.match(code) or len(cells) < 5:
            continue
        out[code] = {
            "class": current_class,
            "input": cells[1],
            "output": cells[2],
            "refusal": cells[3],
            "tier": first_code(cells[4]),
        }
    return out


def parse_decomposition(text: str) -> dict[str, list[str]]:
    """§4 модуля операций: навык → упорядоченный перечень операций."""
    out: dict[str, list[str]] = {}
    for cells in rows(section(text, "## 4. Разложение", "## 5. Реестр")):
        code = first_code(cells[0]) if cells else None
        if not code or not SKILL_CODE.match(code) or len(cells) < 3:
            continue
        out[code] = [c for c in all_codes(cells[2]) if OPERATION_CODE.match(c)]
    return out


def parse_cases(text: str) -> list[dict]:
    """Шаги кейсов: номер, процесс, навык, операции, гейт."""
    steps: list[dict] = []
    case = None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("## SC-"):
            case = s[3:].split(".")[0]
        if not s.startswith("|") or set(s) <= set("| -:"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 5 or not cells[0].isdigit():
            continue
        process = first_code(cells[1])
        skill = first_code(cells[2])
        if not process or not skill:
            continue
        steps.append(
            {
                "case": case,
                "step": int(cells[0]),
                "process": process,
                "skill": skill,
                "operations": all_codes(cells[3]),
                "gate": first_code(cells[4]),
            }
        )
    return steps


def check(hub: Path) -> dict:
    process_text = read(hub / PROCESS_MODULE)
    operation_text = read(hub / OPERATION_MODULE)
    cases_text = read(hub / CASES)

    processes = parse_processes(process_text)
    skills = parse_skills(process_text)
    operations = parse_operations(operation_text)
    decomposition = parse_decomposition(operation_text)
    steps = parse_cases(cases_text)

    errors: list[str] = []

    # C1. Навык принадлежит объявленному процессу и имеет ярус.
    for skill, meta in skills.items():
        if meta["process"] not in processes:
            errors.append(f"C1 навык {skill}: процесс {meta['process']} вне словаря L2")
        if not meta["tier"] or not TIER.match(meta["tier"]):
            errors.append(f"C1 навык {skill}: ярус не объявлен")

    # C2. Множества навыков в двух модулях совпадают.
    for skill in sorted(set(skills) - set(decomposition)):
        errors.append(f"C2 навык {skill} объявлен, но не разложен на операции")
    for skill in sorted(set(decomposition) - set(skills)):
        errors.append(f"C2 навык {skill} разложен, но не объявлен в таксономии процессов")

    # C3. Разложение использует только значения каталога и непусто.
    for skill, ops in decomposition.items():
        if not ops:
            errors.append(f"C3 навык {skill}: пустое разложение")
        for op in ops:
            if op not in operations:
                errors.append(f"C3 навык {skill}: операция {op} вне каталога")

    # C4. Контракт операции заполнен полностью (OC-2, EO-1..EO-4).
    for op, meta in operations.items():
        for field in ("class", "input", "output", "refusal", "tier"):
            if not meta.get(field):
                errors.append(f"C4 операция {op}: не заполнено поле {field}")
        if meta["tier"] and not TIER.match(meta["tier"]):
            errors.append(f"C4 операция {op}: ярус {meta['tier']} вне шкалы G1-G7")

    # C5. Каждая операция каталога вызывается хотя бы одним навыком.
    used = {op for ops in decomposition.values() for op in ops}
    for op in sorted(set(operations) - used):
        errors.append(f"C5 операция {op} не вызывается ни одним навыком")

    # C6. Каждый шаг кейса выражается словарями.
    for st in steps:
        tag = f"{st['case']} шаг {st['step']}"
        if st["process"] not in processes:
            errors.append(f"C6 {tag}: процесс {st['process']} вне словаря")
        if st["skill"] not in skills:
            errors.append(f"C6 {tag}: навык {st['skill']} вне словаря")
            continue
        if skills[st["skill"]]["process"] != st["process"]:
            errors.append(
                f"C6 {tag}: навык {st['skill']} принадлежит "
                f"{skills[st['skill']]['process']}, а объявлен в {st['process']}"
            )
        declared = decomposition.get(st["skill"], [])
        for op in st["operations"]:
            if op not in declared:
                errors.append(f"C6 {tag}: операция {op} не входит в разложение {st['skill']}")

    # C7. Полнота покрытия кейсами.
    covered_processes = {st["process"] for st in steps}
    covered_skills = {st["skill"] for st in steps}
    covered_ops = {op for st in steps for op in st["operations"]}
    for code in sorted(set(processes) - covered_processes):
        errors.append(f"C7 процесс {code} не покрыт ни одним кейсом")
    for code in sorted(set(skills) - covered_skills):
        errors.append(f"C7 навык {code} не покрыт ни одним кейсом")
    for code in sorted(set(operations) - covered_ops):
        errors.append(f"C7 операция {code} не покрыта ни одним кейсом")

    return {
        "mode": "new",
        "counts": {
            "processes": len(processes),
            "skills": len(skills),
            "operations": len(operations),
            "case_steps": len(steps),
            "cases": len({st["case"] for st in steps}),
        },
        "coverage": {
            "processes": f"{len(covered_processes)}/{len(processes)}",
            "skills": f"{len(covered_skills)}/{len(skills)}",
            "operations": f"{len(covered_ops)}/{len(operations)}",
        },
        "errors": errors,
        "passed": not errors,
    }


def check_legacy(hub: Path) -> dict:
    """Воспроизведение дефекта: те же кейсы в прежнем словаре невыразимы."""
    steps = parse_cases(read(hub / CASES))
    unexpressible = []
    for st in steps:
        reasons = []
        if st["process"] not in LEGACY_PROCESSES:
            reasons.append(f"процесс {st['process']} отсутствует в прежнем словаре")
        if st["skill"]:
            reasons.append("уровень навыка в прежней модели не существует")
        outside = [op for op in st["operations"] if op not in LEGACY_OPERATIONS]
        if outside:
            reasons.append(f"операции вне прежнего словаря: {', '.join(outside)}")
        if reasons:
            unexpressible.append(
                {"case": st["case"], "step": st["step"], "reasons": reasons}
            )
    return {
        "mode": "legacy",
        "case_steps": len(steps),
        "unexpressible_steps": len(unexpressible),
        "sample": unexpressible[:3],
        "defect_reproduced": len(unexpressible) == len(steps) and bool(steps),
        "passed": len(unexpressible) == len(steps) and bool(steps),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hub", type=Path, default=Path("."), help="корень hybrid-Intelligence-lab")
    parser.add_argument("--json", type=Path, default=None)
    parser.add_argument("--legacy", action="store_true", help="проверка прежнего словаря")
    args = parser.parse_args()

    hub = args.hub.resolve()
    result = check_legacy(hub) if args.legacy else check(hub)

    if args.json:
        args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if result["mode"] == "legacy":
        print(f"шагов кейсов: {result['case_steps']}")
        print(f"невыразимых в прежнем словаре: {result['unexpressible_steps']}")
        print(f"дефект воспроизведён: {result['defect_reproduced']}")
    else:
        c = result["counts"]
        print(f"процессов: {c['processes']}, навыков: {c['skills']}, операций: {c['operations']}")
        print(f"кейсов: {c['cases']}, шагов: {c['case_steps']}")
        print(
            f"покрытие: процессы {result['coverage']['processes']}, "
            f"навыки {result['coverage']['skills']}, операции {result['coverage']['operations']}"
        )
        for e in result["errors"]:
            print(f"ОШИБКА: {e}", file=sys.stderr)
        print(f"ошибок: {len(result['errors'])}")

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
