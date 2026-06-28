---
status: draft
version: 0.2
updated: 2026-06-15
temperature: 0.1
---

# External Insights

Механизм хранения **извлечённых инсайтов** из внешних источников. Один инсайт —
один файл. Инсайт фиксирует *конкретный вывод*, пригодный для экосистемы, и его
стадию жизненного цикла — от наблюдения до кандидата в практику.

> 🧭 **Зачем отдельно от реестра.** Реестр
> [external-sources-registry.md](../external-sources-registry.md) отвечает «какие
> источники существуют», а инсайт — «что именно мы из источника берём и зачем».
> Это разные слои: реестр компактен и сканируется целиком, инсайт читается только
> когда тема релевантна.

## Модель инсайта

| Свойство | Правило |
| --- | --- |
| Атомарность | Один инсайт = один проверяемый вывод (а не пересказ статьи). |
| Привязка к источнику | Поле `source_id` ссылается на `id` записи в реестре. |
| Стадия lifecycle | Поле `stage` отражает зрелость вывода (см. ниже). |
| Целевые проекты | Поле `projects` фиксирует, кому вывод релевантен. |
| Путь к практике | Секция «Путь к практике» описывает, что нужно для валидации. |

## Frontmatter инсайта

```yaml
---
status: draft | reviewed
version: 0.1
updated: YYYY-MM-DD
temperature: 0.1
type: external-analysis
source_id: ext-NNN
stage: observation | research | hypothesis | candidate-practice
projects: [hub, mango, open-ai.ru, clarify-engine-ai]
context: [tag1, tag2]
---
```

## Стадии жизненного цикла инсайта

Подмножество цепочки из
[governance/rfc/knowledge-lifecycle-proposal.md](../../../governance/rfc/knowledge-lifecycle-proposal.md),
ограниченное стадиями, за которые отвечает `research/`:

| `stage` | Что означает | Что нужно для перехода дальше |
| --- | --- | --- |
| `observation` | Источник замечен, вывод сформулирован, но не проверен. | Сопоставление с практикой Хаба, поиск противоречий. |
| `research` | Вывод сопоставлен с контекстом экосистемы, есть аргументы за/против. | Гипотеза о применении в конкретном проекте. |
| `hypothesis` | Есть конкретная гипотеза применения и критерий проверки. | Пилот/эксперимент или RFC. |
| `candidate-practice` | Вывод подтверждён и предложен к переводу в `practices/`/`standards/`. | **Решение человека** (валидация и явное одобрение). |

> ⛔ **Стоп-правило.** Инсайт не переводит сам себя в практику. `candidate-practice`
> — это максимум, что делает `research/`; дальше требуется reviewable PR в
> `practices/`/`standards/` и решение человека
> ([AI_GOVERNANCE.md](../../../AI_GOVERNANCE.md)).

## Текущие инсайты

| Инсайт | Источник | Stage | Проекты |
| --- | --- | --- | --- |
| [2026-06-13-building-effective-agents.md](2026-06-13-building-effective-agents.md) | `ext-001` | `research` | `all` |
| [2026-06-13-12-factor-agents.md](2026-06-13-12-factor-agents.md) | `ext-002` | `research` | `all` |
| [2026-06-13-spec-driven-development.md](2026-06-13-spec-driven-development.md) | `ext-003` | `hypothesis` | `mango, clarify-engine-ai` |
| [2026-06-15-agent-local-memory-context.md](2026-06-15-agent-local-memory-context.md) | `ext-009` | `research` | `all` |
| [2026-06-15-structured-prompt-driven-development.md](2026-06-15-structured-prompt-driven-development.md) | `ext-011` | `research` | `hub, mango, clarify-engine-ai, open-ai.ru` |

## Как добавить инсайт

1. Убедись, что источник есть в
   [реестре](../external-sources-registry.md) (если нет — добавь запись).
2. Создай файл `<slug>-YYYY-MM.md` с frontmatter выше.
3. Сформулируй один атомарный вывод, аргументы и «Путь к практике».
4. Проставь `✅` и ссылку на инсайт в колонке «Запись в БЗ»
   [реестра](../external-sources-registry.md) и добавь строку в таблицу выше.
5. Обнови `updated`.
