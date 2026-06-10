---
status: draft
version: 0.2
updated: 2026-06-06
ai-generated: true
type: rfc
context: [repository-quality, audit, cleanup, governance, traceability, archive]
method: repository-audit + validator-baseline + link-scan + duplicate-scan
scope: repo-wide
related_artifacts:
  - "governance/artifact-map.md"
  - "governance/backlog.md"
  - "governance/repo-model.md"
  - "standards/file-naming.md"
  - "standards/research-profile.md"
  - "tools/validate-repository-structure.sh"
  - "tools/validate-frontmatter.sh"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/171"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/177"
---

# RFC: Repository Quality Improvement Plan

Этот RFC фиксирует аудит и план, а не выполняет физическую очистку репозитория.
Решение о применении фаз и создании отдельных задач принимает человек.

## Changelog

### v0.2 (2026-06-06)

- Структурирован раздел "Full draft list" с новыми колонками.
- Добавлены рекомендации и обоснования для каждого draft-документа.
- Добавлен раздел "Триаж по категориям".

## 1. Executive Summary

### 1.1. Контекст

После merge PR #170 репозиторий в целом приведён к новой структуре, но аудит
показывает несколько классов долга:

- naming-контракт и валидатор покрывают не все вложенные каталоги;
- часть документов дублирует `status` / `version` / `updated` из frontmatter в
  теле;
- карта артефактов и валидатор всё ещё делают архив Mango обязательным;
- после миграций остались stale-ссылки на удалённые `projects/mango/` и
  `*-old.md` пути;
- 52 audit-scope документа имеют `status: draft` во frontmatter и требуют
  явного решения: согласовать, оставить как draft с exit-plan, объединить,
  удалить или вынести в отдельную задачу.

Концепция портала `open-ai.ru` не анализируется по смыслу: это отдельный scope.
В этом RFC учитываются только repository-quality факты, например битые ссылки в
файлах `research/portal/`.

### 1.2. Метод аудита

Проверки:

- `git ls-files` по всем tracked files;
- scan naming для `standards/`, `governance/rfc/`, `research/` и broader nested
  exceptions;
- exact duplicate scan по tracked text files;
- high-overlap scan по Markdown body без frontmatter;
- scan повторов metadata в body;
- scan локальных Markdown links и frontmatter relation fields;
- scan `status: draft` во frontmatter;
- baseline validators:
  - `./tools/validate-frontmatter.sh .`;
  - `./tools/validate-repository-structure.sh`.

Baseline validation до удаления PR-заглушки:

| Проверка | Результат | Комментарий |
| --- | --- | --- |
| `./tools/validate-frontmatter.sh .` | exit 0, 15 warnings | Warnings уже существуют: root/docs without frontmatter, template placeholders `{{date}}`, template issue body. |
| `./tools/validate-repository-structure.sh` | exit 1 | Единственный FAIL: tracked root `.gitkeep` из auto-generated PR placeholder. |

### 1.3. Приоритеты

| Направление | Вывод | Приоритет |
| --- | --- | --- |
| Именование | `standards/`, `governance/rfc/`, `research/` чистые; broader nested CAPS/underscore exceptions не согласованы явно. | P1 |
| Дубли | Exact duplicate content найден только в пустых `.gitkeep` архива; semantic overlap в основном ожидаемый (standard/template, research/standard), но нужен decision по research profile vs research documentation standard. | P1 |
| Metadata duplication | Повтор `version`/`updated`/`status` найден во многих standards/governance/research docs. | P1 |
| Трассировка | Есть реальные stale-ссылки и stale frontmatter relations после миграций. | P1 |
| Draft-документы | 52 draft frontmatter documents; часть draft является нормальной, часть требует human review или cleanup. | P2 |
| `archive/projects/mango/` | 17 tracked files, 4 `.gitkeep`; архив уже мигрировал во внешний spoke и должен быть удалён после согласования. | P1 |

## 2. Найденные Проблемы

### 2.1. Ошибки именования

Правило именования задано в [standards/file-naming.md](../../standards/file-naming.md):
корень репозитория допускает `UPPERCASE_WITH_HYPHENS.md`, вложенные каталоги
используют `lowercase-with-hyphens.md`; для `standards/` CAPS запрещён явно
(`standards/file-naming.md:20-30`).

| Scope | Результат | Приоритет | Рекомендация |
| --- | --- | --- | --- |
| `standards/` | Нарушений нет. Все `.md` кроме `README.md` используют kebab-case. | P0 закрыт | Ничего не менять. |
| `governance/rfc/` | Нарушений нет: все RFC используют kebab-case. | P0 закрыт | Ничего не менять. |
| `research/` | Нарушений lowercase/hyphen для tracked `.md`/`.html` нет. | P0 закрыт | Ничего не менять. |
| broader nested governance | `governance/agent-onboarding-protocol.md`, `governance/artifact-map.md`, `governance/backlog.md`, `governance/executable-documents-issues.md`, `governance/repo-model.md` остаются CAPS style inside nested directory. | P1 | Human decision: либо переименовать в kebab-case, либо явно закрепить legacy/governance exception в `file-naming.md` и validator. |
| templates/htom root-like files | `templates/htom/AI_GOVERNANCE.md`, `AI_SESSION_HANDOVER_PROMPT.md`, `AI_QUICK_RULES.md`, `CONTRIBUTING.md` выглядят как violations во вложенном каталоге, но при копировании в spoke становятся root files. | P2 | Зафиксировать template-root exception явно, чтобы scanner не считал это silent violation. |
| `archive/projects/mango/` | 8 файлов с `_` в имени (`*_exp`, `*_simple`, `user-story_gen...`, `usecase_gen...`). | P1 | Не переименовывать архив; удалить весь `archive/projects/mango/` после approval. |

