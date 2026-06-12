---
status: canonical
version: 1.0
updated: 2026-06-12
temperature: 0.1
---

# Anthropic Capability Thresholds

## Source, author, link

- Source: Anthropic Responsible Scaling Policy.
- Organization: Anthropic.
- Link: https://www.anthropic.com/responsible-scaling-policy

## Practice

Define capability thresholds that trigger stronger safeguards when an AI
workflow becomes more powerful, autonomous, or sensitive.

## Problem

The same process can move from low-risk drafting to tool-using automation. If
safeguards do not scale with capability, governance lags behind the system.

## Apply In Hub

1. Name the capability being introduced: autonomous tool use, external writes,
   sensitive data handling, public publishing, or decision support.
2. Set the threshold that requires extra review.
3. Attach safeguards: human approval, limited permissions, logs, rollback,
   security review, or narrower scope.
4. Reevaluate thresholds when templates, models, or project context changes.

## Output

A capability threshold table inside the relevant issue, project governance file,
or practice import PR.

## Limits

This is a scaled-down operational pattern, not an adoption of Anthropic's full
frontier-model policy.
