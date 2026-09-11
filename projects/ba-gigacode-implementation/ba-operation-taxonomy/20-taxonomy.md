---
status: draft
version: 0.1
updated: 2026-09-10
temperature: 0.3
type: research
context: [ba, taxonomy, operation, catalog, skill-decomposition, deprecation, issue-571]
method: contract-design + closed-vocabulary + per-item-verification
scope: mango-only
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571"
based_on:
  - projects/ba-gigacode-implementation/ba-operation-taxonomy/10-theory.md
  - projects/ba-gigacode-implementation/ba-process-taxonomy/20-taxonomy.md
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571"
---

# Каталог операций и разложение навыков

## 1. Правила каталога

| Правило | Формулировка |
| --- | --- |
| `OC-1` | Словарь закрыт. Значение вне каталога не используется; потребность в новом значении открывает задачу с непокрытым случаем (`T-2`). |
| `OC-2` | Каждая операция объявляет шесть полей контракта ([`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-operation-taxonomy/10-theory.md), §4). Ниже приведены пять; шестое — ярус — вынесено в отдельную колонку. |
| `OC-3` | Операция не привязана к процессу: она вызывается любым навыком, чей вход удовлетворяет контракту. |
| `OC-4` | Имя операции — глагол предметной области, а не действие с интерфейсом. `read-file` не является операцией. |
| `OC-5` | Ярус в каталоге — нижняя граница. Навык может поднять ярус, но не опустить. |

Итого **31 операция** в пяти классах.

## 2. Каталог

### 2.1 `extract` — извлечение (6)

Содержание выхода целиком присутствует во входе. Новых утверждений не
появляется; отсутствующий элемент даёт отказ, а не догадку.

| Операция | Вход | Единственный выход | Условие отказа | Ярус |
| --- | --- | --- | --- | --- |
| `extract-entities` | связный текст предметной области | перечень сущностей с цитатой-подтверждением на каждую | текст не содержит предметных сущностей | `G6` |
| `extract-actors` | связный текст или `A-CORE` | перечень акторов: роль, тип (человек, агент, Система), цитата | роль не названа во входе явно | `G6` |
| `extract-statements` | связный текст | перечень утверждений о желаемом поведении с цитатами | во входе нет утверждений о поведении | `G6` |
| `extract-constraints` | связный текст или внешний документ | перечень ограничений: предмет, значение, источник | ограничения не заявлены | `G6` |
| `extract-metrics` | связный текст | перечень измеримых показателей: имя, значение, единица | числовых показателей нет | `G6` |
| `extract-source-reference` | элемент и его источник | ссылка: документ, раздел, страница или таймкод, дословная цитата | цитата не находится в источнике | `G6` |

`extract-actors` существует отдельно от `extract-entities`, потому что актор —
самостоятельная сущность мета-модели, а не разновидность сущности предметной
области: без него генерация UML изобретает действующих лиц.

### 2.2 `transform` — преобразование (7)

Меняется форма или структура, смысл сохраняется. Проверка — схемой и полнотой
переноса.

| Операция | Вход | Единственный выход | Условие отказа | Ярус |
| --- | --- | --- | --- | --- |
| `normalize-text` | сырой текст, расшифровка, письмо | нормализованный текст с сохранением атрибуции реплик | вход не является текстом | `G2` |
| `deduplicate-items` | перечень однородных элементов | перечень без дублей и с записью о каждом слиянии | элементы разнородны по классу | `G2` |
| `split-statement` | составное утверждение | перечень утверждений, каждое из которых атомарно | утверждение уже атомарно (возвращается отказ разбиения) | `G2` |
| `classify-item` | элемент и закрытый словарь значений | элемент с ровно одним значением классификации | ни одно значение словаря не подходит | `G2` |
| `map-to-slot` | элемент и объявленный скелет документа | пара «элемент → раздел» | для элемента нет раздела в скелете | `G2` |
| `link-elements` | два элемента и тип связи | ребро следа: источник, приёмник, тип, основание | один из концов не существует | `G2` |
| `render-projection` | структурированная модель и целевая нотация | текст проекции в нотации (UML, BPMN, таблица) | модель не полна для нотации | `G2` |

`render-projection` объявлен преобразованием, а не порождением: диаграмма —
проекция уже существующей модели. Если в диаграмме появляется то, чего в модели
нет, нарушен контракт, а не «дорисован смысл».

### 2.3 `generate` — порождение (5)

Появляется содержание, которого во входе не было. Класс с наибольшим риском:
каждая операция обязана объявить основание и вернуть отказ при его отсутствии.

| Операция | Вход | Единственный выход | Условие отказа | Ярус |
| --- | --- | --- | --- | --- |
| `generate-statement` | элементы `A-CORE` и целевая форма утверждения | одно утверждение целевой формы со ссылкой на основание | основание отсутствует или не покрывает утверждение | `G6` |
| `generate-question` | одна неоднозначность | один вопрос, отвечаемый одним фактом | неоднозначность не сформулирована | `G2` |
| `generate-acceptance-criterion` | атомарное требование | один проверяемый критерий приёмки | требование не атомарно | `G6` |
| `generate-rationale` | решение или вердикт и его вход | обоснование со ссылками на элементы входа | вход не содержит оснований решения | `G6` |
| `generate-abstract` | документ или его раздел | краткое изложение без новых утверждений | документ пуст | `G6` |

`generate-question` держится на `G2`, потому что вопрос сам по себе безвреден;
необратимой становится его **отправка** Заказчику — это ребро маршрута с
гейтом `G5`, а не операция.

### 2.4 `check` — проверка (8)

Выход — вердикт объявленной формы: значение, перечень нарушений, основание.
Вердикт «в целом приемлемо» контрактом запрещён.

| Операция | Вход | Единственный выход | Условие отказа | Ярус |
| --- | --- | --- | --- | --- |
| `check-atomicity` | утверждение | вердикт «атомарно / нет» с перечнем составных частей | вход не является утверждением | `G6` |
| `check-ambiguity` | утверждение | перечень неоднозначных мест с их видом (референциальная, количественная, модальная) | вход пуст | `G6` |
| `check-completeness` | набор элементов и объявленная модель полноты | перечень отсутствующих обязательных элементов | модель полноты не объявлена | `G6` |
| `check-consistency` | набор утверждений | перечень пар, противоречащих друг другу, с видом противоречия | в наборе менее двух утверждений | `G6` |
| `check-verifiability` | требование или критерий | вердикт с указанием способа проверки или причины его отсутствия | вход не является требованием | `G6` |
| `check-source-evidence` | утверждение и ссылка на источник | вердикт «цитата существует и разрешима» | ссылка отсутствует | `G6` |
| `check-vocabulary` | значение и закрытый словарь | вердикт принадлежности с ближайшими значениями при отказе | словарь не объявлен | `G3` |
| `check-schema` | документ или структура и схема | вердикт соответствия с перечнем нарушений полей | схема не объявлена | `G2` |

Предмет `check-atomicity`, `check-ambiguity`, `check-completeness`,
`check-consistency`, `check-verifiability` — характеристики качества требования
и набора по [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html).
Разделение на пять операций отражает то, что каждая проверяется своим способом
и падает по своей причине.

### 2.5 `assess` — оценка и выбор (5)

| Операция | Вход | Единственный выход | Условие отказа | Ярус |
| --- | --- | --- | --- | --- |
| `score-item` | элемент и объявленная шкала | значение по шкале с обоснованием | шкала не объявлена | `G1` |
| `rank-items` | перечень элементов с оценками | упорядоченный перечень с правилом порядка | оценки отсутствуют | `G1` |
| `match-coverage` | два набора элементов и правило соответствия | матрица покрытия с непокрытыми элементами обеих сторон | правило соответствия не объявлено | `G6` |
| `classify-severity` | нарушение или разрыв и шкала значимости | одно значение значимости с обоснованием | шкала не объявлена | `G1` |
| `select-option` | закрытое множество вариантов и критерий | один выбранный вариант с обоснованием и отвергнутыми | множество вариантов пусто | `G5` |

`match-coverage` отнесён к `assess`, а не к `check`: он не выносит вердикта
«соответствует», а строит соответствие, из которого вердикт выводится
отдельной операцией.

## 3. Сводка

| Класс | Количество | Ярус по умолчанию | Что делает класс невозможным при пропуске |
| --- | --- | --- | --- |
| `extract` | 6 | `G6` | требования перестают опираться на источник |
| `transform` | 7 | `G2` | элементы не собираются в документ и не связываются |
| `generate` | 5 | `G6` | не появляются требования, вопросы и критерии |
| `check` | 8 | `G6` | качество перестаёт быть проверяемым свойством |
| `assess` | 5 | `G1`–`G5` | не существует приоритета, покрытия и выбора |

## 4. Разложение навыков на операции

Каждый из 33 навыков
[таксономии процессов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/20-taxonomy.md)
разложен на операции этого каталога. Порядок в колонке значим: он и есть тело
подпроцесса.

| Навык | Процесс | Операции по порядку |
| --- | --- | --- |
| `SK-transcript-normalization` | `P-01` | `normalize-text` → `deduplicate-items` → `check-schema` |
| `SK-context-extraction` | `P-01` | `extract-entities` → `extract-actors` → `extract-statements` → `extract-constraints` → `extract-metrics` → `extract-source-reference` → `check-source-evidence` |
| `SK-ambiguity-detection` | `P-01` | `check-ambiguity` → `classify-severity` → `rank-items` |
| `SK-core-assembly` | `P-01` | `classify-item` → `map-to-slot` → `link-elements` → `check-schema` |
| `SK-question-formation` | `P-02` | `generate-question` → `deduplicate-items` → `check-schema` |
| `SK-question-prioritization` | `P-02` | `score-item` → `rank-items` → `generate-rationale` |
| `SK-answer-integration` | `P-02` | `extract-statements` → `map-to-slot` → `link-elements` → `check-consistency` |
| `SK-problem-statement` | `P-03` | `extract-statements` → `generate-statement` → `check-source-evidence` |
| `SK-value-hypothesis` | `P-03` | `extract-metrics` → `generate-statement` → `check-verifiability` |
| `SK-bcreq-decomposition` | `P-03` | `split-statement` → `classify-item` → `check-atomicity` |
| `SK-bcreq-assembly` | `P-03` | `map-to-slot` → `generate-abstract` → `check-schema` |
| `SK-fr-atomization` | `P-04` | `split-statement` → `check-atomicity` → `deduplicate-items` → `link-elements` |
| `SK-actor-role-identification` | `P-04` | `extract-actors` → `deduplicate-items` → `check-vocabulary` |
| `SK-acceptance-criteria` | `P-04` | `generate-acceptance-criterion` → `check-verifiability` → `check-atomicity` |
| `SK-fr-assembly` | `P-04` | `map-to-slot` → `link-elements` → `check-schema` |
| `SK-tz-structure-mapping` | `P-05` | `classify-item` → `map-to-slot` → `match-coverage` |
| `SK-nfr-specification` | `P-05` | `extract-constraints` → `extract-metrics` → `generate-statement` → `check-verifiability` |
| `SK-constraint-consolidation` | `P-05` | `deduplicate-items` → `check-consistency` → `classify-severity` |
| `SK-tz-assembly` | `P-05` | `map-to-slot` → `generate-abstract` → `check-completeness` → `check-schema` |
| `SK-scenario-extraction` | `P-06` | `extract-actors` → `extract-statements` → `classify-item` → `check-vocabulary` |
| `SK-flow-modeling` | `P-06` | `split-statement` → `link-elements` → `generate-statement` → `check-completeness` |
| `SK-diagram-projection` | `P-06` | `render-projection` → `check-schema` |
| `SK-quality-audit` | `P-07` | `check-atomicity` → `check-ambiguity` → `check-verifiability` → `check-consistency` → `check-completeness` → `classify-severity` |
| `SK-coverage-matching` | `P-07` | `link-elements` → `match-coverage` → `check-completeness` |
| `SK-defect-report` | `P-07` | `classify-severity` → `rank-items` → `generate-rationale` → `check-schema` |
| `SK-tender-requirement-extraction` | `P-08` | `extract-statements` → `extract-constraints` → `extract-source-reference` → `check-source-evidence` |
| `SK-gap-assessment` | `P-08` | `match-coverage` → `classify-item` → `classify-severity` |
| `SK-feasibility-verdict` | `P-08` | `score-item` → `select-option` → `generate-rationale` |
| `SK-change-localization` | `P-09` | `extract-statements` → `match-coverage` → `classify-item` |
| `SK-impact-propagation` | `P-09` | `link-elements` → `match-coverage` → `classify-severity` |
| `SK-state-transition` | `P-10` | `check-completeness` → `select-option` → `check-schema` |
| `SK-trace-materialization` | `P-10` | `link-elements` → `extract-source-reference` → `check-schema` |
| `SK-baseline-assembly` | `P-10` | `check-completeness` → `check-consistency` → `map-to-slot` → `check-schema` |

Все 31 операция вызываются хотя бы одним навыком, и ни один навык не ссылается
на значение вне каталога. Оба утверждения проверяются машинно —
[`validate-new-taxonomy.py`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/validate-new-taxonomy.py).

**Как читать строку.** Стрелка — порядок, а не ветвление: ветвление живёт на
уровне маршрута между навыками
([`ba-process-taxonomy/30-decision-framework.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/30-decision-framework.md), §3).
Отказ любой операции прерывает навык и уводит прогон по ребру отказа.