Пробел валидатора: [tools/validate-repository-structure.sh](../../tools/validate-repository-structure.sh)
проверяет kebab-case только для `standards/` (`validate_standards_file_naming`,
строки 150-166). Для `governance/rfc/`, `research/` и broader nested paths
автоматической проверки пока нет.

### 2.2. Дублирующие и перекрывающиеся документы

Exact duplicates:

| Файлы | Тип | Приоритет | Рекомендация |
| --- | --- | --- | --- |
| `archive/projects/mango/decisions/.gitkeep`, `docs/.gitkeep`, `experiments/.gitkeep`, `kb/.gitkeep` | Пустые identical files | P1 | Удаляются вместе с archive. |

Semantic overlap:

| Пара | Наблюдение | Приоритет | Рекомендация |
| --- | --- | --- | --- |
| `standards/research-profile.md` + бывший draft body-standard | Не exact duplicate. `research-profile.md:45-84` задаёт артефакты, naming, frontmatter и воспроизводимость; бывший отдельный draft отвечал только за порядок body. | P1 | Решение Phase 1: слить правила порядка изложения в `research-profile.md` и удалить отдельный draft. |
| `research/governance/*-format-2026-06.md` + `standards/*-standard.md` | Ожидаемая пара research -> standard. | P2 | Оставить, но добавить явное правило "research source не является duplicate standard". |
| `standards/webportal-concept-standard.md` + `templates/webportal-concept-template.md` | Ожидаемая пара standard -> copyable template. | P2 | Оставить; в template frontmatter решить placeholder-warning отдельно. |
| `AI_GOVERNANCE.md` + `templates/htom/AI_GOVERNANCE.md` | Ожидаемая hub contract -> spoke template пара. | P2 | Оставить; relation должна быть описана как inheritance/template, не duplicate. |
| `research/hub/ai-collaboration-retrospective-2026-06.md` + `research/hub/ai-collaboration-retrospective-mango-migration-2026-06.md` | Высокое пересечение темы ретроспектив, но разные события. | P2 | При следующем изменении добавить cross-link "общая ретроспектива / Mango migration retrospective", не объединять автоматически. |

### 2.3. Дублирование метаданных

Паттерн: frontmatter содержит `status`, `version`, `updated`, а тело повторяет
`Версия:`, `Дата:` и иногда `Статус:`. Это повышает риск рассинхрона.

Standards с повтором metadata:

| Файл | Повтор в body | Приоритет |
| --- | --- | --- |
| `standards/contract-documentation-standard.md` | `19: Версия`, `21: Дата`, `23: Статус` | P1 |
| `standards/education-profile.md` | `10: Версия`, `12: Дата` | P1 |
| `standards/executable-contract-standard.md` | `19: Версия`, `21: Дата`, `23: Статус` | P1 |
| `standards/file-naming.md` | `10: Версия`, `12: Дата` | P1 |
| `standards/glossary.md` | `10: Версия`, `12: Дата` | P1 |
| `standards/issue-workflow.md` | `11: Версия`, `13: Дата` | P1 |
| `standards/portal-repository-structure.md` | `18: Версия`, `20: Дата`, `22: Статус` | P1 |
| `standards/product-profile.md` | `10: Версия`, `12: Дата` | P1 |
| `standards/research-profile.md` | `19: Версия`, `21: Дата`, `23: Статус` | P1 |
| `standards/research-profile.md` | `10: Версия`, `12: Дата` | P1 |
| `standards/team-contract.md` | `10: Версия`, `12: Дата` | P1 |
| `standards/webportal-concept-standard.md` | `26: Версия`, `28: Дата`, `30: Статус` | P1 |

`standards/project-structure-inheritance.md` уже не дублирует body metadata и
может служить эталоном минимального формата.

Broader repeated metadata exists in root, governance, project, research and
archive docs; phase 2 should remove it by class, not random one-off edits.

### 2.4. Нарушения трассировки

Confirmed broken or stale local references:

| Файл | Строка | Проблема | Приоритет | Рекомендация |
| --- | --- | --- | --- | --- |
| `projects/repo-development/docs/contract-violations-self-report-2026-06.md` | 105 | Link points to deleted `../../../docs/analysis/contract-executability-rfc.md`. | P1 | Replace with `../../../governance/rfc/contract-executability-rfc.md`. |
| `research/mango/taxonomy-concept-2026-05.md` | 43-45 | Links point to deleted `classification-old.md`, `classification-tz-old.md`, `requirements-flow-old.md`. | P1 | Replace with active `classification.md`, `classification-tz.md`, `requirements-flow.md` or mark as historical source without link. |
| Superseded spoke-template design draft | 12 | Frontmatter pointed to `research/project-context-and-bootstrap-patterns-2026-05.md`; actual file is under `research/hub/`. | P1 | Merged into `templates/htom/README.md`; stale draft removed. |
| `research/mango/capability-decomposition-2026-05.md` | 11-12 | `related_artifacts` includes `classification.md v3.0` and `classification-glossary.md`; one value mixes path and version, the other does not resolve locally. | P1 | Use path-only relation values; move version into prose if needed. |
| `research/portal/ai-and-mango-integration-patterns-2026-06.md` | 13, 168 | References deleted `projects/mango/README.md`. | P1, portal-deferred | Decide whether to point to `archive/projects/mango/README.md` or external `mango_ba_prompts`; do not alter portal concept semantics here. |
| `research/portal/repository-structure-design-2026-06.md` | 157 | References deleted `projects/mango/README.md`. | P1, portal-deferred | Same decision as above. |

