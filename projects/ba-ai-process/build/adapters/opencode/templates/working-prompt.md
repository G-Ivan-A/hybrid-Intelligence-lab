---
status: draft
version: 0.2
updated: 2026-10-07
temperature: 0.1
---

# Prompt for a Working draft

Read `AGENTS.md`, `routes/pilot.json`, `contracts/c-working-bcreq.schema.json`
and `golden/TASK-0001.json`. The task is either a real BCREQ task brought by
the analyst or the public synthetic example `TASK-0001`. Explain the goal,
source anchor, system boundary, product binding and FR/UC/NFR trace, and agree
every item with the analyst. Search the read-only `kb-readonly` connection
first when it exists, then `docs/kb/` under `docs/kb-policy.md`. If asked to
produce a Working draft, write only `submissions/TASK-ID.json`. Mark missing
evidence as an open question; never invent a source, decision or approval.
Ask the BA to confirm the product binding, source rights and semantic review.
Ask the BA to run `/bcreq-gate TASK-ID` and quote its actual exit code.
