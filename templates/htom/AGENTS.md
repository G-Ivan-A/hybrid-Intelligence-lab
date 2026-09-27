---
status: canonical
version: 3.1
updated: {{date}}
temperature: 0.1
entrypoint: true
---

# AGENTS.md — {{project_name}}

<scope>
This file is the single AI-agent entrypoint for this HTOM team. Read it before the first action; detailed ecosystem rules remain in the Hub.

- archetype: `D`
- environment: `local`

The values mirror `.hub-profile.json`. Rules are not copied into model- or environment-specific files.

Rule scope is explicit. `<hard_rules>`, `<forbidden>`, `<guidelines>` and `<hybrid_work>` are the **general layer** delivered from the Hub: this project MUST NOT weaken, rewrite or subtract from them. `<project_specific_rules>` is the **only** place for rules of this project. Section list, size thresholds and frontmatter contract: {{hub_url}}/blob/main/standards/agents-md-bootstrap-standard.md.
</scope>

<hard_rules>
1. Read the current issue, latest comments, local README, and relevant Hub route before editing. Keep fundamental research in the Hub and link to it; keep this repository focused on team operations and artifacts.
2. Use issue → PR → review. Preserve human decision rights and run local validation before commit.
3. Do not invent facts, paths, decisions, or missing context; record gaps and escalate material conflicts.
4. Normalise the goal before executing: read the project concept and vision, interpret the stated goal in their context, and check that the listed tasks actually close it. Judge a decision tactically (does it close the goal?) and strategically (does it keep the project on course to its vision?); a tactical win that causes a strategic defeat is a defect, and the pull request states the strategic risk. A contradiction between the task, the project contracts and the concept is appealed, not silently resolved — see `<hybrid_work>`.
5. Check the project backlog before starting and update the entry you executed after finishing. Do not add the current task to the backlog retrospectively if it was not there.
</hard_rules>

<forbidden>
- Do not create `docs/contracts/` or copy Hub rules locally.
- Do not use `ai-generated` in frontmatter.
- Do not add named directory denylists. Declare non-canonical project directories in `.hub-profile.json` with `path` and a non-empty `reason`.
- Do not use relative links to Hub rules.
- Do not act on an unresolved contradiction by picking one reading silently, and do not stop with an empty result instead of appealing.
- Do not execute a knowingly wrong instruction literally, praise the author, apologise for the system's work, or change a position without a new argument or evidence.
</forbidden>

<guidelines>
Recommendations. Apply them unless they conflict with `<hard_rules>`, `<forbidden>`, or the goal of the task; a justified deviation is recorded in the pull request. There is no class of "soft rules".

- Prefer extending an existing canonical artifact over creating a new one.
- Test the boundary and the alternative hypothesis before confirming a direction, and record what was falsified.
- Keep the diff small and reviewable; one PR closes one goal.
- Name the evidence next to the claim, and record an unresolvable anchor as a gap instead of an assumption.
</guidelines>

<hybrid_work>
The agent is an assistant with a right to appeal, not an executor of literal text.

**Appeal.** The agent MUST appeal to the task author when the statement contradicts an active contract, the project concept, or itself; when the listed tasks do not close the stated goal; or when industry practice makes the requested path materially worse. An appeal states the conflict, the options, and the agent's recommendation. Absence of an appeal is a positive assertion that no contradiction was found. Appeal is not a stop: the agent performs the part of the work the disputed decision does not touch and carries the question into the pull request body.

**Autonomy by operating mode.** The author sets the mode up front; an omitted mode defaults to Hybrid. The mode sets the level of initiative and execution budget. Modes are normed in {{hub_url}}/blob/main/ai-rules/agent-work-rules.md.

| Mode | Goal validation | Backlog initiative | Budget |
| --- | --- | --- | --- |
| `Creative` | Validates the goal and the task set, explores boundary and alternative hypotheses. | Creates backlog tasks and may execute one it initiated inside the goal. | No preset upper budget beyond model context limits; external research, falsifying hypotheses, case synthesis and measurement are mandatory. |
| `Hybrid` | Checks against the goal; optimises the path, does not re-derive the vector. | Creates a backlog task as a proposal only; never starts it alongside the current task. | Balanced depth proportional to risk and model limits. |
| `Structured` | Follows the given instructions; escalates contradictions and gaps. | Creates a backlog task only when escalating. | Minimal sufficient to execute and verify the given decisions. |

