# Changelog

All notable repository governance changes are documented here.

## Unreleased

### Changed

- Issue #201 (Creative mode): clarified the Hub concept by separating
  **HTOM-команды** (hybrid human + AI work units that inherit the governance
  genome) from **spoke-репозитории** (production code repositories with their
  own lifecycle). The minimal governance genome was renamed
  `templates/spoke/` -> `templates/htom/` (via `git mv`, history preserved),
  and a new `templates/spoke/` (README.md, CONTRIBUTING.md,
  `.github/workflows/ci.yml`) was created as the production-spoke template.
  Migration map (old -> new) for the genome:
  `templates/spoke/AI_GOVERNANCE.md` -> `templates/htom/AI_GOVERNANCE.md`,
  `templates/spoke/AI_QUICK_RULES.md` -> `templates/htom/AI_QUICK_RULES.md`,
  `templates/spoke/AI_HANDOVER_PROMPT.md` -> `templates/htom/AI_HANDOVER_PROMPT.md`,
  `templates/spoke/README.md` -> `templates/htom/README.md`,
  `templates/spoke/CONTRIBUTING.md` -> `templates/htom/CONTRIBUTING.md`,
  `templates/spoke/CHANGELOG.md` -> `templates/htom/CHANGELOG.md`,
  `templates/spoke/init.sh` -> `templates/htom/init.sh`,
  `templates/spoke/.github/ISSUE_TEMPLATE/task.md` -> `templates/htom/.github/ISSUE_TEMPLATE/task.md`,
  `templates/spoke/tools/validate-repository-structure.sh` -> `templates/htom/tools/validate-repository-structure.sh`.
  Added `governance/rfc/htom-vs-spoke-clarification-2026-06.md` with the
  definitions, comparison table and current-project classification
  (Хаб, `repo-development`, `mango_ba_prompts` -> HTOM-команды; `open-ai.ru`
  -> first real spoke). Repointed genome references across `README.md`,
  `AI_GOVERNANCE.md`, `governance/repo-model.md`, `governance/artifact-map.md`
  (1.24 -> 1.25), `standards/glossary.md` (1.2 -> 1.3),
  `projects/README.md` (1.1 -> 1.2) and validators; extended
  `tools/validate-repository-structure.sh` to assert both templates.

### Added

- Issue #203 (Creative mode): added a single Draft documentation package for the
  Hub product layer. New product docs `docs/vision.md` (Product Vision, L1) and
  `docs/product-concept.md` (Product Concept, L2); RFC
  `governance/rfc/hub-vision-concept-proposal-2026-06.md` comparing approaches
  and listing open questions to the founder; a human-facing guide library under
  `guides/` (`README.md`, `quick-start.md`, `init-spoke-repo.md`,
  `sync-from-hub.md`, `interact-with-ai.md`, `deploy-project.md`,
  `rollback-sync.md`, `contribute-template.md`, `troubleshooting.md`,
  `glossary.md`); and an MkDocs Material site (`mkdocs.yml`, `website/`) with a
  GitHub Pages auto-deploy workflow `.github/workflows/deploy-docs.yml` that
  publishes only `guides/` and `research/` (governance/ and standards/ stay
  unpublished). Added responsive table CSS in `website/stylesheets/extra.css`
  and registered the RFC in `governance/rfc/README.md`. Updated root `README.md`
  navigation and the whitelist in `tools/validate-repository-structure.sh`;
  removed the obsolete root `.gitkeep`.
- Issue #199: added split webportal concept standards:
  `standards/webportal-product-concept-standard.md` for L2 Product Concept and
  `standards/webportal-solution-concept-standard.md` for L3 Solution Concept.
  Added matching templates
  `templates/webportal-product-concept-template.md` and
  `templates/webportal-solution-concept-template.md` with approved
  `{{project_name}}`, `{{date}}` and `{{hub_url}}` placeholders.
- Issue #191: added `research/portal/portal-documents-review-2026-06.md`,
  standalone `research/portal/portal-documents-review-2026-06.html`, and a
  desktop verification screenshot to support founder review of the 10 deferred
  portal documents from the repository-quality RFC. The Markdown document
  consolidates clickable links, 2-3 sentence summaries, executor-side disputed
  questions, founder decision placeholders, a Q01-Q12 decision matrix and
  review DoD. The HTML version opens directly in a browser without external
  dependencies and includes full-width responsive tables, sticky navigation,
  color-coded statuses, checkboxes, textareas, local browser persistence and
  JSON export. Registered the artifacts in `governance/artifact-map.md`
  (1.21 -> 1.22),
  `research/README.md` (1.4 -> 1.5), and
  `tools/validate-repository-structure.sh`. The original 10 portal documents
  remain unchanged.
- Issue #186: added `governance/rfc/draft-triage-and-exit-plan.md` with a
  four-group triage of 20 draft documents marked "К доработке" in the
  repository-quality RFC. The new RFC records current state, link/placeholder
  risks, concrete exit plans (`approval_target`, `dependencies`,
  `required_changes`, `estimated_effort`), phased cleanup, placeholder strategy,
  Mango spoke boundaries, education scope questions, and Definition of Done.
  Registered the RFC in `governance/rfc/README.md`,
  `governance/artifact-map.md` (1.20 -> 1.21), and
  `tools/validate-repository-structure.sh`.
- Issue #171 (Creative mode): added
  `governance/rfc/repository-quality-improvement-plan.md` with a full
  repository-quality audit after PR #170. The RFC covers naming, duplicate and
  overlapping documents, metadata duplication, traceability, draft statuses,
  obsolete files, and the recommended removal of `archive/projects/mango/`.
  Registered the RFC in `governance/rfc/README.md`,
  `governance/artifact-map.md` (1.18 -> 1.19), and
  `tools/validate-repository-structure.sh`. The PR removes the generated root
  `.gitkeep` placeholder so structural validation can pass; cleanup actions from
  the RFC remain pending human approval.
