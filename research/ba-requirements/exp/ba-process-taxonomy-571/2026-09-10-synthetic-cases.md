---
status: draft
version: 0.1
updated: 2026-09-10
temperature: 0.3
type: experiment
context: [ba, taxonomy, synthetic-cases, golden-reference, validation, issue-571]
method: synthetic-case-design + golden-reference
scope: mango-only
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571"
based_on:
  - projects/ba-gigacode-implementation/ba-process-taxonomy/20-taxonomy.md
  - projects/ba-gigacode-implementation/ba-operation-taxonomy/20-taxonomy.md
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571"
---

# Синтетические кейсы и эталоны для проверки новой таксономии

## Почему синтетика

Историческим прогоном новую таксономию проверить нельзя: 66 прогонов из 67
объявляют процесс вне словаря, а сам прежний словарь не разделяет ФТ и ТЗ
(`D7`, `D1` —
[факты](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-10-process-taxonomy-defects-facts.md)).
Синтез эталонных данных разрешён правилом 3 `<project_specific_rules>`
[`AGENTS.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/AGENTS.md)
в режиме `Creative` и хранится рядом с породившим артефактом.

Данные вымышлены. Предмет взят из публично известной функциональности
контакт-центра; имена, числа и цитаты сконструированы для эксперимента и не
воспроизводят материалы Заказчика.

Таблицы шагов машинно разбираемы: колонки `Шаг`, `Процесс`, `Навык`,
`Операции`, `Гейт` читаются
[`validate-new-taxonomy.py`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/validate-new-taxonomy.py).

## SC-1. Расшифровка созвона о маршрутизации обращений

**Вход.** Фрагмент расшифровки: «Заказчик (00:14:22): письма должны попадать
нужному оператору быстро, а то сейчас всё валится в общую очередь».

**Что кейс доказывает.** Ветвление по гейту есть исполнение маршрута, а не его
изменение; граница процесса — состояние артефакта, а не «черновик».

| Шаг | Процесс | Навык | Операции | Гейт |
| --- | --- | --- | --- | --- |
| 1 | `P-01` | `SK-transcript-normalization` | `normalize-text`, `deduplicate-items`, `check-schema` | `G2` |
| 2 | `P-01` | `SK-context-extraction` | `extract-entities`, `extract-actors`, `extract-statements`, `extract-constraints`, `extract-metrics`, `extract-source-reference`, `check-source-evidence` | `G6` |
| 3 | `P-01` | `SK-ambiguity-detection` | `check-ambiguity`, `classify-severity`, `rank-items` | `G6` |
| 4 | `P-02` | `SK-question-formation` | `generate-question`, `deduplicate-items`, `check-schema` | `G2` |
| 5 | `P-02` | `SK-question-prioritization` | `score-item`, `rank-items`, `generate-rationale` | `G1` |
| 6 | `P-02` | `SK-answer-integration` | `extract-statements`, `map-to-slot`, `link-elements`, `check-consistency` | `G5` |
| 7 | `P-01` | `SK-core-assembly` | `classify-item`, `map-to-slot`, `link-elements`, `check-schema` | `G2` |

**Эталон.**

- Шаг 2: одно утверждение о поведении; актор «оператор»; `extract-metrics`
  возвращает **отказ** — измеримых показателей во входе нет.
- Шаг 3: ровно две неоднозначности — референциальная («нужному») и
  количественная («быстро»), обе блокирующие.
- Шаг 4: ровно два вопроса, по одному на неоднозначность.
- Шаг 7: `A-CORE` переходит в `validated` только при пустом перечне
  неразрешённых неоднозначностей.
- Ребро маршрута 3 → 4 имеет условие «блокирующих неоднозначностей > 0»;
  ребро 6 → 7 — «все ответы получены».

**Чего не выражал прежний словарь.** Шаги 3 и 4 попадали в одно значение
`understanding` («извлекает ... ; формирует уточняющие вопросы»), поэтому
условие перехода между ними было невыразимо, а прогон объявлялся процессом
`fr-generation` «до черновика ФТ/ТЗ».

## SC-2. Обоснование изменения: лимит одновременных обращений

**Вход.** `A-CORE` в состоянии `validated` c утверждением «оператор берёт до
пяти диалогов одновременно и теряет контекст» и показателем «повторные
обращения — 18% за месяц».

**Что кейс доказывает.** `A-BCREQ` отвечает на «зачем» и «что», а не на «как»;
человеческий гейт требует ссылки на источник.

| Шаг | Процесс | Навык | Операции | Гейт |
| --- | --- | --- | --- | --- |
| 1 | `P-03` | `SK-problem-statement` | `extract-statements`, `generate-statement`, `check-source-evidence` | `G5` |
| 2 | `P-03` | `SK-value-hypothesis` | `extract-metrics`, `generate-statement`, `check-verifiability` | `G5` |
| 3 | `P-03` | `SK-bcreq-decomposition` | `split-statement`, `classify-item`, `check-atomicity` | `G5` |
| 4 | `P-03` | `SK-bcreq-assembly` | `map-to-slot`, `generate-abstract`, `check-schema` | `G2` |

**Эталон.**

- Шаг 1: формулировка проблемы содержит носителя, частоту и следствие; каждое
  утверждение снабжено сноской вида «источник, раздел, таймкод, цитата»
  (`HGC-1`).
- Шаг 2: гипотеза ценности измерима — «снизить долю повторных обращений с 18%
  до 10% за квартал».
- Шаг 3: три бизнес-требования верхнего уровня, ни одно не содержит способа
  реализации; утверждение «добавить очередь в Kafka» отвергается как ответ на
  вопрос «как».
- Шаг 4: `A-BCREQ` не содержит ни одного функционального требования.

**Чего не выражал прежний словарь.** `A-BCREQ` не был отделён от ФТ: процесс
`fr-generation` вёл «от сырого запроса до черновика ФТ/ТЗ», минуя обоснование
ценности, а операция `documentation` производила шесть разных классов
документов под одним именем.

## SC-3. Требования к автоответчику вне рабочего времени

**Вход.** `A-BCREQ` в состоянии `approved` с требованием «клиент должен
получать ответ вне рабочего времени».

**Что кейс доказывает.** ФТ и модель поведения — разные выходы разных
процессов; акторы берутся из `A-CORE`, а не изобретаются.

| Шаг | Процесс | Навык | Операции | Гейт |
| --- | --- | --- | --- | --- |
| 1 | `P-04` | `SK-actor-role-identification` | `extract-actors`, `deduplicate-items`, `check-vocabulary` | `G6` |
| 2 | `P-04` | `SK-fr-atomization` | `split-statement`, `check-atomicity`, `deduplicate-items`, `link-elements` | `G6` |
| 3 | `P-04` | `SK-acceptance-criteria` | `generate-acceptance-criterion`, `check-verifiability`, `check-atomicity` | `G6` |
| 4 | `P-04` | `SK-fr-assembly` | `map-to-slot`, `link-elements`, `check-schema` | `G2` |
| 5 | `P-06` | `SK-scenario-extraction` | `extract-actors`, `extract-statements`, `classify-item`, `check-vocabulary` | `G6` |
| 6 | `P-06` | `SK-flow-modeling` | `split-statement`, `link-elements`, `generate-statement`, `check-completeness` | `G6` |
| 7 | `P-06` | `SK-diagram-projection` | `render-projection`, `check-schema` | `G2` |

**Эталон.**

- Шаг 1: акторы — «Клиент», «Оператор», «Система». «Администратор» в перечень
  не попадает: во входе он не назван, и `extract-actors` обязан вернуть его
  отсутствие, а не догадку.
- Шаг 2: четыре атомарных требования; составное «принять обращение и отправить
  уведомление» разделено.
- Шаг 3: каждый критерий содержит наблюдаемое условие и ожидаемый результат.
- Шаг 7: диаграмма не содержит ни одного элемента, которого нет в модели шага
  6 (`render-projection` — преобразование, не порождение).

**Чего не выражал прежний словарь.** Значение `modeling` покрывало четыре
класса выхода (`use-case`, `user-story`, `uml-bpmn-diagram`,
`acceptance-criteria`), поэтому шаги 3 и 7 были неразличимы, а
`uml-bpmn-visualization` существовал отдельным процессом, хотя собственного
целевого выхода не имеет.

## SC-4. Сборка ТЗ по внешнему эталону структуры

**Вход.** `A-FR` в состоянии `validated` (12 требований) и ограничения из трёх
источников: интеграционные, регуляторные, эксплуатационные.

**Что кейс доказывает.** ТЗ — составной документ, собираемый из уже
проверенных ФТ; `A-FR` и `A-TZ` не совпадают.

| Шаг | Процесс | Навык | Операции | Гейт |
| --- | --- | --- | --- | --- |
| 1 | `P-05` | `SK-tz-structure-mapping` | `classify-item`, `map-to-slot`, `match-coverage` | `G2` |
| 2 | `P-05` | `SK-nfr-specification` | `extract-constraints`, `extract-metrics`, `generate-statement`, `check-verifiability` | `G6` |
| 3 | `P-05` | `SK-constraint-consolidation` | `deduplicate-items`, `check-consistency`, `classify-severity` | `G6` |
| 4 | `P-05` | `SK-tz-assembly` | `map-to-slot`, `generate-abstract`, `check-completeness`, `check-schema` | `G5` |
| 5 | `P-10` | `SK-trace-materialization` | `link-elements`, `extract-source-reference`, `check-schema` | `G2` |
| 6 | `P-10` | `SK-baseline-assembly` | `check-completeness`, `check-consistency`, `map-to-slot`, `check-schema` | `G5` |

**Эталон.**

- Шаг 1: все 12 требований размечены по разделам эталона структуры;
  `match-coverage` показывает пустой перечень требований без раздела.
- Шаг 3: обнаружено одно противоречие — «хранить записи 3 года» против «удалять
  персональные данные через 6 месяцев»; значимость блокирующая.
- Шаг 4: `A-TZ` собран **только** из требований в состоянии `validated`; новое
  требование, не проходившее `P-04`, в ТЗ не попадает.
- Шаг 5: каждое требование `A-TZ` имеет путь до цитаты источника.
- Шаг 6: базис фиксируется при пустом перечне блокирующих противоречий.

**Чего не выражал прежний словарь.** Имя выхода «ФТ/ТЗ» встречается в корпусе
29 раз, притом что онтология спицы объявляет `feature-spec-kk` и `tz-contract`
разными типами. Шаг 4 в прежней модели совпадал с шагом 4 кейса `SC-3`.

## SC-5. Аудит готового документа функциональных требований

**Вход.** Документ с требованием «Система должна корректно обрабатывать
входящие обращения и уведомлять оператора» и ещё 9 требованиями.

**Что кейс доказывает.** Верификация — процесс с собственным выходом, а не
проверка внутри написания.

| Шаг | Процесс | Навык | Операции | Гейт |
| --- | --- | --- | --- | --- |
| 1 | `P-07` | `SK-quality-audit` | `check-atomicity`, `check-ambiguity`, `check-verifiability`, `check-consistency`, `check-completeness`, `classify-severity` | `G6` |
| 2 | `P-07` | `SK-coverage-matching` | `link-elements`, `match-coverage`, `check-completeness` | `G6` |
| 3 | `P-07` | `SK-defect-report` | `classify-severity`, `rank-items`, `generate-rationale`, `check-schema` | `G2` |

**Эталон.**

- Шаг 1 по приведённому требованию: не атомарно (два поведения), неоднозначно
  («корректно»), непроверяемо, полнота нарушена (нет поведения при отказе
  канала), противоречий нет. Пять вердиктов, пять причин.
- Шаг 2: два элемента `A-BCREQ` не покрыты ни одним требованием.
- Шаг 3: `A-REP` содержит перечень дефектов с значимостью и обоснованием; сам
  документ требований при этом не изменяется.

**Чего не выражал прежний словарь.** Значение `validation` давало один вердикт
на три класса выхода (`acceptance-criteria`, `coverage-matrix`,
`defect-report`), из которого не выводится ни одно действие.

## SC-6. Оценка внешнего тендерного ТЗ

**Вход.** Внешний документ на 40 страниц с 60 требованиями к контакт-центру.

**Что кейс доказывает.** Оценка чужого документа не производит требований и
завершается суждением; `A-REP` — производный аналитический артефакт.

| Шаг | Процесс | Навык | Операции | Гейт |
| --- | --- | --- | --- | --- |
| 1 | `P-08` | `SK-tender-requirement-extraction` | `extract-statements`, `extract-constraints`, `extract-source-reference`, `check-source-evidence` | `G6` |
| 2 | `P-08` | `SK-gap-assessment` | `match-coverage`, `classify-item`, `classify-severity` | `G6` |
| 3 | `P-08` | `SK-feasibility-verdict` | `score-item`, `select-option`, `generate-rationale` | `G5` |

**Эталон.**

- Шаг 1: каждое извлечённое требование имеет ссылку «раздел, страница,
  цитата»; требование без цитаты не попадает в перечень.
- Шаг 2: 60 требований разнесены на «покрыто», «покрыто частично», «разрыв»;
  для каждого разрыва назначена значимость.
- Шаг 3: выбран один вариант из закрытого множества «участвуем / участвуем с
  оговорками / не участвуем», отвергнутые варианты перечислены с основанием.
- Ни один шаг не создаёт требований к системе Манго: выход процесса — `A-REP`.

**Чего не выражал прежний словарь.** Процесс `tender-analysis` существовал, но
его выходом объявлялись «ФТ/ТЗ», то есть оценка чужого документа неотличима от
написания собственных требований.

## SC-7. Изменение к зафиксированным требованиям

**Вход.** Заявка «увеличить срок хранения записей разговоров с 3 до 5 лет» и
`A-TRACE` зафиксированного базиса из `SC-4`.

**Что кейс доказывает.** Влияние вычисляется по рёбрам следа, а не экспертной
оценкой; `A-TRACE` — обязательный вход, а не журнал.

| Шаг | Процесс | Навык | Операции | Гейт |
| --- | --- | --- | --- | --- |
| 1 | `P-09` | `SK-change-localization` | `extract-statements`, `match-coverage`, `classify-item` | `G6` |
| 2 | `P-09` | `SK-impact-propagation` | `link-elements`, `match-coverage`, `classify-severity` | `G6` |
| 3 | `P-10` | `SK-state-transition` | `check-completeness`, `select-option`, `check-schema` | `G3` |

**Эталон.**

- Шаг 1: заявка локализована в двух требованиях и одном ограничении.
- Шаг 2: транзитивное замыкание даёт 5 затронутых элементов, включая критерий
  приёмки и раздел `A-TZ`; ранее выявленное противоречие с удалением
  персональных данных воспроизводится и помечается блокирующим.
- Шаг 3: затронутые артефакты переводятся из `baselined` в
  `needs-clarification`; переход имеет основание и проверяется схемой.

**Чего не выражал прежний словарь.** `impact-analysis` существовал как процесс,
но `A-TRACE` не был его обязательным входом, поэтому оценка влияния опиралась
на память исполнителя и не была воспроизводима.

## Сводка покрытия

| Показатель | Значение |
| --- | --- |
| Кейсов | 7 |
| Процессов `L2` покрыто | 10 из 10 |
| Навыков `L3` покрыто | 33 из 33 |
| Операций каталога покрыто | 31 из 31 |
| Шагов с эталоном результата | все |

Покрытие проверяется машинно, а не заявляется:
`python3 validate-new-taxonomy.py --hub ../../../..`.
