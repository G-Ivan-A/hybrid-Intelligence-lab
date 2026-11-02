---
status: draft
version: 0.1
updated: 2026-11-02
temperature: 0.1
analysis-subtype: recommendation
source: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/713
scope: project
based_on: "aether-orbis-gra@1669943 (main, 2026-11-01); Hub main@782742b — AGENTS.md, templates/htom/, docs/analysis/2026-09-15-ai-directories-consolidation-analysis.md, docs/rfc/2026-09-03-rfc-agents-md-root-contract.md, ops/backlog.md"
related_artifacts:
  - "https://github.com/G-Ivan-A/aether-orbis-gra/blob/1669943/AI_QUICK_RULES.md"
  - "https://github.com/G-Ivan-A/aether-orbis-gra/blob/1669943/AI_SESSION_HANDOVER_PROMPT.md"
  - "https://github.com/G-Ivan-A/aether-orbis-gra/blob/1669943/AGENTS.md"
  - "https://github.com/G-Ivan-A/aether-orbis-gra/blob/1669943/docs/adr/2026-11-adr-001-separate-repository-and-ssot.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/templates/htom/README.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/analysis/2026-09-15-ai-directories-consolidation-analysis.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/analysis/2026-11-02-mango-ba-prompts-hub-practice-transfer-check.md"
---

# aether-orbis-gra: проверка передачи практик Хаба

## Summary / BLUF

**Проблема 2 подтверждена как факт, но не как ошибка переноса: корневые
`AI_QUICK_RULES.md`, `AI_SESSION_HANDOVER_PROMPT.md` (и `AI_GOVERNANCE.md`)
поставляет сам геном Хаба `templates/htom/`, и валидатор генома требует их
наличия.** Файлы спицы совпадают с шаблоном с точностью до подстановки
плейсхолдеров (8, 24 и 10 отличающихся строк `diff` соответственно). Ожидание
владельца «в Хабе один `AGENTS.md` с маршрутизацией на `ai-rules/`» верно для
самого Хаба, но геном HTOM от него отстал: после ADR-012 (корневой `AGENTS.md`)
он поставляет **две параллельные точки входа** — `AGENTS.md` и три корневых
`AI_*.md`, — а Хаб в 2026-09-15 сознательно оставил плоские файлы генома
([анализ консолидации `ai-*`](2026-09-15-ai-directories-consolidation-analysis.md)).
Корень дефекта — **в Хабе**, у спицы — его следствие. Отличие от Хаба формально
обосновано (выполнен действующий шаблон), но не выгодно: соседняя спица
`mango_ba_prompts` держит те же контракты в `ai-rules/` и `ai-governance/`, как
Хаб. **Рекомендация: перенести три файла в `ai-rules/` / `ai-governance/`
(вариант, который валидатор генома уже принимает) и исправить геном в Хабе.**
Найдено ещё 5 нарушений консистентности; главное — объявленный в `AGENTS.md`
бэклог проекта не существует, а handover-промпт ссылается на несуществующие
`ops/backlog.md` и `ops/session-digests.md`.

## Context / Scope

- **Дата:** 2026-11-02. **Режим:** Hybrid (задан в issue #713).
- **Что проверено:** `aether-orbis-gra` на `main@1669943` (PR #2 спицы, выделение
  проекта по issue #1) против Хаба `main@782742b`: корень, `docs/`,
  `.hub-profile.json`, `AGENTS.md`, корневые `AI_*.md`, CI и валидаторы; со
  стороны Хаба — следы выноса проекта.
- **Эталон:** [`AGENTS.md`](../../AGENTS.md) Хаба,
  [bootstrap-стандарт](../../standards/agents-md-bootstrap-standard.md), геном
  [`templates/htom/`](../../templates/htom/README.md) (у спицы `target_type: HTOM`,
  `archetype: D`).
- **Критерий допустимости отличия:** (а) обосновано спецификой проекта или
  (б) прямо согласовано/задано владельцем.

### Нормализованная постановка (интерпретация исполнителя)

| Уровень | Содержание |
| --- | --- |
| Цель | Выделенный из Хаба проект читается так же, как Хаб и другие спицы; правила агента имеют одну точку входа; отличия обоснованы. |
| Задачи | 1) проверить корневые `AI_QUICK_RULES.md` / `AI_SESSION_HANDOVER_PROMPT.md` против модели «`AGENTS.md` → `ai-rules/`»; 2) найти другие проблемы переноса практик и стандартов, включая сторону Хаба; 3) вердикт по каждому отличию; 4) отдельный аналитический артефакт с именем проекта в имени файла. |
| Границы | Анализ и рекомендации в Хабе; правки спицы и генома Хаба — отдельные задачи (изменение `templates/` требует явных полномочий). |
| SSOT результата | Этот файл в `docs/analysis/` Хаба. |
| Критерии приёмки | Каждая находка с путём/коммитом; вердикт и рекомендация на каждое отличие; найден корень, а не только симптом. |

