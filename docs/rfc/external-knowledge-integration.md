---
status: draft
version: 0.1
updated: 2026-06-13
temperature: 0.1
owner: G-Ivan-A
rfc-scope: A
---

# RFC: External Knowledge Integration

## Proposal

Принять механизм интеграции внешних знаний экосистемы, состоящий из трёх
связанных частей:

1. **Base Registry** — единый реестр внешних источников в Хабе:
   [research/external-knowledge/external-sources-registry.md](../../research/external-knowledge/external-sources-registry.md).
2. **External Insights** — хранилище атомарных инсайтов с привязкой к lifecycle:
   [research/external-knowledge/external-insights/](../../research/external-knowledge/external-insights/).
3. **Base + Local Extension** — модель синхронизации, где Хаб хранит базовый
   реестр, а проекты добавляют локальные расширения и забирают релевантные строки
   через Smart Sync без дублирования.

RFC фиксирует решение и rationale. Обязательная норма (если потребуется)
делегируется в active artifact: реестр, профиль исследований или standard. До
такой делегации downstream-проект ссылается на RFC как на обоснование, но не
обязан выполнять его механически
([docs/rfc/README.md](README.md)).

## Problem

Исследование внешних источников (GitHub, Habr, международные практики)
происходит ad-hoc: результаты оседают в чатах, проекты не знают релевантных
источников, нет воспроизводимого пути «внешняя идея → внутренняя практика».

Последствия:

- потеря актуальности практик;
- дублирование исследовательских усилий между проектами;
- риск загрязнения `practices/` невалидированной информацией (внешнее принимается
  как практика в обход lifecycle).

## Decision Scope

RFC предлагает **механизм** (реестр + инсайты + модель синхронизации). Он:

