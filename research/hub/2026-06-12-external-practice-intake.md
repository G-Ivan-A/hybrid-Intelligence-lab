---
status: draft
version: 0.1
updated: 2026-06-12
temperature: 0.1
---

# External Practice Intake: Agent Work And HTOM Docs

This research records how external practices were evaluated for issue #217 and
which ones were promoted into fixed Hub practice nodes. It also records the
`mango_ba_prompts/docs/` structure pattern requested in the PR feedback.

## Research vs fixed practices

| Layer | Artifact | Role |
| --- | --- | --- |
| Source analysis | This file | Keeps source notes, alternatives, applicability, and rejected overreach. |
| Fixed practice catalog | [practices/README.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/README.md) | Lists accepted practice nodes. |
| Atomic agent-work nodes | [practices/agent-work/](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/practices/agent-work) | Reusable behaviors imported by projects when applicable. |
| HTOM docs structure | [standards/htom-documentation-structure.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/htom-documentation-structure.md) | Standardizes project documentation layout without editing Mango now. |

Research remains evidence. Practice nodes are the reusable knowledge base.

## Sources Studied

| Source | Author | Link | Useful signal |
| --- | --- | --- | --- |
| Claude Code production experience article | Artem Chirkov | https://habr.com/ru/articles/1045510/ | Hybrid search, Definition of Ready, persistent context, and the Explore -> Plan -> Code -> Test -> Review -> Ship loop. |
| Hermes Skill Hub article | slam | https://habr.com/ru/articles/1045552/ | Skills as reusable workflow packages, catalog scaling risk, dependency/deprecation metadata, and token-budget discipline. |

## Candidate Structure Tested

| Option | Pros | Cons | Decision |
| --- | --- | --- | --- |
| Put practices inside `docs/` | Easy to publish with product docs. | Violates the requested separation; mixes narrative documentation with executable KB. | Rejected. |
| Put practices inside `research/` | Keeps sources nearby. | Research can compare and question; fixed practices need stable import paths. | Rejected. |
| Create top-level `practices/` | Clear KB boundary; atomic nodes can link back to research and templates. | Requires repo-model, validator, and artifact-map updates. | Accepted. |

The accepted structure follows
[standards/executable-documentation-standard.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/executable-documentation-standard.md):

```text
research/hub/2026-06-12-external-practice-intake.md
        │
        ▼
practices/agent-work/README.md
        │
        ├── hybrid-search-before-action.md
        ├── definition-of-ready-check.md
        ├── plan-verify-ship-loop.md
        ├── skills-as-reusable-workflows.md
        └── skill-catalog-token-budget.md
```

## Extracted Practices

| Practice | Source | Why useful in Hub | Fixed node |
| --- | --- | --- | --- |
| Hybrid search before action | Artem Chirkov | Prevents edits before reading validators, artifact map, and linked docs. | [practices/agent-work/hybrid-search-before-action.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/agent-work/hybrid-search-before-action.md) |
| Definition of Ready check | Artem Chirkov | Converts broad Creative tasks into reviewable artifacts and checks. | [practices/agent-work/definition-of-ready-check.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/agent-work/definition-of-ready-check.md) |
| Plan-verify-ship loop | Artem Chirkov | Matches the issue-solver flow: explore, plan, implement, validate, commit, update PR. | [practices/agent-work/plan-verify-ship-loop.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/agent-work/plan-verify-ship-loop.md) |
| Skills as reusable workflows | slam | Gives a promotion path from repeated workflow to reusable practice/template. | [practices/agent-work/skills-as-reusable-workflows.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/agent-work/skills-as-reusable-workflows.md) |
| Skill catalog token budget | slam | Prevents practice catalogs from becoming prompt overload. | [practices/agent-work/skill-catalog-token-budget.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/agent-work/skill-catalog-token-budget.md) |

## Mango docs error pattern

The Mango docs tree was inspected through the GitHub API. It contains valuable
work in `docs/adr/`, `docs/analysis/`, `docs/audit/`, `docs/reviews/`, and
root-level docs. The recurring problem is not content quality; it is mixed
documentation purpose.

| Observed pattern | Why it matters | Hub response |
| --- | --- | --- |
| Root `docs/` mixes domain overview, RFC-like docs, templates, dependencies, taxonomy, and task templates. | A new agent cannot tell which files are narrative, executable, or decision records. | [standards/htom-documentation-structure.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/htom-documentation-structure.md) requires a `docs/README.md` and purpose-specific subfolders. |
| `docs/ba-ecosystem.md` is large and central. | Large catch-all docs are hard to review and partially import. | Use focused docs plus KB/practice nodes for reusable behaviors. |
| ADR numbering is inconsistent (`0001-*` and `001-*`). | Sorting and references become ambiguous. | Standard uses four-digit ADR prefixes. |
| Prompt/template-like docs are in the documentation tree. | Copyable execution surfaces can be mistaken for descriptive docs. | Prompts belong in `prompts/` or Hub `templates/`, not narrative docs. |

No Mango files are changed by this PR. The Hub now records the structure pattern
so a future Mango sync can propose a focused migration.

## Import Rule For Projects

Projects should use
[templates/sync-project-with-hub-prompt.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/templates/sync-project-with-hub-prompt.md)
to compare local structure and practices against the Hub. The prompt must
propose imports and local adaptations; it must not overwrite project-specific
decisions.

## Open Questions

| Question | Current answer |
| --- | --- |
| Should `practices/` be published on the public MkDocs site? | Not now. The issue asked to avoid putting practices into documentation structures. |
| Should practice nodes have custom frontmatter fields? | Not now. Source, author, link stay in the body per [standards/frontmatter-docs-standard.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/frontmatter-docs-standard.md). |
| Should Mango be reorganized in this PR? | No. This PR creates the Hub standard and sync prompt only. |
