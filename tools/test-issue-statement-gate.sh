#!/usr/bin/env bash
# Регрессионный тест гейта постановки tools/validate-issue-statement.sh
# (B-116 (d), issue #727). Фикстуры тела issue встроены в тест: путь,
# запрещённый в «Готово, когда» или «Задаче исполнителю», краснит гейт, а тот же
# путь в «Контексте» или в строке-запрете — нет. Сеть и `gh` не нужны.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GATE="$ROOT_DIR/tools/validate-issue-statement.sh"

work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT

# Изолированный корень: ядро, один проектный каталог и одна миграция пути.
fake_root="$work_dir/root"
mkdir -p "$fake_root/ai-rules" "$fake_root/ops" "$fake_root/docs" "$fake_root/tools" \
  "$fake_root/standards" "$fake_root/.github"
cat >"$fake_root/.hub-profile.json" <<'JSON'
{
  "project_specific_directories": [{"path": "lab/", "decision": "docs/adr/2026-11-adr-999-lab.md"}],
  "path_migrations": [{"from": "legacy-ops/", "to": "ops/", "issue": "#567"}]
}
JSON

failures=0
passed=0

run_gate() {
  local fixture="$1"
  set +e
  ISSUE_STATEMENT_ROOT="$fake_root" bash "$GATE" "$fixture" >"$work_dir/out.log" 2>&1
  local code=$?
  set -e
  printf '%s' "$code"
}

expect() {
  local name="$1" want="$2" fixture="$3" needle="${4:-}"
  local code
  code="$(run_gate "$fixture")"
  if [[ "$code" != "$want" ]]; then
    printf 'FAIL %s: exit %s, expected %s\n' "$name" "$code" "$want"
    sed 's/^/  | /' "$work_dir/out.log"
    failures=$((failures + 1))
    return 0
  fi
  if [[ -n "$needle" ]] && ! grep -Fq -- "$needle" "$work_dir/out.log"; then
    printf 'FAIL %s: output lacks %s\n' "$name" "$needle"
    sed 's/^/  | /' "$work_dir/out.log"
    failures=$((failures + 1))
    return 0
  fi
  printf 'PASS %s\n' "$name"
  passed=$((passed + 1))
}

fixture() {
  local name="$1"
  cat >"$work_dir/$name.md"
  printf '%s' "$work_dir/$name.md"
}

# 1. Нулевой пациент F7: путь docs/contracts/ предписан в «Готово, когда».
f="$(fixture dod-contracts <<'MD'
### 1. Контекст
Нужен контракт цитирования.

### 5. Готово, когда
- [ ] Контрмеры включены в `docs/contracts/kb-citations.md`.
MD
)"
expect "docs/contracts/ in «Готово, когда» is red" 1 "$f" "ai-rules/, контракт процесса — ops/<name>.md"

# 2. Тот же путь в «Контексте» описывает факт и гейт не краснит.
f="$(fixture context-contracts <<'MD'
### 1. Контекст
В спице уже есть `docs/contracts/kb-citations.md` (см. F2).

### 5. Готово, когда
- [ ] Правило перенесено в `ai-rules/kb-citations.md`.
MD
)"
expect "docs/contracts/ in «Контекст» passes" 0 "$f" "issue-statement: OK"

# 3. Вложенный docs/contracts в «Задаче исполнителю» без обратных кавычек.
f="$(fixture task-nested-contracts <<'MD'
## Уровень 4. Задача исполнителю
Создать projects/demo/docs/contracts/api.md с описанием API.
MD
)"
expect "nested docs/contracts in «Задача исполнителю» is red" 1 "$f" "projects/demo/docs/contracts/"

# 4. Строка-запрет в «Готово, когда» не предписывает путь.
f="$(fixture dod-negation <<'MD'
## ✅ Готово, когда
- [ ] Каталог `docs/contracts/` не создан; контракт лежит в `ops/citations.md`.
MD
)"
expect "negated docs/contracts/ in «Готово, когда» passes" 0 "$f"

