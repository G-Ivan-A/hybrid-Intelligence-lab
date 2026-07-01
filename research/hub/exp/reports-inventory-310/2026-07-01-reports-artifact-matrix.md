---
status: draft
version: 0.1
updated: 2026-07-01
temperature: 0.1
---

# Reports artifact candidate matrix

Generated for issue #310. Classification is heuristic and evidence-oriented:
path is only a signal; title and frontmatter are used to detect
audit, general report and statistical report candidates. The written analysis
document performs the final human-readable synthesis and recommendations.

## Repository snapshots

| Repo | URL | SHA |
| --- | --- | --- |
| Hub / hybrid-Intelligence-lab | https://github.com/G-Ivan-A/hybrid-Intelligence-lab | `d0fd509837a56620b4e0c2100edf01df96fa98af` |
| Mango / mango_ba_prompts | https://github.com/G-Ivan-A/mango_ba_prompts | `995c16d175f916ae397d0efc2231f8d30f82c518` |
| Clarify / clarify-engine-ai | https://github.com/G-Ivan-A/clarify-engine-ai | `96c288fd13a2d7cc7c3e3cdd52574944858e6255` |

## Summary

| Repo | Scanned text | Candidates | Audit | Report | Statistics | Output for audit | Output for analysis | Standalone |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Hub / hybrid-Intelligence-lab | 106 | 19 | 6 | 8 | 5 | 6 | 8 | 5 |
| Mango / mango_ba_prompts | 83 | 20 | 15 | 2 | 3 | 15 | 3 | 2 |
| Clarify / clarify-engine-ai | 70 | 8 | 7 | 1 | 0 | 7 | 1 | 0 |

## Current Path Buckets

| Repo | Bucket | Candidates |
| --- | --- | ---: |
| Hub / hybrid-Intelligence-lab | `docs/audit` | 2 |
| Hub / hybrid-Intelligence-lab | `docs/project-summaries` | 3 |
| Hub / hybrid-Intelligence-lab | `governance` | 1 |
| Hub / hybrid-Intelligence-lab | `reports` | 1 |
| Hub / hybrid-Intelligence-lab | `research` | 12 |
| Mango / mango_ba_prompts | `docs` | 1 |
| Mango / mango_ba_prompts | `docs/analysis` | 7 |
| Mango / mango_ba_prompts | `docs/audit` | 5 |
| Mango / mango_ba_prompts | `docs/reviews` | 1 |
| Mango / mango_ba_prompts | `governance` | 6 |
| Clarify / clarify-engine-ai | `docs/analysis` | 2 |
| Clarify / clarify-engine-ai | `docs/audit` | 6 |

## Hub / hybrid-Intelligence-lab

