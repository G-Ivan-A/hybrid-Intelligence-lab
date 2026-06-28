---
status: accepted
version: 1.0
updated: 2026-06-28
temperature: 0.1
owner: G-Ivan-A
rfc-scope: A
---

# RFC: Стандарт структуры ADR

## Summary

Принять единый базовый контракт ADR (Architectural Decision Record) для Хаба и
архетипов A/B/C/D: necessary and sufficient frontmatter, стабильная
идентификация, тело с контекстом, решением, альтернативами, последствиями,
проверкой и явной семантикой supersession.

Этот RFC принят как governance decision record. Обязательная норма делегирована
в [ADR Structure Standard](../../standards/adr-structure-standard.md), а будущие
шаблоны или validator updates должны ссылаться на этот RFC как на rationale, но
не дублировать его proposal-обёртку.

Входные источники:

- [ADR industry norms research](../../research/hub/2026-06-27-adr-industry-norms-and-variants.md);
- [RFC industry norms research](../../research/hub/2026-06-27-rfc-industry-norms-and-variants.md);
- [ADR-001](../../docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md);
- [ADR-002](../../docs/adr/2026-06-adr-002-artifact-document-methodology.md);
- [Frontmatter Docs Standard](../../standards/frontmatter-docs-standard.md);
- [File Naming](../../standards/file-naming.md).

## Decision

1. ADR фиксирует принятое решение и rationale, а не обсуждение всех вариантов.
2. Текущий Хаб создает ADR в `docs/adr/` и не переносит существующие RFC из
   `governance/rfc/` без отдельного миграционного решения.
3. Новый Hub/HTOM ADR использует имя
   `YYYY-MM-adr-NNN-short-title.md`, где `NNN` - стабильный ADR id.
4. Frontmatter ADR содержит поля, необходимые и достаточные для governance:
   `status`, `version`, `updated`, `temperature`, `owner`, `decision-type`.
   Frontmatter `status` является единственным machine-readable canon; body-level
   status в `Decision Metadata` остается narrative summary.
5. Базовый ADR contract обязателен для всех архетипов, но вес отдельных секций
   меняется по матрице A/B/C/D.

## Base Contract

### Identification

| Элемент | Решение |
| --- | --- |
| Canonical path | `docs/adr/` для текущего Хаба и HTOM/spoke ADR. |
| Filename | `YYYY-MM-adr-NNN-short-title.md`. |
| Stable id | `ADR-NNN`, совпадает с номером в имени файла и заголовке. |
| Title | `# ADR-NNN: Short decision title`. |
| Date | В имени файла и в `updated`; дата принятия фиксируется в секции Decision Metadata. |
| Source link | Issue, RFC, research или PR, из которого выросло решение. |

Почему не number-first `NNNN-title.md`: это сильная ADR-tool норма, но текущий
репозиторий уже валидирует date-first ADR в `docs/adr/`. Стабильность ссылки
достигается через `ADR-NNN`, а chronology остается совместимой с
[File Naming](../../standards/file-naming.md).

### Frontmatter

Обязательный frontmatter:

```yaml
---
status: draft
version: 0.1
updated: YYYY-MM-DD
temperature: 0.1
owner: Human owner or owning group
decision-type: governance | methodology | product | curriculum | runtime
---
```

Дополнительные поля не становятся обязательными в YAML, пока их не потребляет
инструмент, индекс, шаблон или provenance rule. `ai-generated` запрещен:
provenance фиксируется в issue, PR, changelog или audit.

### Required Body Sections

ADR должен содержать секции в таком порядке:

1. `Decision Metadata`
2. `Context`
3. `Decision`
4. `Decision Drivers`
5. `Alternatives Considered`
6. `Consequences`
7. `Compliance and Validation`
8. `Lifecycle`
9. `Related Artifacts`

Минимальный шаблон:

