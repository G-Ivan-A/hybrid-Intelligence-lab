---
status: draft
version: 0.5
updated: 2026-10-07
temperature: 0.1
---

# 4. Работа с агентом: реальная задача BCREQ

**Цель:** довести реальную задачу — ссылку на Jira или описание своими
словами — до проверенного Release. Основная работа идёт в диалоге с агентом
Cline; готовые команды в терминале VS Code нужны в трёх местах, и агент подскажет,
какую выполнить.

Перед началом должны быть выполнены [установка](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/02-install.md) и
[развёртывание](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/03-deploy-package.md). [Учебный прогон](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/04-smoke-test.md) не
обязателен.

## Содержание

1. [Как устроена работа](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#как-устроена-работа)
2. [Шаг 1. Выберите TASK ID](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#шаг-1-выберите-task-id)
3. [Шаг 2. Начните задачу в Cline](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#шаг-2-начните-задачу-в-cline)
4. [Шаг 3. Согласуйте пункты с агентом](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#шаг-3-согласуйте-пункты-с-агентом)
5. [Шаг 4. Получите черновик](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#шаг-4-получите-черновик)
6. [Шаг 5. Запечатайте черновик](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#шаг-5-запечатайте-черновик)
7. [Шаг 6. Запустите проверку задачи](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#шаг-6-запустите-проверку-задачи)
8. [Шаг 7. Проверьте результат и примите решение](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#шаг-7-проверьте-результат-и-примите-решение)
9. [Диалог с Cline: вопросы и режимы Plan и Act](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#диалог-с-cline-вопросы-и-режимы-plan-и-act)
10. [Можно ли подключить внешнюю модель, например DeepSeek](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#можно-ли-подключить-внешнюю-модель-например-deepseek)
11. [Что ожидать от модели](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#что-ожидать-от-модели)
12. [Разговорные формулировки и термины модели](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#разговорные-формулировки-и-термины-модели)
13. [Типичные ситуации](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#типичные-ситуации)
14. [Отправка результата в Git](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#отправка-результата-в-git)

## Как устроена работа

| Шаг | Кто | Где | Что происходит |
|-----|-----|-----|----------------|
| 1 | Вы | — | Выбираете номер прогона [TASK ID](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-task-id) |
| 2 | Вы → агент | [Панель Cline](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-cline-panel), режим Plan | Стартовая фраза: процесс, входные данные |
| 3 | Агент ⇄ вы | Панель Cline, режим Plan | Агент ищет подтверждения, перепроверяет, показывает нумерованные пункты; вы подтверждаете или отклоняете |
| 4 | Агент | Панель Cline, режим Act | Агент записывает черновик `submissions/TASK-ID.json`; вы разрешаете запись |
| 5 | Вы | [Терминал VS Code](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-vscode-terminal) | Команда «Запечатать черновик» |
| 6 | Вы | Терминал VS Code | Команда «Запустить проверку задачи» → `PASS` или `FAIL` |
| 7 | Вы (+ агент) | Панель Cline, VS Code | Ваша проверка по чек-листу и решение |

При `FAIL` — шаги 4–6 повторяются с **новым** TASK ID
([почему](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#контроль-прогонов-один-task-id--один-прогон)).

## Шаг 1. Выберите TASK ID

- TASK ID — номер **прогона**, а не задачи в Jira: `TASK-` и минимум 4 цифры.
  Первая реальная задача — `TASK-0002` (номер `TASK-0001` занят учебным
  примером), дальше — следующие свободные номера.
- Свободный номер — тот, которого нет ни в папке `runs/`, ни в папке
  `submissions/` (посмотрите в проводнике VS Code).
- Ключ Jira (`BCREQ-123`) в качестве TASK ID не подходит: runner примет только
  `TASK-NNNN`. Ключ и ссылка на Jira записываются внутрь черновика как
  источник. Для себя ведите соответствие «TASK ID → задача Jira»
  (например, в заметках): одной задаче Jira может соответствовать несколько
  TASK ID — по одному на каждую попытку.

## Шаг 2. Начните задачу в Cline

1. Откройте панель Cline → новая задача (кнопка «+» / New Task). Одна задача
   Jira — один диалог Cline.
2. Переключите режим на **Plan** (переключатель Plan/Act под полем ввода):
   в нём Cline только читает и разговаривает, файлы не меняются.
3. Вставьте стартовую фразу, заменив значения в угловых скобках.

### Стартовая фраза

```text
У меня реальная задача BCREQ, а не учебный пример.
Номер прогона: TASK-0002.
Входные данные: <ссылка на задачу в Jira или страницу Confluence;
или суть задачи своими словами>.

Веди меня по шагам и не пропускай согласование:
1. Покажи нумерованный список доступных процессов и спроси, какой запускаем.
2. Спроси, каких входных данных не хватает.
3. Найди подтверждения: сначала в корпоративных Jira/Confluence, если они
   подключены, затем в базе знаний docs/kb по правилам docs/kb-policy.md.
   Перепроверь найденное ещё раз: связаны ли документы с моей задачей.
4. Показывай находки нумерованными пунктами с цитатой и адресом источника,
   чтобы я мог ответить «1 — да, 2 — нет, потому что …».
5. На каждом шаге показывай, что я могу сделать дальше: человеческое
   название действия, а команду — в скобках.
6. Ничего не выдумывай: нет подтверждения — открытый вопрос.
Файлы не меняй, пока я не скажу «пиши черновик».
```

- **Ожидаемый результат:** Cline отвечает нумерованным списком. В пилоте
  доступен один процесс — «Сформировать бизнес-спецификацию по задаче
  BCREQ»; ответьте `1`.
- **Проверьте:** Cline не начал писать файлы и не предложил выполнить
  команду.

Эта фраза задаёт порядок работы, потому что в пакете пока нет готовой
команды Cline, которая ведёт процесс сама
([О-4](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#ограничения-текущей-версии-пакета)). Правила
агента в пакете написаны для учебного примера
([О-1](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#ограничения-текущей-версии-пакета)), поэтому
первая строка фразы прямо говорит, что задача реальная. Если Cline
ответит, что работает только с учебным примером `TASK-0001`, — повторите
первую строку фразы; если отказ повторится, передайте ответственному текст
ответа.

### Какие входные данные можно дать

| Что у вас есть | Что написать | Что сделает Cline |
|----------------|--------------|-------------------|
| Ссылка на задачу Jira, и администратор подключил Jira к Cline ([MCP](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-mcp)) | `Входные данные: https://…/browse/BCREQ-123` | Попросит разрешения обратиться к Jira (разрешите), прочитает задачу |
| Ссылка на Jira, но подключения нет | Ссылку **и** текст задачи, скопированный из Jira | Возьмёт суть из текста; ссылку запишет как адрес источника. Сам открыть Jira он не может |
| Страница Confluence | Так же, как Jira | Так же, как Jira |
| Только описание своими словами | `Входные данные: клиент хочет …` | Будет искать подтверждения в KB `docs/kb/`; чего не найдёт — станет открытым вопросом |

Проверить, подключена ли Jira: панель Cline → **MCP Servers** — в списке
есть сервер Jira/Confluence. Если списка нет или он пуст — подключения нет.

## Шаг 3. Согласуйте пункты с агентом

Агент показывает найденное нумерованными пунктами. Отвечайте по номерам:

```text
1 — да.
2 — нет: это относится к другому продукту, исключи.
3 — уточни: покажи дословную цитату и где она в документе.
```

Что агент должен согласовать с вами (все пункты нужны runner):

1. Суть задачи и цель клиента.
2. Что входит в изменение и что **не** входит (граница системы).
3. Продуктовую привязку: к какому продукту Mango относится задача.
4. Тип работы (изменение продукта Mango, база знаний, отраслевая практика,
   внешняя спецификация).
5. Источник каждого утверждения: адрес, место в документе и дословную цитату.
6. Требования (FR), сценарии (UC), нефункциональные требования (NFR),
   обратную совместимость.
7. Открытые вопросы. **Пока хотя бы один вопрос открыт, Release не
   собирается** — ответьте на них или исключите пункт.

Полезные просьбы в диалоге:

- «Перепроверь пункт 4 по базе знаний ещё раз».
- «Покажи противоречия между источниками, если есть».
- «Сведи согласованное в таблицу по пунктам».
- «Что мне сейчас можно сделать дальше? Покажи список действий».

## Шаг 4. Получите черновик

1. Переключите режим на **Act**.
2. **Напишите Cline:**

   ```text
   Все пункты согласованы. Пиши черновик в submissions/TASK-0002.json
   по схеме contracts/c-working-bcreq.schema.json, образец формата —
   golden/TASK-0001.json. Моё согласование запиши так:
   проверил и согласовал — <ваши фамилия и имя>, основание — <ссылка на
   комментарий в Jira или «согласовано в диалоге Cline <дата>»>.
   Файлы, кроме submissions/TASK-0002.json, не меняй.
   ```

3. Cline покажет файл и попросит разрешения на запись. **Проверьте** имя
   файла: `submissions/TASK-0002.json`. Если имя другое — нажмите Reject.
   Если имя верное — разрешите запись (Save / Approve).
4. Попросите: «Перескажи черновик по пунктам согласования 1–7» и сверьте
   с тем, что вы согласовали.

Ваше согласование записывается в черновик **до** машинной проверки: runner
не принимает черновик без отметки о согласовании человеком. Отметка
означает «я проверил пункты 1–7», а не «я одобрил публикацию» — решение о
публикации принимается на [шаге 7](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#шаг-7-проверьте-результат-и-примите-решение).

## Шаг 5. Запечатайте черновик

Runner принимает черновик, только если его контрольные суммы совпадают с
содержимым. Cline их правильно посчитать не может, поэтому после **каждой**
правки черновика выполните команду
[«Запечатать черновик»](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#запечатать-черновик).

- **Где:** терминал VS Code, папка пакета.
- **Команда** (замените `TASK-0002` на свой номер):

  ```bash
  python tools/run_task.py seal submissions/TASK-0002.json
  ```

- **Ожидаемый результат:** `sealed: submissions/TASK-0002.json`.

Команда только пересчитывает контрольные суммы и не меняет смысл черновика.

## Шаг 6. Запустите проверку задачи

**Действие: «Запустить проверку задачи»**
(`python tools/run_task.py run TASK-0002 submissions/TASK-0002.json`)

- **Где:** терминал VS Code, папка пакета.
- **Команда:**

  ```bash
  python tools/run_task.py run TASK-0002 submissions/TASK-0002.json
  ```

- **Ожидаемый результат:** `TASK-0002: PASS` или `TASK-0002: FAIL` со
  строками `ERROR: …` выше.

**Если `PASS`** — переходите к шагу 7.

**Если `FAIL`:**

1. Уберите неудачный черновик из `submissions/` командой
   [«Убрать неудачный черновик»](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#убрать-неудачный-черновик):

   ```bash
   mv submissions/TASK-0002.json runs/TASK-0002/working.json
   ```

   Черновик сохранится рядом с журналом этого прогона, а папка
   `submissions/` останется чистой для проверки перед отправкой в Git.
2. Выделите в терминале строки `ERROR: …`, скопируйте (`Ctrl+C`) и
   **напишите Cline:**

   ```text
   Проверка TASK-0002 не прошла. Ошибки runner:
   <вставьте строки ERROR>
   Объясни простыми словами, что не так, по пунктам. Исправленный черновик
   запиши под новым номером в submissions/TASK-0003.json. Прежний черновик
   лежит в runs/TASK-0002/working.json.
   ```

3. Повторите шаги 4–6 с номером `TASK-0003`.

Расшифровка частых ошибок — в разделе [Типичные ситуации](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#типичные-ситуации).
Если причина непонятна — перейдите в [режим отладки](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#режим-отладки).

## Шаг 7. Проверьте результат и примите решение

Машинный `PASS` означает только, что черновик соответствует формату и
правилам. Смысл проверяете вы ([G-human](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-g-human)).

1. Откройте `runs/TASK-0002/release.json` или попросите Cline (режим Plan):
   «Перескажи runs/TASK-0002/release.json по пунктам для согласования».
2. Пройдите чек-лист `evaluation/g-human-checklist.md`:
   - каждый источник действительно прочитан и может использоваться;
   - продуктовая привязка и граница системы соответствуют запросу;
   - FR, UC, NFR, обратная совместимость и смысл Release верны;
   - открытых вопросов нет; публикацию вы одобряете или отклоняете явно.
3. Запишите решение там, где принято в вашей команде (например, комментарием
   в задаче Jira со ссылкой на TASK ID).

До вашего решения Release остаётся кандидатом.

## Диалог с Cline: вопросы и режимы Plan и Act

Cline — полноценный собеседник: задавать ему вопросы можно в любой момент,
на русском языке, обычными словами. Команды Python этому не мешают: их
запускаете вы в терминале VS Code, а диалог идёт в панели Cline.

| Режим Cline | Что Cline может | Когда использовать |
|-------------|-----------------|--------------------|
| **Plan** | Предназначен для чтения, поиска и ответов. В Cline 4.1.21 команды технически доступны и здесь; останавливайте неожиданные вызовы подтверждением и hook | Постановка задачи, поиск источников, согласование, вопросы «почему?», разбор ошибок |
| **Act** | То же + записать файл (с вашего разрешения) | Только когда нужно записать черновик в `submissions/` |

Переключатель Plan/Act находится под полем ввода панели Cline. История
диалога при переключении сохраняется.
Plan сам по себе не является защитой файлов: держите выключенным
автоматическое разрешение команд и следуйте [настройке защиты](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/03-deploy-package.md#настройте-подтверждения-в-cline).

Как задавать вопросы:

- Конкретно: «Почему пункт 3 отнесён к продукту „Речевая аналитика“?
  Покажи цитату».
- С просьбой о форме: «Ответь по пунктам, простыми словами, без JSON».
- С проверкой: «Где это написано? Дай адрес и дословную цитату».
- О следующем шаге: «Что мне делать дальше? Дай список действий с
  командами в скобках».

Встроенные команды Cline, которые пригодятся (вводятся в поле ввода панели
Cline, начинаются с `/`):

| Команда | Что делает |
|---------|------------|
| `/newtask` | Начать новую задачу, перенеся в неё краткое содержание текущей — например, при переходе в режим отладки |
| `/smol` | Сжать длинный диалог, если Cline начал «забывать» начало |

Готовых команд пакета вида `/bcreq-…` нет
([О-4](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#ограничения-текущей-версии-пакета)).

## Можно ли подключить внешнюю модель, например DeepSeek

**Технически — да.** В Cline есть встроенный провайдер DeepSeek:
настройки Cline → API Provider **DeepSeek** → ключ API DeepSeek → модель из
списка. Также Cline позволяет назначить разные модели режимам Plan и Act
(настройка «Use different models for Plan and Act»): например, одна модель
для диалога и согласования, другая — для записи черновика.

**Для пилота — только с разрешения.** Всё, что вы пишете Cline, включая
текст задачи из Jira и выдержки из KB, отправляется выбранной модели. При
внешней модели эти данные уходят за пределы корпоративного контура. Прежде
чем подключать внешнюю модель, получите разрешение ответственного за
информационную безопасность. Без такого разрешения используйте модель
Mango AI ([подключение](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/02-install.md#подключение-модели-в-cline)).

Работу пакета с DeepSeek в пилоте не проверяли. Независимо от модели
результат проверки даёт только runner.

## Что ожидать от модели

Модель **может**: вести диалог по шагам, читать файлы пакета и KB, при
подключении — Jira/Confluence, объяснять, предлагать открытые вопросы,
писать черновик в `submissions/`, разбирать ошибки runner, если вы их
покажете, подсказывать следующую команду.

Модель **не должна**:

- запускать команды — их запускаете вы (отклоняйте такие запросы, Reject);
- менять правила, схемы и программы пакета;
- утверждать, что проверка прошла, — смотрите только строку runner в
  терминале;
- решать за вас вопросы об источниках и публикации.

Модель может ошибаться и уверенно придумывать. Всегда сверяйте цитаты с
источником.

## Разговорные формулировки и термины модели

Пробный диалог в веб-чате показал: модель, не видя файлов пакета,
придумывала шаги процесса и отметки «G-mach ✅», хотя проверка не
запускалась. В пилоте задача ставится в Cline внутри открытой папки пакета,
а проверку даёт только runner.

| Как говорят в чате | Что есть в пакете | Как делать |
|--------------------|-------------------|------------|
| «Изучи репозиторий по ссылке» | Папка пакета, открытая в VS Code | Ссылку на репозиторий не давайте; начните со [стартовой фразы](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#стартовая-фраза) |
| «Запускающий промпт» | [Стартовая фраза](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#стартовая-фраза) | Используйте её |
| «Стартуем задачу BCREQ» | Диалог + черновик + команда «Запустить проверку задачи» | Задача проверена, только когда runner напечатал `PASS` |
| `RG-BCREQ-v1` | Один процесс «Сформировать бизнес-спецификацию по задаче BCREQ» | Других процессов в пилоте нет |
| Узлы `intake`, `source-scan`, `api-impact`, навыки `skills/` | Нет. Машинные шаги только `validate-working`, `compile`, `validate-release` | Такие «узлы» от модели — выдумка |
| `G-self`, «G-mach ✅» в ответе модели | `G-mach` — только результат runner | Верьте терминалу, не тексту модели |
| Проекции `V-BIZ`, `V-APPROVE`, `V-DEV`, `V-CONTRACT`; профили `P-…` | Нет | Не выбирайте |
| `product_class=contact-center` | Продуктовая привязка из `taxonomy/mango-products.yaml` | Подтвердите привязку, которую предложит Cline (пункт 3 согласования) |
| `RUN-ID`, «Продолжи TASK-X, RUN-Y» | Нет RUN-ID. Повторный запуск с тем же TASK ID запрещён | Исправление — новый TASK ID |
| «Статус», «Покажи источники», «Одобрить» | Не команды пакета, но обычные просьбы Cline | Статус — строка runner и `runs/TASK-ID/`; одобрение — [шаг 7](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#шаг-7-проверьте-результат-и-примите-решение) |

Если Cline употребляет термин, которого нет в [глоссарии](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#глоссарий)
и в файлах пакета, спросите: «В каком файле пакета это определено?». Нет
файла — это не термин модели.

## Типичные ситуации

| Ситуация | Что это значит | Что делать |
|----------|----------------|------------|
| `ERROR: BASELINE Working digest does not match canonical content` | Черновик изменён после запечатывания или не запечатан | Выполните [«Запечатать черновик»](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#запечатать-черновик) и запустите проверку с новым TASK ID |
| `ERROR: EVID-03 evidence checksum does not match the retained excerpt` | Цитата источника изменена после запечатывания | То же |
| `ERROR: BASELINE human approval is required` | В черновике нет отметки о вашем согласовании | Повторите [шаг 4](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#шаг-4-получите-черновик) |
| `RELEASE unresolved questions block publication` | Остались открытые вопросы | Ответьте на вопросы или исключите пункт; новый черновик — под новым TASK ID |
| `ERROR: run already exists` | Этот TASK ID уже запускался | Новый номер ([почему](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#контроль-прогонов-один-task-id--один-прогон)) |
| `ERROR: task ID must match TASK-0001` | Номер не в формате `TASK-NNNN` (например, указан ключ Jira) | Используйте `TASK-` и 4 цифры |
| `ERROR: package hash mismatch` | Файл пакета изменён | Не продолжайте; восстановите пакет повторным копированием, сообщите ответственному |
| Cline просит выполнить команду | Модель хочет запустить команду сама | Reject; выполните нужную команду сами по инструкции |
| Cline просит записать файл не в `submissions/` | Модель вышла за границы | Reject; напомните: «Пиши только submissions/TASK-ID.json» |
| Cline пишет «проверка прошла», а runner не запускался | Модель рассуждает, а не проверяет | Запустите проверку сами |
| Cline привёл цитату, которой нет в источнике | Выдуманный источник | Удалите утверждение или сделайте открытым вопросом |
| Нет подтверждения ни в Jira/Confluence, ни в KB | Пробел в источниках | Открытый вопрос, но не догадка |

## Отправка результата в Git

Нужна, только если пакет развёрнут в закрытом (private) runtime-репозитории
и ответственный разрешил отправлять туда черновики. В публичный репозиторий
черновики реальных задач не отправляйте.

1. В `submissions/` должны остаться только черновики, прошедшие проверку.
   Неудачные уберите командой
   [«Убрать неудачный черновик»](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#убрать-неудачный-черновик).
2. Выполните [«Проверить всё перед отправкой»](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#проверить-всё-перед-отправкой):
   `python tools/run_task.py verify-ci`. Ожидаемый результат — `PASS` в каждой
   строке.
3. Коммитьте **только** файлы `submissions/TASK-ID.json`. Папки `runs/`,
   `docs/kb/`, `meta-model/` Git не отправит (`.gitignore`).
4. После отправки CI выполнит ту же проверку (`validate-cline-package / gate`).
   Машинный результат принят только при зелёном статусе.

---

**Навигация:** [Содержание](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/README.md) · [Обзор и глоссарий](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md) ·
[1. Установка](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/02-install.md) · [2. Развёртывание](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/03-deploy-package.md) ·
[3. Учебный прогон](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/04-smoke-test.md) · **4. Работа с агентом** ·
[5. Команды и отладка](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md)

← Назад: [3. Учебный прогон](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/04-smoke-test.md) · Далее: [5. Команды и отладка](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md) →
