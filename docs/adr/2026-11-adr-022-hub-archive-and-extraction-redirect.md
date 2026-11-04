---
status: proposed
version: 0.1
updated: 2026-11-04
temperature: 0.1
owner: G-Ivan-A
decision-type: governance
---

# ADR-022: Архив Хаба — защищённый тег, а не каталог; удалённый путь адресуется манифестом

## Decision Metadata

| Field | Value |
| --- | --- |
| ADR id | ADR-022 |
| Decision type | governance |
| Decision status | proposed (машиночитаемый canon — frontmatter `status`) |
| Decision date | 2026-11-04 (предложено; дата принятия — merge PR, переводящего статус в `accepted`) |
| Owner | G-Ivan-A |
| Source | issue [#721](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/721); обоснование — [RFC завершения выноса GRA](../rfc/2026-11-04-rfc-gra-extraction-completion-and-hub-cleanup.md), доказательства — [сверка полноты выноса](../analysis/2026-11-04-gra-extraction-completeness-check.md) (F-5, F-6, F-7) |
| Impacted artifacts | [`standards/artifact-deprecation-standard.md`](../../standards/artifact-deprecation-standard.md) (v0.3), [`.hub-profile.json`](../../.hub-profile.json) (поле `path_migrations`), `tools/validate-repository-structure.sh`, `tools/validate-historical-immutable.sh` (задача Ш4 RFC) |
| Supersedes | none |
| Superseded by | none |
| Дополняет | [ADR-007](2026-07-adr-007-hub-root-structure.md) — корень Хаба не получает каталога `archive/`; [ADR-014](2026-09-adr-014-legacy-evidence-not-baseline.md) — наследие остаётся свидетельством, но не обязано лежать в рабочем дереве; [ADR-010](2026-08-adr-010-agent-autonomy-principles.md), Принцип 2 — удаление по-прежнему требует мандата |

## Context

[Artifact Deprecation Standard](../../standards/artifact-deprecation-standard.md)
v0.2 задаёт состояния выбытия и правила удаления, но не говорит, как
архивировать и как адресовать путь, который вынесен в другой репозиторий.
Issue #721 требует и того и другого для домена `research/reputation-technologies/`.
Стандарт сам требует decision record для смены правил удаления
([Lifecycle](../../standards/artifact-deprecation-standard.md#lifecycle)).

| Пробел | Наблюдение |
| --- | --- |
| G-1. Форма `archived` | Стандарт определяет состояние («исторический снимок; содержание заморожено»), но не форму хранения. Постановка #721 предлагает общий каталог-архив, исключённый из валидаторов |
| G-2. Каталог не сохраняет адрес | GitHub не перенаправляет удалённый путь, даже объявленный в `path_migrations`: `blob/main/pr-ops/README.md` — 404, тот же путь по SHA — 200 (`permalink-probe.log`). Перенос в каталог меняет путь так же, как удаление |
| G-3. Условие 2 Deletion Rules | Удаление запрещено, если на путь ссылается историческая запись, а адрес не заменён compatibility redirect. Redirect — файл по прежнему пути, то есть удаление невозможно в принципе. У всех 19 единиц, предложенных к удалению, есть ссылки из CHANGELOG |
| G-4. Внешний приёмник | `path_migrations` принимает битую ссылку, только если `to + suffix` существует локально. Для выноса в другой репозиторий это всегда ложь |
| G-5. Персональные данные | Архив тиражирует содержимое, а цель обработки персональных данных достигнута |

## Decision

**1. Архив — аннотированный тег, а не каталог.** Состояние `archived` для
вынесенного или выведенного из дерева набора наблюдается как аннотированный тег
`archive/<slug>-<YYYY-MM>` на последнем коммите, где набор лежит целиком.
Ruleset репозитория запрещает обновлять и удалять теги `archive/*`. Каталог
`archive/` в корне Хаба не создаётся.

**2. Удалённый путь адресуется манифестом.** У префикса выносимого набора
остаётся `README.md` — надгробие. Оно содержит сигнал выбытия и манифест: для
каждого прежнего пути один адрес — SHA-ссылку на приёмник, ссылку на тег или
отметку «удалён; последняя версия — `<SHA>`». Запись `path_migrations` с внешним
`to` и полем `manifest` позволяет валидатору принимать исторические ссылки на
перечисленные пути. Манифестное перенаправление — разновидность compatibility
redirect для условия 2 и запрета 1 раздела Deletion Rules.

**3. Порядок неизменен:** сигнал → заморозка → удаление по мандату → тег →
вынос из дерева → реестры. Удалённое по мандату в тег не попадает.

**4. Персональные данные не архивируются.** Их удаляют до тега. Переписывание
истории git — отдельное решение владельца.

Правило целиком — в стандарте v0.3, раздел
[Extraction and Archive by Tag](../../standards/artifact-deprecation-standard.md#extraction-and-archive-by-tag),
и подраздел
[Manifest redirect](../../standards/artifact-deprecation-standard.md#manifest-redirect).

## Decision Drivers

- Ссылки `blob/main` ломаются при любом изменении пути. Устойчив только адрес
  по SHA или по защищённому тегу ([GitHub Docs: permanent links](https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files)).
- Цель issue — дешевле CI и чище контекст агента. Домен занимает 33,5 % байтов
  Хаба и 19 шагов CI (28 % задания `validate`). Каталог-архив сохранил бы байты
  в поиске агента и потребовал бы исключений в каждом валидаторе.
- Записи решений не удаляются, а получают статус `superseded`
  ([Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)).
  Неиспользуемые черновики удаляются
  ([Google docguide](https://google.github.io/styleguide/docguide/best_practices.html#delete-dead-documentation)).
  Тег разделяет эти классы без каталога.
- Historical link policy запрещает переписывать исторические ссылки. Нужен
  механизм, который разрешает их без правки текста.
- Решение повторяемо. Ближайший следующий вынос — `projects/ba-ai-process/`
  (задача Ш3.6 [RFC #715](../rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md)),
  а контракт выноса PR #718 оставляет шаги Хаба после E6 отдельным задачам.

## Alternatives Considered

Источник — раздел [Alternatives](../rfc/2026-11-04-rfc-gra-extraction-completion-and-hub-cleanup.md#alternatives)
RFC. ADR закрывает одну развилку: **каталог `archive/` против тега с манифестом**.
Каталог допустим только как запасной вариант, если владелец отклонит IPA-1, и
только при трёх мерах:

1. Каталог исключён в каждом валидаторе и в `validate.yml`.
2. Отдельная проверка запрещает правки внутри каталога.
3. Ссылки на прежние пути всё равно разрешаются манифестом: каталог их не
   сохраняет.

## Consequences

- Стандарт выбытия переходит на v0.3. Добавлены `Manifest redirect` и раздел
  `Extraction and Archive by Tag`; условие 2 и запрет 1 раздела Deletion Rules
  принимают манифестное перенаправление.
- Граф Lifecycle стандарта получает рёбра `deprecated → deleted` и
  `superseded → deleted`. Условие 1 раздела Deletion Rules v0.2 уже допускало
  удаление из этих состояний, а граф показывал только `archived → deleted`.
  v0.3 устраняет это расхождение. Без него удаление по мандату до тега (шаг 3
  порядка) было бы недопустимым переходом.
- Определение `archived` в Type Model расширено: для набора, выведенного из
  дерева, файл существует на защищённом теге, а не на `main`.
- Валидаторы получают правило внешнего `to` с манифестом (задача Ш4 RFC).
  До неё удаление выносимых путей невозможно: CI упадёт на исторических ссылках.
- Читатель исторической записи на GitHub получает 404 по ссылке `blob/main`
  на удалённый путь. Адрес он находит в манифесте по тому же префиксу.
- Включение ruleset для `archive/*` — действие администратора репозитория.
- Задачи — в RFC и в Спринте 31 [`ops/backlog.md`](../../ops/backlog.md); здесь
  они не повторяются.

## Compliance and Validation

| Проверка | Как |
| --- | --- |
| Тег существует, аннотирован и защищён | `git cat-file -t archive/<slug>-<YYYY-MM>` = `tag`; ruleset `archive/*` в настройках репозитория |
| Манифест полон | Проверка Ш4.2: каждый удалённый путь под префиксом перечислен ровно один раз и имеет адрес |
| Исторические ссылки не сломаны | `tools/validate-repository-structure.sh` принимает ссылку на путь из манифеста и отклоняет ссылку на путь вне него |
| Персональные данные не попали в тег | `git ls-tree -r archive/<slug>-<YYYY-MM>` не содержит файлов с отметкой PII в манифесте |
| Каталога `archive/` нет | `test ! -e archive` |

## Lifecycle

| Переход | Условие |
| --- | --- |
| `proposed → accepted` | Владелец отвечает на IPA-1 и Q-5 RFC и сливает PR, переводящий ADR в `accepted`; стандарт v0.3 переходит в `accepted` тем же решением |
| `accepted → superseded` | GitHub или другой хостинг начинает перенаправлять удалённые пути, либо Хаб уходит с GitHub |
| Пересмотр | Манифест расходится с деревом хотя бы раз, или ruleset оказывается недоступен |

## Related Artifacts

- [RFC завершения выноса GRA](../rfc/2026-11-04-rfc-gra-extraction-completion-and-hub-cleanup.md) — дорожная карта, IPA-1…IPA-5, Q-1…Q-6.
- [Artifact Deprecation Standard](../../standards/artifact-deprecation-standard.md) — нормативный текст.
- [Сверка полноты выноса](../analysis/2026-11-04-gra-extraction-completeness-check.md) и [evidence-контейнер](../../research/hub/exp/gra-extraction-cleanup-721/README.md) — измерения.
- [Контракт выноса проекта](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/718) (PR #718, этапы E1–E6) — сторона спицы; этот ADR — сторона Хаба.
- [GitHub Docs: rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), [sunset tag protections](https://github.blog/changelog/2024-05-29-sunset-notice-tag-protections).