## Findings / Options

### Проблема 2: корневые `AI_*.md` — источник в геноме Хаба

| Факт | Доказательство |
| --- | --- |
| Геном поставляет файлы в корень | [`templates/htom/`](../../templates/htom/README.md): `AI_GOVERNANCE.md`, `AI_QUICK_RULES.md`, `AI_SESSION_HANDOVER_PROMPT.md`; README генома описывает их как структуру HTOM-команды. |
| Спица скопировала их без изменений | `diff` шаблона (без плейсхолдеров) и файлов спицы: 8 / 24 / 10 строк — только подстановки имени и URL. Импорт сделан `tools/import_from_hub.py` спицы со снимка `32b5fa5`. |
| Валидатор генома требует один из вариантов | [`templates/htom/tools/validate-repository-structure.sh`](../../templates/htom/tools/validate-repository-structure.sh): `AI_QUICK_RULES.md` \| `governance/AI_QUICK_RULES.md` \| `ai-rules/ai-quick-rules.md`; так же для handover и governance. |
| Хаб знал о дубле и отложил исправление | [RFC корневого `AGENTS.md`](../rfc/2026-09-03-rfc-agents-md-root-contract.md), находка K-3: шаблонные `AI_QUICK_RULES.md`/handover отправляют агента в `CONTRIBUTING.md` как governance-чек-лист — «риск раздвоения SSOT»; исправление отнесено к B-111 (`todo`). В спице этот текст сохранился: `AI_QUICK_RULES.md` п. 4, handover строки 68–76. |
| Хаб сознательно сохранил плоские файлы генома | [Анализ консолидации `ai-*`](2026-09-15-ai-directories-consolidation-analysis.md): «Геном физически поставляет три плоских корневых файла … валидатор уже принимает три альтернативные раскладки». |

**Вердикт.** По критерию (а)/(б) отличие **формально обосновано**: спица
выполнила действующий шаблон Хаба. По цели задачи (единообразное чтение)
**не выгодно**: (1) у агента две точки входа с пересекающимися правилами, что
противоречит духу правила `AGENTS.md` «single entrypoint … rules are not copied»;
(2) две спицы экосистемы держат один контракт в разных местах (`mango_ba_prompts`
— `ai-rules/ai-quick-rules.md`, `aether-orbis-gra` — `AI_QUICK_RULES.md`).

**Варианты:**
1. Спица переносит файлы в `ai-rules/ai-quick-rules.md`,
   `ai-rules/AI_SESSION_HANDOVER_PROMPT.md`, `ai-governance/ai-governance.md`
   (раскладка Хаба и mango; валидатор уже принимает) с `path_migrations`.
2. Хаб меняет геном: поставлять эти контракты в `ai-rules/` и `ai-governance/`,
   убрать K-3, оставить корневой `AGENTS.md` единственной точкой входа.
3. Ничего не менять — отклонено: дрейф между спицами останется.

**Рекомендация: 2, затем 1** (сначала устранить источник, иначе следующий
выделенный проект повторит дефект). Если Хаб не готов менять геном, вариант 1
выполним в спице сразу.

### Другие проблемы консистентности

Валидаторы текущего генома Хаба на копии спицы — **pass** (`AGENTS.md bootstrap
validation passed (D/local)`, `HTOM-team structure validation passed`). Поэтому
ниже — смысловые расхождения, которые машина не видит.

