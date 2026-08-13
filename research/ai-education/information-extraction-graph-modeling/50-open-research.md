---
status: draft
version: 0.1
updated: 2026-08-06
temperature: 0.5
type: research
context: [information-extraction, graph-modeling, open-research, integration, sources]
method: synthesis + evidence-audit
scope: repo-wide
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/471"
related_artifacts:
  - "research/ai-education/information-extraction-graph-modeling/00-introduction.md"
  - "research/ai-education/information-extraction-graph-modeling/10-theory.md"
  - "research/ai-education/information-extraction-graph-modeling/20-taxonomy.md"
  - "research/ai-education/information-extraction-graph-modeling/30-decision-framework.md"
  - "research/ai-education/information-extraction-graph-modeling/40-practice-and-cases.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/471"
---

# Information Extraction & Graph Modeling: открытые вопросы, интеграция и источники

## 1. Открытые вопросы

| ID | Вопрос | Как закрывать |
| --- | --- | --- |
| O1 | Какой extractor лучше на реальном corpus/language mix? | stratified local benchmark, не literature ranking |
| O2 | Как calibrated confidence переносится между model versions? | repeated calibration + drift monitoring |
| O3 | Как измерять open IE при неполном gold? | human adjudication + multi-dimensional evaluation |
| O4 | Какой false-merge cost у конкретных downstream consumers? | inject controlled identity errors and measure blast radius |
| O5 | Какие cross-document coreference methods устойчивы к streaming updates? | temporal corpus benchmark |
| O6 | Как управлять ontology evolution без массового скрытого rewrite? | versioned mapping + re-extraction experiment |
| O7 | Как удалять source/claims и производные graph projections? | lineage/deletion propagation test |
| O8 | Когда property graph выигрывает у relational model по реальным queries/TCO? | same workload benchmark |
| O9 | Как проверять evidence entailment для длинных/табличных документов? | layout-aware golden set |
| O10 | Как отделять источник, который ошибается, от extractor, который ошибается? | source truth state + claim support state separately |
| O11 | Когда multi-agent verification даёт независимость, а не коррелированную стоимость? | diversity ablation by model/tool/evidence |
| O12 | Какие provenance поля достаточны для аудита и воспроизводимости? | incident/re-extraction tabletop |

Эти вопросы требуют данных конкретного продукта. Их нельзя честно закрыть
отраслевым обзором или vendor benchmark.

## 2. Связь модулей знаний

### 2.1. Information Extraction ↔ Retrieval

Retrieval поставляет source segments, schema definitions, demonstrations и
canonical candidates в extraction context. Extraction возвращает структурные
claims, которые позволяют entity/relation/path filtering и GraphRAG.

Циклический риск: retrieval по уже ошибочному графу подаёт extractor только
подтверждающий контекст. Контуры оценки должны разделять source retrieval
recall, extraction accuracy и graph retrieval answer quality. GraphRAG не
исправляет missing или hallucinated edge.

### 2.2. Information Extraction ↔ Memory

Extraction — один из mechanisms записи semantic/episodic memory; Memory владеет
retention, update, invalidation, temporal state и read policy. Graph может быть
memory substrate, но не любая извлечённая тройка должна стать памятью.

Интерфейс: candidate claim + evidence + time + confidence → memory acceptance
policy. Обратный интерфейс: canonical entities/history → resolution context.

### 2.3. Information Extraction ↔ Task Processing

Task Processing планирует источники, chunks, retries, bounded refinement,
independent verification и human queues. Extraction возвращает structured
outcomes и uncertainty, но не должно само расширять мандат или бесконечно
искать подтверждение.

Интерфейс: mandate/budget/schema/source index → extraction run; run возвращает
accepted/candidate/rejected/ambiguous, usage, evidence и unresolved gaps.

### 2.4. Дополнительные критические модули

| Модуль | Почему отдельный |
| --- | --- |
| Ontology & Schema Governance | naming, definitions, versioning и promotion новых concepts — human semantic decision |
| Identity / Master Data | canonical IDs и merge/split history имеют domain ownership |
| Evaluation | golden sets, adjudication и drift не являются побочным логом extractor |
| Observability & Lineage | source→span→claim→entity→projection trace пересекает все stages |
| Security / Privacy / Licensing | untrusted sources, prompt injection, PII, right-to-delete и usage rights влияют на ingestion/commit |
| Human Review Operations | приоритет, evidence UI, reviewer disagreement и feedback quality определяют реальную точность |

