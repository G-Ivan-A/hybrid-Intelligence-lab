---
status: draft
version: 0.1
updated: 2026-07-02
temperature: 0.1
---

# Analysis artifact candidate matrix

Generated for issue #342. Classification is heuristic and evidence-oriented:
the requested corpus is scanned by path, then path, filename, title,
frontmatter and early content signals classify each text artifact by actual
role: Research / Analysis / Audit / Report / RFC / ADR / Other. The written
analysis document performs the final synthesis and recommendations.

## Repository snapshots

| Repo | URL | SHA |
| --- | --- | --- |
| Hub / hybrid-Intelligence-lab | https://github.com/G-Ivan-A/hybrid-Intelligence-lab | `3abae05d142284a98719c4549229b6c0099eeb65` |
| Mango / mango_ba_prompts | https://github.com/G-Ivan-A/mango_ba_prompts | `52bc8b72419abb9548d9b6091623f18c080efae4` |
| Clarify / clarify-engine-ai | https://github.com/G-Ivan-A/clarify-engine-ai | `96c288fd13a2d7cc7c3e3cdd52574944858e6255` |

## Summary by actual type

| Repo | Scanned text | Research | Analysis | Audit | Report | RFC | ADR | Other | Non-text |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Hub / hybrid-Intelligence-lab | 110 | 37 | 8 | 8 | 13 | 24 | 0 | 20 | 14 |
| Mango / mango_ba_prompts | 57 | 5 | 6 | 14 | 2 | 14 | 0 | 16 | 2 |
| Clarify / clarify-engine-ai | 19 | 0 | 5 | 7 | 5 | 0 | 0 | 2 | 0 |

## Analysis relation summary

| Repo | Relation | Count |
| --- | --- | ---: |
| Hub / hybrid-Intelligence-lab | `actual-analysis` | 2 |
| Hub / hybrid-Intelligence-lab | `adjacent-not-analysis` | 96 |
| Hub / hybrid-Intelligence-lab | `analysis-named-report` | 3 |
| Hub / hybrid-Intelligence-lab | `analysis-named-research` | 3 |
| Hub / hybrid-Intelligence-lab | `analysis-outside-analysis-path` | 6 |
| Mango / mango_ba_prompts | `actual-analysis` | 6 |
| Mango / mango_ba_prompts | `adjacent-not-analysis` | 36 |
| Mango / mango_ba_prompts | `masked-audit-in-analysis-path` | 5 |
| Mango / mango_ba_prompts | `masked-research-in-analysis-path` | 5 |
| Mango / mango_ba_prompts | `masked-rfc-in-analysis-path` | 5 |
| Clarify / clarify-engine-ai | `actual-analysis` | 5 |
| Clarify / clarify-engine-ai | `adjacent-not-analysis` | 7 |
| Clarify / clarify-engine-ai | `masked-audit-in-analysis-path` | 1 |
| Clarify / clarify-engine-ai | `masked-other-in-analysis-path` | 1 |
| Clarify / clarify-engine-ai | `masked-report-in-analysis-path` | 5 |

## Current path buckets

| Repo | Bucket | Text artifacts | Research | Analysis | Audit | Report | RFC | Other |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Hub / hybrid-Intelligence-lab | `docs/analysis` | 2 | 0 | 2 | 0 | 0 | 0 | 0 |
| Hub / hybrid-Intelligence-lab | `docs/audit` | 3 | 0 | 0 | 3 | 0 | 0 | 0 |
| Hub / hybrid-Intelligence-lab | `docs/report` | 3 | 0 | 0 | 0 | 3 | 0 | 0 |
| Hub / hybrid-Intelligence-lab | `governance` | 6 | 0 | 0 | 0 | 1 | 0 | 5 |
| Hub / hybrid-Intelligence-lab | `governance/rfc` | 21 | 0 | 0 | 0 | 0 | 20 | 1 |
| Hub / hybrid-Intelligence-lab | `research` | 75 | 37 | 6 | 5 | 9 | 4 | 14 |
| Mango / mango_ba_prompts | `docs/analysis` | 21 | 5 | 6 | 5 | 0 | 5 | 0 |
| Mango / mango_ba_prompts | `docs/audit` | 5 | 0 | 0 | 5 | 0 | 0 | 0 |
| Mango / mango_ba_prompts | `governance` | 27 | 0 | 0 | 4 | 2 | 5 | 16 |
| Mango / mango_ba_prompts | `governance/rfc` | 4 | 0 | 0 | 0 | 0 | 4 | 0 |
| Clarify / clarify-engine-ai | `docs/analysis` | 12 | 0 | 5 | 1 | 5 | 0 | 1 |
| Clarify / clarify-engine-ai | `docs/audit` | 7 | 0 | 0 | 6 | 0 | 0 | 1 |

## Masked artifacts in `docs/analysis/`

