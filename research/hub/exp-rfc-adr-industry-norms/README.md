---
status: draft
version: 0.1
updated: 2026-06-27
temperature: 0.1
ai-generated: true
type: experiment
context: [hub, mango, rfc, adr, external-sources, evidence]
method: github-tree-scan
scope: evidence
---

# Experiment: RFC/ADR industry norms evidence

This experiment supports:

- [2026-06-27-rfc-industry-norms-and-variants.md](../2026-06-27-rfc-industry-norms-and-variants.md)
- [2026-06-27-adr-industry-norms-and-variants.md](../2026-06-27-adr-industry-norms-and-variants.md)

It collects a compact, reproducible evidence corpus for issue
[#278](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/278). The
script stores metadata, path signals and small heading/status samples. It does
not mirror external repositories.

## Inputs

| Input | Purpose |
| --- | --- |
| Current repository checkout | Local Hub RFC/ADR audit |
| Local clone `/tmp/mango_ba_prompts_issue278` | Mango RFC/ADR audit |
| GitHub repository tree API | External RFC/ADR path-signal scan |
| Primary README/template files | Manual confirmation for strong signals |

## Command

```bash
python3 research/hub/exp-rfc-adr-industry-norms/collect-evidence.py \
  --mango-path /tmp/mango_ba_prompts_issue278 \
  > research/hub/exp-rfc-adr-industry-norms/outputs/collect-evidence.log 2>&1
```

If `gh auth token` is available, the script uses it for GitHub API requests.
Without a token, GitHub may rate-limit the tree scan.

## Outputs

| Output | Purpose |
| --- | --- |
| [outputs/2026-06-27-local-rfc-adr-audit.md](outputs/2026-06-27-local-rfc-adr-audit.md) | Human-readable Hub/Mango RFC/ADR inventory |
| [outputs/local-rfc-adr-audit.json](outputs/local-rfc-adr-audit.json) | Machine-readable Hub/Mango RFC/ADR inventory |
| [outputs/2026-06-27-rfc-external-tree-summary.md](outputs/2026-06-27-rfc-external-tree-summary.md) | Human-readable RFC-like source tree summary |
| [outputs/rfc-external-tree-summary.json](outputs/rfc-external-tree-summary.json) | Machine-readable RFC-like source tree summary |
| [outputs/2026-06-27-adr-external-tree-summary.md](outputs/2026-06-27-adr-external-tree-summary.md) | Human-readable ADR-like source tree summary |
| [outputs/adr-external-tree-summary.json](outputs/adr-external-tree-summary.json) | Machine-readable ADR-like source tree summary |
| [outputs/collect-evidence.log](outputs/collect-evidence.log) | Last run log |

## Method notes

The path regex intentionally catches broad signals such as `rfcs/`, `keps/`,
`peps/`, `beps/`, `legacy_rfcs/`, `adr/`, `decision-records/`, `architecture/`
and number-first Markdown documents. These are only evidence candidates.

Research conclusions in the parent reports use a stricter rule:

1. Strong claim requires source README/template/process confirmation.
2. Path-only signal is reported as weak.
3. Zero path signal is treated as absence of visible repository convention, not
   proof that the project lacks governance.
4. False positives in education/content repositories are explicitly called out
   in the parent reports.
