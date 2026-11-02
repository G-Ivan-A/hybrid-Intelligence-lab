---
status: draft
version: 0.1
updated: 2026-11-02
temperature: 0.1
analysis-subtype: recommendation
source: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/713
scope: project
based_on: "mango_ba_prompts@6cda9f5 (main, 2026-11-01); Hub main@782742b — AGENTS.md, .hub-profile.json, ops/repo-model.md, ops/backlog.md, standards/agents-md-bootstrap-standard.md, templates/htom/"
related_artifacts:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/tree/6cda9f5/pr-ops"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/6cda9f5/.hub-profile.json"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/6cda9f5/docs/rfc/2026-10-repository-modernization.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/blob/6cda9f5/pr-ops/backlog-instruction.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/rfc/2026-09-04-rfc-bootstrap-environment-and-structure.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/agents-md-bootstrap-standard.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/templates/htom/tools/validate-repository-structure.sh"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/analysis/2026-11-02-aether-orbis-gra-hub-practice-transfer-check.md"
---

# mango_ba_prompts: проверка передачи практик Хаба

## Summary / BLUF

**Проблема 1 подтверждена, но её корень не в «создании» `pr-ops/`, а в том, что
спица ни разу не синхронизировалась с Хабом после переименования
`pr-ops/` → `ops/`.** Хаб переименовал каталог 2026-09-09
([issue #567](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/567),
коммит `3a7306d`, запись `path_migrations` в
[`.hub-profile.json`](../../.hub-profile.json) Хаба). Последний синк
`mango_ba_prompts` — 2026-08-17 по снимку Хаба `3bfa410`, где каталог ещё назывался
`pr-ops/`. Модернизация #413/#418/#420 положила новые файлы бэклога
(`BACKLOG.md` v1.0, `backlog-instruction.md`, `backlog-repository.md`,
`backlog-ba-model.md`) в унаследованный `pr-ops/`, хотя сама ссылается на
`ops/backlog-instruction.md` Хаба, и не указала имя каталога в своей таблице
«Отличия от бэклога Хаба». **Отличие не обосновано спецификой проекта и не
согласовано владельцем; рекомендуется миграция `pr-ops/` → `ops/`.** Кроме того,
найдено ещё 7 нарушений консистентности чтения, из них критичное — нет корневого
`AGENTS.md` (обязателен для каждого репозитория экосистемы). Оправданные отличия
(`prompts/`, `runs/`, `kb/`, `patterns/`, локальные `standards/` и др.) приняты.

## Context / Scope

- **Дата:** 2026-11-02. **Режим:** Hybrid (задан в issue #713).
- **Что проверено:** `mango_ba_prompts` на `main@6cda9f5` против Хаба
  `main@782742b`: корень, `docs/`, `.hub-profile.json`, `ai-rules/`,
  `.github/ISSUE_TEMPLATE/`, валидатор структуры, RFC и бэклог модернизации.
- **Эталон.** Общая часть: [`AGENTS.md`](../../AGENTS.md) Хаба,
  [bootstrap-стандарт](../../standards/agents-md-bootstrap-standard.md), геном
  [`templates/htom/`](../../templates/htom/README.md) (`target_type: HTOM` у спицы),
  [модель репозитория](../../ops/repo-model.md).
- **Критерий допустимости отличия** (из постановки): отличие допустимо, если оно
  (а) обосновано спецификой проекта или (б) прямо согласовано/задано владельцем.
  Отличие без (а) или (б) — дефект консистентности.

### Нормализованная постановка (интерпретация исполнителя)

| Уровень | Содержание |
| --- | --- |
| Цель | Проекты экосистемы читаются единообразно: человек или агент, знающий Хаб, находит в спице те же дома по тем же именам; отличия существуют только с обоснованием. |
| Задачи | 1) проверить `pr-ops/` vs `ops/`; 2) найти другие нарушения консистентности чтения; 3) для каждого отличия дать вердикт «обосновано / не обосновано» по критерию (а)/(б); 4) зафиксировать результат в аналитическом артефакте с именем проекта в имени файла. |
| Границы | Только анализ и рекомендации в Хабе. Правки в `mango_ba_prompts` не выполняются: это другой репозиторий, его изменение — отдельная задача в нём. |
| SSOT результата | Этот файл (`docs/analysis/` Хаба): предмет проверки — передача норм Хаба, эталон лежит в Хабе. Задачи на исправление — в бэклоге спицы. |
| Критерии приёмки | Каждая находка подкреплена путём/коммитом; у каждого отличия вердикт и рекомендация; воспроизводимая проверка указана. |

