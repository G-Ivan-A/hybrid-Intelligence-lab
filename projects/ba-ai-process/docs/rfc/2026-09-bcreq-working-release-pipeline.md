---
status: proposed
version: 0.1
updated: 2026-09-23
temperature: 0.1
owner: G-Ivan-A
rfc-scope: C
---

# RFC: конвейер Working Document → Release Document для BCREQ

## RFC Metadata

| Поле | Значение |
| --- | --- |
| Owner | G-Ivan-A |
| RFC status | `proposed`; принятие только решением человека |
| Source issue | [#607](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/607) |
| Implementation link | [PR #608](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/608) |
| Evidence | Девять вложений issue #607, прочитанных только во временной рабочей области; ранее принятые изменения [PR #602](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/602), [PR #604](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/604) и [PR #606](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/606) |
| Impacted artifacts | После принятия: BCREQ Source schema, skills, gates, compiler, release profiles и Distribution |
| Decision record | Этот RFC является предложением; отдельный ADR до решения владельца не создаётся |
| Archetype scope | `C` — Product Spoke / Runtime |

## Summary

Предлагается не поддерживать два независимо редактируемых документа. Вместо
этого BCREQ получает один типизированный **Working Document** — рабочий пакет и
единственный источник семантики — и один или несколько **Release Document**,
детерминированно скомпилированных из подтверждённого baseline для заданной
аудитории.

Рабочий пакет хранит evidence, User Story, scope, FR/NFR, UC, матрицы покрытия,
варианты решения, решения и edge cases. Release содержит только одобренную и
уместную для получателя проекцию. Каждый NFR обязан ссылаться на конкретные FR.
Признак `requires_backward_compatibility` определяется до FR и при положительном
значении порождает проверяемые обязательства в FR, сценариях, edge cases и
функциональном дизайне. Компиляция не создаёт новую семантику и сама проходит
отдельный `G-release`.

Термины Working/Release являются локальным операционным решением проекта, а не
заявлением, что BABOK, IREB или TM Forum предписывают документы с такими
названиями.

## Motivation

Анализ вложений issue #607 показал повторяемый разрыв между процессом
проектирования требований и конечным документом.

| Наблюдение | Риск | Требуемое свойство процесса |
| --- | --- | --- |
| В ходе диалога варианты, вопросы, UI-детали и edge cases нужны для проверки, но перегружают итоговый текст. | Если удалить их рано, теряется обоснование; если оставить всё, клиент получает историю работы вместо согласованного решения. | Полный Working baseline и управляемая Release-проекция. |
| Раздел 2.3 «Задачи» в разобранных кейсах повторял FR, ограничения и детали решения. | Один смысл редактируется в нескольких местах и расходится. | Заменить обязательные задачи явной границей изменения; задачи исполнителю не включать в системные требования. |
| NFR появлялись как отдельные качественные пожелания или как проценты, добавленные к функциональному поведению. | Качество нельзя проследить к функции или проверить без выдуманной метрики. | Типизированный NFR с явным `applies_to_fr` и доказанным target. |
| Обратная совместимость обсуждалась после формирования решения. | Позднее ограничение меняет FR, состояния и переходные сценарии уже после согласования. | Раннее решение о совместимости и производные обязательства по всей модели. |
| До проверенного FR генерировались UC или технические решения; в других случаях edge cases оставались без владельца. | Возникают фиктивные способности, додуманная архитектура или неполное покрытие. | Направленный trace-граф и гейты между стадиями. |
| Два JSON-вложения оказались байт-в-байт идентичными. | Количество файлов ошибочно принимается за количество независимых свидетельств. | Дедупликация evidence по checksum до анализа. |

Проверена альтернативная гипотеза «достаточно улучшить шаблон конечного
документа». Она опровергнута: дефекты возникали до рендеринга — при
классификации, выборе варианта, удержании состояния согласования и построении
trace. Следовательно, нужен жизненный цикл модели, а не только новый шаблон.

Вложения использованы как контекст процесса, а не как источник продуктовых
фактов. Исходные JSON/TXT и производные расшифровки не входят в репозиторий и
подлежат удалению после анализа.

## Goals and Non-goals

### Goals

- определить роли Working Document и Release Document без двух источников
  истины;
- зафиксировать стадии, переходы, владельцев решений и машинные/человеческие
  гейты;
- решить судьбу раздела 2.3;
- обеспечить трассировку каждого NFR к одному или нескольким FR;
- сделать обратную совместимость ранним драйвером FR, UC, edge cases и дизайна;
- нормировать состав раздела «Функциональный дизайн решения»;
- определить fail-closed правила компиляции и Release-манифест;
- согласовать предложение с уже созданными контрактами продуктовой атрибуции,
  абстракции FR/UC/NFR и Source → Distribution.

### Non-goals

- менять в этом PR schema, skills, route, templates или Distribution;
- объявлять RFC принятым без решения владельца;
- переносить в Git вложения issue, персональные данные или полные диалоги;
- выбирать конкретную продуктовую архитектуру, UI, API, SLA или миграционный
  срок для будущих BCREQ;
- выдавать локальную форму Working/Release за дословное требование внешнего
  стандарта;
- заменять проектные задачи, план разработки или тест-план документом системных
  требований.

## Proposal

### 1. Один источник семантики, две формы использования

**Working Document** — логический рабочий пакет BA-процесса. Физически он может
состоять из нескольких файлов, но все его сущности принадлежат одному
`working_baseline_id`, имеют стабильные ID и собираются в один trace-граф.
Редактируется только Working.

**Release Document** — неизменяемая проекция подтверждённого Working baseline,
собранная для конкретных `audience` и `release_profile`. Release вручную не
редактируется. Исправление начинается в Working, проходит повторное
подтверждение и создаёт новую версию Release.

```text
evidence -> Working model -> approved baseline -> compiler -> Release + manifest
```

В графе действуют как минимум связи:

```text
source -> goal/scope -> User Story -> FR -> UC/edge case -> design decision
                                      \-> NFR -> verification
source -> compatibility decision -> obligation -> FR/UC/edge case/design
approved nodes -> release fragment -> release manifest
```

Связь должна быть представлена ID, а не только упоминанием номера в тексте.
Markdown является представлением модели, но не заменяет типизированный trace.

### 2. Семистадийный поток

| Стадия | Результат Working | Условие перехода |
| --- | --- | --- |
| `W0 Intake and attribution` | Нормализованная цель, автор, source register, checksum-дедупликация, подтверждённая продуктовая цепочка и первичное решение о совместимости. | Источники доступны или пробелы названы; продуктовая атрибуция подтверждена человеком; `requires_backward_compatibility != unknown`. |
| `W1 Context and boundary` | Проблема, цель, обязательная User Story, actor/system boundary, `in_scope`, `out_of_scope`, as-is/delta и ограничения. | Контекст не содержит скрытых FR/NFR; граница и дельта подтверждены BA/заказчиком. |
| `W2 Requirements baseline` | Минимальный набор capability-level FR и измеримых NFR с provenance и ссылками. | Все FR относятся к delta; каждый NFR имеет `applies_to_fr`; TBD не выдан за target. |
| `W3 Behaviour and alternatives` | UC, coverage matrix, edge cases, варианты решения, критерии выбора и открытые решения. | Каждый FR покрыт UC; каждый сценарий и edge case имеет владельца требования/ограничения; выбранные варианты подтверждены человеком. |
| `W4 Functional design` | «Функциональный дизайн решения»: правила, состояния, взаимодействия, разрешённые UI/настройки и исключения, прослеженные к FR/UC. | Дизайн не придумывает архитектуру; каждый FR получает выбранный дизайн либо подтверждённый `design_not_required` с причиной. |
| `W5 Verification and baseline approval` | Результаты `G-mach`, `G-semantic`, BA review, журнал разрешённых вопросов и неизменяемый `working_baseline_id`. | Все блокирующие ошибки закрыты; BA подтверждает baseline; digest зафиксирован. |
| `W6 Release compilation and publication review` | Release Document, `release_manifest`, trace report и результат `G-release`. | Проекция полна для выбранного профиля, не содержит запрещённых/нерешённых данных и одобрена человеком для публикации. |

Переходы последовательны, но возврат на более раннюю стадию разрешён. Любое
семантическое изменение после `W5` инвалидирует baseline и все производные
Release; исправление только отрисовки инвалидирует соответствующую Release,
но не Working baseline.

### 3. Решение по разделу 2.3

Обязательный раздел 2.3 «Задачи» **отклоняется**. В клиентской проекции профиля
`BCREQ-client-v1` его заменяет **2.3 «Границы изменения»**:

- `in_scope` — что меняется в целевой системе;
- `out_of_scope` — что явно не меняется;
- зависимости и допущения, которые меняют границу;
- ссылка на delta и затронутые FR.

User Story обязательна в Working и связывает actor, цель и наблюдаемый outcome.
Её отображение в Release определяется профилем и не превращает её в FR.

Пункт не создаётся, если он лишь пересказывает полный список FR. Задачи
исполнителю («разработать», «протестировать», «доставить») живут в системе
планирования. Бизнес-результат остаётся в цели/User Story, системная способность
— в FR, качество — в NFR, запрет — в constraint, способ реализации — в дизайне.

Это уточняет предложенную в
[RFC уровня абстракции и продуктовой маршрутизации](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md)
проекцию бизнес-контекста. Оба RFC имеют статус `proposed`; принятие этого
решения требует синхронно обновить либо supersede пересекающуюся часть прежнего
RFC, а не оставить две нормы.

### 4. Контракт FR, UC, edge case и функционального дизайна

FR остаётся capability-level утверждением «что должна обеспечивать целевая
система». UI control, поле, шаг, исключение, текущее поведение и технический
компонент самостоятельными FR не становятся.

Каждый FR содержит как минимум:

```yaml
requirement_id: FR-001
source_refs: [SRC-001]
goal_refs: [GOAL-001]
user_story_refs: [US-001]
delta_ref: DELTA-001
product_binding_refs: [PB-001]
scenario_refs: [UC-001]
acceptance_refs: [AC-001]
```

UC реализует один или несколько FR и содержит actor, goal, trigger,
preconditions, основной поток, alternatives/exceptions и outcome. Edge case не
остаётся свободным текстом: он ссылается на FR, NFR или constraint, получает
ожидаемый outcome и verification reference. Связь FR↔UC — many-to-many.

Раздел 4 Release называется **«Функциональный дизайн решения»**. Название
ограничивает содержание наблюдаемой логикой и не обещает архитектурный design.
Раздел может включать только подтверждённые:

- бизнес-правила, состояния и переходы;
- взаимодействия actor↔system и видимые реакции;
- настройки, UI-state и варианты только в глубине, необходимой для однозначного
  поведения;
- выбранные решения и их применимость;
- ошибки, исключения и fallback;
- ссылки на FR/UC/edge cases.

Архитектура сервисов, таблицы БД, недоказанные API и sprint/deployment work в
этот раздел не попадают. Невыбранные варианты остаются в Working.

### 5. Строгая трассировка NFR → FR

Каждый quality NFR обязан иметь непустой `applies_to_fr` и сохраняет контракт
из форензики issue #605: quality attribute, объект измерения, condition,
measure, target, verification method и source.

```yaml
requirement_id: NFR-001
quality_attribute: performance
applies_to_fr: [FR-001, FR-003]
condition: "..."
measure: "..."
target: "..."
verification_method: "..."
source_refs: [SRC-002]
```

Метка `scope: system` допустима в Working только как удобство автора. Перед
baseline она разворачивается в явный список действующих FR. Пустой список,
несуществующий FR или ссылка только на раздел блокируют `G-mach`.

Target нельзя синтезировать из «практики», прилагательного или типового числа.
Неизвестный target остаётся `TBD` с owner и вопросом в Working и блокирует
публикацию соответствующего NFR в Release как согласованного требования. Один
NFR может относиться к нескольким FR; копировать его ради каждого FR нельзя.

Constraint также имеет явный `applies_to_fr`, если ограничивает функции, но не
маскируется под quality NFR. Процент выполнения функционального outcome не
переклассифицирует FR в NFR.

### 6. Обратная совместимость как вход и сквозной драйвер

На `W0` создаётся решение:

```yaml
compatibility:
  requires_backward_compatibility: true
  rationale: "..."
  source_refs: [SRC-003]
  baseline_refs: [BASELINE-001]
  affected_surfaces: [interface, data, workflow]
  obligation_refs: [COMP-001]
```

Поле принимает `true`, `false` или `unknown`.

- `true` требует минимум одного compatibility obligation, связанного FR,
  переходного/legacy UC либо edge case, design decision и verification.
- `false` требует source/rationale и перечисления проверенных поверхностей;
  отсутствие анализа не считается `false`.
- `unknown` создаёт вопрос с owner и блокирует утверждение baseline и Release.

Compatibility obligation описывает сохраняемое внешнее поведение, затронутый
baseline, допустимое изменение, период/условие перехода при наличии источника и
метод проверки. Неизвестный срок не заменяется типовым значением.

Обратная совместимость не является изолированным абзацем в конце документа.
Она может породить новый FR, если целевая система должна предоставить отдельную
способность миграции/совместного действия, либо ограничить существующий FR. В
обоих случаях она обязана породить сценарии старого клиента/данных/настроек,
edge cases переключения и отражение в функциональном дизайне. `G-mach`
проверяет эту замкнутость.

### 7. Состав Working Document

Working хранит необходимое для анализа, проверки и воспроизводимости:

1. source register с provenance, retrieval status и checksum, но не
   автоматически сами чувствительные вложения;
2. продуктовую атрибуцию и границу системы;
3. проблему, цель, User Story, scope и as-is→delta;
4. типизированные FR/NFR/constraints и acceptance criteria;
5. UC, state/decision tables, coverage matrix и edge cases;
6. варианты решения с критериями, статусами `candidate|selected|rejected` и
   rationale;
7. функциональный дизайн выбранного варианта;
8. compatibility decision и производные obligations;
9. открытые вопросы с owner/status и журнал человеческих решений;
10. результаты `G-mach`, `G-semantic`, BA review и baseline digest.

Raw chat exports, debug logs и невоспроизводимые CDN-файлы не становятся частью
Working автоматически. Политика хранения и доступ определяются отдельно;
trace может хранить checksum и стабильную разрешённую ссылку. Это предотвращает
утечку evidence в клиентский документ.

### 8. Release-профиль и правила компиляции

Профиль `BCREQ-client-v1` проецирует:

1. термины;
2. бизнес-контекст: проблема, цель и 2.3 «Границы изменения»;
3. функциональные требования;
4. функциональный дизайн решения;
5. нефункциональные требования;
6. ограничения и подтверждённые допущения;
7. приложения, разрешённые профилем: выбранные UC, migration/compatibility либо
   интерфейсный контракт.

Приложение 7 не является обязательной свалкой внутренних деталей. Внутренняя
техническая спецификация включается только в профиль для внутренней аудитории
или когда она явно является частью согласуемого контракта.

Компилятор получает только approved baseline, версионированный release profile
и аудиторию. Для каждой сущности профиль задаёт `required`, `conditional` или
`internal_only`. Компилятор:

1. проверяет digest и статус baseline;
2. отбирает сущности по типу, статусу, audience и policy;
3. рендерит их без добавления продуктовых фактов или перефразирования смысла;
4. строит обратный trace `release_fragment -> Working IDs`;
5. записывает причины каждого условного исключения;
6. создаёт документ и `release_manifest`;
7. передаёт оба артефакта в `G-release`.

Минимальная форма манифеста:

```yaml
release_id: REL-001
working_baseline_id: WB-001
working_digest: "sha256:..."
release_profile: BCREQ-client-v1
release_profile_version: 1
audience: customer
included_ids: [GOAL-001, FR-001, NFR-001]
excluded:
  - id: OPT-002
    policy: internal_only
    reason: rejected-option
trace_report_ref: TRACE-REL-001
release_digest: "sha256:..."
```

Fail-closed правила:

- `required` entity нельзя исключить или заменить общим резюме;
- FR нельзя публиковать без выбранного дизайна либо подтверждённого
  `design_not_required` с причиной и проверяемого acceptance;
- NFR нельзя публиковать без всех `applies_to_fr` в той же Release либо без
  явного профильно разрешённого cross-reference;
- compatibility obligation нельзя скрыть, если она меняет публикуемый FR;
- unresolved question, `unknown`, `TBD`, rejected option, внутренний review log,
  raw evidence и персональные данные в клиентскую Release не проходят;
- генеративное изменение текста после BA approval создаёт новый draft Working,
  а не Release;
- одинаковые baseline/profile/compiler version должны давать byte-identical
  канонический результат.

### 9. Гейты и ответственность

| Gate | Проверяет | Не подменяет |
| --- | --- | --- |
| `G-mach` | Schema, уникальность ID, абсолютность ссылок, taxonomy membership, source/goal/delta trace, FR↔UC coverage, NFR→FR, compatibility closure, отсутствие dangling refs. | Семантическую релевантность и выбор решения. |
| `G-semantic` | Claim↔source, as-is/delta, уровни FR/UC/NFR, противоречия, полноту flows и edge cases; сохраняет rationale/counterexample. | Детерминированную гарантию или решение заказчика. |
| `G-human/BA` | Границу, User Story, минимальность FR, выбранный вариант, приемлемость дизайна и readiness baseline. | Машинную целостность trace. |
| `G-release` | Digest baseline, профиль, completeness, inclusion/exclusion policy, отсутствие внутренних/TBD данных, обратный trace и детерминизм компиляции. | Разрешение на внешнюю публикацию. |
| `G-human/publish` | Получателя, конфиденциальность, коммерческую/договорную уместность и финальную отправку. | Исправление Release вручную. |

Таким образом, BA review выполняется до компиляции, как предложено в issue, а
`G-release` и publish review после неё проверяют, что сам projector не потерял
или не раскрыл данные.

### 10. Состояния и запрет параллельного редактирования

Минимальные состояния Working:

```text
draft -> context-approved -> requirements-approved -> modeled
      -> design-approved -> baseline-approved -> superseded
```

Release имеет `compiled -> release-verified -> published -> superseded`.
Состояние Release не повышает статус Working и наоборот. Одновременно
существующие Release для разных аудиторий ссылаются на один baseline; ни одна из
них не становится новым source of truth.

## Alternatives

### Два независимо поддерживаемых документа

Отклонено: дублирует FR/NFR и создаёт ручной drift. Разделение нужно на уровне
authoring baseline и проекции, а не источников семантики.

### Один документ со скрываемыми разделами

Отклонено как основной механизм: условное отображение не создаёт манифест,
обратный trace и доказательство того, что внутренняя информация не утекла.

### Редактировать Release после генерации

Отклонено: исправление теряет связь с Working и делает повторную компиляцию
небезопасной. Любая смысловая правка возвращается в Working.

### Оставить 2.3 «Задачи» обязательным

Отклонено: приложенные кейсы показали смешение бизнес-результата, требования к
системе, ограничения и executor work. Явный scope закрывает полезную функцию
раздела без дублирования FR.

### Проверять только готовый Release

Отклонено: поздний гейт не восстанавливает утраченные варианты, evidence и edge
cases. Нужны stage gates до baseline и отдельная проверка проекции после него.

## Trade-offs

- Типизированный Working и стабильные ID увеличивают стоимость authoring, но
  делают потерю требований и ручной drift наблюдаемыми.
- Явный NFR→FR trace требует обновлять связи при изменении FR; зато исключает
  «глобальные» пожелания без проверяемого объекта.
- Ранний compatibility decision может остановить поток на `W0`, но позднее
  выявление той же зависимости дороже и меняет уже выбранный дизайн.
- Детерминированная компиляция ограничивает стилистическую свободу Release.
  Генеративное улучшение допустимо только до baseline с повторным BA review.
- Несколько release profiles требуют versioning и тестов; взамен один Working
  безопасно обслуживает разные аудитории.
- Термин «Функциональный дизайн решения» длиннее «Дизайн решения», но снижает
  риск ожидания архитектурной спецификации.

## Impacted Artifacts

В текущем PR меняются только:

- этот proposal RFC;
- навигация проекта;
- локальный contract test RFC.

После принятия решения потребуются отдельные реализационные изменения:

| Артефакт | Изменение |
| --- | --- |
| BCREQ Source schema | Типы Working, NFR links, compatibility decision, baseline и release manifest. |
| Skills/routes | Семь стадий, переходы и остановки на гейтах. |
| Validators | Coverage, NFR→FR, compatibility closure, release completeness и privacy policy. |
| Compiler | Versioned release profiles, deterministic rendering и reverse trace. |
| Distribution | Повторная компиляция только из принятого Source. |
| Golden tests | Положительные и отрицательные fixtures для API, ЛК, КЦ и multi-product. |

RFC пересекается с разделами 1, 6–9
[RFC уровня абстракции и продуктовой маршрутизации](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md).
После human acceptance пересекающиеся нормы должны быть объединены или явно
superseded до изменения runtime.

## Implementation and Validation

### В этом PR

- предложение переведено в статус `proposed`, но runtime не изменён;
- добавлен тест
  `tools/test-bcreq-working-release-pipeline.sh`, который удерживает ключевые
  маркеры и запрещает относительные Markdown-ссылки в RFC;
- вложения анализируются вне Git и удаляются после завершения работы;
- backlog не обновляется: issue #607 ранее не была его элементом.

Локальная проверка:

```bash
./tools/test-bcreq-working-release-pipeline.sh
./tools/test-ba-requirements-forensics.sh
./tools/validate-frontmatter.sh .
./tools/validate-file-naming.sh
./tools/validate-repository-structure.sh
./tools/validate-rrp-links.sh
python3 tools/generate-manifest.py --check
```

### После принятия

1. Согласовать этот RFC с пересекающимся proposal и закрепить одно решение.
2. Добавить schemas и negative fixtures до изменения skills.
3. Реализовать `G-mach`, baseline digest, compiler и `G-release` в Source.
4. Добавить release profiles и privacy fixtures.
5. Выполнить пробную компиляцию на ранее проверенных формах BCREQ.
6. Скомпилировать Distribution из Source и доказать повторяемость.
7. Обновить runtime только отдельной задачей и отдельным PR.

Definition of Done реализации: orphan NFR, `unknown` compatibility, потерянный
edge case, ручная правка Release и исключение required FR должны падать в
negative tests; повторная компиляция должна быть byte-identical.

## Lifecycle and Decision Path

RFC готов к human review. Он не меняет принятые решения и runtime до явного
решения владельца.

Владельцу предлагается принять либо отклонить одним решением:

1. Working как единственный редактируемый baseline и Release как его проекцию;
2. замену обязательного 2.3 «Задачи» на 2.3 «Границы изменения»;
3. обязательные NFR→FR и compatibility closure;
4. pre-baseline gates плюс post-compilation `G-release`;
5. название раздела 4 «Функциональный дизайн решения».

При принятии статус становится `accepted`, а пересекающийся RFC синхронно
обновляется или получает явную ссылку supersession. Только после этого
открывается реализационная задача. При отклонении статус меняется на `rejected`
с зафиксированной альтернативой.

## Open Questions

Блокирующих вопросов для review нет. Выбор принять или отклонить пакет решений
выше является human decision, а не пробелом анализа. Конкретные имена schema,
формат физического хранения Working и набор дополнительных release profiles
определяются после принятия без изменения семантических инвариантов RFC.

## Related Artifacts

- [Issue #607](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/607)
  — постановка, вложения и Definition of Done.
- [Анализ Golden Form](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-bcreq-golden-forms-and-feasibility.md)
  — уровни абстракции, семь разделов и feasibility Source/Distribution.
- [Форензика требований](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-requirements-run-forensics.md)
  — инварианты FR/UC/NFR, evidence и gate boundary.
- [RFC уровня абстракции и продуктовой маршрутизации](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md)
  — связанный proposal, который должен быть согласован при принятии.
- [ADR-017 Source/Distribution](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/decisions/2026-09-adr-017-ba-ai-process-source-distribution.md)
  — принятая граница Source, Distribution, Runtime и Feedback.
- [IREB CPRE Glossary](https://cpre.ireb.org/en/downloads-and-resources/glossary)
  и [ISO/IEC/IEEE 29148:2018](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec-ieee%3A29148%3Aed-2%3Av1%3Aen)
  — внешние источники определений требований; они не задают локальные имена
  Working/Release.
