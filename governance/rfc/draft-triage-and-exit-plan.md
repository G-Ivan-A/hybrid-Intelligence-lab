---
status: canonical
version: 0.2
updated: 2026-06-07
ai-generated: true
type: rfc
context: [governance, draft-lifecycle, triage, repository-quality, templates, research, education]
method: "document-audit + relation-scan + exit-planning"
scope: repo-wide
related_artifacts:
  - "governance/rfc/repository-quality-improvement-plan.md"
  - "governance/artifact-map.md"
  - "governance/backlog.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/186"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/171"
---

# RFC: Draft Triage And Exit Plan

This RFC resolves the analysis part of issue #186. It does not approve,
rewrite, move, or delete the target documents by itself. It records the current
state of the 20 documents marked "К доработке" in
[repository-quality-improvement-plan.md](repository-quality-improvement-plan.md)
and gives every document a concrete exit path from draft.

## Executive Summary

The 20 target drafts are not one uniform problem. They fall into four different
operational cases:

| Group | Documents | Main risk | Recommended direction |
| --- | ---: | --- | --- |
| Template placeholders | 7 | Source templates intentionally contain `{{...}}` placeholders, while one RFC is already partly implemented but still looks like an open draft. | Create a template-placeholder policy, then approve or explicitly keep the templates as source templates; close or supersede the executable-contract RFC. |
| Hub research | 7 | Several research drafts already fed standards/backlog decisions, but their outputs and limitations are not reconciled with the current repository. | Mark source research as reviewed only after recommendation matrices are reconciled with standards, backlog, or explicit deferral. |
| Mango research | 4 | Research is useful but operational execution now belongs mostly in the external `mango_ba_prompts` spoke; one file has weak relation metadata. | Keep Hub copies as reviewed research sources, push operational work into the external spoke, and fix relation metadata before promotion. |
| Education project | 2 | The project is registered as active in the artifact map, but its content is still a sandbox/raw-ideas area. | Decide whether it is a public project area or an internal sandbox, then align `projects/README.md`, artifact map semantics, and education-profile expectations. |

Near-term cleanup should focus on low-risk governance consistency: placeholder
policy, RFC closure status, relation metadata, and explicit project scope.
Promotion of research into canonical standards should wait for owner review or
pilot evidence.

## Audit Method

The audit used four checks:

- Read all 20 target files and their local navigation contexts.
- Scanned frontmatter, placeholders, links, mentions, and stale paths.
- Compared recommendations with current standards, backlog, artifact map, and
  the repository-quality RFC.
- Kept implementation decisions separate from human approval. Every exit plan
  below names an `approval_target`, `dependencies`, `required_changes`, and
  `estimated_effort`.

## Group 1: Template Placeholders And Executability RFC

This group contains six source templates with intentional placeholders and one
governance RFC that already drove implementation work. The common issue is not
poor content quality; it is unclear lifecycle semantics.

