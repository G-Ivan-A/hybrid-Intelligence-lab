---
status: canonical
version: 1.40
updated: 2026-07-03
temperature: 0.1
---

# Changelog

All notable repository governance changes are documented here.

## Unreleased

### Added

- audit: Modernized local Hub Audit artifacts for B-033 / issue #367. Renamed
  legacy `docs/audit/task-execution-audit-2026-06.md` to canonical date-first
  `docs/audit/2026-06-11-task-execution-audit.md`, added
  `audit_target` / `evidence_model` / `verdict` frontmatter and the six-section
  Audit core (Summary/BLUF, Scope/Target, Method/Evidence, Findings/Verdict,
  Remediation/Deviation, Related Artifacts) to all local `docs/audit/` reports,
  and updated MkDocs navigation, `governance/artifact-map.md`,
  `governance/backlog.md`, `standards/frontmatter-docs-standard.md`,
  `standards/file-naming.md` and `standards/README.md`. Validators now enforce
  `docs/audit/` date-first filenames plus Audit-specific frontmatter and body
  sections; the frontmatter validator regression suite covers the new failure
  modes. External Mango/Clarify snapshot evidence remains linked/deferred; no
  broad repository migration is performed in B-033.

- standard: Создан `standards/audit-standard.md` (draft) — базовый нормативный
  стандарт Audit для B-032 / issue #362. Стандарт фиксирует базовый каркас Audit
  (назначение, frontmatter, naming, lifecycle, минимальное ядро секций),
  **4-компонентную модель** (`compliance target` / `evidence model` /
  `verdict-finding` / `deviation handling`) как нормативное ядро и routing-критерий
  (content-over-path), audit-specific frontmatter (`audit_target` /
  `evidence_model` / `verdict` обязательны; `severity_scale` / `follow_up` /
  `related_norm` опциональны), минимальное ядро секций (Summary/BLUF,
  Scope/Target, Method/Evidence, Findings/Verdict, Remediation/Deviation, Related
  Artifacts) как проекцию четырёх компонентов, routing `docs/audit/YYYY-MM-DD-name.md`,
  knowledge-lifecycle (`draft → reviewed → canonical → superseded`), явное
  разграничение Audit-процесс (этот стандарт) vs audit-report output (профиль
  `audit` в `report-standard.md`, B-043) и границы Audit ↔ Research ↔ Analysis ↔
  Report. Стандарт принимает Вариант C из ADR-005 и RFC B-030, применяет
  section-level delegation (proposal, alternatives A/B/C/D, trade-offs остаются в
  RFC B-030; инвентаризация 29 кандидатов — в B-029; decision rationale — в
  ADR-005) и не мигрирует файлы (это B-033). Обновлены `standards/README.md`,
  `governance/artifact-map.md`, `governance/backlog.md` (B-032 → review) и
  структурный валидатор.

- adr: Создан `docs/adr/2026-07-adr-006-analysis-structure.md` (accepted) —
  human decision gate по структуре Analysis для B-026 / issue #357. ADR
  фиксирует принятое человеком решение принять **Вариант C** из RFC B-025
  (базовый стандарт Analysis + опциональные лёгкие профили подтипов
  `inventory` / `matrix` / `options` / `recommendation` как секции, «A сейчас,
  B потом» с триггером B), подтверждает канонический routing
  `docs/analysis/YYYY-MM-DD-name.md` (уже задан в `research-standard` и ADR-003,
  без изменения ADR-002/ADR-003), frontmatter Analysis с relation-метаданными
  (`source` / `scope` / `based_on` / `related_artifacts` и опционально
  `analysis-subtype`), knowledge-lifecycle (`draft → reviewed → canonical →
  superseded`) и границы Analysis ↔ Research ↔ Audit ↔ Report ↔ RFC ↔ ADR
  методом link/cite к B-024/B-029/B-041/glossary/research-standard (без restate).
  Open Questions RFC B-025 закрыты делегированием: набор профилей и
  обязательность `analysis-subtype` → B-027; физический дом legacy Analysis →
  B-028/B-034; пороги триггера B → B-027. ADR применяет section-level delegation
  (не пересказывает proposal/alternatives/trade-offs RFC), разблокирует стандарт
  B-027 и cleanup B-028, но не создаёт стандарт и не мигрирует файлы. RFC B-025
  переведён в `accepted` (v0.2, decision record — ADR-006). `governance/backlog.md`
  (B-026 → DONE, B-027 разблокирована), `governance/artifact-map.md`,
  `governance/rfc/README.md` и структурный валидатор обновлены. Зеркалит цепочку
  Reports (ADR-004 / B-042).
- adr: Создан `docs/adr/2026-07-adr-005-audit-structure.md` (status `accepted`) —
  ADR-005 / human decision gate для B-031 / issue #358. ADR фиксирует принятие
  **Варианта C** из RFC B-030: базовый стандарт Audit + **4-компонентная модель**
  (`compliance target` / `evidence model` / `verdict-finding` / `deviation
  handling`), подтверждение routing `docs/audit/YYYY-MM-DD-name.md` (без ADR-002-
  дрейфа, делегирован в `research-standard.md`), frontmatter с audit-specific
  метаданными (`audit_target`/`evidence_model`/`verdict` обязательны;
  `severity_scale`/`follow_up`/`related_norm` опциональны), knowledge-lifecycle
  (`draft → reviewed → canonical → superseded`) и разграничение Audit-процесс
  (B-032) vs audit-report output (B-043). Open questions RFC B-030 закрыты или
  делегированы: физический дом audit reports уже решён в ADR-004 v0.3
  (`docs/audit/`), а evidence/statistics output, модернизация legacy и
  governance-audits Mango делегированы в B-032/B-033. ADR применяет section-level
  delegation (proposal, alternatives A/B/C/D, trade-offs остаются в RFC B-030),
  не создаёт стандарт (B-032) и не мигрирует файлы (B-033). Разблокирована B-032.
  Обновлены `governance/artifact-map.md`, `governance/backlog.md` (B-031 → DONE,
  B-032 разблокирована) и структурный валидатор.
- rfc: Создан `governance/rfc/2026-07-02-rfc-audit-structure.md` — draft RFC
  для B-030 / issue #352. RFC предлагает (не нормирует) структуру Audit-
  артефактов на входе цепочки стандартизации после инвентаризации B-029:
  фиксирует Вариант C (базовый стандарт Audit + **4-компонентная модель**
  `compliance target` / `evidence model` / `verdict-finding` / `deviation
  handling`), канонический routing `docs/audit/YYYY-MM-DD-name.md` (без ADR-002-
  дрейфа, в отличие от Reports), Audit-frontmatter с audit-specific
  метаданными (`audit_target`/`evidence_model`/`verdict` обязательны;
  `severity_scale`/`follow_up`/`related_norm` опциональны) и relation-полями
  (`source`/`scope`/`based_on`/`related_artifacts`), разграничение Audit-процесс
  vs audit-report output (координация с Reports B-043) и границы Audit ↔ Research
  ↔ Analysis ↔ Report (link/cite на B-029, без restate). Приведены альтернативы
  A/B/C/D с матрицей дельт (C рекомендован), trade-offs, Critical Analysis,
  lifecycle `draft → reviewed → canonical → superseded` и последствия для цепочки
  B-030..B-033. RFC — proposal (IL-3); decision gate вынесен в future ADR (B-031),
  обязательная норма делегируется в `standards/audit-standard.md` (B-032); ADR/
  Standard не создаются, файлы не мигрируются. `governance/rfc/README.md`,
  `governance/artifact-map.md`, `governance/backlog.md` (B-030 → review) и
  структурный валидатор обновлены.
- standard: Создан `standards/report-standard.md` (draft) — базовый нормативный
  стандарт Report + лёгкие профили подтипов для B-043 / issue #354. Стандарт
  фиксирует базовый каркас Report (назначение, frontmatter, naming, lifecycle,
  минимальные core-секции), профили `audit` / `report` / `statistics`,
  relation-метаданные frontmatter (`based_on`, `source`, `scope`, `supersedes`,
  `related_artifacts`, `report-subtype`), routing split `docs/report/` +
  `docs/audit/` и границы Reports ↔ Analysis ↔ Audit ↔ Research evidence.
  Отмечает knowledge-vocabulary lifecycle для самих Report-артефактов против
  governance-vocabulary для документа стандарта. Стандарт делегирует proposal /
  alternatives / trade-offs в RFC B-041 и принятое решение в ADR-004, не
  дублируя их; физическая миграция файлов остаётся за B-044. Обновлены
  `standards/README.md`, `governance/artifact-map.md` и `governance/backlog.md`
  (B-043 → DONE).
