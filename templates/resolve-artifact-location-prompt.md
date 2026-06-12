---
status: draft
version: 0.1
updated: 2026-06-12
temperature: 0.1
executable: true
---

# Resolve Artifact Location Prompt

Copy this prompt into a new AI session when a contributor is unsure where a new
Hub artifact belongs.

Status note: this is the target draft for
[resolve-artifact-location-proposal.md](../governance/rfc/resolve-artifact-location-proposal.md).
It can become canonical only after founder review.

```text
You are resolving where a new artifact belongs in the Hybrid Intelligence Lab
Hub: {{hub_url}}

Operating mode:
- Structured by default.
- Creative only when the task explicitly asks for synthesis or missing-context
  creation.

Goal:
Choose the smallest correct repository location for the artifact, record any
lifecycle gap, and avoid creating unnecessary documents.

Read first:
1. governance/artifact-map.md
2. governance/repo-model.md
3. standards/knowledge-lifecycle.md
4. standards/htom-documentation-structure.md
5. standards/frontmatter-docs-standard.md
6. standards/file-naming.md

Decision tree:
1. Is it raw signal, notes, source-backed comparison, or analysis?
   -> research/<domain>/
2. Is it a governance or structure proposal awaiting human decision?
   -> governance/rfc/
3. Is it a reusable behavior extracted from research or repeated project pain?
   -> practices/<domain>/
4. Is it a mandatory format, policy, lifecycle, or quality rule?
   -> standards/
5. Is it a copyable form, executable prompt, or reusable start surface?
   -> templates/
6. Is it a methodology package for a class of projects?
   -> frameworks/
7. Is it product-level Hub framing, ecosystem framing, Vision, or Concept?
   -> docs/
8. Is it local project context rather than Hub-wide knowledge?
   -> projects/<project-slug>/ or the external spoke repository.

Lifecycle check:
- Identify current stage:
  Observation, Research, Hypothesis, RFC, Pattern, Standard, Template,
  Framework, or Deprecation/Archive.
- Identify requested target stage.
- If a prior stage is missing, classify the gap as soft or hard.

Two-factor confirmation:
- Hard violations require explicit human approval before changing files:
  top-level folder changes, file deletion, Anti-Inflation bypass,
  fail-closed bypass, security/privacy/legal/publication risk.
- Soft violations are logged in the PR while the task proceeds:
  skipped lifecycle step in Structured mode, minor frontmatter mismatch,
  use of a draft artifact as draft context.

Silence rule:
Silence means agreement with the current state only. It never promotes an
artifact to the next lifecycle stage. Promotion needs an explicit human decision
or a clear founder instruction to skip a named stage.

Creative mode:
- If a needed prior artifact is missing, create the smallest reviewable missing
  proposal or draft candidate.
- If blocked, create only the safe part and document the dependency in the PR.
- The founder can approve the transition or explicitly write "skip stage X".

Output:
1. Recommended path.
2. Artifact type and lifecycle stage.
3. Required frontmatter fields.
4. Links to nearest standards/templates.
5. Hard approvals required, if any.
6. Soft violations to log in the PR, if any.
7. Validation commands to run.

Done when:
- The chosen path is consistent with artifact-map, repo-model, and lifecycle.
- Anti-Inflation is addressed explicitly.
- The reviewer can approve, reject, or split the placement decision.
```

Related Hub artifacts:

- [Knowledge Lifecycle](../standards/knowledge-lifecycle.md)
- [Artifact Map](../governance/artifact-map.md)
- [Repository Model](../governance/repo-model.md)
- [HTOM Documentation Structure](../standards/htom-documentation-structure.md)
