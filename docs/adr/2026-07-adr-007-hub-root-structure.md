---
status: accepted
version: 0.4
updated: 2026-07-04
temperature: 0.1
owner: G-Ivan-A
decision-type: methodology
---

# ADR-007: Целевая структура корня Хаба

## Decision Metadata

| Field | Value |
| --- | --- |
| ADR | ADR-007 |
| Backlog item | B-047 |
| Decision type | methodology |
| Status | accepted |
| Decision date | 2026-07-04 |
| Owner | G-Ivan-A |
| Source issue | [#378](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/378) |
| Refinement issue | [#382](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/382), [#385](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/385), [#386](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/386) |
| Primary input | [B-034 migration and root structure plan](../analysis/2026-07-04-hub-migration-and-root-structure-plan.md) |
| Upstream decisions | [ADR-001](2026-06-adr-001-ecosystem-infrastructure-methodology.md), [ADR-002](2026-06-adr-002-artifact-document-methodology.md) |
| Impacted artifacts | `pr-ops/backlog.md`, `pr-ops/artifact-map.md`, `pr-ops/repo-model.md`, `tools/validate-repository-structure.sh`, future B-048 migration PR |
| Supersedes | none |
| Superseded by | none |

## Context

B-034 подготовил входящий analysis/plan текущей структуры корня Хаба после
стандартизации Research, Analysis и Audit. Тот analysis намеренно оставил
несколько корневых целей неоднозначными, потому что они требовали решения
фаундера.

Issue #378 закрывает эти неоднозначности. Решение уже принято фаундером, поэтому
этот ADR фиксирует принятую цель и downstream-последствия, а не предлагает RFC с
альтернативами. Этот ADR не выполняет физического переноса файлов, не переписывает
ссылки и не отменяет текущие точки входа. Физическая миграция остаётся в scope
B-048 после принятия ADR-007.

ADR-001 и ADR-002 остаются источником истины для инфраструктуры экосистемы и
маршрутизации артефактов. Стандарты Research/Analysis/Audit не являются источником
структуры корня репозитория. Хаб остаётся archetype A; Hub != Portal.

PR #379 замержил этот ADR как decision gate B-047. Issue #382 доработал запись,
сделав финальное целевое дерево читаемым без параллельного открытия ADR-001; он не
менял принятую архитектуру и не выполнял физической миграции. Issue #385
доработал запись до версии 0.3: он приводит целевое дерево в соответствие с
решениями фаундера (изъятие `kb/` и `runs/` с явной фиксацией расхождения с
ADR-001, уточнение `docs/guides/`, сохранение `GOVERNANCE.md`) и переводит
документ на русский для консистентности с ADR-001/002/003–006. Принятая
архитектура при этом не переоткрывается, а физическая миграция не выполняется.
Issue #386 закрыл отложенное исследование целесообразности `kb/` и `runs/`:
операционная боль для root-каталогов в Хабе не обнаружена, рекомендация — не
вводить их сейчас, а исключение архетипа A и триггеры пересмотра зафиксировать в
`pr-ops/repo-model.md`.

## Decision

Полная структура Хаба = ADR-001 (универсальное ядро) + ADR-007 (дельта для архетипа A).
Ниже приведена полная целевая структура (To-Be) с комментариями.

Принять следующие To-Be решения по корню репозитория Хаба.

**Расхождение с ADR-001:** Универсальное ядро ADR-001 содержит `kb/` и `runs/`.
Для Хаба эти каталоги **не вводятся** до явного указания. Обоснование:
анти-инфляция, отсутствие операционной боли. Issue #386 подтвердил это
расхождение и перенес условия будущего пересмотра в `pr-ops/repo-model.md`.

### Full To-Be Repository Structure

Это дерево — консолидированная цель B-048. Оно перечисляет структурные дома и
стабильные якоря, а не каждый текущий файл. Текущие пути остаются активными до
момента, когда PR физической миграции перепишет ссылки и реестры.

```text
hybrid-Intelligence-lab/
├── ai-governance/                 # [NEW] Политики: государство, бизнес-правила, ИБ, внешние ограничения
├── ai-rules/                      # [NEW] Правила поведения агента и быстрая синхронизация внешнего агента
├── pr-ops/                        # [NEW] Управление задачами, PR и review; плоско по правилу 2FA
├── standards/                     # Плоские стандарты; provisional = lifecycle status draft/proposed
├── docs/                          # Документация, решения и outputs по типам артефактов
│   ├── adr/                       # ADR decision records
│   ├── rfc/                       # Proposal-stage RFC; target for migrated docs/rfc/
│   ├── analysis/                  # Analysis-артефакты
│   ├── audit/                     # Audit-отчёты и conformance checks
│   ├── report/                    # General reports and statistics
│   ├── guides/                    # Зарезервирован как потенциальный единый дом руководств; целесообразность определяется в задаче B-054
│   └── concept.md                 # Target for current root docs/concept.md
├── research/                      # Доменный research; базовое расширение archetype A
│   ├── hub/                       # Hub methodology and governance research
│   ├── mango/                     # Mango domain research
│   ├── open-ai-ru/                # Open-ai.ru project research
│   ├── reputation-technologies/   # Reputation Technologies research
│   ├── governance/                # Governance research corpus
│   ├── cicd/                      # CI/CD research corpus
│   └── external-knowledge/        # External source registry and derived insights
├── practices/                     # Внешние практики экосистемы; специфика Хаба в корне
│   ├── agent-work/                # Практики AI-assisted work
│   └── ai-governance/             # External AI governance practices, not the policy bucket
├── projects/                      # Проектные споки/подпроекты
│   ├── education-ba-prompt/       # Education BA Prompt spoke materials
│   └── repo-development/          # Repository-development spoke materials
├── projects-sink/                 # [NEW] Управленческий буфер приёма из проектов; плоский intake
├── frameworks/                    # [Зарезервировано] Future home for frameworks after research -> standard confirmation
├── education/                     # [Зарезервировано] Cross-project education materials
├── templates/                     # Копируемые поверхности for HTOM/spoke reuse
│   ├── htom/                      # HTOM team template surface
│   └── spoke/                     # Spoke repository template surface
├── tools/                         # Валидаторы и maintenance utilities
├── .github/                       # CI workflows and issue templates
├── GOVERNANCE.md                  # Target org-governance anchor aligned with AI_GOVERNANCE.md
├── README.md                      # Repository entry point
├── CHANGELOG.md                   # Date-based governance change log
├── CONTRIBUTING.md                # Contribution workflow and local validation commands
├── LICENSE                        # License placeholder until final license decision
├── .gitignore                     # Git ignore rules
└── .gitattributes                 # Optional git attributes anchor if introduced

# Не вводятся в Хаб до явного указания (расхождение с ADR-001): kb/, runs/
# Удалено при миграции: website/, mkdocs.yml, experiments/
```

| Target | Decision |
| --- | --- |
| `projects-sink/` | Создать специфичный для Хаба плоский управленческий буфер приёма материалов из проектов экосистемы. Перенести `projects-sink/AI_PROJECT_CONTEXT-Summary.md` туда при физической миграции. |
| `ai-governance/` | Использовать для политик: ограничения государства, бизнес-правила, информационная безопасность, внешний compliance и другие обязательства уровня политики. |
| `ai-rules/` | Использовать для правил поведения агента и быстрой синхронизации внешнего агента с контекстом проекта. |
| `practices/` | Оставить в корне репозитория как специфичное для Хаба расхождение с ADR-001 `docs/practice/`. |
| `docs/guides/` | Зарезервировать как потенциальный единый дом руководств; целесообразность определяется в задаче B-054. |
| `education/` | Использовать для cross-project education-материалов. Follow-up-стандарт для archetype D может быть добавлен или перенумерован после миграции. |
| `frameworks/` | Зарезервировать как будущий дом для frameworks после подтверждения scope через путь research -> standard. |
| `docs/concept.md` | Использовать как цель для текущего корневого `docs/concept.md`. |
| `kb/`, `runs/` | Не вводить в Хаб. Универсальное ядро ADR-001 содержит эти каталоги, но issue #386 подтвердил отсутствие текущей операционной боли в Хабе. Исключение архетипа A и trigger-based условия пересмотра записаны в `pr-ops/repo-model.md`. |

Удалить или вывести из эксплуатации следующие корневые артефакты при физической
миграции:

| Current artifact | Decision |
| --- | --- |
| `website/` | Вывести из эксплуатации, потому что веб-стратегия Хаба отменена. Хаб не должен превращаться в Portal. |
| `mkdocs.yml` | Вывести из эксплуатации как следствие отмены веб-стратегии Хаба. |
| `experiments/` | Вывести как корневой каталог. Тесты валидаторов переезжают в `tools/`; иного experiment-корпуса там не остаётся. |

Разделить текущую область `governance/` следующим образом:

| Current area | To-Be route |
| --- | --- |
| политики, compliance и внешние ограничения | `ai-governance/` |
| операции PR/task/review | `pr-ops/` |
| RFC-документы | `docs/rfc/` |
| `docs/rfc/` | `docs/rfc/` |

Использовать lifecycle-статус как механизм provisional-стандарта:

- статусы `draft` и `proposed` отмечают provisional-стандарты;
- не создавать `standards/provisional/` сейчас;
- создавать `standards/provisional/` только если review-боль докажет, что
  lifecycle-статуса недостаточно.

Принять следующую стратегию реализации для B-048:

1. Phase 0: принять этот ADR как decision gate B-047.
2. Phase 1: ввести нейтральные целевые якоря без изменения семантики.
3. Phase 2: перенести `docs/rfc/` в `docs/rfc/` с переписыванием ссылок.
4. Phase 3: разделить `governance/` на `ai-governance/`, `ai-rules/`, `pr-ops/`
   и `docs/rfc/`.
5. Phase 4: согласовать все ранее неоднозначные сущности как one task/PR, а не как
   один PR на каталог. Исполнитель запускает валидаторы и cross-reference
   stress-тесты внутри PR до review.
6. Phase 5: синхронизировать валидаторы, artifact-map, repo-model, manifest и
   навигацию в том же PR, что и структурные изменения.
7. Phase 6: стабилизировать алиасы и удалять переходную совместимость только после
   того, как ссылки и реестры доказали стабильность.

Стратегия переписывания ссылок:

- переписывать ссылки в том же PR, что и физический перенос;
- сохранять алиасы или compatibility-заметки до стабилизации cross-references;
- использовать именованные якоря, а не номера разделов;
- обновлять artifact-map, repo-model, валидаторы и другие синхронные реестры в том
  же PR, что и изменения путей.

## Decision Drivers

- B-034 определил источник истины структуры корня как ADR-001 плюс ADR-002, а не
  стандарты Research/Analysis/Audit.
- Решение фаундера уже существует; RFC переоткрыл бы закрытое решение и добавил бы
  review-накладные расходы.
- Хаб должен оставаться инфраструктурным Хабом экосистемы и не должен дрейфовать в
  профиль Web Portal.
- `ai-governance/` и `ai-rules/` нуждаются в стабильной семантической границе до
  переноса файлов, иначе policy/compliance-материал и правила поведения агента
  снова схлопнутся в один bucket.
- Provisional-стандартам нужен механизм с низкой инфляцией; lifecycle-статуса
  достаточно, пока не доказано обратное.
- B-048 нужна единая стратегия реализации, объединяющая переносы, переписывание
  ссылок, алиасы и синхронизацию реестров.

## Alternatives Considered

Этот ADR намеренно не предлагает альтернатив или trade-offs. B-034 зафиксировал
открытые опции, а issue #378 фиксирует решение фаундера, которое их закрывает. В
этом ADR ни одна альтернатива не находится на рассмотрении.

## Consequences

| Backlog item | Consequence |
| --- | --- |
| B-048 | Задача физической миграции после принятия ADR-007/B-047. Она реализует эту целевую структуру и выполняет integrity stress-тест до review. |
| B-054 | Остаётся отложенной до момента после миграции и ремонта standard-desync; stress-тест B-048 — это execution evidence, а не сам будущий стандарт процесса. Также включает исследование целесообразности `docs/guides/` как единого дома руководств. |
| B-055 | Поглощается ADR-007/B-047 для границы `ai-governance/` vs `ai-rules/`. Отдельный post-migration ADR не нужен, если этот ADR позже не будет superseded. |
| B-056 | Использует этот ADR как источник разделения policy/rule при физическом разделении текущего governance-материала. |
| B-057 | Зарезервированный логический follow-up для маршрутизации `docs/guides/`, если миграционная работа потребует отдельной backlog-задачи. |
| B-058 | Зарезервированный логический follow-up для `education/` и стандартизации education archetype D. |
| B-059 | Зарезервированный логический follow-up для подтверждения `frameworks/` через research -> standard. |
| B-060 | Зарезервированный логический follow-up для `docs/concept.md` -> `docs/concept.md`. |
| B-061 | Зарезервированный логический follow-up для `projects-sink/AI_PROJECT_CONTEXT-Summary.md` -> `projects-sink/`. |
| B-062 | Зарезервированный логический follow-up для вывода из эксплуатации `website/`, `mkdocs.yml` и корневого `experiments/`. |
| issue #386: kb/, runs/ applicability | Исследование целесообразности завершено: root `kb/` и `runs/` не вводятся в Хаб; исключение архетипа A и trigger-based условия пересмотра записаны в `pr-ops/repo-model.md`. |

B-057..B-062 названы здесь как слоты последствий, а не как созданные строки
бэклога. Если текущая нумерация бэклога отличается на момент миграции, они могут
быть созданы или перенумерованы без блокировки B-048.

Текущие пути репозитория остаются активными до того, как B-048 выполнит
физическую миграцию. Этот ADR меняет только состояние решения и реестры.

## Impacted Artifacts

| As-Is | To-Be | Impact |
| --- | --- | --- |
| `pr-ops/backlog.md` | future `pr-ops/` backlog area | Текущий бэклог отмечает B-047 как принятый ADR-gate и B-048 как задачу физической миграции. |
| `pr-ops/artifact-map.md` | future registry location governed by B-048 | Текущий artifact-map регистрирует этот ADR и остаётся активной картой до миграции. |
| `pr-ops/repo-model.md` | future synchronized repo model | B-048 обновляет его принятыми целевыми путями. |
| `docs/rfc/` | `docs/rfc/` | Миграция пути RFC происходит в B-048. |
| `AI_GOVERNANCE.md` and policy material | `ai-governance/` | Policy/compliance-материал переносится согласно границе в этом ADR. |
| agent behavior and sync material | `ai-rules/` | Правила поведения агента и quick-sync-контекст переносятся согласно границе в этом ADR. |
| `practices/` | `practices/` | Корневое расположение остаётся принятым для специфичных для Хаба практик. |
| guide material | `docs/guides/` | `docs/guides/` зарезервирован как потенциальный единый дом руководств; целесообразность определяется в задаче B-054. |
| education material | `education/` | Cross-project education-дом принят; стандартизация archetype D остаётся follow-up. |
| framework material | `frameworks/` | Будущий framework-дом принят после подтверждения research -> standard. |
| `docs/concept.md` | `docs/concept.md` | Физический перенос остаётся B-048 или downstream consequence-задачей. |
| `projects-sink/AI_PROJECT_CONTEXT-Summary.md` | `projects-sink/` | Физический перенос остаётся B-048 или downstream consequence-задачей. |
| `kb/`, `runs/` (ADR-001 core) | не вводятся в Хаб | Расхождение с ADR-001 подтверждено issue #386: каталоги универсального ядра не вводятся в Хаб до trigger-based пересмотра в `pr-ops/repo-model.md`. |
| `website/` | removed | Веб-стратегия Хаба отменена. |
| `mkdocs.yml` | removed | Удалён как следствие отмены website. |
| `experiments/` | removed; validator tests in `tools/` | Корневой каталог experiments выводится из эксплуатации. |
| provisional standards | lifecycle status `draft` or `proposed` | `standards/provisional/` не создаётся, пока не появится review-боль. |

## Compliance and Validation

Этот ADR соответствует `standards/adr-structure-standard.md`, используя ADR
frontmatter, обязательные разделы, decision metadata, lifecycle и related
artifacts. Раздел `Alternatives Considered` намеренно закрыт, потому что решение
фаундера уже принято.

Этот PR валидирует decision record и синхронизацию реестров через:

- `./tools/validate-frontmatter.sh .`
- `./tools/validate-file-naming.sh`
- `./tools/validate-repository-structure.sh`

B-048 должен дополнительно валидировать перенесённые ссылки, алиасы, artifact-map,
repo-model, валидаторы, manifest и навигацию в том же PR, что и физическая
миграция.

## Lifecycle

Этот ADR находится в статусе `accepted` после того, как PR #379 был замержен
владельцем репозитория 2026-07-04. B-047 завершён, а B-048 — следующая задача
физической миграции. Issue #382 — доработка принятого ADR: он добавляет
консолидированное To-Be дерево для читаемости и исполнения AI-агентом, не
переоткрывая решение. Issue #385 — доработка v0.3: она приводит целевое дерево в
соответствие с решениями фаундера (изъятие `kb/` и `runs/` с фиксацией расхождения
с ADR-001, уточнение `docs/guides/`, сохранение `GOVERNANCE.md`) и переводит
документ на русский; принятая архитектура не переоткрывается. Issue #386 —
доработка v0.4: она закрывает исследование `kb/`/`runs/`, подтверждает не вводить
root-каталоги в Хаб и синхронизирует exception/trigger модель с
`pr-ops/repo-model.md`. Будущие ADR могут superseded это решение, только называя
scope, который они заменяют.

## Related Artifacts

- [Issue #378](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/378)
- [Issue #382](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/382)
- [Issue #385](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/385)
- [Issue #386](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/386)
- [B-034 migration and root structure plan](../analysis/2026-07-04-hub-migration-and-root-structure-plan.md)
- [kb/runs Hub applicability analysis](../analysis/2026-07-04-kb-runs-hub-applicability-analysis.md)
- [ADR-001: Ecosystem infrastructure methodology](2026-06-adr-001-ecosystem-infrastructure-methodology.md)
- [ADR-002: Artifact/document methodology](2026-06-adr-002-artifact-document-methodology.md)
- [ADR-003: Research structure](2026-07-adr-003-research-structure.md)
- [ADR-004: Reports structure](2026-07-adr-004-reports-structure.md)
- [ADR-005: Audit structure](2026-07-adr-005-audit-structure.md)
- [ADR-006: Analysis structure](2026-07-adr-006-analysis-structure.md)
- [ADR structure standard](../../standards/adr-structure-standard.md)
- [Backlog](../../pr-ops/backlog.md)
- [Artifact map](../../pr-ops/artifact-map.md)
