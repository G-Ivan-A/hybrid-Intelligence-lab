---
status: draft
version: 0.1
updated: 2026-08-06
temperature: 0.5
type: research
context: [information-extraction, graph-modeling, taxonomy]
method: taxonomy-building + comparative-analysis
scope: repo-wide
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/471"
related_artifacts:
  - "research/ai-education/information-extraction-graph-modeling/00-introduction.md"
  - "research/ai-education/information-extraction-graph-modeling/10-theory.md"
  - "research/ai-education/information-extraction-graph-modeling/30-decision-framework.md"
  - "research/ai-education/information-extraction-graph-modeling/40-practice-and-cases.md"
  - "research/ai-education/information-extraction-graph-modeling/50-open-research.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/471"
---

# Information Extraction & Graph Modeling: таксономии

## 1. Таксономия задач извлечения

| Код | Задача | Вход → выход | Типичная ошибка |
| --- | --- | --- | --- |
| X1 | document parsing | файл → текст/layout/metadata | потеря таблиц и координат |
| X2 | mention detection / NER | текст → spans + local types | boundary/type error |
| X3 | attribute extraction | mention/context → typed values | unit/date normalization |
| X4 | relation extraction | mentions/text → pairwise claim | wrong predicate/direction |
| X5 | event extraction | text → event + roles + qualifiers | пропущенный participant или modality |
| X6 | coreference | mentions → within-context clusters | wrong antecedent |
| X7 | entity linking | mention → catalog ID / NIL | wrong canonical target |
| X8 | entity resolution | records/mentions → cross-source entity clusters | false merge / false split |
| X9 | open IE | text → schema-free propositions | unstable names/granularity |
| X10 | claim verification | candidate + evidence → verdict | unsupported acceptance |
| X11 | graph construction | accepted claims → nodes/edges/provenance | destructive dedupe / schema drift |