| Document | Current state, links, and specific problems | Exit plan |
| --- | --- | --- |
| `templates/htom/AI_GOVERNANCE.md` | Draft source template for a spoke governance contract. Frontmatter uses `{{date}}`; body uses `{{project_name}}` and `{{hub_url}}`. Links to Hub governance are placeholders by design. Problem: a normal active document with unresolved placeholders would be invalid, but source templates need a different rule. | `approval_target`: template source contract. `dependencies`: template-placeholder policy in `templates/htom/README.md` and validator behavior. `required_changes`: define that source templates may keep placeholders, require `init.sh` replacement for generated spokes, and then mark the template `reviewed` or introduce a template-specific canonical status. `estimated_effort`: S. |
| `templates/htom/AI_HANDOVER_PROMPT.md` | Draft executable template, already aligned with `executable: true` and EXECUTION/EXPLANATION blocks. It intentionally keeps `{{REPO_NAME}}` for runtime copy/paste and `{{date}}` in frontmatter. Problem: execution readiness is high, but placeholder lifecycle and source-of-truth relation to `governance/agent-onboarding.md` need explicit approval. | `approval_target`: executable spoke handover template. `dependencies`: `standards/executable-contract-standard.md`, `governance/agent-onboarding.md`, template-placeholder policy. `required_changes`: confirm exact placeholder replacement semantics and source-of-truth statement; after approval set status to `reviewed` or template-canonical. `estimated_effort`: S. |
| `templates/htom/AI_QUICK_RULES.md` | Draft executable quick-start template with placeholders and links to Hub rules. It already reflects current agent survival rules and executable-document structure. Problem: same unresolved placeholder ambiguity; no independent exit criteria. | `approval_target`: executable spoke quick-rules template. `dependencies`: executable-contract standard and template-placeholder policy. `required_changes`: add a small lifecycle note in the template README that this file remains a source template until instantiated; verify quick rules still match current agent-onboarding and artifact-map wording. `estimated_effort`: S. |
| `templates/htom/CHANGELOG.md` | Draft changelog scaffold using `{{date}}` and Keep a Changelog style. Problem: a changelog template should not be judged by the same currentness rule as a live changelog. | `approval_target`: spoke changelog scaffold. `dependencies`: template-placeholder policy. `required_changes`: document that the first generated spoke changelog must replace date/project placeholders and may start with `status: canonical` only after initialization. `estimated_effort`: XS. |
| `templates/htom/CONTRIBUTING.md` | Draft contribution workflow template. It has source-template placeholders and a generic PR checklist. Problem: no explicit boundary between Hub contribution rules and spoke-local adaptation. | `approval_target`: spoke contribution template. `dependencies`: `CONTRIBUTING.md`, `standards/issue-workflow.md`, template-placeholder policy. `required_changes`: add a short source-of-truth note in the template README or template body and verify generated links after `init.sh`. `estimated_effort`: S. |
| `templates/htom/README.md` | Central draft template for spoke repository README. It documents placeholders, `init.sh`, validator behavior, and two onboarding entry points. Problem: it is the right place to define template lifecycle, but it still has draft status and does not fully close the placeholder exception. | `approval_target`: canonical source for spoke-template lifecycle. `dependencies`: founder decision on source-template status, spoke validator expectations. `required_changes`: add a "Template placeholder policy" section, state which placeholders are allowed in source templates, and define generated-spoke DoD. `estimated_effort`: M. |
| `governance/rfc/contract-executability-rfc.md` | Draft RFC v1.1 with Human Review decisions from 2026-06 and implemented follow-up in `standards/executable-contract-standard.md`, `governance/agent-onboarding.md`, and spoke templates. Problem: it still reads like an active proposal even though major decisions are already accepted or delegated to canonical standards. | `approval_target`: closed RFC decision record, either `reviewed/canonical` or explicitly `superseded`. `dependencies`: executable-contract standard, agent-onboarding, CE issue registry, template updates. `required_changes`: add a decision-status table for accepted/deferred/superseded sections; identify the standard as owner of normative rules; update status only after founder confirms closure semantics. `estimated_effort`: M. |

Recommended decision: approve source templates as a special lifecycle class
before changing their statuses. Do not remove placeholders from source
templates; instead, make placeholder replacement part of generated-spoke DoD.

## Group 2: Hub Research

This group contains research and navigation documents that informed standards,
backlog, and governance decisions. The main exit path is not "make every
research file canonical"; it is to reconcile each output with the active
standard/backlog it influenced.

