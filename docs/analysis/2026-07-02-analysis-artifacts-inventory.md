---
status: draft
version: 0.1
updated: 2026-07-02
temperature: 0.1
type: internal-analysis
context: [hub, mango, clarify, analysis, inventory, issue-342, b-024]
method: repository-scan + content-classification
scope: ecosystem
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/342"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/342"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/296"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/288"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/328"
related_artifacts:
  - "research/hub/2026-06-28-research-analysis-audit-inventory.md"
  - "docs/analysis/2026-07-01-reports-artifacts-inventory.md"
  - "research/hub/exp/analysis-inventory-342/2026-07-02-analysis-artifact-matrix.md"
  - "research/hub/exp/analysis-inventory-342/scan-analysis.py"
  - "standards/glossary.md"
  - "standards/research-standard.md"
  - "docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md"
  - "docs/adr/2026-06-adr-002-artifact-document-methodology.md"
  - "docs/adr/2026-07-adr-003-research-structure.md"
  - "governance/backlog.md#b-024-analysis-сквозной-анализ-артефактов-analysis-хаб-mango-clarify"
external_artifacts:
  - "G-Ivan-A/mango_ba_prompts@52bc8b72419abb9548d9b6091623f18c080efae4"
  - "G-Ivan-A/clarify-engine-ai@96c288fd13a2d7cc7c3e3cdd52574944858e6255"
---

# Analysis artifacts: inventory and boundaries

