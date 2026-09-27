---
status: proposed
version: 1.0
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
| Impacted artifacts | [`AGENTS.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/AGENTS.md), [`templates/htom/AGENTS.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/templates/htom/AGENTS.md), [`templates/spoke/AGENTS.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/templates/spoke/AGENTS.md), [`ai-rules/agent-collaboration-rules.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-rules/agent-collaboration-rules.md), [`ai-rules/agent-work-rules.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-rules/agent-work-rules.md); после решения по K-1/K-2 — [`ai-governance/ai-governance.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-governance/ai-governance.md), [`standards/glossary.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/glossary.md) |
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

Анализ выявил два противоречия действующих контрактов. Issue требует
зафиксировать их отдельным ADR без изменения существующих формулировок.

| ID | Противоречие | Источники |
| --- | --- | --- |
| K-1 | `Hybrid` определён двумя способами. **(а) По частям:** части задачи явно назначаются `Structured` или `Creative`. **(б) Средний уровень:** агент сверяет с целью, оптимизирует способ, не переопределяет вектор, бюджет средний. Issue #625 описывает вариант (б). | (а): [agent-work-rules §Operating Modes](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-rules/agent-work-rules.md#operating-modes), [ai-governance §Обоснованное отклонение](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-governance/ai-governance.md). (б): [agent-work-rules §Контракт апелляции](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-rules/agent-work-rules.md#контракт-апелляции), `<hybrid_work>` в `AGENTS.md` |
| K-2 | Глоссарий: Operating Mode «не определяет тип результата и глубину обработки». Agent Work Rules: режим — разрешение «на бюджет исполнения: Creative — наибольшая глубина проработки». Issue #625 требует бюджет токенов по режимам. | [standards/glossary.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/glossary.md) (строка Operating Mode); agent-work-rules §Operating Modes |

## Decision

**1. Слой сотрудничества.** Правила коммуникации, профили режимов, креативный
протокол, правило обоснованных задач, якоря синхронизации и реестр
анти-паттернов живут в одном файле —
[`ai-rules/agent-collaboration-rules.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-rules/agent-collaboration-rules.md).
Общий слой `AGENTS.md` (Хаб и оба шаблона, мажорная версия 3.0) несёт краткую
норму и маршрут:

- стратегическую проверку в правиле нормализации цели;
- запрет пустого исполнения и подхалимства в `<forbidden>`;
- бюджет по режимам и абзац Collaboration в `<hybrid_work>`.

`agent-work-rules.md` получает только ссылки: бюджет размера точки входа
исчерпан на 96%.

**2. Якоря — не гейты.** Точек человеческого контроля остаётся две: режим при
постановке и merge. Якоря делают дрейф видимым и не блокируют работу.
Единственный блокирующий случай — критический риск (C-5). Это сочетание
Контракта эскалации и human decision rights, а не новый гейт.

**3. Негативные кейсы обязательны.** В `Creative` каждый найденный негативный
кейс превращается в проверку контракта. Модель без негативных кейсов не
считается готовой. Урок ADR-014 обобщается с мета-модели БА на любую модель
(анти-паттерны F-1, F-2).

**4. Предлагаемое согласование K-1 и K-2** (не применено; ждёт решения
владельца):

- K-1: `Hybrid` — средний уровень по умолчанию (вариант (б)). Явное назначение
  частей задачи `Structured` или `Creative` остаётся опцией автора и для этих
  частей имеет приоритет. Новый файл уже формулирует обе нормы совместимо;
  формулировки варианта (а) в Agent Work Rules и AI Governance дополняются
  после решения.
- K-2: Operating Mode задаёт уровень автономии **и** бюджет глубины; `Task Type`
  задаёт тип результата. Строка глоссария правится после решения: `standards/`
  не меняется без явных полномочий.

## Decision Drivers

