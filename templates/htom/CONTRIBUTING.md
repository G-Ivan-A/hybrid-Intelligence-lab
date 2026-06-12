---
status: draft
version: 0.2
updated: {{date}}
temperature: 0.1
---

# Contributing - {{project_name}}

Вклад в HTOM-команду `{{project_name}}` сохраняет малый размер активных
контрактов, traceability и практическую полезность для hybrid human + AI work.
Правила входа наследуются от Хаба `hybrid-Intelligence-lab` и не дублируют его.

## Workflow: issue -> PR -> review

1. **Issue.** Начинайте с GitHub issue. Для обычных задач используйте
   [.github/ISSUE_TEMPLATE/task.md](.github/ISSUE_TEMPLATE/task.md), для
   Creative mode - [.github/ISSUE_TEMPLATE/task-creative.md](.github/ISSUE_TEMPLATE/task-creative.md).
2. **PR.** Держите изменение reviewable: одна цель, понятные ссылки, без
   unrelated restructuring. Связывайте PR с issue.
3. **Review.** Финальные решения по vision, publication и merge остаются за
   человеком согласно [AI_GOVERNANCE.md](AI_GOVERNANCE.md).

## AI-Assisted Work

AI agents следуют [AI_GOVERNANCE.md](AI_GOVERNANCE.md) и
[AI_QUICK_RULES.md](AI_QUICK_RULES.md): читают issue и последние комментарии,
сохраняют human decision rights, не публикуют sensitive data, работают внутри
requested scope и не создают `research/` в HTOM-команде.

### Специфика работы с AI-агентами

- Каждый запуск агента - новая сессия. Передавайте summary, issue, PR или
  handover prompt, если нужен контекст предыдущей работы.
- Агент не мониторит GitHub comments, review comments и CI после остановки
  сессии. Для продолжения нужен manual restart.
- Comment + manual restart означает итерацию в том же PR; merge означает
  принятие результата; close без merge означает отклонение или отмену.
- Агент не заполняет пустые поля задачи выдуманными значениями.
- В Creative mode допустим обоснованный обход рекомендации Хаба, если он не
  нарушает hard bans и записан в PR, ADR или audit.

## Локальная проверка

```bash
./tools/validate-repository-structure.sh
```

## Pull Request Checklist

- [ ] PR связан с issue.
- [ ] Изменённые файлы соответствуют целевой структуре HTOM-команды.
- [ ] Значимое изменение отражено в [CHANGELOG.md](CHANGELOG.md) (`## Unreleased`).
- [ ] Решение, отклоняющееся от рекомендации Хаба, зафиксировано как ADR в `docs/adr/`.
- [ ] Локальная проверка `./tools/validate-repository-structure.sh` пройдена.
- [ ] Риски, допущения и фокус human review сформулированы явно.
