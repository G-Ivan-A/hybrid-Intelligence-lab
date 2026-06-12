---
status: draft
version: 0.1
updated: 2026-06-12
temperature: 0.1
---

# International AI Governance Practices

This research separates source-backed analysis from fixed Hub practices. It
translates selected international AI governance sources into concrete,
proportional practices for Hub and HTOM projects.

## Sources

| Source | Organization | Link | Useful governance pattern |
| --- | --- | --- | --- |
| NIST AI RMF | National Institute of Standards and Technology | https://www.nist.gov/itl/ai-risk-management-framework | Risk profile loop: map, measure, manage, govern. |
| EU AI Act materials | European Commission | https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai | Risk-based classification before deployment. |
| ISO/IEC 42001 | ISO | https://www.iso.org/standard/42001 | AI management system with policies, roles, processes, and continual improvement. |
| OpenAI safety materials | OpenAI | https://openai.com/safety/ | Evaluations, system cards, deployment safety, and feedback loops. |
| Anthropic Responsible Scaling Policy | Anthropic | https://www.anthropic.com/responsible-scaling-policy | Capability thresholds and stronger safeguards as risk grows. |
| Google SAIF | Google | https://saif.google/ | Agent security controls and AI-specific risk self-assessment. |

## Applicability Matrix

| Source | Concrete practice | Applicability in Hub | Implemented as |
| --- | --- | --- | --- |
| NIST AI RMF | Maintain a small risk profile for AI-assisted workflows. | High: fits issue/PR-driven governance and validator-backed checks. | [practices/ai-governance/nist-ai-rmf-profile-loop.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/ai-governance/nist-ai-rmf-profile-loop.md) |
| EU AI Act | Classify AI use by risk tier before public or sensitive deployment. | Medium: useful as triage, not as legal compliance. | [practices/ai-governance/eu-ai-act-risk-tiering.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/ai-governance/eu-ai-act-risk-tiering.md) |
| ISO/IEC 42001 | Treat AI governance as a management loop with owner and review cadence. | High: prevents standards and templates from becoming stale. | [practices/ai-governance/iso-42001-management-loop.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/ai-governance/iso-42001-management-loop.md) |
| OpenAI | Pair pre-release evaluations with post-release feedback. | High: matches tests, validators, and issue feedback. | [practices/ai-governance/openai-evaluation-and-feedback-loop.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/ai-governance/openai-evaluation-and-feedback-loop.md) |
| Anthropic | Trigger stronger safeguards when capabilities cross thresholds. | Medium: applies to tool-using agents and higher-impact automation. | [practices/ai-governance/anthropic-capability-thresholds.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/ai-governance/anthropic-capability-thresholds.md) |
| Google SAIF | Apply AI security controls to agent tools, data, and autonomous actions. | High for tool-using agents; low for simple docs edits. | [practices/ai-governance/google-saif-agent-security.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/practices/ai-governance/google-saif-agent-security.md) |

## Executable implementation matrix

| Practice | Trigger | Minimum action | Evidence |
| --- | --- | --- | --- |
| NIST AI RMF profile loop | New AI-assisted workflow or template | Add Map/Measure/Manage/Govern notes to issue or PR. | Risk note linked from the PR. |
| EU AI Act risk tiering | Workflow touches public users, rights, safety, education, employment, identity, or regulated contexts. | Assign a risk tier and escalate non-minimal cases to human review. | Tier note and reviewer decision. |
| ISO/IEC 42001 management loop | Governance rule or template becomes reused across projects. | Assign owner, review trigger, and affected artifacts. | Artifact-map row or standard reference. |
| OpenAI evaluation and feedback loop | AI workflow is shipped or synced into a project. | Define evaluation cases and feedback channel. | Test, validator, issue checklist, or review log. |
| Anthropic capability thresholds | Agent gains external writes, tool autonomy, sensitive data access, or public publishing. | Add safeguard threshold and approval rule. | Capability threshold note. |
| Google SAIF agent security | Agent uses tools, repositories, external systems, or data. | List tools, permissions, and safeguards. | Security note or CI/check output. |

## Separation From Legal Compliance

The Hub turns international practices into proportional operating patterns. It
does not claim certification, legal compliance, or full adoption of the source
frameworks. Project owners must still decide whether a specific product needs
formal legal, security, privacy, or certification review.

## Follow-Up Candidates

| Candidate | Why not now |
| --- | --- |
| Full AI risk register template | Useful after at least two projects need the same register. |
| Machine-readable risk profile schema | Premature until the human issue/PR format stabilizes. |
| Public governance dashboard | Requires product decision and privacy boundary. |
