---
status: draft
version: 0.1
updated: 2026-06-16
temperature: 0.1
owner: G-Ivan-A
rfc-scope: A
---

# RFC: Methodology Research & Proposals for Hub / Mango / Open-AI

## Proposal

Зафиксировать результат исследования (Creative mode, Research → RFC) по шести
методологиям, предложенным консалтинговой командой С, и сформировать на их основе
**единый методологический синтез** для экосистемы плюс **три независимых, но
согласованных предложения** под три проекта:

1. **Исследование и анализ** всех шести методологий — Enterprise Intelligence,
   Opportunity Discovery, Human-AI Collaboration, Trust & Evidence, Influence &
   Network Analysis, AI Solution Architecture — с минимум тремя проверенными
   внешними источниками на каждую, разбором сильных/слабых сторон, рисков
   внедрения и зависимостей.
2. **Сравнение с принятыми RFC** PR #242 (Research Memory & Source Intelligence),
   PR #243 (Repository Archetypes) и PR #244 (Mango Migration Plan): что
   переиспользовать, что расширить, какие Open Decisions затрагиваются.
3. **Подтверждение и расширение предложения фаундера**: классификация
   BA-процессов в Product Layer и шаблон AI Solution Architecture из семи секций —
   приняты, согласованы с уже существующими моделями и дополнены, без изобретения
   заново.
4. **Три независимых предложения** (Хаб / Mango / Open-AI) с определением уровней
   **L3 (детализация)** и **L4 (реализация)** для каждого.
5. **Модель консистентности и переиспользования** — что является универсальным
   скелетом для будущих проектов экосистемы, а что специфично.

RFC фиксирует исследование, синтез и rationale. Обязательная норма после human
decision должна быть делегирована в active artifact (`standards/`, `templates/`,
`practices/`, validators) — до этого документ остаётся draft-рекомендацией
([governance/rfc/README.md](README.md)). Этот RFC **не** создаёт сам по себе шесть
методологических стандартов; он определяет, какие из них и в какой
последовательности должны появиться, под какой реальной операционной болью
(Anti-Inflation, [governance/repo-model.md](../repo-model.md)).

## Decision Scope

- Это **не** немедленное создание шести методологических стандартов. RFC закрывает
  уровень Research → RFC: анализ, синтез, приоритизация и план. Перевод в
  `standards/`/`templates/` идёт отдельными задачами под реальную боль.
- Это **не** физическая миграция Mango или Open-AI. Mango используется как
  проверочный пример приоритетов P1–P4; конкретные переносы — задачи в самих
  споках (см. PR #244 и
  [project-structure-inheritance](../../standards/project-structure-inheritance.md)).
- Это **не** принятие новой 5-слойной модели как canonical. 5-слойная модель
  команды С разбирается как **proposal** и накладывается на действующее разделение
  Framework (L1–L2) / Methodology (L3–L4)
  ([AI_GOVERNANCE.md](../../AI_GOVERNANCE.md)).
- Это **не** новый фреймворк «BA Knowledge Object с нуля». BA Knowledge Object
  трактуется как **расширение** Knowledge Object из PR #242, а не как параллельная
  сущность.
- Это **не** обязательство внедрять все шесть методологий в каждом проекте.
  Влияние, Knowledge Graph и multi-agent governance явно отложены (см.
  приоритеты).
- Это **не** замена решений человека. Vision, publication, license, sensitive
  context и финальный выбор приоритетов остаются за Пользователем
  ([AI_GOVERNANCE.md](../../AI_GOVERNANCE.md), правило 4).

## Почему текущей ситуации недостаточно

