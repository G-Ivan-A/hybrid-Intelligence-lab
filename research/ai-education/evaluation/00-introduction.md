---
status: draft
version: 0.2
updated: 2026-08-11
temperature: 0.5
---

# Agentic Evaluation: введение и карта чтения

## Карта чтения

| Файл | Главный вопрос |
| --- | --- |
| [`10-theory.md`](10-theory.md) | Что именно измеряет eval и почему одного score недостаточно? |
| [`20-taxonomy.md`](20-taxonomy.md) | Какие метрики соответствуют RAG, extraction, graph и agent tasks? |
| [`30-decision-framework.md`](30-decision-framework.md) | Как собрать risk-based контракт качества и golden set? |
| [`40-practice-and-cases.md`](40-practice-and-cases.md) | Что поддерживают Ragas, DeepEval, TruLens, LangSmith, Braintrust и Promptfoo? |
| [`50-open-research.md`](50-open-research.md) | Что остаётся проверить локально и чему учить бизнес-аналитика? |
| [`2026-08-11-source-intelligence-evals-contract.md`](2026-08-11-source-intelligence-evals-contract.md) | Как провести первый прикладной evals-эксперимент Source Intelligence Engine без преждевременных порогов? |

<!-- CROSS-REVIEW [Codex-validation]: два наблюдения к карте чтения. (1) P1 RFC задаёт «ровно шесть файлов» модуля; седьмая строка — датированный отчёт внутри каталога модуля, единственный такой случай в корпусе research/ai-education/. Отклонение зафиксировано и в §7.4 отчёта PR #502; оно проходит все валидаторы Хаба, то есть речь о неопределённости самого RFC (смешанная форма не запрещена и не разрешена явно), а не о дефекте исполнения. Решение о статусе смешанной формы — за фаундером. (2) Traceability: ни в одном файле модуля нет frontmatter-полей source, related_artifacts и related_issues, поэтому связь с issue-постановкой и взаимные ссылки модуля не восстанавливаются машинно — в отличие от модуля information-extraction-graph-modeling, где эти поля заполнены во всех шести файлах. Ни одно из полей не проверяется валидатором tools/validate-frontmatter.sh для класса knowledge (обязательны только status, version, updated, temperature). -->

## BLUF

1. **Eval — это система измерений, а не одна метрика.** Нужны отдельно
   component, end-to-end, safety, cost и latency signals; агрегат не должен
   скрывать критический провал.
2. **Faithfulness не равна истинности.** Ответ может точно воспроизводить
   ошибочный контекст. Поэтому source grounding, source authority и factual
   correctness — разные оси ([RAGAS](https://aclanthology.org/2024.eacl-demo.16/)).
3. **LLM-as-judge масштабирует semantic review, но не отменяет калибровку.**
   MT-Bench показал высокое согласие сильного judge с людьми на своём протоколе,
   одновременно выявив position, verbosity и self-enhancement biases
   ([Zheng et al.](https://arxiv.org/abs/2306.05685)).
4. **Golden set — версионированная выборка решений и ошибок.** Она должна
   включать обычные, пограничные, негативные и high-impact случаи, provenance
   разметки и disagreement, а не только «идеальные ответы».
5. **Для графа текстового score недостаточно.** Нужны entity/relation/triple
   precision, recall и F1, resolution false-merge/false-split, provenance
   coverage, constraint violations и downstream query success.
6. **Фреймворк не создаёт валидность.** Инструменты различаются прежде всего
   execution model, datasets, tracing, CI и hosting; смысл rubric, gold и
   acceptance threshold остаётся доменным решением.
7. **Порог нельзя импортировать из статьи.** Он выводится из цены false accept /
   false reject, human baseline и локального confidence interval. Числа вроде
   `faithfulness > 0.9` до калибровки — гипотезы, не DoD.

## Объект и метод

Модуль рассматривает evaluation для цепочки `source → parsing → extraction →
resolution → graph → retrieval/API`. Evidence разделено на: официальные
контракты продуктов, peer-reviewed papers/benchmarks и vendor case studies.
Документация доказывает наличие функции, но не её качество на нашем домене;
benchmark доказывает результат только для опубликованной выборки и протокола.

Это сравнительный обзор, не локальный benchmark. Он не выбирает архитектуру
Source Intelligence Engine и не вводит правила репозитория.

## Сквозная модель

```mermaid
flowchart LR
  S[Sources] --> P[Parsing]
  P --> X[Extraction]
  X --> G[Graph]
  G --> A[API / answer]
  E[Golden set + rubrics] --> P
  E --> X
  E --> G
  E --> A
  O[Traces, cost, latency] --> P
  O --> X
  O --> G
  O --> A
```

Оценка на каждом переходе локализует дефект; end-to-end задача показывает,
сохранилась ли бизнес-полезность. Только один из этих видов не диагностирует
конвейер полностью.
