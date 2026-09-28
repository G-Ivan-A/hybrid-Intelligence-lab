---
status: draft
version: 0.2
updated: 2026-09-28
temperature: 0.1
---

# Справочник: команды, процессы, папки и параметры

Назад: [тестовый прогон](04-smoke-test.md) · Далее: [работа с Cline](06-working-with-cline.md)

## Содержание

1. [Команды runner](#команды-runner)
2. [Отдельные машинные шаги](#отдельные-машинные-шаги)
3. [Процесс RG-BCREQ-v1](#процесс-rg-bcreq-v1)
4. [Параметры и папки](#параметры-и-папки)
5. [Чего в пилоте нет](#чего-в-пилоте-нет)

Все команды выполняются из корня пакета. На Windows пишите `python`,
на macOS/Linux — `python3`.

## Команды runner

Основная программа — `tools/run_task.py`. У неё **три** команды. Каждая
сначала проверяет целостность пакета.

| Команда | Что делает | Когда использовать | Успех |
|---------|------------|--------------------|-------|
| `python tools/run_task.py check-package` | Сверяет файлы пакета с `package-manifest.yaml` | После копирования пакета; при любых сомнениях | `package: PASS` |
| `python tools/run_task.py run TASK-ID submissions/TASK-ID.json` | Прогоняет черновик через три машинных шага, пишет `runs/TASK-ID/` | Каждый раз, когда черновик готов к проверке | `TASK-ID: PASS`, exit code 0 |
| `python tools/run_task.py verify-ci` | Проверяет эталон и **все** файлы в `submissions/` во временной папке — то же, что делает CI | Перед отправкой в Git | строки `…: PASS` для каждого файла |

Правила:

- TASK ID — `TASK-` и минимум четыре цифры: `TASK-0001`, `TASK-0042`.
- Один TASK ID — один прогон. Повторный `run` с тем же номером отклоняется,
  чтобы журнал нельзя было незаметно перезаписать.
- В `submissions/` допустимы только файлы `TASK-NNNN.json`; иначе
  `verify-ci` выдаст `unexpected submission`.

## Отдельные машинные шаги

`run` сам вызывает эти шаги из `tools/bcreq_pipeline.py`. Вручную они нужны
только для диагностики: **в trace ручной вызов не попадает**.

| Шаг | Команда | Проверяет |
|-----|---------|-----------|
| `validate-working` | `python tools/bcreq_pipeline.py validate-working submissions/TASK-ID.json` | Черновик соответствует схеме `contracts/c-working-bcreq.schema.json`, таксономии и связям FR/UC/NFR |
| `compile` | `python tools/bcreq_pipeline.py compile submissions/TASK-ID.json --output <папка>` | Собирает `release.json` и `release-manifest.json` |
| `validate-release` | `python tools/bcreq_pipeline.py validate-release submissions/TASK-ID.json --release <папка>/release.json --manifest <папка>/release-manifest.json` | Release соответствует черновику и схеме клиента |

Успех каждого шага — строка `G-mach: BCREQ accepted`; ошибки — строки
`ERROR: …`. Для отладки используйте папку вне `runs/`, чтобы не путать с
настоящими прогонами.

## Процесс RG-BCREQ-v1

В пилоте доступен **один** процесс — `RG-BCREQ-v1/synthetic-working-release`
(описание: `routes/pilot.json`).

```text
 Вы + Cline               Runner (G-mach)                       Вы (G-human)
 ─────────────            ───────────────────────────────────   ─────────────────
 submissions/TASK-ID.json → validate-working → compile → validate-release → проверка смысла,
 (Working)                                               (Release)          источников, публикации
```

- **Вход:** одобренный черновик BCREQ Working (JSON).
- **Выход:** BCREQ Release (`bcreq-client-v1`) и его manifest.
- **При ошибке машинного шага:** остальные шаги `step_skipped`, работа
  останавливается.
- **При отсутствии источника:** явная ошибка или открытый вопрос, но не догадка.
- **Человеческий gate `G-human`:** чек-лист `evaluation/g-human-checklist.md`.

## Параметры и папки

| Имя | Что это | Кто меняет |
|-----|---------|------------|
| `TASK-ID` | Номер задачи; аргумент команды `run`, имя файла в `submissions/` и папки в `runs/` | Вы выбираете свободный номер |
| `submissions/` | Черновики Working: `submissions/TASK-ID.json`. Единственное место, куда может писать Cline | Вы и Cline |
| `runs/` | Результаты прогонов: `runs/TASK-ID/trace.jsonl`, `release.json`, `release-manifest.json`. Не отправляется в Git | Только runner |
| `golden/` | Эталонный синтетический пример `TASK-0001.json` | Никто (только чтение) |
| `contracts/` | JSON-схемы Working и Release — «правила формата» | Никто (только чтение) |
| `taxonomy/` | Справочники продуктов Mango и TMF для продуктовой привязки | Никто (только чтение) |
| `docs/kb/` | Локальная база знаний (KB). Не отправляется в Git | Вы (копирование KB) |
| `meta-model/` | Место для разрешённых материалов мета-модели. Runner его не читает. Не отправляется в Git | Вы, по указанию ответственного |
| `routes/pilot.json` | Описание процесса | Никто |
| `templates/working-prompt.md` | Базовый запрос для Cline | Никто |
| `evaluation/g-human-checklist.md` | Ваш чек-лист проверки | Никто |
| `package-manifest.yaml` | Контрольные суммы всех неизменяемых файлов | Никто |

## Чего в пилоте нет

Честный список, чтобы не искать несуществующее:

- Нет других процессов, кроме `RG-BCREQ-v1/synthetic-working-release`.
  Полный граф узлов `n0…n13` есть только в пакете GigaCode.
- Нет переменных окружения: `TASK-ID` передаётся аргументом команды.
- Нет команд Cline вида `/skills`: работа идёт обычным диалогом.
- Корпоративное подключение Jira/Confluence **только на чтение** настраивает
  администратор в Cline MCP Servers; пока его нет — используется `docs/kb/`.
