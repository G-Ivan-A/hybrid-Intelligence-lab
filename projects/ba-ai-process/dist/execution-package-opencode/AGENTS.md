---
status: draft
version: 0.1
updated: 2026-10-07
temperature: 0.1
---

# BCREQ pilot in OpenCode

This workspace contains a fixed pilot of the BCREQ Working → Release route.
Read `README.md`, `docs/kb-policy.md`, `routes/pilot.json`, and the Working
schema before drafting. `templates/working-prompt.md` is the pilot prompt.
The normative package files are pinned by `package-manifest.yaml`.
Answer the analyst in Russian unless asked otherwise.

1. The analyst may bring a real BCREQ task or the public synthetic example.
   Draft one JSON document at `submissions/TASK-ID.json` following
   `contracts/c-working-bcreq.schema.json`; `TASK-0001` is the synthetic
   example and `golden/TASK-0001.json` shows the format. Agree every item with
   the analyst first. Keep exact evidence anchors; mark missing evidence as an
   open question. Never invent a Jira or Confluence quote.
2. Write only `submissions/TASK-ID.json`, and only after the analyst says to
   write the draft. Do not edit `tools/`, `contracts/`, `taxonomy/`,
   `.opencode/`, `opencode.json`, `golden/`, the manifest or CI. A change to the
   model or gate needs a new Source revision and package compilation.
3. You cannot run commands. Ask the analyst to type `/bcreq-gate TASK-ID` in
   OpenCode (it seals the draft and runs the gate), or to run
   `python tools/run_task.py seal submissions/TASK-ID.json` and then
   `python tools/run_task.py run TASK-ID submissions/TASK-ID.json` in the
   PowerShell terminal. Read the exit status and `runs/TASK-ID/trace.jsonl`; do
   not claim a gate passed from your own text.
4. `script_invoked` records an actual process, `step_skipped` blocks progress,
   and `contract_mode` records that human semantic review is still required.
   A machine PASS does not approve sources, product attribution, meaning or
   publication. The analyst decides those matters before using a Release.
5. A failed run is never repeated with the same TASK ID; a corrected draft
   gets a new TASK ID. Commit only permitted submissions. CI must pass on the
   submitted Working document before it is treated as machine verified.
