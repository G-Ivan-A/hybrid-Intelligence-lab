---
status: draft
version: 0.1
updated: 2026-06-28
temperature: 0.1
type: internal-analysis
context: [hub, issue-282, issue-284, frontmatter, lifecycle, validator, migration]
method: comparative-analysis
scope: repo-wide
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/284"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/282"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/284"
related_artifacts:
  - "standards/frontmatter-standard.md"
  - "standards/frontmatter-docs-standard.md"
  - "docs/adr/2026-06-adr-002-artifact-document-methodology.md"
  - "docs/rfc/2026-06-27-rfc-rfc-standard.md"
  - "docs/rfc/2026-06-27-rfc-adr-standard.md"
  - "tools/validate-frontmatter.sh"
  - "research/hub/exp/ripple-effects-282/2026-06-28-frontmatter-scan.md"
---

# Исследование: Ripple Effects issue 282

## 1. Введение

**Причина.** Issue
[#282](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/282) предлагает
спринт по стандартизации RFC/ADR, переходу на правило "необходимый и
достаточный" frontmatter, введению двух словарей статусов, обновлению
валидатора и удалению `ai-generated`. Issue
[#284](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/284) просит не
внедрять эти решения сразу, а исследовать ripple effects: какие системные
вопросы появятся и какие варианты решения есть.

**Цель.** Показать пространство решений для выполнения issue #282: переходы
между словарями статусов, маршрутизацию валидатора, реестр допустимых
frontmatter-полей, стратегию миграции, CI-режимы и граничные кейсы. Документ не
выбирает лучший вариант и не повышает lifecycle stage артефактов. Выбор
варианта остаётся за фаундером.

**Связанные артефакты.**

- [Frontmatter Standard](../../standards/frontmatter-standard.md) - текущий
  базовый контракт четырёх полей.
- [Frontmatter Docs Standard](../../standards/frontmatter-docs-standard.md) -
  текущая специализация по классам документов.
- [ADR-002](../../docs/adr/2026-06-adr-002-artifact-document-methodology.md) -
  текущая методология цепочки research -> RFC -> ADR -> standard/template/tool.
- [RFC structure draft](../../docs/rfc/2026-06-27-rfc-rfc-standard.md) и
  [ADR structure draft](../../docs/rfc/2026-06-27-rfc-adr-standard.md) -
  свежие RFC issue #280, ещё не обязательные стандарты.
- [Frontmatter scan](exp/ripple-effects-282/2026-06-28-frontmatter-scan.md) -
  воспроизводимый снимок текущего состояния frontmatter.

**Метод.** Сопоставление issue #282/#284, текущих стандартов, ADR-002, RFC/ADR
drafts из PR #281, текущего валидатора и синтаксического baseline scan-а 170
tracked Markdown-файлов. Scan исключает сам research artifact issue #284 и его
experiment directory, чтобы результаты описывали состояние репозитория, которое
должен будет мигрировать issue #282. Анализ ограничен текущим репозиторием;
cross-repo миграция Mango отмечена как отдельный риск, потому что локальная
копия спока не является частью этого рабочего дерева.

## 2. Результаты исследования

### 2.1. Главный вывод

Issue #282 затрагивает не один валидатор, а четыре связанных контура:

1. **Семантика lifecycle.** Текущий одинарный словарь (`draft`, `reviewed`,
   `canonical`) используется и для knowledge maturity, и для governance
   decisions. Новый двойной словарь убирает семантическое смешение, но требует
   правил перехода.
2. **Машиночитаемость frontmatter.** Переход от "минимального" к
   "необходимому и достаточному" оправдывает `owner`, `decision-type` и
   `rfc-scope`, но только если выбран реестр полей и понятно, кто его
   поддерживает.
3. **Валидатор и CI.** Текущий `tools/validate-frontmatter.sh` выдаёт warning-и
   и всегда завершает работу с `0`; если новые правила должны блокировать PR,
   нужен отдельный выбор режима fail-open/fail-closed.
4. **Миграция существующих файлов.** Scan текущего репозитория показал 170
   tracked Markdown-файлов, 119 файлов с `ai-generated` и 126 файлов с полями
   вне четырёх базовых. Жёсткий запрет без миграционного режима приведёт к
   массовому изменению, а не к локальной правке.

Иными словами, issue #282 может быть выполнено как один большой breaking PR,
как phased migration или как сначала research/RFC -> затем validator/templates ->
затем bulk cleanup. Все три класса сценариев технически возможны; отличаются
риском, размером PR и скоростью получения enforceable правил.

### 2.2. Сводка ripple effects

| Изменение issue #282 | Системный вопрос | Почему это важно |
| --- | --- | --- |
| Два словаря статусов | Как маппить `canonical` governance-документы в `accepted` и что делать с `reviewed`? | Без transition matrix массовая миграция может поменять смысл статуса. |
| Смешение path/type | Валидатор должен выбирать словарь по пути, `type`, manifest или их комбинации? | Конфликт пути и `type` может сделать файл валидным для одного инструмента и невалидным для другого. |
| `owner` в frontmatter | Обязательно для всех governance-документов или только RFC/ADR? | `standards/` и `governance/` содержат разные классы: правила, индексы, RFC, контракты. |
| `decision-type` / `rfc-scope` | Это обязательный YAML или body-level metadata до появления индекса? | Иначе новый frontmatter начнёт дублировать body tables. |
| "Необходимый и достаточный" | Где живёт approved list полей? | Без машинного реестра валидатор будет кодировать governance-логику в shell-case. |
| Запрет `ai-generated` | Удалять 119 полей сразу или по мере редактирования? | Big-bang cleanup reviewable только при автоматической проверке и понятном rollback. |
| `deprecated` в governance | Это frontmatter status уже сейчас или только после validator update? | Иначе статус появится в документах раньше, чем CI его понимает. |
| Open Questions cleanup | Валидируется машинно или остаётся review checklist? | Автоматически понять "blocking/non-blocking" вопрос сложно без ложных срабатываний. |
| CI | Warning или error? Все файлы или changed files? | Разный blast radius: локальный sprint vs исторический cleanup всего repo. |

### 2.3. Evidence snapshot

Скан текущего checkout-а зафиксирован в
[exp-ripple-effects-282](exp/ripple-effects-282/README.md):

| Метрика | Значение |
| --- | ---: |
| Tracked Markdown files | 170 |
| Files with frontmatter | 170 |
| Files with `ai-generated` | 119 |
| Files with fields outside four base fields | 126 |
| `draft` status | 94 |
| `canonical` status | 69 |
| `reviewed` status | 7 |
| Knowledge path class | 58 |
| Governance path class | 74 |
| Other path class | 38 |

Интерпретация:

- Репозиторий уже дисциплинирован по наличию frontmatter: пропусков нет.
- `ai-generated` - массовое legacy-поле, а не локальное исключение.
- Дополнительные поля (`type`, `context`, `method`, `scope`, `source`,
  `related_issues`, `related_artifacts`) уже широко применяются в research,
  templates и issue forms. Поэтому запрет "лишних полей" требует profile-aware
  registry, а не одного глобального списка.
- Governance-файлы сейчас используют `canonical`; после введения governance
  vocabulary это основной кандидат на `accepted`, но такой маппинг должен быть
  human-confirmed для RFC, ADR, standards и contracts отдельно.

### 2.4. Решения, которые нужно оставить фаундеру

| # | Decision point | Варианты |
| --- | --- | --- |
| D1 | Какой источник классификации артефакта главный? | path-first / type-first / hybrid path+type / manifest registry |
| D2 | Как мигрировать governance `canonical`? | direct `canonical -> accepted` / manual triage / keep `canonical` until acceptance |
| D3 | Какой scope `owner`? | all governance / only RFC+ADR / only files consumed by routing/index |
| D4 | Где хранить approved field list? | Markdown standard / YAML manifest / JSON Schema / validator code |
| D5 | Как удалять `ai-generated`? | big-bang / touched-on-change / hybrid soft-ban then cleanup |
| D6 | Какой CI режим? | warnings only / fail changed files / fail whole repository |
| D7 | Что делать с `templates/`? | enforce target-generated docs / treat templates as source artifacts / split source vs rendered validation |

## 3. Детализация

### 3.1. Ripple 1: два словаря статусов

Issue #282 предлагает:

| Класс | Vocabulary | Семантика |
| --- | --- | --- |
| Knowledge | `draft -> reviewed -> canonical -> superseded` | Зрелость знания |
| Governance | `draft -> proposed -> accepted -> rejected -> deprecated -> superseded` | Процесс принятия решения |

Проблема не в наличии двух словарей, а в переходе от текущего состояния к двум
словарям. Сейчас `canonical` одновременно означает "принято как база знания" и
"активная governance-норма/decision record".

#### Варианты transition matrix

| Вариант | Суть | Плюсы | Риски |
| --- | --- | --- | --- |
| A. Direct semantic mapping | Knowledge сохраняет `canonical`, governance получает `accepted`; `draft` остаётся `draft`; `reviewed` для governance вручную маппится в `proposed` или `accepted`. | Быстро устраняет смешение словарей. | Ошибка в auto-map может повысить proposal до accepted без human decision. |
| B. Reset on type change | При переводе Research -> RFC -> ADR новый артефакт начинает с `draft`/`proposed`, даже если source был `canonical`. | Чёткая decision gate; нет автоматического наследования статуса. | Больше ручной работы; теряется визуальная связь зрелости source research. |
| C. Bridge period | Валидатор временно принимает старый и новый словари, но предупреждает о mismatch. | Меньше breaking changes; удобно для phased migration. | Два словаря дольше сосуществуют; риск затянуть переход. |
| D. Dual status fields | Ввести `knowledge-status` и `decision-status` рядом с `status`. | Явно разделяет зрелость знания и решение. | Увеличивает frontmatter inflation и противоречит цели единого canon-status. |

#### Граничные переходы

| Переход | Вопрос | Возможные правила |
| --- | --- | --- |
| Research `canonical` -> RFC | Наследовать ли зрелость? | Новый RFC `draft`/`proposed`; source research остаётся `canonical`; связь через `source`/body. |
| RFC `accepted` -> Standard | Какой статус у standard? | Standard может быть `accepted` как governance artifact или `canonical` если standards остаются отдельным vocabulary class. |
| RFC `accepted` -> ADR | Нужен ли ADR? | По RFC #280: ADR нужен только если нужен отдельный concise decision record. |
| ADR `accepted` -> superseded | Кто ставит replacement link? | Только human-approved PR, потому что supersession меняет guidance. |
| Knowledge `reviewed` -> Governance `accepted` | Можно ли без RFC? | Только если issue/PR уже содержит явное human decision; иначе `proposed`. |

Ключевой нерешённый вопрос: входят ли `standards/` в governance vocabulary
полностью или им нужен подтип. Для RFC/ADR `accepted` естественен. Для standards
слово `canonical` исторически читалось как "активная норма"; замена на
`accepted` возможна, но меняет язык репозитория.

### 3.2. Ripple 2: маршрутизация валидатора

Issue #282 формулирует path-based routing:

- `research/`, `docs/analysis/` -> Knowledge;
- `docs/rfc/`, `docs/adr/`, `standards/`, `ai-rules/` -> Governance.

Текущий Хаб имеет важную поправку: active RFC находятся в `docs/rfc/`, а
не в `docs/rfc/`. Кроме того, `templates/`, `practices/`, `guides/` и корневые
документы не попадают в простую бинарную схему.

#### Варианты routing

| Вариант | Как работает | Когда целесообразен | Риски |
| --- | --- | --- | --- |
| A. Path-first | Словарь и approved fields выбираются только по пути. | Простая структура, легко реализовать в shell. | Конфликты при legacy-путях (`docs/rfc/`), templates и переездах. |
| B. Type-first | Словарь выбирается по `type` в frontmatter. | Гибко при переносах и mixed catalogs. | Требует `type` почти везде, увеличивает metadata и ломает "минимальный" подход. |
| C. Hybrid path + optional type | Path даёт default; `type` уточняет только там, где path неоднозначен. | Баланс между простотой и mixed artifacts. | Нужно правило конфликта path vs type. |
| D. Manifest registry | Отдельный YAML/JSON manifest описывает path globs, artifact classes, allowed fields and status vocabularies. | Хорошо для CI/CD, schema generation и downstream sync. | Новый artifact и новый owner; риск over-engineering для малого repo. |

#### Правила конфликта path vs type

| Conflict case | Варианты реакции |
| --- | --- |
| `research/...` + `type: rfc` | fail / warn and classify by path / classify by type only with explicit override |
| `docs/rfc/...` + `status: canonical` | fail after migration / warn during bridge / auto-suggest `accepted` |
| `templates/...` with placeholder values | validate source-template profile / skip rendered-only fields / require template-specific schema |
| Root docs (`README`, `CONCEPT`, `AI_GOVERNANCE`) | governance default / root-doc profile / explicit allowlist |

Если выбран path-first или hybrid, current Hub должен явно добавить
`docs/rfc/` в governance paths, иначе собственные RFC Хаба выпадут из
новой схемы.

### 3.3. Ripple 3: approved list полей

Текущее правило в `frontmatter-docs-standard.md` уже формулирует
"necessary and sufficient": extra fields allowed only when a tool, template,
provenance rule or document class consumes them. Issue #282 усиливает это до
валидируемого запрета неутверждённых полей.

#### Варианты registry

| Вариант | Содержание | Плюсы | Риски |
| --- | --- | --- | --- |
| A. Markdown table in standard | Расширить `frontmatter-docs-standard.md`: class -> required/optional fields. | Самый readable, без нового формата. | Валидатору придётся парсить Markdown или дублировать правила. |
| B. YAML manifest | `standards/frontmatter-registry.yml`: classes, globs, required fields, optional fields, vocabularies. | Удобно для shell/Python validator и review. | Нужно добавить новый active artifact и держать human-readable explanation рядом. |
| C. JSON Schema per class | `schemas/frontmatter/*.schema.json`. | Стандартная machine validation, easy strict mode. | Добавляет каталог/schema tooling; Markdown templates with placeholders сложнее. |
| D. Validator-owned rules | Все правила в `tools/validate-frontmatter.sh`. | Быстро для маленького набора. | Governance logic становится невидимой в standard; сложнее review. |
| E. Two-layer model | Markdown standard = human contract; YAML/JSON generated or mirrored for validator. | Разделяет объяснение и исполнение. | Требует drift check между human и machine слоями. |

#### Candidate field classes

| Artifact class | Fields that may be necessary | Open question |
| --- | --- | --- |
| All active Markdown | `status`, `version`, `updated`, `temperature` | Остаётся ли `temperature` обязательным после issue #282? |
| Research | `type`, `context`, `method`, `scope`, `source`, `related_issues`, `related_artifacts` | Research profile уже использует эти поля; блокировать их нельзя без замены. |
| RFC | `owner`, `rfc-scope`, maybe `source-issue` | Переносить ли `impacted-artifacts` в YAML или оставить body table? |
| ADR | `owner`, `decision-type`, maybe `supersedes` | Нужен ли ADR index, который реально потребляет эти поля? |
| Standard/contract | `owner` or `governance-owner`, maybe `executable` | Все standards имеют одного owner или достаточно repo owner/human reviewer? |
| Template | placeholders, `entrypoint`, `executable` | Проверять source templates или только rendered artifacts? |

Главный критерий "необходимости" должен быть проверяемым: поле считается
допустимым, если указан consumer (validator, index, template renderer,
governance process, provenance rule). Без consumer-а поле переносится в body.

### 3.4. Ripple 4: `owner`, `decision-type`, `rfc-scope`

Issue #282 хочет вынести `owner` в frontmatter для governance-critical routing.
Это меняет текущее ограничение `frontmatter-standard.md`, где owners and process
mapping recommended to live outside metadata unless consumed.

#### Варианты owner-scope

| Вариант | Область | Плюсы | Риски |
| --- | --- | --- | --- |
| A. All governance artifacts | `governance/`, `docs/adr/`, `docs/rfc/`, `standards/`, `ai-rules/` | Единое правило, автоматический dashboard. | Массовый update всех governance docs; owner для README/index may be artificial. |
| B. RFC/ADR only | Proposal/decision records require `owner`; standards/contracts пока body/repo owner. | Минимальный blast radius. | Standards still cannot be owner-routed. |
| C. Consumer-driven | `owner` required only for classes consumed by routing/index. | Соответствует necessary/sufficient rule. | До создания consumer-а owner не enforceable. |
| D. Body-first bridge | В RFC/ADR body owner обязателен, YAML owner optional until validator/index exists. | Совместимо с PR #281 drafts. | Не закрывает issue #282 fully if frontmatter owner is explicit requirement. |

`decision-type` and `rfc-scope` имеют похожую дилемму. Они полезны для поиска,
но становятся "necessary" только после появления routing/index/dashboard or
validator checks. Если их добавить раньше, они становятся governance bet:
future tooling обязано их потреблять, иначе поле снова будет избыточным.

### 3.5. Ripple 5: удаление `ai-generated`

Issue #282 предлагает убрать `ai-generated` из templates, standards, validator
and existing files. Evidence scan показывает 119 tracked Markdown-файлов с этим
полем.

#### Варианты миграции

| Вариант | Суть | Плюсы | Риски |
| --- | --- | --- | --- |
| A. Big-bang cleanup | Одним PR удалить `ai-generated` из всех tracked Markdown, templates and docs. | Быстро закрывает drift; validator can fail on any reintroduction. | Большой шумный diff; сложнее review; возможны merge conflicts. |
| B. Touched-on-change | Запретить новые occurrences, удалять existing only when file edited. | Минимальный diff; меньше конфликтов. | Legacy field остаётся долго; validator должен отличать changed vs existing. |
| C. Hybrid | Удалить из templates, standards, validator examples now; active docs batch later; historical outputs optional. | Балансирует enforceability and review size. | Нужно два-три PR и временный warning mode. |
| D. Provenance replacement first | Сначала создать provenance rule (issue/PR/changelog/audit), затем удалить field. | Не теряется rationale об AI contribution. | Дольше; issue #282 может ждать отдельного governance decision. |

Граничные случаи:

- Generated experiment outputs may keep historical frontmatter? Если цель
  запрета - не хранить AI authorship at artifact level, outputs тоже попадают в
  cleanup. Если цель - не менять frozen evidence, outputs may be excluded.
- Templates with `ai-generated` create new violations downstream. Их стоит
  рассматривать отдельно от historical docs.
- Current validator lists `ai-generated` as optional and validates boolean. New
  validator must choose between "warn if present" and "error if present".

### 3.6. Ripple 6: validator and CI design

Current validator behavior:

- required fields: `status`, `version`, `updated`, `temperature`;
- optional fields: `ai-generated`, `executable`, `entrypoint`;
- accepted statuses: `draft`, `reviewed`, `published`, `superseded`,
  `canonical`, `experimental`;
- warnings do not fail CI because script exits `0`.

Issue #282 implies at least five validator changes:

1. allow `deprecated`;
2. route status vocabulary by class;
3. require `owner` for governance artifacts;
4. block unapproved fields by class;
5. block `ai-generated`.

#### CI modes

| Mode | Description | Useful when | Trade-off |
| --- | --- | --- | --- |
| Warning only | Report violations but exit 0. | Discovery phase, before migration. | CI does not enforce new standard. |
| Changed-files strict | Fail only changed files; legacy allowed. | Gradual migration. | Requires Git diff base in CI and local mode. |
| Whole-repo strict | Fail if any tracked file violates. | After cleanup complete. | Requires big-bang or pre-cleaned repo. |
| Two-step job | `--warn-existing` and `--strict-new` modes. | Bridge period. | More validator complexity, but explicit migration state. |

#### Implementation variants

| Variant | Tooling | Notes |
| --- | --- | --- |
| Keep Bash | Extend `validate-frontmatter.sh` with path globs and associative arrays. | Works for simple path-first rules; harder for schema and changed-files. |
| Python validator | Replace or wrap Bash with Python frontmatter parser. | Easier to parse YAML-like fields and JSON/YAML registry. |
| Shell + manifest | Bash reads simple manifest or generated allowlist. | Possible, but quoting/list parsing gets fragile. |
| JSON Schema | Use Python package or custom lightweight checks. | Strong for strict validation, but adds dependency and template exceptions. |

### 3.7. Ripple 7: RFC/ADR standard drafts

PR #281 added draft RFCs for RFC and ADR structure. Issue #282 asks to adjust
them:

- frontmatter becomes canon for status;
- body status table becomes narrative summary;
- `owner`, `decision-type`, `rfc-scope` move to frontmatter;
- Open Questions must be cleared or non-blocking before `accepted`;
- process elements should move out of structure standards;
- examples for archetypes B and C should be added;
- file naming should be clarified.

Ripple effects:

| Area | Question |
| --- | --- |
| Body metadata tables | Which rows remain once YAML becomes canonical? |
| `Decision status` vs `status` | Do we remove body status or label it non-normative? |
| Open Questions | Does validator inspect section content or reviewer checklist only? |
| Examples B/C | Are examples in RFC drafts, templates, or future standards? |
| Numeric RFC IDs | Issue #282 says evaluate after RFC-020; no tooling now. What creates the threshold counter? |
| RFC path | Current Hub uses `docs/rfc/`; target HTOM/spoke may use `docs/rfc/`. Both must be recognized during transition. |

### 3.8. Ripple 8: templates and downstream sync

Templates create future files. A template cleanup has higher leverage than
historical cleanup.

| Template concern | Option space |
| --- | --- |
| `ai-generated` in templates | Remove immediately / keep in legacy HTOM template until downstream migration / fail new rendered docs only |
| Placeholder dates | Validator already accepts `{{date}}` for source templates; new schema must preserve this. |
| Owner placeholders | Add `owner: {{owner}}` only if placeholder is approved; otherwise use body TODO. |
| Downstream sync | Hub can change template source, but spoke repositories need separate sync and local review. |

If `owner` becomes mandatory in templates, `tools/validate-repository-structure.sh`
currently approves only `{{date}}`, `{{project_name}}`, `{{hub_url}}` and
`{{REPO_NAME}}`. A new `{{owner}}` placeholder would require placeholder
approval, or templates must use concrete default text.

### 3.9. Migration scenarios

#### Scenario A: one breaking sprint PR

Scope:

- update standards and RFC drafts;
- implement strict validator;
- remove all `ai-generated`;
- migrate all statuses and add owner fields;
- update templates and CI.

Pros:

- one final state;
- no bridge vocabulary;
- CI can be whole-repo strict immediately.

Cons:

- large review surface;
- status migration can accidentally encode decisions;
- high merge-conflict risk with PR #283 or other governance work.

#### Scenario B: phased migration

Phase examples:

1. Update standards with final vocabulary and registry decision.
2. Add validator in warning/changed-files mode.
3. Clean templates and new docs.
4. Bulk-migrate historical `ai-generated` and status fields.
5. Switch CI to whole-repo strict.

Pros:

- each PR is reviewable;
- humans can approve ambiguous mappings;
- CI can become stricter only after evidence.

Cons:

- bridge period creates temporary complexity;
- requires tracking open migration state.

#### Scenario C: research/RFC first, implementation later

Scope:

- issue #282 becomes a governance RFC/update first;
- no validator or mass cleanup until founder selects options.

Pros:

- best match for unresolved decision points;
- avoids accidental decisions in code.

Cons:

- slower to get enforceable improvements;
- existing inconsistency remains visible.

### 3.10. Acceptance checks for issue 282 after decision

Whatever option is selected, issue #282 implementation should be able to answer:

| Check | Evidence |
| --- | --- |
| Status vocabulary chosen for every path/class | Standard or registry table |
| Transition matrix exists | Table for old -> new statuses and type changes |
| Path/type conflict rule exists | Validator docs and tests |
| Approved fields are traceable to consumers | Standard/manifest entries |
| `ai-generated` policy has migration mode | Validator behavior and cleanup plan |
| CI mode is explicit | Workflow and validator exit-code behavior |
| Templates do not generate invalid docs | Template validation and placeholder allowlist |
| Existing RFC/ADR drafts match chosen model | Updated PR diff |

## 4. Источники

- Issue #284:
  [research: Ripple Effects 282](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/284).
- Issue #282:
  [Спринт: Стандартизация RFC/ADR, Frontmatter и Валидация](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/282).
- [Frontmatter Standard](../../standards/frontmatter-standard.md).
- [Frontmatter Docs Standard](../../standards/frontmatter-docs-standard.md).
- [ADR-002: Методология создания и управления артефактами](../../docs/adr/2026-06-adr-002-artifact-document-methodology.md).
- [RFC: Стандарт структуры RFC](../../docs/rfc/2026-06-27-rfc-rfc-standard.md).
- [RFC: Стандарт структуры ADR](../../docs/rfc/2026-06-27-rfc-adr-standard.md).
- [Frontmatter scan for issue 284](exp/ripple-effects-282/2026-06-28-frontmatter-scan.md).
