---
status: canonical
version: 1.2
updated: 2026-06-09
temperature: 0.1
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

## Классификация: HTOM-команда vs Spoke

Слово «проект» раньше смешивало два разных типа. Их различает
[RFC htom-vs-spoke](../governance/rfc/htom-vs-spoke-clarification-2026-06.md):

- **HTOM-команда** — гибридная human + AI рабочая единица, наследующая
  governance-геном [`templates/htom/`](../templates/htom/). Сюда относятся
  knowledge-base проекты, промпт-наборы и сам Хаб.
- **Spoke-репозиторий** — production-репозиторий с собственным кодом, CI/CD и
  release lifecycle, создаётся из [`templates/spoke/`](../templates/spoke/) и
  ссылается на Хаб как на источник правил.

| Текущий проект | Тип | Обоснование |
| --- | --- | --- |
| `hybrid-Intelligence-lab` (Хаб) | HTOM-команда | Governance-first knowledge hub без production-кода. |
| `repo-development` | HTOM-команда | Развитие governance и проверок самого Хаба, кода-продукта нет. |
| `mango_ba_prompts` | HTOM-команда | Промпт- и knowledge-репозиторий БА, гибридная human + AI работа. |
| `open-ai.ru` | Spoke | Первый реальный production-спок с собственным кодом и жизненным циклом. |

## Рекомендуемая структура проекта

Подкаталоги проекта наследуют структуру репозитория по
[standards/project-structure-inheritance.md](../standards/project-structure-inheritance.md):
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

Прежняя архивная копия в Хабе удалена; история доступна через git, рабочая версия
живёт во внешнем spoke-репозитории `mango_ba_prompts`.