| ID | Нарушение | Доказательство | Вердикт (а)/(б) | Рекомендация |
| --- | --- | --- | --- | --- |
| A-1 | **Объявленного бэклога нет** | `AGENTS.md` спицы, hard rule 5: «Check the project backlog before starting»; файла бэклога в репозитории нет (`ops/` отсутствует) | Не обосновано | Создать `ops/backlog.md` (задекларировать `ops` в `project_specific_directories` — геном его каноническим не считает) или явно указать, что бэклог ведётся в GitHub Issues. |
| A-2 | Висячие ссылки handover-промпта | `AI_SESSION_HANDOVER_PROMPT.md` стр. 55–70: `ops/session-digests.md`, `ops/backlog.md`, `ops/repo-model.md`, `ops/artifact-map.md`, `standards/project-structure-inheritance.md` — локально не существуют | Не обосновано (наследие генома) | Вместе с A-1; в геноме — H-1 (см. парный анализ mango) и H-3 ниже. |
| A-3 | Хаб не знает о выносе | В Хабе 0 упоминаний `aether-orbis-gra` (`grep -rn aether-orbis-gra --include=*.md`); таблица статусов в [`ops/backlog.md`](../../ops/backlog.md#статус-репозиториев-экосистемы) её не содержит; ADR-001 спицы сам предлагает «отдельным PR в Хабе зафиксировать вынос (ADR и указатель)» — не сделано | Не обосновано | Строка статуса в бэклоге Хаба и указатель в `research/reputation-technologies/README.md` на новый SSOT. |
| A-4 | Два SSOT курса после выноса | Спица импортировала снимок `32b5fa5` (ADR-001); Хаб после этого продолжает добавлять материалы курса в `research/reputation-technologies/` (issue #711, слит 2026-11-02) | Требует решения владельца (б) | Зафиксировать, где живёт курс после выноса; затем либо ре-импорт, либо заморозка Хаб-копии со статусом `superseded`. |
| A-5 | Имя проекта двусмысленно в экосистеме | В бэклоге Хаба есть отдельная спица `aether-orbis` (`active`) и задача B-113 о её геноме; `aether-orbis-gra` — другой репозиторий | Рекомендация | В таблице статусов указать оба репозитория и их связь, чтобы B-113 не применили не к тому репозиторию. |

### Оправданные отличия (приняты)

| Отличие | Основание |
| --- | --- |
| `methodology/`, `education/`, `tests/` | Задекларированы в `project_specific_directories` с причинами; перенос курса разрешён владельцем в issue #1 спицы (б); ADR-001. |
| L1–L4 = vision, concept, **methodology**, roadmap; карта в `docs/README.md` | ADR-002 спицы: проект — методология; структура L1–L4 читается так же, как в Хабе и mango (а). |
| `archetype: D` при `target_type: HTOM` | Архетип D (обучающий пакет) соответствует курсу; ADR-001 (а). |
| `<project_specific_rules>` в `AGENTS.md` (7 правил о статусе GRA, этике данных и т. д.) | Общие секции совпадают с шаблоном генома; проектный слой — единственное разрешённое место для дельты (а). |
| `CITATION.cff`, `docs/overview.en.md` | Внешняя аудитория и партнёры — специфика проекта (а). |

## Recommendations

**В `aether-orbis-gra`:**

1. A-1 + A-2: завести бэклог (`ops/backlog.md` с декларацией `ops`) — тогда
   ссылки handover-промпта станут рабочими.
2. Перенести `AI_QUICK_RULES.md`, `AI_SESSION_HANDOVER_PROMPT.md`,
   `AI_GOVERNANCE.md` в `ai-rules/` и `ai-governance/` с `path_migrations`
   (если Хаб не исправит геном раньше — после исправления это сделает ре-синк).
3. Убрать из `AI_QUICK_RULES.md` / handover отсылку к `CONTRIBUTING.md` как к
   governance-чек-листу (K-3).

**В Хабе** (предложения в бэклог; Hybrid: не исполняются в этой задаче):

- **H-1** (общая с mango): согласовать `ops/` в шаблонах генома и в
  `canonical_directories`.
- **H-3.** Обновить геном `templates/htom/`: контракты агента — в `ai-rules/` и
  `ai-governance/`, без корневых `AI_*.md`; закрыть K-3 (B-111). Требует
  полномочий на изменение `templates/`.
- **H-4.** A-3 + A-5: строка `aether-orbis-gra` в таблице статусов и указатель
  выноса в `research/reputation-technologies/README.md`.
- **H-5.** A-4: решение владельца о единственном SSOT материалов курса.

## Related Artifacts

- Парный анализ: [mango_ba_prompts: проверка передачи практик Хаба](2026-11-02-mango-ba-prompts-hub-practice-transfer-check.md).
- [Анализ консолидации `ai-*`](2026-09-15-ai-directories-consolidation-analysis.md), [RFC корневого `AGENTS.md`](../rfc/2026-09-03-rfc-agents-md-root-contract.md).
- Геном: [`templates/htom/`](../../templates/htom/README.md).
- Спица: [`AGENTS.md`](https://github.com/G-Ivan-A/aether-orbis-gra/blob/1669943/AGENTS.md),
  [ADR-001](https://github.com/G-Ivan-A/aether-orbis-gra/blob/1669943/docs/adr/2026-11-adr-001-separate-repository-and-ssot.md).

**Воспроизведение проверки:**

```bash
git clone https://github.com/G-Ivan-A/aether-orbis-gra a && git -C a checkout 1669943
for f in AI_QUICK_RULES.md AI_SESSION_HANDOVER_PROMPT.md AI_GOVERNANCE.md; do
  diff <(sed 's/{{[a-zA-Z_]*}}//g' hybrid-Intelligence-lab/templates/htom/$f) a/$f | grep -c '^[<>]'
done                                                     # 8, 24, 10
cp hybrid-Intelligence-lab/templates/htom/tools/*.sh a/tools/
(cd a && bash tools/validate-repository-structure.sh)    # passed
ls a/ops 2>&1                                            # нет каталога
```
