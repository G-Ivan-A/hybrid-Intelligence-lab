---
status: draft
version: 0.1
updated: 2026-06-13
temperature: 0.1
ai-generated: true
type: external-analysis
source_id: ext-003
stage: hypothesis
projects: [mango, clarify-engine-ai]
context: [spec-driven, requirements, agents, executable-spec]
---

# Инсайт: спецификация как исполнимый артефакт между требованием и кодом

**Источник:** `ext-003` —
[GitHub Spec Kit / Spec-Driven Development](https://github.com/github/spec-kit)
(см. [реестр](../external-sources-registry.md)).

## Вывод (атомарно)

Spec-Driven Development (SDD) делает **спецификацию первичным исполнимым
артефактом**: агент сначала формирует структурированную спецификацию
(`specify → plan → tasks → implement`), и только потом генерирует код. Спека
становится контрактом между человеком (намерение) и агентом (реализация), а не
одноразовым промптом.

## Почему это релевантно экосистеме

- Прямо ложится на домен **clarify-engine-ai** (движок уточнения требований) и
  **mango_ba_prompts** (требования → ТЗ): SDD — это формализованный мост
  «неопределённое требование → проверяемая спецификация».
- Совпадает с нашим различением **descriptive vs executable**
  ([standards/executable-documentation-standard.md](../../../standards/executable-documentation-standard.md))
  и с lifecycle-стадией `RFC → Pattern`.
- Перекликается с исследованием жизненного цикла требований Mango
  ([research/mango/2026-05-requirements-lifecycle-uncertainty.md](../../../research/mango/2026-05-requirements-lifecycle-uncertainty.md)).

## Аргументы за/против

| За | Против / Ограничение |
| --- | --- |
| Закрывает реальный gap «требование → ТЗ → реализация» для 2 проектов. | Tooling завязан на конкретные CLI; берём метод, не инструмент. |
| Спека как контракт = совпадает с executable-documentation курсом Хаба. | Требует пилота, прежде чем предлагать как практику. |

## Путь к практике

- **Гипотеза проверки:** прогнать SDD-цикл на одном реальном кейсе требований
  Mango и сравнить traceability с текущим flow
  ([research/mango/2026-05-requirements-flow.md](../../../research/mango/2026-05-requirements-flow.md)).
- **Если гипотеза подтвердится:** инициировать отдельный RFC «spec-driven
  requirements flow» для clarify-engine-ai/Mango (а не сразу практику).
- **Решение о пилоте и RFC — за человеком.**

## Стадия

`stage: hypothesis` — есть конкретная гипотеза применения и критерий проверки
(traceability на реальном кейсе Mango); до пилота вывод не переводится дальше.
