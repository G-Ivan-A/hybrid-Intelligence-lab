---
status: proposed
version: 0.1
updated: 2026-09-25
temperature: 0.1
owner: G-Ivan-A
decision-type: runtime
---

# ADR-018: Граница детерминированного исполнения в GigaCode CLI

## Decision Metadata

| Field | Value |
| --- | --- |
| ADR id | ADR-018 |
| Decision type | runtime |
| Decision status | proposed; решение принимает владелец при review PR |
| Decision date | 2026-09-25 (предложение) |
| Owner | G-Ivan-A |
| Source | [issue #615](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/615), [комментарий команды D](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/615#issuecomment-5832987604) |
| Impacted artifacts | `projects/ba-ai-process/dist/execution-package-gigacode-cli/`; будущий runtime `G-Ivan-A/mango-ba-ai-runtime-cli` |
| Supersedes | none; уточняет [ADR-017](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/decisions/2026-09-adr-017-ba-ai-process-source-distribution.md) для одной среды |
| Superseded by | none |

## Context

Цель пользователя — повторяемый запуск `A-IN → A-CORE → A-BCREQ` на АРМ БА. Существующий [пакет](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/projects/ba-ai-process/dist/execution-package-gigacode-cli) содержит граф, dispatcher skill, JSON Schema, Python-валидатор и детерминированный компилятор Working → Release. Его [dispatcher](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/dist/execution-package-gigacode-cli/.gigacode/skills/rg-bcreq-v1-dispatcher/SKILL.md) описывает вычисление следующего узла **текстом для агента** и требует `python3 tools/validate-package.py` на preflight. [README пакета](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/dist/execution-package-gigacode-cli/README.md) предлагает команды валидатора и компилятора. Исполняемого контроллера, который сам читает `routes/rg-bcreq-v1.yaml`, вызывает Python на каждом переходе и блокирует следующий узел по exit code, в пакете нет. Поэтому успешный тест Python-функции доказывает поведение функции **при вызове**, но не факт её вызова агентом.

По [официальной документации GigaCode CLI](https://gitverse.ru/docs/ai/ai-assistant-gigacode/gigacode-cli/skills) проектные skills обнаруживаются в `.gigacode/skills/`, вызываются через `/skills`, а автоматическое применение зависит от контекста. [Команды CLI](https://gitverse.ru/docs/ai/ai-assistant-gigacode/gigacode-cli/commands) позволяют запускать shell через `!` и смотреть `/tools` и `/mcp`. Это доказывает возможность **локального** запуска Python при наличии интерпретатора и разрешения, но не обязательный запуск по графу. Гипотеза команды Q из [приложенного диалога](https://github.com/user-attachments/files/32652327/-.Q.250926.txt) о том, что Tool Calling сам превращает описание шага в обязательный вызов, не следует из документации или кода пакета.

## Decision

Сохранять GigaCode CLI как **отдельную** среду с собственным пакетом и без API Mango AI. Рабочая станция БА запускает GigaCode CLI и локальный Python; разрешённый Confluence MCP подключается через локальную конфигурацию CLI. Не объявлять skill или граф исполнительным механизмом, пока запуск каждого перехода и гейта не вынесен в исполняемый контроллер и не проверен на реальном CLI.

Для следующей версии `execution-package-gigacode-cli` в Source спроектировать один командный вход `tools/run-task` (точное имя закрепит реализация): он читает сохранённый `TASK_ID` и граф, выбирает ровно одно допустимое ребро, запускает gate как отдельный процесс, проверяет exit code и фиксирует результат. Агент готовит содержимое узла; контроллер владеет переходом. Human gates требуют явного ответа БА и не обходятся командой CLI. `G-mach` остаётся исполняемым Python, а `G-semantic` и `G-human` остаются отдельными проверками. Fail-closed означает остановку на ошибке, отсутствие автоматической корректирующей попытки и запрет Release до утверждения Working baseline.

До реализации контроллера действующий пакет используется как **ручной пилот**: БА явно запускает `/skills rg-bcreq-v1-dispatcher`, затем утверждает каждую команду проверки и смотрит её exit code; это не квалифицируется как доказанный детерминированный end-to-end прогон. Чтение Python как текста не выполняет JSON Schema, не даёт exit code и не заменяет `G-mach`.

Граница пакета и репозитория: Source остаётся в `projects/ba-ai-process/`, Distribution — в `dist/execution-package-gigacode-cli/`, GigaCode runtime — в уже существующем [`G-Ivan-A/mango-ba-ai-runtime-cli`](https://github.com/G-Ivan-A/mango-ba-ai-runtime-cli). Не копировать в него инструкции другого клиента. После компиляции копировать **весь** пакет, включая `.gigacode/skills/`, `AGENTS.md`, `contracts/`, `routes/`, `taxonomy/`, `templates/`, `evaluation/`, `golden/`, `tools/` и manifest; `meta-model/` и `docs/kb/` наполнять только разрешёнными локальными материалами. Реальная `.gigacode/settings.json`, ключи и бизнес-прогоны остаются вне публичного Git.

Минимальный операторский маршрут для будущего guide пакета:

1. На разрешённом АРМ установить GigaCode CLI по [официальному quick start](https://gitverse.ru/docs/ai/ai-assistant-gigacode/getting-started-with-gigacode/quick-start), Git и Python 3 с зависимостями, указанными **зафиксированной версией** пакета; подтвердить `gigacode --version`, `python3 --version` и доступ к корпоративной сети. Локальная GPU не требуется при использовании удалённой модели; поддержку ОС и конкретную версию Python подтвердить при пилоте, а не угадывать.
2. Клонировать runtime в отдельный каталог задачи, сверить manifest и выполнить `sh tools/validate-package.sh`. Заполнить `meta-model/` и `docs/kb/` с учётом лицензий и доступа.
3. Создать локальную `.gigacode/settings.json` из example только после выдачи корпоративным администратором адреса, транспорта и credentials одобренного Confluence MCP. Проверить `/mcp` и `/tools`; наличие подключения не доказывает право чтения конкретной страницы.
4. Вызвать `/skills rg-bcreq-v1-dispatcher` с `TASK-0001`, пройти `n0` и сохранить подтверждение БА. На каждом узле видеть фактическую команду `G-mach`, exit code, путь результата и checkpoint. При reject остановиться. Для `n12` проверить утверждённый Working, для `n13` отдельно выполнить `validate-working`, `compile`, `validate-release` и просмотреть Release человеком.

## Decision Drivers

- Принцип [ADR-017](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/decisions/2026-09-adr-017-ba-ai-process-source-distribution.md): runtime автономен от Source, Distribution версионируется и проверяется.
- Приоритет пользователя: доказанное исполнение маршрута и гейтов, затем удобство джуна БА.
- Возможность shell в CLI подтверждена [документацией](https://gitverse.ru/docs/ai/ai-assistant-gigacode/gigacode-cli/commands); гарантированный порядок вызовов этой возможностью не подтверждён.
- Комментарий команды D верно различает вызов скрипта и результат скрипта, но предложение заменить исполняемый Python «чтением как контракт» не удовлетворяет детерминизму.

## Alternatives Considered

| Вариант | Проверка и вывод |
| --- | --- |
| Только текстовый dispatcher и автоматический выбор skills | Существующий маршрут уже так устроен; нет механического принуждения к вызову Python и переходу. Недостаточно. |
| Python читается агентом как контракт | Убирает локальный runtime, но теряет реальную проверку данных и exit code. Допустимо лишь как подсказка в чате, не как gate. |
| Python только на VPS/MCP | Добавляет инфраструктуру и точку отказа; нет подтверждённого сервера или решения о его эксплуатации. Не нужен для локального CLI при доступном Python. |
| Контроллер плюс локальный CLI | Выбранное направление: формальная проверка перехода и gate вне вероятностного выбора модели; требует отдельной реализации и испытания. |

## Consequences

Этот ADR **не сертифицирует** текущий пакет как детерминированный. Следующая задача должна создать контроллер, человекочитаемый guide для джуна и runtime smoke test на рабочей станции с выключенным доступом к Source. Выходом теста служат реальные trace: версия CLI/Python/пакета, `TASK_ID`, вызванный узел, команда, exit code, human checkpoint и digest результата. Негативные прогоны обязаны показать отказ при пропуске gate, ошибке Python, ложном `gate_passed` и изменённом маршруте. Только после этого можно утверждать детерминированность **машинных переходов и проверок**; смысл BCREQ и качество источников всё равно требуют human review.

Неизвестные для точного deployment guide параметры Confluence MCP — сервер, транспорт, список tools, политика доступа и тестовый документ. Их выдаёт владелец инфраструктуры; придумывать конфигурацию или обещать Jira-доступ нельзя.

## Compliance and Validation

На Source проверять комплектность пакета и негативные кейсы через `tools/test-execution-package.sh`, `tools/validate-package.sh`, тесты `bcreq_pipeline.py`. На runtime проводить pilot smoke с искусственным `TASK_ID`, фиксировать лог фактических команд и преднамеренно повреждать вход, gate и переход. CI runtime должен запускать gate **сам**, а не просить агента запустить его. До такого теста статус «частично проверено».

## Lifecycle

Предложение действует после решения владельца при merge. Пересмотр нужен при появлении официального механизма обязательных хуков GigaCode CLI или доказательства, что локальный контроллер не может запускаться на целевом АРМ. Новая версия решения не переписывает принятый ADR.

## Related Artifacts

- [Пакет GigaCode CLI](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/projects/ba-ai-process/dist/execution-package-gigacode-cli)
- [RFC deployment CLI](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-mango-ba-ai-runtime-cli-deployment.md)
- [Официальные GigaCode CLI skills](https://gitverse.ru/docs/ai/ai-assistant-gigacode/gigacode-cli/skills) и [команды](https://gitverse.ru/docs/ai/ai-assistant-gigacode/gigacode-cli/commands)
- [ADR Structure Standard](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/adr-structure-standard.md)
