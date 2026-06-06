---
status: draft
version: 0.1
updated: 2026-06-06
ai-generated: true
type: external-analysis
context: [portal, concept-document, standardization, modularity, roadmap, research-link]
method: comparative-analysis
scope: portal
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/166"
related_artifacts:
  - "standards/webportal-concept-standard.md"
  - "research/portal/documentation-standards-comparison-2026-06.md"
  - "research/portal/open-ai-portal-concept-rfc.md"
  - "standards/portal-repository-structure.md"
  - "standards/research-profile.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/166"
---

# Исследование: сравнение подходов к стандартизации концепции портала

Версия: 0.1

Дата: 2026-06-06

Статус: черновик исследования (`draft`). Перевод в `reviewed` и утверждение
производного стандарта как обязательного — за фаундером (см. «Решение за
человеком», [AI_GOVERNANCE.md](../../AI_GOVERNANCE.md), правило 4).

## 1. Введение

**Причина.** В Хабе нет стандарта структуры **концепции проекта создания
портала** — документа, который описывает *что и зачем строим* до выбора
архитектуры, стека и структуры репозитория. Соседнее исследование
[documentation-standards-comparison-2026-06.md](documentation-standards-comparison-2026-06.md)
закрыло другой слой — *формат документации* (C4, ADR, RFC, Diátaxis), то есть
*как описываем уже принятые решения*. Слой «структура концепции» (PRD, Vision,
TOGAF-фазы) остался непокрытым. Без него каждая новая концепция портала пишется
с нуля, разного объёма и полноты, что повторяет операционную боль
«непредсказуемый bootstrap» из
[research/hub/project-context-and-bootstrap-patterns-2026-05.md](../hub/project-context-and-bootstrap-patterns-2026-05.md).

**Цель.** Сравнить ≥5 признанных подходов к стандартизации концепций и выбрать
основу для **универсального модульного стандарта** структуры концепции портала
— применимого от простого многостраничника до сложного app-портала. Выход
исследования — [standards/webportal-concept-standard.md](../../standards/webportal-concept-standard.md).

**Связанные артефакты.**
- Стандарт-адресат (выход): [standards/webportal-concept-standard.md](../../standards/webportal-concept-standard.md).
- Профиль и правила оформления: [standards/research-profile.md](../../standards/research-profile.md), [standards/research-documentation-standard.md](../../standards/research-documentation-standard.md).
- Смежный слой (формат документации): [documentation-standards-comparison-2026-06.md](documentation-standards-comparison-2026-06.md).
- Структура репозитория портала (куда концепция «приземляется»): [standards/portal-repository-structure.md](../../standards/portal-repository-structure.md).
- Существующая концепция-RFC (кандидат на оценку по новому стандарту): [open-ai-portal-concept-rfc.md](open-ai-portal-concept-rfc.md).

**Метод.** Сравнительный анализ (`comparative-analysis`) 8 подходов по 7
критериям из issue #166 с матрицей применимости и обоснованием каждой оценки.
Источники — публичные канонические спецификации и общепринятые описания
практик. Оценки «узнаваемости» и «простоты» носят экспертный характер и
проверяются на практике при первом применении стандарта.

