---
status: proposed
version: 1.1
updated: 2026-09-27
temperature: 0.1
owner: G-Ivan-A
decision-type: governance
---

# ADR-021: Слой правил сотрудничества агента и согласование определений режимов

## Decision Metadata

| Field | Value |
| --- | --- |
| ADR id | ADR-021 |
| Decision type | governance |
| Decision status | proposed (narrative summary; машиночитаемый canon — frontmatter `status`) |
| Decision date | 2026-09-27 |
| Owner | G-Ivan-A |
| Source | issue [#625](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/625); обоснование — [RFC agent collaboration and operating modes](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/rfc/2026-09-27-rfc-agent-collaboration-and-operating-modes.md) |
| Impacted artifacts | [`AGENTS.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/AGENTS.md), [`templates/htom/AGENTS.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/templates/htom/AGENTS.md), [`templates/spoke/AGENTS.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/templates/spoke/AGENTS.md), [`ai-rules/agent-collaboration-rules.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-rules/agent-collaboration-rules.md), [`ai-rules/agent-work-rules.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-rules/agent-work-rules.md), [`ai-governance/ai-governance.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-governance/ai-governance.md), [`standards/glossary.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/glossary.md) |
| Supersedes | none |
| Superseded by | none |
| Дополняет | [ADR-010](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-08-adr-010-agent-autonomy-principles.md) — принципы автономии; [ADR-014](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-014-legacy-evidence-not-baseline.md) — обобщает урок наследия с мета-модели БА на любую модель и добавляет контур негативных кейсов |

## Context

Контракты Хаба уже нормируют апелляцию, автономию, эскалацию, верификацию и
инициативу по режимам ([Agent Work Rules](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-rules/agent-work-rules.md)).
Issue #625 и опыт мета-модели БА показывают пробелы, которые эти контракты не
закрывают.

| Пробел | Наблюдение |
| --- | --- |
| G-1. Стратегическая эффективность | Нормализация цели читает только концепцию. Видение и проверка «тактическая победа — стратегическое поражение» отсутствуют. |
| G-2. Правила коммуникации | Обязанность возражать выражена через апелляцию. Запретов на пустое исполнение и подхалимство, требования краткости и правила «disagree and commit» нет. |
| G-3. Протокол `Creative` | «Наибольший бюджет» не раскрыт в обязательства: внешние источники, опровергающие гипотезы, синтез кейсов и оцифровка не требуются. |
| G-4. Негативные кейсы | ADR-014 закрывает первую ошибку БА (наследие как базис) только для мета-модели БА. Вторую ошибку — чистую модель без негативных кейсов — не закрывает ни один контракт. |
| G-5. Обоснованные задачи | Число задач не ограничено, но критерий обоснованности не задан. |
| G-6. Синхронизация | Якоря против дрейфа (readback, журнал решений, повторное чтение после сжатия контекста) не описаны. Запрет дополнительных гейтов при этом действует. |

Анализ выявил два противоречия действовавших контрактов. Они первоначально
оставались открытыми; владелец разрешил оба в
[комментарии к PR #626](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/626#issuecomment-5859825381).

| ID | Противоречие | Источники |
| --- | --- | --- |
| K-1 | `Hybrid` определён двумя способами. **(а) По частям:** части задачи явно назначаются `Structured` или `Creative`. **(б) Средний уровень:** агент сверяет с целью, оптимизирует способ, не переопределяет вектор, бюджет средний. Issue #625 описывает вариант (б). | (а): [agent-work-rules §Operating Modes](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-rules/agent-work-rules.md#operating-modes), [ai-governance §Обоснованное отклонение](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-governance/ai-governance.md). (б): [agent-work-rules §Контракт апелляции](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-rules/agent-work-rules.md#контракт-апелляции), `<hybrid_work>` в `AGENTS.md` |
| K-2 | Глоссарий: Operating Mode «не определяет тип результата и глубину обработки». Agent Work Rules: режим — разрешение «на бюджет исполнения: Creative — наибольшая глубина проработки». Issue #625 требует бюджет токенов по режимам. | [standards/glossary.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/glossary.md) (строка Operating Mode); agent-work-rules §Operating Modes |

## Decision

**1. Слой сотрудничества.** Только правила коммуникации C-1…C-7 и карта
источников истины живут в новом файле —
[`ai-rules/agent-collaboration-rules.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-rules/agent-collaboration-rules.md).
Общий слой `AGENTS.md` (Хаб и оба шаблона, версия 3.1) несёт краткую
норму и маршрут:

- стратегическую проверку в правиле нормализации цели;
- запрет пустого исполнения и подхалимства в `<forbidden>`;
- бюджет по режимам и абзац Collaboration в `<hybrid_work>`.

Определения режимов, бюджет, Creative и правило обоснованных задач размещены в
`agent-work-rules.md`; стратегическая нормализация уже жила там. Якоря
синхронизации размещены в onboarding protocol, а кейсы и анти-паттерны служат
evidence в RFC. Вариант с несколькими активными владельцами одной нормы
отклонён после [аудита дублирования](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/rfc/2026-09-27-rfc-agent-collaboration-and-operating-modes.md#аудит-единственного-источника-истины-по-замечанию-владельца).

**2. Якоря — не гейты.** Точек человеческого контроля остаётся две: режим при
постановке и merge. Якоря делают дрейф видимым и не блокируют работу.
Единственный блокирующий случай — критический риск (C-5). Это сочетание
Контракта эскалации и human decision rights, а не новый гейт.

**3. Негативные кейсы обязательны.** В `Creative` существенный для решения
негативный кейс превращается в проверку. Урок ADR-014 обобщается с мета-модели
БА на любую модель; конкретные кейсы и пределы обобщения остаются в RFC.

**4. Согласование K-1 и K-2** по явному решению владельца:

- K-1: `Hybrid` — средний уровень по умолчанию (вариант (б)). Явное назначение
  частей задачи `Structured` или `Creative` остаётся опцией автора и для этих
  частей имеет приоритет. Agent Work Rules и AI Governance согласованы в PR.
- K-2: Operating Mode задаёт уровень автономии **и** бюджет глубины; `Task Type`
  задаёт тип результата. Строка глоссария исправлена в PR по явному полномочию.

## Decision Drivers

| Драйвер | Содержание |
| --- | --- |
| Стратегия важнее тактики | Ошибки мета-модели БА были тактически разумными (быстро, на готовой практике) и стратегически дорогими: повторная сборка модели. |
| Anti-Inflation | Новый rule-файл оправдан только коммуникацией; остальные нормы расширяют действующие каноны. Точка входа даёт краткий маршрут. |
| Бюджет контекста | Консолидация режимов довела `agent-work-rules.md` до мягкого предупреждения, но ниже жёсткого порога 9K оценочных токенов. Риск указан в RFC и PR. |
| Проверяемость | Каждое правило коммуникации имеет строку «Как проверяется». Маршрут и ключевые формулировки защищены регрессионным тестом. |
| Совместимость | Модель исполнения (перезапуск агента только вручную, merge как согласование) не меняется, гейты не добавляются. |

## Alternatives Considered

| Альтернатива | Почему отклонена |
| --- | --- |
| **Не менять контракты** («близки к совершенству») | Пробелы G-1…G-6 подтверждены чтением контрактов, G-4 — реальным провалом БА. Откладывание оставляет повтор ошибки на следующей модели. |
| **Разместить коммуникацию в `agent-work-rules.md`** | Смешивает форму партнёрского диалога с контрактами исполнения и сильнее увеличивает файл у точки входа. |
| **Отдельный rule-файл на каждую тему** (коммуникация, режимы, креатив) | Три файла на одну норму партнёрства, три маршрута в точке входа — инфляция без операционной выгоды. |
| **Блокирующие гейты человека после сбора данных** (предложение из диалога фаундера с ИИ-ассистентом) | Противоречит модели исполнения: агент не перезапускается комментарием, а дополнительные гейты запрещены. Заменено неблокирующими якорями A-2…A-5. |
| **Оставить K-1/K-2 после ответа владельца** | Сохраняет известные противоречия вопреки явному решению; определения согласованы в этом PR. |

## Consequences

**Положительные.**

- Режимы получают измеримые профили: бюджет, гипотезы, источники, подзадачи.
- Негативный опыт становится проверками контрактов, а не памятью участников.
- Позиция агента в PR (согласие или несогласие, стратегический риск)
  становится обязательной поверхностью ревью.

**Отрицательные и риски.**

- `Creative` дороже по токенам и времени. Это выданное разрешение, но оно
  требует от автора осознанного выбора режима.
- Мажорная версия шаблонов (3.1) требует синхронизации спицами через Smart
  Sync.
- Большинство проверок остаются human-only review. Машинно проверяются только
  наличие маршрута и ключевых норм.
- `agent-work-rules.md` превышает мягкий порог размера; будущие добавления
  должны сначала убрать повторы, чтобы не достигнуть жёсткого порога.

## Compliance and Validation

| Проверка | Форма | Кто выполняет |
| --- | --- | --- |
| Файл коммуникации содержит C-1…C-7 и Single source of truth без повторения других норм | `tools/test-operating-mode-contract.sh` | CI |
| Hybrid, glossary и PR template согласованы | тот же тест | CI |
| `AGENTS.md` и оба шаблона несут стратегическую проверку | `tools/test-agents-md-integration.sh` | CI |
| Якоря объявлены не гейтами | `ai-rules/agent-onboarding-protocol.md` | Review |
| Строка «Стратегический риск» и позиция по постановке в теле PR | ревью | `G-human` |
| Обоснованность апелляций и отсутствие подхалимства | ревью | `G-human` |

## Lifecycle

| Переход | Условие |
| --- | --- |
| `proposed → accepted` | Merge PR [#626](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/626) после проверки дублирования. |
| Реализация K-1/K-2 | Выполнена в PR по решению владельца; принятие зависит от merge. |
| Пересмотр | Повторяющийся провал вне кейсов RFC или измеренный перерасход `Creative` без роста качества. |

## Related Artifacts

- [`ai-rules/agent-collaboration-rules.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-rules/agent-collaboration-rules.md)
  — норма, введённая этим решением.
- [`docs/rfc/2026-09-27-rfc-agent-collaboration-and-operating-modes.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/rfc/2026-09-27-rfc-agent-collaboration-and-operating-modes.md)
  — гипотезы, внешние источники, синтез кейсов и стресс-тесты.
- [`docs/adr/2026-08-adr-010-agent-autonomy-principles.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-08-adr-010-agent-autonomy-principles.md)
  — закрытый перечень автономии, который слой не расширяет.
- [`docs/adr/2026-09-adr-014-legacy-evidence-not-baseline.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-014-legacy-evidence-not-baseline.md)
  — первый урок БА, обобщённый в Creative протоколе.