| Repo | Path | Actual type | Subtype | Rationale |
| --- | --- | --- | --- | --- |
| Clarify / clarify-engine-ai | `docs/analysis/2026-05-17_sprint-1-execution-report_v1.md` | Report | analysis-path-report | descriptive execution/report artifact under docs/analysis |
| Clarify / clarify-engine-ai | `docs/analysis/2026-05-19_code-review-triage_v1.md` | Audit | conformance-check | checks state against a norm, contract, checklist, or expected behavior |
| Clarify / clarify-engine-ai | `docs/analysis/2026-05-19_sprint-5-kickoff_v1.md` | Report | analysis-path-report | descriptive execution/report artifact under docs/analysis |
| Clarify / clarify-engine-ai | `docs/analysis/2026-05-20_sprint-4-kickoff_v1.md` | Report | analysis-path-report | descriptive execution/report artifact under docs/analysis |
| Clarify / clarify-engine-ai | `docs/analysis/2026-05-20_sprint-4-parallel-kickoff_v1.md` | Report | analysis-path-report | descriptive execution/report artifact under docs/analysis |
| Clarify / clarify-engine-ai | `docs/analysis/README.md` | Other | navigation | README/navigation file |
| Clarify / clarify-engine-ai | `docs/analysis/sprint-execution-report_template.md` | Report | analysis-path-report | descriptive execution/report artifact under docs/analysis |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-02-migration-strategy-rfc.md` | RFC | proposal | frontmatter, title, or path marks a proposal/RFC |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-21-industry-inventory.md` | Research | knowledge-generation | docs/analysis artifact generates external or hypothesis-driven knowledge |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-22-mango-taxonomy-convergence-test.md` | Audit | conformance-check | checks state against a norm, contract, checklist, or expected behavior |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-22-rfc-industry-taxonomy-improvement.md` | RFC | proposal | frontmatter, title, or path marks a proposal/RFC |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-22-rfc-mango-taxonomy-improvement.md` | RFC | proposal | frontmatter, title, or path marks a proposal/RFC |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-22-rfc-rules-registry-system.md` | RFC | proposal | frontmatter, title, or path marks a proposal/RFC |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-22-rfc-taxonomy-extension-mechanism.md` | RFC | proposal | frontmatter, title, or path marks a proposal/RFC |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-22-taxonomy-convergence-test.md` | Audit | conformance-check | checks state against a norm, contract, checklist, or expected behavior |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-23-approval-contract-test-industry-rfc.md` | Audit | conformance-check | checks state against a norm, contract, checklist, or expected behavior |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-24-artifact-chain-hypothesis-research.md` | Research | knowledge-generation | docs/analysis artifact generates external or hypothesis-driven knowledge |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-24-naming-convention-audit.md` | Audit | conformance-check | checks state against a norm, contract, checklist, or expected behavior |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-24-runs-contract-log-policy-audit.md` | Audit | conformance-check | checks state against a norm, contract, checklist, or expected behavior |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-25-ba-processes-industry-analysis.md` | Research | knowledge-generation | docs/analysis artifact generates external or hypothesis-driven knowledge |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-25-runs-observability-research.md` | Research | knowledge-generation | docs/analysis artifact generates external or hypothesis-driven knowledge |
| Mango / mango_ba_prompts | `docs/analysis/2026-06-25-telecom-vendors-ba-practices-research.md` | Research | knowledge-generation | docs/analysis artifact generates external or hypothesis-driven knowledge |

## Hub / hybrid-Intelligence-lab

