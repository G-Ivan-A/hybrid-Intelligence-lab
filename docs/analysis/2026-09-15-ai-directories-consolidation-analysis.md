---
status: draft
version: 0.1
updated: 2026-09-15
temperature: 0.1
analysis-subtype: options
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/579"
scope: repo
based_on: "docs/adr/2026-07-adr-007-hub-root-structure.md, templates/htom/tools/validate-repository-structure.sh, tools/validate-repository-structure.sh, AGENTS.md, ops/repo-model.md"
related_artifacts:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-07-adr-007-hub-root-structure.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-012-agents-md-root-contract.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-016-skill-form-and-contract-format.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/AGENTS.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ops/repo-model.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/ai-engineering/2026-09-14-ai-pdlc-industry-alignment.md"
---

# Консолидация `ai-rules/` и `ai-governance/` в единый `ai/`: options analysis

## Summary / BLUF

**Рекомендуется подход А — сохранить `ai-governance/` и `ai-rules/` как два
плоских корневых каталога; консолидация в `ai/` отклоняется.** Ключевой критерий
задачи — простота наследования структуры в `templates/htom/` — измерен прямо по
коду генома и оказался **не зависящим** от раскладки корня Хаба: HTOM-команда не
наследует каталоги `ai-*` вообще. Геном физически поставляет три плоских корневых
файла (`AI_GOVERNANCE.md`, `AI_QUICK_RULES.md`, `AI_SESSION_HANDOVER_PROMPT.md`),
её валидатор уже принимает **три альтернативные раскладки** для каждого
управляющего контракта, а связь с Хабом реализована абсолютными URL, а не
зеркалированием дерева. Следовательно, консолидация не упрощает наследование, а
добавляет к нему четвёртый вариант раскладки. Совокупная выгода — минус **одна**
запись в корне из 26 (26 → 25, из них каталогов 15 → 14), то есть ~4 % корня.
Совокупная цена — перепись **658** вхождений пути в активных артефактах, включая
**229** вхождений в 20 иммутабельных файлах `docs/adr/` и `docs/rfc/`, правка
Хаб-валидатора на 3 107 строк, правка контракта `<artifact_homes>` в `AGENTS.md`,
который по ADR-012 доставляется в спицы **без изменений**, и синхронная миграция
всех спиц экосистемы. Дополнительно подход Б наносит **семантический регресс**:
он поднимает `skills/` и `commands/` из статуса подкласса агентских контрактов
(`ai-rules/skills/`, `ai-rules/commands/` в `<artifact_homes>`) в статус
братьев `rules/`, размывая границу, которую ADR-007 вводил намеренно.

## Context / Scope

