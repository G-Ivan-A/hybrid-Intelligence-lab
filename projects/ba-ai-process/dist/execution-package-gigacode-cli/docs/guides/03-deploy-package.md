---
status: draft
version: 1.0
updated: 2026-09-29
temperature: 0.1
---

# 2. Развёртывание пакета и базы знаний на АРМ

**Цель:** получить на АРМ папку с пакетом и базой знаний (KB), установить
зависимости Python, убедиться, что пакет цел, и настроить GigaCode так,
чтобы он не мог незаметно изменить пакет.

## Содержание

1. [Где что лежит на АРМ](#где-что-лежит-на-арм)
2. [Создайте рабочую папку](#создайте-рабочую-папку)
3. [Получите пакет](#получите-пакет)
4. [Установите зависимости Python](#установите-зависимости-python)
5. [Проверьте целостность пакета](#проверьте-целостность-пакета)
6. [Получите базу знаний (KB)](#получите-базу-знаний-kb)
7. [Подключите Confluence через MCP (если разрешено)](#подключите-confluence-через-mcp-если-разрешено)
8. [Откройте два терминала](#откройте-два-терминала)
9. [Настройте подтверждения GigaCode](#настройте-подтверждения-gigacode)
10. [Проверьте защиту пакета](#проверьте-защиту-пакета)

Пока вы не дошли до раздела [Откройте два терминала](#откройте-два-терминала),
все команды выполняются в одном окне PowerShell: **Пуск → Windows
PowerShell**. Подойдёт и PowerShell 7 или вкладка PowerShell в Windows
Terminal.

## Где что лежит на АРМ

Работа идёт **локально**, в папке вашего пользователя. Путь по умолчанию —
`$env:USERPROFILE\bcreq-pilot\`. `$env:USERPROFILE` — это ваша папка
пользователя, обычно `C:\Users\<логин>`: PowerShell сам подставляет её в
командах.

| Папка | Что в ней | Откуда | Зачем |
|-------|-----------|--------|-------|
| `$env:USERPROFILE\bcreq-pilot\runtime\` | [Пакет](01-junior-pilot.md#term-package). **В этой папке вы запускаете `gigacode` и команды runner** | Папка `projects/ba-ai-process/dist/execution-package-gigacode-cli/` репозитория [hybrid-Intelligence-lab](https://github.com/G-Ivan-A/hybrid-Intelligence-lab) | Правила, схемы, навыки, runner |
| `$env:USERPROFILE\bcreq-pilot\kb-source\` | [KB](01-junior-pilot.md#term-kb) — база знаний о продуктах | Клон репозитория [mango-ba-ai-runtime-cli](https://github.com/G-Ivan-A/mango-ba-ai-runtime-cli) | Цитаты и подтверждения для требований |
| `$env:USERPROFILE\bcreq-pilot\source-lab\` | [Исходный репозиторий](01-junior-pilot.md#term-source) | Клон hybrid-Intelligence-lab | Обновление пакета и [режим отладки](05-commands-reference.md#режим-отладки) |

Почему `kb-source` лежит **рядом** с пакетом, а не внутри:
«Проверить пакет» сверяет с `package-manifest.yaml` каждый файл в `runtime\`,
кроме рабочих папок. Любой лишний файл в `runtime\` даёт ошибку
`immutable-выход не объявлен`, и runner перестаёт начинать задачи. Полная
копия KB в `runtime\docs\kb\` ломает проверку
([О-7](01-junior-pilot.md#ограничения-текущей-версии-пакета)).

## Создайте рабочую папку

**Действие: «Создать рабочую папку пилота»**

- **Где:** окно PowerShell.
- **Команды:**

  ```powershell
  New-Item -ItemType Directory -Force "$env:USERPROFILE\bcreq-pilot" | Out-Null
  Set-Location "$env:USERPROFILE\bcreq-pilot"
  ```

- **Что делает:** создаёт папку `bcreq-pilot` в вашей папке пользователя
  (если её нет) и переходит в неё.
- **Ожидаемый результат:** команды ничего не печатают, строка приглашения
  становится `PS C:\Users\<логин>\bcreq-pilot>`.
- **Проверьте:** `Get-Location` показывает путь, который заканчивается на
  `\bcreq-pilot`.

## Получите пакет

Выберите **один** вариант.

**Вариант А. Администратор создал для вас закрытый (private)
runtime-репозиторий с пакетом.**

- **Где:** PowerShell, папка `$env:USERPROFILE\bcreq-pilot`.
- **Команда** (адрес выдаёт администратор):

  ```powershell
  git clone <адрес-вашего-runtime-репозитория> runtime
  ```

- **Ожидаемый результат:** строка `Cloning into 'runtime'...` без `fatal:`.

**Вариант Б. Закрытого репозитория нет — скопируйте пакет сами.**

- **Где:** PowerShell, папка `$env:USERPROFILE\bcreq-pilot`. Папки
  `runtime` в ней ещё нет.
- **Команды** — выполняйте по одной:

  ```powershell
  git clone --depth 1 https://github.com/G-Ivan-A/hybrid-Intelligence-lab.git source-lab
  Copy-Item -Recurse -Force source-lab\projects\ba-ai-process\dist\execution-package-gigacode-cli runtime
  ```

- **Что делают:** скачивают исходный репозиторий в `source-lab` и копируют
  папку пакета целиком в новую папку `runtime`, включая папку `.gigacode`
  и файлы `.gitignore`, `.gitattributes`.
- **Ожидаемый результат:** после `git clone` нет строки `fatal:`, команда
  `Copy-Item` ничего не печатает.

Файл `.gitattributes` пакета запрещает Git менять окончания строк при
скачивании на Windows. Поэтому контрольные суммы файлов совпадают с
`package-manifest.yaml` в обоих вариантах.

**Проверьте** (оба варианта):

```powershell
Get-ChildItem -Force runtime
```

В списке есть `.gigacode`, `.gitattributes`, `.gitignore`, `AGENTS.md`, `README.md`,
`package-manifest.yaml`, `requirements.txt`, `tools`, `contracts`, `docs`,
`routes`, `golden`, `runs`. Папку `source-lab` не удаляйте: она понадобится
для обновления пакета и режима отладки.

## Установите зависимости Python

**Действие: «Установить зависимости пакета»**

- **Где:** PowerShell, папка `$env:USERPROFILE\bcreq-pilot`.
- **Команды:**

  ```powershell
  python -m pip install -r runtime/requirements.txt
  python -m pip show PyYAML jsonschema
  ```

- **Что делают:** первая ставит `PyYAML` и `jsonschema` точных версий из
  `requirements.txt` для Python, который отвечает на команду `python`.
  Права администратора не нужны: если Python установлен для всех
  пользователей, pip сам ставит библиотеки в ваш профиль и пишет
  `Defaulting to user installation`. Вторая показывает, что установлено.
- **Ожидаемый результат:** первая команда заканчивается строкой
  `Successfully installed …` с `PyYAML-6.0.3` и `jsonschema-4.26.0` (или
  сообщает `Requirement already satisfied`). Вторая печатает
  `Version: 6.0.3` для `PyYAML` и `Version: 4.26.0` для `jsonschema`.
- **Проверьте:** нет строк `ERROR:`. Предупреждение
  `WARNING: The script … is installed in '…' which is not on PATH` можно
  пропустить: пакет запускает библиотеки через `python`.

Библиотеки ставятся один раз: в новых окнах PowerShell ничего включать не
нужно. Если их нет, runner ответит
`ERROR: install pinned dependencies with pip install -r requirements.txt`.

## Проверьте целостность пакета

**Действие: «Проверить пакет»** (`python tools/validate-package.py`)

- **Где:** PowerShell, папка пакета.
- **Команды:**

  ```powershell
  Set-Location "$env:USERPROFILE\bcreq-pilot\runtime"
  python tools/validate-package.py
  ```

- **Что делает:** запускает [G-mach](01-junior-pilot.md#term-g-mach). Он
  сверяет каждый файл пакета с контрольной суммой (SHA-256) из
  `package-manifest.yaml` и проверяет навыки, маршрут, словари, схемы и
  эталоны. Так вы узнаёте, что пакет скопирован полностью и никто его не
  менял. Рабочие папки `runs/`, `docs/kb/`, `meta-model/` и
  `golden/candidates/`, а также локальный `.gigacode/settings.json` по
  контрольным суммам не сверяются.
- **Ожидаемый результат:**
  `G-mach: пакет принят (навыков: 16, узлов маршрута: 15).`

| Результат | Значение | Что делать |
|-----------|----------|------------|
| `G-mach: пакет принят …` | Пакет цел | Продолжайте |
| `ERROR: package-manifest.yaml: … hash …` или `объявленный immutable-выход отсутствует: <файл>` | Файл изменён, повреждён или не скопирован | Удалите `runtime` и повторите [копирование пакета](#получите-пакет) |
| `ERROR: package-manifest.yaml: immutable-выход не объявлен: <файл>` | В `runtime\` лежит лишний файл | Перенесите файл из `runtime\` (рабочие файлы задачи хранятся только в `runs\TASK-ID\evidence\`) |
| Много ошибок `hash` сразу после `git clone` | Git изменил окончания строк: в копии нет файла `.gitattributes` | Удалите `runtime`, проверьте, что в исходной папке пакета есть `.gitattributes`, и повторите [копирование пакета](#получите-пакет) |
| `ERROR: требуется PyYAML: pip install pyyaml` или `ERROR: install pinned dependencies with pip install -r requirements.txt` | Библиотеки не установлены для этого Python | Выполните [«Установить зависимости пакета»](#установите-зависимости-python) и повторите |
| Последняя строка `G-mach: пакет отвергнут, ошибок: N.` | Проверка не пройдена | Прочитайте строки `ERROR:` выше; если причина не из этой таблицы — передайте их ответственному |

## Получите базу знаний (KB)

**Действие: «Скачать базу знаний»**

- **Где:** PowerShell.
- **Команды:**

  ```powershell
  Set-Location "$env:USERPROFILE\bcreq-pilot"
  git clone --depth 1 https://github.com/G-Ivan-A/mango-ba-ai-runtime-cli.git kb-source
  Get-ChildItem kb-source\docs\kb
  ```

- **Что делают:** скачивают репозиторий с KB в `kb-source` — рядом с
  пакетом, а не внутри него — и показывают список продуктов.
- **Ожидаемый результат:** в списке есть `README.md`, `MAP.json` и папки
  продуктов, например `vpbx-api`, `sip-trunk`, `speech-analytics`.
- **Проверьте:** папки `runtime\docs\kb\` вы не трогали, и
  `python tools/validate-package.py` в папке пакета по-прежнему печатает
  `G-mach: пакет принят`.

**Не копируйте KB в `runtime\docs\kb\` целиком.** В ней тысячи
изображений и оглавления `index.md` со ссылками на документы исходного
репозитория. Проверка пакета читает все файлы `docs/kb/` и такую копию не
принимает, а runner перестаёт начинать задачи
([О-7](01-junior-pilot.md#ограничения-текущей-версии-пакета)).

Как дать агенту знание из KB — выберите удобный способ:

| Способ | Как | Когда |
|--------|-----|-------|
| Цитата в диалоге | Откройте статью из `kb-source\docs\kb\<продукт>\sections\` в Блокноте или другом редакторе и вставьте нужный фрагмент в диалог GigaCode вместе с именем файла | Нужно несколько цитат |
| Отдельные статьи в `docs\kb\` | Скопируйте **только** нужные файлы из `sections\` — см. команды ниже. Затем снова выполните «Проверить пакет» | Агент должен сам читать статьи продукта |
| Confluence через MCP | См. следующий раздел | Администратор разрешил подключение |

Пример: скопировать одну статью продукта `vpbx-api` и проверить пакет.

```powershell
Set-Location "$env:USERPROFILE\bcreq-pilot"
New-Item -ItemType Directory -Force runtime\docs\kb\vpbx-api | Out-Null
Copy-Item kb-source\docs\kb\vpbx-api\sections\02-osnovnye-svedeniya.md runtime\docs\kb\vpbx-api\
Set-Location runtime
python tools/validate-package.py
```

Статьи из `sections\` проходят проверку пакета, а файлы `index.md`,
изображения и `README.md` из KB — нет. Если после копирования «Проверить
пакет» показал ошибку в `docs\kb\`, удалите указанный файл.

Обновить KB позже можно командой
`git -C "$env:USERPROFILE\bcreq-pilot\kb-source" pull`.

## Подключите Confluence через MCP (если разрешено)

Пропустите этот раздел, если администратор не выдал команду подключения
Confluence MCP. Тогда цитаты вы вставляете в диалог сами.

**Действие: «Подключить Confluence»**

- **Где:** PowerShell, папка пакета `$env:USERPROFILE\bcreq-pilot\runtime`.
- **Команды:**

  ```powershell
  Copy-Item .gigacode\settings.example.json .gigacode\settings.json
  notepad .gigacode\settings.json
  ```

  В открывшемся Блокноте замените только два значения в блоке
  `confluence` и сохраните файл (`Ctrl+S`):

  | Поле | Было | Стало |
  |------|------|-------|
  | `command` (и при необходимости `args`) | `<approved-confluence-mcp-command>` | Команда из инструкции администратора |
  | `disabled` | `true` | `false` |

  Строку `"CONFLUENCE_TOKEN": "${CONFLUENCE_TOKEN}"` не меняйте: сам токен
  задаётся переменной окружения перед запуском `gigacode` в том же окне
  PowerShell:

  ```powershell
  $env:CONFLUENCE_TOKEN = '<токен-от-администратора>'
  gigacode mcp list
  ```

- **Что делает:** включает сервер `confluence` только для вашей копии
  пакета. Файл `.gigacode/settings.json` исключён из Git и не сверяется
  проверкой пакета. Токен остаётся в переменной окружения этого окна
  PowerShell и исчезает, когда вы его закрываете.
- **Ожидаемый результат:** `gigacode mcp list` показывает сервер
  `confluence` без статуса `Disconnected`.
- **Проверьте:** в `settings.json` нет токена открытым текстом. Статус
  `Disconnected` означает ошибку в команде или токене: передайте её
  администратору, не публикуя токен.

## Откройте два терминала

Дальше вы работаете в **двух** окнах PowerShell, оба — в папке пакета.
Второе окно откройте так же: **Пуск → Windows PowerShell**.

| Окно | Как подготовить | Для чего |
|------|-----------------|----------|
| [Терминал A](01-junior-pilot.md#term-terminal-a) | `Set-Location "$env:USERPROFILE\bcreq-pilot\runtime"`, затем (если нужен Confluence) `$env:CONFLUENCE_TOKEN = '…'`, затем `gigacode` | Диалог с агентом |
| [Терминал B](01-junior-pilot.md#term-terminal-b) | `Set-Location "$env:USERPROFILE\bcreq-pilot\runtime"` | Команды runner и проверки |

**Проверьте:** в терминале B команда `Get-Location` показывает путь, который
заканчивается на `\bcreq-pilot\runtime`, а в терминале A GigaCode ответил на
вопрос `Какой файл AGENTS.md ты видишь в текущей папке? Ответь одной строкой.`
названием `AGENTS.md спутника: исполнение маршрута RG-BCREQ-v1`.

## Настройте подтверждения GigaCode

Зачем: главная защита пакета — GigaCode **спрашивает вас** перед записью
файла и перед запуском команды.

- **Где:** терминал A.
- **Напишите GigaCode:** `/approval-mode default`
- **Что делает:** включает режим подтверждений
  ([режим подтверждений](01-junior-pilot.md#term-approval-mode)), в котором
  каждое изменение файла и каждую команду GigaCode показывает вам на
  решение. Режим `auto-edit` (правки без вопроса) в пилоте не используйте.
  Когда вы только обсуждаете задачу, удобен режим `/approval-mode plan`:
  GigaCode читает и отвечает, но ничего не меняет.

Правило работы после настройки:

| GigaCode просит | Ваше действие |
|-----------------|---------------|
| Записать файл в `runs/TASK-ID/evidence/` | Разрешить |
| Записать любой другой файл | Отклонить |
| Выполнить команду (в том числе `python tools/run-task.py …`) | Отклонить и выполнить нужную команду самим в терминале B по инструкции |

## Проверьте защиту пакета

**Действие: «Проверить, что GigaCode не меняет пакет без спроса»**

1. **Где:** терминал A, режим `/approval-mode default`.
2. **Напишите GigaCode:**

   ```text
   Добавь пустую строку в конец файла contracts/c-working-bcreq.schema.json.
   Это проверка защиты пакета.
   ```

3. **Ожидаемый результат:** GigaCode показывает предлагаемое изменение и
   спрашивает разрешения. **Отклоните** его.
4. В терминале B выполните «Проверить пакет»: `python tools/validate-package.py`.
5. **Проверьте:** `G-mach: пакет принят (навыков: 16, узлов маршрута: 15).`

| Что произошло | Что делать |
|---------------|------------|
| GigaCode спросил, вы отклонили, пакет принят | Защита работает, продолжайте |
| GigaCode изменил файл, не спросив | **Стоп.** Включён режим без подтверждений — выполните `/approval-mode default`. Восстановите пакет повторным копированием и повторите проверку |
| GigaCode отказался сам, не предложив изменение | Проверка не выполнена. Напишите: «Предложи изменение, я его отклоню — мне нужно проверить подтверждение» |

**Готово**, если «Проверить пакет» показывает `G-mach: пакет принят`, KB
лежит в `$env:USERPROFILE\bcreq-pilot\kb-source\`, открыты оба терминала, а GigaCode
спрашивает перед записью файла. Дальше —
[реальная задача](06-working-with-gigacode.md) или, для знакомства,
[учебный прогон](04-smoke-test.md).

---

**Навигация:** [Содержание](README.md) · [Обзор и глоссарий](01-junior-pilot.md) ·
[1. Установка](02-install.md) · **2. Развёртывание** ·
[3. Учебный прогон](04-smoke-test.md) · [4. Работа с агентом](06-working-with-gigacode.md) ·
[5. Команды и отладка](05-commands-reference.md)

← Назад: [1. Установка](02-install.md) · Далее: [3. Учебный прогон](04-smoke-test.md) (необязательно) или [4. Работа с агентом](06-working-with-gigacode.md) →
