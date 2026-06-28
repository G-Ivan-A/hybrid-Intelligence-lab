---
status: draft
version: 0.1
updated: 2026-06-28
temperature: 0.1
---

# Research/Analysis/Audit artifact classification matrix

Generated for issue #288. Classification is heuristic and evidence-oriented:
path is only a signal; title, frontmatter and early content are used to detect
audit/report/research/proposal signals. The written research report performs
the final human-readable synthesis. The issue #288 report and experiment
directory are excluded from the Hub scan so reruns preserve the baseline.

## Repository snapshots

| Repo | URL | SHA |
| --- | --- | --- |
| Hub / hybrid-Intelligence-lab | https://github.com/G-Ivan-A/hybrid-Intelligence-lab | `1a2a9cdfb37ab7e689b143d94623923ade65e33a` |
| Mango / mango_ba_prompts | https://github.com/G-Ivan-A/mango_ba_prompts | `ed636a38a762e848907fcaf607fecf764dcbb9c8` |
| Clarify / clarify-engine-ai | https://github.com/G-Ivan-A/clarify-engine-ai | `96c288fd13a2d7cc7c3e3cdd52574944858e6255` |

## Summary

| Repo | Research | Analysis | Audit | Other | Total text artifacts | Non-text docs artifacts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Hub / hybrid-Intelligence-lab | 42 | 3 | 6 | 21 | 72 | 7 |
| Mango / mango_ba_prompts | 10 | 3 | 11 | 28 | 52 | 19 |
| Clarify / clarify-engine-ai | 12 | 11 | 7 | 40 | 70 | 15 |

## Hub / hybrid-Intelligence-lab