| Поле | Значение |
| --- | --- |
| Дата | 2026-09-15 |
| Источник | [issue #579](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/579) (Creative) |
| Охват (`scope`) | Корень репозитория Хаба, геном `templates/htom/`, шаблон `templates/spoke/`, валидаторы `tools/` |
| Снимок | ветка `issue-579-f2f97d696034`, база `a124199` |
| Что интерпретируется | Целесообразность консолидации `ai-governance/` + `ai-rules/` в единый `ai/` с подкаталогами |

Анализ независимый: он не наследует ответ из постановки и, по прямому указанию
issue, имел право как принять, так и отклонить гипотезу консолидации. Все
количественные утверждения ниже получены измерением репозитория на указанном
снимке, а не оценкой.

### Перечитанные исторические основания

| Артефакт | Что зафиксировал | Релевантность |
| --- | --- | --- |
| [ADR-007](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-07-adr-007-hub-root-structure.md) (`accepted`, v0.4) | Ввёл `ai-governance/` для политик (государство, ИБ, compliance, эскалация) и `ai-rules/` для правил поведения агента, разделив прежний `governance/` на четыре дома. Decision driver: «`ai-governance/` и `ai-rules/` нуждаются в стабильной семантической границе до переноса файлов, иначе policy/compliance-материал и правила поведения агента снова схлопнутся в один bucket». | Прямое основание текущей структуры; граница введена как защита от регрессии, а не как побочный эффект. |
| ADR-007, consequences B-055 | «Поглощается ADR-007/B-047 для границы `ai-governance/` vs `ai-rules/`. Отдельный post-migration ADR не нужен, если этот ADR позже не будет superseded». | Граница уже была отдельно верифицирована после миграции и признана закрытой. |
| [ADR-012](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-012-agents-md-root-contract.md) + [`AGENTS.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/AGENTS.md) v2.0 | `<artifact_homes>` называет `ai-rules/<name>.md`, `ai-rules/commands/<slug>.md`, `ai-rules/skills/<slug>/SKILL.md`; `<forbidden>` содержит «Do not create `docs/contracts/`; agent contracts live in `ai-rules/`». Секции `<hard_rules>`/`<forbidden>` объявлены **general** и «delivered unchanged into spoke templates». | `ai-rules/` — не деталь раскладки Хаба, а имя в экосистемном контракте, доставляемом в спицы дословно. |
| [ADR-016](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-016-skill-form-and-contract-format.md) | Нормирует форму навыка и нижнюю границу («короткое правило или команда» → `AGENTS.md`). | Навык и команда — формы **агентского контракта**, то есть подкласс правил, а не сущность одного уровня с ними. |
| [`ops/repo-model.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ops/repo-model.md) стр. 24-25 | Закрепляет назначение обоих каталогов и правило пополнения каждого. | Действующая модель репозитория; меняется только вместе с ADR. |

## Findings / Options

### F1. Наследование в HTOM от раскладки корня Хаба не зависит (ключевой критерий)

Гипотеза постановки предполагает, что спица зеркалит дерево Хаба и потому
страдает от двух `ai-*` каталогов. Измерение показывает обратное.

1. Геном не содержит ни `ai-rules/`, ни `ai-governance/`. Полный список файлов
   `templates/htom/` — три корневых контракта (`AI_GOVERNANCE.md`,
   `AI_QUICK_RULES.md`, `AI_SESSION_HANDOVER_PROMPT.md`), `AGENTS.md`,
   `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `init.sh`, `.hub-profile.json`,
   `docs/adr/`, `docs/audit/`, `.github/`, `tools/`. Каталогов `ai-*` нет.
2. `templates/htom/tools/validate-repository-structure.sh` через `resolve_one_of`
   принимает для каждого управляющего контракта **три** равноправных размещения —
   плоский корневой файл, `governance/`, либо пара `ai-governance/` + `ai-rules/` —
   и отдельно запрещает наличие двух копий сразу. Ни один из каталогов `ai-*` не
   входит в `required_directories` генома (там только `docs/adr`, `docs/audit`,
   `.github/ISSUE_TEMPLATE`, `.github/workflows`, `tools`); они присутствуют лишь
   в `canonical_directories`, то есть «разрешены, если команда их завела».
3. `templates/htom/README.md` фиксирует это как принцип: «Каталоги создаются по
   запросу, при появлении операционной боли (Anti-Inflation principle Хаба).
   Пустые "органеллы" HTOM-команда с собой не носит».
4. Связь спицы с правилами Хаба реализована абсолютными URL
   (`{{hub_url}}/blob/main/ai-rules/agent-work-rules.md`), что прямо предписано
   `<forbidden>`: «Do not use relative links to Hub rules from a spoke».

**Вывод по ключевому критерию.** Наследование уже развязано с раскладкой корня
Хаба. Подход Б не упрощает его, потому что упрощать нечего: он добавил бы к трём
принимаемым раскладкам четвёртую (`ai/governance/` + `ai/rules/`), увеличив
поверхность `resolve_one_of` и число сообщений об ошибке. Единственный критерий,
названный в постановке ключевым, работает **против** консолидации.

### F2. Выигрыш в корне измерим и мал

Корень содержит 26 записей, из них 15 каталогов. Консолидация убирает ровно одну
запись (два каталога → один). Это ~4 % записей корня и ~7 % каталогов. При этом
префикс `ai-` уже выполняет функцию группировки: в любом алфавитном листинге
(`ls`, дерево GitHub, файловый навигатор IDE) `ai-governance/` и `ai-rules/`
стоят соседними строками сразу после `.`-записей. Визуальная смежность,
ради которой предлагается вложенность, достигнута без неё.

Есть и встречный эффект читаемости. Имена `ai-governance` и `ai-rules`
самоописательны в любой позиции, включая ссылку из спицы, поисковую выдачу и
строку лога. Имя `ai/` рядом с `docs/`, `ops/`, `research/`, `practices/` не
говорит ничего: в репозитории, где `research/`, `practices/ai-engineering/`,
`practices/ai-governance/` и `projects/ba-gigacode-implementation/` посвящены ИИ
по содержанию, каталог с именем `ai/` читается как «всё про ИИ», а не как «дом
агентских контрактов и политик». Это ухудшает навигацию в `AGENTS.md`, а не
улучшает её.

### F3. Стоимость миграции: 658 вхождений, из них 229 в иммутабельных документах

Измерение на снимке (исключены `CHANGELOG.md`, а также посторонние совпадения
`practices/ai-governance/`, `research/hub/2026-06-12-international-ai-governance-practices.md`
и `docs/analysis/2026-09-03-ai-rules-compliance-failure-root-cause.md`):

| Поверхность | Вхождений | Комментарий |
| --- | --- | --- |
| `docs/` (в т.ч. `adr/`, `rfc/`, `analysis/`, `audit/`) | 369 | 229 из них — в 20 файлах `docs/adr/` + `docs/rfc/` |
| `research/` | 165 | 44 файла |
| `ops/` | 125 | `artifact-map.md`, `repo-model.md`, `backlog.md` |
| `tools/` | 106 | в основном `validate-repository-structure.sh` (3 107 строк) |
| `standards/` | 66 | включая `file-naming.md`, чей текст зафиксирован `require_text` |
| `templates/` | 37 | геном и spoke-шаблон |
| корневые контракты (`AGENTS.md`, `README.md`, `GOVERNANCE.md`) | 16 | `AGENTS.md` — экосистемный контракт |
| **Итого (активные артефакты)** | **658** | плюс 43 вхождения в `CHANGELOG.md` |

Иммутабельность `docs/adr/` и `docs/rfc/` — не абсолютный блокер: в
`tools/validate-historical-immutable.sh` есть механизм `is_declared_path_migration`,
разрешающий правку исторического документа, если обратная подстановка объявленной
в `.hub-profile.json` миграции даёт **побайтно** исходное содержимое. Честный
вывод: подход Б **технически исполним**. Но механизм задуман как аварийный выход
для вынужденных переносов (в профиле уже четыре такие записи — по issue #567 и #573),
и тратить его на косметику корня — плохой обмен: каждая запись `path_migrations`
навсегда остаётся в профиле и участвует в каждой последующей проверке
иммутабельности.

Отдельный риск: 229 вхождений в ADR/RFC — это в значительной мере **цитаты
принятых решений** (ADR-007 буквально нормирует строки `ai-governance/` и
`ai-rules/`, а Хаб-валидатор это проверяет через `require_text` на строках
1481-1482). Массовая подстановка переписала бы формулировку принятого решения
под новую раскладку, то есть ретроспективно исказила бы запись «решение на момент
принятия» — ровно то, что иммутабельность защищает по существу, а не по букве.

### F4. Экосистемная цена: `AGENTS.md` доставляется в спицы без изменений

`AGENTS.md` v2.0 делит себя на **general** секции, которые «hold in every
repository of the ecosystem and are delivered unchanged into spoke templates», и
`<project_specific_rules>` — «the **only** home for rules of this repository».
Имя `ai-rules/` встречается именно в general-части: в `<forbidden>` и в
`<artifact_homes>`. То же имя дословно продублировано в
`templates/htom/AGENTS.md` и `templates/spoke/AGENTS.md`.

Следствие: консолидация — это не рефакторинг Хаба, а **смена версии
экосистемного контракта**. Она требует согласованного обновления `AGENTS.md` в
каждой существующей спице; до завершения синхронизации часть экосистемы работает
по контракту, называющему несуществующий дом артефакта. Постановка сама называет
это ограничением («Учитываем, что изменения придётся синхронизировать со
спицами»), и измеренная выгода из F2 его не окупает.

### F5. Подход Б ломает семантику skills/commands

Постановка предлагает в `ai/` подкаталоги `governance/`, `rules/` и опционально
`skills/`, `commands/`. Но `skills/` и `commands/` **уже имеют канонический дом**:
`<artifact_homes>` называет `ai-rules/commands/<slug>.md` и
`ai-rules/skills/<slug>/SKILL.md`, и та же строка продублирована в
`templates/htom/AGENTS.md` и `templates/spoke/AGENTS.md`.

Текущая модель утверждает содержательное: правило, команда и навык — три **формы
одного класса** «агентский контракт», различающиеся объёмом и способом вызова
(что и нормирует ADR-016, задавая нижнюю границу формы). Раскладка
`ai/rules/` + `ai/skills/` + `ai/commands/` ставит их братьями и тем самым
утверждает, что это три разных класса. Это не переименование, а изменение
онтологии контрактов — и изменение в сторону, противоположную ADR-016.

Симметрично, `ai/governance/` + `ai/rules/` ослабляет границу ADR-007. Сейчас
граница проходит по корню и потому видна каждому агенту в первом же листинге:
политика и исполняемое правило — разные дома верхнего уровня. Утопленная на
уровень вложенности, она становится деталью внутри одного каталога — ровно тот
дрейф «policy/compliance-материал и правила поведения агента снова схлопнутся в
один bucket», от которого ADR-007 защищался явно.

### F6. Индустриальный аргумент нейтрален, а не поддерживает Б

Поверхности, которые действительно обнаруживаются инструментами агентных сред,
адресуются **фиксированными именами** (`AGENTS.md` в корне — это и есть принятый
Хабом контракт по ADR-012). Каталоги `ai-rules/` и `ai-governance/` — внутренние
дома артефактов Хаба: ни один внешний инструмент их не открывает по имени, и
каталог `ai/` он не открывал бы тоже. Никакой совместимости с GigaCode/GitVerse
консолидация не добавляет и не отнимает.

Материал, на который ссылается SSOT постановки
([`practices/ai-engineering/2026-09-14-ai-pdlc-industry-alignment.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/ai-engineering/2026-09-14-ai-pdlc-industry-alignment.md)),
говорит о GigaCode в разрезе токенов, on-premise-контура, регуляторики (ЦБ РФ,
ФЗ-152, ФЗ-243) и таблицы GigaCode Mapping (Skills / Subagents / Rules / AI
Workflows / Agent-Plan Modes). Раскладки корневых каталогов он не нормирует, и
названный им пробел — регуляторное измерение (B-168), а не структура корня. Ссылка
на индустриальный контекст в поддержку Б в источниках не подтверждается.

