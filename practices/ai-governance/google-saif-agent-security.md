---
status: canonical
version: 1.0
updated: 2026-06-12
temperature: 0.1
---

# Google SAIF Agent Security

## Source, author, link

- Source: Google's Secure AI Framework.
- Organization: Google.
- Link: https://saif.google/

## Practice

Apply security controls when agents can access tools, data, repositories, or
autonomous actions.

## Problem

Agent workflows add new attack and error surfaces: prompt injection, excessive
permissions, unreviewed writes, data leakage, and silent tool misuse.

## Apply In Hub

1. Identify agent tools and writable surfaces.
2. Grant the minimum permissions needed for the task.
3. Prefer read-only exploration before write actions.
4. Require human approval for destructive or external-state changes.
5. Add validation, logs, or review evidence for tool-using workflows.

## Output

A security note in the issue or project sync report that lists tools, sensitive
surfaces, and safeguards.

## Limits

Do not block simple local documentation edits with heavyweight security review.
Escalate when the agent reaches external systems, secrets, user data, or
irreversible operations.
