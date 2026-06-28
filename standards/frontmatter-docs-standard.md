---
status: accepted
version: 1.1
updated: 2026-06-28
temperature: 0.1
owner: G-Ivan-A
---

# Frontmatter Docs Standard

This standard specializes the base
[frontmatter-standard.md](frontmatter-standard.md) for documentation classes. The
goal is a necessary and sufficient metadata contract: enough fields for
validators, indexes, templates and governance rules, without turning every
Markdown file into a parallel database.

Base artifact path: `standards/frontmatter-standard.md`.
Validator: `tools/validate-frontmatter.sh`.

## Base Rule

Every active Markdown artifact keeps the four base fields:

| Field | Required | Purpose |
| --- | --- | --- |
| `status` | yes | Lifecycle state from the vocabulary for the artifact class. |
| `version` | yes | Human-managed artifact version. |
| `updated` | yes | Last meaningful content update date. |
| `temperature` | yes | Expected AI operating mode: low for contracts/standards, higher for creative drafts. |

Extra fields are allowed only when a validator, index, template, executable
contract, provenance rule or document class consumes them. If a field is only
explanatory, put the explanation in the body.

`ai-generated` is forbidden in frontmatter. AI provenance belongs in issue, PR,
changelog, audit or session records when it matters for review.

## Status Vocabularies

Frontmatter `status` is the canonical machine-readable status. Body-level status
tables may summarize the same state for humans, but they do not override
frontmatter.

| Artifact type | Paths | Status vocabulary | Semantics |
| --- | --- | --- | --- |
| Knowledge | `research/`, `docs/analysis/` | `draft`, `reviewed`, `canonical`, `superseded` | Knowledge maturity: written, reviewed, accepted as reusable basis, obsolete. |
| Governance | `docs/rfc/`, `governance/rfc/`, `docs/adr/`, `standards/`, `ai-rules/` | `draft`, `proposed`, `accepted`, `rejected`, `deprecated`, `superseded` | Decision process: drafted, proposed for review, accepted/rejected, retired or replaced. |

Mixing vocabularies is invalid for paths covered by these classes. For example,
`canonical` is valid for research but invalid for ADR/RFC/standards, while
`accepted` is valid for governance but invalid for research.

## Document Classes

| Class | Examples | Necessary and sufficient frontmatter | Optional only when consumed |
| --- | --- | --- | --- |
| Standard | `standards/*.md` | `status`, `version`, `updated`, `temperature`, `owner` | `executable`, `entrypoint`, `scope`, `level`, `concept_type`, `related_standards`, `related_templates`, `related_issues` when the validator or standard process consumes them. |
| RFC | `governance/rfc/*.md`, `docs/rfc/*.md` | `status`, `version`, `updated`, `temperature`, `owner`, `rfc-scope` | `executable`, `entrypoint`, and legacy research-routing fields only when consumed. |
| ADR | `docs/adr/*.md` | `status`, `version`, `updated`, `temperature`, `owner`, `decision-type` | `supersedes`, `executable`, `entrypoint` only when a local ADR index or validator consumes them. |
| Research | `research/<domain>/*.md`, `docs/analysis/*.md` | `status`, `version`, `updated`, `temperature` | `source`, `scope`, `type`, `context`, `method`, `related_*`, `external_artifacts`, `stage`, `projects`, `source_id`, `based_on` when they improve traceability and match [research-profile.md](research-profile.md). |
| Guide | `guides/*.md` | `status`, `version`, `updated`, `temperature` | `audience`, `entrypoint`, `executable` when navigation or tooling uses it. |
| Template | `templates/**/*.md` | `status`, `version`, `updated`, `temperature` | `executable`, `entrypoint`, `level`, `standard`, and approved placeholders when Smart Sync or an agent consumes them. |
| Practice | `practices/**/*.md` | `status`, `version`, `updated`, `temperature` | `source`, `executable`, `entrypoint` when automated provenance or execution checks use them. |
| GitHub issue template | `.github/ISSUE_TEMPLATE/*.md`, `templates/*/.github/ISSUE_TEMPLATE/*.md` | GitHub template keys plus base fields | `name`, `about`, `title`, `labels`, `assignees` are GitHub-consumed fields, not governance metadata. |

## Governance Fields

Governance artifacts require `owner` because ownership is needed for review
routing, dashboards and validation. The owner may be a human login or owning
group.

ADR artifacts also require `decision-type`:

- `governance`
- `methodology`
- `product`
- `curriculum`
- `runtime`

RFC artifacts also require `rfc-scope`:

- `A` - Governance & Knowledge Hub
- `B` - Prompt & Pattern Library
- `C` - Product Spoke / Runtime, including Library/SDK profiles
- `D` - Education / Learning Package
- `multi` - cross-archetype RFC

## Dependencies Between Fields

| Condition | Required companion |
| --- | --- |
| `executable: true` | Body must follow [executable-documentation-standard.md](executable-documentation-standard.md) or [executable-contract-standard.md](executable-contract-standard.md). |
| `entrypoint: true` | Artifact must be listed from a known navigation entry such as `README.md`, `AI_GOVERNANCE.md`, or `governance/artifact-map.md`. |
| Template placeholders such as `{{project_name}}` | Placeholder must be allowed by `tools/validate-repository-structure.sh` and documented in the template or template README. |
| External research claim | Body must contain source, author or organization, link, and applicability notes. |

## Decision Rule

Use the smallest field set that lets humans and tools answer these questions:

1. Is this artifact active?
2. Which lifecycle vocabulary applies?
3. Which version is being reviewed or synced?
4. When was it last materially changed?
5. What AI operating temperature should be used around it?
6. Does a validator, template, index or governance rule consume each extra field?

If the sixth answer is "no", do not add the extra field.
