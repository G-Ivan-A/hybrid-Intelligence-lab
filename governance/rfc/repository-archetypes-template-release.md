---
status: draft
version: 0.1
updated: 2026-06-15
temperature: 0.1
---

# RFC: Repository Archetypes, Project Template & Release Strategy

## Proposal

Принять лёгкий стандарт проектирования репозиториев экосистемы:

1. Минимальную таксономию архетипов репозиториев, применимую к текущим и будущим
   проектам.
2. Абстрактный Project Template для архетипа **Prompt & Pattern Library**.
3. Универсальное правило синхронизации `governance/` между Хабом и споками.
4. Release Engineering модель: **GitHub Flow + trunk discipline**. `main`
   остаётся production-ready, работа идёт через короткие issue-ветки и PR, а
   production-сборки запускаются только из `main`.

RFC фиксирует стандарт и rationale. Обязательная норма после human decision
должна быть делегирована в active artifact: `templates/`, `standards/`,
`governance/repo-model.md`, Smart Sync metadata или CI templates. До такой
делегации этот документ является draft-рекомендацией
([governance/rfc/README.md](README.md)).

## Decision Scope

- Это **не** план физического рефакторинга `mango_ba_prompts`. Mango используется
  как проверочный пример и источник gaps, но переименования, переносы и cleanup
  относятся к отдельной задаче миграции в самом spoke-репозитории.
- Это **не** полный каталог всех возможных типов репозиториев. Таксономия
  минимальна: она должна классифицировать новый проект без бюрократии.
- Это **не** требование держать пустые директории. Anti-Inflation principle
  сохраняется: каталог появляется только под реальный артефакт
  ([governance/repo-model.md](../repo-model.md)).
- Это **не** решение в пользу долгоживущей `dev`-ветки. Модель ветвления
  выбирается ниже на основе сравнения GitHub Flow, GitFlow и Trunk-Based
  Development.

## Почему текущей ситуации недостаточно

Существующие неформальные договорённости уже перестали быть достаточными.
Экосистема содержит Хаб и несколько разнотипных споков, но слово «проект»
покрывает разные реальности: governance-first Hub, prompt library, product
platform, applied RAG tool и будущие educational/research packages. Без
архетипов новый пятый репозиторий классифицируется по аналогии с ближайшим
текущим примером, а не по критериям.

Формализация нужна именно сейчас, но в лёгкой форме RFC:

| Вопрос | Ответ |
| --- | --- |
| Можно ли обойтись устной договорённостью? | Нет для масштабирования: критерии должны переживать новый чат, нового агента и новый spoke. |
| Нужен ли немедленный жёсткий стандарт? | Нет. Сначала draft RFC и human review; затем делегирование только подтверждённых норм в templates/standards. |
| Что ломается без RFC? | Дублируются каталоги, смешиваются research/template/migration tasks, governance sync трактуется по-разному, а релизная модель выбирается заранее без анализа. |
| Почему не решать только проблемы Mango? | Mango показывает боли, но стандарт должен быть применим к будущим prompt libraries и product spokes. |

Вывод: формализация архетипов, шаблона и release strategy требуется, но должна
быть минимальной и применимой. Этот RFC закрывает уровень Research → RFC; физическая
миграция конкретных репозиториев остаётся отдельной задачей.

## Анализ внешних эталонов структуры

Источники зафиксированы в
[external-sources-registry.md](../../research/external-knowledge/external-sources-registry.md)
(`ext-016`..`ext-020`). Анализ ниже использует только структуру и публичные
описания источников, не копируя их содержимое.

