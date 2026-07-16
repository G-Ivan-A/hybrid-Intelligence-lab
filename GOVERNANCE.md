---
status: canonical
version: 1.0
updated: 2026-07-16
temperature: 0.1
---

# Governance

Корневой навигационный якорь governance-слоя Хаба, предусмотренный ADR-007.
Нормативный материал физически разделён по аудитории:

- [AI Governance](ai-governance/ai-governance.md) — политики, роли, human
  decision rights, security/compliance-ограничения и эскалация;
- [Agent Work Rules](ai-rules/agent-work-rules.md) — правила поведения
  AI-агента, Operating Modes, pre-flight и Definition of Done;
- [PR Operations](pr-ops/README.md) — операции issue/task/PR/review;
- [Standards](standards/README.md) — требования к форме и готовности
  артефактов.

Граница между policy и agent rule задана
[ADR-007](docs/adr/2026-07-adr-007-hub-root-structure.md). Этот файл остаётся
тонкой стабильной точкой входа и не дублирует нормативные тексты.
