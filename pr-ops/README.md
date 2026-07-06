---
status: canonical
version: 1.0
updated: 2026-07-04
temperature: 0.1
---

# PR-Ops

Дом операционного управления задачами, pull request'ами и review: active
backlog, правила его ведения, карта артефактов, модель репозитория и
операционные реестры. Граница
`pr-ops/` зафиксирована в
[ADR-007](../docs/adr/2026-07-adr-007-hub-root-structure.md).

## Содержимое

| Артефакт | Назначение |
| --- | --- |
| [backlog.md](backlog.md) | Active backlog: незавершённые задачи (B-XXX), сгруппированные в логические спринты. |
| [backlog-instruction.md](backlog-instruction.md) | Правила ведения backlog, статусы, lifecycle, sprint format и policy отсутствующих фактов. |
| [artifact-map.md](artifact-map.md) | Карта артефактов репозитория. |
| [repo-model.md](repo-model.md) | Правила структуры и Anti-Inflation principle. |
| [session-digests.md](session-digests.md) | Дайджесты рабочих сессий. |
| [executable-documents-issues.md](executable-documents-issues.md) | Реестр executable-документов и issues. |

## Граница

| Сюда | Не сюда |
| --- | --- |
| Управление задачами, PR и review; операционные реестры Hub. | Политики уровня организации — они в [ai-governance/](../ai-governance/README.md). |
| Backlog, backlog instruction, artifact-map, repo-model, дайджесты. | Правила поведения AI-агента — они в [ai-rules/](../ai-rules/README.md). |
