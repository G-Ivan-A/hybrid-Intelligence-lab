---
status: draft
version: 0.1
updated: 2026-09-28
temperature: 0.1
analysis-subtype: matrix
source: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/634
scope: repo-wide
based_on: ops/backlog.md at 2026-09-28; linked issues, merged PRs, and active artifacts
related_artifacts:
  - "ops/backlog.md"
  - "docs/rfc/2026-09-28-rfc-backlog-sprint-closure.md"
---

# Evidence matrix for backlog and sprint closure (#634)

## Summary

Seven task statuses lag merged implementations and can be corrected now. The
remaining rows describe work, pending review, explicit deferral, or a decision
that the current evidence cannot make. No additional sprint meets both archive
conditions in [backlog instruction](../../ops/backlog-instruction.md). The
largest strategic risk is treating a closed planning issue or a compiled Hub
package as proof of a first independent runtime run.

## Context and scope

On 2026-09-28 the analysis covers every one of the **113 rows** (110 distinct
IDs) in [the active backlog](../../ops/backlog.md), including triggered and
Icebox rows. Status was checked against the row's source, latest issue/PR state,
merged implementation and active artifact status. A closed umbrella issue by
itself is insufficient evidence of `DONE`. The Russian `todo`/`TODO` spelling
is retained; this review does not normalize presentation.

The three duplicate IDs are distinct tasks: `B-121` (GigaCode discovery and
Icebox `L0`), `B-122` (Icebox `L1` and external tracker RFC), `B-123` (Icebox
`L2` and serverless environment delta). Their links cannot be disambiguated by
ID alone. Renumbering requires a reference migration and owner decision; this
review does not silently change traceability.

## Row-by-row disposition

Each ID below denotes one backlog row **in the named section**. All IDs from
that section are included exactly once. `DONE` means the status corrected or
already backed by merged/accepted evidence; `keep` means the current status is
preserved. A `review` row remains pending because its output is draft or lacks
an acceptance anchor. `reconcile` means keep `todo` while correcting the task
statement through an explicit decision.

