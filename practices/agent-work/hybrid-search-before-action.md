---
status: canonical
version: 1.0
updated: 2026-06-12
temperature: 0.1
---

# Hybrid Search Before Action

## Source, author, link

- Source: Habr article "Claude Code создал репозиторий на 56 000 звёзд: реальный опыт работы с ИИ-агентом в продакшне".
- Author: Artem Chirkov.
- Link: https://habr.com/ru/articles/1045510/

## Practice

Before editing, combine structured search with semantic/contextual reading:
first find files, names, and contracts with structured search; then read the
relevant context and infer intent.

## Problem

Agents often edit the first plausible file and miss the governing contract,
related template, or validator.

## Apply In Hub

1. Run structured search with `rg`, `rg --files`, validators, artifact map, and
   issue/PR comments.
2. Read the smallest relevant set of files before choosing an implementation.
3. Record the source document or validator that makes the change necessary.
4. Only then patch files.

## Output

The implementation should name the contract it follows: for example,
`tools/validate-repository-structure.sh`, `pr-ops/artifact-map.md`, or a
specific standard.

## Limits

Do not turn search into exhaustive reading. Stop when the governing files and
affected artifact boundaries are clear.