Artifact map and validator inconsistencies:

| Файл | Строки | Проблема | Приоритет |
| --- | --- | --- | --- |
| `governance/artifact-map.md` | 128 | Related artifacts include deleted `projects/mango/README.md`. | P1 |
| `governance/artifact-map.md` | 136-149, 175 | Archive Mango is documented as present and mostly mandatory. | P1 |
| `tools/validate-repository-structure.sh` | 187-192, 244-260 | Archive Mango directories and files are required by validation. | P1 |
| `README.md` | 58 | Root README points reviewers to archive copy. | P1 |
| `projects/README.md` | 65 | Project index says archive copy exists. | P1 |
| `governance/artifact-map.md` | none for `projects/education-ba-prompt/*` | `README.md` and validator know this project, but artifact map has no row for `projects/education-ba-prompt/README.md` or `docs/course-ideas.md`. | P2 |

Scanner false positives excluded from the problem list:

- example links in standards (`2026-05-topic.md`, `module-01/`, `lesson-01.md`);
- template placeholders such as `{{hub_url}}`;
- external shorthand references to `mango_ba_prompts` when used as prose, not
  Markdown local links.

### 2.5. Draft-документы

Frontmatter scan found 52 draft documents in audit scope before Phase 1
cleanup, excluding this RFC itself:

| Группа | Count | Recommendation |
| --- | ---: | --- |
| `archive/` | 11 | Delete with `archive/projects/mango/`. |
| `governance/` | 5 | Keep as RFC until human decision; each needs accept/reject/update status. |
| `projects/` | 2 | Keep draft sandbox or promote to reviewed after education-scope decision. |
| `research/` | 22 | Review by domain; classify as `reviewed`, keep `draft` with exit-plan, or supersede. |
| `standards/` | 5 | Human approval required; accepted standards become `reviewed`/`canonical`, rejected/merged drafts are removed. |
| `templates/` | 7 | Decide whether template placeholder frontmatter should remain draft or be exempted from strict date validation. |

Full draft list:

