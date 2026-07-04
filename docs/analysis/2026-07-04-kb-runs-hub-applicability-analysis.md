---
status: draft
version: 0.1
updated: 2026-07-04
temperature: 0.1
type: internal-analysis
context: [hub, root-structure, kb, runs, archetype-a, issue-386]
method: artifact-inventory + root-tree-check + ecosystem-comparison
scope: repo
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/386"
based_on: "docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md + docs/adr/2026-07-adr-007-hub-root-structure.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/386"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/385"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/378"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/326"
related_artifacts:
  - "docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md"
  - "docs/adr/2026-06-adr-002-artifact-document-methodology.md"
  - "docs/adr/2026-07-adr-007-hub-root-structure.md"
  - "standards/research-standard.md"
  - "pr-ops/repo-model.md"
  - "pr-ops/artifact-map.md"
  - "projects/README.md"
  - "standards/project-structure-inheritance.md"
  - "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md"
---

# Applicability of `kb/` and `runs/` in the Hub

> Режим: **Analysis (recommendation)** для issue
> [#386](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/386).
> Короткая граница: **этот документ не переносит файлы, не создает root
> `kb/`/`runs/` и не открывает новую архитектурную альтернативу ADR-007.** Он
> проверяет наличие операционной боли и фиксирует рекомендацию.

## Summary / BLUF

Рекомендация для issue #386: **не вводить** root `kb/` и root `runs/` в Хаб
сейчас.

ADR-001 оставляет `kb/` и `runs/` в universal core экосистемы, но текущий Хаб
является archetype A coordination repository. Для наблюдаемых артефактов уже
есть активные дома. Пустые root-каталоги сделали бы дерево визуально полным, но
не сняли бы операционную боль и нарушили бы Anti-Inflation principle.

Исключение нужно зафиксировать в
[pr-ops/repo-model.md](../../pr-ops/repo-model.md) с явными future triggers.

## Scope

Анализ закрывает исследовательскую задачу, вынесенную из ADR-007 v0.3:

1. проверить, есть ли в Хабе orphan operational knowledge, которому нужен root
   `kb/`;
2. проверить, есть ли в Хабе повторяющиеся run records, которым нужен root
   `runs/`;
3. сравнить использование `kb/` и `runs/` в репозиториях экосистемы до изменения
   корня Хаба.

Это internal analysis, а не новый research corpus. Evidence: текущее дерево
репозитория, governance docs и видимые репозитории организации на 2026-07-04.

## Current Hub Artifacts

В текущем корне Хаба нет физических каталогов `kb/` и `runs/`. Активные дома уже
разделены:

- `ai-rules/` для executable runtime rules и agent onboarding;
- `pr-ops/` для repository operations, backlog, artifact map, executable-doc
  registers и session digests;
- `standards/` для reusable norms и artifact formats;
- `practices/` для reusable practice nodes после evidence и review pain;
- `docs/` для ADR/RFC/analysis/audit/report/guides/concept artifacts;
- `research/` для domain research и research evidence under `exp/`;
- `projects/` и `projects-sink/` для project-scoped и synchronized spoke context.

Ни один найденный Hub artifact не является orphan из-за отсутствия root `kb/`.
Операционное знание уже маршрутизируется в `ai-rules/`, `pr-ops/`,
`standards/`, `practices/`, `docs/guides/` или project-local homes. Перенос этих
материалов в root `kb/` добавил бы вторую маршрутизацию вместо снятия
неоднозначности.

## Run-Record Analysis

В Хабе есть research evidence directories вида `research/hub/exp/...`, но они
существуют для проверки research/analysis claims. ADR-002 и
[standards/research-standard.md](../../standards/research-standard.md) уже
отделяют такой evidence corpus от operational run record.

Операционные следы также живут в GitHub issues, pull requests, CI logs и
[pr-ops/session-digests.md](../../pr-ops/session-digests.md). Эти следы пока не
образуют стабильный повторяющийся корпус, которому нужен root `runs/`: это либо
GitHub-native records, либо repository-operation notes, либо research evidence.

Вывод: текущий Хаб не имеет run-record pain, которую решает root `runs/`.

## Ecosystem Comparison

Главный положительный пример -
[G-Ivan-A/mango_ba_prompts](https://github.com/G-Ivan-A/mango_ba_prompts). В нем
есть и `kb/`, и `runs/`, потому что это prompt-library и BA-process repository:

- `kb/` хранит reusable practices, examples, references и processed knowledge для
  prompt/RAG-like reuse;
- `runs/` хранит prompt, BA-process, analysis и self-test execution records.

Это operational product work с повторяющимися executions, стабильными
input/output evidence и локальным knowledge reuse. Такой operating mode не
совпадает с Хабом.

Остальные репозитории экосистемы не создают требования к root-каталогам Хаба:

- `open-ai.ru` не использует root `kb/` или `runs/`;
- `clarify-engine-ai` использует product/runtime-specific homes вроде
  `knowledge_base/` и `outputs/`, а не точные root names из ADR-001;
- малые/static repositories вроде `test` не используют ни один из каталогов.

Сравнение поддерживает trigger-based local adoption: `kb/` и `runs/` нужны там,
где продукт или процесс реально накапливает повторяющиеся operational artifacts,
а не как empty universal placeholders.

## Recommendation

Не вводить root `kb/` и root `runs/` в Хаб сейчас.

Зафиксировать в Hub model следующее исключение:

| ADR-001 catalog | Current Hub status | Current homes | Reconsideration trigger |
| --- | --- | --- | --- |
| `kb/` | Не создается в корне Хаба. | `ai-rules/`, `pr-ops/`, `standards/`, `practices/`, `docs/guides/`; при необходимости project-local `projects/<project>/kb/`. | Появились как минимум 2-3 reusable operational knowledge artifacts, которые регулярно потребляет агент/процесс и которые нельзя без дублирования разместить в существующих домах. |
| `runs/` | Не создается в корне Хаба. | GitHub issue/PR/CI records, `pr-ops/session-digests.md`, `docs/report/`, `research/<domain>/exp/<issue-slug>/` для research evidence. | Появились повторяющиеся non-research operational/business/pipeline runs, которым нужны стабильные repo-hosted metadata, inputs, outputs, feedback и logs. |

Так ADR-001 остается ecosystem-level methodology, а ADR-007 и
`pr-ops/repo-model.md` задают physical exception для Hub archetype A.

## Impact on ADR-007

ADR-007 не требует нового architectural decision о введении каталогов. Нужна
синхронизационная пометка: issue #386 закрыл backlog research task и подтвердил
направление v0.3. Root `kb/` и `runs/` остаются вне Хаба до выполнения trigger
criteria выше.

## Definition of Done Mapping

| Issue #386 requirement | Result |
| --- | --- |
| Analyze operational pain | Текущие orphan operational knowledge и repeated run-record pain не найдены. |
| Give recommendation | Recommendation: не вводить root `kb/` и root `runs/` сейчас. |
| If excluding, record exception in `repo-model.md` | Required: update `pr-ops/repo-model.md` with the archetype A exception and triggers. |
| Compare ecosystem usage | Mango использует оба каталога из-за repeated prompt/process execution и local KB needs; OpenAI.ru и Clarify не создают требования к Hub root. |

## Related Artifacts

- [ADR-001](../adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md)
- [ADR-002](../adr/2026-06-adr-002-artifact-document-methodology.md)
- [ADR-007](../adr/2026-07-adr-007-hub-root-structure.md)
- [Research standard](../../standards/research-standard.md)
- [Repository model](../../pr-ops/repo-model.md)
- [Artifact map](../../pr-ops/artifact-map.md)
- [Projects index](../../projects/README.md)
- [Project structure inheritance](../../standards/project-structure-inheritance.md)
- [Mango migration plan](../../projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md)
