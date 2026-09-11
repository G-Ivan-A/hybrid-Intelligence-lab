---
status: draft
version: 0.1
updated: 2026-09-08
temperature: 0.1
owner: G-Ivan-A
scope: ecosystem
level: L0-L3
related_standards:
  - "standards/glossary.md"
  - "standards/standard-meta-structure.md"
  - "standards/product-profile.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/563"
---

# Product Taxonomy Reference

## Purpose

Справочник задаёт **единственную в Хабе точку ссылки** на продуктовую
таксономию: четыре уровня классификации функциональности и цепочку наследования
`L0 (индустрия) → L1 (ИТ/телеком) → L2/L3 (Манго)`.

Артефакт нужен потому, что таксономия до сих пор существовала только в споке
([`mango_ba_prompts/standards/product-classification-contract.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md),
`scope: mango-only`), а общая методология формируется в Хабе. Ссылка Хаба на
`mango-only` артефакт спицы делает наследование перевёрнутым: норма зависела бы
от проекта, который её применяет.

Справочник **не** вводит новую классификацию. Уровни, определения, источники и
правила унаследованы из контракта спицы, а не переизобретены.

## Scope

| Входит | Не входит |
| --- | --- |
| Уровни `Domain → Capability → Feature → Atomic Function`, их определения, источники и правила отнесения. | Каталог конкретных доменов, capability и features проекта. |
| Отображение терминов предметной области на международные (пример: Манго). | Операционные правила промптов, маршрутов, прогонов и артефактов проекта. |
| Правило наследования уровней `L0 → L1 → L2/L3`. | Профили заполнения слотов документа (`P-SETTINGS`, `P-NO-SETTINGS`, `P-API`, `P-DEVICE`) — они в [модуле микро-структуры](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/artifact-micro-structure/20-taxonomy.md). |

Каталог значений остаётся в споке. Хаб владеет **формой** классификации, спица —
её **содержанием**: иначе появляется второй источник истины по продуктам.

## Identification and Placement

| Элемент | Правило |
| --- | --- |
| Canonical path | `standards/product-taxonomy-reference.md`. |
| Artifact class | Справочный стандарт (reference), IL-3 Markdown в `standards/`. |
| Naming | kebab-case по [`standards/file-naming.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/file-naming.md); не date-first, потому что это живой справочник, а не датированное наблюдение. |
| Normative source | [`mango_ba_prompts/standards/product-classification-contract.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md) v0.1 — источник уровней; при расхождении содержания каталога приоритет у спицы, при расхождении **формы** уровней — у этого справочника. |
| Meta-structure | [`standards/standard-meta-structure.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/standard-meta-structure.md) (F10). |

## Frontmatter

Базовые поля по
[`standards/frontmatter-standard.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/frontmatter-standard.md)
плюс `owner`. Поле `ai-generated` контракта спицы **не переносится**: оно
запрещено правилом 5 базового стандарта. Поле `scope: mango-only` заменено на
`scope: ecosystem`: справочник в Хабе описывает форму, применимую за пределами
одного проекта.

## Minimum Body Sections

### Уровни классификации

```text
L0  Индустриальный базис        — источники: TM Forum SID/eTOM, BABOK, IREB, UNSPSC
 └─ L1  ИТ / телеком            — отраслевая специализация базиса
     └─ L2  Домены проекта      — Domain, Capability
         └─ L3  Функции проекта — Feature, Atomic Function
```

Иерархия классификации внутри проекта:

```text
Domain (Семейство)
  → Capability (Класс)
    → Feature (Подкласс)
      → Atomic Function (Функция)
```

| Уровень | Назначение | Ключевой вопрос |
| --- | --- | --- |
| `Domain` | Крупная бизнес-область продукта или сервиса. | В какой продуктовой или сервисной зоне находится требование? |
| `Capability` | Группа функций, решающая бизнес-задачу в домене. | Какую способность должен иметь продукт или команда? |
| `Feature` | Настраиваемая возможность внутри capability. | Что именно пользователь или администратор включает, настраивает или использует? |
| `Atomic Function` | Минимальная проверяемая единица функциональности. | Какую неделимую функцию, параметр или правило можно протестировать отдельно? |

### Domain (Семейство)

**Определение.** Крупная бизнес-область, объединяющая связанные возможности,
продукты, процессы и требования.

**Источники (L0).** TM Forum SID `Domain` как группировка связанных business
entities; UNSPSC `Segment` как верхний уровень товарно-сервисной классификации;
BABOK `domain` как сфера знаний с общими требованиями и терминологией.

**Правило.** Domain не описывает конкретную функцию. Он нужен для
маршрутизации, назначения владельца, верхнего отчёта и границ анализа.

### Capability (Класс)

**Определение.** Группа функций, решающая конкретную бизнес-задачу в рамках
домена и выражающая способность продукта, сервиса или команды достигать
результата.

**Источники (L0/L1).** BABOK `capability`; TM Forum SID как общий язык
сущностей CSP; TM Forum eTOM для группировки действий service provider по
областям customer, product, service, resource.

**Правило.** Capability формулируется достаточно крупно, чтобы объединять
несколько features, и достаточно конкретно, чтобы назначить владельца и
evidence.

### Feature (Подкласс)

**Определение.** Конкретная настраиваемая возможность внутри capability,
реализующая связанный набор требований и дающая ценность группе stakeholders.

**Источники (L0/L1).** BABOK `feature`; IREB `functional requirement`.

**Правило.** Feature применима в пользовательском, административном или
интеграционном сценарии. Если элемент является только техническим параметром,
это обычно `Atomic Function`.

### Atomic Function (Функция)

**Определение.** Минимальная неделимая единица функциональности с
бизнес-ценностью или проверяемым эффектом, которую можно независимо описать,
настроить, протестировать или связать с критерием приёмки.

**Источники (L0/L1).** IREB requirement quality и `functional requirement`;
IREB `user story` как atomic backlog item; TM Forum product/service modeling для
atomic product/service specification. Термин `Atomic Function` является
адаптацией уровня L2/L3, а не отдельным общим стандартом.

**Правило.** Atomic function не делится дальше без потери смысла проверки. Если
параметр требует отдельной политики, SLA или compliance-review, это по-прежнему
atomic function плюс overlay, а не новый domain.

### Отображение терминов проекта на международные

Таблица показывает **форму** отображения `термин проекта → международный аналог
→ источник`. Значения приведены на примере Манго (L2) и являются иллюстрацией
формы, а не каталогом.

| Термин проекта | Международный аналог | Источник |
| --- | --- | --- |
| Виртуальная АТС | UCaaS / Hosted PBX | TM Forum Product/Service |
| Исходящий обзвон | Outbound Campaign / Outbound Contact | TM Forum Customer Interaction |
| Обратный звонок | Callback / Callback Scheduling | TM Forum Customer Interaction, IREB |
| Запись разговоров | Call Recording | TM Forum Service Usage |
| Голосовое меню IVR | Interactive Voice Response (IVR) | TM Forum Customer Interaction |
| Распределение звонков | Automatic Call Distribution / Routing | TM Forum Customer Interaction |
| Омниканальные коммуникации | Omnichannel Customer Interaction | TM Forum Customer Centricity, eTOM |
| Речевая аналитика | Speech Analytics / Voice Recognition Software | UNSPSC `43233413` |
| Управление качеством | Quality Management / Compliance Software | TM Forum Service Assurance, UNSPSC `43232606` |
| Интеграция с CRM | CRM Integration / External Interface | BABOK External Interface, TM Forum Open APIs |

**Правило неполноты.** Если входящий термин не находится в источниках или не
имеет устойчивого аналога, он помечается как `⚠️ требуется уточнение`,
сохраняется ближайший рабочий mapping, и анализ не блокируется. Полный список
терминов, требующих уточнения, ведётся в споке.

## Type Model

`N/A + rationale`: справочник не вводит архетипов и профилей. Единственная
типизация — четыре уровня выше; их расширение означает новую версию
справочника, а не новый тип.

## Lifecycle

| Переход | Условие |
| --- | --- |
| `draft → accepted` | Подтверждение владельцем продукта и наличие хотя бы одного проекта, ссылающегося на справочник вместо контракта спицы. |
| Изменение уровней | Только через новую версию справочника; уровень не удаляется молча, потому что на него ссылаются артефакты. |
| Расхождение со спицей | Разрешается в пользу спицы по **содержанию каталога** и в пользу Хаба по **форме уровней**. |

## Boundaries

- **Справочник ↔ глоссарий.** Значения общих терминов —
  [`standards/glossary.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/glossary.md);
  здесь только классификация функциональности.
- **Справочник ↔ контракт спицы.** Спица владеет каталогом значений и
  проектными правилами применения; Хаб — формой уровней.
- **Справочник ↔ микро-структура артефакта.** Профили заполнения слотов
  документа выводятся из продуктового класса, но живут в
  [модуле микро-структуры](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/artifact-micro-structure/20-taxonomy.md).
- **Справочник ↔ мета-модель.** Продукт как сущность мета-модели и его связь с
  артефактом описаны в
  [`projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md).

## Validation

Машинно проверяется только присутствие файла в реестре структуры
([`tools/validate-repository-structure.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/validate-repository-structure.sh))
и frontmatter
([`tools/validate-frontmatter.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/validate-frontmatter.sh)).
Проверка отнесения конкретного требования к уровню машинной не является и
выполняется на гейте `G-human`: правило «Domain не описывает функцию»
неформализуемо без каталога значений, который живёт в споке.

## Related Artifacts

- [`mango_ba_prompts/standards/product-classification-contract.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/product-classification-contract.md)
  — источник уровней и каталог значений.
- [`projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md)
  — четыре канонические таксономии мета-модели, включая продуктовую.
- [`standards/product-profile.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/product-profile.md)
  — профиль продуктового spoke-проекта.

## Источники

- TM Forum, Information Framework (SID): <https://www.tmforum.org/open-digital-architecture/information-framework-sid/>
- TM Forum, Business Process Framework (eTOM): <https://www.tmforum.org/oda/business/process-framework-etom/>
- IIBA, BABOK Guide Appendix A Glossary: <https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/glossary/>
- IREB, CPRE Glossary: <https://cpre.ireb.org/en/downloads-and-resources/glossary>
- UNDP, United Nations Standard Products and Services Code: <https://www.undp.org/unspsc>
