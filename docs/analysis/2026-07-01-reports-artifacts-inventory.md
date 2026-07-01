---
status: draft
version: 0.1
updated: 2026-07-01
temperature: 0.1
type: internal-analysis
context: [hub, mango, clarify, reports, audit-report, general-report, statistical-report, inventory, issue-310, b-038]
method: repository-scan + content-classification
scope: ecosystem
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/310"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/310"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/307"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/288"
related_artifacts:
  - "research/hub/2026-06-30-reports-industry-norms-and-standardization-scope.md"
  - "research/hub/2026-06-28-research-analysis-audit-inventory.md"
  - "research/hub/exp/reports-inventory-310/2026-07-01-reports-artifact-matrix.md"
  - "research/hub/exp/reports-inventory-310/scan-reports.py"
  - "docs/adr/2026-06-adr-002-artifact-document-methodology.md"
  - "research/hub/2026-06-23-repository-structure-concept.md"
external_artifacts:
  - "G-Ivan-A/mango_ba_prompts@995c16d175f916ae397d0efc2231f8d30f82c518"
  - "G-Ivan-A/clarify-engine-ai@96c288fd13a2d7cc7c3e3cdd52574944858e6255"
---

# Reports artifacts: inventory and boundaries

> Режим: Analysis для issue
> [#310](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/310).
> Документ не создаёт RFC, ADR, стандарт Reports, новые директории и не
> переносит файлы. Он фиксирует фактическую картину Reports-артефактов в Hub,
> Mango и Clarify как вход для следующей цепочки стандартизации.
> Короткая граница: этот анализ не переносит файлы.

## 1. Введение

### 1.1. Причина

В видении фаундера Reports выделены как отдельный тип артефактов с подтипами
`аудит / отчёт / статистика` и с целевым базовым размещением в `docs/report/`.
На момент анализа в трёх репозиториях такие результаты уже существуют, но они
распределены по `docs/audit/`, `docs/analysis/`, `research/`, `governance/`,
`docs/project-summaries/` и одному текущему пути `reports/report/`.

Без инвентаризации нельзя корректно создать Reports standard: часть файлов
является результатом Audit-процесса, часть результатом Analysis/Research, а
часть самостоятельными summary/report документами. Если стандартизировать всё
как один плоский "отчёт", стандарт начнёт конфликтовать с будущими стандартами
Analysis и Audit.

### 1.2. Охват и снимки

Сканировались tracked text files в `reports/`, `docs/`, `research/` и
`governance/`. Внешние репозитории использовались только как read-only corpus.

| Repo | Snapshot | Scanned paths |
| --- | --- | --- |
| Hub / `hybrid-Intelligence-lab` | `d0fd509837a56620b4e0c2100edf01df96fa98af` | `reports/**`, `docs/**`, `research/**`, `governance/**` |
| Mango / `mango_ba_prompts` | `995c16d175f916ae397d0efc2231f8d30f82c518` | `reports/**`, `docs/**`, `research/**`, `governance/**` |
| Clarify / `clarify-engine-ai` | `96c288fd13a2d7cc7c3e3cdd52574944858e6255` | `reports/**`, `docs/**`, `research/**`, `governance/**` |

Собственные deliverables issue #310 исключены из Hub baseline, чтобы повторный
запуск после merge не менял матрицу из-за добавленных этим PR файлов.

### 1.3. Метод

Классификация опиралась на фактическую роль результата, а не только на путь.
Воспроизводимый scan лежит в
[reports-inventory-310/2026-07-01-reports-artifact-matrix.md](../../research/hub/exp/reports-inventory-310/2026-07-01-reports-artifact-matrix.md);
скрипт:
[reports-inventory-310/scan-reports.py](../../research/hub/exp/reports-inventory-310/scan-reports.py).

| Поле | Рабочий критерий |
| --- | --- |
| `audit` | результат проверки, верификации, compliance review, smoke/E2E проверки, contract test или code review triage. |
| `report` | narrative summary, project/session context, experiment report, retrospective, execution report или другой общий отчёт без доминирующей проверки на норму. |
| `statistics` | inventory, scan, matrix, registry summary, counts или другая табличная/statistical фиксация состояния. |
| `output-for-audit` | Report-подтип является выходом Audit-процесса и требует согласования с будущим Audit standard. |
| `output-for-analysis` | Report-подтип является evidence/result layer для Analysis или Research. |
| `standalone-report` | самостоятельный отчёт/context summary, не привязанный к одному Analysis/Audit артефакту. |

Матрица является evidence layer. Этот документ фиксирует интерпретацию,
границы, modernization candidates и рекомендацию по scope стандартизации.

## 2. Сводная матрица

Полная таблица по каждому найденному артефакту находится в
[Reports artifact candidate matrix](../../research/hub/exp/reports-inventory-310/2026-07-01-reports-artifact-matrix.md).
Она содержит path, текущий path bucket, фактический subtype, relation, routing
hint и заголовок для каждого кандидата.

| Repo | Scanned text | Reports candidates | Audit subtype | Report subtype | Statistics subtype | Output for audit | Output for analysis | Standalone |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Hub / `hybrid-Intelligence-lab` | 106 | 19 | 6 | 8 | 5 | 6 | 8 | 5 |
| Mango / `mango_ba_prompts` | 83 | 20 | 15 | 2 | 3 | 15 | 3 | 2 |
| Clarify / `clarify-engine-ai` | 70 | 8 | 7 | 1 | 0 | 7 | 1 | 0 |
| **Total** | **259** | **47** | **28** | **11** | **8** | **28** | **12** | **7** |

### 2.1. Hub

| Current bucket | Count | Actual subtypes | Interpretation |
| --- | ---: | --- | --- |
| `docs/audit` | 2 | audit | Audit reports already placed in an audit path; future move depends on Report/Audit boundary. |
| `docs/project-summaries` | 3 | report | Standalone project context reports; strong candidates for a general Report profile under `docs/report/` after standard approval. |
| `governance` | 1 | report | `session-digests.md` behaves as a rolling standalone report/log. |
| `reports` | 1 | report | Historical noncanonical report-like path from the fixed scan snapshot; canonical target is `docs/report/` (singular). |
| `research` | 12 | audit, report, statistics | Research/analysis outputs and evidence matrices; keep as research evidence until a standard defines publishable Report mirrors. |

### 2.2. Mango

| Current bucket | Count | Actual subtypes | Interpretation |
| --- | ---: | --- | --- |
| `docs/analysis` | 7 | audit, statistics | Mixed analysis path: inventories and test/audit outputs live together. |
| `docs/audit` | 5 | audit | Audit reports with consistent process stance but inconsistent future Report/Audit routing. |
| `docs` | 1 | report | `docs/kb-experiment-report.md` is a standalone experiment report. |
| `docs/reviews` | 1 | audit | Human review behaves like audit/report output. |
| `governance` | 6 | audit, report, statistics | Operational audit/report artifacts hidden in governance. |

### 2.3. Clarify

| Current bucket | Count | Actual subtypes | Interpretation |
| --- | ---: | --- | --- |
| `docs/analysis` | 2 | report, audit | Execution report and code-review triage are report-like outputs under Analysis. |
| `docs/audit` | 6 | audit | Verification/audit reports with strong Audit-process stance. |

## 3. Boundaries: Reports ↔ Analysis ↔ Audit

| Boundary | Decision rule for this inventory | Consequence for standardization |
| --- | --- | --- |
| Reports vs Analysis | Report records "what was observed, measured, verified, or summarized"; Analysis explains "why it matters / how to interpret / what options follow." | Statistical matrices and retrospectives can be Report subtypes, but their parent analysis remains Analysis. |
| Reports vs Audit | Audit is the process/stance: check against a norm, contract or expected behavior. Audit report is the durable output of that process. | Audit-report profile must not replace the future Audit standard; it should describe the output shape only. |
| Reports vs Research evidence | Experiment outputs can be report-like, but they are part of reproducible evidence packages. | Do not move `research/hub/exp-*` outputs before a research-evidence policy decides whether publishable report mirrors are needed. |
| Standalone report vs process output | Standalone reports are durable summaries/context records; process outputs are tied to Analysis/Audit work. | A base Report standard should support both, but require `based_on` / `source` / `scope` metadata for process outputs. |

Practical boundary: "Report" should be a document genre, not a competing
process. A document can be an `audit report` or `statistics report` while its
parent work remains Audit, Analysis or Research.

## 4. Duplicates, substitutions and drift

| Finding | Evidence | Classification |
| --- | --- | --- |
| Path drift existed in the scan snapshot | Issue #310 and founder vision use `docs/report/`; ADR-002 mentions `docs/reports/`; the fixed Hub snapshot had `reports/report/2026-06-30-pr-303-rfc-hypothesis-analysis.md`. PR review later fixed the canonical target as `docs/report/` (singular). | No longer a path-choice blocker; future migration should use `docs/report/`. |
| Audit outputs dominate Reports candidates | 28 of 47 candidates are `audit` subtype; Mango has 15 audit outputs, Clarify has 7. | Report/Audit substitution risk. |
| Mango mixes audit and statistics under Analysis | `docs/analysis/*inventory*`, `*convergence-test*`, `*audit*`, `*contract-test*`. | Analysis path is being used as generic "work result" container. |
| Hub research contains report-like evidence outputs | Prior matrices and scans under `research/hub/exp-*` plus retrospectives and inventories under `research/hub/`. | Research evidence vs publishable Report boundary is not standardized. |
| Standalone summaries are scattered | Hub project summaries and session digests; Mango session digests and KB experiment report. | General Report profile candidate. |
| Review/audit wording overlaps | Mango `docs/reviews/migration-rfc-human-review-2026-06.md` and Clarify code-review triage behave as audit reports. | Future standard needs relation fields, not only path rules. |

Potential duplicates are mostly semantic overlaps, not safe delete candidates:

| Group | Assessment | Recommended treatment |
| --- | --- | --- |
| Hub project summaries vs session digests | Different cadence and purpose: project context snapshot vs session-level rolling summary. | Keep; future Report profile should distinguish `project-summary` and `session-digest`. |
| Mango `2026-06-22-mango-taxonomy-convergence-test.md` vs `2026-06-22-taxonomy-convergence-test.md` | Related convergence tests with different taxonomy scope. | Keep; add `scope`/`supersedes` only if future Mango cleanup confirms overlap. |
| Mango `audit-contracts-2026-06-17.md` vs `audit-contracts-mango-2026-06-17.md` | Likely overlapping audit contract records. | Candidate for future duplicate review; do not delete in this analysis. |
| Clarify audit series | Repeated audit pattern, but each file targets different issue/system slice. | Keep; modernization is naming/frontmatter consistency, not deletion. |

## 5. Move, delete and modernization candidates

This issue should not move files. The following table records candidates for
future work after a Reports standard exists; the canonical target path is
`docs/report/`.

| Candidate class | Examples | Future action |
| --- | --- | --- |
| General standalone reports | Hub `docs/project-summaries/*`, Hub/Mango `governance/session-digests.md`, Mango `docs/kb-experiment-report.md`, Clarify sprint execution report. | Candidate for `docs/report/` general profile after standard approval. |
| Statistics outputs | Hub/Mango inventory/matrix/scan outputs, Mango sync matrix. | Candidate for statistics profile; experiment outputs may stay in `exp-*` with optional publishable mirror. |
| Audit reports | Hub/Mango/Clarify audit, validation, verification, review and smoke/E2E outputs. | Do not move before Audit standard boundary; later tag as Report subtype + Audit process output. |
| Research retrospectives and executive summaries | Hub AI collaboration retrospectives; reputation executive summary. | Candidate for general report profile only if future policy wants reports outside research corpus. |
| Possible duplicate audits | Mango audit-contracts pair and related taxonomy convergence tests. | Review for `supersedes`, `scope`, `related_artifacts`; no deletion now. |

Modernization should focus on metadata before physical migration:

1. Add explicit `report-subtype` / `artifact-subtype` vocabulary after standard
   approval: `audit`, `report`, `statistics`.
2. Add relation metadata: `based_on`, `source`, `scope`, `supersedes`,
   `related_artifacts`.
3. Normalize title/path conventions only after standard approval, using
   `docs/report/` as the canonical target path.
4. Keep reproducible experiment outputs attached to their experiment directory
   unless the standard defines a second published Report artifact.

## 6. Standardization recommendation

The inventory supports the recommendation from
[Reports industry norms and standardization scope](../../research/hub/2026-06-30-reports-industry-norms-and-standardization-scope.md):
Variant C, one base Report standard plus light subtype profiles.

Recommended scope for the next standardization chain:

| Layer | Include | Exclude |
| --- | --- | --- |
| Base Report standard | Purpose, frontmatter, relation metadata, evidence links, lifecycle states, minimum sections for durable result records. | Audit methodology, analysis method, research methodology. |
| Audit report profile | Output structure for verification/compliance/audit results. | Normative Audit process; belongs to future Audit standard. |
| General report profile | Project summaries, session digests, experiment reports, retrospectives, execution reports. | Product docs, guides, RFCs, ADRs and standards. |
| Statistics report profile | Inventory/matrix/scan/sync outputs and machine-readable evidence summaries. | Raw datasets unless curated as report outputs. |

Open decisions before migration:

| Decision | Why it matters |
| --- | --- |
| Whether audit outputs live physically under Reports or Audit | The inventory shows audit reports are the largest group, so the boundary must be explicit. |
| Whether experiment output matrices are Reports | They are report-like, but also reproducible evidence. Moving them can break research traceability. |

## 7. Status review against issue #310

| Requirement | Status | Evidence |
| --- | --- | --- |
| Matrix across Hub, Mango, Clarify | Done | [2026-07-01-reports-artifact-matrix.md](../../research/hub/exp/reports-inventory-310/2026-07-01-reports-artifact-matrix.md) |
| Actual type/subtype per artifact | Done | Matrix fields `Subtype` and `Relation` for 47 candidates. |
| Duplicates/substitutions/modernization candidates | Done | Sections 4 and 5. |
| Boundaries Reports vs Analysis vs Audit | Done | Section 3. |
| Move/delete/modernization candidates | Done | Section 5; no physical moves in this PR. |
| Recommendation on standardization scope | Done | Section 6; Variant C confirmed for this corpus. |
| Task status review | Done | B-038 should move from TODO to review in `governance/backlog.md`; PR #312 contains this analysis and evidence. |

Conclusion: Reports should be standardized as a durable output/document genre
with three light profiles (`audit`, `report`, `statistics`). The standard must
coordinate with Analysis and Audit rather than absorb them. Physical migration
is a later task after the Reports standard and Report/Audit boundary are
approved; the canonical Reports path is `docs/report/`.
