---
status: canonical
version: 1.2
updated: 2026-07-16
temperature: 0.1
---

# AI Governance

Дом политик уровня организации: ограничения государства, бизнес-правила,
информационная безопасность, внешний compliance и другие обязательства уровня
политики. Граница `ai-governance/` vs `ai-rules/` зафиксирована в
[ADR-007](../docs/adr/2026-07-adr-007-hub-root-structure.md).

## Граница

| Сюда | Не сюда |
| --- | --- |
| Политики, compliance, внешние ограничения, ИБ, бизнес-правила уровня политики. | Правила поведения агента и быстрая синхронизация внешнего агента — они в [ai-rules/](../ai-rules/). |
| Обязательства уровня политики. | Внешние практики AI-governance экосистемы — они в [practices/ai-governance/](../practices/ai-governance/README.md). |

## Содержимое

| Артефакт | Назначение |
| --- | --- |
| [ai-governance.md](ai-governance.md) | Основной policy-контракт: роли, human decision rights, ограничения и эскалация. |
| [agent-security-checklist.md](agent-security-checklist.md) | Единый risk-based checklist и трасса покрытия OWASP LLM Top 10:2025 / SAIF для agent work. |

## Статус

Policy/compliance-материал физически размещается здесь по ADR-007. Новые
политики добавляются через issue -> PR -> human review.
