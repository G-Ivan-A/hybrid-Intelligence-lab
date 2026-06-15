---
status: draft
version: 0.1
updated: 2026-06-15
temperature: 0.1
ai-generated: true
---

# Project Summaries (hub-side staging)

Здесь Хаб хранит **исходные копии** карт `AI_PROJECT_CONTEXT-Summary` для
спок-проектов экосистемы (`mango_ba_prompts`, `open-ai.ru`, `clarify-engine-ai`).

> 🧭 **Зачем staging в Хабе.** По принципу **Need-to-Know**
> ([docs/ecosystem-map.md](../ecosystem-map.md)) Хаб держит полный граф
> экосистемы. Карта `-Summary` каждого спока создаётся здесь как источник истины,
> а её **каноническое место — корень соответствующего репозитория** под именем
> `AI_PROJECT_CONTEXT-Summary.md`. Распространение в споки идёт через
> human-in-control Smart Sync (Хаб предлагает → человек подтверждает в споке),
> как описано в [docs/ecosystem-map.md](../ecosystem-map.md), раздел
> «Принцип Need-to-Know».

> ⚠️ **Статус распространения.** Эти файлы созданы в Хабе в рамках issue #235.
> Применение в корни внешних репозиториев `mango_ba_prompts`, `open-ai.ru`,
> `clarify-engine-ai` выполняется отдельными PR в этих репозиториях (у задачи в
> Хабе нет прав записи в них). Карта Хаба живёт в корне Хаба:
> [AI_PROJECT_CONTEXT-Summary.md](../../AI_PROJECT_CONTEXT-Summary.md).

## Сопоставление staging → каноническое место

| Staging-файл (Хаб) | Каноническое место (спок) |
| --- | --- |
| [mango-ba-prompts-context-Summary.md](mango-ba-prompts-context-Summary.md) | `mango_ba_prompts/AI_PROJECT_CONTEXT-Summary.md` |
| [open-ai-ru-context-Summary.md](open-ai-ru-context-Summary.md) | `open-ai.ru/AI_PROJECT_CONTEXT-Summary.md` |
| [clarify-engine-ai-context-Summary.md](clarify-engine-ai-context-Summary.md) | `clarify-engine-ai/AI_PROJECT_CONTEXT-Summary.md` |

Имена staging-файлов следуют правилу вложенных файлов
([standards/file-naming.md](../../standards/file-naming.md)): `lowercase` базовое
имя + суффикс уровня детализации `-Summary` в `PascalCase`.