| Path | Bucket | Actual type | Subtype | Source signal | Title |
| --- | --- | --- | --- | --- | --- |
| `docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md` | `docs` | Other | decision-record | `accepted` | ADR-001: Методология инфраструктуры проектов экосистемы |
| `docs/adr/2026-06-adr-002-artifact-document-methodology.md` | `docs` | Other | decision-record | `accepted` | ADR-002: Методология создания и управления артефактами |
| `docs/audit/task-execution-audit-2026-06.md` | `docs/audit` | Audit | conformance-check | `draft` | Аудит выполненных задач (1-4) |
| `docs/ecosystem-map-Index.md` | `docs` | Other | reference-or-concept | `draft` | Экосистемная карта — Index |
| `docs/ecosystem-map.md` | `docs` | Other | reference-or-concept | `draft` | Экосистемная карта Хаба |
| `docs/product-concept.md` | `docs` | Other | reference-or-concept | `draft` | Product Concept |
| `docs/project-summaries/README.md` | `docs` | Other | navigation | `draft` | Project Summaries (hub-side staging) |
| `docs/project-summaries/clarify-engine-ai-context-Summary.md` | `docs` | Analysis | local-context-analysis | `draft` | Контекст проекта clarify-engine-ai (Summary) |
| `docs/project-summaries/mango-ba-prompts-context-Summary.md` | `docs` | Analysis | local-context-analysis | `draft` | Контекст проекта mango_ba_prompts (Summary) |
| `docs/project-summaries/open-ai-ru-context-Summary.md` | `docs` | Analysis | local-context-analysis | `draft` | Контекст проекта open-ai.ru (Summary) |
| `docs/vision.md` | `docs` | Other | reference-or-concept | `draft` | Product Vision |
| `research/README.md` | `research` | Other | navigation | `canonical` | Research |
| `research/cicd/2026-06-09-js-cicd-template-analysis.md` | `research` | Research | knowledge-generation | `external-analysis` | Исследование: JS CI/CD Template — Анализ шаблона link-foundation |
| `research/cicd/README.md` | `research` | Other | navigation | `canonical` | Research: CI/CD |
| `research/external-knowledge/2026-06-18-wigers-requirements-analysis.md` | `research` | Research | knowledge-generation | `external-analysis` | Исследование: требования к ПО по Вигерсу с актуализацией на AI-тренды 2026 |
| `research/external-knowledge/README.md` | `research` | Other | navigation | `draft` | Research: External Knowledge |
| `research/external-knowledge/external-insights/2026-06-13-12-factor-agents.md` | `research` | Research | knowledge-generation | `external-analysis` | Инсайт: владей промптами и контекстом как кодом, держи человека в петле |
| `research/external-knowledge/external-insights/2026-06-13-building-effective-agents.md` | `research` | Research | knowledge-generation | `external-analysis` | Инсайт: простые компонуемые паттерны > монолитные «умные» агенты |
| `research/external-knowledge/external-insights/2026-06-13-spec-driven-development.md` | `research` | Research | knowledge-generation | `external-analysis` | Инсайт: спецификация как исполнимый артефакт между требованием и кодом |
| `research/external-knowledge/external-insights/2026-06-15-agent-local-memory-context.md` | `research` | Research | knowledge-generation | `external-analysis` | Инсайт: локальная память проекта снимает нагрузку с контекстного окна |
| `research/external-knowledge/external-insights/2026-06-15-structured-prompt-driven-development.md` | `research` | Research | knowledge-generation | `external-analysis` | Инсайт: промпт как версионируемый артефакт, а не одноразовая команда |
| `research/external-knowledge/external-insights/README.md` | `research` | Other | navigation | `draft` | External Insights |
| `research/external-knowledge/external-sources-registry.md` | `research` | Research | knowledge-generation | `external-analysis` | Реестр внешних источников |
| `research/governance/2026-06-06-contract-documentation-format.md` | `research` | Research | knowledge-generation | `external-analysis` | Исследование: оптимальный формат прочих контрактов |
| `research/governance/2026-06-06-executable-contract-format.md` | `research` | Research | knowledge-generation | `external-analysis` | Исследование: оптимальный формат исполнимых контрактов |
| `research/governance/2026-06-06-governance-folder-structure-decisions.md` | `research` | Other | decision-record | `decision-record` | Решения по структуре governance-каталогов (Q1, Q2, Q3) |
| `research/governance/2026-06-06-research-documentation-format.md` | `research` | Research | knowledge-generation | `external-analysis` | Исследование: оптимальный формат исследований Хаба |
| `research/governance/README.md` | `research` | Other | navigation | `navigation` | Research: Governance (форматы и эволюция Хаба) |
| `research/hub/2026-05-28-project-context-and-bootstrap-patterns.md` | `research` | Research | knowledge-generation | `internal-analysis` | Как передавать контекст и создавать проекты предсказуемо |
| `research/hub/2026-05-28-prompts-classification-audit.md` | `research` | Audit | conformance-check | `internal-analysis` | Аудит входных данных для классификации промптов |
| `research/hub/2026-05-28-prompts-classification-standard.md` | `research` | Other | standard | `classification-standard` | Стандарт классификации промптов |
| `research/hub/2026-05-28-user-prompts-analysis.md` | `research` | Research | knowledge-generation | `prompt-analysis` | Анализ пользовательских промптов |
| `research/hub/2026-06-01-team-c-governance-strategy-audit.md` | `research` | Audit | conformance-check | `internal-analysis` | Интерпретация аудита стратегии governance от команды C |
| `research/hub/2026-06-02-ai-collaboration-retrospective-mango-migration.md` | `research` | Research | knowledge-generation | `canonical` | Ретроспектива AI-collaboration: сессия проектирования миграции Mango (Хаб → спок) |
| `research/hub/2026-06-02-ai-collaboration-retrospective.md` | `research` | Research | knowledge-generation | `canonical` | Ретроспектива AI-collaboration по сессии проектирования шаблонов споков |
| `research/hub/2026-06-02-external-governance-patterns-review.md` | `research` | Research | knowledge-generation | `external-analysis` | Анализ external governance patterns и матрица применимости для Хаба |
| `research/hub/2026-06-12-ecosystem-governance-audit.md` | `research` | Audit | conformance-check | `internal-analysis` | Ecosystem Governance Audit |
| `research/hub/2026-06-12-external-practice-intake.md` | `research` | Research | knowledge-generation | `draft` | External Practice Intake: Agent Work And HTOM Docs |
| `research/hub/2026-06-12-international-ai-governance-practices.md` | `research` | Research | knowledge-generation | `draft` | International AI Governance Practices |
| `research/hub/2026-06-20-ecosystem-architecture-research.md` | `research` | Research | knowledge-generation | `ecosystem-architecture-research` | Комплексное исследование архитектуры экосистемы: Hub, open-ai.ru, репутационные технологии |
| `research/hub/2026-06-23-repository-structure-concept.md` | `research` | Research | knowledge-generation | `repository-structure-concept-research` | Концепция базовых каталогов для архетипов проектов (дополнение к mango-исследованию) |
| `research/hub/2026-06-25-artifact-inventory-and-classification.md` | `research` | Research | knowledge-generation | `artifact-inventory-and-classification-research` | Инвентаризация и классификация артефактов экосистемы (mango_ba_prompts + hybrid-Intelligence-lab) |
| `research/hub/2026-06-27-adr-industry-norms-and-variants.md` | `research` | Research | knowledge-generation | `adr-industry-norms-and-variants-research` | ADR: индустриальные нормы, дельты и варианты для Hub / Mango |
| `research/hub/2026-06-27-rfc-industry-norms-and-variants.md` | `research` | Research | proposal-adjacent-research | `rfc-industry-norms-and-variants-research` | RFC: индустриальные нормы, дельты и варианты для Hub / Mango |
| `research/hub/2026-06-28-ripple-effects-282-research.md` | `research` | Research | knowledge-generation | `internal-analysis` | Исследование: Ripple Effects issue 282 |
| `research/hub/README.md` | `research` | Other | navigation | `canonical` | Research: Hub |
| `research/hub/exp-rfc-adr-industry-norms/README.md` | `research` | Other | navigation | `experiment` | Experiment: RFC/ADR industry norms evidence |
| `research/hub/exp-rfc-adr-industry-norms/outputs/2026-06-27-adr-external-tree-summary.md` | `research` | Research | knowledge-generation | `adr-external-tree-summary` | ADR external source tree summary |
| `research/hub/exp-rfc-adr-industry-norms/outputs/2026-06-27-local-rfc-adr-audit.md` | `research` | Audit | conformance-check | `local-rfc-adr-audit` | Local ecosystem RFC/ADR audit |
| `research/hub/exp-rfc-adr-industry-norms/outputs/2026-06-27-rfc-external-tree-summary.md` | `research` | Research | proposal-adjacent-research | `rfc-external-tree-summary` | RFC external source tree summary |
| `research/hub/exp-ripple-effects-282/README.md` | `research` | Other | navigation | `experiment` | Experiment: Ripple effects 282 frontmatter scan |
| `research/hub/exp-ripple-effects-282/outputs/2026-06-28-frontmatter-scan.md` | `research` | Research | knowledge-generation | `draft` | Frontmatter scan for issue 284 |
| `research/mango/2026-05-22-classification-tz.md` | `research` | Research | knowledge-generation | `internal-analysis` | Классификация требований по корпусу ТЗ (classification (TZ)) |
| `research/mango/2026-05-22-classification.md` | `research` | Research | knowledge-generation | `external-analysis` | Классификация IT/Telecom SaaS-продуктов MANGO OFFICE |
| `research/mango/2026-05-22-requirements-flow.md` | `research` | Research | knowledge-generation | `internal-analysis` | Flow требований для AI-анализа тендерных ТЗ MANGO OFFICE |
| `research/mango/2026-05-26-rag-mapping-roadmap.md` | `research` | Research | knowledge-generation | `process-research` | Маппинг продуктов/фич Mango как RAG-навигатор и roadmap автоматизации БА |
| `research/mango/2026-05-26-requirements-lifecycle-uncertainty.md` | `research` | Research | knowledge-generation | `process-research` | Жизненный цикл требования Mango: неопределенность, декомпозиция и международная практика |
| `research/mango/2026-05-26-taxonomy-concept.md` | `research` | Research | knowledge-generation | `concept-proposal` | Концепция Единой таксономии функциональности Mango |
| `research/mango/2026-05-27-capability-decomposition.md` | `research` | Audit | conformance-check | `atomic-functions-reference` | Fixed per draft-triage RFC Phase 1: local relations use path-only values; |
| `research/mango/2026-06-18-ai-classifications-formalization.md` | `research` | Research | knowledge-generation | `draft` | Формализация AI-классификаций и интеграция в роадмап Mango |
| `research/mango/2026-06-18-requirements-engineering-ai-era.md` | `research` | Research | proposal-adjacent-research | `draft` | RFC: Requirements Engineering in the AI Era — синхронизация Вигерса и mango-ADR |
| `research/mango/2026-06-19-repository-structure-vision.md` | `research` | Research | proposal-adjacent-research | `draft` | RFC: Независимое видение структуры репозитория(ев) `mango_ba_prompts` (ИБ, внешнее хранилище, экосистема) / Independent Vision of `mango_ba_prompts` Repository Structure |
| `research/mango/2026-06-19-token-optimization-proposal.md` | `research` | Other | proposal | `draft` | RFC: Оптимизация потребления токенов при работе AI с репозиторием `mango_ba_prompts` / Token Consumption Optimization for AI Working with the `mango_ba_prompts` Repository |
| `research/mango/README.md` | `research` | Other | navigation | `canonical` | Research: MANGO OFFICE |
| `research/open-ai-ru/2026-06-20-open-ai-ru-repository-architecture-and-l3-l4.md` | `research` | Research | knowledge-generation | `internal-analysis` | Архитектура репозитория open-ai.ru и разработка уровней L3–L4 на основе международных практик |
| `research/open-ai-ru/README.md` | `research` | Other | navigation | `canonical` | Research: open-ai.ru |
| `research/reputation-technologies/2026-06-20-executive-summary.ru-en.md` | `research` | Research | knowledge-generation | `external-analysis` | Executive Summary — GRA Reputation Framework (RU + EN) |
| `research/reputation-technologies/2026-06-20-founders-vision-and-framework.ru.md` | `research` | Research | knowledge-generation | `external-analysis` | Репутационные технологии: от видения фаундера к международному стандарту GRA |
| `research/reputation-technologies/2026-06-20-framework-standard.en.md` | `research` | Research | knowledge-generation | `external-analysis` | GRA Framework Standard — Draft (International Format) |
| `research/reputation-technologies/2026-06-20-glossary.ru-en.md` | `research` | Research | knowledge-generation | `external-analysis` | GRA Terminology Dictionary / Терминологический словарь (RU ↔ EN) |
| `research/reputation-technologies/2026-06-20-white-paper.en.md` | `research` | Research | knowledge-generation | `external-analysis` | GRA — A Graph-Native, Cross-Level Standard for Reputation Engineering (White Paper) |
| `research/reputation-technologies/README.md` | `research` | Other | navigation | `draft` | Research: Reputation Technologies (GRA) |

