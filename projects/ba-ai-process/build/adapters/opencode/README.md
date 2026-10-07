---
status: draft
version: 0.1
updated: 2026-10-07
temperature: 0.1
---

# OpenCode BCREQ execution package

This copyable package runs the public synthetic BCREQ Working → Release pilot
(`RG-BCREQ-v1`) in [OpenCode](https://opencode.ai/docs/). The checked-in
`golden/TASK-0001.json` demonstrates the contract; a real task starts from an
approved Working baseline and human-confirmed evidence. The machine gate
invokes the pinned validator, compiler and Release validator as three separate
processes. `runs/` contains local output and a JSONL trace.
`routes/pilot.json` declares this limited route; `templates/working-prompt.md`
and `evaluation/g-human-checklist.md` guide the agent and analyst.

## Install and pilot

Copy the **contents** of this directory to the root of a clean, private runtime
repository. Keep `.opencode/` and `.github/workflows/` when copying. Start
OpenCode in that root and follow the Russian guide cluster starting at
`docs/guides/README.md` (Windows 10/11 x64 first). The package is verified with
OpenCode 1.18.35. Python 3.11 or newer is required; the gate itself uses the
standard library. The model provider, its API key and any corporate knowledge
connection are local to the user's OpenCode installation, never part of this
package.

```powershell
python tools/run_task.py check-package
Copy-Item golden\TASK-0001.json submissions\TASK-0001.json
python tools/run_task.py run TASK-0001 submissions/TASK-0001.json
python tools/run_task.py verify-ci
```

Inside OpenCode the same steps are available as package commands:
`/bcreq-check`, `/bcreq-start TASK-ID <input>` and `/bcreq-gate TASK-ID`
(seal, then run). The second run of the same task ID is refused so an
existing trace cannot be silently overwritten. Use a new task ID for a new
attempt. Read `runs/TASK-0001/trace.jsonl`, `release.json`, and
`release-manifest.json`.

## Architecture and boundaries

| Layer | File | Role |
|-------|------|------|
| Agent rules | `AGENTS.md` | OpenCode loads it as project instructions |
| Declarative permissions | `opencode.json` | Deny every tool by default; allow reading; `edit` only `submissions/TASK-*.json` with an approval prompt; `bash`, subagents, skills and web access denied; the Plan agent cannot edit |
| Blocking plugin | `.opencode/plugins/bcreq-guard.js` → `tools/opencode_hook.py` | `tool.execute.before` sends every built-in, custom and MCP tool call to the Python policy; a deny throws and cancels the call; a missing Python blocks every tool |
| Analyst commands | `.opencode/commands/*.md` → `tools/opencode_command.py` | Run package checks and the gate when the analyst types the command; the model only explains the output |
| Independent gate | `tools/run_task.py`, `tools/bcreq_pipeline.py` | Package integrity, seal, three machine steps and the trace |
| CI | `.github/workflows/validate-opencode-package.yml` | `verify-ci` on `ubuntu-latest` and `windows-2022` |

The policy allows writes only to `submissions/TASK-[0-9]{4,}.json` (including
every target of an `apply_patch` envelope), resolves relative paths against
the directory OpenCode was started in, and checks package hashes before every
tool call. MCP tools are allowed only from a server the analyst names
`kb-readonly`, and only when the tool name has a read verb and no write verb;
MCP resources are read only from that server.

Known boundaries:

- The protections cooperate with the analyst; they do not defend against the
  analyst. `opencode --pure` (or `OPENCODE_PURE`) skips the plugin and
  `OPENCODE_DISABLE_PROJECT_CONFIG` skips both layers; `OPENCODE_PERMISSION`
  and `OPENCODE_CONFIG_CONTENT` override the rules. `/bcreq-check` reports
  these settings as a failure.
- A global user config that already defines the same permission keys can
  change the order of declarative rules; the plugin layer still decides.
- `!` shell blocks of the package commands run in the analyst's shell
  (PowerShell on Windows) when the analyst types the command; they bypass the
  model permissions by OpenCode design. The TASK ID is passed in single quotes
  and validated by `tools/opencode_command.py`.
- At start-up OpenCode installs its plugin SDK into `.opencode/`
  (`package.json`, lock files, `node_modules/`). These files are ignored by Git
  and excluded from the package hashes; the guard plugin does not import them.
- `kb-readonly` is a naming convention checked by tool-name heuristics, not a
  server-side read-only guarantee. The connection itself must be read-only.
- The hooks inspect only actions selected by OpenCode; they cannot force the
  model to request a tool call. The independent runner produces the
  authoritative process trace.

The included GitHub Actions workflow runs `verify-ci` on every PR and push. It
checks package integrity, the synthetic example and every JSON in `submissions/`.
The runtime repository administrator must make `validate-opencode-package / gate`
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