| Номер | Файл | Линия | Саммари | Рекомендация на русском | Обоснование |
| ---: | --- | ---: | --- | --- | --- |
| 1 | `governance/rfc/README.md` | 2 | Навигация по RFC Хаба: правила попадания в каталог, список RFC и связанные governance-артефакты. | Перевести в canonical | Каталог уже принят как `governance/rfc/` после issue #165 и используется в 4 связанных файлах; документ фиксирует навигацию, а не спорное решение. |
| 2 | `governance/rfc/rfc-two-cases-of-project-initialization.md` | 2 | RFC-манифест разделяет Runtime-онбординг и Bootstrap-клонирование, связывает термины с onboarding и spoke-template. | Перевести в canonical | Термины уже используются в `agent-onboarding-protocol.md`, `templates/htom/README.md` и других RFC; документ упоминается в 9 файлах и стабилизирует vocabulary Хаба. |
| 3 | `research/governance/governance-folder-structure-decisions-2026-06.md` | 2 | Decision record по структуре governance-каталогов: `rfc/` вместо `proposals/`, границы portal research и правила исторических ссылок. | Перевести в canonical | Решения Q1-Q3 уже реализованы в структуре репозитория и валидаторе; документ связан с 4 файлами и должен стать canonical evidence для переименований. |
| 4 | `research/governance/contract-documentation-format-2026-06.md` | 2 | Исследование формата контрактных документов: RFC 2119, API contracts, SLA, design by contract и ADR-подход. | Перевести в canonical | Документ является источником для `standards/contract-documentation-standard.md` и упоминается в 4 файлах; после human review его можно зафиксировать как research source. |
| 5 | `research/governance/executable-contract-format-2026-06.md` | 2 | Исследование формата исполнимых контрактов: action-first структура, системные prompt-паттерны, runbook-подход и восприятие агентом. | Перевести в canonical | На документ опирается `standards/executable-contract-standard.md`; он связан с 3 файлами и уже отражён в принятых executable-doc работах. |
| 6 | `research/governance/research-documentation-format-2026-06.md` | 2 | Исследование структуры research-документов Хаба: BLUF, traceability, выводы, детализация и связи с decision-making. | Перевести в canonical | Документ является источником для раздела порядка изложения в `standards/research-profile.md` и связан с 4 файлами; после Phase 1 merge его можно закрыть как canonical source. |
| 7 | `standards/contract-documentation-standard.md` | 2 | Стандарт оформления контрактных документов Хаба: нормативный язык, frontmatter, секции и decision traceability. | Перевести в canonical | Стандарт уже зарегистрирован в валидаторе и связан с 8 файлами; препятствий кроме human approval и снятия draft-статуса не найдено. |
| 8 | `standards/executable-contract-standard.md` | 2 | Стандарт исполнимых контрактов: разделение EXECUTION/EXPLANATION, директивный блок и требования к агентскому выполнению. | Перевести в canonical | Формат уже применён в `agent-onboarding-protocol.md` и `templates/htom/AI_SESSION_HANDOVER_PROMPT.md`; документ упоминается в 9 файлах и готов к approval. |
| 9 | `research/portal/README.md` | 2 | Навигация по исследованиям портала open-ai.ru: concept, architecture, documentation, repository structure и AI integration. | Отложить | Scope `portal` и сам портал ещё не согласованы; документ связан с 4 файлами, но зависит от отдельного portal review вне repository cleanup. |
| 10 | `research/portal/ai-and-mango-integration-patterns-2026-06.md` | 2 | Исследование AI-интеграции портала: Yandex GPT, `mango_ba_prompts`, auth, маскирование данных и serverless proxy. | Отложить | В разделе 2.4 уже отмечены stale-ссылки на удалённый `projects/mango/README.md`; смысл портальной интеграции должен решаться отдельной portal-задачей. |
| 11 | `research/portal/architecture-and-stack-comparison-2026-06.md` | 2 | Сравнение архитектуры и технологического стека open-ai.ru: SSG, serverless, hosting, open-source и AI integration. | Отложить | Документ относится к portal scope и упоминается в 6 файлах; repository-quality RFC явно не анализирует смысл концепции `open-ai.ru`. |
| 12 | `research/portal/concept-standards-comparison-2026-06.md` | 2 | Исследование стандартов концепции портала: PRD, Vision, RFC, TOGAF-модульность, roadmap и links to research. | Отложить | Документ является источником для портального стандарта, но принятие стандарта зависит от отдельного решения по portal governance. |
| 13 | `research/portal/documentation-standards-comparison-2026-06.md` | 2 | Сравнение стандартов документации портала: ADR, C4, decision traceability, architecture docs и AI-native практики. | Отложить | Документ связан с 7 файлами, но используется только внутри portal package; перевод в canonical преждевременен до согласования portal концепции. |
| 14 | `research/portal/open-ai-portal-concept-rfc.md` | 2 | RFC концепции open-ai.ru: коммуникационный хаб, варианты решения, roadmap, риски и вопросы согласования. | Отложить | Это отдельный concept-RFC, связанный с 10 файлами; текущий RFC фиксирует только repository-quality факты и не должен утверждать portal direction. |
| 15 | `research/portal/repository-structure-design-2026-06.md` | 2 | Исследование структуры репозитория портала: hub-and-spoke inheritance, spoke template, каталогизация и governance boundaries. | Отложить | В разделе 2.4 отмечена stale-ссылка на `projects/mango/README.md`; правка ссылок нужна отдельно, а статус зависит от portal approval. |
| 16 | `standards/portal-repository-structure.md` | 2 | Стандарт структуры репозитория веб-портала: наследование spoke-генома, portal-specific каталоги и validation expectations. | Отложить | Стандарт упоминается в 12 файлах, но является portal-specific; canonical-решение должно следовать после согласования `open-ai.ru`. |
| 17 | `standards/webportal-concept-standard.md` | 2 | Стандарт структуры концепции веб-портала: обязательное PRD-ядро, Vision/TOGAF-модули, roadmap, risks и metrics. | Отложить | Стандарт связан с 6 файлами, но его применение зависит от решения по portal-концепциям и шаблону; оставлять draft до approval. |
| 18 | `templates/webportal-concept-template.md` | 2 | Копируемый шаблон концепции веб-портала с placeholders, portal scope и секциями из webportal concept standard. | Отложить | Шаблон зависит от `standards/webportal-concept-standard.md` и содержит `{{date}}`; нужен общий подход к template placeholders перед снятием draft. |
| 19 | `governance/rfc/contract-executability-rfc.md` | 2 | RFC архитектуры исполнимых документов: маркеры `executable`, directive block, rollout plan и решения фаундера. | Доработать | Принятые части уже вынесены в `agent-onboarding-protocol.md` и standards, но RFC ещё содержит planning/history blocks; нужен explicit статус accepted/superseded по разделам. |
| 20 | `projects/education-ba-prompt/README.md` | 2 | Навигация sandbox-проекта курса БА по prompt engineering: цель, docs, связь с education-profile и текущий draft scope. | Доработать | Проект упоминается в 2 файлах и отсутствует в `artifact-map.md` по разделу 2.6; перед canonical нужно решить, это sandbox или public project. |
| 21 | `projects/education-ba-prompt/docs/course-ideas.md` | 2 | Набор идей курса: термины, практические кейсы БА, рабочие шаблоны промптов, модули и форматы подачи. | Доработать | Документ связан только с project README; требуется разнести идеи в утверждённые course artifacts или оставить как sandbox draft с exit criteria. |
| 22 | `research/governance/README.md` | 2 | Навигация по governance research: форматы research, executable contracts, contract docs и decisions по структуре папок. | Доработать | Каталог уже содержит source-документы для стандартов, но README остаётся draft; нужно синхронизировать статус с решением по derived standards. |
| 23 | `research/hub/external-governance-patterns-review-2026-06.md` | 2 | Анализ external governance patterns и матрицы применимости: что взять сейчас, что отложить, что отклонить. | Доработать | Документ упоминается в 6 файлах и содержит открытые применимые решения; нужен pass, который переносит accepted пункты в backlog или явно закрывает вопросы. |
| 24 | `research/hub/project-context-and-bootstrap-patterns-2026-05.md` | 2 | Исследование передачи контекста и предсказуемого bootstrap проекта на опыте Mango: проблемы, решения и AI checklist. | Доработать | Документ связан с 6 файлами и зависит от решения по удалению `archive/projects/mango/`; после archive decision нужно обновить ссылки и статус. |
| 25 | `research/hub/prompts-classification-audit-2026-05.md` | 2 | Аудит входных данных для классификации промптов: типы, maturity, паттерны отладки и пробелы классификации. | Доработать | Документ связан с 3 файлами и должен быть сверён с текущим состоянием внешнего `mango_ba_prompts`; без этой сверки статус canonical будет преждевременным. |
| 26 | `research/hub/prompts-classification-standard-2026-05.md` | 2 | Draft-стандарт классификации промптов: таксономия, матрица, шаблоны промптов и план интеграции. | Доработать | Документ выглядит как стандарт, но живёт в `research/hub`; нужно решить, переносить ли его в `standards/` или оставить как research source. |
| 27 | `research/hub/team-c-governance-strategy-audit-2026-05.md` | 2 | Интерпретация аудита governance strategy от команды C: риски overgrowth, рекомендации и вопросы human review. | Доработать | Документ связан с 5 файлами, но часть выводов уже покрыта external-governance review и backlog; нужно отметить superseded/accepted пункты. |
| 28 | `research/hub/user-prompts-analysis-2026-05.md` | 2 | Анализ пользовательских промптов: классификация 18 промптов, признаки устаревших паттернов, дубли и план интеграции. | Доработать | Документ связан с 2 файлами и основан на draft prompt-classification standard; нужен review после решения по prompt taxonomy. |
| 29 | `research/mango/capability-decomposition-2026-05.md` | 2 | Справочник атомарных функций Mango по доменам voice-ucaas, contact-center и digital-channels. | Доработать | Раздел 2.4 фиксирует проблемы `related_artifacts` и неразрешённые path/version значения; сначала исправить relations, затем решать статус. |
| 30 | `research/mango/rag-mapping-roadmap-2026-05.md` | 2 | Research по RAG-навигации продуктов и фич Mango: маппинг, diagram usage, roadmap автоматизации БА и вопросы согласования. | Доработать | Документ связан с 5 файлами и остаётся mango-only; нужен review после решения, какие материалы живут во внешнем Mango spoke. |
| 31 | `research/mango/requirements-lifecycle-uncertainty-2026-05.md` | 2 | Исследование жизненного цикла требований Mango: неопределённость, декомпозиция, telecom practice и exit criteria. | Доработать | Документ связан с 3 файлами, но не имеет явного exit-plan; нужно либо добавить criteria для draft, либо принять как reviewed research. |
| 32 | `research/mango/taxonomy-concept-2026-05.md` | 2 | Концепция единой таксономии Mango: capability model, mapping фич, процесс нормализации и pilot risks. | Доработать | Раздел 2.4 фиксирует stale links на `*-old.md`; сначала заменить ссылки на active файлы или историческое описание, потом решать статус. |
| 33 | `templates/htom/AI_GOVERNANCE.md` | 2 | Шаблон governance-файла spoke-проекта: роли, границы действий, escalation и связь с hub governance. | Доработать | Документ содержит `{{date}}` и template placeholders; нужно решить placeholder validation rule, иначе frontmatter warnings останутся ожидаемыми. |
| 34 | `templates/htom/AI_SESSION_HANDOVER_PROMPT.md` | 2 | Шаблон executable handover prompt для spoke: runtime onboarding, directive block и EXECUTION/EXPLANATION структура. | Доработать | Файл упоминается в 7 местах и уже оформлен как executable template, но содержит `{{date}}`; нужен общий template exemption или post-init validation rule. |
| 35 | `templates/htom/AI_QUICK_RULES.md` | 2 | Краткие правила для AI в spoke-проекте: project placeholders, operational constraints и связь с governance. | Доработать | Шаблон связан с 7 файлами, но статус зависит от решения по placeholder frontmatter и от того, какие root-like template files считать canonical. |
| 36 | `templates/htom/CHANGELOG.md` | 2 | Каркас changelog для spoke-проекта: `## Unreleased`, Keep a Changelog и SemVer placeholders. | Доработать | Файл связан с 3 файлами и содержит `{{date}}`; нужен template lifecycle rule, иначе draft-статус остаётся технической защитой. |
| 37 | `templates/htom/CONTRIBUTING.md` | 2 | Шаблон contributing для spoke: issue -> PR -> review, локальная проверка и checklist для изменений. | Доработать | Файл связан с 2 файлами и содержит placeholders; до canonical нужно согласовать, какие template root files валидируются как generated artifacts. |
| 38 | `templates/htom/README.md` | 2 | Главная навигация spoke template: состав генома, placeholders, `init.sh`, validation и ссылки на hub onboarding. | Доработать | Файл упоминается в 11 местах и является центральным template artifact; требуется решить placeholder validation before/after init. |
| 39 | Superseded onboarding design draft | 2 | Дизайн протокола бесшовной передачи проекта: handover prompt, 4-step agent algorithm и место для `agent-onboarding-protocol.md`. | Объединено с `governance/agent-onboarding-protocol.md` | Реализация и rationale теперь живут в canonical `agent-onboarding-protocol.md`; отдельный draft удалён. |
| 40 | Superseded spoke-template design draft | 2 | Дизайн ДНК-шаблона spoke: карта файлов, naming options, Mermaid-схема и anti-patterns bootstrap. | Объединено с `templates/htom/README.md` | Основные решения и unique rationale теперь живут в `templates/htom/README.md`; отдельный draft удалён. |
| 41 | former research body-order draft | 2 | Стандарт body-структуры research-документов: введение, результаты, детализация, sources, open questions и template. | Объединён с `standards/research-profile.md` | Phase 1 слил body-order rules в единый research profile и удалил отдельный draft standard; история остаётся в git. |
| 42 | `archive/projects/mango/experiments/prompts-audit-2026-05-26.md` | 2 | Архивный Mango prompt-audit: что работает в prompt assets, упрощения для simple variants и критичные ссылки для exp variants. | Удалить | Файл находится под `archive/projects/mango/`, а раздел 2.7 рекомендует удалить весь архив после approval; внешним source of truth стал `mango_ba_prompts`. |
| 43 | `archive/projects/mango/experiments/prompts-selftest-2026-05-26.md` | 2 | Архивный self-test Mango prompts: результаты проверки готовых prompt variants и идеи на будущее. | Удалить | Архив Mango создаёт stale local paths и placeholder debt; файл упоминается только как часть archive package и должен удаляться вместе с ним. |
| 44 | `archive/projects/mango/experiments/usecase_gen-stepwise-alignment_2026-05-26.md` | 2 | Архивный эксперимент пошаговой генерации Use Case с согласованием акторов, компонентов и output format. | Удалить | Имя нарушает nested kebab-case из-за underscore, но переименование архива нецелесообразно; раздел 2.7 рекомендует удалить весь archive package. |
| 45 | `archive/projects/mango/experiments/user-story_gen-from-raw-request_2026-05-26.md` | 2 | Архивный эксперимент генерации User Story из сырого запроса: partial/success runs, критерии и lessons learned. | Удалить | Файл лежит в удаляемом archive scope и имеет underscore naming exception; полезная история сохраняется в git history и внешнем Mango spoke. |
| 46 | `archive/projects/mango/prompts/tz-stats-generator_exp-2026-05.md` | 2 | Архивный experimental prompt для TZ Stats: роль, правила, workflow и start prompt. | Удалить | Prompt asset относится к migrated Mango assets; хранение в hub archive дублирует внешний spoke и поддерживает stale `projects/mango` references. |
| 47 | `archive/projects/mango/prompts/tz-stats-generator_simple-2026-05.md` | 2 | Архивный simple prompt для TZ Stats: короткий copy-paste workflow, output format и ограничения. | Удалить | Файл является частью шести archive prompt assets; section 2.7 предлагает удалить пакет целиком, а не поддерживать отдельные variants. |
| 48 | `archive/projects/mango/prompts/usecase-stepwise-generator_exp-2026-05.md` | 2 | Архивный experimental prompt для пошаговой генерации Use Case с согласованием и controlled output. | Удалить | Prompt связан с archive experiment и должен уйти вместе с `archive/projects/mango/`; active source переносится во внешний Mango repository. |
| 49 | `archive/projects/mango/prompts/usecase-stepwise-generator_simple-2026-05.md` | 2 | Архивный simple prompt для Use Case: роль, workflow, правила, формат вывода и start instruction. | Удалить | Файл дублирует migrated prompt asset в archive scope; поддержка simple/exp variants в hub противоречит решению вынести Mango. |
| 50 | `archive/projects/mango/prompts/user-story-generator_exp-2026-05.md` | 2 | Архивный experimental prompt для User Story из сырого запроса: роль, workflow, правила и start prompt. | Удалить | Файл принадлежит archive Mango package и должен удаляться с остальными prompt assets после approval, чтобы убрать stale source of truth. |
| 51 | `archive/projects/mango/prompts/user-story-generator_simple-2026-05.md` | 2 | Архивный simple prompt для User Story: краткий workflow, output format и минимальные правила генерации. | Удалить | Это migrated Mango prompt asset; раздел 2.7 рекомендует удалить весь archive package, а историю оставить в git. |
| 52 | `archive/projects/mango/standards/classification-glossary.md` | 2 | Архивный Mango glossary: Domain, Capability, Feature, Atomic Function, терминологический mapping и уточнения. | Удалить | Glossary имеет `scope: mango-only` и лежит в archive package; после external spoke decision его не нужно держать active в hub. |

