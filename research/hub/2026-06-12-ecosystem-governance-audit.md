---
status: draft
version: 0.1
updated: 2026-06-12
temperature: 0.1
type: internal-analysis
context: [hub, governance, ai-agents, ecosystem]
method: repository-audit
---

# Ecosystem Governance Audit

## Scope

Audit for issue
[#217](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/217).
The goal is to improve Hub governance without turning the Hub into a blocker
for downstream projects.

Reviewed repositories:

| Repository | Snapshot | Why reviewed |
| --- | --- | --- |
| `G-Ivan-A/hybrid-Intelligence-lab` | branch `issue-217-4c43638864f0` | Source Hub, standards, validators and templates. |
| `G-Ivan-A/mango_ba_prompts` | `eed2a6f` | Mature prompt-governance practice, Creative override precedent and frontmatter discipline. |
| `G-Ivan-A/open-ai.ru` | `cbc0d40` | Early spoke with product/solution docs and lightweight AI collaboration rules. |
| `G-Ivan-A/clarify-engine-ai` | `96c288f` | Production-oriented repository with quality gates, ADRs, security and data handling controls. |

The audit is not a full compliance assessment. It extracts practices that are
useful for the Hub as a recommendation source and rejects controls that would
inflate the Hub beyond its current role.

Follow-up rebuild artifacts split this first-pass audit into executable knowledge
layers:

- [2026-06-12-external-practice-intake.md](2026-06-12-external-practice-intake.md)
  records Habr source intake, Mango docs error pattern and agent-work practice
  extraction.
- [2026-06-12-international-ai-governance-practices.md](2026-06-12-international-ai-governance-practices.md)
  records international governance practice analysis and an executable
  implementation matrix.
- [practices/README.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/README.md) contains fixed reusable
  practice nodes separated from research.

## External Governance Practices

| Practice source | Useful pattern for the Hub | Adaptation in this PR |
| --- | --- | --- |
| NIST AI RMF | Governance should connect context, risks, measurement and management instead of relying on a single policy document. | Task templates require context, artifacts, acceptance criteria, validation and traceability. |
| EU AI Act | Obligations are risk-based and proportionate. Not every AI activity needs the same controls. | The Hub distinguishes recommendations from hard bans and allows documented Creative overrides. |
| ISO/IEC 42001 | AI governance works as a management system: repeatable roles, records, review and improvement. | `AI_GOVERNANCE.md`, `CONTRIBUTING.md`, issue templates and validators form a lightweight management loop. |
| OpenAI preparedness practice | Higher-risk work needs explicit thresholds, evaluation and escalation. | Hard bans, escalation triggers and validation evidence are kept explicit in governance and task templates. |
| Anthropic Responsible Scaling Policy | Capabilities and deployment risk should trigger stronger controls. | The Hub keeps Creative mode flexible but requires a record when it bypasses a recommendation. |
| Google SAIF | Security-by-design and traceability matter for AI-enabled systems. | Secrets/private data remain hard bans; production-grade controls are reserved for spoke repositories that need them. |

## Repository Findings

### Hub

Strengths:

- Clear repo model, artifact map, standards registry and local validators.
- HTOM/spoke separation already prevents production controls from leaking into
  the Hub by default.
- Runtime onboarding protocol and handover prompt make agent startup explicit.

Gaps:

- Frontmatter previously treated `ai-generated` as required, while the ecosystem
  needed a smaller base-field convention.
- Root governance did not yet state that the Hub is a recommendation source,
  not a mechanical blocker.
- Creative mode existed as an operating mode but lacked a documented override
  protocol.
- RFCs could still be read as binding rules before human acceptance.
- `templates/htom/.github/ISSUE_TEMPLATE/task.md` mixed structured and creative
  needs in one template.
- Artifact map contained a duplicate `research/mango/README.md` row.

### `mango_ba_prompts`

Practices worth importing:

- Four-field prompt frontmatter (`status`, `version`, `updated`,
  `temperature`) keeps metadata lightweight.
- Creative governance explicitly allows justified deviation from a template
  when the result and rationale are recorded.
- Task templates separate context, expected result, freedom of executor,
  constraints and acceptance criteria.
- "Silence is not automatic action" is stated for AI work: humans must restart
  or explicitly request the next iteration.

Practices not imported wholesale:

- Mango-specific prompt taxonomies and domain metadata belong in the Mango
  repository, not in the Hub core.

### `open-ai.ru`

Useful signal:

- Early-stage product/spoke documentation benefits from compact governance:
  task mode, task template, product concept and solution concept.
- A spoke needs enough guidance to work with the Hub, but not the whole Hub
  governance tree copied locally.

Hub implication:

- The Hub should publish task and governance recommendations that spokes can
  adopt selectively.

### `clarify-engine-ai`

Useful signal:

- Production repositories need stronger controls: ADRs, RACI, CI quality gates,
  security policy, data masking and release discipline.

Hub implication:

- These practices are good references for production spokes, but they should
  not become mandatory Hub defaults. The Hub should point to them as examples
  when risk or product maturity justifies the extra structure.

## Decisions Taken

1. Make `standards/frontmatter-standard.md` the canonical lightweight metadata
   rule: `status`, `version`, `updated`, `temperature`.
2. Update `tools/validate-frontmatter.sh` so the new required set is executable.
3. Reframe `AI_GOVERNANCE.md`: the Hub recommends, records and validates, but
   does not block downstream teams mechanically.
4. Add a Creative override protocol with a mandatory record of rule bypass,
   rationale, artifact and validation.
5. Add AI-agent specifics to root and HTOM contributing docs: no automatic
   post-session monitoring, comments require manual restart, merge/comment/close
   semantics are explicit.
6. Split task authoring into two Markdown templates:
   `.github/ISSUE_TEMPLATE/task.md` for structured execution and
   `.github/ISSUE_TEMPLATE/task-creative.md` for creative tasks.
7. Mirror the structured/creative task templates into `templates/htom/` so new
   HTOM teams inherit the practice.
8. Clarify RFCs as recommendations until accepted and delegated to canonical
   artifacts.
9. Remove the duplicate artifact-map row and register the new audit, standard
   and templates.

## Follow-up Candidates

- Add a production-spoke governance profile only after at least one spoke needs
  it in practice.
- Add CI checks for frontmatter drift only after the warning-only validator
  becomes too easy to ignore.
- Review downstream repositories after they adopt the new templates and record
  actual friction before adding more structure.

## Sources

- [NIST AI Risk Management Framework 1.0](https://www.nist.gov/itl/ai-risk-management-framework)
- [EU AI Act, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)
- [ISO/IEC 42001 AI management systems](https://www.iso.org/standard/42001)
- [OpenAI safety and preparedness](https://openai.com/safety/)
- [Anthropic Responsible Scaling Policy](https://www.anthropic.com/responsible-scaling-policy)
- [Google Secure AI Framework](https://saif.google/)
