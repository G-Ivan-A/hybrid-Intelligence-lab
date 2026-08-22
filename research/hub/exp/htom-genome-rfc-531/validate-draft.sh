#!/usr/bin/env bash
#
# Проверка черновика правок генома HTOM (issue #531, находки G-01 и G-02 аудита
# docs/audit/2026-08-21-hub-structural-normative-contradictions-audit.md).
#
# Скрипт ничего не меняет в репозитории: он собирает во временном каталоге тринадцать
# синтетических HTOM-команд из текущего генома `templates/htom/`, подкладывает в
# них черновой валидатор (`htom-validate-repository-structure-draft.sh`) и
# черновой CI-воркфлоу, после чего сверяет фактический exit code с ожидаемым.
#
# Смысл проверки: показать, что предложенное правило «нормируется наличие
# управляющего контракта, а не его размещение» одновременно (1) не ломает
# существующие спицы с корневой раскладкой, (2) легализует раскладку Хаба и
# раскладку mango PR #292, (3) сохраняет отказ там, где контракт реально
# отсутствует, задублирован или потерял плейсхолдер, и (4) делает отсутствие CI
# машинно наблюдаемым.
#
#   ./research/hub/exp/htom-genome-rfc-531/validate-draft.sh
#
set -euo pipefail

EXP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$EXP_DIR/../../../.." && pwd)"
GENOME="$ROOT_DIR/templates/htom"

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

failures=0

# Базовый случай: геном как есть + черновой валидатор + черновой воркфлоу.
make_baseline() {
  local dest="$WORK_DIR/$1"
  cp -r "$GENOME" "$dest"
  mkdir -p "$dest/.github/workflows"
  cp "$EXP_DIR/htom-validate-workflow-draft.yml" "$dest/.github/workflows/validate.yml"
  cp "$EXP_DIR/htom-validate-repository-structure-draft.sh" "$dest/tools/validate-repository-structure.sh"
  chmod +x "$dest/tools/validate-repository-structure.sh"
  printf '%s\n' "$dest"
}

clone_case() {
  local src="$WORK_DIR/$1"
  local dest="$WORK_DIR/$2"
  cp -r "$src" "$dest"
  printf '%s\n' "$dest"
}

check() {
  local name="$1"
  local dir="$2"
  local expected="$3"
  local actual=0

  printf '\n=== %s (ожидаем exit=%s) ===\n' "$name" "$expected"
  ( cd "$dir" && ./tools/validate-repository-structure.sh ) || actual=$?

  if [[ "$actual" == "$expected" ]]; then
    printf 'OK: exit=%s\n' "$actual"
  else
    printf 'MISMATCH: exit=%s, ожидался %s\n' "$actual" "$expected" >&2
    failures=$((failures + 1))
  fi
}

a="$(make_baseline a)"
check "A. Корневая раскладка (текущие спицы, как mango сейчас)" "$a" 0

b="$(clone_case a b)"
mkdir -p "$b/governance"
mv "$b/AI_GOVERNANCE.md" "$b/AI_QUICK_RULES.md" "$b/AI_SESSION_HANDOVER_PROMPT.md" "$b/governance/"
check "B. Раскладка governance/ (целевая в mango PR #292)" "$b" 0

c="$(clone_case a c)"
mkdir -p "$c/ai-governance" "$c/ai-rules"
mv "$c/AI_GOVERNANCE.md" "$c/ai-governance/ai-governance.md"
mv "$c/AI_QUICK_RULES.md" "$c/ai-rules/ai-quick-rules.md"
mv "$c/AI_SESSION_HANDOVER_PROMPT.md" "$c/ai-rules/"
check "C. Раскладка ai-governance/ + ai-rules/ (фактическая раскладка Хаба, B-056)" "$c" 0

d="$(clone_case a d)"
rm "$d/AI_GOVERNANCE.md"
check "D. Управляющий контракт отсутствует везде" "$d" 1

e="$(clone_case a e)"
mkdir -p "$e/governance"
cp "$e/AI_GOVERNANCE.md" "$e/governance/AI_GOVERNANCE.md"
check "E. Два дома у одного контракта (два SSOT)" "$e" 1

f="$(clone_case a f)"
rm -rf "$f/.github/workflows"
check "F. Геном без CI-воркфлоу (собственно G-02)" "$f" 1

g="$(clone_case c g)"
sed -i 's/{{REPO_NAME}}/mango_ba_prompts/g' "$g/ai-rules/AI_SESSION_HANDOVER_PROMPT.md"
check "G. Handover потерял {{REPO_NAME}} в новом доме" "$g" 1

# --- Классификация каталогов (RFC v0.2, issue #535) --------------------------
#
# Сценарии H–M проверяют баланс: специфичный для проекта каталог сохраняется по
# декларации, а недекларированный переходный каталог становится ошибкой.

write_profile() {
  local dest="$1"
  shift
  cat >"$dest/.hub-profile.json" <<PROFILE
{
  "project_name": "synthetic-htom-team",
  "target_type": "HTOM",
  "stack": "all",
  "phase": 1,
  "hub_url": "https://github.com/G-Ivan-A/hybrid-Intelligence-lab",
$*
  "last_sync": {}
}
PROFILE
}

h="$(clone_case a h)"
mkdir -p "$h/mango-research"
touch "$h/mango-research/.gitkeep"
check "H. Недекларированный каталог проекта (limbo state после реструктуризации)" "$h" 1

i="$(clone_case a i)"
mkdir -p "$i/mango-research"
touch "$i/mango-research/.gitkeep"
write_profile "$i" '  "project_specific_directories": [
    { "path": "mango-research", "reason": "Доменные исследования Mango: не входят в геном, но несут ценность проекта." }
  ],'
check "I. Тот же каталог задекларирован как специфичный" "$i" 0

j="$(clone_case a j)"
mkdir -p "$j/mango-research"
touch "$j/mango-research/.gitkeep"
write_profile "$j" '  "project_specific_directories": [
    { "path": "mango-research" }
  ],'
check "J. Декларация без причины (reason) — не принимается" "$j" 1

k="$(clone_case a k)"
mkdir -p "$k/mango-research"
touch "$k/mango-research/.gitkeep"
write_profile "$k" "  \"structure_grandfather_until\": \"$(date -u -d '+30 days' +%F 2>/dev/null || date -u -v+30d +%F)\","
check "K. Льготный период (grandfathering) активен — warn, а не fail" "$k" 0

l="$(clone_case a l)"
mkdir -p "$l/mango-research"
touch "$l/mango-research/.gitkeep"
write_profile "$l" "  \"structure_grandfather_until\": \"$(date -u -d '-1 day' +%F 2>/dev/null || date -u -v-1d +%F)\","
check "L. Льготный период истёк — недекларированный каталог падает" "$l" 1

m="$(clone_case a m)"
mkdir -p "$m/.archive/governance"
touch "$m/.archive/governance/.gitkeep"
check "M. .archive/ без README.md (архив не объясняет себя)" "$m" 1

n="$(clone_case a n)"
mkdir -p "$n/.archive/governance"
printf '# Archive\n\nПереходный каталог governance/ после реструктуризации.\n' >"$n/.archive/README.md"
check "N. .archive/ с README.md — легитимный архив переходного каталога" "$n" 0

printf '\n'
if (( failures > 0 )); then
  printf 'Draft validation failed: %d сценарий(ев) разошлись с ожиданием.\n' "$failures" >&2
  exit 1
fi

printf 'Draft validation passed: 13/13 сценариев совпали с ожиданием.\n'
