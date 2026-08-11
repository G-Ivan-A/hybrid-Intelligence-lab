---
status: draft
version: 0.1
updated: 2026-08-11
temperature: 0.3
---

# Прикладной evals-контракт Source Intelligence Engine

## Назначение и границы решения

Документ переводит базовый [evals-контракт B-067](../../../standards/evals-contract-standard.md)
в план первого локального эксперимента для цепочки `source → parsing →
extraction → graph → API`. Он опирается на [исследование Agentic
Evaluation](00-introduction.md), замерженное в [PR #482](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/482),
и на модель `Detect → Extract → Resolve → Validate → Commit` из
[исследования Information Extraction & Graph Modeling](../information-extraction-graph-modeling/00-introduction.md).

Контракт является research/design input, а не внедрением в Source Intelligence
Engine. Он фиксирует объект измерения, данные и процедуру, но намеренно не
назначает acceptance thresholds. Числа размера выборки и повторов ниже — дизайн
эксперимента, а не пороги качества.

Решение, которое должен поддержать первый эксперимент: может ли человек
сравнить baseline и candidate pipeline по воспроизводимым stage-level и
end-to-end evidence, локализовать цену ошибок и затем назначить gates для B-068.

## 1. Минимальный набор метрик

Одна строка результата всегда содержит `case_id`, версии corpus/ontology/
pipeline/scorer, stage output, score, raw evidence, latency, token usage, cost и
run ID. Среднее не заменяет результаты по critical slices и confidence interval
([B-067, Evaluation Contract](../../../standards/evals-contract-standard.md#evaluation-contract),
[таксономия метрик](20-taxonomy.md)).

| Этап | Корректность | Полнота | Производительность | Почему этого достаточно для первого замера |
| --- | --- | --- | --- | --- |
| Parsing | доля документов, прошедших schema/required-block checks | text/block coverage относительно gold | latency на документ; cost на документ | Детерминированные checks отделяют потерю структуры от последующих LLM-ошибок; OCR/layout error хранится как slice, а не новый агрегат. |
| Extraction | entity precision и relation precision по типам | entity recall и relation recall по типам | latency; tokens/cost на документ | Precision/recall сохраняют различие false accept и false reject; F1 вычисляется как сводная диагностика, но не скрывает компоненты. |
| Graph | triple precision по ontology-aware matching; constraint violation rate | triple recall; provenance coverage | latency graph commit; cost на документ | Triple matching проверяет содержимое, constraints — допустимость, provenance — связь с источником. GED остаётся диагностикой для малых спорных cases: его edit costs не универсальны. |
| API | correctness и citation correctness по competency questions | task success/answer coverage, включая корректное abstention | end-to-end latency; tokens/cost на запрос | Reference-based ответ проверяет бизнес-полезность и не смешивает её с одной faithfulness-оценкой. Semantic judge применяется только к rubric-only эквивалентности. |

Сквозные обязательные diagnostics: error/retry rate, распределение latency
(включая хвост), cost, disagreement человека и judge, а также результаты по
языку, типу документа, длине, OCR quality, редкому классу, ambiguity,
answerability и business-impact tier. Candidate не может компенсировать провал
critical slice средним score — это правило следует из [risk-based рамки
исследования](30-decision-framework.md#1-от-бизнес-риска-к-измерению).

### Правила сравнения

- Entity matching нормализует aliases, но сохраняет type и source span.
- Relation/triple matching учитывает направление, qualifiers и заранее
  размеченные эквивалентности; неразмеченный факт имеет статус `unknown`, пока
  completeness policy не разрешит считать его false positive.
- Graph scorer отдельно считает false merge/false split для entity resolution.
- API judge не проверяет фактическую истинность без reference и source evidence;
  faithfulness к ошибочному контексту не равна correctness
  ([теория evals](10-theory.md#2-четыре-слоя-доказательства)).

## 2. Golden set: договоры и требования бизнес-анализа

Первый домен — русскоязычные требования и договоры бизнес-анализа: документы с
акторами, системами, бизнес-правилами, требованиями, зависимостями и source
spans. Этот домен проверяет не только упоминание технологии, но и отношения,
provenance, отрицания, неоднозначность и ответы на competency questions.

### Структура case

```yaml
case_id: ba-0001
source:
  snapshot_id: corpus-version-and-content-hash
  document_type: requirement|contract|analysis
  language: ru
  permissions: review-boundary
input:
  content: immutable-source-or-reference
  parsing_hints: optional
expected:
  blocks: []
  entities: []
  relations: []
  triples: []
  provenance_spans: []
  constraints: []
  competency_questions: []
  allowed_equivalences: []
  unknowns: []
slices: [normal|boundary|negative|adversarial|abstention, impact-tier]
annotation:
  guide_version: v1
  annotator_ids: []
  decisions: []
  disagreement: []
  adjudicator: null
```

Набор содержит 30–50 independently reviewable cases — диапазон первого
эксперимента из [открытого плана PR #482](50-open-research.md#4-минимальный-следующий-эксперимент).
До отбора фиксируются population и slice matrix. В набор входят normal,
boundary, negative, adversarial, abstention и high-impact cases; ни один тип не
заполняется только синтетикой.

### Создание и validation

1. Заморозить разрешённый corpus snapshot, ontology, annotation guide и правила
   эквивалентности/unknown.
2. Стратифицированно выбрать реальные документы по slice matrix; удалить или
   санитизировать private/PII content до включения.
3. Использовать synthetic generation только для предлагаемых boundary и
   adversarial cases. Два domain reviewers независимо подтверждают каждый
   synthetic case до перевода в gold.
4. Два domain reviewers независимо размечают entities, relations, qualifiers,
   provenance и competency questions. Они не видят output тестируемой системы.
5. Посчитать per-label agreement: Cohen's kappa для категорий и соответствующий
   span/relation agreement; сохранить confusion/disagreement, затем провести
   adjudication третьим reviewer или совместным решением.
6. Заморозить dev/calibration часть и закрытый regression holdout. Active
   learning после первого запуска предлагает uncertain/disagreement cases
   только в следующую версию; текущий holdout не доразмечается под candidate.

## 3. Калибровка LLM-as-Judge

Judge используется лишь для API-ответов и иных rubric-only semantic dimensions;
parsing, entities, relations, triples, constraints и provenance оцениваются
кодом. Это сохраняет дешёвые воспроизводимые checks перед вероятностным judge
([B-067, Grading](../../../standards/evals-contract-standard.md#grading)).

### Модель и prompt

Выбирается отдельная от pipeline model family, доступная на дату запуска, с
фиксируемой версией, поддержкой русского языка и structured output. Конкретное
имя модели фиксирует run manifest после короткого сравнения минимум двух judge
candidates на человеческой calibration subset: этот документ не превращает
изменяемое имя модели в долговечный контракт.

Основной режим — reference-based pointwise rubric. Pairwise blinded comparison
baseline/candidate используется вторым сигналом. Prompt содержит:

```text
Role: independent evaluator; system identity is hidden.
Inputs: source evidence, competency question, reference invariants, candidate.
Rubric: correctness, evidence support, completeness, appropriate abstention.
Rule: score each dimension independently; quote evidence span IDs; emit
structured decision + reason; use NOT_EVALUABLE when evidence is insufficient.
Do not reward length, style, or agreement with the candidate.
```

### Calibration protocol

1. Использовать все human-adjudicated API cases, стремясь к 50 judgments путём
   нескольких competency questions на case; если их меньше, публиковать sample
   size и uncertainty, не объявлять judge calibrated.
2. Скрыть vendor/pipeline identity, рандомизировать порядок и провести swap test
   `A/B → B/A` на каждой pairwise записи. Position bias — доля изменившихся
   решений; verbosity bias — изменение после length-controlled paraphrase;
   self-preference — разница на outputs той же и другой model family.
3. Сравнить judge с adjudicated human labels: confusion matrix и Cohen's kappa
   для категорий, rank correlation для ordinal rubric, результаты по slices.
   Correlation без agreement не считается достаточной
   ([LLM-as-judge](10-theory.md#3-llm-as-judge)).
4. Повторить stochastic judgments с зафиксированными parameters; сохранить raw
   outputs, prompt/version, order, model ID, latency и cost.
5. Человек утверждает либо отклоняет judge и его рабочие thresholds. До этого
   judge — diagnostic/triage signal; disagreements и high-impact cases всегда
   направляются на human review.

## 4. Runner: DeepEval с domain scorers

Из шести рассмотренных инструментов выбран **DeepEval**: его Python/pytest-like
execution, CLI и open-source core соответствуют offline regression experiment и
позволяют начать без hosted control plane. Исследование прямо относит DeepEval к
pytest-native regression и предупреждает, что graph comparison требует custom
metric ([сравнение фреймворков](40-practice-and-cases.md#1-сравнение-инструментов-на-дату-исследования)).

DeepEval здесь только runner и result adapter. Domain package реализует schema/
provenance checks, ontology-aware entity/relation/triple scorers, resolution и
competency-question adapter. Результат одновременно экспортируется в открытый
JSONL, поэтому смена runner не меняет case schema и исторические runs.

### Integration points

1. Dataset loader читает versioned case + source snapshot.
2. Pipeline adapter сохраняет output каждого этапа и единый trace/run ID.
3. Deterministic scorers запускаются после parsing, extraction и graph commit.
4. API scorer запускает reference checks, затем откалиброванный judge для
   semantic rubric.
5. Reporter строит per-stage, end-to-end и per-slice таблицы, confidence
   intervals, error inventory, latency/cost; CI semantics появляются только
   после human-approved thresholds.

Остаточные риски: drift API/docs и metric semantics, custom scorer maintenance,
provider cost/rate limits и возможный lock-in hosted features. Снижение риска:
pin dependencies, contract-test custom scorers, хранить raw open-format results
и сначала выполнить spike на representative cases. Этот выбор — гипотеза
эксперимента; он не доказывает превосходство DeepEval над остальными runner.

## 5. Пошаговый эксперимент

| Фаза | Действия | Evidence/выход |
| --- | --- | --- |
| 0. Pre-registration | Зафиксировать use case, error costs, population/slices, baseline/candidate, versions и human decision owner; thresholds оставить `TBD`. | Подписанный run plan и manifest. |
| 1. Data | Создать и независимо разметить 30–50 cases, adjudicate, заморозить dev/calibration/holdout. | Dataset version, guide, agreement и disagreement log. |
| 2. Harness | Реализовать adapters и deterministic domain scorers, unit-test на handcrafted fixtures; провести DeepEval spike. | Воспроизводимый runner и scorer test report. |
| 3. Judge | Сравнить отдельные judge candidates, выполнить blinded swap/verbosity/self-preference tests и human calibration. | Calibration report; human approve/reject decision. |
| 4. Runs | Для неизменных baseline и candidate выполнить минимум 5 повторов при stochastic stages; deterministic stages — один run плюс repeatability check. | Raw JSONL, traces, cost/latency и version manifest каждого run. |
| 5. Analysis | Посчитать point estimates, paired deltas, bootstrap confidence intervals, run variance, worst slices и error inventory. Не агрегировать critical failure. | Сводная таблица, plots и каталог ошибок с provenance. |
| 6. Decision | Domain owner и reviewer рассматривают качество, uncertainty, error costs и judge calibration; назначают либо откладывают thresholds. | Human decision record и inputs для B-068. |

### Ресурсы и критерии успеха

Планировать труд двух domain annotators и adjudicator, разработчика adapters/
scorers, reviewer решения; хранение snapshot/traces; pipeline и judge tokens;
лимиты provider; время на пять повторов stochastic path и ручной разбор
disagreements. Run manifest записывает фактические человеко-часы, tokens, cost и
wall-clock вместо предварительного ценового обещания.

Эксперимент успешен, если он воспроизводим из versioned inputs; stage failure
локализуется; human/judge agreement и bias опубликованы с uncertainty; metrics
стабильны либо их variance объяснён; critical slices видны отдельно; каждый
score прослеживается до source/output/scorer; человек располагает evidence для
назначения threshold. Ни одно из этих условий не задаёт числовой gate заранее.

## 6. Handoff в B-068

B-068 получает не средние scores, а immutable bundle:

- dataset/ontology/prompt/pipeline/judge/scorer versions;
- baseline и candidate paired results по case, slice и run;
- effect sizes и bootstrap confidence intervals;
- run-to-run variance, judge calibration/bias и human disagreements;
- false-accept/false-reject error inventory, latency и cost;
- human-approved thresholds либо явный статус `threshold pending`.

Минимальное **N = 5 повторных прогонов** относится к оценке stochastic
run-to-run variance, а не гарантирует статистическую значимость и не является
quality threshold. Число cases/прогонов для конкретного решения B-068 должно
быть рассчитано после baseline variance и минимально practically important
effect; если power/paired confidence interval недостаточны, решение откладывают
и расширяют данные, а не подменяют evidence фиксированным N.

Процедура изменения prompt library:

1. Заморозить одну candidate change и сравнить с текущей библиотекой на тех же
   paired cases/runs; не менять одновременно judge, scorer и ontology.
2. Проверить human-approved primary gates, confidence interval, worst critical
   slice, safety/provenance invariants, latency/cost и отсутствие judge drift.
3. Направить disagreements, regressions и high-impact cases двум людям:
   domain reviewer проверяет смысл, owner принимает итоговое решение.
4. Принять, отклонить или запросить дополнительный run; записать версии,
   rationale и rollback target. Автоматическое продвижение запрещено, пока
   B-068 отдельно не установит human-approved rule.

## Открытые human decisions

- допустимые corpus и publication/privacy boundaries;
- error costs и critical business-impact slices;
- финальная ontology/equivalence/completeness policy;
- judge model после calibration comparison;
- primary gates и числовые acceptance thresholds;
- practically important effect и достаточная statistical power для B-068.

Эти решения намеренно не заполнены исследовательским документом: их принимает
человек по evidence первого эксперимента, как требует B-067.
