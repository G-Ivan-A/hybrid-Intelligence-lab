---
status: canonical
version: 1.2
updated: 2026-06-12
temperature: 0.1
---

# Governance RFC

Каталог хранит **RFC Хаба** — предложения по изменению governance (правил,
структуры, контрактов) до принятия решения человеком. «RFC» (Request for
Comments) — отраслевой термин IETF: документ, выносимый на обсуждение и решение,
а не уже принятая норма.

RFC - это рекомендация или proposal, а не блокирующее правило. Даже canonical
RFC фиксирует принятое решение и rationale, но обязательная норма должна быть
делегирована в active artifact: standard, policy, template, validator или
операционный контракт. До такой делегации downstream-репозиторий может ссылаться
на RFC как на обоснование, но не обязан выполнять его механически.

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
[standards/project-structure-inheritance.md](../../standards/project-structure-inheritance.md)).

## Документы

| RFC | Назначение |
| --- | --- |
| [rfc-two-cases-of-project-initialization.md](rfc-two-cases-of-project-initialization.md) | Разделение двух кейсов инициализации: Runtime-онбординг (Кейс 1) и Bootstrap-клонирование (Кейс 2). |
| [contract-executability-rfc.md](contract-executability-rfc.md) | Архитектура исполнимых документов: маркер `executable: true\|false`, директивные блоки, план внедрения и решения фаундера. |
| [repository-quality-improvement-plan.md](repository-quality-improvement-plan.md) | Комплексный аудит качества репозитория после PR #170: naming, дубли, metadata, traceability, drafts, archive Mango и phased cleanup plan. |
| [draft-triage-and-exit-plan.md](draft-triage-and-exit-plan.md) | Триаж 20 draft-документов категории "К доработке": группы template/hub/Mango/education, exit plans, phased cleanup и вопросы к Founder/PO. |
| [hub-vision-concept-proposal-2026-06.md](hub-vision-concept-proposal-2026-06.md) | Vision (L1) и Concept (L2) Хаба, библиотека гайдов и публикация MkDocs: сравнение подходов, обоснование и вопросы к фаундеру (Draft, единый пакет). |

## Связанные артефакты

- [governance/artifact-map.md](../artifact-map.md) — карта артефактов и связей.
- [governance/repo-model.md](../repo-model.md) — модель структуры и Anti-Inflation principle.
- [research/governance/governance-folder-structure-decisions-2026-06.md](../../research/governance/governance-folder-structure-decisions-2026-06.md) — решения Q1/Q2/Q3.