| Path | Bucket | Subtype | Relation | Hint | Title |
| --- | --- | --- | --- | --- | --- |
| `docs/audit/2026-06-29-research-artifact-format-contract-audit.md` | `docs/audit` | audit | output-for-audit | future Report/Audit boundary decision before moving | Audit: Research artifact format contract |
| `docs/audit/task-execution-audit-2026-06.md` | `docs/audit` | audit | output-for-audit | future Report/Audit boundary decision before moving | Аудит выполненных задач (1-4) |
| `docs/project-summaries/clarify-engine-ai-context-Summary.md` | `docs/project-summaries` | report | standalone-report | candidate for docs/report general report profile after standard | Контекст проекта clarify-engine-ai (Summary) |
| `docs/project-summaries/mango-ba-prompts-context-Summary.md` | `docs/project-summaries` | report | standalone-report | candidate for docs/report general report profile after standard | Контекст проекта mango_ba_prompts (Summary) |
| `docs/project-summaries/open-ai-ru-context-Summary.md` | `docs/project-summaries` | report | standalone-report | candidate for docs/report general report profile after standard | Контекст проекта open-ai.ru (Summary) |
| `governance/session-digests.md` | `governance` | report | standalone-report | candidate for docs/report general report profile after standard | Session Digests — суммарии сессий |
| `reports/report/2026-06-30-pr-303-rfc-hypothesis-analysis.md` | `reports` | report | standalone-report | already-report-path; path spelling unresolved | Отчет по гипотезе проблемы PR #303 |
| `research/hub/2026-05-28-prompts-classification-audit.md` | `research` | audit | output-for-audit | future Report/Audit boundary decision before moving | Аудит входных данных для классификации промптов |
| `research/hub/2026-06-01-team-c-governance-strategy-audit.md` | `research` | audit | output-for-audit | future Report/Audit boundary decision before moving | Интерпретация аудита стратегии governance от команды C |
| `research/hub/2026-06-02-ai-collaboration-retrospective-mango-migration.md` | `research` | report | output-for-analysis | candidate for docs/report general report profile after standard | Ретроспектива AI-collaboration: сессия проектирования миграции Mango (Хаб → спок) |
| `research/hub/2026-06-02-ai-collaboration-retrospective.md` | `research` | report | output-for-analysis | candidate for docs/report general report profile after standard | Ретроспектива AI-collaboration по сессии проектирования шаблонов споков |
| `research/hub/2026-06-12-ecosystem-governance-audit.md` | `research` | audit | output-for-audit | future Report/Audit boundary decision before moving | Ecosystem Governance Audit |
| `research/hub/2026-06-25-artifact-inventory-and-classification.md` | `research` | statistics | output-for-analysis | candidate for docs/report statistics profile after standard | Инвентаризация и классификация артефактов экосистемы (mango_ba_prompts + hybrid-Intelligence-lab) |
| `research/hub/2026-06-28-research-analysis-audit-inventory.md` | `research` | statistics | output-for-analysis | candidate for docs/report statistics profile after standard | Research / Analysis / Audit: инвентаризация и план стандартизации |
| `research/hub/exp-research-analysis-audit-288/outputs/2026-06-28-artifact-classification-matrix.md` | `research` | statistics | output-for-analysis | candidate for docs/report statistics profile after standard | Research/Analysis/Audit artifact classification matrix |
| `research/hub/exp-rfc-adr-industry-norms/outputs/2026-06-27-adr-external-tree-summary.md` | `research` | statistics | output-for-analysis | candidate for docs/report statistics profile after standard | ADR external source tree summary |
| `research/hub/exp-rfc-adr-industry-norms/outputs/2026-06-27-local-rfc-adr-audit.md` | `research` | audit | output-for-audit | future Report/Audit boundary decision before moving | Local ecosystem RFC/ADR audit |
| `research/hub/exp-ripple-effects-282/outputs/2026-06-28-frontmatter-scan.md` | `research` | statistics | output-for-analysis | candidate for docs/report statistics profile after standard | Frontmatter scan for issue 284 |
| `research/reputation-technologies/2026-06-20-executive-summary.ru-en.md` | `research` | report | output-for-analysis | candidate for docs/report general report profile after standard | Executive Summary — GRA Reputation Framework (RU + EN) |

## Mango / mango_ba_prompts

