---
status: draft
version: 0.1
updated: {{date}}
ai-generated: true
---

# {{project_name}}

> Spoke-проект, рождённый из Хаба `hybrid-Intelligence-lab` по «ДНК-шаблону»
> (`templates/spoke/`). Минимальный, но «правильный» геном: правила, контакт с
> Хабом и каркас для роста по запросу.

{{project_description}}

## 🧬 Связь с Хабом

| Что | Где |
| --- | --- |
| Источник истины (governance, стандарты, research) | [{{hub_url}}]({{hub_url}}) |
| Фундаментальные знания | `research/` Хаба (в споке `research/` **не создаётся**) |
| Операционный контракт проекта | [AI_GOVERNANCE.md](AI_GOVERNANCE.md) |
| Быстрые правила для агента | [AI_QUICK_RULES.md](AI_QUICK_RULES.md) |
| «Доверенность» для запуска агента (Handover Prompt) | [AI_HANDOVER_PROMPT.md](AI_HANDOVER_PROMPT.md) |

## 🗂️ Структура (сейчас)

| Путь | Роль |
| --- | --- |
| `AI_GOVERNANCE.md` | Конституция проекта: роли, правила, эскалация, DoD. |
| `AI_QUICK_RULES.md` | Одностраничная инструкция для AI-агента. |
| `AI_HANDOVER_PROMPT.md` | Готовый *Handover Prompt* (`{{REPO_NAME}}`) для запуска агента; копия хабового шаблона. |
| `CONTRIBUTING.md` | Workflow вклада: issue → PR → review. |
| `CHANGELOG.md` | Память проекта: журнал значимых изменений. |
| `docs/adr/` | Architecture Decision Records — «почему», а не только «что». |
| `docs/audit/` | Ревизии, аудиты и проверки соответствия. |
| `.github/ISSUE_TEMPLATE/` | Шаблон постановки задач (язык Хаба). |
| `tools/` | Локальные проверки структуры репозитория. |

Каталоги создаются по запросу, при появлении операционной боли (Anti-Inflation
principle Хаба). Пустые «органеллы» спок не носит с собой.

## ✅ Локальная проверка

```bash
./tools/validate-repository-structure.sh
```