- Issue #166 (Creative mode): **универсальный стандарт структуры концепции
  веб-портала**. Добавлен `standards/webportal-concept-standard.md` (v1.0,
  `draft`): обязательное ядро из 6 разделов (Summary, Vision & Goals, Scope,
  Roadmap, Risks, Metrics) плюс 9 опциональных слоёв, каждый с минимальной и
  расширенной версией; профили сложности (сайт-визитка / контентный портал /
  app-портал); явные связи с roadmap, исследованиями и структурой репозитория
  (структура выбирается из политики Хаба, а не из концепции); явно заданные
  границы (не для лендингов, мобильных приложений, бэкенд-сервисов и
  микросервисов). Основа выбрана исследованием
  `research/portal/concept-standards-comparison-2026-06.md` — сравнение 8
  подходов (ISO/IEC/IEEE 42010, TOGAF, BABOK, Continuous Discovery, PRD, RFC,
  Concept Doc, Vision Document) по 7 критериям; вывод — гибрид «PRD-ядро плюс
  Vision-слой плюс TOGAF-модульность» с учётом (и аргументированным частичным
  несогласием по структуре репозитория) мнения команды Q. Добавлен копируемый
  шаблон `templates/webportal-concept-template.md`. Артефакты
  зарегистрированы в `governance/artifact-map.md` (1.17 → 1.18),
  `standards/README.md`, `research/portal/README.md` и структурном валидаторе
  (`is_active_file` + `required_files`); валидатор проходит (exit 0). Решение о
  переводе стандарта в `reviewed`/`canonical` остаётся за фаундером.

### Changed

- Issue #199: updated `standards/README.md`, `research/README.md`,
  `governance/artifact-map.md`, `governance/rfc/README.md`,
  `research/governance/governance-folder-structure-decisions-2026-06.md`,
  `tools/validate-frontmatter.sh` and `tools/validate-repository-structure.sh`
  for the new L2/L3 webportal standard split and the removal of the active
  portal package from the Hub.
- Issue #173: governance-файлы переименованы в kebab-case, правила порядка
  изложения из бывшего draft body-standard объединены с
  `standards/research-profile.md`, архив `archive/projects/mango/` удалён после
  миграции во внешний `mango_ba_prompts`, `standards/file-naming.md` расширен до
  версии 1.2 для `governance/`, карта артефактов обновлена до 1.20, а
  структурный валидатор обновлён под новый целевой набор артефактов.
- Issue #185 (Structured mode): объединены три дублирующих design/standard
  артефакта с canonical-документами. Rationale протокола онбординга перенесён в
  `governance/agent-onboarding.md`, rationale ДНК-шаблона — в
  `templates/spoke/README.md`, body-structure правила research-документов
  оформлены как `## Body Structure: Введение → Результаты → Детализация` в
  `standards/research-profile.md` (v1.1). Удалены superseded RFC drafts; ссылки,
  карта артефактов и структурный валидатор обновлены под новый canonical-набор.
- Issue #177 (Structured mode): `governance/rfc/repository-quality-improvement-plan.md`
  обновлён до v0.2: раздел "Full draft list" заменён 52-строчной таблицей
  с колонками для номера, файла, строки `status: draft`, summary,
  рекомендации и обоснования. Добавлен "Триаж по категориям" для canonical,
  отложенных, доработки, объединения и удаления; структурный валидатор теперь
  ожидает версию RFC 0.2.
- Issue #169: файлы стандартов внутри `standards/` переименованы из
  `CAPS_LOCK`/underscore-стиля в kebab-case, все ссылки на старые имена
  обновлены. `standards/file-naming.md` обновлён до версии 1.1 с явным правилом
  для `standards/`; `tools/validate-repository-structure.sh` теперь проверяет,
  что все файлы в `standards/` используют kebab-case, кроме `README.md`,
  `LICENSE` и `CHANGELOG.md`.
- Issue #165 (Creative mode): каталог `governance/proposals/` переименован в
  `governance/rfc/` (решение Q1): имя `rfc/` соответствует файлам `*-rfc.md` и
  отраслевому термину IETF «RFC», снимая рассинхрон «proposals vs rfc». `git mv`
  четырёх RFC; обновлены все живые ссылки (`governance/agent-onboarding.md`,
  `repo-model.md`, `backlog.md`, `executable-documents-issues.md`,
  `artifact-map.md`, `standards/glossary.md`, `templates/spoke/README.md`,
  research-документы Хаба и портала, кросс-ссылки внутри RFC). Концепт-RFC
  портала перенесён `governance/proposals/` →
  `research/portal/open-ai-portal-concept-rfc.md` (решение Q2: концепция
  проекта — это research проекта и живёт в `research/{project}/`, а не в
  governance Хаба; канонический путь без точки в имени каталога по
  `standards/file-naming.md`). `governance/rfc/` задокументирован как
  опциональный, не наследуемый споками каталог (решение Q3,
  `standards/portal-repository-structure.md`). `AI_GOVERNANCE.md` (1.1 → 1.2):
  зафиксирован слоган Хаба. `governance/artifact-map.md` (1.16 → 1.17):
  обновлены пути RFC и добавлены строки новых артефактов. Структурный валидатор
  обновлён под новые пути и проходит (exit 0). Исторические записи (этот
  CHANGELOG, §7.4 в `contract-executability-rfc.md`, self-report) сохранены как
  журнал.
- Issue #141 (CE-004): `AI_GOVERNANCE.md` converted to the executable-documents
  standard as a reference contract. Added canonical frontmatter with
  `executable: false`, bumped version to `1.1` and date to `2026-06-04`, and
  replaced the pre-flight note with a directive pointer to
  `governance/agent-onboarding.md`. Roles, Operating Modes, escalation and
  Definition of Done remain unchanged. Structural validation now checks the new
  frontmatter/version markers; removed the generated harness `.gitkeep`.
