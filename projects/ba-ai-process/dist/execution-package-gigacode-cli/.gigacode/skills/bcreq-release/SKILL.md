---
name: bcreq-release
description: Compile an approved Working baseline into a deterministic client Release.
packs: P-03/SK-bcreq-release
interaction: human-checkpointed
inputs: [A-BCREQ]
outputs: [A-BCREQ, release_manifest]
contracts: [C-WORKING-BCREQ, C-RELEASE-BCREQ]
gates: [G-self, G-mach, G-release, G-human]
compiled_from: { package: execution-package-gigacode-cli, route: RG-BCREQ-v1 }
derived_from: [https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-working-release-pipeline.md]
compiled_at: 2026-09-24
status: draft
version: 1.0
updated: 2026-09-24
temperature: 0.1
---

# BCREQ Release

## Когда применять

Run at `n13` after the BA approved Working baseline passes `G-mach` and
`G-semantic`.

## Предусловия

The `working` projection of A-BCREQ is immutable, has a verified digest, and records BA
approval. The versioned `BCREQ-client-v1` profile is available.

## Шаги

1. Run `python3 tools/bcreq_pipeline.py validate-working WORKING.json`.
2. Run `python3 tools/bcreq_pipeline.py compile WORKING.json --output RELEASE_DIR`.
3. Run `python3 tools/bcreq_pipeline.py validate-release WORKING.json --release RELEASE_DIR/release.json --manifest RELEASE_DIR/release-manifest.json`.
4. Inspect all included and excluded Working IDs, audience, NFR to FR links,
   compatibility obligations, the byte-stable digest, and every reverse link.
5. Ask `G-human` to approve publication. A semantic correction creates a new
   Working draft and invalidates this Release.

## Обязательные слоты выхода

`release.json` and `release-manifest.json` contain the selected profile,
baseline ID and digest, release digest, fragment IDs, and reverse links to
approved Working IDs.

## Самопроверка (G-self)

- Working is approved and its digest matches.
- Repeated compilation yields byte-identical files.
- Every fragment has a valid reverse link and adds no semantic text.
- No unresolved question or `TBD` NFR target is published.
- No compatibility obligation affecting a published FR is omitted.

## Отказ

Stop on an unapproved baseline, failed digest, unresolved item, missing
reverse link, nondeterministic output, or rejected human publication review.
