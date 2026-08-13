---
status: draft
version: 0.1
updated: 2026-08-11
temperature: 0.5
---

# Tool Use & Function Calling: открытые вопросы и самоаудит

## 1. Что исследование не доказывает

- Какой model/provider даст лучший tool success на локальном corpus.
- Численные timeout, retry, confidence и cost thresholds для production.
- Что отдельный planner улучшит именно Source Intelligence Engine.
- Что MCP server безопасен или надёжен только потому, что совместим со spec.
- Что framework feature одинаково работает во всех language/version adapters.
- Что fallback сохраняет semantic equivalence без domain test.

## 2. Приоритетные локальные эксперименты

| Приоритет | Эксперимент | Измерение |
| --- | --- | --- |
| P0 | minimal direct orchestrator baseline | task success, cost, p95, calls/task |
| P0 | fault injection: timeout/429/500/404/bad JSON | recovery, stop correctness, retry amplification |
| P0 | duplicate-write scenario | duplicate effects, reconciliation success |
| P0 | prompt injection в parsed source/tool result | policy bypass, data/tool exfiltration |
| P1 | strict native call vs text/ReAct parser | syntax, semantic error, repair cost |
| P1 | sequential vs dependency-aware parallel reads | latency, rate limit, correctness |
| P1 | one-loop vs planner/executor | success delta vs tokens/latency/coordination |
| P1 | direct adapters vs MCP for same tools | integration effort, overhead, failure surface |
| P2 | framework portability spike | code/trace/state migration cost |

Нужны frozen fixtures, deterministic fake tools и recorded remote responses;
live API run дополняет, но не заменяет воспроизводимый suite.

## 3. Открытые вопросы

- O1. Какой минимальный typed tool catalog сохраняет recall без context overload?
- O2. Как формально доказывать independence перед parallel dispatch?
- O3. Как согласовать provider call IDs, MCP request IDs и operation IDs?
- O4. Какая persistence нужна между SQLite transaction и agent checkpoint?
- O5. Когда circuit breaker полезнее token-bucket + fail-fast?
- O6. Как измерять semantic equivalence fallback tools?
- O7. Какие tool outputs можно безопасно compact без потери provenance?
- O8. Как воспроизводить remote MCP server version/configuration?
- O9. Как оценивать recovery under unreliable environment, а не только call accuracy?
- O10. Как разделить user consent, operator policy и automated authorization?
- O11. Какие traces хранить для audit без PII/secrets amplification?
- O12. Когда evolving MCP Tasks/async semantics готовы для durable workloads?

## 4. Связь с соседними модулями

| Модуль | Tool Use получает | Tool Use возвращает |
| --- | --- | --- |
| Retrieval | candidate context/tools | external retrieval calls + provenance |
| Memory | durable task/user state | normalized observations и attempt history |
| Task Processing | plan, constraints, authority | verified action outcome и resumable state |
| Information Extraction | schemas/ontology | extraction tool results + evidence spans |
| Evaluation | rubrics/golden cases | traces, errors, latency, cost, recovery signals |

Tool Use — не шестой изолированный silo: это execution seam между plan и
наблюдаемым изменением среды.

## 5. Ранжирование гипотез

| Гипотеза | Evidence сейчас | Следующий тест |
| --- | --- | --- |
| H1 strict schema ограничена syntax | strong API + benchmark basis | invalid vs semantic error split |
| H2 idempotency защищает writes | strong distributed-systems basis | timeout-after-dispatch chaos test |
| H3 dependency-aware parallelism | strong systems basis | local DAG benchmark |
| H4 retry только transient | strong operational basis | injected error matrix |
| H5 planner окупается условно | mixed benchmark basis | paired local trajectories |
| H6 normalized results помогают recovery | plausible/framework support | A/B error envelope |
| H7 technical least privilege > prompt | strong security basis | adversarial policy test |
| H8 per-stage checks локализуют defects | strong evaluation basis | seeded stage regressions |

## 6. Глоссарий