- Issue #140 (CE-003): `templates/spoke/AI_HANDOVER_PROMPT.md` (версия 0.1 →
  0.2) переведён в стандарт исполнимых документов: во frontmatter добавлен
  `executable: true`, сразу после frontmatter добавлен директивный блок
  «🚦 ИСПОЛНИМЫЙ HANDOVER PROMPT — СКОПИРУЙ И ВЫПОЛНИ», готовый prompt с
  `{{REPO_NAME}}` поднят в блок `▶️ EXECUTION`, а пояснения, источник истины в
  Хабе и ссылки перенесены в `ℹ️ EXPLANATION` без изменения смысла prompt.
  Структурный валидатор теперь проверяет CE-003-маркеры и блоки
  EXECUTION/EXPLANATION; удалён сгенерированный корневой `.gitkeep`, который не
  является active-файлом репозитория.

- Issue #138 (CE-001): `governance/agent-onboarding.md` (версия 1.0 → 1.1)
  переведён в стандарт исполнимых документов
  `governance/proposals/contract-executability-rfc.md` (§5.1, §6.1, §7).
  Во frontmatter добавлены маркеры `executable: true` и `entrypoint: true`;
  сразу после frontmatter добавлен директивный блок «🚦 ИСПОЛНИМЫЙ ДОКУМЕНТ — НЕ
  АНАЛИЗИРУЙ, ВЫПОЛНЯЙ»; содержимое разделено на `▶️ EXECUTION` (Handover Prompt
  и 4-шаговый протокол) и `ℹ️ EXPLANATION` (модель процесса, threat awareness,
  перекрёстные ссылки) без потери смысла. Структурный валидатор
  `tools/validate-repository-structure.sh` обновлён под новую версию/дату и
  проверяет наличие маркеров и блоков EXECUTION/EXPLANATION.

### Removed

- Issue #199: removed the active `research/portal/` package, the old mixed
  `standards/webportal-concept-standard.md`, the portal-specific
  `standards/portal-repository-structure.md`, the old
  `templates/webportal-concept-template.md` and the generated root `.gitkeep`
  placeholder.

### Added

- Issue #165 (Creative mode): **зафиксирован слоган Хаба** «Человек задаёт
  смысл, AI ускоряет путь — вместе по правилам» в `README.md`,
  `AI_GOVERNANCE.md` и `templates/spoke/README.md` (primary для Хаба,
  наследуется споками); слоган закреплён проверками структурного валидатора.
  Добавлены три стандарта оформления —
  `standards/research-profile.md` (структура research:
  Введение → Результаты → Детализация),
  `standards/executable-contract-standard.md` (EXECUTION → EXPLANATION, команда
  первой строкой) и `standards/contract-documentation-standard.md`
  (нормативный язык RFC 2119 / BCP 14) — каждый с опорой на отдельное
  исследование в новом каталоге `research/governance/`
  (`research-documentation-format-2026-06.md`,
  `executable-contract-format-2026-06.md`,
  `contract-documentation-format-2026-06.md` и запись решений
  `governance-folder-structure-decisions-2026-06.md` плюс навигация
  `README.md`). Добавлен навигационный индекс `governance/rfc/README.md`. Все
  новые артефакты зарегистрированы как active в
  `tools/validate-repository-structure.sh` (`is_active_file`, `required_files`,
  `required_directories`) и в `governance/artifact-map.md`.
- Issue #159 (Creative mode): концепт-проект портала `open-ai.ru` («единая точка
  сборки» spoke-проектов) — независимое исследование, сравнительный анализ и
  предложение без старта реализации. Добавлен RFC
  `governance/proposals/open-ai-portal-concept-rfc.md` (15 разделов: 5 слоганов,
  сравнение 4 вариантов концепции по матрице из 14 критериев, синтез
  оптимального решения, дорожная карта Phase 0–4 и запрос на согласование с
  7 вопросами фаундеру); черновик стандарта
  `standards/portal-repository-structure.md` (структура репозитория портала,
  наследующая геном спока и добавляющая портал-каталоги); четыре research-отчёта в
  новом подкаталоге `research/portal/` — сравнение стандартов документации (вывод:
  ADR + C4 — обязательное ядро), сравнение архитектур и стека (модульный монолит,
  SSG + islands, Cloudflare Pages, Supabase, выбор фреймворка по матрице), дизайн
  структуры репозитория и паттерны интеграции AI/`mango_ba_prompts` (Yandex GPT
  через serverless-proxy, content-collection санитизированных промптов, граница
  приватности) — плюс навигация `research/portal/README.md`. Все артефакты
  зарегистрированы как active в `tools/validate-repository-structure.sh`
  (`is_active_file`, `required_files`, `required_directories`),
  `governance/artifact-map.md` (версия карты 1.15 → 1.16), `research/README.md`
  и реестре `standards/README.md`. Стандарт и RFC — в статусе `draft`: принятие
  как обязательного остаётся решением человека (AI_GOVERNANCE, правило 4).
  Реализация портала не начиналась.

- Issue #145 (CE-008): в `standards/glossary.md` (версия 1.1 → 1.2) добавлены
  термины **«Исполнимый документ» (Executable Contract)** и **«Директивный
  блок»** из стандарта исполнимых документов
  `governance/proposals/contract-executability-rfc.md` (§4.2, §6.1, §7).
  Указаны контекст использования и примеры артефактов; зафиксирована
  ортогональность с `Operating Mode` (нет терминологической коллизии: `executable`
  помечает тип документа, Operating Mode — режим выполнения задачи). В раздел
  «Связи терминов» добавлены связи `Исполнимый документ -> Директивный блок`,
  `Operating Mode ⟂ Исполнимый документ` и `Исполнимый документ -> Validation`
  для traceability. Структурный валидатор
  `tools/validate-repository-structure.sh` обновлён под новую версию/дату и
  проверяет наличие новых терминов.

