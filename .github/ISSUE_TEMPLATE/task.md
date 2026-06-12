---
name: "Task"
about: "Structured task for implementation, documentation, tooling, or governance work."
title: "[scope] Краткое описание задачи"
labels: "tools, governance"
assignees: ""
status: canonical
version: 1.0
updated: 2026-06-12
temperature: 0.1
---

<!--
Для ИИ: если поле пустое, не генерируй значение. Работай в Structured mode по
умолчанию. Сохраняй traceability между контекстом, артефактами, изменениями,
проверками и PR.
-->

## Мета

- Labels: `scope` / `priority:P?`
- Milestone: `-`
- User Story / ФТ: `-`
- Linked Backlog: `-`
- Depends On: `-`
- Operating Mode: `Structured`

## Контекст

Опишите, почему задача нужна, какие решения уже приняты, какие источники нужно
прочитать и какие ограничения известны до старта.

## Проблема или история пользователя

Сформулируйте проблему, user story, функциональное требование или governance
gap, который должен быть закрыт.

## Артефакты

- [ ] Создать или изменить ...
- [ ] Обновить навигацию, карту артефактов или changelog, если меняется active
      artifact.
- [ ] Проверить ...

## Ограничения

- Не публиковать secrets, private data, credentials и несанитизированные
  production-промпты.
- Не менять unrelated files и не расширять структуру "на вырост".
- Если контекст противоречив или неполон, остановиться и запросить human
  guidance.

## Специфика AI-агентов

- Каждый запуск агента - новая сессия; нужный контекст должен быть в issue,
  PR, handover prompt или summary.
- Comments и CI после остановки сессии не отслеживаются автоматически.
- Comment + manual restart = итерация; merge = принято; close = отклонено или
  отменено.
- Агент не заполняет пустые поля выдуманными значениями.

## Готово, когда

- [ ] Изменения закрывают описанную проблему без unrelated scope.
- [ ] Новые или изменённые Markdown-артефакты имеют frontmatter
      `status`, `version`, `updated`, `temperature`.
- [ ] Navigation, standards links, artifact map и changelog обновлены там, где
      это нужно.
- [ ] Локальные проверки выполнены и указаны в PR.
- [ ] PR связан с issue и содержит implementation, validation и remaining risks.
