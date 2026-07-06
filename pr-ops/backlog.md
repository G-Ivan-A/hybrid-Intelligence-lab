---
status: canonical
version: 1.27
updated: 2026-07-04
temperature: 0.1
type: backlog
context: [governance, backlog, active-sprints, pr-ops, synchronization]
method: creative-analysis + dependency-mapping
scope: repo-wide
related_artifacts:
  - "pr-ops/backlog-instruction.md"
  - "pr-ops/artifact-map.md"
  - "pr-ops/repo-model.md"
  - "standards/glossary.md"
  - "standards/audit-standard.md"
  - "docs/analysis/2026-06-30-backlog-and-artifact-change-policy-analysis.md"
  - "docs/analysis/2026-07-04-kb-runs-hub-applicability-analysis.md"
  - "docs/adr/2026-07-adr-007-hub-root-structure.md"
  - "docs/report/2026-07-04-cross-standard-stress-tests.md"
  - "tools/test-post-migration-validator.sh"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/392"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/297"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/294"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/296"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/328"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/370"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/374"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/376"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/380"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/386"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/390"
---

# BACKLOG - активные спринты Хаба

Этот файл показывает только незавершённые задачи и их логический порядок.
Правила ведения бэклога вынесены в
[backlog-instruction.md](backlog-instruction.md).

Завершённые задачи удаляются из активного бэклога после архивации спринта.
История остаётся в GitHub Issues/PR, `CHANGELOG.md` и самих артефактах; отдельный
архивный файл бэклога не создаётся.

Если факта нет в исходных issue, PR, артефакте или текущем бэклоге, значение
указывается как `null`. Спринты ниже сгруппированы по логическим цепочкам, а не
по приоритетам.

---

## Спринт 1: Операционный слой бэклога

**Story.**
Бэклог был перегружен: правила работы, активные задачи, выполненная история и
детальные rationale жили в одном файле. Из-за этого синхронизация founder -
исполнитель - команда Q требовала чтения большого документа даже для простого
понимания текущего порядка работ.

Этот спринт отделяет правила от активных задач и оставляет в бэклоге только
рабочую очередь. Он также сохраняет рядом две связанные governance-задачи:
amendment policy для малых правок и lightweight health-практику, потому что они
определяют, как бэклог дальше меняется без раздувания процесса.

**Цель.**
Сделать `pr-ops/backlog.md` коротким active-planning документом, а правила его
ведения - отдельным контрактом в `pr-ops/backlog-instruction.md`.

