---
status: draft
version: 0.1
updated: 2026-06-06
ai-generated: true
type: navigation
scope: repo-wide
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/165"
---

# Governance RFC

Каталог хранит **RFC Хаба** — предложения по изменению governance (правил,
структуры, контрактов) до принятия решения человеком. «RFC» (Request for
Comments) — отраслевой термин IETF: документ, выносимый на обсуждение и решение,
а не уже принятая норма.

Каталог переименован из `governance/proposals/` в `governance/rfc/` по
[issue #165](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/165)
(Q1): имя `rfc/` точнее отражает содержимое (файлы `*-rfc.md`) и устраняет
рассогласование «каталог `proposals/` ↔ файлы `*-rfc.md`». Обоснование и учёт
мнения команды Q — в
[research/governance/governance-folder-structure-decisions-2026-06.md](../../research/governance/governance-folder-structure-decisions-2026-06.md).

## Что сюда попадает

- **RFC изменения governance Хаба** — правил, структуры, контрактов, шаблонов.
- **НЕ сюда:** концепция или исследование конкретного проекта — это
  `research/{project}/` (см. Q2 в
  [decision record](../../research/governance/governance-folder-structure-decisions-2026-06.md)).

Решение по каждому RFC (принять/отклонить/доработать) — за человеком
([AI_GOVERNANCE.md](../../AI_GOVERNANCE.md), правило 4). Статус каталога —
**опциональный, создаётся по необходимости** (Anti-Inflation): проект без
собственных RFC не обязан держать пустой `rfc/` (см. Q3 и
[standards/PORTAL_REPOSITORY_STRUCTURE.md](../../standards/PORTAL_REPOSITORY_STRUCTURE.md)).

## Документы

| RFC | Назначение |
| --- | --- |
| [rfc-creative-template-design.md](rfc-creative-template-design.md) | «ДНК-шаблон» для клонирования spoke-проектов: аналогия, сравнительная матрица имён, карта файлов, Mermaid-схема. |
| [rfc-agent-onboarding-protocol.md](rfc-agent-onboarding-protocol.md) | «Протокол бесшовной передачи проекта»: Handover Prompt, 4-шаговый алгоритм агента, выбор места для `AGENT_ONBOARDING.md`. |
| [rfc-two-cases-of-project-initialization.md](rfc-two-cases-of-project-initialization.md) | Разделение двух кейсов инициализации: Runtime-онбординг (Кейс 1) и Bootstrap-клонирование (Кейс 2). |
| [contract-executability-rfc.md](contract-executability-rfc.md) | Архитектура исполнимых документов: маркер `executable: true\|false`, директивные блоки, план внедрения и решения фаундера. |

## Связанные артефакты

- [governance/ARTIFACT_MAP.md](../ARTIFACT_MAP.md) — карта артефактов и связей.
- [governance/REPO_MODEL.md](../REPO_MODEL.md) — модель структуры и Anti-Inflation principle.
- [research/governance/governance-folder-structure-decisions-2026-06.md](../../research/governance/governance-folder-structure-decisions-2026-06.md) — решения Q1/Q2/Q3.