> Терминология — по [standards/glossary.md](../../standards/glossary.md)
> (термины `Concept`, `Standard`, `Draft`, `Canonical` не переопределяются).
> Нормативные ключевые слова — [RFC 2119 / BCP 14](https://www.rfc-editor.org/info/bcp14).

## 2. Результаты исследования

### 2.1. Главный вывод

**Единого готового стандарта-победителя нет.** Подходы делятся на два класса:

- **Тяжёлые формальные фреймворки** (ISO/IEC/IEEE 42010, TOGAF, BABOK) — полны и
  узнаваемы, но не модульны «из коробки», предполагают большой upfront-документ
  и высокий порог входа. Противоречат Anti-Inflation principle Хаба
  ([governance/REPO_MODEL.md](../../governance/REPO_MODEL.md)) на старте.
- **Лёгкие продуктовые форматы** (PRD, Vision Document, Concept Doc, RFC,
  Continuous Discovery) — модульны, итеративны, низкий порог входа, но поодиночке
  не покрывают весь спектр от сайта-визитки до сложного app.

**Рекомендуемая основа стандарта — гибрид «PRD-ядро + слой Vision + модульность
TOGAF-deliverables»:**

| Что берём | Откуда | Зачем |
| --- | --- | --- |
| Обязательное ядро разделов (Summary, Vision/Goals, Scope, Risks, Metrics) | **PRD** (Cagan/SVPG, Intercom) | Признанное продуктовое ядро, низкий порог, итеративность. |
| Раздел «Видение и цели» как точка старта | **Vision Document** (RUP / Product Vision Board) | Отделяет «зачем» от «что»; работает даже для сайта-визитки. |
| Принцип «обязательные + опциональные разделы по уровню сложности» | **TOGAF** (tailoring of deliverables) + **arc42** (lite-скелет) | Даёт модульность: берём ядро, добавляем разделы по росту. |
| Нормативный язык и «живой» документ через обсуждение | **RFC** (IETF/Rust) | Согласование roadmap и эволюция концепции. |
| Связь «концепция → исследования → пересмотр» | **Continuous Discovery** (Torres) | Концепция как живая гипотеза, а не финальный план. |
| Слои требований (ФТ/НФТ, архитектура, данные, безопасность) | **BABOK** + **42010** (по росту) | Опциональные разделы для сложного app-портала. |

Эта основа закрывает все 7 критериев issue #166: **модульность** (ядро +
опции), **масштабируемость** (визитка → app), **связь с roadmap** (RFC-обсуждение
+ обязательный раздел Roadmap), **связь с исследованиями** (Continuous Discovery
+ явный раздел), **гибкость** (tailoring), **узнаваемость** (PRD/Vision/TOGAF —
индустриальные термины), **примеры** (у всех источников есть публичные образцы).

### 2.2. Рекомендации

| # | Рекомендация | Куда фиксируется |
| --- | --- | --- |
| 1 | Принять гибрид «PRD-ядро + Vision-слой + TOGAF-модульность» как основу стандарта концепции портала. | [standards/webportal-concept-standard.md](../../standards/webportal-concept-standard.md) |
| 2 | Зафиксировать **6 обязательных** разделов (Summary, Vision & Goals, Scope, Roadmap, Risks & Mitigation, Success Metrics) и **9 опциональных** (ФТ, НФТ, Architecture, Tech Stack, Data Model, Integrations, Security & Privacy, Deployment & Ops, Appendices). | Стандарт, §«Структура концепции» |
| 3 | Каждый раздел снабдить **минимальной и расширенной** версией (модульная глубина). | Стандарт + шаблон |
| 4 | Roadmap сделать **обязательным** разделом/документом-спутником; явно описать принцип «живой экосистемы» (после roadmap концепция может измениться). | Стандарт, §«Связь с roadmap» |
| 5 | Явно перечислить, какие исследования порождает концепция (стек, архитектура, структура репозитория) и как их результаты возвращаются в концепцию. | Стандарт, §«Связь с исследованиями» |
| 6 | Зафиксировать, что концепция **не** определяет структуру репозитория напрямую — структура выбирается из политики Хаба (`portal-repository-structure.md`) на её основе. | Стандарт, §«Связь со структурой репозитория» |
| 7 | Приложить копируемый шаблон концепции и чек-лист полноты. | [templates/webportal-concept-template.md](../../templates/webportal-concept-template.md) + приложение стандарта |
| 8 | Оценку существующего [open-ai-portal-concept-rfc.md](open-ai-portal-concept-rfc.md) на соответствие стандарту провести **после** утверждения стандарта; рефакторинг в этой задаче не выполнять. | Backlog / отдельная issue |

### 2.3. Открытые вопросы

1. Делать ли Roadmap **разделом** концепции или **обязательным документом-спутником**
   (`ROADMAP.md`)? Рекомендация — разрешить оба варианта, но требовать наличие.
2. Нужен ли отдельный машиночитаемый индекс разделов (frontmatter `sections:`)
   для AI-агентов, или достаточно Markdown-заголовков? (Кандидат в backlog.)
3. Достаточно ли одного стандарта для всего спектра, или сайту-визитке нужен
   отдельный «микро-профиль»? Рекомендация — один стандарт, профиль не плодить
   (Anti-Inflation), пока не появится повторяющаяся боль.

### 2.4. Учёт мнения команды Q

Команда Q предложила структуру из 15 разделов (6 обязательных + 9 опциональных)
и связанные документы (`ROADMAP.md`, `RESEARCH/`, `REPOSITORY_STRUCTURE.md`).
Мнение — **вход, не догма** (режим `creative`).

