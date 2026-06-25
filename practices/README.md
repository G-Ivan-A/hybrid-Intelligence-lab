---
status: canonical
version: 1.0
updated: 2026-06-12
temperature: 0.1
---

# Practice Catalog

`practices/` is the fixed knowledge base for reusable Hub practices. It is
separate from `docs/` and `research/` on purpose.

## Research vs fixed practices

| Layer | Place | Role |
| --- | --- | --- |
| Research | `research/<domain>/` | Compares sources, alternatives, risks, and open questions. |
| Fixed practice | `practices/<domain>/<practice>.md` | Records one reusable behavior accepted for Hub reuse. |
| Template or prompt | `templates/` | Provides an executable copy surface for applying practices. |
| Project adaptation | Project issue/PR | Decides whether a practice fits local context. |

Research can recommend. A practice node fixes. A sync prompt or issue imports.

## Practice catalog

| Area | Index | Research source |
| --- | --- | --- |
| Agent work | [agent-work/](agent-work/) | [2026-06-12-external-practice-intake.md](../research/hub/2026-06-12-external-practice-intake.md) |
| AI governance | [ai-governance/](ai-governance/) | [2026-06-12-international-ai-governance-practices.md](../research/hub/2026-06-12-international-ai-governance-practices.md) |

## Node Requirements

Every practice node must include:

1. Source, author, link.
2. Problem it solves.
3. When to apply.
4. How to implement in the Hub or a synchronized project.
5. Evidence or review signal.
6. Known limits and local adaptation rule.

Do not add a practice only because an external source is interesting. Add it
when it removes repeated work, improves review quality, or gives projects a
reusable operational pattern.
