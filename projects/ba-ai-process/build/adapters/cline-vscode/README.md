---
status: draft
version: 0.1
updated: 2026-09-26
temperature: 0.1
---

# Cline BCREQ execution package

This copyable package runs a public synthetic BCREQ Working → Release pilot.
The checked-in `golden/TASK-0001.json` demonstrates the contract; a real task
starts from an approved Working baseline and human-confirmed evidence. The
machine gate invokes the pinned validator, compiler and Release validator as
three separate processes. `runs/` contains local output and a JSONL trace.
`routes/pilot.json` declares this limited route; `templates/working-prompt.md`
and `evaluation/g-human-checklist.md` guide the agent and analyst.

## Install and pilot

Copy the **contents** of this directory to the root of a clean, private runtime
repository. Keep `.clinerules/` and `.github/workflows/` when copying. Open that
root in VS Code and follow `docs/guides/01-junior-pilot.md`.
Python 3.11 or newer is required; the gate itself uses the standard library.
The model API settings and any corporate knowledge connection are local to the
user's Cline installation, never part of this package.

```sh
python3 tools/run_task.py check-package
cp golden/TASK-0001.json submissions/TASK-0001.json
python3 tools/run_task.py run TASK-0001 submissions/TASK-0001.json
python3 tools/run_task.py verify-ci
```

The second run of the same task ID is refused so an existing trace cannot be
silently overwritten. Use a new task ID for a new attempt. Read
`runs/TASK-0001/trace.jsonl`, `release.json`, and `release-manifest.json`.

## Gate boundary

Workspace `TaskStart`, `TaskResume` and `PreToolUse` hooks check package hashes.
The tool hook allows Cline to write only `submissions/TASK-ID.json`, and blocks
Cline shell commands and unrecognized tools. Enable hooks in Cline Feature
Settings and verify the hook smoke test in the guide. These hooks inspect only
actions selected by Cline; they cannot force the model to request a tool call.
The independent runner produces the authoritative process trace.

The included GitHub Actions workflow runs `verify-ci` on every PR and push. It
checks package integrity, the synthetic example and every JSON in `submissions/`.
The runtime repository administrator must make `validate-cline-package / gate`
a required branch check to prevent merging around this gate. Corporate or
private inputs belong in a private runtime and must not be copied into a public
PR. `G-human` source, semantic and publication review remains a separate human
decision.

## Package manifest

`package-manifest.yaml` is JSON syntax valid as YAML 1.2. It records the Source
revision, adapter, input allowlist and SHA-256 of each immutable output. The
runner rejects extra or changed immutable files. `docs/kb/`, `meta-model/`,
`submissions/` and `runs/` are explicit runtime inputs/state and are excluded
from those output hashes. They do not override the pinned gate or schemas.

The package does not read the Source repository at runtime. Changes to the
model, scripts, rules or guide are made in Source and compiled again.
