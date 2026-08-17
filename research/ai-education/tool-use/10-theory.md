---
status: draft
version: 0.1
updated: 2026-08-11
temperature: 0.5
---

# Tool Use & Function Calling: теория исполнения

<!-- CROSS-REVIEW [Codex-validation]: P5 RFC (обратная связь «практика → теория»): ссылок на 40-practice-and-cases.md в файле нет, поэтому стрелка «практика → теория» остаётся декоративной. Гипотезы H1–H8 (§7) — сильная сторона модуля и готовое основание для P5: они сформулированы фальсифицируемо и ранжированы в 50-open-research.md §5. Не хватает ровно одного — ссылки из практики на конкретную гипотезу и обратно, чтобы расхождение кейса с H-утверждением было видно как дефект рамки, а не как отдельное наблюдение. Сработавших триггеров P5 в модуле: 0; задач по триггеру в pr-ops/backlog.md нет. -->

## 1. Три независимых слоя

| Слой | Решает | Не решает |
| --- | --- | --- |
| model interface | выбрать tool и сформировать typed arguments | выполнить side effect, проверить бизнес-инвариант |
| protocol/adaptor | discovery, transport, correlation call/result | retry policy, authorization, transaction boundary |
| application runtime | policy, execution, state, recovery, observability | семантический выбор без модели/правила |

OpenAI и Anthropic возвращают структурированный запрос на вызов, после чего
клиент исполняет функцию и возвращает результат модели. MCP помещает инструменты
за унифицированный client-host-server protocol, но его specification прямо
оставляет consent и security control host-приложению. Поэтому «есть function
calling/MCP» не эквивалентно «есть надёжное исполнение»
([OpenAI lifecycle](https://platform.openai.com/docs/guides/function-calling),
[Anthropic lifecycle](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use),
[MCP architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture/index)).

## 2. Эволюция, а не замещение

ReAct чередует reasoning traces и actions, связывая план с наблюдением среды
([Yao et al.](https://openreview.net/forum?id=WE_vluYUL-X)). Native function
calling заменяет хрупкий text parser типизированным каналом, но не устраняет
цикл `decide → act → observe`. MCP не заменяет ни reasoning, ни schema calling:
он делает каталоги инструментов и transport переносимыми.

Практическая эволюция выглядит так:

`text action grammar → provider-native typed call → portable tool protocol →
durable workflow around calls`.

В 2026 году text-only ReAct полезен как conceptual loop и fallback для моделей
без tool API, но не как предпочтительный production wire format. Native calls
доминируют на model boundary; MCP быстро распространяется на integration
boundary, оставаясь развивающимся стандартом, а не reliability layer.

## 3. Вызов как конечный автомат

Каждый intent получает стабильный `operation_id`; каждая попытка — отдельный
`attempt_id` и provider `call_id`.

```text
PROPOSED -> VALIDATED -> AUTHORIZED -> DISPATCHED
                                     -> SUCCEEDED
                                     -> FAILED_RETRYABLE -> DISPATCHED
                                     -> FAILED_FINAL
                                     -> UNKNOWN -> RECONCILE
```

`UNKNOWN` критичен: timeout после отправки не доказывает, что side effect не
произошёл. Для write operation сначала нужен status/reconciliation либо
idempotency key, а не слепой повтор. Stripe описывает этот общий API-паттерн:
одинаковый idempotency key возвращает результат первой операции
([Stripe](https://docs.stripe.com/api/idempotent_requests)).

## 4. Контракт инструмента

Надёжный контракт шире JSON Schema:

- имя, назначение и минимальная input/output schema;
- read/write/destructive class и required scope;
- preconditions, postconditions и domain error codes;
- timeout budget, rate/cost weight и concurrency limit;
- idempotency/commutativity/transaction semantics;
- PII/secrets boundary и audit fields;
- result size, provenance и freshness;
- cancellation и compensation capability.

`strict` schema снижает invalid arguments, но не проверяет, существует ли
указанный объект, разрешено ли действие и правдив ли результат. MCP annotations
также нельзя считать доверенными без доверия к server
([MCP tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)).

## 5. Ошибка как данные

Модели полезнее компактный нормализованный результат, чем stack trace:

```json
{
  "status": "error",
  "code": "RATE_LIMITED",
  "retryable": true,
  "retry_after_ms": 1200,
  "safe_message": "source endpoint temporarily unavailable",
  "operation_id": "op-123"
}
```

Необработанное исключение теряет возможность recovery; передача секретов и
внутренних трасс модели расширяет attack surface. Anthropic предусматривает
`is_error` у `tool_result`; MCP допускает protocol errors и structured tool
results. Семантика retry всё равно определяется приложением
([Anthropic](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use),
[MCP tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)).

## 6. Planner и executor

Одна модель + deterministic executor достаточны, когда каталог мал, горизонт
короток, side effects обратимы и результат проверяется сразу. Отдельный planner
полезен при длинном DAG, дорогих вызовах, специализации моделей или необходимости
утвердить план до исполнения. Он добавляет новую границу рассогласования:
устаревший state, потерянные constraints, incompatible tool names и стоимость
двух inference loops.

MAST классифицирует 14 multi-agent failure modes на 1600+ traces; 36.9% failures
в его корпусе относятся к межагентному рассогласованию. Это эмпирический сигнал
для данного benchmark, а не универсальная вероятность отказа
([MAST](https://arxiv.org/abs/2503.13657)). Поэтому разделение вводится после
измеренного bottleneck, а не как default.

## 7. Проверяемые гипотезы

- H1: strict schema снижает syntax failures, но не semantic/tool-selection errors.
- H2: operation-level idempotency снижает duplicate side effects при timeout.
- H3: dependency-aware parallelism уменьшает latency без роста write conflicts.
- H4: bounded retry улучшает completion только для transient class ошибок.
- H5: отдельный planner окупается лишь при длинных/дорогих trajectories.
- H6: tool result normalization повышает recovery и снижает context cost.
- H7: allowlist + least privilege эффективнее prompt-only запрета.
- H8: stage-specific deterministic checks локализуют дефект лучше final answer score.
