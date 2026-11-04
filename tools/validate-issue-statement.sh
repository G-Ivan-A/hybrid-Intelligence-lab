#!/usr/bin/env bash
# Гейт постановки задачи (B-116 (d), issue #727; решение Г-1 анализа
# docs/analysis/2026-11-04-sprint-13-hub-normative-debt-selection.md).
#
# Проверяет тело issue ДО передачи задачи агенту: пути, которые постановка
# предписывает в разделах «Готово, когда» и «Задача исполнителю», не должны
# попадать в запреты `<forbidden>` корневого AGENTS.md и должны лежать в
# объявленных домах (`<artifact_homes>`, ядро и `project_specific_directories`
# из .hub-profile.json). Нормы: standards/issue-workflow.md
# («Правила формулирования уровней», «Точки автоматизации») и
# standards/contract-documentation-standard.md («Где живёт контракт»).
#
# Проверки:
#   1. Путь `docs/contracts/` на любой глубине — запрещён; дом контракта —
#      ai-rules/ (контракт агента) или ops/<name>.md (контракт процесса).
#   2. Новый каталог верхнего уровня, которого нет в корне репозитория и нет в
#      `project_specific_directories`, — запрещён без записи о решении.
#   3. Предписание поля frontmatter `ai-generated:` — запрещено; участников
#      называют полями contributors и ai-models (ADR-023).
#
# Разбор свободного текста эвристический и намеренно узкий:
#   - проверяются только разделы «Готово, когда» и «Задача исполнителю»
#     (тот же путь в «Контексте» допустим: там он описывает факт, а не результат);
#   - строка с отрицанием («не», «нет», «без», «запрещ…», not/no/never)
#     описывает запрет, а не результат, и пропускается;
#   - URL вырезаются до разбора;
#   - кандидат в каталог верхнего уровня — токен в обратных кавычках из двух и
#     более сегментов: `a/b.ext`, `a/b/` или `a/b/c`. Одиночный `a/` и `owner/repo`
#     без расширения путём от корня не считаются: в постановках это обычно имя
#     подкаталога относительно названного выше проекта;
#   - каталог, перенесённый записью `path_migrations` из .hub-profile.json,
#     получает подсказку с новым путём.
#
# Использование:
#   tools/validate-issue-statement.sh <файл-тела-issue>
#   tools/validate-issue-statement.sh -            # тело из stdin
#   tools/validate-issue-statement.sh --issue N [--repo OWNER/REPO]
#
# Переменные окружения:
#   ISSUE_STATEMENT_ROOT — корень репозитория для сверки каталогов верхнего
#                          уровня (по умолчанию корень этого репозитория).
#
# Коды возврата: 0 — постановка проходит; 1 — найдены нарушения; 2 — ошибка вызова.
# Гейт только краснит проверку и ничего не публикует от имени владельца.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
repo_root="${ISSUE_STATEMENT_ROOT:-$ROOT_DIR}"

usage() {
  printf 'usage: %s <issue-body-file> | - | --issue N [--repo OWNER/REPO]\n' "$(basename "$0")" >&2
  exit 2
}