### Сводная матрица

| Критерий (из постановки) | А: `ai-governance/` + `ai-rules/` | Б: `ai/` с подкаталогами | Победитель |
| --- | --- | --- | --- |
| Простота наследования в `templates/htom/` (**ключевой**) | Геном не наследует `ai-*` вообще; валидатор уже принимает 3 раскладки | Добавляет 4-ю принимаемую раскладку в `resolve_one_of`; наследовать всё равно нечего | **А** (F1) |
| Читаемость и навигация в `AGENTS.md` | Самоописательные имена, работают в абсолютных URL из спиц | `ai/` неоднозначен в репозитории, где ИИ-тематика повсеместна | **А** (F2) |
| Соответствие практикам GigaCode/GitVerse | Нейтрально | Нейтрально | ничья (F6) |
| Сохранение границы политика ↔ правило | Граница на уровне корня, видна в первом листинге | Граница утоплена на уровень вложенности; риск схлопывания, названный в ADR-007 | **А** (F5) |
| Онтология skills/commands | Формы агентского контракта внутри `ai-rules/`, согласовано с ADR-016 | Братья `rules/`, то есть отдельные классы — регресс | **А** (F5) |
| Загромождение корня | 2 записи из 26 | 1 запись из 25 (−4 %) | **Б**, выигрыш мал (F2) |
| Стоимость миграции | 0 | 658 вхождений, 229 в иммутабельных ADR/RFC, расход `path_migrations`, синхронизация всех спиц | **А** (F3, F4) |

