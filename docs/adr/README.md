---
status: accepted
version: 0.2
updated: 2026-08-17
temperature: 0.1
owner: G-Ivan-A
---

# Architecture Decision Records

Каталог хранит **ADR Хаба** — записи уже принятых человеком решений с rationale,
последствиями и способом проверки. ADR отвечает на вопрос «какое решение принято
и почему», в отличие от [RFC](../rfc/README.md), который отвечает на вопрос
«следует ли принять изменение и как» и остаётся proposal до human decision gate.

Обязательная форма ADR задана
[ADR Structure Standard](../../standards/adr-structure-standard.md): имя файла
`YYYY-MM-adr-NNN-short-title.md`, стабильный id `ADR-NNN`, необходимый
frontmatter и девять обязательных секций. Машиночитаемый canon статуса —
поле `status` во frontmatter; таблица `Decision Metadata` повторяет его только
как narrative summary.

Допустимые переходы: `draft → proposed → accepted → deprecated | superseded`.
Перевод в `accepted` требует явного human review или merge-решения; `superseded`
требует backlink на замещающий decision record.

## Документы

| ADR | Статус | Назначение |
| --- | --- | --- |
| [ADR-001](2026-06-adr-001-ecosystem-infrastructure-methodology.md) | accepted | Методология инфраструктуры проектов экосистемы: универсальное ядро каталогов и расширения по архетипам A–D. |
| [ADR-002](2026-06-adr-002-artifact-document-methodology.md) | accepted | Методология создания и управления артефактами: жизненный цикл research → RFC → ADR → standard/template/tool, canonical routing. |
| [ADR-003](2026-07-adr-003-research-structure.md) | accepted | Структура research, контейнер `exp/` и маршрутизация Research / Analysis / Audit. |
| [ADR-004](2026-07-adr-004-reports-structure.md) | accepted | Структура Reports и routing `docs/report/` / `docs/audit/`. |
| [ADR-005](2026-07-adr-005-audit-structure.md) | accepted | Структура Audit-артефактов и 4-компонентная модель. |
| [ADR-006](2026-07-adr-006-analysis-structure.md) | accepted | Структура Analysis-артефактов и профили подтипов. |
| [ADR-007](2026-07-adr-007-hub-root-structure.md) | accepted | Целевая структура корня Хаба как ADR-001 core + delta архетипа A. |
| [ADR-008](2026-07-adr-008-standard-meta-structure.md) | proposed | Мета-структура стандартов: F10 explicit, десять инвариантных секций и specific tail. |
| [ADR-009](2026-07-adr-009-mango-repo-split.md) | proposed | Разделение Mango на публичный и приватный репозитории. |
| [ADR-010](2026-08-adr-010-agent-autonomy-principles.md) | proposed | Три принципа автономии агента: экспертное исполнение, абсолютные границы и роль Operating Mode как мета-контракта. |
| [ADR-011](2026-08-adr-011-research-models.md) | accepted | Модели research-артефакта: базовый отчёт, RRP и Discussion Paper / Survey для ранней стадии; амендмент D6 повышает статус паттерна RRP до `Validated`. |

## Related Artifacts

- [ADR Structure Standard](../../standards/adr-structure-standard.md) — форма и обязательные секции.
- [docs/rfc/README.md](../rfc/README.md) — proposal-стадия и decision path.
- [AI Governance](../../ai-governance/ai-governance.md) — Amendment policy и права решений.
- [pr-ops/artifact-map.md](../../pr-ops/artifact-map.md) — карта артефактов и связей.
