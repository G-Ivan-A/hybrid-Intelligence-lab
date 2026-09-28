---
status: draft
version: 0.1
updated: 2026-09-28
temperature: 0.1
type: external-analysis
source_id: ext-336
stage: research
projects: [hub]
context: [backlog-order, sprint-cancellation, product-ownership]
---

# Insight: make backlog order and cancellation an owner decision

**Source:** `ext-336`, [Scrum Guide 2020](https://scrumguides.org/scrum-guide.html).

## Atomic conclusion

Scrum makes the Product Owner accountable for ordering Product Backlog items;
the Product Owner may cancel a Sprint when its Sprint Goal becomes obsolete.
This supports a visible owner decision and rationale for changing priorities or
canceling work in the Hub.

## Relevance and limit

The Hub backlog uses *logical groups* rather than Scrum timeboxed Sprints.
Its [instruction](../../../ops/backlog-instruction.md) has a specific archive
gate and requires an explicit human decision for `CANCELLED`. Therefore the
external guide is comparative evidence for decision ownership, not a source
for importing Scrum cancellation mechanics. This distinction is used in
[RFC #634](../../../docs/rfc/2026-09-28-rfc-backlog-sprint-closure.md).

## Arguments and counterexample

| Support | Limit |
| --- | --- |
| Explicit accountability prevents agent-inferred cancellation. | Closing a logical Hub group because a Scrum timebox ended would erase unresolved work and violate the Hub contract. |

## Path to practice

The RFC asks the owner to select the priority and exact cancellation/split
decisions. No new standard follows from this source. Reconsider a reusable
practice only after repeated Hub backlog decisions reveal a missing rule.

## Stage

`research`: compared with the Hub contract and bounded to the decision-right
insight; no runtime outcome is claimed.
