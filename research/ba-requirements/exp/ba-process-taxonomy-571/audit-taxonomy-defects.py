#!/usr/bin/env python3
"""Аудит дефектов исторической таксономии процессов и операций БА.

Issue #571 требует пересобрать таксономию процессов и операций, но запрещает
делать это «по тексту»: дефекты действующих словарей должны быть предъявлены
замером, а не мнением. Скрипт отвечает на восемь вопросов, каждый из которых
соответствует одному оспариваемому месту действующей мета-модели Хаба
(projects/ba-gigacode-implementation/ba-meta-model/) и её источника — корпуса спицы
mango_ba_prompts.

D1. Слияние ФТ и ТЗ. Сколько раз действующие определения процессов называют
    выход «ФТ/ТЗ», при том что реестр артефактов той же спицы объявляет ФТ КК
    (A18) и ТЗ (A19) разными типами с разными стандартами-ориентирами.
D2. «Черновик» как объявленная граница процесса. Сколько определений процессов
    заканчиваются черновиком — состоянием жизненного цикла артефакта, а не
    результатом процесса.
D3. Множественность выхода операции. Сколько классов артефактов объявлено
    выходом одной операции в реестре онтологии спицы (§4, колонка «Выход»).
    Операция со многими классами выхода не имеет одного выходного контракта.
D4. Перечисление в определении операции. Сколько операций описаны через
    перечисление разнородных результатов («ФТ, ТЗ, резюме встреч, письма»).
D5. Потеря уровня подпроцесса. Объявлен ли подпроцесс сущностью в онтологии
    спицы и в мета-модели Хаба.
D6. Отсутствие Системы и Пользователя. Объявлены ли в таблице сущностей
    мета-модели Хаба система-объект изменения и пользователь, и есть ли в
    корпусе спрос на акторов.
D7. Использование словаря процессов. Сколько прогонов объявляют процесс из
    закрытого словаря, сколько — произвольную метку.
D8. Маршрут без ветвления. Есть ли в контракте маршрут-листа Хаба понятие
    ветвления и условия перехода.

Скрипт ничего не интерпретирует: интерпретация — в датированном отчёте
research/ba-requirements/2026-09-10-process-taxonomy-defects-facts.md.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Файлы корпуса спицы, несущие действующие определения процессов и операций.
SPOKE_PROCESS_FILES = (
    "docs/taxonomy.md",
    "docs/ba-processes/00-index.md",
    "standards/ba-ontology.md",
)

# Файлы мета-модели Хаба, унаследовавшие эти определения (issue #563).
HUB_META_MODEL_FILES = (
    "projects/ba-gigacode-implementation/ba-meta-model/00-introduction.md",
    "projects/ba-gigacode-implementation/ba-meta-model/10-theory.md",
    "projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md",
    "projects/ba-gigacode-implementation/ba-meta-model/30-decision-framework.md",
    "projects/ba-gigacode-implementation/ba-meta-model/40-practice-and-cases.md",
    "projects/ba-gigacode-implementation/ba-meta-model/50-open-research.md",
)

# Тринадцать операций действующего словаря спицы (docs/taxonomy.md §1).
DECLARED_OPERATIONS = (
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

# Девять процессов действующего словаря спицы (docs/taxonomy.md §2).
DECLARED_PROCESSES = (
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

# Слияние двух классов документа в одном имени выхода.
FR_TZ_MERGE = re.compile(r"ФТ\s*/\s*ТЗ")

# Черновик как объявленная граница работы, а не состояние артефакта.
DRAFT_AS_BOUNDARY = re.compile(r"до\s+чернович?к?а|черновик[аеу]?\s+ФТ|черновик\s+ФТ\s*/\s*ТЗ")
DRAFT_TOKEN = re.compile(r"чернови[кч]")

# Маркеры перечисления разнородных результатов в определении операции.
ENUMERATION_MARKERS = (",", ";", " или ", ":")

# Сущности, которых issue #571 требует в таблице сущностей мета-модели.
# Значение — допустимые написания имени (мета-модель ведёт часть имён латиницей).
REQUIRED_ENTITIES = {
    "Система": ("Система", "System"),
    "Пользователь": ("Пользователь", "User"),
    "Актор": ("Актор", "Actor"),
    "Подпроцесс": ("Подпроцесс", "Subprocess"),
}

# Понятия ветвления, которых требует определение маршрута как графа.
BRANCH_TOKENS = ("ветвлен", "ветк", "branch", "условие перехода", "when:", "gate_condition")


def git_commit(repo: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def table_rows(text: str, header_token: str) -> list[list[str]]:
    """Строки markdown-таблицы, чья шапка содержит header_token."""
    rows: list[list[str]] = []
    collecting = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            collecting = False
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if header_token in stripped and not collecting:
            collecting = True
            continue
        if not collecting:
            continue
        if set(stripped) <= set("| -:"):
            continue
        rows.append(cells)
    return rows


def d1_fr_tz_merge(spoke: Path, hub: Path) -> dict:
    hits = []
    for rel in SPOKE_PROCESS_FILES:
        for n, line in enumerate(read(spoke / rel).splitlines(), 1):
            if FR_TZ_MERGE.search(line):
                hits.append({"repo": "mango_ba_prompts", "file": rel, "line": n})
    for rel in HUB_META_MODEL_FILES:
        for n, line in enumerate(read(hub / rel).splitlines(), 1):
            if FR_TZ_MERGE.search(line):
                hits.append({"repo": "hybrid-Intelligence-lab", "file": rel, "line": n})

    ontology = read(spoke / "standards/ba-ontology.md")
    distinct_types = [t for t in ("feature-spec-kk", "tz-contract") if t in ontology]
    return {
        "question": "D1: слияние ФТ и ТЗ в одном имени выхода",
        "merge_hits": len(hits),
        "merge_locations": hits,
        "distinct_artifact_types_in_ontology": distinct_types,
        "contradiction": bool(hits) and len(distinct_types) == 2,
    }


def d2_draft_as_boundary(spoke: Path, hub: Path) -> dict:
    boundary_hits, token_hits = [], 0
    for repo_name, root, files in (
        ("mango_ba_prompts", spoke, SPOKE_PROCESS_FILES),
        ("hybrid-Intelligence-lab", hub, HUB_META_MODEL_FILES),
    ):
        for rel in files:
            for n, line in enumerate(read(root / rel).splitlines(), 1):
                if DRAFT_TOKEN.search(line):
                    token_hits += 1
                if DRAFT_AS_BOUNDARY.search(line):
                    boundary_hits.append(
                        {"repo": repo_name, "file": rel, "line": n, "text": line.strip()[:200]}
                    )

    lifecycle = read(spoke / "standards/ba-ontology.md")
    draft_is_state = "`draft`" in lifecycle and "черновик" in lifecycle
    return {
        "question": "D2: черновик объявлен границей процесса",
        "boundary_hits": len(boundary_hits),
        "boundary_locations": boundary_hits,
        "draft_token_hits": token_hits,
        "draft_declared_as_lifecycle_state": draft_is_state,
        "contradiction": bool(boundary_hits) and draft_is_state,
    }


def d3_operation_output_multiplicity(spoke: Path) -> dict:
    ontology = read(spoke / "standards/ba-ontology.md")
    rows = table_rows(ontology, "Стандарт")
    produced: dict[str, set[str]] = {op: set() for op in DECLARED_OPERATIONS}
    parsed_rows = 0
    for cells in rows:
        if len(cells) < 7 or not cells[0].startswith("A"):
            continue
        parsed_rows += 1
        artifact_type = cells[1].strip("`")
        producers = cells[4]
        for op in DECLARED_OPERATIONS:
            if re.search(rf"`{re.escape(op)}`", producers):
                produced[op].add(artifact_type)

    per_operation = {
        op: {"output_classes": sorted(v), "count": len(v)} for op, v in produced.items()
    }
    violating = sorted(op for op, v in produced.items() if len(v) > 1)
    return {
        "question": "D3: число классов выхода на одну операцию",
        "artifact_rows_parsed": parsed_rows,
        "per_operation": per_operation,
        "operations_with_multiple_outputs": violating,
        "violation_share": round(len(violating) / len(DECLARED_OPERATIONS), 3),
    }


def d4_enumerated_definitions(spoke: Path) -> dict:
    taxonomy = read(spoke / "docs/taxonomy.md")
    rows = table_rows(taxonomy, "Пример артефакта")
    findings = {}
    for cells in rows:
        if len(cells) < 4:
            continue
        op = cells[0].strip("`")
        if op not in DECLARED_OPERATIONS:
            continue
        definition = cells[2]
        markers = sum(definition.count(m) for m in ENUMERATION_MARKERS)
        findings[op] = {
            "definition": definition,
            "enumeration_markers": markers,
            "enumerates": markers >= 2,
        }
    enumerating = sorted(op for op, v in findings.items() if v["enumerates"])
    return {
        "question": "D4: определение операции перечисляет разнородные результаты",
        "operations_parsed": len(findings),
        "per_operation": findings,
        "operations_enumerating": enumerating,
    }


def d5_subprocess_level(spoke: Path, hub: Path) -> dict:
    ontology = read(spoke / "standards/ba-ontology.md")
    adr009 = read(spoke / "docs/adr/009-bcreq-formation-process.md")
    spoke_has = "Подпроцесс" in ontology
    spoke_subprocess_count = len(set(re.findall(r"П\d", adr009)))
    hub_hits = 0
    for rel in HUB_META_MODEL_FILES:
        hub_hits += len(re.findall(r"[Пп]одпроцесс", read(hub / rel)))
    return {
        "question": "D5: уровень подпроцесса между процессом и операцией",
        "spoke_declares_subprocess_entity": spoke_has,
        "spoke_named_subprocesses_in_adr009": spoke_subprocess_count,
        "hub_meta_model_mentions": hub_hits,
        "level_lost_in_hub": spoke_has and hub_hits == 0,
    }


def d6_missing_entities(spoke: Path, hub: Path) -> dict:
    theory = read(hub / "projects/ba-gigacode-implementation/ba-meta-model/10-theory.md")
    rows = table_rows(theory, "Ключ идентичности")
    declared = [cells[0].strip() for cells in rows if cells and cells[0].strip()]
    declared_plain = [re.sub(r"[`*]", "", d) for d in declared]
    missing = [
        name
        for name, spellings in REQUIRED_ENTITIES.items()
        if not any(sp in d for sp in spellings for d in declared_plain)
    ]

    actor_demand = 0
    prompts_dir = spoke / "prompts"
    if prompts_dir.is_dir():
        for prompt in sorted(prompts_dir.glob("*.md")):
            if re.search(r"актор|actor", read(prompt), flags=re.IGNORECASE):
                actor_demand += 1
    return {
        "question": "D6: Система и Пользователь как сущности мета-модели",
        "declared_entities": declared_plain,
        "missing_required_entities": missing,
        "spoke_prompts_requiring_actors": actor_demand,
    }


def d7_process_vocabulary_usage(spoke: Path) -> dict:
    runs = sorted((spoke / "runs").rglob("metadata.yaml")) if (spoke / "runs").is_dir() else []
    in_vocab, out_vocab, absent = 0, [], 0
    for meta in runs:
        text = read(meta)
        m = re.search(r"^process:\s*(.+)$", text, flags=re.MULTILINE)
        if not m:
            absent += 1
            continue
        value = m.group(1).strip().strip("\"'")
        if value in DECLARED_PROCESSES:
            in_vocab += 1
        else:
            out_vocab.append(value)
    return {
        "question": "D7: используется ли закрытый словарь процессов",
        "runs": len(runs),
        "process_declared_in_vocabulary": in_vocab,
        "process_declared_outside_vocabulary": len(out_vocab),
        "process_absent": absent,
        "outside_vocabulary_sample": sorted(set(out_vocab))[:15],
    }


def d8_route_without_branching(hub: Path) -> dict:
    framework = read(hub / "projects/ba-gigacode-implementation/ba-meta-model/30-decision-framework.md")
    theory = read(hub / "projects/ba-gigacode-implementation/ba-meta-model/10-theory.md")
    branch_hits = sum(
        len(re.findall(re.escape(token), framework + theory, flags=re.IGNORECASE))
        for token in BRANCH_TOKENS
    )
    immutability_hits = len(re.findall(r"[Мм]аршрут неизменен|неизменност\w* маршрута", framework + theory))
    linear_steps = "steps:" in framework
    return {
        "question": "D8: маршрут как граф с ветвлением",
        "branch_tokens_found": branch_hits,
        "route_immutability_statements": immutability_hits,
        "route_sheet_declares_linear_steps": linear_steps,
        "route_is_linear_only": branch_hits == 0 and linear_steps,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mango", required=True, type=Path, help="клон mango_ba_prompts")
    parser.add_argument("--hub", type=Path, default=Path("."), help="корень hybrid-Intelligence-lab")
    parser.add_argument("--json", type=Path, default=Path("taxonomy-defects.json"))
    args = parser.parse_args()

    spoke, hub = args.mango.resolve(), args.hub.resolve()
    if not (spoke / "docs/taxonomy.md").is_file():
        print(f"нет корпуса спицы: {spoke}", file=sys.stderr)
        return 2

    findings = {
        "D1": d1_fr_tz_merge(spoke, hub),
        "D2": d2_draft_as_boundary(spoke, hub),
        "D3": d3_operation_output_multiplicity(spoke),
        "D4": d4_enumerated_definitions(spoke),
        "D5": d5_subprocess_level(spoke, hub),
        "D6": d6_missing_entities(spoke, hub),
        "D7": d7_process_vocabulary_usage(spoke),
        "D8": d8_route_without_branching(hub),
    }

    result = {
        "corpus": {
            "spoke": str(spoke),
            "spoke_commit": git_commit(spoke),
            "hub_commit": git_commit(hub),
        },
        "findings": findings,
    }
    args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"корпус спицы: {result['corpus']['spoke_commit']}")
    print(f"корпус Хаба:  {result['corpus']['hub_commit']}")
    d1 = findings["D1"]
    print(
        f"D1 ФТ/ТЗ как один выход: {d1['merge_hits']} мест; "
        f"в онтологии спицы это разные типы: {d1['distinct_artifact_types_in_ontology']}"
    )
    d2 = findings["D2"]
    print(
        f"D2 черновик как граница процесса: {d2['boundary_hits']} мест; "
        f"черновик объявлен состоянием ЖЦ: {d2['draft_declared_as_lifecycle_state']}"
    )
    d3 = findings["D3"]
    print(
        f"D3 операций с более чем одним классом выхода: "
        f"{len(d3['operations_with_multiple_outputs'])} из {len(DECLARED_OPERATIONS)} "
        f"({d3['violation_share']}): {d3['operations_with_multiple_outputs']}"
    )
    d4 = findings["D4"]
    print(f"D4 операций с перечислением в определении: {len(d4['operations_enumerating'])} из {d4['operations_parsed']}")
    d5 = findings["D5"]
    print(
        f"D5 подпроцесс: спица объявляет={d5['spoke_declares_subprocess_entity']}, "
        f"именованных подпроцессов в ADR-009={d5['spoke_named_subprocesses_in_adr009']}, "
        f"упоминаний в мета-модели Хаба={d5['hub_meta_model_mentions']}"
    )
    d6 = findings["D6"]
    print(
        f"D6 отсутствующие сущности: {d6['missing_required_entities']}; "
        f"промптов, требующих акторов: {d6['spoke_prompts_requiring_actors']}"
    )
    d7 = findings["D7"]
    print(
        f"D7 прогонов {d7['runs']}: процесс из словаря={d7['process_declared_in_vocabulary']}, "
        f"вне словаря={d7['process_declared_outside_vocabulary']}, без поля={d7['process_absent']}"
    )
    d8 = findings["D8"]
    print(
        f"D8 маршрут: маркеров ветвления={d8['branch_tokens_found']}, "
        f"утверждений неизменности={d8['route_immutability_statements']}, "
        f"линейный steps[]={d8['route_sheet_declares_linear_steps']}"
    )
    print(f"результат: {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
