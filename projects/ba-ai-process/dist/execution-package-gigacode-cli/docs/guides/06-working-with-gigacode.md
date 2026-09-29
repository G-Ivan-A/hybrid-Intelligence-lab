---
status: draft
version: 1.0
updated: 2026-09-29
temperature: 0.1
---

# 4. Работа с агентом: реальная задача BCREQ

**Цель:** провести реальную задачу от входных материалов до проверенного
[Release](01-junior-pilot.md#term-release) по маршруту `RG-BCREQ-v1`.
GigaCode готовит артефакты узлов, вы проверяете смысл и принимаете решения,
[runner](01-junior-pilot.md#term-runner) проверяет и выполняет переходы.

Перед началом: [развёртывание](03-deploy-package.md) завершено, «Проверить
пакет» показывает `G-mach: пакет принят`, открыты
[терминал A](01-junior-pilot.md#term-terminal-a) с `gigacode` и
[терминал B](01-junior-pilot.md#term-terminal-b) — второе окно PowerShell,
оба — в папке `$env:USERPROFILE\bcreq-pilot\runtime`.

## Содержание

1. [Как устроена работа](#как-устроена-работа)
2. [Шаг 1. Выберите TASK ID](#шаг-1-выберите-task-id)
3. [Шаг 2. Начните задачу](#шаг-2-начните-задачу)
4. [Шаг 3. Дайте GigaCode задачу](#шаг-3-дайте-gigacode-задачу)
5. [Шаг 4. Подготовьте и подтвердите вход A-IN](#шаг-4-подготовьте-и-подтвердите-вход-a-in)
6. [Шаг 5. Пройдите узлы маршрута](#шаг-5-пройдите-узлы-маршрута)
7. [Шаг 6. Запечатайте Working и соберите Release](#шаг-6-запечатайте-working-и-соберите-release)
8. [Шаг 7. Проверьте результат и примите решение](#шаг-7-проверьте-результат-и-примите-решение)
9. [Диалог с GigaCode: режимы и встроенные команды](#диалог-с-gigacode-режимы-и-встроенные-команды)
10. [Что ожидать от модели](#что-ожидать-от-модели)
11. [Разговорные формулировки и термины модели](#разговорные-формулировки-и-термины-модели)
12. [Типичные ситуации](#типичные-ситуации)
13. [Передача результата](#передача-результата)

## Как устроена работа

Задача идёт по узлам. На каждом узле повторяется один и тот же цикл:

1. **Терминал A.** Вы вызываете навык узла (`/skills <имя>`), GigaCode
   готовит [артефакт узла](01-junior-pilot.md#term-artifact) и спрашивает
   разрешения записать его в `runs/TASK-ID/evidence/`. Вы разрешаете.
2. **Вы.** Читаете артефакт. Если нужно — просите GigaCode исправить.
3. **Терминал A** (только узлы с [G-human](01-junior-pilot.md#term-g-human)).
   GigaCode готовит [checkpoint](01-junior-pilot.md#term-checkpoint) —
   короткую сводку для вашего решения.
4. **Терминал B.** Вы выполняете команду «Выполнить переход». Runner
   проверяет артефакт, на узле с G-human спрашивает строку подтверждения и
   переводит задачу в следующий узел.

| Кто | Что делает | Чего не делает |
|-----|------------|----------------|
| Вы | Выдаёте TASK ID, даёте источники, подтверждаете продукт, смысл и границы, вводите строку подтверждения, выполняете команды в терминале B | Не правите файлы пакета |
| GigaCode | Читает навыки и контракты, пишет артефакты и checkpoint в `runs/TASK-ID/evidence/` | Не выполняет переходы, не подтверждает за вас, не отправляет вопросы Заказчику |
| Runner | Проверяет артефакт, запускает G-mach, спрашивает подтверждение, ведёт журнал | Не оценивает смысл требований |

Состояние задачи хранится в файлах `runs/TASK-ID/`, а не в чате. Если
сессия GigaCode прервалась, начните новую, покажите состояние задачи и
продолжайте с текущего узла.

## Шаг 1. Выберите TASK ID

Возьмите следующий свободный номер: `TASK-` и 4 цифры, например
`TASK-0002`. Проверьте, что его ещё нет:

```powershell
Get-ChildItem runs
```

Номера `TASK-0001` лучше оставить для [учебного прогона](04-smoke-test.md).
Ключ задачи в Jira — это не TASK ID: в A-IN он попадает в название
задачи (`task.title`) и в источник вида `ticket`
(см. [TASK ID](01-junior-pilot.md#term-task-id)). Во всех примерах ниже
замените `TASK-0002` на свой номер.

## Шаг 2. Начните задачу

**Действие: «Начать задачу»**

- **Где:** терминал B, папка пакета.
- **Команды:**

  ```powershell
  python tools/run-task.py start TASK-0002
  New-Item -ItemType Directory -Force runs\TASK-0002\evidence\sources | Out-Null
  ```

- **Ожидаемый результат:**
  `TASK-0002: started at entry; next transition requires G-mach`
- **Проверьте:** `Get-ChildItem runs\TASK-0002` показывает `evidence`, `state.json`,
  `trace.jsonl`.

Файлы-источники (стенограмму, письмо, выгрузку) скопируйте в
`runs/TASK-0002/evidence/sources/`. Папка `runs/` не сверяется проверкой
пакета и исключена из Git, поэтому материалы задачи не ломают пакет и не
попадают в репозиторий. Можно ли дать GigaCode файл вне папки пакета, в
пилоте не проверялось — копируйте источники в `sources/`.

## Шаг 3. Дайте GigaCode задачу

- **Где:** терминал A. Если сессия уже шла, завершите её (`/quit`) и
  запустите `gigacode` заново: у каждой задачи своя сессия.
- Проверьте режим: `/approval-mode default`.

### Стартовая фраза

**Напишите GigaCode** (замените значения в угловых скобках):

```text
Задача BCREQ <TASK-0002> по маршруту RG-BCREQ-v1. Ключ в Jira: <MANGO-123>.
Коротко: <одна-две фразы о том, чего хочет Заказчик>.
Источники: <список файлов в runs/TASK-0002/evidence/sources/ или ссылки Confluence>.

Правила работы:
1. Пиши файлы только в runs/<TASK-0002>/evidence/. Остальные файлы пакета не меняй.
2. Работаем по одному узлу. Порядок узлов и артефакты — routes/rg-bcreq-v1.yaml.
   Для каждого узла используй его навык из .gigacode/skills/ и контракт из contracts/.
3. После каждого артефакта остановись, назови файл и дай мне точную команду runner
   для терминала B. Сам команды не выполняй: переходы делаю я.
4. На узлах n0, n4, n7, n8, n10a, n12, n13 подготовь checkpoint-<узел>.md по
   templates/checkpoint-skeleton.md: что проверить, цитаты с locator, какое решение нужно.
5. Факт — только с дословной цитатой и locator источника. Без источника — пометь как
   гипотезу. Не придумывай продукты, числа и ссылки.
6. Не отправляй ничего Заказчику и во внешние системы.

Начни с узла n0: прочитай источники и предложи тип работы и продуктовую цепочку.
Файлы пока не пиши.
```

- **Ожидаемый результат:** GigaCode пересказывает задачу, предлагает тип
  работы (`mango-change`, `mango-kb`, `industry-practice` или
  `external-spec`) и одну или несколько продуктовых цепочек из
  `taxonomy/mango-products.yaml`, со ссылками на цитаты источников.
- **Проверьте:** GigaCode ничего не записал и не запускал команд.

Навыка, который сам ведёт задачу по всем узлам, в пакете нет: порядок задают
эта фраза и [таблица узлов](#шаг-5-пройдите-узлы-маршрута). Модель может
отступать от фразы — тогда напомните нужное правило по номеру
([О-9](01-junior-pilot.md#ограничения-текущей-версии-пакета)).

### Какие входные данные можно дать

| Вид (`kind` в A-IN) | Пример | Как передать GigaCode |
|---------------------|--------|-----------------------|
| `transcript` | Стенограмма встречи | Файл в `evidence/sources/`, в диалоге — `@runs/TASK-0002/evidence/sources/<файл>` |
| `document` | ТЗ, спецификация, статья KB | Файл в `evidence/sources/`; статья KB — из `$env:USERPROFILE\bcreq-pilot\kb-source\` (см. [KB](03-deploy-package.md#получите-базу-знаний-kb)) |
| `email` | Письмо Заказчика | Текст вставьте в диалог или сохраните файлом в `evidence/sources/` |
| `ticket` | Карточка Jira | Текст карточки вставьте в диалог |
| `system-export` | Выгрузка из системы | Файл в `evidence/sources/` |

Каждый источник получает уровень (`tier`): `ST-1-ATTACHED` — приложен к
задаче, `ST-2-CORPUS` — корпус знаний, `ST-3-PRODUCT-DOC` — документация
продукта, `ST-4-HUMAN` — ваш ответ в диалоге. Не передавайте GigaCode
персональные данные клиентов и секреты.

## Шаг 4. Подготовьте и подтвердите вход A-IN

Узел `n0` — первая и главная проверка: к какому продукту относится задача.
Без вашего подтверждения маршрут дальше не пойдёт.

1. **Напишите GigaCode:**

   ```text
   /skills product-attribution
   Запиши вход runs/TASK-0002/evidence/A-IN.json по contracts/c-in.schema.json.
   Образец формы — A-IN.json из docs/guides/04-smoke-test.md, шаг 2.
   task: id "TASK-0002", title "<MANGO-123: краткое название>", requested_by "<ваш логин>".
   "state": "raw", "language": "ru", work_type и routing.rule — предложенный тип работы,
   routing.decision "pending", routing.decision_ref "evidence/checkpoint-n0.md",
   product_attribution: {"status": "pending"}.
   Все источники — в sources[] с id SRC-NN, kind, tier и locator.
   ```

   Разрешите запись файла.
2. **Выполните в терминале B** — переход `entry → n0`:

   ```powershell
   python tools/run-task.py advance TASK-0002 --to n0 --artifact runs/TASK-0002/evidence/A-IN.json
   ```

   **Ожидаемый результат:** `TASK-0002: entry -> n0; G-mach exit 0; trace seq 1`
3. **Проверьте цепочку.** Для каждой цепочки в `products` убедитесь, что
   домен, возможность, функция, атомарная функция, профиль и владелец
   верны. Спорное уточните в диалоге: «Почему `crm-connectors`, а не …?
   Покажи цитату».
4. **Посчитайте контрольную сумму** цепочки в терминале B — команда
   [«Посчитать binding_digest»](05-commands-reference.md#посчитать-binding_digest)
   (в конце команды замените путь на `runs/TASK-0002/evidence/A-IN.json`:
   файла `A-IN-confirmed.json` ещё нет). Скопируйте результат `sha256:…`.
5. **Напишите GigaCode:**

   ```text
   Я подтверждаю продуктовую цепочку. Запиши runs/TASK-0002/evidence/A-IN-confirmed.json —
   копию A-IN.json, где routing.decision "confirmed", а product_attribution:
   status "confirmed", confirmed_by "<ваш логин>", confirmed_at "<дата и время UTC, например 2026-09-29T12:00:00Z>",
   decision_ref "evidence/checkpoint-n0.md", binding_digest "<вставьте sha256:…>".
   Массив products не меняй. Затем подготовь checkpoint-n0.md.
   ```

6. **Выполните в терминале B** «Проверить вход A-IN»:

   ```powershell
   python tools/validate-package.py --input runs/TASK-0002/evidence/A-IN-confirmed.json
   ```

   **Ожидаемый результат:** `G-mach: пакет принят …`. Если есть
   `ERROR:` — передайте строки GigaCode и повторите этот пункт. Задача при
   этом не блокируется.
7. **Выполните в терминале B** переход `n0 → n1` с подтверждением:

   ```powershell
   python tools/run-task.py advance TASK-0002 --to n1 --artifact runs/TASK-0002/evidence/A-IN-confirmed.json --checkpoint runs/TASK-0002/evidence/checkpoint-n0.md
   ```

   Прочитайте checkpoint, введите строку `APPROVE TASK-0002:n0 sha256:…`
   ([как](05-commands-reference.md#выполнить-переход)).
   **Ожидаемый результат:** `TASK-0002: n0 -> n1; G-mach exit 0; trace seq 2`

Если тип работы `external-spec` (оценка внешнего ТЗ), runner направит
задачу в `handoff-p08`: это другой процесс, BCREQ по ней не формируется.
Переход выполняется командой `--to handoff-p08` на шаге 7.

## Шаг 5. Пройдите узлы маршрута

Для каждого узла **напишите GigaCode** по образцу:

```text
/skills <навык узла>
Узел <nX> задачи TASK-0002. Подготовь артефакт узла в runs/TASK-0002/evidence/<файл>.
```

Затем **выполните в терминале B** переход по образцу (для узлов с G-human
добавьте `--checkpoint runs/TASK-0002/evidence/checkpoint-<nX>.md` и
введите строку подтверждения):

```powershell
python tools/run-task.py advance TASK-0002 --to <следующий узел> --artifact runs/TASK-0002/evidence/<файл>
```

Навыки узлов описывают результат для человека, а runner на части узлов
требует JSON по контракту
([О-10](01-junior-pilot.md#ограничения-текущей-версии-пакета)). Столбец
«Файл для runner» показывает, что именно передавать в `--artifact`. Если
навык подготовил Markdown там, где нужен JSON, попросите: «Запиши этот
результат в JSON по contracts/<схема>».

| Узел | Навык | Файл для runner (`--artifact`) | Формат | `--to` | G-human |
|------|-------|--------------------------------|--------|--------|---------|
| `n1` | `transcript-normalization` | `normalized-text.md` | Текст | `n2` | — |
| `n2` | `context-extraction` | `marked-elements.md` | Текст | `n3` | — |
| `n3` | `ambiguity-detection` | `ambiguities.md` | Текст | `n4` | — |
| `n4` | `core-assembly` | `A-CORE.json` | JSON, `contracts/c-core.schema.json` | `n5`, если в `ambiguities` есть `"severity": "blocker"`; иначе `n9` | Да: источники и каждая цитата |
| `n5` | `question-formation` | `A-QUEST.json` | JSON, `contracts/c-quest.schema.json` | `n6` | — |
| `n6` | `question-prioritization` | `A-QUEST-prioritized.json` | JSON, `contracts/c-quest.schema.json` | `n7` | — |
| `n7` | Нет: вопросы Заказчику отправляете вы | `answers.json` | JSON `{"answers": [...]}` | `n8` | Да: отправка санкционирована |
| `n8` | `answer-integration` | `A-CORE-answers.json` | JSON, `contracts/c-core.schema.json` | `n9`; `n5`, если остались `blocker` без `resolved_by` | Да |
| `n9` | `problem-statement` | `problem-statement.md` | Текст | `n10` | — |
| `n10` | `value-hypothesis` | `value-hypothesis.md` | Текст | `n10a` | — |
| `n10a` | `bcreq-preflight` | `preflight.json` | JSON `{"preflight_registers": {"valid": true}}` | `n11`; при `false` — `halt` | Да: реестры до FR/UC/NFR |
| `n11` | `bcreq-decomposition` | `bcreq-items.md` | Текст | `n12` | — |
| `n12`, `n13` | `bcreq-assembly`, `bcreq-release` | См. [шаг 6](#шаг-6-запечатайте-working-и-соберите-release) | JSON | `n13`, `exit` | Да |

Особые узлы:

- **`n4`.** Куда идти, решает runner по `ambiguities` в A-CORE: при
  неверном `--to` он ответит `predicate selects n9, not n5` и заблокирует
  задачу. Посмотрите в A-CORE, есть ли `"severity": "blocker"`, до
  перехода.
- **`n7`.** Вопросы из A-QUEST отправляете Заказчику вы — агент этого не
  делает. Пока ответов нет, переход **не выполняйте**: задача ждёт на `n7`
  сколько угодно. Когда ответы пришли, попросите GigaCode записать их в
  `answers.json` дословно, с источником `ST-4-HUMAN`. Переход с пустым
  массивом `answers` уводит задачу в `halt`, и она заканчивается.
- **`n10a`.** GigaCode готовит реестры (источники, цель, задачи, as-is →
  delta, привязка, claims) в `preflight.md` и checkpoint. Поставьте
  `"valid": true` в `preflight.json`, только если согласны с реестрами:
  `false` останавливает задачу (`halt`).

## Шаг 6. Запечатайте Working и соберите Release

Узлы `n12` и `n13` работают с машинными файлами: черновиком
[Working](01-junior-pilot.md#term-working) и Release.

1. **Напишите GigaCode:**

   ```text
   /skills bcreq-assembly
   Узел n12 задачи TASK-0002. Запиши runs/TASK-0002/evidence/working.json строго по
   contracts/c-working-bcreq.schema.json ("state": "approved", "projection": "working")
   из утверждённых артефактов прошлых узлов. В evidence[].excerpt — дословные цитаты.
   Поля checksum и working_digest заполни значением "sha256:" и 64 нулями: их пересчитаю я.
   ```

2. **Выполните в терминале B** [«Запечатать Working»](05-commands-reference.md#запечатать-working)
   для `runs/TASK-0002/evidence/working.json`.
   **Ожидаемый результат:** `sealed: runs/TASK-0002/evidence/working.json`
3. **Выполните в терминале B** «Проверить Working»:

   ```powershell
   python tools/bcreq_pipeline.py validate-working runs/TASK-0002/evidence/working.json
   ```

   **Ожидаемый результат:** `G-mach: BCREQ accepted`. Если есть строки
   `ERROR:`, передайте их GigaCode («Исправь в working.json: <строки>»),
   затем снова пункты 2 и 3. **После каждой правки — снова запечатать.**
4. **Напишите GigaCode:** «Подготовь checkpoint-n12.md: что входит в
   требования, что не входит, открытые вопросы». Прочитайте его.
5. **Выполните в терминале B** переход `n12 → n13`:

   ```powershell
   python tools/run-task.py advance TASK-0002 --to n13 --artifact runs/TASK-0002/evidence/working.json --checkpoint runs/TASK-0002/evidence/checkpoint-n12.md
   ```

   Введите строку подтверждения. **Ожидаемый результат:**
   `TASK-0002: n12 -> n13; G-mach exit 0; trace seq …`
6. **Выполните в терминале B** «Собрать Release» и «Проверить Release»:

   ```powershell
   python tools/bcreq_pipeline.py compile runs/TASK-0002/evidence/working.json --output runs/TASK-0002/release
   python tools/bcreq_pipeline.py validate-release runs/TASK-0002/evidence/working.json --release runs/TASK-0002/release/release.json --manifest runs/TASK-0002/release/release-manifest.json
   ```

   **Ожидаемый результат:** обе команды печатают `G-mach: BCREQ accepted`.
7. **Напишите GigaCode:**

   ```text
   /skills bcreq-release
   Узел n13 задачи TASK-0002. Прочитай runs/TASK-0002/release/release.json и подготовь
   checkpoint-n13.md для решения о публикации. Release не меняй.
   ```

8. **Выполните в терминале B** переход `n13 → exit`:

   ```powershell
   python tools/run-task.py advance TASK-0002 --to exit --artifact runs/TASK-0002/release/release.json --working runs/TASK-0002/evidence/working.json --manifest runs/TASK-0002/release/release-manifest.json --checkpoint runs/TASK-0002/evidence/checkpoint-n13.md
   ```

   Введите строку подтверждения только после [шага 7](#шаг-7-проверьте-результат-и-примите-решение).
   **Ожидаемый результат:** `TASK-0002: n13 -> exit; G-mach exit 0; trace seq …`
9. **Выполните в терминале B** «Показать состояние задачи»:
   `python tools/run-task.py metrics TASK-0002`. **Ожидаемый результат:**
   `"current": "exit"`, `"status": "completed"`, `"deterministic_share": 1.0`.

## Шаг 7. Проверьте результат и примите решение

Machine-проверка (G-mach) подтверждает форму, ссылки и контрольные суммы.
Смысл проверяете вы: это [G-human](01-junior-pilot.md#term-g-human).

1. **Напишите GigaCode** в режиме `/approval-mode plan`:

   ```text
   Прочитай runs/TASK-0002/release/release.json и перескажи по пунктам:
   что получит клиент, что не входит в изменение, какие открытые вопросы остались.
   Для каждого требования дай источник и дословную цитату.
   ```

2. Пройдите чек-лист `evaluation/g-human-checklist.md`: смысл проблемы,
   гипотеза ценности, границы, цитаты, открытые вопросы, проекция документа.
3. Примите решение:

| Решение | Что сделать |
|---------|-------------|
| Принять | Введите строку подтверждения на переходе `n13 → exit` |
| Нужны правки | Не вводите строку: нажмите `Ctrl+C`. Runner ответит `BLOCKED: human gate was not approved`, задача остановится. Исправьте Working и пройдите задачу с новым TASK ID ([контроль прогонов](05-commands-reference.md#контроль-прогонов-один-task-id--один-прогон)) |
| Отклонить | Так же прервите подтверждение и опишите причину в карточке задачи |

## Диалог с GigaCode: режимы и встроенные команды

Режимы подтверждений (`/approval-mode <режим>`,
[режим подтверждений](01-junior-pilot.md#term-approval-mode)):

| Режим | Что GigaCode может | Когда использовать |
|-------|--------------------|--------------------|
| `plan` | Только читать и отвечать | Обсуждение, пересказ, проверка результата |
| `default` | Предлагать правки и команды, каждую — с вашим подтверждением | Подготовка артефактов. **Основной режим пилота** |
| `auto-edit` | Править файлы без вопроса | **Не использовать в пилоте** |

Встроенные команды, которые пригодятся
([команда со слешем](01-junior-pilot.md#term-slash-command)):

| Команда | Что делает |
|---------|------------|
| `/skills <имя>` | Вызывает навык пакета, например `/skills core-assembly` |
| `/approval-mode <режим>` | Меняет режим подтверждений |
| `/model` | Показывает и меняет модель |
| `/mcp` | Показывает подключённые MCP-серверы (Confluence) |
| `/tools` | Показывает инструменты агента |
| `/compress` | Сжимает историю, когда диалог стал длинным |
| `/resume` | Возвращает прошлую сессию |
| `/clear` | Очищает экран и историю текущей сессии |
| `/stats` | Показывает статистику сессии |
| `/help` | Список команд |
| `/quit` | Выход |
| `@<путь>` | Вставляет файл в сообщение: `@runs/TASK-0002/evidence/A-CORE.json` |
| `!<команда>` | Выполняет команду оболочки. **Команды runner так не запускайте**: на узлах с G-human переход не пройдёт ([О-5](01-junior-pilot.md#ограничения-текущей-версии-пакета)) |

Если GigaCode просит выполнить команду (в том числе `python tools/run-task.py …`),
отклоните её и выполните сами в терминале B.

## Что ожидать от модели

- Модель может ошибаться в продуктовой цепочке, путать похожие функции и
  придумывать цитаты. Поэтому цитаты и цепочку проверяете вы, а G-mach
  проверяет, что цепочка есть в словаре и цитата совпадает с контрольной
  суммой.
- Модель может пропустить правило стартовой фразы или предложить сразу
  несколько узлов. Напомните: «Правило 2: один узел за раз».
- Длинный диалог модель «забывает». Выполните `/compress` или начните новую
  сессию: попросите «Покажи состояние задачи TASK-0002 по файлам
  runs/TASK-0002/» и продолжайте.
- Результат модели не детерминирован: одинаковый вопрос может дать разные
  ответы. Детерминированы только проверки и сборка Release.

## Разговорные формулировки и термины модели

| Модель пишет | Что это значит |
|--------------|----------------|
| «Атрибуция», «продуктовая привязка» | Цепочка домен → возможность → функция → атомарная функция |
| «Blocker», «неоднозначность уровня blocker» | Без ответа Заказчика требование не сформулировать; маршрут пойдёт через вопросы `n5`–`n8` |
| «Слот», `S-FR`, `S-AC` | Раздел документа: функциональные требования, критерии приёмки |
| «Baseline», «одобренная базовая линия» | Working со `"state": "approved"` и верным `working_digest` |
| «Проекция» | Вид документа для адресата: `working` — черновик, Release — для клиента |
| «Gate», «гейт» | [Контрольная точка](01-junior-pilot.md#term-gate) |

Если непонятно, спросите: «Объясни без терминов, что это значит для
Заказчика».

## Типичные ситуации

После любого `BLOCKED:` на `advance` задача остановлена: исправьте причину
и начните с новым TASK ID
([контроль прогонов](05-commands-reference.md#контроль-прогонов-один-task-id--один-прогон)).

| Сообщение runner | Причина | Что делать |
|------------------|---------|------------|
| `BLOCKED: task already exists; use a new task id` | Номер уже использован | Возьмите следующий номер |
| `BLOCKED: task id must have form TASK-NNNN` | Неверный формат номера | `TASK-` и ровно 4 цифры |
| `BLOCKED: package preflight failed: …` | Пакет не прошёл проверку | «Проверить пакет», см. [развёртывание](03-deploy-package.md#проверьте-целостность-пакета) |
| `BLOCKED: transition is absent from the route` | Такого перехода из текущего узла нет | «Показать состояние задачи» и [таблица узлов](05-commands-reference.md#процесс-формирования-бизнес-спецификации) |
| `BLOCKED: node artifact is missing` / `is empty` | Нет файла или он пуст | Проверьте путь в `--artifact` |
| `BLOCKED: A-IN belongs to another task` | `task.id` в A-IN — другой номер | Исправьте `task.id` |
| `BLOCKED: n0 requires confirmed product attribution` | В `--artifact` передан A-IN без подтверждения | Передайте `A-IN-confirmed.json` |
| `BLOCKED: predicate selects n9, not n5` | Неверный `--to` на развилке | Используйте узел, который назвал runner |
| `BLOCKED: human gate requires checkpoint` | Узел с G-human, а `--checkpoint` не указан | Добавьте `--checkpoint` |
| `BLOCKED: human checkpoint is missing or empty` | Файла checkpoint нет или он пуст | Попросите GigaCode подготовить checkpoint |
| `BLOCKED: human gate requires an interactive terminal` | Команда запущена через `!` в GigaCode или агентом | Запускайте в терминале B |
| `BLOCKED: human gate was not approved` | Строка подтверждения введена с ошибкой или прервана | Копируйте строку после `Type exactly: ` целиком |
| `BLOCKED: G-mach exited 1: …` | Проверка нашла ошибки в артефакте | Прочитайте `ERROR:` в сообщении или в `gate_output` журнала |
| `BLOCKED: Working baseline is not approved` | В Working нет `"state": "approved"` или `working_digest` | Запечатайте и проверьте Working |
| `BLOCKED: Release gate requires --working and --manifest` | На `n13` не указаны оба файла | Добавьте `--working` и `--manifest` |
| `BLOCKED: route or node artifact changed during gate` | Файл изменили во время проверки | Не правьте файлы, пока идёт команда |
| `BLOCKED: branch requires ambiguities array` (или `answers array`, `preflight_registers.valid`) | В JSON нет нужного поля | Попросите GigaCode добавить поле по контракту |
| `BLOCKED: task is blocked or finished` | Задача уже остановлена или завершена | Новый TASK ID |
| `BLOCKED: another runner command is active or its lock needs review` | Идёт другая команда runner для этой задачи или она прервалась | Дождитесь её. Если другой команды нет — к ответственному |
| `BLOCKED: runner state or trace is missing` | Задача не начата или её папка повреждена | Проверьте номер; начните задачу командой `start` |

## Передача результата

- Итог задачи — папка `runs/TASK-0002/`: `release/release.json`,
  `release/release-manifest.json`, `evidence/` и журнал `trace.jsonl`.
- Папка `runs/` исключена из Git (`.gitignore`), поэтому результаты задачи
  не уходят в репозиторий случайно. Передайте их так, как принято в
  команде: приложите к карточке задачи или положите в закрытый
  (private) репозиторий по указанию ответственного.
- **Не публикуйте** `runs/` в открытом репозитории: там цитаты из
  корпоративных источников.
- Решение о приёмке и его основание запишите в карточку задачи.

---

**Навигация:** [Содержание](README.md) · [Обзор и глоссарий](01-junior-pilot.md) ·
[1. Установка](02-install.md) · [2. Развёртывание](03-deploy-package.md) ·
[3. Учебный прогон](04-smoke-test.md) · **4. Работа с агентом** ·
[5. Команды и отладка](05-commands-reference.md)

← Назад: [3. Учебный прогон](04-smoke-test.md) · Далее: [5. Команды и отладка](05-commands-reference.md) →
