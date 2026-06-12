---
status: canonical
version: 0.1
updated: 2026-06-12
temperature: 0.1
executable: true
---

# Sync Project With Hub Prompt

Copy this prompt into a new AI session when a project needs to compare its local
structure and practices with the Hub.

```text
You are helping synchronize {{project_name}} with the Hybrid Intelligence Lab
Hub: {{hub_url}}

Operating mode: Structured unless the task explicitly asks for Creative mode.

Goal:
Compare local project practices with Hub practices, standards, templates, and
governance recommendations. Propose only imports that fit this project.

Inputs to read first:
1. Local README, CONTRIBUTING, AI_GOVERNANCE, task templates, docs index, and
   available validators.
2. Hub entry points: README.md, governance/artifact-map.md,
   governance/repo-model.md, standards/README.md, practices/README.md,
   templates/manifest.json.
3. Project-specific constraints, product type, audience, and current lifecycle.

Execution:
1. Identify the project type: HTOM team, spoke repository, or another local
   category. If uncertain, stop and ask.
2. Build a comparison table:
   - local artifact or practice;
   - matching Hub artifact or practice;
   - difference;
   - impact;
   - recommended action.
3. For every candidate import, classify it:
   - import now;
   - adapt locally;
   - defer;
   - reject with reason.
4. Check Hub practice nodes before proposing new local rules:
   - practices/agent-work/;
   - practices/ai-governance/.
5. Check whether a Hub template already exists before creating a new local
   template.
6. Do not overwrite project-specific decisions. Preserve local domain knowledge,
   product constraints, accepted ADRs, and existing public contracts unless a
   human explicitly approves a change.
7. If the project has a messy docs tree, apply the HTOM documentation structure
   standard as a recommendation, not an automatic migration.
8. Produce a sync report with:
   - summary;
   - proposed imports;
   - local adaptations;
   - rejected or deferred Hub recommendations;
   - risks and required human decisions;
   - validation commands to run after changes.

Stop conditions:
- Missing repository access or missing local governance files.
- A proposed change would delete or overwrite local decisions.
- A legal, privacy, security, or regulated AI risk tier is plausible.
- The Hub recommendation conflicts with the project's explicit product context.

Done when:
- The project owner can approve, reject, or split each proposed import.
- No Hub practice is copied blindly.
- Every difference has a rationale.
```

Related Hub artifacts:

- [practices/README.md](../practices/README.md)
- [standards/htom-documentation-structure.md](../standards/htom-documentation-structure.md)
- [standards/executable-documentation-standard.md](../standards/executable-documentation-standard.md)
