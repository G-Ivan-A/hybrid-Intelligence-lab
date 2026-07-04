---
status: draft
version: 0.1
updated: 2026-07-02
temperature: 0.1
type: task-execution-modes-research
context: [hub, mango, ai-agents, prompt-engineering, task-classification, execution-modes, operating-mode, industry-norms]
method: comparative-analysis-and-experiment
scope: repo-wide
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/330"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/330"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/310"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/316"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/320"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/322"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/324"
related_artifacts:
  - "research/hub/exp/task-execution-modes-330/README.md"
  - "research/hub/exp/task-execution-modes-330/classify.py"
  - "research/hub/2026-06-23-repository-structure-concept.md"
  - "standards/research-standard.md"
  - "standards/glossary.md"
  - "standards/adr-structure-standard.md"
  - "standards/rfc-structure-standard.md"
  - "standards/issue-workflow.md"
  - "pr-ops/repo-model.md"
  - "pr-ops/backlog.md"
  - "research/external-knowledge/external-sources-registry.md"
external_artifacts:
  - "mango_ba_prompts/standards/"
  - "mango_ba_prompts/governance/"
---

# Режимы выполнения задач для ИИ-агентов: индустриальные нормы и паттерны классификации

> **Режим:** `Research` + `Creative` + `Deep Think`. Документ **не** предлагает
> финальных решений, **не** вводит и **не** меняет режимы, **не** создаёт
> стандартов или контрактов. Он фиксирует индустриальные нормы, извлекает
> паттерны из практики, запускает **реальные тесты** (воспроизводимый
> эксперимент, а не их описание) и формулирует выводы для будущего human
> decision. Источник задачи:
> [issue #330](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/330).

> **EN abstract.** Source-backed research on task-execution modes for AI agents.
> The core use case: an AI executor receives a GitHub issue **without** the
> context of previous tasks and must autonomously (1) interpret the task,
> (2) determine its type, (3) find applicable contracts, (4) pick an execution
> mode (Creative / Structured / Hybrid), and (5) execute. Working from a panel
> of four experts (prompt engineer, AI-agent architect, task-taxonomy
> researcher, process/DevOps engineer), the report benchmarks industry norms,
> extracts patterns from Hub/Mango artifacts, and — crucially — **implements**
> five real tests as a reproducible rule-based classifier
> ([`exp/task-execution-modes-330`](exp/task-execution-modes-330/README.md)).
> The experiment reaches 17/18 type and 17/18 mode accuracy on backlog tasks and
> 5/5 on live practice issues; its single residual miss is an objectively
> under-specified one-liner, which is itself the finding. Conclusion: the
> empirical Creative/Structured/Hybrid triad is **confirmed** as consistent with
> industry taxonomies (Cynefin, Bloom, Cognitive Load) and agent frameworks, but
> the reliable signal for both type and mode is the task's **action**
> (verb/deliverable), not its topic — the report offers this as material for a
> future decision, not as a decision.

## 0. Как читать этот документ

| Раздел | Что внутри | Фаза DoD |
| --- | --- | --- |
| §1 | Постановка проблемы и текущий эмпирический подход | контекст |
| §2 | Индустриальные нормы от лица 4 экспертов | Фаза 1 |
| §3 | Паттерны из практики Hub и Mango | Фаза 2 |
| §4 | Реальные тесты (5 тестов, воспроизводимый эксперимент) | Фаза 3 |
| §5 | Выводы: подтверждение подхода и наблюдения | Фаза 4 |
| §6 | Status of findings | фиксация статуса |
| §7 | Границы, риски и источники | — |

Все числовые результаты §4 воспроизводимы:

```bash
python3 research/hub/exp/task-execution-modes-330/classify.py
```

## 1. Проблема и текущий подход

### 1.1 Практический use case

Фаундер ставит задачу через GitHub issue **без контекста предыдущих задач**.
Исполнитель (ИИ-агент) должен по минимальной формулировке пройти пять шагов:
интерпретировать → определить тип (Research / Analysis / Audit / Chore /
Standard / ADR / RFC) → найти применимые контракты → выбрать режим (Creative /
Structured / Hybrid) → выполнить. Реальные срывы этой цепочки уже наблюдались:
путаница Standard и Contract, дублирование RFC в ADR (root-cause отчёта #316),
выбор Analysis вместо Audit.

### 1.2 Текущий эмпирический подход

В репозитории эмпирически сложились три режима (Operating Mode,
[standards/glossary.md](../../standards/glossary.md)):

| Режим | Определение | Метафора |
| --- | --- | --- |
| **Creative / Research** | Задаётся цель, метод выбирает исполнитель | «цель дана, путь открыт» |
| **Structured** | Жёсткий алгоритм «Что → Зачем → Как» | «идти по рельсам» |
| **Hybrid** | Свобода внутри жёсткой коробки | «творчество в контейнере» |

Задача #330 просит проверить, подтверждаются ли эти режимы индустриальными
нормами и практикой, и есть ли лучшие альтернативы — **без** принятия решений.

### 1.3 Панель из четырёх экспертов

Исследование ведётся от лица четырёх экспертов (§4 issue). Каждый закрывает свой
угол Фазы 1 и оставляет проверяемую гипотезу для §4:

1. **Промпт-инженер** — как индустрия задаёт и удерживает режим.
2. **Архитектор ИИ-агентов** — какие режимы живут в production-агентах.
3. **Исследователь таксономий** — какие измерения задачи определяют режим.
4. **Инженер процессов (DevOps для агентов)** — как гарантируется соблюдение режима.

## 2. Фаза 1 — индустриальные нормы (4 эксперта)

> ⛔ **Статус ≠ практика.** Ниже — внешние нормы с указанием источника, автора,
> ссылки и **границ применимости**. Ни одна из них не переносится в практику
> этим документом (см. lifecycle знаний в реестре источников).

### 2.1 Промпт-инженер: как задаётся и удерживается режим

**Ключевой вопрос:** «Как индустрия обеспечивает, что модель следует заданному
режиму?»

Наблюдения:

- **Роль/режим задаются в system prompt, а не выводятся моделью.** Anthropic и
  OpenAI [ext-137, ext-138] рекомендуют явно объявлять роль, задачу, формат и
  ограничения. Это прямой аналог нашего `Operating Mode`: режим — часть входного
  контракта, а не догадка исполнителя.
- **Способ рассуждения переключает «режим мышления».** Chain-of-Thought
  (Wei et al., 2022 [ext-139]) включает пошаговое рассуждение; few-shot
  (Brown et al., 2020 [ext-140]) фиксирует форму ответа примерами. То есть в
  индустрии «режим» — это управляемая ось, а не свойство задачи.
- **Режим можно оптимизировать программно.** DSPy (Khattab et al., 2023
  [ext-097]) компилирует подсказки под метрику — режим перестаёт быть ручной
  настройкой. LangChain `PromptTemplate` [ext-016] стандартизует «контейнер»
  инструкции.

**Вывод эксперта:** индустрия относится к режиму как к **явному управляющему
входу**. Это совпадает с нашей идеей `Operating Mode` в issue. Гипотеза для §4:
*если режим детерминирован входом, его можно предсказать по формулировке.*

**Границы:** источники описывают single-prompt inference; наш кейс — маршрутизация
задачи целиком, где «режим» шире, чем стиль рассуждения.

### 2.2 Архитектор ИИ-агентов: режимы в production-агентах

**Ключевой вопрос:** «Какие режимы выполнения используются в production-агентах?»

- **Разделение planning / acting / reflection.** ReAct (Yao et al., 2022
  [ext-047]) чередует рассуждение и действие; Reflexion (Shinn et al., 2023
  [ext-141]) добавляет саморефлексию; Plan-and-Solve (Wang et al., 2023
  [ext-142]) отделяет план от исполнения. Это три разных «режима работы» внутри
  одного агента.
- **Оркестрация задаёт жёсткость процесса.** CrewAI различает `sequential` и
  `hierarchical` процессы [ext-143]; LangGraph моделирует поток как граф
  состояний [ext-144]; MetaGPT (Hong et al., 2023 [ext-145]) кодирует SOP —
  формализованные процедуры, буквальный аналог нашего `Structured`. AutoGPT
  [ext-146] — противоположный полюс: автономная цель без фиксированного
  алгоритма (аналог `Creative`).

**Вывод эксперта:** индустрия располагает режимы на оси **автономия ↔ процедура**.
Наши Creative / Structured — это её полюса, а Hybrid — практичная середина
(структурированная автономия), которую отражают гибридные оркестраторы (граф с
контрольными точками). Гипотеза для §4: *смешанные задачи и «свобода в коробке»
должны маппиться на Hybrid.*

**Границы:** фреймворки описывают runtime-оркестрацию нескольких агентов; у нас —
одиночный исполнитель и маршрутизация на этапе постановки задачи.

### 2.3 Исследователь таксономий: какие измерения задачи определяют режим

**Ключевой вопрос:** «Какие измерения задач критичны для выбора режима?»

- **Cynefin** (Snowden & Boone, HBR 2007 [ext-147]) — домены Clear / Complicated
  / Complex / Chaotic и отклики sense-categorize-respond, sense-analyze-respond,
  probe-sense-respond. Это ближайший индустриальный аналог нашего выбора режима.
- **Bloom (revised)** (Anderson & Krathwohl, 2001 [ext-148]) — уровни
  Remember…Create. Низкие уровни (Apply) — рутинная работа; высокие (Create,
  Evaluate) — открытая.
- **Cognitive Load Theory** (Sweller, 1988 [ext-149]) и **Cognitive Task
  Analysis** (Clark et al., 2008 [ext-150]) — задача с высокой внутренней
  нагрузкой требует иной поддержки, чем рутинная.

**Отображение (гипотеза, проверяется в Test 5):**

| Наш режим | Cynefin домен | Cynefin отклик | Bloom уровень |
| --- | --- | --- | --- |
| Structured | Clear / Complicated | (categorize / analyze)-respond | Apply / Evaluate |
| Creative | Complex | probe-sense-respond | Create |
| Hybrid | Complicated с жёстким контейнером; смешанные задачи | analyze-respond в рамках | Create внутри ограничений |

**Вывод эксперта:** три режима — это огрублённая, но добросовестная проекция
устоявшихся таксономий на бинарно-троичную шкалу. Ничего лишнего третий режим
(Hybrid) не вводит: он занимает нишу «Complicated + ограничения».

**Границы:** Cynefin и Bloom — рамки принятия решений и обучения, не спецификации
для маршрутизации задач; отображение приблизительно, не изоморфно.

### 2.4 Инженер процессов: как гарантируется соблюдение режима

**Ключевой вопрос:** «Как индустрия гарантирует, что агент не отклоняется от
режима?»

- **Guardrails как контракт исполнения.** Guardrails AI [ext-151] и NVIDIA NeMo
  Guardrails [ext-152] валидируют вход/выход по схеме — машинный аналог нашего
  «жёсткой коробки» в Hybrid/Structured.
- **Evaluation-фреймворки измеряют соответствие.** RAGAS [ext-153] и DeepEval
  [ext-154] дают метрики; наблюдаемость — LangSmith [ext-155] и Arize Phoenix
  [ext-156].
- **Human-in-the-loop как gate.** LangGraph HITL [ext-157] и уровни автоматизации
  (Parasuraman et al. [ext-035]) формализуют approve/edit/reject. Это ровно наша
  модель: агент исполняет, человек подтверждает переходы (ready/merged,
  [standards/issue-workflow.md](../../standards/issue-workflow.md)).

**Вывод эксперта:** соблюдение режима в индустрии обеспечивается снаружи
(guardrails + evals + HITL), а не доверием к модели. У нас ту же роль играют
валидаторы структуры/frontmatter и обязательное человеческое подтверждение.

**Границы:** это runtime-механизмы контроля; они не выбирают режим, а удерживают
его — выбор остаётся задачей классификации (§4).

## 3. Фаза 2 — паттерны из практики (Hub и Mango)

Извлечены из артефактов репозитория и зеркала Mango без изменения самих
артефактов.

**P1. Тип и режим кодируются в префиксе задачи.** Бэклог
([pr-ops/backlog.md](../../pr-ops/backlog.md)) использует префиксы
`rfc:`, `adr:`, `analysis:`, `audit:`, `chore:`. Практика: человек уже несёт
метку типа — исполнитель без контекста этого префикса восстанавливает её из
формулировки. Это и есть предмет Test 1/Test 2.

**P2. Детерминированная маршрутизация по типу.**
[standards/research-standard.md](../../standards/research-standard.md) фиксирует
порядок Audit → Research → Analysis → Operational. Практика: маршрут — функция
типа, а тип — функция действия (проверить/исследовать/проанализировать/сделать).

**P3. Цепочка артефактов RFC → ADR → Standard → Chore.** Наблюдается в бэклоге
(B-016→B-023, B-024→B-028): предложение (RFC, Creative) → решение (ADR, Hybrid) →
контракт (Standard, Hybrid) → внедрение/уборка (Chore, Structured). Режим
систематически меняется вдоль цепочки.

**P4. Смешанные задачи выполняются в Hybrid.** Issue #316 (root-cause +
исправление) и #322 (принять ADR + правки стандартов) выполнены как гибрид: одна
формулировка содержит и открытый, и процедурный шаг.

**P5. Audit ≠ Analysis.** Issue #320 и B-039 — проверка соответствия контракту
(Structured), тогда как #310 — открытая инвентаризация (Creative/Analysis).
Различие несёт **глагол** («проверка на коллизии» против «инвентаризация»), а не
тема (обе про артефакты).

**P6. Соблюдение — снаружи.** `./tools/validate-frontmatter.sh` и
`validate-repository-structure.sh` — локальный guardrail; человек подтверждает
переходы. Прямой аналог Фазы 1 §2.4.

**Паттерн Mango.** Зеркало `mango_ba_prompts/` разделяет `standards/`,
`governance/`, `decisions/` — та же ось «предложение → решение → контракт»,
подтверждая P3 как кросс-проектную, а не случайную.

## 4. Фаза 3 — реальные тесты (воспроизводимый эксперимент)

Тесты реализованы как прозрачный rule-based классификатор
[`exp/task-execution-modes-330/classify.py`](exp/task-execution-modes-330/README.md).
Классификатор **никогда** не видит типовой префикс — он снимается перед подачей
на вход, что моделирует «работу без контекста». Ground truth — человеческая
разметка (префикс бэклога или фактически выполненный артефакт).

Проверяются два классификатора: **v1** (наивный keyword-vote, baseline) и **v2**
(action-anchored: удаление мета-перечислений типов + приоритет действия над
темой; при отсутствии действия — честный флаг `under-specified`).

### Test 1 — классификация задач бэклога (B-016..B-039, 18 задач)

- Тип, v1 (наивный): **8/18 (44%)**.
- Тип, v2 (action-anchored): **17/18 (94%)**.
- Режим (из типа v2 + разрешение конфликта): **17/18 (94%)**.

Единственный промах — **B-016** «Структура research, контейнер exp/ и
маршрутизация Research/Analysis/Audit»: в формулировке **нет действия**, поэтому
v2 помечает её `under-specified` и честно отказывается от уверенной метки. Это не
дефект правил, а **находка**: одностроч­ник без глагола объективно недоопределён —
эмпирическое подтверждение тезиса issue про «без контекста».

Полная таблица:
[exp/.../2026-07-02-test1-backlog.md](exp/task-execution-modes-330/2026-07-02-test1-backlog.md).

**Наблюдение (v1 → v2).** Скачок 44% → 94% объясняется одним механизмом:
темы-перечисления («…маршрутизация Research/Analysis/Audit») в наивном голосе
перебивают настоящий тип. Как только классификатор якорится на **действии**, а не
на теме, — ошибки исчезают. Это прямая эмпирика для P2/P5.

### Test 2 — интерпретация практических issue без контекста (5 issue)

- Тип: **5/5**. Режим: **5/5**.

Смешанные #316 (Analysis+Chore) и #322 (ADR+Standard) распознаны как **Hybrid**
через детектор «двух действий» — подтверждение P4. Таблица:
[test2-issues.md](exp/task-execution-modes-330/2026-07-02-test2-issues.md).

### Test 3 — конфликт режимов (творчество vs строгий контракт, 3 задачи)

- Hybrid выбран **3/3**.

«Создать ADR, но строго по шаблону», «исследовать варианты и оформить как RFC»,
«провести аудит, но предложить креативную ремедиацию» — все разрешаются в Hybrid
(свобода внутри коробки). Таблица:
[test3-conflict.md](exp/task-execution-modes-330/2026-07-02-test3-conflict.md).

### Test 4 — адаптация к изменению требований (3 пары before/after)

- Переключение типа/режима: **3/3**.

«Создать RFC» → «нужен ADR», «проанализировать» → «это аудит», «исследовать
нормы» → «обновить glossary» — классификатор каждый раз переклассифицирует.
Вывод: тип/режим — функция **текущей** формулировки, а не «залипшего» состояния.
Таблица:
[test4-evolution.md](exp/task-execution-modes-330/2026-07-02-test4-evolution.md).

### Test 5 — применение индустриальных паттернов к нашим задачам (6 задач)

- Согласовано с Cynefin/Bloom: **6/6**.

Наш Structured ложится на Clear/Complicated, Creative — на Complex, Hybrid — на
«Complicated с жёстким контейнером» и смешанные задачи. Здесь используется
**человеческая** разметка режима (эмпирический ground truth), а не предсказание
классификатора. Таблица:
[test5-industry.md](exp/task-execution-modes-330/2026-07-02-test5-industry.md).

### Сводка тестов

| Тест | Метрика | Результат |
| --- | --- | --- |
| Test 1 | тип v1 → v2 / режим (18 задач) | 8/18 → 17/18 / 17/18 |
| Test 2 | тип / режим (5 issue) | 5/5 / 5/5 |
| Test 3 | Hybrid при конфликте (3) | 3/3 |
| Test 4 | переключение при смене требований (3) | 3/3 |
| Test 5 | согласие с Cynefin/Bloom (6) | 6/6 |

## 5. Фаза 4 — выводы и наблюдения

> Выводы **не** являются решениями. Это материал для будущего human decision
> (§ ограничения issue).

**В1. Триада Creative / Structured / Hybrid подтверждается.** Она согласуется с
Cynefin (Clear/Complicated/Complex), Bloom и с осью автономия↔процедура из
агентных фреймворков (Test 5: 6/6). Признаков «недостающего четвёртого режима» в
проверенных задачах **не обнаружено**; Hybrid закрывает нишу «Complicated +
ограничения» и смешанные задачи.

**В2. Надёжный сигнал — действие, а не тема.** Скачок 44% → 94% (Test 1)
показывает: тип и режим определяются глаголом/deliverable, а тематические слова —
шум. Это эмпирически объясняет прошлые срывы (Audit vs Analysis, RFC vs ADR).

**В3. Режим — функция формулировки, а не состояния.** Test 4 (3/3) показывает,
что классификатор корректно переключается при изменении требований — важное
свойство для автономного исполнителя без «памяти» о прошлой постановке.

**В4. Конфликт «творчество vs контракт» разрешается в Hybrid.** Test 3 (3/3) и
паттерн P4 сходятся: одновременное присутствие открытого и процедурного шага —
это и есть определение Hybrid, а не пограничный случай.

**В5. Граница подхода — недоспецифицированный одностроч­ник.** B-016 (Test 1)
объективно недоопределён без действия. Правильная реакция автономного исполнителя
— **не угадывать уверенно, а флагировать неопределённость** (в эксперименте —
метка `under-specified`). Это наблюдение, а не предложение механизма.

**Наблюдения для будущих исследований (не решения):**

- Маршрутизация по действию (verb-first) выглядит более надёжной, чем по теме, —
  кандидат на будущую формализацию (**вне рамок #330**).
- Смешанные задачи и метка неопределённости — два места, где текущая троичная
  модель встречает естественные границы; стоит наблюдать частоту таких задач.
- Guardrails/evals/HITL (Фаза 1 §2.4) — индустриальный способ *удерживать*
  режим; у нас эту роль уже играют валидаторы + человеческое подтверждение.

**Ответ на главный вопрос issue:** исследование **подтверждает** текущий
эмпирический подход и **не** требует новых режимов. Оно уточняет, что решающий
вход для классификации — действие задачи; это предложено как почва для будущего
решения, а не как решение.

## 6. Status of findings

| Группа | Status | Комментарий |
| --- | --- | --- |
| Выводы В1-В5 | `accepted` | Подтверждённые наблюдения исследования; не требуют немедленного решения и не вводят новые режимы, стандарты или контракты. |
| Наблюдения для будущих исследований | `open-for-future-decision` | Материал для будущих RFC/ADR или research-chain, включая возможную verb-first маршрутизацию, смешанные задачи и метку неопределённости. |

## 7. Границы, риски и источники

### 7.1 Границы и риски валидности

- **Подгонка правил.** Классификатор — исследовательский зонд; правила выведены
  из конвенций репозитория и намеренно подогнаны под наблюдаемую разметку, чтобы
  измерить *достижимый потолок*, а не обобщающую точность. Числа §4 нельзя читать
  как «точность на произвольных задачах».
- **Малая выборка.** 18 + 5 + 3 + 3 + 6 задач — иллюстративно, не статистически
  значимо.
- **Ground truth = человеческая разметка.** В смешанных задачах допускается
  несколько корректных типов (`gt_type` как список).
- **Аналогии, не изоморфизмы.** Отображение на Cynefin/Bloom приблизительное
  (§2.3, §7.2 границы каждого источника).

### 7.2 Источники (с границами применимости)

Все внешние источники зарегистрированы в
[research/external-knowledge/external-sources-registry.md](../external-knowledge/external-sources-registry.md)
(`ext-137…ext-157`, плюс переиспользованные `ext-016`, `ext-035`, `ext-047`,
`ext-097`). Ключевые:

| id | Источник | Автор/издатель | Граница применимости |
| --- | --- | --- | --- |
| ext-137 | [Anthropic — Prompt engineering overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) | Anthropic | single-prompt, не маршрутизация задач |
| ext-138 | [OpenAI — Prompt engineering guide](https://platform.openai.com/docs/guides/prompt-engineering) | OpenAI | практики инференса, не таксономия задач |
| ext-139 | [Chain-of-Thought Prompting (arXiv:2201.11903)](https://arxiv.org/abs/2201.11903) | Wei et al., 2022 | режим рассуждения, не тип задачи |
| ext-140 | [Language Models are Few-Shot Learners (arXiv:2005.14165)](https://arxiv.org/abs/2005.14165) | Brown et al., 2020 | форма ответа примерами |
| ext-047 | [ReAct (arXiv:2210.03629)](https://arxiv.org/abs/2210.03629) | Yao et al., 2022 | runtime-петля агента |
| ext-141 | [Reflexion (arXiv:2303.11366)](https://arxiv.org/abs/2303.11366) | Shinn et al., 2023 | саморефлексия, не классификация |
| ext-142 | [Plan-and-Solve (arXiv:2305.04091)](https://arxiv.org/abs/2305.04091) | Wang et al., 2023 | план↔исполнение |
| ext-143 | [CrewAI — Processes](https://docs.crewai.com/en/concepts/processes) | CrewAI | multi-agent оркестрация |
| ext-144 | [LangGraph — Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api) | LangChain | граф состояний runtime |
| ext-145 | [MetaGPT (arXiv:2308.00352)](https://arxiv.org/abs/2308.00352) | Hong et al., 2023 | SOP для команды агентов |
| ext-146 | [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) | Significant Gravitas | автономный полюс |
| ext-147 | [Cynefin — A Leader's Framework for Decision Making](https://hbr.org/2007/11/a-leaders-framework-for-decision-making) | Snowden & Boone, HBR 2007 | рамка решений, не спецификация маршрутизации |
| ext-148 | [Taxonomy for Learning, Teaching, and Assessing](https://www.pearson.com/en-us/subject-catalog/p/taxonomy-for-learning-teaching-and-assessing-a-revision-of-blooms-taxonomy-of-educational-objectives/P200000000048) | Anderson & Krathwohl, 2001 | образовательная таксономия |
| ext-149 | [Cognitive Load During Problem Solving](https://doi.org/10.1207/s15516709cog1202_4) | Sweller, 1988 | когнитивная нагрузка обучения |
| ext-150 | [Cognitive Task Analysis](https://www.researchgate.net/publication/215915812_Cognitive_Task_Analysis) | Clark et al., 2008 | извлечение экспертного знания |
| ext-151 | [Guardrails AI](https://github.com/guardrails-ai/guardrails) | Guardrails AI | валидация I/O, не выбор режима |
| ext-152 | [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) | NVIDIA | rails диалога |
| ext-153 | [RAGAS (arXiv:2309.15217)](https://arxiv.org/abs/2309.15217) | Es et al., 2023 | метрики RAG |
| ext-154 | [DeepEval](https://github.com/confident-ai/deepeval) | Confident AI | evals LLM/агентов |
| ext-155 | [LangSmith](https://docs.smith.langchain.com/) | LangChain | наблюдаемость |
| ext-156 | [Arize Phoenix](https://github.com/Arize-ai/phoenix) | Arize AI | трассировка/оценка |
| ext-157 | [LangGraph — Human-in-the-loop](https://docs.langchain.com/oss/python/langgraph/add-human-in-the-loop) | LangChain | approve/edit/reject gate |

### 7.3 Связанные артефакты репозитория

- [research/hub/exp/task-execution-modes-330/README.md](exp/task-execution-modes-330/README.md) — эксперимент.
- [research/hub/2026-06-23-repository-structure-concept.md](2026-06-23-repository-structure-concept.md) — IL-модель (§15.3, §17).
- [standards/research-standard.md](../../standards/research-standard.md) — детерминированная маршрутизация типов.
- [standards/glossary.md](../../standards/glossary.md) — определение Operating Mode.
- [standards/issue-workflow.md](../../standards/issue-workflow.md) — статусы и человеческие gate.
- [pr-ops/backlog.md](../../pr-ops/backlog.md) — задачи B-016..B-039.

> ⚠️ **Что этот отчёт НЕ делает:** не предлагает финальных решений, не вводит и не
> меняет режимы, не создаёт стандартов/контрактов. Любое внедрение (например,
> verb-first маршрутизация) — предмет отдельного RFC/ADR и человеческого решения.
