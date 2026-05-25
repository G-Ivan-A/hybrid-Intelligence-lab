# Contributing

This repository is a public knowledge hub for research, education, methodology,
and hybrid human + AI governance. Contributions should preserve traceability,
clear ownership, and separation between research artifacts, educational
materials, experiments, project knowledge bases, and future production spokes.

## Workflow

1. Start from a GitHub issue with context, scope, language, and acceptance
   criteria.
2. Use the issue template that best matches the work type: AI implementation,
   research task, or governance change.
3. Keep changes focused and reviewable; use follow-up issues for scope that is
   useful but not required for the current task.
4. Place artifacts in the directory defined by
   [docs/concept/repository-structure.md](docs/concept/repository-structure.md).
5. Update nearby README files or navigation when adding or moving public
   artifacts.
6. Run local validation before opening or updating a pull request.

## Governance References

- [AI_GOVERNANCE.md](AI_GOVERNANCE.md) defines roles, operating modes,
  Definition of Done, and escalation rules for AI-assisted work.
- [docs/governance/hybrid-team-collaboration.md](docs/governance/hybrid-team-collaboration.md)
  defines the collaboration workflow and review checklist.
- [docs/concept/repository-structure.md](docs/concept/repository-structure.md)
  defines artifact placement and the ru/en language policy.
- [docs/concept/vision-standard.md](docs/concept/vision-standard.md) defines
  the format for product vision, concept decisions, and research-facing
  publication structure.

## Local Validation

Run:

```bash
./tests/validate-repository-structure.sh
```

## Pull Requests

Pull requests should include:

- Linked issue.
- Summary of the change.
- Files or artifacts changed.
- Validation performed.
- Risks, assumptions, and follow-up tasks.
- Human review focus, especially for governance, publication, language, and
  safety decisions.

## TODO

- Replace the license placeholder after Founder & PO approves the final license.
- Add maturity status rules after the `status:` frontmatter trigger is
  confirmed.
- Add release/versioning rules if this repository later publishes packages or
  production artifacts.
