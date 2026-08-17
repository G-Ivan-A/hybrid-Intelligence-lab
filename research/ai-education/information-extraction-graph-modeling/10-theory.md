---
status: draft
version: 0.1
updated: 2026-08-06
temperature: 0.5
type: research
context: [information-extraction, graph-modeling, theory, object-model]
method: conceptual-analysis + adversarial-hypotheses
scope: repo-wide
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/471"
related_artifacts:
  - "research/ai-education/information-extraction-graph-modeling/00-introduction.md"
  - "research/ai-education/information-extraction-graph-modeling/20-taxonomy.md"
  - "research/ai-education/information-extraction-graph-modeling/30-decision-framework.md"
  - "research/ai-education/information-extraction-graph-modeling/40-practice-and-cases.md"
  - "research/ai-education/information-extraction-graph-modeling/50-open-research.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/471"
---

# Information Extraction & Graph Modeling: концептуальная рамка

<!-- CROSS-REVIEW [Codex-validation]: P5 RFC (обратная связь «практика → теория»): ссылок на 40-practice-and-cases.md в теле нет, файл перечислен только во frontmatter. Таблица гипотез H1–H16 с вердиктами («опровергнута», «условна») — самое сильное основание для P5 во всём корпусе: вердикт по построению является результатом столкновения утверждения с практикой. Но источник вердикта не указан ни у одной из шестнадцати гипотез, поэтому проверить, какое именно наблюдение практики его дало, по артефактам нельзя. Сработавших триггеров P5 (заведённых задач по расхождению практики с рамкой): 0. -->

## 1. Два контракта, а не один prompt

Information extraction преобразует наблюдаемый материал в кандидаты
утверждений; graph modeling задаёт, как эти утверждения сохраняют идентичность,
семантику и доказательства. Полезная сигнатура конвейера:

```text
Mentions  = Detect(document, span_policy)
Claims    = Extract(Mentions, extraction_schema, context)
Entities  = Resolve(Claims.participants, identity_policy, catalog)
Accepted  = Validate(Claims, Entities, graph_schema, evidence_policy)
Graph'    = Commit(Graph, Accepted, provenance, valid_time, system_time)
```

`Extract` не имеет права молча выполнять `Resolve`, `Validate` и `Commit`.
Иначе невозможно отличить ошибку чтения текста от ошибочного слияния сущностей
или нарушения модели графа.

### 1.1. Claim как минимальная единица

Минимальная практическая запись:

```json
{
  "subject_mention": "эта компания",
  "predicate": "acquired",
  "object_mention": "Acme",
  "qualifiers": {"announced_at": "2026-01-10", "modality": "reported"},
  "evidence": {"source_id": "doc-17", "span_start": 104, "span_end": 148},
  "extractor": {"name": "pipeline-x", "version": "..."},
  "confidence": 0.71,
  "validation_state": "candidate"
}
```

Канонические IDs добавляются после resolution. `confidence` — сигнал модели,
а не вероятность истинности без calibration. Evidence span позволяет повторно
проверить claim при смене модели, схемы или источника.

## 2. Объектная модель

| ID | Объект | Инвариант |
| --- | --- | --- |
| E1 | Source | имеет стабильный ID, URI/locator, версию или content hash |
| E2 | Document version | неизменяемый снимок текста и metadata |
| E3 | Segment | сохраняет координаты относительно версии документа |
| E4 | Mention | surface form + span + локальный тип; ещё не каноническая сущность |
| E5 | Entity candidate | гипотеза о реальном объекте и набор упоминаний |
| E6 | Canonical entity | стабильный ID, aliases, тип и история merge/split |
| E7 | Relation / event claim | утверждение с ролями, qualifiers и состоянием |
| E8 | Extraction schema | допустимые типы, поля, cardinality и определения |
| E9 | Ontology / vocabulary | устойчивые понятия и их семантические связи |
| E10 | Evidence | точная связь claim → source/version/span |
| E11 | Provenance | кто/что/когда/какой версией произвёл и изменил claim |
| E12 | Validation result | machine/human verdict, причина, применённая schema version |
| E13 | Graph projection | выбранное представление accepted claims для query/analysis |
| E14 | Evaluation case | вход, gold/acceptable alternatives и тип ошибки |
| E15 | Extraction run | конфигурация, usage, latency, failures и produced IDs |

Различение E4/E5/E6 критично. Одинаковая строка может обозначать разные
объекты, а разные строки — один. Канонический узел не должен терять исходные
mention/evidence records.

## 3. Границы семантики

### 3.1. Тройка недостаточна для события

`Apple — acquired → Acme` скрывает дату, роль источника, статус сделки,
валюту, сумму, отрицание и модальность. Варианты:

