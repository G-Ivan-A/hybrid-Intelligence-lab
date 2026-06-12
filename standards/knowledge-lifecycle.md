---
status: draft
version: 0.1
updated: 2026-06-12
temperature: 0.1
---

# Knowledge Lifecycle

This draft standard defines how knowledge artifacts move through the Hub without
turning every idea into an active rule too early.

Status note: this is the target draft for
[knowledge-lifecycle-proposal.md](../governance/rfc/knowledge-lifecycle-proposal.md).
It can become canonical only after founder review.

## Lifecycle Chain

```text
Observation -> Research -> Hypothesis -> RFC -> Pattern -> Standard -> Template -> Framework -> Deprecation/Archive
```

## Stage Table

| Stage | What it is | Repository location | Who can use it | Transition criteria |
| --- | --- | --- | --- | --- |
| Observation | Raw signal: incident, comment, repeated question, external example, project feedback. | Issue, PR comment, audit note, or `research/<domain>/` when it needs preservation. | Humans and AI agents as context only. | Enough repeated signal or risk exists to justify structured analysis. |
| Research | Source-backed analysis that compares alternatives and records evidence. | `research/<domain>/`. | Reviewers, contributors, AI agents preparing a decision. | The research names an applicable practice, unresolved risk, or decision candidate. |
| Hypothesis | Testable claim about a better way to work. | Usually inside research, issue body, or RFC section. | Humans and AI agents as a proposed direction. | The hypothesis has an owner, expected benefit, and failure condition. |
| RFC | Reviewable proposal for changing governance, structure, standards, templates, or lifecycle. | `governance/rfc/`. | Humans for decision; AI agents as proposal context. | Founder or delegated reviewer accepts, rejects, or asks for changes. |
| Pattern | Reusable behavior observed to work, but still adaptable by context. | `practices/<domain>/` for fixed practice nodes; research remains the source rationale. | Projects can import or adapt it with rationale. | Repeated use shows the pattern is stable enough to become a rule, template, or framework part. |
| Standard | Mandatory format, rule, or quality gate for a class of artifacts. | `standards/`. | Contributors and AI agents must apply it when in scope. | A template, validator, or project framework needs a reusable operational surface. |
| Template | Copyable starting form or executable prompt. | `templates/`. | Projects and AI agents can copy, sync, or execute it. | The template is stable, has approved placeholders, and is registered where sync/validation expects it. |
| Framework | L1-L2 product framework or a methodology package for a project class. | `docs/` for Hub Vision/Concept; `frameworks/` when a reusable methodology package is needed. | Humans align on direction; projects choose applicable methodology pieces. | The framework is linked to L3-L4 methodology and has enough practice/standard support to be useful. |
| Deprecation/Archive | Final state for outdated artifacts that should no longer guide new work. | Prefer `status: superseded` plus replacement links; physical archive requires explicit decision. | Humans and AI agents use it only as history. | Replacement exists or the artifact is proven obsolete; removal or archival is done through PR. |

## Framework vs Methodology

The Hub separates product framing from operating methodology:

| Level | Layer | Location | Question answered |
| --- | --- | --- | --- |
| L1 | Vision / Framework boundary | `docs/vision.md` | Why the Hub exists. |
| L2 | Product Concept / Framework scope | `docs/product-concept.md`, `docs/ecosystem-map.md` | What the Hub does and how the ecosystem exchanges value. |
| L3 | Methodology contracts | `governance/`, `standards/`, `practices/` | How decisions, rules, and reusable practices work. |
| L4 | Operational surfaces | `templates/`, `tools/`, project-specific adaptations | How a team executes or imports the methodology. |

A framework document at L1-L2 must link to the L3-L4 methodology needed for
execution. A methodology artifact at L3-L4 must avoid redefining the product
vision; it should link back to the framework layer instead.

## Resolver Rules

The resolver decides where a new artifact belongs. Its executable surface is
[resolve-artifact-location-prompt.md](../templates/resolve-artifact-location-prompt.md).

| Mode | Resolver behavior |
| --- | --- |
| Structured | Record lifecycle gaps and soft violations in the PR, then complete the requested task inside the explicit scope. Do not silently promote an artifact to the next lifecycle stage. |
| Creative | If a required prior stage is missing, initiate the smallest missing document or proposal needed to make the work reviewable. If blocked, create what is safe and document the dependency. |

Hard violations require explicit human approval before proceeding:

- changing the top-level repository structure;
- deleting or overwriting user work;
- bypassing Anti-Inflation;
- bypassing fail-closed behavior for security, publication, privacy, or legal risk.

Soft violations are recorded in the PR:

- lifecycle stage skipped in Structured mode;
- minor frontmatter mismatch that can be fixed locally;
- using a draft artifact as context while clearly marking it as draft.

## Silence Rule

Silence means acceptance of the current review state only. It does not approve a
transition to the next lifecycle stage. Promotion from RFC to Standard, Template,
or Framework requires an explicit merge/review decision or a clear founder
comment such as "approve", "canonical", or "skip stage X".

## Deprecation And Archive

An artifact becomes deprecated when one of these is true:

- a newer artifact supersedes it;
- its assumptions are invalid;
- it causes repeated confusion or failed validation;
- its target project or practice is no longer active.

Deprecation steps:

1. Set `status: superseded` or record a removal PR when the artifact should
   disappear entirely.
2. Add a visible replacement link near the top of the file if the file remains.
3. Update `governance/artifact-map.md`, indexes, validators, and template
   manifest metadata if the artifact was active.
4. Preserve history through git and PR links. Create a physical archive only
   when an issue explicitly approves that exception.
