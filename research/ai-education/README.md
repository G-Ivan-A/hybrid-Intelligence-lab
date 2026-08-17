---
status: draft
version: 0.9
updated: 2026-08-17
temperature: 0.1
---

# AI Education — модульные исследования

Этот каталог содержит AI-специфичные исследования, организованные по
экспериментальному Reference Research Pattern:
`[00-introduction, 10-theory, 20-taxonomy, 30-decision-framework,
40-practice-and-cases, 50-open-research]`.

Общие образовательные исследования, которым такая модульная структура не
нужна, остаются в [`research/education/`](../education/README.md).

## Модули

- [`retrieval/`](retrieval/00-introduction.md) — первая валидация паттерна;
- [`task-processing/`](task-processing/00-introduction.md) — вторая валидация
  паттерна: агентное исполнение задач (мандаты, автономное планирование,
  guardrails);
- [`memory/`](memory/00-introduction.md) — третья валидация паттерна: память
  AI-агентов (контуры чтения и записи, жизненный цикл, забывание,
  темпоральность). Модуль содержит образовательный срез для бизнес-аналитиков
  (Приложение A в [`40-practice-and-cases.md`](memory/40-practice-and-cases.md)).
- [`information-extraction-graph-modeling/`](information-extraction-graph-modeling/00-introduction.md)
  — четвёртая валидация паттерна: извлечение структурированных знаний,
  нормализация сущностей и моделирование графа. Модуль содержит образовательный
  срез для бизнес-аналитиков (Приложение A в
  [`40-practice-and-cases.md`](information-extraction-graph-modeling/40-practice-and-cases.md)).
- [`evaluation/`](evaluation/00-introduction.md) — пятая валидация паттерна:
  метрики RAG/extraction/graph/agent tasks, LLM-as-judge, golden sets,
  risk-based thresholds, сравнение eval-фреймворков и образовательный срез для
  бизнес-аналитика. Прикладной [evals-контракт Source Intelligence
  Engine](evaluation/2026-08-11-source-intelligence-evals-contract.md)
  переводит модуль в план локального эксперимента и handoff для B-068 без
  назначения числовых acceptance thresholds.
- [`tool-use/`](tool-use/00-introduction.md) — шестая валидация паттерна:
  typed function calling, MCP, execution/recovery patterns, planner/executor,
  framework comparison и интеграция в Source Intelligence Engine.
- [`observability/`](observability/00-introduction.md) — седьмая валидация
  паттерна: наблюдаемость и трейсинг AI-агентов (таксономия сигналов, паттерны
  трейсинга многошаговых выполнений, стоимость наблюдения против стоимости
  отладки, сравнение платформ, интеграция в конвейер Source Intelligence Engine
  и общеобразовательный разрез для всех ролей).
- [`multi-agent-orchestration/`](multi-agent-orchestration/00-introduction.md) —
  восьмая валидация паттерна: таксономия паттернов оркестрации, механизмы
  координации и разрешения конфликтов, cost-benefit мультиагентности,
  сравнение фреймворков и протоколов, встраивание в конвейер Source
  Intelligence Engine. Образовательный срез — общий для всех ролей
  (§2 в [`50-open-research.md`](multi-agent-orchestration/50-open-research.md)).
- [`agent-context-engineering/`](agent-context-engineering/00-introduction.md) —
  девятая валидация паттерна: граница «Человек → Агент». Контекст как конечный
  бюджет окна, блоки входа B1–B7, таксономия приёмов инструкции, стратегий
  подачи знаний и вытеснения, измеримые пороги выбора подхода, ландшафт
  фреймворков и зрелость работы с промптом как артефактом.

Описание паттерна, его ограничений и критерия повышения статуса находится в
[RFC Reference Research Pattern](../../docs/rfc/2026-07-17-rfc-reference-research-pattern.md).
