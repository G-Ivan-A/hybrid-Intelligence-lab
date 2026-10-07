---
status: draft
version: 0.3
updated: 2026-10-07
temperature: 0.1
---

Read `AGENTS.md` in this workspace before starting. Draft a BCREQ Working JSON only in
`submissions/TASK-ID.json`. The analyst uses `python tools/run_task.py seal submissions/TASK-ID.json`, then `python tools/run_task.py run TASK-ID submissions/TASK-ID.json` in the VS Code Git Bash terminal on Windows and reads the trace. Give the analyst commands in Git Bash syntax: `/` separators, `cp`, `mv`, `mkdir -p`, quoted `"$HOME/..."` paths. Do not report a machine
PASS from your own text. Corporate evidence requires an approved read-only connection
and an exact source anchor; follow `docs/kb-policy.md` when it is unavailable.
