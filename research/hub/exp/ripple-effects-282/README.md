---
status: draft
version: 0.1
updated: 2026-06-28
temperature: 0.1
type: experiment
context: [hub, issue-282, frontmatter, lifecycle, migration]
method: repository-frontmatter-scan
scope: evidence
---

# Experiment: Ripple effects 282 frontmatter scan

This experiment supports
[2026-06-28-ripple-effects-282-research.md](../../2026-06-28-ripple-effects-282-research.md)
for issue [#284](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/284).
It scans the current repository checkout and captures concrete evidence for
frontmatter migration questions raised by issue
[#282](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/282).

## Inputs

| Input | Purpose |
| --- | --- |
| Current repository checkout | Count Markdown frontmatter fields and status usage |
| `standards/frontmatter-standard.md` | Current base contract |
| `tools/validate-frontmatter.sh` | Current validator behavior |

## Command

```bash
python3 research/hub/exp/ripple-effects-282/scan-frontmatter.py
```

## Outputs

| Output | Purpose |
| --- | --- |
| [frontmatter-scan.json](frontmatter-scan.json) | Machine-readable counts and examples |
| [2026-06-28-frontmatter-scan.md](2026-06-28-frontmatter-scan.md) | Human-readable summary |

## Method notes

The scan is intentionally syntactic. It reads only the first YAML-like
frontmatter block of tracked Markdown files and reports field names, status
values, path classes and representative examples. It excludes this issue #284
research artifact and its experiment directory so the generated counts stay
reproducible after the PR is committed. It does not decide which fields are
valid, because issue #284 is a decision-support research task rather than a
standards implementation task.