### Триаж по категориям

#### К переводу в canonical (8 документов):
- [ ] `governance/rfc/README.md`
- [ ] `governance/rfc/rfc-two-cases-of-project-initialization.md`
- [ ] `research/governance/governance-folder-structure-decisions-2026-06.md`
- [ ] `research/governance/contract-documentation-format-2026-06.md`
- [ ] `research/governance/executable-contract-format-2026-06.md`
- [ ] `research/governance/research-documentation-format-2026-06.md`
- [ ] `standards/contract-documentation-standard.md`
- [ ] `standards/executable-contract-standard.md`

#### К откладыванию (10 документов):
- [ ] `research/portal/README.md`
- [ ] `research/portal/ai-and-mango-integration-patterns-2026-06.md`
- [ ] `research/portal/architecture-and-stack-comparison-2026-06.md`
- [ ] `research/portal/concept-standards-comparison-2026-06.md`
- [ ] `research/portal/documentation-standards-comparison-2026-06.md`
- [ ] `research/portal/open-ai-portal-concept-rfc.md`
- [ ] `research/portal/repository-structure-design-2026-06.md`
- [ ] `standards/portal-repository-structure.md`
- [ ] `standards/webportal-concept-standard.md`
- [ ] `templates/webportal-concept-template.md`

#### К доработке (20 документов):
- [ ] `governance/rfc/contract-executability-rfc.md`
- [ ] `projects/education-ba-prompt/README.md`
- [ ] `projects/education-ba-prompt/docs/course-ideas.md`
- [ ] `research/governance/README.md`
- [ ] `research/hub/external-governance-patterns-review-2026-06.md`
- [ ] `research/hub/project-context-and-bootstrap-patterns-2026-05.md`
- [ ] `research/hub/prompts-classification-audit-2026-05.md`
- [ ] `research/hub/prompts-classification-standard-2026-05.md`
- [ ] `research/hub/team-c-governance-strategy-audit-2026-05.md`
- [ ] `research/hub/user-prompts-analysis-2026-05.md`
- [ ] `research/mango/capability-decomposition-2026-05.md`
- [ ] `research/mango/rag-mapping-roadmap-2026-05.md`
- [ ] `research/mango/requirements-lifecycle-uncertainty-2026-05.md`
- [ ] `research/mango/taxonomy-concept-2026-05.md`
- [ ] `templates/htom/AI_GOVERNANCE.md`
- [ ] `templates/htom/AI_SESSION_HANDOVER_PROMPT.md`
- [ ] `templates/htom/AI_QUICK_RULES.md`
- [ ] `templates/htom/CHANGELOG.md`
- [ ] `templates/htom/CONTRIBUTING.md`
- [ ] `templates/htom/README.md`

