---
status: draft
version: 0.1
updated: 2026-08-11
temperature: 0.1
analysis-subtype: recommendation
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/495"
scope: repo
based_on: "PR #491 + PR #492 + ADR-010 + RFC #470 + active governance contracts"
related_artifacts:
  - "docs/adr/2026-08-adr-010-agent-autonomy-principles.md"
  - "docs/rfc/2026-08-06-rfc-task-statement-architecture.md"
  - "ai-governance/ai-governance.md"
  - "ai-rules/agent-work-rules.md"
  - "docs/adr/2026-06-adr-002-artifact-document-methodology.md"
  - "docs/adr/2026-07-adr-008-standard-meta-structure.md"
  - "standards/adr-structure-standard.md"
---

# Неоднозначность контрактов при последовательных задачах внедрения

## Summary / BLUF

Конфликт PR [#491](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/491)
и [#492](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/492) — не
единичная ошибка выбора между удалением и redirect. Это **пробел композиции
норм**: контракты отдельно регулируют автономию агента, human-only границы,
уровень governance-изменения, ссылки, статусы и верификацию, но не задают
целостную семантику изменения уже существующего артефакта во времени. Поэтому
оба агента смогли локально обосновать взаимоисключающие действия над одним
путём.

Пробел составной. Нет одновременно: объекта, охватываемого запретом на удаление
human work; различия между historical record и active dependency; семантики
переходов `active → deprecated → superseded → absent`; правил сохранения
идентичности пути и входящих ссылок; приоритета между исторической целостностью
и текущей link validation; precondition проверки решений недавно завершённых
задач. Существующие правила обнаруживают конфликт только после выбора действия,
а не сужают выбор заранее.

Следовательно, будущая нормативная работа должна начинаться не с выбора
конкретного механизма. Сначала требуется закрыть вопросы идентичности,
историчности, допустимых переходов, обратимости, ссылочной совместимости,
приоритета норм и межзадачной преемственности. Этот Analysis фиксирует вопросы,
но не принимает стандарт, правило или способ проверки.

## Context / Scope

Анализ интерпретирует состояние репозитория на 2026-08-11 и выполняет issue
[#495](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/495). Основные
evidence:

- PR #491 сохранил `.github/ISSUE_TEMPLATE/task-creative.md` как скрытый
  deprecated compatibility redirect, чтобы не менять ссылки в ADR-010 и RFC
  #470; отклонение было явно записано в PR;
- PR #492 первоначально удалил тот же файл, а активные Markdown-ссылки в
  ADR-010 и RFC #470 превратил в code spans с маркером удаления, чтобы пройти
  проверку ссылок;
- maintainer в
  [комментарии review](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/492#issuecomment-5255432841)
  потребовал восстановить historical links и redirect: валидатор должен
  адаптироваться к историческим артефактам, а не переписывать их;
- финальный PR #492 восстановил подход PR #491.

В охват входят названные в issue контракты и их взаимодействие. Это локальный
causal Analysis: внешнее исследование не проводится, compliance verdict не
выносится. Документ не меняет контракты, не выбирает стандарт, не задаёт
валидатор и не ретроактивно оценивает качество работы отдельных агентов.

## Findings

### 1. Тип ошибки: пробел композиции норм

Формулировка «консолидировать шаблоны» определила целевую функцию, но не
определила судьбу прежнего пути. Из неё следовали как минимум две внутренне
согласованные интерпретации:

1. функциональная консолидация: старый entry point перестаёт быть активным, но
   путь сохраняет совместимость;
2. физическая консолидация: superseded-файл удаляется, а его упоминания
   адаптируются к новому состоянию дерева.

PR #491 выбрал первую интерпретацию через право экспертного исполнения
[ADR-010, Принцип 1](../adr/2026-08-adr-010-agent-autonomy-principles.md) и
зафиксировал отклонение. PR #492 выбрал вторую, сопоставив явный scope шага 3
[RFC #470](../rfc/2026-08-06-rfc-task-statement-architecture.md) с текущей
структурой и link validation. Ни один исходный контракт не отвечал на
предшествующий вопрос: означает ли прекращение active-функции прекращение
файла, пути, содержимого, ссылочного адреса или только регистрации в UI.

Это не только пробел стандарта деприкации. Он образован пересечением пяти
неопределённых границ:

| Граница | Что определено | Чего не хватает для однозначного действия |
| --- | --- | --- |
| Автономия | Агент выбирает способ достижения цели; отклонение traceable. | Где заканчивается выбор способа при изменении identity/lifecycle существующего артефакта. |
| Hard Limits | Удаление или перезапись human work не переопределяются. | Является ли путь, metadata-only redirect, accepted ADR/RFC text или машинно созданный файл охраняемой human work; что считать удалением и перезаписью. |
| Amendment tier | Удаление артефакта — Tier 3; update links и allowlist могут быть Tier 1. | Как классифицировать одно составное изменение, где удаление, переписывание historical links и validator semantics конкурируют. |
| Lifecycle | Статусы существуют для классов документов. | Какие переходы разрешены физически, сохраняется ли path identity и что происходит с incoming links после terminal status. |
| Верификация | Проверки подтверждают структуру, ссылки и непустой дифф. | Как разрешать конфликт двух корректных инвариантов и какой из них должен адаптироваться. |

Поэтому корневая ошибка — **нормативная недоопределённость перехода и его
композиции**: нормы перечисляют ограничения вокруг действия, но не описывают
сам объект перехода, его состояние «до/после» и приоритеты при столкновении
инвариантов.

### 2. Почему действующие предохранители не сузили выбор

#### ADR-010

[Принцип 1](../adr/2026-08-adr-010-agent-autonomy-principles.md) разрешает
корректировать способ, если цель и hard limits сохранены. Однако изменение
пути одновременно выглядит как способ реализации консолидации и как решение о
жизненном цикле. Критерия различения этих классов нет.

[Принцип 2](../adr/2026-08-adr-010-agent-autonomy-principles.md) относит удаление
или перезапись существующей человеческой работы к закрытому перечню. Но предмет
защиты не операционализирован: текст, файл, путь, история, принятая ссылка и
служебная оболочка могут давать разные ответы. В результате запрет силён по
форме, но не определяет applicability.

[Принцип 3](../adr/2026-08-adr-010-agent-autonomy-principles.md) регулирует
ширину автономии, а не семантику lifecycle. Creative mode увеличивает множество
допустимых способов, но не помогает выбрать один при конкурирующих нормах.
`Consequences` сохраняет ADR/RFC как historical records, однако не определяет,
является ли active Markdown-link частью неизменяемого снимка и допустима ли
maintenance-правка принятого документа.

#### RFC #470

[§P.1](../rfc/2026-08-06-rfc-task-statement-architecture.md) повторяет границу
«как» против human-only решений, но наследует неопределённость объекта удаления.
[§P.2](../rfc/2026-08-06-rfc-task-statement-architecture.md) даёт безопасный
выход, когда противоречие уже распознано; он не требует искать недавно принятое
решение по тому же пути и потому не гарантирует обнаружение конфликта до
изменения.

[§P.3](../rfc/2026-08-06-rfc-task-statement-architecture.md) честно разделяет
машинную проверку и human review, но не задаёт отношения между валидатором
текущих ссылок и целостностью historical record. [§P.8](../rfc/2026-08-06-rfc-task-statement-architecture.md)
разрешает конфликт источников по иерархии authority; здесь же конфликтуют не
источники разного authority, а два следствия одного уровня. `Implementation and
Validation` задаёт порядок шагов внедрения, но не postcondition преемственности
между шагами и не объявляет результаты предыдущего шага входным состоянием
следующего.

#### AI Governance

[Amendment policy](../../ai-governance/ai-governance.md) классифицирует удаление
как Tier 3, update links/allowlist — как Tier 1, а validator semantics может
поднять tier. Но она не объясняет атомарную классификацию составного перехода и
не отличает «удалить active artifact» от «убрать obsolete implementation,
сохранив address compatibility».

[Обоснованное отклонение](../../ai-governance/ai-governance.md) проверяет цель,
минимальность, hard bans и traceability. Оно не проверяет temporal consistency
с недавно merged PR. Эскалация требует guidance при противоречии, но
предполагает, что противоречие уже видимо агенту.

#### Agent Work Rules

[Operating Modes](../../ai-rules/agent-work-rules.md) определяют степень
автономии, но не способ разрешения нескольких допустимых стратегий lifecycle.
[Контракт автономии](../../ai-rules/agent-work-rules.md) наследует размытость
`human work`. [Специфика сессий](../../ai-rules/agent-work-rules.md) описывает
новую сессию без памяти и необходимость передавать context, но не превращает
recent merged decisions по затронутым путям в обязательный context input.

Definition of Done допускает, что historical material «сохранён, перенесён или
удалён с rationale». Это проверяет наличие объяснения, но оставляет все три
взаимоисключающих исхода равноправными и не задаёт условия их выбора.

#### ADR-002

[ADR-002](../adr/2026-06-adr-002-artifact-document-methodology.md) различает
artifact classes, routing и status vocabularies. Для knowledge и governance
есть `superseded`/`deprecated`, но статусы не связаны с физическими состояниями
файла, стабильностью URL, ссылочной политикой и критериями удаления. Это
таксономия зрелости, а не полный lifecycle transition contract.

Кроме того, issue template неочевидно относится к одному из описанных классов:
он одновременно governance artifact, executable intake surface и historical
dependency. Поэтому даже правильное применение status vocabulary не снимает
неоднозначность.

#### ADR-008

[ADR-008](../adr/2026-07-adr-008-standard-meta-structure.md) задаёт единый
скелет стандартов, включая `Lifecycle`, `Boundaries`, `Validation` и
`Related Artifacts`. Он стандартизирует наличие секций, но не отношения между
нормами разных стандартов: ownership общей сущности, precedence, разрешение
перекрытия и поведение при несовместимых validators остаются вне модели.

#### ADR Structure Standard

[ADR Structure Standard](../../standards/adr-structure-standard.md) фиксирует
форму, статусы, supersession и traceability ADR. Он не отвечает, какие части
accepted ADR являются historical snapshot, какие допускают maintenance, как
обращаться с исходящими ссылками после исчезновения target и должен ли старый
ADR отражать современное дерево или состояние принятия решения.

### 3. Сопутствующие характерные ошибки

Один и тот же пробел проявляется там, где изменение имеет temporal identity,
несколько представлений и конкурирующие инварианты.

| Паттерн | Ситуация | Пространство разночтений | Пример |
| --- | --- | --- | --- |
| Historical integrity vs link health | Target исчез, historical document продолжает на него ссылаться. | ADR-010 не определяет maintenance historical links; §P.3 не задаёт приоритет проверок. | PR #492: code span против compatibility path. |
| Functional retirement vs physical deletion | Функция поглощена новым артефактом. | ADR-002 даёт статус, но не file-state transition; amendment tiers оценивают разные части по-разному. | `task-creative.md`: hidden redirect против отсутствующего файла. |
| Consolidation vs structural limits | Несколько домов надо объединить, но новый archive/compatibility home запрещён Anti-Inflation. | Resolver ограничивает routing, но не выбирает судьбу legacy paths. | Гипотетическое перемещение deprecated templates в новый каталог. |
| Agent initiative vs implicit governance decision | Технически малое действие меняет identity, routing или decision boundary. | Принцип 1 описывает способ; Tier 3 — смысл/структуру; критерий перехода между ними неполон. | Замена старого entry point alias на новый path. |
| Issue mandate vs hard limit applicability | Issue явно просит cleanup, но затрагивает существующую работу. | Запрет силён, но `human work`, `delete`, `overwrite` не имеют testable scope. | Удаление generated template с human-reviewed history. |
| Sequential task drift | Вторая задача пересекает свежий результат первой, но формально имеет собственный SSOT. | Session rules признают отсутствие памяти; обязательного recent-path decision scan нет. | #491 merged в процессе #492; первоначальные решения разошлись. |
| Validator-induced semantic edit | Проверка текущего состояния мотивирует изменить исторический или нормативный текст. | V-1 требует validators, но нет границы «адаптировать проверку или данные». | Перевод Markdown-links в code spans ради broken-link check. |
| Partial representation update | Artifact представлен файлом, index entry, manifest row, redirect и links. | DoD требует sync, но не определяет canonical identity и атомарность перехода. | Файл удалён, а downstream historical identity сохранена только текстовым маркером. |
| Status without operational meaning | `deprecated`/`superseded` присвоен, но потребители не знают допустимое поведение. | Status vocabularies не задают availability, discoverability и compatibility guarantees. | Deprecated redirect скрыт из UI, но сохранён для ссылок. |
| Concurrent base movement | Решение принимается на старом base, а новая работа меняет тот же объект. | RFC рассматривает source conflicts, но не temporal conflict между PR outcomes. | #492 начат до merge #491 и затем синхронизирован с `main`. |

Общий признак: локальная корректность каждого шага не обеспечивает
последовательную корректность состояния. Traceability объясняет решение после
факта, но не заменяет transition semantics.

### 4. Узкие места как cross-contract matrix

| Вопрос | ADR-010 | RFC #470 | Governance / Rules | ADR-002 / ADR-008 / ADR standard | Итоговый gap |
| --- | --- | --- | --- | --- | --- |
| Что именно сохраняется во времени? | Охраняет human work. | Охраняет human decision rights. | Требует rationale historical material. | Описывает classes/status/form. | Нет единой модели identity: content/path/history/interface. |
| Когда допустим physical removal? | Hard limit без applicability criteria. | Эскалация после обнаружения конфликта. | Tier 3 для deletion. | Нет transition preconditions. | Запрет и процесс есть, критериев выбора нет. |
| Что делать с historical links? | Historical record упомянут без link semantics. | Link health проверяется, precedence отсутствует. | Validators обязательны. | ADR maintenance не определён. | Нет политики target disappearance. |
| Как наследуется решение предыдущей задачи? | Не рассматривает temporal ordering. | Priority для sources, не PR outcomes. | Каждая session без памяти. | Traceability статична. | Recent accepted precedent необязателен как input. |
| Как конфликтуют validators? | Human review для смысла. | V-1/V-2 разделены. | Tier зависит от semantics. | Validation section обязательна по форме. | Нет ownership и precedence инвариантов. |
| Как оценить составное изменение? | По hard limit. | По цели/способу. | Tier по maximum sign. | По artifact class. | Нет общей единицы классификации transition. |

## Reasoning Chain: от пробела к вопросам будущих стандартов

Ниже не proposal решения, а последовательность, показывающая, почему до
следующего normative шага нужны определённые ответы.

1. Последовательные задачи меняют не изолированные файлы, а состояние
   репозитория во времени.
2. Состояние одного артефакта наблюдается через содержимое, путь, metadata,
   навигацию, входящие ссылки, validators и Git history.
3. Поэтому «консолидировать», «deprecated», «superseded» и «удалить» нельзя
   интерпретировать только как filesystem operation или status label.
4. Если identity и переход не определены, Принцип 1 легализует несколько
   способов, а Hard Limits невозможно одинаково применить к каждому.
5. Если не определён historical boundary, link validator и historical integrity
   могут требовать взаимоисключающих изменений.
6. Если результат предыдущей задачи не является обязательным входом следующей,
   каждый агент может заново открыть уже принятое локальное решение.
7. Если у норм нет ownership/precedence при пересечении, amendment tiers и
   validators классифицируют части изменения, но не весь переход.
8. Следовательно, до выбора конкретных норм должны быть закрыты вопросы ниже;
   только после ответов можно понять, какие normative artifacts вообще нужны и
   как они взаимодействуют с существующими контрактами.

### Вопросы, которые должны быть закрыты

**Identity и объект защиты**

- Что является идентичностью артефакта: содержимое, путь, роль, запись в
  navigation, публичный интерфейс или их комбинация?
- Какие части accepted/historical документа образуют snapshot, а какие являются
  обслуживаемыми метаданными?
- Что означает `human work` для generated, agent-authored и human-reviewed
  артефактов?

**Lifecycle и переходы**

- Какие наблюдаемые состояния соответствуют `active`, `deprecated`,
  `superseded`, `archived` и физическому отсутствию?
- Какие preconditions, evidence и human decisions требуются для каждого
  перехода?
- Какие гарантии discoverability, availability и reversibility сохраняются
  после перехода?

**Ссылки и история**

- Должна ли ссылка в historical record разрешаться в современном дереве или
  сохранять буквальный снимок момента принятия?
- Где проходит граница между maintenance исторического документа и
  ретроактивным переписыванием rationale/evidence?
- Какая сторона адаптируется при конфликте historical integrity и link health,
  и по какому признаку?

**Композиция контрактов**

- Кто владеет нормой, если lifecycle, routing, status, amendment tier и
  validator одновременно применимы к одному переходу?
- Как определяется приоритет при несовместимых, но одинаково обязательных
  инвариантах?
- Как классифицируется составное изменение: целиком, по максимальному риску или
  по независимым частям?

**Преемственность задач**

- Какие результаты недавно merged PR обязательны как вход следующей задачи,
  затрагивающей тот же path/contract?
- Как отличить уточнение предыдущего решения от его отмены?
- В какой момент временное расхождение веток становится нормативным конфликтом,
  требующим human decision?

**Верификация**

- Какие свойства перехода механически наблюдаемы, а какие остаются human-only?
- Как validator сообщает конфликт норм, не вынуждая семантически менять
  historical evidence?
- Как доказать не только корректность конечного дерева, но и легальность
  перехода из предыдущего состояния?

### Взаимодействие с действующими контрактами

Ответы должны сохранить разделение ответственности, уже присутствующее в
репозитории:

- ADR-010 остаётся источником границы автономии и human-only limits, но ему
  нужна однозначная applicability внешней lifecycle-семантики;
- RFC #470 и Agent Work Rules остаются execution/escalation/verification
  слоем, которому требуется проверяемый вход о предшествующих решениях;
- AI Governance остаётся owner amendment tiers и human decision rights, но
  должна получать однозначный класс составного перехода;
- ADR-002 остаётся owner artifact classes/routing/status vocabularies, не
  смешивая их с ещё не определённой физической семантикой;
- ADR-008 остаётся стандартом формы стандартов; cross-standard ownership и
  precedence должны быть явно размещены, а не возникать как побочный эффект
  одинаковых секций;
- ADR Structure Standard остаётся owner формы ADR и сможет ссылаться на
  определённую historical/link семантику, не дублируя её.

Такой порядок не предрешает, будет ли результат одним стандартом, несколькими
уточнениями или иным normative artifact. Он лишь предотвращает повторение
исходной ошибки: выбор механизма до определения вопроса, который механизм
должен разрешать.

## Recommendations

Использовать этот Analysis как вход для отдельного human-reviewed этапа
сравнения вариантов. На этом этапе не считать redirect, archive, tombstone,
allowlist, rewrite или validator change решением по умолчанию: каждый из них
отвечает только на часть матрицы вопросов.

Review focus для текущего документа:

1. верно ли выделен корневой класс ошибки — композиция норм и transition
   semantics, а не ошибка конкретного агента;
2. полный ли набор identity/lifecycle/history/precedence/continuity вопросов;
3. не превращена ли аналитическая цепочка в скрытое предписание механизма;
4. согласовано ли распределение будущих ответов с ownership существующих
   контрактов.

## Related Artifacts

- [Issue #495](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/495)
- [PR #491](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/491)
- [PR #492](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/492)
- [ADR-010](../adr/2026-08-adr-010-agent-autonomy-principles.md)
- [RFC #470](../rfc/2026-08-06-rfc-task-statement-architecture.md)
- [AI Governance](../../ai-governance/ai-governance.md)
- [Agent Work Rules](../../ai-rules/agent-work-rules.md)
- [ADR-002](../adr/2026-06-adr-002-artifact-document-methodology.md)
- [ADR-008](../adr/2026-07-adr-008-standard-meta-structure.md)
- [ADR Structure Standard](../../standards/adr-structure-standard.md)
- [Analysis Standard](../../standards/analysis-standard.md)
