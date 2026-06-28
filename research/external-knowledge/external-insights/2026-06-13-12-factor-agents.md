---
status: draft
version: 0.1
updated: 2026-06-13
temperature: 0.1
type: external-analysis
source_id: ext-002
stage: research
projects: [hub, mango, open-ai.ru, clarify-engine-ai]
context: [agents, production, prompt-ownership, human-in-the-loop]
---

# Инсайт: владей промптами и контекстом как кодом, держи человека в петле

**Источник:** `ext-002` —
[12-Factor Agents (HumanLayer)](https://github.com/humanlayer/12-factor-agents)
(см. [реестр](../external-sources-registry.md)).

## Вывод (атомарно)

Производственные LLM-приложения надёжнее, когда команда **владеет промптами,
контекстом и control flow явно** (как версионируемым кодом), а не прячет их
внутри фреймворка, и когда **человек остаётся точкой контроля** в ключевых
переходах (factors «own your prompts», «own your context window»,
«contact humans with tool calls»).

## Почему это релевантно экосистеме

- Подтверждает наш курс на **исполнимые контракты и явные промпты в репозитории**
  ([standards/executable-contract-standard.md](../../../standards/executable-contract-standard.md)),
  а не «магию» внутри инструментов.
- «Человек в петле» = наш hard rule **«Человек > Команда Q > Исполнитель»** и
  «решение за человеком» ([AI_GOVERNANCE.md](../../../AI_GOVERNANCE.md)).
- «Own your context window» резонирует с token-budget практикой
  ([practices/agent-work/skill-catalog-token-budget.md](../../../practices/agent-work/skill-catalog-token-budget.md)).

## Аргументы за/против

| За | Против / Ограничение |
| --- | --- |
| Инженерная, проверяемая формулировка владения промптами. | «12 факторов» — маркетинговая рамка; берём принципы, не нумерацию. |
| Совпадает с уже принятыми практиками Хаба — низкий риск интеграции. | Часть факторов про инфраструктуру (stateless, deploy) вне scope Хаба. |

## Путь к практике

- **Кандидат:** усиление практики
  [practices/agent-work/](../../../practices/agent-work/README.md) пунктом
  «промпты и контекст — версионируемые артефакты репозитория».
- **Для перехода в `candidate-practice`:** отобрать 3–4 фактора, релевантные
  HTOM-командам, и переформулировать провайдер-агностично.
- **Решение о переводе — за человеком.**

## Стадия

`stage: research` — большинство факторов уже совпадают с действующими практиками
Хаба; нужен отбор и переформулировка перед practice-кандидатом.
