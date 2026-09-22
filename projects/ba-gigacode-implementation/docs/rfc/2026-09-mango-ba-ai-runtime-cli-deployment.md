---
status: proposed
version: 0.2
updated: 2026-09-21
temperature: 0.1
owner: G-Ivan-A
rfc-scope: C
---

# RFC: развёртывание MVP BCREQ в GigaCode CLI

## RFC Metadata

| Поле | Значение |
| --- | --- |
| Owner | G-Ivan-A |
| RFC status | `proposed`; принятие только решением человека |
| Source issue | [#591](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/591); implementation boundary and source correction: [#593](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/593) |
| Impacted artifacts | Hub RFC/guide/navigation/registry; после принятия — отдельный runtime PR |
| Decision record | Not yet — human acceptance pending |
| Implementation link | Hub package: [PR #594](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/594); внешний runtime не изменяется |
| Archetype scope | `C` — Product Spoke / Runtime |
| Целевой репозиторий | [`mango-ba-ai-runtime-cli`](https://github.com/G-Ivan-A/mango-ba-ai-runtime-cli) |
| Маршрут | `RG-BCREQ-v1` |
| Целевая среда | GigaCode CLI на локальной рабочей станции |
| Решение | Требует принятия человеком; этот RFC не меняет runtime |
| Источники | `ext-323`, официальная документация GigaCode CLI, проверена 2026-09-21 |

## Summary

Предлагается разворачивать MVP как **явно вызываемый project skill-диспетчер**
`rg-bcreq-v1-dispatcher` в `.gigacode/skills/`. Он исполняет граф
`RG-BCREQ-v1` по сохранённому состоянию, а не полагается на семантический выбор
навыка или автоматическое делегирование субагенту. Пользователь запускает его
командой `/skills rg-bcreq-v1-dispatcher`, после чего передаёт `TASK_ID`.

Логическая единица работы — `TASK_ID`; все следы лежат в
`runs/<TASK_ID>/`. Идентификатор сессии GigaCode записывается только как
необязательная наблюдаемая ссылка и не определяет идентичность задачи. Поиск
знаний использует локальный `docs/kb/` и корпоративный Confluence через
разрешённый MCP как дополняющие каналы. Каждый выбранный источник подтверждает
человек по заголовку, разделу, странице/anchor, цитате и locator. Ошибка машинной проверки
останавливает маршрут без автоматического исправления и возвращает управление
`G-human`.

Канонический результат остаётся Markdown, а для публикации создаётся
`A-BCREQ.confluence.html` — семантический XHTML/HTML-фрагмент, совместимый с
Confluence Storage Format. Публикация является отдельным, дважды подтверждаемым
действием. Операторский HTML-гайд поставляется вместе с этим RFC.

## Motivation

Текущий execution package уже задаёт контракты, одиннадцать навыков, граф и
валидатор, но его перенос в отдельный runtime выявил четыре разрыва:

1. Runtime хранит навыки в `.agents/skills/`. Текущая документация именно
   GigaCode **CLI** определяет project skills в `.gigacode/skills/`; путь
   `.agents/skills/` относится к другому GitVerse execution context и не может
   считаться подтверждённым CLI-контрактом.
2. CLI выбирает model-invoked skills и автоматических subagents семантически
   по описанию и контексту. Это не гарантирует порядок узлов и гейтов строгого
   графа `RG-BCREQ-v1`.
3. Нынешний run sheet разделяет `TASK-*` и `RUN-*`, а результат кладёт в
   `runs/<RUN_ID>/`. После `/resume` или новой сессии нет одного стабильного
   адреса задачи.
4. Текущая политика допускает корректирующую попытку после reject, тогда как
   контракт issue #591 требует остановки, объяснения дефекта и решения человека.

Без явного решения пакет может выглядеть установленным, но быть невидимым CLI,
пройти узлы в неверном порядке либо незаметно исправить результат после
машинного reject.

### Проверенная граница документации

На 2026-09-21 изучены следующие официальные страницы GitVerse (`ext-323`):

| Область | Подтверждённый факт | Следствие для RFC |
| --- | --- | --- |
| [Quick start](https://gitverse.ru/docs/ai/ai-assistant-gigacode/getting-started-with-gigacode/quick-start) | CLI запускается локально командой `gigacode` после организационной установки | Инструкция не подменяет корпоративный канал установки |
| [Skills](https://gitverse.ru/docs/ai/ai-assistant-gigacode/gigacode-cli/skills) | Project skills: `.gigacode/skills/`; ручной запуск: `/skills <name>`; model invocation зависит от `description` | Мигрировать путь; диспетчер запускать явно |
| [Subagents](https://gitverse.ru/docs/ai/ai-assistant-gigacode/gigacode-cli/subagents) | Project agents: `.gigacode/agents/`; auto-delegation семантическое; named agent имеет отдельный контекст | Не использовать subagent как источник порядка графа |
| [Commands](https://gitverse.ru/docs/ai/ai-assistant-gigacode/gigacode-cli/commands) | Доступны `/resume`, `/skills`, `/mcp`, `/memory`; project commands лежат в `.gigacode/commands/` | Resume не заменяет TASK_ID; preflight может проверить skills/MCP |
| [Memory](https://gitverse.ru/docs/ai/ai-assistant-gigacode/gigacode-cli/memory) | Новая сессия начинает с чистого контекста; проектные инструкции перечитываются | Состояние маршрута должно жить в Git-файлах, не в чате |
| [MCP](https://gitverse.ru/docs/ai/ai-assistant-gigacode/gigacode-cli/mcp) | Project config: `.gigacode/settings.json`; доступны allowlist инструментов и `/mcp`; секреты передаются окружением | Confluence задаётся контрактом capability, без вымышленных tool names и секретов |

Альтернативная гипотеза «текущая `.agents/skills/` уже является нативным путём
CLI» опровергнута CLI-справкой. Альтернативная гипотеза «автоматический subagent
даёт строгую маршрутизацию» опровергнута описанной в справке моделью выбора по
формулировке запроса, `description` и контексту.

## Goals and Non-goals

### Goals

- задать устанавливаемую структуру MVP для текущего GigaCode CLI;
- обеспечить воспроизводимый порядок `RG-BCREQ-v1` и возобновление по
  `TASK_ID` между сессиями;
- нормировать дополняющий поиск `docs/kb/` + Confluence MCP и human confirmation;
- сделать reject валидатора fail-closed и управляемым человеком;
- встроить возражение, проверку полноты и двойное подтверждение в маршрут;
- определить Confluence-ready выход и процедуру добавления golden-примеров;
- дать оператору автономное HTML-руководство.

### Non-goals

- реализовывать изменения в `mango-ba-ai-runtime-cli` этим PR;
- выбирать корпоративный Confluence MCP server, URL или имена его tools;
- публиковать результат в Confluence;
- обучать модель или автоматически превращать пользовательские прогоны в
  golden-набор;
- менять семантику самого BCREQ, таксономии или принятые Hub ADR;
- гарантировать совместимость GigaCode for VS Code: целевой продукт — CLI.

## Proposal

### 1. Целевая структура runtime

После отдельного implementation PR runtime имеет минимальную структуру:

```text
.
├── AGENTS.md
├── .gigacode/
│   ├── skills/
│   │   ├── rg-bcreq-v1-dispatcher/SKILL.md
│   │   └── <route-node>/SKILL.md
│   └── settings.example.json
├── contracts/
├── docs/
│   ├── guides/
│   └── kb/
├── golden/
├── routes/rg-bcreq-v1.yaml
├── runs/<TASK_ID>/
└── tools/validate-package.sh
```

`AGENTS.md` остаётся единственным нормативным project contract. Не создаётся
копия правил в `GIGACODE.md`; если конкретная версия CLI потребует такой файл,
он может быть только сгенерированным указателем на `AGENTS.md` и должен
проверяться на drift.

Все runtime skills мигрируют из `.agents/skills/` в `.gigacode/skills/` одним
атомарным изменением. Дублирование двух деревьев после миграции запрещено:
иначе исправления разойдутся. Валидатор проверяет наличие диспетчера и каждого
узла маршрута по новому пути.

### 2. Диспетчер вместо неявной маршрутизации

Решение: один project skill `rg-bcreq-v1-dispatcher` с явным пользовательским
вызовом и отключённым model invocation, если установленная версия CLI
поддерживает соответствующее поле. Даже без этого поля обязательным входом
остаётся `/skills rg-bcreq-v1-dispatcher`, а первым предметным входом —
валидный `TASK_ID`.

Диспетчер:

1. проверяет формат `TASK_ID` и обнаруживает `runs/<TASK_ID>/task.yaml`;
2. создаёт новый task record либо сверяет неизменяемые поля существующего;
3. читает `routes/rg-bcreq-v1.yaml`, находит последний принятый event и
   вычисляет **ровно один** следующий узел;
4. вызывает инструкции этого узла по имени, записывает вход, выход, ссылки на
   evidence и gate event;
5. не перескакивает узел и не принимает решение gate из текста ответа;
6. после каждого перехода запускает структурную проверку состояния;
7. на `reject`, неоднозначности или запросе опасного действия останавливается у
   `G-human`.

Нативный model routing разрешён для справочных навыков вне маршрута, но не для
выбора следующего узла `RG-BCREQ-v1`. Named subagent можно позднее добавить для
изоляции контекста или MCP-прав, однако он получает от диспетчера один узел и не
владеет графом. Это сохраняет полезную специализацию, не делая вероятностное
делегирование механизмом корректности.

Строгость обеспечивают вместе: явный entrypoint, машиночитаемый граф,
persisted state, append-only events и валидатор. Один prompt или один subagent
сам по себе строгой оркестрацией не считается.

### 3. TASK_ID, сессия и `runs/<TASK_ID>/`

`TASK_ID` — выданная человеком стабильная идентичность предметной задачи по
regex `^TASK-[0-9]{4}$`. `RUN_ID` — идентификатор попытки исполнения внутри
задачи. `session_ref` — необязательная диагностическая ссылка на сессию CLI;
официальная документация не обещает программно доступный стабильный session ID,
поэтому он не используется как ключ.

```text
runs/TASK-0001/
├── task.yaml
├── runs/
│   └── RUN-0001.yaml
├── evidence/
├── A-BCREQ.md
└── A-BCREQ.confluence.html
```

`task.yaml` содержит как минимум:

```yaml
schema_version: 1
task_id: TASK-0001
route_id: RG-BCREQ-v1
active_run_id: RUN-0001
status: in_progress
session_refs: []
created_at: 2026-09-21T00:00:00Z
updated_at: 2026-09-21T00:00:00Z
```

Каждый `runs/RUN-*.yaml` хранит упорядоченные append-only events с полями
`seq`, `at`, `node_id`, `gate`, `decision`, `evidence_refs`, `actor` и
`reason`. При старте в новой сессии оператор повторяет ту же команду с
`TASK_ID`; диспетчер восстанавливает следующий узел из файлов, а не из chat
history. `/resume` удобен, но не является условием воспроизводимости.

Одновременно допустим только один `active_run_id`. Новый RUN разрешён после
явного решения человека `restart`; предыдущий файл не переписывается. Результат
задачи хранится на уровне `TASK_ID`, а не внутри попытки, и обновляется только
после принятого gate.

### 4. Дополняющий поиск знаний и подтверждение источника

Каналы используются в доступной комбинации, а не как последовательный fallback:

1. `ST-LOCAL`: искать релевантные документы в `docs/kb/`, фиксировать пути и
   найденные фрагменты в evidence;
2. `ST-CONFLUENCE`: проверить разрешённый Confluence MCP, если канал доступен
   и соответствует предмету задачи; локальная находка не запрещает проверку;
3. `G-human`: перед использованием показать `title`, `section`,
   `page_or_anchor`, `quote`, `locator` и получить явное подтверждение; при
   недоступности канала, новых credentials или конфликте остановить маршрут.

Диспетчер не выдумывает имя сервера или tools. На preflight он проверяет через
`/mcp`, что оператором настроен один server с capability `search` и `read` для
корпоративной БЗ. Конкретное отображение capability → tool name находится в
локальной конфигурации организации. `.gigacode/settings.example.json` может
показывать форму, но URL, токены и заголовки авторизации не коммитятся; секреты
поступают из окружения.

Выбор комбинации каналов фиксируется в evidence и зависит от вопроса, а не от
правила «первый hit победил». Если использован Confluence, evidence record содержит server alias, запрос,
идентификатор/URL страницы и время чтения, но не секреты и не полный кэш
страницы. Web-поиск не является неявным третьим уровнем MVP.

### 5. Fail-closed машинная проверка

В route policy устанавливаются `corrective_attempts: 0` и
`on_reject: halt_and_request_human`. `tools/validate-package.sh` остаётся
единственной публичной командой package validation и должен:

- завершаться `0` только при полном принятии;
- завершаться ненулевым кодом при любом нарушении;
- не редактировать, не форматировать и не генерировать проверяемые файлы;
- вывести `TASK_ID`, нарушенный invariant, путь/поле, ожидаемое значение и
  команду повторной проверки;
- добавить `reject` event в активный RUN через отдельный append-only recorder;
- прекратить диспетчер и запросить у `G-human` одно из решений: исправить
  вручную, разрешить новую попытку, отменить задачу.

Пример интерфейса ошибки:

```text
REJECT TASK-0001 C-RK:event-sequence
runs/TASK-0001/runs/RUN-0001.yaml: event seq=7 skips gate G-mach
No files were changed. Choose: manual-fix | restart | cancel.
Recheck: sh tools/validate-package.sh --task TASK-0001
```

Валидатор не вызывает модель и не предлагает patch как выполненное действие.
Он может дать диагностическую рекомендацию, но любое изменение начинается
после нового явного решения человека.

### 6. Мета-когнитивные human checkpoints

Диспетчер реализует три независимых правила:

**Возражение до исполнения.** Если задача противоречит контракту, источнику,
безопасности или существует существенно лучший путь, диспетчер показывает
конфликт, варианты и рекомендацию. До ответа `G-human` затронутая ветка не
выполняется; незатронутый анализ можно продолжить.

**Проверка полноты после черновика.** Перед финальным gate диспетчер строит
матрицу «цель/критерий → evidence → секция результата» и отдельно перечисляет
полезные шаги за пределами запроса. Пробел в цели возвращает работу в нужный
узел только после решения человека; смежные улучшения не расширяют scope
автоматически.

**Двойное подтверждение необратимого действия.** Для публикации в Confluence,
перезаписи существующей страницы или внешней отправки нужны два разных события:

1. `intent_confirmed`: показаны точная цель, page ID/URL, representation,
   preview/diff и возможная перезапись;
2. `execution_confirmed`: непосредственно перед MCP write человек повторно
   подтверждает тот же fingerprint действия.

Изменение fingerprint аннулирует оба подтверждения. Локальное создание нового
файла не считается необратимым и двойного подтверждения не требует. Машинный
reject нельзя обойти подтверждением публикации.

### 7. Выход для Confluence

Канонический редактируемый результат — `A-BCREQ.md`. Экспорт
`A-BCREQ.confluence.html` содержит fragment в безопасном подмножестве
XHTML/Confluence Storage Format: заголовки, абзацы, списки, таблицы,
`<ac:structured-macro>` только при проверенной поддержке целевого MCP, ссылки на
evidence и стабильные section anchors. В нём нет JavaScript, inline event
handlers, секретов и локальных абсолютных путей.

Перед публикацией adapter запрашивает capabilities MCP:

- если поддерживается `storage`, fragment передаётся без потери структуры;
- если сервер принимает `atlas_doc_format` или Markdown, adapter выполняет
  явное преобразование и сохраняет representation в event;
- если capability не объявлена, сохраняется локальный export и вызывается
  `G-human`, а формат не угадывается.

Публикация идемпотентна по паре `TASK_ID + content_sha256`: повтор с тем же hash
не создаёт новую страницу. Обновление существующей страницы требует текущую
версию страницы, preview/diff и двойное подтверждение.

### 8. HTML user guide и Golden Set

Целевой операторский документ:
[`mango-ba-ai-runtime-cli-user-guide.html`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/meta-model-guides/gigacode-cli/mango-ba-ai-runtime-cli-user-guide.html).
Он описывает реализованный в Хабе копируемый пакет; перенос во внешний runtime
остаётся отдельным implementation PR. Руководство покрывает установку, preflight,
запуск, resume, KB/MCP, reject, публикацию и golden workflow.

Golden-пример добавляется только из успешно завершённой задачи после отдельного
одобрения человека:

1. выбрать принятый TASK и проверить происхождение evidence;
2. удалить персональные данные, секреты и закрытые ссылки либо получить право
   на их хранение;
3. скопировать минимальный вход и ожидаемый результат в новый стабильный
   `case-id`, не менять существующий case;
4. записать `origin_task_id`, `confirmed_by`, `confirmed_at`, класс кейса и
   обоснование ожидаемого вердикта;
5. добавить как минимум один связанный negative case, если пример закрывает
   новый дефект;
6. обновить `golden/cases.yaml`, прогнать package validator и тесты golden set;
7. провести обычный PR review.

Runtime никогда не пополняет golden автоматически из чата или Confluence.

### Acceptance mapping

| Критерий issue #591 | Решение | Проверка implementation PR |
| --- | --- | --- |
| TASK/session и `runs/<TASK_ID>/` | §3 | restart/resume test с двумя CLI-сессиями |
| Skill routing или dispatcher subagent | §2: явный dispatcher skill | graph-order и skipped-gate negative tests |
| `docs/kb/` + Confluence MCP + source confirmation | §4 | complementary-channel, confirmation-gate и MCP-unavailable tests |
| `validate-package.sh`, stop, G-human | §5 | validator non-mutation и reject-event tests |
| Возражение, полнота, двойное подтверждение | §6 | три dialogue contract tests |
| Confluence output, HTML guide, golden | §7–8 | export fixture, guide link check, golden workflow test |

## Alternatives

### A. Оставить model-invoked skills как маршрутизатор

Отклонено. Это минимально по коду, но выбор по `description` и текущему
контексту не доказывает порядок графа и не восстанавливает состояние между
сессиями.

### B. Сделать named subagent единственным диспетчером

Отклонено как основной механизм. Отдельный контекст и tool allowlist полезны,
но автоматическое делегирование также семантическое. Subagent допустим только
как исполнитель явно назначенного узла под контролем persisted dispatcher.

### C. Ввести внешний workflow engine

Отложено. Он дал бы более сильную транзакционность, но для одного MVP-графа
добавляет отдельный runtime, deployment и модель отказов. Файловый state machine
с тестами закрывает текущую цель меньшей ценой.

### D. Использовать session ID или `RUN_ID` как верхний каталог

Отклонено. Сессия может смениться, а task продолжиться; несколько попыток одной
задачи должны оставаться рядом. `TASK_ID` — единственный стабильный внешний ключ.

### E. Публиковать Markdown напрямую

Отклонено как единственный формат: качество таблиц, anchors и macros зависит от
конкретного MCP. Markdown сохраняется как source, а representation-aware export
делает преобразование явным и проверяемым.

## Trade-offs

- Явный `/skills` старт менее «магический», зато наблюдаем и воспроизводим.
- Persisted state добавляет schema и locking, зато переживает смену сессии.
- Нулевая автокоррекция чаще возвращает работу человеку, зато исключает скрытую
  смену результата после reject.
- Миграция `.agents/skills/` → `.gigacode/skills/` является breaking change для
  пользователей старого не-CLI контекста; параллельные копии сознательно не
  поддерживаются.
- XHTML export требует adapter tests; взамен Confluence representation и
  потери преобразования становятся видимыми.
- Двойное подтверждение замедляет публикацию, но ограничено необратимыми
  действиями и не мешает локальной подготовке.

## Impacted Artifacts

Этот PR изменяет только Hub:

- настоящий RFC и HTML-гайд;
- навигацию направления и Artifact Map;
- registry внешних источников (`ext-323`).

После принятия RFC отдельный PR в `mango-ba-ai-runtime-cli` должен изменить:

- `.agents/skills/**` → `.gigacode/skills/**` и добавить dispatcher;
- `routes/rg-bcreq-v1.yaml` — zero-correction policy и explicit halt;
- контракты `C-IN`/`C-RK` и run sheet — TASK-rooted state/events;
- `taxonomy/source-tiers.yaml` — complementary local/Confluence collection и обязательный `G-human`;
- `tools/validate-package.sh` и Python validator — non-mutating task checks;
- `.gigacode/settings.example.json` — только capability-shaped MCP example;
- `meta-model-guides/**`, `golden/**`, README и тесты.

Секреты, реальные corporate URLs и пользовательские run data в Git не входят.

## Implementation and Validation

Implementation PR выполняется атомарными стадиями:

1. добавить failing compatibility test, требующий `.gigacode/skills/`, затем
   мигрировать skills;
2. добавить schema/tests task state и перенести fixtures в `runs/<TASK_ID>/`;
3. реализовать dispatcher state machine с graph-order negative tests;
4. реализовать дополняющие source channels и human confirmation с mocked MCP capabilities;
5. сделать validator non-mutating для package/result и добавить filesystem
   before/after test, допускающий только новый append-only `reject` event;
6. добавить meta-checkpoints и dialogue tests;
7. добавить Confluence export fixtures, guide и golden procedure;
8. прогнать полный runtime CI и ручной smoke test в установленном GigaCode CLI.

Минимальные автоматические доказательства:

- skill discovery fixture совпадает с `.gigacode/skills/`;
- два запуска с одним TASK и разными `session_ref` продолжают один state;
- нельзя пропустить gate, повторить `seq` или открыть второй active RUN;
- local KB и configured MCP используются в объявленной комбинации, а источник
  не принимается без human confirmation;
- недоступный MCP и validator reject завершают маршрут без изменений результата;
- публикация невозможна без двух подтверждений одного fingerprint;
- export проходит structural fixture test и не содержит запрещённых элементов;
- новый golden case не проходит без provenance и human confirmation.

Ручной smoke test фиксирует версию `gigacode --version`, вывод `/skills`, `/mcp`
и два последовательных запуска одного `TASK_ID`. Логи не должны содержать
credentials или полное содержимое закрытых Confluence-страниц.

## Lifecycle and Decision Path

Статус `proposed` означает, что анализ завершён и локальные Hub validators
пройдены, но архитектура ещё не принята. Владелец:

1. принимает RFC либо возвращает его в `draft` с вопросами;
2. после принятия создаёт/подтверждает implementation scope в runtime;
3. runtime PR прикладывает acceptance evidence из предыдущего раздела;
4. после его merge HTML-гайд дополняется фактическим runtime status и
   проверенной минимальной версией CLI; текущий banner подтверждает только
   реализацию копируемого пакета в Хабе.

Если официальная CLI-документация изменит paths, invocation или MCP schema,
RFC возвращается в `draft`; изменение не переносится в runtime молча.

## Open Questions

Блокирующих вопросов для архитектурного решения нет. До implementation PR
организация должна предоставить два конфигурационных значения, которые нельзя
вывести из публичной документации: alias корпоративного Confluence MCP и
отображение его read/search/write capabilities на реальные tools. Их отсутствие
не меняет архитектуру: неподтверждённый read останавливается у `G-human`, а publish
остаётся выключен.

## Related Artifacts

- [Execution package MVP BCREQ](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/projects/ba-gigacode-implementation/execution-package-gigacode-cli)
- [BA meta-model decision framework](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/30-decision-framework.md)
- [Runtime repository](https://github.com/G-Ivan-A/mango-ba-ai-runtime-cli)
- [HTML operator guide](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/meta-model-guides/gigacode-cli/mango-ba-ai-runtime-cli-user-guide.html)
- [External Sources Registry](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/external-knowledge/external-sources-registry.md)
- [Issue #591](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/591)
- [Issue #593](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/593)
