---
status: canonical
version: 1.0
updated: 2026-06-12
temperature: 0.1
---

# Plan-Verify-Ship Loop

## Source, author, link

- Source: Habr article "Claude Code создал репозиторий на 56 000 звёзд: реальный опыт работы с ИИ-агентом в продакшне".
- Author: Artem Chirkov.
- Link: https://habr.com/ru/articles/1045510/

## Practice

Use the issue loop `Explore -> Plan -> Code -> Test -> Review -> Ship` for any
non-trivial Hub change.

## Problem

Without a loop, an agent can skip from reading to final answer and leave missing
validation, stale indexes, or uncommitted files.

## Apply In Hub

1. Explore: read issue, comments, related code/docs, and validators.
2. Plan: turn requirements into a checklist and identify tests.
3. Code: make scoped edits.
4. Test: run local validators and relevant builds.
5. Review: inspect diff for semantics, duplication, and broken links.
6. Ship: commit, push, update PR description, and check CI.

## Output

The PR should show changed artifacts, validation results, and any remaining
human decision points.

## Limits

For tiny edits, collapse the loop but keep the same order.