```markdown
# ADR-NNN: Short decision title

## Decision Metadata

| Field | Value |
| --- | --- |
| ADR id | ADR-NNN |
| Decision type | governance / methodology / product / curriculum / runtime |
| Decision status | same as frontmatter status; narrative summary only |
| Decision date | YYYY-MM-DD |
| Owner | Human owner or owning group |
| Source | Issue/RFC/research/PR link |
| Impacted artifacts | Paths or "none" |
| Supersedes | ADR-NNN or "none" |
| Superseded by | ADR-NNN or "none" |

## Context

Problem, constraints, and why the decision is needed now.

## Decision

One accepted decision, stated directly.

## Decision Drivers

- Driver 1.
- Driver 2.

## Alternatives Considered

| Alternative | Why rejected |
| --- | --- |
| ... | ... |

## Consequences

Positive effects, trade-offs, and follow-up work.

## Compliance and Validation

How humans, validators, docs, tests or runtime checks verify the decision.

## Lifecycle

Transition state, review trigger, deprecation and supersession rules.

## Related Artifacts

Links to RFC, standard, template, validator, implementation PR or research.
```

## Lifecycle

ADR lifecycle uses the Governance frontmatter vocabulary from
[Frontmatter Docs Standard](../../standards/frontmatter-docs-standard.md).

| Frontmatter status | Meaning |
| --- | --- |
| `draft` | ADR text is being written before review. |
| `proposed` | ADR text is ready for human review before acceptance. |
| `accepted` | Human decision accepted; ADR is the active decision record. |
| `rejected` | Decision proposal was rejected but preserved for rationale. |
| `deprecated` | Decision still describes history but should not guide new work. |
| `superseded` | Later ADR/RFC replaces this decision. |

Allowed transitions:

```mermaid
flowchart LR
    Draft[draft] --> Proposed[proposed]
    Proposed[proposed] --> Accepted[accepted]
    Proposed --> Rejected[rejected]
    Accepted --> Deprecated[deprecated]
    Accepted --> Superseded[superseded]
    Deprecated --> Superseded
```

Rules:

- `accepted` requires explicit human review or merge decision.
- `superseded` requires a backlink to the replacing ADR/RFC.
- `deprecated` requires a migration or replacement note.
- Rejected ADRs remain linkable when the rejected alternative is likely to
  reappear in future work.

## Матрица дельт A/B/C/D

| Архетип | ADR role | Required deltas | Keep light |
| --- | --- | --- | --- |
| A. Governance & Knowledge Hub | Governance-record for cross-repository methodology, lifecycle, standards and AI contracts. | Require source RFC/research link, impacted artifacts, compliance/validation and supersession. | Do not create ADR for typo fixes, local cleanup or accepted RFCs that already serve as decision records. |
| B. Prompt & Pattern Library | Lightweight decision record for stable prompt/process/pattern standards. | Require evidence link, affected prompts/patterns and rollback/evaluation notes. | Do not create ADR for routine prompt wording, experiments or one-off tuning. |
| C. Product Spoke / Runtime | Engineering decision record for public API, runtime architecture, data, compatibility and release-impact choices. Library/SDK is a profile of archetype C, not a separate archetype. | Require compatibility, migration, runtime validation and owner. | Do not duplicate product specs, issue acceptance criteria or small feature PRs. |
| D. Education / Learning Package | Curriculum/platform decision record for durable learning outcomes, assessment and course architecture. | Require learner impact, curriculum migration and review trigger. | Do not create ADR for individual lesson edits or short-lived course notes. |

## Appendix: Minimal Archetype Examples

### B. Prompt & Pattern Library ADR

```yaml
---
status: proposed
version: 0.1
updated: YYYY-MM-DD
temperature: 0.1
owner: Prompt library owner
decision-type: methodology
---
```

Minimum body emphasis: affected prompts or patterns, evidence from a failed case
or evaluation, rollback rule and review trigger.

### C. Product Spoke / Runtime ADR

```yaml
---
status: proposed
version: 0.1
updated: YYYY-MM-DD
temperature: 0.1
owner: Product or engineering owner
decision-type: product
---
```