Подход Б выигрывает ровно по одному критерию из семи, и именно по тому, где
выигрыш измерен как ~4 % записей корня. По ключевому критерию постановки он
проигрывает.

## Recommendations

1. **Принять подход А: структуру не менять.** `ai-governance/` и `ai-rules/`
   остаются двумя плоскими корневыми каталогами с назначением по ADR-007.
   Названия не меняются — постановка допускает альтернативные имена только «если
   изменение двух ai-каталогов целесообразно», а целесообразность не
   подтвердилась. Рефакторинг не выполняется; `git mv`, перепись ссылок, правка
   валидаторов и актуализация `templates/htom/` не запускаются.
2. **Нового ADR не требуется.** ADR-007 остаётся в силе и не становится
   `superseded`: решение подтверждено, а не изменено. Эта записка — knowledge-вход
   для возможного будущего пересмотра, а не decision record.
3. **Зафиксировать критерий пересмотра.** Вопрос уместно переоткрыть, только если
   появится хотя бы один из триггеров: (а) геном HTOM начнёт физически поставлять
   каталоги `ai-*`, то есть наследование действительно станет структурным;
   (б) число корневых `ai-*` каталогов превысит два, и группировка даст выигрыш
   больше косметического; (в) внешняя среда (GigaCode/GitVerse) введёт
   обнаруживаемый по имени каталог, требующий конкретной раскладки. Ни один из
   трёх на снимке не наблюдается.
