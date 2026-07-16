---
status: canonical
version: 1.34
updated: 2026-07-16
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
  - "docs/adr/2026-07-adr-008-standard-meta-structure.md"
  - "standards/standard-meta-structure.md"
  - "docs/audit/2026-07-04-cross-standard-stress-tests.md"
  - "research/hub/2026-07-04-hub-as-agent-system-global-analysis.md"
  - "tools/test-post-migration-validator.sh"
  - "LICENSE"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/396"
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
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/394"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/398"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/400"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/402"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/411"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/413"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/419"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/417"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/427"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/423"
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
После завершения реструктуризации бэклога в этой цепочке остались связанные
governance-задачи: amendment policy для малых правок, lightweight
health-практика и отдельный RFC по frontmatter validator. Они определяют, как
бэклог и проверки дальше меняются без раздувания процесса.

**Цель.**
Зафиксировать правила малых governance-изменений и поддерживающих проверок для
уже действующего active-planning backlog.

**Критерий закрытия.**
Спринт закрывается, когда B-036 зафиксировал amendment policy, а B-014/B-015
либо выполнены, либо явно оставлены по своим триггерам.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
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
Audit и Report standards. Stress-test artifact уже маршрутизирован в Audit;
теперь нужно выбрать общий инвариант и только после этого править стандарты.

Этот спринт сохраняет цепочку Analysis -> ADR -> Standard -> Implementation.
Так он не смешивает аудит, выбор решения, нормирование и массовое обновление
существующих стандартов в один PR.

**Цель.**
Принять и применить единый skeleton для стандартов, чтобы future standards не
расходились по section order, profile/model policy и boundary delegation.

