---
status: draft
version: 0.3
updated: 2026-07-31
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

Описание паттерна, его ограничений и критерия повышения статуса находится в
[RFC Reference Research Pattern](../../docs/rfc/2026-07-17-rfc-reference-research-pattern.md).
