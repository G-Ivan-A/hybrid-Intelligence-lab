---
status: draft
version: 0.2
updated: 2026-07-10
temperature: 0.1
type: internal-analysis
context: [hub, standards, meta-structure, structural-desync, raar, issue-407, b-050]
method: source-of-truth-tracing + structural-comparison + option-matrix
scope: repo
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/407"
based_on: "docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md + docs/adr/2026-06-adr-002-artifact-document-methodology.md + docs/audit/2026-07-04-cross-standard-stress-tests.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/407"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/370"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/374"
related_artifacts:
  - "docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md"
  - "docs/adr/2026-06-adr-002-artifact-document-methodology.md"
  - "docs/audit/2026-07-04-cross-standard-stress-tests.md"
  - "standards/research-standard.md"
  - "standards/analysis-standard.md"
  - "standards/audit-standard.md"
  - "standards/report-standard.md"
  - "pr-ops/backlog.md"
---

# Варианты решения структурного рассинхрона стандартов R/A/A/Report

> Режим: **Analysis (options)** для issue
> [#407](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/407) / B-050,
> amended по review issue
> [#415](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/415).
> Это вход для human decision gate B-051: документ **не принимает решение, не
> создаёт ADR или мета-стандарт, не меняет R/A/A/Report-стандарты и валидаторы**.

## 1. Summary / BLUF

B-051 должен выбрать между тремя явными стратегиями: **E — сохранить baseline**,
**F8 — компактный инвариантный skeleton из 8 разделов** или **F10 — подробный
skeleton из 10 разделов**. **F12** остаётся расширенным подвариантом, если human
decision gate признает отдельные governance-разделы оправданными. A–D сохранены
как исследованные механизмы, но не выносятся в shortlist: каждый оставляет
существенный gap или создаёт пересекающиеся механизмы исключений.

Матрица не содержит заранее обязательного принципа как критерия: это constraint,
которому должен соответствовать любой вариант изменения. Варианты F используют
один `Type Model` с двумя формами — `model` или `N/A`; subtype profiles являются
содержанием `model`, а не третьей формой. Specific tail допускается только с
явной ссылкой на `Purpose` или `Scope`. Canonical owner общей routing/boundary
нормы — ADR-002. Решение между baseline, компактностью и подробностью остаётся
за человеком в B-051.

## 2. Sources, scope and authority

Иерархия источников:

1. [ADR-001](../adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md) —
   universal core, archetypes A–D, 2FA и физическое размещение;
2. [ADR-002](../adr/2026-06-adr-002-artifact-document-methodology.md) — типы,
   lifecycle и routing артефактов;
3. [кросс-стресс-тест](../audit/2026-07-04-cross-standard-stress-tests.md) —
   evidence о 22 дефектах рассинхрона;
4. четыре действующих стандарта — наблюдаемая форма и типоспецифичное
   содержание, но не источник решения о физической структуре репозитория.

При противоречии ADR имеет приоритет. Предложенная meta-structure нормирует
форму стандартов и не изменяет физический routing из ADR-001/002.

Scope B-050: сравнить механизмы meta-structure и подготовить варианты решения.
Out of scope: выбрать решение за человека, менять тексты стандартов, создавать
ADR/meta-standard, мигрировать артефакты или расширять validator enforcement.

## 3. Baseline: фактический рассинхрон

На 2026-07-10 все четыре стандарта существуют, поэтому бывший P0 `META-01`
(отсутствующий Analysis standard) как состояние репозитория уже снят. Остальные
классы findings сохраняют значение для дизайна meta-structure.

| Наблюдение | Research | Analysis | Audit | Report |
| --- | --- | --- | --- | --- |
| Число `##`-разделов | 12 | 11 | 11 | 10 |
| Profile/model | отсутствует | `Subtype Profiles` | `4-компонентная модель` | `Subtype Profiles` |
| Model position | — | после body | до frontmatter | после body |
| Minimum body | отдельного блока нет | есть | есть | есть |
| Boundaries | два блока routing/classification | `Boundaries` | `Boundaries` | `Boundaries` |
| Type-specific blocks | evidence, exp/runs, legacy | anti-inflation trigger | process vs output | отсутствуют |
| Общий финал | Lifecycle → Validation → Related | Boundaries → Trigger → Validation → Related | Lifecycle → Boundaries → Validation → Related | Lifecycle → Boundaries → Validation → Related |

Это подтверждает, что проблема — не отсутствие полезных различий, а отсутствие
общей оболочки для их выражения. Простое выравнивание заголовков не устранит
competing sources, различия frontmatter convention и неопределённость позиции
профильного/модельного блока.

### 3.1. Требования к решению

Решение должно:

- давать человеку и агенту предсказуемый адрес правила;
- позволять валидатору проверять наличие и порядок общего каркаса;
- представлять profiles, models и отсутствие обоих одной конструкцией;
- сохранять типоспецифичные правила, не превращая исключения во второй стандарт;
- не дублировать routing/boundary-норму между sibling standards;
- оставлять автору творческую свободу внутри назначений разделов;
- быть применимым к будущим стандартам, а не только к текущим четырём.

Требование issue #407 об инвариантном skeleton — **constraint для вариантов,
которые меняют meta-structure**, а не взвешиваемый критерий. Оно не применяется
к baseline E, потому что смысл baseline — осознанно отказаться от изменения,
если operational pain не оправдывает миграцию. Такое исключение должен явно
принять человек в B-051.

## 4. Options

### 4.1. Вариант A — Subtype Profiles

**Суть.** Каждый стандарт получает одинаковый раздел профилей; обязательные и
опциональные body-секции определяются профильными таблицами. При отсутствии
подтипов раздел явно сообщает `no subtypes`.

**Плюсы.** Устраняет STRUCT-01/PROF-01; хорошо выражает Analysis и Report;
валидатор может проверять наличие profile slot и допустимые profile names.

**Минусы.** Audit имеет ортогональную 4-компонентную модель, а Research —
evidence-container rules, поэтому искусственные профили добавят ceremony. Сам
механизм не задаёт порядок остальных разделов, единый frontmatter или owner
границ.

**Trade-off.** Единообразная типизация ценой ложного представления стандартов
без естественных подтипов.

**Validator impact.** Средний: section-presence и profile vocabulary просты;
семантическую полноту профиля проверить трудно.

**Review ergonomics.** Хороши для сравнения профилей, слабы для поиска общих
норм вне profile block.

**Соответствие обязательному принципу.** Частичное: даёт один слот, но не полный
инвариантный скелет и не правило для специфичных нижних разделов.

### 4.2. Вариант B — общий Model block

**Суть.** Каждый стандарт получает одинаковый `Type Model`, описывающий
сущности, отношения, инварианты и при необходимости profiles.

**Плюсы.** Естественно покрывает subtype profiles и Audit model; создаёт единое
место для machine-readable vocabulary и инвариантов.

**Минусы.** Слишком абстрактен для простых стандартов; не решает order,
frontmatter, body, boundaries или validation; модель легко превращается в
дублирующий пересказ документа.

**Trade-off.** Сильная концептуальная унификация ценой сложности и риска
over-modeling.

**Validator impact.** Высокий без schema, низкий только для заголовка; глубокая
проверка потребует формальной модели, которой пока нет.

**Review ergonomics.** Улучшает поиск концептов, но заставляет сверять модель с
распределёнными нормативными разделами.

**Соответствие обязательному принципу.** Частичное: унифицирует один блок, но не
весь каркас и не политику дополнительных разделов.

### 4.3. Вариант C — Allowed differences

**Суть.** Meta-structure перечисляет допустимые отличия каждого типа стандарта:
отсутствующие секции, иной порядок, profiles/model и boundary ownership.

**Плюсы.** Минимальная миграция, честно сохраняет доменную форму, быстро снимает
формальное обвинение в рассинхроне.

**Минусы.** Кодифицирует текущее расхождение вместо его устранения; список
исключений растёт; навигация остаётся непредсказуемой; validator и reviewer
должны знать матрицу типов.

**Trade-off.** Низкая стоимость сейчас ценой постоянной когнитивной и
операционной стоимости.

**Validator impact.** Высокий: type-aware exception matrix и её версионирование.

**Review ergonomics.** Худшие: для ответа «где правило?» сначала нужен тип и
таблица исключений.

**Соответствие обязательному принципу.** Низкое: allowed differences заменяют
инвариантный скелет, а не дополняют его.

### 4.4. Вариант D — Profiles + Model block + Allowed differences

**Суть.** Общая оболочка содержит profile и model blocks, а таблица allowed
differences разрешает их вариации по типам.

**Плюсы.** Выразителен; может описать все четыре текущих стандарта без потери
содержания; обеспечивает эволюционный переход.

**Минусы.** Три механизма пересекаются: profile может быть частью model, а
allowed difference может отменить оба. Нужны приоритеты и больше review rules;
риск meta-standard сложнее объектов регулирования.

**Trade-off.** Максимальная выразительность ценой максимальной сложности и
неоднозначности.

**Validator impact.** Высокий: compositional rules, conditional sections и
exception precedence.

**Review ergonomics.** Лучше C при дисциплине, но reviewer проверяет три слоя.

**Соответствие обязательному принципу.** Среднее: может реализовать принцип, но
не гарантирует его; allowed differences способны размыть skeleton.

### 4.5. Вариант F — invariant skeleton + type slot + specific tail

**Суть.** Фиксированный каркас всегда присутствует и имеет один порядок. Внутри
него обязательный `Type Model` использует одну из двух форм: `model` или `N/A`.
Таблица subtype profiles при необходимости находится внутри `model` и не
является отдельной формой. После каркаса разрешены обоснованные
типоспецифичные разделы.
Их содержание и содержание общих разделов свободно в рамках назначения.

**Предлагаемый каркас для решения B-051 (названия могут быть уточнены ADR):**

1. `Purpose`;
2. `Scope`;
3. `Identification and Placement`;
4. `Frontmatter`;
5. `Minimum Body Sections`;
6. `Type Model` — model (включая таблицу подтипов при необходимости) или `N/A`;
7. `Lifecycle`;
8. `Boundaries` — локальные отличия и ссылка на canonical routing owner;
9. `Validation`;
10. `Related Artifacts`;
11. далее — только type-specific sections.

Пустой общий раздел не удаляется: он кратко фиксирует `N/A` и почему.
Специфичный раздел добавляется снизу только при реальной полезности и обязан в
первом абзаце сослаться на конкретное утверждение `Purpose` или границу `Scope`,
которую он реализует. Это открытое правило расширения вместо закрытого
классификатора: validator может проверить наличие cross-reference, а человек —
его смысловую корректность.

**Плюсы.** Прямо устраняет STRUCT-01…04 и ORDER; даёт единый model/profile slot;
локализует специфичность; позволяет простую проверку порядка; улучшает diff и
навигацию; сохраняет creative mode внутри разделов.

**Минусы.** Для простых стандартов возможны короткие `not applicable` sections;
перенос существующих секций создаст крупный, хотя в основном механический diff;
границу между общим `Boundaries` и specific tail нужно сформулировать точно.

**Trade-off.** Принимается небольшая структурная избыточность ради
предсказуемости; семантическая гибкость сохраняется через свободное содержание
и нижний specific tail.

**Validator impact.** Низкий/средний: сначала проверять наличие, уникальность и
порядок 10 headings; семантические и cross-document проверки добавлять только
отдельными решениями. Validator не должен запрещать headings после skeleton.

**Review ergonomics.** Лучшие: общий вопрос имеет стабильный адрес, специфичные
правила собраны после него, а нестандартное расширение видно в конце diff.

**Соответствие обязательному принципу.** Полное.

### 4.6. Вариант E — baseline: не менять meta-structure

**Суть.** Сохранить четыре действующих стандарта и не создавать общий skeleton,
пока structural desync не проявится как повторяющаяся operational pain.

**Плюсы.** Нулевая миграционная стоимость; нет нового meta-standard и validator
complexity; полностью следует Anti-Inflation principle, если различия не мешают
поиску, review или сопровождению.

**Минусы.** STRUCT/ORDER/PROF/BND/FM/VAL findings остаются; навигация и review
требуют знания каждого стандарта; будущий пятый стандарт может увеличить drift.

**Trade-off.** Принимается текущая когнитивная стоимость ради отсутствия
структурной работы сейчас. B-051 должен зафиксировать наблюдаемый threshold
пересмотра: например, повторяющиеся review comments, validator exceptions или
ошибочная маршрутизация, а не календарный срок.

**Validator impact.** Нет новых проверок; действующие проверки сохраняются.

**Review ergonomics.** Без изменений; приемлемы только если текущий drift не
создаёт измеримой боли.

**Соответствие constraint issue #407.** Не соответствует по конструкции. Это
явный no-change choice, который допустим только как human Anti-Inflation decision.

### 4.7. Размер skeleton: F8, F10 и F12

Число 10 не является самостоятельной архитектурной истиной. Оно получилось из
разделения semantic content и document metadata в исходном F. B-051 должен
выбрать гранулярность по стоимости навигации и проверки:

| Подвариант | Состав | Что выигрываем | Что теряем |
| --- | --- | --- | --- |
| **F8 compact** | `Purpose`, `Scope`, `Identification and Placement`, `Content Contract`, `Type Model`, `Lifecycle`, `Boundaries`, `Validation and Related Artifacts` | Меньше ceremony; `Frontmatter` входит в identification, minimum body — в content contract; подходит коротким standards | В одном разделе смешиваются validation/links; точечные validator errors и стабильные anchors слабее |
| **F10 explicit** | Исходные 10 разделов F | Отдельные адреса для frontmatter, minimum body, validation и related artifacts; проще order/presence checks | Два metadata-раздела могут выглядеть избыточно; больше `N/A`/коротких блоков |
| **F12 governance-heavy** | F10 + `Conformance` + `Evolution and Compatibility` | Явно отделяет нормативность, совместимость и версионирование для зрелой meta-structure | Максимальная ceremony; преждевременно без повторяющихся conformance/compatibility problems |

F8 — минимальный достаточный skeleton, F10 — более проверяемый, F12 — только при
доказанной governance pain. Specific tail следует после выбранных 8/10/12
разделов и подчиняется одному cross-reference rule во всех подвариантах.

## 5. Comparison matrix

Шкала: `5` — лучшее соответствие критерию, `1` — худшее. Оценки служат
объяснимым сравнением, а не автоматическим решением ADR.

| Критерий | Вес | A | B | C | D | E baseline | F8 | F10 | F12 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Предсказуемая навигация / порядок | 5 | 2 | 2 | 1 | 3 | 1 | 4 | **5** | **5** |
| Единый model/N/A slot | 4 | 3 | 4 | 2 | **5** | 1 | **5** | **5** | **5** |
| Specific tail с контролируемым расширением | 4 | 3 | 3 | 4 | 4 | 2 | **5** | **5** | **5** |
| Простота validator enforcement | 4 | 3 | 2 | 2 | 1 | **5** | 4 | **5** | 3 |
| Review ergonomics | 4 | 3 | 3 | 1 | 2 | 2 | 4 | **5** | 4 |
| Frontmatter/boundary consistency | 3 | 2 | 2 | 2 | 3 | 1 | 4 | **5** | **5** |
| Creative mode внутри разделов | 3 | 4 | 4 | **5** | 4 | **5** | **5** | **5** | 4 |
| Низкая сложность внедрения | 2 | 4 | 3 | **5** | 1 | **5** | 4 | 3 | 1 |
| **Взвешенный итог / 145** |  | **87** | **91** | **75** | **99** | **73** | **125** | **141** | **124** |

Строка «обязательный принцип issue #407» удалена: constraint нельзя повторно
вознаграждать весом. Итог показывает свойства вариантов, но не выбирает решение:
E требует минимум изменений, F8 снижает ceremony, F10 максимизирует явность и
проверяемость, F12 выносит compatibility в отдельный governance contract.

## 6. Decision options for B-051

B-051 должен выбрать и обосновать один из вариантов, а не подтвердить заранее
заданную recommendation:

1. **E baseline** — ничего не менять и задать operational trigger пересмотра;
2. **F8 compact** — принять 8-section skeleton и объединённые metadata blocks;
3. **F10 explicit** — принять 10-section skeleton с отдельными anchors;
4. **F12 governance-heavy** — принять только при evidence, что отдельные
   conformance/compatibility sections уже решают повторяющуюся боль.

Если выбран любой F, ADR фиксирует: точные headings/order; `Type Model` только
как `model`/`N/A`; cross-reference specific tail; структурный validator scope;
и **ADR-002 как canonical owner общей artifact boundary/routing table**.
Sibling standards содержат только локальную delta + ссылку на ADR-002.

### 6.1. Accepted trade-offs

- Пустая секция лучше исчезнувшего контракта: `N/A + rationale` создаёт
  наблюдаемое состояние, но не требует искусственного контента.
- Механический migration diff допустим один раз; смысловые изменения должны
  быть отделены или явно перечислены в B-053.
- Validator проверяет наличие cross-reference specific tail на `Purpose` или
  `Scope`; human review остаётся источником решения о смысловой корректности.

### 6.2. Risk mitigations

| Риск | Митигация для ADR/meta-standard/implementation |
| --- | --- |
| Skeleton превращается в бюрократический шаблон | Короткий `N/A + rationale`; не задавать минимальный объём текста. |
| Specific tail становится свалкой | Требовать явную ссылку на `Purpose`/`Scope` в первом абзаце и review question «почему это не часть общего раздела?». |
| Дублирование boundary rules | Canonical owner — ADR-002; sibling standards содержат только delta + link. |
| Model и profiles снова расходятся | Один slot с двумя формами: `model` (включая profiles) или `N/A`. |
| Validator блокирует полезное расширение | Проверять выбранные 8/10/12 sections; разрешать дополнительные headings только после них и с Purpose/Scope cross-reference. |
| B-053 незаметно меняет семантику | Separate mechanical mapping и semantic-delta list; каждый смысловой delta требует ссылки на B-051/B-052. |

## 7. Validator and migration impact

Предлагаемая последовательность downstream, без выполнения в B-050:

1. B-051 принимает/корректирует skeleton и boundary ownership.
2. B-052 задаёт normative heading vocabulary, N/A convention и extension rule.
3. B-053 разделяет миграцию на два независимо reviewable слоя:
   - **механический**: mapping headings, перенос блоков без изменения смысла;
   - **семантический**: отдельный список content deltas, каждый со ссылкой на
     решение B-051/B-052; отсутствие ссылки блокирует semantic change.
4. Validator получает fixture на один корректный standard, отсутствующий
   section, неверный order, duplicate section и разрешённый specific tail.
5. После миграции повторяется cross-standard stress test; B-054/B-065 решают,
   нужно ли нормировать сам процесс.

Пример ожидаемого mapping, не изменение стандартов:

| Current block | Skeleton destination |
| --- | --- |
| Research `Evidence Container`, `exp/ vs runs`, legacy mode | specific tail после `Related Artifacts` |
| Research routing/classification | общий `Boundaries`; operational detail — specific tail |
| Analysis/Report `Subtype Profiles` | `Type Model: model` с таблицей подтипов |
| Audit `4-компонентная модель` | `Type Model: model` |
| Analysis anti-inflation trigger | `Type Model` policy или specific tail, по решению B-051 |
| Audit process vs report output | `Boundaries` delta или specific tail, без копии общего routing |

## 8. Review focus and open decision gate

Этот analysis не оставляет вопроса, требующего отдельной backlog-записи: B-051
уже является human decision gate. Reviewer B-051 должен подтвердить или
скорректировать:

- выбрать E baseline, F8, F10 или обоснованный F12;
- точные названия и порядок sections, если выбран F;
- нужен ли `N/A + rationale` всегда или только для `Type Model`;
- подтвердить ADR-002 как canonical owner общей boundary/routing table;
- относится ли anti-inflation trigger к общему `Type Model` или к specific tail;
- должен ли validator разрешать specific tail только с формально проверяемой
  ссылкой на `Purpose`/`Scope`.

## 9. Related Artifacts

- [ADR-001](../adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md)
- [ADR-002](../adr/2026-06-adr-002-artifact-document-methodology.md)
- [Cross-standard stress tests](../audit/2026-07-04-cross-standard-stress-tests.md)
- [Research Standard](../../standards/research-standard.md)
- [Analysis Standard](../../standards/analysis-standard.md)
- [Audit Standard](../../standards/audit-standard.md)
- [Report Standard](../../standards/report-standard.md)
- [Backlog B-050..B-054](../../pr-ops/backlog.md)
