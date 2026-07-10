---
status: draft
version: 0.1
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

> Режим: **Analysis (options + recommendation)** для issue
> [#407](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/407) / B-050.
> Это вход для human decision gate B-051: документ **не принимает решение, не
> создаёт ADR или мета-стандарт, не меняет R/A/A/Report-стандарты и валидаторы**.

## 1. Summary / BLUF

Для ADR B-051 рекомендуется **вариант F: инвариантный скелет + типовой слот +
специфичные разделы снизу**.

У всех стандартов должен быть один фиксированный каркас из 10 разделов. Слот
`Type Model` всегда присутствует и может содержать subtype profiles, модель без
подтипов или явное `not applicable`. После общего каркаса разрешены только
типоспецифичные разделы. Их заранее исчерпывающе классифицировать не нужно:
автор обосновывает полезность, человек проверяет на review. Порядок и назначение
разделов фиксированы, содержание внутри них остаётся свободным и релевантным.

F — не простое переименование гибрида D. D складывает три механизма исключений;
F начинает с одного проверяемого инварианта и локализует вариативность в двух
явных местах. Это лучше закрывает найденные STRUCT/ORDER/PROF/BND/FM/VAL-дефекты,
даёт предсказуемую навигацию и допускает особенности Research, Analysis, Audit
и Report без пустого каталога профилей или скрытого расхождения структуры.

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

Scope B-050: сравнить механизмы meta-structure и подготовить recommendation.
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
него обязательный `Type Model` использует одну из форм: `profiles`, `model` или
`not applicable`. После каркаса разрешены обоснованные типоспецифичные разделы.
Их содержание и содержание общих разделов свободно в рамках назначения.

**Предлагаемый каркас для решения B-051 (названия могут быть уточнены ADR):**

1. `Purpose`;
2. `Scope`;
3. `Identification and Placement`;
4. `Frontmatter`;
5. `Minimum Body Sections`;
6. `Type Model` — profiles/model/явное отсутствие;
7. `Lifecycle`;
8. `Boundaries` — локальные отличия и ссылка на canonical routing owner;
9. `Validation`;
10. `Related Artifacts`;
11. далее — только type-specific sections.

Пустой общий раздел не удаляется: он кратко фиксирует `not applicable` и
почему. Специфичный раздел добавляется снизу при реальной полезности; отсутствие
исчерпывающего классификатора — сознательный human review gate, а не ошибка.

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

## 5. Comparison matrix

Шкала: `5` — лучшее соответствие критерию, `1` — худшее. Оценки служат
объяснимым сравнением, а не автоматическим решением ADR.

| Критерий | Вес | A | B | C | D | F |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Предсказуемая навигация / порядок | 5 | 2 | 2 | 1 | 3 | **5** |
| Profiles + model/no-model | 4 | 3 | 4 | 2 | **5** | **5** |
| Специфичные разделы без потери | 4 | 3 | 3 | **5** | **5** | **5** |
| Простота validator enforcement | 4 | 3 | 2 | 2 | 1 | **5** |
| Review ergonomics | 4 | 3 | 3 | 1 | 2 | **5** |
| Frontmatter/boundary consistency | 3 | 2 | 2 | 2 | 3 | **5** |
| Creative mode внутри разделов | 3 | 4 | 4 | **5** | 4 | **5** |
| Низкая сложность внедрения | 2 | 4 | 3 | **5** | 1 | 3 |
| Обязательный принцип issue #407 | 5 | 2 | 2 | 1 | 3 | **5** |
| **Взвешенный итог / 170** |  | **87** | **91** | **79** | **104** | **158** |

Sensitivity check: даже без строки «обязательный принцип» F набирает 133/145,
а ближайший D — 89/145. Рекомендация не зависит только от заранее заданного
требования: F также лучше по validator cost и review ergonomics.

## 6. Recommendation for B-051

ADR B-051 следует рассмотреть вариант F и зафиксировать пять решений:

1. единые названия, назначение и порядок 10 разделов skeleton;
2. обязательный `Type Model` с ровно одной формой: profiles, model или явное N/A;
3. type-specific sections разрешены только после skeleton, без закрытого
   классификатора и с human review полезности;
4. `Boundaries` содержит локальную дельту и ссылку на один canonical owner, но
   не копирует общую routing-таблицу;
5. validator сначала проверяет только структуру (presence/order/uniqueness), а
   не пытается формализовать свободное содержание.

### 6.1. Accepted trade-offs

- Пустая секция лучше исчезнувшего контракта: `N/A + rationale` создаёт
  наблюдаемое состояние, но не требует искусственного контента.
- Механический migration diff допустим один раз; смысловые изменения должны
  быть отделены или явно перечислены в B-053.
- Human review остаётся источником решения о полезности specific tail; validator
  ловит структурный drift, но не заменяет редакционное суждение.

### 6.2. Risk mitigations

| Риск | Митигация для ADR/meta-standard/implementation |
| --- | --- |
| Skeleton превращается в бюрократический шаблон | Короткий `N/A + rationale`; не задавать минимальный объём текста. |
| Specific tail становится свалкой | Требовать связь с purpose/scope и review question «почему это не часть общего раздела?». |
| Дублирование boundary rules | Один canonical owner; sibling standards содержат только delta + link. |
| Model и profiles снова расходятся | Один slot и три исчерпывающие формы, а не два независимых раздела. |
| Validator блокирует полезное расширение | Проверять первые 10 sections; разрешать дополнительные headings только после них. |
| B-053 незаметно меняет семантику | Separate structural mapping и semantic-delta list; каждый смысловой delta требует ссылки на ADR. |

## 7. Validator and migration impact

Предлагаемая последовательность downstream, без выполнения в B-050:

1. B-051 принимает/корректирует skeleton и boundary ownership.
2. B-052 задаёт normative heading vocabulary, N/A convention и extension rule.
3. B-053 составляет mapping текущих headings к skeleton, переносит блоки и
   отдельно перечисляет semantic deltas.
4. Validator получает fixture на один корректный standard, отсутствующий
   section, неверный order, duplicate section и разрешённый specific tail.
5. После миграции повторяется cross-standard stress test; B-054/B-065 решают,
   нужно ли нормировать сам процесс.

Пример ожидаемого mapping, не изменение стандартов:

| Current block | Skeleton destination |
| --- | --- |
| Research `Evidence Container`, `exp/ vs runs`, legacy mode | specific tail после `Related Artifacts` |
| Research routing/classification | общий `Boundaries`; operational detail — specific tail |
| Analysis/Report `Subtype Profiles` | `Type Model: profiles` |
| Audit `4-компонентная модель` | `Type Model: model` |
| Analysis anti-inflation trigger | `Type Model` policy или specific tail, по решению B-051 |
| Audit process vs report output | `Boundaries` delta или specific tail, без копии общего routing |

## 8. Review focus and open decision gate

Этот analysis не оставляет вопроса, требующего отдельной backlog-записи: B-051
уже является human decision gate. Reviewer B-051 должен подтвердить или
скорректировать:

- точные названия и порядок 10 sections;
- нужен ли `N/A + rationale` всегда или только для `Type Model`;
- кто является canonical owner общей boundary/routing table;
- относится ли anti-inflation trigger к общему `Type Model` или к specific tail;
- должен ли validator разрешать дополнительные sections без registry.

## 9. Related Artifacts

- [ADR-001](../adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md)
- [ADR-002](../adr/2026-06-adr-002-artifact-document-methodology.md)
- [Cross-standard stress tests](../audit/2026-07-04-cross-standard-stress-tests.md)
- [Research Standard](../../standards/research-standard.md)
- [Analysis Standard](../../standards/analysis-standard.md)
- [Audit Standard](../../standards/audit-standard.md)
- [Report Standard](../../standards/report-standard.md)
- [Backlog B-050..B-054](../../pr-ops/backlog.md)