# 5. Новый каталог верхнего уровня без записи о решении.
f="$(fixture dod-new-top <<'MD'
### 5. Готово, когда
- [ ] Скрипт лежит в `scripts/validate_shift.py`.
MD
)"
expect "undeclared top-level scripts/ is red" 1 "$f" "creates top-level directory scripts/"

# 6. Объявленный каталог (ядро и project_specific_directories) проходит,
#    одиночный `exp/` и `owner/repo` путями от корня не считаются.
f="$(fixture dod-known-top <<'MD'
### 5. Готово, когда
- [ ] Обновлены `tools/validate-x.sh`, `.github/workflows/ci.yml` и `lab/notes/plan.md`.
- [ ] Логи лежат в `exp/` проекта; PR открыт в `G-Ivan-A/hybrid-Intelligence-lab`.
MD
)"
expect "declared top-level directories pass" 0 "$f"

# 7. Перенесённый каталог получает подсказку с новым путём.
f="$(fixture dod-moved <<'MD'
### 5. Готово, когда
- [ ] Строка добавлена в `legacy-ops/backlog.md`.
MD
)"
expect "moved top-level legacy-ops/ is red with hint" 1 "$f" "path_migrations to ops/"

# 8. Предписание поля frontmatter ai-generated.
f="$(fixture dod-ai-generated <<'MD'
### 5. Готово, когда
- [ ] Во frontmatter отчёта стоит `ai-generated: true`.
MD
)"
expect "ai-generated frontmatter in «Готово, когда» is red" 1 "$f" "contributors"

# 9. Секция кончается на заголовке того же уровня; URL вырезаются.
f="$(fixture section-end <<'MD'
### 5. Готово, когда
- [ ] Ссылка https://github.com/o/r/tree/main/docs/contracts/x.md прочитана.

### Отклонения от постановки
Раньше был путь `docs/contracts/x.md`.
MD
)"
expect "URL and next section are not checked" 0 "$f"

# 10. Заголовок внутри блока кода не открывает проверяемую секцию.
f="$(fixture fenced-heading <<'MD'
### 1. Контекст
```markdown
### 5. Готово, когда
- [ ] `docs/contracts/x.md`
```
MD
)"
expect "heading inside code fence is ignored" 0 "$f"

# 11. Ошибки вызова: нет файла и нет аргументов.
code="$(run_gate "$work_dir/missing.md")"
if [[ "$code" == "2" ]]; then printf 'PASS missing file exits 2\n'; passed=$((passed + 1)); else printf 'FAIL missing file exit %s\n' "$code"; failures=$((failures + 1)); fi
set +e
bash "$GATE" >/dev/null 2>&1
code=$?
set -e
if [[ "$code" == "2" ]]; then printf 'PASS no arguments exits 2\n'; passed=$((passed + 1)); else printf 'FAIL no arguments exit %s\n' "$code"; failures=$((failures + 1)); fi

# 12. Тело из stdin.
set +e
printf '### 5. Готово, когда\n- [ ] `docs/contracts/a.md`\n' | ISSUE_STATEMENT_ROOT="$fake_root" bash "$GATE" - >/dev/null 2>&1
code=$?
set -e
if [[ "$code" == "1" ]]; then printf 'PASS stdin body is checked\n'; passed=$((passed + 1)); else printf 'FAIL stdin body exit %s\n' "$code"; failures=$((failures + 1)); fi

# 13. Шаблоны постановки Хаба сами проходят гейт.
for template in "$ROOT_DIR/.github/ISSUE_TEMPLATE/task.md" "$ROOT_DIR/templates/htom/.github/ISSUE_TEMPLATE/task.md"; do
  expect "template ${template#"$ROOT_DIR"/} passes" 0 "$template"
done

printf 'Passed: %s, Failed: %s\n' "$passed" "$failures"
[[ "$failures" -eq 0 ]]
