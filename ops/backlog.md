---
status: canonical
version: 1.97
updated: 2026-11-28
temperature: 0.1
type: backlog
context: [governance, backlog, active-sprints, pr-ops, synchronization]
method: creative-analysis + dependency-mapping
scope: repo-wide
related_artifacts:
  - "ops/backlog-instruction.md"
  - "ops/artifact-map.md"
  - "ops/repo-model.md"
  - "standards/glossary.md"
  - "standards/audit-standard.md"
  - "docs/analysis/2026-06-30-backlog-and-artifact-change-policy-analysis.md"
  - "docs/analysis/2026-07-04-kb-runs-hub-applicability-analysis.md"
  - "docs/adr/2026-07-adr-007-hub-root-structure.md"
  - "docs/adr/2026-07-adr-008-standard-meta-structure.md"
  - "standards/standard-meta-structure.md"
  - "docs/audit/2026-07-04-cross-standard-stress-tests.md"
  - "research/hub/2026-07-04-hub-as-agent-system-global-analysis.md"
  - "docs/rfc/2026-08-06-rfc-task-statement-architecture.md"
  - "docs/rfc/2026-08-25-rfc-ba-artifact-pipeline-rrp-roadmap.md"
  - "research/ba-requirements/2026-08-26-m0-m2-layering-hypothesis-check.md"
  - "research/ba-requirements/exp/ba-artifact-pipeline-roadmap-541/README.md"
  - "research/ba-requirements/normalization/00-introduction.md"
  - "research/ba-requirements/methodology-unification/00-introduction.md"
  - "research/ba-requirements/2026-09-07-ecosystem-knowledge-inventory.md"
  - "research/hub/2026-07-31-ops-task-strategy-validation.md"
  - "tools/test-post-migration-validator.sh"
  - "LICENSE"
  - "docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md"
  - "docs/analysis/2026-11-03-ba-meta-model-extraction-step1.md"
  - "ops/hub-project-extraction-contract.md"
  - "docs/ecosystem-map.md"
  - "docs/rfc/2026-11-04-rfc-gra-extraction-completion-and-hub-cleanup.md"
  - "docs/analysis/2026-11-16-hub-optimization-start.md"
  - "research/hub/2026-11-28-digital-employee-methodology-survey.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/580"
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
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/434"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/423"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/436"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/437"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/449"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/475"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/511"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/515"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/555"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/575"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/715"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/717"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/727"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/723"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/721"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/738"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/740"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/747"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/749"
---

# BACKLOG - активные спринты Хаба

Этот файл показывает только незавершённые задачи и их логический порядок.
Правила ведения бэклога вынесены в
[backlog-instruction.md](backlog-instruction.md).

