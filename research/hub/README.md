---
status: canonical
version: 1.2
updated: 2026-06-18
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
| [project-context-and-bootstrap-patterns-2026-05.md](project-context-and-bootstrap-patterns-2026-05.md) | Минималистичные паттерны передачи контекста, предсказуемого project bootstrap и маршрута "рекомендация -> задача" на опыте Mango. |
| [prompts-classification-audit-2026-05.md](prompts-classification-audit-2026-05.md) | Аудит входных данных для классификации промптов: инвентаризация типов, паттерны отладки, пробелы. |
| [prompts-classification-standard-2026-05.md](prompts-classification-standard-2026-05.md) | Стандарт классификации промптов: таксономия (6 осей), матрица зрелости, шаблоны отладки, план интеграции. |
| [team-c-governance-strategy-audit-2026-05.md](team-c-governance-strategy-audit-2026-05.md) | Интерпретация аудита стратегии governance от команды C: сильные стороны, риски overgrowth, hierarchy/lifecycle вопросы и backlog candidates. |
| [user-prompts-analysis-2026-05.md](user-prompts-analysis-2026-05.md) | Анализ 18 пользовательских промптов по стандарту классификации: матрица, устаревшие паттерны, дубли, рекомендации и план интеграции. |
| [ai-collaboration-retrospective-2026-06.md](ai-collaboration-retrospective-2026-06.md) | Ретроспектива ошибок AI-агента в сессии проектирования шаблонов споков: реестр ошибок, корневые причины и системные выводы для будущего onboarding/governance proposal. |
| [ai-collaboration-retrospective-mango-migration-2026-06.md](ai-collaboration-retrospective-mango-migration-2026-06.md) | Ретроспектива ошибок AI-агента в сессии проектирования миграции Mango (Хаб → спок): реестр ошибок (включая архитектурное размещение артефактов), корневые причины и системные выводы для будущего onboarding/governance proposal. |
| [external-governance-patterns-review-2026-06.md](external-governance-patterns-review-2026-06.md) | Анализ external governance patterns (GitAgent/EGAProtocol/IETF AgentID) и матрица применимости рекомендаций команды С: 8 ценных идей, колонки «взять сейчас / отложить / отклонить», North Star и триггеры пересмотра. |
| [ecosystem-governance-audit-2026-06.md](ecosystem-governance-audit-2026-06.md) | Аудит governance-практик Хаба, `mango_ba_prompts`, `open-ai.ru`, `clarify-engine-ai` и международных AI governance patterns для issue #217. |
| [external-practice-intake-2026-06.md](external-practice-intake-2026-06.md) | Анализ внешних agent-work практик по Habr-источникам Artem Chirkov и slam, тест структуры `practices/`, и Mango docs error pattern без изменения Mango. |
| [international-ai-governance-practices-2026-06.md](international-ai-governance-practices-2026-06.md) | Анализ международных AI governance sources и executable implementation matrix: NIST AI RMF, EU AI Act, ISO/IEC 42001, OpenAI, Anthropic, Google SAIF. |

## Воспроизводимость

Скрипты и эксперименты размещаются рядом с направлением как
`research/hub/exp-<slug>/` и связываются с отчетом по
[standards/research-profile.md](../../standards/research-profile.md).
