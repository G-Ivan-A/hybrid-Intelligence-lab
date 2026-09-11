---
status: draft
version: 0.2
updated: 2026-09-10
temperature: 0.3
type: research
context: [ba, methodology, meta-model, taxonomy, actor, execution-package, gigacode, deprecation, traceability, issue-563, issue-571]
method: synthesis + corpus-measurement + entity-modeling + package-design
scope: mango-only
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/563"
based_on:
  - research/ba-requirements/2026-09-08-meta-model-inputs-facts.md
  - research/ba-requirements/exp/ba-meta-model-563/meta-model-inputs.json
  - research/ba-requirements/methodology-unification/10-theory.md
  - research/ba-requirements/artifact-micro-structure/20-taxonomy.md
related_artifacts:
  - "docs/adr/2026-09-adr-013-run-modes-deprecation.md"
  - "docs/adr/2026-09-adr-015-process-operation-taxonomy-rebuild.md"
  - "projects/ba-gigacode-implementation/ba-process-taxonomy/20-taxonomy.md"
  - "projects/ba-gigacode-implementation/ba-operation-taxonomy/20-taxonomy.md"
  - "standards/product-taxonomy-reference.md"
  - "research/ba-requirements/orchestration/00-introduction.md"
  - "ops/backlog.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/563"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/561"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/557"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571"
---

# Каноническая BA Meta-Model и Execution Package

> **Модуль** оформлен по
> [Reference Research Pattern](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/rfc/2026-07-17-rfc-reference-research-pattern.md):
> `00` — рамка и навигация, `10` — сущности мета-модели и закон производства
> артефакта, `20` — четыре канонические таксономии, `30` — состав Execution
> Package и контракт скомпилированного навыка, `40` — модель производства
> BCREQ, вертикальный срез и метрики, `50` — незакрытое и бэклог.
> **Ссылки абсолютные** (требование issue #563). Единственное исключение —
> внутримодульные ссылки в
> [`40-practice-and-cases.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/40-practice-and-cases.md):
> правило `P2` требует относительной ссылки и проверяется машинно
> ([`tools/validate-rrp-links.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/validate-rrp-links.sh)).

## Зачем модуль существует

Исследовательская база БА к 2026-09-08 состоит из пяти модулей конвейера
(`M0`–`M4`) и двух ортогональных осей — макро (`methodology-unification/`) и
микро (`artifact-micro-structure/`). Каждый модуль внутренне связен, но между
модулями одно и то же названо по-разному: гейты описаны трижды, операция и
навык различаются только в одном модуле, обратная связь живёт и в `M3`, и в
шаге `S7` макро-оси.

