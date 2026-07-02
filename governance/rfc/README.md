---
status: accepted
version: 1.15
updated: 2026-07-02
temperature: 0.1
owner: G-Ivan-A
---

# Governance RFC

Каталог хранит **RFC Хаба** — предложения по изменению governance (правил,
структуры, контрактов) до принятия решения человеком. «RFC» (Request for
Comments) — отраслевой термин IETF: документ, выносимый на обсуждение и решение,
а не уже принятая норма.

RFC - это рекомендация или proposal, а не блокирующее правило. Даже accepted RFC
фиксирует принятое решение и rationale, но обязательная норма должна быть
делегирована в active artifact: standard, policy, template, validator или
операционный контракт. До такой делегации downstream-репозиторий может ссылаться
на RFC как на обоснование, но не обязан выполнять его механически.

Каталог переименован из `governance/proposals/` в `governance/rfc/` по
[issue #165](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/165)
(Q1): имя `rfc/` точнее отражает содержимое (файлы `*-rfc.md`) и устраняет
рассогласование «каталог `proposals/` ↔ файлы `*-rfc.md`». Обоснование и учёт
мнения команды Q — в
[research/governance/2026-06-06-governance-folder-structure-decisions.md](../../research/governance/2026-06-06-governance-folder-structure-decisions.md).

## Что сюда попадает

- **RFC изменения governance Хаба** — правил, структуры, контрактов, шаблонов.
- **НЕ сюда:** концепция или исследование конкретного проекта — это
  `research/{project}/` (см. Q2 в
  [decision record](../../research/governance/2026-06-06-governance-folder-structure-decisions.md)).

Решение по каждому RFC (принять/отклонить/доработать) — за человеком
([AI_GOVERNANCE.md](../../AI_GOVERNANCE.md), правило 4). Статус каталога —
**опциональный, создаётся по необходимости** (Anti-Inflation): проект без
собственных RFC не обязан держать пустой `rfc/` (см. Q3 и
[standards/project-structure-inheritance.md](../../standards/project-structure-inheritance.md)).

## Документы

| RFC | Назначение |
| --- | --- |
| [rfc-two-cases-of-project-initialization.md](rfc-two-cases-of-project-initialization.md) | Разделение двух кейсов инициализации: Runtime-онбординг (Кейс 1) и Bootstrap-клонирование (Кейс 2). |
| [contract-executability-rfc.md](contract-executability-rfc.md) | Архитектура исполнимых документов: маркер `executable: true\|false`, директивные блоки, план внедрения и решения Пользователя. |
| [repository-quality-improvement-plan.md](repository-quality-improvement-plan.md) | Комплексный аудит качества репозитория после PR #170: naming, дубли, metadata, traceability, drafts, archive Mango и phased cleanup plan. |
| [draft-triage-and-exit-plan.md](draft-triage-and-exit-plan.md) | Триаж 20 draft-документов категории "К доработке": группы template/hub/Mango/education, exit plans, phased cleanup и вопросы к Пользователю. |
| [hub-vision-concept-proposal-2026-06.md](hub-vision-concept-proposal-2026-06.md) | Vision (L1) и Concept (L2) Хаба, библиотека гайдов и публикация MkDocs: сравнение подходов, обоснование и вопросы к Пользователю (Draft, единый пакет). |
| [knowledge-lifecycle-proposal.md](knowledge-lifecycle-proposal.md) | Proposal для стандарта жизненного цикла знаний: Observation -> Research -> Hypothesis -> RFC -> Pattern -> Standard -> Template -> Framework -> Deprecation/Archive. |
| [resolve-artifact-location-proposal.md](resolve-artifact-location-proposal.md) | Proposal для executable resolver prompt, который выбирает каталог и фиксирует lifecycle gaps. |
| [product-concept-template-proposal.md](product-concept-template-proposal.md) | Proposal для универсального L2 Product Concept template, отделённого от webportal-специализации. |
| [solution-concept-template-proposal.md](solution-concept-template-proposal.md) | Proposal для универсального L3 Solution Concept template, отделённого от webportal-специализации. |
| [external-knowledge-integration.md](external-knowledge-integration.md) | Механизм интеграции внешних знаний: Base Registry (Хаб) + Local Extension (проекты) + Smart Sync, привязка к knowledge lifecycle и применение для 4 проектов экосистемы (Anti-Inflation, без CI-скраперов). |
| [documentation-architecture-balance.md](documentation-architecture-balance.md) | Баланс Anti-Inflation vs атомарность: рамка уровней детализации Index → Summary → Full, классификация документов (макс. 3 класса) с критериями и переходами, гибкая навигация без новой инфраструктуры и решения для 4 проектов экосистемы. |
| [repository-archetypes-template-release.md](repository-archetypes-template-release.md) | Таксономия архетипов репозиториев экосистемы, Project Template для Prompt & Pattern Library, правило Governance sync и Release Engineering strategy GitHub Flow + trunk discipline. |
| [research-memory-source-intelligence.md](research-memory-source-intelligence.md) | Framework Research Memory & Source Intelligence: Knowledge Object primacy поверх Tier 1 external sources, Tier 2 internal research memory, статусы `Observed` / `Candidate` / `Applied` / `Rejected` / `Superseded`, критерии source intelligence и traceability-схема `Knowledge Object → Sources → RFC/ADR → Consumer`. |
| [methodology-research-and-proposals.md](methodology-research-and-proposals.md) | Исследование шести методологий (Enterprise Intelligence, Opportunity Discovery, Human-AI Collaboration, Trust & Evidence, Influence & Network Analysis, AI Solution Architecture) с внешними источниками; сравнение с PR #242/#243/#244; подтверждение предложения фаундера (BA-классификация, шаблон AI Solution Architecture, ось доверия E0–E4); три независимых предложения (Хаб/Mango/Open-AI) с уровнями L3/L4 и модель консистентности. |
| [2026-06-27-rfc-adr-standard.md](2026-06-27-rfc-adr-standard.md) | Accepted RFC стандарта структуры ADR: rationale для [ADR Structure Standard](../../standards/adr-structure-standard.md), базовая модель decision record, identification, frontmatter, body sections, lifecycle, A/B/C/D дельты, Critical Analysis и boundary RFC/ADR. |
| [2026-06-27-rfc-rfc-standard.md](2026-06-27-rfc-rfc-standard.md) | Accepted RFC стандарта структуры RFC: rationale для [RFC Structure Standard](../../standards/rfc-structure-standard.md), proposal structure, frontmatter, metadata, Open Questions cleanup, lifecycle, A/B/C/D дельты, Critical Analysis и boundary RFC/ADR. |
| [2026-06-30-rfc-research-structure.md](2026-06-30-rfc-research-structure.md) | Accepted RFC структуры research: единый контейнер `exp/`, запрет вложенного `outputs/` (плоская структура внутри `exp/<issue-slug>/`), граница `exp/` (research evidence) vs `runs/` (operational run record), маршрутизация Research / Analysis / Audit по типу задачи, эвристики классификации, переходный режим legacy `exp-*` и последствия для цепочки B-017..B-023. |

## Связанные артефакты

- [governance/artifact-map.md](../artifact-map.md) — карта артефактов и связей.
- [governance/repo-model.md](../repo-model.md) — модель структуры и Anti-Inflation principle.
- [research/governance/2026-06-06-governance-folder-structure-decisions.md](../../research/governance/2026-06-06-governance-folder-structure-decisions.md) — решения Q1/Q2/Q3.
