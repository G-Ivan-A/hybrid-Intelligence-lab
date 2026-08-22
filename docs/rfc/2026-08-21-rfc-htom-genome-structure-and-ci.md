---
status: draft
version: 0.1
updated: 2026-08-21
temperature: 0.1
owner: G-Ivan-A
rfc-scope: A
type: rfc
context: [genome, htom, templates, validators, ci, structure, governance, adr-007, b-056, issue-531]
method: audit-delegation + executable-draft + scenario-matrix
scope: repo
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/531"
related_artifacts:
  - "docs/audit/2026-08-21-hub-structural-normative-contradictions-audit.md"
  - "templates/htom/tools/validate-repository-structure.sh"
  - "templates/sync-metadata.json"
  - "templates/manifest.json"
  - "templates/spoke/.github/workflows/ci.yml"
  - "docs/adr/2026-07-adr-007-hub-root-structure.md"
  - "standards/rfc-structure-standard.md"
  - "standards/glossary.md"
  - "research/hub/exp/htom-genome-rfc-531/README.md"
  - "pr-ops/artifact-map.md"
  - "pr-ops/backlog.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/531"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/529"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/292"
---

# RFC: Геном HTOM — размещение управляющих контрактов и CI-валидация

## RFC Metadata

| Field | Value |
| --- | --- |
| Owner | G-Ivan-A |
| RFC status | draft — предложение, решение за фаундером |
| Source issue | [#531](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/531) |
| Impacted artifacts | При принятии: `templates/htom/tools/validate-repository-structure.sh`, новый `templates/htom/.github/workflows/validate.yml`, `templates/sync-metadata.json`, `templates/manifest.json`, `templates/htom/README.md`, `templates/htom/CHANGELOG.md`, `pr-ops/backlog.md`. **В рамках этого PR не изменяется ничего из перечисленного**; готовые к применению правки лежат черновиком в [`research/hub/exp/htom-genome-rfc-531/`](../../research/hub/exp/htom-genome-rfc-531/README.md). |
| Decision record | not yet |
| Implementation link | not yet |
| Archetype scope | A |

## Summary

Геном `templates/htom/` требует от каждой HTOM-команды держать `AI_GOVERNANCE.md`
**в корне** и называет это «жёстким ограничением Хаба», тогда как сам Хаб —
HTOM-команда по [глоссарию](../../standards/glossary.md) — вынес этот материал в
`ai-governance/` и `ai-rules/`. RFC предлагает заменить требование к **месту**
требованием к **наличию**: валидатор генома проверяет, что управляющий контракт
существует в одном из разрешённых домов (корень, `governance/`, либо
`ai-governance/` + `ai-rules/`), и отдельно запрещает держать его в двух домах
сразу. Параллельно в геном добавляется `.github/workflows/validate.yml`, который
запускает валидатор структуры на каждый `pull_request`, а сам валидатор
поднимается в Smart Sync с `RECOMMENDED` до `CORE`. Черновик правок исполним и
проверен на семи сценариях: изменение не ломает ни одну существующую спицу.

## Motivation

Проблема зафиксирована аудитом
[2026-08-21 «Структурные, нормативные и терминологические противоречия Хаба»](../audit/2026-08-21-hub-structural-normative-contradictions-audit.md)
как две Critical-находки. Доказательная база — там; здесь только то, что
требует решения.

**G-01 — геном противоречит Хабу.** `templates/htom/tools/validate-repository-structure.sh`
дважды требует корневой `AI_GOVERNANCE.md` (в списке `required_files` и
отдельной строкой с комментарием про «жёсткое ограничение Хаба»). После B-056 и
[ADR-007](../adr/2026-07-adr-007-hub-root-structure.md) в корне Хаба этого файла
нет — более того, собственный валидатор Хаба содержит `reject_file "AI_GOVERNANCE.md"`
и `reject_path "governance"`. Геном и Хаб предъявляют одному и тому же классу
репозиториев несовместимые требования.

**Почему это не теоретическая проблема.** В
[mango_ba_prompts PR #292](https://github.com/G-Ivan-A/mango_ba_prompts/pull/292)
постановка требовала вынести управляющие файлы из корня, а геном Хаба —
оставить их в корне. Исполнитель остановился, оставил файлы на месте и вынес
вопрос владельцу. Пока противоречие живо, этот отказ воспроизводится в каждой
новой HTOM-команде, и цена растёт линейно по числу спиц.

**G-02 — противоречие невидимо для машины.** Геном не содержит
`.github/workflows/`, а его валидатор помечен в Smart Sync как `RECOMMENDED`.
В клонированной HTOM-команде «иммунная система» не запускается никогда: в
mango она вообще не была перенесена при bootstrap, и структурный дрейф прожил
четыре PR незамеченным. Для сравнения, у спицы CI есть
([`templates/spoke/.github/workflows/ci.yml`](../../templates/spoke/.github/workflows/ci.yml))
и он помечен `CORE`. Асимметрия не обоснована ничем, кроме истории.

G-01 и G-02 решаются одним пакетом: без G-02 исправленное правило G-01 всё равно
проверялось бы только вручную, а без G-01 автоматический запуск валидатора начал
бы массово ронять CI у спиц, которые следуют актуальной архитектуре Хаба.

## Goals and Non-goals

**Цели.**

1. Снять с генома требование конкретного **места** для управляющих контрактов и
   заменить его требованием **наличия** в закрытом перечне допустимых мест.
2. Устранить дублирующую проверку `require_file "AI_GOVERNANCE.md"`.
3. Сделать валидацию структуры HTOM-команды автоматической: CI-воркфлоу в
   геноме плюс повышение criticality валидатора до `CORE`.
4. Явно описать impact на существующие спицы и дать план миграции.

**Не цели.**

1. RFC **не вводит новый стандарт**: правила остаются внутри генома и его
   метаданных (Anti-Inflation, контракт 5 постановки).
2. RFC не предписывает спицам переезжать на раскладку Хаба. Он делает переезд
   *разрешённым*, а не *обязательным*.
3. RFC не меняет содержание управляющих документов — только правило их
   размещения и запуск проверки.
4. RFC не трогает `templates/spoke/`: у спицы своя CI-модель и свой архетип.
5. RFC не решает остальные десять находок аудита (G-03…G-12) — они относятся к
   другим задачам.

## Proposal

### P.1. Инвариант: нормируется наличие контракта, а не его размещение

Геном перестаёт быть источником структурного требования «файл лежит в корне» и
становится источником требования «управляющий контракт существует и у него ровно
один дом». Обоснование: цель проверки — гарантировать агенту, что у команды есть
конституция, быстрые правила и handover-промпт. Физический путь к ним —
следствие архитектуры конкретной команды, и он уже разошёлся у Хаба и у спиц.
Правило, которому не следует его собственный автор, — не правило, а долг.

### P.2. Закрытый перечень допустимых домов

| Контракт | Допустимые размещения (в порядке разрешения) |
| --- | --- |
| Конституция команды | `AI_GOVERNANCE.md`, `governance/AI_GOVERNANCE.md`, `ai-governance/ai-governance.md` |
| Быстрые правила | `AI_QUICK_RULES.md`, `governance/AI_QUICK_RULES.md`, `ai-rules/ai-quick-rules.md` |
| Handover-промпт | `AI_SESSION_HANDOVER_PROMPT.md`, `governance/AI_SESSION_HANDOVER_PROMPT.md`, `ai-rules/AI_SESSION_HANDOVER_PROMPT.md` |

Перечень закрытый: произвольный каталог не легализуется, иначе проверка теряет
смысл. Рекомендуемая целевая раскладка для новых HTOM-команд — раскладка самого
Хаба (`ai-governance/` + `ai-rules/`), поскольку Хаб является эталоном SSOT.
Вариант `governance/` включён как допустимый переходный дом: именно он
рассматривался в mango PR #292, и запрет на него означал бы новый отказ вместо
снятого. Корневая раскладка остаётся допустимой бессрочно — это текущее
состояние всех спиц.

**Отклонение от формулировки постановки.** Постановка называет целевые пути
«`governance/` или `ai-rules/`». Фактическая раскладка Хаба — `ai-governance/`
и `ai-rules/`; корневой `governance/` у Хаба явно отвергается его собственным
валидатором (`reject_path "governance"`). НФТ постановки требует строгого
соответствия фактической структуре Хаба, поэтому перечень содержит оба имени, а
`ai-governance/` указан как рекомендуемое.

### P.3. Два дома — это отказ

Если один и тот же контракт найден более чем в одном допустимом месте,
валидатор падает. Иначе «разрешить несколько мест» превращается в «разрешить
несколько SSOT», и первая же правка разведёт копии. Это правило — плата за
гибкость P.2 и вводится вместе с ней, а не после.

### P.4. CI-воркфлоу в геноме

В геном добавляется `templates/htom/.github/workflows/validate.yml`: `checkout`,
`bash -n tools/*.sh`, `./tools/validate-repository-structure.sh` на `push` в
`main` и на каждый `pull_request`. Воркфлоу намеренно минимален и не содержит
шагов линта и тестов продукта: геном не знает стека HTOM-команды, а шаблон CI
для продуктовой части — зона `templates/spoke/`.

Соответственно, `.github/workflows` и `.github/workflows/validate.yml`
добавляются в списки обязательных каталогов и файлов самого валидатора: геном,
который декларирует иммунную систему, обязан её содержать.

### P.5. Smart Sync: валидатор становится CORE

В `templates/sync-metadata.json` criticality `templates/htom/tools/validate-repository-structure.sh`
поднимается `RECOMMENDED` → `CORE`, и добавляется запись для нового воркфлоу
(`target_type: ["HTOM"]`, `criticality: CORE`). `templates/manifest.json`
регенерируется `python3 tools/generate-manifest.py` — руками он не правится
(issue #207). Без этого шага G-02 закрыт лишь наполовину: файл в геноме есть, но
Smart Sync не обязан доставлять его в спицу.

### P.6. Черновик исполним, а не описателен

Готовые к применению правки лежат в
[`research/hub/exp/htom-genome-rfc-531/`](../../research/hub/exp/htom-genome-rfc-531/README.md)
вместе с гарнитурой из семи сценариев и логом прогона. Черновик размещён в
evidence-контейнере, а не в `templates/htom/`, потому что до human decision gate
геном не меняется — но предложение должно быть проверяемым.

## Alternatives

| # | Альтернатива | Почему отклонена |
| --- | --- | --- |
| A1 | Оставить как есть: `AI_GOVERNANCE.md` обязателен в корне | Хаб — HTOM-команда и уже нарушает это правило. Сохранение означает, что либо Хаб должен откатить B-056 и ADR-007, либо геном официально лжёт. Отказ mango PR #292 будет повторяться. |
| A2 | Сделать раскладку Хаба (`ai-governance/` + `ai-rules/`) единственно допустимой | Настоящий breaking change: все существующие спицы падают в CI в момент включения P.4 и обязаны мигрировать по расписанию Хаба, а не по своему. Выигрыш — только единообразие, которого никто сейчас не требует. |
| A3 | Убрать проверку управляющих контрактов из генома совсем | Снимает противоречие ценой самой иммунной системы: команда без конституции перестаёт быть наблюдаемой. Аудит показал, что дрейф выживает ровно там, где нет проверки. |
| A4 | Понизить проверку до `warn` | Warning в CI, который всегда зелёный, не меняет поведения. Это отсрочка решения, а не решение; ровно так G-02 и возник. |
| A5 | Разрешить любой каталог, лишь бы файл существовал где-то в дереве | Проверка перестаёт быть структурной: `grep -r` найдёт контракт в архиве или в примере. Закрытый перечень P.2 сохраняет смысл проверки. |

## Trade-offs

**Цена гибкости.** Три допустимых дома вместо одного — это три пути в сообщении
об ошибке и обязательное правило P.3 против двойного SSOT. Инварианта «один
известный путь» больше нет; вместо него — «один известный перечень».

**Цена автоматизации.** После P.4 и P.5 валидатор начнёт падать там, где раньше
молчал. Это и есть цель, но первая волна миграции спиц даст красный CI на
репозиториях, где структура дрейфовала. Смягчение — план миграции ниже:
изменение генома не ретроактивно, оно применяется к спице в момент её
собственной синхронизации.

**Риск ложной легализации.** Разрешив `governance/`, Хаб фиксирует как
допустимое имя, которое сам отверг. Это осознанный переходный компромисс, и он
вынесен в открытый вопрос Q-2.

**Совместимость.** Сценарии A (корневая раскладка) и C (раскладка Хаба) в
[прогоне черновика](../../research/hub/exp/htom-genome-rfc-531/README.md)
проходят одновременно. Для существующих спиц предложение **не является breaking
change** по правилу размещения; breaking-эффект возможен только через требование
наличия CI-воркфлоу (сценарий F) — см. план миграции.

## Impacted Artifacts

| Артефакт | Изменение при принятии | Затронут в этом PR |
| --- | --- | --- |
| `templates/htom/tools/validate-repository-structure.sh` | P.1–P.4: `resolve_one_of`, перечень домов, запрет двух домов, обязательный CI-файл; удалён дубль `require_file "AI_GOVERNANCE.md"` | нет (черновик) |
| `templates/htom/.github/workflows/validate.yml` | Новый файл (P.4) | нет (черновик) |
| `templates/sync-metadata.json` | criticality валидатора → `CORE`, запись для воркфлоу | нет |
| `templates/manifest.json` | Регенерация `tools/generate-manifest.py` | нет |
| `templates/htom/README.md`, `templates/htom/CHANGELOG.md` | Описание раскладки и CI | нет |
| Существующие спицы (`mango_ba_prompts` и др.) | Разблокирован перенос управляющих файлов; появляется обязательство завести CI-воркфлоу | нет |
| `pr-ops/backlog.md`, `pr-ops/artifact-map.md`, `docs/rfc/README.md`, `CHANGELOG.md` | Регистрация этого RFC | **да** |
| `research/hub/exp/htom-genome-rfc-531/` | Исполнимый черновик и лог прогона | **да** |

**Impact на существующие спицы — по шагам.**

1. **Правило размещения.** Спица, держащая управляющие файлы в корне, проходит
   валидацию без единой правки (сценарий A). Спица, уже переехавшая в
   `governance/` или в раскладку Хаба, начинает проходить валидацию, которую
   сейчас не проходит (сценарии B и C). Здесь breaking change отсутствует.
2. **Требование CI-воркфлоу.** Спица без `.github/workflows/validate.yml`
   получит `FAIL` (сценарий F). Это единственный breaking-элемент предложения.
3. **Момент срабатывания.** Геном не выполняется в спицах сам по себе: правило
   доезжает до спицы только при Smart Sync или при ручном прогоне валидатора.
   Ретроактивного слома «в момент merge этого RFC» не происходит ни в одной
   спице.

**План миграции (безопасный порядок).**

| Шаг | Действие | Кто | Условие перехода к следующему |
| --- | --- | --- | --- |
| M0 | Решение фаундера по этому RFC | человек | RFC переведён в `accepted` |
| M1 | Применить черновик к геному, добавить воркфлоу, обновить `sync-metadata.json`, регенерировать манифест | Хаб | Валидаторы Хаба зелёные |
| M2 | Разблокировать mango PR #292: перенос управляющих файлов становится легальным | спица | PR #292 закрыт |
| M3 | Синхронизировать спицы поштучно; в том же PR, что приносит валидатор, приносить и воркфлоу | спица | CI спицы зелёный |
| M4 | Через один цикл синхронизации — ревизия: остались ли спицы вне перечня P.2 | Хаб | — |

Ключ безопасности плана — **M3**: валидатор и воркфлоу доставляются одним PR,
поэтому спица никогда не оказывается в состоянии «проверка включена, а файла,
которого она требует, ещё нет».

## Implementation and Validation

### Черновик правки валидатора генома

```diff
--- a/templates/htom/tools/validate-repository-structure.sh
+++ b/templates/htom/tools/validate-repository-structure.sh
@@ -32,17 +32,30 @@
   [[ -f "$1" ]] || fail "missing file: $1"
 }
 
+# Печатает первый существующий путь из списка кандидатов, иначе возвращает 1.
+# Нормируется наличие контракта, а не его физическое размещение: HTOM-команда
+# вправе держать управляющие документы в корне или вынести их в governance-каталог
+# (как это сделал сам Хаб по ADR-007 / B-056).
+resolve_one_of() {
+  local candidate
+  for candidate in "$@"; do
+    if [[ -f "$candidate" ]]; then
+      printf '%s\n' "$candidate"
+      return 0
+    fi
+  done
+  return 1
+}
+
 required_directories=(
   "docs/adr"
   "docs/audit"
   ".github/ISSUE_TEMPLATE"
+  ".github/workflows"
   "tools"
 )
 
 required_files=(
-  "AI_GOVERNANCE.md"
-  "AI_QUICK_RULES.md"
-  "AI_SESSION_HANDOVER_PROMPT.md"
   "README.md"
   "CONTRIBUTING.md"
   "CHANGELOG.md"
@@ -50,6 +63,7 @@
   "docs/audit/.gitkeep"
   ".github/ISSUE_TEMPLATE/task.md"
   ".github/ISSUE_TEMPLATE/task-creative.md"
+  ".github/workflows/validate.yml"
   "tools/validate-repository-structure.sh"
 )
 
@@ -61,15 +75,51 @@
   require_file "$file"
 done
 
-# AI_GOVERNANCE.md обязателен в корне каждой HTOM-команды (жёсткое ограничение Хаба).
-require_file "AI_GOVERNANCE.md"
+# Управляющие контракты HTOM-команды: обязательно наличие, размещение — на выбор
+# команды. Порядок кандидатов задаёт приоритет разрешения при нескольких копиях.
+# shellcheck disable=SC2034  # путь резолвится для сообщения об ошибке, не используется дальше
+governance_contract="$(resolve_one_of \
+  "AI_GOVERNANCE.md" \
+  "governance/AI_GOVERNANCE.md" \
+  "ai-governance/ai-governance.md")" ||
+  fail "missing governance contract: ожидался один из AI_GOVERNANCE.md, governance/AI_GOVERNANCE.md, ai-governance/ai-governance.md"
+
+quick_rules="$(resolve_one_of \
+  "AI_QUICK_RULES.md" \
+  "governance/AI_QUICK_RULES.md" \
+  "ai-rules/ai-quick-rules.md")" ||
+  fail "missing quick rules: ожидался один из AI_QUICK_RULES.md, governance/AI_QUICK_RULES.md, ai-rules/ai-quick-rules.md"
+
+handover_prompt="$(resolve_one_of \
+  "AI_SESSION_HANDOVER_PROMPT.md" \
+  "governance/AI_SESSION_HANDOVER_PROMPT.md" \
+  "ai-rules/AI_SESSION_HANDOVER_PROMPT.md")" ||
+  fail "missing handover prompt: ожидался один из AI_SESSION_HANDOVER_PROMPT.md, governance/AI_SESSION_HANDOVER_PROMPT.md, ai-rules/AI_SESSION_HANDOVER_PROMPT.md"
 
 # Handover Prompt должен оставаться параметризованным ({{REPO_NAME}}), чтобы
 # «доверенность» переносилась в любую HTOM-команду без правок (см. AI_SESSION_HANDOVER_PROMPT.md).
-if [[ -f "AI_SESSION_HANDOVER_PROMPT.md" ]] && ! grep -Fq '{{REPO_NAME}}' "AI_SESSION_HANDOVER_PROMPT.md"; then
-  fail "AI_SESSION_HANDOVER_PROMPT.md must keep the {{REPO_NAME}} placeholder"
+if [[ -n "${handover_prompt:-}" ]] && ! grep -Fq '{{REPO_NAME}}' "$handover_prompt"; then
+  fail "$handover_prompt must keep the {{REPO_NAME}} placeholder"
 fi
 
+# Управляющие контракты не должны существовать в двух местах одновременно:
+# два дома означают два SSOT и расхождение при первой же правке.
+for pair in \
+  "AI_GOVERNANCE.md:governance/AI_GOVERNANCE.md:ai-governance/ai-governance.md" \
+  "AI_QUICK_RULES.md:governance/AI_QUICK_RULES.md:ai-rules/ai-quick-rules.md" \
+  "AI_SESSION_HANDOVER_PROMPT.md:governance/AI_SESSION_HANDOVER_PROMPT.md:ai-rules/AI_SESSION_HANDOVER_PROMPT.md"; do
+  IFS=':' read -r -a candidates <<<"$pair"
+  found=()
+  for candidate in "${candidates[@]}"; do
+    if [[ -f "$candidate" ]]; then
+      found+=("$candidate")
+    fi
+  done
+  if [[ "${#found[@]}" -gt 1 ]]; then
+    fail "duplicate governance contract: ${found[*]} — оставьте ровно одно размещение"
+  fi
+done
+
 # Negative check: research/ по умолчанию не создаётся в HTOM-команде.
 # Фундаментальные знания живут в research/ Хаба. Если папка появилась — это
 # должно быть осознанным решением, зафиксированным как ADR (см. AI_QUICK_RULES.md).
```

### Черновик нового CI-воркфлоу генома

Полный файл — `research/hub/exp/htom-genome-rfc-531/htom-validate-workflow-draft.yml`:

```yaml
name: validate

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  structure:
    name: Repository structure
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Validate shell syntax
        run: bash -n tools/*.sh

      - name: Validate repository structure
        run: ./tools/validate-repository-structure.sh
```

### Черновик правки Smart Sync

В `templates/sync-metadata.json`:

```json
"templates/htom/tools/validate-repository-structure.sh": {
  "id": "htom-validate-repository-structure",
  "version": "1.1.0",
  "target_type": ["HTOM"],
  "criticality": "CORE",
  "tags": ["validation", "tooling"],
  "description": "Валидатор структуры HTOM-репозитория."
},
"templates/htom/.github/workflows/validate.yml": {
  "id": "htom-validate-workflow",
  "version": "1.0.0",
  "target_type": ["HTOM"],
  "criticality": "CORE",
  "tags": ["ci", "validation"],
  "description": "CI-воркфлоу HTOM-команды: запуск валидатора структуры на pull_request."
}
```

После правки — `python3 tools/generate-manifest.py --write` и `python3 tools/generate-manifest.py --check`
(`templates/manifest.json` правится только генератором, issue #207).

### Как доказана работоспособность черновика

Гарнитура [`research/hub/exp/htom-genome-rfc-531/validate-draft.sh`](../../research/hub/exp/htom-genome-rfc-531/README.md)
собирает во временном каталоге семь синтетических HTOM-команд из текущего генома
и сверяет фактический exit code с ожидаемым. Прогон 2026-08-21:

```text
Draft validation passed: 7/7 сценариев совпали с ожиданием.
```

| Сценарий | Ожидание | Что доказывает |
| --- | --- | --- |
| A. Корневая раскладка | pass | Существующие спицы не ломаются |
| B. `governance/` | pass | Разблокирован mango PR #292 |
| C. `ai-governance/` + `ai-rules/` | pass | Раскладка Хаба легальна, G-01 закрыт |
| D. Контракта нет нигде | fail | Проверка не выродилась в no-op |
| E. Контракт в двух домах | fail | P.3 работает |
| F. Нет CI-воркфлоу | fail | G-02 стал машинно наблюдаемым |
| G. Handover без `{{REPO_NAME}}` | fail | Параметризация проверяется по новому пути |

### Локальные проверки Хаба для этого PR

```bash
./tools/validate-frontmatter.sh .
./tools/validate-file-naming.sh
./tools/validate-evidence-structure.sh
./tools/validate-repository-structure.sh
./research/hub/exp/htom-genome-rfc-531/validate-draft.sh
```

## Lifecycle and Decision Path

**Текущее состояние.** `draft`. Геном не изменён; изменения этого PR
ограничены самим RFC, его evidence-контейнером и регистрацией в реестрах.

**Требуемый human gate.** Фаундер принимает или отклоняет P.1–P.5 и отвечает на
Q-1 и Q-2. Аудит прямо классифицировал G-01 как выбор архитектуры, а не как
микро-правку, поэтому автоматическое применение исключено.

**После принятия.** Шаги M1–M4 плана миграции выполняются отдельной задачей
бэклога. Decision record: при принятии без изменений сам accepted RFC является
решением (`standards/rfc-structure-standard.md`, boundary RFC/ADR); если фаундер
выберет A2 или сузит перечень P.2, потребуется ADR, поскольку это меняет
структурное решение ADR-007 для класса HTOM-команд.

**Метаданные.** Поля `Decision record` и `Implementation link` содержат
`not yet` и должны быть заменены конкретными ссылками первым же PR, который
тронет этот RFC после появления решения и реализации.

## Open Questions

- **Q-1 (блокирующий).** Принимается ли инвариант P.1 «нормируется наличие, а не
  размещение», или геном должен остаться источником единственной обязательной
  раскладки? Ответ определяет выбор между этим предложением и альтернативами A1/A2.
- **Q-2 (блокирующий).** Остаётся ли `governance/` в закрытом перечне P.2 как
  переходный дом, при том что Хаб отверг это имя у себя (`reject_path "governance"`)?
  Исключение варианта делает mango PR #292 снова заблокированным до переезда на
  раскладку Хаба.
- **Q-3 (неблокирующий).** Нужен ли для спиц льготный период по требованию
  CI-воркфлоу (сначала `warn`, через один цикл синхронизации — `fail`), или шаг
  M3 «валидатор и воркфлоу одним PR» уже закрывает риск?

## Related Artifacts

- Issue: <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/531>
- Источник находок: [docs/audit/2026-08-21-hub-structural-normative-contradictions-audit.md](../audit/2026-08-21-hub-structural-normative-contradictions-audit.md) (G-01, G-02), issue [#529](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/529)
- Триггер-инцидент: [mango_ba_prompts PR #292](https://github.com/G-Ivan-A/mango_ba_prompts/pull/292)
- Структурное решение Хаба: [ADR-007](../adr/2026-07-adr-007-hub-root-structure.md)
- Норма оформления: [standards/rfc-structure-standard.md](../../standards/rfc-structure-standard.md)
- Определение HTOM-команды: [standards/glossary.md](../../standards/glossary.md)
- Геном: [templates/htom/README.md](../../templates/htom/README.md), [templates/htom/tools/validate-repository-structure.sh](../../templates/htom/tools/validate-repository-structure.sh)
- Исполнимый черновик: [research/hub/exp/htom-genome-rfc-531/README.md](../../research/hub/exp/htom-genome-rfc-531/README.md)
- Реестры: [pr-ops/artifact-map.md](../../pr-ops/artifact-map.md), [pr-ops/backlog.md](../../pr-ops/backlog.md)
