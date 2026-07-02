---
status: draft
version: 0.1
updated: 2026-07-02
temperature: 0.1
type: experiment
context: [hub, mango, clarify, analysis, inventory, issue-342, b-024]
method: repository-scan
---

# Experiment: Analysis inventory for issue 342

Reproducible scan for the cross-repo Analysis artifact inventory in issue #342.
The script creates the evidence layer for
[2026-07-02-analysis-artifacts-inventory.md](../../../../docs/analysis/2026-07-02-analysis-artifacts-inventory.md).

## Scope

Scanned tracked text artifacts from:

- `hybrid-Intelligence-lab`: `docs/analysis/**`, `docs/report/**`,
  `docs/audit/**`, `research/**`, `governance/**`;
- `mango_ba_prompts`: `docs/analysis/**`, `docs/report/**`,
  `docs/audit/**`, `research/**`, `governance/**`;
- `clarify-engine-ai`: `docs/analysis/**`, `docs/report/**`,
  `docs/audit/**`, `research/**`, `governance/**`.

The script also accepts legacy `docs/reports/**` as an alias so older snapshots
do not hide report-like artifacts during reruns. Classification does not rely on
path alone: `scan-analysis.py` uses path, frontmatter, title, filename and early
content signals to classify each text artifact as `Research`, `Analysis`,
`Audit`, `Report`, `RFC`, `ADR` or `Other`.

Own issue #342 deliverables are excluded from the Hub baseline so reruns after
merge do not count the new report or this evidence container.

## Reproduce

```bash
git clone --branch issue-342-77d04d6f83f9 https://github.com/konard/G-Ivan-A-hybrid-Intelligence-lab.git /tmp/issue-342-hub-working
git clone --branch issue-342-77d04d6f83f9 https://github.com/konard/G-Ivan-A-hybrid-Intelligence-lab.git /tmp/issue-342-hub-baseline
git clone https://github.com/G-Ivan-A/mango_ba_prompts.git /tmp/issue-342-mango_ba_prompts
git clone https://github.com/G-Ivan-A/clarify-engine-ai.git /tmp/issue-342-clarify-engine-ai
git -C /tmp/issue-342-hub-baseline checkout 3abae05d142284a98719c4549229b6c0099eeb65
git -C /tmp/issue-342-mango_ba_prompts checkout 52bc8b72419abb9548d9b6091623f18c080efae4
git -C /tmp/issue-342-clarify-engine-ai checkout 96c288fd13a2d7cc7c3e3cdd52574944858e6255

python3 /tmp/issue-342-hub-working/research/hub/exp/analysis-inventory-342/scan-analysis.py \
  --hub-root /tmp/issue-342-hub-baseline \
  --mango-root /tmp/issue-342-mango_ba_prompts \
  --clarify-root /tmp/issue-342-clarify-engine-ai \
  --out-dir /tmp/issue-342-hub-working/research/hub/exp/analysis-inventory-342
```

## Outputs

The `exp/` container uses the flat structure from `standards/research-standard.md`:
evidence files live next to `README.md` and the script.

| Output | Purpose |
| --- | --- |
| [analysis-inventory.json](analysis-inventory.json) | Full machine-readable scan with repository snapshots, current buckets, actual types, relation to Analysis and routing hints. |
| [2026-07-02-analysis-artifact-matrix.md](2026-07-02-analysis-artifact-matrix.md) | Markdown matrix for review and links from the main analysis report. |
