---
status: draft
version: 0.1
updated: 2026-06-12
temperature: 0.1
---

# RFC: Universal Solution Concept Template

## Proposal

Adopt
[templates/solution-concept-template.md](../../templates/solution-concept-template.md)
as the universal L3 Solution Concept template.

## Source Adaptation

The source pattern is
[templates/webportal-solution-concept-template.md](../../templates/webportal-solution-concept-template.md).
The specialized webportal template remains valid for portals:

> Этот шаблон оптимизирован для веб-порталов, но может быть адаптирован для
> других типов проектов.

The universal template removes webportal-specific assumptions and keeps the
portable core: L2 inputs, methodology link, boundaries, architecture or operating
model, key decisions, integrations, data/knowledge model, NFRs, validation,
rollout, risks, and open solution questions.

## Lifecycle Link

Solution Concept is an L3 Methodology-layer artifact. It turns L2 product
decisions into an implementation or operating approach and links to L4 templates,
tools, prompts, and checks.

## Target Artifact

| Target | Status in this PR | Promotion condition |
| --- | --- | --- |
| `templates/solution-concept-template.md` | Draft universal template | Founder review or explicit delegated approval. |

## Acceptance Criteria

- The template is usable outside web portals.
- Webportal specialization remains in the existing webportal template.
- The L1-L4 link is visible.
- The template keeps implementation decisions out of Product Concept.