## 3. Ранжирование гипотез

### 3.1. Несущие

- H1: schema conformance ≠ factual correctness.
- H3: LLM не универсально заменяет specialized extraction.
- H6: semantic similarity ≠ entity identity.
- H8: graph не универсальная final representation.
- H11: deduplication/merge — semantic decision с blast radius.
- H14: downstream graph retrieval не компенсирует плохой input graph.
- H16: open extraction переносит, а не устраняет ontology work.

### 3.2. Условные

- one-shot выигрывает только на измеренном low-risk slice;
- ontology улучшает extraction, если definitions и unknown policy корректны;
- human review помогает при наличии evidence, clear definitions и manageable queue;
- multi-agent помогает при независимых tools/evidence и bounded roles.

### 3.3. Что может изменить выводы

- независимый multi-domain benchmark, где один end-to-end LLM стабильно
  превосходит specialized/hybrid baselines по accuracy, TCO и reproducibility;
- reliable calibrated semantic confidence across model upgrades;
- storage system, одновременно демонстрирующий relational constraints,
  graph traversal, semantic interoperability и lower TCO на representative
  workloads без additional operational complexity.

## 4. Что паттерн показал на четвёртом домене

Шесть файлов снова разделили slow conceptual layer от dynamic framework layer.
Обратная связь из practice изменила theory: event benchmarks потребовали
qualifiers/time, а provider structured-output limitations — явного run/stop
state. Это подтверждает полезность механизма «практика → теория».

<!-- CROSS-REVIEW [Codex-validation]: ключевое расхождение перекрёстной проверки. Утверждение о сработавшей обратной связи «практика → теория» — единственное такое утверждение в корпусе из восьми модулей, но оно не подтверждается артефактами: ссылок 40 → 10 и 10 → 40 в теле нет, у гипотез H1–H16 не указан источник вердикта, изменение теории не помечено ссылкой на вызвавшее его наблюдение, а задачи по триггеру P5 в pr-ops/backlog.md нет ни одной. RFC требует по триггеру P5 именно заводимую задачу и пометку кейса ссылкой на неё. Обратная связь, вероятно, действительно произошла внутри одного прогона исполнителя, но она произошла в голове модели, а не в артефакте: воспроизвести или оспорить её внешний читатель не может. Это ровно тот дефект, против которого P5 и вводился, — «практика → теория» остаётся декларацией, пока не оставляет следа. -->


Однако эта работа не делает домены независимыми: Retrieval, Task Processing,
Memory и Information Extraction выполнены в одной repository lineage и близкой
методике. Human decision о lifecycle Reference Research Pattern остаётся за
пределами исследования.

## 5. Глоссарий

| Термин | Рабочее определение |
| --- | --- |
| mention | span текста, потенциально ссылающийся на entity/event |
| canonical entity | объект со стабильным ID и управляемой identity history |
| claim | извлечённое утверждение с qualifiers и evidence |
| coreference | связывание mentions, ссылающихся на одно в контексте |
| entity linking | mapping mention к известному catalog ID или NIL |
| entity resolution | cross-record clustering/merge в canonical entities |
| normalization | приведение representation/value к controlled form без обязательного merge |
| ontology | формальная/контролируемая семантика concepts и relations |
| provenance | происхождение и история производства/изменения данных |
| property graph | nodes/relationships с labels и properties |
| RDF | graph data model из triples и IRIs/literals/blank nodes/triple terms |
| SHACL | язык shapes/constraints и validation RDF graphs |
| NIL | mention, не сопоставленное с catalog entity |
| false merge | объединение разных entities |
| false split | сохранение одного entity как нескольких |
| GraphRAG | retrieval/generation, использующий graph structure; downstream от construction |

## 6. Источники

### S1 — спецификации и официальная документация

