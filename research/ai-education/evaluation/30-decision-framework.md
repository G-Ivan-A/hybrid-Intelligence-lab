---
status: draft
version: 0.1
updated: 2026-08-08
temperature: 0.5
---

# Agentic Evaluation: рамка решений и контракт golden set

## 1. От бизнес-риска к измерению

1. Назвать решение, принимаемое по output, и обратимость ошибки.
2. Разделить false accept, false reject и abstention; оценить их цену.
3. Определить unit of evaluation и critical slices.
4. Назначить дешёвые deterministic checks до semantic judges.
5. Создать и независимо разметить минимальный golden set.
6. Калибровать judges против людей, baseline и disagreement.
7. Установить gate по confidence interval и worst critical slice.
8. Версионировать dataset/rubric/judge; мониторить drift и escapes.

## 2. Risk matrix

| Цена ошибочного accepted result | Обратимость высокая | Обратимость низкая |
| --- | --- | --- |
| низкая | sampled offline eval + monitoring | component gates + regression set |
| средняя | deterministic + judge, review disagreement | human-reviewed high-impact slices |
| высокая | abstain/review gate, evidence required | deterministic invariants + independent review; LLM judge только triage |

## 3. Минимальный контракт B-067 (research recommendation)

Это вход для будущего решения, не нормативное правило Хаба.

| Поле | Минимальное содержание |
| --- | --- |
| decision/use case | какое решение поддерживает output |
| corpus snapshot | source IDs, version/date, language, permissions |
| ontology/schema | версии entities, relations, qualifiers, unknown policy |
| cases | normal, boundary, negative, adversarial, abstention, critical slices |
| annotation | guide, annotators, adjudication, agreement, provenance |
| metrics | primary gate + diagnostic metrics + cost/latency |
| thresholds | baseline, loss rationale, sample size, confidence interval |
| graders | code/judge model, prompt, ordering, calibration results |
| execution | offline PR regression, release gate, sampled production monitoring |
| governance | owner, version, change history, escape review |

### Candidate metric bundle for Source Intelligence Engine

| Stage | Gate candidate | Diagnostics |
| --- | --- | --- |
| parsing | required blocks/schema, text coverage | OCR/layout errors, latency |
| extraction | per-type entity/relation F1 | precision/recall, unknown rate |
| resolution | false-merge ceiling | false split, ambiguous/NIL rate |
| graph commit | schema/constraint pass, provenance coverage | triple F1, contradictions |
| retrieval/API | task success, citation correctness | Recall@k, faithfulness, abstention |
| system | critical safety invariant | cost/doc, p95 latency, retry/error rate |

Численные thresholds намеренно не заданы: без локального corpus и error-cost
решения они создавали бы ложную точность. Первый benchmark должен оценить human
baseline и простую baseline pipeline, затем предложить порог для human review.

## 4. Where to evaluate

`per-stage eval` локализует regression; `end-to-end eval` обнаруживает compounding
errors и проверяет полезность; `production monitoring` ловит drift, но не может
заменить labeled regression. Практический минимум использует все три с разной
частотой: fast deterministic PR suite, более дорогой scheduled semantic suite и
sampled production review.

Cost of evaluation сравнивается с expected cost of error. Оптимизация начинается
с cascade: schema/rules → small/reference grader → expensive judge → human only
for disagreement/high impact. Кэширование допустимо только при ключе из input,
output, rubric, judge и source versions.

## 5. Stop/go decision

Релиз не проходит, если нарушен critical invariant, нижняя граница confidence
interval ниже согласованного gate либо critical slice регрессировал сверх
tolerance. Средний score не компенсирует это. Изменение judge или dataset сначала
запускается параллельно старой версии, иначе нельзя отличить product regression
от measurement drift.