## Findings / Options

### Проблема 1: `pr-ops/` вместо `ops/` — подтверждена

| Факт | Доказательство |
| --- | --- |
| Хаб переименовал `pr-ops/` → `ops/` | RFC [2026-09-04, раздел о `pr-ops`](../rfc/2026-09-04-rfc-bootstrap-environment-and-structure.md): «имя `pr-ops` семантически неверно уже сегодня»; коммит `3a7306d refactor: migrate pr-ops to ops` (2026-09-09); `path_migrations` `pr-ops/` → `ops/` (#567) в профиле Хаба. |
| Спица синхронизирована до переименования | `.hub-profile.json` спицы: `last_sync.date = 2026-08-17`, `hub_sha = 3bfa4103…`; все ссылки синкнутых стандартов ведут на `…/3bfa410…/pr-ops/…`. |
| Новые файлы положены в `pr-ops/` | Коммит `8795880` (issue #418, 2026-10-31) добавил `pr-ops/backlog-instruction.md`, `pr-ops/backlog-repository.md`, `pr-ops/backlog-ba-model.md`, `BACKLOG.md` v1.0. |
| Отличие не названо | [`pr-ops/backlog-instruction.md` §«Отличия от бэклога Хаба»](https://github.com/G-Ivan-A/mango_ba_prompts/blob/6cda9f5/pr-ops/backlog-instruction.md) перечисляет 5 отличий (число файлов, уровень заголовков, `null`, зависимости, префикс `BL`), но не имя каталога, и при этом ссылается на `ops/backlog-instruction.md` Хаба. |
| Обоснование в профиле устарело | Декларация `pr-ops` в `project_specific_directories`: «Дом наследован от модели репозитория Хаба (`pr-ops/repo-model.md`)» — такого пути в Хабе нет с 2026-09-09. |
| RFC модернизации не рассматривал вопрос | [`docs/rfc/2026-10-repository-modernization.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/6cda9f5/docs/rfc/2026-10-repository-modernization.md) упоминает `pr-ops/BACKLOG.md` только как файл с ссылками для правки (T-08). |

**Вердикт:** отличие **не обосновано** ни (а), ни (б). Единственный аргумент
«каталог унаследован от Хаба» опровергнут самим Хабом.

**Цена миграции** (измерено `grep` на `6cda9f5`): 394 вхождения `pr-ops` в
markdown, 75 — в Python, 85 файлов всего (включая валидаторы
`scripts/validate_issue_*.py`). Это на порядок меньше, чем стоила та же миграция в
Хабе (1 087 вхождений в 140 файлах), и выполнимо тем же способом.

**Уточнение к ожиданию владельца.** Геном HTOM Хаба **не** делает `ops/`
каноническим каталогом спицы: в
[`templates/htom/tools/validate-repository-structure.sh`](../../templates/htom/tools/validate-repository-structure.sh)
`canonical_directories` = `.github`, `docs`, `tools`, `governance`,
`ai-governance`, `ai-rules`. Поэтому валидатор формально принимает и `pr-ops/`,
и `ops/` — любой из них должен быть задекларирован в
`project_specific_directories`. При этом шаблон `AGENTS.md` генома говорит
«Process contracts … live in `ops/`», а handover-промпт генома ссылается на
`ops/backlog.md`. Это противоречие в самом Хабе (см. рекомендацию H-1): оно и
позволило дрейфу пройти CI.

### Другие нарушения консистентности чтения

Проверка воспроизводима: копия спицы + валидаторы текущего генома Хаба
(`templates/htom/tools/*.sh`) → 6 FAIL:

```text
FAIL: missing file: AGENTS.md
FAIL: missing file: .github/ISSUE_TEMPLATE/task.md
FAIL: missing file: .github/ISSUE_TEMPLATE/task-creative.md
FAIL: ai-rules/AI_SESSION_HANDOVER_PROMPT.md must keep the {{REPO_NAME}} placeholder
ERROR: missing file: AGENTS.md
FAIL: .hub-profile.json не разбирается как JSON: archetype must be one of A, B, C, D
HTOM-team structure validation failed with 6 issue(s).
```

Собственный валидатор спицы (`tools/validate-repository-structure.sh`, локальная
версия) проходит: он не проверяет `AGENTS.md` и профиль — это и есть механизм,
которым расхождение остаётся незаметным.

| ID | Нарушение | Доказательство | Вердикт по критерию (а)/(б) | Рекомендация |
| --- | --- | --- | --- | --- |
| M-1 | `pr-ops/` вместо `ops/` | см. выше | **Не обосновано** | Миграция `pr-ops/` → `ops/` с записью в `path_migrations`, правкой валидаторов и строки «Отличия от бэклога Хаба». |
| M-2 | **Нет корневого `AGENTS.md`** | `ls AGENTS.md` → нет; bootstrap-стандарт: «Every ecosystem repository … MUST contain `/AGENTS.md`» | **Не обосновано.** Сама спица признаёт пробел: RFC модернизации, задача T-01 (DEC-07). | Выполнить T-01: `AGENTS.md` из `templates/htom/AGENTS.md`, проектные правила — только в `<project_specific_rules>`. |
| M-3 | В профиле нет `archetype`, `environment`, `profile_version` | `.hub-profile.json` спицы | Не обосновано; RFC спицы рекомендует `archetype: B` (DEC-07) | Добавить ключи вместе с M-2 (они проверяются на согласие с `AGENTS.md`). |
| M-4 | Синк с Хабом устарел на 2,5 месяца | `last_sync` 2026-08-17; в `ai-rules/` нет `agent-work-routing.md` и `agent-collaboration-rules.md` (ADR-021 Хаба), на которые ссылается `AGENTS.md` | Не обосновано | Ре-синк `scripts/sync_from_hub.py` на текущий `main` Хаба после M-1, M-2. |
| M-5 | Нет шаблонов постановки задач `task.md` / `task-creative.md` | `.github/ISSUE_TEMPLATE/` содержит только `prompt-feedback.yml`, `run-execution.yml`, `run-statistics.yml` | Частично обосновано: шаблоны прогонов — специфика проекта; отсутствие общих шаблонов задач — нет | Добавить два шаблона генома рядом с проектными. |
| M-6 | `docs/contracts/` существует (3 файла BCREQ) | `docs/contracts/bcreq-manual-state.md`, `bcreq-stage-gates.md`, `kb-citations.md`; `AGENTS.md` Хаба: «Do not create `docs/contracts/`» | Не обосновано: это процессные контракты BCREQ, их дом по модели — `ops/` (или `standards/`, если это норма) | Перенести вместе с M-1; записать в `path_migrations`. |
| M-7 | Два дома одного предмета: `docs/ba-process/` и `docs/ba-processes/` | `docs/ba-process/` содержит только `README.md` | Не обосновано (Anti-Inflation) | Слить в один каталог или превратить первый в указатель. |
| M-8 | Нет карты L1–L4 в `docs/` | L1–L4 (`vision.md`, `concept.md`, `architecture.md`, `roadmap.md`, все `accepted` 2026-10-31) есть, но `docs/README.md` отсутствует (только `.gitkeep`); у `aether-orbis-gra` карта есть | Рекомендация, не нарушение | Добавить `docs/README.md` с картой L1–L4 и SSOT. |
| M-9 | Статус в Хабе противоречит решению владельца | [`ops/backlog.md` Хаба](../../ops/backlog.md#статус-репозиториев-экосистемы): `mango_ba_prompts` — `legacy/archived`, «активная задача, предполагающая изменение этого репозитория, в бэклоге запрещена»; issue #713 и #413 спицы: владелец инициировал модернизацию | Это **апелляция** (см. ниже), а не дефект спицы | Владельцу: подтвердить новый статус; после решения обновить таблицу статусов Хаба. |

### Оправданные отличия (приняты)

| Отличие | Основание |
| --- | --- |
| `prompts/`, `patterns/`, `runs/`, `kb/`, `site/`, `scripts/`, `experiments/` | Продуктовые и эмпирические дома проекта; каждый задекларирован в `project_specific_directories` с причиной (критерий (а)). |
| Локальные `standards/` (контракты промптов, прогонов, БЗ) | Специфика предметной области; синкнутые стандарты помечены `source_of_truth`, решение — `docs/adr/0004-hub-resync-2026-08.md` (а). |
| `ai-rules/ai-quick-rules.md`, `ai-rules/AI_SESSION_HANDOVER_PROMPT.md`, `ai-governance/ai-governance.md` вместо корневых `AI_*.md` | Раскладка разрешена геномом (валидатор принимает три варианта) и совпадает с раскладкой Хаба (`ai-rules/`, `ai-governance/`); миграция записана в `path_migrations` (issue #291). Это **лучше** консистентно с Хабом, чем раскладка `aether-orbis-gra`. |
| Бэклог из трёх файлов, префикс `BL-NNN` | Записано в «Отличиях от бэклога Хаба» со ссылкой на разрешение issue #418 (б). |
| `standards/GLOSSARY.md` в верхнем регистре | Имя синкнутого файла на снимке Хаба; низкий приоритет, исправится ре-синком (M-4). |

### Апелляция (hybrid_work)

Постановка исходит из того, что модернизация `mango_ba_prompts` — действующая
работа. Бэклог Хаба (решение по issue #583) объявляет этот репозиторий
`legacy/archived` и запрещает задачи на его изменение. Варианты:
1) владелец подтверждает возврат `mango_ba_prompts` в `active` — тогда статус в
Хабе обновляется, рекомендации M-1…M-8 становятся задачами спицы;
2) статус `legacy/archived` сохраняется — тогда модернизация должна идти в
`mango-ba-ai-runtime`, а M-1…M-8 теряют смысл.
**Рекомендация исполнителя — вариант 1:** issue #413/#420 спицы — прямое и более
позднее (2026-10-31…11-01) решение владельца, чем #583. Решение остаётся за
владельцем; эта апелляция не блокирует анализ.

## Recommendations

**В `mango_ba_prompts`** (порядок важен: профиль и `AGENTS.md` — до ре-синка):

1. M-2 + M-3: `AGENTS.md` и ключи `archetype`/`environment` (задача T-01 RFC спицы).
2. M-1 + M-6: миграция `pr-ops/` → `ops/` и `docs/contracts/` → `ops/` одним PR
   с `path_migrations`; правка `scripts/validate_issue_*.py`; заменить
   устаревшую причину в декларации каталога.
3. M-4: ре-синк с текущим Хабом; M-5: шаблоны задач генома.
4. M-7, M-8: слияние `docs/ba-process*`, карта `docs/README.md`.
5. Подключить в CI спицы валидаторы генома Хаба (`validate-agents-bootstrap.sh`),
   чтобы дрейф ловился машиной.

**В Хабе** (предложения в бэклог, Hybrid: не исполняются в этой задаче):

- **H-1.** Устранить противоречие генома: `templates/htom/AGENTS.md` и
  handover-промпт называют `ops/` домом процессных контрактов, а
  `canonical_directories` генома `ops/` не содержит. Либо внести `ops/` в
  канонический набор генома, либо убрать `ops/` из текста шаблонов.
  Требует полномочий на изменение `templates/`.
- **H-2.** Обновить статус `mango_ba_prompts` в таблице статусов бэклога после
  решения по апелляции.

## Related Artifacts

- Парный анализ: [aether-orbis-gra: проверка передачи практик Хаба](2026-11-02-aether-orbis-gra-hub-practice-transfer-check.md).
- Решение о переименовании в Хабе: [RFC bootstrap 2026-09-04](../rfc/2026-09-04-rfc-bootstrap-environment-and-structure.md).
- Норма `AGENTS.md`: [bootstrap-стандарт](../../standards/agents-md-bootstrap-standard.md).
- Геном: [`templates/htom/`](../../templates/htom/README.md).
- Спица: [RFC модернизации](https://github.com/G-Ivan-A/mango_ba_prompts/blob/6cda9f5/docs/rfc/2026-10-repository-modernization.md),
  [`.hub-profile.json`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/6cda9f5/.hub-profile.json),
  [`pr-ops/backlog-instruction.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/6cda9f5/pr-ops/backlog-instruction.md).

**Воспроизведение проверки:**

```bash
git clone https://github.com/G-Ivan-A/mango_ba_prompts m && git -C m checkout 6cda9f5
cp hybrid-Intelligence-lab/templates/htom/tools/*.sh m/tools/
(cd m && bash tools/validate-repository-structure.sh)   # 6 issues
grep -ro 'pr-ops' --include=*.md m | wc -l               # 394
```
