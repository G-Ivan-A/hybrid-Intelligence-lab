---
status: draft
version: 0.1
updated: 2026-06-15
temperature: 0.1
---

# RFC: Research Memory & Source Intelligence Framework

## Proposal

Принять **Research Memory & Source Intelligence** как тонкий слой принятия
решений поверх существующего механизма внешних знаний:

1. **Tier 1: External Trusted Sources** — внешние базы, статьи, репозитории,
   стандарты и практики, на которые Хаб ссылается, но не дублирует.
2. **Tier 2: Internal Research Memory** — внутренние Knowledge Objects: выводы,
   вердикты, статусы, связи с проектами и причины принятия или отклонения.

Ключевой принцип: **Knowledge Object первичен, источник вторичен**. Источник
является атрибутом и доказательством, а не единицей хранения смысла. Один объект
знания может ссылаться на несколько источников и несколько downstream-решений.

Этот RFC не создаёт универсальную базу знаний и не вводит новую онтологию.
Он фиксирует минимальную модель, статусы и правила, которые должны удержать уже
созданные артефакты
[external-sources-registry.md](../../research/external-knowledge/external-sources-registry.md)
и [external-insights/](../../research/external-knowledge/external-insights/)
от превращения в source dump.

## Problem

Текущий механизм внешних знаний уже решает часть боли: источник можно занести в
Base Registry, а полезный вывод — в `external-insights/`. Но он всё ещё
ориентирован на поток `source -> insight`. Для задачи #239 нужна более сильная
рамка: агент должен повторно использовать не факт чтения статьи, а внутренний
вердикт команды о знании.

Последствия без Research Memory:

- агент повторно анализирует уже изученный источник, потому что не видит
  итоговый объект знания и его статус;
- несколько источников про одну идею создают дубли вместо единого объекта;
- `observed` и `candidate` идеи смешиваются с отклонённым хайпом;
- связь `источник -> RFC/ADR -> проект` остаётся ручной и легко теряется;
- доверенный автор или организация могут ошибочно восприниматься как доверенный
  вывод.

## Decision Scope

RFC описывает **рамку и правила применения**. Он:

- НЕ копирует внешний контент в Хаб;
- НЕ вводит CI-скраперы, автоматические парсеры источников или графовую БД;
- НЕ заменяет
  [governance/rfc/external-knowledge-integration.md](external-knowledge-integration.md),
  а уточняет, как его source-centric механизм превращается в object-centric
  Research Memory;
- НЕ продвигает draft-модель в canonical standard без human decision
  ([AI_GOVERNANCE.md](../../AI_GOVERNANCE.md));
- НЕ требует отдельного каталога Research Memory на Phase 0: текущие
  `external-insights/` могут быть носителем Knowledge Objects, пока второй
  независимый use case не докажет потребность в новом формате или шаблоне.

## 1. Анализ Необходимости

### Почему существующих механизмов недостаточно

| Механизм | Что уже решает | Где недостаточен | Решение RFC |
| --- | --- | --- | --- |
| `external-sources-registry.md` | Фиксирует факт изучения источника, тип, теги, проекты и stage. | Источник остаётся первичной сущностью; несколько источников про одну идею не собираются в единый вывод. | Использовать реестр как Tier 1 source map, а не как память решений. |
| `external-insights/` | Хранит полезные выводы из источников и стадии `observation -> candidate-practice`. | Инсайт всё ещё может быть source-shaped: один файл на источник, а не на объект знания. Нет статусов `Applied/Rejected/Superseded`. | Считать новый инсайт Knowledge Object, если он формулирует самостоятельный вывод, статус и traceability. |
| `governance/rfc/` | Фиксирует предложения и rationale до решения человека. | RFC слишком тяжёлый для каждой наблюдаемой идеи; нельзя превращать каждую заметку в governance proposal. | RFC появляется только для decision-worthy знаний; обычные объекты остаются в research memory. |
| `practices/` и `standards/` | Хранят принятые reusable practices и нормы. | Туда нельзя помещать гипотезы и наблюдения без валидации. | Research Memory держит pre-practice слой и не обходит human review. |

**Вывод:** новый слой нужен, но как **модель поверх существующих артефактов**, а
не как новая тяжёлая база. Phase 0 — этот RFC и регистрация источников. Phase 1,
если модель подтвердится, — нормализовать шаблон Knowledge Object в
`external-insights/README.md` или отдельном standard.

### Риски новой сущности

