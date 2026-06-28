---
status: canonical
version: 1.0
updated: 2026-06-04
temperature: 0.1
type: registry
context: [governance, contracts, executable-documents, issues, sprint-3]
method: structured-issue-generation
scope: repo-wide
source: governance/rfc/contract-executability-rfc.md
related_artifacts:
  - "governance/rfc/contract-executability-rfc.md"
  - "governance/backlog.md"
  - "standards/glossary.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/133"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/138"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/139"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/140"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/141"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/142"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/143"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/144"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/145"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/146"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/147"
---

# Реестр issues: внедрение стандарта исполнимых документов

Источник: [`governance/rfc/contract-executability-rfc.md`](rfc/contract-executability-rfc.md),
раздел 6.1 «Файлы, подлежащие обновлению».

Этот реестр фиксирует GitHub Issues, созданные по issue
[#133](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/133) для
внедрения стандарта исполнимых документов. Принцип RFC сохранён: одна задача
соответствует одному файлу. Строка RFC с двумя стандартами разделена на две
отдельные задачи: `CE-006` и `CE-007`.

> Примечание по GitHub metadata: метки и milestone зафиксированы в теле каждой
> созданной задачи. Автоматическое применение GitHub labels и milestone требует
> maintainer-доступа к upstream-репозиторию.

## Сводная таблица

| ID | Issue | Файл | Приоритет | Зависимости | Статус |
| --- | --- | --- | --- | --- | --- |
| CE-001 | [#138](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/138) | `governance/agent-onboarding-protocol.md` | P0 | CE-008 | TODO |
| CE-002 | [#139](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/139) | `templates/htom/AI_QUICK_RULES.md` | P0 | CE-008 | TODO |
| CE-003 | [#140](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/140) | `templates/htom/AI_SESSION_HANDOVER_PROMPT.md` | P1 | CE-001, CE-008 | TODO |
| CE-004 | [#141](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/141) | `AI_GOVERNANCE.md` | P1 | CE-001, CE-008 | TODO |
| CE-005 | [#142](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/142) | `governance/repo-model.md` | P2 | CE-008 | TODO |
| CE-006 | [#143](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/143) | `standards/project-structure-inheritance.md` | P3 | CE-008 | TODO |
| CE-007 | [#144](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/144) | `standards/issue-workflow.md` | P3 | CE-008 | TODO |
| CE-008 | [#145](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/145) | `standards/glossary.md` | P1 | — | TODO |
| CE-009 | [#146](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/146) | `tools/validate-frontmatter.sh` | P2 | CE-008 | TODO |
| CE-010 | [#147](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/147) | `governance/artifact-map.md` | P2 | CE-001, CE-002, CE-003, CE-004, CE-008 | TODO |

## Обязательные метки

Каждая задача создана с требованием следующих меток в теле issue:

| ID | Метки |
| --- | --- |
| CE-001 | `contracts`, `refactoring`, `executable-documents`, `priority:P0` |
| CE-002 | `contracts`, `refactoring`, `executable-documents`, `priority:P0` |
| CE-003 | `contracts`, `refactoring`, `executable-documents`, `priority:P1` |
| CE-004 | `contracts`, `refactoring`, `executable-documents`, `priority:P1` |
| CE-005 | `contracts`, `refactoring`, `executable-documents`, `priority:P2` |
| CE-006 | `contracts`, `refactoring`, `executable-documents`, `priority:P3` |
| CE-007 | `contracts`, `refactoring`, `executable-documents`, `priority:P3` |
| CE-008 | `contracts`, `refactoring`, `executable-documents`, `priority:P1` |
| CE-009 | `contracts`, `refactoring`, `executable-documents`, `priority:P2` |
| CE-010 | `contracts`, `refactoring`, `executable-documents`, `priority:P2` |

## Проверка полноты

- [x] RFC §6.1 изучен.
- [x] Файлы сверх RFC §6.1 не добавлены в план задач.
- [x] Комбинированная строка стандартов из RFC §6.1 разделена по принципу
      «один issue = один файл».
- [x] Созданы отдельные issues CE-001..CE-010.
- [x] Все URLs созданных issues зафиксированы в этом реестре.
- [x] Сводная таблица добавлена в [`governance/backlog.md`](backlog.md).