- relation с properties — удобно в property graph;
- event node с participant roles — лучше при n-арных событиях;
- RDF statement/triple term + qualifiers/provenance — для interoperable
  semantic model;
- relational fact table — когда запросы известны и graph traversal не нужен.

Модель выбирается формой вопросов, а не словом «граф».

### 3.2. Open-world и closed-world

В closed-world extraction отсутствующее значение часто означает «не найдено в
этом документе по этой схеме». Оно не означает «в мире отсутствует». RDF
обычно работает с open-world semantics; прикладная таблица часто неявно
трактуется closed-world. Этот выбор влияет на negative facts, completeness и
валидацию.

### 3.3. Время

Нужно различать:

- source time — дата публикации/получения;
- valid time — когда claim считается истинным в предметном мире;
- transaction/system time — когда запись появилась или изменилась в системе;
- extraction time и model/schema version.

Без этого обновлённый источник перезаписывает историю и создаёт ложные
противоречия. Темпоральный подход в Graphiti/Zep показывает ценность
bi-temporal lineage для agent memory, но vendor paper не доказывает, что такой
граф нужен любому продукту
([Rasmussen et al., 2025](https://arxiv.org/abs/2501.13956)).

## 4. Точки решений

| ID | Решение | Альтернативы | Наблюдаемое последствие |
| --- | --- | --- | --- |
| D1 | единица входа | sentence / passage / document / corpus | context против cost и missed cross-span links |
| D2 | схема | closed / extensible / open | precision и governance новых типов |
| D3 | extractor | rules / specialized model / LLM / hybrid | annotation, latency, portability |
| D4 | orchestration | one-shot / staged / iterative / multi-agent | число проходов и диагностируемость |
| D5 | identity policy | exact / aliases / linking / probabilistic resolution | false merges и false splits |
| D6 | fact granularity | triple / qualified relation / event | выразимость и сложность query |
| D7 | graph model | relational / property / RDF / in-memory | constraints, traversal, interoperability |
| D8 | acceptance | auto / threshold / verifier / human gate | coverage, risk и review load |
| D9 | conflict policy | coexist / rank / supersede / reject | auditability и current view |
| D10 | provenance depth | source / span / run / full lineage | storage против explainability |
| D11 | evaluation | component / end-to-end / downstream | локализация ошибки |
| D12 | update mode | append / upsert / bitemporal / rebuild | reversibility и freshness |

## 5. Гипотезы для опровержения

| ID | Гипотеза | Статус после обзора | Что её опровергает / ограничивает |
| --- | --- | --- | --- |
| H1 | Валидный JSON означает корректный факт | опровергнута | grammar constrains form, not truth |
| H2 | Один проход дешевле каскада | условна | повторные исправления и human review могут стоить дороже |
| H3 | LLM заменяет NER/RE модели | опровергнута широко | сложные графы и стабильные домены сохраняют преимущество specialized parsers |
| H4 | Больше контекста всегда повышает recall | условна | distractors, positional effects, token cost |
| H5 | Онтология автоматически повышает качество | условна | плохие/слишком узкие классы принуждают hallucinated mapping |
| H6 | Embedding similarity решает entity identity | опровергнута | похожие имена/описания могут быть разными объектами |
| H7 | Coreference можно выполнить после extraction без потерь | условна | relation roles могут зависеть от разрешения местоимений до/внутри extraction |
| H8 | Knowledge graph — лучшая конечная форма | опровергнута широко | известные aggregation/reporting queries проще в relational model |
| H9 | Multi-agent consensus независим | опровергнута широко | одинаковые модели, prompts и evidence дают correlated errors |
| H10 | Precision/recall достаточно | опровергнута для generative/open extraction | granularity, factualness и incomplete gold требуют дополнительных измерений |
| H11 | Дедупликация — безопасная housekeeping операция | опровергнута | merge меняет семантику всех adjacent claims |
| H12 | Confidence можно сравнивать между моделями | условна | нужна calibration на домене и стабильная версия |
| H13 | Graph constraints можно применить только при записи | опровергнута | early schema feedback снижает invalid candidates, post-write checks ловят global constraints |
| H14 | GraphRAG компенсирует плохое extraction | опровергнута | retrieval не восстанавливает отсутствующий/ложный fact |
| H15 | Human review каждого claim гарантирует качество | условна | reviewer fatigue и отсутствие evidence/definitions делают review фиктивным |
| H16 | Open extraction избавляет от ontology work | опровергнута | ontology work переносится в clustering, naming и mapping после extraction |

## 6. Почему эти гипотезы важны

Они разделяют три разные цели: получить parseable object, получить
семантически полезный candidate и принять auditable fact. Производители API
документируют первую цель; NLP benchmarks чаще измеряют вторую; продукту нужна
третья. Универсальный «лучший extractor» невозможен без конкретных costs of
false positive/negative, corpus и downstream questions.
