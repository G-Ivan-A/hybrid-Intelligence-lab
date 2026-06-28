---
status: canonical
version: 1.1
updated: 2026-06-15
temperature: 0.1
---

# Проект: Развитие репозитория

Версия: 1.1

Дата: 2026-06-15

`projects/repo-development/` координирует работы по эволюции структуры,
стандартов и процессов самого репозитория `hybrid-Intelligence-lab`. В отличие
от продуктовых spoke-проектов (например, `mango_ba_prompts`), этот проект
рассматривает сам hub как объект развития: его навигацию, governance-правила и
миграцию.

Файл является навигацией, а не контрактом: обязательные правила остаются в
[CONCEPT.md](../../CONCEPT.md), [governance/repo-model.md](../../governance/repo-model.md)
и [standards/README.md](../../standards/README.md).

## 🎯 Назначение

Координация работ по эволюции структуры, стандартов и процессов репозитория:
аудит согласованности, cleanup legacy-файлов после миграции и сбор предложений
по оптимизации без их немедленной реализации.

## 📋 Текущие приоритеты

- Аудит согласованности миграции (см. отчёт ниже).
- Предложения по оптимизации — фиксируются как рекомендации, реализуются только
  после согласования.
- Поддержание active структуры после cleanup issue #49: новые legacy-файлы не
  добавляются без отдельного migration issue.

## 🗂️ Навигация

| Документ | Назначение |
| --- | --- |
| [docs/migration-audit-2026-05.md](docs/migration-audit-2026-05.md) | Отчёт аудита миграции: согласованность с `CONCEPT.md`, матрица ссылок, таблица `-old`, рекомендации. |
| [docs/contract-violations-self-report-2026-06.md](docs/contract-violations-self-report-2026-06.md) | Self-report (`type: audit`) ошибок исполнения контрактов в сессии миграции Mango: обоснование таргета, 6 нарушений, системные выводы и анализ размещения ретроспектив. |
| [docs/mango-ba-prompts-repository-migration-plan-2026-06.md](docs/mango-ba-prompts-repository-migration-plan-2026-06.md) | План миграции `mango_ba_prompts` к Repository Archetype Standard: применение merged Task 2 RFC, gap analysis, сравнение сценариев, рекомендация и checklist исполнения. |
| [governance/repo-model.md](../../governance/repo-model.md) | Модель структуры репозитория и Anti-Inflation principle. |
| [governance/artifact-map.md](../../governance/artifact-map.md) | Карта артефактов: где что лежит и как связано. |
| [standards/issue-workflow.md](../../standards/issue-workflow.md) | Жизненный цикл задач: статусы и правила переходов. |
| [.github/ISSUE_TEMPLATE/task.yml](../../.github/ISSUE_TEMPLATE/task.yml) | Предложить улучшение через Issue. |

## 🔄 Процесс

Развитие репозитория следует принципу `human-in-control` и Anti-Inflation:
артефакт или изменение появляется только после зафиксированной операционной
боли и согласования.

1. Зафиксируй идею или проблему в Issue (см. [task.yml](../../.github/ISSUE_TEMPLATE/task.yml)).
2. Предложи рекомендацию в отчёте или Issue.
3. Получи ревью и явное согласование (`human-in-control`).
4. Реализуй изменение отдельным reviewable pull request.

Порядок статусов задачи соответствует
[standards/issue-workflow.md](../../standards/issue-workflow.md).

## Связанные артефакты

- [CONCEPT.md](../../CONCEPT.md)
- [governance/repo-model.md](../../governance/repo-model.md)
- [governance/artifact-map.md](../../governance/artifact-map.md)
- [standards/README.md](../../standards/README.md)
- [standards/issue-workflow.md](../../standards/issue-workflow.md)
- [mango_ba_prompts](https://github.com/G-Ivan-A/mango_ba_prompts)