#### К объединению (3 документа):
- [x] Superseded onboarding design draft -> объединён с `governance/agent-onboarding-protocol.md`
- [x] Superseded spoke-template design draft -> объединён с `templates/htom/README.md`
- [x] former research body-order draft -> объединён с `standards/research-profile.md`

#### К удалению (11 документов):
- [ ] `archive/projects/mango/experiments/prompts-audit-2026-05-26.md`
- [ ] `archive/projects/mango/experiments/prompts-selftest-2026-05-26.md`
- [ ] `archive/projects/mango/experiments/usecase_gen-stepwise-alignment_2026-05-26.md`
- [ ] `archive/projects/mango/experiments/user-story_gen-from-raw-request_2026-05-26.md`
- [ ] `archive/projects/mango/prompts/tz-stats-generator_exp-2026-05.md`
- [ ] `archive/projects/mango/prompts/tz-stats-generator_simple-2026-05.md`
- [ ] `archive/projects/mango/prompts/usecase-stepwise-generator_exp-2026-05.md`
- [ ] `archive/projects/mango/prompts/usecase-stepwise-generator_simple-2026-05.md`
- [ ] `archive/projects/mango/prompts/user-story-generator_exp-2026-05.md`
- [ ] `archive/projects/mango/prompts/user-story-generator_simple-2026-05.md`
- [ ] `archive/projects/mango/standards/classification-glossary.md`

