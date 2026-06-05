---
status: draft
version: 0.1
updated: 2026-06-05
ai-generated: true
type: external-analysis
context: [portal, documentation-standards, architecture-docs, ai-native, decision-traceability]
method: comparative-analysis
scope: portal
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/159"
related_artifacts:
  - "research/portal/architecture-and-stack-comparison-2026-06.md"
  - "research/portal/repository-structure-design-2026-06.md"
  - "governance/proposals/open-ai-portal-concept-rfc.md"
  - "standards/RESEARCH_PROFILE.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/159"
---

# Исследование 1: Сравнение стандартов документации для портала open-ai.ru

Версия: 0.1

Дата: 2026-06-05

Статус: черновик исследования (`draft`). Перевод в `reviewed` и выбор стандарта
как обязательного — за человеком (см. раздел «Решение за человеком»).

## Вопрос, гипотеза, метод

| Поле | Значение |
| --- | --- |
| **Вопрос** | Какой стандарт документации оптимален для портала `open-ai.ru` — AI-native проекта с итеративной разработкой, требованием трассируемости решений и визуализации архитектуры? |
| **Гипотеза** | Ни один единичный стандарт не покрывает все 5 критериев; оптимум — минимальная композиция «docs-as-code» стандартов, наследующая практику Хаба, а не один монолит. |
| **Метод** | Сравнительный анализ (`comparative-analysis`) 7 стандартов по 5 критериям из issue #159 с матрицей применимости. |
| **Критерий успеха** | Выбран первичный стандарт + явные дополняющие, каждый выбор трассируется к критерию и источнику. |
| **Ограничения** | Анализ опирается на публичные спецификации стандартов (стабильны); оценки «простоты для команды» носят экспертный характер и проверяются на практике в Phase 0–1. |

