# Standards

Каталог является плоским реестром активных и планируемых стандартов. Более
глубокая структура добавляется только после повторяющегося использования, когда
плоский реестр становится операционно неудобным.

## Реестр

| Стандарт | Статус | Где применяется | Источник |
| --- | --- | --- | --- |
| Единый глоссарий терминов | Active | Issues, standards, governance, AI-assisted work | [standards/glossary.md](glossary.md) |
| `file-naming.md` | Active | Правило именования файлов, обязательно для всех новых файлов | [standards/file-naming.md](file-naming.md) |
| Education project profile | Active | `education/{course}/`, course materials, workshops и учебная документация | [standards/education-profile.md](education-profile.md) |
| Концепция репозитория | Active | Root concept и назначение репозитория | [CONCEPT.md](../CONCEPT.md) |
| AI governance contract | Active | AI-assisted issues, PRs и reviews | [AI_GOVERNANCE.md](../AI_GOVERNANCE.md) |
| Repository model | Active | Размещение артефактов и правила создания | [governance/repo-model.md](../governance/repo-model.md) |
| Профиль исследовательских проектов | Active | `research/<domain>/` | [research-profile.md](research-profile.md) |
| Product profile | Active | Продуктовые spoke-проекты (ПО, сервис, услуга) | [product-profile.md](product-profile.md) |
| Team contract template | Active | Создание project-level `CONTRIBUTING.md` и `AI_GOVERNANCE.md` для spoke-проектов | [team-contract.md](team-contract.md) |
| Жизненный цикл задач | Active | Issues, PRs, переходы статусов, AI-assisted task execution | [issue-workflow.md](issue-workflow.md) |
| project-structure-inheritance.md | Active | Правило наследования структуры каталогов в проектах; обязательно для новых проектов | [project-structure-inheritance.md](project-structure-inheritance.md) |
| executable-contract-standard.md | Canonical | Формат исполнимых контрактов (`executable: true`): директива → EXECUTION → EXPLANATION | [executable-contract-standard.md](executable-contract-standard.md) |
| contract-documentation-standard.md | Canonical | Формат прочих контрактов (обязательства сверху, обоснование под катом; нормативный словарь RFC 2119) | [contract-documentation-standard.md](contract-documentation-standard.md) |
| webportal-product-concept-standard.md | Draft (L2, предложен на утверждение) | Product Concept веб-портала: personas, jobs-to-be-done, MVP scope, user flows, success metrics и high-level roadmap | [webportal-product-concept-standard.md](webportal-product-concept-standard.md) |
| webportal-solution-concept-standard.md | Draft (L3, предложен на утверждение) | Solution Concept веб-портала: C4 architecture, technology stack, integrations, data model, NFR, deployment и risks | [webportal-solution-concept-standard.md](webportal-solution-concept-standard.md) |
| Research report | Planned | `research/<domain>/` | Создать после повторяющихся research tasks. |
| Framework proposal | Planned | `frameworks/` | Создать после documented framework gap. |
| Project knowledge base | Planned | `projects/` | Создать после повторяющейся потребности в project context. |
| Artifact lifecycle | Planned | Все reviewed artifacts | Создать, когда maturity states станут операционно необходимы. |

## Как пользоваться

1. Определите тип артефакта и целевой каталог по
   [governance/repo-model.md](../governance/repo-model.md). Для навигации по
   существующим артефактам и их связям используйте
   [governance/artifact-map.md](../governance/artifact-map.md).
2. Выберите имя файла или каталога по
   [standards/file-naming.md](file-naming.md).
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
