---
status: draft
version: 0.1
updated: 2026-10-07
temperature: 0.1
description: Запечатать черновик и запустить проверку задачи — /bcreq-gate TASK-ID
agent: plan
---

Аналитик запечатал черновик и запустил машинную проверку G-mach. Вывод runner:

```text
!`python tools/opencode_command.py gate '$1'`
```

Ответь по-русски по пунктам:
1. Итог: строка `TASK-…: PASS` или `TASK-…: FAIL` из вывода. Если такой строки
   нет — проверка не состоялась; объясни почему.
2. Если `FAIL` или ошибка — каждую строку `ERROR: …` простыми словами.
3. Что делать дальше: при `PASS` — пройти чек-лист
   evaluation/g-human-checklist.md по runs/<TASK-ID>/release.json; при `FAIL` —
   убрать неудачный черновик и подготовить исправленный под новым TASK ID.
Не утверждай ничего сверх вывода runner. Ничего не запускай и файлы не меняй.