Ключевой вывод аудита команды С: **Хаб сейчас строится преимущественно как
Knowledge Management Framework, а не как AI Transformation Framework**. Для
собственных исследований этого достаточно; для внешнего консалтинга и
коммерциализации репутационного инжиниринга — уже нет. При этом около **40 %**
того, что предлагает команда С, в Хабе уже есть, но разрозненно и без единой точки
входа для внешнего клиента (детальная карта — в разделе
[«Сравнение с существующими RFC»](#сравнение-с-существующими-rfc-242--243--244)).

| Вопрос | Ответ |
| --- | --- |
| Можно ли обойтись текущими RFC #242/#243/#244? | Для governance и knowledge-слоёв — да. Но они не покрывают **Analysis** (Opportunity Discovery, Enterprise Intelligence) и **Solution** (AI Solution Architecture) слои, нужные для прикладного консалтинга. |
| Почему нельзя просто принять все шесть методологий? | Без анализа зависимостей и рисков это нарушит Anti-Inflation: появятся пустые каталоги и «методологии впрок». Часть (Influence/Knowledge Graph) сейчас не нужна ни одному проекту. |
| Что ломается без этого RFC? | Каждая из шести методологий заходит в экосистему по-своему, дублирует уже существующие модели (Knowledge Object, archetypes, lifecycle) и теряет traceability к источникам. |
| Почему три отдельных предложения, а не одно? | Хаб, Mango и Open-AI — три разных архетипа (PR #243) с разными primary value artifacts и разными рисками. Универсальная «одна структура» противоречит таксономии архетипов. |
| Почему именно сейчас? | Задача #245 зависит от уже влитых PR #242/#243/#244 (Depends On). Их модели — основа, на которую методологии должны лечь без дублирования. Это окно консолидации. |

Вывод: нужен синтез, который (а) свяжет уже существующие 40 % в одну
методологическую рамку с точкой входа, (б) проанализирует недостающие методологии
прежде чем создавать под них артефакты, и (в) выдаст три согласованных, но
независимых плана развития. Именно это и есть граница данного RFC.

## Карта методологий и 5-слойная модель

### 5-слойная модель как proposal

Команда С предлагает смотреть на экосистему через пять слоёв. Это **новое
предложение**, его нет в репозитории; ниже оно накладывается на действующее
разделение Framework / Methodology.

| Слой команды С | Что описывает | Методологии команды С | Отображение на текущую модель Хаба |
| --- | --- | --- | --- |
| **1. Governance** | Правила, роли, режимы, lifecycle, контракты. | (сквозной слой) | Methodology **L3–L4**: `AI_GOVERNANCE.md`, `governance/`, `standards/`. **Сильный.** |
| **2. Knowledge** | Источники, доверие, память исследований, traceability. | Trust & Evidence | Methodology **L3–L4**: PR #242 (Research Memory), `research/external-knowledge/`. **Сильный, но без явной шкалы доверия.** |
| **3. Analysis** | Понять предприятие и найти возможности для AI. | Enterprise Intelligence, Opportunity Discovery | **Фрагментарно.** Нет артефактов для разбора процессов клиента и поиска ROI-возможностей. |
| **4. Solution** | Спроектировать AI-решение под возможность. | AI Solution Architecture, Human-AI Collaboration | **Фрагментарно.** Есть archetypes (PR #243) и Operating Modes, но нет шаблона «архитектура одного AI-решения». |
| **5. Product** | Каталог продуктов/процессов как предметная область. | Influence & Network Analysis (как один из доменов) | **Сильный для Mango:** Product Layer (`research/mango/2026-05-22-classification.md`). |

> 🧭 **Принцип отображения.** 5-слойная модель — это **аналитическая линза над
> существующим разделением**, а не замена ему. Governance и Knowledge — уже
> сильные слои Хаба (L3–L4). Главный разрыв экосистемы — слои **Analysis** и
> **Solution**: именно туда нацелены недостающие методологии.

### Консалтинговый конвейер

Шесть методологий складываются не в плоский список, а в конвейер внешнего
консалтинга. Это объясняет их зависимости и приоритеты:

```
Enterprise Intelligence  →  Opportunity Discovery  →  AI Solution Architecture  →  Implementation  →  Trust & Evidence
   (понять предприятие)       (найти возможность)         (спроектировать)          (внедрить)         (доказать ценность)
        Analysis                   Analysis                   Solution              Product/Runtime        Knowledge
```

- **Human-AI Collaboration** — сквозная: определяет, кто (человек/агент)
  отвечает за каждый шаг конвейера.
- **Influence & Network Analysis** — это **отдельный продуктовый домен**
  (репутационный инжиниринг), а не звено основного конвейера. Поэтому он
  приоритизируется ниже и отложен для Mango.

## Анализ шести методологий

Для каждой методологии: назначение и цепочка, минимум три внешних источника
(зарегистрированы в
[external-sources-registry.md](../../research/external-knowledge/external-sources-registry.md),
`ext-025`..`ext-048`; повторно используются `ext-001`, `ext-005`, `ext-008`),
сильные и слабые стороны, риски внедрения, зависимости и вывод с приоритетом.

> ⚠️ **Оговорка по источникам.** Часть первоисточников (McKinsey, Cisco, Gartner,
> HTML-лендинги OpenAI) отдаёт 403/таймаут для ботов. Там, где это так, в анализе
> используется каноническая/CDN/DOI-альтернатива, а ограничение отмечено инлайн.
> Ссылки сознательно не скрапятся (Anti-Inflation).

### 1. Enterprise Intelligence Methodology

**Назначение.** Систематически понять предприятие до проектирования AI:
бизнес-процессы (BPM) + корпоративная архитектура (Enterprise Architecture) +
готовность к AI (AI Readiness). Цепочка: `Процессы → Архитектура → Готовность`.

| # | Источник | Тип | Релевантность |
| --- | --- | --- | --- |
| `ext-025` | [OMG BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2/About-BPMN) | standard | Каноническая нотация моделирования бизнес-процессов; основа для разбора процессов клиента. |
| `ext-026` | [The Open Group TOGAF](https://www.opengroup.org/togaf) | standard | Зрелый метод Enterprise Architecture (ADM-цикл, слои business/data/application/technology). |
| `ext-027` | [The Open Group ArchiMate](https://www.opengroup.org/archimate-forum/archimate-overview) | standard | Язык моделирования EA; связывает бизнес-слой с приложениями и технологиями. |
| `ext-028` | [Oxford Insights — Government AI Readiness Index 2025](https://oxfordinsights.com/ai-readiness/government-ai-readiness-index-2025/) | docs | Публичная, воспроизводимая методика оценки готовности к AI по измеримым осям. |
| `ext-029` | [Microsoft — Agentic AI adoption maturity model](https://learn.microsoft.com/en-us/agents/adoption-maturity-model/) | docs | Модель зрелости внедрения agentic AI; шкала готовности на уровне организации. |

- **Сильные стороны.** Стандарты зрелые, проверенные индустрией и совместимые
  между собой (BPMN моделирует процесс, ArchiMate/TOGAF — контекст, AI Readiness —
  готовность). Дают общий язык с корпоративным клиентом.
- **Слабые стороны.** TOGAF/ArchiMate тяжеловесны; полное внедрение избыточно для
  малых проектов и противоречит Anti-Inflation. AI Readiness Index создавался для
  государств — нужна адаптация под предприятие.
- **Риски внедрения.** Соблазн «корпоративной бюрократии»: моделировать всё
  предприятие вместо одного процесса под конкретную задачу. Риск отрыва от
  Product Layer Mango (дублирование таксономии).
- **Зависимости.** Питает Opportunity Discovery (процессы → точки боли). Использует
  нотацию BPMN, общую с AI Solution Architecture (§ Workflow).
- **Вывод.** Подтверждаем **как лёгкий профиль**: один-два процесса в BPMN-стиле +
  чек-лист AI Readiness, без полного TOGAF. Приоритет для Хаба — средний (методичка
  консалтинга), для Mango/Open-AI — низкий сейчас.

### 2. Opportunity Discovery Framework

**Назначение.** Превратить понимание предприятия в приоритизированные возможности
для AI. Цепочка: `Процесс → Точка боли → AI-возможность → ROI`.

| # | Источник | Тип | Релевантность |
| --- | --- | --- | --- |
| `ext-030` | [Teresa Torres — Opportunity Solution Trees](https://www.producttalk.org/opportunity-solution-trees/) | blog | Структура «desired outcome → opportunities → solutions → experiments»; прямой аналог цепочки. |
| `ext-031` | [Strategyn — Jobs-to-be-Done / Outcome-Driven Innovation](https://strategyn.com/jobs-to-be-done/) | docs | Перевод «боли» в измеримые desired outcomes; основа для ROI-оценки. |
| `ext-032` | [Eric Ries — The Lean Startup: Principles](https://theleanstartup.com/principles) | docs | Validated learning: проверять возможность дёшево до полноценной разработки. |
| `ext-033` | [McKinsey — Economic Potential of Generative AI](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier) | docs | Каталог зон ценности GenAI по функциям; ориентир для ROI (бот-блок: цитируется как ориентир). |
| `ext-034` | [Product School — Impact / Effort Matrix](https://productschool.com/blog/product-fundamentals/impact-effort-matrix) | blog | Простой инструмент приоритизации возможностей impact × effort. |

- **Сильные стороны.** Дисциплина «не строить решение без подтверждённой
  возможности и ROI». Прямо ложится на роль BA и на Lean-подход экосистемы.
- **Слабые стороны.** ROI для AI-проектов трудно измерить заранее; риск
  псевдо-точных цифр. JTBD требует доступа к пользователям клиента, которого у
  консультанта может не быть.
- **Риски внедрения.** «Opportunity theatre»: красивые деревья без проверки.
  Митигируется привязкой к Trust & Evidence (каждая оценка ROI — с уровнем
  доверия E0–E4).
- **Зависимости.** Вход — из Enterprise Intelligence. Выход — в AI Solution
  Architecture (возможность → решение). Опирается на Trust & Evidence для оценок.
- **Вывод.** Подтверждаем. Для Mango — **приоритет P2** (после Trust & Evidence):
  каталог типовых BA-возможностей. Для Хаба — методичка «от процесса к
  возможности». Реализуется как шаблон, не как тяжёлый процесс.

### 3. Human-AI Collaboration Model

**Назначение.** Описать распределение ответственности человек ↔ агент ↔
инструменты ↔ знания. Цепочка: `Human → Agent → Tool → Knowledge`.

| # | Источник | Тип | Релевантность |
| --- | --- | --- | --- |
| `ext-001` | [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) | blog | Паттерны workflow vs agent, уровни автономии (повторное использование). |
| `ext-005` | [OpenAI — A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | paper | Guardrails и human-in-the-loop как явные контракты (повторное использование). |
| `ext-035` | [Parasuraman, Sheridan & Wickens — Types and Levels of Human Interaction with Automation (IEEE 2000, DOI 10.1109/3468.844354)](https://dblp.org/rec/journals/tsmc/ParasuramanSW00.html) | paper | Классическая 10-уровневая шкала автоматизации; академическая база для уровней автономии. |
| `ext-036` | [Vats et al. — Survey on Human-AI Collaboration with LFMs (arXiv:2403.04931)](https://arxiv.org/abs/2403.04931) | paper | Современный обзор паттернов взаимодействия человек–LLM. |
| `ext-037` | [Anthropic — Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) | docs | Стандарт связи агента с инструментами и источниками знаний (Tool/Knowledge). |

- **Сильные стороны.** Совпадает с **Operating Modes** Хаба (Structured / Creative
  / Research / Education) и правилом эскалации к человеку. Академически обоснована
  (Parasuraman). 40 %-перекрытие с уже существующим.
- **Слабые стороны.** Модель `Human → Agent → Tool → Knowledge` слишком линейна;
  реальное взаимодействие — цикл с обратными связями и памятью (см. дополнение
  фаундера `Human → Agent → (Tool/Knowledge/Memory) → Result → Human`).
- **Риски внедрения.** Формализм без операционных последствий. Митигируется
  привязкой уровней автономии к конкретным режимам и DoD.
- **Зависимости.** Сквозная для всего конвейера. Уровни автономии — это секция 3
  (Agent Role) шаблона AI Solution Architecture.
- **Вывод.** Подтверждаем **как формализацию уже существующего**, а не как новый
  механизм. Достаточно явно описать три уровня автономии (full-auto /
  needs-confirmation / recommendation-only) и связать их с Operating Modes.
  Приоритет — низкий-средний (документирование, не строительство).

### 4. Trust & Evidence Framework

**Назначение.** Связать утверждение с доказательной базой и уровнем уверенности.
Цепочка: `Source → Evidence → Claim → Conclusion → Confidence`; шкала **E0–E4**.

| # | Источник | Тип | Релевантность |
| --- | --- | --- | --- |
| `ext-038` | [OCEBM — Oxford Levels of Evidence (2009)](https://www.cebm.ox.ac.uk/resources/levels-of-evidence/oxford-centre-for-evidence-based-medicine-levels-of-evidence-march-2009) | standard | Иерархия уровней доказательности; почти 1:1 отображается на E0–E4. |
| `ext-039` | [GRADE Working Group](https://www.gradeworkinggroup.org/) | docs | Оценка certainty of evidence (high/moderate/low/very low) — модель для confidence. |
| `ext-040` | [W3C — PROV Data Model (PROV-DM)](https://www.w3.org/TR/prov-dm/) | standard | Стандарт provenance: Entity → Activity → Agent; основа traceability source→claim. |
| `ext-041` | [Stanford Encyclopedia of Philosophy — Argument (Toulmin model)](https://plato.stanford.edu/entries/argument/) | paper | Модель аргумента claim/grounds/warrant; структура «source → evidence → claim». |

- **Сильные стороны.** Закрывает прямой разрыв: в Хабе есть Knowledge Status
  (`Observed`/`Candidate`/`Applied`/…) и Verdict Rules (PR #242 §6), но **нет явной
  шкалы силы доказательства**. E0–E4 — её недостающая ось. Опирается на зрелые
  стандарты (OCEBM, GRADE, PROV).
- **Слабые стороны.** Риск смешать E0–E4 (сила доказательства) с двумя другими
  осями: Knowledge Status (стадия жизненного цикла) и mango L0–L5 (зрелость
  capability). Нужна явная ортогональность.
- **Риски внедрения.** Формальная простановка E-уровней «для галочки» без реальной
  проверки источника. Митигируется привязкой к source intelligence критериям
  PR #242.
- **Зависимости.** Базовый слой для Opportunity Discovery (доверие к ROI),
  AI Solution Architecture (секция 4, trust level источников) и всей Knowledge.
- **Вывод.** Подтверждаем как **первый приоритет**. E0–E4 вводится как новая
  **ось доверия**, ортогональная Knowledge Status и mango L0–L5 (таблица в разделе
  [«Подтверждение … фаундера»](#подтверждение-и-расширение-предложения-фаундера)).
  Для Mango — **P1** вместе с BA Knowledge Object.

### 5. Influence & Network Analysis

**Назначение.** Анализ сущностей, связей, влияния, нарратива и репутации.
Цепочка: `Entity → Relation → Influence → Narrative → Reputation`. Прикладная
область — репутационный инжиниринг.

| # | Источник | Тип | Релевантность |
| --- | --- | --- | --- |
| `ext-042` | [Wasserman & Faust — Social Network Analysis](https://www.cambridge.org/core/books/social-network-analysis/90030086891EB3491D096034684EFFB8) | paper | Каноническая основа SNA: сущности, связи, метрики. |
| `ext-043` | [Freeman — Centrality in Social Networks (1978)](https://www.bebr.ufl.edu/sites/default/files/Centrality%20in%20Social%20Networks.pdf) | paper | Метрики влияния: degree / betweenness / closeness centrality. |
| `ext-044` | [Brin & Page — Anatomy of a Large-Scale Hypertextual Web Search Engine (PageRank)](https://snap.stanford.edu/class/cs224w-readings/Brin98Anatomy.pdf) | paper | Алгоритмическая модель влияния/ранжирования в графе. |
| `ext-045` | [Hogan et al. — Knowledge Graphs (ACM CSUR, DOI 10.1145/3447772)](https://doi.org/10.1145/3447772) | paper | Модель «сущности + связи + provenance»; мост к Trust & Evidence. |

- **Сильные стороны.** Зрелый математический аппарат (centrality, PageRank,
  knowledge graphs). Knowledge Graph-модель естественно соединяется с Trust &
  Evidence через provenance.
- **Слабые стороны.** Требует данных и инфраструктуры (граф, сбор связей), которых
  нет ни у одного проекта сейчас. Этические/правовые риски при анализе персон.
- **Риски внедрения.** Высокие: сбор данных о людях затрагивает hard-ban
  AI_GOVERNANCE (private data, sensitive context — решение за человеком). Строить
  впрок = прямое нарушение Anti-Inflation.
- **Зависимости.** Опирается на Trust & Evidence (provenance связей). Это
  **продуктовый домен**, а не звено основного конвейера.
- **Вывод.** **Отложить.** Регистрируем источники как наблюдение (`observation`),
  фиксируем как будущий домен. Ни для Хаба, ни для Mango, ни для Open-AI сейчас не
  внедряется. Любое применение к персонам — только после явного решения человека.

### 6. AI Solution Architecture

**Назначение.** «BPMN для AI»: единый язык описания одного AI-решения. Цепочка:
`Problem → Workflow → Agent Role → Knowledge Sources → Tools → Memory → Governance`.

| # | Источник | Тип | Релевантность |
| --- | --- | --- | --- |
| `ext-001` | [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) | blog | Паттерны и компоненты агентов (повторное использование). |
| `ext-005` | [OpenAI — A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | paper | Сквозная структура агентного решения (повторное использование). |
| `ext-046` | [Lewis et al. — Retrieval-Augmented Generation (arXiv:2005.11401)](https://arxiv.org/abs/2005.11401) | paper | Каноническая модель Knowledge Sources (секция 4 шаблона). |
| `ext-047` | [Yao et al. — ReAct: Reasoning + Acting (arXiv:2210.03629)](https://arxiv.org/abs/2210.03629) | paper | Цикл reasoning/tool-use — основа секций Workflow и Tools. |
| `ext-048` | [AWS — Well-Architected Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html) | standard | Референс-архитектура GenAI: governance, надёжность, безопасность. |

- **Сильные стороны.** Семь секций (Problem/Workflow/Agent/Knowledge/Tools/Memory/
  Governance) исчерпывающе описывают AI-решение и совпадают с индустриальными
  компонентами (RAG, ReAct, MCP, Well-Architected). 40 %-перекрытие: archetypes
  (PR #243) и Project Template уже задают часть.
- **Слабые стороны.** Семь секций для простого промпта избыточны — нужен
  «lite»-профиль. Память (секция 6) в Хабе пока проработана только как context
  engineering (`ext-008`), не как стандарт.
- **Риски внедрения.** Шаблон ради шаблона. Митигируется тем, что секции прямо
  ссылаются на уже существующие механизмы (Workflow → Product Layer; Knowledge →
  Trust E0–E4; Governance → lifecycle + Knowledge Status).
- **Зависимости.** Финальный артефакт конвейера: потребляет Opportunity Discovery
  (вход — Problem), Trust & Evidence (секция 4), Human-AI Collaboration (секция 3),
  Product Layer (секция 2).
- **Вывод.** Подтверждаем шаблон фаундера из семи секций как **целевой Hub
  template** с lite/full-профилями. Для Mango — **P3** (после Trust & Evidence и
  Opportunity Discovery). Детали — в разделе подтверждения фаундера.

### Сводка приоритетов методологий

| Методология | Слой | Перекрытие с Хабом | Приоритет (экосистема) | Решение |
| --- | --- | --- | --- | --- |
| Trust & Evidence | Knowledge | Высокое (PR #242) | **P1** | Подтвердить, ввести ось E0–E4. |
| AI Solution Architecture | Solution | Среднее (PR #243) | **P3** (Mango), средний (Hub) | Подтвердить шаблон 7 секций. |
| Opportunity Discovery | Analysis | Низкое | **P2** | Подтвердить как шаблон. |
| Human-AI Collaboration | сквозной | Высокое (Operating Modes) | низкий-средний | Документировать уровни автономии. |
| Enterprise Intelligence | Analysis | Низкое | средний (Hub) | Лёгкий профиль, без полного TOGAF. |
| Influence & Network Analysis | Product (домен) | Нет | **отложить** | Зафиксировать как будущий домен. |

## Сравнение с существующими RFC (#242 / #243 / #244)

### Карта «уже существует / разрыв»

Подтверждение тезиса «≈40 % уже есть, но разрозненно»:

| Что предлагает команда С | Где уже есть в Хабе | Чего не хватает |
| --- | --- | --- |
| Trust & Evidence (E0–E4) | PR #242: Knowledge Status + Verdict Rules (§6); `source_intelligence` | Явной **шкалы силы доказательства** как отдельной оси. |
| AI Solution Architecture | PR #243: archetypes + Project Template; Operating Modes | Шаблона **одного AI-решения** (7 секций) как артефакта. |
| BA Knowledge Object | PR #242: Knowledge Object (§7), поля и статусы | **BA-специализации** объекта (привязка к BA-процессу/возможности). |
| Human-AI Collaboration | `AI_GOVERNANCE.md`: Operating Modes, эскалация | Явных **уровней автономии** в терминах решения. |
| Opportunity Discovery | — | Полностью (новый артефакт). |
| Enterprise Intelligence | — | Полностью (лёгкий профиль). |

Главный разрыв — не в отдельных кирпичах, а в том, что они **не связаны в одну
методологию с точкой входа для внешнего клиента**. Этот RFC задаёт связь; сами
артефакты создаются отдельными задачами.

### PR #242 — Research Memory & Source Intelligence

| Аспект | Решение |
| --- | --- |
| **Переиспользовать** | Модель Knowledge Object (поля `object_id`, `statement`, `status`, `source_refs`, `source_intelligence`, `verdict`, `consumers`, `linked_decisions`, `review_rule`); пять статусов; Verdict Rules (§6); traceability-схему. |
| **Расширить** | **BA Knowledge Object** = Knowledge Object + поля BA-контекста: `ba_process` (узел BA-классификации), `opportunity_ref`, `evidence_level` (E0–E4). Это **специализация**, не новая сущность. |
| **Затрагиваемые Open Decisions** | (1) external-insights/ vs отдельный research-memory/ каталог — BA Knowledge Object живёт там же, где Knowledge Object; (2) `Applied` глобально vs consumer-specific — BA-объекты усиливают аргумент за consumer-specific (один объект применим в Mango, но не в Open-AI); (3) нужен ли отдельный валидатор — да, при появлении поля `evidence_level` валидатор E0–E4 становится оправданным. |

### PR #243 — Repository Archetypes, Project Template & Release

| Аспект | Решение |
| --- | --- |
| **Переиспользовать** | Четыре архетипа и правило классификации по primary value artifact; Project Template для Prompt & Pattern Library; правило Governance sync (Base + Local Extension); GitHub Flow + trunk discipline. |
| **Расширить** | Шаблон AI Solution Architecture (7 секций) дополняет Project Template на уровне **одного решения** (template описывает репозиторий, AI Solution Architecture — одно AI-решение внутри него). Возможен новый под-профиль **Public Methodology Portal** для Open-AI (см. Open Decisions). |
| **Затрагиваемые Open Decisions** | (1) повышать ли RFC в standard/template — для AI Solution Architecture: да, при первом применении в Mango; (2) создавать ли `templates/prompt-pattern-library/` до миграции — методологии не меняют этот ответ; (3) нужен ли новый архетип для публичного портала Open-AI. |

### PR #244 — Mango Migration Plan

| Аспект | Решение |
| --- | --- |
| **Переиспользовать** | Product Layer таксономию (`Семейство → Класс → Подкласс → Функция`); mango статусы (`Есть`/`Частично`/`Не выявлено`/`Вне SaaS-ядра`); L0–L5 capability maturity; правила именования (`lowercase-with-hyphens`, `snake_case` для параметров). |
| **Расширить / согласовать** | Классификация **BA-процессов** фаундера повторно использует ту же 4-уровневую форму Product Layer, что и продуктовый каталог Mango. Trust & Evidence (E0–E4) добавляется к prompt-объектам Mango. Приоритеты P1–P4 встраиваются в план миграции, не переписывая его. |
| **Затрагиваемые Open Decisions** | Порядок миграции в Mango должен учесть, что **Trust & Evidence + BA Knowledge Object (P1)** идут раньше, чем перенос промптов под AI Solution Architecture (P3). |

## Подтверждение и расширение предложения фаундера

Предложение фаундера (Часть 3 issue #245) **подтверждается** и согласуется с уже
существующими моделями. Ниже — что принимается и чем дополняется.

### D.1 Классификация BA-процессов (Product Layer)

Фаундер предлагает классифицировать BA-процессы как Product Layer с семейством
`Business Analysis Processes`. Подтверждаем и согласуем с **тем же 4-уровневым
скелетом**, что уже используется в продуктовом каталоге Mango
(`Семейство → Класс → Подкласс → Функция`, `research/mango/2026-05-22-classification.md`):

| Уровень | Значение фаундера | Пример |
| --- | --- | --- |
| Семейство (Domain) | Business Analysis Processes | — |
| Класс (Capability) | 1. Requirements Engineering · 2. Integration Design · 3. Stakeholder Communication · 4. Quality Assurance | Класс 1 |
| Подкласс (Feature) | 1.1 Elicitation · 1.2 Analysis · 1.3 Validation; 2.1 System Analysis · 2.2 Solution Design · 2.3 Documentation; 3.1 Clarification · 3.2 Presentation; 4.1 Verification · 4.2 Traceability | Подкласс 1.1 |
| Функция (Atomic Function) | Конкретные действия | «Анализ документации заказчика», «Маппинг полей» |

**Дополнение (согласование, не изобретение):** в Mango теперь сосуществуют **две
ветки Product Layer одной формы** — продуктовый каталог (что Mango умеет как
продукт) и BA-процессы (как BA работает). Чтобы не смешивать «процесс» и
«мыслительную операцию», вводится **ортогональная ось Cognitive Operations** как
тег, а не как уровень иерархии. Тогда любой prompt-объект Mango описывается тройкой:

```
(BA-процесс: 1.1 Elicitation) × (Cognitive Operation: extraction) × (целевой продукт-узел)
```

Это переиспользует Product Layer, не плодит новую иерархию и держит BA-процессы и
когнитивные операции раздельно.

### D.2 Шаблон AI Solution Architecture (7 секций)

Подтверждаем семь секций как целевой Hub template. Каждая секция **привязывается к
уже существующему механизму** Хаба — это и есть «не изобретать заново»:

| # | Секция | Содержимое (фаундер) | Привязка к существующему |
| --- | --- | --- | --- |
| 1 | **Problem** | Бизнес-проблема, контекст, ограничения, критерии успеха. | Вход из Opportunity Discovery; критерии успеха ← ROI-оценка. |
| 2 | **Workflow** | Принадлежность Product Layer, когнитивные операции, шаги, точки решений. | **Product Layer Mango** + ось Cognitive Operations (D.1); нотация BPMN (`ext-025`). |
| 3 | **Agent Role** | Тип промпта (simple/system/RAG/agentic); автономия (full-auto / needs-confirmation / recommendation-only). | **Operating Modes** + Human-AI Collaboration (уровни автономии). |
| 4 | **Knowledge Sources** | PDF/web/vector/API/history + уровень доверия. | **Trust & Evidence E0–E4** + Knowledge Object (PR #242). |
| 5 | **Tools** | RAG / Re-RAG / Python / MCP / валидаторы. | `ext-046` (RAG), `ext-037` (MCP), существующие `tools/`. |
| 6 | **Memory** | session / episodic / semantic + caching / compression / selective load. | Context engineering (`ext-008`); пока **lite**, без отдельного стандарта. |
| 7 | **Governance** | Lifecycle, Knowledge Status, Trust & Evidence, Human-AI Collaboration, ADR. | **AI_GOVERNANCE.md** + lifecycle + PR #242. |

**Профили.** Вводим два профиля во избежание избыточности: **lite** (секции 1–3 +
7) для простого промпта и **full** (все 7) для агентного решения. Это снимает риск
«семь секций ради одного промпта».

### D.3 Trust & Evidence (E0–E4) и три ортогональные оси

Подтверждаем шкалу E0–E4 и явно разводим её с двумя другими осями, чтобы избежать
смешения (главный риск методологии 4):

| Ось | Что измеряет | Значения | Источник |
| --- | --- | --- | --- |
| **Evidence (E0–E4)** | Силу доказательства утверждения. | E0 мнение · E1 один источник · E2 несколько источников · E3 подтверждённый факт · E4 воспроизводимый факт | команда С + OCEBM (`ext-038`) |
| **Knowledge Status** | Стадию жизненного цикла знания. | Observed · Candidate · Applied · Rejected · Superseded | PR #242 |
| **Capability Maturity (L0–L5)** | Зрелость capability продукта. | L0 Raw … L5 Managed | `research/mango/2026-05-26-taxonomy-concept.md` |

> 🧭 Оси **ортогональны**: знание может быть `Applied` (статус) с доказательством
> `E2` (несколько источников) для capability уровня `L4`. Смешивать их в одно поле
> запрещено. E0–E4 маппится на Verdict Rules PR #242: `verdict` усиливается
> доказательным уровнем, но не заменяет его.

### D.4 Модель Human → Agent → (Tool / Knowledge / Memory) → Result → Human

Подтверждаем дополнение фаундера к линейной модели команды С: реальное
взаимодействие — **цикл с памятью и возвратом к человеку**, а не линейная цепочка.
Это согласуется с правилом эскалации AI_GOVERNANCE (человек принимает финальные
решения) и с секциями 3/6/7 шаблона. Различение фаундера **Components vs
Architecture vs Governance** принимается как поясняющая рамка:

| Уровень | Вопрос | Пример артефакта |
| --- | --- | --- |
| **Components** | Из чего собрано? | RAG, MCP-tool, vector store, валидатор. |
| **Architecture** | Как собрано под задачу? | Шаблон AI Solution Architecture (7 секций). |
| **Governance** | По каким правилам живёт? | AI_GOVERNANCE, lifecycle, Trust & Evidence. |

## Три независимых предложения

Три предложения **независимы** (каждое самодостаточно для своего проекта и
архетипа), но **согласованы** общим методологическим хребтом: Knowledge Object →
Trust & Evidence → AI Solution Architecture → lifecycle. L3 = детализация
(артефакты, директории, шаблоны); L4 = реализация (конкретные файлы, содержимое,
примеры, валидаторы). Все целевые артефакты создаются **пофазно под реальную боль**
(Anti-Inflation), а не этим PR.

### E.1 Хаб (hybrid-Intelligence-lab) — Governance & Knowledge Hub

**Роль:** методологический центр. Хаб владеет универсальными определениями
методологий и шаблонами, споки их наследуют.

**Какие методологии:** Trust & Evidence (ось E0–E4), AI Solution Architecture
(шаблон), Human-AI Collaboration (уровни автономии), Enterprise Intelligence и
Opportunity Discovery (лёгкие методички). Influence — только реестр источников.

**Какие RFC создавать (последовательность):**
1. `trust-and-evidence-framework.md` — ось E0–E4 + маппинг на PR #242.
2. `ai-solution-architecture-template.md` — 7 секций, lite/full.
3. `ba-process-classification.md` — согласование с Product Layer (для Mango).
4. (позже) `opportunity-discovery-method.md`, `enterprise-intelligence-profile.md`.

| Уровень | Содержание |
| --- | --- |
| **L3 (детализация)** | Артефакты: ось E0–E4 в `standards/`; целевой шаблон `templates/ai-solution-architecture/`; раздел уровней автономии в `AI_GOVERNANCE.md` или `standards/`. Директории: переиспользовать `governance/rfc/`, `standards/`, `templates/` — **без новых пустых каталогов**. Шаблоны документов: единый frontmatter (4 поля), kebab-case, ISO-даты. |
| **L4 (реализация)** | Конкретные файлы: `standards/trust-and-evidence.md` (таблица E0–E4 + критерии перехода + примеры); `templates/ai-solution-architecture/template.md` (7 секций с плейсхолдерами) + `example-*.md` (заполненный пример). Валидаторы: расширить `tools/validate-frontmatter.sh`; опциональный `tools/validate-evidence-level.sh` (проверка значения из {E0..E4}). Регистрация источников `ext-025..048` (этот PR). |

### E.2 Mango (mango_ba_prompts) — Prompt & Pattern Library

**Роль:** прикладная библиотека BA-промптов. Наследует методологии из Хаба,
применяет к 23 промптам.

**Какие методологии и приоритеты (коррекция фаундера):**

| Приоритет | Методология | Что делает в Mango |
| --- | --- | --- |
| **P1** | Trust & Evidence + BA Knowledge Object | Каждый prompt-объект получает `evidence_level` (E0–E4) и BA-контекст. |
| **P2** | Opportunity Discovery | Каталог типовых BA-возможностей (process → pain → opportunity). |
| **P3** | AI Solution Architecture | 23 промпта описываются шаблоном (lite-профиль для большинства). |
| **P4** | Agent Workflow Catalog | Типовые workflow BA-агента. |
| **Не сейчас** | Knowledge Graph, Influence, Advanced Memory, Multi-Agent Governance | Отложено. |

| Уровень | Содержание |
| --- | --- |
| **L3 (детализация)** | Артефакты: BA Knowledge Object schema (расширение PR #242); BA-классификация (`Business Analysis Processes` в Product Layer); поле `evidence_level` в метаданных промптов. Директории: переиспользовать существующие `prompts/`, `patterns/`, `docs/`, `standards/` (PR #243) — без новых. Шаблоны: AI Solution Architecture lite для промпта. |
| **L4 (реализация)** | Конкретные файлы: `docs/ba-processes/` (узлы классификации, индекс уже есть); `standards/ba-knowledge-object.md` (поля + пример заполнения на реальном промпте); добавить `evidence_level`/`ba_process` во frontmatter промптов. Примеры: один промпт целиком по шаблону AI Solution Architecture. Валидаторы: расширить существующие `validate_*` скрипты Mango на новые поля. Источники — через Local Extension реестр Mango при специфичности. |

### E.3 Open-AI (open-ai.ru) — Product Spoke / Public Portal

**Роль:** прикладной/публичный проект. Здесь методология становится **продуктом
для внешнего клиента** (точка входа, которой не хватает).

**Какие методологии:** Enterprise Intelligence + Opportunity Discovery (как
консалтинговая услуга), AI Solution Architecture (как deliverable клиенту), Trust &
Evidence (как доказательство ценности). Influence/репутационный инжиниринг — как
**будущий продуктовый домен**, только после решения человека по sensitive context.

| Уровень | Содержание |
| --- | --- |
| **L3 (детализация)** | Артефакты: публичная точка входа «методология консалтинга» (конвейер EI → OD → ASA → Trust); классификация архетипа (Product Spoke или новый Public Methodology Portal — Open Decision). Директории: по архетипу Product Spoke (PR #243) — `src/`, `docs/`, `infra/` под реальный runtime; без cloud-инфраструктуры до появления рантайма. Шаблоны: client-facing версия AI Solution Architecture. |
| **L4 (реализация)** | Конкретные файлы: `docs/methodology/` (публичное изложение конвейера, ссылается на Hub RFC как источник истины); landing/портал — только при реальном serverless MVP. Примеры: один сквозной кейс «процесс клиента → возможность → AI-решение → доказанная ценность». Валидаторы: наследуются из Хаба (Governance sync). Репутационный инжиниринг — **не реализуется**, фиксируется как backlog. |

> 🔗 **Независимость ≠ изоляция.** Три предложения не ссылаются друг на друга
> механически: Mango и Open-AI наследуют **определения** из Хаба (Base Governance),
> но имеют собственные backlog и решения (Local Extension, PR #243). Хаб не знает о
> внутренних артефактах споков — это сохраняет правило «repo-wide standard не
> ссылается на project standard»
> ([project-structure-inheritance](../../standards/project-structure-inheritance.md)).

## Консистентность и переиспользование для будущих проектов

Чтобы методологии работали и для пятого, и для десятого проекта экосистемы,
разделяем **универсальный скелет** и **специфичное наполнение**:

| Элемент | Универсальный (Hub-owned) | Специфичный (проект) |
| --- | --- | --- |
| Ось доверия | E0–E4 (определение, критерии) | Какие источники у проекта получают какой E-уровень. |
| Knowledge Object | Базовая схема (PR #242) | BA Knowledge Object, prompt-объект — специализации. |
| AI Solution Architecture | Шаблон 7 секций, lite/full | Конкретные заполненные решения проекта. |
| Product Layer | 4-уровневая форма `Семейство→Класс→Подкласс→Функция` | Домены: voice-ucaas (Mango), Business Analysis Processes и т.д. |
| Lifecycle | Observation → … → Framework → Archive | Конкретные документы проекта на стадиях. |
| Уровни автономии | full-auto / needs-confirmation / recommendation-only | Какие роли в проекте на каком уровне. |
| Archetype | 4 архетипа + правило классификации (PR #243) | Конкретный архетип проекта. |

**Правило переиспользования (для нового проекта):**
1. Определить архетип (PR #243) → взять скелет директорий.
2. Унаследовать Base Governance из Хаба (Smart Sync).
3. Подключить универсальные методологии **под реальную боль**, не впрок.
4. Специализировать Knowledge Object и Product Layer под домен проекта.
5. Применять AI Solution Architecture lite, повышая до full по необходимости.

Это даёт консистентность (общий язык, общие оси, общие шаблоны) без потери
независимости (каждый проект — свой архетип, свой домен, свой backlog) и без
нарушения Anti-Inflation.

## Acceptance Criteria

- Раздел «Почему текущей ситуации недостаточно» добавлен.
- Исследованы все шесть методологий; на каждую — ≥3 проверенных внешних источника
  (`ext-025`..`ext-048`, плюс повторно используемые `ext-001`/`ext-005`/`ext-008`),
  с разбором сильных/слабых сторон, рисков внедрения и зависимостей.
- Найдены противоречия и дополнения относительно существующих RFC (#242/#243/#244)
  с явным указанием, что переиспользовать и что расширить.
- 5-слойная модель команды С разобрана как proposal и отображена на действующее
  разделение Framework (L1–L2) / Methodology (L3–L4).
- Предложение фаундера (BA-классификация + шаблон AI Solution Architecture из 7
  секций + Human-AI модель + E0–E4) подтверждено и согласовано с существующими
  моделями без изобретения заново.
- E0–E4 введена как ось доверия, ортогональная Knowledge Status и mango L0–L5.
- Сформированы три независимых, но согласованных предложения (Хаб / Mango /
  Open-AI), каждое с уровнями L3 и L4.
- Определена модель консистентности и переиспользования (универсальный скелет vs
  специфика) для будущих проектов.
- Соблюдены Anti-Inflation (целевые артефакты — пофазно, без пустых каталогов),
  kebab-case, полные пути и frontmatter-стандарт.

## Open Decisions

1. **Принять ли 5-слойную модель** (Governance/Knowledge/Analysis/Solution/Product)
   как официальную линзу над Framework/Methodology, или оставить только как
   аналитический инструмент этого RFC?
2. **Повышать ли Trust & Evidence (E0–E4) до canonical standard** сразу, или после
   первого применения в Mango (P1)?
3. **Куда поместить шаблон AI Solution Architecture** — в `templates/` Хаба как
   универсальный, и в какой момент его делегировать из RFC в active template?
4. **BA Knowledge Object** — формализовать как расширение Knowledge Object PR #242
   (предлагается) или как отдельный документ? Это затрагивает Open Decision PR #242
   про `Applied` global vs consumer-specific.
5. **Нужен ли новый архетип Public Methodology Portal** для Open-AI, или достаточно
   Product Spoke (PR #243)?
6. **Порядок методологических RFC Хаба** — подтвердить последовательность
   (Trust & Evidence → AI Solution Architecture → BA classification → Opportunity
   Discovery → Enterprise Intelligence)?
7. **Influence & Network Analysis** — подтвердить отсрочку и условие активации
   (явное решение человека по sensitive context, наличие проекта-потребителя)?

## Источники

Все источники зарегистрированы в
[external-sources-registry.md](../../research/external-knowledge/external-sources-registry.md).
Новые — `ext-025`..`ext-048`; повторно используемые — `ext-001`, `ext-005`,
`ext-008`.

- **Enterprise Intelligence:** `ext-025` BPMN 2.0.2, `ext-026` TOGAF, `ext-027`
  ArchiMate, `ext-028` Oxford AI Readiness Index 2025, `ext-029` Microsoft Agentic
  AI maturity.
- **Opportunity Discovery:** `ext-030` Opportunity Solution Trees, `ext-031`
  JTBD/ODI, `ext-032` Lean Startup, `ext-033` McKinsey GenAI potential, `ext-034`
  Impact/Effort Matrix.
- **Human-AI Collaboration:** `ext-001` Building Effective Agents, `ext-005` OpenAI
  Practical Guide, `ext-035` Parasuraman et al. 2000, `ext-036` Vats et al. survey,
  `ext-037` Model Context Protocol.
- **Trust & Evidence:** `ext-038` OCEBM Levels of Evidence, `ext-039` GRADE,
  `ext-040` W3C PROV-DM, `ext-041` SEP Argument (Toulmin).
- **Influence & Network Analysis:** `ext-042` Wasserman & Faust, `ext-043` Freeman
  Centrality, `ext-044` Brin & Page PageRank, `ext-045` Hogan et al. Knowledge
  Graphs.
- **AI Solution Architecture:** `ext-001`, `ext-005`, `ext-046` RAG, `ext-047`
  ReAct, `ext-048` AWS Well-Architected GenAI Lens, `ext-037` MCP, `ext-025` BPMN.

## Связанные артефакты

- [governance/rfc/research-memory-source-intelligence.md](research-memory-source-intelligence.md)
  — PR #242: Knowledge Object, Verdict Rules, source intelligence (переиспользуется
  и расширяется как BA Knowledge Object).
- [governance/rfc/repository-archetypes-template-release.md](repository-archetypes-template-release.md)
  — PR #243: архетипы, Project Template, Governance sync, release strategy.
- [projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md](../../projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md)
  — PR #244: план миграции Mango (приоритеты P1–P4 встраиваются в него).
- [governance/rfc/knowledge-lifecycle-proposal.md](knowledge-lifecycle-proposal.md)
  — жизненный цикл знаний (универсальный скелет).
- [research/mango/2026-05-22-classification.md](../../research/mango/2026-05-22-classification.md) —
  Product Layer Mango (4-уровневая форма, переиспользуется для BA-классификации).
- [AI_GOVERNANCE.md](../../AI_GOVERNANCE.md) — Operating Modes, Creative bypass,
  DoD, разделение Framework / Methodology.
- [governance/repo-model.md](../repo-model.md) — Anti-Inflation principle.
- [standards/project-structure-inheritance.md](../../standards/project-structure-inheritance.md)
  — Base Governance + Local Extension, scope-правила.
- [research/external-knowledge/external-sources-registry.md](../../research/external-knowledge/external-sources-registry.md)
  — зарегистрированные источники `ext-025`..`ext-048`.