| Пункт Q | Решение | Обоснование |
| --- | --- | --- |
| 6 обязательных разделов (Summary, Vision & Goals, Scope, Roadmap, Risks, Metrics) | ✅ **Согласие** | Совпадает с PRD-ядром индустрии; минимальный набор закрывает «зачем/что/границы/риски/успех». |
| 9 опциональных разделов | ✅ **Согласие** с уточнением | Принимаем, но добавляем правило «минимальная/расширенная версия» каждого раздела — это и есть модульность глубины из issue. |
| Roadmap как часть концепции **или** отдельный документ | ✅ **Согласие** | Подтверждено практикой RFC и продуктовых PRD; фиксируем оба варианта при обязательности наличия. |
| `REPOSITORY_STRUCTURE.md` как «связанный документ» концепции | 🟡 **Частичное несогласие** | Концепция **не** порождает структуру репозитория напрямую (явное требование issue). Структура выбирается из политики Хаба ([portal-repository-structure.md](../../standards/portal-repository-structure.md)) **на основе** концепции. Поэтому это не «документ концепции», а **следствие** через политику Хаба. |
| «От простого к сложному, добавляя и углубляя» | ✅ **Согласие** | Это и есть гибрид tailoring (TOGAF) + минимальная/расширенная версия раздела. |

## 3. Детализация

### 3.1. Кандидаты

