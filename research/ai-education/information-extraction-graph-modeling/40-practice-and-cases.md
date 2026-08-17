---
status: draft
version: 0.1
updated: 2026-08-06
temperature: 0.5
type: research
context: [information-extraction, graph-modeling, frameworks, industry-cases, education]
method: framework-comparison + case-analysis
scope: repo-wide
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/471"
related_artifacts:
  - "research/ai-education/information-extraction-graph-modeling/00-introduction.md"
  - "research/ai-education/information-extraction-graph-modeling/10-theory.md"
  - "research/ai-education/information-extraction-graph-modeling/20-taxonomy.md"
  - "research/ai-education/information-extraction-graph-modeling/30-decision-framework.md"
  - "research/ai-education/information-extraction-graph-modeling/50-open-research.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/471"
---

# Information Extraction & Graph Modeling: практика, инструменты и образовательный срез

<!-- CROSS-REVIEW [Codex-validation]: P2 RFC в теле файла не выполнен — markdown-ссылок на 10-theory.md, 20-taxonomy.md и 30-decision-framework.md нет, все ссылки внешние. Отличие от модулей evaluation и tool-use в том, что здесь основание объявлено во frontmatter (related_artifacts перечисляет все пять соседних файлов), то есть граф модуля машинно читаем. Но критерий P2 — ссылка, видимая читателю практики в точке утверждения; YAML-перечисление в шапке этой функции не выполняет: читатель кейса по-прежнему не знает, какой вывод рамки решений этот кейс подтверждает или опровергает. Оценка: не выполнен, но ближе к выполнению, чем у двух других модулей Codex. -->

## 1. Фреймворки: разные уровни абстракции

### 1.1. LangChain