**Критерий закрытия.**
B-050/B-051 приняли решение, B-052 создал meta-standard, B-053 выровнял четыре
стандарта, а B-054 остался отложенным или выполнен после B-053.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-050** | Варианты решения структурного рассинхрона стандартов R/A/A/Report | **P1** | B-049 | review | [#407](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/407), [#415](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/415) | Issue #374; findings issue #370; [analysis B-050](../docs/analysis/2026-07-10-r-a-a-report-structural-desync-options.md) | Review amendment устранил circular scoring и вынес в B-051 явный выбор: baseline E либо skeleton F8/F10/F12; `Type Model` = `model`/`N/A`, specific tail связан с Purpose/Scope, routing owner = ADR-002, миграция разделена на mechanical/semantic. Стандарты и валидаторы не менялись. | Hybrid |
| **B-051** | Принять мета-структуру стандартов | **P1** | B-050 | review | [#417](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/417) | Issue #374; [analysis B-050](../docs/analysis/2026-07-10-r-a-a-report-structural-desync-options.md); [ADR-008](../docs/adr/2026-07-adr-008-standard-meta-structure.md) | Founder decision принят: F10 explicit с точным порядком 10 секций, `N/A + rationale` для всех пустых invariant sections, `Type Model` = `model`/`N/A`, Purpose/Scope cross-reference для specific tail и ADR-002 как canonical routing owner. | Hybrid |
| **B-052** | Создать мета-стандарт структуры стандартов | **P1** | B-051 | review | [#423](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/423) | Issue #374; [ADR-008](../docs/adr/2026-07-adr-008-standard-meta-structure.md); [Standard Meta-Structure Standard](../standards/standard-meta-structure.md) | F10 explicit нормативно зафиксирован: десять уникальных секций в строгом порядке, `N/A + rationale`, `Type Model` = `model`/`N/A`, specific-tail cross-reference, ADR-002 как canonical boundary owner и точная граница machine/human validation. | Structured |
| **B-053** | Привести Research/Analysis/Audit/Report standards к мета-стандарту | **P1** | B-052 | TODO | - (planned) | Issue #374; [Standard Meta-Structure Standard](../standards/standard-meta-structure.md) | Обновить четыре стандарта двумя reviewable слоями: mechanical block moves и отдельно обоснованные semantic deltas. Синхронизировать validators/navigation where required. | Structured |
| **B-054** | Стандарт процесса стресс-тестирования связанных документов | **P3** | B-048, B-053 | TODO | - (deferred) | Issue #374; issue #370 | Отложенная process-задача: описать триггеры, метод, severity/output route и критерии acceptance для повторяемых cross-document stress tests. Не делать до B-053. | Structured |

---

## Спринт 4: Post-migration границы корня Хаба

**Story.**
ADR-007 и PR #388 физически перестроили корень Хаба, но часть follow-up решений
остаётся на уровне активной синхронизации. Здесь собраны задачи, которые
уточняют границы `ai-governance/`, `ai-rules/`, `practices/`, retired website
strategy и будущих root catalogs.

Спринт отделяет уже поглощённые ADR-007 решения от ещё не начатых
trigger-based исследований. Это важно после миграции: новые каталоги не должны
заполняться на вырост, а follow-up должен возникать из реальной боли.

**Цель.**
Довести post-migration границы до исполнимого состояния без расширения
репозитория пустыми правилами и speculative artifacts.

**Критерий закрытия.**
Boundary work по `ai-governance/`/`ai-rules/` выполнен или явно закрыт;
absorbed ADR-007 задачи закрыты; B-059..B-062 стартуют только по своим триггерам.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-056** | Физически разделить remaining policy/rule material между `ai-governance/` и `ai-rules/` | **P1** | B-048, B-047 | review | [#425](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/425) | Issue #376; issue #378; B-034 Phase 3; ADR-007/B-047 | Root `AI_GOVERNANCE.md` разделён на policy-контракт `ai-governance/ai-governance.md` и agent rules `ai-rules/agent-work-rules.md`; `GOVERNANCE.md` оставлен thin root-anchor по ADR-007. Ссылки, validator и artifact map синхронизированы. | Hybrid |
| **B-057** | Зафиксировать специфичность Хаба: root `practices/` vs `docs/practice/` | **P1** | B-047 | review (absorbed by ADR-007/B-047) | [#378](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/378) | Issue #380; B-034 document-plan; ADR-007 | ADR-007 уже оставляет root `practices/` как Hub-specific Archetype A extension. Строка нужна для traceability; отдельный ADR не нужен, если ADR-007 не superseded. | Structured |
| **B-058** | Отменить или подтвердить веб-стратегию Хаба (`website/`, `mkdocs.yml`) | **P1** | B-047 | review (absorbed by ADR-007/B-047) | [#378](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/378) | Issue #380; B-034 document-plan; ADR-007; former `mkdocs.yml` | ADR-007 retired `website/` and `mkdocs.yml`; PR #388 physically removed them. Строка остаётся review-traceability до финального закрытия. | Structured |
| **B-059** | Проверить целесообразность `docs/guides/` как единого дома руководств | **P3** | B-048 | TODO | - (deferred) | Issue #380; B-034; ADR-007; current `guides/` | Triggered research for guide routing when `guides/` vs `docs/guides/` creates review pain or a reconcile task needs a decision. | Creative |
| **B-060** | Структура и правила наполнения `projects-sink/` | **P3** | B-048 | TODO | - (deferred) | Issue #380; B-034 Phase 4; ADR-007; `projects/` intake pain | Triggered research for managed intake from ecosystem projects. Rules should follow real intake ambiguity, not placeholder taxonomy. | Creative |
| **B-061** | Learning Profile архетипа D для `education/` | **P3** | B-048 | TODO | - (deferred) | Issue #380; B-034; ADR-007; `standards/education-profile.md` | Defer until founder starts an actual course or learning product; then standardize education/Learning Profile boundaries from practice. | Creative |
| **B-062** | Стандарт фреймворков (архетип A/B) для `frameworks/` | **P3** | B-048 | TODO | - (deferred) | Issue #380; B-034; ADR-007; current `frameworks/` placeholder | Defer until the first reusable framework emerges and the repo must decide whether it belongs to Hub capability or spoke/product material. | Creative |

---

## Спринт 5: Несущие дефекты агентной модели (v0.4, «сейчас»)

**Story.**
Глобальный анализ Хаба как агентной системы (v0.4, issues #394/#398/#400)
консолидировал 17 ❌ в 11 пробелов (§11) и 11 рекомендаций (§8). Три из них
помечены как P1 «несущие»: они не требуют нового слоя, а чинят расхождение уже
существующей модели с её же интерфейсом и практиками. `task.yml` не даёт выбрать
Hybrid и Deep Think, хотя glossary трактует режим как регулятор автономии (пробел
B1). Метод стресс-тестирования применён уже дважды, но не зафиксирован как
повторяемая процедура с единым словарём вердиктов (пробел C1). Security-правила
рассеяны по практикам без единого чек-листа, размеченного по OWASP LLM Top-10 и
SAIF (пробел G2).

Этот спринт собирает именно «дешёвые и сейчас» правки: каждая закрывает несущий
дефект без введения новых каталогов, статусов или инфраструктуры. Он отделён от
V2-среза (Спринт 6), потому что здесь чинится текущая модель, а не строится новая
операционная способность.

**Цель.**
Устранить три P1-пробела (B1, C1, G2) точечными правками формы и нормы, не
нарушая anti-inflation.

**Критерий закрытия.**
Спринт закрывается, когда B-064 привёл `task.yml` к модели (или задокументировал
отсутствие режимов), B-065 зафиксировал метод стресс-тестирования, а B-066 собрал
единый OWASP-LLM чек-лист. Каждая задача проходит собственный RFC/ADR-цикл
(мета-рекомендация §8: не внедрять пакетом).

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-064** | Довести `task.yml` до модели: сделать Hybrid и Deep Think выбираемыми | **P1** | - | DONE | [#406](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/406) | Global analysis v0.4 §8/R1; §11-B1; H3; `research/hub/2026-07-04-hub-as-agent-system-global-analysis.md` | `.github/ISSUE_TEMPLATE/task.yml` предлагает `hybrid` и `deep-think` вместе со Structured/Creative; regression-test фиксирует интерфейс. | Hybrid |
| **B-065** | Зафиксировать метод стресс-тестирования как повторяемую процедуру | **P1** | - | DONE | [#406](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/406) | Global analysis v0.4 §8/R3; §9.4; §11-C1; H4/H27 | `ai-rules/adversarial-stress-testing.md` фиксирует ≥5 независимых тестов, словарь вердиктов, evidence/limitations и route вывода. | Hybrid |
| **B-066** | Единый OWASP-LLM чек-лист агентной системы (закрывает R2/G2) | **P1** | - | DONE | [#406](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/406) | Global analysis v0.4 §15.8.2/RFC-D; §15.1.8; §3.3; H25; §11-G2/R2 | `ai-governance/agent-security-checklist.md` собирает существующие контроли в risk-based checklist с трассой OWASP LLM01–LLM10:2025 и SAIF, residual risk и stop route. | Hybrid |

---

## Спринт 6: V2 — тонкий вертикальный срез «Валидация ФТ/ТЗ»

**Story.**
До-исследование §15 (issue #400) показало: прежний анализ закрыл структурную
готовность к миграции репо→агент, но не операционно-измеримую. Рекомендация для
RFC — **V2**, тонкий вертикальный срез на процессе «Валидация ФТ/ТЗ» с двумя
параллельными треками (библиотека промптов по статистике ∥ первый Агент). §15.8
выделяет три входа, замыкающих разрывы готовности ПГ-4: контракт evals (RFC-A),
правило изменения библиотеки по run-статистике (RFC-B) и план инфраструктуры
первого Агента (RFC-C). Четвёртый вход — наблюдаемость (RFC-G): нужен ли Хабу
эпизодический слой прогонов, без которого run-статистика RFC-B не на чем считать.

Этот спринт собран как причинная цепочка одной способности — сделать работу
агента измеримой: сначала контракт качества (evals), затем правило улучшения по
статистике и план первого агента, с открытым вопросом наблюдаемости в основании.
Он отделён от несущих правок (Спринт 5), потому что строит новую операционную
способность, а не чинит текущую модель.

**Цель.**
Подготовить входы для RFC, превращающие структурную готовность Mango в
операционно-измеримый срез V2, без принятия решений за человека (Rule 4).

**Критерий закрытия.**
Каждый вход (B-067..B-070) либо эскалирован в собственный RFC/ADR, либо явно
отложен под свой триггер. Наблюдаемость (B-070) координируется с анализом kb/runs
(`docs/analysis/2026-07-04-kb-runs-hub-applicability-analysis.md`) и ADR-007.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-067** | Контракт `evals`/golden-sets для спока | **P1** | - | review | [#426](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/426) | Global analysis v0.4 §15.8.2/RFC-A; §15.1.6; ПГ4.3; §11-D1/R6 | Форма evals не стандартизована (RO3): нет контракта golden-sets, рубрик и офлайн-проверок, по которым качество агента переводится в число. Новый переиспользуемый актив экосистемы. Создан [`standards/evals-contract-standard.md`](../standards/evals-contract-standard.md) в статусе `draft`: форма golden-set, бинарная рубрика, три слоя оценки, офлайн-проверки, метрики и форма записи порога. Значения порогов и минимальное N не назначены (Rule 4) — остаются за B-068; открытые вопросы Q1 (каталог evals в споке) и Q5 (область F10) вынесены в стандарт. | Hybrid |
| **B-068** | Правило «изменение библиотеки промптов по run-статистике» + порог N | **P1** | B-067, B-070 | TODO | - (planned) | Global analysis v0.4 §15.8.2/RFC-B; §15.6.1; ПГ-5; §11-A2/R4 | Governance-правило: когда run-статистика (при минимальном N + человеческое ревью) даёт основание менять библиотеку промптов. Требует контракта evals (B-067) и эпизодического слоя прогонов (B-070). | `null` |
| **B-069** | План инфраструктуры первого Агента (V2, «Валидация ФТ/ТЗ») | **P1** | B-067 | TODO | - (planned) | Global analysis v0.4 §15.8.2/RFC-C; §15.6.2; ПГ-6 | Проектный план тонкого вертикального среза: инфраструктура первого Агента на процессе «Валидация ФТ/ТЗ» с human gate на статус (RO2). Опирается на контракт evals (B-067). | `null` |
| **B-070** | Наблюдаемость: нужен ли Хабу эпизодический слой (`runs/`) (закрывает R4) | **P2** | - | TODO | - (deferred) | Global analysis v0.4 §15.8.2/RFC-G; §15.1.7; Q1; §11-A2/R4; ADR-007 | Открытый вопрос AgentOps: нужен ли Хабу журнал прогонов/трасс как эпизодическая память. Поглощает R4 (тот же пробел A2). Текущее решение по kb/runs (анализ 2026-07-04 + ADR-007) — не вводить до боли; строка держит вопрос трассируемым. | `null` |

---

## Спринт 7: Триггерные входы RFC/ADR из анализа v0.4

**Story.**
Оставшиеся входы §8/§11/§15.8 — второго порядка: они не чинят несущий дефект и не
входят в срез V2, а ждут собственного операционного триггера. Мета-рекомендация
§8 прямо запрещает внедрять их пакетом: каждый проходит собственный цикл
observation→RFC→ADR под свою боль, иначе массовое «улучшение» само нарушает
anti-inflation (H7, «start simplest»).

Внутри спринт держит несколько причинных пар: роутер и разум (доспецификация
роутера R5 и критерий вызова Deep Think R9 — оба про интерпретацию входа §9.1);
семантическая целостность (guardrails заземления цитат R6 и машиночитаемый тег
`layer` RFC-E, закрывающий single-source-of-truth R7); петля обучения (обратный
поток Hub↔project R8, без которого метрика петли R11 неизмерима). Отдельно —
watch-item внешних норм (R10) и учебный актив (RFC-F). Все строки — трассируемые
входы для человеческого RFC/ADR, не решения (Rule 4).

**Цель.**
Сохранить трассируемость P2/P3-входов v0.4, чтобы отсутствие строки не читалось
как упущение, но не запускать их до появления реальной боли.

**Критерий закрытия.**
Каждая строка стартует только по своему триггеру: либо эскалируется в RFC/ADR при
появлении боли, либо остаётся отложенной. Спринт не закрывается «пакетом».

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-071** | Доспецифицировать роутер для verb-less / unknown-type входа | **P2** | - | TODO | - (deferred) | Global analysis v0.4 §8/R5; §11-A1; H1/H2 | Роутер недоспецифицирован на входе без глагола / без объекта / неизвестного типа — нет явного правила дефолта и эскалации к человеку. Малая правка research-модели роутера; ценность растёт с числом нетипичных задач. | `null` |
| **B-072** | Семантические guardrails: заземление цитат и проверка ссылок | **P2** | - | TODO | - (deferred) | Global analysis v0.4 §8/R6; §11-D1; H12/H13/H20 | CI проверяет только форму; онбординг покрывает вход, но не середину исполнения. Добавить семантическую проверку (grounding цитат, валидность ссылок) с оценкой стоимости/ложных срабатываний на пилоте. | `null` |
| **B-073** | Машиночитаемый тег `layer` (проект/продукт) (закрывает R7) | **P2** | - | TODO | - (deferred) | Global analysis v0.4 §15.8.2/RFC-E; §15.3.2; ПГ3.5; H11; §11-G4/R7 | Контракт формы против расползания слоёв проект/продукт (RO4) и дрейфа корпуса норм. Поглощает R7 (тот же пробел G4): enforced-граница как single source of truth. | `null` |
| **B-074** | Материализовать обратный поток Hub↔project (трасса синка, арбитраж) | **P2** | - | TODO | - (deferred) | Global analysis v0.4 §8/R8; §9.2; §11-F1; H22 | Синхронизация Hub↔project недоматериализована (наименее зрелая область, 5 ⚠️): нет обратного потока практика→норма, арбитража конфликтов человеком и единой трассы синка. Требует продуктового решения о механике петли. | `null` |
| **B-075** | Критерий «когда вызывать Deep Think» + единое fail-состояние | **P3** | - | TODO | - (deferred) | Global analysis v0.4 §8/R9; §11-D2; H4/H8/H16 | Deep Think сейчас редкий метод; нужен критерий вызова, защита от само-галлюцинации панели и единое fail-состояние. Вводить только когда Deep Think станет частым. | `null` |
| **B-076** | Отслеживание версий внешних норм (EU AI Act, OWASP, NIST) | **P3** | - | TODO | - (deferred) | Global analysis v0.4 §8/R10; §11-G3; H24 | Внешние нормы эволюционируют — риск устаревания проекций. Watch-item; вводить после стабилизации корпуса, иначе обслуживание ради обслуживания. | `null` |
| **B-077** | Метрика эффективности петли обучения (practice-exchange) | **P3** | B-074 | TODO | - (deferred) | Global analysis v0.4 §8/R11; §11-F2; H23 | Нельзя измерить, «прижилась» ли практика. Требует сперва материализованной петли обучения (B-074/R8), поэтому зависит от неё. | `null` |
| **B-078** | Разместить учебный курс в `education/` Хаба | **P2** | - | TODO | - (deferred) | Global analysis v0.4 §15.8.2/RFC-F; §15.2.4; Vision | Международно-заземлённый курс рискует застрять в споке (RO6). Разместить учебный актив в `education/` Хаба как образовательный актив архетипа A. Наполнение — глоссарий §15.9. | `null` |

---

## Спринт 8: Разделение Mango на два репозитория

**Story.**
Текущий репозиторий `mango_ba_prompts` совмещает две роли: операционку (боевые
промпты с приватными данными, прогоны, golden-sets) и публичную методологию
(переиспользуемые паттерны, стандарты, примеры). Это создаёт проблемы:
приватные данные не могут быть публичными, публичный репо не может быть
витриной, разные темпы изменений требуют разных ревью-процессов. Фаундер
принял решение (обсуждение 2026-07-10) разделить Mango на публичный репо
`ai-ba-playbooks` (продукт-методология, архетип B, без привязки к бренду
Mango) и приватный репо `mango-ba-prompt-library` (операционка Mango).

Спринт собран как причинная цепочка: сначала ADR фиксирует решение в Хабе
(принцип «сначала Хаб, потом Mango»), затем план миграции определяет, что
куда переносится, затем создаются оба репозитория, затем выполняется
физическая миграция артефактов, и в конце настраивается и тестируется
односторонняя синхронизация приватный → публичный.

**Цель.**
Создать два репозитория с разными жизненными циклами и аудиториями,
мигрировать артефакты из `mango_ba_prompts` и настроить одностороннюю
синхронизацию приватный → публичный.

**Критерий закрытия.**
Спринт закрывается, когда ADR B-079 принят, план миграции B-080 составлен,
оба репозитория созданы (B-081, B-082), артефакты мигрированы (B-083), а
синхронизация настроена и протестирована (B-084).

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-079** | ADR о разделении Mango на два репозитория | **P1** | - | review | [#424](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/424) / [PR #429](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/429) | Обсуждение 2026-07-10 (решение фаундера); issues #411, #413 | Зафиксировать решение фаундера о разделении Mango на публичный (`ai-ba-playbooks`) и приватный (`mango-ba-prompt-library`) репозитории через ADR: причина разделения, структура обоих репо, механизм синхронизации, связь с Хабом. Результат: `docs/adr/2026-07-adr-009-mango-repo-split.md` (`status: proposed` до acceptance gate на merge). | Hybrid |
| **B-080** | План миграции Mango | **P2** | B-079 | TODO | - (planned) | ADR B-079; issues #411, #413 | На основе ADR B-079 составить план миграции: какие артефакты из `mango_ba_prompts` идут в публичный репо, какие — в приватный, какие удаляются/архивируются, порядок миграции и синхронизация ссылок/реестров. | Structured |
| **B-081** | Создание публичного репо `ai-ba-playbooks` | **P2** | B-079, B-080 | TODO | - (planned) | ADR B-079; план миграции B-080; issues #411, #413 | Создать публичный репозиторий `ai-ba-playbooks` с базовой структурой архетипа B (`prompt-library/`, `patterns/`, `standards/`, `examples/`, `docs/`, `templates/`) и настроить GitHub Pages для презентационного слоя. | Structured |
| **B-082** | Создание приватного репо `mango-ba-prompt-library` | **P2** | B-079, B-080 | TODO | - (planned) | ADR B-079; план миграции B-080; issues #411, #413 | Создать приватный репозиторий `mango-ba-prompt-library` со структурой операционки (`prompts/`, `kb/processes/`, `runs/`, `evals/`, `internal-rfc/`, `internal-docs/`) и настроить локальные валидаторы без GitHub Actions. | Structured |
| **B-083** | Физическая миграция артефактов из `mango_ba_prompts` | **P2** | B-081, B-082 | TODO | - (planned) | План миграции B-080; issues #411, #413 | Перенести артефакты из `mango_ba_prompts` в новые репозитории согласно плану миграции B-080, обновить ссылки и реестры, прогнать валидаторы. | Structured |
| **B-084** | Синхронизация и тестирование | **P2** | B-083 | TODO | - (planned) | ADR B-079; issues #411, #413 | Настроить одностороннюю синхронизацию приватный → публичный (ручной отбор на старте), протестировать workflow и задокументировать lessons learned. | Structured |

## Спринт 9: Теоретическая основа образовательного модуля

**Story.**
Глобальный анализ v0.4 (§15.2) фиксирует структуру обучения и выносит RFC-F
(«Размещение учебного курса в `education/` Хаба») как вход для решения
фаундера. Но RFC-F нечем наполнить: решение о курсе по retrieval-стратегиям
принималось бы на основании блогов и вкусовых предпочтений, а не на основании
того, что известно предметной области. Спринт закрывает этот разрыв: сначала
исследование даёт source-backed теорию, затем RFC-F принимает решение о
продукте.

**Цель.**
Дать фаундеру проверяемый вход для RFC-F: что известно про retrieval-стратегии,
откуда это известно, какие утверждения не выдерживают проверки и какие
конструкции (матрица, уровни готовности) переиспользуемы за пределами курса.

**Критерий закрытия.**
Спринт закрывается, когда исследование B-085 принято фаундером и RFC-F получил
вход. Решение о самом курсе — предмет отдельной задачи (Rule 4).

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-085** | Исследование retrieval-стратегий для AI-агентов | **P2** | - | review | [#418](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/418) | Issue #418 (постановка фаундера, гипотезы H1–H7); глобальный анализ v0.4 §15.1.4, §15.1.6, §15.2.5 (RFC-F) | Научно-теоретический survey и критический разбор retrieval-стратегий в трёх этапах: research questions, объектная модель, граф зависимостей, 9 точек решений, 20 гипотез с ранжированием; таксономии БЗ/запросов/стратегий, матрица «БЗ × Запрос → Стратегия», chunking/embeddings/reranking/evaluation, уровни готовности БЗ L0–L5; индустриальные кейсы, тренды 2024–2026, связь с памятью агента, вход для RFC-F. Результат: `research/education/2026-07-16-retrieval-strategies-survey.md` (`status: draft` до подтверждения фаундером). | Creative |
| **B-086** | Валидация шкалы готовности БЗ L0–L5 на реальных корпусах | **P3** | B-085 | TODO | - (planned) | Исследование B-085, §26.2 (признанная слабость: пороги не измерены) | Проверить шкалу L0–L5 на ≥3 реальных корпусах: воспроизводимы ли шесть признаков без построения индекса, различают ли пороги (95%/80%) уровни на практике, предсказывает ли уровень применимость стратегий. Условие перевода B-085 в `reviewed`. | Structured |
| **B-087** | Исследование самоотравления памяти агента | **P3** | B-085 | TODO | - (planned) | Исследование B-085, §19.2 (открытый вопрос О5) | Когда агент пишет в тот же корпус, из которого читает, возникает класс дефекта, не ловимый ни одной метрикой оценки RAG: faithfulness к самозаписанному контексту высока. Исследовать механизмы разделения пространств «знание человека» / «знание агента» и их различения при извлечении. | Creative |

---

## Спринт 9: Governance и юридическая чистота

**Story.**
Корневой `LICENSE` был governance placeholder: он фиксировал, что финальная
лицензия не выбрана, и не давал пользователям прав сверх платформенных. Для
базы знаний это блокирующая неопределённость — методологии Хаба создаются для
переиспользования внешними споками и сообществом, но без лицензии внешний
пользователь юридически не может ни адаптировать стандарт, ни встроить его в
коммерческий процесс.

Дополнительная сложность в том, что репозиторий неоднороден: основной актив —
текстовые артефакты (стандарты, промпты, ADR/RFC, исследования), а скрипты
(`tools/`, CI) вторичны и требуют другой правовой рамки, включая патентный
грант. Одна универсальная лицензия покрывает один из двух типов плохо, поэтому
решение фаундера (обсуждение 2026-07-10) — гибридная модель CC BY 4.0 +
Apache-2.0.

**Цель.**
Заменить license placeholder на юридически определённую модель лицензирования,
сохраняющую обязательное указание авторства и дающую внешним пользователям
явное право на переиспользование и коммерческое применение методологий Хаба.

**Критерий закрытия.**
Спринт закрывается, когда B-085 merged: корневой `LICENSE` содержит выбранную
модель, `README.md` объясняет права человекочитаемо, а карта артефактов и
`CHANGELOG.md` синхронизированы.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-085** | Гибридная лицензия репозитория Хаба | **P2** | - | review | [#419](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/419) / [PR #422](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/422) | Обсуждение с фаундером (2026-07-10); issue #419; ADR-007 | Заменить license placeholder на гибридную модель CC BY 4.0 (текстовые артефакты) + Apache-2.0 (скрипты) с разделением по признаку файла, обновить `README.md`, artifact map и changelog. | Hybrid |

## Отложенные задачи с триггером

Задачи этого блока не запускаются по факту регистрации. Они переходят в работу
только после появления указанной операционной боли, чтобы соблюдать принцип
Anti-Inflation.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-088** | Зафиксировать многоуровневую иерархию SSOT (ADR vs Стандарт) | **P3** | - | deferred (triggered) | - (tech debt) | Обсуждение 2026-07-16; B-050 v0.2 §2; [issue #427](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/427) | Текущая формулировка «ADR имеет приоритет» слишком общая. Необходимо чётко разграничить компетенции: ADR = SSOT для решений, Стандарт = SSOT для исполнения. Задача стартует **только** при появлении боли: повторяющиеся конфликты между свежим ADR и устоявшейся практикой в стандарте. | Creative |


---

## Источники активного порядка

| Источник | Что даёт бэклогу |
| --- | --- |
| [backlog-instruction.md](backlog-instruction.md) | Правила ведения, статусы, sprint format, archiving policy and `null` rule. |
| [docs/analysis/2026-06-30-backlog-and-artifact-change-policy-analysis.md](../docs/analysis/2026-06-30-backlog-and-artifact-change-policy-analysis.md) | Источник проблем перегрузки бэклога and amendment policy B-036. |
| [docs/analysis/2026-07-04-kb-runs-hub-applicability-analysis.md](../docs/analysis/2026-07-04-kb-runs-hub-applicability-analysis.md) | Trigger-based decision source for not adding root `kb/` and `runs/` to the Hub now. |
| [docs/adr/2026-07-adr-007-hub-root-structure.md](../docs/adr/2026-07-adr-007-hub-root-structure.md) | Decision source for post-migration root boundaries and B-056..B-063. |
| [docs/audit/2026-07-04-cross-standard-stress-tests.md](../docs/audit/2026-07-04-cross-standard-stress-tests.md) | Source findings for the standard-structure repair chain B-049..B-054 after B-049 routing to Audit. |
| [research/hub/2026-07-04-hub-as-agent-system-global-analysis.md](../research/hub/2026-07-04-hub-as-agent-system-global-analysis.md) | Global analysis v0.4 (issues #394/#398/#400): §8 рекомендации, §11 реестр пробелов, §15.8 входы RFC/ADR — источник задач B-064..B-078 (Спринты 5–7). |
| Issue [#411](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/411) / [#413](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/413) (обсуждение 2026-07-10, решение фаундера) | Источник задач B-079..B-084 (Спринт 8): разделение Mango на публичный `ai-ba-playbooks` и приватный `mango-ba-prompt-library` репозитории. |
| Issue [#419](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/419) (обсуждение 2026-07-10, решение фаундера) | Источник задачи B-085 (Спринт 9): гибридная лицензия CC BY 4.0 + Apache-2.0 и свобода исполнителя предложить альтернативу. |
| Issue [#418](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/418) (постановка фаундера) | Источник задач B-085..B-087 (Спринт 9): научно-теоретическое исследование retrieval-стратегий как вход для RFC-F и теоретическая основа образовательного модуля. |
| Issue [#427](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/427) (обсуждение 2026-07-16; B-050 v0.2 §2) | Источник triggered-задачи B-088: разграничение ADR как SSOT для решений и Стандарта как SSOT для исполнения только после появления повторяющейся операционной боли. |
| GitHub Issues/PR | История выполненных задач, review discussion and implementation evidence. |
