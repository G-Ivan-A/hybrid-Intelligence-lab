---
status: proposed
version: 0.1
updated: 2026-07-15
temperature: 0.1
owner: G-Ivan-A
decision-type: methodology
---

# ADR-008: Мета-структура стандартов R/A/A/Report

## Decision Metadata

| Field | Value |
| --- | --- |
| ADR id | ADR-008 |
| Backlog item | B-051 |
| Decision type | methodology |
| Decision status | proposed (narrative summary; машиночитаемый canon — frontmatter `status`) |
| Decision date | 2026-07-10 |
| Owner | G-Ivan-A |
| Source | Решение фаундера в issue [#417](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/417) |
| Primary input | [Analysis B-050 v0.2](../analysis/2026-07-10-r-a-a-report-structural-desync-options.md) |
| Impacted artifacts | Будущие `standards/standard-meta-structure.md` (B-052), `standards/research-standard.md`, `standards/analysis-standard.md`, `standards/audit-standard.md`, `standards/report-standard.md` и validator changes (B-053) |
| Supersedes | none |
| Superseded by | none |

## Context

Кросс-стресс-тест R/A/A/Report выявил структурный рассинхрон четырёх стандартов:
общие правила находятся по разным адресам, model/profile policy и границы
выражены неодинаково, а проверка порядка секций требует type-specific
исключений. [Analysis B-050 v0.2](../analysis/2026-07-10-r-a-a-report-structural-desync-options.md)
сравнил стратегии и передал варианты на human decision gate B-051.

Фаундер выбрал **F10 explicit** в issue #417. Поэтому этот ADR не переоткрывает
решение и не переносит в себя полный option matrix B-050. Он фиксирует выбор,
точный инвариант и governance-границы, необходимые для downstream
meta-standard B-052 и миграции B-053. Создание meta-standard, изменение четырёх
сibling standards и validator implementation остаются вне scope этого ADR.

## Decision

Принять **F10 explicit**: инвариантный десятисекционный skeleton для стандартов
Research, Analysis, Audit и Report. F10 максимизирует явность и проверяемость:
отдельные адреса для `Frontmatter`, `Minimum Body Sections`, `Validation` и
`Related Artifacts` упрощают проверки наличия и порядка и дают стабильные
anchors. Компромисс в виде двух metadata-разделов принят ради предсказуемости.

Обязательные разделы и их порядок:

1. `Purpose`;
2. `Scope`;
3. `Identification and Placement`;
4. `Frontmatter`;
5. `Minimum Body Sections`;
6. `Type Model`;
7. `Lifecycle`;
8. `Boundaries`;
9. `Validation`;
10. `Related Artifacts`.

Все десять разделов всегда присутствуют. Если инвариантный раздел не имеет
применимого содержания, он содержит `N/A` и краткое rationale; это правило
относится ко всем пустым инвариантным разделам, а не только к `Type Model`.
Наблюдаемое пустое состояние предпочтительнее исчезнувшего контракта.

`Type Model` использует одну из двух форм: `model` или `N/A`. Если стандарту
нужны subtype profiles, они являются содержанием `model`, а не третьей формой.
Anti-inflation trigger относится либо к общей policy в `Type Model`, либо к
конкретному дополнительному разделу, но его привязка всегда указывается явно.

[ADR-002](2026-06-adr-002-artifact-document-methodology.md) остаётся canonical
owner общей таблицы artifact boundary и routing. Sibling standards не
дублируют эту общую норму: раздел `Boundaries` содержит только локальную delta
для своего типа и ссылку на ADR-002.

После десяти инвариантных разделов допускается specific tail. Дополнительный
раздел разрешён только тогда, когда его первый абзац содержит формально
проверяемую cross-reference на конкретное утверждение в `Purpose` либо границу
в `Scope`, которую раздел реализует. Validator проверяет наличие и позицию этой
ссылки; смысловую корректность связи подтверждает human review.

## Decision Drivers

- Стабильные anchors сокращают стоимость навигации, review и диагностики
  validator errors.
- Явные секции позволяют простую проверку наличия, уникальности и порядка без
  type-aware exception matrix.
- Единый `Type Model` slot устраняет конкуренцию model и profiles.
- Specific tail сохраняет доменную выразительность и creative mode, не размывая
  общий skeleton.
- Делегирование общей routing/boundary нормы в ADR-002 предотвращает появление
  competing sources of truth.

## Alternatives Considered

Полное сравнение baseline E, F8, F10, F12 и исследованных вариантов A–D остаётся
в [B-050 §4–§6](../analysis/2026-07-10-r-a-a-report-structural-desync-options.md).
Human decision gate #417 закрыл решающий выбор в пользу F10 explicit; остальные
варианты не переносятся в финальную норму.

## Consequences

Положительные последствия:

- общие вопросы получают предсказуемые адреса во всех четырёх стандартах;
- validator может проверять наличие, уникальность и порядок десяти headings;
- diff и human review явно отделяют общий контракт от type-specific tail;
- локальная boundary delta не конкурирует с canonical routing ADR-002.

Компромиссы и риски:

- B-053 создаст крупный, преимущественно механический migration diff;
- простые стандарты могут содержать короткие блоки `N/A + rationale`;
- отдельные metadata-секции увеличивают ceremony;
- validator способен проверить cross-reference, но не её смысловую честность,
  поэтому semantic review остаётся человеческой ответственностью.

B-052 кодифицирует решение как reusable meta-standard. B-053 отдельно показывает
mechanical block moves и список любых semantic deltas; смысловое изменение
требует явной ссылки на этот ADR или downstream human decision.

## Compliance and Validation

Этот ADR соответствует
[ADR Structure Standard](../../standards/adr-structure-standard.md): использует
необходимый frontmatter и обязательные секции ADR, а proposal detail делегирует
B-050. Репозиторные проверки для этого draft:

- `bash tools/test-frontmatter-validator.sh`;
- `bash tools/test-smart-sync.sh`;
- `./tools/validate-file-naming.sh`;
- `./tools/validate-frontmatter.sh .`;
- `./tools/validate-repository-structure.sh`;
- `python3 tools/generate-manifest.py --check`.

Downstream validator B-053 проверяет десять headings в заданном порядке,
разрешает дополнительные headings только после `Related Artifacts` и требует
в первом абзаце каждого дополнительного раздела cross-reference на `Purpose`
или `Scope`. Семантическое соответствие проверяет человек.

## Lifecycle

ADR находится в статусе `proposed`: решение фаундера уже зафиксировано в issue
#417, а merge PR является явным acceptance gate по ADR Structure Standard.
После принятия B-051 переходит в `review`, B-052 получает основание создать
meta-standard, затем B-053 выполняет миграцию четырёх стандартов.

Пересмотр F10 требует нового RFC/ADR или явного superseding decision, если
операционные данные покажут повторяющиеся избыточные `N/A`, validator
exceptions либо review pain. Замещение требует backlink на новый decision
record; календарный срок сам по себе не является trigger.

## Related Artifacts

- [Issue #417: решение фаундера F10 explicit](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/417)
- [B-050 v0.2: варианты решения структурного рассинхрона](../analysis/2026-07-10-r-a-a-report-structural-desync-options.md)
- [ADR-001: Методология инфраструктуры экосистемы](2026-06-adr-001-ecosystem-infrastructure-methodology.md)
- [ADR-002: Методология создания и управления артефактами](2026-06-adr-002-artifact-document-methodology.md)
- [Research Standard](../../standards/research-standard.md)
- [Analysis Standard](../../standards/analysis-standard.md)
- [Audit Standard](../../standards/audit-standard.md)
- [Report Standard](../../standards/report-standard.md)
- [ADR Structure Standard](../../standards/adr-structure-standard.md)
- [Backlog](../../pr-ops/backlog.md)
- [Artifact Map](../../pr-ops/artifact-map.md)