Завершённые задачи удаляются из активного бэклога после архивации спринта.
В рамках [#747](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/747)
также архивированы завершённые строки действующих спринтов.
История остаётся в GitHub Issues/PR, `CHANGELOG.md` и самих артефактах; отдельный
архивный файл бэклога не создаётся.

Если факта нет в исходных issue, PR, артефакте или текущем бэклоге, значение
указывается как `null`. Спринты ниже сгруппированы по логическим цепочкам, а не
по приоритетам.

---

## Статус репозиториев экосистемы

Статусы и классы репозиториев ведутся только в едином реестре —
[матрице проектов `docs/ecosystem-map.md`](../docs/ecosystem-map.md#матрица-проектов)
(решение владельца Q-4 в issue
[#717](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/717)); бэклог
не дублирует таблицу. Для задач бэклога из реестра следует:

- задачи, меняющие репозиторий класса `governed`, допустимы;
- `mango_ba_prompts` — `governed` (Q-3): статус `legacy/archived` по issue
  [#583](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583) отменён,
  а запрет #583 на активные задачи в нём снят. Исторические прогоны и промпты
  остаются свидетельством по
  [ADR-014](../docs/adr/2026-09-adr-014-legacy-evidence-not-baseline.md)
  (`LG-1`…`LG-6`) до уточнения ADR (B-267);
- `mango-ba-ai-runtime` — `exempt-runtime`, единственная среда исполнения MVP;
  задачи Спринта 19 (теперь в бэклоге `ba-ai-metamodel`) выполняются только в нём;
- для `dormant` (`open-ai.ru`) и `stopped` (`clarify-engine-ai`) задачи не
  планируются;
- `aether-orbis-gra` — `governed`, спица направления «Репутационные
  технологии (GRA)», вынесенного из `research/reputation-technologies/`
  2026-11-01. Исключение A-4 RFC #715 для домена GRA снято владельцем в
  [issue #725](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/725) (Q-1
  [RFC #721](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/rfc/2026-11-04-rfc-gra-extraction-completion-and-hub-cleanup.md)):
  задачи курса ведутся только в [бэклоге спицы](https://github.com/G-Ivan-A/aether-orbis-gra/blob/main/ops/backlog.md);
  шаги выноса в Хабе завершены и архивированы (Спринт 31).
- `ba-ai-metamodel` — `governed`, архетип B: дом проекта метамодели БА
  (`projects/ba-ai-process/` и связанных путей) после выноса по [ba-ai-metamodel#1](https://github.com/G-Ivan-A/ba-ai-metamodel/issues/1).
  Этапы E1–E6 приняты (PR #2–#7, `e1f67e2`); надгробие B-249 оставило в Хабе
  только манифесты redirect. Задачи проекта ведутся только в
  [бэклоге спицы](https://github.com/G-Ivan-A/ba-ai-metamodel/blob/main/ops/backlog.md).
  Шаг 3 Спринта 30 закрыт со стороны Хаба.

**Правило компиляции (`EP-C1` в редакции issue #583).** Исполняемые файлы
`mango-ba-ai-runtime` не содержат ссылок на исследовательские документы Хаба,
требующих перехода по ним для получения инструкции: пакет обязан работать в
изолированной среде. Ссылка на документ Хаба допустима только как
`derived_from` (происхождение нормы), а не как часть инструкции.

**Архивировано по issue #583.** Спринты 3 (ремонт структуры стандартов), 6
(V2 «Валидация ФТ/ТЗ»), 7 (триггерные входы RFC/ADR) и 8 (разделение Mango на
два репозитория) закрыты и удалены из активного бэклога по правилу архивации
[backlog-instruction.md](backlog-instruction.md). Обоснование по каждой задаче
записано в [`CHANGELOG.md`](../CHANGELOG.md); история — в GitHub Issues/PR.

**Архивировано по issue #725.** Спринт 29 (курс по репутационным технологиям
после Дня 1) закрыт по задаче B-275 и удалён из активного бэклога: B-228 —
`DONE` ([PR #661](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/661) слит); B-229 — `DONE` (материалы Дня 2 —
issues [#660](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/660), [#673](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/673), [#679](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/679),
теперь в спице); B-230, B-231, B-233 — `CANCELLED`, перенесены в спицу
([L84](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/ops/backlog.md#L84), [L85](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/ops/backlog.md#L85), [L86](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/ops/backlog.md#L86)); B-232 — `CANCELLED`:
каталог `gra-research-program/` уходит из дерева Хаба, а в спице его нет.
Решение — ответ владельца Q-1 в [issue #725](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/725).

**Архивировано по issue [#747](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/747).**
Спринты 23, 31 и 33 закрыты. B-281 — `DONE`: активный
[ruleset `archive-tags-immutable`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/rules/27672263)
защищает все пять архивных тегов от изменения и удаления
([CI на `main`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/actions/runs/44605421723)).
B-260 — `DONE`: из активных таблиц сняты завершённые строки, статусы `TODO`
приведены к одному написанию, повторов ID в Хабе нет. Источники приёмки и
указатель на архивированные строки записаны в [CHANGELOG](../CHANGELOG.md#changed).

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
| **B-059** | Проверить целесообразность `docs/guides/` как единого дома руководств | **P3** | B-048 | TODO | - (deferred) | Issue #380; B-034; ADR-007; current `guides/` | Triggered research for guide routing when `guides/` vs `docs/guides/` creates review pain or a reconcile task needs a decision. | Creative |
| **B-061** | Learning Profile архетипа D для `education/` | **P3** | B-048 | TODO | - (deferred) | Issue #380; B-034; ADR-007; `standards/education-profile.md` | Defer until founder starts an actual course or learning product; then standardize education/Learning Profile boundaries from practice. | Creative |
| **B-062** | Стандарт фреймворков (архетип A/B) для `frameworks/` | **P3** | B-048 | TODO | - (deferred) | Issue #380; B-034; ADR-007; current `frameworks/` placeholder | Defer until the first reusable framework emerges and the repo must decide whether it belongs to Hub capability or spoke/product material. | Creative |

---

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
| **B-085** | Исследование retrieval-стратегий для AI-агентов | **P2** | - | review | [#418](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/418) | Issue #418 (постановка фаундера, гипотезы H1–H7); глобальный анализ v0.4 §15.1.4, §15.1.6, §15.2.5 (RFC-F) | Научно-теоретическое исследование retrieval-стратегий реализовано как модуль [`research/ai-education/retrieval/`](../research/ai-education/retrieval/) из шести файлов и [RFC Reference Research Pattern](../docs/rfc/2026-07-17-rfc-reference-research-pattern.md) со статусом паттерна `Experimental`. Модуль включает research questions, Conceptual Framing и формальную сигнатуру `S = Decision(KB, Query, Constraints)`, объектную модель, граф зависимостей, 9 точек решений, 20 гипотез с ранжированием; таксономии БЗ/запросов/стратегий, матрицу «БЗ × Запрос → Стратегия», chunking/embeddings/reranking/evaluation, уровни готовности БЗ L0–L5; индустриальные кейсы, тренды 2024–2026, связь с памятью агента и вход для RFC-F. Исходный монолит помечен `superseded` и результатом B-085 больше не является. | Creative |
| **B-086** | Валидация шкалы готовности БЗ L0–L5 на реальных корпусах | **P3** | B-085 | TODO | - (planned) | Исследование B-085, §26.2 (признанная слабость: пороги не измерены) | Проверить шкалу L0–L5 на ≥3 реальных корпусах: воспроизводимы ли шесть признаков без построения индекса, различают ли пороги (95%/80%) уровни на практике, предсказывает ли уровень применимость стратегий. Условие перевода B-085 в `reviewed`. | Structured |
| **B-087** | Исследование самоотравления памяти агента | **P3** | B-085 | TODO | - (planned) | Исследование B-085, §19.2 (открытый вопрос О5) | Когда агент пишет в тот же корпус, из которого читает, возникает класс дефекта, не ловимый ни одной метрикой оценки RAG: faithfulness к самозаписанному контексту высока. Исследовать механизмы разделения пространств «знание человека» / «знание агента» и их различения при извлечении. | Creative |

---

## Спринт 10: Эволюция методологии инженерных исследований

**Story.**
Глубокое ревью исследования Retrieval выявило, что создаваемая структура выходит
за рамки шаблона для AI-доменов. Формируется гипотеза о минимальной архитектуре
инженерного знания, применимой к любым сложным дисциплинам. Чтобы избежать
преждевременной стандартизации, необходимо явно зафиксировать модель зрелости
артефактов, разделить методологию исследования и предметной области, а также
спланировать проверку универсальности паттерна.

**Цель.**
Зафиксировать модель зрелости исследовательских артефактов (Reference Pattern),
внедрить терминологию «Conceptual Framing» и определить дорожную карту валидации
этой методологии за пределами AI.

**Критерий закрытия.**
Модель зрелости задокументирована, разделение методологий явно прописано в
governance-нормах, а план валидации на не-AI доменах добавлен в бэклог как
triggered-задача.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-092** | Исследование промышленных практик агентного исполнения задач | **P1** | B-089 | review | [#457](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/457) | Issue #457 (постановка фаундера, гипотеза о мандате) | Вторая валидация Reference Research Pattern — на домене agentic task execution. Модуль [`research/ai-education/task-processing/`](../research/ai-education/task-processing/00-introduction.md) из шести файлов: сигнатура `A = Policy(M, S, T, C)`, объектная модель E1–E12, точки решений D1–D10, гипотезы H1–H16; таксономии мандатов M0–M5, подходов к планированию P0–P7 и механизмов контроля G1–G7; матрица «мандат × цена ошибки», правило размещения guardrail по обратимости, шкала автономии A0–A5; индустриальная практика (LangChain, OpenAI Agents SDK, MCP, CrewAI, AutoGen, OTel GenAI, MAST) и описательный разбор прецедентов #454/#456. Без внедрения правил и без RFC — по ограничениям постановки. | Creative |
| **B-093** | RFC по архитектуре постановки задач для AI-агентов | **P2** | B-092 | review | [PR #470](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/470) | Issue #457 (явное вынесение RFC в отдельную задачу) | На фактической базе B-092 подготовлен [RFC об архитектуре постановки задач для AI-агентов](../docs/rfc/2026-08-06-rfc-task-statement-architecture.md). Следствия RFC остаются в статусе `experimental` до проспективного замера эффекта (B-095). | Creative |

## Спринт 13: Развёртывание контрактов бутстрапа в целевом репо

**Story.**
Исходная постановка спринта — ввести корневой `AGENTS.md` как единый диспетчер правил для
всех моделей — **исполнена в части Хаба**: корневой [`AGENTS.md`](../AGENTS.md) размещён и
легализован (`B-110`). Оставшийся контур — доставка контрактов в спицы — переопределён
решением владельца ([issue #583](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583)):
целевой репозиторий доставки — `mango-ba-ai-runtime`, а `mango_ba_prompts` объявлен
`legacy/archived`, поэтому задачи, чьим предметом было изменение старого репо (`B-112`),
закрываются как `CANCELLED`, а не переносятся.

Остаточная часть спринта — нормативная работа Хаба (стандарты постановки, машинные гейты,
ось «Среда»), которая не зависит от выбора целевого репо и остаётся активной: без неё
разворачивать в новом репо нечего.

**Цель.**
Развернуть проектный `AGENTS.md` и базовые контракты в `mango-ba-ai-runtime` на основе шаблона
[`templates/htom/`](../templates/htom/README.md) и достроить нормативную часть Хаба
(уровни постановки, машинные гейты, ось «Среда»), от которой это развёртывание зависит.

**Критерий закрытия** (пересмотрен по решению владельца, Q-3 issue #727).
Спринт закрывается по части Хаба: дом контракта, правила уровней постановки и шаблоны
задач зафиксированы нормой Хаба и генома; машинные гейты запретов и постановки работают
в CI, а не держатся на доверии к агенту; решение о provenance ИИ-участия принято ADR.
Доставка в спицы (`mango-ba-ai-runtime`, `aether-orbis`) в критерий не входит: она идёт
шагами 2 и 4 [RFC #715](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md)
(B-239, B-241, B-251…B-253). Пункты, адресованные `mango_ba_prompts`, закрыты как
`CANCELLED` по статусу `legacy/archived`.

**Исполнение по issue #727 (2026-11-04).** Нормативная часть Хаба — B-169, B-114,
B-115, B-116 и B-154 — исполнена в [PR #728](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/728) и переведена в `DONE`:
PR смёржен 2026-11-05, merge-коммит `7d11a7e`. Строки меняют только файлы Хаба и не затрагивают `mango_ba_prompts`,
`mango-ba-ai-runtime` и `aether-orbis-gra` ([выбор и доказательства](../docs/analysis/2026-11-04-sprint-13-hub-normative-debt-selection.md)).
Решения владельца по Q-1…Q-6 приняты по рекомендациям (комментарий к PR #728):
исполнение — точечное исключение из порядка RFC #715 (Q-1), записанное в каждой строке;
B-111 и B-113 закрыты как `CANCELLED` — поглощены B-239, B-241, B-253 (Q-3); критерий
закрытия спринта пересмотрен (Q-3). Вне выбора остаются B-117 и B-120 (ждут схемы
профиля B-236, B-238) и B-121. Дубликат B-121 ушёл в бэклог спицы при B-247.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-111** | Скрипт `tools/inject-agents-md.sh` для управляемой доставки в спицы | **P1** | B-110, B-060 | CANCELLED | [#547](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/547), [#727](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/727) / [PR #728](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/728) | Вывод В6 [исследования практик](../research/hub/2026-09-03-ai-agent-onboarding-entrypoint-practices.md): Copilot и Cursor читают только файлы внутри самого репозитория; [правила синхронизации](../projects-sink/agents-md/synchronization-rules.md) | Реализовать идемпотентный скрипт, который **не копирует файл вслепую**, а применяет классификацию general/archetype/environment/project layers из `projects-sink/agents-md/`. Скрипт читает `.hub-profile.json`, выбирает template архетипа, включает только объявленные среды, сохраняет project delta и записывает проверяемый `derived_from` с точным upstream SHA в согласованной схеме profile/manifest. Требования: dry-run по умолчанию, посекционный отчёт `add/update/keep/remove-duplicate/conflict`, отказ при локальных правках без флага, вызов из CI/по расписанию, запись в `CHANGELOG` спицы. Обязателен парный check-режим, падающий при отсутствии/дрейфе `AGENTS.md`, рассогласовании profile со `<scope>`, дублях правил в adapters и нарушении изоляции EP-C1. **Переопределено по issue #583:** целевой список — `mango-ba-ai-runtime` (обязательно) и `aether-orbis`; `mango_ba_prompts` исключён как `legacy/archived`. **Отменено по issue #727 (Q-3, решение владельца):** идемпотентная доставка с закреплением upstream SHA, dry-run и check-режимом поглощена каноническим инструментом синка B-239 (Ш2.4) и CI-проверкой дрейфа B-241 (Ш2.6) [RFC #715](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md); отдельный `tools/inject-agents-md.sh` не создаётся. | Structured |
| **B-112** | Mango: устранить `docs/contracts/` и задать канонический дом контрактных документов | **P1** | B-110 | CANCELLED | [#547](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/547) | Находка F2 [анализа](../docs/analysis/2026-09-03-ai-rules-compliance-failure-root-cause.md): [`docs/contracts/kb-citations.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/contracts/kb-citations.md) | Двухчастная задача. В Хабе: дополнить [`standards/contract-documentation-standard.md`](../standards/contract-documentation-standard.md) и [`ops/repo-model.md`](repo-model.md) явным домом для документов класса «контракт» — текущий стандарт описывает форму, но не отвечает на вопрос «где он живёт», что и породило сбой. В Mango: перенести содержимое `docs/contracts/` в каноничный дом (`ai-rules/`), удалить каталог, убрать запрещённое поле `ai-generated` из frontmatter, обновить ссылки. Задача не считается закрытой, пока запрет на `docs/contracts/` не проверяется машинно (см. B-116). **Уточнение по находке F7:** путь `docs/contracts/kb-citations.md` был предписан дословно в разделе «Готово, когда» задачи [mango#353](https://github.com/G-Ivan-A/mango_ba_prompts/issues/353), а не выбран агентом, — поэтому одного запрета недостаточно: при переносе обязательно закрыть и канал постановки (B-116, пункт 2), иначе исполнитель получит конфликт «правило против DoD». **Отменено по issue #583:** предмет задачи — каталог `docs/contracts/` в `mango_ba_prompts`, который объявлен `legacy/archived` и изменению не подлежит. Часть, относящаяся к Хабу (явный дом документов класса «контракт» в `standards/contract-documentation-standard.md` и `ops/repo-model.md`), перенесена в `B-169`; машинный запрет остаётся за `B-116` и действует для новых репозиториев. | Structured |
| **B-113** | Aether-Orbis: приведение репозитория в соответствие с геномом | **P1** | B-110, B-111 | CANCELLED | [#547](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/547), [#727](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/727) / [PR #728](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/728) | Находка F3 [анализа](../docs/analysis/2026-09-03-ai-rules-compliance-failure-root-cause.md): в репозитории отсутствует `.github/ISSUE_TEMPLATE` | Разложить в [aether-orbis](https://github.com/G-Ivan-A/aether-orbis) базовый геном: `.github/ISSUE_TEMPLATE/task.md` и `task.yml` из Хаба, `AGENTS.md`, `CONTRIBUTING.md`, минимальный набор валидаторов из [`templates/spoke/`](../templates/spoke/README.md). Провести ревизию существующих issues и зафиксировать, какие из них требуют переоформления по пяти уровням постановки, а какие закрываются как есть. Требование соблюдать шаблон вступает в силу только после его фактической доставки в репозиторий. **Дополнительно (находка F8, ревью PR [#548](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/548)): провести аудит корневых файлов `aether-orbis`. Выявить и устранить дубликаты или запрещённые файлы (например, [`PRODUCT_VISION.md`](https://github.com/G-Ivan-A/aether-orbis/blob/main/PRODUCT_VISION.md), [`GOVERNANCE.md`](https://github.com/G-Ivan-A/aether-orbis/blob/main/GOVERNANCE.md)). Перенести их содержимое в каноничные дома (`docs/vision.md`, `ai-governance/`) и удалить из корня. Обновить все абсолютные ссылки.** Дублирование SSOT подтверждено фактически: [`docs/vision.md`](https://github.com/G-Ivan-A/aether-orbis/blob/main/docs/vision.md) уже существует одновременно с корневым `PRODUCT_VISION.md`. Перенос выполнять с журналированием каждого перемещения (`path_migrations` в `.hub-profile.json`) и с явным указателем на старом месте там, где на файл есть внешние ссылки, — по образцу Mango (F7.5); молчаливое удаление запрещено. **Отменено по issue #727 (Q-3, решение владельца):** приведение `aether-orbis` к геному поглощено B-253 (шаг 4 RFC #715) на инструменте синка B-239 и проверке дрейфа B-241; аудит корневых файлов (F8) и журналирование переносов через `path_migrations` переходят в B-253 вместе с предметом. | Structured |
| **B-117** | Стандарт бутстрапа: ось «Среда» и контракт классов `ai-rules/` | **P1** | — | TODO | [#553](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/553) | [RFC оси «Среда» и рефакторинга базовых структур](../docs/rfc/2026-09-04-rfc-bootstrap-environment-and-structure.md) (issue #553); decision record — [ADR-012 «Корневой `AGENTS.md` как обязательный артефакт бутстрапа»](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-012-agents-md-root-contract.md) (issue #559) | Создать `standards/bootstrap-environment-standard.md` по разделам `P.1`–`P.5` RFC: словарь сред (`local`, `gigacode`, `serverless`), формула композиции `ядро ⊕ Δархетип ⊕ Δсреда ⊕ Δпродукт`, правила `R1`–`R7` (аддитивность, разделение предметов, приоритет при конфликте, адаптер вместо второго SSOT, одна первичная среда, дефолт `local`, закрытый словарь), поля `archetype`/`environment`/`secondary_environments` в `.hub-profile.json`, контракт трёх классов `ai-rules/` (правило — плоско, команда — `commands/<slug>.md`, навык — `skills/<slug>/SKILL.md`) с различающим тестом «кто инициирует применение». Подкаталоги `commands/`/`skills/` объявляются разрешёнными, но физически в Хабе не создаются до появления не менее двух артефактов класса. Решения фаундера по `Q-1`, `Q-2`, `Q-3` получены (issue #555): ось принимается вместе с правилом аддитивности `R1`, `ai-rules/` сохраняется, дельта `gigacode` до результата B-121 строится по `R4`. **Дополнительно по решениям `Q-6` и `Q-7` (раздел `P.9` RFC):** стандарт фиксирует создание заглушек `ai-rules/commands/` и `ai-rules/skills/` (`README.md`, `status: placeholder`) при бутстрапе нового репозитория под целевую среду — с явной границей «заглушка только в момент бутстрапа как часть шаблона; пустой каталог отдельным PR в существующем репозитории запрещён», — и правило `R8` «декларация вместо запрета»: каталог вне канонического набора легализуется декларацией в `project_specific_directories` с обязательным непустым `reason`, поимённые denylist-ы имён каталогов (в том числе для `plans/` и `tasks/`) запрещены ([ADR-012 «Корневой `AGENTS.md` как обязательный артефакт бутстрапа»](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-012-agents-md-root-contract.md), issue #559). Синхронизировать решения новыми ADR к ADR-001 и ADR-007 (шаг `M2` плана миграции), не переписывая принятые ADR. | Structured |
| **B-120** | Валидаторы и `AGENTS.md`, чувствительные к объявленной среде | **P1** | B-117 | TODO | [#553](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/553) | [RFC оси «Среда» и рефакторинга базовых структур](../docs/rfc/2026-09-04-rfc-bootstrap-environment-and-structure.md) (issue #553), разделы `P.7`, `M5`, `M6` | Двухчастная задача. Валидаторы: [`tools/validate-repository-structure.sh`](../tools/validate-repository-structure.sh) и геном [`templates/htom/tools/validate-repository-structure.sh`](../templates/htom/tools/validate-repository-structure.sh) читают `environment` из `.hub-profile.json` **до** проверки требуемого набора; каталог, канонический для объявленной среды, проходит без записи в `project_specific_directories`; значение вне словаря и вычитающая дельта дают `FAIL`; декларация каталога через `project_specific_directories` с пустым или отсутствующим `reason` даёт `FAIL`, а поимённый denylist имён каталогов в валидаторах отсутствует (правило `V-10`, раздел `P.9.2` RFC в редакции issue #559); [`tools/sync-from-hub.sh`](../tools/sync-from-hub.sh) учитывает среду при раскладке, а ручная правка сгенерированного адаптера падает в check-режиме. `AGENTS.md`: правки `A-1`–`A-5` и `A-6`–`A-9` (пороги объёма в токенах 4K/8K, запуск навыка, машинные и контрактные гейты, правило `R8`) в [RFC корневого контракта](../docs/rfc/2026-09-03-rfc-agents-md-root-contract.md) (`v1.0`, `accepted`) и в [`templates/agents-md-root-draft.md`](../templates/agents-md-root-draft.md) (`v0.2`) **внесены по решению `Q-5`** в рамках issue #555; в задаче остаётся только реализация валидаторов и перенос правок в корневой `AGENTS.md` при его размещении (B-110). **Приоритет P1 из-за `A-1`:** действующая формулировка `<forbidden>` «модель-специфичные файлы правил запрещены» буквально запрещает нативную поверхность среды GigaCode и тем самым блокирует Трек А; запрет должен быть сужен до копии правил с разрешением сгенерированного указателя. B-111 дополняется требованием чувствительности скрипта инъекции к среде. | Structured |
| **B-121** | Исследование механизма обнаружения навыков в GigaCode | **P1** | — | TODO | [#555](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/555) | Решение фаундера по `Q-2` [RFC оси «Среда» и рефакторинга базовых структур](../docs/rfc/2026-09-04-rfc-bootstrap-environment-and-structure.md) (issue #555) | Установить по документации среды GigaCode фактический механизм discovery навыков: путь реестра конфигурируется или жёстко задан средой, формат записи, есть ли автозагрузка. Результат — исследование по [стандарту research](../standards/research-standard.md) со ссылками на первоисточники документации среды; утверждения без проверяемого источника не публикуются. Выход исследования закрывает условность дельты `gigacode` в разделе `P.2` RFC и определяет, достаточно ли каталога `ai-rules/skills/` или обязателен сгенерированный адаптер на нативном пути. До получения данных действует правило `R4` (адаптер, а не второй SSOT), поэтому задача не блокирует Трек А, а снимает с него неопределённость. | Structured |

## Спринты 14–21, 24–28: Перенесены в ba-ai-metamodel

Тринадцать разделов проекта метамодели БА (100 строк, ID без перенумерации)
перенесены дословно этапом E5 ([PR #6](https://github.com/G-Ivan-A/ba-ai-metamodel/pull/6)) и подтверждены E6
([PR #7](https://github.com/G-Ivan-A/ba-ai-metamodel/pull/7)) — [бэклог спицы на `e1f67e2`](https://github.com/G-Ivan-A/ba-ai-metamodel/blob/e1f67e267beb73809e1edb26313691a5c769c92a/ops/backlog.md).
Исполнение, статусы и новые задачи проекта ведутся только там. Строки Хаба,
которые зависят от этих ID (B-068 и B-070 — от B-173), ссылаются на те же ID
в бэклоге спицы. Шаги выноса на стороне Хаба — Спринт 30 (B-248…B-250).

---

## Отложенные задачи с триггером

Задачи этого блока не запускаются по факту регистрации. Они переходят в работу
только после появления указанной операционной боли, чтобы соблюдать принцип
Anti-Inflation.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-088** | Зафиксировать многоуровневую иерархию SSOT (ADR vs Стандарт) | **P3** | - | deferred (triggered) | - (tech debt) | Обсуждение 2026-07-16; B-050 v0.2 §2; [issue #427](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/427) | Текущая формулировка «ADR имеет приоритет» слишком общая. Необходимо чётко разграничить компетенции: ADR = SSOT для решений, Стандарт = SSOT для исполнения. Задача стартует **только** при появлении боли: повторяющиеся конфликты между свежим ADR и устоявшейся практикой в стандарте. | Creative |
| **B-091** | Проверить Reference Pattern на не-AI доменах | **P2** | B-089, B-090 | deferred (triggered) | - (deferred) | Ревью Retrieval и методологическое обсуждение 2026-07-16 | Проверить гипотезу Reference Pattern за пределами AI на Business Analysis, Requirements Engineering и Prompt Engineering. Запускать только после успешной валидации на Memory и Agents. | Creative |
| **B-094** | Knowledge Integrity Auditor — агент периодического аудита целостности знаний | **P2** | - | deferred (regular) | [#475](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/475) | Согласование ОПС с фаундером (RFC [#470](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/470)) | Регулярная задача вне спринтов: автономный агент по расписанию сканирует исторические документы (RFC, ADR) на упоминания дефектов и проверяет, устранены ли они в замерженных PR; добавляет блок `Status Update` со ссылкой на закрывающий PR. Триггер автоматизации — явная боль от ручного аудита; до неё задача не автоматизируется. | Structured |
| **B-095** | Проспективный замер эффекта RFC #470 | **P2** | B-093 | deferred (regular) | [#475](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/475) | RFC [#470](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/470); [валидация стратегии постановки задач](../research/hub/2026-07-31-ops-task-strategy-validation.md); PR [#462](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/462) | Регулярная задача вне спринтов, запуск через 3 месяца после внедрения RFC #470: повторный прогон скриптов из `research/hub/exp/ops-task-strategy-461/` для измерения доли непродуктивных PR, `contract_score` и доли PR-с-вопросами. Основание для перевода следствий RFC в canonical или их корректировки. | Structured |
| **B-096** | Создание инструкции по меткам GitHub | **P3** | - | deferred (triggered) | [#475](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/475) | Согласование ОПС с фаундером; PR [#467](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/467) | Документировать допустимые метки (`no-diff-expected`, `needs-human-decision`, `incomplete-dod` и другие) как часть общей инструкции по Хабу, чтобы пользователи не забывали, какие метки можно использовать. Триггер — повторяющиеся ошибки в разметке issues/PR. | Structured |
| **B-097** | Автоматизация переноса неактивных PR-с-вопросами в `ops/backlog.md` | **P3** | B-096 | deferred (triggered) | [#475](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/475) | Согласование ОПС с фаундером; RFC [#470](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/470) | Скрипт, который по расписанию или триггеру находит PR с меткой `needs-human-decision` старше N дней, переносит описание вопроса в `backlog.md` и закрывает PR с комментарием. Запуск по запросу; не автоматизировать до явной боли от ручного разбора зависших PR. | Structured |
| **B-122** | RFC: замена `ops/backlog.md` внешним трекером через MCP | **P3** | B-119 | deferred (triggered) | [#555](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/555) | Решение фаундера по `Q-7` [RFC оси «Среда» и рефакторинга базовых структур](../docs/rfc/2026-09-04-rfc-bootstrap-environment-and-structure.md) (issue #555) | Отложенная задача: завести отдельный RFC на перенос планирования и учёта задач из markdown-бэклога во внешнюю систему планирования, подключаемую через MCP. Триггер запуска — операционная боль ведения `ops/backlog.md` вручную (расхождение бэклога с GitHub Issues, стоимость синхронизации), а не факт регистрации задачи. В scope RFC: границы SSOT состояния работ, судьба `backlog-instruction.md`, миграция истории, требования к MCP-подключению. Решение по `Q-7` о запрете собственных каталогов планирования (`plans/`, `tasks/`) от этого RFC не зависит и исполняется раньше — в B-117 и B-120 (см. `P.9.2` RFC). | Creative |
| **B-123** | Состав дельты среды комплексного развёртывания агента (`serverless`) | **P2** | B-117 | deferred (triggered) | [#555](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/555) | Решение фаундера по `Q-8`б [RFC оси «Среда» и рефакторинга базовых структур](../docs/rfc/2026-09-04-rfc-bootstrap-environment-and-structure.md) (issue #555), раздел `P.9.3` | Отложенная задача: определить состав дельты среды `serverless` (манифест развёртывания, контракт API чтения знаний) и утвердить её итоговое наименование из кандидатов `hosted-agent` (рекомендация), `vps-runtime`, `standalone-agent`. Триггер — принятие RFC Трека Б, выбирающего стек серверного агента `ai-ba-playbooks`: до выбора стека состав дельты определить нельзя, а зафиксированный преждевременно он будет переписан. Смена имени — правка закрытого словаря `R7`, поэтому исполняется тем же ADR, что легализует ось (шаг `M2`); до её принятия ни одна спица значение `serverless` в профиле не объявляет. | Structured |
| **B-068** | Правило «изменение библиотеки промптов по run-статистике» + порог N | **P2** | B-173 | deferred (triggered) | - (перенесено из Спринта 6 по issue #583) | Global analysis v0.4 §15.8.2/RFC-B; [`standards/evals-contract-standard.md`](../standards/evals-contract-standard.md) | Governance-правило: когда run-статистика (при минимальном N + человеческое ревью) даёт основание менять библиотеку навыков. **Перенесено в отложенные по issue #583:** правило нечем питать, пока нет ни одного прогона в `mango-ba-ai-runtime`. Триггер — накоплен корпус прогонов MVP (`B-173`), позволяющий назначить минимальное N фактом, а не оценкой. Приоритет понижен `P1 → P2`. | `null` |
| **B-070** | Наблюдаемость: нужен ли отдельный эпизодический слой (`runs/`) (закрывает R4) | **P2** | B-173 | deferred (triggered) | - (перенесено из Спринта 6 по issue #583) | Global analysis v0.4 §15.8.2/RFC-G; §11-A2/R4; ADR-007 | Открытый вопрос AgentOps: нужен ли журнал прогонов/трасс как эпизодическая память и где его дом. **Перенесено в отложенные по issue #583:** решение «не вводить до боли» (анализ 2026-07-04 + ADR-007) остаётся в силе; вопрос переадресован `mango-ba-ai-runtime`, потому что прогоны будут исполняться там, а не в Хабе. Триггер — первые прогоны MVP (`B-173`) породили потребность в трассе. | `null` |
| **B-317** | Калибровка мульти-LLM гейта на размеченном наборе | **P2** | - | deferred (triggered) | - (deferred) | [исследование #757](../research/hub/2026-11-28-digital-employee-methodology-survey.md), §5 и гипотеза H2 | Проверить гипотезу фаундера «мульти-LLM гейт быстрее и лучше проверки пользователем» до того, как она станет свойством продукта. На одном пилотном процессе с Golden Set (кандидат — процесс Mango с `G-mach`) измерить TPR/TNR каждого судьи, корреляцию их ошибок, пропуск дефектов и ложные отказы панели против одного судьи и против пользователя, долю эскалаций и время до решения; не меньше 97 размеченных дефектных примеров на судью. **Триггер:** решение фаундера пилотировать или продавать цифрового сотрудника с мульти-LLM гейтом. По итогам — решение о повышении исследования #757 с M3 до M2 или его отклонении. | Creative |

## Спринт 22: Проверка контрактов сотрудничества на реальных прогонах

**Story.** Issue #625 вводит правила режимов и сотрудничества. Текстовые проверки
подтверждают согласованность контрактов, но не показывают, как правила влияют
на поведение агента в работе. До появления реальных прогонов базовой линии нет.

**Цель.** На первых сопоставимых прогонах измерить качество результата и
стоимость координации по режимам, включая негативные кейсы и дрейф контекста.

**Критерий закрытия.** Корпус, критерии оценки и повторные прогоны позволяют
решить, какие правила сохранить, пересмотреть или удалить.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-195** | Проверить режимы и якоря сотрудничества на прогонах агентов | **P3** | - | deferred (triggered) | - (deferred) | [RFC #625](../docs/rfc/2026-09-27-rfc-agent-collaboration-and-operating-modes.md), S-16…S-19 | После появления сопоставимых реальных прогонов собрать трассы, негативные кейсы, оценку результата человеком и затраты токенов; сравнить режимы и проверить пороги M-1…M-4. До этого изменения основаны только на анализе контрактов. | Creative |

---

## Спринт 30: Детерминированное управление спицами и вынос проекта метамодели БА

**Story.** RFC [#715](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md)
принят решением владельца в issue
[#717](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/717). Хаб
несёт жизненный цикл другого продукта (2/3 бэклога и 36% шагов CI), а спицы
синхронизируются тремя несовместимыми способами с плавающего `main`. Решение —
семь шагов: контракт наследования (шаг 2), вынос проекта метамодели БА (шаг 3),
согласованное чтение спиц (шаг 4), инвентаризация устаревшего (шаг 5), чистка
Хаба (шаг 6) и закрытие техдолга (шаг 7). Вынос проекта метамодели идёт по
[контракту выноса](hub-project-extraction-contract.md), который локально
применяет I-2, I-3 и I-4. Анализ и доказательства шага 1 —
[анализ шага 1](../docs/analysis/2026-11-03-ba-meta-model-extraction-step1.md).

**Вынос отложен** [решением владельца 2026-11-04](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/718#issuecomment-6625672558): заморозить источники
нельзя, пока работа над `mango_ba_prompts` и связанными репозиториями идёт и
меняет источник БА в Хабе. Репозиторий `ba-ai-metamodel` создан и остаётся с
одним `README.md`; контракт, инструмент, параметры, репетиция и базовый снимок
дрейфа сохранены в Хабе. Ш3.0–Ш3.7 (B-243…B-250) ждут триггера B-243;
возобновление начинается со сверки с базовым снимком. Пока вынос отложен,
порядок RFC действует без исключения: шаг 2 идёт первым. Обоснование, риски и
возможности — [анализ шага 1, «Отложенный вынос»](../docs/analysis/2026-11-03-ba-meta-model-extraction-step1.md).

**Вынос возобновлён** решением владельца в issue [#738](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/738) (2026-11-16): работа над
`mango_ba_prompts` и связанными репозиториями поставлена на паузу на два дня —
это окно заморозки. B-243 исполнена: источники закреплены на `HUB_SHA`
`54face1` и заморожены шагом CI Хаба `tools/check-extraction-freeze.sh` до
надгробия B-249; задача выноса — [ba-ai-metamodel#1](https://github.com/G-Ivan-A/ba-ai-metamodel/issues/1). Триггеры B-244…B-250 сработали, порядок
задают зависимости. Анализ старта —
[анализ #738](../docs/analysis/2026-11-16-hub-optimization-start.md).

**Этапы E1–E6 приняты** 2026-11-17: PR #2–#7 слиты в `ba-ai-metamodel`, CI
спицы зелёный на `e1f67e2`. Заморозка источников держалась до последнего
коммита `main` Хаба перед надгробием (`54face1..24cd7ff` без изменений).
Надгробие B-249 ([PR #745](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/745)) удалило источники и BA-разделы бэклога, сняло
шаг заморозки. B-248 перевела runtime на спицу в [runtime PR #24](https://github.com/G-Ivan-A/mango-ba-ai-runtime/pull/24).
B-249 — `DONE`: надгробие принято, релиз закреплённых ссылок в спице
закрыл [mango_ba_prompts#488](https://github.com/G-Ivan-A/mango_ba_prompts/issues/488)
([PR #496](https://github.com/G-Ivan-A/mango_ba_prompts/pull/496)).

**Шаг 3 закрыт.** B-250 — `DONE` по
[решению владельца в PR #748](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/748#issuecomment-7046732697).
CI Хаба без BA и CI спицы прошли. Проверка на новом `source_commit`
`657abccc171d1ad6d860bbc262b5cc56aa5e99e0` показала совпадение 324 из 324
файлов источника и 0 из 5 сгенерированных контрактов с пакетом runtime PR #24.
Во всех пяти закреплённых схемах обязательно поле `product_attribution`,
которого нет в опубликованных контрактах. Проверка со стороны Хаба завершена,
расхождение зафиксировано, пересборка делегирована репозиториям
`mango-ba-ai-runtime` и `mango_ba_prompts`. B-249 и B-250 архивированы,
[результаты замера](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/748#замер-b-250)
и след закрытия сохранены в [CHANGELOG](../CHANGELOG.md#changed).

**Цель.** Хаб освобождается от бэклога и CI метамодели БА. При создании
`governed`-спица наследует структуру архетипа с закреплённого SHA Хаба.
Дальнейший синк каноническим инструментом и проверка закреплённого генома
доступны по запросу команды спицы.

**Критерий закрытия.** Задачи Ш1–Ш6 имеют статус `DONE` или `CANCELLED`, шаг 7
поставлен строками по итогам Ш6.4. Ш3.7 принят по решению владельца после
успешного CI Хаба без BA и CI спицы и фиксации результатов сверки runtime.

Предшествующая задача B-234 завершена в
[#717](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/717) и [PR #718](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/718).
Принятие ADR-024 завершает B-236. Схема профиля B-238 закрыта, на ней работают
канонический синк B-239 и будущая процедура создания спицы B-307.
B-237, B-240 и B-242 могут идти параллельно, B-241 следует за B-239.
Закрытие B-250 выполняет предусловие инвентаризации B-255…B-257.
Приоритеты задач указаны как `null` до Ш6.4.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-236** | Ш2.1: ADR «Контракт наследования экосистемы» (I-1…I-8) | null | B-234 | DONE | [#749](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/749) / [PR #751](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/751) | [RFC #715, шаг 2](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) / [ADR-024](../docs/adr/2026-11-adr-024-ecosystem-inheritance-contract.md) | Владелец принял ADR-024 [22 ноября 2026 года](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/751#issuecomment-7077648276). ADR фиксирует I-1…I-8, проверки для B-237…B-242 и переход от E1 к каноническому синку. | Hybrid |
| **B-237** | Ш2.2: единый реестр экосистемы (I-1) | null | B-234, B-236 | ЧАСТИЧНО | [#717](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/717) | [RFC #715, Q-4](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) | Сделано в #717: реестр — [`docs/ecosystem-map.md`](../docs/ecosystem-map.md) с классами I-1, таблица статусов бэклога заменена ссылкой. Осталось: машиночитаемая форма реестра для инструмента синка по ADR B-236. Ссылка на `ba-ai-metamodel` уже в реестре. | null |
| **B-238** | Ш2.3: схема профиля, её валидатор и шаблоны `templates/*/.hub-profile.json` (I-2, I-6) | null | B-236 | DONE | [#752](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/752) / [PR #753](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/753) | [RFC #715, шаг 2](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) / [ADR-024](../docs/adr/2026-11-adr-024-ecosystem-inheritance-contract.md) | [Схема и валидатор](../CONTRIBUTING.md#профиль-наследования-хаба) проверяют `last_sync` и `deviations[]`. CI проверяет оба шаблона и исходные снимки E1, GRA и Mango. | Hybrid |
| **B-239** | Ш2.4: канонический инструмент синка с закреплением (I-3, I-4) | null | B-238 | DONE | [#754](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/754) / [PR #755](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/755) | [RFC #715, шаг 2](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) / [ADR-024](../docs/adr/2026-11-adr-024-ecosystem-inheritance-contract.md) | [`tools/hub-sync.py`](../CONTRIBUTING.md#синхронизация-спицы-с-хабом) применяет геном `tools/hub-genome.json` только с SHA или тега Хаба и пишет `last_sync` после проверки схемой B-238. Локальные скрипты спиц — обёртки вида `tools/hub-sync-wrapper.sh`. Карта архетипа B совпадает с E1, поэтому спица после E1 переходит на синк без изменения файлов. Вместе с B-241 поглощает B-111. | Hybrid |
| **B-240** | Ш2.5: исправить геном (I-7: H-1, H-3) | null | B-236, B-239 | DONE | [#756](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/756) / [PR #759](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/759) | [RFC #715, шаг 2](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) / [Разбор B-240](../docs/analysis/2026-11-28-genome-defects-b240.md) | Геном B и D закрепляет ссылки на SHA и поставляет `ops/`. Полные HTOM-контракты живут в `ai-rules/` и `ai-governance/`, прежние корневые имена ведут к ним через указатели. Исторический E1 переходит на канонический синк с сохранением проектных файлов. B-240 завершает предпосылки B-307. | Creative |
| **B-241** | Ш2.6: шаблон CI-проверки дрейфа для спиц (I-5) | null | B-239 | TODO | - (planned) | [RFC #715, шаг 2](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) | Спица запускает валидаторы генома на закреплённом SHA; отставание от текущего Хаба — предупреждение, не блокировка. | null |
| **B-242** | Ш2.7: шаблон issue обратного сбора практик (I-8) | null | B-236 | TODO | - (planned) | [RFC #715, шаг 2](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) | Сбор практики из спицы — только по запуску пользователя, с конкретным SHA спицы; автоотправки нет (ADR-017). | null |
| **B-251** | Ш4.1: `mango_ba_prompts` — находки M-1…M-8 ре-синком на закреплённом SHA | null | B-239, B-240 | TODO | - (planned) | [Анализ #713](../docs/analysis/2026-11-02-mango-ba-prompts-hub-practice-transfer-check.md); [RFC #715, Q-3](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) | Класс `governed` (Q-3): референсная реализация универсальной модели; 6 FAIL генома. Запрет #583 на задачи, меняющие этот репозиторий, снят. Геном HTOM исправлен в PR #724 (B-197: Hybrid по умолчанию): ре-синк доставит в спицу `AI_SESSION_HANDOVER_PROMPT.md` 0.10, `AI_GOVERNANCE.md` 0.6 и `task.md` 2.2. | null |
| **B-252** | Ш4.2: `aether-orbis-gra` — A-1, A-2, A-3, A-5 и `last_sync` по схеме I-2 | null | B-239, B-240 | TODO | - (planned) | [Анализ #713](../docs/analysis/2026-11-02-aether-orbis-gra-hub-practice-transfer-check.md) | Корневые `AI_*.md` уходят одним ре-синком после исправления генома; A-4 исключена решением владельца. Геном HTOM исправлен в PR #724 (B-197: Hybrid по умолчанию): ре-синк доставит в спицу `AI_SESSION_HANDOVER_PROMPT.md` 0.10, `AI_GOVERNANCE.md` 0.6 и `task.md` 2.2. | null |
| **B-253** | Ш4.3: `aether-orbis` — бутстрап `AGENTS.md` и профиля | null | B-239 | TODO | - (planned) | [RFC #715, Ш4.3](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) | Поглощает B-113. | null |
| **B-254** | Ш4.4: матрица согласованного чтения по реестру | null | B-237, B-251, B-252, B-253 | TODO | - (planned) | [RFC #715, Ш4.4](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) | Прогон `spoke-consistency-matrix.py` по `governed`-репозиториям реестра и запись результата в реестр; запуск по инициативе пользователя. | null |
| **B-255** | Ш5.1: инвентаризация содержания | null | B-250 | TODO | - (planned) | [RFC #715, Ш5.1](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) | 207 документов в открытом статусе без обновления с 2026-09-01 за вычетом вынесенных; `docs/project-summaries/`, `research/open-ai-ru/` (`dormant`, не архивируется как остановленный), `projects/education-ba-prompt/`. | null |
| **B-256** | Ш5.2: инвентаризация норм | null | B-250 | TODO | - (planned) | [RFC #715, Ш5.2](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) | 17 legacy RFC без даты, 7 ADR в `proposed`, 10 стандартов и 11 руководств в `draft`. | null |
| **B-257** | Ш5.3: инвентаризация инструментов и связей | null | B-250 | TODO | - (planned) | [RFC #715, Ш5.3](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) | Тесты одноразовых контрактов, неподключённый `test-ba-requirements-forensics.sh`, пути валидатора, ссылки на ветки `issue-*` и на `mango-ba-ai-runtime-cli`. | null |
| **B-258** | Ш6.1: архивация и депрекация по Ш5.1–Ш5.2 | null | B-255, B-256 | TODO | - (planned) | [RFC #715, Ш6.1](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) | Статус, навигация, входящие ссылки, CHANGELOG; физическое удаление — только с мандатом владельца. | null |
| **B-259** | Ш6.2: валидаторы — правила дома вместо явных путей | null | B-257 | TODO | - (planned) | [RFC #715, Ш6.2](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) | Около 800 явных путей `validate-repository-structure.sh` → правила «каталог + шаблон имени»; удалить устаревшие тесты; свернуть 22 шага самопроверок курса в один цикл. | null |
| **B-261** | Ш6.4: переприоритизация бэклога Хаба | null | B-260 | TODO | - (planned) | [RFC #715, Ш6.4](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md); [RFC закрытия спринтов](../docs/rfc/2026-09-28-rfc-backlog-sprint-closure.md) | Обосновать приоритеты оставшихся спринтов Хаба, включая задачи Спринта 30 с приоритетом `null`. | null |
| **B-262** | Ш6.5: индексы и навигация | null | B-258, B-259, B-261 | TODO | - (planned) | [RFC #715, Ш6.5](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) | `docs/rfc/README.md`, `docs/adr/README.md`, `ops/artifact-map.md`, `CHANGELOG.md` совпадают с деревом. | null |
| **B-263** | Шаг 7: закрытие техдолга бэклога Хаба | null | B-261 | deferred (triggered) | - (deferred) | [RFC #715, шаг 7](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) | Триггер — закрытие B-261. До 18 готовых строк Хаба (B-111 и B-113 поглощены B-239, B-241 и B-253) исполняются по новым приоритетам; 11 строк с триггером остаются `deferred`. | null |
| **B-264** | Версионированный crosswalk «операция/навык метамодели ↔ класс практики» | null | B-247 | CANCELLED | [#744](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/744) / [PR #746](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/746) | [Анализ шага 1, «Состав как база масштабирования»](../docs/analysis/2026-11-03-ba-meta-model-extraction-step1.md) | В новом репозитории: соответствие 31 операции и 33 навыков метамодели 39 классам `mango_ba_prompts` с тремя ID, one-to-many и диапазоном совместимых версий модели. Без него модель нельзя модернизировать, не трогая практики. **Отменена без исполнения** ([решение владельца в PR #746](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/746#issuecomment-6977571960)): задача потеряла актуальность для Хаба — по правилу шага 7 [RFC #715](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) строки метамодели после Ш3.4 принадлежат спице [`ba-ai-metamodel`](https://github.com/G-Ivan-A/ba-ai-metamodel); условие владельца: «задачи, потерявшие актуальность, завершить без исполнения». Подробно — [аудит #744](../docs/analysis/2026-11-17-backlog-audit-after-extractions.md). | null |
| **B-265** | ADR об осях версий метамодели | null | B-247 | CANCELLED | [#744](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/744) / [PR #746](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/746) | [Анализ шага 1, «Состав как база масштабирования»](../docs/analysis/2026-11-03-ba-meta-model-extraction-step1.md) | В новом репозитории: версия модели, версия crosswalk, версия дистрибутива и `source_commit` runtime меняются независимо. **Отменена без исполнения** ([решение владельца в PR #746](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/746#issuecomment-6977571960)): задача потеряла актуальность для Хаба — по правилу шага 7 [RFC #715](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) строки метамодели после Ш3.4 принадлежат спице [`ba-ai-metamodel`](https://github.com/G-Ivan-A/ba-ai-metamodel); условие владельца: «задачи, потерявшие актуальность, завершить без исполнения». Подробно — [аудит #744](../docs/analysis/2026-11-17-backlog-audit-after-extractions.md). | Hybrid |
| **B-266** | Общий фреймворк оценки (eval) метамодели | null | B-264 | CANCELLED | [#744](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/744) / [PR #746](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/746) | [Анализ шага 1, «Состав как база масштабирования»](../docs/analysis/2026-11-03-ba-meta-model-extraction-step1.md) | Триггер — второй проект-потребитель метамодели. Сейчас есть оценка одного MVP-среза (Golden Set, `G-mach`, `M-1`…`M-5`); обобщение с одного потребителя закрепит его частности. **Отменена без исполнения** ([решение владельца в PR #746](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/746#issuecomment-6977571960)): задача потеряла актуальность для Хаба — по правилу шага 7 [RFC #715](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) строки метамодели после Ш3.4 принадлежат спице [`ba-ai-metamodel`](https://github.com/G-Ivan-A/ba-ai-metamodel); условие владельца: «задачи, потерявшие актуальность, завершить без исполнения». Подробно — [аудит #744](../docs/analysis/2026-11-17-backlog-audit-after-extractions.md). | null |
| **B-267** | Уточнить ADR-014 после решения Q-3 | null | B-234 | TODO | - (planned) | [ADR-014](../docs/adr/2026-09-adr-014-legacy-evidence-not-baseline.md); [RFC #715, Q-3](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md) | `mango_ba_prompts` больше не `legacy/archived`: отделить его исторические прогоны и промпты (свидетельство по `LG-1`…`LG-6`) от действующей референсной реализации (39 классов) и снять формулировки, которые объявляют весь репозиторий наследием. | Hybrid |
| **B-307** | Процедура рождения новой спицы и проверка Хаба по реестру | null | B-236, B-238, B-240 | TODO | [#738](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/738) | [Анализ #738, «Ошибки передачи практик»](../docs/analysis/2026-11-16-hub-optimization-start.md) | Спицы создаются вручную копированием, поэтому каждая рождается со своим набором отклонений (M-1…M-8, A-1…A-5): контракт выноса покрывает только вынос из Хаба, а для новой спицы без исходного проекта процедуры нет. Нужно: (1) рождение спицы = этап E1 контракта (геном с закреплённого SHA, профиль по схеме B-238) без E2–E6; (2) регистрация в матрице `docs/ecosystem-map.md` до первого содержательного PR; (3) проверка Хаба, которая читает реестр и отмечает `governed`-спицу без `AGENTS.md`, `.hub-profile.json` или с `last_sync` старше порога. Критерий: новая спица проходит валидаторы генома Хаба (0 FAIL) в первый день. | Structured |

## Спринт 32: Перенесён в aether-orbis-proxeneta

Полный спринт и его незавершённые задачи B-287…B-306 находятся в
[бэклоге спицы](https://github.com/G-Ivan-A/aether-orbis-proxeneta/blob/582f8a074e1377405429196764b562fa8cb32fb4/ops/backlog.md).
Удалённая E6 подтвердила перенос без перенумерации. Проектные задачи ведутся в
приватной спице.

---

## Спринт 34: Методология создания проектов экосистемы

**Story.** Issue [#757](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/757)
поставил цель продавать цифровых сотрудников как SaaS или сервис и запросил
исследование индустриальной практики автономных мультиагентных систем.
[исследование #757](../research/hub/2026-11-28-digital-employee-methodology-survey.md) (модель M3) предложило шаги M0–M9 создания цифрового сотрудника.
Шаги M0–M7 совпадают с цепочкой артефактов Хаба: видение → концепция →
архитектура → дорожная карта.

Проекты экосистемы до сих пор создаются без общей методологии этой цепочки:
каждый проект заново решает, какие артефакты нужны и какой гейт их принимает.
Фаундер в #757 решил завести такую методологию с приоритетом P2 и зависимостью
от исследования.

**Цель.** Одна методология создания проекта экосистемы (vision, concept,
architecture, roadmap) с артефактом и гейтом на каждом шаге, согласованная с
шагами M0–M7 исследования #757, чтобы не появились две параллельные рамки.

**Критерий закрытия.** B-316 имеет статус `DONE` или `CANCELLED`, а
методология принята или отклонена человеком в issue или PR.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **B-316** | Методология создания проектов экосистемы (vision/concept/architecture/roadmap) | **P2** | - | TODO | - (planned) | Решение фаундера в issue [#757](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/757); [исследование #757](../research/hub/2026-11-28-digital-employee-methodology-survey.md), §6 и §10 | Описать, как создаётся проект экосистемы: какие артефакты (vision, concept, architecture, roadmap) нужны, кто их утверждает, какой гейт принимает каждый и как проект переходит от одного шага к следующему. Входы: шаги M0–M7 и модель ответственности исследования #757, [ADR-002](../docs/adr/2026-06-adr-002-artifact-document-methodology.md), уровни L1–L4 [видения](../docs/vision.md). Не дублировать ai-education и исследование #757 — ссылаться на них. Критерий: методология применена хотя бы к одному существующему проекту экосистемы и прошла ревью человека. | null |

---

## Источники активного порядка

| Источник | Что даёт бэклогу |
| --- | --- |
| [backlog-instruction.md](backlog-instruction.md) | Правила ведения, статусы, sprint format, archiving policy and `null` rule. |
| [docs/analysis/2026-06-30-backlog-and-artifact-change-policy-analysis.md](../docs/analysis/2026-06-30-backlog-and-artifact-change-policy-analysis.md) | Источник проблем перегрузки бэклога and amendment policy B-036. |
| [docs/analysis/2026-07-04-kb-runs-hub-applicability-analysis.md](../docs/analysis/2026-07-04-kb-runs-hub-applicability-analysis.md) | Trigger-based decision source for not adding root `kb/` and `runs/` to the Hub now. |
| [docs/adr/2026-07-adr-007-hub-root-structure.md](../docs/adr/2026-07-adr-007-hub-root-structure.md) | Decision source for post-migration root boundaries and B-056..B-063. |
| [docs/audit/2026-07-04-cross-standard-stress-tests.md](../docs/audit/2026-07-04-cross-standard-stress-tests.md) | Source findings for the standard-structure repair chain B-049..B-054 after B-049 routing to Audit. Цепочка закрыта и архивирована по issue [#583](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583) (Спринты 3 и 6); строка сохранена как источник происхождения нормы. |
| [research/hub/2026-07-04-hub-as-agent-system-global-analysis.md](../research/hub/2026-07-04-hub-as-agent-system-global-analysis.md) | Global analysis v0.4 (issues #394/#398/#400): §8 рекомендации, §11 реестр пробелов, §15.8 входы RFC/ADR — источник задач B-064..B-078 (Спринты 5–7). Спринты 6 и 7 закрыты и архивированы по issue [#583](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583); в активном бэклоге от них остались B-068 и B-070 (отложенные с триггером `B-173`) и B-069 (перенесён в Спринт 19). |
| Issue [#411](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/411) / [#413](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/413) (обсуждение 2026-07-10, решение фаундера) | Источник задач B-079..B-084 (Спринт 8): разделение Mango на публичный `ai-ba-playbooks` и приватный `mango_ba_prompts` (существующий репозиторий переводится в режим Private по уточнению issue [#511](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/511)). Спринт 8 закрыт и архивирован по issue [#583](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583): стратегия Hub + Spoke утверждена, `mango_ba_prompts` переведён в `legacy/archived`, целевой репозиторий новой разработки — `mango-ba-ai-runtime`. |
| Issue [#418](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/418) (постановка фаундера) | Источник задач B-085..B-087 (Спринт 9): научно-теоретическое исследование retrieval-стратегий как вход для RFC-F и теоретическая основа образовательного модуля. |
| Issue [#427](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/427) (обсуждение 2026-07-16; B-050 v0.2 §2) | Источник triggered-задачи B-088: разграничение ADR как SSOT для решений и Стандарта как SSOT для исполнения только после появления повторяющейся операционной боли. |
| Issue [#437](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/437) и методологическое обсуждение 2026-07-16 | Источник задач B-089..B-091 (Спринт 10): модель зрелости Reference Pattern, разделение Research Method и Domain Methodology, валидация на не-AI доменах. |
| Issue [#457](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/457) (постановка фаундера) | Источник задач B-092..B-093: исследование промышленных практик агентного исполнения задач как вторая валидация Reference Research Pattern и фактическая база для будущего RFC по архитектуре постановки задач. |
| [docs/rfc/2026-08-06-rfc-task-statement-architecture.md](../docs/rfc/2026-08-06-rfc-task-statement-architecture.md) (RFC [#470](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/470)) | Источник задач ОПС B-094..B-097 и статуса B-093: архитектура постановки задач для AI-агентов, следствия которой требуют проспективного замера эффекта. |
| Issue [#466](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/466) и PR [#467](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/467) | Источник обновления правил работы агентов (`ai-rules/`) и практики разметки артефактов ОПС: вход для B-096 (инструкция по меткам GitHub). |
| Issue [#555](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/555) (решения фаундера по `Q-1`…`Q-8` RFC оси «Среда») | Источник задач B-121 (исследование discovery навыков GigaCode), B-122 (RFC замены бэклога внешним трекером через MCP) и B-123 (состав дельты среды комплексного развёртывания) и разблокировки B-117…B-120. |
| Issue [#561](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/561) и модуль [`research/ba-requirements/artifact-micro-structure/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/artifact-micro-structure/00-introduction.md) | Источник задач B-136..B-145 (Спринт 15): микро-уровень методологии БА — закрытый словарь слотов, валидатор структуры, три проекции одного документа, реестр Golden Set, правила нескольких продуктов в одной задаче и поправки к макро-модулю. Фактическая база — замер 17 результирующих документов корпуса `runs/` и проверка словаря слотов на независимом корпусе [KB runtime](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/main/docs/kb) (на дату замера — `mango_ba_prompts/kb/processed`). Задачи B-144 и B-145 заведены по [комментарию фаундера к PR #562](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/562). |
| Issue [#571](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571) и модули [`projects/ba-ai-process/ba-meta-model/process-taxonomy/`](https://github.com/G-Ivan-A/ba-ai-metamodel/blob/e1f67e267beb73809e1edb26313691a5c769c92a/ba-meta-model/process-taxonomy/00-introduction.md) и [`projects/ba-ai-process/ba-meta-model/operation-taxonomy/`](https://github.com/G-Ivan-A/ba-ai-metamodel/blob/e1f67e267beb73809e1edb26313691a5c769c92a/ba-meta-model/operation-taxonomy/00-introduction.md) | Источник задач B-155..B-163 (Спринт 17): пересборка таксономии процессов и операций от индустриального базиса BABOK v3 с объявленной дельтой КК Манго. Фактическая база — [замер восьми дефектов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-10-process-taxonomy-defects-facts.md) на коммитах `8cbf82a` и `15aa76f` и валидация нового словаря на семи синтетических кейсах. Правила решения — [ADR-015](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-015-process-operation-taxonomy-rebuild.md). Приложенный к issue диалог с фаундером имеет приоритет над телом issue и задал сущности `Система`/`Актор`, навык как подпроцесс и графовый маршрут. |
| Issue [#575](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/575) и аналитическая записка [`practices/ai-engineering/2026-09-14-ai-pdlc-industry-alignment.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/ai-engineering/2026-09-14-ai-pdlc-industry-alignment.md) | Источник задач B-164..B-168 (Спринт 18): сверка мета-модели БА v2 с индустриальным отчётом Ассоциации ФинТех «ИИ-трансформация разработки 2026» по пяти углам. Фундаментальных противоречий с архитектурой не выявлено; зафиксированы пять адресных разрывов — отсутствие отдельного слоя намерения, отсутствие узла-оркестратора, отсутствие метрики стоимости прогона в токенах при числовой границе `SK-6`, неагрегируемый список гипотез исполнителя по `GT-5` и необъявленные границы входных данных и контура исполнения. |
| Issue [#580](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/580) и [пакет исполнения](https://github.com/G-Ivan-A/ba-ai-metamodel/blob/e1f67e267beb73809e1edb26313691a5c769c92a/dist/execution-package-gigacode-cli/README.md) | Источник задач B-179..B-188 (Спринт 20): компиляция вертикального среза `A-IN → A-CORE → A-BCREQ` в развёртываемый пакет и бэклог его масштабирования. Состав скопированного, преобразованного и отброшенного объявлен в [манифесте компиляции](https://github.com/G-Ivan-A/ba-ai-metamodel/blob/e1f67e267beb73809e1edb26313691a5c769c92a/dist/execution-package-gigacode-cli/package-manifest.yaml); обязательство независимости прогона от Хаба — в [`AGENTS.md` спутника](https://github.com/G-Ivan-A/ba-ai-metamodel/blob/e1f67e267beb73809e1edb26313691a5c769c92a/dist/execution-package-gigacode-cli/AGENTS.md). |
| Issue [#583](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583) (решение владельца) | Источник актуализации бэклога: архивация Спринтов 3, 6, 7 и 8, перевод `mango_ba_prompts` в `legacy/archived`, переопределение цели Спринта 13, перевод Спринта 14 в `Icebox` и формирование Спринта 19 (B-069..B-174) — задач, необходимых только для первого прогона BCREQ в `mango-ba-ai-runtime`. Там же зафиксировано правило компиляции `EP-C1`. |
| [RFC #715](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md), принят в issue [#717](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/717) | Источник Спринта 30 (B-234…B-267): шаги 1–7 дорожной карты, решения владельца Q-1…Q-5 и замена таблицы статусов репозиториев ссылкой на единый реестр. |
| Issue [#721](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/721) и [RFC завершения выноса GRA](../docs/rfc/2026-11-04-rfc-gra-extraction-completion-and-hub-cleanup.md) | История закрытого Спринта 31 (B-268…B-286): решение владельца, предусловия в спице, перенос задач Спринта 29, manifest redirect в валидаторах, вынос домена из дерева с архивом тегом ([ADR-022](../docs/adr/2026-11-adr-022-hub-archive-and-extraction-redirect.md)) и реестры. Фактическая база — [evidence-контейнер](../research/hub/exp/gra-extraction-cleanup-721/README.md). |
| Issue [#738](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/738) и [анализ старта оптимизации Хаба](../docs/analysis/2026-11-16-hub-optimization-start.md) | Решение владельца о возобновлении выноса метамодели БА (окно заморозки 2026-11-16): исполнение B-243, снятие триггеров B-244…B-250, задача B-307 и рекомендации по бэклогу. |
| Issue [#740](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/740), [#742](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/742) | Спринты 32/33 и 28 ID перенесены в [бэклог спицы](https://github.com/G-Ivan-A/aether-orbis-proxeneta/blob/582f8a074e1377405429196764b562fa8cb32fb4/ops/backlog.md); приёмка Хаба (B-308…B-310) завершена и архивирована. |
| Issue [#757](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/757) и [исследование #757](../research/hub/2026-11-28-digital-employee-methodology-survey.md) | Источник Спринта 34 (B-316 — решение фаундера) и отложенной задачи B-317: методология создания проектов экосистемы и калибровка мульти-LLM гейта перед продажей цифровых сотрудников. |
| GitHub Issues/PR | История выполненных задач, review discussion and implementation evidence. |
