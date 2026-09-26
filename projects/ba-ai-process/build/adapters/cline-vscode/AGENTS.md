---
status: draft
version: 0.1
updated: 2026-09-26
temperature: 0.1
---

# BCREQ pilot in Cline

This workspace contains a fixed pilot of the BCREQ Working → Release route.
Read `README.md`, `docs/kb-policy.md`, `routes/pilot.json`, and the Working
schema before drafting. `templates/working-prompt.md` is the pilot prompt.
The normative package files are pinned by `package-manifest.yaml`.

1. Use a public synthetic input for the pilot. Draft one JSON document at
   `submissions/TASK-0001.json` following `contracts/c-working-bcreq.schema.json`.
   The example is `golden/TASK-0001.json`. Keep exact evidence anchors; mark
   missing evidence as a gap. Never invent a Jira or Confluence quote.
2. Do not edit `tools/`, `contracts/`, `taxonomy/`, `.clinerules/`, `golden/`,
   the manifest or CI during a task. A change to the model or gate needs a
   new Source revision and package compilation.
3. Ask the analyst to run `python3 tools/run_task.py run TASK-0001 submissions/TASK-0001.json` in the VS Code terminal. Read the exit status
   and `runs/TASK-0001/trace.jsonl`; do not claim a gate passed from your text.
4. `script_invoked` records an actual process, `step_skipped` blocks progress,
   and `contract_mode` records that human semantic review is still required.
   A machine PASS does not approve sources, product attribution, meaning or
   publication. The analyst decides those matters before using a Release.
5. Commit only permitted synthetic submissions. CI must pass on the submitted
   Working document before it is treated as machine verified.