- не переводит ни один источник в практику или стандарт автоматически;
- не вводит CI-скраперы и автоматический сбор контента (прямой запрет НФТ задачи
  #227);
- не меняет правила lifecycle, а **использует** существующее предложение
  [docs/rfc/knowledge-lifecycle-proposal.md](knowledge-lifecycle-proposal.md).

## Target Artifacts

| Target | Статус в этом PR | Условие повышения |
| --- | --- | --- |
| `research/external-knowledge/external-sources-registry.md` | Создан как `draft` | Перевод в `reviewed` — решение человека после первого применения в проекте. |
| `research/external-knowledge/external-insights/` (механизм + 3 примера) | Создан как `draft` | Инсайт переходит в `candidate-practice` → reviewable PR в `practices/` + решение человека. |
| `docs/rfc/external-knowledge-integration.md` | Этот RFC, `draft` | Остаётся `draft` до решения Founder & PO. |

> ⚠️ **Creative override (зафиксирован).** Issue #227 называет пути
> `research/external-sources-registry.md` и `research/external-insights/` в
> корне `research/`. Это нарушает hard rule «файлы исследований только в
> тематических подкаталогах, корень `research/` содержит лишь `README.md`»
> ([research/README.md](../../research/README.md)). Поэтому артефакты размещены в
> новом доменном подкаталоге `research/external-knowledge/` с сохранением
> исходных имён файлов. Обоснование: соответствие правилу изоляции по доменам и
> resolver-логике
> ([docs/rfc/resolve-artifact-location-proposal.md](resolve-artifact-location-proposal.md)).

## Base Registry + Local Extension

| Слой | Где живёт | Что содержит | Кто владеет |
| --- | --- | --- | --- |
| **Base Registry** | Хаб: `research/external-knowledge/external-sources-registry.md` | Источники общей ценности (`projects: all` или ≥2 проекта). | Хаб (методологический центр). |
| **Local Extension** | Проект/спок: `research/<project>/external-sources-registry.md` (по необходимости) | Источники, релевантные только этому проекту. | Команда проекта. |

**Правила слоёв:**

- Источник попадает в Base Registry, только если он полезен ≥2 проектам или всему
  Хабу. Узкий источник остаётся в Local Extension (Anti-Inflation).
- Проект **не дублирует** Base Registry у себя — он ссылается на него и хранит
  лишь свои локальные строки (принцип «Need-to-Know»,
  [docs/ecosystem-map.md](../ecosystem-map.md)).
- Промоция источника `Local → Base` — отдельное решение при появлении второго
  заинтересованного проекта.

## Smart Sync

Механизм опирается на уже существующий Smart Sync
([guides/sync-from-hub.md](../../guides/sync-from-hub.md),
[tools/sync-from-hub.sh](../../tools/sync-from-hub.sh)) без новой инфраструктуры:

- Base Registry — это **читаемый источник**, а не шаблон для копирования: проект
  фильтрует строки по колонкам «Теги» и «Проекты» и подтягивает только нужное.
- Никакого автоматического зеркалирования контента источников: синхронизируется
  карта (метаданные), а не первоисточники.
- Фильтрация по тегам делает выборку компактной для агента (НФТ «оптимизация для
  агентов»): агент читает не весь реестр, а срез.

## Lifecycle Binding

Поток знания подчинён цепочке
[docs/rfc/knowledge-lifecycle-proposal.md](knowledge-lifecycle-proposal.md):

```text
external source (registry)
  -> insight: observation -> research -> hypothesis -> candidate-practice
  -> [решение человека] -> practices/ / standards/
```

- `research/` отвечает за стадии до `candidate-practice` включительно.
- Переход в `practices/`/`standards/` требует reviewable PR и **решения
  человека** ([AI Governance](../../ai-governance/ai-governance.md)). Инсайт не повышает свой
  статус сам.

## Применение для 4 проектов экосистемы

| Проект | Что даёт механизм | Релевантные источники (пример) |
| --- | --- | --- |
| **Хаб** (`hybrid-Intelligence-lab`) | Base Registry + единый поток «источник → practice-кандидат»; фильтр шума перед `practices/`. | `ext-001` (паттерны агентов), `ext-006` (Diátaxis для docs), `ext-008` (context engineering). |
| **mango_ba_prompts** | Local Extension для доменных источников БА; путь «внешняя практика → ТЗ-flow». | `ext-003` (spec-driven), `ext-007` (context engineering, ru). |
| **open-ai.ru** | Источники UX/AI-native интерфейса и coding-agent практик через фильтр тегов. | `ext-004` (Claude Code practices), `ext-001`. |
| **clarify-engine-ai** | Гипотеза spec-driven уточнения требований как кандидат в отдельный RFC. | `ext-003` (spec-driven), `ext-002` (human-in-the-loop). |

Проекты получают **не весь реестр**, а срез по своим тегам, и ведут собственные
Local Extension без обращения к Хабу за каждой узкой ссылкой.

## Follow-up (инициированные исследования/RFC)

Механизм сознательно оставляет «крючки», не раздувая текущий PR:

1. **Пилот spec-driven requirements** для Mango/clarify-engine-ai (инсайт
   `ext-003`, стадия `hypothesis`) → при подтверждении — отдельный RFC.
2. **Local Extension реестра в споке** — предложить шаблон
   `research/<project>/external-sources-registry.md` для синхронизации, когда у
   первого спока появится ≥3 локальных источника.
3. **Промоция `candidate-practice` → practice** — отработать на первом инсайте,
   дошедшем до `candidate-practice`, и описать как practice-node в
   [practices/README.md](../../practices/README.md).

## Acceptance Criteria

- Реестр внешних источников создан с минимальными метаданными и фильтрацией по
  тегам/проектам.
- Механизм инсайтов описан и снабжён 3 примерами с разными стадиями lifecycle.
- Модель Base + Local Extension и роль Smart Sync описаны без новой
  инфраструктуры.
- Применение для 4 проектов экосистемы предложено.
- Артефакты зарегистрированы в `pr-ops/artifact-map.md`, навигации и
  валидаторе; lifecycle-привязка явная.
- CI-скраперы и автосбор контента отсутствуют (Anti-Inflation).

## Open Decision (за человеком)

1. Принять `research/external-knowledge/` как доменный подкаталог реестра внешних
   знаний (Creative override от путей в issue)?
2. Оставить реестр и инсайты в статусе `draft` до первого применения в проекте,
   или сразу инициировать Local Extension в одном из споков?
3. Делегировать ли обязательную норму реестра в `standards/research-profile.md`
   (поле `external-sources`) или оставить механизм на уровне research до накопления
   практики?

## Связанные артефакты

- [research/external-knowledge/README.md](../../research/external-knowledge/README.md) — навигация направления.
- [research/external-knowledge/external-sources-registry.md](../../research/external-knowledge/external-sources-registry.md) — Base Registry.
- [research/external-knowledge/external-insights/README.md](../../research/external-knowledge/external-insights/README.md) — механизм инсайтов.
- [docs/rfc/knowledge-lifecycle-proposal.md](knowledge-lifecycle-proposal.md) — жизненный цикл знаний.
- [docs/rfc/resolve-artifact-location-proposal.md](resolve-artifact-location-proposal.md) — выбор расположения артефакта.
- [pr-ops/repo-model.md](../../pr-ops/repo-model.md) — Anti-Inflation principle.
- [practices/README.md](../../practices/README.md) — fixed practices KB.
