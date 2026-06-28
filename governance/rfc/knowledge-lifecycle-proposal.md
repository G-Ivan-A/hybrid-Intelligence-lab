---
status: draft
version: 0.2
updated: 2026-06-13
temperature: 0.1
owner: G-Ivan-A
rfc-scope: A
---

# RFC: Knowledge Lifecycle

## Proposal

Adopt `standards/knowledge-lifecycle.md` as the future canonical Hub lifecycle
standard for knowledge artifacts after explicit User approval:

```text
Observation -> Research -> Hypothesis -> RFC -> Pattern -> Standard -> Template -> Framework -> Deprecation/Archive
```

## Problem

The Hub already has research, practices, standards, templates, frameworks, and
product docs, but there is no single rule that explains how knowledge moves
between them. That makes it easy to promote an idea too early or to create a
template without a traceable prior stage.

## Decision Scope

This RFC proposes the lifecycle standard only. It does not approve every draft
artifact currently in the repository and does not promote any RFC to canonical
status by itself.

## Обратная трассируемость

**Правило обратной трассируемости:**

- Каждый **Standard** должен ссылаться минимум на один **Pattern**: откуда взята
  повторяемая практика.
- Каждый **Pattern** должен ссылаться минимум на один **RFC**: как принималось
  решение.
- Каждый **RFC** должен ссылаться минимум на одно **Research/Observation**:
  какую проблему решает предложение.

**Исключение:** если артефакт импортируется из внешнего источника
(международные практики, стандарты или публичные frameworks), ссылка на внешний
источник заменяет внутренний upstream.

**Проверка:** без этой цепочки артефакт не может быть переведён на следующий
этап зрелости. Если цепочка неполная, PR фиксирует missing upstream как
lifecycle gap, а не молча повышает статус.

## Frontmatter Traceability Contract

Будущий canonical standard должен закрепить стандартные поля frontmatter для
артефактов, которые переходят между lifecycle stages:

```yaml
traceability:
  based_on: [ссылка на upstream]
  supersedes: [ссылка на устаревший артефакт, если есть]
  used_by: [ссылки на downstream]
```

Поля `based_on`, `supersedes` и `used_by` не заменяют body links и PR evidence:
они дают быстрый индекс зависимостей, а обоснование остаётся в RFC, issue, PR
или source-backed research.

## Target Artifact

| Target | Status in this PR | Promotion condition |
| --- | --- | --- |
| `standards/knowledge-lifecycle.md` | Proposed target, not created by this PR | User review plus явное подтверждение Пользователя. |

## Key Rules

- Each stage has a default location, user group, and transition criteria.
- Reverse traceability is required before moving an artifact to the next
  maturity stage.
- Framework L1-L2 lives in `docs/`; Methodology L3-L4 lives in
  `governance/`, `standards/`, `practices/`, `templates/`, `tools/`, and
  project/framework packages.
- Structured mode logs lifecycle gaps and completes the explicit task without
  silently promoting artifacts.
- Creative mode can initiate missing prior documents when that is the smallest
  way to make the work reviewable.
- Silence means acceptance of current state only, not approval to transition to
  the next stage.
- Merge silence means applying this PR as-is: the RFC stays in
  `governance/rfc/` with `status: draft`; it does not create the target file and
  does not promote the artifact to `canonical`.

## Acceptance Criteria

- The lifecycle chain is documented end to end.
- Each stage has a repository location, user group, and transition criteria.
- Reverse traceability and standard `traceability` frontmatter fields are
  documented.
- Resolver behavior for Structured and Creative modes is described.
- Deprecation/Archive is defined without reintroducing an archive directory by
  default.
- Artifact map, standards index, governance docs, and contributing guidance link
  to the lifecycle.

## Open Decision

Should the draft target be promoted to `status: canonical`, or should it remain
draft until the first project applies it and reports feedback?
