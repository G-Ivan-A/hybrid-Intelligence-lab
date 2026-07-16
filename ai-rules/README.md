---
status: canonical
version: 1.2
updated: 2026-07-16
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
| [agent-work-rules.md](agent-work-rules.md) | Основной контракт поведения агента: pre-flight, operating modes и Definition of Done. |
| [agent-onboarding-protocol.md](agent-onboarding-protocol.md) | Протокол онбординга и синхронизации AI-агента. |
| [adversarial-stress-testing.md](adversarial-stress-testing.md) | Повторяемая процедура проверки гипотез и решений попыткой опровержения. |

## Граница

| Сюда | Не сюда |
| --- | --- |
| Правила поведения агента, onboarding, быстрая синхронизация. | Политики уровня организации, compliance, ИБ — они в [ai-governance/](../ai-governance/README.md). |
