---
status: canonical
version: 1.2
updated: 2026-06-25
temperature: 0.1
---

# hybrid-Intelligence-lab

> **«Человек задаёт смысл, AI ускоряет путь — вместе по правилам»** — слоган
> Хаба и формула гибридной работы человек + AI. Зафиксирован для Хаба и
> наследуется всеми HTOM-командами (геном [`templates/htom/`](templates/htom/)).

`hybrid-Intelligence-lab` - governance-first knowledge hub для исследований,
образования, стандартов, проектных knowledge bases и управляемой работы
гибридных human + AI команд.

Репозиторий не является production-кодовой базой. Production-системы,
клиентские реализации и приложения с собственным жизненным циклом должны жить
в отдельных spoke-репозиториях и ссылаться сюда как на источник переиспользуемых
знаний и правил работы.

> **🛫 Новый агент? Начни здесь → [`ai-rules/agent-onboarding-protocol.md`](ai-rules/agent-onboarding-protocol.md).**
> Это обязательный предполётный чек-лист *Runtime-онбординга* (Кейс 1): любой
> ИИ-агент проходит его, получив ссылку на репозиторий, **до** первого изменения
> файлов.

## Ключевые документы

| Документ | Назначение |
| --- | --- |
| [docs/concept.md](docs/concept.md) | Актуальная концепция репозитория, аудитории, границы и модель hub-and-spoke. |
| [AI_GOVERNANCE.md](AI_GOVERNANCE.md) | Операционный контракт для Founder & PO, reviewers, contributors и AI-агентов. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Правила участия, локальные проверки и ожидания к review. |
| [CHANGELOG.md](CHANGELOG.md) | Date-based журнал governance-изменений репозитория. |
| [LICENSE](LICENSE) | Текущий статус лицензии и pending-решение Founder & PO. |
| [standards/README.md](standards/README.md) | Таблица активных и планируемых стандартов. |
| [standards/file-naming.md](standards/file-naming.md) | Правила именования файлов, включая date-first research/analysis/RFC/ADR артефакты. |
| [standards/glossary.md](standards/glossary.md) | Единый словарь терминов для standards, governance и AI-assisted work. |
| [standards/frontmatter-standard.md](standards/frontmatter-standard.md) | Минимальный frontmatter для Markdown-артефактов: `status`, `version`, `updated`, `temperature`. |
| [practices/README.md](practices/README.md) | Каталог фиксированных практик: отдельный KB-слой между research, templates и проектными адаптациями. |
| [standards/team-contract.md](standards/team-contract.md) | Шаблон и инструкция для создания project-level `CONTRIBUTING.md` и `AI_GOVERNANCE.md`. |
| [ai-rules/agent-onboarding-protocol.md](ai-rules/agent-onboarding-protocol.md) | Обязательный предполётный протокол для нового ИИ-агента (*Runtime-онбординг*, Кейс 1): Handover Prompt, 4-шаговый чек-лист и стоп до апрува. |
| [pr-ops/repo-model.md](pr-ops/repo-model.md) | Модель структуры репозитория и Anti-Inflation правило. |
| [pr-ops/artifact-map.md](pr-ops/artifact-map.md) | Карта артефактов: где что лежит, зачем нужно и как связано. |
| [templates/htom/](templates/htom/) | Геном **HTOM-команды** — минимальный governance-скелет для гибридной human + AI работы (*Bootstrap-клонирование*, Кейс 2). Точка входа: `templates/htom/README.md`. |
| [templates/spoke/](templates/spoke/) | Шаблон **production-спока** — репозитория с собственным кодом и жизненным циклом. Точка входа: `templates/spoke/README.md`. Различие HTOM-команда vs spoke — в [RFC](docs/rfc/htom-vs-spoke-clarification-2026-06.md). |

## Продукт и гайды

| Документ | Назначение |
| --- | --- |
| [docs/vision.md](docs/vision.md) | Product Vision (L1) Хаба: зачем он существует, для кого и какую ценность создаёт (1 страница). |
| [docs/product-concept.md](docs/product-concept.md) | Product Concept (L2): персоны, сценарии, ключевые возможности, метрики и дорожная карта. |
| [docs/ecosystem-map.md](docs/ecosystem-map.md) | Экосистемная карта: полный граф проектов, их связи и принцип Need-to-Know. |
| [guides/README.md](guides/README.md) | Библиотека человекочитаемых гайдов «как это сделать»: быстрый старт, синхронизация, развёртывание, решение проблем. |

