---
status: proposed
version: 0.1
updated: 2026-09-25
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
| Impacted artifacts | будущий `dist/execution-package-cline-vscode/`, отдельный runtime `mango-ba-ai-runtime-cline` |
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

## Decision Drivers

- Техническая пригодность: официальный [Cline provider guide](https://github.com/cline/cline/blob/main/docs/provider-config/openai-compatible.mdx) описывает прямую настройку OpenAI-compatible API, а [Cline README](https://github.com/cline/cline/blob/main/README.md) — shell и review диффов.
- При равной недетерминированности решения агента Cline даёт junior БА визуальную настройку модели, список файлов, diff, approval и терминал в одной среде. Это **вывод из описанного workflow**, который нужно проверить наблюдением junior на пилоте.
- [OpenCode](https://opencode.ai/docs/providers) также поддерживает custom OpenAI-compatible provider и [встроенный bash tool](https://opencode.ai/docs/tools/). Его [custom tools](https://opencode.ai/docs/custom-tools/) могут вызывать Python, но определены как tools, которые вызывает модель; это не доказывает обязательный вызов на каждом переходе. [V1/V2 схемы конфигурации](https://opencode.ai/v2/docs/providers) различаются; приложенная инструкция AI Core содержит разные JSON-примеры для них. Это повышает стоимость настройки пилота для junior, не добавляя доказанного обязательного вызова Python.
- Вне перечня команды Q рассмотрен [Continue для VS Code](https://docs.continue.dev/ide-extensions/agent/quick-start): он поддерживает [настраиваемый OpenAI-compatible endpoint](https://docs.continue.dev/customize/deep-dives/model-capabilities), но [модель также выбирает вызовы tools](https://docs.continue.dev/ide-extensions/agent/how-it-works). При той же границе детерминизма его настройка модели и возможностей добавляет шаги к первому пилоту; это предварительный UX-вывод, а не результат сравнительного испытания с junior.

## Alternatives Considered

| Клиент/подход | Проверка | Решение |
| --- | --- | --- |
| OpenCode | [Custom provider и Base URL](https://opencode.ai/docs/providers) поддерживаются; [bash и custom tools](https://opencode.ai/docs/custom-tools/) позволяют вызвать Python. Документация не обещает, что agent всегда вызовет конкретный скрипт и не изменит его; V1/V2 конфиг различается. | Отклонён для этого пилота по UX при равной границе детерминизма. Пересмотреть при доказанном обязательном hook/runner, отсутствующем у Cline. |
| Continue (VS Code) | [Agent mode](https://docs.continue.dev/ide-extensions/agent/how-it-works) и [OpenAI-compatible endpoint](https://docs.continue.dev/guides/how-to-self-host-a-model) подходят для пилота; обязательный вызов Python из поведения модели не следует. | Не выбран: сопоставимый IDE путь с дополнительной настройкой модели и capabilities; оценить отдельно, если Cline не пройдёт пилот. |
| Qwen Code | Приложенная инструкция даёт CLI-конфиг; требует терминала и отдельной настройки модели. Относится к другому клиенту и не упрощает шаги junior по сравнению с GUI Cline. | Не включать в пакет среды 2. |
| JetBrains AI Assistant | Возможность OpenAI-compatible заявлена в инструкции AI Core, но эквивалентный управляемый shell/route gate для этой задачи не доказан. | Не выбирать без отдельного runtime spike. |
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
