---
status: draft
version: 0.1
updated: 2026-08-06
temperature: 0.5
type: research
context: [information-extraction, graph-modeling, decision-framework, evaluation]
method: comparative-analysis + decision-matrix
scope: repo-wide
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/471"
related_artifacts:
  - "research/ai-education/information-extraction-graph-modeling/00-introduction.md"
  - "research/ai-education/information-extraction-graph-modeling/10-theory.md"
  - "research/ai-education/information-extraction-graph-modeling/20-taxonomy.md"
  - "research/ai-education/information-extraction-graph-modeling/40-practice-and-cases.md"
  - "research/ai-education/information-extraction-graph-modeling/50-open-research.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/471"
---

# Information Extraction & Graph Modeling: рамка решений

## 1. Начинать с решения и ошибок, а не с графовой БД

Последовательность вопросов:

1. Какие решения/запросы должен поддержать результат?
2. Какие entities, events, relations и qualifiers для них минимально нужны?
3. Что считается одним объектом и каковы false-merge/false-split costs?
4. Какая evidence нужна для принятия или оспаривания claim?
5. Какая схема известна, а где discovery допустим?
6. Какие component и downstream метрики образуют acceptance contract?
7. Только затем: extractor, orchestration и storage projection.

Это не проектная рекомендация, а vendor-neutral способ сравнить варианты.

## 2. Матрица «изменчивость схемы × цена ошибки»

| Схема / цена ошибочного accepted fact | Низкая | Средняя | Высокая |
| --- | --- | --- | --- |
| стабильная closed | rules/specialized model или one-shot schema LLM; sampling audit | hybrid + verifier; component metrics | deterministic candidates + independent verification + human gate |
| расширяемая | schema LLM + logged unknowns | staged extraction/resolution; extension review | closed accepted core + quarantined candidate vocabulary |
| open/discovery | LLM/open IE + clustering | discovery отдельно от production graph | exploration only; ни один новый predicate не становится accepted автоматически |

Цена ошибки определяется downstream impact и обратимостью, не «важностью AI».
False negative допустимее false merge, когда один ошибочный canonical node
распространяет загрязнение по многим consumers.

## 3. Выбор extraction mechanism

| Условие | Rules / dictionaries | Fine-tuned model | General LLM structured output | Hybrid |
| --- | --- | --- | --- | --- |
| старт без разметки | слабый/средний | слабый | сильный | средний |
| стабильная массовая схема | сильный на узком pattern | сильный | нужно доказать экономику | сильный |
| длинный хвост типов | слабый | требует данных | сильный для candidates | сильный |
| строгая воспроизводимость | сильный | средний при pinned model | средний; provider drift | сильный при logged stages |
| локальный/offline | сильный | сильный | зависит от model deployment | зависит от состава |
| объяснение через evidence | сильный при spans | возможно | нужно явно запросить и проверить spans | сильный при общем claim contract |
| cross-document identity | не решает один | не решает один | candidate scorer, не final authority | нужен resolver/catalog |

Сравнение выполняется на одном corpus snapshot и одной ontology version. Нельзя
переносить числа из biomedical RE на договоры, новости или русский язык.

## 4. Выбор graph model

### 4.1. Query-first scorecard

| Вопрос | Если «да», усиливает |
| --- | --- |
| Нужны variable-depth paths и neighborhood queries online? | property graph / RDF store |
| Нужны глобальные IRIs, vocabularies и межсистемная семантика? | RDF |
| Нужны транзакционные tabular reports и известные joins? | relational |
| Нужны graph algorithms на ограниченном снимке? | NetworkX projection |
| Нужен semantic nearest-neighbor candidate search? | vector index рядом с source/graph data |
| Нужны n-ary events, provenance и temporal qualifiers? | event nodes / statement model, не bare edges |
| Нет подтверждённого graph-shaped query? | не материализовать graph database только ради термина |

RDF определяет graph как set of triples и dataset как default + named graphs;
SHACL добавляет validation shapes. Property graph хранит properties непосредственно
на nodes/relationships. Relational model может быть authoritative store, а
граф — производной projection. Эти варианты можно комбинировать, но тогда
нужно назвать owner identity и source of truth
([RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/),
[SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/)).

## 5. Resolution policy

### 5.1. Лестница решений

