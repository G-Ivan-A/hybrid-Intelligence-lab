---
status: accepted
version: 1.0
updated: 2026-09-24
temperature: 0.1
type: analysis
scope: mango-only
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/609"
related_artifacts:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-working-release-pipeline.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-requirements-run-forensics.md"
---

# Согласование архитектуры BCREQ и готовность Source к реализации

## Вердикт

**Можно переходить к изменениям модели контрактов и Source пакета.** Для
решений, которые определяют форму BCREQ, роли гейтов и границу
Working → Release, дополнительное архитектурное согласование не требуется.
Это не утверждение, что текущая Distribution уже исполняет принятые RFC.
Переход на новый runtime требует отдельной реализации, тестов и human review.

Полное правило «MANGO-first при ≥80% шаблонных требований внешнего ТЗ» пока
нельзя компилировать: нет утверждённого versioned каталога шаблонов, единицы
счёта и процедуры проверки совпадений. Точный TM Forum binding тоже не
заполняется без доступного authoritative snapshot. Эти пробелы не блокируют
Source-схему с явными `unresolved` и `not-applicable` состояниями и не дают
права подставлять похожие названия как точные ID.

## Граница и метод

Проверены [issue #609](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/609)
и приложенный к нему диалог, [PR #602](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/602),
[PR #604](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/604),
[PR #606](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/606),
[PR #608](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/608),
проектный README, три проектных RFC, два анализа, модули мета-модели,
таксономии, route/skills/schemas Distribution и тесты исполнения. Проверка
ссылок прошла по Markdown-файлам проекта. Первичный факт текущего runtime
взят из [route `n0`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/dist/execution-package-gigacode-cli/routes/rg-bcreq-v1.yaml)
и [навыка атрибуции](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/dist/execution-package-gigacode-cli/.gigacode/skills/product-attribution/SKILL.md),
а не из пересказа прежнего ассистента. Приложение issue использовано только
как контекст и не копируется в репозиторий.

Альтернативы проверены на границе: простой `n0` с выбором BA уже есть, но не
вычисляет первичную ось из типа работы; 80-процентное правило без шаблонного
каталога не является воспроизводимым; публичный SID Overview описывает
информационные домены, но не заменяет идентификатор capability. Поэтому
выбраны явный классификатор намерения, два типизированных industry binding и
отложенный измеримый порог.

## Согласованные уточнения и дом фиксации

| Источник | Итоговое правило | Дом и граница |
| --- | --- | --- |
| #602: 14 слотов, семь разделов, L1–L4, три Golden Form | 14 слотов остаются внутренней семантикой; L1 FR описывает наблюдаемую способность, L2–L4 раскрывают её. Три формы приняты как целевые кандидаты. | [RFC абстракции](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md) и [анализ форм](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-bcreq-golden-forms-and-feasibility.md); перенос в runtime Golden Set после воспроизводимого теста и human gate. |
| #602: Product routing | Тип работы задаёт первичную ось: MANGO-доработка/KB — MANGO; проверка практик и внешнего ТЗ — отрасль, затем MANGO. Все unmatched и uncertain сохраняются. | [RFC абстракции §5](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md); `P-08` остаётся оценкой ТЗ, а не формированием BCREQ по [таксономии процессов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/process-taxonomy/20-taxonomy.md). |
| #602: Порог 80% | До versioned каталога и правил подсчёта не является исполняемым условием. При наличии базы может выбирать порядок поиска, сохраняя полный отчёт о покрытии. | [RFC абстракции §5](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md); недостающий вход реализации указан ниже. |
| #602 и #604: `G-human` и `n0` | Агент предлагает mapping с правилом, evidence, альтернативами, риском и мотивированной рекомендацией; BA подтверждает/отклоняет mapping с причиной, не придумывает метод маршрута. `n0` остаётся ранним обязательным гейтом для BCREQ. | [RFC абстракции §5](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md); текущий [route](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/dist/execution-package-gigacode-cli/routes/rg-bcreq-v1.yaml) пока подтверждает лишь MANGO-цепочку. |
| #602: Content profiles | Профили API, ЛК, коммуникаций контакт-центра, клиента коммуникаций сотрудника и AI/автоматизации сочетаются. Роботы и речевая аналитика используют один AI-профиль с разными продуктовыми bindings. Видео не требует собственного профиля только по факту наличия capability. | [RFC абстракции §6](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md); продуктовые факты ограничены [снимком MANGO](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/product-taxonomy/mango-products.yaml). |
| #606: Pre-decomposition и три гейта | Evidence, goal/task/boundary, as-is→delta, product binding и claim register создаются в Working до FR/UC/NFR. `G-mach` проверяет структуру, `G-semantic` — смысл с rationale, `G-human` — спорный выбор и приёмку. | [Форензика](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-requirements-run-forensics.md) и оба RFC; отдельный runtime contract ещё не собран. |
| #606: TM Forum + SID | Точные ID TM Forum остаются `unresolved` без snapshot; SID — отдельно типизированный контекст и кандидат для эскалации, а не замена capability/eTOM ID. Владелец счёл текущую выборку достаточной; 23 недоступных чата остаются границей evidence. | [RFC абстракции §10](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md) и [форензика](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-requirements-run-forensics.md). Основание о роли SID — [TM Forum Information Framework](https://www.tmforum.org/open-digital-architecture/information-framework-sid/). |
| #608: пять решений конвейера | Working — единственный редактируемый baseline; Release — детерминированная проекция; 2.3 «Границы изменения»; NFR→FR и compatibility closure; pre/post gates; раздел 4 «Функциональный дизайн решения». | [RFC Working → Release](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-working-release-pipeline.md), статус `accepted`. |

## Сквозная проверка зависимостей

| Контур | Проверенный факт | Исполнение и зависимость |
| --- | --- | --- |
| Scope и продукт | [README проекта](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/README.md) определяет `mango-only` как весь портфель; [MANGO](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/product-taxonomy/mango-products.yaml) и [telecom](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/product-taxonomy/telecom-products.yaml) содержат 42 соответствия. Последний каталог хранит prose, не точные TM Forum IDs. | Сохранить provenance при компиляции; добавить типизированные ID только из разрешённого snapshot. |
| Process → route | [Таксономия процессов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/process-taxonomy/20-taxonomy.md) выделяет `P-08` для оценки чужого ТЗ. [Route](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/dist/execution-package-gigacode-cli/routes/rg-bcreq-v1.yaml) имеет `n0` и MANGO binding, но только вертикальный BCREQ-срез. | В Source определить классификатор намерения и переходы; нельзя описывать P-08 как уже скомпилированный путь. |
| Evidence → FR/UC/NFR | [Форензика](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-requirements-run-forensics.md) задаёт инварианты; [Golden forms](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-bcreq-golden-forms-and-feasibility.md) задают примеры. Текущая [C-OUT schema](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/dist/execution-package-gigacode-cli/contracts/c-out-bcreq.schema.json) ещё не задаёт новый coverage contract. | Сначала Working schema и negative fixtures, затем `G-mach`, semantic regressions и изменение skills. |
| Working → Release | Два RFC теперь делят ответственность: внутренние слоты и типы — RFC абстракции; обязательная клиентская проекция, 2.3, 4 и условный 7 — RFC конвейера. | Source compiler, baseline digest, reverse trace, `G-release` и privacy checks; Distribution выпускать из Source по [ADR-017](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/decisions/2026-09-adr-017-ba-ai-process-source-distribution.md). |
| CLI deployment | Третий [RFC о развёртывании](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-mango-ba-ai-runtime-cli-deployment.md) остаётся `proposed`: он определяет среду запуска и публикацию, а не семантику BCREQ. | Проверять совместимость Source → Distribution с этим предложением при отдельной runtime-задаче; его принятие не требуется для начала изменений Source. |
| Проверка | [Пакет](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/dist/execution-package-gigacode-cli/README.md) уже имеет структурный валидатор и эмуляцию. Они не доказывают релевантность, выбор первичной оси, NFR→FR или Release-компиляцию. | Добавить позитивные/негативные fixtures для каждого нового gate, включая non-CC, external TZ, missing mapping, orphan NFR, unknown compatibility и потерянный edge case. |

Проверка ссылок обнаружила 12 относительных Markdown-ссылок в модулях
мета-модели и один URL на отсутствующий `30-production-law.md`. Они исправлены
в этом PR. Остальные относительные пути в frontmatter, коде и YAML являются
внутренними путями/значениями, а не Markdown-ссылками.

## Неисполненное и путь к реализации

1. **Контракт намерения и routing.** Source должен задать входной тип работы,
   правило первичной оси, per-requirement mapping, объяснение агента и исход
   `G-human`; затем обновить `n0`, dispatcher, schemas, validator и route tests.
   Для внешнего ТЗ использовать `P-08` с industry-first и полным отчётом о
   MANGO coverage. Порог 80% добавлять только после versioned шаблонного
   каталога и измерительной спецификации.
2. **Семантика и конвейер.** Source должен объединить pre-decomposition,
   FR/UC/NFR, NFR→FR, compatibility closure и Working baseline. Отдельно
   определить профили публикации, compiler, reverse trace и `G-release`.
   Компиляция Distribution следует только после контрактных тестов Source.
3. **Industry evidence.** Хранить TM Forum и SID по разным типам элементов.
   При недоступном snapshot принимать `unresolved` с вопросом и owner;
   доступный публичный SID Overview можно показывать человеку как контекст,
   не как точный capability ID. Неподтверждённые названия продуктов,
   поставщиков и функций не добавлять в profile rules.
4. **Golden и rollout.** Три согласованные формы превратить в replayable
   positive/negative cases, провести human review, испытать API/ЛК/КЦ и
   multi-product, доказать повторяемую компиляцию. Исторический корпус
   форензики сохраняет 23 неполных диалога как известную границу; новые чаты,
   если появятся, запускают отдельную повторную оценку.

Эта последовательность замыкает зависимость Source → Distribution → runtime.
Блокеров **для начала** изменений модели контрактов и Source пакета нет.
Блокерами **для заявления о полной реализации** остаются отсутствующий
каталог шаблонных требований, отсутствие authoritative snapshot для точных ID
и невыпущенные схемы/гейты/компилятор. Для первых двух допустима честная
`unresolved` ветка; обход не превращается в ложное соответствие.

Issue #609 не присутствовала в активном
[backlog](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ops/backlog.md)
до начала работы, поэтому задача не добавлена туда задним числом. Пункты
реализации являются входом следующей issue, а не заявлением об исполнении
существующих backlog-задач.