| Document | Current state, links, and specific problems | Exit plan |
| --- | --- | --- |
| `research/governance/README.md` | Draft navigation for governance-format research. It points to research files whose outputs already became `standards/research-profile.md`, `standards/executable-contract-standard.md`, `standards/contract-documentation-standard.md`, and governance folder decisions. Problem: index status lags behind the derived standards. | `approval_target`: reviewed/canonical navigation. `dependencies`: current statuses of derived standards and decision records. `required_changes`: update summaries to distinguish active standards from source research; then promote navigation status. `estimated_effort`: S. |
| `research/hub/external-governance-patterns-review-2026-06.md` | Draft external-patterns review with take/defer/reject recommendations for fail-closed behavior, capability taxonomy, evidence model, approval semantics, and trigger review. Links remain current. Problem: "take now" recommendations are partly implemented, but the matrix has not been reconciled with current backlog and standards. | `approval_target`: reviewed research source. `dependencies`: backlog state, executable-contract standard, glossary, issue workflow. `required_changes`: add an implementation-status column for each recommendation and move remaining accepted work into backlog or explicit deferral. `estimated_effort`: M. |
| `research/hub/project-context-and-bootstrap-patterns-2026-05.md` | Draft context/bootstrap research tied to Mango migration and runtime onboarding. Related artifacts now include external `mango_ba_prompts` after archive removal. Problem: some operational recommendations predate the final archive-removal and external-spoke decision. | `approval_target`: reviewed source research for onboarding/bootstrap decisions. `dependencies`: PR #174 archive-removal outcome, `governance/agent-onboarding.md`, spoke templates. `required_changes`: update the conclusion with current external-spoke state and mark which recommendations were implemented, deferred, or superseded. `estimated_effort`: M. |
| `research/hub/prompts-classification-audit-2026-05.md` | Draft audit of prompt materials. It records source limitations, including inaccessible DOCX material, and references external `mango_ba_prompts`. Problem: the evidence base is explicitly incomplete and should not be promoted without that limitation. | `approval_target`: reviewed audit with limitation, not a standard. `dependencies`: access to source prompt files and external Mango repository state. `required_changes`: re-run or spot-check the audit against current external sources; keep the DOCX limitation visible; update relation metadata if sources moved. `estimated_effort`: M. |
| `research/hub/prompts-classification-standard-2026-05.md` | Draft research document named like a standard. It defines a six-axis taxonomy, matrices, prompt templates, and asks whether to move a concise version into `standards/`. Problem: name and status can mislead reviewers into treating it as normative, but it has not yet been validated by prompt integration. | `approval_target`: either reviewed research source or new canonical prompt-classification standard. `dependencies`: audit update, user-prompts analysis, at least one pilot integration. `required_changes`: decide whether to rename as research or extract a short standard; avoid promoting the full research body as-is. `estimated_effort`: L. |
| `research/hub/team-c-governance-strategy-audit-2026-05.md` | Draft Team C strategy audit with recommendations TC-GOV-001..006. Later research and backlog entries absorbed parts of it. Problem: recommendation ownership and current status are not explicit. | `approval_target`: reviewed or superseded research source. `dependencies`: external-governance review and backlog. `required_changes`: add a status table for each TC-GOV recommendation: implemented, delegated, deferred, rejected, or superseded. `estimated_effort`: S-M. |
| `research/hub/user-prompts-analysis-2026-05.md` | Draft analysis of 18 user prompts using the draft prompt-classification taxonomy. It depends on the classification standard and external prompt material. Problem: it cannot exit before the taxonomy decision; otherwise it may lock in a draft taxonomy as a rule. | `approval_target`: reviewed applied research after taxonomy decision. `dependencies`: prompt-classification standard decision and external Mango source availability. `required_changes`: update examples against accepted taxonomy or keep them as exploratory cases; move operational follow-up to spoke issues only after taxonomy approval. `estimated_effort`: M. |

Recommended decision: use `reviewed` for source-backed research after each
document records how its recommendations map to active standards/backlog.
Reserve `canonical` for navigation, standards, and decision records.

## Group 3: Mango Research

These documents are valuable domain research, but the operational Mango prompt
work now belongs in the external `mango_ba_prompts` spoke. Hub research should
preserve decision context and reviewed models without becoming the live Mango
knowledge base.

