---
status: draft
version: 0.1
updated: 2026-06-13
temperature: 0.1
type: external-analysis
source_id: ext-001
stage: research
projects: [hub, mango, open-ai.ru, clarify-engine-ai]
context: [agents, workflow-patterns, orchestration, hybrid-collaboration]
---

# Инсайт: простые компонуемые паттерны > монолитные «умные» агенты

**Источник:** `ext-001` —
[Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
(см. [реестр](../external-sources-registry.md)).

## Вывод (атомарно)

Надёжные агентные системы строятся не из одного «универсального» агента, а из
небольшого набора **компонуемых паттернов**: prompt chaining, routing,
parallelization, orchestrator-workers, evaluator-optimizer. Сложность вводится
только тогда, когда более простой паттерн (один LLM-вызов с инструментами)
перестаёт справляться.

## Почему это релевантно экосистеме

- **Прямое совпадение с Anti-Inflation principle** Хаба
  ([governance/repo-model.md](../../../governance/repo-model.md)): «не добавлять
  сложность без операционной боли». Источник формулирует тот же принцип для
  архитектуры агентов.
- Совпадает с нашим разделением **descriptive vs executable** документов
  ([standards/executable-documentation-standard.md](../../../standards/executable-documentation-standard.md)):
  атомарные практики ≈ компонуемые шаги.

## Аргументы за/против

| За | Против / Ограничение |
| --- | --- |
| Паттерны проверены на проде, легко объясняются человеку. | Терминология вендора (Anthropic); нужна провайдер-агностичная переформулировка. |
| Снижают premature complexity — ровно наш принцип. | Не покрывают governance/безопасность — это берут источники `ext-005`, NIST. |

## Путь к практике

- **Кандидат:** практика `practices/agent-work/` — «выбирай простейший
  достаточный паттерн агента» (чек-лист перед усложнением).
- **Для перехода в `candidate-practice`:** провайдер-агностичная формулировка +
  один пример применения в задаче Хаба.
- **Решение о переводе в `practices/` — за человеком.**

## Стадия

`stage: research` — вывод сопоставлен с принципами Хаба, есть аргументы; гипотеза
конкретного применения формулируется при создании practice-кандидата.