> Режим: Analysis для issue
> [#342](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/342)
> и backlog B-024.
> Документ не создаёт RFC, не создаёт `analysis-standard.md`, не переносит
> файлы и не выполняет cleanup. Он фиксирует фактическую картину
> Analysis-adjacent артефактов в Hub, Mango и Clarify как вход для RFC B-025,
> стандарта Analysis и будущей модернизации B-028.
> Короткая граница: этот анализ не переносит файлы.

## 1. Введение

### 1.1. Причина

Issue #296 разделило цепочку стандартизации Research / Analysis / Audit на
самостоятельные ветки: Analysis standard не наследует Research standard и не
должен поглощать Audit или Report. Issue #288 дало первичную инвентаризацию
Research / Analysis / Audit, но перед RFC B-025 нужен отдельный срез именно по
Analysis: какие файлы фактически являются Analysis, какие только находятся в
`docs/analysis/`, и какие артефакты используют слово "analysis" как свободную
метку для Research, Audit, Report или RFC.

B-020 в backlog фиксирует терминологическую зависимость от glossary update.
На момент этого отчёта B-020 ещё не выполнен как отдельная задача, поэтому этот
документ использует рабочие критерии из `standards/glossary.md`,
`standards/research-standard.md`, ADR-001, ADR-002, ADR-003 и предыдущих
инвентаризаций. Нормативные определения остаются задачей B-020/B-025.

### 1.2. Охват и снимки

Сканировались tracked text files в `docs/analysis/`, `docs/report/`,
`docs/audit/`, `research/` и `governance/`. Внешние репозитории использовались
только как read-only corpus. Скрипт также принимает legacy alias
`docs/reports/`, чтобы старые snapshots не скрывали report-like artifacts; это
не является предложением создать или перенести такой путь.

| Repo | Snapshot | Scanned paths |
| --- | --- | --- |
| Hub / `hybrid-Intelligence-lab` | `3abae05d142284a98719c4549229b6c0099eeb65` | `docs/analysis/**`, `docs/report/**`, `docs/audit/**`, `research/**`, `governance/**` |
| Mango / `mango_ba_prompts` | `52bc8b72419abb9548d9b6091623f18c080efae4` | `docs/analysis/**`, `docs/report/**`, `docs/audit/**`, `research/**`, `governance/**` |
| Clarify / `clarify-engine-ai` | `96c288fd13a2d7cc7c3e3cdd52574944858e6255` | `docs/analysis/**`, `docs/report/**`, `docs/audit/**`, `research/**`, `governance/**` |

Собственные deliverables issue #342 исключены из Hub baseline, чтобы повторный
запуск после merge не считал новый отчёт и evidence-контейнер частью
исходного корпуса.

### 1.3. Метод

Воспроизводимый scan лежит в
[analysis-inventory-342/2026-07-02-analysis-artifact-matrix.md](../../research/hub/exp/analysis-inventory-342/2026-07-02-analysis-artifact-matrix.md);
скрипт:
[analysis-inventory-342/scan-analysis.py](../../research/hub/exp/analysis-inventory-342/scan-analysis.py).

Классификация опиралась на фактическую роль результата, а не только на путь.
Сигналы: path bucket, filename, title, frontmatter, ранний body text и
лексические признаки proposal/check/report/research/analysis. Матрица является
evidence layer; этот документ фиксирует интерпретацию, границы и candidates for
B-028.

| Тип | Рабочий критерий |
| --- | --- |
| `Research` | Генерация нового знания: внешние источники, industry/market benchmark, гипотеза, source-backed исследование или доменная модель. |
| `Analysis` | Интерпретация локального/внутреннего контекста, inventory, matrix, options или recommendation без доминирующей внешней research-части и без проверки на норму. |
| `Audit` | Проверка соответствия стандарту, contract, checklist, expected behavior или convergence condition; pass/fail stance и remediation. |
| `Report` | Описание выполненной работы, состояния, запуска, kickoff, execution summary, retrospective или другой "что произошло" результат. |
| `RFC` | Proposal/change record до decision gate, включая файлы с RFC intent даже при размещении вне `governance/rfc/`. |
| `ADR` | Accepted decision record. В просканированном scope ADR не найдено, потому что `docs/adr/**` не входит в issue #342. |
| `Other` | Navigation, template, policy, registry, contract, README или иной справочный артефакт. |

## 2. Сводная матрица

Полная таблица по каждому найденному артефакту находится в
[Analysis artifact candidate matrix](../../research/hub/exp/analysis-inventory-342/2026-07-02-analysis-artifact-matrix.md).
Она содержит path, текущий bucket, фактический тип, relation to Analysis,
routing hint и title.

| Repo | Scanned text | Research | Analysis | Audit | Report | RFC | ADR | Other | Non-text |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Hub / `hybrid-Intelligence-lab` | 110 | 37 | 8 | 8 | 13 | 24 | 0 | 20 | 14 |
| Mango / `mango_ba_prompts` | 57 | 5 | 6 | 14 | 2 | 14 | 0 | 16 | 2 |
| Clarify / `clarify-engine-ai` | 19 | 0 | 5 | 7 | 5 | 0 | 0 | 2 | 0 |
| **Total** | **186** | **42** | **19** | **29** | **20** | **38** | **0** | **38** | **16** |

Главный результат: фактических Analysis всего 19 из 186 scanned text
artifacts. Путь `docs/analysis/` не равен типу Analysis: у Mango и Clarify там
лежит существенная доля Research, Audit, Report и RFC.

### 2.1. Current path buckets

| Repo | Current bucket | Text artifacts | Actual type mix | Interpretation |
| --- | ---: | --- | --- | --- |
| Hub | `docs/analysis` | 2 | 2 Analysis | Текущий canonical path уже чистый в рамках baseline; обе записи являются входом для будущего Analysis standard. |
| Hub | `docs/audit` | 3 | 3 Audit | Соседний Audit corpus; не должен попадать в Analysis standard. |
| Hub | `docs/report` | 3 | 3 Report | Report path содержит files со словом analysis в названии, но по цели это reports. |
| Hub | `governance` | 6 | 1 Report, 5 Other | Governance navigation/logs; Analysis standard должен только ссылаться на них при необходимости. |
| Hub | `governance/rfc` | 21 | 20 RFC, 1 Other | Proposal corpus; RFC не является Analysis даже при использовании analytical rationale. |
| Hub | `research` | 75 | 37 Research, 6 Analysis, 5 Audit, 9 Report, 4 RFC, 14 Other | Исторический mixed corpus: часть локальных analyses живёт в `research/`, но физический перенос отложен до стандарта. |
| Mango | `docs/analysis` | 21 | 5 Research, 6 Analysis, 5 Audit, 5 RFC | Самый явный mixed Analysis path; 15 из 21 файлов замаскированы под Analysis. |
| Mango | `docs/audit` | 5 | 5 Audit | Audit path в целом соответствует фактическому типу. |
| Mango | `governance` | 27 | 4 Audit, 2 Report, 5 RFC, 16 Other | Operational governance смешивает policy, report, audit и proposal artifacts. |
| Mango | `governance/rfc` | 4 | 4 RFC | RFC corpus в ожидаемом routing. |
| Clarify | `docs/analysis` | 12 | 5 Analysis, 1 Audit, 5 Report, 1 Other | Analysis path смешан с sprint execution/kickoff reports и review triage. |
| Clarify | `docs/audit` | 7 | 6 Audit, 1 Other | Audit path в целом соответствует фактическому типу. |

### 2.2. Actual Analysis candidates

Файлы ниже фактически выполняют Analysis role в текущем corpus. Это не означает
автоматический перенос в `docs/analysis/`; B-028 должен применять будущий
standard и relation metadata.

| Repo | Current path | Status for B-025/B-028 |
| --- | --- | --- |
| Hub | `docs/analysis/2026-06-30-backlog-and-artifact-change-policy-analysis.md` | Canonical Analysis path; modernize metadata/sections after standard. |
| Hub | `docs/analysis/2026-07-01-reports-artifacts-inventory.md` | Canonical Analysis path; useful precedent for B-025. |
| Hub | `research/hub/2026-05-28-project-context-and-bootstrap-patterns.md` | Historical Analysis in `research/`; candidate for explicit Analysis metadata or future move. |
| Hub | `research/hub/2026-06-28-research-analysis-audit-inventory.md` | Analysis input for R/A/A split; candidate to cite as predecessor, not duplicate. |
| Hub | `research/hub/2026-06-28-ripple-effects-282-research.md` | Local impact analysis despite research naming; candidate for metadata clarification. |
| Hub | `research/mango/2026-05-22-classification-tz.md` | Analysis of existing TZ corpus; route after standard. |
| Hub | `research/mango/2026-05-22-requirements-flow.md` | Local process analysis; route after standard. |
| Hub | `research/open-ai-ru/2026-06-20-open-ai-ru-repository-architecture-and-l3-l4.md` | Local architecture analysis; route after standard. |
| Mango | `docs/analysis/2026-06-16-experiment-1027-analysis.md` | Actual Analysis already in target path. |
| Mango | `docs/analysis/2026-06-21-voice-digital-channels-comparison.md` | Actual comparative Analysis. |
| Mango | `docs/analysis/2026-06-22-issue-170-mango-inventory.md` | Actual inventory Analysis. |
| Mango | `docs/analysis/2026-06-23-executable-contracts-and-rfc-problems.md` | Local problem analysis for executable contracts and RFCs. |
| Mango | `docs/analysis/2026-06-23-repository-structure-analysis.md` | Local repository structure analysis. |
| Mango | `docs/analysis/2026-06-25-bcreq-fr-contract-process-analysis.md` | Local process/contract analysis. |
| Clarify | `docs/analysis/2026-05-12_review_mvp-context_v1.md` | Review-style Analysis; needs naming/frontmatter modernization. |
| Clarify | `docs/analysis/2026-05-13_analysis_next-docs-implementation-task_v1.md` | Actual Analysis with legacy filename convention. |
| Clarify | `docs/analysis/2026-05-15_analysis_repo-state-and-mvp-recommendations_v1.md` | Actual repository-state Analysis. |
| Clarify | `docs/analysis/2026-05-17_analysis_tz-structure_samples.md` | Actual local Analysis. |
| Clarify | `docs/analysis/metadata-coverage-fix_v1.md` | Actual local Analysis but non-date path; modernization candidate. |

## 3. Masked artifacts in `docs/analysis/`

These artifacts are physically under `docs/analysis/` but are not actual
Analysis by content and purpose. They are the highest-priority inputs for B-028
after `analysis-standard.md` exists.

| Repo | Path | Actual type | Rationale |
| --- | --- | --- | --- |
| Mango | `docs/analysis/2026-06-02-migration-strategy-rfc.md` | RFC | RFC/proposal intent; should not be standardized as Analysis. |
| Mango | `docs/analysis/2026-06-21-industry-inventory.md` | Research | Generates external/industry knowledge for taxonomy completion. |
| Mango | `docs/analysis/2026-06-22-mango-taxonomy-convergence-test.md` | Audit | Convergence test checks mapping against expected behavior. |
| Mango | `docs/analysis/2026-06-22-rfc-industry-taxonomy-improvement.md` | RFC | RFC/proposal intent. |
| Mango | `docs/analysis/2026-06-22-rfc-mango-taxonomy-improvement.md` | RFC | RFC/proposal intent. |
| Mango | `docs/analysis/2026-06-22-rfc-rules-registry-system.md` | RFC | RFC/proposal intent. |
| Mango | `docs/analysis/2026-06-22-rfc-taxonomy-extension-mechanism.md` | RFC | RFC/proposal intent. |
| Mango | `docs/analysis/2026-06-22-taxonomy-convergence-test.md` | Audit | Convergence test stance. |
| Mango | `docs/analysis/2026-06-23-approval-contract-test-industry-rfc.md` | Audit | Contract test / validation stance. |
| Mango | `docs/analysis/2026-06-24-artifact-chain-hypothesis-research.md` | Research | Explicit hypothesis/research stance. |
| Mango | `docs/analysis/2026-06-24-naming-convention-audit.md` | Audit | Naming convention audit. |
| Mango | `docs/analysis/2026-06-24-runs-contract-log-policy-audit.md` | Audit | Contract/log policy audit. |
| Mango | `docs/analysis/2026-06-25-ba-processes-industry-analysis.md` | Research | Industry/process research despite analysis wording. |
| Mango | `docs/analysis/2026-06-25-runs-observability-research.md` | Research | Observability research. |
| Mango | `docs/analysis/2026-06-25-telecom-vendors-ba-practices-research.md` | Research | External vendor practice research. |
| Clarify | `docs/analysis/2026-05-17_sprint-1-execution-report_v1.md` | Report | Execution report. |
| Clarify | `docs/analysis/2026-05-19_code-review-triage_v1.md` | Audit | Code-review triage checks state and defects. |
| Clarify | `docs/analysis/2026-05-19_sprint-5-kickoff_v1.md` | Report | Kickoff/execution planning report. |
| Clarify | `docs/analysis/2026-05-20_sprint-4-kickoff_v1.md` | Report | Kickoff/execution planning report. |
| Clarify | `docs/analysis/2026-05-20_sprint-4-parallel-kickoff_v1.md` | Report | Kickoff/execution planning report. |
| Clarify | `docs/analysis/README.md` | Other | Navigation file, not Analysis. |
| Clarify | `docs/analysis/sprint-execution-report_template.md` | Report | Report template, not Analysis. |

## 4. Boundaries: Analysis ↔ Research ↔ Audit ↔ Report

| Boundary | Decision rule for this inventory | Consequence for B-025 |
| --- | --- | --- |
| Analysis vs Research | If the dominant value is new external/domain knowledge, source-backed benchmark, market/industry synthesis or hypothesis generation, classify as Research. If the dominant value is interpreting local repository/project context, classify as Analysis. | Analysis standard can cite Research as input, but should not inherit Research evidence rules or require external sources. |
| Analysis vs Audit | If the document checks compliance, conformance, expected behavior, contract execution or pass/fail state, classify as Audit. | Analysis standard should not define audit verdicts, checklists or remediation protocols; those belong to B-029..B-033. |
| Analysis vs Report | If the document records what happened, what was executed, kickoff state, sprint state or a descriptive summary, classify as Report. Analysis explains what the state means and what options follow. | Analysis standard should allow evidence links to Reports, not absorb Report profiles. |
| Analysis vs RFC | RFC proposes a change before a decision gate. Analysis may prepare options or evidence, but a proposal with decision alternatives and acceptance path is RFC. | B-025 is the RFC for the Analysis standard; existing RFC-like files should remain proposal artifacts. |
| Analysis vs ADR | ADR records an accepted decision. Analysis can be upstream evidence for ADR, but is not itself a decision record. | ADR-001 and ADR-002 are governance constraints for placement/lifecycle, not Analysis examples. |

Practical boundary: Analysis is an interpretation layer. It connects local
facts, constraints and options. It is not the evidence-generation layer
(Research), not the compliance stance (Audit), not the execution log (Report),
and not the proposal/decision record (RFC/ADR).

## 5. Duplicates, substitutions and drift

No safe deletion is recommended in B-024. The duplicates below are review
candidates only; deletion or move belongs to B-028 after the Analysis standard
and to the matching Research/Audit/Report cleanup chains where applicable.

| Finding | Evidence | Classification |
| --- | --- | --- |
| `docs/analysis/` is used as a generic work-results folder in Mango | 15 masked artifacts under Mango `docs/analysis/`: 5 Research, 5 Audit, 5 RFC. | Concept substitution: Analysis path substitutes Research/Audit/RFC routing. |
| Clarify mixes reports into Analysis | 5 report-like sprint/kickoff/template artifacts under Clarify `docs/analysis/`. | Concept substitution: execution Report under Analysis. |
| Hub has legacy local Analysis inside `research/` | 6 actual Analysis files under Hub `research/`. | Historical routing drift; not a cleanup instruction before standard. |
| Word "analysis" appears in report filenames | Hub `docs/report/2026-06-30-pr-303-rfc-hypothesis-analysis.md`, `docs/report/2026-07-01-reports-inventory-placement-analysis.md`, `docs/report/2026-07-01-rfc-adr-duplication-analysis.md`. | Filename wording does not override Report role. |
| RFC-like artifacts outside canonical RFC path | Mango RFC files under `docs/analysis/`; Hub RFC-like research files under `research/mango/`. | Proposal/RFC routing drift. |

Potential duplicate-review groups:

| Group | Assessment | Recommended treatment |
| --- | --- | --- |
| Mango taxonomy RFC set: `rfc-industry-taxonomy-improvement`, `rfc-mango-taxonomy-improvement`, `rfc-rules-registry-system`, `rfc-taxonomy-extension-mechanism` | Interrelated proposal family, not safe duplicates. | Add `scope`, `supersedes` and `related_artifacts` if future Mango cleanup confirms overlap. |
| Mango convergence tests: `mango-taxonomy-convergence-test` vs `taxonomy-convergence-test` | Related audit/convergence tests with different taxonomy scope. | Keep until Audit cleanup; clarify `scope` and `based_on`. |
| Mango contract/log audits | `approval-contract-test-industry-rfc`, `runs-contract-log-policy-audit` and audit files in `docs/audit/` share contract-check stance. | Route through future Audit inventory/standard, not Analysis cleanup alone. |
| Clarify sprint kickoff/execution report series | Multiple report-like sprint artifacts and a template under `docs/analysis/`. | Future Report cleanup should distinguish template vs execution report. |
| Hub historical Analysis under `research/` vs newer `docs/analysis/` | Older local analyses predate the newer routing. | Keep as historical sources; B-028 can add metadata or move only after standard. |

## 6. Move, delete and modernization candidates for B-028

This issue should not move files. The following list is a future work queue for
B-028 and adjacent cleanup chains.

| Candidate class | Examples | Future action |
| --- | --- | --- |
| Actual Analysis already in `docs/analysis/` | Hub two current reports-inventory/backlog-policy analyses; Mango six analyses; Clarify five analyses. | Modernize frontmatter and sections to future `analysis-standard.md`; preserve path where already acceptable. |
| Actual Analysis outside `docs/analysis/` | Hub six Analysis files under `research/`. | Either add explicit Analysis metadata in place or move to `docs/analysis/` after standard and migration plan. |
| Research masked as Analysis | Mango industry inventory, artifact-chain hypothesis research, BA processes industry analysis, runs observability research, telecom vendors practices research. | Route through Research standard; do not force into Analysis. |
| Audit masked as Analysis | Mango convergence/contract/naming/runs audits; Clarify code-review triage. | Route through Audit standard/inventory B-029..B-033. |
| Report masked as Analysis | Clarify sprint execution/kickoff/template reports. | Route through Reports chain B-041..B-044, using `docs/report/` if accepted by future Report standard. |
| RFC masked as Analysis | Mango migration strategy RFC and four taxonomy/rules RFC files. | Route to RFC/proposal handling; add relation metadata before any physical migration. |
| Navigation/template files in Analysis path | Clarify `docs/analysis/README.md` and report template. | Keep navigation or move template only if future docs/report/template policy requires it. |

Metadata modernization should precede physical movement:

1. Add explicit `artifact_type` / subtype vocabulary only after B-025..B-027.
2. Add relation fields where useful: `based_on`, `source`, `scope`,
   `supersedes`, `related_artifacts`.
3. Record source issue and upstream evidence in frontmatter for Analysis files.
4. Normalize legacy Clarify filenames only with a spoke-specific migration plan.
5. Add `supersedes` only when a human or follow-up cleanup confirms actual
   replacement, not just semantic proximity.

## 7. Implications for B-025

B-025 should write an RFC for Analysis standard with these constraints:

1. Analysis is a local interpretation artifact, not a Research subclass.
2. Analysis can consume Research, Audit and Report outputs via links and
   relation metadata, but must not duplicate their standards.
3. The standard needs a minimum evidence section, but not source-backed research
   methodology.
4. The standard needs explicit boundaries against Audit verdicts and Report
   execution summaries.
5. Routing must handle legacy files: "actual Analysis outside path" is a
   modernization candidate, not an immediate violation.
6. Cleanup B-028 must wait for accepted standard and migration plan, matching
   ADR-001/ADR-002 lifecycle discipline.

## 8. Status against issue #342 DoD

| Requirement | Status |
| --- | --- |
| Hub, Mango and Clarify candidates listed with rationale | Done: full matrix plus summarized tables in sections 2 and 3. |
| Actual type identified as Research / Analysis / Audit / Report / RFC / ADR / Other | Done: matrix classifies all scanned text artifacts; section 2 summarizes counts. |
| Duplicates, concept substitutions and modernization candidates for B-028 | Done: sections 5 and 6. |
| References issue #296, issue #288, ADR-001/ADR-002 and B-020 | Done: frontmatter and section 1.1; ADR-003 and Reports inventory are also linked as context. |
| No cleanup, no physical migration, no standard creation | Done: this document is inventory and boundary analysis only. |

## 9. Conclusion

B-024 should move from TODO to review. The corpus shows that Analysis must be a
separate standard focused on local interpretation and recommendation, with
explicit links to but not inheritance from Research, Audit and Report.

For B-025, the actionable input is narrow: define the Analysis artifact shape,
frontmatter and routing while preserving boundaries. For B-028, the actionable
input is the candidate list above, especially Mango `docs/analysis/` masked
Research/Audit/RFC files and Clarify report-like files under `docs/analysis/`.
No file should be moved or deleted by this issue.
