---
status: draft
version: 0.1
updated: 2026-08-11
temperature: 0.5
---

# Tool Use & Function Calling: таксономия

## 1. По механизму интерфейса

| Тип | Сильная сторона | Ограничение |
| --- | --- | --- |
| text/ReAct action | provider-neutral, видимый reasoning loop | brittle parser, слабая schema guarantee |
| native function/tool call | typed arguments, call IDs, parallel call support | vendor message model; execution вне API |
| built-in provider tool | минимум integration work | hosted boundary, cost/data/provider coupling |
| MCP tool | discovery и переносимость client/server | host всё равно реализует trust и reliability |
| framework wrapper | graph/state/middleware/observability | дополнительная abstraction и version drift |
| workflow activity | durable retry/state/timers | больше infrastructure, model loop надо встроить |

Эти типы компонуются: native call может выбрать MCP tool, который executor
запускает как durable activity.

## 2. По времени и зависимости

| Режим | Критерий | Пример |
| --- | --- | --- |
| synchronous | caller ждёт короткий bounded result | schema lookup |
| asynchronous | операция длительная; нужен handle/status/cancel | большой parse job |
| parallel | calls независимы и budget допускает fan-out | чтение разных sources |
| chained | следующий input зависит от предыдущего output | parse → extract |
| speculative | несколько путей, один победитель | редкий read-only search |
| batched | один tool обрабатывает множество items | embeddings/extraction batch |

Parallel calls нельзя выводить только из того, что model API их поддерживает.
Нужны independence, bounded fan-out, rate budget и deterministic join. OpenAI и
Anthropic имеют настройки parallel tool use; это transport capability, не
доказательство безопасности конкретной группы
([OpenAI](https://platform.openai.com/docs/guides/function-calling),
[Anthropic](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use)).

## 3. По эффекту и обратимости

| Класс | Пример | Default control |
| --- | --- | --- |
| pure/local compute | parse, normalize, graph metric | sandbox + resource limit |
| external read | GET source, search | allowlist + timeout + cache |
| idempotent write | upsert by stable key | idempotency + verify |
| non-idempotent write | append/send/create without key | approval/transaction, no blind retry |
| destructive | delete/publish/permission change | explicit human authorization + audit |

## 4. По типу отказа

| Класс | Примеры | Реакция |
| --- | --- | --- |
| validation | malformed JSON, wrong type, unknown tool | repair once/replan; не network retry |
| semantic | valid ID format, но объекта нет; wrong tool | refresh state/replan/ask |
| authorization | 401/403, denied scope | re-auth или человек; не retry storm |
| transient transport | reset, 429, selected 5xx | bounded exponential backoff + jitter |
| permanent remote | 404 stable resource, unsupported operation | fallback or final failure |
| timeout before dispatch | local queue deadline | safe reschedule |
| timeout after dispatch | outcome unknown | reconcile/idempotency lookup |
| corrupt/untrusted result | schema mismatch, prompt injection, stale data | quarantine, validate, alternate source |
| policy | cost/risk/concurrency budget exhausted | stop, degrade or authorize |

Amazon показывает, почему retries умножаются по слоям и создают overload; retry
должен жить в одном выбранном layer, иметь cap и jitter
([AWS](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)).

## 5. Recovery patterns

- **bounded retry:** только retryable class, deadline-aware, exponential backoff
  с full/decorrelated jitter;
- **rate-limit obedience:** `Retry-After`, token bucket, global concurrency cap;
- **circuit breaker:** закрывает вызовы к unhealthy dependency; полезен при
  fail-fast, но stateful и требует half-open probes;
- **bulkhead:** отдельные pools/budgets не дают одному tool исчерпать систему;
- **fallback:** equivalent source/model/local implementation с явной маркировкой
  degraded quality;
- **checkpoint/resume:** durable state на границе stage;
- **compensation:** обратное действие для saga, когда transaction невозможна;
- **human escalation:** ambiguous, destructive и exhausted cases;
- **dead-letter/quarantine:** вход сохраняется для анализа без бесконечного loop.

## 6. Каталог отказов agent loop

1. tool hallucination или неоднозначные descriptions;
2. schema-valid, но доменно неверные arguments;
3. пропущенный обязательный tool call или ошибочный вызов вместо abstain;
4. бесконечный call/repair loop;
5. duplicate side effect после timeout;
6. неполное сопоставление parallel `call_id → result`;
7. stale observation/planner state;
8. prompt injection из tool result;
9. privilege escalation через overly broad tool;
10. context overflow из-за raw outputs;
11. retry amplification и rate-limit cascade;
12. silent fallback, меняющий semantics;
13. partial success, выданный за полный;
14. невозможность воспроизвести вызов из-за отсутствия version/provenance.

OWASP отдельно выделяет excessive agency: чрезмерную функциональность,
разрешения и автономию extension. Control должен быть техническим, а не только
инструкцией модели
([OWASP LLM06](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)).

## 7. Метрики

| Слой | Метрики |
| --- | --- |
| selection | tool precision/recall, abstention, unknown-tool rate |
| arguments | schema validity, exact/semantic argument accuracy |
| execution | success by error class, duplicate effect, timeout, retry count |
| trajectory | task success, steps, invalid/extra calls, recovery rate |
| system | p50/p95 latency, cost/task, fan-out, saturation |
| safety | unauthorized/destructive attempts, approval bypass, data exposure |

BFCL оценивает serial/parallel/multiple calls, abstention и stateful multi-turn;
ToolBench/StableToolBench расширяют real-world API planning, а τ-bench —
stateful user/tool interaction. Ни один benchmark не заменяет chaos cases с
локальными 429/5xx/timeouts и проверкой duplicate effects
([BFCL](https://proceedings.mlr.press/v267/patil25a.html),
[StableToolBench](https://arxiv.org/abs/2403.07714),
[τ-bench](https://arxiv.org/abs/2406.12045)).
