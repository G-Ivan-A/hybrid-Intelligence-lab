---
name: ba-debug-orchestrator
description: >-
  Явно запускай для безопасной диагностики графа на mock-данных; все следы
  создаются только в изолированном runs/DEBUG-<TIMESTAMP>/.
priority: low
disable-model-invocation: true
packs: ORCH/DEBUG
interaction: human-checkpointed
inputs: [DEBUG-SCENARIO]
outputs: [DEBUG-TRACE, DEBUG-REPORT]
contracts: [C-RK]
gates: [G-self, G-mach, G-human]
compiled_from: { package: execution-package-gigacode-cli, mode: debug }
derived_from: [routes/rg-bcreq-v1.yaml, contracts/c-rk.schema.json]
compiled_at: 2026-09-21
status: draft
version: 1.0
updated: 2026-09-21
temperature: 0.1
---

# Изолированный debug-оркестратор

## Когда применять

Применяй только после явной команды `/skills ba-debug-orchestrator`, когда
нужно проверить маршрутизацию, гейт или журнал без исполнения предметной задачи.

## Предусловия

1. Сценарий использует mock-входы и не содержит пользовательских данных.
2. Назначен новый UTC timestamp формата `YYYYMMDDTHHMMSSZ`.
3. MCP и любые необратимые внешние действия отключены.

## Шаги

1. Создай единственный корень `runs/DEBUG-<TIMESTAMP>/`; не создавай
   `TASK-NNNN` и не открывай существующие task runs.
2. Скопируй mock-вход сценария в debug-корень и запиши его digest.
3. Эмулируй разрешённые рёбра `routes/rg-bcreq-v1.yaml`, сохраняя каждое
   микро-событие и результат гейта. Не вызывай LLM и внешние системы.
4. При human gate создай читаемый Markdown checkpoint, зафиксируй состояние
   `awaiting-human` и остановись.
5. Сохрани `DEBUG-REPORT.md` с воспроизведением, фактической траекторией и
   расхождением. Ничего не переносится в production run автоматически.

## Обязательные слоты выхода

- `runs/DEBUG-<TIMESTAMP>/events.yaml` — последовательный debug trace.
- `runs/DEBUG-<TIMESTAMP>/DEBUG-REPORT.md` — человекочитаемый отчёт.
- `runs/DEBUG-<TIMESTAMP>/evidence/*.md` — checkpoints, если они возникли.

## Самопроверка (G-self)

- Все записи находятся под одним `runs/DEBUG-<TIMESTAMP>/` — да/нет.
- Ни один `runs/TASK-NNNN/` не создан и не изменён — да/нет.
- LLM, MCP и внешние записи не вызывались — да/нет.
- Траектория состоит только из рёбер канонического графа — да/нет.

## Отказ

Остановись до исполнения, если сценарий требует реальных данных, внешнего
вызова, записи вне debug-корня или изменения production run. Диагностика не
расширяет полномочия и не маскируется идентификатором `TASK-NNNN`.