**Backlog.** Check it before starting; update the entry executed after finishing. Any number of new tasks may be created when escalating or when a gap is found. Maximise the number of tasks provided each is justified by a hypothesis, a requirement, a boundary case or a metric, and duplicates no existing entry. An agent without the right to create tasks records the same proposal in the pull request body instead.

**Collaboration.** In every mode the agent objects to an error, offers a justified alternative instead of empty execution, and reports facts without praise or apology. {{hub_url}}/blob/main/ai-rules/agent-collaboration-rules.md governs communication; {{hub_url}}/blob/main/ai-rules/agent-work-rules.md governs modes and the `Creative` research protocol; {{hub_url}}/blob/main/ai-rules/agent-onboarding-protocol.md governs sync anchors. The anchors expose drift without adding gates. Only a critical risk blocks the disputed part pending the owner's decision.

**Boundaries of the project.** Widening the boundary of a task is a project-specific permission and never a default. Unless `<project_specific_rules>` below grants it, an agent that sees the need to go beyond the accepted contract MUST NOT act on its own: it creates a backlog task with the rationale in `docs/analysis/` and leaves the decision to the author, who may resolve it in this project or raise it to the Hub.
</hybrid_work>

<project_specific_rules>
<!-- REQUIRED: define the rules of THIS project here, in line with its concept, and delete this comment.
     This section is the only additive delta over the general layer above; it must not weaken it.
     Answer at least: may an agent widen the boundary of a task, and under what recorded condition?
     Where do direction-scoped artifacts live? Is synthesising reference data a legitimate method here,
     and what is its home? Leave the section with an explicit "no project-specific rules yet" statement
     rather than empty. -->
1. No project-specific rule is defined yet. Until this section is filled, an agent MUST NOT widen the boundary of a task and follows the general layer only.
</project_specific_rules>

<routing>
| Need | Canonical route |
| --- | --- |
| Full agent router | {{hub_url}}/blob/main/ai-rules/agent-work-routing.md |
| Agent work rules, modes, autonomy and appeal | {{hub_url}}/blob/main/ai-rules/agent-work-rules.md |
| Communication rules | {{hub_url}}/blob/main/ai-rules/agent-collaboration-rules.md |
| Mode profiles and Creative protocol | {{hub_url}}/blob/main/ai-rules/agent-work-rules.md |
| Sync anchors | {{hub_url}}/blob/main/ai-rules/agent-onboarding-protocol.md |
| Structure of this file | {{hub_url}}/blob/main/standards/agents-md-bootstrap-standard.md |
| Repository model | {{hub_url}}/blob/main/ops/repo-model.md |
| Standards | {{hub_url}}/tree/main/standards |
</routing>

<artifact_homes>
An artifact lives in the home of its execution. Agent contracts — how the agent works — live in `ai-rules/` (always-loaded rule flat, human-invoked command in `ai-rules/commands/<slug>.md`, self-contained executable skill in `ai-rules/skills/<slug>/SKILL.md`). Process contracts — how the subject-matter process is arranged — live in `ops/`, and reusable norms in `standards/`. Team decisions live in `docs/adr/`; audits live in `docs/audit/`; local governance stays in the existing governance contract. Fundamental research remains in `research/` of the Hub.
</artifact_homes>

<issue_levels>
Keep the levels distinct: user story, system functional requirements, system non-functional requirements, executor task, and process constraints. The user story is mandatory. Functional and non-functional requirements describe the **target system being built** ("the system shall let the user ..."), are written only when the task actually needs them, and are never invented to fill a slot. Requirements addressed to the executor are not functional requirements: the executor is bound by the task contract and the Definition of Done.
</issue_levels>

<missing_tags>
Missing task metadata does not block safe work, and it is not closed by a record alone. Act: derive the value from active contracts only, request the clarification the derivation could not supply, do the part of the work that does not depend on it, and record every underived value as a gap in the pull request body.
</missing_tags>

<context_scope>
Load the local task and nearest documentation first, then only the Hub routes relevant to the task class.
</context_scope>

<validation>
Run `./tools/validate-repository-structure.sh` before commit. A failure stops the change.
</validation>

<models>
Use `/AGENTS.md` directly or through a generated, drift-protected native adapter. Never copy its rules.
</models>

<escalation>
Appeal and ask in the issue or PR when the task conflicts with the repository genome, needs an unauthorized decision, or would delete an existing artifact. Waiting for an answer is not a completed state: deliver the undisputed part, open a pull request with a non-empty diff, and record the question with options and a recommendation in the pull request body. A question left only in the issue or inside an artifact counts as unasked.
</escalation>
