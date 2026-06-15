---
status: draft
version: 0.2
updated: 2026-06-15
temperature: 0.1
ai-generated: true
type: external-analysis
context: [external-knowledge, registry, hub, ecosystem, lifecycle]
method: comparative-analysis
scope: repo-wide
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/227"
related_artifacts:
  - "research/external-knowledge/README.md"
  - "research/external-knowledge/external-insights/README.md"
  - "governance/rfc/external-knowledge-integration.md"
  - "governance/rfc/knowledge-lifecycle-proposal.md"
  - "standards/research-profile.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/227"
---

# Реестр внешних источников

Единый **Base Registry** внешних источников знаний экосистемы. Реестр отвечает
на один вопрос: *какие внешние источники мы считаем ценными, в какой они стадии
жизненного цикла и каким проектам релевантны* — без загрузки полного текста
источников в контекст агента.

> 🧭 **Принцип фильтрации.** Агент читает не весь реестр, а строки, отобранные по
> колонке «Теги» и «Проекты». Это держит контекст компактным (Anti-Inflation,
> см. [governance/repo-model.md](../../governance/repo-model.md)).

> ⛔ **Статус ≠ практика.** Запись в реестре означает «источник замечен и
> оценён», а не «практика принята». Перевод инсайта в `practices/`/`standards/`
> идёт только через валидацию по
> [governance/rfc/knowledge-lifecycle-proposal.md](../../governance/rfc/knowledge-lifecycle-proposal.md).

## Минимальные метаданные

Каждая запись использует ровно столько полей, сколько нужно для **фильтрации** и
**синхронизации**. Расширять состав можно только при доказанной операционной
потребности (Anti-Inflation).

| Поле | Назначение | Значения |
| --- | --- | --- |
| `id` | Стабильный якорь для ссылок из инсайтов и проектов. | `ext-NNN` (сквозная нумерация). |
| Источник | Человекочитаемое имя + ссылка на первоисточник. | Markdown-ссылка. |
| Тип | Класс источника для грубой фильтрации. | `github` · `blog` · `habr` · `standard` · `paper` · `docs`. |
| Язык | Язык первоисточника — для фильтрации и Traceability. | `ru` · `en` · др. |
| Теги | Тематические метки для отбора агентами и проектами. | `kebab-case`, через запятую. |
| Stage | Стадия жизненного цикла знания (см. lifecycle). | `observation` · `research` · `hypothesis` · `deprecated`. |
| Проекты | Кому источник релевантен. | `hub` · `mango` · `open-ai.ru` · `clarify-engine-ai` · `all`. |
| Запись в БЗ | Есть ли извлечённый инсайт в базе знаний и ссылка на него. | `✅` + путь в `external-insights/` · `❌` (бесполезен/не извлечён). |

> 📌 **Почему `stage` не идёт дальше `hypothesis` в реестре.** Реестр фиксирует
> только стадии «наблюдения и исследования». Стадии `rfc → pattern → standard`
> живут в `governance/rfc/`, `practices/` и `standards/` — у реестра нет права
> «протащить» источник в практику в обход валидации человеком.

## Реестр

