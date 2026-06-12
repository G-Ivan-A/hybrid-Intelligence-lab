---
status: canonical
version: 1.0
updated: 2026-06-12
temperature: 0.1
---

# Skills As Reusable Workflows

## Source, author, link

- Source: Habr article "Мы стали жертвами собственного успеха: как 91,000+ навыков убили Claude Code и почему OpenAI был прав с подходом Skills".
- Author: slam.
- Link: https://habr.com/ru/articles/1045552/

## Practice

Package repeated agent workflows as discoverable, self-contained instructions
with optional resources and scripts.

## Problem

When repeated workflows stay only in chat history or long README prose, agents
cannot reuse them reliably and humans cannot review their scope.

## Apply In Hub

1. Promote a workflow only after repeated use.
2. Keep the workflow small enough to load on demand.
3. Store reusable prompts in `templates/` and fixed behavior in `practices/`.
4. Link each workflow to its source research and validation command when one
   exists.

## Output

A reusable workflow has a name, trigger, steps, inputs, outputs, and a clear
place in the artifact map or manifest.

## Limits

Do not turn every one-off instruction into a workflow. The catalog should save
context, not consume it.
