---
name: "Task"
about: "Универсальный 5-блочный шаблон задачи: Structured, Creative или Hybrid."
title: "[scope] Краткое описание задачи"
labels: "tools, governance"
assignees: ""
status: canonical
version: 2.0
updated: 2026-08-11
temperature: 0.1
---

<!--
Для ИИ: пустое поле не заполняется выдуманным значением. Универсальные
контракты автономии, эскалации и верификации живут в
ai-rules/agent-work-rules.md и здесь не дублируются. Список файлов не
перечисляется: место артефакта разрешается на момент исполнения.
Источник шаблона: docs/rfc/2026-08-06-rfc-task-statement-architecture.md, §P.9.
-->

Operating Mode: `Structured / Creative / Hybrid` ·
Task Type (optional): `Research / Education / Implementation / Audit / Analysis / RFC / ADR` ·
User Story / ФТ / НФТ (optional): `-`

## Контекст

Зачем это делается, какие решения уже приняты, что НЕ входит в задачу.

## Цель

Какое состояние станет правдой после выполнения. Без описания реализации.

## SSOT

1–3 якоря: путь в репозитории, issue/PR или permalink с SHA. Якорь
разрешается на момент исполнения; неразрешимый якорь фиксируется как gap, а не
заменяется догадкой.

## Контракты задачи

Только отклонения от универсальных контрактов
[ai-rules/agent-work-rules.md](../../ai-rules/agent-work-rules.md)
(автономия / эскалация / верификация). Пусто = действуют универсальные.

## Готово, когда

3–5 пунктов, каждый проверяем.

- [ ] ...
- [ ] ...
- [ ] ...
