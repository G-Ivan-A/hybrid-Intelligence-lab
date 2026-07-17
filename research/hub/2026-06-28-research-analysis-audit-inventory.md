---
status: draft
version: 0.1
updated: 2026-06-28
temperature: 0.1
type: internal-analysis
context: [hub, mango, clarify, research, analysis, audit, classification, standardization, issue-288]
method: repository-scan
scope: ecosystem
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/288"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/288"
related_artifacts:
  - "docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md"
  - "docs/adr/2026-06-adr-002-artifact-document-methodology.md"
  - "standards/research-standard.md"
  - "research/hub/2026-06-25-artifact-inventory-and-classification.md"
  - "research/hub/2026-06-28-ripple-effects-282-research.md"
  - "research/hub/exp/research-analysis-audit-288/2026-06-28-artifact-classification-matrix.md"
external_artifacts:
  - "G-Ivan-A/mango_ba_prompts@ed636a38a762e848907fcaf607fecf764dcbb9c8"
  - "G-Ivan-A/clarify-engine-ai@96c288fd13a2d7cc7c3e3cdd52574944858e6255"
---

# Research / Analysis / Audit: инвентаризация и план стандартизации

> **Режим:** анализ для issue
> [#288](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/288).
> Документ не создаёт RFC, standard, ADR, новые директории или переезды файлов.
> Он фиксирует фактическую картину и планирует три будущие цепочки
> `Analysis -> RFC -> Standard`.

## 1. Введение

### 1.1. Причина

В Hub, Mango и Clarify накопились документы, которые называются Research,
Analysis, Audit, Report, RFC, Review или находятся в одноимённых каталогах, но
их фактическая роль не всегда совпадает с именем пути. Это мешает запускать
стандартизацию: один будущий стандарт "для analysis" не сможет покрыть
исследования внешних источников, локальные отчёты и проверки соответствия без
смешения смыслов.

Issue #288 просит сквозную инвентаризацию артефактов Research / Analysis /
Audit в трёх репозиториях и план запуска трёх отдельных цепочек
`Analysis -> RFC -> Standard`: Research, Analysis и Audit.

### 1.2. Охват

Сканировались tracked files в следующих путях:

| Repo | Snapshot | Paths |
| --- | --- | --- |
| Hub / `hybrid-Intelligence-lab` | `1a2a9cdfb37ab7e689b143d94623923ade65e33a` | `research/**`, `docs/**` |
| Mango / `mango_ba_prompts` | `ed636a38a762e848907fcaf607fecf764dcbb9c8` | `research/**`, `docs/**` |
| Clarify / `clarify-engine-ai` | `96c288fd13a2d7cc7c3e3cdd52574944858e6255` | `research/**`, `docs/**` |

Файлы не переносились и не переименовывались. Внешние репозитории
использовались только как read-only corpus. Собственные файлы issue #288
исключены из Hub scan baseline, чтобы повторный запуск после merge не менял
матрицу из-за добавленного отчёта и experiment directory.

### 1.3. Метод

Классификация опиралась на содержательную роль документа, а не только на путь:

| Actual type | Рабочий критерий |
| --- | --- |
| Research | создаёт или сравнивает знания: внешние источники, гипотезы, варианты, market / industry evidence, source-backed выводы |
| Analysis | разбирает локальный контекст: состояние репозитория, execution report, inventory, summary, roadmap без проверки на норму |
| Audit | проверяет состояние по норме, контракту, checklist, expected behavior или явно фиксирует verification / validation |
| Other | ADR, RFC/proposal, standard, navigation, guide, concept, template, screenshot или продуктовая справка |

Воспроизводимый снимок лежит в
[exp/research-analysis-audit-288/2026-06-28-artifact-classification-matrix.md](exp/research-analysis-audit-288/2026-06-28-artifact-classification-matrix.md).
Скрипт:
[exp/research-analysis-audit-288/scan-artifacts.py](exp/research-analysis-audit-288/scan-artifacts.py).
Матрица является эвристическим evidence layer; этот документ фиксирует
человеческую интерпретацию и план.

## 2. Результаты анализа

### 2.1. Главный вывод

Три будущих стандарта нужны отдельно. Корпус показывает не одну стадию
"analysis", а три разные операции:

1. **Research** отвечает на вопрос "что известно и какие варианты существуют?".
   Это самый сильный контур в Hub: `research/`, `standards/research-profile.md`
   и серия source-backed исследований уже задают стиль.
2. **Analysis** отвечает на вопрос "что происходит в локальном контексте?".
   Сейчас это слабее всего нормировано: в Mango и Clarify `docs/analysis/`
   одновременно содержит analysis, research, audit, report и RFC/proposal.
3. **Audit** отвечает на вопрос "соответствует ли текущее состояние норме?".
   Audit-артефакты наиболее проверяемы, но часто прячутся под analysis/report
   naming и не имеют единого профиля evidence/severity/remediation.

Практический вывод: стандартизацию надо запускать тремя независимыми цепочками
`Analysis -> RFC -> Standard`, иначе будущий стандарт будет закреплять текущую
перегрузку `analysis`.

### 2.2. Сводная матрица

| Repo | Research | Analysis | Audit | Other | Text artifacts | Non-text docs artifacts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Hub / `hybrid-Intelligence-lab` | 42 | 3 | 6 | 21 | 72 | 7 |
| Mango / `mango_ba_prompts` | 10 | 3 | 11 | 28 | 52 | 19 |
| Clarify / `clarify-engine-ai` | 12 | 11 | 7 | 40 | 70 | 15 |

Counts are directional, not normative. They are useful for spotting the shape of
the corpus:

- Hub is research-heavy and already has a research profile, but also keeps some
  historical standards/audits under `research/hub/`.
- Mango concentrates mixed analytical work in `docs/analysis/`: research,
  audit, RFC/proposal and local reports share one directory.
- Clarify has the clearest explicit `docs/audit/` set, but its `docs/analysis/`
  contains sprint/report/triage documents and its `docs/research/` is local to
  `docs/`, not the Hub-style root `research/`.

## 3. Дельты между репозиториями

| Area | Hub | Mango | Clarify | Delta |
| --- | --- | --- | --- | --- |
| Research home | root `research/` by domain | mostly `docs/analysis/`; no root `research/` in scanned corpus | `docs/research/` | Need one routing rule per archetype, not one global path rule. |
| Analysis home | no dedicated `docs/analysis/` corpus in Hub | `docs/analysis/` is a catch-all | `docs/analysis/` is sprint/report/analysis area | Analysis needs a profile independent from folder name. |
| Audit home | small `docs/audit/` plus historical research-side audits | `docs/audit/` and audit files in `docs/analysis/` | explicit `docs/audit/` with verification reports | Audit needs a standard evidence/remediation model and routing exceptions. |
| RFC/proposal adjacency | canonical governance in `docs/rfc/`; research docs may prepare RFCs | RFC-like docs appear in `docs/analysis/` and `docs/` | ADR-like decisions live in `docs/ADR/` | RFC/proposal must stay out of R/A/A standards except as downstream dependency. |
| Frontmatter | Hub-style four required fields plus research metadata | partial Hub-aligned frontmatter in newer docs | many older docs without Hub frontmatter | Future standards need migration mode, not immediate hard enforcement. |

## 4. Подмена понятий и дубли

### 4.1. Audit спрятан как Analysis

| Artifact | Why it is Audit in content |
| --- | --- |
| `mango_ba_prompts/docs/analysis/2026-06-24-naming-convention-audit.md` | checks naming violations against a convention |
| `mango_ba_prompts/docs/analysis/2026-06-24-runs-contract-log-policy-audit.md` | checks runs contract/log policy conformance |
| `mango_ba_prompts/docs/analysis/2026-06-22-mango-taxonomy-convergence-test.md` | validation/convergence test, not neutral analysis |
| `clarify-engine-ai/docs/analysis/2026-05-19_code-review-triage_v1.md` | verifies review findings and triages fixes |

Pattern: if the document contains norm/check/result/remediation semantics, the
standardization chain should treat it as Audit even when the folder is
`docs/analysis/`.

### 4.2. Research спрятан как Analysis

| Artifact | Why it is Research in content |
| --- | --- |
| `mango_ba_prompts/docs/analysis/2026-06-24-artifact-chain-hypothesis-research.md` | explores a hypothesis about artifact chains |
| `mango_ba_prompts/docs/analysis/2026-06-25-telecom-vendors-ba-practices-research.md` | builds empirical external evidence from telecom vendors |
| `mango_ba_prompts/docs/analysis/2026-06-23-repository-structure-analysis.md` | source-backed architecture/repository-structure research despite analysis path |
| `clarify-engine-ai/docs/research/2026-05-21_bl-61_market-research_v1.md` | market comparison research in a docs-local research folder |

Pattern: path-level "analysis" often means "knowledge work". The future
Research standard should define when comparative/external evidence becomes
Research even if the local repo lacks root `research/`.

### 4.3. RFC/proposal спрятан как Analysis

| Artifact | Why it is Other/proposal |
| --- | --- |
| `mango_ba_prompts/docs/analysis/2026-06-02-migration-strategy-rfc.md` | RFC function and title, not analysis output |
| `mango_ba_prompts/docs/analysis/2026-06-22-rfc-industry-taxonomy-improvement.md` | proposal for taxonomy improvement |
| `mango_ba_prompts/docs/analysis/2026-06-22-rfc-rules-registry-system.md` | proposal for rules registry |
| `mango_ba_prompts/docs/rfc-format-validator.md` | RFC tooling/reference, not R/A/A |

Pattern: RFC/proposal artifacts should be dependencies or downstream stages of
R/A/A chains, not members of the R/A/A artifact types themselves.

### 4.4. Duplicate and overlap risks

| Cluster | Risk | Treatment |
| --- | --- | --- |
| Hub `2026-06-25-artifact-inventory-and-classification.md` vs this issue | overlapping inventory topic | keep as base evidence; this issue narrows to Research / Analysis / Audit and adds Clarify |
| Mango `2026-06-23-repository-structure-analysis.md` vs Hub `2026-06-23-repository-structure-concept.md` | sequential repository-structure variants | cite both as Research inputs; do not merge in this task |
| Clarify BL-61 market research v1, RU education v1/v2 | version/adaptation chain can look like duplicates | future Research standard should require relation fields: supersedes, adapts, based_on |
| Mango `docs/ba-process/` vs `docs/ba-processes/` | archive/current process naming ambiguity | outside R/A/A standardization, but Analysis/Audit RFC should define archive/current signals |
| Clarify `docs/ADR/004-*` and `docs/ADR/007-*` | duplicate ADR numbering | adjacent governance issue, not part of this R/A/A task |

## 5. План запуска трёх цепочек стандартизации

Это отдельный плановый раздел для issue #288. Он определяет только будущие
цепочки; этот PR намеренно не создаёт RFC или Standard artifacts.

### 5.1. Research chain: `Analysis -> RFC -> Standard`

| Item | Plan |
| --- | --- |
| Current base | `standards/research-profile.md`; Hub `research/` corpus; `research/hub/2026-06-25-artifact-inventory-and-classification.md`; RFC/ADR industry-norm research from issue #278; Mango and Clarify research-like examples from this matrix |
| Gap | No ecosystem-wide rule for root `research/` vs `docs/research/` vs research in `docs/analysis/`; no required relation fields for versions/adaptations; unclear rule for research that prepares RFC/ADR without being an RFC/ADR |
| Analysis artifact | Dedicated analysis of research profiles across archetypes, using this issue's matrix as the seed corpus |
| RFC scope | Define Research purpose, evidence classes, source policy, frontmatter, relation fields, path routing and examples for archetypes A-D |
| Standard scope | Normative Research Profile v2 or Research Standard: required sections, source/evidence requirements, reproducibility, relation metadata, placement rules |
| Dependencies | ADR-002 lifecycle, frontmatter issue #282 decisions, artifact-map routing, RFC/ADR standardization outcomes from issue #278 |

Archetype coverage:

| Archetype | Repo mapping | Research routing question |
| --- | --- | --- |
| A: Governance & Knowledge Hub | Hub | root `research/<domain>/` remains canonical; research can prepare RFC/ADR without becoming RFC/ADR |
| B: Prompt & Pattern Library | Mango | decide whether source-backed work stays in `docs/analysis/` or gets a local research home |
| C: Product Spoke / Runtime | Clarify | decide whether `docs/research/` is acceptable for product-spoke research |
| D: Education | no dedicated repo in this scan | define default route and evidence level without inventing a migration |

### 5.2. Analysis chain: `Analysis -> RFC -> Standard`

| Item | Plan |
| --- | --- |
| Current base | ADR-002 lifecycle; project summaries in Hub; Mango/Clarify `docs/analysis/` reports; this matrix's split between Analysis, Research, Audit and Other |
| Gap | `analysis` is a catch-all label; no profile separates local-context analysis, inventory, execution report, synthesis and RFC-prep; no completion criteria |
| Analysis artifact | Dedicated analysis of local-context analysis documents and report/inventory patterns |
| RFC scope | Define Analysis as local-context reasoning, not external research and not conformance audit; specify allowed subtypes, relation to RFC, and examples for archetypes A-D |
| Standard scope | Analysis Standard: required problem/context/findings/options/limitations sections, source of truth, non-normative boundaries, allowed outputs |
| Dependencies | Research chain definitions, Audit chain definitions, artifact-map routing, frontmatter migration mode |

Archetype coverage:

| Archetype | Repo mapping | Analysis routing question |
| --- | --- | --- |
| A: Governance & Knowledge Hub | Hub | where cross-repo analysis lives when it is not external research |
| B: Prompt & Pattern Library | Mango | how to split existing `docs/analysis/` into analysis vs research vs audit semantics without moving files immediately |
| C: Product Spoke / Runtime | Clarify | how sprint reports, kickoff docs and repo-state reports map to Analysis |
| D: Education | no dedicated repo in this scan | define lightweight analysis profile for curriculum/content repos later |

### 5.3. Audit chain: `Analysis -> RFC -> Standard`

| Item | Plan |
| --- | --- |
| Current base | `docs/audit/` in Hub/Mango/Clarify; validators in Hub; Mango naming/runs audits; Clarify verification/smoke/comprehensive audit reports |
| Gap | No shared Audit profile for norm, evidence, severity, remediation, re-check status and exceptions; audit files appear in both `docs/audit/` and `docs/analysis/` |
| Analysis artifact | Dedicated analysis of audit reports and validator-backed checks across the three repos |
| RFC scope | Define Audit purpose, evidence levels, finding severity, remediation tracking, relation to CI/validators and placement rules for archetypes A-D |
| Standard scope | Audit Standard: required sections, finding schema, proof format, re-run policy, links to validators and issue/PR lifecycle |
| Dependencies | Frontmatter issue #282, repository-structure rules from ADR-001, artifact lifecycle from ADR-002, validator ownership and CI policy |

Archetype coverage:

| Archetype | Repo mapping | Audit routing question |
| --- | --- | --- |
| A: Governance & Knowledge Hub | Hub | how validator-backed governance audits should reference standards and RFCs |
| B: Prompt & Pattern Library | Mango | how prompt/taxonomy/process conformance audits differ from analysis notes |
| C: Product Spoke / Runtime | Clarify | how smoke/E2E/verification reports become durable audit artifacts |
| D: Education | no dedicated repo in this scan | define minimum audit profile for content quality and curriculum governance later |

### 5.4. Sequencing

| Step | Action | Output |
| --- | --- | --- |
| 1 | Freeze definitions from this analysis as working vocabulary | issue comment or backlog item, no file moves |
| 2 | Start Research chain | dedicated Research analysis artifact, then RFC, then Standard |
| 3 | Start Analysis chain after Research boundaries are clear | dedicated Analysis analysis artifact, then RFC, then Standard |
| 4 | Start Audit chain with validator/evidence focus | dedicated Audit analysis artifact, then RFC, then Standard |
| 5 | Only after standards are accepted, plan optional migrations | separate issues for renames/moves/frontmatter updates |

Recommended order: Research first, Analysis second, Audit third. Research already
has the strongest base; Analysis depends on knowing what is not Research; Audit
can then define checks against standards and validators without turning every
report into an audit.

## 6. Статус выполнения issue #288

| Requirement | Status | Evidence |
| --- | --- | --- |
| Scan Hub, Mango, Clarify target paths | done | matrix output covers `research/**` and `docs/**` snapshots for all three repos |
| Classify by actual content/purpose | done | this document uses Research / Analysis / Audit / Other semantics and lists substitutions |
| Identify deltas | done | section 3 |
| Identify duplicates and concept substitutions | done | section 4 |
| Plan three standardization chains | done | section 5 |
| Keep plan as separate section | done | section 5 |
| Do not create RFC/standard or move files | done | only analysis artifact, experiment script and evidence matrix are added |

## 7. Источники

- Issue #288:
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/288>
- Matrix:
  [exp/research-analysis-audit-288/2026-06-28-artifact-classification-matrix.md](exp/research-analysis-audit-288/2026-06-28-artifact-classification-matrix.md)
- Existing Hub inventory:
  [2026-06-25-artifact-inventory-and-classification.md](2026-06-25-artifact-inventory-and-classification.md)
- Research profile:
  [../../standards/research-standard.md](../../standards/research-standard.md)
- ADR-001:
  [../../docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md](../../docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md)
- ADR-002:
  [../../docs/adr/2026-06-adr-002-artifact-document-methodology.md](../../docs/adr/2026-06-adr-002-artifact-document-methodology.md)