## Mango / mango_ba_prompts

| Path | Bucket | Actual type | Subtype | Source signal | Title |
| --- | --- | --- | --- | --- | --- |
| `docs/adr/0001-hub-sync-pr208.md` | `docs` | Other | decision-record | `adr` | ADR-0001: Синхронизация governance-файлов с Хабом после PR #208 |
| `docs/adr/0002-issue48-handover-local-enrichment.md` | `docs` | Other | decision-record | `adr` | ADR-0002: Локальное обогащение `AI_SESSION_HANDOVER_PROMPT.md` (issue #48) |
| `docs/adr/0003-creative-mode-governance.md` | `docs` | Other | decision-record | `adr` | ADR-0003: Creative-mode governance без архитектурного долга |
| `docs/adr/001-prompt-standard.md` | `docs` | Other | decision-record | `adr` | ADR-001: Стандарт промптов `mango_ba_prompts` |
| `docs/adr/002-pattern-standard.md` | `docs` | Other | decision-record | `adr` | ADR-002: Стандарт паттернов бизнес-анализа |
| `docs/adr/003-ba-ontology.md` | `docs` | Other | decision-record | `adr` | ADR-003: Онтология бизнес-анализа (Артефакт ↔ Процесс ↔ Операция) |
| `docs/adr/004-operations-taxonomy.md` | `docs` | Other | decision-record | `adr` | ADR-004: Ревизия таксономии операций и маппинг на BABOK / ISO / ГОСТ |
| `docs/adr/005-artifact-team-naming.md` | `docs` | Other | decision-record | `adr` | ADR-005: Стандарт нейминга артефактов, стандартов и команд (Team Directory) |
| `docs/adr/006-prompt-naming.md` | `docs` | Other | decision-record | `adr` | ADR-006: Стандарт нейминга промптов (подтверждение схемы, запрет перегрузки, KB-промпты) |
| `docs/adr/007-kb-standard.md` | `docs` | Other | decision-record | `adr` | ADR-007: Стандарт базы знаний (KB) до настоящего RAG — формат цитирования, синхронизация с глоссарием, pre-RAG механизм |
| `docs/adr/008-industry-standards-standard.md` | `docs` | Other | decision-record | `adr` | ADR-008: Стандарт отраслевых стандартов и best practices — терминология, правила применения, верификация источников |
| `docs/adr/009-bcreq-formation-process.md` | `docs` | Other | decision-record | `adr` | ADR-009: Многоуровневый процесс формирования BCREQ — подпроцессы, human gates, механизм незавершённых подпроцессов |
| `docs/adr/010-pages-ux.md` | `docs` | Other | decision-record | `adr` | ADR-010: UX GitHub Pages — дерево процессов/подпроцессов, показывающее только элементы с промптами |
| `docs/analysis/2026-06-02-migration-strategy-rfc.md` | `docs/analysis` | Other | proposal | `rfc` | RFC: стратегия миграции проекта Mango из Хаба в спок `mango_ba_prompts` |
| `docs/analysis/2026-06-16-experiment-1027-analysis.md` | `docs/analysis` | Analysis | local-context-analysis | `analysis` | Анализ эксперимента «Задача 1027» |
| `docs/analysis/2026-06-21-industry-inventory.md` | `docs/analysis` | Research | knowledge-generation | `research-inventory` | Industry Inventory — аналитическое доисследование для дозаполнения реестра (issue #168) |
| `docs/analysis/2026-06-21-voice-digital-channels-comparison.md` | `docs/analysis` | Research | knowledge-generation | `analysis` | Сравнительный анализ: голосовые vs текстовые каналы в Industry Taxonomy (ADR-011) |
| `docs/analysis/2026-06-22-issue-170-mango-inventory.md` | `docs/analysis` | Analysis | local-context-analysis | `analysis` | Инвентаризация Mango-реестра и перевод в JSON (issue #170) |
| `docs/analysis/2026-06-22-mango-taxonomy-convergence-test.md` | `docs/analysis` | Audit | conformance-check | `convergence-test` | Тест на сходимость маппинга Mango Taxonomy на Industry Taxonomy |
| `docs/analysis/2026-06-22-rfc-industry-taxonomy-improvement.md` | `docs/analysis` | Other | proposal | `rfc` | RFC: доработка Industry Taxonomy после теста на сходимость |
| `docs/analysis/2026-06-22-rfc-mango-taxonomy-improvement.md` | `docs/analysis` | Other | proposal | `rfc` | RFC: доработка Mango Taxonomy после теста на сходимость |
| `docs/analysis/2026-06-22-rfc-rules-registry-system.md` | `docs/analysis` | Other | proposal | `proposed` | RFC: Rules Registry System для управления правилами создания артефактов |
| `docs/analysis/2026-06-22-rfc-taxonomy-extension-mechanism.md` | `docs/analysis` | Other | proposal | `rfc` | RFC: системный механизм расширения таксономий (Industry + Mango) |
| `docs/analysis/2026-06-22-taxonomy-convergence-test.md` | `docs/analysis` | Audit | conformance-check | `analysis` | Тест на сходимость классификации функций по Industry Taxonomy Standard |
| `docs/analysis/2026-06-23-approval-contract-test-industry-rfc.md` | `docs/analysis` | Audit | conformance-check | `validation-note` | Тест контракта согласования: RFC Industry Taxonomy |
| `docs/analysis/2026-06-23-executable-contracts-and-rfc-problems.md` | `docs/analysis` | Research | knowledge-generation | `analysis` | Систематизация проблем исполнимых контрактов и RFC |
| `docs/analysis/2026-06-23-repository-structure-analysis.md` | `docs/analysis` | Research | knowledge-generation | `analysis` | Аналитическое исследование структуры каталогов проекта (обоснование архитектуры) |
| `docs/analysis/2026-06-24-artifact-chain-hypothesis-research.md` | `docs/analysis` | Research | knowledge-generation | `analysis` | Исследование гипотезы цепочки артефактов |
| `docs/analysis/2026-06-24-naming-convention-audit.md` | `docs/analysis` | Audit | conformance-check | `analysis` | Аудит нарушений naming convention |
| `docs/analysis/2026-06-24-runs-contract-log-policy-audit.md` | `docs/analysis` | Audit | conformance-check | `analysis` | Аудит контракта runs: Markdown-логи |
| `docs/analysis/2026-06-25-ba-processes-industry-analysis.md` | `docs/analysis` | Research | knowledge-generation | `analysis` | Структурный анализ БА-процессов и артефактов с опорой на индустриальные практики телекома |
| `docs/analysis/2026-06-25-bcreq-fr-contract-process-analysis.md` | `docs/analysis` | Research | knowledge-generation | `analysis` | Структурный анализ применения контракта BCREQ-FR: монолитный промпт против последовательности операций |
| `docs/analysis/2026-06-25-runs-observability-research.md` | `docs/analysis` | Research | knowledge-generation | `analysis` | Исследование трассируемости промптов в runs и внешних практик контроля проходов |
| `docs/analysis/2026-06-25-telecom-vendors-ba-practices-research.md` | `docs/analysis` | Research | knowledge-generation | `analysis` | Эмпирическая база: BA/Requirements-практики телеком-вендоров и операторов |
| `docs/audit/initial-state-2026-06.md` | `docs/audit` | Audit | conformance-check | `audit` | Аудит и план миграции `mango_ba_prompts` (2026-06) |
| `docs/audit/issue-115-kb-pipeline.md` | `docs/audit` | Audit | conformance-check | `audit` | Issue #115 — аудит KB Pipeline #11 |
| `docs/audit/issue-144-kb-structure.md` | `docs/audit` | Audit | conformance-check | `audit` | Аудит структуры `kb/` после миграции product docs |
| `docs/audit/issue-146-mango-taxonomy-validation.md` | `docs/audit` | Audit | conformance-check | `audit` | Issue #146: Mango Taxonomy validation on processed product docs |
| `docs/audit/taxonomy-standards-independent-review.md` | `docs/audit` | Audit | conformance-check | `audit` | Независимый аудит двух стандартов таксономии командой экспертов |
| `docs/ba-ecosystem.md` | `docs` | Other | reference-or-concept | `ecosystem-map` | Экосистема работы БА Mango |
| `docs/ba-process/README.md` | `docs` | Other | navigation | `index` | Прогоны BA-процесса (архивный указатель) |
| `docs/ba-processes/00-index.executable.md` | `docs` | Other | documentation | `registry` | BA Processes Index — executable layer |
| `docs/ba-processes/00-index.md` | `docs` | Other | documentation | `registry` | Процессы БА: карта маршрутов, операций и промптов |
| `docs/ba-processes/README.md` | `docs` | Other | navigation | `index` | docs/ba-processes |
| `docs/hub-research-dependencies.md` | `docs` | Research | knowledge-generation | `research-dependency-registry` | Реестр зависимостей от исследований Хаба |
| `docs/kb-experiment-report.md` | `docs` | Analysis | local-context-analysis | `experiment-report` | Отчёт по эксперименту: машиночитаемая база знаний из PDF (issue #111) |
| `docs/requirements-engineering-crosswalk.md` | `docs` | Other | reference-or-concept | `reference` | Crosswalk: Вигерс ↔ mango operations ↔ BCREQ |
| `docs/reviews/migration-rfc-human-review-2026-06.md` | `docs` | Audit | conformance-check | `human-review-report` | Human Review: `2026-06-02-migration-strategy-rfc.md` (issue #13) |
| `docs/rfc-format-validator.md` | `docs` | Other | proposal | `draft` | Валидатор формата RFC |
| `docs/rfc-hub-integration.md` | `docs` | Other | proposal | `rfc` | RFC: рекомендации по переносу лучших практик из `mango_ba_prompts` в Хаб |
| `docs/task-for-konard-template.md` | `docs` | Other | reference-or-concept | `template` | Шаблон задачи для Конарда |
| `docs/taxonomy.md` | `docs` | Other | reference-or-concept | `taxonomy` | Таксономия: когнитивные операции и процессы БА |

## Clarify / clarify-engine-ai

| Path | Bucket | Actual type | Subtype | Source signal | Title |
| --- | --- | --- | --- | --- | --- |
| `docs/ADR/001-rag-architecture.md` | `docs` | Other | decision-record | `-` | ADR-001: RAG Architecture with Hybrid Search |
| `docs/ADR/002-export-schema-extension.md` | `docs` | Other | decision-record | `-` | ADR-002. Расширение схемы экспорта результатов анализа ТЗ |
| `docs/ADR/003-multi-agent-orchestration-draft.md` | `docs` | Other | decision-record | `-` | ADR-003 (Draft). Мультиагентная оркестрация, обогащение KB и анализ рыночного спроса |
| `docs/ADR/004-prompt-management.md` | `docs` | Other | decision-record | `-` | ADR-004. Централизованная Prompt Library и версионирование промптов |
| `docs/ADR/004-ui-operation-modes.md` | `docs` | Other | decision-record | `-` | ADR-004: Two UI Operation Modes — "Анализ ТЗ" (stateless) and "Консультация" (stateful, history ≤ 6) |
| `docs/ADR/005-audit-trail.md` | `docs` | Other | decision-record | `-` | ADR-005. LLM audit trail with per-request run_id |
| `docs/ADR/006-citation-links.md` | `docs` | Other | decision-record | `-` | ADR-006: Citation Links |
| `docs/ADR/007-canonical-cache-draft.md` | `docs` | Other | decision-record | `-` | ADR-007: Canonical Query Cache & Clustering |
| `docs/ADR/007-error-handling.md` | `docs` | Other | decision-record | `-` | ADR-007: Graceful UI Error Handling and Retry |
| `docs/ADR/008-data-export.md` | `docs` | Other | decision-record | `-` | ADR-008: Context-Dependent UI Export |
| `docs/ADR/009-parent-document-retrieval.md` | `docs` | Other | decision-record | `-` | ADR-009: Parent Document Retrieval |
| `docs/ADR/README.md` | `docs` | Other | decision-record | `-` | Architecture Decision Records |
| `docs/CONCEPT.md` | `docs` | Other | reference-or-concept | `-` | 📘 Концепция внедрения ИИ-анализатора тендерных ТЗ (MVP) |
| `docs/DEV_NOTES.md` | `docs` | Other | documentation | `-` | DEV_NOTES — issue #73 (RAG-пайплайн) |
| `docs/RAG_OPTIMIZATION_ANALYSIS.md` | `docs` | Analysis | local-context-analysis | `-` | RAG Pipeline Analysis & Optimization Roadmap |
| `docs/README.md` | `docs` | Other | navigation | `-` | Документация `clarify-engine-ai` |
| `docs/analysis/2026-05-12_review_mvp-context_v1.md` | `docs/analysis` | Analysis | local-context-analysis | `-` | ⚠️ WARNING: ANALYTICAL DOCUMENT ONLY |
| `docs/analysis/2026-05-13_analysis_next-docs-implementation-task_v1.md` | `docs/analysis` | Analysis | local-context-analysis | `-` | ⚠️ WARNING: ANALYTICAL DOCUMENT ONLY |
| `docs/analysis/2026-05-15_analysis_repo-state-and-mvp-recommendations_v1.md` | `docs/analysis` | Analysis | local-context-analysis | `-` | Анализ состояния репозитория и рекомендации по MVP |
| `docs/analysis/2026-05-17_analysis_tz-structure_samples.md` | `docs/analysis` | Analysis | local-context-analysis | `-` | 🔍 Анализ структуры входных ТЗ (`.xlsx` / `.docx` / `.doc`) и матрица изменений под `.docx`-поддержку |
| `docs/analysis/2026-05-17_sprint-1-execution-report_v1.md` | `docs/analysis` | Analysis | local-context-analysis | `-` | Sprint-1 P0 — Execution Report (issue #87) |
| `docs/analysis/2026-05-19_code-review-triage_v1.md` | `docs/analysis` | Audit | conformance-check | `-` | Верификация замечаний Code Review (BL-26) |
| `docs/analysis/2026-05-19_sprint-5-kickoff_v1.md` | `docs/analysis` | Analysis | local-context-analysis | `-` | Sprint 5 — UX Polish & Documentation Sync — Kickoff (issue #192) |
| `docs/analysis/2026-05-20_sprint-4-kickoff_v1.md` | `docs/analysis` | Analysis | local-context-analysis | `-` | Sprint 4 — Pilot Readiness & Automation — Kickoff (issue #187) |
| `docs/analysis/2026-05-20_sprint-4-parallel-kickoff_v1.md` | `docs/analysis` | Analysis | local-context-analysis | `-` | Sprint 4 Parallel — BL-48 Installer PoC — Kickoff (issue #190) |
| `docs/analysis/README.md` | `docs/analysis` | Other | navigation | `-` | 📂 docs/analysis/ |
| `docs/analysis/metadata-coverage-fix_v1.md` | `docs/analysis` | Analysis | local-context-analysis | `-` | Metadata Coverage Fix — Section Propagation (issue #109) |
| `docs/analysis/sprint-execution-report_template.md` | `docs/analysis` | Analysis | local-context-analysis | `-` | Sprint [N] Execution Report |
| `docs/audit/2026-05-12_repository-consistency_audit_v1.md` | `docs/audit` | Audit | conformance-check | `-` | 🔍 Audit: Repository Consistency & Testability |
| `docs/audit/2026-05-16_post-implementation-audit-#53_v1.md` | `docs/audit` | Audit | conformance-check | `-` | 🔍 Post-Implementation Audit: Issue #53 |
| `docs/audit/2026-05-19_bl-34_architecture-consistency-audit_v1.md` | `docs/audit` | Audit | conformance-check | `-` | 📊 Architecture Consistency Audit — BL-34 |
| `docs/audit/2026-05-20_bl-43-smoke-e2e-report_v1.md` | `docs/audit` | Audit | conformance-check | `-` | 📊 Post-fix Smoke & E2E Verification — BL-43 (ARM Deployment Readiness) |
| `docs/audit/2026-05-20_bl-57_comprehensive-verification_v1.md` | `docs/audit` | Audit | conformance-check | `-` | BL-57 Comprehensive Verification — UI / Code / Docs Alignment Before Pilot |
| `docs/audit/README.md` | `docs/audit` | Other | navigation | `-` | 📂 docs/audit/ |
| `docs/audit/data-masking_v1.md` | `docs/audit` | Audit | conformance-check | `-` | 🔒 Audit: Data Masking Implementation |
| `docs/backlog/2026-05-17_backlog_rag-optimization_v1.2.md` | `docs` | Other | planning | `-` | 📦 Бэклог оптимизации RAG-пайплайна (P0–P2) — v1.2 |
| `docs/backlog/2026-05-17_backlog_rag-optimization_v1.3.md` | `docs` | Other | planning | `-` | 📦 Бэклог оптимизации RAG-пайплайна (P0–P2) — v1.3 |
| `docs/backlog/2026-05-17_backlog_rag-optimization_v1.4.md` | `docs` | Other | planning | `-` | 📦 Бэклог оптимизации RAG-пайплайна (P0–P2) — v1.4 |
| `docs/backlog/2026-05-17_backlog_rag-optimization_v1.5.md` | `docs` | Other | planning | `-` | 📦 Бэклог оптимизации RAG-пайплайна (P0–P2) — v1.5 |
| `docs/backlog/2026-05-17_backlog_rag-optimization_v1.md` | `docs` | Other | planning | `-` | 📦 Бэклог оптимизации RAG-пайплайна (P0–P2) |
| `docs/backlog/2026-05-19_track2-cache-validation_v2.md` | `docs` | Other | planning | `-` | Track 2 Cache Validation Backlog — v2.0 |
| `docs/backlog/2026-05-20_backlog_arm-pilot-test-fixes_v1.md` | `docs` | Other | planning | `-` | 🔧 Бэклог исправлений по результатам тестирования на АРМ (Pilot Readiness) — v1.0 |
| `docs/research/2026-05-20_bl-47_arm-installer-cloud-research_v1.md` | `research` | Research | knowledge-generation | `-` | 🔬 Research: ARM Installer, Cloud TZ Access & Documentation Update Flow (BL-47) |
| `docs/research/2026-05-20_bl-59_requirement-parsing_v1.md` | `research` | Research | knowledge-generation | `-` | 🔬 Research: Requirement Atomization & Document Structure Recognition (BL-59) |
| `docs/research/2026-05-20_bl-60_next-gen-architecture_v1.md` | `research` | Research | knowledge-generation | `-` | 🔬 Research: Next-Gen RAG Architecture, Dynamic LLM Routing & Infrastructure Tiers (BL-60) |
| `docs/research/2026-05-21_bl-57_retrieval-architecture_v1.md` | `research` | Research | knowledge-generation | `-` | 🔬 Research: Advanced Retrieval Architecture for Complex Requirement Matching (BL-58) |
| `docs/research/2026-05-21_bl-61_market-research_ru-education_v1.md` | `research` | Research | knowledge-generation | `-` | Research: RU-education adaptation for BL-61 Market Comparison (BL-67) |
| `docs/research/2026-05-21_bl-61_market-research_ru-education_v2.md` | `research` | Research | knowledge-generation | `-` | Research: Business-readable RU education adaptation for BL-61 Market Comparison (BL-61.1) |
| `docs/research/2026-05-21_bl-61_market-research_v1.md` | `research` | Research | knowledge-generation | `-` | Research: Market Comparison for Microservices Architecture Components (BL-61) |
| `docs/research/2026-05-21_bl-62_synthesis-optimized-architectures_v1.md` | `research` | Research | knowledge-generation | `-` | Research: Synthesis Research — Optimized Architecture Options for Pilot & Production (BL-62) |
| `docs/research/2026-05-21_bl-68_breakthrough-team-vision_v1.md` | `research` | Research | knowledge-generation | `-` | Research: Видение команды «Прорыва» — стратегия развития Clarify Engine (BL-68) |
| `docs/research/2026-05-21_support-team_mvp-architecture-proposal_v1.md` | `research` | Research | knowledge-generation | `-` | Research: Предложения команды поддержки по архитектуре MVP Clarify Engine |
| `docs/research/html/2026-05-21_bl-61_market-research_ru-education_v1.html` | `research` | Research | knowledge-generation | `-` | - |
| `docs/research/html/2026-05-21_bl-61_market-research_ru-education_v2.html` | `research` | Research | knowledge-generation | `-` | - |
| `docs/runbooks/README.md` | `docs` | Other | navigation | `-` | 📚 Runbooks (Эксплуатационные инструкции) |
| `docs/runbooks/arm-deployment-ivan.md` | `docs` | Other | guide | `-` | ARM Deployment Runbook for Ivan Gulienko |
| `docs/standards/README.md` | `docs` | Other | standard | `-` | 📂 docs/standards/ |
| `docs/standards/embedding-model.md` | `docs` | Other | standard | `-` | 🧮 Standard: Embedding Model |
| `docs/standards/evaluation-metrics.md` | `docs` | Other | standard | `-` | Retrieval Evaluation Metrics |
| `docs/standards/export-markup.md` | `docs` | Other | standard | `-` | 🧾 Standard: Export Markup (table / Word / Markdown) |
| `docs/standards/llm-behavior.md` | `docs` | Other | standard | `-` | 🎛️ Standard: LLM Decoding Behavior |
| `docs/standards/naming-convention.md` | `docs` | Other | standard | `-` | 📐 Стандарт именования файлов документации |
| `docs/standards/roles.md` | `docs` | Other | standard | `-` | 👥 Roles & Responsibilities — Команда проекта |
| `docs/standards/templates/analysis-template.md` | `docs` | Other | standard | `-` | <Заголовок документа> |
| `docs/standards/templates/decision-template.md` | `docs` | Other | standard | `-` | Decision: <короткая формулировка решения> |
| `docs/user_guide/01_intro_modes.md` | `docs` | Other | guide | `-` | 1. Режимы работы |
| `docs/user_guide/02_interface_elements.md` | `docs` | Other | guide | `-` | 2. Кнопки и селекторы |
| `docs/user_guide/03_results_and_export.md` | `docs` | Other | guide | `-` | 3. Результаты и экспорт |
| `docs/user_guide/04_troubleshooting.md` | `docs` | Other | guide | `-` | 4. Устранение проблем |
| `docs/user_guide/README.md` | `docs` | Other | navigation | `-` | 📘 Справка для БА — Руководство пользователя |
