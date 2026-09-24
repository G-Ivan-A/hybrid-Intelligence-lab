---
status: accepted
version: 0.3
updated: 2026-09-24
temperature: 0.1
owner: G-Ivan-A
rfc-scope: C
---

# RFC: уровень абстракции BCREQ и продуктовая маршрутизация

## RFC Metadata

| Поле | Значение |
| --- | --- |
| Owner | G-Ivan-A |
| RFC status | `accepted`; решение владельца в [issue #609](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/609), уточнения и границы — в [сквозной проверке](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-24-architecture-convergence-and-readiness.md) |
| Source issue | [#601](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/601) |
| Evidence and golden-form candidates | [Анализ трёх форм BCREQ](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-bcreq-golden-forms-and-feasibility.md) |
| Run forensics and semantic contracts | [Форензика 67 прогонов и двух диалогов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-requirements-run-forensics.md) |
| Impacted artifacts | Мета-модель и Source-контракты; затем отдельная компиляция Distribution и изменение runtime |
| Decision record | Владелец принял вариант 1 с уточнениями в приложенном к [issue #609](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/609) диалоге; принятие runtime Golden Set и публикация остаются отдельными решениями |
| Archetype scope | `C` — Product Spoke / Runtime |
| Маршрут | `RG-BCREQ-v1` |
| Решение | Архитектура принята; этот RFC сам по себе не меняет навыки, диспетчер или схему BCREQ |

## Summary

Сохраняется внутренняя 14-слотовая модель BCREQ; для неё вводятся
семантическая проекция из семи читаемых разделов и явная лестница абстракции.
Функциональное требование в разделе 3 описывает способность целевой системы —
«что должна делать система». Сценарии, бизнес-правила, UI, настройки и
технические решения раскрывают эту способность в разделах 4 и 7, не размножая
псевдо-ФТ.

До декомпозиции маршрут должен связать задачу с продуктовой таксономией и
проверить релевантность каждого выбранного факта цели, границе системы и
продукту. После декомпозиции отдельный coverage contract связывает ФТ и UC как
отношение многие-ко-многим. Детерминированный валидатор проверяет форму,
идентификаторы, членство в таксономии и покрытие; семантический гейт и человек
отвечают за уровень абстракции и релевантность.

RFC описывает изменение Source. Физическая правка навыков, схем, dispatcher и
маршрута Distribution вынесена в последующую реализационную задачу.

## Motivation

Разбор пяти BCREQ, двух трасс исполнения и диалога с фаундером выявил четыре
связанных дефекта.

1. Действующая декомпозиция требует атомарности каждого утверждения. В
   результате поля, состояния UI, ограничения и варианты поведения превращаются
   в десятки ФТ вместо раскрытия нескольких способностей системы.
2. Наличие citation доказывает происхождение текста, но не его релевантность
   цели. Неудачный прогон использовал формально найденные, но предметно чужие
   факты и прошёл структурные проверки.
3. Distribution скомпилирована для `contact-center`. API-, ЛК- и
   multi-product-задача не получают явной продуктовой привязки до выбора
   предметных навыков.
4. Trace связывает требования с источниками, но не требует полной матрицы
   `ФТ ↔ UC`. Поэтому генератор может либо оставить способность без сценария,
   либо создать фиктивное ФТ для каждого варианта.

Полная доказательная таблица и три кандидата Golden Form находятся в
[анализе реализуемости](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-bcreq-golden-forms-and-feasibility.md).

### Проверенные альтернативы

- **Исправить только prompt.** Не закрывает дефект: текстовая инструкция всё
  ещё исполняется вероятностно, а текущий валидатор не видит семантическую
  ошибку.
- **Считать каждое атомарное правило отдельным ФТ.** Противоречит образцам:
  десятки настроек и вариантов реализуют несколько устойчивых способностей.
- **Сделать отдельную мета-модель для API, ЛК и КЦ.** Не требуется: верхний
  семантический скелет совпадает, различается раскрытие решения и технической
  спецификации.
- **Заменить 14 слотов семью.** Удаляет полезные границы trace, integrations и
  open questions. Проекция даёт читаемость без потери внутренней структуры.
- **Полностью автоматизировать semantic accept.** На текущем уровне
  формализации это обещание нельзя проверить детерминированно; окончательное
  решение остаётся за человеком.

## Goals and Non-goals

### Goals

- нормировать уровень абстракции функционального требования;
- отделить способность системы от сценария, правила, UI и реализации;
- ввести проверяемую продуктовую привязку до предметной декомпозиции;
- доказать релевантность evidence не только источнику, но цели и границе;
- сделать покрытие ФТ↔UC явным и допускающим многие-ко-многим;
- разделить детерминированные и семантические гейты;
- сохранить обратимо компилируемую границу Source → Distribution.

### Non-goals

- менять в этом PR физические навыки, dispatcher, route или BCREQ schema;
- объявлять три формы runtime Golden Set без воспроизводимого прогона и
  отдельной human acceptance;
- задавать конкретные UI, API-методы, payload, коды ошибок или SLA;
- закрывать полную перестройку отраслевой методологии или задачи
  [`B-121`, `B-122`, `B-123`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ops/backlog.md);
- доказывать переносимость MANGO-контракта за пределы `scope: mango-only`.

## Proposal

### 1. Семь разделов как проекция 14 слотов

Каноническая внутренняя модель остаётся 14-слотовой. Для внутреннего читателя
она группируется так:

| Раздел | Внутренние слоты |
| --- | --- |
| 1. Термины и определения | `S-GLOSSARY` |
| 2. Бизнес-контекст | `S-PROBLEM`, `S-SCOPE` |
| 3. Функциональные требования | `S-FR` |
| 4. Ожидаемое решение и Use Cases | `S-SOLUTION`, `S-SETTINGS`, `S-UI`, `S-SCENARIO`, `S-AC` |
| 5. Нефункциональные требования | `S-NFR` |
| 6. Ограничения и открытые вопросы | `S-LIMITS`, `S-OPEN` |
| 7. Внутренняя техническая спецификация | `S-TRACE`, `S-INTEGRATION` и проекция `V-DEV` |

Это внутренняя семантическая группировка, а не обязательный клиентский профиль.
Клиентский `BCREQ-client-v1` из
[RFC Working → Release](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-working-release-pipeline.md)
заменяет 2.3 «Задачи» на «Границы изменения», называет раздел 4
«Функциональный дизайн решения» и публикует раздел 7 только по разрешённому
профилю. Проектор не переносит детали между слотами и не скрывает пустоту во
внутреннем trace; отсутствие обязательного клиентского содержания блокирует
Release, а неприменимый слот получает явную причину.

### 2. Лестница абстракции

Каждое кандидатное утверждение получает ровно один уровень:

| Уровень | Вопрос | Целевой дом |
| --- | --- | --- |
| `L1 capability` | Что должна уметь целевая система? | `S-FR` |
| `L2 scenario/rule` | При каком событии и по какому бизнес-правилу проявляется способность? | `S-SCENARIO`, `S-AC`, `S-SOLUTION` |
| `L3 interaction/setting` | Как пользователь настраивает или наблюдает поведение? | `S-SETTINGS`, `S-UI` |
| `L4 technical` | Какими интерфейсами, данными и состояниями это реализуется? | `S-INTEGRATION`, `S-TRACE`, `V-DEV` |

Атомарность сохраняется на L2–L4: один сценарий, критерий или правило должен
быть проверяемым. На L1 критерием качества становится одна независимая
способность и полное покрытие нижними уровнями. Название поля, экрана, метода,
кода или конкретного значения является сигналом L3/L4, но не самостоятельным
семантическим доказательством ошибки: окончательное решение принимает
semantic gate.

### 3. Pre-decomposition contract

До формирования слотов создаётся `C-REQ-MAP` — реестр кандидатных
утверждений. Минимальные поля:

```yaml
statement_id: ST-001
goal_refs: [GOAL-01]
task_refs: [TASK-01]
system_boundary: target-system
product_binding:
  domain_id: D-01
  capability_id: PC-001
  feature_id: PF-001
  atomic_function_id: AF-001
source_refs: [SRC-01]
candidate_statement: "..."
abstraction_level: L1
target_slot: S-FR
relevance_decision: accepted
relevance_reason: "..."
```

Окончательные имена и schema version определяются реализационной задачей.
Нормативен смысл: ни одно утверждение не попадает в BCREQ без связи с целью,
задачей, границей системы, продуктом и evidence либо без явного решения
`rejected` с причиной.

### 4. Relevance gate

Citation отвечает на вопрос «откуда утверждение». Relevance gate отдельно
отвечает на четыре вопроса:

1. Какую цель и задачу поддерживает факт?
2. Относится ли субъект к целевой системе, а не к соседнему продукту или
   процессу исполнителя?
3. Совместим ли факт с выбранной продуктовой привязкой?
4. Меняет ли факт содержание целевого BCREQ или является лишь тематически
   похожим фоном?

Совпадение ключевых слов, продукта верхнего уровня или отрасли недостаточно.
Конфликтующие факты не усредняются: оба сохраняются как evidence, а решение
выносится в `S-OPEN` и `G-human`.

### 5. Product routing preflight

До `n0` диспетчер определяет **тип работы и направление поиска** по заявленной
цели, виду входа и результату процесса. `n0` вычисляет одну или несколько
цепочек `domain → capability → feature → atomic function` из версионированных
снимков:

- [таксономия продуктов MANGO](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/product-taxonomy/mango-products.yaml);
- [отраслевые соответствия ИТ/телеком](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/product-taxonomy/telecom-products.yaml).

| Вход и цель | Первичная ось | Вторая ось и результат |
| --- | --- | --- |
| Доработка системы MANGO, которой заказчик пользуется или которую документированно рассматривает | MANGO | Сопоставить соответствующие отраслевые классы; подтверждение интереса не доказывает существование capability. |
| Поиск документации или решений в базе знаний MANGO | MANGO | Отраслевое соответствие добавлять, когда оно помогает ответу; отсутствие не запрещает поиск KB. |
| Проверка отраслевой или лучшей практики | Отраслевая классификация | Сопоставить с MANGO, если продуктовая применимость заявлена; не выдавать общий стандарт за локальную функцию. |
| Оценка внешнего ТЗ (`P-08`) | Требования внешнего ТЗ и отраслевая классификация | Сопоставить найденные классы с MANGO и сохранить `matched/unmatched/uncertain` для каждого требования. Результат `P-08` — суждение об осуществимости, не BCREQ. |

В диалоге [issue #609](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/609)
предложен переход для внешнего ТЗ на MANGO-first при покрытии шаблонными
требованиями не менее 80%. В Source нет утверждённого версионированного
каталога таких шаблонов, правил единицы счёта и процедуры проверки ложных
совпадений. До их появления порог не используется как детерминированный
предикат. Даже после появления каталога он меняет **порядок поиска**, а не
скрывает unmatched-требования и не подменяет отраслевую проверку. Измерение
сохраняет numerator, denominator, версию каталога и anchors каждого совпадения.

Предложение агента содержит тип работы, использованное правило, обе цепочки,
версии снимков, evidence, альтернативы и рекомендацию `accept/reject` с
обоснованием риска. `G-human` подтверждает или отклоняет **сопоставление и
основание**; он не выбирает алгоритм по умолчанию. При отклонении хранится
причина, а маршрут останавливается до нового кандидата и повторной проверки.
Неизвестный ID, несогласованная цепочка или требуемое, но отсутствующее
соответствие останавливает затронутую ветвь. Отсутствие отраслевого mapping
не запрещает чистый поиск в KB, но запрещает заявлять подтверждённую двойную
привязку. Dispatcher не содержит безусловного `contact-center`.

Существующий [узел `n0`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/dist/execution-package-gigacode-cli/routes/rg-bcreq-v1.yaml)
из PR #604 подтверждает MANGO-цепочку до `n1`, но ещё не содержит этого
классификатора намерения и двунаправленного сопоставления. Это обязательная
дельта следующей компиляции Source → Distribution, а не описание уже
выполненного runtime.

Multi-product-задача остаётся одним BCREQ, если у неё одна бизнес-цель и одна
граница изменения. Она хранит несколько product bindings и прослеживает каждое
ФТ к одной или нескольким цепочкам. Разделение на несколько документов
требуется при независимых целях или несвязанных границах, а не только из-за
числа продуктов.

### 6. Content semantics и rendering

Source владеет семантикой слотов, лестницей уровней и правилами покрытия.
Шаблон Distribution владеет представлением. Он рендерит семь разделов из 14
слотов по выбранному release-профилю и применяет **один или несколько**
содержательных overlay-профилей:

- API усиливает интерфейсный контракт, состояния доступа, ошибки и события;
- ЛК усиливает роли, настройки, UI-state matrix и обратную связь;
- коммуникации контакт-центра усиливают рабочий контекст оператора,
  бизнес-правила, очереди, маршруты и устойчивость исторических данных;
- клиент коммуникаций сотрудника (в том числе Mango Talker) усиливает
  состояния клиентского приложения, уведомления, сеансы и переходы между
  устройствами, только если они подтверждены источником;
- AI и автоматизация усиливают входные данные, управление моделью/правилом,
  вмешательство человека, качество результата и обработку ошибок для роботов
  **и** речевой аналитики.

Профиль описывает паттерн содержания, а не отдельный продукт и не официальный
класс TM Forum. Поэтому робот и речевая аналитика могут использовать один
профиль при разных MANGO-capabilities; Talker может сочетаться с API или ЛК.
Контакт-центр здесь — предмет коммуникаций, не синоним продукта «КЦ Манго».
Видеоконференции сами по себе не требуют отдельного профиля: известная
[таксономия](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/product-taxonomy/mango-products.yaml)
содержит capability `voice-ucaas/video-conferencing`, но не доказывает
отдельный способ rendering. Новые профили появляются по повторяющемуся
контрпримеру, который нельзя выразить сочетанием существующих. Overlay не
меняет смысл L1 и не добавляет обязательства без evidence.

### 7. Coverage contract ФТ↔UC

Вводится явный many-to-many реестр:

```yaml
coverage:
  - scenario_id: UC-001
    kind: happy
    requirement_refs: [FR-001, FR-002]
    nfr_refs: []
    constraint_refs: []
    acceptance_refs: [AC-001]
```

`kind` принимает как минимум `happy`, `alternative`, `exception`, `boundary`.
Каждое ФТ имеет не менее одного UC; каждый UC связан хотя бы с ФТ, NFR или
ограничением. UC, проверяющий только качество или запрет, не порождает
фиктивного ФТ. Машинный гейт проверяет ссылки и полноту; человек проверяет, что
сценарий действительно демонстрирует указанную способность.

### 8. Разделение гейтов

`G-mach` может детерминированно проверять:

- schema version, обязательные поля и уникальность ID;
- существование taxonomy IDs и полную цепочку product binding;
- наличие отраслевого соответствия там, где выбранная ветвь его требует;
- непротиворечивые ссылки statement→goal/task/source/slot;
- полное покрытие ФТ↔UC и отсутствие dangling references;
- наличие причины для пустого слота;
- диагностические маркеры L3/L4 в ФТ как reject или warning по принятой
  политике.

`G-semantic` выполняет model-assisted review релевантности, уровня абстракции и
полноты, но не объявляется детерминированным. Он сохраняет основание решения и
контрпример. `G-human` принимает спорные классификации и переводит новый
пример в Golden Set. Ни prompt, ни `G-semantic` без внешней схемы и человека не
дают жёсткой гарантии.

### 9. Typed contracts FR, UC и NFR

Форензика полного legacy-корпуса уточняет лестницу абстракции тремя
инвариантами. Полные определения, негативные примеры и evidence находятся в
[анализе прогонов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-requirements-run-forensics.md).

- `FR-INV-01`: один FR выражает одну независимо проверяемую capability
  целевой системы; UI, шаг, правило, constraint и implementation detail сами по
  себе не являются FR.
- `UC-INV-01`: UC содержит actor, goal, trigger, preconditions, основной поток,
  alternatives/exceptions и outcome; он демонстрирует FR, но не создаёт новую
  capability.
- `NFR-INV-01`: quality NFR содержит attribute, объект, condition, measure,
  target, verification и source. Неизвестный target остаётся `TBD`, а не
  заполняется типовым или выведенным моделью числом.

Для всех трёх типов обязательны typed ID, source trace и двустороннее coverage.
Процент или числовой target не превращает функциональное поведение в NFR.
Автоматическое действие формулируется от субъекта «Система», а не механически
как «возможность Пользователя».

### 10. TM Forum и SID: две типизированные оси

Локальная product taxonomy и TM Forum mapping разделяются. Поля `PC-*`,
`PF-*`, `AF-*` принадлежат MANGO taxonomy и не являются TM Forum ID. Prose в
`industry_correspondence.tm_forum` является ориентиром, но не точным binding.

```yaml
industry_bindings:
  tm_forum:
    status: unresolved # resolved | unresolved | not-applicable
    element_type: capability # capability | etom-process | oda-component | open-api
    snapshot_ref: null
    element_id: null
    element_name: null
    source_anchor: null
  sid_context:
    status: unresolved # resolved | unresolved | not-applicable
    snapshot_ref: null
    element_type: null # domain | ABE | business-entity
    element_id: null
    element_name: null
    source_anchor: null
  local_product_binding_refs: [PB-01]
  rationale: "..."
  reviewed_by: null
```

`resolved` на любой оси требует доступного версионированного источника,
точного element ID, имени и anchor; поле ID типизировано по виду элемента.
Если публичный обзор даёт только домен без стабильного ID, сохраняется
`unresolved` и отдельный **кандидат** с URL и rationale, но не `resolved`.
Similarity, свободный перевод и угадывание по названию запрещены. Точный
binding принимает `G-human`, а `G-mach` проверяет membership и тип поля.

[Information Framework (SID)](https://www.tmforum.org/open-digital-architecture/information-framework-sid/)
сам принадлежит TM Forum и описывает информационные сущности и их домены.
Это полезная **вторая ось контекста**, но не независимый стандарт, который
замещает отсутствующий ID capability/eTOM. Наличие SID-контекста не повышает
`tm_forum.status` до `resolved` и не снимает блокировку там, где задача требует
точного capability/process binding. Так сохраняется намерение владельца
использовать доступный обзор как поддержку эскалации без ложной точности.

## Impacted artifacts for implementation

| Артефакт | Предлагаемое изменение | Было в PR #602 |
| --- | --- | --- |
| [Мета-модель: taxonomy](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/20-taxonomy.md) | Закрепить product binding и версионирование snapshot. | Только snapshot и навигация. |
| [Мета-модель: decision framework](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/30-decision-framework.md) | Добавить `C-REQ-MAP`, relevance/abstraction/coverage invariants. | Нет. |
| [Мета-модель: practice](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/40-practice-and-cases.md) | После приёмки оформить три кейса Golden Set. | Нет. |
| Source contracts/schemas | Описать pre-decomposition и coverage contracts. | Нет. |
| Source templates | Описать 14→7 projection и сочетаемые content overlays. | Нет. |
| [BCREQ skeleton](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/dist/execution-package-gigacode-cli/templates/bcreq-skeleton.md) | Скомпилировать принятую проекцию. | Нет. |
| [Output schema](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/dist/execution-package-gigacode-cli/contracts/c-out-bcreq.schema.json) | Добавить versioned mapping/coverage representation либо отдельную schema. | Нет. |
| Skills, dispatcher, route | Добавить product preflight, новую декомпозицию и гейты. | Нет. |
| Package validator/evaluation | Проверять routing data и новые структурные invariants. | В этом PR — только целостность taxonomy snapshots. |

## Migration plan

### Phase 0 — решение

Владелец принял архитектуру и три формы как целевые кандидаты в
[issue #609](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/609).
Это не является приёмкой новых runtime Golden cases без отдельного
воспроизводимого прогона и human review.

### Phase 1 — Source contracts

Добавляются `C-REQ-MAP`, coverage contract, abstraction ladder, rendering
projection и три принятых реальных кейса. Каждый контракт получает собственные
положительные и отрицательные fixtures.

### Phase 2 — compiler и validator

Компилятор производит versioned schemas/templates/route data из Source.
Валидатор проверяет taxonomy membership, mapping completeness, dangling refs,
coverage и устойчивость повторной компиляции.

### Phase 3 — skills и route

Отдельная issue изменяет навыки, dispatcher и `RG-BCREQ-v1`. Старый пакет
остаётся воспроизводимым по своей версии; миграция выполняется новым package
version без ручного drift Distribution.

### Phase 4 — runtime trial

Три согласованных кейса прогоняются из исходных входов вслепую. Человек
сравнивает уровень абстракции, релевантность и покрытие с Golden Form. Baseline
обновляется только после зафиксированного результата, а не по ожиданию.

## Acceptance criteria

Решение принято для проектирования Source на следующих условиях:

1. раздел 3 содержит только L1 capabilities, а атомарность переносится на
   L2–L4;
2. семь разделов являются projection, а 14 слотов остаются внутренним
   контрактом;
3. product binding обязателен до предметной декомпозиции;
4. три формы из анализа приняты как Golden candidates, но не как уже
   скомпилированные runtime эталоны;
5. `G-mach`, `G-semantic` и `G-human` имеют разные полномочия;
6. физические изменения Distribution выполняются отдельной задачей.

Будущая реализация принимается, когда автоматические проверки докажут:

- неизвестный taxonomy ID и обязательное, но отсутствующее отраслевое
  соответствие дают fail-closed для соответствующей ветви;
- факт только с keyword match не проходит без goal/task/system/product refs;
- ФТ без UC, dangling UC/AC и квадратная матрица с фиктивным ФТ отвергаются;
- UI field, API method или конкретное значение в L1 создают диагностируемый
  reject/warning согласно принятой политике;
- один UC может покрывать несколько ФТ и одно ФТ — несколько UC;
- повторная компиляция Source создаёт byte-identical Distribution;
- три Golden Form воспроизводятся без раскрытия вложений issue в репозитории.

Количество ФТ намеренно не фиксируется числом: жёсткий лимит легко обойти
укрупнением независимых способностей. Проверяется семантика, покрытие и
отсутствие деталей нижнего уровня.

## Risks and trade-offs

- Дополнительный pre-decomposition artifact увеличивает стоимость трассы, но
  делает ошибочную релевантность наблюдаемой до генерации BCREQ.
- Model-assisted `G-semantic` остаётся недетерминированным; поэтому он не
  заменяет структурный валидатор и human acceptance.
- Product binding может выявить, что одной задаче нужны несколько веток. Это
  усложняет routing, но устраняет ложное сведение всего к Контактному центру.
- Семь читаемых разделов могут скрыть происхождение из 14 слотов; поэтому
  projection должна быть воспроизводимой, а canonical structured output —
  сохраняться.

## Privacy and evidence retention

Пять PDF, два JSON-экспорта и диалог использовались только как временный вход
для анализа issue #601. Они, извлечённый текст и персональные данные не входят
в Source или Distribution и удаляются после проверки артефактов. Golden Form
содержат только синтезированную структуру и обезличенные предметные примеры.

## Decision

В [issue #609](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/609)
владелец принял вариант 1 с уточнениями о маршрутизации и профилях. Этот
документ фиксирует проверяемую формулировку. Порог 80% и точный SID binding
не являются готовыми исполняемыми предикатами без указанных источников и
правил измерения; границы зафиксированы в
[сквозной проверке](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-24-architecture-convergence-and-readiness.md).

Снимки продуктовой и отраслевой таксономий, добавленные PR #602, являются
операционными routing inputs для будущей компиляции. Они не исполняют и не
закрывают более широкие отложенные задачи `B-121`, `B-122`, `B-123`.
