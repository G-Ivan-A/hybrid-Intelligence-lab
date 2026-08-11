#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

python3 - <<'PY'
from pathlib import Path
import re

rules_path = Path("ai-rules/agent-work-rules.md")
template_path = Path(".github/ISSUE_TEMPLATE/task.yml")
markdown_template_path = Path(".github/ISSUE_TEMPLATE/task.md")
governance_path = Path("ai-governance/ai-governance.md")
glossary_path = Path("standards/glossary.md")
workflow_path = Path("standards/issue-workflow.md")
onboarding_path = Path("ai-rules/agent-onboarding-protocol.md")


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


def markdown_modes() -> list[str]:
    text = rules_path.read_text(encoding="utf-8")
    match = re.search(
        r"^## Operating Modes\s*$\n(?P<section>.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        fail(f"{rules_path} must contain an Operating Modes section")

    rows = []
    for line in match.group("section").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 2 and cells[0] not in {"Mode", "---"}:
            rows.append(cells[0].lower())
    return rows


def dropdown_options(field_id: str) -> list[str]:
    lines = template_path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        if line.strip() == f"id: {field_id}":
            break
    else:
        fail(f"{template_path} must define the {field_id} field")

    options = []
    in_options = False
    for line in lines[index + 1 :]:
        stripped = line.strip()
        if re.match(r"^- type:", stripped):
            break
        if stripped == "options:":
            in_options = True
            continue
        if in_options:
            match = re.match(r"^- (.+)$", stripped)
            if match:
                options.append(match.group(1))
            elif stripped and not line.startswith("        "):
                break
    if not options:
        fail(f"{field_id} must define at least one option")
    return options


expected_modes = ["structured", "creative", "hybrid"]
expected_task_types = [
    "research",
    "education",
    "implementation",
    "audit",
    "analysis",
    "rfc",
    "adr",
]

rules_modes = markdown_modes()
template_modes = dropdown_options("operating_mode")
task_types = dropdown_options("task_type")

if rules_modes != expected_modes:
    fail(f"Operating Modes table must contain exactly {expected_modes}; got {rules_modes}")
if template_modes != expected_modes:
    fail(f"operating_mode options must match the table; got {template_modes}")
if task_types != expected_task_types:
    fail(f"task_type options must be exactly {expected_task_types}; got {task_types}")

for forbidden in ("research", "education", "deep-think"):
    if forbidden in template_modes:
        fail(f"{forbidden} must not be an operating_mode option")


def require_text(path: Path, needles: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            fail(f"{path} must contain {needle!r}")


require_text(
    rules_path,
    [
        "## Контракт автономии",
        "перечень закрытый",
        "## Контракт эскалации",
        "Не выполнено и вопросы",
        "## Контракт верификации",
        "V-1",
        "V-2",
        "Как проверяется",
    ],
)
for path in (template_path, markdown_template_path):
    require_text(path, ["Отклонения от постановки", "Не выполнено и вопросы"])
require_text(governance_path, ["ADR-010", "закрытый перечень"])
require_text(
    glossary_path,
    [
        "мета-контракт",
        "| Экспертное исполнение (Justified Deviation) |",
        "| Абсолютные границы (Hard Limits) |",
        "| Легальный выход (Legal Exit) |",
    ],
)
require_text(workflow_path, ["Отклонения от постановки", "Не выполнено и вопросы"])
require_text(
    onboarding_path,
    ["Принцип 1", "Принцип 2", "Принцип 3", "2026-08-adr-010-agent-autonomy-principles.md"],
)

legacy_template = Path(".github/ISSUE_TEMPLATE/task-creative.md")
require_text(legacy_template, ['name: ""', "Creative Task (consolidated)"])

print("Operating mode contract regression tests passed.")
PY