> Перед исследованием проверено (issue #159): в Хабе **нет** обязательного
> стандарта документации архитектуры для порталов. Есть смежная практика — RFC в
> `governance/proposals/`, Concept Doc (`CONCEPT.md`), Mermaid-диаграммы и
> `standards/GLOSSARY.md`. Поэтому исследование обязательно.

## Кандидаты

| # | Стандарт | Что это | Каноничный источник |
| --- | --- | --- | --- |
| 1 | **C4 Model** | Иерархия диаграмм Context → Container → Component → Code + supplementary (landscape, dynamic, deployment). | Simon Brown — [c4model.com](https://c4model.com) |
| 2 | **arc42** | Шаблон из 12 разделов для полного описания архитектуры (цели, ограничения, контекст, решения, риски). | [arc42.org](https://arc42.org), [docs.arc42.org](https://docs.arc42.org) |
| 3 | **ADR** (Architecture Decision Record) | Короткие записи отдельных решений: контекст → решение → последствия. | M. Nygard, 2011; [adr.github.io](https://adr.github.io); [joelparkerhenderson/architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record) |
| 4 | **RFC** (Request for Comments) | Структурированное предложение изменения с обсуждением и нормативным языком (BCP 14 / RFC 2119: MUST/SHOULD/MAY). | [rfc-editor.org/rfc/rfc2119](https://www.rfc-editor.org/rfc/rfc2119) |
| 5 | **Diátaxis** | Каркас пользовательской документации: tutorials / how-to / reference / explanation. | D. Procida — [diataxis.fr](https://diataxis.fr) |
| 6 | **Concept Doc (Хаб)** | Внутренняя практика Хаба: `CONCEPT.md` + executable-documents + frontmatter-стандарт. | [CONCEPT.md](../../CONCEPT.md), [governance/proposals/contract-executability-rfc.md](../../governance/proposals/contract-executability-rfc.md) |
| 7 | **IEEE/ISO/IEC 42010** | Формальный стандарт описания архитектуры через stakeholders, concerns, viewpoints, views. | ISO/IEC/IEEE 42010:2022 — [iso.org/standard/74393.html](https://www.iso.org/standard/74393.html) |

## Критерии оценки (из issue #159)

1. **AI-native применимость** — насколько формат удобен для генерации, чтения и проверки AI-агентами (текст/Markdown, машиночитаемость, предсказуемая структура).
2. **Поддержка итеративной разработки** — приживается ли при инкрементальном росте без «большого upfront-документа».
3. **Трассируемость решений** — фиксирует ли *почему* принято решение, со связью к контексту и последствиям.
4. **Простота использования командой** — порог входа, объём церемоний, кривая обучения.
5. **Поддержка визуализации архитектуры** — насколько помогает показать структуру системы наглядно.

Шкала: 🟢 сильно / 🟡 частично / 🔴 слабо.

## Матрица применимости

| Стандарт | AI-native | Итеративность | Трассируемость | Простота | Визуализация | Итог (🟢) |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| **C4 Model** | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 4 |
| **arc42** | 🟡 | 🟡 | 🟢 | 🟡 | 🟡 | 1 |
| **ADR** | 🟢 | 🟢 | 🟢 | 🟢 | 🔴 | 4 |
| **RFC** | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 3 |
| **Diátaxis** | 🟢 | 🟢 | 🔴 | 🟢 | 🔴 | 3 |
| **Concept Doc (Хаб)** | 🟢 | 🟢 | 🟡 | 🟢 | 🟡 | 3 |
| **IEEE 42010** | 🔴 | 🔴 | 🟢 | 🔴 | 🟡 | 1 |

### Обоснование оценок

- **C4 Model.** Текстовые DSL (Structurizr DSL, Mermaid `C4Context`) дают
  машиночитаемые, версионируемые диаграммы — AI-native и docs-as-code 🟢.
  Иерархия Context→Container→Component позволяет начать с одной диаграммы и
  углублять итеративно 🟢. Визуализация — это его суть 🟢. Сам по себе он не
  хранит *почему* решения (для этого нужен ADR) — трассируемость 🟡.
- **arc42.** Полный шаблон силён трассируемостью (раздел 9 — Architecture
  Decisions) 🟢, но для портала на старте — избыточен: 12 разделов провоцируют
  «документ ради документа», что противоречит Anti-Inflation principle Хаба;
  итеративность и простота 🟡. Хорош как *скелет обзора* позже, не как старт.
- **ADR.** Короткий Markdown-файл на решение: контекст → решение → последствия.
  Идеален для трассируемости 🟢, AI-native и итеративен 🟢, низкий порог входа
  🟢. Не визуализирует 🔴 (и не должен — это его не задача). **Уже частично
  присутствует** в геноме спока: `templates/spoke/docs/adr/`.
- **RFC.** Сильное предложение-with-rationale (как этот документ-сосед);
  нормативный язык MUST/SHOULD/MAY полезен для контрактов 🟢 трассируемость. Но
  RFC тяжелее ADR для рутинных решений (порог 🟡). **Уже practice Хаба**
  (`governance/proposals/`).
- **Diátaxis.** Лучший каркас для *пользовательской* документации портала
  (`learning/`, `knowledge-base/`) 🟢, но не для архитектурных решений
  (трассируемость 🔴) — это другой слой.
- **Concept Doc (Хаб).** Внутренняя практика: `status/version/updated/ai-generated`
  frontmatter + executable-documents. AI-native и проста 🟢; портал её
  **наследует по умолчанию** как spoke. Трассируемость через связанные RFC 🟡.
- **IEEE 42010.** Формально полон и силён трассируемостью 🟢, но тяжёл, не
  Markdown-native, высокий порог 🔴 — нерационален для итеративного open-source
  портала уровня MVP.

## Вывод: оптимальная композиция, а не один стандарт

Гипотеза подтвердилась: единого победителя нет. Каждый стандарт силён в своём
слое, и они **ортогональны** (C4 — структура, ADR — решения, Diátaxis —
пользователь). Навязывать один — значит либо потерять трассируемость (только
C4), либо потерять визуализацию (только ADR), либо утонуть в церемониях (arc42 /
IEEE на старте).

**Рекомендуемый стандарт для портала (минимальное ядро + дополнения):**

| Слой | Стандарт | Статус для портала | Почему |
| --- | --- | --- | --- |
| **Решения** | **ADR** | 🔴 обязательно (ядро) | Дешёвая трассируемость; уже в геноме спока (`docs/adr/`); AI-native; итеративен. |
| **Визуализация** | **C4 Model** (через Mermaid `C4*`) | 🔴 обязательно (ядро) | Лучшая наглядность архитектуры; docs-as-code; диаграммы версионируются рядом с кодом. |
| **Предложения** | **RFC** | 🟡 наследуется от Хаба | Крупные изменения курса портала идут через RFC в Хабе или споке. |
| **Обзор архитектуры** | **arc42 (lite)** | 🟢 опционально (по росту) | Когда портал перерастёт «несколько ADR» — один обзорный `docs/architecture.md` по сокращённому arc42-скелету (разделы 1, 3, 4, 5, 8, 9). |
| **Документация пользователя** | **Diátaxis** | 🟢 опционально | Каркас для `learning/` и `knowledge-base/` портала. |
| **Метаданные/lifecycle** | **Concept Doc (Хаб)** | 🔴 наследуется | frontmatter `status/version/updated/ai-generated` обязателен для всех `.md` (валидатор Хаба). |

Формула: **«ADR + C4 как обязательное ядро, RFC и Concept Doc по наследованию от
Хаба, arc42-lite и Diátaxis — по мере роста».** Это AI-native, docs-as-code,
итеративно, трассируемо и наглядно — все 5 критериев закрыты композицией, при
этом стартовая церемония минимальна (Anti-Inflation).

### Как это ложится на структуру портал-спока

- `docs/adr/` — ADR (уже в `templates/spoke/`).
- `docs/architecture.md` + Mermaid `C4Context`/`C4Container` — C4 (вводится в Phase 0–1).
- `learning/`, `knowledge-base/` — Diátaxis (Phase 1+).
- RFC крупных решений — `governance/proposals/` Хаба или `docs/` спока.

Связь со стандартом структуры: [research/portal/repository-structure-design-2026-06.md](repository-structure-design-2026-06.md)
и [standards/PORTAL_REPOSITORY_STRUCTURE.md](../../standards/PORTAL_REPOSITORY_STRUCTURE.md).

## Решение за человеком

Это исследование рекомендует, но не вводит обязательный стандарт. Финальное
решение по тому, какой набор сделать обязательным для порталов, принимает
фаундер в рамках RFC
[open-ai-portal-concept-rfc.md](../../governance/proposals/open-ai-portal-concept-rfc.md)
(см. эскалацию «нужен новый обязательный standard, но нет comparison» в
[AI_GOVERNANCE.md](../../AI_GOVERNANCE.md) — это comparison закрывает её).

### Вопросы для согласования

1. Утвердить **ADR + C4** как обязательное ядро документации для порталов?
2. Достаточно ли C4 через Mermaid (`C4Context`/`C4Container`), или нужен
   Structurizr DSL (богаче, но +инструмент)?
3. Вводить ли Diátaxis сразу в Phase 1 для пользовательских разделов, или
   отложить до появления реального объёма документации?

## Источники

- C4 Model — Simon Brown, [c4model.com](https://c4model.com) (стабилен).
- arc42 — [arc42.org](https://arc42.org), раздел 9 «Architecture Decisions» — [docs.arc42.org/section-9](https://docs.arc42.org/section-9/).
- ADR — M. Nygard, «Documenting Architecture Decisions», 2011; [adr.github.io](https://adr.github.io); коллекция шаблонов — [github.com/joelparkerhenderson/architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record).
- RFC 2119 / BCP 14 — нормативные ключевые слова — [rfc-editor.org/rfc/rfc2119](https://www.rfc-editor.org/rfc/rfc2119).
- Diátaxis — Daniele Procida, [diataxis.fr](https://diataxis.fr).
- ISO/IEC/IEEE 42010:2022 — [iso.org/standard/74393.html](https://www.iso.org/standard/74393.html).
- Внутренние: [CONCEPT.md](../../CONCEPT.md), [governance/proposals/contract-executability-rfc.md](../../governance/proposals/contract-executability-rfc.md), [templates/spoke/README.md](../../templates/spoke/README.md).