| Эталон | Наблюдение | Что заимствуем | Что не заимствуем |
| --- | --- | --- | --- |
| [LangChain](https://github.com/langchain-ai/langchain) | Framework/library repo с корневым `libs/`, сильной документацией, интеграциями и экосистемой вокруг LangGraph/LangSmith. | Разделение reusable framework/core, integrations, docs/resources; не смешивать библиотеку и прикладные примеры в одном слое. | Не переносим monorepo-масштаб `libs/` в prompt library: для Mango-подобных проектов это избыточно. |
| [CrewAI examples](https://github.com/crewAIInc/crewAI-examples) | Официальная коллекция runnable applications, организованная как `crews/`, `flows/`, `integrations/`, `notebooks/`; каждый пример самостоятельный. | Примеры должны быть runnable, с README/setup и понятной категорией; templates отделяются от feature tutorials. | Не копируем доменные категории CrewAI (`crews`, `flows`) как универсальную таксономию для всех prompt libraries. |
| [Microsoft Foundry samples](https://github.com/microsoft-foundry/foundry-samples) | Top-level каталог официальных samples: `samples/` по языкам/API, `infrastructure/`, `CONTRIBUTING.md`, `SECURITY.md`, tests/config. | Samples отделены от инфраструктуры и contributor/security contracts; сценарии можно группировать по runtime/language. | Не требуем облачную infrastructure-папку для prompt library, пока нет deployable runtime. |
| [Microsoft Foundry AI solution templates](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/ai-template-get-started) | Solution templates дают task-specific code, preintegrated services, GitHub quick-start guides, quick deploy и явное требование проверки поведения. | Template должен ускорять bootstrap, но содержать quickstart, проверку результата, human oversight и production-readiness checklist. | Не делаем vendor-specific Azure template обязательным для всей экосистемы. |
| [Azure get-started-with-ai-chat](https://github.com/Azure-Samples/get-started-with-ai-chat) | Deployable sample с `src/`, `tests/`, `docs/`, `infra/`, `scripts/`, `azure.yaml`. | Для product spoke нужны `src/`, `tests/`, `docs/`, `infra/scripts` и CI как отдельный архетип. | Не смешиваем product-spoke layout с Prompt & Pattern Library, если библиотека не содержит runtime-код. |

**Вывод для Хаба.** Универсальный шаблон должен быть не «одна структура для всех»,
а набор архетипов. Для Prompt & Pattern Library нужно явно разделить
`prompts/`, `patterns/`, `docs/`, `standards/`, `scripts/tools` и
`experiments/evals`, но не требовать `src/` и cloud `infra/` до появления
production runtime.

## Анализ моделей Release Engineering

Источники зафиксированы в реестре как `ext-021`..`ext-024`.

| Модель | Суть | Что заимствуем | Что не подходит |
| --- | --- | --- | --- |
| [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow) | Lightweight branch-based workflow: короткая ветка, commits, PR, review, merge в default branch. | Основной процесс для Хаба и споков: issue branch → PR → checks → human review → merge. Хорошо совпадает с AI-assisted workflow. | Сам по себе не описывает preview/staging для Pages; это нужно добавить через Actions/environment rules. |
| [GitFlow](https://nvie.com/posts/a-successful-git-branching-model/) | Долгоживущие `master` и `develop`, плюс feature/release/hotfix branches. | Полезны понятия release tag/hotfix для зрелого product spoke с версионированными релизами. | Слишком тяжёл для текущего масштаба: постоянная `develop` ветка создаёт overhead и риск дрейфа governance-документов. |
| [Trunk-Based Development](https://trunkbaseddevelopment.com/) | Одна trunk/main ветка, частая интеграция, сопротивление долгоживущим веткам. | Дисциплина маленьких PR, частых merges, `main` как всегда releasable. | Pure direct-to-main не подходит: human review и branch protections остаются обязательными. |
| [GitHub Pages with Actions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) | Pages можно публиковать из branch/folder или кастомным GitHub Actions workflow; deploy step должен быть ограничен default branch. | Production Pages deploy только из `main`; PR builds создают preview artifact/check, но не публикуют в production. | Не используем отдельную `gh-pages` как рабочую dev-ветку; она может быть только generated deploy target, если workflow требует. |

**Выбор.** Для текущей экосистемы подходит **GitHub Flow + trunk discipline**:
одна постоянная production-ready ветка `main`, короткие issue branches, PR как
место review и checks, production deploy только после merge. GitFlow оставляем
как future option для зрелых product spokes с регулярными релизами и поддержкой
нескольких production versions.

## Таксономия архетипов

Минимальный набор архетипов:

| Архетип | Назначение | Критерии отнесения | Обязательные свойства | Внешние эталоны | Текущий маппинг |
| --- | --- | --- | --- | --- | --- |
| **Governance & Knowledge Hub** | Источник методологии, стандартов, шаблонов, practices и ecosystem maps. | Репозиторий управляет правилами для нескольких проектов; product runtime не является главным артефактом. | `governance/`, `standards/`, `templates/`, `tools/`, artifact map, changelog, local validators. | LangChain как ecosystem hub по структуре docs/resources; Microsoft Foundry samples как sample registry. | `hybrid-Intelligence-lab` |
| **Prompt & Pattern Library** | Библиотека исполняемых prompt assets, reusable patterns, domain mappings и проверочных сценариев. | Главная ценность: prompts/patterns для повторяемой работы человека и AI; runtime-код вторичен или отсутствует. | `prompts/`, `patterns/` или обоснованный equivalent, prompt/pattern standards, docs taxonomy/map, validation/self-test, governance sync link. | CrewAI examples, Microsoft templates, LangChain prompt/template ecosystem. | `mango_ba_prompts` |
| **Product Spoke / Application Runtime** | Production или pilot-продукт с кодом, UI/API, тестами, секретами, deploy lifecycle. | Есть `src/`/runtime, CI/CD, production-like environments, отдельные release risks. | `src/`, `tests/`, `docs/`, config, security/deploy guidance, CI, product concept/roadmap, inherited governance. | Azure get-started-with-ai-chat, Microsoft Foundry templates. | `open-ai.ru`, `clarify-engine-ai` |
| **Education / Learning Package** | Учебные материалы, курс, упражнения, demos, методические сценарии. | Главная ценность: передача знания и exercises; production runtime отсутствует или демонстрационный. | Learning README, curriculum/module docs, examples/exercises, source links, governance boundaries. | Microsoft Learn template quickstarts, notebook/example collections. | `projects/education-ba-prompt` как внутренняя область; future standalone repo возможен |

Правило классификации: если репозиторий подходит под несколько архетипов,
выбирается тот, чей **primary value artifact** создаёт ревью и релизные риски.
Например, `clarify-engine-ai` содержит prompts/knowledge base, но primary value
artifact — RAG application runtime, значит это Product Spoke.

## Project Template для Prompt & Pattern Library

Шаблон ниже абстрактный. Он описывает expected roles директорий, а не требует
создавать пустые каталоги.

### Обязательные директории и файлы

| Путь | Назначение | Условие обязательности |
| --- | --- | --- |
| `README.md` | Product/library entrypoint, scope, quickstart, navigation. | Всегда. |
| `AI_GOVERNANCE.md`, `CONTRIBUTING.md`, `CHANGELOG.md` | Inherited HTOM governance, contribution workflow, change history. | Всегда для самостоятельного repo. |
| `governance/artifact-map.md` | Local map of active artifacts and sync state. | Всегда после выделения в standalone repo. |
| `prompts/` | Active prompt assets. `drafts/` and `archive/` are subareas, not root peers. | Если библиотека поставляет prompts. |
| `patterns/` | Reusable patterns/classes of work used by prompts. | Если prompts are pattern-backed. |
| `docs/` | Taxonomy, process map, domain model, hub dependency register, ADR/RFC/audit. | Всегда, если выбор prompt зависит от доменного контекста. |
| `standards/` | Local prompt/pattern contracts and synced/shared standards. | Если validation depends on explicit format rules. |
| `scripts/` or `tools/` | Executable generators, validators, build helpers. | Если есть automation. Выбор имени должен быть единым внутри repo. |
| `tests/` or `experiments/` | Reproducible checks/evals for prompt behavior. | Если качество prompt assets проверяется автоматически или полуавтоматически. |

### Опциональные директории

| Путь | Когда нужен | Ограничение |
| --- | --- | --- |
| `kb/` | Domain examples, reference snippets, reusable context that is not a standard. | Не превращать в research mirror Хаба. |
| `examples/` | Real-world usage cases, sample inputs/outputs, tutorials. | Примеры должны быть runnable/reviewable, не декоративные. |
| `site/` | Static catalog or docs UI generated from source of truth. | Generated data must be reproducible by script. |
| `infra/` | Deployable runtime/infrastructure for catalog or app. | При появлении полноценного runtime проект может стать Product Spoke hybrid. |
| `.github/workflows/` | CI, Pages, validation workflows. | Production deploy only from protected/default branch. |

### Разграничение спорных зон

| Зона | Правило |
| --- | --- |
| `experiments/` vs `prompts/experiments/` | `prompts/experiments/` хранит prompt-specific provenance, self-tests and run artifacts tied to prompt promotion. Root `experiments/` хранит cross-library experiments/evals. Если граница неочевидна, нужен README или index. |
| `scripts/` vs `experiments/` | Исполняемый код проверки/генерации живёт в `scripts/` или `tools/`; experiment stores scenario/results, not reusable automation. |
| `docs/ba-processes/` | Domain-specific process map. Каталог оправдан, если он реально помогает выбрать prompt/pattern; пустой placeholder недопустим. |
| `governance/` | Общие правила синхронизируются из Хаба; local backlog, migration manifest, decisions and artifact map are local extensions. |

## Маппинг mango_ba_prompts

Снимок проверен по GitHub API на 2026-06-15:
[`mango_ba_prompts`](https://github.com/G-Ivan-A/mango_ba_prompts) содержит
`prompts/`, `patterns/`, `docs/`, `governance/`, `kb/`, `standards/`, `scripts/`,
`site/`, root `experiments/` и `prompts/experiments/`.

| Элемент Mango | Соответствие шаблону | Комментарий |
| --- | --- | --- |
| `prompts/` | Соответствует | Active prompt assets, drafts/archive/experiments are colocated with prompts. |
| `patterns/` | Соответствует | Pattern layer exists; content depth is a project question, not RFC scope. |
| `docs/taxonomy.md`, `docs/ba-ecosystem.md` | Соответствует | Domain taxonomy and map support prompt selection. |
| `docs/ba-processes/00-index.md` | Соответствует | Current state is not an empty placeholder; it is the process-to-prompt index. Completeness across all BA processes is a local review task. |
| `docs/hub-research-dependencies.md` | Соответствует | Good boundary: Hub research is linked through one register, not copied. |
| `standards/` | Соответствует with sync caveat | Local prompt/pattern standards are valid; synced general standards need source-of-truth notes. |
| `scripts/generate-pages-data.mjs` and `site/` | Соответствует | Static catalog is generated from markdown source of truth. |
| `governance/` | Соответствует with split | Local backlog/manifest/session digests are local; inherited governance files need sync provenance. |
| Root `experiments/` plus `prompts/experiments/` | Gap / ambiguity | This RFC does not prescribe moves. It flags the need for a local boundary: root experiments should be cross-library evals; prompt-specific scenarios should stay under `prompts/experiments/`. Existing `validate_issue_*.py` files look more like validation scripts/tests than experiments. |

Вывод: предложенный шаблон выдерживает проверку Mango. Главный gap — не наличие
обеих experiment-зон само по себе, а отсутствие явной границы между
cross-library experiments, prompt-specific self-tests and reusable validation
automation. Это должно стать входом для отдельного Migration Plan в
`mango_ba_prompts`, а не правкой из Хаба.

## Правило синхронизации Governance

Для всех standalone HTOM/spoke репозиториев вводится правило **Base Governance
from Hub + Local Extension in project**.

### Строго синхронизируемые из Хаба

| Группа | Источник истины | Правило |
| --- | --- | --- |
| HTOM genome | `templates/htom/` in Hub | `AI_GOVERNANCE.md`, quick rules, handover/onboarding prompts and base CONTRIBUTING patterns sync through Smart Sync or reviewed manual copy. |
| Shared standards | `standards/` in Hub | Frontmatter, file naming, issue workflow, executable documentation and other cross-project standards are Hub-owned unless explicitly forked. |
| Issue/PR intake | `.github/ISSUE_TEMPLATE/` in Hub | Projects may adapt labels/text, but structural changes to common workflow originate in Hub. |
| Sync tooling metadata | `templates/manifest.json`, `templates/sync-metadata.json`, `tools/sync-from-hub.sh` | Hub controls the sync protocol; projects keep local profile and acceptance history. |

### Локальные расширения спока

| Группа | Где живёт | Правило |
| --- | --- | --- |
| Local backlog and open questions | `governance/backlog.md` or project equivalent | Owned by project; not overwritten from Hub. |
| Local artifact map | `governance/artifact-map.md` | Uses Hub format, but entries describe local artifacts and sync snapshot. |
| Migration manifests and project decisions | `governance/`, `docs/adr/`, `docs/rfc/` | Owned by project; may link to Hub RFCs. |
| Domain standards | `standards/` in project | Allowed when domain-specific. Must state whether it is local, synced, or forked from Hub. |

### Механизм синхронизации

1. Default path: Smart Sync
   ([guides/sync-from-hub.md](../../guides/sync-from-hub.md),
   [tools/sync-from-hub.sh](../../tools/sync-from-hub.sh)).
2. If Smart Sync does not cover an artifact yet: manual PR with source Hub SHA,
   diff review and CHANGELOG entry in the project.
3. No silent overwrite: local extensions are never replaced by Hub text without
   human review.
4. Drift is not always a bug: a spoke may keep a local fork, but must record
   rationale and source version.

## Release Engineering Strategy

### Branching model

Use **GitHub Flow + trunk discipline**:

- `main` is the only permanent production-ready branch.
- Work happens in short issue branches, e.g. `issue-240-...`.
- Every change goes through PR with local validation, CI and human review.
- Draft or experimental work stays in PR branches, not in a shared `dev` branch.
- Tags/releases are optional and belong to mature Product Spokes; they do not
  require GitFlow by default.

### CI/CD для GitHub Pages и web resources

| Stage | Trigger | Result | Production risk |
| --- | --- | --- | --- |
| PR validation | `pull_request` | Lint/test/build, upload preview artifact or comment link if configured. | No production deploy. |
| Main deploy | `push` to `main` | Build static site and deploy to `github-pages` environment. | Controlled by branch protection and environment rules. |
| Manual rebuild | `workflow_dispatch` by maintainer | Rebuild current approved state. | Allowed for recovery/audit. |

Draft isolation is provided by branches and PR checks. Production isolation is
provided by `if: github.ref == 'refs/heads/main'` on deploy jobs and the
`github-pages` environment.

Example workflow fragment:

```yaml
name: pages

on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        with:
          path: dist

  deploy:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
    steps:
      - uses: actions/deploy-pages@v4
```

For repositories that use Python/MkDocs, replace the Node build steps with the
existing pattern from
[.github/workflows/deploy-docs.yml](../../.github/workflows/deploy-docs.yml).
For generic product spokes, start from
[templates/spoke/.github/workflows/ci.yml](../../templates/spoke/.github/workflows/ci.yml)
and add deploy only after product readiness is explicit.

## Acceptance Criteria

- Раздел «Почему текущей ситуации недостаточно» добавлен.
- Проанализированы внешние AI/template эталоны: LangChain, CrewAI examples,
  Microsoft Foundry samples/templates and Azure AI chat sample.
- Проанализированы GitHub Flow, GitFlow, Trunk-Based Development and GitHub
  Pages Actions deployment.
- Определена минимальная таксономия архетипов с критериями, обязательными
  свойствами, примерами и текущим маппингом.
- Предложен абстрактный Project Template для Prompt & Pattern Library.
- Mango mapped as illustrative validation; gaps identified without migration
  instructions.
- Governance sync rule defined as Hub base + local extension.
- Release strategy selected and CI/CD workflow example provided.

## Open Decision

1. После review повысить этот RFC в standard/template work или оставить как
   reference-RFC до первого применения в новом репозитории?
2. Создавать ли отдельный `templates/prompt-pattern-library/` после принятия
   RFC, или сначала провести Migration Plan в `mango_ba_prompts`?
3. Нужны ли preview URLs для PR Pages builds в текущем масштабе, или достаточно
   build artifact + screenshot/manual verification?
4. Должен ли Smart Sync явно проверять forked/synced status of governance files
   in spokes?

## Связанные артефакты

- [governance/repo-model.md](../repo-model.md) — Anti-Inflation principle and
  repository structure rules.
- [governance/rfc/documentation-architecture-balance.md](documentation-architecture-balance.md)
  — Index/Summary/Full and lazy loading framework.
- [governance/rfc/htom-vs-spoke-clarification-2026-06.md](htom-vs-spoke-clarification-2026-06.md)
  — HTOM vs spoke distinction.
- [docs/ecosystem-map-Index.md](../../docs/ecosystem-map-Index.md) — current
  ecosystem project map.
- [research/external-knowledge/external-sources-registry.md](../../research/external-knowledge/external-sources-registry.md)
  — registered external sources `ext-016`..`ext-024`.
- [guides/sync-from-hub.md](../../guides/sync-from-hub.md) — Smart Sync guide.
