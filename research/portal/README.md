---
status: draft
version: 0.1
updated: 2026-06-05
ai-generated: true
type: navigation
scope: portal
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/159"
---

# Research: Portal (open-ai.ru)

Направление исследований для концепции портала `open-ai.ru` — «универсального
инструмента коммуникации» и единой точки сборки spoke-проектов экосистемы
(Reputation Engineering, автоматизация БА Mango через `mango_ba_prompts`, и до
10+ open-source проектов в перспективе).

Это исследовательское направление (`scope: portal`) производит **знание для
решения**, а не сам портал: сравнение стандартов документации, архитектур,
стеков и структур репозитория. Реализация портала здесь **не ведётся** — это
вход для RFC [open-ai-portal-concept-rfc.md](open-ai-portal-concept-rfc.md).

Задача-источник: [issue #159](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/159)
(режим `creative`, полная автономия исполнителя).

## Документы

| Документ | Назначение |
| --- | --- |
| [documentation-standards-comparison-2026-06.md](documentation-standards-comparison-2026-06.md) | Исследование 1: сравнение ≥3 стандартов документации (C4, arc42, ADR, RFC, Diátaxis, Concept Doc, IEEE 42010) по 5 критериям; выбор оптимального для портала. |
| [concept-standards-comparison-2026-06.md](concept-standards-comparison-2026-06.md) | Исследование (issue #166): сравнение 8 подходов к стандартизации структуры **концепции** (ISO 42010, TOGAF, BABOK, Continuous Discovery, PRD, RFC, Concept Doc, Vision Document) по 7 критериям; выход — [standards/webportal-concept-standard.md](../../standards/webportal-concept-standard.md). |
| [architecture-and-stack-comparison-2026-06.md](architecture-and-stack-comparison-2026-06.md) | Исследование 2: независимое сравнение ≥4 архитектурных подходов и ≥7 стеков, таблица на ≥10 критериев, выбор оптимального. |
| [repository-structure-design-2026-06.md](repository-structure-design-2026-06.md) | Исследование 3: анализ структуры Хаба, требований портала, альтернатив; обоснование структуры и связь со стандартом `PORTAL_REPOSITORY_STRUCTURE.md`. |
| [ai-and-mango-integration-patterns-2026-06.md](ai-and-mango-integration-patterns-2026-06.md) | Дополнительное исследование: паттерны AI-интеграции (Yandex GPT), интеграции `mango_ba_prompts`, аутентификации и маскирования данных по фазам. |

## Политики направления

| Политика | Значение |
| --- | --- |
| Язык результата | Русский (как в Хабе), технические термины — в оригинале. ru/en пара добавляется перед внешней публикацией. |
| Независимость | Варианты команды G и фаундера — **входные данные, не догма**. Исследование ведётся с нуля; каждый вывод трассируется к источнику. |
| Ограничения по данным | Реальные клиентские промпты Mango, секреты и production-конфигурация **не коммитятся** (см. [AI_GOVERNANCE.md](../../AI_GOVERNANCE.md), правило 6). |
| Цитирование | Каждое version-sensitive утверждение (версии фреймворков, лимиты free-tier) помечено как требующее проверки перед фиксацией (см. [standards/RESEARCH_PROFILE.md](../../standards/RESEARCH_PROFILE.md)). |
| Решение за человеком | Перевод в `reviewed` и выбор итогового варианта — за фаундером (RFC, раздел «Запрос на согласование»). |

## Связанные артефакты

- [open-ai-portal-concept-rfc.md](open-ai-portal-concept-rfc.md) — RFC, синтезирующий эти исследования в предложение.
- [standards/PORTAL_REPOSITORY_STRUCTURE.md](../../standards/PORTAL_REPOSITORY_STRUCTURE.md) — стандарт структуры портал-спока (выход Исследования 3).
- [standards/RESEARCH_PROFILE.md](../../standards/RESEARCH_PROFILE.md) — правила frontmatter, источников и воспроизводимости.
- [projects/README.md](../../projects/README.md) — критерии «когда `/projects`, а когда отдельный spoke-репозиторий».