| Section | IDs and disposition | Evidence and reason |
| --- | --- | --- |
| Sprint 4 | `B-056`, `B-057`, `B-058`: keep `DONE`; `B-060`: `REVIEW → DONE`; `B-059`, `B-061`, `B-062`: keep `TODO` | [PR #590](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/590) merged `projects-sink/agents-md/`. Remaining three depend on a real guide, education profile or framework demand; no closure decision exists. |
| Sprint 9 | `B-085`: keep `review`; `B-086`, `B-087`: keep `TODO` | The [retrieval research](../../research/ai-education/retrieval/00-introduction.md) remains draft; corpus validation and memory poisoning research have no accepted outputs. Closed [issue #418](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/418) is not acceptance of all three. |
| Sprint 10 | `B-089`, `B-090`, `B-098`, `B-103`, `B-104`: keep `DONE`; `B-092`, `B-093`: keep `review` | [Research on task processing](../../research/ai-education/task-processing/00-introduction.md) and the [RFC from PR #470](../rfc/2026-08-06-rfc-task-statement-architecture.md) remain draft at artifact level. Their merged PRs do not supply an accepted decision. |
| Sprint 13 | `B-110`: keep `DONE`; `B-112`: keep `CANCELLED`; `B-118`, `B-119`: `todo → DONE`; `B-111`, `B-113`–`B-117`, `B-120`, `B-154`, `B-169`: keep `todo`; `B-121` (GigaCode): keep `todo`, reconcile target | [PR #568](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/568) merged the historical path migration gate and `ops/` migration; [issue #583](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583) explicitly cancelled `B-112`. The injector, standard and target integration have no completed evidence. [Environment facts](../../research/ba-requirements/2026-09-10-gigacode-environment-facts.md) discuss `.agents/skills`, while the current GigaCode CLI package uses `.gigacode/skills`; the discovery task needs an explicit environment target. |
| Sprint 14, Icebox | `B-135`: keep `DONE`; `B-121`–`B-134` **in this section**: keep `deferred (icebox)` | [Issue #583](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583) deferred the block until empirical `M-1`…`M-5`; the first ten runtime runs have not been evidenced. These IDs do not identify the unrelated Sprint 13/triggered tasks with the same numbers. |
| Sprint 15 | `B-136`, `B-137`, `B-139`–`B-145`: keep `todo`; `B-138`: keep `todo`, rewrite on decision | Slot, validator, Golden Set and owner gates remain downstream tasks. The current [package projection taxonomy](../../projects/ba-ai-process/dist/execution-package-gigacode-cli/taxonomy/projections.yaml) includes `V-CONTRACT`, so the phrase “three projections” in `B-138` needs reconciliation before execution. |
| Sprint 16 | `B-146`, `B-147`: `todo → DONE`; `B-148`–`B-153`: keep `todo` | [PR #582](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/582) merged eleven `SKILL.md` files, route graph, run sheet and contract schemas. Validator fragments exist, but `B-149` and `B-153` ask for stronger full rules; the baseline, mode refactor and human confirmations lack completion evidence. |
| Sprint 17 | `B-155`: `review → DONE`; `B-161`: `todo → DONE`; `B-156`–`B-160`, `B-162`, `B-163`: keep `todo` | [PR #574](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/574) moved the meta-model; [PR #582](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/582) compiled the L3 slice. A Hub standard `B-156` needs measured baseline and portability evidence first. |
| Triggered/regular | `B-088`, `B-091`, `B-096`, `B-097`, `B-122` (external tracker), `B-123` (serverless), `B-068`, `B-070`: keep `deferred (triggered)`; `B-094`, `B-095`: keep `deferred (regular)` | Each row retains its named trigger or periodic cadence. `B-068` and `B-070` wait for the first `B-173` run; there is no evidence that it occurred. |
| Sprint 18 | `B-164`–`B-168`: keep `todo` | AI-PDLC alignment is a source of hypotheses, not proof of route validation or first-run cost measurement. |
| Sprint 19 | `B-170`–`B-174`, `B-069`: keep `todo`, reconcile target and ordering | [Issue #583](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583) targets `mango-ba-ai-runtime`; accepted [ADR-017](../../projects/ba-ai-process/decisions/2026-09-adr-017-ba-ai-process-source-distribution.md) now distinguishes Source, Distribution and Runtime and describes a deployed CLI runtime. Neither source establishes completion of this sprint in the named target. |
| Sprint 20 | `B-179`–`B-188`: keep `todo`; stage deployment and measurement before scaling | [PR #582](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/582) compiled a distribution package; deploy, offline run, CI gate, human gate and ten measured runs remain a separate outcome. Scaling before baseline would propagate unmeasured defects. |
| Sprint 21 | `B-189`–`B-194`: keep `todo` | The [meta-model open research](../../projects/ba-ai-process/ba-meta-model/50-open-research.md) names real gaps; execution depends on initial run evidence and selected runtime target. |
| Sprint 22 | `B-195`: keep `deferred (triggered)` | Real agent runs are the declared trigger. ADR-021 alone cannot validate the collaboration contract empirically. |
| Sprint 23 | `B-196`, `B-197`: keep `TODO` | [ADR-021 follow-up analysis](2026-09-28-adr-021-downstream-contract-gaps.md) identifies the validator and handover mismatch. Neither correction is merged yet. |

The matrix accounts for **113/113 rows**. The seven status changes have direct
merged PR anchors. `B-112` is the only cancelled row and already has the
required owner decision. No new cancellation is claimed by this analysis.

## Causal findings and options

1. A PR can close a research or compilation deliverable while the backlog row
   still asks for an accepted norm, confirmed baseline or runtime outcome. The
   alternative hypothesis “closed issue = `DONE` for every child” fails on
   `B-085`, `B-092`, `B-093`, `B-149` and `B-179`.
2. The fastest path to useful evidence is the first independent BCREQ run and
   then ten measured runs. Completing more conceptual rows first would delay
   the trigger for Icebox, operation limits and scaling decisions.
3. Whole-sprint closure requires both terminal rows and an accepted outcome.
   Sprints 4 and 10 contain small review/trigger residue, while Sprints 19 and
   20 contain strategic runtime work. They need different treatment; moving
   rows solely to make a sprint look complete would erase traceability.
4. The three duplicate IDs and the runtime name drift are separate integrity
   gaps. Options are an owner-approved renumber/migration and target
   reconciliation respectively. Until then, references must include a sprint
   qualifier and runtime work should remain open.

## Limits and next decision

This is a Hub SSOT audit. The task excludes an experiment in
`mango-ba-ai-runtime`; external deployment and run state were inferred only
from linked Hub records, so the RFC requests a target confirmation before any
runtime status change. Source links on individual backlog rows remain the
primary evidence for the unchanged items. The [RFC](../rfc/2026-09-28-rfc-backlog-sprint-closure.md)
states the proposed order and founder questions.
