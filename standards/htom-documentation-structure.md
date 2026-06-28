---
status: accepted
version: 1.0
updated: 2026-06-12
temperature: 0.1
owner: G-Ivan-A
---

# HTOM Documentation Structure

This standard defines the recommended documentation structure for HTOM
repositories that synchronize with the Hub. It uses the `mango_ba_prompts/docs/`
inspection as a concrete warning case, but does not edit Mango.

## Mango docs error pattern

The inspected Mango docs tree contains valuable material, but several purposes
crowd the same root:

| Pattern | Risk |
| --- | --- |
| Large catch-all domain file such as `docs/ba-ecosystem.md` | Hard to review, partially import, or turn into atomic practices. |
| RFC, dependency notes, taxonomy, task templates, reviews, and process docs mixed in root `docs/` | Agents cannot infer which documents are descriptive, executable, or decision records. |
| ADR naming split between `0001-*` and `001-*` | Sorting and references become ambiguous. |
| Missing `docs/README.md` index | New contributors read by filename guesswork. |
| Templates stored as ordinary documentation | Copyable execution surfaces are easy to confuse with narrative docs. |

## Standard HTOM Layout

```text
docs/
  README.md
  overview.md
  adr/
    0001-short-title.md
  rfc/
    yyyy-mm-topic.md
  audit/
    yyyy-mm-topic.md
  reviews/
    yyyy-mm-topic.md
  decisions/
    yyyy-mm-topic.md
```

Recommended non-`docs/` neighbors:

```text
prompts/
  README.md
kb/
  README.md
templates/
  README.md
```

## Placement Rules

| Artifact class | Place | Rule |
| --- | --- | --- |
| Human-facing overview | `docs/overview.md` or another focused `docs/*.md` | Narrative only; no copyable prompt bodies. |
| ADR | `docs/adr/NNNN-title.md` | One decision per file, monotonically increasing four-digit prefix. |
| RFC | `docs/rfc/YYYY-MM-topic.md` | Proposal or recommendation before a local decision. |
| Audit/review | `docs/audit/` or `docs/reviews/` | Evidence and findings; not a reusable practice by itself. |
| Prompt | `prompts/` or Hub `templates/` | Executable copy surface; do not bury it in narrative docs. |
| Project knowledge base | `kb/` | Project-specific reusable knowledge that is not suitable for Hub-wide `practices/`. |
| Hub practice import | Local issue or PR linked to `practices/` | Import only what applies; keep local deviations explicit. |

## Sync With Hub

Use [templates/sync-project-with-hub-prompt.md](../templates/sync-project-with-hub-prompt.md)
to start a synchronization pass. The prompt compares the project with Hub
standards, templates, and practice nodes, then proposes imports that fit the
project's type and current constraints.

## Review Checklist

1. `docs/README.md` exists and explains what each docs subfolder is for.
2. Every root `docs/*.md` file has one clear purpose.
3. ADR filenames use one numbering scheme.
4. Prompts and templates are not mixed with descriptive docs.
5. Research findings stay in research/audit files until promoted to fixed
   practices.
6. Imported Hub practice nodes are linked by path and adapted through a local
   issue or PR, not copied silently.
