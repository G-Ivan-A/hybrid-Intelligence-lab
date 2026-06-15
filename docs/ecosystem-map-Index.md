---
status: draft
version: 0.1
updated: 2026-06-15
temperature: 0.1
ai-generated: true
---

# Экосистемная карта — Index

> 🧭 **Уровень детализации: Index.** Это минимальная навигационная точка входа в
> экосистему: одна строка на проект, по которой агент или человек решает, **в
> какой `-Summary` идти дальше**, не читая полные репозитории. Уровень `Full`
> (граф связей, Need-to-Know, roadmap) — в [ecosystem-map.md](ecosystem-map.md).
> Рамка уровней `Index → Summary → Full` — в
> [standards/file-naming.md](../standards/file-naming.md), раздел про суффиксы.

## Карта проектов

| Проект | URL | Текущая фаза | Ключевые теги | Ссылка на Summary |
| --- | --- | --- | --- | --- |
| hybrid-Intelligence-lab (Хаб) | [github](https://github.com/G-Ivan-A/hybrid-Intelligence-lab) | Sprint 3 «Hybrid Minimum Bootstrap» | `hub`, `governance`, `knowledge-lifecycle`, `external-knowledge` | [AI_PROJECT_CONTEXT-Summary.md](../AI_PROJECT_CONTEXT-Summary.md) |
| mango_ba_prompts | [github](https://github.com/G-Ivan-A/mango_ba_prompts) | Фаза 1 — миграция в standalone-спок | `ba-prompts`, `mango`, `taxonomy`, `github-pages` | [staging](project-summaries/mango-ba-prompts-context-Summary.md) → `mango_ba_prompts/AI_PROJECT_CONTEXT-Summary.md` |
| open-ai.ru | [github](https://github.com/G-Ivan-A/open-ai.ru) | Phase 0 — Planning & Vision | `ai-native`, `hybrid-teams`, `product`, `bootstrap` | [staging](project-summaries/open-ai-ru-context-Summary.md) → `open-ai.ru/AI_PROJECT_CONTEXT-Summary.md` |
| clarify-engine-ai | [github](https://github.com/G-Ivan-A/clarify-engine-ai) | MVP/Pilot — CONCEPT v2.6 Approved | `rag`, `tender-analysis`, `human-in-the-loop`, `hybrid-search` | [staging](project-summaries/clarify-engine-ai-context-Summary.md) → `clarify-engine-ai/AI_PROJECT_CONTEXT-Summary.md` |

> ⚠️ **Staging vs канон.** Карты `-Summary` спок-проектов созданы в Хабе как
> источник истины и физически лежат в
> [docs/project-summaries/](project-summaries/README.md). Их каноническое место —
> корень соответствующего репозитория (`AI_PROJECT_CONTEXT-Summary.md`);
> распространение туда идёт отдельными PR (у задачи в Хабе нет прав записи в
> споки). Карта Хаба уже живёт в корне Хаба.

## Как пользоваться

1. Нашёл нужный проект по фазе или тегам в таблице.
2. Перешёл в его `-Summary` — получил цель, фокус, активные стандарты и границы.
3. Нужны детали связей и синхронизации? → [ecosystem-map.md](ecosystem-map.md)
   (уровень `Full`).

## Связанные документы

- [docs/ecosystem-map.md](ecosystem-map.md) — полный граф экосистемы (`Full`).
- [docs/project-summaries/README.md](project-summaries/README.md) — staging карт
  спок-проектов.
- [standards/file-naming.md](../standards/file-naming.md) — правило суффиксов
  `-Index` / `-Summary` / `-Full`.
