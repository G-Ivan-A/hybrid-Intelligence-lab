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

> **🛫 Новый агент? Начни здесь → [`governance/agent-onboarding-protocol.md`](governance/agent-onboarding-protocol.md).**
> Это обязательный предполётный чек-лист *Runtime-онбординга* (Кейс 1): любой
> ИИ-агент проходит его, получив ссылку на репозиторий, **до** первого изменения
> файлов.

## Ключевые документы

| Документ | Назначение |
| --- | --- |
| [CONCEPT.md](CONCEPT.md) | Актуальная концепция репозитория, аудитории, границы и модель hub-and-spoke. |
| [AI_GOVERNANCE.md](AI_GOVERNANCE.md) | Операционный контракт для Founder & PO, reviewers, contributors и AI-агентов. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Правила участия, локальные проверки и ожидания к review. |
| [CHANGELOG.md](CHANGELOG.md) | Date-based журнал governance-изменений репозитория. |
| [LICENSE](LICENSE) | Текущий статус лицензии и pending-решение Founder & PO. |
| [standards/README.md](standards/README.md) | Таблица активных и планируемых стандартов. |
| [standards/glossary.md](standards/glossary.md) | Единый словарь терминов для standards, governance и AI-assisted work. |
| [standards/team-contract.md](standards/team-contract.md) | Шаблон и инструкция для создания project-level `CONTRIBUTING.md` и `AI_GOVERNANCE.md`. |
| [governance/agent-onboarding-protocol.md](governance/agent-onboarding-protocol.md) | Обязательный предполётный протокол для нового ИИ-агента (*Runtime-онбординг*, Кейс 1): Handover Prompt, 4-шаговый чек-лист и стоп до апрува. |
| [governance/repo-model.md](governance/repo-model.md) | Модель структуры репозитория и Anti-Inflation правило. |
| [governance/artifact-map.md](governance/artifact-map.md) | Карта артефактов: где что лежит, зачем нужно и как связано. |
| [templates/htom/](templates/htom/) | Геном **HTOM-команды** — минимальный governance-скелет для гибридной human + AI работы (*Bootstrap-клонирование*, Кейс 2). Точка входа: `templates/htom/README.md`. |
| [templates/spoke/](templates/spoke/) | Шаблон **production-спока** — репозитория с собственным кодом и жизненным циклом. Точка входа: `templates/spoke/README.md`. Различие HTOM-команда vs spoke — в [RFC](governance/rfc/htom-vs-spoke-clarification-2026-06.md). |

## Продукт и гайды

| Документ | Назначение |
| --- | --- |
| [docs/vision.md](docs/vision.md) | Product Vision (L1) Хаба: зачем он существует, для кого и какую ценность создаёт (1 страница). |
| [docs/product-concept.md](docs/product-concept.md) | Product Concept (L2): персоны, сценарии, ключевые возможности, метрики и дорожная карта. |
| [guides/README.md](guides/README.md) | Библиотека человекочитаемых гайдов «как это сделать»: быстрый старт, синхронизация, развёртывание, решение проблем. |

Разделы `guides/` и `research/` дополнительно публикуются как сайт MkDocs через
GitHub Pages (см. [`mkdocs.yml`](mkdocs.yml) и
[`.github/workflows/deploy-docs.yml`](.github/workflows/deploy-docs.yml)).

## Структура

| Путь | Роль |
| --- | --- |
| `standards/` | Плоский реестр стандартов, шаблонов и правил оформления артефактов. |
| `research/` | Исследования по доменам и source-backed анализ. |
| `frameworks/` | Методологии, создаваемые только после доказанного gap с существующими подходами. |
| `projects/` | Project knowledge bases, промпты, процессы и контекст spoke-репозиториев. |
| `education/` | Open education: программы, учебные материалы и сценарии занятий. |
| `governance/` | Модель репозитория, операционные решения и сквозные governance-правила. |
| `tools/` | Локальные проверки и служебные скрипты сопровождения репозитория. |
| `.github/ISSUE_TEMPLATE/` | GitHub-native структура постановки задач. |

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
./tools/validate-frontmatter.sh .
./tools/validate-repository-structure.sh
```