## 5. Реестр депрекации прежних тринадцати значений

Каждое прежнее значение проверено по отдельности (`DL-4`). «Класс работы»
означает, что значение остаётся полезным как **рубрика отчётности**, но
перестаёт быть операцией.

| Прежнее значение | Решение | Куда перешло |
| --- | --- | --- |
| `ingestion` | класс работы, не операция | `normalize-text`, `deduplicate-items` в `P-01` |
| `understanding` | **разделено** (`D4`: перечисляло извлечение и порождение) | `extract-*` (6 операций) + `generate-question` |
| `validation` | **разделено** (`D3`: три класса выхода) | `check-atomicity`, `check-ambiguity`, `check-completeness`, `check-consistency`, `check-verifiability`, `match-coverage` |
| `modeling` | **разделено** (`D3`: четыре класса выхода) | `extract-actors`, `split-statement`, `link-elements`, `render-projection` |
| `solution_design` | **выведено за границу** | проектирование решения не является работой БА в модели; относится к смежной роли |
| `documentation` | **разделено** (`D3`: шесть классов выхода) | `map-to-slot`, `generate-abstract`, `check-schema`; выбор класса документа задаётся процессом `P-03`, `P-04`, `P-05`, а не операцией |
| `quality` | **слито** с проверкой | класс `check`; отдельного значения не остаётся |
| `research` | депрекировано как операция | работа с внешними источниками выражается `extract-*` и `check-source-evidence` |
| `governance` | класс работы, не операция | `P-10` целиком; операции `select-option`, `check-completeness` |
| `impact_analysis` | класс работы, не операция | `P-09`; операции `match-coverage`, `link-elements`, `classify-severity` |
| `reverse_requirements` | депрекировано как операция | восстановление требований по готовой системе выражается теми же операциями, что и прямая работа: `extract-statements` → `split-statement` → `check-atomicity`; источником вместо расшифровки выступает система |
| `risk_analysis` | депрекировано как операция | риск — атрибут элемента; операции `score-item`, `classify-severity` |
| `release_readiness` | депрекировано как операция | `SK-baseline-assembly` в `P-10` |

`deprecated` означает: значение перестаёт быть допустимым для **новых**
артефактов; исторические артефакты не переписываются (`LG-1`,
[ADR-014](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-014-legacy-evidence-not-baseline.md)).

**Что видно из реестра.** Ни одно прежнее значение не удалено без замены, и ни
одно не перенесено целиком: четыре из тринадцати пришлось разделить, потому что
они объединяли разные типы когнитивной работы. Это и есть измеренный дефект
`D4`, выраженный как решение.

## 6. Границы

- Каталог покрывает работу с требованиями. Работа по планированию анализа
  (`BAPM`) операциями не разложена: в КК Манго она выполняется человеком и не
  оркеструется агентом.
- Восстановление требований по готовой системе (прежнее `reverse_requirements`)
  выражено операциями, но не выделено в отдельный процесс `L2`: в корпусе не
  нашлось прогона, где оно завершалось бы собственным целевым выходом. При
  появлении такого случая открывается `T-2`.
- Ярусы назначены по классу работы и правилу необратимости; эмпирической
  калибровки на прогонах ещё нет.
