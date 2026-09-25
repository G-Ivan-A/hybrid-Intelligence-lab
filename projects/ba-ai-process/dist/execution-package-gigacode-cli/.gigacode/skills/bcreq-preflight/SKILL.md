---
name: bcreq-preflight
description: Build and review typed registers before FR, UC, or NFR generation.
packs: P-03/SK-bcreq-preflight
interaction: human-checkpointed
inputs: [A-CORE, A-IN]
outputs: [preflight_registers]
contracts: [C-WORKING-BCREQ]
gates: [G-self, G-mach, G-semantic, G-human]
compiled_from: { package: execution-package-gigacode-cli, route: RG-BCREQ-v1 }
derived_from: [https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-abstraction-and-product-routing.md, https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-working-release-pipeline.md]
compiled_at: 2026-09-24
status: draft
version: 1.0
updated: 2026-09-24
temperature: 0.1
---

# BCREQ preflight

## Когда применять

Run at `n10a`, before any FR, UC, or NFR is written. This is a checkpoint for
the registers in the approved Working contract.

## Предусловия

`A-IN`, `A-CORE`, the confirmed product chain, and the approved routing decision
are available. Every source can be inspected or is recorded as a gap.

## Шаги

1. Create evidence entries with retrieval status, exact anchor, excerpt, and
   checksum. An unread source cannot support an accepted claim.
2. Record goals, tasks, the target system boundary, in-scope and out-of-scope
   items, and the as-is to requested-delta matrix.
3. Bind each candidate to a complete MANGO taxonomy path and its source.
4. Classify every claim as accepted, rejected, hypothesis, or open. Record
   source, goal, task, delta, boundary, product binding, level, target slot,
   and a relevance reason. Retain rejected claims as evidence of the decision.
5. Have `G-semantic` review source entailment, goal relevance, and as-is versus
   delta with rationale and counterexamples. Present disputed decisions to
   `G-human`. Only approved registers allow `n11`.

## Обязательные слоты выхода

`evidence`, `goals`, `tasks`, `boundary`, `deltas`, `product_bindings`, and
`claims` are all present and nonempty in the Working model.

## Самопроверка (G-self)

- Every accepted claim has a read source and exact anchor.
- Every accepted claim links to a goal, task, requested delta, boundary, and
  complete product binding.
- Current state and proposed change have distinct dispositions.
- FR, UC, and NFR generation has not started.

## Отказ

Stop on an unread source, unexplained empty register, unknown product path,
unresolved goal relevance, or missing human decision. Preserve the gap and
question rather than filling a plausible value.