## Структура

| Путь | Роль |
| --- | --- |
| `standards/` | Плоский реестр стандартов, шаблонов и правил оформления артефактов. |
| `research/` | Исследования по доменам и source-backed анализ. |
| `practices/` | Фиксированные атомарные практики для импорта в проекты после research review. |
| `frameworks/` | Методологии, создаваемые только после доказанного gap с существующими подходами. |
| `projects/` | Project knowledge bases, промпты, процессы и контекст spoke-репозиториев. |
| `education/` | Open education: программы, учебные материалы и сценарии занятий. |
| `ai-governance/` | Якорь AI-governance слоя: границы и точки входа (сквозные правила — в `AI_GOVERNANCE.md`). |
| `ai-rules/` | Исполнимые правила рантайма AI-агента: протокол онбординга и операционные инструкции. |
| `pr-ops/` | Операции над репозиторием и PR: модель репозитория, карта артефактов, бэклог, реестры и журнал сессий. |
| `projects-sink/` | Приёмник контекста spoke-проектов, синхронизируемого в Хаб. |
| `tools/` | Локальные проверки и служебные скрипты сопровождения репозитория. |
| `.github/ISSUE_TEMPLATE/` | GitHub-native структура постановки задач. |

## Шаблоны задач

| Шаблон | Когда использовать |
| --- | --- |
| [.github/ISSUE_TEMPLATE/task.md](.github/ISSUE_TEMPLATE/task.md) | Structured task: понятный scope, артефакты, ограничения и измеримый Definition of Done. |
| [.github/ISSUE_TEMPLATE/task-creative.md](.github/ISSUE_TEMPLATE/task-creative.md) | Creative task: задана цель и критерии качества, а способ решения оставлен исполнителю. |
| [.github/ISSUE_TEMPLATE/task.yml](.github/ISSUE_TEMPLATE/task.yml) | GitHub-native форма для задач в UI. |

## Проекты

| Проект | Назначение |
| --- | --- |
| [projects/README.md](projects/README.md) | Навигация по проектным рабочим областям и правило выбора `/projects` vs spoke-репозиторий. |
| [projects/repo-development/README.md](projects/repo-development/README.md) | Развитие самого репозитория: аудит миграции, согласованность и предложения по оптимизации. |
| [projects/education-ba-prompt/README.md](projects/education-ba-prompt/README.md) | Песочница идей, терминов, кейсов и шаблонов для будущего курса БА по промпт-инжинирингу. |
| [mango_ba_prompts](https://github.com/G-Ivan-A/mango_ba_prompts) | Мигрировавший spoke-репозиторий Mango; прежняя архивная копия удалена из Хаба, история доступна через git. |

## Исследования

| Направление | Назначение |
| --- | --- |
| [research/README.md](research/README.md) | Навигация по исследовательским направлениям и правилам воспроизводимости. |
| [research/hub/README.md](research/hub/README.md) | Исследования Хаба: governance, практики agent work, международные AI governance sources и проектный bootstrap. |
| [research/mango/README.md](research/mango/README.md) | Активные исследования Mango: классификация продуктов, анализ корпуса ТЗ и flow требований. |

## Состояние миграции

Cleanup issue #49 завершает миграцию предыдущей структуры: legacy files с
суффиксом `-old` удалены или перенесены в active paths с указанием `source` во
frontmatter. Исторический контекст и решение по категориям зафиксированы в
[projects/repo-development/docs/migration-audit-2026-05.md](projects/repo-development/docs/migration-audit-2026-05.md).

Новые артефакты добавляются только тогда, когда решают операционную проблему,
и должны ссылаться на ближайший стандарт или governance-правило.

## Локальная проверка

```bash
./tools/validate-file-naming.sh
./tools/validate-frontmatter.sh .
./tools/validate-repository-structure.sh
```
