---
status: canonical
version: 1.10
updated: 2026-06-18
temperature: 0.1
ai-generated: false
source: research/README-old.md
---

# Research

Каталог для независимых исследований рынка, технологий, стандартов и доменных
задач.

> ⛔ **Строгое правило:** Размещение файлов исследований в корне каталога
> `research/` запрещено. Все исследования должны находиться в тематических
> подкаталогах (например, `research/hub/`, `research/mango/`,
> `research/governance/`).
> Это обеспечивает масштабируемость и изоляцию контекста.

## Принципы

| Принцип | Требование |
| --- | --- |
| Изоляция по доменам | Файлы исследований размещаются только в тематических подкаталогах (`research/hub/`, `research/mango/`); корень `research/` содержит лишь `README.md`. |
| Независимость | Research не должен зависеть от production-секретов или закрытых контрактов. |
| Воспроизводимость | Скрипты и эксперименты размещаются рядом с направлением как `research/<domain>/exp-<slug>/` и связываются с отчетом. |
| Сравнение вариантов | Если исследование выбирает стандарт, классификацию или подход, нужна таблица вариантов. |
| Языковая политика | Публичные исследования для международной аудитории поддерживают ru/en пару. |
| Traceability | Отчет ссылается на issue, источники, эксперименты и связанные документы. |

## Текущие исследования

| Подкаталог | Назначение |
| --- | --- |
| [hub/](hub/) | Фундаментальные исследования работы Хаба: передача контекста, project bootstrap, governance-стратегия и классификация промптов (`scope: repo-wide`). |
| [mango/](mango/) | Классификация продуктов и требований MANGO OFFICE, анализ корпуса ТЗ и flow требований (`scope: mango-only`). |
| [governance/](governance/) | Исследования governance-форматов Хаба: формат research-документации, исполнимых контрактов, contract documentation и решений по структуре каталогов (`scope: repo-wide`). |
| [external-knowledge/](external-knowledge/) | Интеграция внешних знаний: Base Registry внешних источников, механизм инсайтов и привязка к knowledge lifecycle (`scope: repo-wide`). |
| [cicd/](cicd/) | Исследования практик и стандартов CI/CD для AI-native проектов: анализ шаблонов, паттернов автоматизации и применимости к нашим репозиториям (`scope: repo-wide`). |

### Подкаталог `hub/`

| Файл | Назначение |
| --- | --- |
| [project-context-and-bootstrap-patterns-2026-05.md](hub/project-context-and-bootstrap-patterns-2026-05.md) | Минималистичные паттерны передачи контекста, предсказуемого project bootstrap и маршрута "рекомендация -> задача" на опыте Mango. |
| [prompts-classification-audit-2026-05.md](hub/prompts-classification-audit-2026-05.md) | Аудит входных данных для классификации промптов: инвентаризация типов, паттерны отладки, пробелы. |
| [prompts-classification-standard-2026-05.md](hub/prompts-classification-standard-2026-05.md) | Стандарт классификации промптов: таксономия (6 осей), матрица зрелости, шаблоны отладки, план интеграции. |
| [team-c-governance-strategy-audit-2026-05.md](hub/team-c-governance-strategy-audit-2026-05.md) | Интерпретация аудита стратегии governance от команды C: сильные стороны, риски overgrowth, hierarchy/lifecycle вопросы и backlog candidates. |
| [user-prompts-analysis-2026-05.md](hub/user-prompts-analysis-2026-05.md) | Анализ 18 пользовательских промптов по стандарту классификации: матрица, устаревшие паттерны, дубли, рекомендации и план интеграции. |
| [external-governance-patterns-review-2026-06.md](hub/external-governance-patterns-review-2026-06.md) | Анализ external governance patterns (GitAgent/EGAProtocol/IETF AgentID) и матрица применимости рекомендаций команды С: «взять сейчас / отложить / отклонить», North Star и триггеры пересмотра. |
| [ecosystem-governance-audit-2026-06.md](hub/ecosystem-governance-audit-2026-06.md) | Аудит governance-практик Хаба, `mango_ba_prompts`, `open-ai.ru`, `clarify-engine-ai` и международных AI governance patterns для issue #217. |
| [external-practice-intake-2026-06.md](hub/external-practice-intake-2026-06.md) | Анализ Habr-источников Artem Chirkov и slam, тест структуры `practices/`, выделение agent-work практик и Mango docs error pattern. |
| [international-ai-governance-practices-2026-06.md](hub/international-ai-governance-practices-2026-06.md) | Анализ NIST AI RMF, EU AI Act, ISO/IEC 42001, OpenAI, Anthropic и Google SAIF с executable implementation matrix для Хаба. |

## Рекомендуемая структура

```text
research/<domain>/
  README.md
  <topic>.ru.md
  <topic>.en.md
```

Если issue явно требует только русский результат, допускается один `.md` файл.
Перед внешней публикацией нужно добавить английскую пару или зафиксировать
исключение.

Подробные правила frontmatter, источников и экспериментов зафиксированы в
[standards/research-profile.md](../standards/research-profile.md).
