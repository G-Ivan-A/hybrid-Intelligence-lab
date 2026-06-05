---
status: canonical
version: 1.1
updated: 2026-06-05
ai-generated: false
source: projects/README-old.md
---

# Projects

Каталог для проектных рабочих областей: промптов, баз знаний, процессов,
прототипов и интеграционных контуров.

## Когда использовать `/projects`

Используйте этот каталог, если задача:

- требует собственного контекста для AI-агентов;
- связана с промптами или knowledge base для конкретного домена;
- еще не доросла до отдельного production-репозитория;
- должна ссылаться на материалы из `frameworks/`, `research/` или `education/`.

## Когда выносить в отдельный spoke-репозиторий

Проект лучше вынести отдельно, если у него есть:

| Признак | Почему это spoke |
| --- | --- |
| Production-код | Нужны отдельные CI/CD, secrets, runtime и release lifecycle. |
| Отдельная команда | Нужны собственные issue templates, ownership и roadmap. |
| Закрытый контекст | Нельзя смешивать с open education/research. |
| Долгий жизненный цикл | Требуется самостоятельная история решений, контрактов и версий. |

## Рекомендуемая структура проекта

Подкаталоги проекта наследуют структуру репозитория по
[standards/PROJECT_STRUCTURE_INHERITANCE.md](../standards/PROJECT_STRUCTURE_INHERITANCE.md):
проект может добавлять `standards/`, `kb/`, `prompts/`, `docs/`,
`experiments/` и `decisions/` только в области своего проекта и без
обязательных зависимостей для других проектов.

```text
projects/<project-slug>/
  README.md
  standards/
  kb/
  prompts/
  docs/
  experiments/
  decisions/
```

## Активные проекты

| Проект | Назначение |
| --- | --- |
| [repo-development/](repo-development/) | Развитие структуры, governance и локальных проверок самого репозитория. |

## Мигрировавшие проекты

| Проект | Статус | Новый репозиторий | Дата миграции |
|--------|--------|-------------------|---------------|
| Mango | ✅ Мигрировал | [mango_ba_prompts](https://github.com/G-Ivan-A/mango_ba_prompts) | 2026-06-05 |

Архивная версия: `archive/projects/mango/` (только для истории, не для разработки).