1. **Normalize** представления, не сливая records.
2. **Block** plausible candidates по IDs/aliases/lexical/semantic/context.
3. **Score** независимые signals и negative constraints.
4. **Decide** match / NIL / ambiguous / do-not-merge по calibrated thresholds.
5. **Review** high-impact or uncertain merges вместе с evidence.
6. **Record** resolver/version/features/reason и reversible merge event.
7. **Monitor** cluster growth, contradictions и downstream corrections.

### 5.2. Что нельзя считать evidence identity

- только cosine similarity имени;
- только LLM assertion «это одна компания»;
- совпавший короткий alias;
- shared relation, созданная тем же ошибочным extraction;
- отсутствие второго кандидата в неполном catalog.

End-to-end entity linking systems значительно различаются по datasets и
candidate regimes; fair evaluation требует одинаковых settings
([Bast et al., 2023](https://aclanthology.org/2023.emnlp-main.411/)).

## 6. Verification ladder

| Уровень | Проверка | Что ловит |
| --- | --- | --- |
| V0 | JSON parse | syntax only |
| V1 | JSON/Pydantic/schema | types, required fields, enums |
| V2 | ontology/graph shapes | domain/range/cardinality/pattern constraints |
| V3 | evidence-span entailment/check | unsupported or wrong-span claims |
| V4 | cross-source/graph consistency | duplicates, contradictions, temporal conflicts |
| V5 | independent model/rule/human | high-cost semantic errors |
| V6 | downstream task evaluation | graph may be locally plausible but useless |

Strict structured output поднимает систему до V1, но не до V3–V6. Отказ
модели или truncation может нарушить schema даже при constrained output; это
явно отмечает Anthropic. Следовательно, API status/stop reason входит в run
contract
([Anthropic Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)).

## 7. Evaluation contract

### 7.1. Component metrics

- mention: exact/partial span precision, recall, F1; type accuracy;
- relation/event: strict and relaxed F1, direction/role/qualifier accuracy;
- coreference: стандартный набор cluster metrics, плюс downstream effect;
- linking/resolution: accuracy@1, candidate recall, NIL accuracy,
  false-merge/false-split rates, cluster metrics;
- schema: parse rate, constraint violation rate, unknown-type rate;
- provenance: share of accepted claims with resolvable source/version/span;
- temporal/conflict: stale-current errors, contradiction detection/resolution.

### 7.2. Generative/open extraction

Exact-match precision/recall недостаточно, если допустимы разные labels и
gold неполна. GenRES предлагает измерять topic similarity, uniqueness,
granularity, factualness и completeness и показывает две опасности: reference
relations могут быть неполны, а fixed relation/entity sets способны вызывать
hallucinated outputs
([Jiang et al., 2024](https://aclanthology.org/2024.naacl-long.155/)).

Практический golden set поэтому хранит:

- explicit acceptable aliases/relations;
- negative cases и `no relation`;
- ambiguous/NIL cases;
- cross-sentence and multi-relation examples;
- temporal, negated and modal statements;
- high-impact near-duplicate entities;
- source/version and adjudication notes.

### 7.3. Operational economics

```text
cost_per_accepted_claim =
  (model + compute + storage + review + correction) /
  accepted_supported_claims
```

Также измеряются tokens/document, calls/document, p50/p95 latency, retry rate,
manual-review rate, change after adjudication, throughput, correction blast
radius и time-to-reextract after schema/model change. Прайс модели без этих
величин не сравнивает pipelines.

## 8. Minimal reproducible evaluation

1. Заморозить corpus, source versions, language/domain slices.
2. Зафиксировать ontology/schema и identity catalog.
3. Разметить small stratified golden set двумя annotators + adjudication.
4. Запустить простую baseline: rules или one-shot structured extraction.
5. Добавлять staged/iterative/multi-agent механизм только если известен класс
   ошибки, который он должен снизить.
6. Считать component, end-to-end, downstream и cost metrics раздельно.
7. Проверить regression набор после каждого model/prompt/schema change.
8. Версионировать run config и сохранять evidence, не только final graph.

## 9. Stop rules против бесконечного refinement

Refinement прекращается при первом условии:

- all required fields + V0–V2 pass и confidence calibrated above threshold;
- verifier не добавляет нового evidence;
- два последовательных прохода не меняют claim set materially;
- достигнут call/token/latency budget;
- disagreement требует external source или human decision;
- source сам неоднозначен, и правильный результат — `ambiguous`, а не догадка.
