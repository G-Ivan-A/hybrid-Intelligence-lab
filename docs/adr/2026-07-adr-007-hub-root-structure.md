---
status: proposed
version: 0.1
updated: 2026-07-04
temperature: 0.1
owner: G-Ivan-A
decision-type: methodology
---

# ADR-007: Целевая структура корня Хаба

## Decision Metadata

| Field | Value |
| --- | --- |
| ADR | ADR-007 |
| Backlog item | B-047 |
| Decision type | methodology |
| Status | proposed |
| Decision date | 2026-07-04 |
| Owner | G-Ivan-A |
| Source issue | [#378](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/378) |
| Primary input | [B-034 migration and root structure plan](../analysis/2026-07-04-hub-migration-and-root-structure-plan.md) |
| Upstream decisions | [ADR-001](2026-06-adr-001-ecosystem-infrastructure-methodology.md), [ADR-002](2026-06-adr-002-artifact-document-methodology.md) |
| Impacted artifacts | `governance/backlog.md`, `governance/artifact-map.md`, `governance/repo-model.md`, `tools/validate-repository-structure.sh`, future B-048 migration PR |
| Supersedes | none |
| Superseded by | none |

## Context

B-034 produced an upstream analysis/plan for the current Hub root structure after
Research, Analysis and Audit standardization. That analysis intentionally left
several root-level targets as ambiguous because they needed founder decision.

Issue #378 closes those ambiguities. The decision is already made by the
founder, so this ADR records the accepted target and downstream consequences
instead of proposing an RFC with alternatives. This ADR does not physically move
files, rewrite links or cancel current entry points. Physical migration remains
the scope of B-048 after this ADR is accepted.

ADR-001 and ADR-002 remain the source of truth for ecosystem infrastructure and
artifact routing. The Research/Analysis/Audit standards are not a source of root
repository structure. The Hub remains Archetype A; Hub != Portal.

## Decision

Adopt the following To-Be root decisions for the Hub repository.

| Target | Decision |
| --- | --- |
| `projects-sink/` | Create a Hub-specific flat management intake buffer for incoming material from ecosystem projects. Move `AI_PROJECT_CONTEXT-Summary.md` there during physical migration. |
| `ai-governance/` | Use for policies: state constraints, business rules, information security, external compliance and other policy-level obligations. |
| `ai-rules/` | Use for agent behavior rules and fast synchronization of an external agent with project context. |
| `practices/` | Keep at the repository root as a Hub-specific divergence from ADR-001 `docs/practice/`. |
| `docs/guides/` | Use as the unified home for guides. A missing backlog task for guide migration is not a blocker; it can be added or renumbered after migration. |
| `education/` | Use for cross-project education materials. A follow-up standard for archetype D can be added or renumbered after migration. |
| `frameworks/` | Reserve as the future home for frameworks after the research -> standard path confirms framework scope. |
| `docs/concept.md` | Use as the target for current root `CONCEPT.md`. |

Delete or retire the following root artifacts during physical migration:

| Current artifact | Decision |
| --- | --- |
| `website/` | Retire because the Hub web strategy is cancelled. The Hub must not be turned into Portal. |
| `mkdocs.yml` | Retire as a consequence of cancelling the Hub website strategy. |
| `experiments/` | Retire as a root directory. Validator tests move to `tools/`; no other experiment corpus remains there. |

Split the current `governance/` area as follows:

| Current area | To-Be route |
| --- | --- |
| policy, compliance and external constraints | `ai-governance/` |
| PR/task/review operations | `pr-ops/` |
| RFC documents | `docs/rfc/` |
| `governance/rfc/` | `docs/rfc/` |

Use lifecycle status as the provisional-standard mechanism:

- `draft` and `proposed` status mark provisional standards.
- Do not create `standards/provisional/` now.
- Create `standards/provisional/` only if review pain proves that lifecycle
  status is insufficient.

Adopt the following implementation strategy for B-048:

1. Phase 0: accept this ADR as B-047 decision gate.
2. Phase 1: introduce neutral target anchors without changing semantics.
3. Phase 2: move `governance/rfc/` to `docs/rfc/` with link rewrites.
4. Phase 3: split `governance/` into `ai-governance/`, `ai-rules/`, `pr-ops/`
   and `docs/rfc/`.
5. Phase 4: reconcile all previously ambiguous entities as one task/PR, not as
   one PR per catalog. The executor runs validators and cross-reference
   stress-tests inside the PR before review.
6. Phase 5: synchronize validators, artifact-map, repo-model, manifest and
   navigation in the same PR as the structural changes.
7. Phase 6: stabilize aliases and remove transitional compatibility only after
   links and registries are proven stable.

Link rewrite strategy:

- Rewrite links in the same PR as the physical move.
- Keep aliases or compatibility notes until cross-references stabilize.
- Use named anchors, not section numbers.
- Update artifact-map, repo-model, validators and other synchronous registries
  in the same PR as path changes.

## Decision Drivers

- B-034 identified the root-structure source of truth as ADR-001 plus ADR-002,
  not Research/Analysis/Audit standards.
- The founder decision already exists; an RFC would reopen a closed decision and
  add review overhead.
- The Hub must remain an ecosystem infrastructure Hub and must not drift into a
  Web Portal profile.
- `ai-governance/` and `ai-rules/` need a stable semantic boundary before file
  moves, otherwise policy/compliance material and agent behavior rules will
  collapse back into one bucket.
- Provisional standards need a low-inflation mechanism; lifecycle status is
  enough until proven otherwise.
- B-048 needs a single implementation strategy that combines moves, link
  rewrites, aliases and registry synchronization.

## Alternatives Considered

This ADR intentionally does not propose alternatives or trade-offs. B-034
recorded the open options and issue #378 records the founder decision that closes
them. No alternative is under review in this ADR.

## Consequences

| Backlog item | Consequence |
| --- | --- |
| B-048 | Becomes the physical migration task after ADR-007/B-047 is accepted. It implements this target structure and performs the integrity stress-test before review. |
| B-054 | Remains deferred until after migration and standard-desync repair; the B-048 stress-test is execution evidence, not the future process standard itself. |
| B-055 | Is absorbed by ADR-007/B-047 for the `ai-governance/` vs `ai-rules/` boundary. A separate post-migration ADR is not needed unless this ADR is rejected or superseded. |
| B-056 | Uses this ADR as the policy/rule split source when physically separating current governance material. |
| B-057 | Reserved logical follow-up for `docs/guides/` routing if migration work needs a separate backlog item. |
| B-058 | Reserved logical follow-up for `education/` and archetype D education standardization. |
| B-059 | Reserved logical follow-up for `frameworks/` research -> standard confirmation. |
| B-060 | Reserved logical follow-up for `CONCEPT.md` -> `docs/concept.md`. |
| B-061 | Reserved logical follow-up for `AI_PROJECT_CONTEXT-Summary.md` -> `projects-sink/`. |
| B-062 | Reserved logical follow-up for retiring `website/`, `mkdocs.yml` and root `experiments/`. |

B-057..B-062 are named here as consequence slots, not as created backlog rows.
If current backlog numbering differs at migration time, they may be created or
renumbered without blocking B-048.

Current repository paths remain active until B-048 performs the physical
migration. This ADR changes decision state and registries only.

## Impacted Artifacts

| As-Is | To-Be | Impact |
| --- | --- | --- |
| `governance/backlog.md` | future `pr-ops/` backlog area | Current backlog is updated to make B-047 a review-stage ADR and B-048 the physical migration task. |
| `governance/artifact-map.md` | future registry location governed by B-048 | Current artifact-map registers this ADR and remains the active map until migration. |
| `governance/repo-model.md` | future synchronized repo model | B-048 updates it with accepted target paths. |
| `governance/rfc/` | `docs/rfc/` | RFC path migration happens in B-048. |
| `AI_GOVERNANCE.md` and policy material | `ai-governance/` | Policy/compliance material moves according to the boundary in this ADR. |
| agent behavior and sync material | `ai-rules/` | Agent behavior rules and quick-sync context move according to the boundary in this ADR. |
| `practices/` | `practices/` | Root location remains accepted for Hub-specific practices. |
| guide material | `docs/guides/` | Unified guide home is accepted; backlog task may be added later. |
| education material | `education/` | Cross-project education home is accepted; archetype D standardization remains follow-up. |
| framework material | `frameworks/` | Future framework home is accepted after research -> standard confirmation. |
| `CONCEPT.md` | `docs/concept.md` | Physical move remains B-048 or downstream consequence task. |
| `AI_PROJECT_CONTEXT-Summary.md` | `projects-sink/` | Physical move remains B-048 or downstream consequence task. |
| `website/` | removed | Hub web strategy is cancelled. |
| `mkdocs.yml` | removed | Removed as website cancellation consequence. |
| `experiments/` | removed; validator tests in `tools/` | Root experiments directory is retired. |
| provisional standards | lifecycle status `draft` or `proposed` | `standards/provisional/` is not created unless review pain appears. |

## Compliance and Validation

This ADR complies with `standards/adr-structure-standard.md` by using ADR
frontmatter, required sections, decision metadata, lifecycle and related
artifacts. The `Alternatives Considered` section is intentionally closed because
the founder decision has already been made.

This PR validates the decision record and registry synchronization with:

- `./tools/validate-frontmatter.sh .`
- `./tools/validate-file-naming.sh`
- `./tools/validate-repository-structure.sh`

B-048 must additionally validate moved links, aliases, artifact-map,
repo-model, validators, manifest and navigation in the same PR as the physical
migration.

## Lifecycle

This ADR is `proposed` while PR #379 is under review. If accepted, B-047 becomes
complete and B-048 becomes the next physical migration task. If rejected, B-047
must be reopened as a proposal gate and backlog changes that depend on ADR-007
must be revised. Future ADRs may supersede this decision only by naming the
scope they replace.

## Related Artifacts

- [Issue #378](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/378)
- [B-034 migration and root structure plan](../analysis/2026-07-04-hub-migration-and-root-structure-plan.md)
- [ADR-001: Ecosystem infrastructure methodology](2026-06-adr-001-ecosystem-infrastructure-methodology.md)
- [ADR-002: Artifact/document methodology](2026-06-adr-002-artifact-document-methodology.md)
- [ADR-003: Research structure](2026-07-adr-003-research-structure.md)
- [ADR-004: Reports structure](2026-07-adr-004-reports-structure.md)
- [ADR-005: Audit structure](2026-07-adr-005-audit-structure.md)
- [ADR-006: Analysis structure](2026-07-adr-006-analysis-structure.md)
- [ADR structure standard](../../standards/adr-structure-standard.md)
- [Backlog](../../governance/backlog.md)
- [Artifact map](../../governance/artifact-map.md)
