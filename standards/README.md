---
status: accepted
version: 1.10
updated: 2026-07-03
temperature: 0.1
owner: G-Ivan-A
---

# Standards

Каталог является плоским реестром активных и планируемых стандартов. Более
глубокая структура добавляется только после повторяющегося использования, когда
плоский реестр становится операционно неудобным.

## Реестр

| Стандарт | Статус | Где применяется | Источник |
| --- | --- | --- | --- |
| Единый глоссарий терминов | Active | Issues, standards, governance, AI-assisted work | [standards/glossary.md](glossary.md) |
| File naming convention | Active | Правило именования файлов, включая date-first research/analysis/audit/report/RFC/ADR артефакты | [standards/file-naming.md](file-naming.md), [standards/file-naming-convention.md](file-naming-convention.md) |
| Education project profile | Active | `education/{course}/`, course materials, workshops и учебная документация | [standards/education-profile.md](education-profile.md) |
| Концепция репозитория | Active | Root concept и назначение репозитория | [CONCEPT.md](../CONCEPT.md) |
| AI governance contract | Active | AI-assisted issues, PRs и reviews | [AI_GOVERNANCE.md](../AI_GOVERNANCE.md) |
| Repository model | Active | Размещение артефактов и правила создания | [governance/repo-model.md](../governance/repo-model.md) |
| Frontmatter standard | Canonical | Минимальное metadata rule для Markdown-артефактов и шаблонов | [frontmatter-standard.md](frontmatter-standard.md) |
| Frontmatter docs standard | Canonical | Necessary and sufficient frontmatter по классам документов: Standard, Guide, RFC, ADR, Research/report, Audit, Template, Practice | [frontmatter-docs-standard.md](frontmatter-docs-standard.md) |
| ADR structure standard | Active | Единая структура ADR: frontmatter, stable id, required body sections, lifecycle, section-level delegation, archetype deltas and Boundary RFC/ADR | [adr-structure-standard.md](adr-structure-standard.md) |
| RFC structure standard | Active | Единая структура RFC-like документов: frontmatter, metadata, required body sections, Research→RFC delegation, lifecycle, Open Questions and Boundary RFC/ADR | [rfc-structure-standard.md](rfc-structure-standard.md) |
| Knowledge lifecycle | Draft RFC (предложен на утверждение) | Переходы Observation -> Research -> Hypothesis -> RFC -> Pattern -> Standard -> Template -> Framework -> Deprecation/Archive | [../governance/rfc/knowledge-lifecycle-proposal.md](../governance/rfc/knowledge-lifecycle-proposal.md) |
| Research structure standard | Active | `research/<domain>/`: размещение отчётов, контейнер `exp/`, запрет `outputs/`, routing Research / Analysis / Audit и граница `exp/` vs `runs/` | [research-standard.md](research-standard.md) |
| Report standard | Draft (предложен на утверждение) | `docs/report/` и `docs/audit/`: базовый каркас Report, профили `audit`/`report`/`statistics`, relation-frontmatter, routing split, knowledge-lifecycle и границы Reports ↔ Analysis ↔ Audit ↔ Research evidence | [report-standard.md](report-standard.md) |
| Audit standard | Draft (предложен на утверждение) | `docs/audit/`: базовый каркас Audit, 4-компонентная модель (target/evidence/verdict/deviation), audit-specific frontmatter, разграничение Audit-процесс vs audit-report output, knowledge-lifecycle и границы Audit ↔ Research ↔ Analysis ↔ Report | [audit-standard.md](audit-standard.md) |
| Analysis standard | Draft (предложен на утверждение) | `docs/analysis/`: базовый каркас Analysis (interpretation layer), опциональные профили `inventory`/`matrix`/`options`/`recommendation`, relation-frontmatter (`analysis-subtype`/`source`/`scope`/`based_on`/`related_artifacts`), routing `docs/analysis/`, knowledge-lifecycle, триггер B (anti-inflation) и границы Analysis ↔ Research ↔ Audit ↔ Report ↔ RFC ↔ ADR | [analysis-standard.md](analysis-standard.md) |
| Product profile | Active | Продуктовые spoke-проекты (ПО, сервис, услуга) | [product-profile.md](product-profile.md) |
| Team contract template | Active | Создание project-level `CONTRIBUTING.md` и `AI_GOVERNANCE.md` для spoke-проектов | [team-contract.md](team-contract.md) |
| Жизненный цикл задач | Active | Issues, PRs, переходы статусов, AI-assisted task execution | [issue-workflow.md](issue-workflow.md) |
| Session handover prompt | Draft (предложен на утверждение) | `AI_SESSION_HANDOVER_PROMPT.md`: передача контекста между чатами и запуск Runtime-онбординга | [session-handover-standard.md](session-handover-standard.md) |
| project-structure-inheritance.md | Active | Правило наследования структуры каталогов в проектах; обязательно для новых проектов | [project-structure-inheritance.md](project-structure-inheritance.md) |
| executable-contract-standard.md | Canonical | Формат исполнимых контрактов (`executable: true`): директива → EXECUTION → EXPLANATION | [executable-contract-standard.md](executable-contract-standard.md) |
| executable-documentation-standard.md | Canonical | Разделение descriptive/executable docs, атомизация practice graph и правила импорта практик | [executable-documentation-standard.md](executable-documentation-standard.md) |
| contract-documentation-standard.md | Canonical | Формат прочих контрактов (обязательства сверху, обоснование под катом; нормативный словарь RFC 2119) | [contract-documentation-standard.md](contract-documentation-standard.md) |
| htom-documentation-structure.md | Canonical | Стандарт структуры `docs/` для HTOM-репозиториев и разбор Mango docs error pattern | [htom-documentation-structure.md](htom-documentation-structure.md) |
| webportal-product-concept-standard.md | Draft (L2, предложен на утверждение) | Product Concept веб-портала: personas, jobs-to-be-done, MVP scope, user flows, success metrics и high-level roadmap | [webportal-product-concept-standard.md](webportal-product-concept-standard.md) |
| webportal-solution-concept-standard.md | Draft (L3, предложен на утверждение) | Solution Concept веб-портала: C4 architecture, technology stack, integrations, data model, NFR, deployment и risks | [webportal-solution-concept-standard.md](webportal-solution-concept-standard.md) |
| Research report | Planned | `research/<domain>/` | Создать после повторяющихся research tasks. |
| Framework proposal | Planned | `frameworks/` | Создать после documented framework gap. |
| Project knowledge base | Planned | `projects/` | Создать после повторяющейся потребности в project context. |
| Artifact location resolver | Draft RFC (предложен на утверждение) | Выбор каталога и lifecycle stage для нового артефакта | [../governance/rfc/resolve-artifact-location-proposal.md](../governance/rfc/resolve-artifact-location-proposal.md) |

## Как пользоваться

1. Определите тип артефакта и целевой каталог по
   [governance/repo-model.md](../governance/repo-model.md). Для навигации по
   существующим артефактам и их связям используйте
   [governance/artifact-map.md](../governance/artifact-map.md).
2. Выберите имя файла или каталога по
   [standards/file-naming.md](file-naming.md); compatibility entry для
   date-first правила — [standards/file-naming-convention.md](file-naming-convention.md).
3. Проверьте терминологию по [standards/glossary.md](glossary.md), если
   документ вводит governance, lifecycle или AI-assisted work terms.
4. Для образовательных материалов используйте
   [standards/education-profile.md](education-profile.md) до создания курса,
   воркшопа или учебной документации.
5. Используйте active standard из таблицы, если он уже есть.
6. Если standard planned, но еще не active, держите артефакт минимальным и
   объясните gap в issue или PR.
7. Не добавляйте новый standard только потому, что документ можно
   стандартизировать. Добавляйте его, когда повторяющаяся работа создает
   реальную coordination или review problem.
8. Ссылайтесь на новый active standard из этой таблицы и ближайшего README или
   governance document.