- rfc: Added `governance/rfc/2026-07-02-rfc-analysis-structure.md` (status
  `proposed`) for issue #350 (B-025). The RFC proposes the structure of Analysis
  artifacts: a single base Analysis standard plus optional light subtype profiles
  (`inventory`/`matrix`/`options`/`recommendation`) as Variant C ("A now, B
  later" with an explicit anti-inflation trigger B), confirms the canonical
  routing `docs/analysis/YYYY-MM-DD-name.md` (delegated to `research-standard`),
  proposes Analysis frontmatter with relation metadata
  (`source`/`scope`/`based_on`/`related_artifacts`/`analysis-subtype`), the
  knowledge-lifecycle (`draft → reviewed → canonical → superseded`), a minimal
  core section set (Summary/BLUF, Context/Scope, Findings/Options,
  Recommendations, Related Artifacts) and the boundaries Analysis ↔ Research ↔
  Audit ↔ Report ↔ RFC ↔ ADR. It delegates evidence to B-024 (186-artifact
  inventory and boundaries), B-029 (Analysis ↔ Audit), B-041 (Analysis ↔ Reports
  precedent), `research-standard` (R/A/A routing) and `glossary` (definitions)
  instead of restating them, gives Alternatives A/B/C/D with rejection rationale,
  Trade-offs, delta matrix and Critical Analysis. The change intentionally does
  not create an Analysis standard (B-027), does not create an ADR (B-026) and
  does not migrate files (B-028); the decision record stays `not yet` pending the
  human decision gate. Registered in the RFC README, `governance/artifact-map.md`,
  the structure validator allowlist/required-text and `governance/backlog.md`
  (B-025 → review).
- analysis: Added `docs/analysis/2026-07-02-audit-artifacts-deep-analysis.md`
  for issue #344 (B-029). The report uses the B-024 matrix as input, reviews 29
  Audit candidates across Hub, Mango and Clarify at fixed artifact snapshots,
  and records for each artifact the compliance target, Audit process/report
  boundary, evidence model, deviation handling and B-033 modernization
  candidate. It identifies masked Audit artifacts in `docs/analysis/` and legacy
  `research/`/`governance/` paths, clarifies Audit ↔ Research ↔ Analysis ↔
  Report boundaries, and intentionally does not repeat the B-024 scan, does not
  create an RFC/ADR/Standard, and does not move files.
- analysis: Added `docs/analysis/2026-07-02-analysis-artifacts-inventory.md`
  for issue #342 (B-024) plus the reproducible evidence package
  `research/hub/exp/analysis-inventory-342/`. The inventory scans Hub, Mango and
  Clarify at fixed SHAs, classifies 186 text artifacts by actual type
  (Research / Analysis / Audit / Report / RFC / ADR / Other), identifies masked
  `docs/analysis/` artifacts in Mango and Clarify, records boundaries Analysis ↔
  Research ↔ Audit ↔ Report, and lists duplicate-review/modernization
  candidates for B-028. The change intentionally does not create an Analysis
  standard, does not create an RFC, does not move files, and does not clean up
  existing artifacts.
- adr: Создан `docs/adr/2026-07-adr-004-reports-structure.md` — accepted ADR
  для B-042 / issue #338. ADR фиксирует human decision по RFC B-041: принят
  Вариант C (базовый стандарт Report + лёгкие профили `audit`/`report`/
  `statistics`), канонический routing `docs/report/` (единственное число) и
  реконсиляция строки ADR-002 `docs/reports/` → `docs/report/` как later single
  decision source. Open questions из RFC получили явный статус: audit-report path
  и statistics-vs-evidence policy делегированы в B-043/B-030 и research-evidence
  policy; Триггер B принят как anti-inflation criterion с операционными порогами
  в B-043. Стандарт `standards/report-standard.md` не создан, физическая миграция
  файлов не выполнялась. RFC B-041 переведён в `accepted` и связан с ADR-004;
  routing row в ADR-002 обновлена на `docs/report/`; `governance/artifact-map.md`,
  `governance/backlog.md` и структурный валидатор обновлены.
- research: Создан `research/hub/2026-07-02-task-execution-modes-research.md` —
  research-отчёт по режимам выполнения задач для ИИ-агентов (B-045, issue #330)
  в режиме `Research` + `Creative` + `Deep Think` от лица 4 экспертов
  (промпт-инженер, архитектор ИИ-агентов, исследователь таксономий, инженер
  процессов). Фаза 1: индустриальные нормы (Anthropic/OpenAI prompt-eng, CoT,
  few-shot, DSPy; ReAct/Reflexion/Plan-and-Solve, CrewAI/LangGraph/MetaGPT/
  AutoGPT; Cynefin, Bloom revised, Cognitive Load / Cognitive Task Analysis;
  guardrails/evals/HITL) с указанием источника, автора, ссылки и границ. Фаза 2:
  шесть паттернов практики Hub/Mango (тип/режим в префиксе, детерминированная
  маршрутизация по действию, цепочка RFC→ADR→Standard→Chore, смешанные задачи →
  Hybrid, Audit ≠ Analysis по глаголу, внешнее удержание режима). Фаза 3: пять
  реальных тестов как воспроизводимый rule-based классификатор
  `research/hub/exp/task-execution-modes-330/` (тип v1 8/18 → v2 17/18, режим
  17/18 на бэклоге; 5/5 на практических issue; 3/3 конфликт; 3/3 эволюция; 6/6
  индустрия). Фаза 4: подтверждение триады Creative/Structured/Hybrid и вывод об
  action-anchored сигнале как решающем входе; единственный промах (B-016)
  помечен `under-specified` как находка о недоопределённом одностроч­нике.
  Отчёт не предлагает решений, не вводит и не меняет режимы, не создаёт
  стандартов/контрактов. Зарегистрирован в `governance/artifact-map.md`; 21 новый
  внешний источник (`ext-137`…`ext-157`) добавлен в
  `research/external-knowledge/external-sources-registry.md`; задача B-045
  зарегистрирована в `governance/backlog.md`.
- rfc: Создан `governance/rfc/2026-07-02-rfc-reports-structure.md` — Accepted RFC
  структуры Reports-артефактов (B-041, issue #328). Режим Hybrid: каркас — из
  `standards/rfc-structure-standard.md`, креативная часть (формулировки
  предложения, альтернативы, trade-offs) — авторская в рамках входных данных
  инвентаризации B-038 и Research industry norms. Предлагает **Вариант C**: единый
  базовый стандарт Report + лёгкие профили подтипов (`audit`/`report`/`statistics`)
  как секции («A сейчас, B потом» с явным Trigger B против инфляции артефактов);
  канонический routing `docs/report/` (единственное число) с реконсиляцией
  дрейфа ADR-002 `docs/reports/` через ADR-004 (B-042); frontmatter Reports с
  relation-метаданными (`based_on`/`source`/`scope`/`supersedes`/`related_artifacts`).
  Зафиксированы 4 альтернативы (A плоский единый стандарт — отклонён; B три
  независимых стандарта — отклонён; C базовый + профили — рекомендован; D Reports
  как подтип Analysis — отклонён) с rationale и trade-offs, а также границы
  Reports ↔ Analysis ↔ Audit ↔ Research evidence (через ссылки/cite, без
  дублирования Research benchmark-норм и Analysis-инвентаря 47 кандидатов). RFC
  принят через ADR-004: обязательная норма делегирована в будущий
  `standards/report-standard.md` (B-043), физическая миграция — в B-044.
  Зарегистрирован в `governance/artifact-map.md`,
  `governance/rfc/README.md` и структурном валидаторе; задачи B-041..B-044
  добавлены в `governance/backlog.md`.

- audit: Создан `docs/audit/2026-07-01-documentation-boundary-audit.md` — аудит
  коллизий интерпретации стандартов RFC/ADR/Standard (B-039, issue #320). Аудит
  проверяет 5 IL-3 артефактов (`standards/research-standard.md`, RFC B-016,
  ADR-003, `standards/adr-structure-standard.md`, `standards/rfc-structure-standard.md`)
  по трём измерениям (внутри артефактов, на переходах RFC→ADR / ADR→Standard /
  Research→RFC / Analysis→RFC, cross-cutting) в режиме Deep Think (4 эксперта,
  4 стресс-теста). Вердикты: ни один артефакт не содержит блокирующего нарушения;
  посекционное дублирование ADR-003 ↔ RFC B-016 подтверждено как ремедиированное;
  `research-standard.md` и RFC B-016 проверены чисто. Зафиксированы причины
  (F-01 смешение терминов Standard/Contract в трёх стандартах;
  F-07 шаблон ADR приглашает дублирование; F-08 отсутствие overlap-guard/чеклиста)
  и последствия (F-02/F-03 stale-refs, F-09 семантика версий, F-10 двойная
  supersession) с классификацией причины-vs-последствия и трёхуровневыми
  приоритизированными рекомендациями по лечению причин (стандарты / шаблоны /
  валидация). Терминологический риск (Standard ≠ Contract, category error
  относительно canonical глоссария и IL-модели) флагуется для Tier 2 remediation
  в issue #322.
  Зарегистрирован в `governance/artifact-map.md`, `mkdocs.yml` и структурном
  валидаторе; задача B-039 добавлена в `governance/backlog.md`.

- standard: Создан `standards/research-standard.md` — стандарт (IL-3 reusable
  rule) структуры research-артефактов Хаба (B-018, issue #318). Стандарт принимает
  модель ADR-003 и RFC B-016 без корректировок и нормативно фиксирует:
  размещение отчётов `research/<domain>/YYYY-MM-DD-name.md`, единый контейнер
  воспроизводимой доказательной базы `research/<domain>/exp/<issue-slug>/`,
  запрет обязательной папки `outputs/` (плоская структура), границу `exp/`
  (research evidence corpus) vs `runs/` (operational run record per ADR-002),
  маршрутизацию Research / Analysis / Audit по типу задачи и переходный режим
  для legacy `exp-*`. Стандарт становится replacement для
  `standards/research-profile.md` (физическое удаление профиля — B-021).
  Зарегистрирован в `standards/README.md`, `governance/artifact-map.md` и
  структурном валидаторе; задача B-018 зарегистрирована в
  `governance/backlog.md`. Alternatives, trade-offs и rejected options не
  дублируются — они остаются в RFC B-016. По review-фидбэку PR #319 стандарт
  зарегистрирован в `status: draft` (governance-vocabulary), frontmatter
  дополнен полями traceability (`executable`, `scope`,
  `related_standards`, `related_issues`), и явно разведено противоречие
  lifecycle vs frontmatter: `standards/*.md` используют governance-vocabulary, а
  нормируемые research reports (`research/*.md`) — knowledge-vocabulary.

- report: Added `docs/report/2026-07-01-rfc-adr-duplication-analysis.md` for issue
  #316. Root-cause analysis of the RFC B-016 ↔ ADR-003 duplication: it maps the
  duplicated sections (ADR `Decision` P1–P4, `Alternatives Considered` table,
  `Consequences` downstream list) against RFC B-016, identifies the cause as a
  section-level misinterpretation of the RFC/ADR boundary (stated only at document
  level in the standard, with a template that invites section-filling and no
  validator backstop), records which contracts the author applied and how, and
  recommends prevention measures. Registered in `governance/artifact-map.md`,
  `mkdocs.yml` and the structure validator.
- analysis: Added `docs/analysis/2026-07-01-reports-artifacts-inventory.md` for
  issue #310 (backlog B-038) plus the reproducible evidence package
  `research/hub/exp/reports-inventory-310/`. The inventory scans Hub, Mango and
  Clarify at fixed SHAs, classifies 47 Reports candidates by actual subtype
  (`audit`, `report`, `statistics`) and relation (`output-for-audit`,
  `output-for-analysis`, `standalone-report`), identifies path drift,
  substitutions, duplicate-review candidates and modernization candidates, and
  confirms Variant C scope: one base Report standard with light subtype profiles.
  The change intentionally does not create a Reports standard, does not move or
  rename files, and does not change directory structure.
- adr: Added `docs/adr/2026-07-adr-003-research-structure.md` (ADR-003) for issue
  #314 (backlog B-017). Human decision gate that accepts the RFC B-016 model
  without changes: single `research/<domain>/exp/<issue-slug>/` evidence
  container, ban on nested `outputs/` (flat structure), the `exp/` (research
  evidence corpus) vs `runs/` (operational run record per ADR-002) boundary and
  Research / Analysis / Audit routing by task type. `Supersedes`
  `standards/research-profile.md` effective after its removal in B-021; delegates
  the normative rule to `standards/research-standard.md` (B-018) and an ADR-002
  addendum (B-019); consequences cover the B-018..B-023 chain. Registered in
  `governance/artifact-map.md`, `governance/backlog.md` (B-017 later accepted
  by issue #322) and the
  structure validator allowlist. Follows `standards/adr-structure-standard.md`
  (frontmatter and required body sections). No validator logic or file migration
  performed (deferred to B-022/B-023).

- research: Added
  `research/hub/2026-06-30-reports-industry-norms-and-standardization-scope.md`
  for issue #307 (backlog B-038). Source-backed industry benchmark of how
  Reports artifacts (audit / statistical / general) are classified by Diátaxis,
  DITA, ISO/IEC/IEEE, ANSI/NISO Z39.18, ГОСТ 7.32/19.101, SDMX/DDI, NIST AI RMF,
  the EU AI Act and OSS governance repos (Kubernetes/CNCF/OpenTelemetry). Tests
  hypotheses H1-H4 about standardization scope (H1 confirmed with nuance — Report
  is a distinct genre that is usually a process output; H2 holds for industry but
  not at Hub scale; H3 holds in hybrid form; H4 confirmed), maps Reports ↔
  Analysis/Audit boundary cases by dominant stance, and recommends Variant C
  (hybrid: one base Report standard + light subtype profiles, "A now, B later").
  Registered in `governance/artifact-map.md`, `research/README.md`,
  `research/hub/README.md`, `mkdocs.yml`,
  `research/external-knowledge/external-sources-registry.md` and the structure
  validator. Stays research-only: it does not create a Reports standard, does not
  inventory current reports and does not change directory structure.
- report: Added `docs/report/2026-06-30-pr-303-rfc-hypothesis-analysis.md`
  for issue #306 with a critical analysis of the attached PR #303 hypothesis,
  the no-generation-error conclusion, the confirmed minor RFC gaps and the
  applied remediation.
- chore: Добавлена задача B-038 в бэклог (Reports inventory, issue #304).
  Источник: видение фаундера §3, согласование в чате 2026-07-01.
- rfc: Added `governance/rfc/2026-06-30-rfc-research-structure.md` for issue #302
  (backlog B-016). The RFC proposes the base research-structure model: a single
  `research/<domain>/exp/<issue-slug>/` evidence container, a ban on the nested
  `outputs/` folder (flat package inside `exp/`), the `exp/` (research evidence
  corpus) vs `runs/` (operational run record) boundary, Research / Analysis /
  Audit routing by task type with a classification decision tree, transitional
  handling of legacy `exp-*` until migration (B-022), a Critical Analysis
  stress-test, and consequences for chain B-017..B-023. It references issues
  #294/#290/#288 and stays a proposal (status `draft`); the normative standard is
  delegated to B-018 after the ADR (B-017). Registered the RFC in
  `governance/rfc/README.md` (version 1.13 -> 1.14), `governance/artifact-map.md`,
  the structure validator allowlist, and updated backlog B-016 status. No file
  migration and no research-format enforcement logic were changed.
- chore: Добавлены задачи B-035..B-037 в бэклог (реорганизация backlog +
  amendment policy + валидатор). Источники: согласование в чате 2026-06-30,
  issue #297.
- analysis: Added `docs/analysis/2026-06-30-backlog-and-artifact-change-policy-analysis.md`
  for issue #297. The report confirms backlog role overload and the missing
  tiered amendment policy, compares native tracker, sprint backlog, small-change
  review, ADR/RFC and ITIL-style change-class practices, and records follow-up
  recommendations without changing `governance/backlog.md` or creating new
  RFC/ADR/standard artifacts.
- backlog: Added the issue #296 Analysis and Audit standardization sprints to
  `governance/backlog.md` as tasks B-024..B-033, with five stages each:
  current-state analysis, RFC, ADR, standard and post-standard cleanup. Added
  B-034 as the separate Hub migration-plan RFC gate after the Research,
  Analysis and Audit standards exist, updated `governance/artifact-map.md`, and
  bumped the structure validator's canonical backlog version check.
- backlog: Added the issue #294 sprint to `governance/backlog.md` as tasks
  B-016..B-023. The sprint traces to issues #288 and #290, defines the
  dependency chain `RFC -> ADR -> standard -> ADR-002 addendum -> glossary ->
  profile removal`, and records migration/validator follow-ups for the `exp/`
  research structure without implementing those follow-up tasks in this PR.
  Updated the structure validator's canonical backlog version check accordingly.
- audit: Format-contract audit for issue #290. Added
  `docs/audit/2026-06-29-research-artifact-format-contract-audit.md` to trace
  the source of `research/hub/exp-*` folders, distinguish report Markdown files
  from reproducible experiment corpora, identify the unresolved
  `exp-<slug>/outputs/` vs ADR-002 `runs/` boundary, and recommend preserving the
  dual report + experiment model until a follow-up standard/ADR clarification.
- research: Research / Analysis / Audit inventory for issue #288. Added
  `research/hub/2026-06-28-research-analysis-audit-inventory.md` plus a
  reproducible scan under `research/hub/exp-research-analysis-audit-288/`,
  classifying Hub, Mango and Clarify artifacts by actual purpose, identifying
  concept substitutions and duplicate risks, and planning three future
  `Analysis -> RFC -> Standard` chains without creating RFCs or standards.
- rfc: ADR/RFC structure standards for issue #280. Added
  `governance/rfc/2026-06-27-rfc-adr-standard.md` and
  `governance/rfc/2026-06-27-rfc-rfc-standard.md` with base contracts,
  lifecycle rules, A/B/C/D delta matrices, Critical Analysis sections and an
  explicit RFC/ADR boundary. Registered both RFCs in the RFC index,
  artifact-map and repository-structure validator.
- research: RFC/ADR industry norms and variants for issue #278. Added separate
  Hub research reports for RFC-like proposal processes and ADR/decision-record
  processes, plus a reproducible evidence experiment under
  `research/hub/exp-rfc-adr-industry-norms/`, external-source registry entries
  `ext-075`..`ext-126`, MkDocs navigation, and artifact-map/index wiring. The
  change intentionally does not create a new RFC or ADR; it preserves the result
  as research input for later founder decisions.
- adr: Fixed founder infrastructure decisions for issue #276 in
  `docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md` and
  `docs/adr/2026-06-adr-002-artifact-document-methodology.md`. The two incoming
  research files are now `reviewed`, linked to the ADRs, and registered through
  `governance/artifact-map.md`; the PR intentionally records methodology and
  transition rules without a repo-wide physical migration.
- research: Follow-up study of the "Ecosystem Project Infrastructure
  Architecture" Agreement (issue #274). Appended **Part II** (§14–§22) to
  `research/hub/2026-06-23-repository-structure-concept.md` — a critical
  `Research` extension in refutation-first mode. It records the Agreement in
  structured form with its deltas vs the founder vision (§15), stress-tests every
  section and delta against industry norms — 8 ✅ / 3 ⚠️ / 4 ❌ (§16), correlates
  the IL-0..IL-3 executability levels with the industrial executability norm and
  refutes "IL-1 = 100% YAML/JSON" via policy-as-code (Rego), SKOS taxonomies and
  the repo's own Markdown contract format (§17), and proves IL is **orthogonal**
  to the documentation axes of Diátaxis and DITA (§18). It locates and refutes the
  task's deliberately planted incorrect statement — the claim that "Golden
  Standard" is a valid ML/AI term (the industry terms are *gold standard* /
  *ground truth*) — with secondary refutations (§19), opens boundary-case
  hypotheses (§20) and reconciles with the founder vision (§21). Part I is not
  rewritten (Anti-Inflation); the file version bumps to 0.2. Eight external
  sources (`ext-067`..`ext-074`) are registered in the external-sources registry;
  structural decisions remain with the founder via RFC → ADR.
- research: До-исследование Соглашения «Архитектура инфраструктуры проектов
  экосистемы» (issue #274). В
  `research/hub/2026-06-23-repository-structure-concept.md` дописана **Часть II**
  (§14–§22) — критическое расширение в режиме `Research` с приоритетом
  опровержения. Соглашение зафиксировано структурированно с дельтами относительно
  видения фаундера (§15); каждый раздел и дельта проверены по индустриальным
  нормам — 8 ✅ / 3 ⚠️ / 4 ❌ (§16); уровни исполнимости IL-0..IL-3 соотнесены с
  индустриальной нормой, тезис «IL-1 = 100 % YAML/JSON» опровергнут через
  policy-as-code (Rego), таксономии SKOS и собственный Markdown-формат контрактов
  репозитория (§17); доказано, что IL **ортогонален** осям документации Diátaxis
  и DITA (§18). Обнаружена и опровергнута заложенная в задачу некорректная
  постановка — тезис о валидности термина «Golden Standard» в ML/AI (корректно —
  *gold standard* / *ground truth*) — со вторичными опровержениями (§19); открыты
  гипотезы граничных кейсов (§20) и проведена реконсиляция с видением фаундера
  (§21). Часть I не переписана (Anti-Inflation); версия файла повышена до 0.2.
  Восемь внешних источников (`ext-067`..`ext-074`) зарегистрированы в реестре;
  структурные решения остаются за фаундером через RFC → ADR.
- research: Axes decomposition, executability routing, format rules (variants
  provided) (issue #269). Appended **Part II** (§16–§23) to
  `research/hub/2026-06-25-artifact-inventory-and-classification.md` — a critical
  `Research` extension that deliberately provides **objective, evidence-backed
  variants instead of recommendations** (the choice is the founder's). It
  registers all six problems without solutions (§16); gives variant axis sets
  that split the conflated L0–L4 ladder into independent orthogonal axes, each
  with level semantics, the classification task it solves, international-practice
  examples and an admissibility criterion (§17); gives executability-type and
  routing variants with placement principles (§18); gives "abstraction → format"
  variants and the honest finding that no standard binds level to format —
  format follows function (§19); gives 2+ evidenced variants for each key
  catalog `governance/kb/standards/prompts/docs/runs` without adapting to the
  current state (§20); verifies and confirms the `Depends On` = context
  hypothesis and supplies wording variants for the contract (§21); gives
  research-file naming variants (§22) and Part II sources (§23). Every variant
  carries either an international-practice link or an explicit "practice absent —
  variant theoretical" note. Part I is not rewritten (Anti-Inflation); the file
  version bumps to 0.2. §22 records that the ecosystem has since adopted
  date-first naming (issue #267) — i.e. its Variant A — while preserving the
  objective variant analysis intact.
- research: Декомпозиция осей, маршрутизация по исполнимости, правила форматов
  (предоставлены варианты) (issue #269). В
  `research/hub/2026-06-25-artifact-inventory-and-classification.md` дописана
  **Часть II** (§16–§23) — критическое расширение в режиме `Research`, которое
  намеренно даёт **объективные доказательные варианты вместо рекомендаций**
  (выбор — за фаундером). Зафиксированы все шесть проблем без решений (§16);
  даны варианты наборов осей, разделяющие смешанную лестницу L0–L4 на
  независимые ортогональные оси (семантика уровней, решаемая задача
  классификации, международная практика, критерий допустимости) (§17); даны
  варианты типов исполнимости и правил маршрутизации с принципами размещения
  (§18); даны варианты «уровень абстракции → формат» с честным выводом, что
  стандарта, связывающего уровень с форматом, нет — формат следует функции
  (§19); для каждого ключевого каталога `governance/kb/standards/prompts/docs/runs`
  даны 2+ доказательных варианта без адаптации к текущему состоянию (§20);
  проверена и подтверждена гипотеза «`Depends On` = контекст» с вариантами
  формулировок контракта (§21); даны варианты именования research-файлов (§22) и
  источники Части II (§23). Каждый вариант сопровождается либо ссылкой на
  международную практику, либо явной пометкой «практика отсутствует — вариант
  теоретический». Часть I не переписывается (Anti-Inflation); версия файла
  повышена до 0.2. §22 фиксирует, что экосистема с тех пор приняла date-first
  именование (issue #267) — то есть его Вариант A — сохраняя объективный анализ
  вариантов в неизменном виде.
- governance: Ecosystem-wide date-first file naming for Hub research and spoke
  analysis/RFC/ADR artifacts (issue #267). Added
  `standards/file-naming-convention.md`, extended
  `standards/file-naming.md`, added `tools/validate-file-naming.sh`, wired the
  check into CI and spoke templates, and renamed chronological `research/`
  files to `YYYY-MM-name.md` or `YYYY-name.md` with links updated.
- research: Artifact inventory and classification (mango_ba_prompts +
  hybrid-Intelligence-lab) (issue #265). Added
  `research/hub/2026-06-25-artifact-inventory-and-classification.md` — a full
  artifact inventory of both ecosystem repositories (the Governance Hub and the
  Prompt & Pattern Library spoke) classified on four orthogonal axes
  (abstraction level L0–L4, eight knowledge areas, archetype A–D, lifecycle
  status). It surfaces the ecosystem's central classification hazard — four
  mutually incompatible "L1–L4" ladders — and proposes a single neutral routing
  ladder (the L0+L4 extension is justified, not invented for novelty),
  overlays the inventory on four prior studies (directory-structure concept,
  artifact-chain hypothesis, approval-contract test, BCREQ-FR contract
  analysis), lists cleanup candidates as recommendations only (no deletion), and
  derives executable routing rules for AI agents (RT-01…RT-10). A research note,
  not an RFC; decisions stay with the human. Registered in
  `research/hub/README.md`, `research/README.md`, `governance/artifact-map.md`
  and the MkDocs nav.
- research: Инвентаризация и классификация артефактов (mango_ba_prompts +
  hybrid-Intelligence-lab) (issue #265). Добавлен
  `research/hub/2026-06-25-artifact-inventory-and-classification.md` — полная
  инвентаризация артефактов обоих репозиториев экосистемы (Хаб governance и спок
  Prompt & Pattern Library) с классификацией по четырём ортогональным осям
  (уровень абстракции L0–L4, восемь областей знаний, архетип A–D, статус
  жизненного цикла). Выявляет ключевой риск классификации экосистемы — четыре
  несовместимые лестницы «L1–L4» — и предлагает единую нейтральную ось
  маршрутизации (расширение L0+L4 с обоснованием), накладывает инвентарь на
  четыре исследования (концепция структуры каталогов, гипотеза цепочки
  артефактов, тест контракта согласования, анализ BCREQ-FR-контракта),
  перечисляет cleanup-кандидаты только как рекомендации (без удаления) и выводит
  исполнимые правила маршрутизации для AI-агентов (RT-01…RT-10). Это
  research-заметка, а не RFC; решение остаётся за человеком. Зарегистрирован в
  `research/hub/README.md`, `research/README.md`, `governance/artifact-map.md` и
  навигации MkDocs.

- research: Repository structure concept for project archetypes (issue #263).
  Added `research/hub/2026-06-23-repository-structure-concept.md` — an addendum
  (not a replacement) to the `mango_ba_prompts` directory-structure research. It
  fixes the founder's vision as the priority base, closes the four open
  questions (`prompts/` vs in-process prompts, `docs/` vs `knowledge/`, flat vs
  subdirectory criterion, `scripts/` vs `tools/`), resolves three
  contradictions (root `prompts/`, root `standards/` vs `kb/`, `knowledge/` vs
  `docs/`), runs a critical risk analysis where the vision diverges from
  international practice, and derives a base/recommended/specific directory
  concept for the four PR #243 archetypes (Governance & Knowledge Hub, Prompt &
  Pattern Library, Product Spoke/Runtime, Education) benchmarked against 10+
  international repositories each, plus Hub sync recommendations. A research
  note, not an RFC; decisions stay with the human. Registered in
  `research/hub/README.md`, `research/README.md`, `governance/artifact-map.md`,
  the MkDocs nav and the structure validator.
- research: Концепция структуры репозитория для архетипов проектов (issue #263).
  Добавлен `research/hub/2026-06-23-repository-structure-concept.md` — дополнение
  (не замена) к исследованию структуры каталогов `mango_ba_prompts`: фиксирует
  видение фаундера как приоритетную базу, закрывает четыре открытых вопроса
  (`prompts/` ↔ процессные промпты, `docs/` ↔ `knowledge/`, критерий «плоский vs
  с подкаталогами», `scripts/` ↔ `tools/`), разрешает три противоречия
  (корневой `prompts/`, корневой `standards/` vs `kb/`, `knowledge/` vs
  `docs/`), проводит критический анализ рисков расхождения с международной
  практикой и выводит концепцию базовых/рекомендуемых/специфичных каталогов для
  четырёх архетипов PR #243 (10+ международных проектов на архетип) с
  рекомендациями по синхронизации с Хабом. Это research-документ, не RFC;
  решение остаётся за человеком. Зарегистрирован в `research/hub/README.md`,
  `research/README.md`, `governance/artifact-map.md`, навигации MkDocs и
  валидаторе структуры.
- creative: Independent vision of the `mango_ba_prompts` repository structure
  (issue #253). Added
  `research/mango/2026-06-19-repository-structure-vision.md` — a bilingual (ru/en)
  draft RFC that audits the real spoke repository, synthesises the four team
  visions (C/Q/G/founder) into a comparison table, weighs structure options
  A/B/C and recommends Option B in a phased path (Phase 0 write-contract +
  cleanup → Phase 1 Yandex Object Storage → Phase 2 Public `mango_ba_framework`
  + Private `mango_ba_operations` → Phase 3 VPS). Includes per-repo/storage
  directory trees, three information-security tiers (Public / Private /
  Confidential), a unified run-writing contract (`runs/RUN-XXXX/` +
  `metadata.yaml`) for the three scenarios, a single Hub bridge, open-ai.ru
  portal reuse, and records the token-inflation problem **without** proposing
  optimisation (per the founder's constraint). As a spoke-scoped RFC it lives in
  `research/mango/` (not the Hub-core `governance/rfc/`); registered in
  `research/mango/README.md`, `governance/artifact-map.md`, the MkDocs nav and
  the structure validator. Decision stays with the human (accept/reject RFC).
- creative: Независимое видение структуры репозитория `mango_ba_prompts`
  (issue #253). Добавлен
  `research/mango/2026-06-19-repository-structure-vision.md` — двуязычный (ru/en)
  draft RFC: аудит реального спока, синтез четырёх командных видений
  (C/Q/G/фаундер) с таблицей сравнения, варианты A/B/C и решение (Вариант B
  фазово), деревья каталогов, три уровня ИБ, единый контракт записи прогонов
  для трёх сценариев, один мост к Хабу, переиспользование портала open-ai.ru и
  фиксация проблемы токеновой инфляции **без** предложения оптимизации. Как RFC
  спок-проекта размещён в `research/mango/` (а не в Hub-core `governance/rfc/`);
  зарегистрирован в `research/mango/README.md`, `governance/artifact-map.md`,
  навигации MkDocs и валидаторе структуры. Решение за человеком.
- creative: Formalize AI-classifications and integrate into Mango roadmap
  (issue #251, builds on PR #248/#250). Added
  `research/mango/2026-06-18-ai-classifications-formalization.md` — a detailed
  formalization of the four new AI-subprocesses (prompt engineering, RAG
  configuration, agent orchestration design, AI-component testing), each with
  operations (input → action → output), descriptive/executable artifacts, an
  explicit link to a Wiegers chapter, a worked example and quality criteria.
  Added the "Эволюция операций в роадмапе Mango" section (4 phases with a
  per-operation transition plan: training, configuration, validation,
  integration) and the synchronization preparation for `mango_ba_prompts`
  (С1 `requirement_level` axis, С2 Business-Rule type with 5 categories, С3
  Wiegers ↔ mango ↔ BCREQ crosswalk). All terms are bilingual (RU/EN) and open
  questions (ОВ-1…ОВ-6) are answered at the end. Registered the artifact in
  `research/mango/README.md` and the structure validator.
- creative: Fix Wigers research — paths, classification, AI-processes, BABOK
  comparison (issue #249, corrects PR #248). Moved the Wigers requirements
  analysis into
  `research/external-knowledge/2026-06-18-wigers-requirements-analysis.md` (it is
  a Tier-1 external source, not internal Hub research) and moved the
  requirements-engineering AI-era RFC into
  `research/mango/2026-06-18-requirements-engineering-ai-era.md` (it is a
  spoke-project RFC for `mango`, not Hub core), updating every reference.
  Corrected the RFC
  classification: removed "prompt engineering as a type of requirement"; recorded
  that a Prompt is an **interface to a Tool** (analogy: SQL query ≠ database),
  that prompt engineering is a **subprocess** (operations: task analysis, draft
  writing, testing, iteration, validation), and split prompt artifacts into an
  executable prompt (`prompts/analyze-doc.md`) vs a descriptive **Prompt
  specification** (`docs/prompts/analyze-doc-spec.md`). Added the RFC section
  "Процессы и подпроцессы для разработки AI-агента" (process "Разработка
  AI-агента" with five subprocesses: agent architecture design, RAG
  configuration, prompt engineering, agent orchestration, AI-component testing).
  Added the research section "Сравнение классификаций" (Wiegers 2020 / BABOK v3 /
  ISO/IEC 29148 / AI-development LangChain·CrewAI / delta) with conclusions, and
  moved the open questions (ОВ-1…ОВ-4) to the end of the document with answers.
  Re-registered both artifacts across `research/README.md`,
  `research/hub/README.md`, `research/external-knowledge/README.md`,
  `governance/rfc/README.md` (v1.10), `research/mango/README.md`,
  `governance/artifact-map.md` (v1.42), the structure validator and the MkDocs
  navigation.
- creative: Research Wigers book with AI-era actualization (issue #247). Added
  `research/external-knowledge/2026-06-18-wigers-requirements-analysis.md` — an independent,
  bilingual (ru/en) extraction of the Wiegers & Beatty *Software Requirements*
  system (requirement levels Business → User → Functional/Non-functional,
  requirement types incl. the five business-rule categories and quality
  attributes, requirements-engineering processes, and the Appendix А glossary),
  plus a three-trend actualization (2020 Wiegers / 2026 Agile-DevOps-CI·CD /
  2026 AI) mapped onto the five-layer model and the full-vs-local chain
  variability. Added `research/mango/2026-06-18-requirements-engineering-ai-era.md` —
  an RFC comparing the extracted Wiegers system with `mango_ba_prompts`
  ADR-003..ADR-010, grading genuine gaps (🔴 requirement-level ladder, absent
  Business-Rule type), bridge-needed overlaps (🟡 operations crosswalk) and
  justified localizations (🟢 glossary, ГОСТ ТЗ vs SRS), with a C1–C5
  synchronization proposal kept under the human decision gate. Registered both
  artifacts in `research/README.md`, `research/external-knowledge/README.md`,
  `research/mango/README.md`, `governance/artifact-map.md`, the
  structure validator and the MkDocs navigation. Drive-by: registered the
  pre-existing `governance/rfc/methodology-research-and-proposals.md`
  (issue #245) in the structure validator allowlist — it was tracked but never
  added to `is_active_file()`, which left the validator failing on `main`.
- structured: Migration Plan for `mango_ba_prompts` repository (issue #241).
  Added
  `projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md`
  as a draft planning artifact based on the merged Task 2 RFC
  `governance/rfc/repository-archetypes-template-release.md`. The plan records
  the final RFC sections used, current Mango repository snapshot, gap analysis
  against the Prompt & Pattern Library archetype, Scenario A vs Scenario B
  comparison, the in-place migration recommendation, Dev/Prod strategy based on
  GitHub Flow + trunk discipline, and a future GitHub Actions example.
  Registered the artifact in `projects/repo-development/README.md`,
  `governance/artifact-map.md` (v1.39), and the structure validator.
- creative: repository archetypes, project template and release strategy RFC
  (issue #240). Added
  `governance/rfc/repository-archetypes-template-release.md` with a necessity
  analysis, external structure benchmark (LangChain, CrewAI examples, Microsoft
  Foundry samples/templates, Azure AI chat sample), release-model benchmark
  (GitHub Flow, GitFlow, Trunk-Based Development, GitHub Pages Actions), a
  minimal ecosystem repository archetype taxonomy, a Prompt & Pattern Library
  project template, illustrative `mango_ba_prompts` mapping without migration
  instructions, a Governance sync rule (Hub base + local extension), and a
  GitHub Flow + trunk discipline release strategy with a Pages workflow example.
  Registered external sources as `ext-016`..`ext-024`, added navigation in
  `governance/rfc/README.md` and `governance/artifact-map.md`, and extended the
  structure validator to protect the RFC acceptance criteria.
- creative: Research Memory & Source Intelligence RFC (issue #239). Added
  `governance/rfc/research-memory-source-intelligence.md` as a draft framework
  for Knowledge Object primacy over Tier 1 external sources and Tier 2 internal
  research memory. The RFC includes the required necessity analysis, comparison
  of PKM/Zettelkasten/Evergreen Notes, ResearchOps and ADR/Decision Records,
  the five knowledge statuses (`Observed`, `Candidate`, `Applied`, `Rejected`,
  `Superseded`), source-intelligence criteria for separating verifiable claims
  from hype, a concrete Context Engineering traceability example linked to
  `clarify-engine-ai` ADR-009, and anti-dump rules. Registered the RFC in
  `governance/rfc/README.md`, `governance/artifact-map.md` (v1.37), the
  structure validator, and extended `external-sources-registry.md` (v0.4) with
  methodology sources `ext-012`..`ext-015`.
- structured: improve Index/Summary format with ISO phase dates and future-phase
  tagging (issue #237). Added `Дата актуализации фазы` to
  `docs/ecosystem-map-Index.md` (v0.2) for all four ecosystem projects, added
  `Горизонты / Актуально для будущих фаз` to
  `AI_PROJECT_CONTEXT-Summary.md` (v0.2), extended
  `external-sources-registry.md` (v0.3) with `Теги будущих фаз / тем`, and
  replaced the old registry-only discard rule in `CONTRIBUTING.md` (v1.5) and
  `research/external-knowledge/README.md` (v0.3) with future-phase/topic tagging
  plus explicit `rejected` handling for hype/water. Fixed the date-format rule
  in `standards/file-naming.md` (v1.4) as ISO 8601: `YYYY-MM-DD`.
- creative: external sources rules + Index/Summary maps + Habr test (issue #235).
  Added the detail-level suffix rule (`-Index` / `-Summary` / `-Full`) to
  `standards/file-naming.md` (v1.3) with a cross-reference in
  `standards/executable-documentation-standard.md` (v1.2). Codified rules for
  working with external sources — task recognition (label `research` without a
  URL = broad search; concrete URL = study that source), result fixation (a
  studied fact always goes to the registry; a useful insight additionally to
  `external-insights/`; a useless source stays registry-only with status
  «бесполезен» and no insight), and record cleanliness (study facts never enter
  `CHANGELOG.md`) — in `research/external-knowledge/README.md` and
  `CONTRIBUTING.md` (v1.4). Extended `external-sources-registry.md` (v0.2) with
  the `Запись в БЗ`, `Проекты` and `Язык` columns. Created the two-level
  navigation maps: `docs/ecosystem-map-Index.md` (Index over the four ecosystem
  projects) and `AI_PROJECT_CONTEXT-Summary.md` in the hub root, plus staged
  spoke summaries under `docs/project-summaries/` (mango_ba_prompts, open-ai.ru,
  clarify-engine-ai) for later propagation via separate PRs. Tested the
  Index → Summary filter on three Habr articles: registered `ext-009`/`ext-011`
  with insight files and `ext-010` as registry-only «бесполезен». Registered the
  new active artifacts in `governance/artifact-map.md` (v1.36).
- structured: open questions consolidation rule (issue #233). Added the rule
  that open questions from `governance/session-digests.md` must be consolidated
  into `governance/backlog.md` without duplication, with digest links tracked in
  «Связанные дайджесты». Added the `governance/backlog.md` section
  «Открытые вопросы», seeded it from the existing 2026-06-13 session digest,
  and synchronized `CONTRIBUTING.md`,
  `templates/htom/AI_SESSION_HANDOVER_PROMPT.md`, `governance/session-digests.md`
  and `governance/artifact-map.md`.
- creative: documentation architecture balance research and RFC (issue #231).
  Added `governance/rfc/documentation-architecture-balance.md` resolving the
  tension between Anti-Inflation (merge to avoid excess documents) and Atomicity
  (one artifact per file) at ecosystem scale. Introduced an Index → Summary →
  Full detail-level framework (explicitly distinct from Framework L1–L4) and a
  max-three-class document classification (A Index / B Summary / C Full) with
  selection criteria (query frequency, size, reach), class transitions and
  examples applied to real files across the four ecosystem projects (hub,
  mango_ba_prompts, open-ai.ru, clarify-engine-ai). The current-state analysis
  flags whole-file version copies (`…_vN.md`) in clarify-engine-ai as inflation
  and oversized monolithic ADR/RFC/CONCEPT files as lacking entry points.
  Navigation stays bureaucracy-free: markdown links + heading anchors +
  `governance/artifact-map.md`, no `artifact-graph.json`, no CI scrapers, and a
  minimal four-field frontmatter (no new navigation fields). Develops PR #229's
  external-knowledge conclusions (Diátaxis `ext-006`, context engineering
  `ext-008`/`ext-007`) without duplicating its source analysis. Registered the
  RFC in `governance/artifact-map.md` (v1.34), `governance/rfc/README.md` (v1.5)
  and the structure validator. Status `draft`; promotion stays a human decision.
- creative: external knowledge integration research and RFC (issue #227). Added
  the `research/external-knowledge/` domain with a Base Registry of external
  sources (`external-sources-registry.md`, minimal metadata, tag/project
  filtering, no content scraping — Anti-Inflation), an insight storage mechanism
  (`external-insights/` with stages `observation → candidate-practice` and a
  stop-rule before `practices/`) plus three example insights (`ext-001`
  Building Effective Agents, `ext-002` 12-Factor Agents, `ext-003` spec-driven
  development). Added `governance/rfc/external-knowledge-integration.md`
  describing the Base Registry (Hub) + Local Extension (projects) + Smart Sync
  model, lifecycle binding and application for the four ecosystem projects (hub,
  mango_ba_prompts, open-ai.ru, clarify-engine-ai). No CI scrapers; promotion to
  `practices/` stays a human decision. Registered all artifacts in
  `governance/artifact-map.md` (v1.33) and the structure validator.
- creative: session digest mechanism for context transfer between chats
  (issue #225). Added `governance/session-digests.md` as the single storage
  point for session summaries (index + instructions + first digest for the
  2026-06-13 documentation-architecture discussion). The mechanism is for
  external agents (ChatGPT/Claude) on chat-to-chat handover only and explicitly
  does NOT affect the task-executor agent — no token burn on summarization
  during task execution. Propagates to project repos via Smart
  Sync of the `templates/htom/AI_SESSION_HANDOVER_PROMPT.md` genome.

- Issue #209 (Creative mode): ecosystem layer for the Hub. New
  `docs/ecosystem-map.md` (full project graph + the **Need-to-Know** principle —
  the Hub keeps the full graph, each project keeps a partial graph via
  `.hub-ecosystem.json` + `docs/ecosystem-context.md`, synced semi-automatically
  with human confirmation) and a new human-facing guide
  `guides/sync-with-projects.md` (how to keep the map and a project's links in
  sync). Wired the map into `docs/vision.md` (ecosystem positioning),
  `docs/product-concept.md` (new «Функциональная архитектура» and «Зависимости
  от других проектов» sections), `guides/README.md`, root `README.md` and the
  MkDocs nav (`mkdocs.yml`, published under «Продукт»; enabled Material's native
  Mermaid rendering for the connection graph). Extended RFC
  `governance/rfc/hub-vision-concept-proposal-2026-06.md` (0.1 -> 0.2) with
  Decision E (ecosystem representation + Need-to-Know) and issue #209. All new
  artefacts are **Draft**. Allowlisted both new files in
  `tools/validate-repository-structure.sh`.
- Issue #207 (Creative mode): Smart Sync infrastructure for Hub ↔ spoke
  template synchronization. New auto-generated registry `templates/manifest.json`
  (fields `manifest_version`, `last_updated`, `templates[]` with
  `id`/`path`/`version`/`target_type`/`stack`/`min_phase`/`criticality`/`tags`/
  `description`), produced from the hand-maintained `templates/sync-metadata.json`
  by `tools/generate-manifest.py` (`--write`/`--check`) — the manifest is never
  hand-edited. New GitHub Action `.github/workflows/update-manifest.yml`
  regenerates and commits the manifest (`chore: update manifest.json`) on pushes
  to `main` that touch `templates/`. New client `tools/sync-from-hub.sh` with
  `--report` / `--apply` / `--apply --force` / `--init`: it filters templates by
  the local `.hub-profile.json` (target_type, stack, min_phase), compares
  versions against `last_sync`, prints a sync report, and applies safely by
  default (writes `<name>.hub-new.<ext>` alongside local files; `--force`
  overwrites). End-to-end test `experiments/test-smart-sync.sh`. Extended
  `tools/validate-repository-structure.sh` to allowlist and assert the new
  artifacts plus a manifest drift check; bumped `governance/artifact-map.md`
  (1.25 -> 1.26) with rows for the new artifacts.
- Issue #203 (Creative mode): added a single Draft documentation package for the
  Hub product layer. New product docs `docs/vision.md` (Product Vision, L1) and
  `docs/product-concept.md` (Product Concept, L2); RFC
  `governance/rfc/hub-vision-concept-proposal-2026-06.md` comparing approaches
  and listing open questions to the User; a human-facing guide library under
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
  desktop verification screenshot to support User review of the 10 deferred
  portal documents from the repository-quality RFC. The Markdown document
  consolidates clickable links, 2-3 sentence summaries, executor-side disputed
  questions, User decision placeholders, a Q01-Q12 decision matrix and
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
  переводе стандарта в `reviewed`/`canonical` остаётся за Пользователем.

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
  (`2026-06-06-research-documentation-format.md`,
  `2026-06-06-executable-contract-format.md`,
  `2026-06-06-contract-documentation-format.md` и запись решений
  `2026-06-06-governance-folder-structure-decisions.md` плюс навигация
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
  7 вопросами Пользователю); черновик стандарта
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
  `research/hub/2026-06-02-ai-collaboration-retrospective-mango-migration.md` —
  ретроспектива ошибок AI-агента в сессии проектирования миграции Mango
  (Хаб → спок): реестр из 5 ошибок (режимы, pre-flight контекст, Anti-Inflation,
  формат issue, архитектурное размещение артефактов), их корневые причины и
  4 системных вывода для будущего onboarding/governance proposal (режим
  `Research`, governance-файлы не меняются). Имя файла осознанно отличается от
  запрошенного в issue `2026-06-02-ai-collaboration-retrospective.md`: тот файл уже
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
  (решение агента-исполнителя, упрощающее «ментальный список» команды Q сильнее; источники
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
  ([`governance/agent-onboarding.md`](governance/agent-onboarding-protocol.md), создаётся в
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
  обоснование с трассировкой к `research/hub/2026-06-02-ai-collaboration-retrospective.md`;
  фиксация будущих README по каждому кейсу и follow-up-список. Манифест
  намеренно не определяет термины — только использует их со ссылкой на глоссарий.
  Файл зарегистрирован как active в `tools/validate-repository-structure.sh` и
  `governance/artifact-map.md` (тип `RFC`, версия карты 1.6 → 1.7).

### Changed

- adr: Уточнён `docs/adr/2026-07-adr-004-reports-structure.md` по issue #348:
  ADR-004 повышен до v0.3 и закрывает Open Question #1 физическим routing split
  `docs/audit/` для audit-reports и `docs/report/` для general/statistics
  reports. Вариант C сохранён: audit-report остаётся profile внутри base Report
  standard B-043, а Audit process artifacts остаются контрактами в `standards/`
  или `kb/`. ADR-002 повышен до v1.4 с отдельной строкой `Audit report` →
  `docs/audit/`, RFC B-041 получил lifecycle note о решении, artifact-map и
  структурный валидатор синхронизированы. Физическая миграция файлов не
  выполнялась.
- adr: Уточнён `docs/adr/2026-07-adr-004-reports-structure.md` по issue #345:
  текст ADR-004 приведён к русскому стилю ADR-003, убрана англоязычная
  дублирующая пометка к Варианту C, будущие пороги B-043 описаны в будущем
  времени, терминологически неточное свойство заменено на решение/соглашение, а
  контроль пути для audit-отчётов оставлен в блоке компромиссов. Содержательные
  решения ADR-004, routing `docs/report/` и делегирование в B-043/B-044 не
  менялись.
- glossary: Обновлён `standards/glossary.md` по issue #336 / B-020:
  добавлены определения `Research`, `Analysis`, `Audit`, `RFC` и `ADR`;
  уточнены `Standard` и `Contract` через IL-3 / IL-1 и явное
  `Standard ≠ Contract`; добавлены связи Research → RFC → ADR → Standard и
  routing Research / Analysis / Audit по функции артефакта, а не по имени
  каталога. Routing, ADR-002 и `standards/research-standard.md` не менялись.
- rfc: Устранена терминологическая конфляция F-01 в
  `governance/rfc/2026-07-02-rfc-reports-structure.md` по issue #332: две
  конфликтные формулировки заменены на `общий каркас`, чтобы RFC Reports
  описывал структуру будущего стандарта Report без смешения Standard и Contract.
- governance: Синхронизированы `governance/backlog.md` и `CHANGELOG.md` по issue
  #333 после merged PR #303..#331. В backlog статусы B-018, B-019, B-038,
  B-039, B-040, B-041 и B-045 приведены к `DONE`, B-019 связан с issue #326 /
  PR #327, B-038 связан с issue #307 / PR #308 и issue #310 / PR #312,
  B-041..B-045 упорядочены по номеру, а `Unreleased` в changelog сведён к
  единственным секциям `Added`, `Changed` и `Removed` без удаления старых
  записей.
- adr: Добавлен addendum B-019 к
  `docs/adr/2026-06-adr-002-artifact-document-methodology.md` по issue #326.
  ADR-002 теперь явно фиксирует границу `research/<domain>/exp/<issue-slug>/`
  (research evidence corpus, всегда связан с parent dated report) vs `runs/`
  (operational run record, не обязан быть связан с research), включает
  нормативный критерий «один вопрос исполнителю» и ссылается на ADR-003 как
  источник решения и RFC B-016 как источник rationale. Routing-таблица ADR-002
  сохранена без конфликта: строка `Run record` остаётся правилом для
  operational records, а research evidence routing делегирован
  `standards/research-standard.md`.
- adr + standard: Приняты ADR-003 и RFC B-016 по issue #322 / PR #323. Устранены
  причинные дефекты F-01/F-07/F-07-parallel/F-08 из audit B-039: три structure
  standards больше не смешивают Standard и Contract; ADR standard получил
  section-level delegation, минимальный шаблон без invitation to duplicate и
  acceptance checklist; RFC standard получил Research→RFC delegation и правило
  обновления `Decision record` / `Implementation link`; backlog, artifact-map,
  RFC index and CHANGELOG приведены к accepted/status и glossary-aligned
  terminology.
- chore: Исправлены точечные последствия audit B-039 по issue #324 после
  acceptance issue #322. RFC B-016 сохраняет `status: accepted`, `version: 0.3`
  и `updated: 2026-07-02`; forward-refs `not yet — будущий` заменены
  фактическими ссылками на ADR-003 и `standards/research-standard.md`. ADR-003
  сохраняет `status: accepted` и `version: 0.3`; пометка `будущий` у
  `standards/research-standard.md` убрана. Supersession профиля разграничена:
  ADR фиксирует human decision, `standards/research-standard.md` задаёт
  technical replacement, физическое удаление профиля остаётся B-021.
  `standards/research-standard.md` переведён с `version: 1.1` на draft-aligned
  `version: 0.1`; `governance/artifact-map.md` синхронизирован с новой
  формулировкой replacement.
- adr: Устранено дублирование RFC B-016 в `docs/adr/2026-07-adr-003-research-structure.md`
  по issue #316 (версия ADR `0.1` → `0.2`, решение и статус `proposed` не
  изменены). Секция `Decision` больше не пересказывает Proposal P1–P4, а кратко
  фиксирует «принять модель RFC B-016» со ссылками на разделы RFC; `Alternatives
  Considered` делегирует полный разбор в RFC вместо копии таблицы; `Consequences`
  оставляет только архитектурные последствия, а список задач B-018..B-023 отдан
  RFC Impacted Artifacts и `governance/backlog.md`. `Decision Drivers` сжаты до
  трёх. RFC B-016 и стандарты ADR/RFC не изменялись (ограничение issue #316).
- correction: Fixed the placement of the issue #310 deliverables to conform to
  RFC B-016 v0.2 before merge. Moved the reproducible experiment container from
  the legacy sibling format `research/hub/exp-reports-inventory-310/` into the
  target container `research/hub/exp/reports-inventory-310/` (P1) and flattened
  it — the nested `outputs/` directory was removed so evidence files sit next to
  the README and script (P2). Moved the inventory itself from
  `research/hub/2026-07-01-reports-artifacts-inventory.md` to
  `docs/analysis/2026-07-01-reports-artifacts-inventory.md` because an inventory
  is an Analysis, not Research (P4 routing). Updated all links, the artifact-map,
  backlog, research indexes, MkDocs navigation and the structure validator.
  Recorded the root-cause analysis in
  `docs/report/2026-07-01-reports-inventory-placement-analysis.md`.
- backlog: Linked B-038 (Reports inventory and boundaries) to issue #310 and PR
  #312, and recorded `docs/report/` (singular) as the canonical Reports path per
  founder vision §3 and PR review. Physical migration remains deferred to later
  Reports standardization and cleanup work.
- chore: Перенесён report по гипотезе PR #303 из корневого
  `reports/report/2026-06-30-pr-303-rfc-hypothesis-analysis.md` в canonical
  `docs/report/2026-06-30-pr-303-rfc-hypothesis-analysis.md` по issue #311.
  Добавлен frontmatter `owner`, `type`, `context`, `method`, source и related
  links; корневой каталог `reports/` удалён; registry, MkDocs navigation,
  file-naming/frontmatter validators and standards updated for `docs/report/`.
- rfc: Уточнен `governance/rfc/2026-06-30-rfc-research-structure.md` по issue
  #306: добавлены явная матрица дельт A/B/C/D и таблица Boundary RFC/ADR для
  подготовки к ADR B-017. Ошибка генерации PR #303 не подтверждена; гипотеза
  проблемы признана частично существенной как minor completeness gap.
- chore: Accepted the ADR/RFC structure RFCs for issue #286 and delegated their
  normative standard rules into `standards/adr-structure-standard.md` and
  `standards/rfc-structure-standard.md`. Registered both standards in
  `standards/README.md`, `governance/artifact-map.md`,
  `governance/rfc/README.md` and the structure validator; added backlog tech debt
  for frontmatter validator routing, status migration and approved-field policy.
- correction: Normalized Hub research artifact filenames from `YYYY-MM-name.md`
  / `YYYY-name.md` to `YYYY-MM-DD-name.md` using git creation dates (issue
  #271). Updated all repository links, MkDocs navigation, artifact-map entries,
  the file-naming standards, spoke templates, and validation scripts so
  research and spoke `docs/analysis/` artifacts sort correctly when there is
  more than one file per month.

- creative: добавлен раздел «Периодическая суммаризация сессии» в
  `templates/htom/AI_SESSION_HANDOVER_PROMPT.md` (порог 30 обращений / ~50К
  токенов; путь `governance/session-digests.md`; структура контекст/решения/
  открытые вопросы/следующие шаги; агент инициирует вопрос пользователю только
  при передаче контекста в чат). Обновлена `governance/artifact-map.md`.
- structured: strengthened governance contracts for issue #228. Added reverse
  traceability and `traceability` frontmatter fields to the knowledge lifecycle
  RFC, constrained resolver scope to routing plus missing-upstream checks,
  added the Framework vs Template contract to
  `standards/executable-documentation-standard.md`, normalized operational
  terminology to `Пользователь` / `агент-исполнитель`, and expanded structure
  validation coverage for these rules.
- structured: обновить Vision/Concept + создать knowledge-lifecycle + resolver + универсальные шаблоны.
- fix: откатить автоматический перевод Draft → Canonical, требуется явное подтверждение Пользователя.
- Issue #217 PR rebuild (Creative mode): added a separate `practices/` KB for
  fixed practices; extracted Habr agent-work practices with sources/authors;
  added international AI governance practice analysis (NIST AI RMF, EU AI Act,
  ISO/IEC 42001, OpenAI, Anthropic, Google SAIF); introduced
  `frontmatter-docs-standard.md`, `executable-documentation-standard.md` and
  `htom-documentation-structure.md`; added
  `templates/sync-project-with-hub-prompt.md`; refined Vision, Product Concept
  and Ecosystem Map around practice exchange, multi-chat handover and Hub as a
  connective layer; updated validators, manifest metadata and artifact map.
- Issue #217 (Creative mode): audited Hub, `mango_ba_prompts`, `open-ai.ru` and
  `clarify-engine-ai` against current AI governance practices; reframed the Hub
  as a recommendation source rather than a blocker; added the four-field
  `standards/frontmatter-standard.md`; documented Creative override records and
  AI-agent session semantics; split task authoring into structured
  `task.md` and creative `task-creative.md` templates for root and HTOM genome;
  updated validators, manifest metadata and artifact map.
- Issue #218 (Structured mode): removed generated HTML build artifacts from
  `research/mango/` and obsolete PNG screenshots from `docs/screenshots/`.
  Added scoped `.gitignore` rules for those artifact paths and removed the
  deleted files from repository-structure validation.
- Issue #215 (Creative mode): separated **Runtime-онбординг** from chat-to-chat
  context handover and synchronized `AI_SESSION_HANDOVER_PROMPT.md` with a new
  draft standard. Added `standards/session-handover-standard.md`, updated
  `docs/ecosystem-map.md` with the ecosystem principle, expanded the canonical
  `governance/agent-onboarding-protocol.md` and
  `templates/htom/AI_SESSION_HANDOVER_PROMPT.md` with project-type detection,
  `Контекст чата диалога`, `Канал взаимодействия с репо`, `Проверка шаблонов`
  and `Формат постановки задач`. Synced Operating Modes by removing the stale
  `Project` mode from active AI governance contracts in favour of `Creative`
  for open-ended project-context work. Extended structural validation to assert
  the new standard and prompt sections.
- Issue #207 (Creative mode): semantic separation of the onboarding files into
  **protocol** (process/checklist) and **artefact** (copyable prompt). Renamed
  (via `git mv`, history preserved):
  `governance/agent-onboarding.md` -> `governance/agent-onboarding-protocol.md`
  (1.1 -> 1.2) and
  `templates/htom/AI_HANDOVER_PROMPT.md` -> `templates/htom/AI_SESSION_HANDOVER_PROMPT.md`
  (0.2 -> 0.3). Added disambiguation disclaimers — to the protocol
  «⚠️ ЭТО ПРОТОКОЛ (ИНСТРУКЦИЯ). Не копируйте в чат.» and to the prompt
  «⚠️ ЭТО АРТЕФАКТ ДЛЯ КОПИРОВАНИЯ. Скопируйте в новый чат.» Repointed all live
  references across `README.md`, `AI_GOVERNANCE.md`, `governance/`, `standards/`,
  `research/`, `templates/htom/` and both validators. NB: the issue proposed
  `UPPER_CASE` governance paths and a `templates/spoke/` location; both were
  adapted to the repository's `standards/file-naming.md` (governance uses
  kebab-case) and the actual genome layout (the handover prompt lives in
  `templates/htom/`).
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

- Issue #199: updated `standards/README.md`, `research/README.md`,
  `governance/artifact-map.md`, `governance/rfc/README.md`,
  `research/governance/2026-06-06-governance-folder-structure-decisions.md`,
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
  `research/hub/2026-06-02-external-governance-patterns-review.md` (разделы 1.3 и
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
  ретроспективы `research/hub/2026-05-28-project-context-and-bootstrap-patterns.md`
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
- Issue #81: исследование `research/2026-05-28-project-context-and-bootstrap-patterns.md`
  с минималистичными паттернами передачи контекста между чатами, предсказуемого
  создания project areas и маршрута "рекомендация -> задача" на опыте Mango.
  Файл зарегистрирован как active в `tools/validate-repository-structure.sh`,
  `governance/artifact-map.md` и `research/README.md`.
- Issue #79: исследование `research/2026-05-28-prompts-classification-audit.md`
  (аудит входных данных: инвентаризация 6 Mango промптов, паттерны отладки,
  пробелы классификации) и `research/2026-05-28-prompts-classification-standard.md`
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
- Issue #69: справочник `research/mango/2026-05-27-capability-decomposition.md`
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
  Atomic Function` в `research/mango/2026-05-22-classification.md` (v3.0): семь доменов
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

- Issue #91: рефакторинг структуры `research/` (namespacing). Фундаментальные
  (`scope: repo-wide`) исследования перенесены через `git mv` из корня в новый
  подкаталог `research/hub/` (`2026-05-28-project-context-and-bootstrap-patterns.md`,
  `2026-05-28-prompts-classification-audit.md`,
  `2026-05-28-prompts-classification-standard.md`,
  `2026-06-01-team-c-governance-strategy-audit.md`,
  `2026-05-28-user-prompts-analysis.md`); добавлен `research/hub/README.md`.
  `research/README.md` получил строгое правило о запрете файлов в корне
  `research/` и актуализированное оглавление; пути обновлены в
  `governance/artifact-map.md` (v1.4). Валидатор структуры теперь требует
  подкаталоги `research/hub` и `research/mango` и запрещает любые файлы в корне
  `research/`, кроме `README.md`.
- Issue #77: прототипные `_exp` prompt-файлы для User Story и Use Case
  заменены короткими copy-paste промптами; валидатор структуры теперь проверяет
  наличие ровно 6 файлов в `projects/mango/prompts/` и лимиты длины prompt body
  для `_exp` / `_simple`.
- Issue #67: `research/mango/2026-05-22-classification.md` обновлён с версии 2 до v3.0
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

- chore: Удалён legacy `standards/research-profile.md` по issue #340 / B-021
  после замены на `standards/research-standard.md` (B-018). Причина — завершение
  цепочки Research standardization B-016..B-020 и устранение конкурирующего
  источника правил для research-артефактов; активные ссылки и реестры
  перенаправлены на `research-standard.md`, исторические упоминания оставлены
  только как migration/provenance context.
- Issue #199: removed the active `research/portal/` package, the old mixed
  `standards/webportal-concept-standard.md`, the portal-specific
  `standards/portal-repository-structure.md`, the old
  `templates/webportal-concept-template.md` and the generated root `.gitkeep`
  placeholder.

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

- Issue #52: draft-концепция `research/mango/2026-05-26-taxonomy-concept.md`
  для Unified Capability Taxonomy Mango: обзор применимых стандартов,
  мета-модель capability, mapping реальных фич, процесс нормализации,
  интерфейс продуктовых команд, метрики, план пилота и риски.
- Issue #49: active directory indexes for `projects/`, `research/`,
  `education/` and `frameworks/` after cleanup of legacy `-old` inputs.
- Issue #49: active Mango research artifacts in `research/mango/`
  (`README.md`, `2026-05-22-classification.md`, `2026-05-22-classification-tz.md`,
  `2026-05-22-requirements-flow.md` and HTML exports) with frontmatter and source
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
- Заменить license placeholder после решения Пользователя.