body_file=""
issue_number=""
issue_repo=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --issue) [[ $# -ge 2 ]] || usage; issue_number="$2"; shift 2 ;;
    --repo) [[ $# -ge 2 ]] || usage; issue_repo="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) [[ -z "$body_file" ]] || usage; body_file="$1"; shift ;;
  esac
done

tmp_body="$(mktemp)"
trap 'rm -f "$tmp_body"' EXIT

if [[ -n "$issue_number" ]]; then
  [[ -z "$body_file" ]] || usage
  repo_args=()
  [[ -z "$issue_repo" ]] || repo_args=(--repo "$issue_repo")
  gh issue view "$issue_number" "${repo_args[@]}" --json body -q .body >"$tmp_body"
elif [[ "$body_file" == "-" ]]; then
  cat >"$tmp_body"
elif [[ -n "$body_file" ]]; then
  [[ -f "$body_file" ]] || { printf 'issue-statement: file not found: %s\n' "$body_file" >&2; exit 2; }
  cat "$body_file" >"$tmp_body"
else
  usage
fi

python3 -I - "$tmp_body" "$repo_root" <<'PY'
import json
import os
import re
import sys

body_path, repo_root = sys.argv[1], sys.argv[2]
with open(body_path, encoding="utf-8") as handle:
    lines = handle.read().replace("\r\n", "\n").split("\n")

CHECKED = ("готово, когда", "задача исполнителю", "definition of done")
NEGATION = re.compile(r"(?<![\w-])(не|нет|без|запрещ\w*|not|no|never|forbidden)(?![\w-])", re.IGNORECASE)
URL = re.compile(r"https?://\S+")
CODE_SPAN = re.compile(r"`([^`\n]+)`")
CONTRACTS = re.compile(r"(?<![\w.-])(?:[\w.-]+/)*docs/contracts(?![\w-])")
AI_GENERATED = re.compile(r"(?<![\w-])ai-generated\s*:")
PATH_TOKEN = re.compile(r"^(?:\./|/)?([A-Za-z0-9._-]+)/([A-Za-z0-9._*<>{}/-]*)$")

known_top = set()
moved_top = {}
if os.path.isdir(repo_root):
    known_top = {entry for entry in os.listdir(repo_root) if os.path.isdir(os.path.join(repo_root, entry))}
profile_path = os.path.join(repo_root, ".hub-profile.json")
if os.path.isfile(profile_path):
    with open(profile_path, encoding="utf-8") as handle:
        profile = json.load(handle)
    for entry in profile.get("project_specific_directories", []) or []:
        name = entry.get("path", "") if isinstance(entry, dict) else str(entry)
        name = name.strip().strip("/").split("/")[0]
        if name:
            known_top.add(name)
    for migration in profile.get("path_migrations", []) or []:
        source = str(migration.get("from", "")).strip("/")
        if source and "/" not in source:
            moved_top[source] = str(migration.get("to", ""))


def is_top_level_candidate(token, rest):
    # Нужен хотя бы второй сегмент: `a/b/`, `a/b/c` или `a/b.ext`.
    inner = rest.rstrip("/")
    if not inner:
        return False
    return token.endswith("/") or "/" in inner or bool(re.search(r"\.[A-Za-z0-9]{1,8}$", inner))


violations = []
section = None
section_level = 0
in_fence = False
for number, raw in enumerate(lines, start=1):
    stripped = raw.strip()
    if stripped.startswith("```") or stripped.startswith("~~~"):
        in_fence = not in_fence
    heading = None if in_fence else re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", raw)
    if heading:
        level, title = len(heading.group(1)), heading.group(2).strip()
        if any(key in title.lower() for key in CHECKED):
            section, section_level = title, level
            continue
        if section is not None and level <= section_level:
            section = None
        continue
    if section is None:
        continue
    text = URL.sub(" ", raw)
    if NEGATION.search(text):
        continue
    where = f"line {number} («{section}»)"
    for match in CONTRACTS.finditer(text):
        violations.append(
            f"{where}: path {match.group(0).rstrip('/')}/ is forbidden by AGENTS.md <forbidden> — "
            "контракт живёт в доме своего класса (AGENTS.md, <artifact_homes>): контракт агента — "
            "ai-rules/, контракт процесса — ops/<name>.md; "
            "см. standards/contract-documentation-standard.md#где-живёт-контракт"
        )
    if AI_GENERATED.search(text):
        violations.append(
            f"{where}: frontmatter field ai-generated is forbidden by AGENTS.md <forbidden> — "
            "назовите участников полем contributors и модель полем ai-models (ADR-023)"
        )
    for span in CODE_SPAN.findall(text):
        token = span.strip()
        if token.startswith(("../", "#", "@", "~")):
            continue
        match = PATH_TOKEN.match(token)
        if not match:
            continue
        top, rest = match.group(1), match.group(2)
        if top in (".", "..") or not is_top_level_candidate(token, rest):
            continue
        if top in moved_top:
            violations.append(
                f"{where}: path {token} uses top-level directory {top}/ moved by .hub-profile.json "
                f"path_migrations to {moved_top[top]} — обновите путь в постановке"
            )
        elif top not in known_top:
            violations.append(
                f"{where}: path {token} creates top-level directory {top}/ that is neither in the "
                "repository root nor in .hub-profile.json project_specific_directories — "
                "положите артефакт в дом из AGENTS.md <artifact_homes> или приложите запись о решении (ADR)"
            )

if violations:
    for item in violations:
        print(f"issue-statement: FAIL {item}")
    print(f"issue-statement: {len(violations)} violation(s); escalate per AGENTS.md <escalation> if the path is intended")
    sys.exit(1)
print("issue-statement: OK")
PY
