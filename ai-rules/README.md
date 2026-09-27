---
status: canonical
version: 1.3
updated: 2026-09-27
temperature: 0.1
---

# AI Rules

Дом правил поведения AI-агента и быстрой синхронизации внешнего агента:
onboarding-протокол и операционные инструкции агента. Граница `ai-rules/` vs
`ai-governance/` зафиксирована в
[ADR-007](../docs/adr/2026-07-adr-007-hub-root-structure.md).

## Содержимое

| Артефакт | Назначение |
| --- | --- |
| [agent-work-rules.md](agent-work-rules.md) | Контракт исполнения: pre-flight, стратегическая проверка, режимы, Creative-протокол и Definition of Done. |
| [agent-collaboration-rules.md](agent-collaboration-rules.md) | Правила коммуникации агента с автором и ревьюером. |
| [agent-onboarding-protocol.md](agent-onboarding-protocol.md) | Протокол онбординга и неблокирующие якоря синхронизации. |
| [adversarial-stress-testing.md](adversarial-stress-testing.md) | Повторяемая процедура проверки гипотез и решений попыткой опровержения. |

## Граница

| Сюда | Не сюда |
| --- | --- |
| Правила поведения агента, onboarding, быстрая синхронизация. | Политики уровня организации, compliance, ИБ — они в [ai-governance/](../ai-governance/README.md). |
