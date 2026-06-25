---
status: canonical
version: 1.6
updated: 2026-06-25
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
   [governance/repo-model.md](governance/repo-model.md),
   [governance/rfc/knowledge-lifecycle-proposal.md](governance/rfc/knowledge-lifecycle-proposal.md) и
   [governance/rfc/resolve-artifact-location-proposal.md](governance/rfc/resolve-artifact-location-proposal.md),
   если место артефакта не очевидно.
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

### Правило авто-заполнения Мета

Автор задачи может указать только цель и Operating Mode. AI-агент обязан
достроить рабочую Мета из активных контрактов:

| Что отсутствует | Как достраивается |
| --- | --- |
| Target artifact | По `governance/artifact-map.md`, `governance/repo-model.md` и resolver prompt. |
| Lifecycle stage | По `governance/rfc/knowledge-lifecycle-proposal.md`; сомнительный переход записывается как gap. |
| L1-L4 link | Product docs дают L1-L2, governance/standards/templates дают L3-L4. |
| Validation | Минимум: frontmatter, structure validator, manifest check when templates changed. |

Явная Мета в issue имеет приоритет, если она не нарушает hard rules. Если
правило нарушено, агент фиксирует конфликт и запрашивает guidance.

Historical migration material используется только как source context через
audit, PR history или явно указанный `source` path. Новый active artifact должен
показывать, откуда перенесено содержание и почему оно остается полезным.

### Консолидация открытых вопросов

При создании дайджеста сессии, если в ней есть открытые вопросы, Исполнитель
должен добавить их в [`governance/backlog.md`](governance/backlog.md), секция
«Открытые вопросы». Если вопрос уже есть в BACKLOG — не дублировать, добавить
ссылку на дайджест в колонку «Связанные дайджесты».

### Работа с внешними источниками

Полный свод правил — в
[research/external-knowledge/README.md](research/external-knowledge/README.md),
раздел «Правила работы с внешними источниками». Краткая выжимка:

- **Распознавание.** Метка `research`/«исследование» без ссылки = широкий поиск;
  конкретный URL = изучение именно этого источника.
- **Фиксация.** Факт изучения → в
  [реестр](research/external-knowledge/external-sources-registry.md) **ВСЕГДА**.
  Полезный вывод → инсайт в
  [external-insights/](research/external-knowledge/external-insights/). Если
  источник не полезен для текущей фазы, но содержит идеи для будущих фаз или
  смежных тем, он маркируется тегами `future-phase: X`, `topic: Y` (при
  необходимости `use-case: Z`) и сохраняется в БЗ как задел на будущее.
  Повторный анализ инициирует только Пользователь.
- **Отклонение.** Источники с явными признаками хайпа или воды (нет кода для
  проверки, нет метрик результата, только маркетинговые обещания) отклоняются
  полностью: только факт в реестре со статусом `rejected` и пометкой
  «отклонено», без инсайта.
- **Чистота.** Факты изучения внешних источников **НЕ** попадают в `CHANGELOG.md`
  проектов.
- **Traceability.** Автор/организация, дата и язык фиксируются всегда; лицензия —
  когда применима.

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

## File Naming

Новые и мигрируемые хронологические Markdown-артефакты используют date-first
имена по [standards/file-naming.md](standards/file-naming.md):
`YYYY-MM-name.md`, `YYYY-name.md` или `YYYY-MM-adr-NNN-name.md` для spoke ADR.
Проверяемые области: Hub `research/`, spoke `docs/analysis/`, `docs/rfc/` и
`docs/adr/`.

## Локальная проверка

```bash
./tools/validate-file-naming.sh
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
