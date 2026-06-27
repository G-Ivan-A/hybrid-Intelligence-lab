---
status: canonical
version: 1.8
updated: 2026-06-27
temperature: 0.1
ai-generated: false
---

# Research: Hub

Фундаментальные исследования, касающиеся работы самого Хаба: передачи контекста,
project bootstrap, governance-стратегии и классификации промптов. В отличие от
доменных подкаталогов (например, [mango/](../mango/)), материалы здесь имеют
`scope: repo-wide` и применяются ко всему репозиторию.

## Документы

| Документ | Назначение |
| --- | --- |
| [2026-05-28-project-context-and-bootstrap-patterns.md](2026-05-28-project-context-and-bootstrap-patterns.md) | Минималистичные паттерны передачи контекста, предсказуемого project bootstrap и маршрута "рекомендация -> задача" на опыте Mango. |
| [2026-05-28-prompts-classification-audit.md](2026-05-28-prompts-classification-audit.md) | Аудит входных данных для классификации промптов: инвентаризация типов, паттерны отладки, пробелы. |
| [2026-05-28-prompts-classification-standard.md](2026-05-28-prompts-classification-standard.md) | Стандарт классификации промптов: таксономия (6 осей), матрица зрелости, шаблоны отладки, план интеграции. |
| [2026-06-01-team-c-governance-strategy-audit.md](2026-06-01-team-c-governance-strategy-audit.md) | Интерпретация аудита стратегии governance от команды C: сильные стороны, риски overgrowth, hierarchy/lifecycle вопросы и backlog candidates. |
| [2026-05-28-user-prompts-analysis.md](2026-05-28-user-prompts-analysis.md) | Анализ 18 пользовательских промптов по стандарту классификации: матрица, устаревшие паттерны, дубли, рекомендации и план интеграции. |
| [2026-06-02-ai-collaboration-retrospective.md](2026-06-02-ai-collaboration-retrospective.md) | Ретроспектива ошибок AI-агента в сессии проектирования шаблонов споков: реестр ошибок, корневые причины и системные выводы для будущего onboarding/governance proposal. |
| [2026-06-02-ai-collaboration-retrospective-mango-migration.md](2026-06-02-ai-collaboration-retrospective-mango-migration.md) | Ретроспектива ошибок AI-агента в сессии проектирования миграции Mango (Хаб → спок): реестр ошибок (включая архитектурное размещение артефактов), корневые причины и системные выводы для будущего onboarding/governance proposal. |
| [2026-06-02-external-governance-patterns-review.md](2026-06-02-external-governance-patterns-review.md) | Анализ external governance patterns (GitAgent/EGAProtocol/IETF AgentID) и матрица применимости рекомендаций команды С: 8 ценных идей, колонки «взять сейчас / отложить / отклонить», North Star и триггеры пересмотра. |
| [2026-06-12-ecosystem-governance-audit.md](2026-06-12-ecosystem-governance-audit.md) | Аудит governance-практик Хаба, `mango_ba_prompts`, `open-ai.ru`, `clarify-engine-ai` и международных AI governance patterns для issue #217. |
| [2026-06-20-ecosystem-architecture-research.md](2026-06-20-ecosystem-architecture-research.md) | Комплексное исследование архитектуры экосистемы для issue #257: Hub как центр 5+ проектов, token balance, L1-L4 для `open-ai.ru` и репутационные технологии. |
| [2026-06-12-external-practice-intake.md](2026-06-12-external-practice-intake.md) | Анализ внешних agent-work практик по Habr-источникам Artem Chirkov и slam, тест структуры `practices/`, и Mango docs error pattern без изменения Mango. |
| [2026-06-12-international-ai-governance-practices.md](2026-06-12-international-ai-governance-practices.md) | Анализ международных AI governance sources и executable implementation matrix: NIST AI RMF, EU AI Act, ISO/IEC 42001, OpenAI, Anthropic, Google SAIF. |
| [2026-06-23-repository-structure-concept.md](2026-06-23-repository-structure-concept.md) | Reviewed research input для issue #276: дополнение к mango-исследованию структуры каталогов (issue #263), Часть II по соглашению «Архитектура инфраструктуры проектов экосистемы» (issue #274), критическая проверка соглашения и источники для [ADR-001](../../docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md) / [ADR-002](../../docs/adr/2026-06-adr-002-artifact-document-methodology.md). |
| [2026-06-25-artifact-inventory-and-classification.md](2026-06-25-artifact-inventory-and-classification.md) | Reviewed research input для issue #276: инвентаризация артефактов экосистемы, классификация по ортогональным осям, routing rules RT-01..RT-10 и source-backed вход для [ADR-002](../../docs/adr/2026-06-adr-002-artifact-document-methodology.md) / [ADR-001](../../docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md). |
| [2026-06-27-rfc-industry-norms-and-variants.md](2026-06-27-rfc-industry-norms-and-variants.md) | Research input для issue #278: аудит RFC Hub/Mango, индустриальные RFC-like нормы по архетипам A-D, дельты, lifecycle diagrams и варианты RFC-модели без создания нового RFC. |
| [2026-06-27-adr-industry-norms-and-variants.md](2026-06-27-adr-industry-norms-and-variants.md) | Research input для issue #278: аудит ADR/decision records Hub/Mango, индустриальные ADR-нормы, дельты, lifecycle diagrams и варианты ADR-модели без создания нового ADR. |

## Эксперименты

| Эксперимент | Назначение |
| --- | --- |
| [exp-rfc-adr-industry-norms/](exp-rfc-adr-industry-norms/) | Воспроизводимый corpus scan для issue #278: local Hub/Mango RFC/ADR audit и external RFC/ADR path-signal summaries по архетипам A-D. |

## Воспроизводимость

Скрипты и эксперименты размещаются рядом с направлением как
`research/hub/exp-<slug>/` и связываются с отчетом по
[standards/research-profile.md](../../standards/research-profile.md).
