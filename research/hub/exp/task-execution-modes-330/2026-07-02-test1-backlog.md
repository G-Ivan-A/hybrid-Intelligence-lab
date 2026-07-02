---
status: draft
version: 0.1
updated: 2026-07-02
temperature: 0.1
type: experiment-output
---

# Test 1 — классификация задач бэклога (B-016..B-039)

> Evidence for [research report](../../2026-07-02-task-execution-modes-research.md), issue [#330](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/330). Regenerate with `python3 research/hub/exp/task-execution-modes-330/classify.py`.

Классификатор видит формулировку **без** типового префикса (симуляция «без контекста»).

- Тип, v1 (наивный keyword-vote): **8/18** (44%).
- Тип, v2 (action-anchored): **17/18** (94%).
- Режим (из типа v2 + детектор конфликта): **17/18** (94%).

`*` — v2 не нашёл action-сигнал: формулировка under-specified, тип угадан наивным голосованием.

| ID | Вход (усечён) | GT тип | v1 тип | v1? | v2 тип | v2? | Режим | M? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B-016 | Структура research, контейнер exp/ и маршрутиз | RFC | Audit | ❌ | Audit* | ❌ | Structured | ❌ |
| B-017 | Принять стандарт структуры research | ADR | Research | ❌ | ADR | ✅ | Hybrid | ✅ |
| B-018 | Создать standards/research-standard.md как ста | Standard | Standard | ✅ | Standard | ✅ | Hybrid | ✅ |
| B-020 | Обновить standards/glossary.md: Research / Ana | Chore | Audit | ❌ | Chore | ✅ | Structured | ✅ |
| B-021 | Удалить standards/research-profile.md после за | Chore | Research | ❌ | Chore | ✅ | Structured | ✅ |
| B-022 | Мигрировать существующие exp-* в контейнер exp | Chore | Chore | ✅ | Chore | ✅ | Structured | ✅ |
| B-023 | Обновить валидатор структуры под exp/ и routin | Chore | Chore | ✅ | Chore | ✅ | Structured | ✅ |
| B-024 | Сквозной анализ артефактов Analysis (Хаб, Mang | Analysis | Analysis | ✅ | Analysis | ✅ | Creative | ✅ |
| B-025 | Стандарт структуры Analysis | RFC | Analysis | ❌ | RFC | ✅ | Creative | ✅ |
| B-026 | Принятие analysis-standard | ADR | Analysis | ❌ | ADR | ✅ | Hybrid | ✅ |
| B-027 | Создание standards/analysis-standard.md | Standard/Chore | Standard | ✅ | Standard | ✅ | Hybrid | ✅ |
| B-028 | Cleanup и модернизация Analysis-артефактов | Chore | Analysis | ❌ | Chore | ✅ | Structured | ✅ |
| B-029 | Сквозной анализ артефактов Audit (Хаб, Mango,  | Analysis | Analysis | ✅ | Analysis | ✅ | Creative | ✅ |
| B-030 | Стандарт структуры Audit | RFC | Audit | ❌ | RFC | ✅ | Creative | ✅ |
| B-032 | Создание standards/audit-standard.md | Standard/Chore | Standard | ✅ | Standard | ✅ | Hybrid | ✅ |
| B-034 | План миграции репо Хаба после стандартов Resea | RFC | Audit | ❌ | RFC | ✅ | Creative | ✅ |
| B-038 | Инвентаризация и границы Reports-артефактов (а | Analysis | Audit | ❌ | Analysis | ✅ | Creative | ✅ |
| B-039 | Проверка документации на коллизии интерпретаци | Audit | Audit | ✅ | Audit | ✅ | Structured | ✅ |
