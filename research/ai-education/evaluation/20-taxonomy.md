---
status: draft
version: 0.1
updated: 2026-08-08
temperature: 0.5
---

# Agentic Evaluation: таксономия метрик

## 1. По уровню объекта

| Уровень | Метрики | Главная ловушка |
| --- | --- | --- |
| token/span | exact match, token F1, span IoU | семантически равные формы штрафуются |
| sentence/claim | entailment, claim precision/recall, attribution | entailment не проверяет authority источника |
| entity/relation | entity F1, relation F1, linking accuracy | matching policy меняет score |
| graph | triple F1, GED, constraint violations, provenance coverage | GED дорог и цена edit не универсальна |
| task/trajectory | success, tool correctness, plan adherence, recovery | одинаковый успех может иметь разный риск/стоимость |
| system | latency p50/p95, tokens, cost, error/abstention rate | среднее скрывает хвосты и slices |

## 2. По типу задачи

### RAG

- retrieval: Recall@k, Precision@k, MRR/nDCG и context relevance;
- generation: faithfulness/groundedness, answer relevance, correctness,
  citation precision/recall;
- end-to-end: answerable task success и calibrated abstention.

RAGAS предложил reference-free faithfulness, answer relevance и context
relevance, а ARES — synthetic training data плюс небольшой human-annotated set
для automated judges. ARES прямо требует domain-specific validation и сообщает
confidence intervals, что важнее единственного score
([RAGAS](https://aclanthology.org/2024.eacl-demo.16/),
[ARES](https://aclanthology.org/2024.naacl-long.20/)).

### Extraction и graph

| Что | Формула/контракт |
| --- | --- |
| entity/relation/triple precision | correct predicted / predicted |
| recall | correct predicted / gold |
| F1 | harmonic mean precision/recall |
| linking accuracy | correct canonical IDs / linkable mentions |
| false merge / false split | ошибочно объединённые / разделённые identities |
| provenance coverage | accepted claims с valid evidence / accepted claims |
| constraint violation | invalid nodes/edges / evaluated objects |
| query success | passed competency questions / all questions |

Exact triple F1 требует заранее определить equivalence: aliases, inverse
relations, qualifiers и partial/incomplete gold. Graph Edit Distance измеряет
минимальную стоимость edits между графами, но зависит от заданных edit costs и
может быть вычислительно дорог; поэтому для production acceptance полезнее
component F1 + constraints + competency queries, а GED — диагностический signal
([NetworkX GED](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.similarity.graph_edit_distance.html)).

### Generation

Reference-based: exact/semantic similarity, factual claim precision, rubric
coverage. Reference-free: coherence, usefulness, style/safety. BLEU/ROUGE
измеряют lexical overlap и слабо подходят как единственный критерий открытого
ответа; BERTScore использует contextual embeddings и лучше отражает semantic
similarity, но также не доказывает factuality
([BERTScore](https://openreview.net/forum?id=SkeHuCVFDr)).

### Planning и agents

- final task success и constraint satisfaction;
- valid tool call / argument accuracy;
- trajectory precision (лишние шаги) и recall (пропущенные необходимые шаги);
- recovery from tool errors, loop/retry rate;
- grounded decision rate, safety violations;
- cost, tokens, wall-clock latency.

Trajectory match нельзя абсолютизировать: несколько путей могут быть правильными.
Поэтому проверяют обязательные invariants и outcome, а exact trajectory оставляют
только там, где порядок является частью риска.

## 3. Диагностические slices

Минимальные срезы: document/source type, language, length, OCR quality, entity
frequency, relation cardinality, answerability, ambiguity, graph size, tool
failure и business-impact tier. Общий micro-F1 может выглядеть высоким при
failure и business-impact tier. Общий micro-F1 может выглядеть высоким при
нулевом recall редкого, но критичного relation type.
