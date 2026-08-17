---
status: draft
version: 0.1
updated: 2026-08-11
temperature: 0.5
---

# Tool Use & Function Calling: индустриальные реализации и кейсы

<!-- CROSS-REVIEW [Codex-validation]: P2 RFC Reference Research Pattern не выполнен: в файле нет ни одной markdown-ссылки на 10-theory.md, 20-taxonomy.md или 30-decision-framework.md, все ссылки внешние (OpenAI, Anthropic, MCP, frameworks). Отклонение здесь особенно заметно содержательно: 10-theory.md вводит конечный автомат вызова и контракт инструмента, 30-decision-framework.md — risk matrix и retry decision, и разделы этого файла прямо продолжают обе конструкции, но основание не адресовано. Frontmatter тоже не содержит related_artifacts, поэтому связь не восстанавливается и машинно. Текст не изменяется. -->

## 1. Сравнение protocol/framework layers

Состояние проверено по официальной документации и репозиториям на 2026-08-11.

| Подход | Фактический слой | Async/parallel/chaining | Error/state boundary | Graph output |
| --- | --- | --- | --- | --- |
| [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling) | provider model API; built-in, custom и remote MCP tools | parallel calls; loop реализует application/SDK | strict args, call IDs; execution/retry у клиента | structured payload, graph semantics у приложения |
| [Anthropic tool use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use) | provider message API; client/server tools | parallel blocks; client возвращает все results | `is_error`; execution/retry у клиента | content blocks, graph semantics у приложения |
| [MCP](https://modelcontextprotocol.io/specification/2025-06-18/architecture/index) | open client-host-server integration protocol | progress/cancel; task support развивается | JSON-RPC + tool errors; policy у host | structured content/resources, не graph DB |
| [LangChain/LangGraph](https://docs.langchain.com/oss/python/langgraph/) | tool abstraction + graph runtime | ToolNode parallelism, explicit graph loops | configurable error messages, state/checkpoints | arbitrary state; custom NetworkX/DB adaptor |
| [LlamaIndex](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/) | data/RAG-centric tools, agents, workflows | async tools/workflows and handoffs | framework events/state; domain recovery custom | property-graph integrations, not universal tool output |
| [CrewAI](https://docs.crewai.com/en/concepts/tools) | role/task/crew orchestration + tools | async execution and task processes | tool errors/caching configurable; durable guarantees external | custom tool/model output |

Стоимость function/tool calling — это прежде всего model tokens/inference плюс
цена самого API; MCP specification не вводит per-call tariff. Framework core
часто OSS, но tracing, hosted control plane, models и external services могут
быть платными. Поэтому сравнение одной цифрой «стоимость framework» вводит в
заблуждение.

## 2. Что видно в реальном коде

LangGraph `ToolNode` параллельно исполняет несколько вызовов, валидирует имя и
arguments и позволяет превратить выбранные exceptions в `ToolMessage`; wrappers
могут добавить retry/cache. Это подтверждает separation: framework предоставляет
hook, но operator задаёт policy
([source](https://github.com/langchain-ai/langgraph/blob/main/libs/prebuilt/langgraph/prebuilt/tool_node.py)).

OpenAI Agents SDK отделяет function tools, agents-as-tools, MCP servers,
guardrails/tripwires, sessions и tracing. Его docs предупреждают, что tool
guardrails применяются к function tools, но не автоматически ко всем hosted
tools/agents-as-tools — abstraction boundary важна для threat model
([tools](https://openai.github.io/openai-agents-python/tools/),
[guardrails](https://openai.github.io/openai-agents-python/guardrails/)).

MCP tools specification требует считать annotations недоверенными, если server
не доверен. Следовательно, discovery metadata не должно само выдавать authority
([MCP tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)).

## 3. Production reliability pattern

Типовой envelope вокруг любого framework:

1. registry возвращает только tools, разрешённые роли и текущей фазе;
2. model выдаёт typed proposal;
3. validator проверяет schema, semantic preconditions и budget;
4. policy engine/человек авторизует effect;
5. executor применяет timeout, isolation и operation ID;
6. adapter нормализует result/error и удаляет secrets;
7. state store фиксирует attempt и checkpoint;
8. verifier проверяет postconditions;
9. loop продолжает, replans или останавливается по bounded rule.

Этот слой нельзя делегировать LLM: prompt не обеспечивает atomicity, network
deadline или least privilege.

## 4. Error scenarios

| Сценарий | Неподходящая реакция | Production pattern |
| --- | --- | --- |
| 429 | немедленные параллельные retries | `Retry-After`, jitter, shared token bucket |
| 500/503 | бесконечный agent repair loop | capped retry at one layer, circuit/bulkhead |
| 404 | retry с тем же ID | refresh lookup/replan; retry лишь при eventual consistency contract |
| malformed args | network retry | schema feedback, bounded repair or alternate model |
| timeout on create | повтор с новым ID | same idempotency key/status reconciliation |
| malformed result | передать raw text дальше | quarantine + output schema/provenance validation |
| unavailable tool | скрытый fallback | equivalent fallback с degraded marker или stop |

AWS рекомендует выбирать timeout по downstream latency distribution, учитывать
connection setup, ограничивать retry и добавлять jitter; многослойные retries
могут умножить нагрузку. Эти принципы применимы к agent tools как к обычным
distributed calls
([AWS](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)).

## 5. Benchmarks и реальные ограничения

BFCL вырос от AST-based function-call accuracy к multi-turn, state и abstention;
его авторы отмечают, что single-turn сильнее long-horizon behavior. ToolBench
предложил large-scale real API corpus, а StableToolBench — virtual API server
для стабильности. τ-bench проверяет tool-agent-user interaction и конечное
состояние. Вместе они показывают, что нельзя выводить system reliability из
одной schema-accuracy метрики
([BFCL](https://proceedings.mlr.press/v267/patil25a.html),
[ToolBench](https://openreview.net/forum?id=dHng2O0Jjr),
[StableToolBench](https://arxiv.org/abs/2403.07714),
[τ-bench](https://arxiv.org/abs/2406.12045)).

В 2026 году ToolBench-X специально добавил recoverable environment hazards и
сообщил разрыв между корректностью function call и task completion при
ненадёжных tools. Это актуальный preprint, поэтому он задаёт перспективное
направление fault-oriented eval, но ещё не зрелую индустриальную baseline
([ToolBench-X](https://arxiv.org/abs/2606.25819)).

ReAct показал преимущество объединения reasoning/action над отдельными
baselines на исследованных задачах, но его результаты не сравнивают современный
provider-native schema channel или production retry runtime напрямую
([ReAct](https://openreview.net/forum?id=WE_vluYUL-X)).

## 6. Security и sandboxing

- allowlist egress, domains и filesystem roots;
- отдельная identity на tool и least-privilege scope;
- sandbox CPU/memory/time/output size для local code;
- данные tool result считать untrusted input, не system instruction;
- secrets выдавать executor, не помещать в model context;
- destructive calls требуют preview/explicit authorization;
- audit хранит correlation и digest, но не дублирует sensitive payload;
- server/tool version pinning и supply-chain review.

Это особенно важно для MCP: удобное подключение нового server одновременно
расширяет code/data boundary. MCP specification требует user consent и контроля
host, а OWASP рекомендует минимизировать extensions, permissions и autonomy
([MCP security](https://modelcontextprotocol.io/specification/2025-03-26/index),
[OWASP](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)).

## 7. Общий образовательный срез

Любой участник — разработчик, архитектор, аналитик или product manager — должен
уметь различать:

1. tool proposal и фактически выполненную операцию;
2. syntactic schema validity и business correctness;
3. model API, integration protocol и orchestration runtime;
4. read, idempotent write и irreversible effect;
5. retryable failure, replanning error и outcome unknown;
6. sequential dependency и безопасный parallelism;
7. task success и скрытую цену/latency/safety trajectory;
8. framework feature и доказанную локальную reliability.

Типичные ошибки: «MCP решит retry», «strict JSON гарантирует правильный вызов»,
«все 5xx можно повторять», «parallel всегда быстрее», «больше автономии лучше»,
«final answer достаточно для eval». Trade-off нельзя оптимизировать по одной
оси: дополнительная верификация повышает latency/cost, но снижает expected loss;
parallelism уменьшает critical path, но увеличивает fan-out и rate pressure.

Ролевые учебные планы, упражнения и терминология — downstream-задача. Этот
модуль сохраняет общий фундамент и не выбирает одну профессию как адресата.
