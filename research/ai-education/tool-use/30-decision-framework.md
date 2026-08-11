---
status: draft
version: 0.1
updated: 2026-08-11
temperature: 0.5
---

# Tool Use & Function Calling: рамка решений

## 1. Порядок выбора

1. Зафиксировать outcome и инвариант, а не название framework.
2. Проверить, нужен ли model-selected tool: известный deterministic step дешевле
   и надёжнее вызвать обычным кодом/workflow.
3. Классифицировать effect, обратимость, данные и required authority.
4. Описать typed contract, domain errors и result validation.
5. Построить dependency DAG; выбрать sync/async/parallel/batch.
6. Назначить deadline, idempotency, retry owner, fallback и stop rule.
7. Выбрать integration boundary: native, MCP или framework adaptor.
8. Записать trace/eval contract и проверить normal + injected failures.

## 2. Когда модель вообще нужна

| Ситуация | Предпочтительно |
| --- | --- |
| фиксированный шаг конвейера | direct deterministic call |
| semantic routing между малым набором tools | native typed call + allowlist |
| большой динамический каталог integrations | retrieval of tools / MCP discovery |
| длинный branching workflow | graph/durable workflow + bounded model nodes |
| destructive or regulated action | deterministic policy + explicit human decision |

Вызов модели ради выбора единственного заранее известного parser добавляет
latency, стоимость и новую точку отказа без информационной выгоды.

## 3. Risk matrix исполнения

| Effect | Низкая неопределённость | Высокая неопределённость |
| --- | --- | --- |
| pure/read | auto execute, validate | bounded agent loop + provenance |
| reversible write | idempotent execute + verify | preview/approval + checkpoint |
| irreversible/high impact | explicit command contract | не автономно; clarify/authorize |

## 4. Planner topology

| Условия | Топология |
| --- | --- |
| ≤3 steps, immediate feedback, small catalog | одна model loop + executor |
| known DAG, semantic work only in nodes | deterministic orchestrator + model workers |
| long horizon, high tool cost, plan review useful | planner → validated plan → executor |
| independent specialist domains | supervisor/handoffs только с typed state |

Отдельный planner допускается, если измеренный выигрыш task success или cost
превышает дополнительные inference, latency и coordination failures. Иначе это
overkill. Его plan — proposal: executor повторно проверяет current state,
preconditions и authority перед каждым действием.

## 5. Retry decision

```text
if deadline exhausted: stop
elif validation/4xx/policy: repair, replan or escalate
elif outcome unknown and write: reconcile by operation_id
elif transient and idempotent: retry with capped backoff+jitter
elif equivalent fallback exists: degrade explicitly
else: fail final with resumable state
```

Retry budget общий на user task, а не независимый в каждом слое. Circuit
breaker разумен для shared remote dependency с измеримым health; для редкого
локального вызова он часто сложнее обычного fail-fast + fallback.

## 6. Cost/performance model

Полная цена шага:

`C = model tokens + tool fee + compute + expected retry + validation +
coordination + expected loss from error`.

Полная latency критического пути:

`L = Σ sequential nodes + max(parallel branch) + queue + retry delay`.

Отсюда следуют практические рычаги: deterministic routing до LLM, compact tool
catalog, batch operations, parallel independent reads, cache по versioned key,
small model для repair/routing и дорогая модель только для ambiguous semantics.
Кэш write-result не заменяет idempotency; кэш external read требует freshness и
provenance.

## 7. Candidate mapping для Source Intelligence Engine

Это исследовательская рекомендация для будущего architecture decision, не
спецификация проекта.

| Stage | Model/tool boundary | Execution pattern | Reliability gate |
| --- | --- | --- | --- |
| acquire/parse | fetch/browser/parser — tools; format choice rule-first | parallel bounded reads; async для больших jobs | allowlist, size/type/hash, timeout, provenance |
| extract | LLM structured extraction уместна для semantics | batch/chunk; retries только transport/provider | strict schema, evidence spans, abstain/unknown |
| resolve | model предлагает candidates; deterministic scorer/rules verify | chained after extraction; checkpoint | stable IDs, merge/split checks, confidence routing |
| SQLite commit | direct application code, не model-selected SQL | idempotent upsert + transaction | constraints, rollback, operation_id, audit |
| NetworkX graph | local deterministic code | batch build after committed snapshot | schema/graph invariants, provenance coverage |
| API publish/query | FastAPI/auth deterministic; agent may call read endpoint | read concurrency; write separately authorized | auth, rate limit, response schema, version |
| evaluation | deterministic checks + selected judge tools | per-stage + end-to-end replay | frozen fixtures, trace, cost/latency/error slices |

Таким образом, agent не должен выбирать каждый механический шаг. Orchestrator
знает pipeline; модель вызывается для extraction, ambiguous resolution и
semantic recovery. SQLite/NetworkX/FastAPI остаются narrow tools или обычным
кодом с invariants.

## 8. Минимальный execution envelope

| Поле | Назначение |
| --- | --- |
| task/operation/attempt/call IDs | correlation и deduplication |
| tool + contract version | воспроизводимость |
| input digest + redaction class | audit без утечки payload |
| authority/approval reference | доказательство допустимости |
| deadline + retry budget | bounded execution |
| state + normalized error | recovery |
| output digest/provenance | проверка результата |
| cost/latency/tokens | оптимизация и regression |

## 9. Stop/go критерии локального прототипа

Не переходить к более автономной топологии, пока minimal baseline не измерил:
task success; invalid/extra tool calls; recovery по каждому injected failure;
duplicate side effects; critical safety violations; p95 latency; cost/task.
Нулевой duplicate/unauthorized tolerance нужен для тестового набора, но численные
production thresholds требуют локального corpus и human decision.
