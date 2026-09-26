---
status: draft
version: 1.2
updated: 2026-09-25
temperature: 0.1
---

# Руководства по использованию BA meta-model

Модуль объясняет человеку, как подготовить и использовать скомпилированную
модель. Нормативные правила остаются в `ba-meta-model/`, а исполняемые — в
`dist/execution-package-gigacode-cli/`; здесь нет их второй копии.

Для отдельной задачи на временный сценарий Qwen Chat в существующем runtime
подготовлен [мандат модернизации](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/issue-615-ab7082802ba9/projects/ba-ai-process/meta-model-guides/qwen-chat-runtime-migration-instruction.md).
Это Source-инструкция для будущего PR, а не готовый execution package.

## Подготовка чистой рабочей директории

1. Убедиться, что локально доступна корпоративно установленная GigaCode CLI:
   `gigacode --version`.
2. Скопировать содержимое `dist/execution-package-gigacode-cli/` в чистую рабочую
   директорию. Не смешивать её с внешним runtime-репозиторием: issue #593
   реализует пакет в Source
   [`G-Ivan-A/hybrid-Intelligence-lab`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab).
3. Скопировать утверждённый срез `ba-meta-model/` в placeholder `meta-model/`
   рабочей директории, сохраняя структуру. Добавить разрешённые локальные
   материалы продукта в `docs/kb/`.
4. Установить PyYAML в локальное окружение и выполнить
   `sh tools/validate-package.sh`. Красный гейт останавливает подготовку.

## Подключение Confluence

1. Скопировать `.gigacode/settings.example.json` в локальный
   `.gigacode/settings.json`.
2. Подставить только одобренную команду корпоративного MCP и allowlist tools.
   Реальный URL и token передавать через окружение; файл settings уже исключён
   из Git.
3. В CLI проверить подключение командой `/mcp`. Локальная `docs/kb/` и
   Confluence дополняют друг друга; отсутствие результата в одном канале не
   делает второй единственным источником истины.
4. До использования цитаты подтвердить в human checkpoint её заголовок,
   раздел, страницу или anchor, точную цитату и locator.

## Новый и продолжаемый task

1. Запустить GigaCode из корня рабочей директории.
2. Явно вызвать `/skills rg-bcreq-v1-dispatcher` и передать новый
   `TASK-NNNN`. Не вызывать навыки узлов напрямую: порядок принадлежит графу.
3. Читать пользовательский результат в `runs/<TASK_ID>/A-BCREQ.md`, а запросы
   решения — в `runs/<TASK_ID>/evidence/*.md`. YAML под `runs/.../runs/` —
   машинный журнал микро-событий; пользователь не обязан его редактировать.
4. После смены сессии снова вызвать dispatcher с тем же `TASK_ID`. `/resume`
   удобен, но источником состояния остаются файлы task, а не история чата.
5. При reject решить вопрос явно. Dispatcher не делает скрытую исправляющую
   попытку. Внешняя публикация и promotion в Golden Set также требуют
   отдельного человеческого решения.

## Безопасная диагностика

Для mock-проверки вызвать `/skills ba-debug-orchestrator`. Он создаёт новый
`runs/DEBUG-<UTC-TIMESTAMP>/`, не вызывает LLM, MCP или внешнюю запись и не
изменяет `runs/TASK-NNNN/`. Отчёт `DEBUG-REPORT.md` можно приложить к задаче о
дефекте механизма; debug run не становится production evidence автоматически.

## Визуальный гайд

Автономная версия для чтения в браузере:
[`gigacode-cli/mango-ba-ai-runtime-cli-user-guide.html`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/meta-model-guides/gigacode-cli/mango-ba-ai-runtime-cli-user-guide.html).
Она служит обзором; актуальные команды и границы выше имеют приоритет в рамках
issue #593.