Minimum body emphasis: compatibility impact, migration path, runtime validation,
release impact and rollback rule. Library/SDK decisions use this same C profile.

## Boundary RFC/ADR

Use this rule for the RFC/ADR boundary:

| Situation | Decision |
| --- | --- |
| Proposal needs broad review, alternatives and human choice before the decision. | Create RFC first; create ADR after acceptance only if a short accepted decision record is needed. |
| Accepted RFC already contains final status, rationale, alternatives, consequences and no separate downstream standard is produced. | Accepted RFC may itself be the decision record; do not duplicate it as ADR. |
| Decision is narrow, already accepted, or does not need proposal-stage discussion. | Create ADR directly. |
| Accepted decision creates or changes a standard, template, validator, practice or cross-repository rule. | Prefer RFC -> ADR -> standard/template/validator route. |
| Decision only explains implementation details of one PR. | Do not create ADR; PR description is enough. |

The key invariant: RFC answers "should we accept this change and how?", ADR
answers "what decision was accepted and why?".

## Critical Analysis

| Hypothesis under attack | Refutation attempt | Decision |
| --- | --- | --- |
| ADR filenames should switch to number-first because strict ADR tools use that norm. | Number-first improves ADR tool compatibility, but conflicts with the current Hub date-first ADR validator and would require a migration unrelated to this task. Stable `ADR-NNN` inside a date-first filename preserves both citation and chronology. | Keep `YYYY-MM-adr-NNN-short-title.md`. |
| `owner` and `decision-type` should stay in body metadata only. | Issue #282 makes both fields governance-critical: validators and routing need them without reading prose. | Require `owner` and `decision-type` in frontmatter; keep impacted artifacts and rationale in the body. |
| Every accepted RFC should produce an ADR. | Backstage-like RFC -> ADR separation is useful for large proposal histories, but PEP/EIP/Rust-like accepted proposals can be decision records themselves. Mandatory duplication would create two sources of truth. | ADR is required only when a concise accepted decision record or downstream standard trace is needed. |
| One strict ADR template should apply identically to A/B/C/D. | Industry evidence shows strong ADR signals in governance/product contexts and weak signals in prompt/education contexts. Uniform weight would over-formalize B/D. | Use a common base contract plus archetype deltas. |
| `deprecated` should remain body-only. | Deprecation is a governance lifecycle state and the validator now supports it. Keeping it body-only would recreate two status sources. | Allow `deprecated` in frontmatter Governance status. |

Confirmation threshold: all accepted decisions above survived refutation except
with bounded, documented trade-offs. The trade-offs are below the issue's 20%
counter-argument threshold because each rejected alternative requires a broader
migration, extra validator work or duplicate decision source.

## Impacted Artifacts

Accepted impact:

- promote this RFC to `accepted` governance status;
- create [ADR Structure Standard](../../standards/adr-structure-standard.md);
- register the RFC and standard in [Governance RFC README](README.md),
  [Standards README](../../standards/README.md), [Artifact Map](../artifact-map.md)
  and `tools/validate-repository-structure.sh`;
- keep `tools/validate-frontmatter.sh` as-is because it already enforces ADR
  `owner` and `decision-type` requirements from
  [Frontmatter Docs Standard](../../standards/frontmatter-docs-standard.md).

Future work after acceptance:

- create an ADR template if repeated ADR creation continues;
- evaluate numeric RFC/ADR id allocation after RFC-020; if adopted, migrate with
  backlink preservation.

## Open Questions

No blocking Open Questions remain for acceptance. Non-blocking follow-up work is
limited to future templates, numeric id allocation and validator migration tasks
tracked outside this RFC.

## Review Status

Accepted for issue #286 as the rationale source for
[ADR Structure Standard](../../standards/adr-structure-standard.md). The
mandatory contract lives in the standard; this RFC preserves context,
alternatives, trade-offs and boundary reasoning.