| Риск | Почему опасен | Ограничение |
| --- | --- | --- |
| Enterprise ontology | Система начнёт классифицировать всё знание мира и умрёт от сложности. | Не больше 5 статусов, теги только для фильтрации, не больше 5 тематических тегов на объект без отдельного rationale. |
| Source dump | В память попадут все прочитанные статьи. | Объект создаётся только после Research Pipeline: анализ -> вердикт -> связь с проектом или причиной отклонения. |
| Дубли | Каждая статья рождает новый файл про ту же идею. | Если объект уже есть, добавляется `source_ref`, а не новый Knowledge Object. |
| Ложное доверие | `OpenAI/Anthropic/NASA` воспринимаются как автоматическая истина. | Доверенный источник упрощает provenance, но не заменяет проверку вывода. |
| Скрытая бюрократия | Метаданные станут параллельной БД. | Минимальная запись: statement, status, sources, verdict, consumers, linked decisions, review rule. |

## 2. Existing Approaches: Что Берём И Что Не Берём

| Подход | Что заимствуем | Что не заимствуем и почему |
| --- | --- | --- |
| **PKM / Zettelkasten / Evergreen Notes** | Атомарность заметки, связь между идеями, развитие заметки во времени, ориентация на концепт, а не на источник. | Не берём личный бесконечный сад заметок: Хабу нужен reviewable слой для команды, а не приватная мыслительная среда без DoD. |
| **ResearchOps / Lessons Learned** | Операционную дисциплину: роли, процессы, повторное использование результатов исследований, масштабирование эффекта исследования через общие механизмы. | Не берём тяжёлую оргструктуру ResearchOps: у Хаба нет отдельной research-операционной команды, поэтому ownership фиксируется через PR, RFC и human review. |
| **ADR / Decision Records** | Контекст -> решение -> последствия, лёгкий формат, трассируемость решений после смены команды. | Не превращаем каждую гипотезу в ADR: ADR нужен для принятого решения, а Research Memory хранит и `Observed`, и `Rejected`, и `Candidate`. |
| **Существующий Hub lifecycle** | Reverse traceability и переходы `Research -> RFC -> Pattern -> Standard` из [knowledge-lifecycle-proposal.md](knowledge-lifecycle-proposal.md). | Не копируем всю lifecycle-цепочку внутрь каждого объекта: статус Research Memory отвечает на пригодность знания, а не на расположение файла. |

## 3. Двухуровневая Архитектура

### Tier 1: External Trusted Sources

Tier 1 — это карта внешних источников:

- статьи, стандарты, репозитории, документация, research reports;
- метаданные для фильтрации: тип, язык, теги, релевантные проекты, stage;
- ссылки на первоисточник и на внутренние объекты, где есть вердикт.

Tier 1 **не хранит знание как решение**. Он отвечает на вопрос: "Что мы уже
видели, откуда это пришло и где искать первичный материал?"

### Tier 2: Internal Research Memory

Tier 2 — это слой внутренних Knowledge Objects:

- формулировка знания человеческим языком;
- статус (`Observed`, `Candidate`, `Applied`, `Rejected`, `Superseded`);
- проверочный вердикт: почему это полезно, сомнительно или отклонено;
- связи с источниками, RFC/ADR, practices/standards и проектами-потребителями;
- правило пересмотра или устаревания.

Tier 2 отвечает на вопрос: "Что команда поняла, какой статус у вывода и где он
уже влияет на решения?"

## 4. Knowledge Object Model

Минимальная запись Knowledge Object:

| Поле | Назначение |
| --- | --- |
| `object_id` | Стабильный `kebab-case` якорь, например `ko-context-engineering`. |
| `statement` | Один проверяемый вывод, а не пересказ источника. |
| `status` | Один из пяти статусов Research Memory. |
| `source_refs` | Ссылки на Tier 1 (`ext-NNN`) и первоисточники. |
| `source_intelligence` | Оценка claim type: код/метрики/алгоритм/практика/маркетинг/гипотеза. |
| `verdict` | Почему команда принимает, наблюдает, отклоняет или считает устаревшим вывод. |
| `consumers` | Проекты или артефакты, которые используют или могут использовать объект. |
| `linked_decisions` | RFC, ADR, practice, standard, issue или PR, где объект повлиял на решение. |
| `review_rule` | Когда пересмотреть: milestone, дата, событие или появление replacement object. |

Минимальный объект можно хранить прямо в `external-insights/` до появления
потребности в отдельном каталоге. Если один source даёт несколько независимых
выводов, создаются несколько Knowledge Objects. Если несколько sources говорят
об одном выводе, они добавляются в `source_refs` одного объекта.