| Document | Current state, links, and specific problems | Exit plan |
| --- | --- | --- |
| `research/mango/capability-decomposition-2026-05.md` | Very large draft capability catalog with atomic feature entries, NFR linkage, and integration with `mango_ba_prompts/kb/product-matrix.md`. Body links mostly point to current active or external artifacts. Problem: frontmatter `related_artifacts` mixes path and version (`classification.md v3.0`) and still names `classification-glossary.md`, which is no longer an active local path. Promotion also requires SME review because the file is product-domain heavy. | `approval_target`: reviewed Mango capability research. `dependencies`: product SME review, external Mango glossary/source decision, taxonomy pilot. `required_changes`: fix relation metadata to path-only values or external URLs, add owner-reviewed sample coverage, and record review scope before status promotion. `estimated_effort`: L. |
| `research/mango/requirements-lifecycle-uncertainty-2026-05.md` | Draft process research for raw requirement `0 -> 1`, ambiguity maps, case modeling, gates, metrics, and n8n-oriented prompt orchestration. Links to related Mango research and external `mango_ba_prompts` are current. Problem: recommendations are candidates for a future process standard, not approved rules; there is no explicit exit plan section. | `approval_target`: reviewed research source or future Mango BA process standard. `dependencies`: PO/Founder choice of uncertainty model and pilot metrics. `required_changes`: add an exit-plan note, record chosen uncertainty model, and only extract a standard after pilot evidence. `estimated_effort`: M. |
| `research/mango/rag-mapping-roadmap-2026-05.md` | Draft roadmap for `kb/product-matrix.md`, source confidence, diagrams, and prompt-chain pilot increments in external `mango_ba_prompts`. Links are current and mostly operationally specific. Problem: roadmap items are not tracked as external spoke tasks and should not remain only as Hub research recommendations. | `approval_target`: reviewed roadmap research plus external spoke backlog. `dependencies`: external `mango_ba_prompts` ownership and source-indexing policy. `required_changes`: convert accepted increments into external spoke issues or backlog items; add status of each roadmap stage; keep Hub copy as rationale. `estimated_effort`: M. |
| `research/mango/taxonomy-concept-2026-05.md` | Draft Unified Capability Taxonomy concept with domains, maturity, evidence fields, evolution rules, pilot plan, and PO/Founder questions. Links to active Mango research and external spoke are current. Problem: it is a strong standard candidate but still lacks pilot approval, owner assignment, and private-data boundary decisions. | `approval_target`: future `standards/feature-taxonomy.md` or reviewed Mango research. `dependencies`: taxonomy owner, pilot corpus, evidence policy, external spoke integration. `required_changes`: run pilot, decide owner and threshold rules, then extract concise normative taxonomy if approved. `estimated_effort`: L. |

Recommended decision: do not move Mango research into Hub standards until at
least one pilot demonstrates stable taxonomy, evidence, and source-owner rules.
Use the external spoke for implementation backlog and examples.

## Group 4: Education Project

The education files are not obsolete, but their scope is ambiguous. They are
registered in the artifact map as active project artifacts while their language
describes a sandbox of ideas.

| Document | Current state, links, and specific problems | Exit plan |
| --- | --- | --- |
| `projects/education-ba-prompt/README.md` | Draft navigation for a future BA prompt-engineering course sandbox. It links to `standards/education-profile.md`, project structure rules, and issue workflow. Problem: `governance/artifact-map.md` treats the file as required/active, while `projects/README.md` active project list currently emphasizes repo-development and migration history. | `approval_target`: project scope decision. `dependencies`: Founder/PO choice: public project area vs internal sandbox. `required_changes`: if public, list it consistently in `projects/README.md`; if sandbox, label scope explicitly and decide whether artifact-map "required" is appropriate. `estimated_effort`: S. |
| `projects/education-ba-prompt/docs/course-ideas.md` | Draft raw material for course modules, terms, exercises, and prompt templates. Links to education profile are current. Problem: it is useful raw input, but not a curriculum artifact and has no exit criteria for becoming one. | `approval_target`: raw-ideas backlog or first reviewed course concept. `dependencies`: education project scope decision and course owner. `required_changes`: add a "not curriculum yet" boundary and a conversion checklist, or split accepted items into course artifacts per education profile. `estimated_effort`: M. |

Recommended decision: keep the education area as a sandbox unless Founder/PO
explicitly approves it as a public project area with an owner and course
roadmap.

## Cross-Cutting Recommendations

1. Define source-template lifecycle.
   Source templates may contain `{{...}}` placeholders. Generated spokes must
   not keep unresolved placeholders except deliberately documented runtime
   placeholders such as `{{REPO_NAME}}` in a copied handover prompt.

