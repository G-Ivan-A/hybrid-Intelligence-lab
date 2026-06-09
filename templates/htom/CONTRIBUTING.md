---
status: draft
version: 0.1
updated: {{date}}
ai-generated: true
---

# Contributing — {{project_name}}

Вклад в HTOM-команду `{{project_name}}` сохраняет малый размер активных
контрактов, traceability и практическую полезность для hybrid human + AI work.
Правила входа наследуются от Хаба `hybrid-Intelligence-lab` и не дублируют его.

## Workflow: issue → PR → review

1. **Issue.** Начинайте с GitHub issue (см. шаблон в
   [.github/ISSUE_TEMPLATE/task.md](.github/ISSUE_TEMPLATE/task.md)): context,
   scope, Operating Mode, измеримый Definition of Done.
2. **PR.** Держите изменение reviewable: одна цель, понятные ссылки, без
   unrelated restructuring. Связывайте PR с issue.
3. **Review.** Финальные решения по vision, publication и merge остаются за
   человеком согласно [AI_GOVERNANCE.md](AI_GOVERNANCE.md).

## AI-Assisted Work

AI agents следуют [AI_GOVERNANCE.md](AI_GOVERNANCE.md) и
[AI_QUICK_RULES.md](AI_QUICK_RULES.md): читают issue и последние комментарии,
сохраняют human decision rights, не публикуют sensitive data, работают внутри
requested scope и не создают `research/` в HTOM-команде.

## Локальная проверка

```bash
./tools/validate-repository-structure.sh
```

## Pull Request Checklist

- [ ] PR связан с issue.
- [ ] Изменённые файлы соответствуют целевой структуре HTOM-команды.
- [ ] Значимое изменение отражено в [CHANGELOG.md](CHANGELOG.md) (`## Unreleased`).
- [ ] Решение, отклоняющееся от правила Хаба, зафиксировано как ADR в `docs/adr/`.
- [ ] Локальная проверка `./tools/validate-repository-structure.sh` пройдена.
- [ ] Риски, допущения и фокус human review сформулированы явно.
