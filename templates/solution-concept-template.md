---
status: draft
version: 0.1
updated: {{date}}
temperature: 0.1
---

# Solution Concept: {{project_name}}

> Universal L3 template for implementation methodology, architecture, operating
> model, or delivery design. Use it after the L2 Product Concept is clear enough
> to guide execution.
> Source Hub: {{hub_url}}.

## 1. Summary

Describe the proposed solution approach for {{project_name}} in 3-5 sentences:
boundaries, operating model, main components, key dependencies, and decision
status.

## 2. Inputs From L2

| L2 Input | Value | Link / Source |
| --- | --- | --- |
| Primary user / context | TBD | Product Concept section |
| Main job or flow | TBD | Product Concept section |
| MVP boundary | TBD | Product Concept section |
| Success metric | TBD | Product Concept section |

## 3. Methodology Link

| Level | Artifact | How this solution uses it |
| --- | --- | --- |
| L1 | Vision | TBD |
| L2 | Product Concept | TBD |
| L3 | Governance / standards / practices | TBD |
| L4 | Templates / tools / prompts / checks | TBD |

Use [Knowledge Lifecycle](../standards/knowledge-lifecycle.md) to keep solution
decisions traceable to L1-L2 context and L3-L4 execution.

## 4. Solution Boundaries

| Boundary | Inside | Outside | Owner |
| --- | --- | --- | --- |
| Functional scope | TBD | TBD | TBD |
| Data / knowledge scope | TBD | TBD | TBD |
| Governance scope | TBD | TBD | TBD |
| Integration scope | TBD | TBD | TBD |

## 5. Architecture Or Operating Model

Use the lightest model that makes the decision reviewable. For software, this
can be a C4-style context/container view. For process, education, or knowledge
systems, use workflow and responsibility views.

```mermaid
flowchart LR
  user[User / Team]
  solution[{{project_name}}]
  hub[Hub Practices and Standards]
  output[Expected Result]

  user --> solution
  hub --> solution
  solution --> output
```

| Component / Workstream | Responsibility | Inputs | Outputs | Owner |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD |

## 6. Key Decisions

| Decision | Options Considered | Selected Option | Status | Rationale |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | proposed / accepted / deferred | TBD |

## 7. Integrations And Dependencies

| Dependency | Purpose | Direction | Failure Mode | Fallback |
| --- | --- | --- | --- | --- |
| Hub artifact | Reuse standards or practices | inbound | Draft changes or mismatch | Pin version and document adaptation |
| External system / team | TBD | TBD | TBD | TBD |

## 8. Data, Knowledge, Or Content Model

| Entity / Artifact | Purpose | Owner | Retention | Sensitivity |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD |

## 9. Non-Functional Requirements

| Category | Requirement | Target | Measurement | Phase |
| --- | --- | --- | --- | --- |
| Reliability | TBD | TBD | TBD | MVP |
| Security / privacy | TBD | TBD | TBD | MVP |
| Maintainability | TBD | TBD | TBD | MVP |
| Usability | TBD | TBD | TBD | MVP |

## 10. Validation Plan

| Check | Command / Method | Owner | Pass Criteria |
| --- | --- | --- | --- |
| Local validation | TBD | TBD | TBD |
| Review checklist | TBD | TBD | TBD |
| User or stakeholder signal | TBD | TBD | TBD |

## 11. Rollout And Change Management

| Step | Action | Approval Needed | Rollback |
| --- | --- | --- | --- |
| 1 | Prepare draft | Reviewer | Revert draft branch |
| 2 | Validate | Reviewer / owner | Fix or split PR |
| 3 | Adopt | Human owner | Supersede or deprecate |

## 12. Risks And Mitigations

| Risk | Probability | Impact | Mitigation | Trigger |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD |

## 13. Open Solution Questions

- Which L2 decision is still too unclear for implementation?
- Which dependency requires explicit human approval?
- Which part should be a reusable Hub template or practice later?
- Which validation command or review checklist proves this solution is ready?
