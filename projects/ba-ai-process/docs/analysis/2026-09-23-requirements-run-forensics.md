---
status: accepted
version: 0.2
updated: 2026-09-24
temperature: 0.1
type: analysis
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/605"
scope: mango-only
based_on: "https://github.com/G-Ivan-A/mango_ba_prompts/tree/8cbf82aa73129ec5747af07f790aaf438b0fb6e9/runs"
related_artifacts:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-bcreq-golden-forms-and-feasibility.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/20-taxonomy.md"
---

# Форензика прогонов требований и строгий семантический контракт

## Результат

Корпус подтверждает не единичную ошибку формулировки, а четыре независимых
класса отказа: неподтверждённый факт повышается до требования; текущее
поведение, решение, UI или ограничение ошибочно становятся функциональным
требованием; состояние согласованного текста теряется между итерациями;
отраслевая классификация заявляется без версионированного каталога и точного
идентификатора. Лечение только prompt-ом эти отказы не закрывает. Нужен
исполняемый контракт с раздельными инвариантами для FR, UC и NFR, реестром
источников, матрицей `as-is → delta`, продуктовой привязкой и тремя гейтами:
детерминированным, семантическим и человеческим.

Предлагаемые ниже правила усиливают, но не заменяют действующий
[RFC уровня абстракции и продуктовой маршрутизации](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md).
Инварианты приняты как основание для Source-контрактов в
[issue #609](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/609),
но сами по себе не являются разрешением менять runtime-пакет. Предложенный
issue путь `docs/contracts/` не использован: он
запрещён каноническим `AGENTS.md`; Analysis размещён в контуре инициативы.

## Контекст и охват

Снимок на 2026-09-23 включает все 67 каталогов `RUN-0001`…`RUN-0067` legacy-
репозитория на commit
[`8cbf82a`](https://github.com/G-Ivan-A/mango_ba_prompts/tree/8cbf82aa73129ec5747af07f790aaf438b0fb6e9/runs),
27 доступных внешних JSON-экспортов, на которые ссылаются metadata прогонов, и
три вложения issue #605. Два JSON-вложения содержат диалоги BCREQ-1104 и
BCREQ-1106; текстовое вложение использовано только как контекст постановки.
Вложения читались во временной рабочей области и в репозиторий не переносились.

Единица анализа — наблюдаемое утверждение или преобразование артефакта, а не
предполагаемая причина поведения модели. Поэтому здесь нет психологических
объяснений: фиксируются вход, выход, нарушенный инвариант и проверяемое правило.
Статистика конкретного прогона не экстраполируется на всю популяцию без
доказательства. Для повторяемой инвентаризации добавлен read-only скрипт
[`issue_605_run_inventory.py`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/issue-605-67068bc98bc2/projects/ba-ai-process/experiments/issue_605_run_inventory.py).

### Полнота evidence

| Срез | Количество | Как использован |
| --- | ---: | --- |
| Все каталоги runs | 67 | Metadata, outputs, logs и feedback проверены для каждого каталога. |
| Полный диалог в каталоге run | 17 | Семантический разбор реплик и итогов. |
| Полный диалог по внешней ссылке metadata | 27 | Экспорт получен во временную область и разобран; в Git не добавлен. |
| Run без полного диалога | 23 | Анализ ограничен зафиксированными outputs/logs; включён в gap list. |
| Диалоги issue #605 | 2 | Отдельные кейсы BCREQ-1104 и BCREQ-1106. |
| Контекстное текстовое вложение | 1 | Уточнение цели; не доказательство продуктовых фактов. |

`RUN-0030`…`RUN-0055` не являются пробелом: их полные экспорты отсутствуют в
Git-дереве, но доступны по ссылкам в `metadata.yaml`. `RUN-0061` также содержит
доступную ссылку на экспорт и потому включён в разобранную выборку.

### Проверенные альтернативные гипотезы

1. **Ошибка только в одной формуле FR.** Опровергнуто: RUN-0016, RUN-0020,
   RUN-0026, RUN-0063 и оба вложенных диалога показывают разные независимые
   отказы — grounding, scope, state и classification.
2. **Citation автоматически означает релевантность.** Опровергнуто: в
   RUN-0024 и RUN-0026 ссылки не поддерживали вывод либо страницы не были
   прочитаны; в BCREQ-1104 тематически похожие факты о записи разговора были
   нерелевантны звуковому уведомлению.
3. **Атомарность требует отдельного FR на каждое поле и состояние.**
   Опровергнуто RUN-0063→RUN-0067: пять описаний текущей функциональности
   удалены, а требуемая дельта сведена к двум способностям с критериями.
4. **TM Forum даёт готовый стандарт написания каждой строки FR/UC/NFR.** Не
   подтверждено. TM Forum описывает capabilities, процессы и ODA-контекст;
   требования как текст и их качество непосредственно нормирует
   [ISO/IEC/IEEE 29148:2018](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec-ieee%3A29148%3Aed-2%3Av1%3Aen),
   а типы FR/NFR — официальный
   [IREB CPRE Glossary](https://cpre.ireb.org/en/downloads-and-resources/glossary).

## Находки: дефекты, лечение и обязательные правила

Каждая строка имеет требуемую debug-форму: категория, факт, негативное
ограничение и стандартное правило. `Запрет` — что исполнитель не вправе делать;
`Правило` — что будущий контракт обязан проверять.

| ID / категория | Наблюдаемый факт | Запрет | Стандартное правило |
| --- | --- | --- | --- |
| `EVID-01` grounding | RUN-0026 заявил проверку документации при `extract_page_success=[0,0,0]`; точная UI-метка дошла до итога без проверенного изображения. | Нельзя писать «проверено», цитировать страницу или точную метку, если источник фактически не открыт. | Каждое продуктовое утверждение содержит `source_ref`, точный anchor и `retrieval_status=read`; иначе только `hypothesis` или `open_question`. |
| `EVID-02` citation | RUN-0024 дал три сноски, которые не содержали приписанные им факты; одно утверждение дошло до бизнес-текста. | Нельзя считать наличие URL доказательством entailment. | Гейт проверяет пару `claim ↔ excerpt`, а затем отдельно `claim ↔ goal/boundary`; обе связи обязательны. |
| `EVID-03` attachment | RUN-0016 ссылался на временные CDN-вложения, которых не было в зафиксированном run. | Нельзя принимать невоспроизводимый attachment за проверяемую SSOT. | Evidence получает checksum или стабильную версионированную ссылку; иначе в результате фиксируется gap. |
| `REL-01` relevance | BCREQ-1104 подтянул факты про speech analytics, TTS и удаление записей для требования проигрывания сигнала. | Нельзя включать факт только из-за совпадения слов «запись», «звук» или продукта верхнего уровня. | Для каждого факта обязательны `goal_refs`, `system_boundary`, `product_binding`, `relevance_reason`; keyword match недостаточен. |
| `SCOPE-01` as-is/delta | В RUN-0063 пять из шести FR описывали существующие фильтры, колонки или экспорт; RUN-0067 удалил их. | Нельзя превращать текущее состояние или предусловие в требование к доработке. | До FR создаётся матрица `evidence → as_is → requested_delta → disposition`; в FR допускается только подтверждённая delta. |
| `SCOPE-02` invented scope | RUN-0016 добавил режим инкогнито, активную вкладку и пакет интеграции; RUN-0064 нашёл выдуманный XLSX и изменение ролевой модели. | Нельзя добавлять роль, технологию, формат, лимит или entitlement без источника потребности. | Неподтверждённый вариант живёт в `solution_option`/`open_question`, не в FR/NFR. |
| `FR-01` wrong level | BCREQ-1104/1106 и ряд chat exports разложили поля, кнопки, настройки и варианты на самостоятельные FR. | Нельзя считать UI control, поле, значение, шаг сценария, API-метод или критерий отдельной способностью системы. | FR отвечает только «какой результат/поведение предоставляет целевая система» и покрывается L2–L4 деталями. |
| `FR-02` wrong subject | RUN-0026 механически применил «дать Пользователю возможность» к автоматическим действиям, потеряв субъекта и тестируемость. | Нельзя подменять автоматическое поведение возможностью пользователя. | Subject определяется событием: `Система должна <наблюдаемое действие/результат>`; actor используется только для инициируемой actor-ом возможности. |
| `FR-03` duplication | RUN-0016 не обнаружил дубли 4.3.2/4.4.1 и 4.5.1/6.1.1. | Нельзя оставлять два ID с одним обязательством или одно обязательство одновременно как FR и constraint. | Semantic gate строит нормализованный граф субъект→действие→объект→условие и требует merge/link решения для дублей. |
| `UC-01` mixed artifact | В диалогах сценарий, исключение и UI-решение регулярно публиковались как FR; в BCREQ-1106 не сохранялось покрытие variants. | Нельзя выдавать последовательность взаимодействий или ветку ошибки за отдельный FR. | UC содержит actor, trigger, preconditions, main flow, alternatives/exceptions, outcome и ссылки на FR/NFR/constraints. |
| `NFR-01` invented metric | RUN-0015 предложил 5 минут, 100 ms, 2 секунды и 24/7; все числа были отклонены человеком. | Нельзя генерировать числовой target из практики, ожидания модели или слова «быстро». | NFR принимается только с quality attribute, объектом, condition, measure, target и provenance; неизвестное значение — TBD/open question. |
| `NFR-02` misclassification | BCREQ-1104 превратил обязательное проигрывание сигнала в «100%» NFR, хотя это functional outcome. | Нельзя делать NFR из функционального поведения посредством добавления процента. | Сначала классифицируется проверяемый outcome. NFR существует только для качества/constraint поверх функции; target не создаёт новый тип. |
| `STATE-01` baseline drift | RUN-0028 потерял верхний уровень 4.1–4.4 и удалил 4.4.3; RUN-0016 вернул снятые разделы в summary. | Нельзя молча удалять, переименовывать или возвращать согласованный элемент. | Каждая итерация применяет explicit change set к baseline; гейт проверяет ID continuity, accepted/rejected decisions и unexplained diff. |
| `STATE-02` user correction | BCREQ-1104 несколько раз исправлял ложный продуктовый факт; модель позже снова опиралась на прежнюю версию. | Нельзя использовать superseded claim после явной коррекции человека. | Decision log помечает claim `accepted/rejected/superseded`; retrieval и generation исключают rejected/superseded. |
| `FORMAT-01` instruction | RUN-0029 дважды вернул заголовки и комментарии после требования «только список вопросов». | Нельзя менять запрошенную форму без конфликта с обязательным контрактом. | Rendering gate проверяет формат отдельно от семантики; отклонение требует явной причины. |
| `TMF-01` false authority | BCREQ-1104 выдал общие ODA/eTOM-направления как точное TM Forum mapping без catalog ID и версии. | Нельзя называть свободный текст точным TM Forum соответствием. | Binding валиден только по доступному versioned snapshot с точными ID; иначе `unresolved`, а не guessed label. |

## Положительные случаи и извлечённые правила

| Evidence | Что сработало | Переиспользуемое правило |
| --- | --- | --- |
| RUN-0016 | Непроверяемое требование было удалено; поведение сформулировано через результат настроек, не их значения. | Деталь без evidence удаляется или становится вопросом; настройка раскрывает FR, но не порождает его. |
| RUN-0025 | Найдены дубли разделов, этапы работ под видом правил и конфликт термина; решение человека сохранено. | Review обязан проверять тип артефакта и decision authority, а не только грамматику. |
| RUN-0026 | Scope expansion и реальный дубль были обнаружены; модель предложила варианты и дала человеку выбрать. | При нескольких допустимых решениях публикуются варианты и trade-offs, не фиктивный единственный ответ. |
| RUN-0027 | Три числовых ограничения подтверждены реально полученными источниками; частичная подтверждённость помечена явно. | Число допускается только с anchor и статусом доказательства; partial не повышается до fact. |
| RUN-0029 | После коррекции режим изменён с предложения решения на выявление потребности. | Режим работы — часть baseline и меняется явным decision event. |
| RUN-0055 | 40 из 50 продуктовых утверждений подтверждены, 10 исправлены по документации. | Claim-level verification должен предшествовать feasibility verdict. |
| RUN-0056→RUN-0058 | Первичный gap из-за недоступности API был пересмотрен после обнаружения источника. | Вердикт хранит состояние evidence и обязан быть пересчитан при появлении SSOT. |
| RUN-0059 | Неизвестные Mango endpoints и JSON не были придуманы; пробел оставлен архитектурным gap. | Fail-closed полезнее правдоподобной схемы без источника. |
| RUN-0060 | 101 требование получили воспроизводимые source anchors; шесть расхождений исправлены, один verdict понижен. | Reproducible index и повторная проверка должны уметь ухудшать прежний ответ. |
| RUN-0063→RUN-0067 | Пять as-is псевдо-FR удалены; дельта сведена к двум FR, 14 AC и девяти вопросам. | Малое число capability FR + полное покрытие деталями лучше списка текущих UI-фактов. |
| BCREQ-1104 | После фактических поправок сформировались четыре чистых обязательства без лишней технической детализации. | Human correction должна становиться regression example, а не одноразовой правкой текста. |
| BCREQ-1106 | Разделение вариантов ожидаемого решения от финального выбора сохранило свободу продуктового решения. | До решения владельца варианты находятся в solution layer, не маскируются под FR. |

## Строгие определения и инварианты

Определения совместимы с
[ISO/IEC/IEEE 29148:2018](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec-ieee%3A29148%3Aed-2%3Av1%3Aen)
и [IREB CPRE Glossary](https://cpre.ireb.org/en/downloads-and-resources/glossary),
но адаптированы к BCREQ-проекции проекта.

### Functional Requirement

**Определение.** FR — одно необходимое, наблюдаемое поведение или результат,
который целевая система должна предоставить для подтверждённой потребности в
заданной границе. FR описывает `что`, а не экран, control, последовательность
шагов или выбранный механизм реализации.

`FR-INV-01` — у FR ровно один `requirement_id`, один system subject и одна
независимо проверяемая capability; составное обязательство декомпозируется.

`FR-INV-02` — FR имеет `goal_refs`, `task_refs`, `source_refs`,
`product_binding`, `delta_ref` и минимум один `scenario_ref`.

`FR-INV-03` — текст выражает обязательность (`shall` / «должна») и наблюдаемый
outcome. Слова `кнопка`, `поле`, `вкладка`, `endpoint`, формат payload и
конкретная технология в FR являются warning, пока semantic gate не докажет,
что это само запрошенное внешнее поведение.

`FR-INV-04` — as-is, project task, rationale, constraint, NFR, acceptance
criterion и solution option не могут иметь тип FR.

Минимальная форма:

```yaml
requirement_id: FR-001
system_subject: target-system
shall: "provide <observable behavior or result>"
goal_refs: [GOAL-01]
task_refs: [TASK-01]
source_refs: [SRC-01]
delta_ref: DELTA-01
product_binding_refs: [PB-01]
scenario_refs: [UC-001]
acceptance_refs: [AC-001]
```

### Use Case

**Определение.** UC — ограниченный целью сценарий взаимодействия actor-а с
целевой системой, который начинается trigger-ом, проходит основной и
альтернативные/исключительные потоки и заканчивается наблюдаемым outcome. UC
демонстрирует реализацию одного или нескольких требований; сам по себе он не
создаёт новую capability.

`UC-INV-01` — UC содержит actor, goal, trigger, preconditions, numbered main
flow, alternatives/exceptions и postcondition/outcome.

`UC-INV-02` — каждый UC ссылается минимум на FR, NFR или constraint; каждый FR
имеет хотя бы один UC. Связь many-to-many допустима и проверяется в обе стороны.

`UC-INV-03` — UI control может быть шагом UC; failure branch — alternative или
exception. Ни один из них не становится FR без отдельной подтверждённой
capability.

Минимальная форма:

```yaml
scenario_id: UC-001
actor: ACTOR-01
goal_ref: GOAL-01
trigger: "..."
preconditions: [PRE-01]
main_flow: [STEP-01, STEP-02]
alternatives: [ALT-01]
exceptions: [EXC-01]
outcome: "..."
requirement_refs: [FR-001]
nfr_refs: [NFR-001]
constraint_refs: []
```

### Non-functional Requirement

**Определение.** NFR — измеримое требование к качеству функции/системы либо
явное ограничение, которое не задаёт новое функциональное поведение. Внутри
BCREQ качество и constraint могут храниться раздельными subtype, сохраняя
IREB-совместимую общую категорию non-functional.

`NFR-INV-01` — quality NFR содержит `quality_attribute`, объект измерения,
condition, measure, target, verification method и source; constraint содержит
тип ограничения, предмет, правило и source.

`NFR-INV-02` — target запрещено синтезировать. Если stakeholder или SSOT не
задаёт значение, создаётся `TBD` с owner и вопросом, но не требование с
«типовым» числом.

`NFR-INV-03` — процент не переклассифицирует функциональный outcome в NFR.
Например, «система проигрывает сигнал» — FR; доля успешных проигрываний при
указанных условиях может быть reliability NFR только при доказанном target.

Минимальная форма:

```yaml
requirement_id: NFR-001
subtype: quality
quality_attribute: reliability
applies_to_refs: [FR-001]
condition: "..."
measure: "successful outcomes / eligible events"
target: TBD
target_source_ref: OPEN-01
verification: "..."
source_refs: [SRC-01]
```

## TM Forum: строгая привязка без ложной точности

[TM Forum Capability Framework](https://www.tmforum.org/open-digital-architecture/capability-framework/)
описывает способности организации для достижения outcome, а
[Business Architecture Overview](https://www.tmforum.org/open-digital-architecture/business-architecture-framework/)
определяет eTOM как иерархическую классификацию process building blocks. Это
полезные оси traceability, но не взаимозаменяемые ID и не шаблон строки FR.

`TMF-INV-01` — точная привязка существует только как tuple
`framework + document/version + element_id + element_name + source_anchor`.

`TMF-INV-02` — capability, eTOM process, ODA component и Open API — разные
типы элементов. Их ID запрещено записывать в одно универсальное поле.

`TMF-INV-03` — локальный `PC-*`/`PF-*` ID является MANGO taxonomy ID, а не TM
Forum ID. Текущее поле `industry_correspondence.tm_forum` содержит prose и не
доказывает точного соответствия.

`TMF-INV-04` — если лицензированный/доступный версионированный snapshot не
загружен в утверждённый реестр, результат `unresolved`; модель не угадывает ID
по названию и не публикует similarity как факт.

`TMF-INV-05` — [Information Framework (SID)](https://www.tmforum.org/open-digital-architecture/information-framework-sid/)
является информационной моделью TM Forum. Его домены и сущности дают отдельный
контекст для эскалации, но не заменяют ID capability, процесса или компонента.
Каждая ось хранит собственные status, тип элемента, версию и anchor. Публичное
описание домена без точного ID даёт кандидата, а не `resolved` binding.

```yaml
industry_bindings:
  tm_forum:
    status: unresolved
    element_type: capability
    snapshot_ref: null
    element_id: null
    element_name: null
    source_anchor: null
  sid_context:
    status: unresolved
    element_type: null
    snapshot_ref: null
    element_id: null
    element_name: null
    source_anchor: null
  local_product_binding_refs: [PB-01]
  rationale: "why this element supports the requirement"
  reviewed_by: null
```

ID и membership проверяются в реестре соответствующего типа элемента; для
eTOM и ODA нельзя переиспользовать поле capability. На дату анализа доступной
в репозитории таблицы точных TM Forum IDs нет. Поэтому массовая автоматическая
разметка текущего корпуса была бы фабрикацией, а не выполнением задачи.

## Контракт исполнения и проверки

### Pre-decomposition

До декомпозиции FR/UC/NFR внутри Working исполнитель обязан создать:

1. реестр evidence с состоянием retrieval и точными anchors;
2. goal/task/system-boundary register;
3. `as-is → requested delta` matrix;
4. локальную product binding;
5. claim register с `accepted/rejected/hypothesis/open`;
6. только затем — FR, UC, NFR и solution details.

Ни один пустой слот не заполняется правдоподобным значением. Пустота получает
reason, owner и open question.

### Три гейта

| Gate | Обязательные проверки | Не имеет права решать |
| --- | --- | --- |
| `G-mach` | Schema, уникальность ID, typed references, source existence, exact taxonomy membership, FR↔UC coverage, baseline diff, отсутствие unresolved TMF ID в resolved binding. | Релевантность смысла и достаточность требования. |
| `G-semantic` | Claim↔source entailment, goal relevance, as-is/delta, тип FR/UC/NFR, уровень абстракции, дубли, неполнота flows. Сохраняет rationale и counterexample. | Объявлять своё решение детерминированной гарантией или принимать спорный mapping. |
| `G-human` | Конфликтующие факты, scope/solution decision, новый Golden case, disputed classification и точная TM Forum привязка. | Молча принимать необъяснённый diff или неподтверждённый факт. |

### Регрессионные пары

Минимальный Golden Set должен хранить пары, а не только «хороший финал»:

- RUN-0063 invalid → RUN-0067 corrected;
- RUN-0026 automatic-action pseudo-FR → system-behavior FR;
- RUN-0015 invented numeric NFR → TBD/open question;
- BCREQ-1104 keyword-relevant product fact → rejected by goal relevance;
- BCREQ-1106 UI/variant pseudo-FR → UC/solution detail;
- unresolved TM Forum prose → fail-closed typed binding.

Каждая пара содержит input, wrong output, violated invariant, corrected output
и regression assertion. Только финальный хороший текст не учит гейт ловить
конкретную ошибку.

## Недоступные полные диалоги

Ниже перечислены все 23 run, для которых в проверенном snapshot нет локального
транскрипта и metadata не указывает JSON chat export. Для записей без
подтверждённого BCREQ-номера используется `BCREQ-UNKNOWN`; номер не выводится
из GitHub issue или названия процесса. Это не означает, что output run
непригоден: он учтён как вторичное evidence, но подробный семантический разбор
реплик невозможен.

- `[BCREQ-UNKNOWN / RUN-0001]` prompt experiment
- `[BCREQ-UNKNOWN / RUN-0002]` user-story generation
- `[BCREQ-UNKNOWN / RUN-0003]` use-case generation
- `[BCREQ-UNKNOWN / RUN-0004]` prompt audit
- `[BCREQ-UNKNOWN / RUN-0005]` prompt self-test
- `[BCREQ-UNKNOWN / RUN-0006]` session debug documentation
- `[BCREQ-UNKNOWN / RUN-0007]` FR generation
- `[BCREQ-UNKNOWN / RUN-0008]` KB citation check
- `[BCREQ-UNKNOWN / RUN-0009]` industry-standards A/B check
- `[BCREQ-1025 / RUN-0010]` email routing
- `[BCREQ-UNKNOWN / RUN-0011]` multichannel agent workload
- `[BCREQ-1069 / RUN-0012]` restricted API key
- `[BCREQ-765 / RUN-0056]` HH.ru chats feasibility
- `[BCREQ-UNKNOWN / RUN-0057]` tender STT/TTS/NLU/dialogue manager
- `[BCREQ-765 / RUN-0058]` HH.ru Chats API re-evaluation
- `[BCREQ-765 / RUN-0059]` HH.ru↔Mango architecture spike
- `[BCREQ-765 / RUN-0060]` combined HH.ru L4 report
- `[BCREQ-UNKNOWN / RUN-0062]` tender appendices 5–7
- `[BCREQ-1074 / RUN-0063]` communication expenses report
- `[BCREQ-1074 / RUN-0064]` error analysis and report-view specification
- `[BCREQ-1099 / RUN-0065]` telephony feasibility, model A
- `[BCREQ-1099 / RUN-0066]` telephony feasibility, model B
- `[BCREQ-1074 / RUN-0067]` detailed export rework

## Рекомендации

1. Уточнённые инварианты приняты в существующем RFC как typed contracts.
   Runtime компилируется отдельной задачей с проверяемыми fixtures.
2. В следующей реализационной задаче сначала добавить schemas и `G-mach`, затем
   semantic regression set; prompt менять после появления измеримого gate.
3. Версионированный реестр точных ID заполнять только из доступного
   авторитетного snapshot. До него `tm_forum.status=unresolved` корректен;
   отдельно сохранять подтверждённый SID-контекст или кандидата с anchor.
4. Владелец в [issue #609](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/609)
   признал доступную выборку достаточной для этих инвариантов. Список 23 run
   остаётся границей evidence; получение новых чатов — триггер повторного
   анализа, а не условие принятия текущего Source-дизайна.
5. Анализ не повышается до стандарта или ADR: issue не даёт полномочий менять
   `standards/` или `docs/adr/`; runtime имеет отдельный цикл приёмки.

## Связанные артефакты

- [Issue #605](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/605)
- [Legacy runs snapshot](https://github.com/G-Ivan-A/mango_ba_prompts/tree/8cbf82aa73129ec5747af07f790aaf438b0fb6e9/runs)
- [Анализ эталонных форм BCREQ](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-bcreq-golden-forms-and-feasibility.md)
- [RFC уровня абстракции и маршрутизации](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md)
- [Мета-модель: taxonomy](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/20-taxonomy.md)
- [TM Forum Capability Framework](https://www.tmforum.org/open-digital-architecture/capability-framework/)
- [TM Forum Business Architecture](https://www.tmforum.org/open-digital-architecture/business-architecture-framework/)
- [ISO/IEC/IEEE 29148:2018](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec-ieee%3A29148%3Aed-2%3Av1%3Aen)
- [IREB CPRE Glossary](https://cpre.ireb.org/en/downloads-and-resources/glossary)