| Драйвер | Содержание |
| --- | --- |
| Стратегия важнее тактики | Ошибки мета-модели БА были тактически разумными (быстро, на готовой практике) и стратегически дорогими: повторная сборка модели. |
| Anti-Inflation | Один новый rule-файл вместо разнесения по нескольким. Точка входа получает норму и маршрут, а не копию. |
| Бюджет контекста | `agent-work-rules.md` занимает ~6.7K из 7K оценочных токенов; новое содержание туда не помещается. |
| Проверяемость | Каждое правило коммуникации имеет строку «Как проверяется». Маршрут и ключевые формулировки защищены регрессионным тестом. |
| Совместимость | Модель исполнения (перезапуск агента только вручную, merge как согласование) не меняется, гейты не добавляются. |

## Alternatives Considered

| Альтернатива | Почему отклонена |
| --- | --- |
| **Не менять контракты** («близки к совершенству») | Пробелы G-1…G-6 подтверждены чтением контрактов, G-4 — реальным провалом БА. Откладывание оставляет повтор ошибки на следующей модели. |
| **Расширить `agent-work-rules.md`** | Превышает бюджет размера файла глубины 0 (порог 7K) и смешивает контракты исполнения с правилами партнёрства. |
| **Отдельный rule-файл на каждую тему** (коммуникация, режимы, креатив) | Три файла на одну норму партнёрства, три маршрута в точке входа — инфляция без операционной выгоды. |
| **Блокирующие гейты человека после сбора данных** (предложение из диалога фаундера с ИИ-ассистентом) | Противоречит модели исполнения: агент не перезапускается комментарием, а дополнительные гейты запрещены. Заменено неблокирующими якорями A-2…A-5. |
| **Сразу переписать определения `Hybrid` и глоссарий** | Issue запрещает менять существующие контракты при противоречии без решения владельца, а `standards/` требует явных полномочий. |

## Consequences

**Положительные.**

- Режимы получают измеримые профили: бюджет, гипотезы, источники, подзадачи.
- Негативный опыт становится проверками контрактов, а не памятью участников.
- Позиция агента в PR (согласие или несогласие, стратегический риск)
  становится обязательной поверхностью ревью.

**Отрицательные и риски.**

- `Creative` дороже по токенам и времени. Это выданное разрешение, но оно
  требует от автора осознанного выбора режима.
- Мажорная версия шаблонов (3.0) требует синхронизации спицами через Smart
  Sync.
- Большинство проверок остаются human-only review. Машинно проверяются только
  наличие маршрута и ключевых норм.
- До решения по K-1 и K-2 в контрактах сосуществуют две формулировки `Hybrid`.

## Compliance and Validation

| Проверка | Форма | Кто выполняет |
| --- | --- | --- |
| Файл правил существует и содержит разделы §1–§7, правила C-1…C-7 и формулировку правила обоснованных задач | `tools/test-agent-collaboration-contract.sh` | CI |
| `AGENTS.md` и оба шаблона маршрутизируют к файлу и несут стратегическую проверку | тот же тест | CI |
| Якоря объявлены не гейтами | тот же тест | CI |
| Строка «Стратегический риск» и позиция по постановке в теле PR | ревью | `G-human` |
| Обоснованность апелляций и отсутствие подхалимства | ревью | `G-human` |

## Lifecycle

| Переход | Условие |
| --- | --- |
| `proposed → accepted` | Merge PR [#626](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/626) или явное решение владельца по K-1 и K-2. |
| Реализация K-1/K-2 | Отдельная задача бэклога после решения. |
| Пересмотр | Повторяющийся провал, не покрытый реестром F-*, или измеренный перерасход `Creative` без роста качества. |

## Related Artifacts

- [`ai-rules/agent-collaboration-rules.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ai-rules/agent-collaboration-rules.md)
  — норма, введённая этим решением.
- [`docs/rfc/2026-09-27-rfc-agent-collaboration-and-operating-modes.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/rfc/2026-09-27-rfc-agent-collaboration-and-operating-modes.md)
  — гипотезы, внешние источники, синтез кейсов и стресс-тесты.
- [`docs/adr/2026-08-adr-010-agent-autonomy-principles.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-08-adr-010-agent-autonomy-principles.md)
  — закрытый перечень автономии, который слой не расширяет.
- [`docs/adr/2026-09-adr-014-legacy-evidence-not-baseline.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-014-legacy-evidence-not-baseline.md)
  — первый урок БА, обобщённый в F-1.
