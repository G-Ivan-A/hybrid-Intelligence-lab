---
status: draft
version: 0.1
updated: 2026-09-29
temperature: 0.1
type: analysis
scope: mango-only
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/644"
based_on: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-29-cline-package-expectation-gap.md"
related_artifacts:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/645"
---

# Cline package on Windows: execution choices

## Summary

The package needs a Windows hook launcher, Cline v4 tool names, and a shell
independent runner command for sealing. PowerShell is the documented terminal
for Windows 10/11; Git Bash remains available for Git and for drive paths passed
to native Python. The package must preserve its hashed bytes during checkout.

## Context and scope

Issue [#644](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/644)
targets the copied Cline package on Windows 10/11 x64 with Git installed. The
existing [Cline gap analysis](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-29-cline-package-expectation-gap.md#в-физика-работы-python-hooks-mcp-режимы-cline)
records the initial negative cases (Г-10, Г-11, Г-15). This note records the
execution choice and its falsification tests, rather than a new product model.

## Findings and options

1. **Hooks.** Cline v4.1.21's
   [Windows discovery code](https://github.com/cline/cline/blob/787ad1b077d8b697892dc3bfcd42e7c65b88789e/apps/vscode/src/core/hooks/hook-factory.ts#L975-L997)
   looks for `<Hook>.ps1`; the [hook process](https://github.com/cline/cline/blob/787ad1b077d8b697892dc3bfcd42e7c65b88789e/apps/vscode/src/core/hooks/HookProcess.ts#L52-L67)
   launches it with PowerShell and a process scoped execution policy bypass.
   Its [tool list](https://github.com/cline/cline/blob/787ad1b077d8b697892dc3bfcd42e7c65b88789e/sdk/packages/core/src/extensions/tools/constants.ts#L12-L22)
   and [editor schema](https://github.com/cline/cline/blob/787ad1b077d8b697892dc3bfcd42e7c65b88789e/sdk/packages/core/src/extensions/tools/schemas.ts)
   explain why the old allowlist blocks routine v4 reads and edits. Keep one
   Python decision function, add three thin `.ps1` launchers, and test both
   allowed and blocked v4 calls. Rejected alternative: extensionless hooks alone,
   because the Windows discovery code ignores them. A PowerShell-only rewrite
   would duplicate the policy and increase drift.
2. **Terminal and paths.** Document PowerShell for `New-Item` and `Copy-Item`.
   Move sealing into `run_task.py` so Windows PowerShell 5.1 need not pass a
   Python program through a here-string. Accept `/c/...` and
   `/cygdrive/c/...` only when native Python runs on Windows. Rejected
   alternative: writing every instruction for Git Bash, because the existing
   guide and Windows dialogs already use PowerShell paths and commands.
   Explicit UTF-8 input and output in the launchers follows Microsoft's
   [PowerShell encoding guidance](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding?view=powershell-5.1).
3. **Package hashes.** Git's
   [attribute specification](https://git-scm.com/docs/gitattributes)
   says `-text` disables checkout line ending conversion. A package-local
   `.gitattributes` avoids changing the user's global `core.autocrlf` setting.
   The shared compiler inputs also need `build/common/.gitattributes`, since
   converted Source bytes change the generated manifest hashes. A clone with
   `core.autocrlf=true` must pass both compiler `--check` and `check-package`.

## Verification boundary

Success means the compiled package matches Source, Linux package tests pass,
and Windows CI runs the PowerShell launcher, native Python path test, and
runner tests. A failure of any of these falsifies the chosen path. Windows
Server CI tests the same shell and path mechanics but is not a live Cline
session on an analyst's Windows 10/11 workstation. The deployment guide's
protection exercise remains the workstation acceptance check. Hooks can stop
Cline actions; only the runner and CI attest the machine result.

## Related artifacts

- [PR #645](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/645) contains implementation and check results.
- [Cline v4.1.21 release](https://github.com/cline/cline/releases/tag/v4.1.21) fixes the documented tool version.