## 5. Knowledge Status

| Статус | Что означает | Требование |
| --- | --- | --- |
| `Observed` | Идея замечена, сформулирована и не отброшена, но пока нет достаточного основания для внедрения. | Есть источник и краткая причина, почему не выброшено. |
| `Candidate` | Вывод проверен на уровне research и имеет понятный consumer или сценарий применения. | Есть source intelligence, риски, expected use и критерий проверки. |
| `Applied` | Вывод внедрён в проект, практику, standard, template, ADR или RFC с явным следом. | Есть linked decision и evidence: PR, тест, ADR, practice или standard. |
| `Rejected` | Вывод изучен и осознанно отклонён. | Есть причина: hype, нет проверяемости, конфликт с governance, слабая применимость. |
| `Superseded` | Вывод устарел или заменён новым объектом знания. | Есть ссылка на replacement или причина устаревания. |

### Правила переходов

```text
Observed -> Candidate: найден consumer, проверочный критерий и аргументы за/против.
Candidate -> Applied: есть принятое downstream-решение и evidence.
Observed/Candidate -> Rejected: выявлен hype, отсутствие проверяемости или несоответствие контексту.
Observed/Candidate/Applied -> Superseded: появился replacement object или изменился внешний контекст.
Rejected -> Observed/Candidate: только при новом источнике или явном human request.
Applied -> Superseded: предпочтительный путь при замене; тихий downgrade запрещён.
```

Статус может иметь consumer-specific evidence. Например, Knowledge Object может
быть `Candidate` для Хаба как reusable practice, но иметь `Applied evidence` в
одном spoke-проекте. В таком случае основной статус остаётся консервативным, а
проектное применение указывается в `linked_decisions`.

## 6. Source Intelligence: Как Отличать Гипотезу От Хайпа

Доверенный источник не равен доверенному выводу. Агент оценивает claim, а не
бренд автора.

### Признаки проверяемой гипотезы

- описан конкретный механизм, алгоритм, протокол, код или архитектурный приём;
- есть воспроизводимый пример, benchmark, метрика, тест или процедура проверки;
- указаны ограничения, trade-offs и условия применимости;
- источник позволяет отделить факт, интерпретацию и рекомендацию;
- вывод можно связать с issue, RFC, ADR, practice или экспериментом.

### Признаки маркетинговой воды

- обещание результата без механизма проверки;
- абсолютные формулировки без ограничений и контрпримеров;
- только storytelling, промо-скриншоты или sales narrative;
- нет кода, метрик, алгоритма, данных, примера или операционного критерия;
- источник требует принять вывод из-за репутации автора, а не из-за evidence.

### Verdict Rules

| Claim type | Действие |
| --- | --- |
| Код/алгоритм/метрика/ADR/practice с понятной применимостью | `Candidate` или `Applied`, если есть consumer evidence. |
| Хорошая идея без проверки | `Observed` с review rule. |
| Сильный бренд, слабая доказательность | `Observed`, не `Candidate`. |
| Маркетинг без проверяемого механизма | `Rejected`, только registry + причина. |
| Устаревшая, но важная для истории идея | `Superseded`, ссылка на replacement. |

## 7. Traceability Model

Базовая цепочка:

```text
Knowledge Object
  -> source_refs (Tier 1)
  -> internal verdict / source intelligence
  -> linked RFC/ADR/practice/standard
  -> project consumers
  -> review or supersession rule
```

Research Memory не заменяет
[knowledge-lifecycle-proposal.md](knowledge-lifecycle-proposal.md). Он добавляет
память решения до и между lifecycle-переходами.

### Concrete Example: Context Engineering

