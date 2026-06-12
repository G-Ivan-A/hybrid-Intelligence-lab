---
status: canonical
version: 1.0
updated: 2026-06-12
temperature: 0.1
---

# Skill Catalog Token Budget

## Source, author, link

- Source: Habr article "Мы стали жертвами собственного успеха: как 91,000+ навыков убили Claude Code и почему OpenAI был прав с подходом Skills".
- Author: slam.
- Link: https://habr.com/ru/articles/1045552/

## Practice

Keep reusable workflows discoverable through indexes and metadata, but load only
the specific workflow needed for the task. The 91,000+ skills case is a warning:
catalog size without retrieval discipline becomes context noise.

## Problem

Large catalogs degrade agent performance when too much instruction text is
placed in the prompt or default context.

## Apply In Hub

1. Keep `practices/README.md` as a catalog, not a full content dump.
2. Use domain indexes such as `agent-work/README.md` and
   `ai-governance/README.md`.
3. Link to atomic nodes; do not inline every practice everywhere.
4. Prefer sync prompts that compare and select relevant nodes over blanket
   copying.

## Output

Agents can find practices by area and import only the nodes that match the
project.

## Limits

If discovery becomes difficult, improve indexes before adding a new hierarchy.
