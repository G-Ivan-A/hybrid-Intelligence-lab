---
status: canonical
version: 1.0
updated: 2026-06-12
temperature: 0.1
---

# Agent Work Practices

Atomic practices for AI-agent work in Hub issues, PRs, and synchronized HTOM
projects.

| Practice | Source signal | Use when |
| --- | --- | --- |
| [Hybrid search before action](hybrid-search-before-action.md) | Claude Code production workflow described by Artem Chirkov | The agent must understand an existing codebase or document graph before editing. |
| [Definition of Ready check](definition-of-ready-check.md) | DoR / `VERIFICATION.txt` pattern from the same article | A task is underspecified or needs reviewable acceptance criteria. |
| [Plan-verify-ship loop](plan-verify-ship-loop.md) | Explore -> Plan -> Code -> Test -> Review -> Ship cycle | A non-trivial issue needs traceable execution. |
| [Skills as reusable workflows](skills-as-reusable-workflows.md) | Hermes Skill Hub analysis by slam | A workflow repeats across repos and should become reusable. |
| [Skill catalog token budget](skill-catalog-token-budget.md) | 91,000+ skill overload case | A catalog grows large enough to hurt agent context quality. |
