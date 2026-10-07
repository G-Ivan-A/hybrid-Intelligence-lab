---
status: draft
version: 0.1
updated: 2026-09-26
temperature: 0.1
---

# Knowledge source policy

For each claim, first query the approved **read-only corporate connection**
for Jira or Confluence and record the exact resource, anchor, retrieval time
and short evidence excerpt. The Mango AI model API supplies the model; a
separately approved connection supplies corporate knowledge. If the corporate
query is unavailable or yields no verified source, search permitted files in
`docs/kb/` and record the file path, revision and anchor. If neither source
provides evidence, stop with an explicit missing-source error or open question.
Do not fill a gap with a guessed citation, an empty locator or model memory.

The local KB is a fallback for a missing external source, not proof that the
external resource was read. When sources disagree, show both anchors to the BA
for resolution; do not silently prefer one. The BA confirms each claim and
decides whether its source may be included in a client Release. Never commit
corporate KB files or credentials to a public repository.