4. **Зафиксировать выявленный побочный пробел.** `ai-rules/skills/` и
   `ai-rules/commands/` объявлены в `<artifact_homes>` `AGENTS.md`, но физически
   на снимке отсутствуют. Это корректно по Anti-Inflation (дом объявлен, каталог
   создаётся под первый артефакт) и не является дефектом, но стоит держать в
   виду: первый навык или команда Хаба обязаны появиться именно там, а не в новом
   корневом доме.

## Related Artifacts

- [Issue #579](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/579) — постановка задачи.
- [ADR-007: Целевая структура корня Хаба](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-07-adr-007-hub-root-structure.md) — источник разделения `ai-governance/` / `ai-rules/`.
- [ADR-012: AGENTS.md root contract](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-012-agents-md-root-contract.md) — контракт точки входа, доставляемый в спицы.
- [ADR-016: Форма навыка и формат контракта](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-016-skill-form-and-contract-format.md) — границы формы навыка и команды.
- [`AGENTS.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/AGENTS.md) — `<forbidden>` и `<artifact_homes>` с именем `ai-rules/`.
- [`ops/repo-model.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ops/repo-model.md) — действующая модель корня и Anti-Inflation.
- [`ops/artifact-map.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ops/artifact-map.md) — реестр артефактов.
- [`templates/htom/tools/validate-repository-structure.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/templates/htom/tools/validate-repository-structure.sh) — evidence F1: `resolve_one_of` и `canonical_directories`.
- [`templates/htom/README.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/templates/htom/README.md) — evidence F1: три принимаемые раскладки и Anti-Inflation.
- [`tools/validate-historical-immutable.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/validate-historical-immutable.sh) — evidence F3: механизм `path_migrations`.
- [`practices/ai-engineering/2026-09-14-ai-pdlc-industry-alignment.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/ai-engineering/2026-09-14-ai-pdlc-industry-alignment.md) — индустриальный контекст, evidence F6.