| Path | Bucket | Actual type | Relation | Hint | Title |
| --- | --- | --- | --- | --- | --- |
| `docs/analysis/2026-06-30-backlog-and-artifact-change-policy-analysis.md` | `docs/analysis` | Analysis | `actual-analysis` | already in target Analysis path; future standard should modernize metadata/sections | Анализ: бэклог и политика изменений артефактов |
| `docs/analysis/2026-07-01-reports-artifacts-inventory.md` | `docs/analysis` | Analysis | `actual-analysis` | already in target Analysis path; future standard should modernize metadata/sections | Reports artifacts: inventory and boundaries |
| `docs/audit/2026-06-29-research-artifact-format-contract-audit.md` | `docs/audit` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Audit: Research artifact format contract |
| `docs/audit/2026-07-01-documentation-boundary-audit.md` | `docs/audit` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Аудит: коллизии интерпретации стандартов RFC/ADR/Standard (B-039) |
| `docs/audit/task-execution-audit-2026-06.md` | `docs/audit` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Аудит выполненных задач (1-4) |
| `docs/report/2026-06-30-pr-303-rfc-hypothesis-analysis.md` | `docs/report` | Report | `analysis-named-report` | route by Reports standard / docs/report profile, not Analysis | Отчет по гипотезе проблемы PR #303 |
| `docs/report/2026-07-01-reports-inventory-placement-analysis.md` | `docs/report` | Report | `analysis-named-report` | route by Reports standard / docs/report profile, not Analysis | Отчёт: анализ размещения deliverables инвентаризации Reports (issue #310) |
| `docs/report/2026-07-01-rfc-adr-duplication-analysis.md` | `docs/report` | Report | `analysis-named-report` | route by Reports standard / docs/report profile, not Analysis | Отчёт: анализ причины дублирования RFC B-016 ↔ ADR-003 |
| `governance/agent-onboarding-protocol.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Agent Onboarding — Протокол бесшовной передачи проекта |
| `governance/artifact-map.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Artifact Map |
| `governance/backlog.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | BACKLOG — единый бэклог работ Хаба |
| `governance/executable-documents-issues.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Реестр issues: внедрение стандарта исполнимых документов |
| `governance/repo-model.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Repository Model |
| `governance/rfc/2026-06-27-rfc-adr-standard.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Стандарт структуры ADR |
| `governance/rfc/2026-06-27-rfc-rfc-standard.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Стандарт структуры RFC |
| `governance/rfc/2026-06-30-rfc-research-structure.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Структура research, контейнер `exp/` и маршрутизация Research / Analysis / Audit |
| `governance/rfc/2026-07-02-rfc-reports-structure.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Структура Reports-артефактов — базовый стандарт, профили подтипов и routing |
| `governance/rfc/README.md` | `governance/rfc` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Governance RFC |
| `governance/rfc/contract-executability-rfc.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Архитектура исполнимых документов (Executable Contracts) |
| `governance/rfc/documentation-architecture-balance.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Documentation Architecture Balance (Anti-Inflation vs Atomicity) |
| `governance/rfc/draft-triage-and-exit-plan.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Draft Triage And Exit Plan |
| `governance/rfc/external-knowledge-integration.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: External Knowledge Integration |
| `governance/rfc/htom-vs-spoke-clarification-2026-06.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: разделение концепций «HTOM-команда» и «spoke-репозиторий» |
| `governance/rfc/hub-vision-concept-proposal-2026-06.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Vision и Concept Хаба + библиотека гайдов + MkDocs + экосистемная карта |
| `governance/rfc/knowledge-lifecycle-proposal.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Knowledge Lifecycle |
| `governance/rfc/methodology-research-and-proposals.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Methodology Research & Proposals for Hub / Mango / Open-AI |
| `governance/rfc/product-concept-template-proposal.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Universal Product Concept Template |
| `governance/rfc/repository-archetypes-template-release.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Repository Archetypes, Project Template & Release Strategy |
| `governance/rfc/repository-quality-improvement-plan.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Repository Quality Improvement Plan |
| `governance/rfc/research-memory-source-intelligence.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Research Memory & Source Intelligence Framework |
| `governance/rfc/resolve-artifact-location-proposal.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Resolve Artifact Location Prompt |
| `governance/rfc/rfc-two-cases-of-project-initialization.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC-манифест: два ортогональных кейса инициализации проекта |
| `governance/rfc/solution-concept-template-proposal.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Universal Solution Concept Template |
| `governance/rfc/tech-debt-solutions-proposal-2026-06.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Предложения по решению техдолга |
| `governance/session-digests.md` | `governance` | Report | `adjacent-not-analysis` | route by Reports standard / docs/report profile, not Analysis | Session Digests — суммарии сессий |
| `research/README.md` | `research` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Research |
| `research/cicd/2026-06-09-js-cicd-template-analysis.md` | `research` | Research | `analysis-named-research` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Исследование: JS CI/CD Template — Анализ шаблона link-foundation |
| `research/cicd/README.md` | `research` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Research: CI/CD |
| `research/external-knowledge/2026-06-18-wigers-requirements-analysis.md` | `research` | Research | `analysis-named-research` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Исследование: требования к ПО по Вигерсу с актуализацией на AI-тренды 2026 |
| `research/external-knowledge/README.md` | `research` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Research: External Knowledge |
| `research/external-knowledge/external-insights/2026-06-13-12-factor-agents.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Инсайт: владей промптами и контекстом как кодом, держи человека в петле |
| `research/external-knowledge/external-insights/2026-06-13-building-effective-agents.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Инсайт: простые компонуемые паттерны > монолитные «умные» агенты |
| `research/external-knowledge/external-insights/2026-06-13-spec-driven-development.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Инсайт: спецификация как исполнимый артефакт между требованием и кодом |
| `research/external-knowledge/external-insights/2026-06-15-agent-local-memory-context.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Инсайт: локальная память проекта снимает нагрузку с контекстного окна |
| `research/external-knowledge/external-insights/2026-06-15-structured-prompt-driven-development.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Инсайт: промпт как версионируемый артефакт, а не одноразовая команда |
| `research/external-knowledge/external-insights/README.md` | `research` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | External Insights |
| `research/external-knowledge/external-sources-registry.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Реестр внешних источников |
| `research/governance/2026-06-06-contract-documentation-format.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Исследование: оптимальный формат прочих контрактов |
| `research/governance/2026-06-06-executable-contract-format.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Исследование: оптимальный формат исполнимых контрактов |
| `research/governance/2026-06-06-governance-folder-structure-decisions.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Решения по структуре governance-каталогов (Q1, Q2, Q3) |
| `research/governance/2026-06-06-research-documentation-format.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Исследование: оптимальный формат исследований Хаба |
| `research/governance/README.md` | `research` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Research: Governance (форматы и эволюция Хаба) |
| `research/hub/2026-05-28-project-context-and-bootstrap-patterns.md` | `research` | Analysis | `analysis-outside-analysis-path` | candidate for docs/analysis or explicit Analysis metadata after standard | Как передавать контекст и создавать проекты предсказуемо |
| `research/hub/2026-05-28-prompts-classification-audit.md` | `research` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Аудит входных данных для классификации промптов |
| `research/hub/2026-05-28-prompts-classification-standard.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Стандарт классификации промптов |
| `research/hub/2026-05-28-user-prompts-analysis.md` | `research` | Research | `analysis-named-research` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Анализ пользовательских промптов |
| `research/hub/2026-06-01-team-c-governance-strategy-audit.md` | `research` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Интерпретация аудита стратегии governance от команды C |
| `research/hub/2026-06-02-ai-collaboration-retrospective-mango-migration.md` | `research` | Report | `adjacent-not-analysis` | route by Reports standard / docs/report profile, not Analysis | Ретроспектива AI-collaboration: сессия проектирования миграции Mango (Хаб → спок) |
| `research/hub/2026-06-02-ai-collaboration-retrospective.md` | `research` | Report | `adjacent-not-analysis` | route by Reports standard / docs/report profile, not Analysis | Ретроспектива AI-collaboration по сессии проектирования шаблонов споков |
| `research/hub/2026-06-02-external-governance-patterns-review.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Анализ external governance patterns и матрица применимости для Хаба |
| `research/hub/2026-06-12-ecosystem-governance-audit.md` | `research` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Ecosystem Governance Audit |
| `research/hub/2026-06-12-external-practice-intake.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | External Practice Intake: Agent Work And HTOM Docs |
| `research/hub/2026-06-12-international-ai-governance-practices.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | International AI Governance Practices |
| `research/hub/2026-06-20-ecosystem-architecture-research.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Комплексное исследование архитектуры экосистемы: Hub, open-ai.ru, репутационные технологии |
| `research/hub/2026-06-23-repository-structure-concept.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Концепция базовых каталогов для архетипов проектов (дополнение к mango-исследованию) |
| `research/hub/2026-06-25-artifact-inventory-and-classification.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Инвентаризация и классификация артефактов экосистемы (mango_ba_prompts + hybrid-Intelligence-lab) |
| `research/hub/2026-06-27-adr-industry-norms-and-variants.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | ADR: индустриальные нормы, дельты и варианты для Hub / Mango |
| `research/hub/2026-06-27-rfc-industry-norms-and-variants.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | RFC: индустриальные нормы, дельты и варианты для Hub / Mango |
| `research/hub/2026-06-28-research-analysis-audit-inventory.md` | `research` | Analysis | `analysis-outside-analysis-path` | candidate for docs/analysis or explicit Analysis metadata after standard | Research / Analysis / Audit: инвентаризация и план стандартизации |
| `research/hub/2026-06-28-ripple-effects-282-research.md` | `research` | Analysis | `analysis-outside-analysis-path` | candidate for docs/analysis or explicit Analysis metadata after standard | Исследование: Ripple Effects issue 282 |
| `research/hub/2026-06-30-reports-industry-norms-and-standardization-scope.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Reports: индустриальные нормы и scope стандартизации |
| `research/hub/2026-07-02-task-execution-modes-research.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Режимы выполнения задач для ИИ-агентов: индустриальные нормы и паттерны классификации |
| `research/hub/README.md` | `research` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Research: Hub |
| `research/hub/exp-research-analysis-audit-288/README.md` | `research` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Experiment: Research/Analysis/Audit inventory for issue 288 |
| `research/hub/exp-research-analysis-audit-288/outputs/2026-06-28-artifact-classification-matrix.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Research/Analysis/Audit artifact classification matrix |
| `research/hub/exp-rfc-adr-industry-norms/README.md` | `research` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Experiment: RFC/ADR industry norms evidence |
| `research/hub/exp-rfc-adr-industry-norms/outputs/2026-06-27-adr-external-tree-summary.md` | `research` | Report | `adjacent-not-analysis` | route by Reports standard / docs/report profile, not Analysis | ADR external source tree summary |
| `research/hub/exp-rfc-adr-industry-norms/outputs/2026-06-27-local-rfc-adr-audit.md` | `research` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Local ecosystem RFC/ADR audit |
| `research/hub/exp-rfc-adr-industry-norms/outputs/2026-06-27-rfc-external-tree-summary.md` | `research` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC external source tree summary |
| `research/hub/exp-ripple-effects-282/README.md` | `research` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Experiment: Ripple effects 282 frontmatter scan |
| `research/hub/exp-ripple-effects-282/outputs/2026-06-28-frontmatter-scan.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Frontmatter scan for issue 284 |
| `research/hub/exp/reports-inventory-310/2026-07-01-reports-artifact-matrix.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Reports artifact candidate matrix |
| `research/hub/exp/reports-inventory-310/README.md` | `research` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Experiment: Reports inventory for issue 310 |
| `research/hub/exp/task-execution-modes-330/2026-07-02-test1-backlog.md` | `research` | Report | `adjacent-not-analysis` | route by Reports standard / docs/report profile, not Analysis | Test 1 — классификация задач бэклога (B-016..B-039) |
| `research/hub/exp/task-execution-modes-330/2026-07-02-test2-issues.md` | `research` | Report | `adjacent-not-analysis` | route by Reports standard / docs/report profile, not Analysis | Test 2 — интерпретация практических issue без контекста |
| `research/hub/exp/task-execution-modes-330/2026-07-02-test3-conflict.md` | `research` | Report | `adjacent-not-analysis` | route by Reports standard / docs/report profile, not Analysis | Test 3 — конфликт режимов (творчество vs строгий контракт) |
| `research/hub/exp/task-execution-modes-330/2026-07-02-test4-evolution.md` | `research` | Report | `adjacent-not-analysis` | route by Reports standard / docs/report profile, not Analysis | Test 4 — адаптация к изменению требований |
| `research/hub/exp/task-execution-modes-330/2026-07-02-test5-industry.md` | `research` | Report | `adjacent-not-analysis` | route by Reports standard / docs/report profile, not Analysis | Test 5 — применение индустриальных паттернов к нашим задачам |
| `research/hub/exp/task-execution-modes-330/README.md` | `research` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | exp: task-execution-modes-330 |
| `research/mango/2026-05-22-classification-tz.md` | `research` | Analysis | `analysis-outside-analysis-path` | candidate for docs/analysis or explicit Analysis metadata after standard | Классификация требований по корпусу ТЗ (classification (TZ)) |
| `research/mango/2026-05-22-classification.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Классификация IT/Telecom SaaS-продуктов MANGO OFFICE |
| `research/mango/2026-05-22-requirements-flow.md` | `research` | Analysis | `analysis-outside-analysis-path` | candidate for docs/analysis or explicit Analysis metadata after standard | Flow требований для AI-анализа тендерных ТЗ MANGO OFFICE |
| `research/mango/2026-05-26-rag-mapping-roadmap.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Маппинг продуктов/фич Mango как RAG-навигатор и roadmap автоматизации БА |
| `research/mango/2026-05-26-requirements-lifecycle-uncertainty.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Жизненный цикл требования Mango: неопределенность, декомпозиция и международная практика |
| `research/mango/2026-05-26-taxonomy-concept.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Концепция Единой таксономии функциональности Mango |
| `research/mango/2026-05-27-capability-decomposition.md` | `research` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Fixed per draft-triage RFC Phase 1: local relations use path-only values; |
| `research/mango/2026-06-18-ai-classifications-formalization.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Формализация AI-классификаций и интеграция в роадмап Mango |
| `research/mango/2026-06-18-requirements-engineering-ai-era.md` | `research` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Requirements Engineering in the AI Era — синхронизация Вигерса и mango-ADR |
| `research/mango/2026-06-19-repository-structure-vision.md` | `research` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Независимое видение структуры репозитория(ев) `mango_ba_prompts` (ИБ, внешнее хранилище, экосистема) / Independent Vision of `mango_ba_prompts` Repository Structure |
| `research/mango/2026-06-19-token-optimization-proposal.md` | `research` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Оптимизация потребления токенов при работе AI с репозиторием `mango_ba_prompts` / Token Consumption Optimization for AI Working with the `mango_ba_prompts` Repository |
| `research/mango/README.md` | `research` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Research: MANGO OFFICE |
| `research/open-ai-ru/2026-06-20-open-ai-ru-repository-architecture-and-l3-l4.md` | `research` | Analysis | `analysis-outside-analysis-path` | candidate for docs/analysis or explicit Analysis metadata after standard | Архитектура репозитория open-ai.ru и разработка уровней L3–L4 на основе международных практик |
| `research/open-ai-ru/README.md` | `research` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Research: open-ai.ru |
| `research/reputation-technologies/2026-06-20-executive-summary.ru-en.md` | `research` | Report | `adjacent-not-analysis` | route by Reports standard / docs/report profile, not Analysis | Executive Summary — GRA Reputation Framework (RU + EN) |
| `research/reputation-technologies/2026-06-20-founders-vision-and-framework.ru.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Репутационные технологии: от видения фаундера к международному стандарту GRA |
| `research/reputation-technologies/2026-06-20-framework-standard.en.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | GRA Framework Standard — Draft (International Format) |
| `research/reputation-technologies/2026-06-20-glossary.ru-en.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | GRA Terminology Dictionary / Терминологический словарь (RU ↔ EN) |
| `research/reputation-technologies/2026-06-20-white-paper.en.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | GRA — A Graph-Native, Cross-Level Standard for Reputation Engineering (White Paper) |
| `research/reputation-technologies/2026-06-29-partner-attraction-strategy.ru.md` | `research` | Research | `adjacent-not-analysis` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Стратегия привлечения партнёров к курсу Репутационных технологий |
| `research/reputation-technologies/README.md` | `research` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Research: Reputation Technologies (GRA) |

## Mango / mango_ba_prompts

| Path | Bucket | Actual type | Relation | Hint | Title |
| --- | --- | --- | --- | --- | --- |
| `docs/analysis/2026-06-02-migration-strategy-rfc.md` | `docs/analysis` | RFC | `masked-rfc-in-analysis-path` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: стратегия миграции проекта Mango из Хаба в спок `mango_ba_prompts` |
| `docs/analysis/2026-06-16-experiment-1027-analysis.md` | `docs/analysis` | Analysis | `actual-analysis` | already in target Analysis path; future standard should modernize metadata/sections | Анализ эксперимента «Задача 1027» |
| `docs/analysis/2026-06-21-industry-inventory.md` | `docs/analysis` | Research | `masked-research-in-analysis-path` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Industry Inventory — аналитическое доисследование для дозаполнения реестра (issue #168) |
| `docs/analysis/2026-06-21-voice-digital-channels-comparison.md` | `docs/analysis` | Analysis | `actual-analysis` | already in target Analysis path; future standard should modernize metadata/sections | Сравнительный анализ: голосовые vs текстовые каналы в Industry Taxonomy (ADR-011) |
| `docs/analysis/2026-06-22-issue-170-mango-inventory.md` | `docs/analysis` | Analysis | `actual-analysis` | already in target Analysis path; future standard should modernize metadata/sections | Инвентаризация Mango-реестра и перевод в JSON (issue #170) |
| `docs/analysis/2026-06-22-mango-taxonomy-convergence-test.md` | `docs/analysis` | Audit | `masked-audit-in-analysis-path` | route by future Audit standard; do not absorb into Analysis | Тест на сходимость маппинга Mango Taxonomy на Industry Taxonomy |
| `docs/analysis/2026-06-22-rfc-industry-taxonomy-improvement.md` | `docs/analysis` | RFC | `masked-rfc-in-analysis-path` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: доработка Industry Taxonomy после теста на сходимость |
| `docs/analysis/2026-06-22-rfc-mango-taxonomy-improvement.md` | `docs/analysis` | RFC | `masked-rfc-in-analysis-path` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: доработка Mango Taxonomy после теста на сходимость |
| `docs/analysis/2026-06-22-rfc-rules-registry-system.md` | `docs/analysis` | RFC | `masked-rfc-in-analysis-path` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Rules Registry System для управления правилами создания артефактов |
| `docs/analysis/2026-06-22-rfc-taxonomy-extension-mechanism.md` | `docs/analysis` | RFC | `masked-rfc-in-analysis-path` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: системный механизм расширения таксономий (Industry + Mango) |
| `docs/analysis/2026-06-22-taxonomy-convergence-test.md` | `docs/analysis` | Audit | `masked-audit-in-analysis-path` | route by future Audit standard; do not absorb into Analysis | Тест на сходимость классификации функций по Industry Taxonomy Standard |
| `docs/analysis/2026-06-23-approval-contract-test-industry-rfc.md` | `docs/analysis` | Audit | `masked-audit-in-analysis-path` | route by future Audit standard; do not absorb into Analysis | Тест контракта согласования: RFC Industry Taxonomy |
| `docs/analysis/2026-06-23-executable-contracts-and-rfc-problems.md` | `docs/analysis` | Analysis | `actual-analysis` | already in target Analysis path; future standard should modernize metadata/sections | Систематизация проблем исполнимых контрактов и RFC |
| `docs/analysis/2026-06-23-repository-structure-analysis.md` | `docs/analysis` | Analysis | `actual-analysis` | already in target Analysis path; future standard should modernize metadata/sections | Аналитическое исследование структуры каталогов проекта (обоснование архитектуры) |
| `docs/analysis/2026-06-24-artifact-chain-hypothesis-research.md` | `docs/analysis` | Research | `masked-research-in-analysis-path` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Исследование гипотезы цепочки артефактов |
| `docs/analysis/2026-06-24-naming-convention-audit.md` | `docs/analysis` | Audit | `masked-audit-in-analysis-path` | route by future Audit standard; do not absorb into Analysis | Аудит нарушений naming convention |
| `docs/analysis/2026-06-24-runs-contract-log-policy-audit.md` | `docs/analysis` | Audit | `masked-audit-in-analysis-path` | route by future Audit standard; do not absorb into Analysis | Аудит контракта runs: Markdown-логи |
| `docs/analysis/2026-06-25-ba-processes-industry-analysis.md` | `docs/analysis` | Research | `masked-research-in-analysis-path` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Структурный анализ БА-процессов и артефактов с опорой на индустриальные практики телекома |
| `docs/analysis/2026-06-25-bcreq-fr-contract-process-analysis.md` | `docs/analysis` | Analysis | `actual-analysis` | already in target Analysis path; future standard should modernize metadata/sections | Структурный анализ применения контракта BCREQ-FR: монолитный промпт против последовательности операций |
| `docs/analysis/2026-06-25-runs-observability-research.md` | `docs/analysis` | Research | `masked-research-in-analysis-path` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Исследование трассируемости промптов в runs и внешних практик контроля проходов |
| `docs/analysis/2026-06-25-telecom-vendors-ba-practices-research.md` | `docs/analysis` | Research | `masked-research-in-analysis-path` | keep under Research routing unless future Analysis standard cites it as upstream evidence | Эмпирическая база: BA/Requirements-практики телеком-вендоров и операторов |
| `docs/audit/initial-state-2026-06.md` | `docs/audit` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Аудит и план миграции `mango_ba_prompts` (2026-06) |
| `docs/audit/issue-115-kb-pipeline.md` | `docs/audit` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Issue #115 — аудит KB Pipeline #11 |
| `docs/audit/issue-144-kb-structure.md` | `docs/audit` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Аудит структуры `kb/` после миграции product docs |
| `docs/audit/issue-146-mango-taxonomy-validation.md` | `docs/audit` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Issue #146: Mango Taxonomy validation on processed product docs |
| `docs/audit/taxonomy-standards-independent-review.md` | `docs/audit` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Независимый аудит двух стандартов таксономии командой экспертов |
| `governance/BACKLOG.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Бэклог Mango BA Prompts |
| `governance/agent-onboarding-protocol.executable.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Agent Onboarding Protocol — executable layer |
| `governance/agent-onboarding-protocol.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Agent Onboarding — Протокол бесшовной передачи проекта |
| `governance/approval-contract.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Контракт AI-агента: итеративное согласование документов |
| `governance/artifact-map.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Artifact Map — mango_ba_prompts |
| `governance/audit-contracts-2026-06-17.md` | `governance` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Аудит контрактов — отладка и изменение промптов (2026-06-17) |
| `governance/audit-contracts-mango-2026-06-17.md` | `governance` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Аудит контрактов mango_ba_prompts (2026-06-17) |
| `governance/audit-hub-2026-06-17.md` | `governance` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Аудит документов Хаба для mango_ba_prompts (2026-06-17) |
| `governance/audit-research-1027.md` | `governance` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | Аудит исследования — эксперимент «Задача 1027» (issue #101) |
| `governance/bcreq-fr-generation-contract.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | - |
| `governance/contracts-registry.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Реестр исполнимых контрактов |
| `governance/knowledge-transfer-to-hub/README.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Передача знаний в Хаб — уникальные практики mango_ba_prompts |
| `governance/knowledge-transfer-to-hub/ba-ontology.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Передача знаний: онтология бизнес-анализа (граф Артефакт↔Процесс↔Операция) |
| `governance/knowledge-transfer-to-hub/bcreq-process.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Передача знаний: процесс формирования BCREQ (бизнес- и системных требований) |
| `governance/knowledge-transfer-to-hub/operations-taxonomy.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Передача знаний: таксономия когнитивных операций БА |
| `governance/knowledge-transfer-to-hub/pages-ux.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Передача знаний: UX дерева процессов на GitHub Pages |
| `governance/migration-issues-registry.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Реестр созданных issues для Фазы 1 миграции |
| `governance/migration-manifest.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Migration Manifest — mango_ba_prompts |
| `governance/migration-phase1-issues.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Migration Phase 1 — 9 executable issues (M-001 … M-009) |
| `governance/prompt-debugging-process.md` | `governance` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | Процесс отладки промптов (Draft) |
| `governance/rfc-generation-contract.md` | `governance` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | - |
| `governance/rfc-process.md` | `governance` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC-процесс mango_ba_prompts (интеграция процесса Хаба) |
| `governance/rfc-register.md` | `governance` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | Реестр RFC (живой документ) |
| `governance/rfc-to-hub-001-knowledge-transfer.md` | `governance` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC в Хаб 001: передача уникальных практик БА (онтология, таксономия, BCREQ, Pages UX) |
| `governance/rfc-to-hub-002-prompt-debugging-process.md` | `governance` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC в Хаб 002: процесс отладки промптов как общая практика |
| `governance/rfc/ba-processes-observability-implementation-proposal.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC-243: предложение по БА-процессам и observability |
| `governance/rfc/bcreq-ft-scope-formation-rules-proposal.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Правила формирования скоупа bcreq ФТ (что описываем, а что исключаем) |
| `governance/rfc/prompt-improvement-bcreq-1025-proposal.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Улучшение промптов на основе эксперимента BCREQ-1025 |
| `governance/rfc/prompt-improvement-multichannel-proposal.md` | `governance/rfc` | RFC | `adjacent-not-analysis` | keep as proposal/RFC; Analysis can cite it as downstream or upstream context | RFC: Улучшение промптов на основе эксперимента «Многоканальная нагрузка агента» |
| `governance/session-digests.md` | `governance` | Report | `adjacent-not-analysis` | route by Reports standard / docs/report profile, not Analysis | Session Digests — Mango BA Prompts |
| `governance/sync-matrix-2026-06-17.md` | `governance` | Report | `adjacent-not-analysis` | route by Reports standard / docs/report profile, not Analysis | Матрица синхронизации mango_ba_prompts ↔ Хаб (2026-06-17) |

## Clarify / clarify-engine-ai

| Path | Bucket | Actual type | Relation | Hint | Title |
| --- | --- | --- | --- | --- | --- |
| `docs/analysis/2026-05-12_review_mvp-context_v1.md` | `docs/analysis` | Analysis | `actual-analysis` | already in target Analysis path; future standard should modernize metadata/sections | ⚠️ WARNING: ANALYTICAL DOCUMENT ONLY |
| `docs/analysis/2026-05-13_analysis_next-docs-implementation-task_v1.md` | `docs/analysis` | Analysis | `actual-analysis` | already in target Analysis path; future standard should modernize metadata/sections | ⚠️ WARNING: ANALYTICAL DOCUMENT ONLY |
| `docs/analysis/2026-05-15_analysis_repo-state-and-mvp-recommendations_v1.md` | `docs/analysis` | Analysis | `actual-analysis` | already in target Analysis path; future standard should modernize metadata/sections | Анализ состояния репозитория и рекомендации по MVP |
| `docs/analysis/2026-05-17_analysis_tz-structure_samples.md` | `docs/analysis` | Analysis | `actual-analysis` | already in target Analysis path; future standard should modernize metadata/sections | 🔍 Анализ структуры входных ТЗ (`.xlsx` / `.docx` / `.doc`) и матрица изменений под `.docx`-поддержку |
| `docs/analysis/2026-05-17_sprint-1-execution-report_v1.md` | `docs/analysis` | Report | `masked-report-in-analysis-path` | route by Reports standard / docs/report profile, not Analysis | Sprint-1 P0 — Execution Report (issue #87) |
| `docs/analysis/2026-05-19_code-review-triage_v1.md` | `docs/analysis` | Audit | `masked-audit-in-analysis-path` | route by future Audit standard; do not absorb into Analysis | Верификация замечаний Code Review (BL-26) |
| `docs/analysis/2026-05-19_sprint-5-kickoff_v1.md` | `docs/analysis` | Report | `masked-report-in-analysis-path` | route by Reports standard / docs/report profile, not Analysis | Sprint 5 — UX Polish & Documentation Sync — Kickoff (issue #192) |
| `docs/analysis/2026-05-20_sprint-4-kickoff_v1.md` | `docs/analysis` | Report | `masked-report-in-analysis-path` | route by Reports standard / docs/report profile, not Analysis | Sprint 4 — Pilot Readiness & Automation — Kickoff (issue #187) |
| `docs/analysis/2026-05-20_sprint-4-parallel-kickoff_v1.md` | `docs/analysis` | Report | `masked-report-in-analysis-path` | route by Reports standard / docs/report profile, not Analysis | Sprint 4 Parallel — BL-48 Installer PoC — Kickoff (issue #190) |
| `docs/analysis/README.md` | `docs/analysis` | Other | `masked-other-in-analysis-path` | no B-028 move candidate unless a future standard names it | 📂 docs/analysis/ |
| `docs/analysis/metadata-coverage-fix_v1.md` | `docs/analysis` | Analysis | `actual-analysis` | already in target Analysis path; future standard should modernize metadata/sections | Metadata Coverage Fix — Section Propagation (issue #109) |
| `docs/analysis/sprint-execution-report_template.md` | `docs/analysis` | Report | `masked-report-in-analysis-path` | route by Reports standard / docs/report profile, not Analysis | Sprint [N] Execution Report |
| `docs/audit/2026-05-12_repository-consistency_audit_v1.md` | `docs/audit` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | 🔍 Audit: Repository Consistency & Testability |
| `docs/audit/2026-05-16_post-implementation-audit-#53_v1.md` | `docs/audit` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | 🔍 Post-Implementation Audit: Issue #53 |
| `docs/audit/2026-05-19_bl-34_architecture-consistency-audit_v1.md` | `docs/audit` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | 📊 Architecture Consistency Audit — BL-34 |
| `docs/audit/2026-05-20_bl-43-smoke-e2e-report_v1.md` | `docs/audit` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | 📊 Post-fix Smoke & E2E Verification — BL-43 (ARM Deployment Readiness) |
| `docs/audit/2026-05-20_bl-57_comprehensive-verification_v1.md` | `docs/audit` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | BL-57 Comprehensive Verification — UI / Code / Docs Alignment Before Pilot |
| `docs/audit/README.md` | `docs/audit` | Other | `adjacent-not-analysis` | no B-028 move candidate unless a future standard names it | 📂 docs/audit/ |
| `docs/audit/data-masking_v1.md` | `docs/audit` | Audit | `adjacent-not-analysis` | route by future Audit standard; do not absorb into Analysis | 🔒 Audit: Data Masking Implementation |