| Path | Bucket | Subtype | Relation | Hint | Title |
| --- | --- | --- | --- | --- | --- |
| `docs/analysis/2026-06-21-industry-inventory.md` | `docs/analysis` | statistics | output-for-analysis | candidate for docs/report statistics profile after standard | Industry Inventory — аналитическое доисследование для дозаполнения реестра (issue #168) |
| `docs/analysis/2026-06-22-issue-170-mango-inventory.md` | `docs/analysis` | statistics | output-for-analysis | candidate for docs/report statistics profile after standard | Инвентаризация Mango-реестра и перевод в JSON (issue #170) |
| `docs/analysis/2026-06-22-mango-taxonomy-convergence-test.md` | `docs/analysis` | audit | output-for-audit | future Report/Audit boundary decision before moving | Тест на сходимость маппинга Mango Taxonomy на Industry Taxonomy |
| `docs/analysis/2026-06-22-taxonomy-convergence-test.md` | `docs/analysis` | audit | output-for-audit | future Report/Audit boundary decision before moving | Тест на сходимость классификации функций по Industry Taxonomy Standard |
| `docs/analysis/2026-06-23-approval-contract-test-industry-rfc.md` | `docs/analysis` | audit | output-for-audit | future Report/Audit boundary decision before moving | Тест контракта согласования: RFC Industry Taxonomy |
| `docs/analysis/2026-06-24-naming-convention-audit.md` | `docs/analysis` | audit | output-for-audit | future Report/Audit boundary decision before moving | Аудит нарушений naming convention |
| `docs/analysis/2026-06-24-runs-contract-log-policy-audit.md` | `docs/analysis` | audit | output-for-audit | future Report/Audit boundary decision before moving | Аудит контракта runs: Markdown-логи |
| `docs/audit/initial-state-2026-06.md` | `docs/audit` | audit | output-for-audit | future Report/Audit boundary decision before moving | Аудит и план миграции `mango_ba_prompts` (2026-06) |
| `docs/audit/issue-115-kb-pipeline.md` | `docs/audit` | audit | output-for-audit | future Report/Audit boundary decision before moving | Issue #115 — аудит KB Pipeline #11 |
| `docs/audit/issue-144-kb-structure.md` | `docs/audit` | audit | output-for-audit | future Report/Audit boundary decision before moving | Аудит структуры `kb/` после миграции product docs |
| `docs/audit/issue-146-mango-taxonomy-validation.md` | `docs/audit` | audit | output-for-audit | future Report/Audit boundary decision before moving | Issue #146: Mango Taxonomy validation on processed product docs |
| `docs/audit/taxonomy-standards-independent-review.md` | `docs/audit` | audit | output-for-audit | future Report/Audit boundary decision before moving | Независимый аудит двух стандартов таксономии командой экспертов |
| `docs/kb-experiment-report.md` | `docs` | report | standalone-report | candidate for docs/report general report profile after standard | Отчёт по эксперименту: машиночитаемая база знаний из PDF (issue #111) |
| `docs/reviews/migration-rfc-human-review-2026-06.md` | `docs/reviews` | audit | output-for-audit | future Report/Audit boundary decision before moving | Human Review: `2026-06-02-migration-strategy-rfc.md` (issue #13) |
| `governance/audit-contracts-2026-06-17.md` | `governance` | audit | output-for-audit | future Report/Audit boundary decision before moving | Аудит контрактов — отладка и изменение промптов (2026-06-17) |
| `governance/audit-contracts-mango-2026-06-17.md` | `governance` | audit | output-for-audit | future Report/Audit boundary decision before moving | Аудит контрактов mango_ba_prompts (2026-06-17) |
| `governance/audit-hub-2026-06-17.md` | `governance` | audit | output-for-audit | future Report/Audit boundary decision before moving | Аудит документов Хаба для mango_ba_prompts (2026-06-17) |
| `governance/audit-research-1027.md` | `governance` | audit | output-for-audit | future Report/Audit boundary decision before moving | Аудит исследования — эксперимент «Задача 1027» (issue #101) |
| `governance/session-digests.md` | `governance` | report | standalone-report | candidate for docs/report general report profile after standard | Session Digests — Mango BA Prompts |
| `governance/sync-matrix-2026-06-17.md` | `governance` | statistics | output-for-analysis | candidate for docs/report statistics profile after standard | Матрица синхронизации mango_ba_prompts ↔ Хаб (2026-06-17) |

## Clarify / clarify-engine-ai

| Path | Bucket | Subtype | Relation | Hint | Title |
| --- | --- | --- | --- | --- | --- |
| `docs/analysis/2026-05-17_sprint-1-execution-report_v1.md` | `docs/analysis` | report | output-for-analysis | candidate for docs/report general report profile after standard | Sprint-1 P0 — Execution Report (issue #87) |
| `docs/analysis/2026-05-19_code-review-triage_v1.md` | `docs/analysis` | audit | output-for-audit | future Report/Audit boundary decision before moving | Верификация замечаний Code Review (BL-26) |
| `docs/audit/2026-05-12_repository-consistency_audit_v1.md` | `docs/audit` | audit | output-for-audit | future Report/Audit boundary decision before moving | 🔍 Audit: Repository Consistency & Testability |
| `docs/audit/2026-05-16_post-implementation-audit-#53_v1.md` | `docs/audit` | audit | output-for-audit | future Report/Audit boundary decision before moving | 🔍 Post-Implementation Audit: Issue #53 |
| `docs/audit/2026-05-19_bl-34_architecture-consistency-audit_v1.md` | `docs/audit` | audit | output-for-audit | future Report/Audit boundary decision before moving | 📊 Architecture Consistency Audit — BL-34 |
| `docs/audit/2026-05-20_bl-43-smoke-e2e-report_v1.md` | `docs/audit` | audit | output-for-audit | future Report/Audit boundary decision before moving | 📊 Post-fix Smoke & E2E Verification — BL-43 (ARM Deployment Readiness) |
| `docs/audit/2026-05-20_bl-57_comprehensive-verification_v1.md` | `docs/audit` | audit | output-for-audit | future Report/Audit boundary decision before moving | BL-57 Comprehensive Verification — UI / Code / Docs Alignment Before Pilot |
| `docs/audit/data-masking_v1.md` | `docs/audit` | audit | output-for-audit | future Report/Audit boundary decision before moving | 🔒 Audit: Data Masking Implementation |