| `id` | Источник | Тип | Язык | Теги | Stage | Проекты | Запись в БЗ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ext-001` | [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) | `blog` | `en` | `agents, workflow-patterns, orchestration, hybrid-collaboration` | `research` | `all` | ✅ [building-effective-agents-2026-06.md](external-insights/building-effective-agents-2026-06.md) |
| `ext-002` | [12-Factor Agents (HumanLayer)](https://github.com/humanlayer/12-factor-agents) | `github` | `en` | `agents, production, prompt-ownership, human-in-the-loop` | `research` | `all` | ✅ [12-factor-agents-2026-06.md](external-insights/12-factor-agents-2026-06.md) |
| `ext-003` | [GitHub Spec Kit (Spec-Driven Development)](https://github.com/github/spec-kit) | `github` | `en` | `spec-driven, requirements, agents, executable-spec` | `hypothesis` | `mango, clarify-engine-ai` | ✅ [spec-driven-development-2026-06.md](external-insights/spec-driven-development-2026-06.md) |
| `ext-004` | [Anthropic — Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) | `blog` | `en` | `agents, coding-agent, workflow, tooling` | `observation` | `hub, open-ai.ru` | ❌ |
| `ext-005` | [OpenAI — A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | `paper` | `en` | `agents, guardrails, orchestration` | `observation` | `all` | ❌ |
| `ext-006` | [Diátaxis — documentation framework](https://diataxis.fr/) | `docs` | `en` | `documentation, tutorials, reference, knowledge-structure` | `observation` | `hub` | ❌ |
| `ext-007` | [Habr — Контекст-инжиниринг для AI-агентов](https://habr.com/ru/companies/ru_mts/articles/) | `habr` | `ru` | `context-engineering, agents, ru-community` | `observation` | `hub, mango` | ❌ |
| `ext-008` | [Anthropic — Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | `blog` | `en` | `context-engineering, agents, token-budget` | `observation` | `all` | ❌ |
| `ext-009` | [Habr — Codex и локальная память на SQLite (Hermes Codex Plugin)](https://habr.com/ru/articles/1045262/) | `habr` | `ru` | `context-engineering, agent-memory, token-budget, mcp, project-rules` | `research` | `hub, mango, open-ai.ru, clarify-engine-ai` | ✅ [agent-local-memory-context-2026-06.md](external-insights/agent-local-memory-context-2026-06.md) |
| `ext-010` | [Habr — Паттерн экономии токенов в Claude Code на правке файлов](https://habr.com/ru/articles/1045186/) | `habr` | `ru` | `token-budget, claude-code, file-editing, tool-specific` | `observation` | `hub` | ❌ (бесполезен) |
| `ext-011` | [Habr — Структурированная разработка на основе промптов (SPDD)](https://habr.com/ru/articles/1045060/) | `habr` | `ru` | `spec-driven, prompts-as-artifacts, reproducibility, workflow` | `research` | `hub, mango, clarify-engine-ai, open-ai.ru` | ✅ [structured-prompt-driven-development-2026-06.md](external-insights/structured-prompt-driven-development-2026-06.md) |

> 🔗 **Ссылки сознательно не загружаются автоматически.** Реестр — это карта, а
> не зеркало контента. Скрапинг и кэширование первоисточников запрещены
> (Anti-Inflation НФТ задачи); агент или человек открывает ссылку вручную, когда
> источник релевантен.

## Как добавить источник

1. Проверь, что источник действительно полезен экосистеме (не дублирует уже
   принятую практику).
2. Добавь строку в таблицу с новым `id` (`ext-NNN`), минимальными метаданными и
   `stage: observation`.
3. Если из источника извлечён конкретный вывод — создай инсайт в
   [external-insights/](external-insights/), проставь `✅` и ссылку в колонке
   «Запись в БЗ». Если источник бесполезен — оставь `❌ (бесполезен)`, инсайт не
   создавай (Anti-Inflation).
4. Если источник относится только к одному проекту — он может жить в **Local
   Extension** проекта (`research/<project>/external-sources-registry.md` в споке),
   а в Base Registry попадает лишь при общей ценности (см.
   [governance/rfc/external-knowledge-integration.md](../../governance/rfc/external-knowledge-integration.md)).
5. Обнови `updated` во frontmatter.

## Как использовать (для агентов)

- Нужны паттерны агентов? → фильтруй по тегу `agents`.
- Работаешь над требованиями Mango? → фильтруй `Проекты ⊇ mango`.
- Нужен только зрелый материал? → бери `stage: research`, пропускай
  `observation`.
- Нашёл готовый вывод? → открывай связанный инсайт, а не первоисточник.

## Связанные артефакты

- [research/external-knowledge/README.md](README.md) — навигация направления.
- [external-insights/README.md](external-insights/README.md) — механизм инсайтов.
- [governance/rfc/external-knowledge-integration.md](../../governance/rfc/external-knowledge-integration.md) — RFC интеграции и Base + Local Extension.
- [governance/rfc/knowledge-lifecycle-proposal.md](../../governance/rfc/knowledge-lifecycle-proposal.md) — жизненный цикл знаний.
- [standards/research-profile.md](../../standards/research-profile.md) — правила цитирования и frontmatter.
