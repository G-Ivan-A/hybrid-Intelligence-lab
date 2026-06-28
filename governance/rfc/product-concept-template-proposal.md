---
status: draft
version: 0.2
updated: 2026-06-13
temperature: 0.1
owner: G-Ivan-A
rfc-scope: A
---

# RFC: Universal Product Concept Template

## Proposal

Adopt `templates/product-concept-template.md` as the future universal L2 Product
Concept template after explicit User approval.

## Source Adaptation

The source pattern is
[templates/webportal-product-concept-template.md](../../templates/webportal-product-concept-template.md).
The specialized webportal template remains valid for portals:

> Этот шаблон оптимизирован для веб-порталов, но может быть адаптирован для
> других типов проектов.

The universal template removes webportal-specific assumptions and keeps the
portable core: summary, users, jobs-to-be-done, value proposition, capabilities,
scope, flows, metrics, roadmap, risks, and open product questions.

## Lifecycle Link

Product Concept is an L2 Framework-layer artifact. It should define product
scope and value, then link to L3-L4 methodology artifacts instead of embedding
implementation rules.

## Target Artifact

| Target | Status in this PR | Promotion condition |
| --- | --- | --- |
| `templates/product-concept-template.md` | Proposed target, not created by this PR | User review plus explicit User approval. |

Merge silence means applying this PR as-is: the RFC stays in `governance/rfc/`
with `status: draft`; it does not create the target file and does not promote
the artifact to `canonical`.

## Acceptance Criteria

- The template is usable outside web portals.
- Webportal specialization remains in the existing webportal template.
- The L1-L4 link is visible.
- Approved placeholders remain limited to repository-approved placeholders.
