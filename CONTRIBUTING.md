---
status: canonical
version: 1.1
updated: 2026-06-12
temperature: 0.1
---

# Contributing

Вклад в репозиторий должен сохранять малый размер активных контрактов,
traceability и практическую полезность для hybrid human + AI work.

## Workflow

1. Начинайте с GitHub issue, где есть context, scope, язык результата,
   acceptance criteria и forbidden changes.
2. Для обычных задач используйте
   [.github/ISSUE_TEMPLATE/task.md](.github/ISSUE_TEMPLATE/task.md) или
   GitHub-native форму [.github/ISSUE_TEMPLATE/task.yml](.github/ISSUE_TEMPLATE/task.yml).
3. Для Creative mode используйте
   [.github/ISSUE_TEMPLATE/task-creative.md](.github/ISSUE_TEMPLATE/task-creative.md):
   описывайте цель, constraints и Definition of Done, не предписывая исполнителю
   лишние шаги реализации.
4. Выбирайте целевой каталог по
   [governance/repo-model.md](governance/repo-model.md).
5. Используйте ближайший стандарт из [standards/README.md](standards/README.md).
6. Держите изменение reviewable: одна цель, понятные ссылки, без unrelated
   restructuring.
7. Обновляйте навигацию, changelog и artifact map, если новый active artifact
   становится частью публичного контракта репозитория.
8. Запускайте локальную проверку перед открытием или обновлением PR.

## AI-Assisted Work

AI agents следуют [AI_GOVERNANCE.md](AI_GOVERNANCE.md): читают issue и
последние комментарии, сохраняют human decision rights, не публикуют sensitive
data и работают внутри requested scope.

Historical migration material используется только как source context через
audit, PR history или явно указанный `source` path. Новый active artifact должен
показывать, откуда перенесено содержание и почему оно остается полезным.

### Специфика работы с AI-агентами

- Каждый запуск агента - новая сессия. Передавайте summary, issue, PR или
  handover prompt, если нужен контекст предыдущей работы.
- Агент не мониторит GitHub comments, review comments и CI после остановки
  сессии. Для продолжения нужен manual restart.
- Comment + manual restart означает итерацию в том же PR; merge означает
  принятие результата; close без merge означает отклонение или отмену.
- Агент не заполняет пустые поля задачи выдуманными значениями. Недостающий
  контекст фиксируется как gap или вопрос.
- В Creative mode допустим обоснованный обход рекомендации Хаба, если он не
  нарушает hard bans и записан в PR, ADR/RFC или audit.

## Frontmatter

Новые и существенно изменённые Markdown-артефакты используют минимальный
frontmatter из [standards/frontmatter-standard.md](standards/frontmatter-standard.md):
`status`, `version`, `updated`, `temperature`. Дополнительные поля добавляются
только когда их потребляет валидатор, executable contract или migration
provenance.

## Локальная проверка

```bash
./tools/validate-frontmatter.sh .
./tools/validate-repository-structure.sh
python3 tools/generate-manifest.py --check
```

## Pull Request Checklist

- PR связан с issue.
- Измененные файлы соответствуют целевой структуре.
- Новые артефакты ссылаются на standards или объясняют, почему стандарта пока
  нет.
- Перенос historical material указывает source path.
- Creative override, если был, записан с rationale и validation.
- Локальная проверка указана в PR.
- Риски, допущения и human review focus сформулированы явно.