1. OpenAI. [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
   и [Agents SDK: Agents](https://openai.github.io/openai-agents-python/agents/).
   API semantics; model/version support проверяется на дату внедрения.
2. Anthropic. [Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs).
   JSON/strict-tool guarantees, limitations, cache/latency; не quality benchmark.
3. LangChain. [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output)
   и [LLMGraphTransformer](https://python.langchain.com/api_reference/experimental/graph_transformers/langchain_experimental.graph_transformers.llm.LLMGraphTransformer.html).
   Framework capability; graph transformer experimental.
4. LlamaIndex. [Property Graph Index and extractors](https://docs.llamaindex.ai/en/stable/module_guides/indexing/lpg_index_guide/).
   Framework capability; не independent evaluation.
5. W3C. [RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/) и
   [SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/). Data model и shapes;
   актуальный статус спецификаций проверяется отдельно.
6. NetworkX. [Introduction / data structure](https://networkx.org/documentation/stable/reference/introduction.html)
   и [Graph class](https://networkx.org/documentation/stable/reference/classes/graph.html).
7. Neo4j. [Constraints](https://neo4j.com/docs/cypher-manual/current/schema/constraints/),
   [vector indexes](https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/),
   [memory configuration](https://neo4j.com/docs/operations-manual/current/performance/vector-index-memory-configuration/).
8. PostgreSQL / pgvector. [Recursive queries](https://www.postgresql.org/docs/current/queries-with.html),
   [pgvector](https://github.com/pgvector/pgvector).
9. Stanford NLP Group. [CoreNLP Coreference](https://stanfordnlp.github.io/CoreNLP/coref.html).

### S2 — papers и benchmarks

10. Wadhwa, Amir, Wallace (2023). [Revisiting Relation Extraction in the Era of LLMs](https://aclanthology.org/2023.acl-long.868/).
11. Jiang et al. (2024). [GenRES](https://aclanthology.org/2024.naacl-long.155/).
12. Li, Ramprasad, Zhang (2024). [Generate-and-Organize structured IE](https://arxiv.org/abs/2402.13364).
13. Li, Wang, Ke (2023). [LLMs as Zero-shot Relation Extractors](https://aclanthology.org/2023.findings-emnlp.459/).
14. Xu et al. (2022). [Realistic Low-resource Relation Extraction](https://aclanthology.org/2022.findings-emnlp.29/).
15. Taillé et al. (2026). [LLMs Underperform Graph-Based Parsers on Complex Graphs](https://aclanthology.org/2026.acl-short.17/).
16. Brokman et al. (2025). [End-to-end zero-shot biomedical RE](https://aclanthology.org/2025.wasp-main.6/).
17. Gong, Zheng, Hu (2025). [EventRelBench](https://aclanthology.org/2025.findings-emnlp.482/).
18. Bohnet, Alberti, Collins (2023). [Seq2seq Coreference Resolution](https://aclanthology.org/2023.tacl-1.13/).
19. Bast et al. (2023). [Fair Evaluation of Entity Linking Systems](https://aclanthology.org/2023.emnlp-main.411/).
20. Zhu et al. (2023). [LLMs for KG Construction and Reasoning](https://arxiv.org/abs/2305.13168).

### S3/S4 — implementations и vendor case

21. LangChain. [langchain-experimental repository](https://github.com/langchain-ai/langchain-experimental).
22. Rasmussen et al. / Zep (2025). [A Temporal Knowledge Graph Architecture for Agent Memory](https://arxiv.org/abs/2501.13956).
    Vendor-authored implementation/evaluation; переносимость требует проверки.

## 7. Самоаудит

### 7.1. Покрытие Definition of Done

- таксономия extraction, orchestration, schemas, identity и graph models — `20`;
- сравнение JSON/Pydantic, frameworks, NetworkX, Neo4j, PostgreSQL/pgvector,
  RDF/SHACL — `20`, `30`, `40`;
- coreference/normalization/entity resolution — `10 §2`, `20 §4`, `30 §5`;
- связь Retrieval/Memory/Task Processing и дополнительные interfaces — `50 §2`;
- самостоятельный educational appendix — `40 §5`;
- sources и границы применимости — этот раздел и inline links;
- проектных architecture prescriptions и изменений правил нет.

### 7.2. Признанные слабости

- нет локального corpus benchmark: невозможно выбрать model/tool;
- официальный LangChain graph transformer относится к experimental surface и
  API может измениться;
- часть 2025–2026 papers — новые результаты, требующие репликации;
- vendor case Graphiti/Zep не является независимым сравнением;
- глубоко не покрыты OCR/layout, multilingual/cross-lingual linking, graph
  security, privacy/licensing и ontology alignment algorithms;
- cost comparison качественный, потому что provider prices и model lineup
  нестабильны, а representative workload не задан.

### 7.3. Что намеренно не сделано

- не выбран стек и не спроектирован Source Intelligence Engine;
- не написан RFC и не предложены изменения репозитория;
- не объявлены benchmark numbers универсальными;
- не приравнены schema validity, model confidence и truth;
- не создан отдельный insight на каждый source: выводы связаны в одном
  issue-scoped research module и зарегистрированы в Base Registry.
