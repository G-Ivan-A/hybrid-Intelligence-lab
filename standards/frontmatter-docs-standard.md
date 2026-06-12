---
status: canonical
version: 1.0
updated: 2026-06-12
temperature: 0.1
---

# Frontmatter Docs Standard

This standard specializes the base
[frontmatter-standard.md](frontmatter-standard.md) for documentation classes. The
goal is a necessary and sufficient metadata contract: enough fields for
automation and review, without turning every Markdown file into a database.
Base artifact path: `standards/frontmatter-standard.md`.

## Base Rule

Every active Markdown artifact keeps the four mandatory fields from
[frontmatter-standard.md](frontmatter-standard.md):

| Field | Required | Purpose |
| --- | --- | --- |
| `status` | yes | Lifecycle state: `draft`, `reviewed`, `canonical`, or another controlled status already used by the repo. |
| `version` | yes | Human-managed artifact version. |
| `updated` | yes | Last meaningful content update date. |
| `temperature` | yes | Expected AI operating mode: low for contracts/standards, higher for creative drafts. |

Extra fields are allowed only when a tool, template, provenance rule, or
document class consumes them. If a field is only explanatory, put the explanation
in the body.

## Document Classes

| Class | Examples | Necessary and sufficient frontmatter | Optional only when consumed |
| --- | --- | --- | --- |
| Standard | `standards/*.md` | `status`, `version`, `updated`, `temperature` | `executable` when the standard itself must be performed; otherwise body text explains applicability. |
| Guide | `guides/*.md` | `status`, `version`, `updated`, `temperature` | `audience`, `entrypoint` when navigation or tooling uses it. |
| RFC | `governance/rfc/*.md` | `status`, `version`, `updated`, `temperature` | `executable` when the RFC is an accepted instruction; otherwise RFCs remain proposals or rationale. |
| ADR | `docs/adr/*.md` in HTOM repos | `status`, `version`, `updated`, `temperature` | `decision`, `supersedes` only if a local ADR index reads them. |
| Research | `research/<domain>/*.md` | `status`, `version`, `updated`, `temperature` | `source`, `scope`, `type` when they improve traceability and match `standards/research-profile.md`. |
| Template | `templates/**/*.md` | `status`, `version`, `updated`, `temperature` | `executable`, `entrypoint`, and approved placeholders when Smart Sync or an agent consumes them. |
| Practice | `practices/**/*.md` | `status`, `version`, `updated`, `temperature` | `source` only if automated provenance checks are added; otherwise source, author, link live in the body. |

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
2. Which version is being reviewed or synced?
3. When was it last materially changed?
4. What AI operating temperature should be used around it?
5. Is there a tool or executable contract that consumes any extra field?

If the fifth answer is "no", do not add the extra field.