LangChain models expose structured output through provider-native schema or
tool-calling strategies. Отдельный `LLMGraphTransformer` превращает documents
в graph documents и допускает allowed node/relation types и strict filtering,
но живёт в experimental package. Это удобный adapter/prototype, а не доказанный
resolver, provenance model или quality guarantee
([LangChain structured output](https://docs.langchain.com/oss/python/langchain/structured-output),
[LLMGraphTransformer API](https://python.langchain.com/api_reference/experimental/graph_transformers/langchain_experimental.graph_transformers.llm.LLMGraphTransformer.html),
[langchain-experimental](https://github.com/langchain-ai/langchain-experimental)).

Практический вывод: `allowed_nodes` ограничивает vocabulary output, но
canonical IDs, merge/split и evidence validation остаются приложению.

### 1.2. LlamaIndex

`PropertyGraphIndex` поддерживает paths extraction и property-graph stores.
`SimpleLLMPathExtractor` извлекает свободные paths, `SchemaLLMPathExtractor`
задаёт возможные entity/relation types и validation schema; implicit extractors
могут добавлять already-known relations. Фреймворк связывает ingestion и graph
retrieval, но storage/index abstraction не решает истинность facts
([LlamaIndex PropertyGraphIndex](https://docs.llamaindex.ai/en/stable/module_guides/indexing/lpg_index_guide/),
[Property Graph Index guide](https://docs.llamaindex.ai/en/stable/module_guides/indexing/lpg_index_guide/)).

Практический вывод: различие simple/schema extraction хорошо отражает
open/closed axes, но entity resolution между documents требует отдельной
политики.

### 1.3. OpenAI Agents SDK

`Agent(output_type=...)` принимает Pydantic, dataclass, TypedDict и другие
типы, которые оборачиваются Pydantic `TypeAdapter`; SDK использует structured
outputs для final result. Code-driven orchestration может chain extractors,
запускать evaluator loop или parallel agents. SDK не содержит специальной
ontology/KG construction semantics
([Agents: output types](https://openai.github.io/openai-agents-python/agents/),
[Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/)).

Практический вывод: SDK — orchestration и typed boundary. Extract/resolve/
validate contracts проектируются поверх него.

### 1.4. Anthropic Claude

Claude API предоставляет JSON outputs и strict tool use. Схема компилируется в
grammar; первый вызов новой схемы получает latency compilation, cache зависит
от schema/tool set, сложность схемы ограничена. Refusal и `max_tokens` могут
вернуть output вне schema; citations несовместимы с strict JSON output
([Anthropic Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)).

Практический вывод: если нужны и strict JSON, и traceable quotes, evidence spans
лучше передавать как offsets/IDs в schema и проверять против input, а не считать
platform citations частью того же response.

### 1.5. Сводка

| Инструмент | Native primitive | Graph-specific layer | Что остаётся приложению |
| --- | --- | --- | --- |
| LangChain | structured output | experimental graph transformer | identity, provenance, verification, storage policy |
| LlamaIndex | Pydantic/schema extraction | PropertyGraphIndex + path extractors/stores | cross-source resolution, acceptance, ontology governance |
| OpenAI Agents SDK | `output_type`, tools, orchestration | нет domain KG primitive | полный domain pipeline |
| Anthropic API | JSON outputs, strict tools | нет domain KG primitive | полный domain pipeline |

Фреймворк и модель нельзя сравнивать одной колонкой «accuracy»: один и тот же
framework может использовать разные providers, prompts, schemas и stores.

## 2. Хранилища и analytical tools

### 2.1. NetworkX

Подходит для прототипа graph model, connected components, centrality, path
analysis и offline validation на снимке. Node IDs могут быть любыми hashable
objects, nodes/edges несут attributes. Не заменяет ingestion catalog,
transactional persistence или concurrent service
([NetworkX Graph](https://networkx.org/documentation/stable/reference/classes/graph.html)).

### 2.2. Neo4j

Property graph, Cypher, constraints и indexes подходят для online traversal и
application graph. Vector indexes дают approximate nearest-neighbor search,
имеют version-dependent capabilities и operational memory requirements.
Entity uniqueness constraints помогают после выбора canonical key, но не
выбирают ключ и не разрешают identity автоматически
([Neo4j constraints](https://neo4j.com/docs/cypher-manual/current/schema/constraints/),
[Neo4j vector indexes](https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/)).

### 2.3. PostgreSQL + JSONB/pgvector

Полезен, когда authoritative entities/claims, transactions и reporting уже
relational, а semantic candidates нужны через vector index. Recursive queries
покрывают некоторые traversals; pgvector — similarity extension, не graph DB.
Преимущество «одна операционная система» нужно проверять на реальных paths и
объёмах, а не предполагать
([pgvector](https://github.com/pgvector/pgvector),
[PostgreSQL WITH queries](https://www.postgresql.org/docs/current/queries-with.html)).

### 2.4. RDF / SHACL

RDF полезен для reusable vocabularies, globally scoped IRIs, graph datasets и
interoperability; SHACL — для shape constraints и machine-readable validation
reports. Цена — modeling discipline и иной query/tooling stack. Это сильный
кандидат при межсистемной семантике, но не default для каждого локального graph
([RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/),
[SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/)).

## 3. Реальные evidence и ограничения

### 3.1. Relation extraction: метрика меняет вывод

Wadhwa et al. показали near-SOTA few-shot GPT-3 при human evaluation, потому
что exact match занижал generative outputs. Jiang et al. позже формализовали
multi-dimensional GenRES и показали неполноту human references и риск
hallucination от fixed candidate sets. Значит, «LLM хуже/лучше» без протокола
matching и adjudication — слабое утверждение
([Wadhwa et al., 2023](https://aclanthology.org/2023.acl-long.868/),
[Jiang et al., 2024](https://aclanthology.org/2024.naacl-long.155/)).

### 3.2. Complexity breaks broad claims

Taillé et al. сравнили четыре LLM с graph-based parser на шести datasets и
нашли растущий разрыв в пользу меньшего parser при увеличении числа relations.
Biomedical benchmark Brokman et al. также сообщает приближение zero-shot LLM к
supervised methods лишь на части datasets и трудности с complex multi-relation
inputs
([Taillé et al., 2026](https://aclanthology.org/2026.acl-short.17/),
[Brokman et al., 2025](https://aclanthology.org/2025.wasp-main.6/)).

### 3.3. Cross-sentence and event relations remain hard

Low-resource study Xu et al. отмечает запас улучшения на cross-sentence
contexts с несколькими triples. EventRelBench (35K questions) покрывает
coreference, temporal, causal и supersub event relations на sentence/document
levels и сообщает, что современные LLM ещё отстают
([Xu et al., 2022](https://aclanthology.org/2022.findings-emnlp.29/),
[Gong et al., 2025](https://aclanthology.org/2025.findings-emnlp.482/)).

### 3.4. Industry case: temporal graph memory

Graphiti/Zep представляет facts, entities, episodes и bi-temporal relations и
публикует evaluation для agent memory. Это содержательный case связи extraction
с Memory и временем; результаты остаются vendor-authored и не переносятся на
любой corpus без локальной проверки
([Rasmussen et al., 2025](https://arxiv.org/abs/2501.13956)).

## 4. Паттерны pipeline

### 4.1. One-shot closed schema

```text
document → structured output → V0/V1 → accepted/candidate queue
```

Подходит для low-risk bootstrap и малой схемы. Обязательны negative examples и
evidence spans. Не выполняет cross-document resolution.

### 4.2. Staged high-precision

```text
parse → mentions → relation/event candidates → resolve IDs
      → schema/evidence checks → human review for high-impact cases → commit
```

Диагностируем, но дороже по latency/operations. Каждый этап должен уменьшать
конкретный error class.

### 4.3. Discovery plus governed promotion

```text
open extraction → cluster predicates/types → label/definition review
                → map to accepted vocabulary → re-extract/evaluate → promote
```

Новые strings не попадают сразу в production ontology. Open extraction
обнаруживает candidates, а не принимает semantic decisions.

### 4.4. Multi-agent checker

Extractor и verifier полезно разделять, если verifier получает независимый
инструмент: exact source lookup, catalog, schema engine или human evidence.
«Ещё один prompt той же модели» — слабая независимость; disagreement следует
сохранять, не усреднять в уверенный fact.

## 5. Приложение A. Образовательный срез для бизнес-аналитиков

### A.1. Восемь тезисов

1. Сначала формулируется downstream decision/query, затем entity/relation model.
2. Mention, source record и canonical entity — разные объекты.
3. JSON Schema гарантирует форму; factual evidence и validation задаются отдельно.
4. «Не найдено» не равно «не существует».
5. Coreference, linking, normalization и resolution требуют разных критериев.
6. Every accepted claim должен вести к версии источника и фрагменту evidence.
7. Graph database выбирается по query patterns, а не по моде или наличию LLM.
8. Quality — набор component, downstream и cost metrics, а не одна accuracy.

### A.2. Минимальный словарь требований

`mention`, `entity`, `canonical ID`, `relation`, `event`, `role`, `qualifier`,
`ontology`, `closed/open schema`, `coreference`, `entity linking`, `NIL`,
`false merge`, `false split`, `provenance`, `evidence span`, `valid time`,
`system time`, `golden set`, `precision`, `recall`, `constraint violation`.

### A.3. Чек-лист постановки задачи

1. Какие бизнес-вопросы должен поддержать результат?
2. Что является entity, event и просто attribute?
3. Какие types/relations разрешены и что делать с неизвестными?
4. Что означает «тот же объект» и какие canonical catalogs доступны?
5. Что дороже: false positive, false negative, false merge или false split?
6. Какой context нужен: sentence, document, previous documents?
7. Как представляются отрицание, предположение, время и конфликт источников?
8. Какой source/version/span обязан сопровождать claim?
9. Какие claims принимаются автоматически, а какие идут человеку?
10. Как устроены golden set, negative/ambiguous/NIL examples и adjudication?
11. Какие latency, throughput, review-rate и cost limits действуют?
12. Как переизвлечь и откатить данные после смены schema/model/source?

### A.4. Плохие и проверяемые формулировки

| Плохо | Проверяемее |
| --- | --- |
| «Извлечь все сущности» | «Извлечь Organization/Person mentions по definition v3; неизвестные типы — candidates» |
| «Склеить дубли» | «Предлагать merge при exact registry ID; остальные — ambiguous queue; считать false-merge rate» |
| «Построить граф знаний» | «Поддержать queries Q1–Q5; claim хранит source version/span и valid time» |
| «Использовать JSON mode» | «Output проходит schema v2, но acceptance требует evidence entailment и constraints» |
| «Точность 95%» | «Entity/relation F1 по slice, NIL accuracy, false merges, provenance coverage и review rate» |

### A.5. Семинарское упражнение

Дать группе два документа: «Apple купила Acme» и «Она опровергла завершение
сделки; Apple Records не участвовала». Участники должны:

1. выделить mentions и candidates;
2. не слить Apple Inc. и Apple Records;
3. представить announcement/denial как события с modality/time;
4. приложить evidence spans;
5. определить ambiguous state вместо выдуманного verdict;
6. составить component metrics и три downstream query.

## 6. Обратная связь «практика → теория»

| Наблюдение практики | Изменение медленного слоя |
| --- | --- |
| strict JSON допускает refusal/truncation вне schema | V0/V1 включают API stop state, а не только parser |
| LlamaIndex разделяет simple/schema path extractors | ось open/closed schema сделана самостоятельной |
| graph transformers не дают canonical resolution | E4 mention, E5 candidate и E6 entity разделены |
| event benchmarks выделяют temporal/causal/coreference | bare triples признаны недостаточными для событий |
| Neo4j vector search остаётся ANN с отдельной memory economics | vector index отделён от graph semantics/storage decision |
