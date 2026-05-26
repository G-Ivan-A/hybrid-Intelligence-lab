# Contributing

Вклад в репозиторий должен сохранять малый размер активных контрактов,
traceability и практическую полезность для hybrid human + AI work.

## Workflow

1. Начинайте с GitHub issue, где есть context, scope, язык результата,
   acceptance criteria и forbidden changes.
2. Выбирайте целевой каталог по
   [governance/REPO_MODEL.md](governance/REPO_MODEL.md).
3. Используйте ближайший стандарт из [standards/README.md](standards/README.md).
4. Держите изменение reviewable: одна цель, понятные ссылки, без unrelated
   restructuring.
5. Обновляйте навигацию, если новый active artifact становится частью
   публичного контракта репозитория.
6. Запускайте локальную проверку перед открытием или обновлением PR.

## AI-Assisted Work

AI agents следуют [AI_GOVERNANCE.md](AI_GOVERNANCE.md): читают issue и
последние комментарии, сохраняют human decision rights, не публикуют sensitive
data и работают внутри requested scope.

Historical migration material используется только как source context через
audit, PR history или явно указанный `source` path. Новый active artifact должен
показывать, откуда перенесено содержание и почему оно остается полезным.

## Локальная проверка

```bash
./tools/validate-frontmatter.sh .
./tools/validate-repository-structure.sh
```

## Pull Request Checklist

- PR связан с issue.
- Измененные файлы соответствуют целевой структуре.
- Новые артефакты ссылаются на standards или объясняют, почему стандарта пока
  нет.
- Перенос historical material указывает source path.
- Локальная проверка указана в PR.
- Риски, допущения и human review focus сформулированы явно.