| # | Подход | Что это | Канонический источник |
| --- | --- | --- | --- |
| 1 | **ISO/IEC/IEEE 42010** | Стандарт описания архитектуры через stakeholders → concerns → viewpoints → views. | ISO/IEC/IEEE 42010:2022 — [iso.org/standard/74393.html](https://www.iso.org/standard/74393.html) |
| 2 | **TOGAF** (ADM + deliverables) | Корпоративный фреймворк архитектуры; фазы A–H, каталог deliverables (в т.ч. Architecture Vision, Statement of Architecture Work). | The Open Group — [pubs.opengroup.org/togaf-standard](https://pubs.opengroup.org/togaf-standard/) |
| 3 | **BABOK** | Свод знаний бизнес-анализа: области знаний, требования (бизнес/stakeholder/solution/transition). | IIBA — [iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/](https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/) |
| 4 | **Continuous Discovery** | Непрерывное открытие: Opportunity Solution Tree, eженедельный контакт с пользователем, гипотезы. | T. Torres, «Continuous Discovery Habits», 2021 — [producttalk.org](https://www.producttalk.org/) |
| 5 | **PRD** (Product Requirements Document) | Продуктовый документ: проблема, цели, пользователи, scope, требования, метрики. | M. Cagan / SVPG — [svpg.com](https://www.svpg.com/); Intercom — [intercom.com/blog/product-requirement-documents](https://www.intercom.com/blog/product-requirement-documents/) |
| 6 | **RFC** (Request for Comments) | Структурированное предложение с обсуждением и нормативным языком (MUST/SHOULD/MAY). | IETF RFC 2119/7322; Rust RFCs — [github.com/rust-lang/rfcs](https://github.com/rust-lang/rfcs) |
| 7 | **Concept Doc** (Google/Amazon/Microsoft) | Внутренние форматы: Google Design Doc, Amazon PR/FAQ + 6-pager, Microsoft one-pager/spec. | Amazon Working Backwards; Google design docs (industry write-ups) |
| 8 | **Vision Document** | Документ видения: проблема, целевая аудитория, ценностное предложение (RUP Vision, Product Vision Board). | RUP Vision; R. Pichler Product Vision Board — [romanpichler.com](https://www.romanpichler.com/tools/vision-board/) |

### 3.2. Критерии оценки (из issue #166)

1. **Применимость к порталам разной сложности** — годится ли от сайта-визитки до сложного app.
2. **Модульность** — можно ли брать только часть разделов.
3. **Связь с roadmap** — встроена ли связь с планом развития.
4. **Связь с исследованиями** — порождает ли документ исследования (стек, архитектура).
5. **Гибкость** — можно ли расширять «от простого к сложному», углубляя разделы.
6. **Узнаваемость в индустрии** — насколько термины и структура общеприняты.
7. **Примеры использования** — есть ли публичные образцы.

Шкала: 🟢 сильно / 🟡 частично / 🔴 слабо.

### 3.3. Матрица применимости

| Подход | Сложность | Модульность | Roadmap | Исследования | Гибкость | Узнаваемость | Примеры | Итог (🟢) |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **ISO 42010** | 🟡 | 🔴 | 🔴 | 🟡 | 🔴 | 🟢 | 🟡 | 2 |
| **TOGAF** | 🟢 | 🟡 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 5 |
| **BABOK** | 🟢 | 🟡 | 🟡 | 🟢 | 🟡 | 🟢 | 🟡 | 3 |
| **Continuous Discovery** | 🟡 | 🟢 | 🟡 | 🟢 | 🟢 | 🟡 | 🟡 | 3 |
| **PRD** | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 6 |
| **RFC** | 🟡 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 5 |
| **Concept Doc** | 🟢 | 🟢 | 🟡 | 🟡 | 🟢 | 🟡 | 🟢 | 4 |
| **Vision Document** | 🟢 | 🟢 | 🟡 | 🔴 | 🟢 | 🟢 | 🟢 | 5 |

### 3.4. Обоснование оценок

- **ISO/IEC/IEEE 42010.** Узнаваем и силён формальной строгостью (🟢
  узнаваемость), но это стандарт *описания архитектуры*, а не концепции проекта:
  не модульный для сайта-визитки (🔴), не содержит roadmap (🔴), высокий порог,
  тяжёлый upfront (🔴 гибкость). Для концепции — источник идеи «stakeholders →
  concerns» (полезно в опциональном разделе НФТ/Architecture), но не основа.
- **TOGAF.** Богатый каталог deliverables, среди которых **Architecture Vision**
  и **Statement of Architecture Work** — близкие аналоги концепции. Ключевая
  ценность для нас — принцип **tailoring**: брать из каталога только нужные
  артефакты под масштаб (🟢 сложность, 🟢 roadmap через ADM, 🟢 исследования
  через Phase A/B). Но «из коробки» он корпоративно-тяжёл (🟡 модульность,
  гибкость). Берём **принцип модульности deliverables**, не весь ADM.
- **BABOK.** Чёткая иерархия требований (business → stakeholder → solution →
  transition) — отличная основа для опциональных разделов ФТ/НФТ сложного app
  (🟢 исследования, 🟢 сложность). Но это свод знаний аналитика, не шаблон
  документа (🟡 модульность/гибкость как готовой структуры). Берём слой
  требований.
- **Continuous Discovery.** Даёт главную идею «живой управляемой экосистемы» из
  issue: концепция — это **гипотеза**, которая меняется после контакта с
  пользователем и исследований (🟢 гибкость, 🟢 связь с исследованиями). Слаб как
  документная структура (🟡 узнаваемость в роли стандарта документа). Берём
  принцип итеративного пересмотра концепции после roadmap/исследований.
- **PRD.** Лучшее соотношение «покрытие/порог входа». Типовое ядро PRD (проблема,
  цели, пользователи, scope, требования, метрики, риски) почти 1:1 ложится на 6
  обязательных разделов Q (🟢 по большинству критериев). Модулен и итеративен,
  узнаваем в индустрии, множество публичных шаблонов (Intercom, SVPG). Связь с
  исследованиями неявная (🟡) — дополняем разделом из Continuous Discovery.
  **Основа ядра стандарта.**
- **RFC.** Силён «живым» обсуждением и нормативным языком — это механизм
  **согласования roadmap** и эволюции концепции (🟢 roadmap, гибкость). Уже
  practice Хаба (`governance/rfc/`, `open-ai-portal-concept-rfc.md`). Как
  *структура концепции* избыточно процедурен для сайта-визитки (🟡 сложность).
  Берём механизм обсуждения и нормативный словарь.
- **Concept Doc (Google/Amazon/Microsoft).** Amazon PR/FAQ («работай назад от
  пресс-релиза») и 6-pager — отличный приём для **Executive Summary** и проверки
  ценности до разработки (🟢 примеры, модульность). Google Design Doc ближе к
  техническому дизайну (пересекается с documentation-standards). Менее
  стандартизованы как термин (🟡 узнаваемость). Берём приём PR/FAQ для Summary.
- **Vision Document.** RUP Vision и Product Vision Board дают сжатый,
  масштабируемый слой «зачем/для кого/ценность», работающий даже для простейшего
  сайта (🟢 сложность, гибкость, узнаваемость). Почти не касается исследований и
  технических слоёв (🔴 исследования). Берём как **обязательный раздел Vision &
  Goals**.

### 3.5. Синтез: почему гибрид, а не один стандарт

Каждый подход силён в своём слое и они **ортогональны**: Vision — «зачем», PRD —
«что и для кого», TOGAF/BABOK/42010 — «как (опционально, по росту)», RFC —
«как согласуем и эволюционируем», Continuous Discovery — «как живёт и меняется».
Навязать один — значит либо утонуть в церемониях (TOGAF/42010 для визитки), либо
потерять масштабируемость до app (чистый Vision). Поэтому стандарт строится как
**модульная композиция**: лёгкое продуктовое ядро (PRD + Vision), расширяемое
опциональными слоями (BABOK/42010/TOGAF) по мере роста, с RFC-механизмом
согласования и Continuous-Discovery-принципом живого пересмотра.

Это согласуется и с выводом соседнего исследования формата документации
([documentation-standards-comparison-2026-06.md](documentation-standards-comparison-2026-06.md)):
«оптимум — минимальная композиция, а не один монолит».

### 3.6. Связь со структурой репозитория (важное уточнение issue)

Issue прямо требует: концепция **не** определяет структуру репозитория. Это
подтверждается разделением слоёв: концепция отвечает на «зачем/что», а структура
репозитория — следствие выбора стека и архитектуры, которые исследуются
**после** концепции. В Хабе структура портал-спока уже стандартизована в
[standards/portal-repository-structure.md](../../standards/portal-repository-structure.md)
и [research/portal/repository-structure-design-2026-06.md](repository-structure-design-2026-06.md).
Поэтому стандарт концепции лишь **ссылается** на политику Хаба, из которой
структура выбирается или дорабатывается.

### 3.7. Оценка существующей концепции-RFC (без рефакторинга)

[open-ai-portal-concept-rfc.md](open-ai-portal-concept-rfc.md) уже содержит
бóльшую часть рекомендуемых разделов (видение, слоганы, сравнение вариантов,
roadmap Phase 0–4, структура, план миграции, запрос на согласование). Беглая
сверка показывает высокое соответствие будущему стандарту, но это **наблюдение**,
а не задача: issue прямо запрещает рефакторинг существующих концепций до
исследования и утверждения стандарта. Полную оценку соответствия следует
вынести в отдельную issue после перевода стандарта в `canonical`.

## 4. Источники

- ISO/IEC/IEEE 42010:2022 — [iso.org/standard/74393.html](https://www.iso.org/standard/74393.html) (требует проверки версии перед фиксацией).
- TOGAF Standard, 10th Edition — The Open Group, [pubs.opengroup.org/togaf-standard](https://pubs.opengroup.org/togaf-standard/); Architecture Vision deliverable.
- BABOK Guide v3 — IIBA, [iiba.org](https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/).
- Teresa Torres, «Continuous Discovery Habits», 2021 — [producttalk.org](https://www.producttalk.org/).
- Marty Cagan / SVPG — [svpg.com](https://www.svpg.com/); Intercom, «Product requirement documents» — [intercom.com/blog/product-requirement-documents](https://www.intercom.com/blog/product-requirement-documents/).
- IETF RFC 2119 / BCP 14 — [rfc-editor.org/rfc/rfc2119](https://www.rfc-editor.org/rfc/rfc2119); RFC 7322 (RFC Style Guide); Rust RFCs — [github.com/rust-lang/rfcs](https://github.com/rust-lang/rfcs).
- Amazon «Working Backwards» (PR/FAQ, 6-pager) — Colin Bryar & Bill Carr, 2021.
- Roman Pichler, Product Vision Board — [romanpichler.com/tools/vision-board](https://www.romanpichler.com/tools/vision-board/); RUP Vision Document.
- Внутренние: [standards/research-profile.md](../../standards/research-profile.md), [standards/research-documentation-standard.md](../../standards/research-documentation-standard.md), [standards/portal-repository-structure.md](../../standards/portal-repository-structure.md), [research/portal/documentation-standards-comparison-2026-06.md](documentation-standards-comparison-2026-06.md), [standards/glossary.md](../../standards/glossary.md), [AI_GOVERNANCE.md](../../AI_GOVERNANCE.md).
