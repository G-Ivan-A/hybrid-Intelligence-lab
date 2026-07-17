---
status: canonical
version: 1.1
updated: 2026-07-17
temperature: 0.1
---

# Education — общие образовательные материалы

Этот каталог содержит общие образовательные активы Хаба: глоссарии,
introductions, общие курсы и материалы, не привязанные к специфичной
методологии AI-образования.

## Связь с `ai-education/`

Для AI-специфичных модульных исследований (Reference Research Pattern)
см. [`research/ai-education/`](../ai-education/README.md).

Разделение:

- `education/` — общие материалы, не требующие модульной структуры;
- `ai-education/` — AI-специфичные исследования по шаблону
  `[00-intro, 10-theory, 20-taxonomy, 30-decision-framework, 40-practice, 50-open-research]`.

Граница с корневым каталогом [education/](../../education/): здесь лежит
**исследование** (source-backed теория, таксономии, обзоры), там — **учебный
продукт** (курсы, программы, сценарии преподавателя). Research отвечает на
вопрос «что известно предметной области и откуда мы это знаем», education —
«как этому научить».

Связанная issue: [G-Ivan-A/hybrid-Intelligence-lab#418](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/418)

## Документы

| Документ | Назначение |
| --- | --- |
| [2026-07-16-retrieval-strategies-survey.md](2026-07-16-retrieval-strategies-survey.md) | Исходный монолит исследования retrieval-стратегий для AI-агентов (issue #418), реорганизованный в Reference Research Pattern. |

## Политики направления

- **Приоритет источников**: академические статьи 2023–2026 (arXiv, ACL, NeurIPS,
  ICLR, SIGIR) — приоритет №1; индустриальные white papers — приоритет №2;
  блоги/туториалы — только как иллюстрация, не как основа.
- **Заземление**: каждое утверждение ссылается на источник
  ([AI Governance](../../ai-governance/ai-governance.md), политика 1).
- **Границы**: исследования направления не привязаны к конкретному споку —
  это переиспользуемый актив экосистемы ([docs/vision.md](../../docs/vision.md)).
- **Направление не создаёт стандартов и не принимает решений**: результат —
  вход для RFC/ADR и для учебных материалов в `education/`.
