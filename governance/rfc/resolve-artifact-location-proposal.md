---
status: draft
version: 0.2
updated: 2026-06-13
temperature: 0.1
owner: G-Ivan-A
rfc-scope: A
---

# RFC: Resolve Artifact Location Prompt

## Proposal

Adopt `templates/resolve-artifact-location-prompt.md` as the future executable
resolver for deciding where a new Hub artifact belongs after explicit User
approval.

## Problem

The Hub has multiple artifact classes and lifecycle stages. Without an
executable resolver, contributors and AI agents can place artifacts by local
guesswork, skip lifecycle stages, or create duplicate standards/templates.

## Scope Resolver-а

**Scope Resolver-а (строго):**

1. Ответить на вопрос: *"Куда положить этот артефакт?"* (маршрутизация).
2. Ответить на вопрос: *"Каких upstream-зависимостей не хватает?"* (проверка
   трассируемости).

**Out of Scope (запрещено):**

- Принимать решения о переводе артефакта на следующий этап Lifecycle: это
  делает lifecycle governance через review и явное подтверждение Пользователя.
- Проверять содержательное качество артефакта.
- Управлять миграцией старых файлов.
- Создавать новые артефакты: resolver только маршрутизирует существующие или
  явно предложенные артефакты.

## Decision Tree

| Question | Target |
| --- | --- |
| Is it raw signal, source-backed analysis, or comparison? | `research/<domain>/` |
| Is it a governance or structure proposal? | `governance/rfc/` |
| Is it an approved reusable behavior? | `practices/<domain>/` |
| Is it an obligatory rule or format? | `standards/` |
| Is it a copyable form or executable prompt? | `templates/` |
| Is it a methodology package for a class of projects? | `frameworks/` |
| Is it product-level Hub Vision, Concept, or ecosystem framing? | `docs/` |

## Integration

The resolver must read:

- [artifact-map.md](../artifact-map.md) as the factual map of active artifacts;
- [htom-documentation-structure.md](../../standards/htom-documentation-structure.md)
  for HTOM docs structure;
- [knowledge-lifecycle-proposal.md](knowledge-lifecycle-proposal.md) for the
  proposed lifecycle stage and transition rules;
- [repo-model.md](../repo-model.md) for Anti-Inflation and folder boundaries.

## Two-Factor Confirmation

Hard violations require explicit human approval:

- changing the top-level folder structure;
- deleting files or overwriting local project decisions;
- bypassing Anti-Inflation;
- bypassing fail-closed behavior.

Soft violations are logged in the PR:

- skipped lifecycle stage in Structured mode;
- minor frontmatter drift;
- draft artifact used only as draft context.

## Creative Mode Initiation

If a needed prior stage is missing, Creative mode creates the smallest missing
proposal or draft candidate. If blocked, the agent creates the safe part and
documents the dependency in the PR. The User then approves the transition or
explicitly writes "skip stage X".

## Target Artifact

| Target | Status in this PR | Promotion condition |
| --- | --- | --- |
| `templates/resolve-artifact-location-prompt.md` | Proposed target, not created by this PR | User review plus явное подтверждение Пользователя. |

Merge silence means applying this PR as-is: the RFC stays in `governance/rfc/`
with `status: draft`; it does not create the target file and does not promote
the artifact to `canonical`.