2. Add draft exit-plan expectations.
   Any non-trivial document with `status: draft` should include one of:
   `approval_target`, `dependencies`, `required_changes`, `estimated_effort`,
   or a clearly named "Exit plan" section. Short scaffolds may instead point to
   a parent template lifecycle rule.

3. Separate research source status from normative status.
   Research can become `reviewed` when evidence, limitations, and outputs are
   reconciled. It becomes a standard only after a concise normative extraction
   and human approval.

4. Keep Mango operations in the external spoke.
   Hub research should link to `mango_ba_prompts` and record decisions. Live
   prompt chains, product matrix entries, and pilot examples should be tracked
   in the external spoke.

5. Align project registration semantics.
   If a project appears as required in artifact map, the corresponding project
   README should explain whether it is active public work, a sandbox, or a
   historical/migrated area.

## 9. Масштабируемость и защита от бюрократии (Anti-Bureaucracy)

Founder approval for issue #193 adds the following Phase 1 constraints to keep
draft cleanup reviewable and prevent metadata inflation:

1. **Unidirectional Links.** Research may point to standards as its output or
   normative owner. Standards must not carry research backlinks in frontmatter;
   if a major standard bump needs rationale traceability, record that link in
   the changelog or body history instead.
2. **Index over Frontmatter.** Deep relation matrices belong in
   `governance/artifact-map.md` or catalog `README.md` files. Frontmatter
   `related_artifacts` should stay at three or fewer critical links and should
   use path-only local values or explicit external URLs.
3. **Lazy Reconciliation.** Moving research to `reviewed` does not force
   immediate updates to every influenced standard. Standards are reconciled when
   they receive a planned major version bump or when an issue explicitly targets
   that standard.
4. **Static Exit-Plans.** Draft exit-plan fields such as `approval_target` and
   `dependencies` are a point-in-time snapshot. They do not require cascading
   rewrites when adjacent documents change; update them only when reviewing that
   draft or executing the named phase.

These rules are intentionally procedural. They govern how cleanup proceeds; they
do not promote Phase 2/3 research, create new artifacts, or require broad
metadata deduplication in this PR.

## Phased Plan

| Phase | Scope | Deliverables |
| --- | --- | --- |
| Phase 1: Governance consistency | Low-risk cleanup that does not change domain content. | Template placeholder policy; closure decision table for `contract-executability-rfc.md`; fixed relation metadata for `capability-decomposition-2026-05.md`; updated `research/governance/README.md`; education scope decision recorded. |
| Phase 2: Research reconciliation | Map draft recommendations to accepted standards, backlog, or deferral. | Status matrices for hub research; prompt-classification decision; external Mango roadmap issues; explicit limitations for prompt audit and user-prompt analysis. |
| Phase 3: Pilot-backed promotion | Promote only after owner review or pilot evidence. | Taxonomy/process standard extraction if approved; Mango pilot evidence; first education course concept or explicit sandbox retention. |

## Questions To Founder And PO

1. Should source templates get a dedicated lifecycle rule, or should they remain
   `draft` until generated-spoke validation is implemented?
2. Should `governance/rfc/contract-executability-rfc.md` become a canonical
   accepted RFC, or should it be marked as superseded by
   `standards/executable-contract-standard.md`?
3. Should prompt classification stay as reviewed research, or should a concise
   prompt-classification standard be extracted now?
4. Should Mango research in this Hub be reviewed rationale only, with all live
   operational work moved to `mango_ba_prompts` issues/backlog?
5. Should `projects/education-ba-prompt/` be a public active project area or a
   sandbox that remains registered only as raw material?
6. Which owner role can approve domain-heavy Mango research: Founder/PO,
   product SME, BA owner, or a named taxonomy owner?

## Definition Of Done For This RFC

- All 20 target documents from issue #186 are listed.
- Every document has current-state analysis, specific problems, and an exit
  plan with approval target, dependencies, required changes, and effort.
- The four requested groups are covered separately.
- Placeholder strategy, draft lifecycle rule, Mango external-spoke boundary,
  and education scope ambiguity are called out.
- The RFC is registered in RFC navigation, artifact map, and structure
  validation so it is not an untracked active artifact.
- Local frontmatter and structure validators pass.
