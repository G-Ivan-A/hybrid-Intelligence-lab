---
status: canonical
version: 1.0
updated: 2026-09-19
temperature: 0.1
---

# Синхронизировать `AGENTS.md` в {{project_name}}

Operating Mode: `Structured`

## Контекст

- Project repository: `{{project_url}}`
- Hub source commit: `{{hub_commit_sha}}`
- Причина синхронизации: `{{initial_delivery|hub_update|profile_update|drift}}`
- Локальный issue/PR: `{{project_issue_url}}`

## User Story

Как владелец `{{project_name}}`, я хочу получить актуальный и адаптированный
корневой `AGENTS.md`, чтобы агент следовал общим правилам экосистемы и реальным
контрактам проекта без дублирования и правил неиспользуемых сред.

## Что сделать

1. Прочитать issue/comments, README/concept, governance и `.hub-profile.json`.
2. Проверить наличие `AGENTS.md`; сравнить его по слоям с template объявленного
   archetype на `{{hub_commit_sha}}`.
3. Сохранить general layer; адаптировать profile, routes, artifact homes,
   validation и `<project_specific_rules>` только по активным контрактам.
4. Добавить только adapters объявленных сред; удалить дубли норм из adapters.
5. Запустить project validators и check-режим B-111; приложить delta report.

## Чего не делать

- не копировать Hub-файл без адаптации;
- не угадывать archetype/environment и project rules;
- не включать GigaCode без profile или Cursor/Copilot adapter без явного scope;
- не переписывать локальную работу и не ослаблять general layer;
- не хранить копии правил в model/environment-specific files.

## Готово, когда

- [ ] profile согласован с `<scope>`, placeholders отсутствуют;
- [ ] обязательные секции и general layer сохранены;
- [ ] каждый project-specific rule имеет локальный источник;
- [ ] adapters соответствуют объявленным средам и являются pointers;
- [ ] validators зелёные, повторный dry-run не показывает дельту;
- [ ] PR содержит upstream SHA, delta report, риски и вопросы;
- [ ] human review выполнен; автоматического merge нет.

## Не выполнено и вопросы

Если решение принадлежит владельцу, перечислить конфликт, варианты и
рекомендацию; выполнить независимую часть и оставить PR неполным по DoD.