**Критерий закрытия.**
Спринт закрывается, когда B-035 принят в review/merge, B-036 зафиксировал
amendment policy, а B-014/B-015 либо выполнены, либо явно оставлены по своим
триггерам.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-035** | Реструктурировать бэклог: active backlog + инструкции, без архивного файла | **P1** | B-048 | review | [#392](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/392) | Issue #392; issue #297 analysis | Текущий `pr-ops/backlog.md` разделён на активные спринты и `pr-ops/backlog-instruction.md`. История выполненных работ остаётся в GitHub Issues/PR и `CHANGELOG.md`; отдельный архивный файл не создаётся. | Creative |
| **B-036** | Зафиксировать 3-tier amendment policy в `AI_GOVERNANCE.md` | **P2** | - | TODO | - (tech debt) | Issue #297; `docs/analysis/2026-06-30-backlog-and-artifact-change-policy-analysis.md` | Нужно правило, когда допустима механическая или ограниченная правка, а когда требуется полный RFC/ADR path. Без policy малые изменения либо блокируются лишней церемонией, либо дрейфуют без контроля. | `null` |
| **B-014** | Лёгкий governance health: регулярный прогон валидаторов + мониторинг триггеров | **P3** | B-010 | TODO | - (отложено) | Креативное улучшение агента-исполнителя | Зафиксировать практику периодического запуска `validate-frontmatter.sh` и `validate-repository-structure.sh` вместе со сверкой backlog-триггеров. Вводить только при появлении боли от пропущенных регрессий или CI-потребности. | Structured |
| **B-015** | RFC: Валидатор frontmatter, миграция статусов и approved list | **P2** | RFC/ADR structure standards | TODO | - (tech debt) | `research/hub/2026-06-28-ripple-effects-282-research.md`; issue #286 | Нужен отдельный RFC/implementation path для routing валидатора, матрицы миграции статусов, approved fields и режима CI. Issue #286 сознательно не меняет validator/migration rules. | Structured |

---

## Спринт 2: Выравнивание evidence и cleanup артефактов

**Story.**
Research, Analysis и Reports цепочки уже получили стандарты и decision records,
но часть физической структуры и ссылок ещё отражает старое состояние. Эти задачи
не принимают новые решения, а приводят существующие артефакты к уже принятому
маршруту.

Спринт собран как cleanup-chain: сначала evidence-контейнеры и валидатор, затем
модернизация Analysis и Reports. Это снижает риск скрытой миграции, потому что
каждая строка ограничена уже существующим стандартом или inventory.

**Цель.**
Убрать старые формы размещения evidence и привести Analysis/Reports artifacts к
принятым стандартам без переоткрытия решений.

**Критерий закрытия.**
Все cleanup-задачи выполнены или имеют явные исключения; ссылки, artifact-map и
валидаторы проходят локальную проверку.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-022** | Мигрировать существующие `exp-*` в контейнер `exp/`, убрать `outputs/` | **P2** | B-018, B-019 | TODO | - (tech debt) | Issue #294; issue #290; текущие `research/hub/exp-*` | Перенести legacy experiment folders в согласованный `research/<domain>/exp/` и убрать вложенный `outputs/` по research standard. Содержательные результаты экспериментов не менять. | Structured |
| **B-023** | Обновить валидатор структуры под `exp/` и routing по типам задач | **P2** | B-018, B-019 | TODO | - (tech debt) | Issue #294; `tools/validate-repository-structure.sh`; `tools/validate-file-naming.sh` | Сделать принятый `exp/` contract исполнимым: проверять контейнер, parent links, запрет legacy shape или явные exceptions. | Structured |
| **B-028** | Cleanup и модернизация Analysis-артефактов | **P2** | B-027 | TODO | - (tech debt) | Issue #296; B-024 inventory; `standards/analysis-standard.md` | Убрать или явно отложить дубли Analysis, обновить frontmatter, cross-references, lifecycle и индексы по принятому Analysis standard. Не выполнять широкую физическую миграцию. | Structured |
| **B-044** | Cleanup и модернизация Reports-артефактов в `docs/report/` | **P2** | B-043, B-034 | TODO | - (tech debt) | Issue #328; Reports inventory; `standards/report-standard.md`; B-034 | Обновить Reports-кандидаты: `report-subtype`, relation-поля, дубли, masked reports, artifact-map и индексы. Координируется с migration plan B-034. | `null` |

---

## Спринт 3: Ремонт структуры стандартов

**Story.**
Кросс-стресс-тест issue #370 обнаружил рассинхрон между Research, Analysis,
Audit и Report standards. Проблема не решается одной правкой текста: сначала
нужно правильно маршрутизировать сам stress-test artifact, затем выбрать общий
инвариант и только после этого править стандарты.

Этот спринт сохраняет цепочку Analysis -> ADR -> Standard -> Implementation.
Так он не смешивает аудит, выбор решения, нормирование и массовое обновление
существующих стандартов в один PR.

**Цель.**
Принять и применить единый skeleton для стандартов, чтобы future standards не
расходились по section order, profile/model policy и boundary delegation.

**Критерий закрытия.**
B-049 перенёс audit artifact в правильный route, B-050/B-051 приняли решение,
B-052 создал meta-standard, B-053 выровнял четыре стандарта, а B-054 остался
отложенным или выполнен после B-053.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-049** | Переместить отчёт кросс-стресс-тестов в `docs/audit/` и модернизировать frontmatter | **P1** | B-033, B-043 | TODO | - (planned) | Issue #374; issue #370; `docs/report/2026-07-04-cross-standard-stress-tests.md` | Stress-test report имеет audit-природу, но лежит в `docs/report/`. Нужно перенести его в Audit route, добавить audit frontmatter/sections и обновить ссылки. | Structured |
| **B-050** | Варианты решения структурного рассинхрона стандартов R/A/A/Report | **P1** | B-049 | TODO | - (planned) | Issue #374; findings issue #370 | Сравнить варианты meta-structure: профили, model block, allowed differences, validator impact и review ergonomics. Результат - recommendation для ADR B-051, без правки стандартов. | `null` |
| **B-051** | Принять мета-структуру стандартов | **P1** | B-050 | TODO | - (planned) | Issue #374; future analysis B-050 | Human decision gate: принять или скорректировать recommendation B-050, зафиксировать invariant skeleton, frontmatter convention и boundary-delegation rule. | Structured |
| **B-052** | Создать мета-стандарт структуры стандартов | **P1** | B-051 | TODO | - (planned) | Issue #374; future ADR B-051 | Нормативно описать структуру стандартов: обязательные секции, порядок, profile/model slot policy, frontmatter conventions and validation expectations. | Structured |
| **B-053** | Привести Research/Analysis/Audit/Report standards к мета-стандарту | **P1** | B-052 | TODO | - (planned) | Issue #374; future meta-standard B-052 | Обновить четыре стандарта по принятому skeleton без переоткрытия смысловых решений. Синхронизировать validators/navigation where required. | Structured |
| **B-054** | Стандарт процесса стресс-тестирования связанных документов | **P3** | B-048, B-053 | TODO | - (deferred) | Issue #374; issue #370 | Отложенная process-задача: описать триггеры, метод, severity/output route и критерии acceptance для повторяемых cross-document stress tests. Не делать до B-053. | Structured |

---

## Спринт 4: Post-migration границы корня Хаба

**Story.**
ADR-007 и PR #388 физически перестроили корень Хаба, но часть follow-up решений
остаётся на уровне активной синхронизации. Здесь собраны задачи, которые
уточняют границы `ai-governance/`, `ai-rules/`, `practices/`, retired website
strategy, будущих root catalogs и post-migration validator coverage.

Спринт отделяет уже поглощённые ADR-007 решения от ещё не начатых
trigger-based исследований. Это важно после миграции: новые каталоги не должны
заполняться на вырост, а follow-up должен возникать из реальной боли.

**Цель.**
Довести post-migration границы до исполнимого состояния без расширения
репозитория пустыми правилами и speculative artifacts.

**Критерий закрытия.**
Boundary work по `ai-governance/`/`ai-rules/` и B-063 review выполнены или явно
закрыты; absorbed ADR-007 задачи закрыты; B-059..B-062 стартуют только по своим
триггерам.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-056** | Физически разделить remaining policy/rule material между `ai-governance/` и `ai-rules/` | **P1** | B-048, B-047 | TODO | - (planned) | Issue #376; issue #378; B-034 Phase 3; ADR-007/B-047 | Проверить оставшийся policy/compliance and agent-rule material, маршрутизировать его по ADR-007, обновить ссылки, validators, artifact-map и transition notes. | Structured |
| **B-063** | Ревизия валидаторов после физической миграции Хаба | **P2** | B-048 | review | [#390](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/390) / [PR #391](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/391) | issue #390; ADR-007/B-048; `pr-ops/artifact-map.md`; `pr-ops/repo-model.md`; validators | Post-migration audit closes stale validator references to retired root paths, adds regression coverage, and keeps validator registry files synced with the actual ADR-007 tree. | Structured |
| **B-057** | Зафиксировать специфичность Хаба: root `practices/` vs `docs/practice/` | **P1** | B-047 | review (absorbed by ADR-007/B-047) | [#378](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/378) | Issue #380; B-034 document-plan; ADR-007 | ADR-007 уже оставляет root `practices/` как Hub-specific Archetype A extension. Строка нужна для traceability; отдельный ADR не нужен, если ADR-007 не superseded. | Structured |
| **B-058** | Отменить или подтвердить веб-стратегию Хаба (`website/`, `mkdocs.yml`) | **P1** | B-047 | review (absorbed by ADR-007/B-047) | [#378](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/378) | Issue #380; B-034 document-plan; ADR-007; former `mkdocs.yml` | ADR-007 retired `website/` and `mkdocs.yml`; PR #388 physically removed them. Строка остаётся review-traceability до финального закрытия. | Structured |
| **B-059** | Проверить целесообразность `docs/guides/` как единого дома руководств | **P3** | B-048 | TODO | - (deferred) | Issue #380; B-034; ADR-007; current `guides/` | Triggered research for guide routing when `guides/` vs `docs/guides/` creates review pain or a reconcile task needs a decision. | Creative |
| **B-060** | Структура и правила наполнения `projects-sink/` | **P3** | B-048 | TODO | - (deferred) | Issue #380; B-034 Phase 4; ADR-007; `projects/` intake pain | Triggered research for managed intake from ecosystem projects. Rules should follow real intake ambiguity, not placeholder taxonomy. | Creative |
| **B-061** | Learning Profile архетипа D для `education/` | **P3** | B-048 | TODO | - (deferred) | Issue #380; B-034; ADR-007; `standards/education-profile.md` | Defer until founder starts an actual course or learning product; then standardize education/Learning Profile boundaries from practice. | Creative |
| **B-062** | Стандарт фреймворков (архетип A/B) для `frameworks/` | **P3** | B-048 | TODO | - (deferred) | Issue #380; B-034; ADR-007; current `frameworks/` placeholder | Defer until the first reusable framework emerges and the repo must decide whether it belongs to Hub capability or spoke/product material. | Creative |

---

## Источники активного порядка

| Источник | Что даёт бэклогу |
| --- | --- |
| [backlog-instruction.md](backlog-instruction.md) | Правила ведения, статусы, sprint format, archiving policy and `null` rule. |
| [docs/analysis/2026-06-30-backlog-and-artifact-change-policy-analysis.md](../docs/analysis/2026-06-30-backlog-and-artifact-change-policy-analysis.md) | Источник проблем перегрузки бэклога and amendment policy B-036. |
| [docs/analysis/2026-07-04-kb-runs-hub-applicability-analysis.md](../docs/analysis/2026-07-04-kb-runs-hub-applicability-analysis.md) | Trigger-based decision source for not adding root `kb/` and `runs/` to the Hub now. |
| [docs/adr/2026-07-adr-007-hub-root-structure.md](../docs/adr/2026-07-adr-007-hub-root-structure.md) | Decision source for post-migration root boundaries and B-056..B-063. |
| [docs/report/2026-07-04-cross-standard-stress-tests.md](../docs/report/2026-07-04-cross-standard-stress-tests.md) | Source findings for the standard-structure repair chain B-049..B-054. |
| GitHub Issues/PR | История выполненных задач, review discussion and implementation evidence. |
