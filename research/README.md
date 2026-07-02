---
status: canonical
version: 1.22
updated: 2026-07-01
temperature: 0.1
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
| Date-first naming | Хронологические research-файлы именуются `YYYY-MM-DD-name.md`; дата всегда стоит первой и берётся из git history создания файла. |
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
| [open-ai-ru/](open-ai-ru/) | Архитектура репозитория и продуктовых уровней L1–L4 для spoke-проекта open-ai.ru: инвентаризация стандартов Хаба, аудит репо, международные практики и детализация L3–L4 (`scope: open-ai-ru`). |
| [governance/](governance/) | Исследования governance-форматов Хаба: формат research-документации, исполнимых контрактов, contract documentation и решений по структуре каталогов (`scope: repo-wide`). |
| [external-knowledge/](external-knowledge/) | Интеграция внешних знаний: Base Registry внешних источников, механизм инсайтов и привязка к knowledge lifecycle (`scope: repo-wide`). |
| [cicd/](cicd/) | Исследования практик и стандартов CI/CD для AI-native проектов: анализ шаблонов, паттернов автоматизации и применимости к нашим репозиториям (`scope: repo-wide`). |
| [reputation-technologies/](reputation-technologies/) | Фреймворк репутационных технологий **GRA**: видение фаундера, концептуальная модель, международный стандарт, словарь, white paper, архитектура отдельного репозитория в экосистеме (`scope: repo-wide`). |

### Подкаталог `hub/`

| Файл | Назначение |
| --- | --- |
| [2026-05-28-project-context-and-bootstrap-patterns.md](hub/2026-05-28-project-context-and-bootstrap-patterns.md) | Минималистичные паттерны передачи контекста, предсказуемого project bootstrap и маршрута "рекомендация -> задача" на опыте Mango. |
| [2026-05-28-prompts-classification-audit.md](hub/2026-05-28-prompts-classification-audit.md) | Аудит входных данных для классификации промптов: инвентаризация типов, паттерны отладки, пробелы. |
| [2026-05-28-prompts-classification-standard.md](hub/2026-05-28-prompts-classification-standard.md) | Стандарт классификации промптов: таксономия (6 осей), матрица зрелости, шаблоны отладки, план интеграции. |
| [2026-06-01-team-c-governance-strategy-audit.md](hub/2026-06-01-team-c-governance-strategy-audit.md) | Интерпретация аудита стратегии governance от команды C: сильные стороны, риски overgrowth, hierarchy/lifecycle вопросы и backlog candidates. |
| [2026-05-28-user-prompts-analysis.md](hub/2026-05-28-user-prompts-analysis.md) | Анализ 18 пользовательских промптов по стандарту классификации: матрица, устаревшие паттерны, дубли, рекомендации и план интеграции. |
| [2026-06-02-external-governance-patterns-review.md](hub/2026-06-02-external-governance-patterns-review.md) | Анализ external governance patterns (GitAgent/EGAProtocol/IETF AgentID) и матрица применимости рекомендаций команды С: «взять сейчас / отложить / отклонить», North Star и триггеры пересмотра. |
| [2026-06-12-ecosystem-governance-audit.md](hub/2026-06-12-ecosystem-governance-audit.md) | Аудит governance-практик Хаба, `mango_ba_prompts`, `open-ai.ru`, `clarify-engine-ai` и международных AI governance patterns для issue #217. |
| [2026-06-20-ecosystem-architecture-research.md](hub/2026-06-20-ecosystem-architecture-research.md) | Комплексное исследование архитектуры экосистемы для issue #257: Hub как центр 5+ проектов, token balance, L1-L4 для `open-ai.ru` и репутационные технологии. |
| [2026-06-12-external-practice-intake.md](hub/2026-06-12-external-practice-intake.md) | Анализ Habr-источников Artem Chirkov и slam, тест структуры `practices/`, выделение agent-work практик и Mango docs error pattern. |
| [2026-06-12-international-ai-governance-practices.md](hub/2026-06-12-international-ai-governance-practices.md) | Анализ NIST AI RMF, EU AI Act, ISO/IEC 42001, OpenAI, Anthropic и Google SAIF с executable implementation matrix для Хаба. |
| [2026-06-23-repository-structure-concept.md](hub/2026-06-23-repository-structure-concept.md) | Reviewed research input для issue #276: дополнение к mango-исследованию (issue #263), Часть II по соглашению «Архитектура инфраструктуры проектов экосистемы» (issue #274), критическая проверка соглашения и источники для [ADR-001](../docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md) / [ADR-002](../docs/adr/2026-06-adr-002-artifact-document-methodology.md). |
| [2026-06-25-artifact-inventory-and-classification.md](hub/2026-06-25-artifact-inventory-and-classification.md) | Reviewed research input для issue #276: инвентаризация артефактов экосистемы, классификация по ортогональным осям, routing rules RT-01..RT-10 и source-backed вход для [ADR-002](../docs/adr/2026-06-adr-002-artifact-document-methodology.md) / [ADR-001](../docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md). |
| [2026-06-27-rfc-industry-norms-and-variants.md](hub/2026-06-27-rfc-industry-norms-and-variants.md) | Research input для issue #278: RFC-like индустриальные нормы и варианты для Hub/Mango по архетипам A-D, с воспроизводимым external source corpus. |
| [2026-06-27-adr-industry-norms-and-variants.md](hub/2026-06-27-adr-industry-norms-and-variants.md) | Research input для issue #278: ADR/decision-record индустриальные нормы и варианты для Hub/Mango по архетипам A-D, с дельтами и критериями применимости. |
| [2026-06-28-research-analysis-audit-inventory.md](hub/2026-06-28-research-analysis-audit-inventory.md) | Analysis input для issue #288: Research / Analysis / Audit matrix по Hub, Mango и Clarify, concept substitutions, duplicate risks and three `Analysis -> RFC -> Standard` chains. |
| [2026-06-30-reports-industry-norms-and-standardization-scope.md](hub/2026-06-30-reports-industry-norms-and-standardization-scope.md) | Research input для issue #307 (B-038): индустриальный benchmark норм Reports (Diátaxis, DITA, ISO/IEC/IEEE, ANSI/NISO Z39.18, ГОСТ 7.32/19.101, SDMX/DDI, NIST AI RMF, EU AI Act, Kubernetes/CNCF/OpenTelemetry), проверка гипотез H1-H4, граничные кейсы Reports ↔ Analysis/Audit и рекомендация Вариант C (гибрид) без создания стандарта. |

