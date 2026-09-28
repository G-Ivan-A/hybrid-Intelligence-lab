---
status: proposed
version: 0.1
updated: 2026-09-28
temperature: 0.1
owner: G-Ivan-A
rfc-scope: A
---

# RFC: Evidence-based closure and priority for Hub backlog sprints

## RFC Metadata

| Field | Value |
| --- | --- |
| Owner | G-Ivan-A |
| RFC status | `proposed`, awaiting founder review |
| Source issue | [#634](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/634) |
| Impacted artifacts | [`ops/backlog.md`](../../ops/backlog.md), its source issues, and downstream runtime planning |
| Decision record | This RFC after explicit owner acceptance; no ADR proposed for the present backlog order |
| Implementation link | [PR #635](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/635) for evidence-backed status corrections; subsequent PR for accepted restructuring |
| Archetype scope | A (Hub), with an interface to the BA process distribution and runtime |

## Summary

Correct seven stale statuses using merged PR evidence. Prioritize a reconciled
first independent BCREQ run and its ten-run baseline, then use measurements to
decide scale and standardization. Close small residual sprints only after their
review and outcome gates. Preserve the Icebox and triggered tasks until their
declared conditions occur. The founder decides on sprint detachment,
cancellation, duplicate IDs and the current runtime target.

## Motivation

The [113-row audit](../analysis/2026-09-28-backlog-closure-evidence-634.md)
found a mismatch between task status and merged implementation, three reused
IDs, and planning text that names `mango-ba-ai-runtime` although [accepted
ADR-017](../../projects/ba-ai-process/decisions/2026-09-adr-017-ba-ai-process-source-distribution.md)
describes Source → Distribution → Runtime with a CLI runtime. A closed umbrella
issue or a Hub distribution package does not prove an independent runtime run.
These ambiguities can direct effort to repeated theory or premature scaling
while the project's first empirical test remains open.

The newly merged [Source pilot RFC](../../projects/ba-ai-process/docs/rfc/2026-09-source-pilot-verification.md)
found a shared compiler and a local synthetic check across the GigaCode and
Cline packages, while leaving live pilot runs open. It supports verifying the
existing Source and runtime path before changing Sprint 19/20 statuses or
claiming a measured baseline.

The [Scrum Guide](https://scrumguides.org/scrum-guide.html) gives the Product
Owner responsibility for backlog order and reserves cancellation of a Scrum
Sprint for an obsolete Sprint Goal. Hub “sprints” are logical task groups under
[`ops/backlog-instruction.md`](../../ops/backlog-instruction.md), so Scrum's
timebox cancellation rule is not imported as a Hub norm. The useful external
principle is to make the owner decision and its reason visible.

## Goals and Non-goals

- Give a disposition for every active row, a full-sprint priority or a named
  critical subset for every sprint, and a dependency-led order toward the Hub
  concept of reusable, evidence-based contracts.
- Distinguish merged implementation, review, empirical validation and owner
  acceptance; keep the accepted `CANCELLED` decision for `B-112`.
- Do not infer runtime results from a Hub document or run an experiment in the
  runtime repository. Do not accept an ADR, standard, or cancellation in place
  of the founder.

## Proposal

### Status and closure rule

Apply the seven corrections in [the evidence matrix](../analysis/2026-09-28-backlog-closure-evidence-634.md):
`B-060`, `B-118`, `B-119`, `B-146`, `B-147`, `B-155`, `B-161` become `DONE`.
Preserve draft research/review rows, incomplete validators and unmeasured
runtime rows. Archive a sprint only when all its rows are `DONE` or
owner-authorized `CANCELLED` **and** the result has an accepted/rejected outcome,
as the [backlog contract](../../ops/backlog-instruction.md) requires. A moved
task needs a named trigger and traceable source; moving is not completion.

### Sprint decisions

The priority is for **whole-sprint execution** when the goal produces a coherent
outcome. “Extract” names critical rows to carry forward while the rest stays
visible. These are proposed choices, not applied status changes.

| Group | Proposed treatment | Dependency, order, and strategic risk |
| --- | --- | --- |
| Sprint 4 | Finish `B-060` status now; extract `B-059`, `B-061`, `B-062` to named demand triggers, then archive only after the owner accepts the outcome. | Root boundaries are largely settled. Keeping an old umbrella sprint open obscures new delivery; deleting the three tasks would lose legitimate guide, D-profile and framework needs. |
| Sprint 9 | Defer the whole research sprint until a real corpus/use case; keep `B-085` in review and `B-086`–`B-087` open. | Corpus validation and memory safety need actual evaluation material. Converting a draft review into a norm would overstate evidence. |
| Sprint 10 | Prioritize whole-sprint closure of `B-092` and `B-093` review, then archive on accepted/rejected outcome. | Most tasks are done; drafts cannot be treated as accepted merely because PRs merged. |
| Sprint 13 | Extract `B-169` → `B-117`/`B-120` → `B-111` as the runtime bootstrap path; keep `B-113`–`B-116`, `B-121` (GigaCode), `B-154` visible. | Contract home and environment profile must precede reliable sync. The broad sprint mixes unrelated governance work; doing it all first delays the empirical run. `B-118`/`B-119` are now done. |
| Sprint 14 | Preserve the full Icebox (`B-121`–`B-134` here), with `B-135` done; reopen after `M-1`…`M-5` from `B-183`. | [Issue #583](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583) deferred the theory; speculative standards before data are the strategic failure mode. |
| Sprint 15 | Extract `B-136`, `B-137`, `B-139` for package/run quality; reconcile `B-138` with `V-CONTRACT`; stage `B-140`–`B-145` after first-run defects and owner gates. | A compiled package is partial evidence for structure, not for every sprint criterion. The old “three projections” wording may encode an obsolete target. |
| Sprint 16 | Mark `B-146`/`B-147` done; extract `B-149` and `B-153` for complete machine gates, `B-148` for baseline; schedule `B-150`–`B-152` against owner review. | Partial validator checks should not be counted as the full rule. Missing gates let package failures reach the run. |
| Sprint 17 | Mark `B-155`/`B-161` done; extract `B-157`, `B-159`, `B-162` measurements; keep `B-156` until baseline and portability `B-158`; `B-160`, `B-163` follow evidence. | Standardizing a Mango-specific model as a Hub norm before portability would weaken the Hub's generality. |
| Triggered tasks | Keep `B-088`, `B-091`, `B-096`, `B-097`, `B-122` (tracker), `B-123` (serverless), `B-068`, `B-070` triggered; keep `B-094`, `B-095` regular. | Execute only on each recorded trigger. The duplicate IDs require sprint qualifiers until migrated. |
| Sprint 18 | Extract `B-168` boundary check and `B-164`/`B-165` route hypotheses for the first run; measure `B-166` during that run and test `B-167` against its trace. | A new orchestration layer before a failed route case would add unverified complexity. |
| Sprint 19 | Give the whole first-run sprint strategic priority **after** confirming the target and evidence already present; detach `B-069` to its V2 trigger if the founder agrees. | `B-170` → `B-171`/`B-172` → `B-173` → `B-174` yields an independently checked BCREQ run. Current runtime names disagree; silently creating a second runtime could duplicate the product path. |
| Sprint 20 | Extract `B-179`–`B-184` as the next coherent delivery and measurement slice; defer `B-185`–`B-188` until the baseline is examined. | Deploy → offline run → machine/human gates → ten runs → `M-1`…`M-5`/`MP-1`…`MP-6`. Scaling first multiplies unknown defects. |
| Sprint 21 | Keep the full correction sprint queued after first-run signals; pull `B-189`/`B-190` forward only for a demonstrated release gate gap. | `B-191`–`B-194` need actual traces, not a hypothetical integration model. |
| Sprint 22 | Preserve `B-195` triggered by real agent runs. | A paper contract cannot prove collaboration behavior. |
| Sprint 23 | Execute the whole two-task sprint (`B-196`, `B-197`) now, then close on review. | [ADR-021 gap analysis](../analysis/2026-09-28-adr-021-downstream-contract-gaps.md) gives two bounded consistency defects; closure reduces false CI and onboarding guidance. |

**Suggested order:** (1) Sprint 23 and Sprint 10 review cleanup in parallel with
target reconciliation; (2) Sprint 19 first-run path, with critical contract and
validator rows extracted from 13/15/16/18; (3) Sprint 20 `B-179`–`B-184` and
Sprint 17 measurements; (4) Sprint 21 and measured scale; (5) reopen Icebox or
generalize to a Hub standard only on evidence. This is an order of decisions
and deliverables, not a claim that every dependency is complete.

### Falsifiable hypothesis and adversarial check

**H1:** prioritizing the first independent BCREQ run, then measured scale,
closes the project's empirical gap without weakening the Hub's reusable
contracts. H1 succeeds if a selected runtime produces an isolated BCREQ run,
machine and human gate records, ten comparable runs with `M-1`…`M-5` and
`MP-1`…`MP-6`, and no unaccepted Hub standard. H1 is refuted if the first run
cannot use the distributed package without an undeclared Hub dependency, if
the target remains ambiguous, or if the metrics cannot distinguish a quality
gain from a regression.

| Test | Attack and perspective | Evidence | Verdict and route |
| --- | --- | --- | --- |
| H1.1 | Closed planning issue mistaken for a completed runtime task (operational). | [Audit](../analysis/2026-09-28-backlog-closure-evidence-634.md), [PR #582](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/582) | ✅ держит: status gate retains `B-179`–`B-184`. |
| H1.2 | First run executed in the wrong or duplicate repository (architecture). | [ADR-017](../../projects/ba-ai-process/decisions/2026-09-adr-017-ba-ai-process-source-distribution.md), [issue #583](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583) | ❌ вскрывает границу: founder must confirm runtime target before Sprint 19; track in this RFC/PR, high priority. |
| H1.3 | Three reused IDs misroute a dependency or status change (operations). | [Audit](../analysis/2026-09-28-backlog-closure-evidence-634.md) | ⚠️ держит с оговоркой: use sprint-qualified references; renumber with migration before automation consumes IDs. |
| H1.4 | Icebox rule made normative without representative runs (strategy/human governance). | [Issue #583](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583), [backlog instruction](../../ops/backlog-instruction.md) | ✅ держит: empirical trigger and owner gate remain. |
| H1.5 | Compiled validator is assumed to cover skill identity and full provenance (quality/security). | [Package validator](../../projects/ba-ai-process/dist/execution-package-gigacode-cli/tools/validate-package.py), `B-149`/`B-153` | ⚠️ держит с оговоркой: complete and test gates before claiming full sprint closure; keep rows open. |
| H1.6 | Small review sprint consumes capacity while first run slips (priority). | Sprint 10/23 and 19/20 rows in [backlog](../../ops/backlog.md) | ⚠️ держит с оговоркой: timebox the small closure work, then measure progress to first run; founder may reorder. |

Count: **2 ✅ / 3 ⚠️ / 1 ❌**. H1 is conditional on target resolution.
The high-priority `❌` is an owner question below; cautionary cases are routed
to existing backlog rows and the duplicate-ID decision here. This review does
not claim to measure runtime behavior in an external repository.

## Alternatives

| Alternative | Why it loses against the goal |
| --- | --- |
| Close every row attached to a closed issue | [The audit](../analysis/2026-09-28-backlog-closure-evidence-634.md) falsifies this for draft review, partial validators and never-run distribution. |
| Finish all conceptual sprints before first runtime run | Delays the baseline needed to test their premises and to reopen the Icebox. |
| Cancel incomplete old sprints wholesale | Removes legitimate untriggered work and conflicts with the explicit owner decision required for `CANCELLED`. |
| Treat Scrum timeboxes as authority for Hub sprint deletion | Hub uses logical groups and its own two-part archive contract; Scrum's owner-accountability insight applies, its mechanics do not. |

## Trade-offs

An explicit target decision and named triggers add a small planning
step before runtime execution. They prevent duplicated runtimes and invisible
task loss. Retaining nonterminal rows keeps the backlog longer; archival waits
for accepted outcomes. Prioritizing measurements delays broad P-04…P-10
coverage, but exposes package defects before multiplying them.

## Impacted Artifacts

- `ops/backlog.md`: seven status fixes in this PR; accepted sprint splits,
  target wording and ID migration in a subsequent scoped change.
- `docs/analysis/2026-09-28-backlog-closure-evidence-634.md`: complete audit
  and limitations.
- Existing BA direction artifacts remain in `projects/ba-ai-process/`; this RFC
  does not move their home or assert acceptance of proposed ADR-018/019.

## Implementation and Validation

1. Confirm seven changes against merged [PR #568](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/568),
   [#574](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/574),
   [#582](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/582),
   [#590](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/590).
2. Check the audit matrix covers all 113 rows including duplicate IDs;
   check that no new `CANCELLED`, archival deletion or runtime `DONE` appears.
3. Run the applicable repository validators listed in
   [CONTRIBUTING](../../CONTRIBUTING.md) before commit; record results in PR #635.
4. After founder decision, migrate IDs with reference checks, select the
   runtime target, split or archive sprints only under the backlog contract,
   and verify the actual run and metrics in their implementation PRs.

## Lifecycle and Decision Path

This complete proposal uses `status: proposed`, the review state allowed by
[RFC Structure Standard](../../standards/rfc-structure-standard.md). The
founder may accept, amend or reject it in [PR #635](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/635).
Acceptance can be recorded here because the decision concerns this backlog
order; a new ADR is needed only if it changes a reusable governance norm.
No `CANCELLED` transition or sprint archive follows automatically from this
proposal. The owner decision is applied in a separate PR with history-preserving
references and a changelog entry.

## Open Questions

1. **Runtime target (blocks Sprint 19):** should `B-170`–`B-174` and `B-179`–`B-184`
   use the CLI runtime described by ADR-017, or is `mango-ba-ai-runtime` a
   separate intended target? Recommend reconciling the existing runtime and
   package first, then changing backlog wording and dependencies together.
2. **Sprint split and cancellation:** accept the critical-path extraction and
   named triggers above, or retain the current whole-sprint groupings?
   Recommend extraction without cancellation, then archive 4/10 only after
   accepted outcomes. If an obsolete task truly needs `CANCELLED`, name the
   exact ID and rationale in the decision.
3. **Duplicate IDs:** approve a reference-preserving migration to unique IDs
   for the Sprint 13/14/triggered `B-121`–`B-123` collisions, or continue with
   sprint-qualified references? Recommend migration before machine routing,
   with an explicit old→new map and validator for unresolved references.
4. **`B-138` projection count:** retain a historical three-projection deliverable
   or rewrite for the accepted four-projection BCREQ pipeline? Recommend rewrite
   after checking its exact acceptance criteria with the BA direction owner.

## Related Artifacts

- [Backlog instruction](../../ops/backlog-instruction.md), [Hub concept](../concept.md),
  [Hub vision](../vision.md), [audit matrix](../analysis/2026-09-28-backlog-closure-evidence-634.md).
- [ADR-017](../../projects/ba-ai-process/decisions/2026-09-adr-017-ba-ai-process-source-distribution.md),
  [Source pilot RFC](../../projects/ba-ai-process/docs/rfc/2026-09-source-pilot-verification.md),
  [PR #582](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/582),
  [issue #583](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/583).
- [Scrum Guide](https://scrumguides.org/scrum-guide.html), registered as `ext-339`.