Issue [#563](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/563)
останавливает расширение теории и ставит две задачи: **свести накопленное к
одной мета-модели** и **скомпилировать из неё минимальный исполняемый пакет**,
которым можно запустить сквозной вертикальный срез в GigaCode. Модуль не
добавляет нового слоя поверх существующих — он объявляет, какие сущности
канонические, а какие являются их проекциями.

**Область применимости (версия 0.2).** Мета-модель специализирована под
предметную область КК Манго и среду исполнения GigaCode. Универсальность **не
утверждается**: `L0` и `L1` процессной таксономии унаследованы из BABOK Guide v3
и переносимы по построению, а `L2`, `L3` и словарь операций выведены из одной
предметной области. Переносимость на другой домен — гипотеза дорожной карты
([`50-open-research.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/50-open-research.md)),
а не свойство модели.

**Что изменила версия 0.2**
([issue #571](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571)):
добавлены сущности `System` и `Actor` в расширенном значении, `Skill` объявлен
подпроцессом и самостоятельной сущностью, процессная и операционная таксономии
вынесены в отдельные модули и пересобраны на индустриальном базисе, а
унаследованные из спицы словари девяти процессов и тринадцати операций
депрекированы.

## BLUF: двенадцать утверждений

1. **Мета-модель состоит из одиннадцати сущностей.** `Product`, `System`,
   `Artifact`, `Operation`, `Skill`, `Process`, `Route`, `Actor`, `Gate`,
   `Contract`, `Trace`. Версия 0.2 добавила `System` — объект изменения, к
   которому предъявляются требования, — и перевела `Skill` из реализации
   операции в самостоятельную сущность. Всё остальное в накопленных модулях —
   проекция, а не новая сущность
   ([`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/10-theory.md), §2).
2. **Идентичность работы задаётся парой «операция + продуктовый класс».**
   Режим запуска (`stepwise`, `oneshot`, `legacy`) идентичностью не является и
   переведён в `deprecated`
   ([ADR-013](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-013-run-modes-deprecation.md)).
   Основание измеримо: 24 промпта на 13 способностей, средний Жаккар скелетов
   режимных вариантов — 0.077.
3. **Процесс → навыки (1:N) → операции (1:N).** Навык — не реализация
   операции, а **подпроцесс**: участок процесса с собственным входом, выходом,
   гейтом и правом ветвиться. Операция ветвиться не может и производит ровно
   один класс результата. Три сущности, слитые в корпусе спицы в один артефакт
   (промпт), разведены и связаны цепочкой вложения, а не отображением «многие к
   одному»
   ([`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/10-theory.md), §4).
4. **Гейт — одна сущность с тремя исполнителями.** `G-self` (агент проверяет
   себя), `G-mach` (валидатор), `G-human` (человек) — не три типологии из трёх
   модулей, а три значения поля `executor` одной сущности. Человеческие гейты
   `HG-0`…`HG-8` конвейера являются **экземплярами** `G-human`, а не параллельным
   словарём.
5. **Контракт отделён от гейта.** Контракт объявляет, каким должен быть
   артефакт; гейт — событие проверки контракта в конкретной точке маршрута.
   Один контракт проверяется несколькими гейтами; гейт без контракта запрещён.
6. **Прослеживаемость — сущность, а не свойство.** `Trace` связывает вход,
   операцию, актора, гейт и выход. Без неё ни одна метрика вертикального среза
   не вычислима: замер показывает, что 50 прогонов из 67 не ссылаются ни на один
   промпт, то есть цепочка «вход → работа → выход» сегодня не восстанавливается.
7. **Четыре таксономии канонические, пятая — служебная.** Артефакты,
   операции, процессы, продукты — канонические. Таксономия гейтов и контрактов
   служебная: она описывает не предмет работы, а её контроль
   ([`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md), §7).
8. **Продуктовая таксономия унаследована, а не изобретена.** Уровни
   `Domain → Capability → Feature → Atomic Function` перенесены в Хаб чистым
   справочником
   ([`standards/product-taxonomy-reference.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/product-taxonomy-reference.md));
   каталог значений остаётся в споке.
9. **Execution Package — компиляция, а не портирование.** В пакет уходят семь
   классов файлов; исследовательские тексты не переносятся. Скомпилированный
   `SKILL.md` самодостаточен: активных ссылок, по которым агент должен ходить во
   время исполнения, в нём нет, а версия слоёв объявлена во frontmatter
   ([`30-decision-framework.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/30-decision-framework.md), §3).
10. **Вертикальный срез запускается на одном артефакте.** MVP — `BCREQ` для
    одного продуктового класса: один маршрут, четыре навыка, три гейта, пять
    метрик. Расширение начинается только после накопления эмпирики на нём
    ([`40-practice-and-cases.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/40-practice-and-cases.md), §4).

11. **Историческое наследие — свидетельство о прошлом, а не базис новой
    нормы.** Промпты и прогоны дают факты о практике и не задают структуру и
    логику новых процессов: правила `LG-1`…`LG-6`, объявленное происхождение
    (`derived_from`, `EP-C6`, `SK-7`) и запрет обосновывать контракт ссылкой
    «так сделано в промпте»
    ([ADR-014](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-014-legacy-evidence-not-baseline.md)).
    Основание измеримо: 10 из 12 нормативных конструкций мета-модели
    отсутствуют во всех 24 активных промптах.

12. **Актор объявляется, а не изобретается.** `Актор` — общее понятие
    действующего лица: пользователь, заказчик, аналитик, AI-агент, валидатор.
    Перечень акторов задачи извлекается из источника операцией
    `extract-actors` и фиксируется в `A-CORE`; артефакт-проекция (диаграмма
    вариантов использования, пользовательская история) берёт акторов только
    оттуда. `Система` при этом — объект требований, а не исполнитель шага
    ([`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/10-theory.md), §2.1–§2.2).

## Что закрывают файлы модуля

| Контракт issue #563 | Где закрыт |
| --- | --- |
| 1. Депрекация `stepwise`/`oneshot`/`legacy` | [ADR-013](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-013-run-modes-deprecation.md), [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md) §6 |
| 2. Синтез четырёх канонических таксономий | [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md) §2–§5, [`standards/product-taxonomy-reference.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/product-taxonomy-reference.md) |
| 3. Визуализация модели производства артефакта | [`40-practice-and-cases.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/40-practice-and-cases.md) §2–§3 |
| 4. Состав Execution Package для GigaCode | [`30-decision-framework.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/30-decision-framework.md) §2–§5 |
| 5. Автономия исполнителя: выбор артефактов и их дома | [`50-open-research.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/50-open-research.md) §2 |
| План вертикального среза и сбора эмпирики | [`40-practice-and-cases.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/40-practice-and-cases.md) §4–§5 |
| Защита новой нормы от диктата наследия ([комментарий фаундера к PR #564](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/564)) | [ADR-014](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-014-legacy-evidence-not-baseline.md), §6.1 [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md), §7 [`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/10-theory.md), `EP-C6`/`SK-7` [`30-decision-framework.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/30-decision-framework.md) |
| Не выполнено и вопросы | [`50-open-research.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/50-open-research.md) §4 |

Контракты [issue #571](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571)
закрываются версией 0.2 и двумя новыми модулями.

| Контракт issue #571 | Где закрыт |
| --- | --- |
| Глубокий разбор дефектов действующей таксономии | [`2026-09-10-process-taxonomy-defects-facts.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-10-process-taxonomy-defects-facts.md) |
| Индустриальный базис процессов и дельта КК Манго | [`ba-process-taxonomy/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/projects/ba-gigacode-implementation/ba-process-taxonomy) |
| Гранулярность операций и связь с навыками | [`ba-operation-taxonomy/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/projects/ba-gigacode-implementation/ba-operation-taxonomy) |
| Однозначные определения артефактов (`A-CORE`, `A-TZ`, `A-BCREQ`, `A-REP`, `A-TRACE`) | [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md) §2 |
| Сущности `Система`, `Пользователь`, `Актор`, навык как подпроцесс | [`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/10-theory.md) §2, §4 |
| Маршрут как граф с ветвлениями по гейтам | [`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/10-theory.md) §6, [`30-decision-framework.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/30-decision-framework.md) §6.1 |
| Обязательная ссылка на источник в контракте человеческого гейта | [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md) §7, `GT-5` |
| Синтетические кейсы и эталоны | [`exp/ba-process-taxonomy-571/2026-09-10-synthetic-cases.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/2026-09-10-synthetic-cases.md) |
| Решение о пересборке | [ADR-015](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-015-process-operation-taxonomy-rebuild.md) |

## Доказательная база

- [`2026-09-08-meta-model-inputs-facts.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-08-meta-model-inputs-facts.md)
  — датированный замер входов мета-модели на коммите `8cbf82a`: режимы,
  дублирование способностей, покрытие словарей операций и процессов,
  продуктовая привязка прогонов.
- [`2026-09-09-legacy-normative-influence-facts.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-09-legacy-normative-influence-facts.md)
  — замер присутствия нормативных конструкций мета-модели в историческом
  корпусе и сплошной аудит происхождения нормативных блоков модуля; основание
  ADR-014.
- [`exp/ba-meta-model-563/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/research/ba-requirements/exp/ba-meta-model-563)
  — два измерителя, сырые результаты и логи прогонов.
- [`2026-09-08-artifact-structure-variance-facts.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-08-artifact-structure-variance-facts.md)
  — замер структуры результирующих документов (issue #561), основание для слоя
  артефакта в мета-модели.
- [`2026-09-07-ecosystem-knowledge-inventory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-07-ecosystem-knowledge-inventory.md)
  — инвентаризация 368 артефактов экосистемы, источник карты дублирований.

## Чего в модуле нет

- **Нет реализации пакета.** Модуль задаёт состав и контракты Execution
  Package, но не создаёт его файлы: их дом — исполняющая среда, а не
  исследовательский модуль Хаба
  ([`50-open-research.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/50-open-research.md), §2).
- **Нет переписывания модулей `M0`–`M4` и обеих осей.** Расхождения
  зафиксированы как отображение сущностей
  ([`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/10-theory.md), §5)
  и вынесены в бэклог, а не устранены правкой исторических текстов.
- **Нет продуктового каталога.** Домены, capability и features остаются в
  споке; Хаб владеет формой уровней.
- **Нет утверждённой нормы.** Модуль — исследование. Переход в норму идёт
  задачами `B-146`…`B-152` и `B-155`…`B-161`.
- **Нет заявки на универсальность.** Модуль описывает реализацию БА-процессов
  КК Манго в GigaCode. Перенос дома мета-модели в `projects/` и создание
  стандарта мета-модели — задачи дорожной карты `B-155` и `B-156`, а не
  содержание этой версии.
