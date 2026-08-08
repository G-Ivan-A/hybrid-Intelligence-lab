---
status: draft
version: 0.1
updated: 2026-08-08
temperature: 0.5
---

# Agentic Evaluation: образовательный срез и открытые исследования

## 1. Что должен уметь бизнес-аналитик

1. Перевести «качество» в решение, unit of evaluation и цену видов ошибок.
2. Не смешивать source faithfulness, factual correctness и usefulness.
3. Определить population и slices до выбора среднего score.
4. Описать gold, допустимую эквивалентность, unknown/abstention и evidence.
5. Отличать deterministic check от model judge и human acceptance.
6. Требовать baseline, sample size и uncertainty рядом с threshold.
7. Версионировать dataset/rubric/judge и отделять system drift от eval drift.
8. Задавать non-functional acceptance: cost, latency, privacy, auditability.

### Типовые ошибки требований

| Ошибка | Исправляющий вопрос |
| --- | --- |
| «accuracy 90%» | На какой population, какая формула и цена FP/FN? |
| «faithfulness > 0.9» | Каким grader, относительно какого context и как он calibrated? |
| только average | Каковы worst critical slice и confidence interval? |
| gold = один ответ | Какие эквивалентные ответы/графы допустимы? |
| judge без human sample | Как измерены agreement и systematic bias? |
| только offline | Как обнаруживаются drift и production escapes? |

## 2. Связь с соседними модулями

| Модуль | Evaluation interface |
| --- | --- |
| Retrieval | Recall@k/nDCG, context relevance, citation coverage |
| Memory | factual consistency over time, stale/conflicting memory, retrieval success |
| Task Processing | task success, constraints, tool/trajectory correctness, recovery |
| Information Extraction | entity/relation/triple F1, resolution, provenance, graph queries |

Сквозной eval связывает один case ID и source snapshot через все стадии. Тогда
ошибка ответа может быть отнесена к retrieval miss, extraction false positive,
identity merge или generation, а не просто к «модели».

## 3. Открытые вопросы для локального benchmark

- Как выглядит реальная distribution источников, языков и graph queries MVP?
- Какова цена false merge против false split для каждого entity type?
- Насколько полон gold: unannotated relation — false positive или неизвестность?
- Какой human agreement достижим по faithfulness/usefulness rubrics?
- Какой judge даёт приемлемую confusion matrix на русском доменном тексте?
- Как меняются scores после model, prompt, ontology и source drift?
- Какой cascade минимизирует evaluation cost при заданном escape rate?
- Какие traces можно хранить с учётом privacy/license/deletion?

Эти вопросы требуют corpus и human decisions; обзор не может честно назначить
им ответы.

## 4. Минимальный следующий эксперимент

В рамках будущей B-067: выбрать 30–50 cases по слоям риска; независимо разметить
двумя domain reviewers; adjudicate disagreement; реализовать deterministic +
graph scorers; сравнить минимум два judges с blinded/randomized order; посчитать
per-slice confusion, agreement, bootstrap intervals, cost и latency. Результат —
не «лучший framework», а обоснованный contract и список gaps для расширения set.

## 5. Источники

- Zheng et al., [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685), 2023.
- Es et al., [RAGAS](https://aclanthology.org/2024.eacl-demo.16/), 2024.
- Saad-Falcon et al., [ARES](https://aclanthology.org/2024.naacl-long.20/), 2024.
- Guha et al., [LegalBench](https://arxiv.org/abs/2308.11462), 2023.
- Singhal et al., [Large language models encode clinical knowledge](https://www.nature.com/articles/s41586-023-06291-2), 2023.
- Chen et al., [FinQA](https://aclanthology.org/2021.emnlp-main.300/), 2021.
- Zhang et al., [BERTScore](https://openreview.net/forum?id=SkeHuCVFDr), 2020.
- Official docs: [Ragas](https://docs.ragas.io/), [DeepEval](https://deepeval.com/docs/getting-started), [TruLens](https://www.trulens.org/getting_started/), [LangSmith](https://docs.langchain.com/langsmith/evaluation), [Braintrust](https://www.braintrust.dev/docs/guides/evals), [Promptfoo](https://www.promptfoo.dev/docs/intro/).

## 6. Ограничения обзора

Не выполнен benchmark на локальном корпусе; vendor capabilities и коммерческие
условия меняются; medical/legal/financial datasets показывают дизайн evidence,
но не переносят thresholds в бизнес-анализ; graph evaluation всё ещё требует
domain-specific equivalence и completeness policy.
