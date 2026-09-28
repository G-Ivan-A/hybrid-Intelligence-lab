---
status: draft
version: 0.1
updated: 2026-09-28
temperature: 0.1
analysis-subtype: recommendation
source: https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/631
scope: slice
based_on: ADR-021, tools/check-agent-work-rules-size.sh, templates/htom/AI_SESSION_HANDOVER_PROMPT.md
---

# Downstream contract gaps after ADR-021

## Summary

The contract audit for issue #631 found two downstream implementation gaps.
They need separate tasks because the issue limits modernization to `AGENTS.md`
and `ai-rules/`, apart from the authorized ADR correction and its navigation and
test updates.

## Context and scope

On 2026-09-28, the audit compared [ADR-021](../adr/2026-09-adr-021-agent-collaboration-layer.md),
the active agent rules, the size validator and the HTOM handover prompt. The
Hub's `AGENTS.md` already matches the general sections of both bootstrap
templates. No change to those shared sections is proposed here.

## Findings and options

| Gap | Evidence | Consequence | Options |
| --- | --- | --- | --- |
| The 9K limit is enforced as an error although ADR-021 now calls it a recommendation. | [`tools/check-agent-work-rules-size.sh`](../../tools/check-agent-work-rules-size.sh) sets `ERROR_TOKENS=9000` and exits 1 above the limit; [`tools/test-check-agent-work-rules-size.sh`](../../tools/test-check-agent-work-rules-size.sh) expects that failure. | A future contract addition above 9K would fail CI even when the norm remains necessary. The current file is below the threshold, so issue #631 is not blocked. | Change the validator and regression test to warn and recommend decomposition; or retain a hard limit only after a new human decision that supersedes the ADR guidance. |
| The HTOM handover prompt still names `structured` as the implicit mode. | [`templates/htom/AI_SESSION_HANDOVER_PROMPT.md`](../../templates/htom/AI_SESSION_HANDOVER_PROMPT.md) says `по умолчанию — structured`, while [Agent Work Rules](../../ai-rules/agent-work-rules.md#operating-modes) defines `Hybrid` as the default. | A newly bootstrapped team can receive a different mode from an agent reading the Hub onboarding protocol. | Synchronize the generated prompt and its tests with the accepted mode contract; or make an explicit HTOM-specific override with a decision record. |

## Recommendations

Track the size-validator change as B-196 and the handover-template change as
B-197 in [the backlog](../../ops/backlog.md). Execute neither within issue
#631. Keep the current ADR wording visible in the PR so reviewers can assess
the temporary mismatch.

## Related artifacts

- [Issue #631](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/631)
- [PR #626](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/626)
- [Analysis Standard](../../standards/analysis-standard.md)