- Issue #133: созданы отдельные GitHub Issues CE-001..CE-010
  ([#138](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/138)–[#147](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/147))
  для каждого файла из плана внедрения стандарта исполнимых документов
  `governance/proposals/contract-executability-rfc.md` §6.1. В
  `governance/backlog.md` добавлен отдельный backlog-раздел с приоритетами,
  зависимостями и ссылками на issues; создан реестр
  `governance/executable-documents-issues.md`; реестр зарегистрирован в
  `governance/artifact-map.md` и структурном валидаторе. Физический рефакторинг
  файлов из RFC §6.1 не выполнялся.

- Issue #124: новый research-артефакт
  `research/hub/ai-collaboration-retrospective-mango-migration-2026-06.md` —
  ретроспектива ошибок AI-агента в сессии проектирования миграции Mango
  (Хаб → спок): реестр из 5 ошибок (режимы, pre-flight контекст, Anti-Inflation,
  формат issue, архитектурное размещение артефактов), их корневые причины и
  4 системных вывода для будущего onboarding/governance proposal (режим
  `Research`, governance-файлы не меняются). Имя файла осознанно отличается от
  запрошенного в issue `ai-collaboration-retrospective-2026-06.md`: тот файл уже
  существует в `main` и описывает другую сессию (проектирование шаблонов споков,
  #95) — перезапись уничтожила бы прежний артефакт. Новые термины «Ретроспектива»
  и «Корневая причина» добавлены в `standards/glossary.md` (версия 1.0 → 1.1) как
  единый источник определений. Артефакт зарегистрирован как active в
  `tools/validate-repository-structure.sh` (`is_active_file`) и в навигации
  `research/hub/README.md`. Удалён сгенерированный харнессом корневой `.gitkeep`
  (его нет в `main`), снимавший FAIL структурного валидатора.
- Issue #113 (B-007): в шаблон генома спока `templates/spoke/AI_GOVERNANCE.md`
  добавлена секция «Границы действий» — простая capability taxonomy из трёх
  корзин разрешений **прозой** («можно без спроса / можно с апрувом / нельзя
  никогда») с 1–2 примерами на корзину. Сознательно без YAML-машинерии и
  таблиц: формальный Capability Manifest (YAML) `ОТЛОЖЕН` до первого инцидента
  (решение Конарда, упрощающее «ментальный список» команды Q сильнее; источники
  — Q «взять сейчас», команда С `[C5]`, внешний паттерн `[GAP]`). Секция даёт
  агенту ясные границы между корзинами «Правила» и «Эскалация» без новой
  структуры (Anti-Inflation).
- Issue #115 (B-005): шаблон `templates/spoke/README.md` (точка входа **Кейса 2**,
  *Bootstrap-клонирование*) дополнен разделами «🛠️ Как адаптировать
  `{{...}}`-плейсхолдеры» (таблица плейсхолдеров, запуск `init.sh`, ручная правка,
  пояснение про `{{REPO_NAME}}`) и «✅ Как валидировать структуру» (запуск
  `./tools/validate-repository-structure.sh` перед PR). Замкнуты перекрёстные
  ссылки между двумя точками входа (follow-up #4, #5 RFC-манифеста двух кейсов):
  спок-README → Хаб `governance/agent-onboarding.md` (Кейс 1),
  `rfc-two-cases-of-project-initialization.md` и canonical rationale в этом README
  через `{{hub_url}}`; обратная ссылка (онбординг → спок-README) уже существовала.
  Структурный валидатор расширен проверками контента спок-README
  (`tools/validate-repository-structure.sh`: ссылка на `governance/agent-onboarding.md`
  и наличие раздела валидации). Удалён сгенерированный харнессом корневой
  `.gitkeep` (его нет в `main`), снимавший FAIL структурного валидатора.

- Issue #114 (B-003): новый артефакт генома спока
  `templates/spoke/AI_HANDOVER_PROMPT.md` — копия *Handover Prompt* с
  плейсхолдером `{{REPO_NAME}}` (по умолчанию `hybrid-Intelligence-lab`), готовая
  «доверенность» для запуска агента (*Runtime-онбординг*) прямо из склонированного
  спока. Источник истины зафиксирован за Хабом
  ([`governance/agent-onboarding.md`](governance/agent-onboarding.md), создаётся в
  B-001 → #109): файл явно помечен как копия шаблона со ссылкой на хабовый
  оригинал, чтобы избежать рассинхронизации. Файл зарегистрирован как active в
  обоих валидаторах (`tools/validate-repository-structure.sh` — `is_active_file`,
  `required_files` и проверки контента; `templates/spoke/tools/validate-repository-structure.sh`
  — `required_files` и проверка сохранности `{{REPO_NAME}}`) и в
  `governance/artifact-map.md` (тип `шаблон`, версия карты 1.9 → 1.10).
  Перекрёстные ссылки добавлены в `templates/spoke/README.md`; шаблонный
  `templates/spoke/CHANGELOG.md` упоминает *Handover Prompt* в составе генома.
  Удалён сгенерированный харнессом корневой `.gitkeep` (его нет в `main`),
  снимавший FAIL структурного валидатора.

### Changed

- Issue #146 (CE-009): `tools/validate-frontmatter.sh` теперь мягко
  валидирует опциональные маркеры стандарта исполнимых документов:
  `executable` допускает только `true|false`, а `entrypoint` при наличии
  допускает только `true`. Поле `executable` не стало обязательным, поэтому
  существующая fail-open семантика и документы без этого маркера сохранены.
- Issue #144 (CE-007): `standards/issue-workflow.md` converted to the
  executable-documents frontmatter standard as a reference process standard.
  Version `1.0 → 1.1`, date `2026-06-04`; frontmatter now includes
  `executable: false`. The terminology note explicitly separates task
  Operating Mode from document executability, while task statuses and transition
  rules remain unchanged. The structural validator now checks the new
  version/date and `executable: false` marker.
- Issue #142 (CE-005): `governance/repo-model.md` converted to the executable
  document standard as a reference policy: added canonical frontmatter with
  `executable: false`, bumped version `1 → 1.1` and date to `2026-06-04`, and
  marked Decision Rules as the executable decision checklist inside the
  otherwise reference document. Structural validation now checks the new
  frontmatter/version markers; removed the generated harness `.gitkeep`.
- Issue #143 (CE-006): `standards/project-structure-inheritance.md` converted
  to the executable-documents standard as a reference standard. Version
  `1.0 → 1.1`; `updated` is now `2026-06-04`; frontmatter explicitly contains
  `executable: false`. The project-structure inheritance rules are unchanged,
  and `tools/validate-repository-structure.sh` now checks the new metadata.

- Issue #147 (CE-010): `governance/artifact-map.md` refactored for the
  executable-documents standard. Version `1.14 → 1.15`; the main artifact table
  now has a `🚦 Исполнимый?` column with `🚦 entrypoint`, `🚦 да`, `справка` and
  `—` markers. RFC `governance/proposals/contract-executability-rfc.md` remains
  registered in `governance/proposals/` and is linked from the map legend,
  related contracts and the relevant executable/reference rows. The structural
  validator expectation is updated to the new map version and table header.

- Issue #111 (B-004): в канон `governance/repo-model.md` добавлен раздел
  «Spoke Lifecycle: два кейса инициализации», фиксирующий разделение
  *Runtime-онбординг* (Кейс 1) ⟂ *Bootstrap-клонирование* (Кейс 2) как часть
  модели жизненного цикла spoke. Operating Mode привязан к кейсу (Кейс 1 →
  `Structured`, Кейс 2 → `Project`). Раздел сознательно краткий: определения
  терминов вынесены в `standards/glossary.md`, полное обоснование с аналогиями и
  Mermaid-схемой — в RFC-манифесте
  `governance/proposals/rfc-two-cases-of-project-initialization.md`; канон
  ссылается на источники, а не дублирует их (Anti-Inflation). Снят риск
  повторения терминологической путаницы (ошибка №5 ретроспективы). Удалён
  сгенерированный харнессом корневой `.gitkeep`, снимавший FAIL структурного
  валидатора.

- Issue #110 (B-002): связаны входные точки репозитория с онбордингом. В
  `README.md` добавлены предполётный блок «🛫 Новый агент? Начни здесь →
  `governance/agent-onboarding.md`» и строка в таблице «Ключевые документы»; в
  `AI_GOVERNANCE.md` онбординг закреплён как обязательный pre-flight шаг (нота в
  шапке + ссылка в правиле 2 «читай до изменения файлов»). Это ссылки, а не
  копии протокола (Anti-Inflation, риск дублирования снят). Навигационные связи
  зафиксированы в валидаторе (`require_text` на `governance/agent-onboarding.md`
  в `README.md` и `AI_GOVERNANCE.md`) и в `governance/artifact-map.md` (связи у
  строк `README.md`, `AI_GOVERNANCE.md` и `agent-onboarding.md`; версия карты
  1.10 → 1.11). Замыкает Кейс 1: артефакт B-001 (#109) теперь виден из двух
  очевидных точек входа.
- Issue #116 (B-011): в RFC-манифест
  `governance/proposals/rfc-two-cases-of-project-initialization.md` добавлен
  раздел «Evidence trail: git history + issues + PRs как след доказательств»,
  явно называющий уже работающую способность (тезис команды С `[C5]`, метка
  «взять сейчас» из матрицы применимости) и связывающий её ссылкой с
  `research/hub/external-governance-patterns-review-2026-06.md` (разделы 1.3 и
  3.1). Имя evidence trail закреплено рядом с моделью жизненного цикла; новый
  формат/обёртка сознательно не вводятся (Anti-Inflation). Версия RFC `0.1 → 0.2`,
  во frontmatter добавлены external-review в `related_artifacts` и #116 в
  `related_issues`. Статус B-011 в `governance/backlog.md`: `ЧАСТИЧНО → DONE`.
  Удалён сгенерированный харнессом корневой `.gitkeep`, снимавший FAIL
  структурного валидатора.

- Issue #107 (B-013): `governance/backlog.md` промоутнут из `draft` в `canonical`
  (`version 0.1 → 1.0`) по команде Human Review. Замкнут маршрут «бэклог →
  issues»: по всем открытым задачам бэклога заведены отдельные issues со ссылкой
  на строку-источник — B-001 → #109, B-002 → #110, B-004 → #111, B-006 → #112,
  B-007 → #113, B-003 → #114, B-005 → #115, B-011 → #116. Задача B-014 (P3)
  намеренно отложена и не заведена; задачи `DONE` (B-010 → #105, B-008 → #91) уже
  имеют issues. В бэклог добавлена колонка «Issue» в сводной таблице, маппинг в
  разделе 3 (B-013), обновлены `related_issues` во frontmatter и разделы 6/8.
  Удалён сгенерированный харнессом корневой `.gitkeep` (его нет в `main`),
  снимавший FAIL структурного валидатора.

### Added

- Issue #109 (B-001): рабочая инструкция `governance/agent-onboarding.md`
  (`status: canonical`, тип `правило`) — единый входной артефакт *Runtime-онбординга*
  (Кейс 1) по утверждённому onboarding-дизайну. Содержит:
  *Handover Prompt* с плейсхолдером `{{REPO_NAME}}`, 4-шаговый протокол агента
  (чек-лист governance → чек-лист контекста → *Readback* → стоп до апрува), шаблон
  *Readback* и раздел threat awareness «Что может пойти не так» (5 рисков холодного
  старта) — реализация рекомендации команды Q без отдельного файла (Anti-Inflation).
  Все термины — со ссылкой на `standards/glossary.md`; добавлены перекрёстные ссылки
  на `templates/spoke/README.md` (Кейс 2) и на RFC-манифест двух кейсов. Граница с
  design rationale позже упрощена: `agent-onboarding.md` стал и рабочей
  инструкцией, и canonical-историей решений. Файл зарегистрирован как active в
  `tools/validate-repository-structure.sh` (`is_active_file`, `required_files` и
  набор `require_text`) и `governance/artifact-map.md` (версия карты 1.9 → 1.10).
- Issue #99: RFC-манифест `governance/proposals/rfc-two-cases-of-project-initialization.md`
  — концептуальное разделение двух ортогональных кейсов инициализации проекта:
  Кейс 1 (Runtime-онбординг) и Кейс 2 (Bootstrap-клонирование). Ведущая аналогия
  «сертификация самолёта ≠ лицензия пилота» + анализ ещё трёх смежных областей
  (медицина, юриспруденция, DevOps) с выводами для модели; таблица-манифест из 13
  строк; Mermaid-схема жизненного цикла проекта с явным разделением кейсов;
  обоснование с трассировкой к `research/hub/ai-collaboration-retrospective-2026-06.md`;
  фиксация будущих README по каждому кейсу и follow-up-список. Манифест
  намеренно не определяет термины — только использует их со ссылкой на глоссарий.
  Файл зарегистрирован как active в `tools/validate-repository-structure.sh` и
  `governance/artifact-map.md` (тип `RFC`, версия карты 1.6 → 1.7).

### Changed

- Issue #99: уточнён onboarding-дизайн —
  добавлен раздел «Модель процесса» (без блока терминологии, только ссылки на
  `standards/glossary.md` и на RFC-манифест), фиксирующий, что агент работает в
  *Среде работы агента* (чат) и обращается к *Источнику контекста* (репозиторий);
  *Handover Prompt* параметризован плейсхолдером `{{REPO_NAME}}` и
  переформулирован без ложной модели «агент в репозитории».
- Issue #99: в `standards/glossary.md` добавлены 6 терминов (Bootstrap-клонирование,
  Runtime-онбординг, Handover Prompt, Readback, Среда работы агента, Источник
  контекста) со ссылками на вводящие их RFC, плюс две строки связей терминов.


  — «Протокол бесшовной передачи проекта» (Seamless Project Handover Protocol)
  против ошибок холодного старта. Аналогия предполётного чек-листа и «читки
  обратно» (readback); обоснование с дословной трассировкой к 5 провалам
  ретроспективы `research/hub/project-context-and-bootstrap-patterns-2026-05.md`
  и аудиту команды C; готовый к копированию Handover Prompt для пользователя;
  4-шаговый алгоритм агента (чек-лист governance → чек-лист контекста → readback
  → стоп до апрува); Mermaid-схема потока инициализации и сравнение мест для
  будущего `agent-onboarding.md` (рекомендация — `governance/`). RFC намеренно не
  создаёт `agent-onboarding.md` и завершается блоком «Решение за человеком».
  Файл зарегистрирован как active в `tools/validate-repository-structure.sh` и
  `governance/artifact-map.md` (тип `RFC`, версия карты 1.5 → 1.6).
- Issue #93: «ДНК-шаблон» `templates/spoke/` — минимальный геном для клонирования
  новых spoke-проектов из Хаба. Девять базовых артефактов: `AI_GOVERNANCE.md`
  (конституция спока со ссылкой на Хаб), `AI_QUICK_RULES.md` (инструкция по
  выживанию агента), `README.md`, `CONTRIBUTING.md` (issue → PR → review),
  `CHANGELOG.md` (каркас с `## Unreleased`), `docs/adr/.gitkeep`,
  `docs/audit/.gitkeep`, `.github/ISSUE_TEMPLATE/task.md` (наследует поля Хаба
  из `standards/issue-workflow.md`) и исполняемый `tools/validate-repository-structure.sh`
  (минимальный валидатор с предупреждением о `research/`). Шаблон по умолчанию
  не содержит `research/`: фундаментальные знания остаются в Хабе. Креативное
  улучшение UX инициализации — исполняемый `templates/spoke/init.sh`:
  интерактивная/CLI-замена плейсхолдеров (`{{project_name}}`,
  `{{project_description}}`, `{{hub_url}}`), автоген `{{date}}` (`updated:` во
  frontmatter), портабельный `sed` (без `sed -i`) и самоудаление после запуска.
  Артефакты зарегистрированы как active в `tools/validate-repository-structure.sh`
  и `governance/artifact-map.md` (тип `шаблон`, версия карты 1.4 → 1.5).
- Issue #89: креативный дизайн "ДНК-шаблона" для клонирования spoke-проектов:
  концептуальная аналогия
  (геном, а не чемодан), сравнительная матрица имён корневого каталога
  (`templates`/`blueprints`/`genesis`), минимальная карта файлов с креативными
  комментариями, три антипаттерна, обработка краевых случаев ("А что, если...") и
  Mermaid-схема процесса клонирования. RFC соблюдает запрет на создание `research/`
  в споках по умолчанию (`docs/adr/`, `docs/audit/` только) и завершается блоком
  "Решение за человеком". Создан каталог `governance/proposals/`. Файл
  зарегистрирован как active в `tools/validate-repository-structure.sh` и
  `governance/artifact-map.md`.
- Issue #81: исследование `research/project-context-and-bootstrap-patterns-2026-05.md`
  с минималистичными паттернами передачи контекста между чатами, предсказуемого
  создания project areas и маршрута "рекомендация -> задача" на опыте Mango.
  Файл зарегистрирован как active в `tools/validate-repository-structure.sh`,
  `governance/artifact-map.md` и `research/README.md`.
- Issue #79: исследование `research/prompts-classification-audit-2026-05.md`
  (аудит входных данных: инвентаризация 6 Mango промптов, паттерны отладки,
  пробелы классификации) и `research/prompts-classification-standard-2026-05.md`
  (стандарт классификации промптов: таксономия из 6 осей, матрица «тип × зрелость
  × сценарий» с 10 ячейками, 3 шаблона для отладки формата (Simple/System/Agent),
  план интеграции к Mango промптам и вопросы для согласования). Scope: repo-wide.
  Файлы зарегистрированы как active в `tools/validate-repository-structure.sh`,
  `governance/artifact-map.md` и `research/README.md`.
- Issue #77: аудит `projects/mango/experiments/prompts-audit-2026-05-26.md`,
  self-test `projects/mango/experiments/prompts-selftest-2026-05-26.md` и
  шесть готовых Mango prompt assets в `projects/mango/prompts/`: TZ Stats,
  User Story и Use Case в вариантах `_exp` и `_simple`. Prompt assets
  зарегистрированы в `tools/validate-repository-structure.sh`,
  `projects/mango/README.md` и `governance/artifact-map.md`.
- Issue #69: справочник `research/mango/capability-decomposition-2026-05.md`
  (`status: draft`, `scope: mango-only`) — детализация уровня `Atomic Function`
  для трёх пилотных доменов (`voice-ucaas`, `contact-center`,
  `digital-channels`): 54 функции с параметрами, ≥2 международными источниками
  и примерами требований из реальных ТЗ, критерии атомарности, модель связи с
  НФТ-классами, интеграция с `kb/product-matrix.md` и процесс обновления.
  Файл зарегистрирован как active в `tools/validate-repository-structure.sh`,
  `governance/artifact-map.md` и `research/mango/README.md`.
- Issue #75: эксперимент `projects/mango/experiments/usecase_gen-stepwise-alignment_2026-05-26.md`
  и промпт `projects/mango/prompts/usecase-stepwise-generator_exp-2026-05.md`
  для пошаговой генерации Use Case с согласованием акторов, компонентов,
  controlled output, логами и тестами на 4 кейсах.
- Issue #67: четырёхуровневая иерархия `Domain → Capability → Feature →
  Atomic Function` в `research/mango/classification.md` (v3.0): семь доменов
  пилота, явные слои `📊 Product Layer` и `🛒 Commercial Layer` со связью через
  `related_commercial_fields`, пять новых `Capability` (R2.1–R2.5) и раздел
  `🚀 Возможные улучшения (не активны в v3.0)` с отложенными атрибутами
  R2.6–R2.8 (обоснование и критерии активации).
- Issue #65: Mango-only `projects/mango/standards/classification-glossary.md`
  with the Domain -> Capability -> Feature -> Atomic Function hierarchy,
  source-backed definitions, Mango examples, mapping table and terms requiring
  clarification.
- Issue #59: каркас подкаталогов `projects/mango/` (`kb/`, `prompts/`, `docs/`,
  `experiments/`, `decisions/`) как точки расширения для будущей документации
  промптов и базы знаний. Пустые папки отслеживаются в Git через `.gitkeep` и
  зарегистрированы как active в `tools/validate-repository-structure.sh`.

### Changed

- Issue #91: рефакторинг структуры `research/` (namespacing). Фундаментальные
  (`scope: repo-wide`) исследования перенесены через `git mv` из корня в новый
  подкаталог `research/hub/` (`project-context-and-bootstrap-patterns-2026-05.md`,
  `prompts-classification-audit-2026-05.md`,
  `prompts-classification-standard-2026-05.md`,
  `team-c-governance-strategy-audit-2026-05.md`,
  `user-prompts-analysis-2026-05.md`); добавлен `research/hub/README.md`.
  `research/README.md` получил строгое правило о запрете файлов в корне
  `research/` и актуализированное оглавление; пути обновлены в
  `governance/artifact-map.md` (v1.4). Валидатор структуры теперь требует
  подкаталоги `research/hub` и `research/mango` и запрещает любые файлы в корне
  `research/`, кроме `README.md`.
- Issue #77: прототипные `_exp` prompt-файлы для User Story и Use Case
  заменены короткими copy-paste промптами; валидатор структуры теперь проверяет
  наличие ровно 6 файлов в `projects/mango/prompts/` и лимиты длины prompt body
  для `_exp` / `_simple`.
- Issue #67: `research/mango/classification.md` обновлён с версии 2 до v3.0
  аддитивно — все 37 существующих строк сохранены и переструктурированы под
  новую модель; сравнительная таблица международной классификации дополнена
  колонками `Domain → Capability (v3.0)` и `BABOK` и строками 38–42; HTML-экспорт
  `research/mango/classification.html` перегенерирован.
- Issue #65: `projects/mango/README.md`, `governance/artifact-map.md` and
  `tools/validate-repository-structure.sh` now register the Mango
  classification glossary as an active project artifact.
- Issue #59: раздел «Шаблон структуры» в `projects/mango/README.md` (v1.1)
  дополнен папкой `decisions/` и пометкой о том, что подкаталоги уже созданы как
  placeholder-точки.

### Removed

- Issue #81: повторно удалён служебный корневой `.gitkeep`, восстановленный при
  создании PR-ветки, чтобы `tools/validate-repository-structure.sh` проходил
  без ошибок.
- Issue #77: удалены root `.gitkeep` из служебного PR-initial commit и
  `projects/mango/prompts/.gitkeep`, потому что `prompts/` теперь содержит
  шесть активных prompt files.
- Issue #69: повторно удалён служебный корневой `.gitkeep`, восстановленный при
  создании PR-ветки, чтобы `tools/validate-repository-structure.sh` проходил без
  ошибок.
- Issue #75: повторно удалён служебный корневой `.gitkeep`, восстановленный при
  создании PR-ветки, чтобы `tools/validate-repository-structure.sh` проходил без
  ошибок.
- Issue #67: повторно удалён служебный корневой `.gitkeep`, восстановленный при
  создании PR-ветки, чтобы `tools/validate-repository-structure.sh` проходил без
  ошибок.
- Issue #59: служебный корневой `.gitkeep`, автогенерированный при создании PR,
  чтобы `tools/validate-repository-structure.sh` снова проходил без ошибок.

## [1.1] - 2026-05-26

### Added

- Issue #52: draft-концепция `research/mango/taxonomy-concept-2026-05.md`
  для Unified Capability Taxonomy Mango: обзор применимых стандартов,
  мета-модель capability, mapping реальных фич, процесс нормализации,
  интерфейс продуктовых команд, метрики, план пилота и риски.
- Issue #49: active directory indexes for `projects/`, `research/`,
  `education/` and `frameworks/` after cleanup of legacy `-old` inputs.
- Issue #49: active Mango research artifacts in `research/mango/`
  (`README.md`, `classification.md`, `classification-tz.md`,
  `requirements-flow.md` and HTML exports) with frontmatter and source
  traceability.
- Issue #47: проект `projects/repo-development/` с навигационным `README.md` и
  отчётом аудита миграции `docs/migration-audit-2026-05.md` (чек-лист
  согласованности с `CONCEPT.md`, матрица перекрёстных ссылок, таблица миграции
  `-old`, ≥5 примеров переноса ценного содержания, ≥3 предложения по улучшениям
  со статусом «На рассмотрении» и рекомендация по удалению `-old` в категориях
  ✅/⚠️/❌). Новые активные файлы зарегистрированы в
  `tools/validate-repository-structure.sh` и связаны из корневого `README.md`.
- Issue #43: `governance/artifact-map.md` — canonical карта артефактов для
  навигации (таблица «Путь | Тип | Назначение | Обязательный? | Связанные
  артефакты», разделы «Как использовать карту» и «Как обновлять карту»).
  Зарегистрирована как active в `tools/validate-repository-structure.sh` и
  связана из `README.md` и `standards/README.md`.
- Canonical file naming standard в `standards/file-naming.md` для
  исследований, standards, экспериментов, профилей и курсов; зарегистрирован
  в `standards/README.md` и structure validation.
- Canonical education project profile в `standards/education-profile.md` для
  структуры курсов, модулей, уроков, упражнений и адаптации под open,
  commercial и internal learning formats.
- Canonical glossary в `standards/glossary.md` для единых терминов standards,
  governance и AI-assisted work.
- Issue #17 migration structure: `CONCEPT.md`, обновленные root governance
  files, `standards/README.md`, `governance/repo-model.md` и `tools/`.
- Repository structure validation в `tools/validate-repository-structure.sh`.
- Issue #35: soft frontmatter validation в `tools/validate-frontmatter.sh`
  для проверки обязательных полей `status`, `version`, `updated` и
  `ai-generated` без блокирующего exit code.
- Active documentation для Anti-Inflation principle: артефакт создается только
  когда снижает операционную боль.
- Issue #31: `standards/research-profile.md` — canonical профиль
  исследовательских проектов (именование `YYYY-MM-topic.md`, frontmatter
  исследований, организация экспериментов `exp-<slug>/`, чек-лист публикации и
  цитируемые best practices). Зарегистрирован как active в `standards/README.md`
  и проверяется в `tools/validate-repository-structure.sh`.
- `standards/product-profile.md` (issue #29): профиль для продуктовых проектов
  с обязательными артефактами, шаблоном `PRODUCT_VISION.md` и матрицей
  адаптации по стадиям MVP / Pilot / Production; зарегистрирован в реестре
  standards и в structure validation.
- `standards/team-contract.md` как шаблон и инструкция для создания
  project-level `CONTRIBUTING.md` и `AI_GOVERNANCE.md` в spoke-проектах.
- Issue #41: `standards/issue-workflow.md` — canonical жизненный цикл задач
  (7 статусов: `draft`, `ready`, `in-progress`, `review`, `merged`, `closed`,
  `blocked`), правила переходов, связи между артефактами (`User Story / ФТ`,
  `CHANGELOG.md`, `governance/artifact-map.md`) и точки автоматизации.
  Зарегистрирован как active в `standards/README.md` и проверяется в
  `tools/validate-repository-structure.sh`.

### Changed

- Issue #49: migration state updated from "legacy files preserved for analysis"
  to "legacy files removed or promoted"; `projects/mango/README.md` now links
  to active project/research navigation instead of `projects/README-old.md`.
- Issue #49: `tools/validate-repository-structure.sh` now registers promoted
  active files and fails if tracked `-old` files are reintroduced.
- Issue #47: previous tracked files were renamed with suffix `-old` for audit
  and selective migration before cleanup issue #49.
- Active navigation теперь указывает на `governance/` вместо `meta/` и на
  `tools/` вместо `tests/`.
- Standards рассматриваются как плоский registry, пока operational use не
  докажет потребность в более глубокой taxonomy.

### Removed

- Issue #49: removed legacy root files, old GitHub templates, `docs-old/`,
  `meta-old/`, `tests-old/`, `experiments-old/`, old education package files,
  repository-governance archive candidates, `.gitkeep` placeholders and other
  superseded `-old` inputs according to the migration audit categories.

## Связанные документы

- [README.md](README.md)
- [CONCEPT.md](CONCEPT.md)
- [AI_GOVERNANCE.md](AI_GOVERNANCE.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [standards/README.md](standards/README.md)
- [standards/glossary.md](standards/glossary.md)
- [standards/file-naming.md](standards/file-naming.md)
- [standards/education-profile.md](standards/education-profile.md)
- [standards/team-contract.md](standards/team-contract.md)
- [standards/issue-workflow.md](standards/issue-workflow.md)
- [governance/repo-model.md](governance/repo-model.md)
- [governance/artifact-map.md](governance/artifact-map.md)

## TODO

- Добавить concrete artifact templates после появления повторяющихся работ и
  стабильных потребностей.
- Заменить license placeholder после решения Founder & PO.