| Поле | Пример |
| --- | --- |
| `object_id` | `ko-context-engineering-selective-context` |
| Knowledge Object | Context Engineering as selective context loading for AI agents: agent quality improves when the system retrieves the smallest relevant context slice instead of dumping the whole knowledge base. |
| Sources | `ext-008` Anthropic context engineering, `ext-009` agent local memory/context, `ext-001` building effective agents. |
| Status | `Candidate` for Hub-level reusable practice. |
| Applied evidence | `G-Ivan-A/clarify-engine-ai` has accepted [ADR-009 Parent Document Retrieval](https://github.com/G-Ivan-A/clarify-engine-ai/blob/main/docs/ADR/009-parent-document-retrieval.md), which applies selective parent-context retrieval in consultation mode. |
| Consumers | `clarify-engine-ai` (applied evidence), `hub` (agent context/lazy loading), `mango_ba_prompts` (candidate for requirements-context retrieval). |
| Linked RFC | [documentation-architecture-balance.md](documentation-architecture-balance.md) uses the same lazy-loading principle for documentation; this RFC defines the Research Memory layer. |
| Linked ADR | [clarify-engine-ai/docs/ADR/009-parent-document-retrieval.md](https://github.com/G-Ivan-A/clarify-engine-ai/blob/main/docs/ADR/009-parent-document-retrieval.md). |
| Review rule | Promote to `Applied` in the Hub only after a Hub practice or standard adopts selective context loading with a reproducible check. |

Этот пример показывает, почему Knowledge Object первичен: источники разные, но
внутренний вывод один. ADR подтверждает downstream-применение, но не делает
вывод автоматически canonical для всего Хаба.

## 8. Как Не Превратить Research Memory В Свалку

1. **Entry gate:** объект создаётся только после формулировки вывода и вердикта.
   Просто прочитанный источник остаётся в Tier 1 registry.
2. **One object, many sources:** новый source добавляется к существующему объекту,
   если statement не меняется.
3. **Default agent load:** агент по умолчанию читает только `Applied` и
   `Candidate` по релевантным тегам. `Observed`, `Rejected` и `Superseded`
   открываются по явному запросу или при conflict analysis.
4. **Review rule обязательна:** у `Observed` и `Candidate` должен быть trigger
   пересмотра: milestone, второй source, project consumer, pilot или срок.
5. **Rejection is useful memory:** `Rejected` не удаляется, потому что экономит
   будущий повторный анализ. Но он не попадает в default recommendations.
6. **Supersession вместо копий:** новая версия идеи не создаёт `v2`-копию файла,
   а связывает старый объект как `Superseded`.
7. **No universal taxonomy:** классификация отвечает "что это за decision-worthy
   knowledge для нашей команды?", а не "как описать все знания мира?".

## 9. Implementation Path

| Фаза | Действие | Условие перехода |
| --- | --- | --- |
| Phase 0 (этот PR) | Создать RFC, описать модель, статусы, source intelligence, traceability example; зарегистрировать изученные методологические источники в Base Registry. | Локальная валидация проходит, PR готов к review. |
| Phase 1 | Нормализовать `external-insights/README.md` под Knowledge Object template или добавить отдельный lightweight template. | Human review подтверждает, что object-centric модель нужна повторно. |
| Phase 2 | Перевести 2-3 существующих инсайта (`ext-001`, `ext-003`, `ext-009`) в Knowledge Object format без потери ссылок. | Есть пилотный consumer и review feedback. |
| Phase 3 | При необходимости делегировать обязательную норму в standard или practice. | Человек явно подтверждает promotion из RFC. |

## Acceptance Criteria

- Есть раздел "Анализ необходимости" и объяснение, почему registry/insights
  недостаточны без object-centric слоя.
- Сравнены минимум 3 существующие методологии управления знаниями.
- Описана двухуровневая архитектура Tier 1 / Tier 2.
- Определены 5 статусов знания и правила перехода между ними.
- Сформулированы критерии отличия проверяемой гипотезы от hype/marketing.
- Дана traceability-схема `Knowledge Object -> Sources -> RFC/ADR -> Consumer`.
- Приведён конкретный пример Knowledge Object с источниками, статусом,
  consumers, linked RFC и linked ADR.
- Описаны правила против превращения Research Memory в свалку.

## Open Decisions

1. Достаточно ли считать `external-insights/` носителем Knowledge Objects, или
   после пилота нужен отдельный каталог `research-memory/`?
2. Должен ли `Applied` быть глобальным статусом Хаба или consumer-specific
   статусом внутри объекта?
3. Нужен ли отдельный validator для Knowledge Object template, или human review
   и структура RFC пока достаточны?

## Sources

- [Communication with Zettelkastens](https://zettelkasten.de/communications-with-zettelkastens/) — источник для принципа атомарных связанных заметок.
- [Evergreen notes](https://notes.andymatuschak.org/z5E5QawiXCMbtNtupvxeoEX) — источник для идеи заметок, которые развиваются и накапливают ценность между проектами.
- [ResearchOps Community: About](https://researchops.community/about/) — источник для operational layer вокруг исследований.
- [Michael Nygard: Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) — источник для decision records и traceability через context/decision/consequences.
- [external-knowledge-integration.md](external-knowledge-integration.md) — существующий механизм Base Registry + Local Extension + Smart Sync.
- [knowledge-lifecycle-proposal.md](knowledge-lifecycle-proposal.md) — lifecycle и reverse traceability.
