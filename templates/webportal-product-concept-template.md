---
status: draft
version: 0.1
updated: {{date}}
temperature: 0.1
ai-generated: true
level: L2
standard: "{{hub_url}}/standards/webportal-product-concept-standard.md"
---

# Product Concept: {{project_name}}

> Template aligned with
> [Webportal Product Concept Standard]({{hub_url}}/standards/webportal-product-concept-standard.md).
> Fill the product decisions for the next 1-2 years. Keep implementation
> details in the L3 Solution Concept.

## 1. Summary

Briefly state what {{project_name}} is, who it serves and what user value it
creates.

Example:

> {{project_name}} helps independent learners find a clear starting path through
> a topic, choose the next useful material and return when they are ready to
> continue.

## 2. User Personas

| Persona | Context | Need | Success Criteria |
| --- | --- | --- | --- |
| First-time visitor | Arrives from search or a shared link | Understand where to start | Finds one relevant start path within 2 minutes |
| Returning user | Comes back after reading earlier material | Continue without losing context | Opens the next useful item without searching again |

## 3. User Stories / Jobs-to-Be-Done

| Persona | Story / Job | Priority | Acceptance Criteria |
| --- | --- | --- | --- |
| First-time visitor | As a first-time visitor, I want to understand the portal's value quickly, so that I can decide whether to continue. | MVP | User reaches a clear next action from the first screen. |
| Returning user | When I return after a previous visit, I want to continue from a known point, so that I do not restart discovery. | Next | User can identify what changed and what to open next. |

## 4. Key Features (MVP Scope)

| Feature | Persona / Job | MVP? | Rationale | Usefulness Check |
| --- | --- | --- | --- | --- |
| Start path | First-time visitor chooses where to begin | Yes | Core value is unclear without an entry path | Activation rate for first useful action |
| Curated content set | Visitor needs enough material to evaluate value | Yes | MVP needs a small but coherent set | Scroll depth, repeat visits, qualitative feedback |
| Personal workspace | Returning user saves progress | No | Useful later, not needed to validate the first path | Revisit after retention is proven |

## 5. User Flows

| Flow | Persona | Steps | Successful Completion |
| --- | --- | --- | --- |
| First visit | First-time visitor | Opens portal -> scans value statement -> chooses start path -> opens first material -> sees next step | User understands why to continue |
| Return visit | Returning user | Opens portal -> sees recent updates or known path -> opens next item -> completes action | User continues without manual guidance |

## 6. Success Metrics

| Metric | Type | Baseline | Target | Horizon |
| --- | --- | --- | --- | --- |
| First useful action rate | North Star | Measure during MVP | 30% of new visitors | 8 weeks |
| 7-day return rate | Retention | Measure during MVP | 15% of activated users | 12 weeks |
| Qualitative value signal | Product learning | 0 structured interviews | 10 clear user signals | Phase 0 |

## 7. Roadmap (High-Level)

| Phase | Product Result | Hypothesis | Exit Criteria |
| --- | --- | --- | --- |
| Phase 0: Discovery | Personas and jobs are validated | Users recognize the problem | Evidence from interviews, support requests or equivalent signals |
| Phase 1: MVP | First useful action flow is live | Users can start without explanation | North Star metric reaches the target range |
| Phase 2: Growth | Repeat usage scenarios are added | Users return for new value | Retention improves without manual follow-up |

## 8. Product Risks

| Risk | Impact | Mitigation | Owner |
| --- | --- | --- | --- |
| Personas are too broad | MVP becomes unfocused | Prioritize one primary persona for Phase 1 | Product owner |
| Content does not create repeat value | Retention stays low | Validate content themes before scaling | Editor / product owner |

## 9. Open Product Questions

- Which persona is primary for MVP?
- What is the smallest useful content set?
- Which action best represents the North Star Metric?
- What must be explicitly out of scope for the next phase?
