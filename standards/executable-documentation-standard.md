---
status: canonical
version: 1.0
updated: 2026-06-12
temperature: 0.1
---

# Executable Documentation Standard

This standard separates documents that describe knowledge from documents that an
agent or human must execute. It extends
[executable-contract-standard.md](executable-contract-standard.md) from contracts
to reusable documentation, prompts, and practice nodes.

## Descriptive documents

Descriptive documents explain context, rationale, research, or decisions. They
are read before action, but the whole file is not an instruction to perform.

Examples:

- research reports in `research/`;
- product documents in `docs/`;
- RFCs before a human decision;
- artifact maps, indexes, and historical rationale.

Descriptive documents should answer: what is known, what was compared, which
sources support the conclusion, and what remains open.

## Executable documents

Executable documents are action surfaces. When an agent receives one, it should
apply the steps, not only summarize them.

Examples:

- copyable prompts such as `templates/sync-project-with-hub-prompt.md`;
- onboarding prompts and runbooks;
- validation scripts described by a wrapper document;
- fixed practice nodes under `practices/`.

Executable documents should contain:

1. Trigger: when to use it.
2. Inputs: what context is required.
3. Steps: ordered, testable actions.
4. Outputs: expected artifacts or decisions.
5. Stop conditions: when to ask a human.

## Atomization

Executable knowledge should be atomic enough that a reviewer can import,
reject, or adapt one practice without taking an entire research report.

| Unit | Allowed in | Rule |
| --- | --- | --- |
| Research report | `research/` | Can compare many sources and alternatives. |
| Practice matrix | `research/` or `practices/README.md` | Maps sources to fixed practice nodes. |
| Practice node | `practices/<domain>/<practice>.md` | One reusable behavior, with source, author or organization, link, Hub applicability, and implementation steps. |
| Prompt template | `templates/` | Copyable execution surface, with approved placeholders. |

## Practice graph

Practice nodes form a lightweight graph through body links, not frontmatter
overload:

```text
source research -> practice index -> atomic practice -> template/check/script
```

For international AI governance, the research owner is
[international-ai-governance-practices-2026-06.md](../research/hub/international-ai-governance-practices-2026-06.md).
Its fixed practice nodes live under `practices/ai-governance/`.

For external agent-work practices, the research owner is
[external-practice-intake-2026-06.md](../research/hub/external-practice-intake-2026-06.md).
Its fixed practice nodes live under `practices/agent-work/`.

## Import Rule

Research can recommend a practice. Only a practice node fixes it as reusable Hub
knowledge. A project imports the node through a sync prompt, issue, or PR and may
adapt it when local constraints are documented.