### 2.6. Устаревшие и ненужные файлы

| Artifact | Evidence | Recommendation | Priority |
| --- | --- | --- | --- |
| `archive/projects/mango/` | 17 tracked files, 4 `.gitkeep`; `projects/README.md:63-65` says Mango migrated to `mango_ba_prompts`. | Delete after approval; update references, map and validator in same PR. | P1 |
| Archive `.gitkeep` placeholders | `archive/projects/mango/decisions`, `docs`, `kb` contain only `.gitkeep`; `experiments/.gitkeep` duplicates empty content. | Delete with archive. | P1 |
| Root PR placeholder `.gitkeep` | Auto-generated branch placeholder; structure validator rejects it as unknown tracked file. | Remove in this PR because it is not part of repo state and blocks validation. | Done in this PR |
| `projects/education-ba-prompt/*` missing from `artifact-map.md` | Validator and README include it, map does not. | Add rows or decide it is non-public sandbox and remove from README/validator. | P2 |
| Frontmatter `source: *-old.md` fields | `education/README.md`, `frameworks/README.md`, `projects/README.md`, `research/README.md`, `research/mango/*.md` reference historical paths that no longer exist. | Decide whether historical source references are allowed as non-resolving provenance, or replace with PR/history references. | P2 |

### 2.7. `archive/projects/mango/`

Recommendation: approve full deletion of `archive/projects/mango/`.

Reasoning:

- Mango working assets moved to `https://github.com/G-Ivan-A/mango_ba_prompts`;
- git history preserves the old files;
- current archive creates stale local paths (`projects/mango/...`) and placeholder
  directories;
- validator and artifact map now treat the archive as required, which conflicts
  with the issue decision to remove it;
- keeping both archive and external spoke blurs source of truth.

Deletion is not a standalone `rm -rf`: it must update at least
`README.md`, `projects/README.md`, `governance/artifact-map.md`,
`tools/validate-repository-structure.sh`, and affected research/frontmatter links.

## 3. План Исправлений

### Phase 1: P0/P1, critical consistency

1. Remove `archive/projects/mango/` and update all active references.
2. Resolve naming-contract inconsistency:
   - either rename nested governance CAPS files to kebab-case;
   - or add explicit legacy/governance/template exceptions to `file-naming.md`
     and validator.
3. Fix confirmed stale links and frontmatter relations listed in section 2.4.
4. Merge body-order rules into `research-profile.md` and remove the separate
   draft body-standard.

### Phase 2: P1, validation and metadata

5. Remove body-level duplication of `Версия`, `Дата`, `Статус` where the same
   data is already in frontmatter.
6. Update `governance/artifact-map.md` to reflect actual state, including the
   education project decision.
7. Strengthen validators:
   - nested naming check beyond `standards/`;
   - local link check with allowlist for examples/placeholders;
   - relation-field path check;
   - metadata duplication check;
   - archive absence check after deletion.

### Phase 3: P2, draft lifecycle and cleanup

8. Triage all draft documents by class: approve, keep draft with exit-plan,
   supersede, merge, or delete.
9. Add a small "draft exit-plan" rule to standards for new draft documents.
10. Convert frontmatter warnings into either a documented allowlist or actionable
    failures, especially for template placeholders.
11. Remove empty/placeholder directories that are not part of a documented
    template.