X6–X8 — не синонимы. Coreference отвечает «какие упоминания в дискурсе
совместно ссылаются?», linking — «какой это объект каталога?», resolution —
«какие записи разных источников следует объединить?». Отдельные модели
coreference остаются измеримой специализацией: seq2seq-система Bohnet et al.
сообщает 83.3 F1 на English CoNLL-2012, но это результат конкретного корпуса,
не универсальная гарантия
([Bohnet et al., 2023](https://aclanthology.org/2023.tacl-1.13/)).

## 2. Таксономия методов

### 2.1. По механизму

| Код | Метод | Сильная сторона | Главный trade-off |
| --- | --- | --- | --- |
| M1 | regex/dictionaries/rules | детерминизм, низкая цена, exact audit | хрупкость к вариативности |
| M2 | classical/statistical NLP | быстрый фиксированный label set | feature/domain engineering |
| M3 | fine-tuned encoder/parser | throughput и accuracy на stable schema | разметка и retraining |
| M4 | generative specialized model | joint entities/relations | output alignment и deployment |
| M5 | prompted general LLM | быстрый старт, definitions/few-shot | cost, drift, factual errors |
| M6 | constrained LLM output | parseable schema-conforming result | не гарантирует semantic accuracy |
| M7 | hybrid cascade | rules/NER candidates + LLM semantics + verifier | больше компонентов |
| M8 | retrieval-grounded extraction | catalog/schema/examples доступны в context | retrieval error входит в extraction |

Исследования relation extraction не дают единого победителя. Few-shot GPT-3
оказался близок к SOTA при human-aware evaluation у Wadhwa et al.; более поздняя
работа на complex sentence graphs показывает растущий перевес лёгкого
graph-based parser над четырьмя LLM при росте числа relations
([Wadhwa et al., 2023](https://aclanthology.org/2023.acl-long.868/),
[Taillé et al., 2026](https://aclanthology.org/2026.acl-short.17/)). Вывод:
schema stability и graph complexity — оси решения, не детали benchmark.

### 2.2. По orchestration

| Код | Режим | Когда полезен | Стоп-условие |
| --- | --- | --- | --- |
| O1 | one-shot | малая closed schema, короткий текст, низкий риск | schema+semantic checks pass |
| O2 | staged | разделить detect → extract → resolve → verify | каждый этап имеет измеримый output |
| O3 | iterative refinement | missing fields можно диагностировать | bounded attempts / no new evidence |
| O4 | map-reduce | большой корпус, независимые segments | cross-chunk reconciliation обязателен |
| O5 | ensemble / self-consistency | оценить disagreement | diversity моделей/prompts/evidence |
| O6 | multi-agent roles | разные tools/permissions/independent checks | role-specific metric и budget |
| O7 | human-in-the-loop | высокая цена merge/accept | prioritized queue + evidence |

Двухшаговый подход «generate then organize» улучшал zero-shot NER/RE в
эксперименте Li et al.; это evidence за разделение задач, но не доказательство
конкретного production pipeline
([Li et al., 2024](https://arxiv.org/abs/2402.13364)).

## 3. Таксономия схем

| Код | Схема | Поведение неизвестного типа | Риск |
| --- | --- | --- | --- |
| S0 | schema-less strings | принимается как новая строка | vocabulary explosion |
| S1 | JSON shape | структурная форма без domain semantics | parseable nonsense |
| S2 | typed closed schema | reject / `other` | forced fit, lost novelty |
| S3 | extensible schema | candidate extension queue | governance load |
| S4 | property graph schema | labels, relationship types, properties | application coupling |
| S5 | RDF vocabulary + SHACL | IRIs, reusable semantics, graph shapes | modeling/standards complexity |
| S6 | upper + domain ontology | mapping к общим и предметным понятиям | ontology alignment cost |

JSON Schema/Pydantic валидируют structure/types. Онтология дополнительно задаёт
значение типов и отношений. SHACL формально описывает constraints на RDF nodes
и edges и формирует validation report; это не механизм извлечения
([SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/)).

## 4. Таксономия identity resolution

### 4.1. Нормализация без слияния

- Unicode/case/whitespace/punctuation normalization;
- legal suffixes и controlled aliases;
- даты, деньги, units, телефоны, адреса;
- transliteration и language-aware variants;
- domain identifiers: LEI, DOI, ORCID, tax ID, internal master-data ID.

Нормализованная строка — blocking feature, не окончательный identity verdict.

### 4.2. Candidate generation

- exact canonical ID;
- alias dictionary;
- lexical/fuzzy blocking;
- embedding/semantic candidates;
- graph-neighborhood/context candidates;
- external catalog search.

### 4.3. Scoring и решение

| Signal | Положительный пример | Контрпример |
| --- | --- | --- |
| identifier | одинаковый LEI | recycled/local IDs |
| name | `Open AI` ~ `OpenAI` | однофамильцы/одноимённые компании |
| attributes | domain, address, date | устаревшие данные |
| context | те же products/people | copied text |
| graph neighborhood | устойчивые shared relations | круговая зависимость от ошибочного графа |

Решение должно иметь `matched`, `unmatched/NIL`, `ambiguous`, `do-not-merge` и
причины. Merge хранится как обратимая операция; canonical record не поглощает
source records физически.

## 5. Таксономия графовых представлений

| Представление | Что делает дёшево | Что требует отдельной работы |
| --- | --- | --- |
| relational tables + JSONB | transactions, constraints, reporting, known joins | variable-depth traversal, semantic interoperability |
| NetworkX | algorithms/prototyping on an in-memory graph | persistence, concurrency, access control, large-scale serving |
| property graph / Neo4j | traversal, labeled nodes/edges, properties, Cypher | ontology alignment, operational database cost |
| RDF triple store | global IRIs, vocabularies, SPARQL, linked data | developer learning curve, n-ary modeling choices |
| document store | source-shaped records and flexible ingestion | graph consistency and traversal |
| vector index / pgvector | approximate semantic candidate/retrieval search | exact identity, constraints, paths, provenance semantics |
| hybrid graph + vectors | semantic candidate retrieval + structural filtering | two scoring regimes and more operations |

NetworkX хранит node/edge attributes в словарных структурах и даёт graph
algorithms; его документация не заявляет database semantics
([NetworkX](https://networkx.org/documentation/stable/reference/introduction.html)).
Neo4j даёт constraints и vector indexes, однако ANN может не вернуть точные k
nearest, а memory planning включает JVM/page cache и OS filesystem cache
([Neo4j vector limitations](https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/),
[Neo4j memory configuration](https://neo4j.com/docs/operations-manual/current/performance/vector-index-memory-configuration/)).

`pgvector` — расширение vector similarity search для PostgreSQL, а не graph
model. Рекурсивные CTE и link tables позволяют graph-shaped data, но сравнивать
следует фактические query patterns, а не названия технологий
([pgvector](https://github.com/pgvector/pgvector),
[PostgreSQL recursive queries](https://www.postgresql.org/docs/current/queries-with.html)).

## 6. Таксономия ошибок

| Слой | False positive | False negative | Особая ошибка |
| --- | --- | --- | --- |
| mention | лишний span | пропущенный span | wrong boundary/type |
| relation/event | unsupported relation | missing relation | wrong direction/role/qualifier |
| coreference | wrong cluster link | split cluster | pronoun/exophora ambiguity |
| entity resolution | false merge | false split | identity cascade across graph |
| schema | invalid type/property | forced omission | ontology drift |
| provenance | wrong evidence | missing evidence | stale source version |
| graph | spurious edge | disconnected fact | duplicate node / temporal overwrite |

End-to-end score скрывает слой, который нужно исправлять. False merge обычно
дороже локального false negative: он загрязняет все связи объединённого узла и
может влиять на retrieval, memory и решения агента.
