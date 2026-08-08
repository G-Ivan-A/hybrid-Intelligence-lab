---
status: draft
version: 0.1
updated: 2026-08-08
temperature: 0.5
---

# Agentic Evaluation: фреймворки и практические паттерны

## 1. Сравнение инструментов на дату исследования

| Инструмент | Сильный центр | Execution / integration | Hosting / cost boundary | Graph output |
| --- | --- | --- | --- | --- |
| [Ragas](https://docs.ragas.io/) | RAG и metric composition | Python, datasets/experiments; model-backed metrics | OSS; оплата выбранных model providers | custom metrics, не native graph comparator |
| [DeepEval](https://deepeval.com/docs/getting-started) | pytest-like LLM evals, RAG/agent metrics | Python/pytest, CLI, synthetic data | OSS core + Confident AI platform | custom metric required |
| [TruLens](https://www.trulens.org/getting_started/) | feedback functions + tracing/observability | Python instrumentation, OpenTelemetry ecosystem | OSS + TruEra service options | custom feedback required |
| [LangSmith](https://docs.langchain.com/langsmith/evaluation) | datasets, offline/online eval and tracing | SDK/API, experiments, human/code/LLM evaluators | hosted platform with plan limits | custom evaluator required |
| [Braintrust](https://www.braintrust.dev/docs/guides/evals) | code-defined evals, scorers, experiments | Python/TypeScript SDK, CI, tracing | hosted/self-hosting options; model/infrastructure costs separate | custom scorer required |
| [Promptfoo](https://www.promptfoo.dev/docs/intro/) | declarative prompt/model red-teaming and CI | YAML/CLI/Node, assertions, provider matrix | OSS CLI + commercial platform options | JS/Python/custom assertion required |

Таблица фиксирует documented capability, не сравнительный benchmark. Ни один из
шести не задаёт из коробки ontology-aware entity alignment, qualifier-sensitive
triple matching и false-merge graph resolution contract. Это должен быть
domain scorer поверх выбранного runner.

## 2. Как выбирать

| Нужда | Первый shortlist |
| --- | --- |
| быстро исследовать RAG metrics в Python | Ragas / DeepEval |
| связать eval с traces и online feedback | TruLens / LangSmith / Braintrust |
| pytest-native regression | DeepEval |
| model/prompt matrix и security assertions в CLI | Promptfoo |
| code-defined cross-language experiments | Braintrust |
| уже используется LangChain/LangGraph platform | LangSmith |

Выбор проверяется spike на 20–50 representative cases: воспроизводимость,
custom graph scorer, dataset export, CI exit semantics, trace portability,
parallelism/rate limits и стоимость. Vendor lock-in оценивается по возможности
выгрузить inputs, outputs, scores, reasons и traces в открытом формате.

## 3. Reference implementation shape

```text
case + source snapshot
  -> pipeline under test
  -> deterministic schema/provenance checks
  -> entity/relation/graph comparator
  -> semantic judge for rubric-only dimensions
  -> human queue for critical/disagreement cases
  -> versioned result + trace + cost
```

Custom graph scorer сначала канонизирует IDs/aliases и qualifiers, затем считает
per-type entities/relations/triples, отдельно resolution и provenance. Он не
сравнивает сериализованный JSON строка-в-строку.

## 4. Практические anti-patterns

- запускать только «happy path» из synthetic generator;
- использовать ту же model family как generator, judge и gold author без audit;
- менять prompt judge и threshold одновременно;
- принимать vendor metric name за одинаковую формулу между frameworks;
- оптимизировать на открытом golden set до saturation;
- хранить score без raw output, source snapshot и judge reason;
- увеличивать среднее ценой critical slice;
- сравнивать цену tools без model calls, annotation и review labor.

## 5. BA acceptance examples

Плохое: «агент строит качественный граф».

Проверяемое: «на versioned set договоров система (a) не коммитит relation без
source span, (b) считает entity/relation metrics по type, (c) отправляет
ambiguous identity в review, (d) не превышает согласованный false-merge ceiling,
(e) публикует p95 latency и cost/document». Конкретные числа появляются после
baseline, error-cost workshop и confidence interval, а не из отраслевого обзора.
