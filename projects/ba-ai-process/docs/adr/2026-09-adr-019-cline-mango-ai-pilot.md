---
status: proposed
version: 0.3
updated: 2026-09-26
temperature: 0.1
owner: G-Ivan-A
decision-type: runtime
---

# ADR-019: Cline в VS Code для пилота с Mango AI

## Decision Metadata

| Field | Value |
| --- | --- |
| ADR id | ADR-019 |
| Decision type | runtime |
| Decision status | proposed; выбор клиента утверждается владельцем при review PR |
| Decision date | 2026-09-25 (предложение) |
| Owner | G-Ivan-A |
| Source | [issue #615](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/615) и [параметры AI Core](https://github.com/user-attachments/files/32652321/default.txt) |
| Impacted artifacts | будущий `dist/execution-package-cline-vscode/`, отдельный runtime `mango-ba-ai-runtime-cline`; проектный контур проверки среды 4 |
| Supersedes | none; конкретизирует [ADR-017](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/decisions/2026-09-adr-017-ba-ai-process-source-distribution.md) |
| Superseded by | none |

## Context

Нужен один OpenAI-совместимый агент для БА от junior до expert с корпоративной моделью AI Core и проверяемым BCREQ. [Приложенная инструкция AI Core](https://github.com/user-attachments/files/32652321/default.txt) указывает OpenAI-compatible `/chat/completions`, `tool calls`, модельные ID `gpu-default` и `gpu-deep`, персональный ключ и HTTP endpoint, доступный только из корпоративной сети/VPN. Она описывает **API модели**. Она не задаёт MCP-серверы Jira/Confluence, их URL, transport, tool names или права. Утверждение «подключение к Mango AI API само даёт доступ к Jira/Confluence» не подтверждено этим источником.

[Документация Cline](https://github.com/cline/cline/blob/main/docs/provider-config/openai-compatible.mdx) подтверждает пользовательский путь через настройки `OpenAI Compatible`: Base URL, API Key, Model ID, контекст и output. [Cline](https://github.com/cline/cline/blob/main/README.md) умеет читать/изменять файлы и выполнять shell-команды в VS Code с показом diff и подтверждением операций. [Документация MCP](https://github.com/cline/cline/blob/main/docs/mcp/mcp-overview.mdx) требует отдельного подключения сервера и проверки доступных tools. Но [документация инструментов](https://github.com/cline/cline/blob/main/docs/tools-reference/all-cline-tools.mdx) прямо говорит: **модель выбирает**, какой tool вызвать. Следовательно, наличие `bash` и `tool calls` не гарантирует вызов Python-гейта на каждом шаге.

## Decision

Выбрать **Cline как расширение VS Code** и только его для среды 2. Отдельный runtime репозиторий рекомендуется назвать `G-Ivan-A/mango-ba-ai-runtime-cline`; не размещать его настройки и инструкции в GigaCode-пакете. Source модели и общий набор контрактов остаются в `projects/ba-ai-process/`; адаптер Cline компилирует отдельный `dist/execution-package-cline-vscode/` с собственным manifest и документацией для БА. Название — предлагаемый путь будущей реализации, репозиторий этим ADR не создаётся.

Детерминизм квалифицировать по уровням:

1. **Машинный:** отдельный локальный runner/CI сам вызывает валидатор и компилятор, проверяет exit code, граф и сохранённое состояние. Этот уровень может быть проверен воспроизводимым тестом.
2. **Агентный:** Cline получает правила, готовит черновик, предлагает вызовы tools и исправления. Его выбор и текстовый вывод вероятностны; `AGENTS.md` и Cline rules помогают, но не заменяют runner.
3. **Человеческий:** БА подтверждает продуктовую атрибуцию, источники, Working baseline и Release. Семантика и права на публикацию не выдаются из Python exit code.

В будущей поставке `AGENTS.md` — единственный основной контракт; необходимый для Cline `.clinerules` может быть только коротким проверяемым указателем на него и на явную команду runner. Навыки, нужные для Cline, компилируются в нативный формат без копии независимой нормы. Не допускать agent edit `tools/`, `contracts/`, `routes/` или manifest внутри бизнес-прогона: изменения в них проходят отдельный Source PR и recompilation. Исполнение валидатора производится под правами БА/CI, а не «чтением Python как контракта». CI обязан отвергать артефакт без успешного результата гейта.

Операторский маршрут для guide будущего Cline-пакета:

1. На разрешённом АРМ установить Git, VS Code, официальное расширение [Cline](https://github.com/cline/cline/blob/main/docs/getting-started/installing-cline.mdx), Python 3 и зависимости **зафиксированной** версии пакета. Достаточен компьютер, поддерживающий VS Code и Python; локальная GPU для удалённой модели не нужна. Junior БА должен уметь открыть папку в VS Code, выполнить готовую команду в терминале и прочесть PASS/FAIL; создание MCP-конфигурации и выдача прав — задача администратора.
2. Получить **свой** ключ в AI Core. Открыть Cline Settings → API Provider `OpenAI Compatible`; указать Base URL, выданный AI Core, модель `gpu-default`, персональный ключ, Context Window `114688`, Max Output Tokens `16384`, выключить image support. Для более длинного анализа `gpu-deep` имеет отдельные лимиты `98304`/`32768`; переключать после пилота. Эти значения взяты из [внутренней инструкции](https://github.com/user-attachments/files/32652321/default.txt), а не измерены в Cline. HTTP использовать лишь в корпоративной сети/VPN согласно той же инструкции; ключ не помещать в Git, чат или скриншот.
3. Создать/клонировать `mango-ba-ai-runtime-cline` в отдельную папку. Проверить package manifest, `python3 --version`, зависимости и команду gate из README пакета. Пакет должен содержать `AGENTS.md`, адаптер Cline, `contracts/`, `routes/`, `taxonomy/`, `templates/`, `evaluation/`, `golden/`, `tools/`, `meta-model/` и `docs/kb/`; `runs/` и секреты исключить из публичного Git. Не копировать `.gigacode/skills/` как якобы нативные Cline skills.
4. Администратор добавляет **отдельный** одобренный MCP для Jira/Confluence через Cline MCP Servers и проверяет `tools/list`/пробный read-only поиск по тестовой странице и issue. Пока MCP не выдан, BA работает только с разрешённой локальной KB, маркирует недоступный внешний источник как пробел и не утверждает непроверенную цитату. Model API key не подставлять в MCP как универсальный пароль.
5. В VS Code открыть runtime-папку, проверить отключённое автоодобрение опасных действий, дать Cline один `TASK-0001` с синтетическим/разрешённым входом, подтвердить `n0`, затем выполнять route через runner. После каждого шага БА видит узел, источник, команду/exit code гейта и Markdown checkpoint; при FAIL останавливается. Для Release отдельно требуются одобренный Working, `validate-working`, `compile`, `validate-release`, human review.

## Расширенное исследование среды 2 по review PR #616 (2026-09-26)

Проверены **23 именованных варианта**: пять из исходного перечня, пять из [нового комментария владельца](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/616#issuecomment-5844819799) и 13 вне обоих перечней. Для **21** первичный источник подтверждает собственное подключение к OpenAI-compatible endpoint; Raven подтверждает подключение *других агентов* через такой API, а для KiwiQ произвольный Mango AI base URL не подтверждён. Они сохранены в матрице как проверенные альтернативные гипотезы, но не засчитаны в 21. Наличие UI, self-hosting или Python само по себе не доказывает обязательный вызов BA gate. Метка `РФ ?` означает: наличие исходников/дистрибутива установлено, фактическая загрузка с целевого АРМ в России **не проверена**; по решению владельца это информационная метка, не фильтр.

Шкала проверки: **H** — клиентский блокирующий hook/plugin после выбора действия моделью; **W** — платформа может исполнить заранее построенный workflow независимо от выбора моделью tool; **T** — tool/скрипт вызывается моделью или человеком; **A** — автоматический тест после правки. Ни H, ни W без адаптера маршрута `A-IN → A-BCREQ` не означают готовую BA-гарантию. Наблюдаемость `E` — есть события/траектория выполнения; `L` — доступен общий лог/история; `?` — подтверждения нет. Ни один источник не показывает готовые поля `script_invoked` / `contract_mode` / `step_skipped` именно для нашей модели. Это требование продукта.

| Группа и клиент | OpenAI-compatible и подтверждённый механизм | Наблюдаемость; роль для БА | РФ |
| --- | --- | --- | --- |
| Исходный: **Cline** | [Base URL/API key/model](https://github.com/cline/cline/blob/main/docs/provider-config/openai-compatible.mdx); [H: PreToolUse/PostToolUse/TaskStart](https://cline.bot/blog/cline-v3-36-hooks), `cancel` блокирует выбранное действие. | E: hook JSON и UI; VS Code diff/approval, короткий путь junior. | ? |
| Исходный: **OpenCode** | [Custom provider](https://opencode.ai/docs/providers); [H: `tool.execute.before/after`](https://opencode.ai/docs/plugins/), нужен JS/TS plugin. | E: события plugin; CLI/TUI, нужна настройка. | ? |
| Исходный: **Continue** | [Custom provider](https://docs.continue.dev/customize/model-providers/top-level/openai); [T: agent tool calls](https://docs.continue.dev/ide-extensions/agent/how-it-works). | L: IDE history; нет подтверждённого обязательного BA gate. | ? |
| Исходный: **Qwen Code** | [OpenAI-compatible custom provider](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/auth/); [H: PreToolUse/Stop](https://qwenlm.github.io/qwen-code-docs/en/users/features/hooks/) может блокировать действие/завершение. | E: hook events; CLI сложнее для junior. | ? |
| Исходный: **JetBrains AI Assistant** | [OpenAI-compatible provider, URL и tool-calling flag](https://www.jetbrains.com/help/ai-assistant/settings-reference-providers-and-api-keys.html); T, BA hook не подтверждён. | L: IDE; требуется лицензия/корпоративная проверка. | ? |
| Команда D: **Raven** | [WebUI и подключение сторонних агентов через OpenAI-compatible API](https://github.com/EverMind-AI/Raven); прямой Mango AI model endpoint не подтверждён. | L: WebUI, sandbox; требует отдельного агентного adapter. | ? |
| Команда D: **Nanobot** | [OpenAI-compatible модели, WebUI, Python SDK и tools](https://github.com/HKUDS/nanobot); T, обязательный маршрут потребует собственного кода. | L: история/WebUI; BA workflow пришлось бы разработать. | ? |
| Команда D: **Bernstein** | [Custom OpenAI-compatible base URL](https://bernstein.readthedocs.io/en/latest/operations/self-hosted-endpoints/); [W: deterministic Python scheduler](https://github.com/sipyourdrink-ltd/bernstein/blob/main/docs/architecture/WHY_DETERMINISTIC.md). | [E: operator GUI/audit](https://github.com/sipyourdrink-ltd/bernstein/blob/main/docs/gui/index.md); сильный контроль, но BA-план и adapter ещё нужны. | ? |
| Команда D: **CUGA** | [OPENAI_BASE_URL, web/API agent, trajectory visualizer](https://github.com/cuga-project/cuga-agent); T, обязательный маршрут потребует отдельной оркестрации. | E: trajectory; enterprise setup требует администратора. | ? |
| Команда D: **KiwiQ** | [UI/API, Prefect workflow и observability](https://github.com/rcortx/kiwiq); документация показывает `OPENAI_API_KEY`, но не произвольный model base URL. | E: Prefect/логи; интеграция Mango AI остаётся gap. | ? |
| Дополнительный 1: **Aider** | [Custom endpoint](https://aider.chat/docs/llms/openai-compat.html); [A: `--auto-test`](https://aider.chat/docs/usage/lint-test.html) после правки, не перед BA-переходом. | L: terminal/test output. | ? |
| Дополнительный 2: **Kilo Code** | [Custom OpenAI-compatible provider](https://kilo.ai/docs/code-with-ai/agents/custom-models); [H: `tool.execute.before/after`, `session.idle`](https://kilo.ai/docs/automate/extending/plugins). | E: plugin events; **VS Code GUI**, реальный конкурент Cline. | ? |
| Дополнительный 3: **Roo Code** | [OpenAI-compatible provider и native tool calls](https://github.com/RooCodeInc/Roo-Code/blob/main/apps/docs/docs/providers/openai-compatible.md); T, BA hook не подтверждён. | L: tool timeline/IDE diff; GUI. | ? |
| Дополнительный 4: **Goose** | [OpenAI provider с custom `OPENAI_HOST`](https://github.com/aaif-goose/goose/blob/main/documentation/docs/getting-started/providers.md); T через extensions. | L: desktop/CLI history; маршрут требует adapter. | ? |
| Дополнительный 5: **OpenHands** | [UI с custom OpenAI base URL/model](https://docs.openhands.dev/usage/llms/groq); T: agent в sandbox, BA gate отдельно. | L: agent events/UI; серверный запуск сложнее IDE. | ? |
| Дополнительный 6: **gptme** | [OpenAI-compatible `OPENAI_BASE_URL`](https://gptme.org/docs/providers.html); T/собственные Python tools. | L: CLI history; настройка для разработчика. | ? |
| Дополнительный 7: **Plandex** | [Custom provider с OpenAI-compatible `baseUrl`](https://docs.plandex.ai/models/custom-models/); T: план и применение требуют BA adapter. | L: план/CLI; дополнительный операторский слой. | ? |
| Дополнительный 8: **Flowise** | [Custom OpenAI base path](https://docs.flowiseai.com/integrations/langchain/chat-models/azure-chatopenai); [W: Agentflow V2](https://docs.flowiseai.com/using-flowise/agentflowv2) может явно связать validation nodes. | E: flow state/UI; проектирование workflow администратором. | ? |
| Дополнительный 9: **Dify** | [OpenAI-compatible model plugin с endpoint URL](https://github.com/langgenius/dify-official-plugins/blob/main/models/openai_api_compatible/provider/openai_api_compatible.yaml); [W: workflow nodes](https://docs.dify.ai/en/guides/application-orchestrate/creating-an-application). | E: workflow runs/UI; потребует BA-specific bridge к Git и gate. | ? |
| Дополнительный 10: **Open WebUI** | [Custom OpenAI-compatible connection](https://docs.openwebui.com/getting-started/quick-start/connect-a-provider/starting-with-openai-compatible/); [Pipe function](https://docs.openwebui.com/getting-started/quick-start/connect-a-provider/starting-with-functions/) может завернуть свой runner. | L: chat/UI; [MCP tool выбирает модель](https://docs.openwebui.com/features/extensibility/mcp/). | ? |
| Дополнительный 11: **LibreChat** | [Custom OpenAI-compatible endpoint](https://www.librechat.ai/docs/compatibility); [agent tools](https://www.librechat.ai/docs/features/agents) — T. | L: web chat; BA repo/gate отдельно. | ? |
| Дополнительный 12: **Cherry Studio** | [Custom OpenAI provider/base URL](https://docs.cherry-ai.com/cherry-studio-wen-dang/en-us/pre-basic/providers/zi-ding-yi-fu-wu-shang); T через chat/MCP. | L: desktop chat, простой вход; нет repo gate. | ? |
| Дополнительный 13: **AnythingLLM** | [Generic OpenAI model provider](https://docs.useanything.com/setup/llm-configuration/cloud/openai-generic); [T: agent flow вызывается из чата](https://docs.useanything.com/agent-flows/overview). | L: web/desktop chat; BA repo/gate отдельно. | ? |

**Фальсификация альтернативы «все платформы — только external runner».** Raven, Nanobot, Bernstein, CUGA и KiwiQ имеют собственные интерфейсы или операторские поверхности, поэтому могут выступать клиентом для БА после настройки; предыдущая групповая классификация была ошибкой. Однако у Bernstein GUI служит прежде всего наблюдению/approval, а у KiwiQ не подтверждён нужный endpoint. Flowise и Dify тоже могут дать порядок вызова через workflow. Для всех платформ нужно отдельно реализовать узлы BA, файловый доступ, `G-mach`, проверку exit code и безопасный доступ к корпоративной KB. Готовой BA-гарантии источники не показали.

**Решение для среды 2:** сохранить **Cline** для быстрого пилота в репозитории. Он уже имеет прямой OpenAI-compatible setup, доступ к файлам/Git через VS Code и hook events; Kilo сопоставим по GUI и plugin events, поэтому прежнее утверждение об уникальности Cline снято. Kilo требует собственного JS/TS plugin, Cline — скриптов hooks, но **ни один** не запускает нужный BA route по умолчанию. Cline выигрывает не абсолютной гарантией, а меньшим объёмом новой интеграции с текущим Git-пакетом. Это проектная оценка, не испытание junior; на пилоте сравнить один synthetic BCREQ в Cline и Kilo по настройке, обязательности gate и trace. Если Kilo даст более надёжный контроль при равном времени настройки, вернуться к выбору новым ADR. Доступность загрузки в России проверить с целевого АРМ до пилота; недоказанная доступность не изменила рейтинг.

Клиентский hook может проверить выбранный вызов и зафиксировать событие, но не доказывает, что модель предложит нужный вызов или что пользователь не завершит/обойдёт hook. [Документация Cline](https://github.com/cline/cline/blob/main/.clinerules/hooks/README.md) помечает `TaskComplete` как *coming soon*, поэтому нельзя строить Release barrier на нём. Защитить `runs/<TASK_ID>/` и Release должен отдельный runner/CI с проверкой exit code и provenance. Поддержка hooks в Windows зависит от версии: [анонс v3.36](https://cline.bot/blog/cline-v3-36-hooks) ограничивал её macOS/Linux; целевую версию/ОС нужно проверить на АРМ, не считать WSL универсальным требованием.

**Наблюдаемость продукта:** на каждый запланированный узел/попытку нужен trace из [ADR-018](2026-09-adr-018-gigacode-cli-execution-boundary.md#схема-наблюдаемости-шага): ровно одно состояние `script_invoked`, `contract_mode` или `step_skipped`, плюс `recorded_by`, TASK ID, route/node, package hash, время, command/gate ID, exit code, input/output hash и actor. Hook/client может дать исходные события, но только product runner/CI создаёт авторитетную запись `script_invoked` по реально выполненному процессу и находит отсутствующий узел по ожидаемому графу. `contract_mode` означает явно разрешённый ручной переход и не засчитывается как машинный gate; `step_skipped` блокирует продвижение. Доля детерминированных шагов считается по успешным авторитетным `script_invoked` среди всех ожидаемых шагов; отдельно выводить долю missing trace, чтобы исчезновение лога не улучшало метрику.

## Среда 4: контролируемая машинная проверка на уровне продукта

**Рекомендация:** проектный runner с конечным автоматом BA-маршрута, вызываемый вне модельного tool loop, а для Release — обязательный CI gate runtime-репозитория. Это четвёртый *контур исполнения и проверки*, совместимый с клиентами сред 1/2, а не четвёртый конкурирующий чат. Runner читает подписанный/хешированный package manifest и route, сам выбирает следующий допустимый узел, запускает Python validator/compiler, проверяет exit code и схему выхода, атомарно пишет checkpoint и JSONL trace, запрещает переход без `G-mach` и ожидает явное подтверждение БА для `G-human`. CI независимо воспроизводит проверку кандидата и отклоняет отсутствующий/изменённый trace, skipped gate, изменённый пакет и Release без human approval. Нужны негативные тесты на каждый из этих обходов.

Для быстрого пилота достаточно локального `tools/run-task` плюс CI защищённой ветки; контролируемый VPS уместен лишь когда централизованные права, журнал и доступ к Jira/Confluence оправдают эксплуатационные затраты и будут одобрены корпоративным владельцем инфраструктуры. MCP можно сделать интерфейсом к runner для Cline/GigaCode, **но не единственным триггером**: вызов MCP-tool выбирает модель. Отдельный собственный MCP *протокол* не нужен; стандартный MCP transport передаёт вызов, продуктовый runner определяет порядок и результат. Flowise/Dify/Bernstein дают готовую оболочку и планировщик, но BA graph, contracts, gates и trace всё равно пришлось бы написать и закрепить в Source, а настройка платформы добавила бы второй операторский контур. Поэтому узкий runner + CI минимальнее и переносим между средами. Среда 4 предлагается как следующая отдельная задача, не объявляется реализованной этим ADR.

## Decision Drivers

- Техническая пригодность: официальный [Cline provider guide](https://github.com/cline/cline/blob/main/docs/provider-config/openai-compatible.mdx) описывает прямую настройку OpenAI-compatible API, а [Cline README](https://github.com/cline/cline/blob/main/README.md) — shell и review диффов.
- Приоритет выбора — возможность проверить вызов gate и зафиксировать наблюдаемый результат. У Cline и Kilo есть blocking hooks/plugins, но они не создают обязательный BA-маршрут; решающий уровень остаётся у продуктового runner/CI. Поэтому клиент выбирается по цене интеграции с Git-пакетом; UX junior — вторичный критерий и отдельная проверка пилота.
- [OpenCode](https://opencode.ai/docs/providers) поддерживает custom OpenAI-compatible provider и [блокирующий plugin hook](https://opencode.ai/docs/plugins/). Это сравнимый механизм H; он не запускает пропущенный моделью BA-шаг. [V1/V2 схемы конфигурации](https://opencode.ai/v2/docs/providers) различаются; приложенная инструкция AI Core содержит разные JSON-примеры для них. Требуется собственный JS/TS plugin и настройка CLI/TUI.
- [Continue для VS Code](https://docs.continue.dev/ide-extensions/agent/quick-start) поддерживает [настраиваемый OpenAI-compatible endpoint](https://docs.continue.dev/customize/model-providers/top-level/openai), но [модель выбирает вызовы tools](https://docs.continue.dev/ide-extensions/agent/how-it-works). При той же границе детерминизма его настройка модели и возможностей добавляет шаги к первому пилоту; это предварительный вывод, а не результат сравнительного испытания.

## Alternatives Considered

| Клиент/подход | Проверка | Решение |
| --- | --- | --- |
| OpenCode | [Custom provider и Base URL](https://opencode.ai/docs/providers) поддерживаются; [блокирующий plugin hook](https://opencode.ai/docs/plugins/) контролирует выбранный вызов. Документация не обещает, что агент сам инициирует каждый BA-шаг; V1/V2 конфиг различается. | Для текущего пилота потребуется новый JS/TS plugin и настройка CLI/TUI. Пересмотреть при сравнительном испытании с меньшей ценой интеграции или лучшим контролем. |
| Continue (VS Code) | [Agent mode](https://docs.continue.dev/ide-extensions/agent/how-it-works) и [OpenAI-compatible endpoint](https://docs.continue.dev/guides/how-to-self-host-a-model) подходят для пилота; обязательный вызов Python из поведения модели не следует. | Не выбран: сопоставимый IDE путь с дополнительной настройкой модели и capabilities; оценить отдельно, если Cline не пройдёт пилот. |
| Qwen Code | Приложенная инструкция даёт CLI-конфиг; требует терминала и отдельной настройки модели. Относится к другому клиенту и не упрощает шаги junior по сравнению с GUI Cline. | Не включать в пакет среды 2. |
| JetBrains AI Assistant | Возможность OpenAI-compatible заявлена в инструкции AI Core, но эквивалентный управляемый shell/route gate для этой задачи не доказан. | Не выбирать без отдельного runtime spike. |
| Kilo Code | [Custom provider](https://kilo.ai/docs/code-with-ai/agents/custom-models) и [plugin hooks](https://kilo.ai/docs/automate/extending/plugins) дают GUI и контроль выбранного tool. | Ближайший конкурент Cline; сравнить синтетический BCREQ и trace в пилоте. |
| Bernstein, Flowise, Dify | Workflow/scheduler может запускать узлы по плану. | Возможные оболочки среды 4; каждый требует BA adapter, gates и операционной настройки. |
| Только Cline rules + Python-код как текст | Инструкции агенту и чтение кода не создают обязательный exit code. | Отклонён как способ обеспечить машинный гейт. |

## Consequences

Выбор клиента однозначен, но интеграция **не считается проверенной** до пилота с выданным ключом и корпоративным MCP. Нужны отдельная сборка Cline-пакета, фиксированные версии VS Code/Cline/Python/модели, операторский guide без настройки других клиентов, сгенерированный и проверяемый указатель `.clinerules`, runner и CI с отрицательными тестами. Пилот должен проверить 401/отозванный ключ, недоступную сеть, отсутствие tool calls, недоступный MCP, пропуск gate, изменённый script, reject и возобновление TASK после новой сессии.

Ключевой открытый вход — контракт MCP (адрес/transport, tool names, права, тестовые Jira/Confluence ресурсы и кто их выдаёт). Без него можно проверить локальную работу и API модели, но нельзя заявить корпоративную KB интеграцию. Сохранять локальную `docs/kb/` и внешнюю KB как **дополняющие** каналы с human source confirmation согласно действующему [контракту пакета](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/dist/execution-package-gigacode-cli/AGENTS.md); не превращать их в скрытый fallback.

## Compliance and Validation

Проверить подключение Cline на тестовом prompt с `gpu-default` и отдельным tool call; зафиксировать версию клиента и модель. Отдельно проверить read-only MCP вызов по тестовому ресурсу. В будущей сборке runner и CI должны запускать те же негативные gate tests, что Source, плюс тест, где агент не зовёт Python: CI всё равно отклоняет невалидный результат. Оценка UX: junior без помощи разработчика проходит установку, настройку модели, открытие runtime, тестовый прогон и чтение отказа; число ошибок и запросов помощи записывается, порог утверждает владелец до пилота.

## Lifecycle

Предложение ожидает merge-решения владельца. Пересматривать при изменении API AI Core, корпоративной политики HTTP/VPN, документации клиентов или измеренном UX. Замена выбора оформляется новым ADR, принятый текст не переписывается.

## Related Artifacts

- [ADR-018: GigaCode CLI](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/issue-615-ab7082802ba9/projects/ba-ai-process/docs/adr/2026-09-adr-018-gigacode-cli-execution-boundary.md)
- [Инструкция AI Core](https://github.com/user-attachments/files/32652321/default.txt)
- [Cline OpenAI Compatible](https://github.com/cline/cline/blob/main/docs/provider-config/openai-compatible.mdx), [Tools](https://github.com/cline/cline/blob/main/docs/tools-reference/all-cline-tools.mdx), [MCP](https://github.com/cline/cline/blob/main/docs/mcp/mcp-overview.mdx)
- [OpenCode providers V1](https://opencode.ai/docs/providers) и [V2](https://opencode.ai/v2/docs/providers)
- [Continue Agent mode](https://docs.continue.dev/ide-extensions/agent/how-it-works) и [model capabilities](https://docs.continue.dev/customize/deep-dives/model-capabilities)
- [ADR Structure Standard](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/adr-structure-standard.md)
