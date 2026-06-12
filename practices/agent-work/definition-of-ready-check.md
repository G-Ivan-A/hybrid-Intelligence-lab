---
status: canonical
version: 1.0
updated: 2026-06-12
temperature: 0.1
---

# Definition of Ready Check

## Source, author, link

- Source: Habr article "Claude Code создал репозиторий на 56 000 звёзд: реальный опыт работы с ИИ-агентом в продакшне".
- Author: Artem Chirkov.
- Link: https://habr.com/ru/articles/1045510/

## Practice

Before implementation, convert a task into a short Definition of Ready: goal,
required artifacts, acceptance checks, and unknowns.

## Problem

Creative tasks can be broad enough that an agent starts producing artifacts
before knowing what "done" means.

## Apply In Hub

1. Read the issue, latest comments, and PR review comments.
2. List required artifacts and validation commands.
3. If the issue is clear, encode the expectation in a validator or checklist.
4. If the issue is unclear, ask a clarifying question before creating broad
   structures.

## Output

A ready task has an implementation target, a validation path, and a reviewable
artifact list.

## Limits

Definition of Ready is not a blocker for Creative mode exploration. It is a
guardrail that keeps exploration reviewable.
