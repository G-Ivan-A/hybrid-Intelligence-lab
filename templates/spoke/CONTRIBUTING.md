---
status: draft
version: 0.1
updated: {{date}}
temperature: 0.1
ai-generated: true
---

# Contributing — {{project_name}}

`{{project_name}}` — это **spoke-репозиторий** (отдельный продукт с
production-кодом), связанный с Хабом `hybrid-Intelligence-lab`. В отличие от
HTOM-команды, здесь основной артефакт — код в `src/` с тестами и CI/CD.
Governance-правила наследуются от Хаба и не дублируются.

## Workflow: issue → PR → review

1. **Issue.** Начинайте с GitHub issue: context, scope, измеримый Definition of
   Done. Для продуктовых изменений ссылайтесь на концепцию (L2) и решения (L3) в
   стандартах Хаба.
2. **PR.** Держите изменение reviewable: одна цель, зелёный CI, без unrelated
   restructuring. Связывайте PR с issue.
3. **Review.** Финальные решения по vision, publication и merge остаются за
   человеком.

## Качество кода и тесты

- Код живёт в `src/`, тесты — в `tests/`. Новая функциональность сопровождается
  тестами; багфикс — тестом, воспроизводящим проблему.
- CI (`.github/workflows/ci.yml`) обязан быть зелёным до merge: линт + тесты на
  каждый push и pull request.
- Значимые архитектурные решения фиксируются как ADR в `docs/adr/`.
- Хронологические документы в `docs/analysis/`, `docs/rfc/` и `docs/adr/`
  именуются с датой в начале (`YYYY-MM-name.md`, для ADR —
  `YYYY-MM-adr-NNN-name.md`) и проверяются через
  `./tools/validate-file-naming.sh`.

## AI-Assisted Work

ИИ-агенты сохраняют human decision rights, не публикуют sensitive data, работают
внутри requested scope и наследуют контракты Хаба `hybrid-Intelligence-lab`.

## Pull Request Checklist

- [ ] PR связан с issue.
- [ ] Новая функциональность/багфикс покрыты тестами в `tests/`.
- [ ] CI (`ci.yml`) зелёный: линт и тесты проходят.
- [ ] Значимое изменение отражено в документации / ADR (`docs/adr/`).
- [ ] Риски, допущения и фокус human review сформулированы явно.
