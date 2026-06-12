---
status: draft
version: 0.1
updated: 2026-06-12
temperature: 0.1
---

# RFC: Knowledge Lifecycle

## Proposal

Adopt [standards/knowledge-lifecycle.md](../../standards/knowledge-lifecycle.md)
as the Hub lifecycle for knowledge artifacts:

```text
Observation -> Research -> Hypothesis -> RFC -> Pattern -> Standard -> Template -> Framework -> Deprecation/Archive
```

## Problem

The Hub already has research, practices, standards, templates, frameworks, and
product docs, but there is no single rule that explains how knowledge moves
between them. That makes it easy to promote an idea too early or to create a
template without a traceable prior stage.

## Decision Scope

This RFC proposes the lifecycle standard only. It does not approve every draft
artifact currently in the repository and does not promote any RFC to canonical
status by itself.

## Target Artifact

| Target | Status in this PR | Promotion condition |
| --- | --- | --- |
| `standards/knowledge-lifecycle.md` | Draft candidate | Founder review or explicit delegated approval. |

## Key Rules

- Each stage has a default location, user group, and transition criteria.
- Framework L1-L2 lives in `docs/`; Methodology L3-L4 lives in
  `governance/`, `standards/`, `practices/`, `templates/`, `tools/`, and
  project/framework packages.
- Structured mode logs lifecycle gaps and completes the explicit task without
  silently promoting artifacts.
- Creative mode can initiate missing prior documents when that is the smallest
  way to make the work reviewable.
- Silence means acceptance of current state only, not approval to transition to
  the next stage.

## Acceptance Criteria

- The lifecycle chain is documented end to end.
- Each stage has a repository location, user group, and transition criteria.
- Resolver behavior for Structured and Creative modes is described.
- Deprecation/Archive is defined without reintroducing an archive directory by
  default.
- Artifact map, standards index, governance docs, and contributing guidance link
  to the lifecycle.

## Open Decision

Should the draft target be promoted to `status: canonical`, or should it remain
draft until the first project applies it and reports feedback?