## 4. Порядок Выполнения

| Step | Что сделать | Файлы | Зависимости | Риски | Rollback |
| --- | --- | --- | --- | --- | --- |
| 1 | Approve this RFC and choose archive decision. | This RFC, issue #171 | Human approval | Without decision, cleanup tasks should not start. | Keep RFC draft. |
| 2 | Delete `archive/projects/mango/` and update archive references. | `archive/projects/mango/**`, `README.md`, `projects/README.md`, `governance/artifact-map.md`, `tools/validate-repository-structure.sh`, selected research docs | Step 1 | Broken references if partial. | Revert deletion commit or restore from git history. |
| 3 | Fix stale links and relation values. | Files in section 2.4 | Step 1 | Portal links require scope discipline. | Revert link-only commit. |
| 4 | Resolve naming exception strategy. | `standards/file-naming.md`, validator, possibly renamed governance/template files | Step 1 | Renames touch many links. | Use `git mv` and revert if validation fails. |
| 5 | Resolve research-profile split. | `standards/research-profile.md`, `standards/README.md`, map/validator | Step 1 | Removing a draft too early may lose useful body-order standard. | Restore from git history if review requests a separate standard. |
| 6 | Remove metadata duplication by class. | `standards/**`, then governance/research batches | Steps 2-5 | Review churn across many docs. | Batch commits by directory. |
| 7 | Add validator improvements. | `tools/validate-repository-structure.sh`, possibly `tools/validate-frontmatter.sh` | Steps 2-6 | False positives for examples/templates. | Add explicit allowlist and fixture examples. |
| 8 | Triage drafts. | All files in section 2.5 | Steps 2-7 | Human review capacity. | Keep status draft with exit-plan. |

## 5. Предотвращение Повторов

### 5.1. Validation

Add checks to `tools/validate-repository-structure.sh`:

- `validate_nested_file_naming`: enforce lowercase hyphen names for nested docs,
  with explicit exceptions for root-like template files if approved.
- `validate_markdown_links`: resolve local Markdown links and frontmatter
  relation paths; ignore documented examples and `{{placeholder}}` URLs.
- `validate_metadata_single_source`: warn/fail when `Версия`, `Дата`, `Статус`
  duplicate frontmatter fields in the body.
- `validate_artifact_map_paths`: ensure local paths in `artifact-map.md` exist
  and required files are represented or intentionally excluded.
- `validate_no_archive_mango`: after approval, fail if
  `archive/projects/mango/` reappears.

### 5.2. Contracts

Update contracts after approval:

- `standards/file-naming.md`: add explicit section for governance legacy files
  and template-root files, or require renames.
- `standards/research-profile.md`: own both research metadata/reproducibility and
  body-order rules.
- `standards/contract-documentation-standard.md` and related standards: state
  that metadata lives in frontmatter; body may contain status prose only when it
  adds decision context not already represented by a field.
- Add rule: every new `status: draft` document must contain one of:
  `approval_target`, `supersedes`, `merge_candidate`, or a short "Exit plan"
  section in body.
- Add rule: do not create duplicate documents; update or extend existing
  standard unless the new document has a different responsibility.

### 5.3. CI/CD

Add GitHub Actions after validator improvements:

- run `./tools/validate-frontmatter.sh .`;
- run `./tools/validate-repository-structure.sh`;
- upload validator logs on failure;
- fail PRs on unknown tracked files, broken local links, stale archive paths,
  and forbidden naming patterns.

## 6. Запрос На Согласование

Questions for Founder & PO:

1. Approve this phased plan?
2. Approve Phase 1 execution first, before metadata and draft lifecycle cleanup?
3. Approve full deletion of `archive/projects/mango/`?
4. For nested CAPS governance files, choose one:
   - rename to kebab-case;
   - keep as explicit legacy exception;
   - defer decision.
5. For research body-order rules, confirm the Phase 1 merge into
   `research-profile.md` or request restoration of a separate standard from git
   history.
6. May I create the follow-up issues listed below after approval?

## 7. Задачи Для Создания После Согласования

No follow-up GitHub issues were created by this PR because the issue explicitly
requires approval of the RFC before physical fixes and task decomposition.

| Proposed issue title | Priority | Scope |
| --- | --- | --- |
| `cleanup: remove archive/projects/mango and stale archive references` | P1 | Delete archive, update README/projects/map/validator/research refs. |
| `fix: resolve nested governance file naming exceptions` | P1 | Rename or codify exceptions for uppercase governance/template files. |
| `fix: repair stale local links and frontmatter relations` | P1 | Section 2.4 link and relation issues. |
| `fix: decide research profile vs research documentation standard` | P1 | Keep complementary docs or merge. |
| `fix: remove metadata duplication from standards` | P1 | Remove body `Версия`/`Дата`/duplicate `Статус` from standards. |
| `fix: update artifact map coverage for education project` | P2 | Add rows or remove public registration. |
| `chore: strengthen repository structure validation` | P2 | Naming, link, relation, metadata, archive checks. |
| `governance: triage draft documents and add draft exit-plan rule` | P2 | Review 52 draft documents by class. |

## 8. Definition Of Done For This RFC

- Audit covers naming, duplicates, metadata duplication, traceability, draft
  statuses, obsolete files and Mango archive.
- Each finding has priority and recommendation.
- Phase 1-3 plan exists with order, dependencies, risks and rollback.
- Prevention plan covers validation, contracts and CI/CD.
- Approval questions are explicit.
- Local validators are run in the PR and results are reported.