### Подкаталог `open-ai-ru/`

| Файл | Назначение |
| --- | --- |
| [2026-06-20-open-ai-ru-repository-architecture-and-l3-l4.md](open-ai-ru/2026-06-20-open-ai-ru-repository-architecture-and-l3-l4.md) | Архитектура репозитория open-ai.ru и детализация уровней L3–L4 для issue #259: инвентаризация стандартов Хаба, аудит репо, сравнение с международными практиками (8 проектов, проверено через GitHub API), C4-диаграммы, ADR-формат и предложение структуры репо с trade-offs. |

### Подкаталог `reputation-technologies/`

| Файл | Назначение |
| --- | --- |
| [2026-06-20-founders-vision-and-framework.ru.md](reputation-technologies/2026-06-20-founders-vision-and-framework.ru.md) | Основной отчёт (RU): видение фаундера, эволюция, репутация как система, роль ИИ, 15 международных проектов, фреймворк GRA, стандарт, отдельный репозиторий, roadmaps, trade-offs. |
| [2026-06-20-framework-standard.en.md](reputation-technologies/2026-06-20-framework-standard.en.md) | Проект стандарта (EN) в формате ISO/IEC/IEEE 42010:2022 + ISO/IEC 42001:2023. |
| [2026-06-20-white-paper.en.md](reputation-technologies/2026-06-20-white-paper.en.md) | White paper (EN, 10–15 c.) для международной аудитории. |
| [2026-06-20-executive-summary.ru-en.md](reputation-technologies/2026-06-20-executive-summary.ru-en.md) | Executive summary (RU + EN, 2–3 c.). |
| [2026-06-20-glossary.ru-en.md](reputation-technologies/2026-06-20-glossary.ru-en.md) | Терминологический словарь (RU↔EN) с международными аналогами. |

## Рекомендуемая структура

```text
research/<domain>/
  README.md
  YYYY-MM-DD-topic.md
  YYYY-MM-DD-topic.ru.md
  YYYY-MM-DD-topic.en.md
```

Если issue явно требует только русский результат, допускается один `.md` файл.
Перед внешней публикацией нужно добавить английскую пару или зафиксировать
исключение.

Подробные правила структуры research-артефактов, источников и экспериментов
зафиксированы в
[standards/research-standard.md](../standards/research-standard.md). Правила
date-first именования зафиксированы в
[standards/file-naming.md](../standards/file-naming.md) и проверяются командой
`./tools/validate-file-naming.sh`.