- **Tool/function call** — структурированное предложение модели вызвать функцию.
- **Executor** — код, который проверяет и фактически выполняет вызов.
- **MCP host/client/server** — coordinator, connection endpoint и capability
  provider в Model Context Protocol.
- **Idempotency** — повтор одной logical operation не создаёт новый effect.
- **Outcome unknown** — запрос отправлен, но итог не подтверждён.
- **Circuit breaker** — stateful fail-fast control для unhealthy dependency.
- **Bulkhead** — изоляция pool/budget между зависимостями.
- **Compensation** — отдельное обратное действие в неатомарном workflow.
- **Trajectory** — последовательность model decisions, calls и observations.

## 7. Источники

### S1 — официальные контракты

- OpenAI. [Function calling](https://platform.openai.com/docs/guides/function-calling).
- Anthropic. [How to implement tool use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use).
- Model Context Protocol. [Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture/index),
  [Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools),
  [Security principles](https://modelcontextprotocol.io/specification/2025-03-26/index).
- LangGraph. [Overview](https://docs.langchain.com/oss/python/langgraph/).
- LlamaIndex. [Tools](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/).
- CrewAI. [Tools](https://docs.crewai.com/en/concepts/tools).
- OpenAI Agents SDK. [Tools](https://openai.github.io/openai-agents-python/tools/),
  [Guardrails](https://openai.github.io/openai-agents-python/guardrails/).
- AWS. [Timeouts, retries and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/).
- OWASP. [LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/).

### S2 — papers и benchmarks

- Yao et al. [ReAct](https://openreview.net/forum?id=WE_vluYUL-X), ICLR 2023.
- Patil et al. [BFCL](https://proceedings.mlr.press/v267/patil25a.html), ICML 2025.
- Qin et al. [ToolBench](https://openreview.net/forum?id=dHng2O0Jjr), ICLR 2024.
- Guo et al. [StableToolBench](https://arxiv.org/abs/2403.07714), 2024.
- Yao et al. [τ-bench](https://arxiv.org/abs/2406.12045), 2024.
- Cemri et al. [MAST](https://arxiv.org/abs/2503.13657), 2025.
- [ToolBench-X](https://arxiv.org/abs/2606.25819), preprint, 2026.

### S3 — код

- LangGraph.
  [`ToolNode`](https://github.com/langchain-ai/langgraph/blob/main/libs/prebuilt/langgraph/prebuilt/tool_node.py).

## 8. Рефлексия Reference Research Pattern

<!-- CROSS-REVIEW [Codex-validation]: альтернативное мнение. Рефлексия утверждает устойчивость маршрута intro → theory → taxonomy → decision → practice → open research, и по составу файлов (P1) это верно. Но проверено и подтверждено здесь только членение артефакта, а не метод: P2 в модуле не выполнен, обратных ссылок практика → теория нет, триггер P5 не срабатывал ни разу. Формулировка «шестой домен подтверждает устойчивость» поэтому шире имеющегося основания — подтверждена воспроизводимость формы, а не воспроизводимость метода. Самоаудит (§9) этого различия не фиксирует. -->

Шестой домен подтверждает устойчивость маршрута `intro → theory → taxonomy →
decision → practice → open research`. Специфика Tool Use потребовала
распределить material по слоям, а не по брендам: иначе comparison смешивает
model API, protocol и runtime. `30` стал stage mapping для Source Intelligence
Engine, но сохраняет форму research recommendation; `40` отделяет документированную
capability от доказанной reliability.

## 9. Самоаудит

- Все направления issue покрыты; sandboxing, idempotency, observability,
  cost model и fault injection добавлены по Creative mandate.
- Ключевые утверждения опираются на S1–S3; vendor guidance не выдано за
  универсальный benchmark.
- MAST 36.9% ограничено исходным corpus и не представлено как base rate.
- Framework comparison датировано; быстро меняющиеся детали требуют повторной
  проверки перед architecture decision.
- Специализация по ролям явно оставлена downstream.
- Репозиторные или проектные правила не изменяются; численные thresholds не
  выдуманы без локального эксперимента.
