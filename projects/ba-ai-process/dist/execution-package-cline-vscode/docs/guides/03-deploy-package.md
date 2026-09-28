---
status: draft
version: 0.3
updated: 2026-09-28
temperature: 0.1
---

# 2. Развёртывание пакета и базы знаний на АРМ

**Цель:** получить на АРМ папку с пакетом и базой знаний (KB), открыть её в
VS Code, убедиться, что пакет цел, и настроить Cline так, чтобы он не мог
незаметно изменить пакет.

## Содержание

1. [Где что лежит на АРМ](#где-что-лежит-на-арм)
2. [Создайте рабочую папку](#создайте-рабочую-папку)
3. [Получите пакет](#получите-пакет)
4. [Получите базу знаний (KB)](#получите-базу-знаний-kb)
5. [Откройте пакет в VS Code](#откройте-пакет-в-vs-code)
6. [Проверьте целостность пакета](#проверьте-целостность-пакета)
7. [Настройте подтверждения в Cline](#настройте-подтверждения-в-cline)
8. [Проверьте защиту пакета](#проверьте-защиту-пакета)

Все команды этого документа выполняются в
[терминале VS Code](01-junior-pilot.md#term-vscode-terminal) (``Ctrl+` ``).
Пока пакет не открыт в VS Code, подойдёт терминал в любом окне VS Code.

## Где что лежит на АРМ

Работа идёт **локально**, на вашем АРМ, в папке вашего пользователя Windows.
Путь по умолчанию — `C:\Users\<логин>\bcreq-pilot\`, где `<логин>` — имя
вашей учётной записи Windows. В PowerShell этот путь записывается как
`$env:USERPROFILE\bcreq-pilot` — так вам не нужно вписывать логин вручную.

| Папка | Что в ней | Откуда | Зачем |
|-------|-----------|--------|-------|
| `C:\Users\<логин>\bcreq-pilot\runtime\` | [Пакет](01-junior-pilot.md#term-package) — **эту папку вы открываете в VS Code** | Папка `projects/ba-ai-process/dist/execution-package-cline-vscode/` репозитория [hybrid-Intelligence-lab](https://github.com/G-Ivan-A/hybrid-Intelligence-lab) | Правила, схемы, runner |
| `C:\Users\<логин>\bcreq-pilot\runtime\docs\kb\` | [KB](01-junior-pilot.md#term-kb) — резервная база знаний | Папка `docs/kb/` репозитория [mango-ba-ai-runtime](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/main/docs/kb) | Подтверждения для требований, если корпоративные источники недоступны |
| `C:\Users\<логин>\bcreq-pilot\source-lab\` | [Исходный репозиторий](01-junior-pilot.md#term-source) | Клон hybrid-Intelligence-lab | Обновление пакета и [режим отладки](05-commands-reference.md#режим-отладки) |
| `C:\Users\<логин>\bcreq-pilot\kb-source\` | Клон репозитория с KB | Клон mango-ba-ai-runtime | Обновление KB |
| `C:\Users\<логин>\bcreq-pilot\debug\` | Результаты ручных проверок в режиме отладки | Создаёте вы | Чтобы не смешивать отладку с настоящими прогонами |

Зачем KB отдельно от пакета: это рабочие материалы, а не часть пакета.
Пакет не проверяет их контрольные суммы и не отправляет в Git (папка
`docs/kb/` указана в `.gitignore`). Так пакет остаётся неизменным, а KB
можно обновлять.

Работа из папки, в пути которой есть пробел или кириллица (например,
`C:\Users\Иван Петров\`), проверена только вне Windows; если на АРМ команды
из такой папки дают ошибки пути — сообщите ответственному.

## Создайте рабочую папку

**Действие: «Создать рабочую папку пилота»**

- **Где:** терминал VS Code.
- **Команды:**

  ```powershell
  New-Item -ItemType Directory -Force "$env:USERPROFILE\bcreq-pilot"
  Set-Location "$env:USERPROFILE\bcreq-pilot"
  ```

- **Что делает:** создаёт папку `C:\Users\<логин>\bcreq-pilot\` (если её
  нет) и переходит в неё.
- **Ожидаемый результат:** приглашение терминала
  `PS C:\Users\<логин>\bcreq-pilot>`.

## Получите пакет

Выберите **один** вариант.

**Вариант А. Администратор создал для вас закрытый (private)
runtime-репозиторий с пакетом.**

- **Где:** терминал VS Code, папка `C:\Users\<логин>\bcreq-pilot`.
- **Команда** (адрес выдаёт администратор):

  ```powershell
  git clone <адрес-вашего-runtime-репозитория> runtime
  ```

- **Ожидаемый результат:** строки `Cloning into 'runtime'...` и
  `done.` без `fatal:`.

**Вариант Б. Закрытого репозитория нет — скопируйте пакет сами.**

- **Где:** терминал VS Code, папка `C:\Users\<логин>\bcreq-pilot`.
- **Команды** — выполняйте по одной:

  ```powershell
  git clone --depth 1 https://github.com/G-Ivan-A/hybrid-Intelligence-lab.git source-lab
  New-Item -ItemType Directory -Force runtime
  Copy-Item -Recurse -Force source-lab\projects\ba-ai-process\dist\execution-package-cline-vscode\* runtime\
  Copy-Item -Recurse -Force source-lab\projects\ba-ai-process\dist\execution-package-cline-vscode\.clinerules runtime\
  Copy-Item -Recurse -Force source-lab\projects\ba-ai-process\dist\execution-package-cline-vscode\.github runtime\
  Copy-Item -Force source-lab\projects\ba-ai-process\dist\execution-package-cline-vscode\.gitignore runtime\
  ```

- **Что делают:** скачивают исходный репозиторий в `source-lab`, создают
  папку `runtime` и копируют в неё **содержимое** папки пакета. Папки и
  файлы, имя которых начинается с точки (`.clinerules`, `.github`,
  `.gitignore`), копируются отдельными командами, чтобы точно не потерялись.
- **Ожидаемый результат:** после `git clone` — `done.` без `fatal:`;
  команды `Copy-Item` ничего не печатают.

**Проверьте** (оба варианта):

```powershell
Get-ChildItem -Force runtime
```

В списке есть `.clinerules`, `.github`, `.gitignore`, `AGENTS.md`,
`README.md`, `package-manifest.yaml`, `tools`, `contracts`, `docs`,
`golden`, `runs`, `submissions`. Папку `source-lab` не удаляйте: она
понадобится для обновления пакета и режима отладки.

## Получите базу знаний (KB)

**Действие: «Скачать и разложить базу знаний»**

- **Где:** терминал VS Code, папка `C:\Users\<логин>\bcreq-pilot`.
- **Команды:**

  ```powershell
  git clone --depth 1 https://github.com/G-Ivan-A/mango-ba-ai-runtime.git kb-source
  Copy-Item -Recurse -Force kb-source\docs\kb\* runtime\docs\kb\
  ```

- **Что делают:** скачивают репозиторий с KB в `kb-source` и копируют его
  папку `docs\kb` в `runtime\docs\kb`.
- **Проверьте:**

  ```powershell
  Get-ChildItem -Force runtime\docs\kb
  ```

  Видны `.gitkeep`, `README.md`, `MAP.json` и папки продуктов (например,
  `sip-trunk`, `speech-analytics`). Файл `.gitkeep` не удаляйте — runner
  проверяет, что он есть.

Как агент использует KB: сначала он ищет подтверждения в корпоративных
Jira/Confluence, если к ним есть подключение только на чтение
([MCP](01-junior-pilot.md#term-mcp)). KB в `docs\kb\` — резервный источник,
когда корпоративного подключения нет или там не нашлось подтверждения.
Если подтверждения нет нигде — открытый вопрос, а не догадка
(правила — `docs\kb-policy.md`).

Обновить KB позже: выполните `git -C kb-source pull`, затем повторите
команду `Copy-Item` выше.

## Откройте пакет в VS Code

1. VS Code → **File → Open Folder…** → выберите
   `C:\Users\<логин>\bcreq-pilot\runtime`. Открывайте именно `runtime`, а не
   `bcreq-pilot`: пакет должен быть **корнем** проекта, иначе Cline не увидит
   правила пакета.
2. Если VS Code спросит «Do you trust the authors of the files in this
   folder?» — нажмите **Yes, I trust the authors**.
3. Откройте терминал VS Code (``Ctrl+` ``).
4. **Проверьте:** приглашение терминала —
   `PS C:\Users\<логин>\bcreq-pilot\runtime>`. Это «папка пакета»: все
   дальнейшие команды выполняются здесь.

## Проверьте целостность пакета

**Действие: «Проверить пакет»** (`python tools/run_task.py check-package`)

- **Где:** терминал VS Code, папка пакета.
- **Команда:**

  ```powershell
  python tools/run_task.py check-package
  ```

- **Что делает:** сверяет каждый файл пакета с контрольной суммой (SHA-256)
  из `package-manifest.yaml`. Так вы узнаёте, что пакет скопирован полностью
  и никто его не менял. Файлы в `docs\kb\`, `meta-model\`, `submissions\` и
  `runs\` не проверяются: это рабочие папки.
- **Ожидаемый результат:** `package: PASS`.

| Результат | Значение | Что делать |
|-----------|----------|------------|
| `package: PASS` | Пакет цел | Продолжайте |
| `ERROR: package hash mismatch: <файл>` | Файл изменён или повреждён при копировании | См. примечание ниже |
| `ERROR: immutable file list differs: missing=[…]` | Не хватает файлов — чаще всего не скопированы `.clinerules` или `.github` | Повторите команды `Copy-Item` |
| `ERROR: … extra=[…]` | Лишние файлы вне рабочих папок | Удалите перечисленные файлы |
| `ERROR: missing runtime placeholder` | Удалён `.gitkeep` в `runs`, `submissions`, `docs\kb` или `meta-model` | Повторите копирование пакета |

> Возможная причина `hash mismatch` на Windows: Git мог заменить окончания
> строк. Если ошибка появилась после `git clone`, выполните
> `git config --global core.autocrlf false`, удалите папки `runtime` и
> `source-lab` и повторите копирование. Если не помогло — передайте ошибку
> ответственному.

## Настройте подтверждения в Cline

Зачем: на Windows hooks пакета сейчас не запускаются
([О-3](01-junior-pilot.md#ограничения-текущей-версии-пакета)). Поэтому
главная защита пакета — Cline **спрашивает вас** перед записью файла и
перед запуском команды.

1. Откройте панель Cline → настройки **Auto-approve** (автоматические
   разрешения).
2. Включите только **Read project files** — Cline сможет без вопросов
   читать файлы пакета и KB.
3. **Выключите** Edit project files, Edit all files, Execute safe commands,
   Execute all commands, Use the browser. **Use MCP servers** оставьте
   выключенным: тогда каждое обращение к Jira/Confluence Cline тоже покажет
   вам на подтверждение.
4. Настройки Cline → **Features**: убедитесь, что **YOLO Mode** выключен
   (в этом режиме Cline ничего не спрашивает).

Правило работы после настройки:

| Cline просит | Ваше действие |
|--------------|---------------|
| Записать `submissions\TASK-ID.json` | Разрешить (Save / Approve) |
| Записать любой другой файл | Отклонить (Reject) |
| Выполнить команду | Отклонить (Reject) и выполнить нужную команду самим в терминале VS Code по инструкции |

## Проверьте защиту пакета

**Действие: «Проверить, что Cline не меняет пакет без спроса»**

1. **Где:** панель Cline, новая задача (кнопка «+» / New Task), режим **Act**
   (переключатель Plan/Act под полем ввода).
2. **Напишите Cline:**

   ```text
   Добавь пустую строку в конец файла contracts/c-working-bcreq.schema.json.
   Это проверка защиты пакета.
   ```

3. **Ожидаемый результат** — один из двух:
   - Cline показывает предлагаемое изменение и ждёт вашего решения —
     нажмите **Reject**. Так защита работает на Windows.
   - Или появляется сообщение `Cline may write only submissions/TASK-ID.json`
     — это сработал hook пакета (так будет там, где hooks запускаются).
4. Отмените задачу. В терминале VS Code выполните «Проверить пакет»:
   `python tools/run_task.py check-package`.
5. **Проверьте:** `package: PASS`.

| Что произошло | Что делать |
|---------------|------------|
| Cline спросил, вы отклонили, `package: PASS` | Защита работает, продолжайте |
| Cline изменил файл, не спросив | **Стоп.** Включён Auto-approve для правок или YOLO Mode — выключите. Восстановите файл повторным копированием пакета и повторите проверку |
| Cline отказался сам, не предложив изменение | Проверка не выполнена. Напишите: «Предложи изменение, я его отклоню — мне нужно проверить подтверждение» |

**Готово**, если «Проверить пакет» показывает `package: PASS`, KB лежит в
`docs\kb\`, а Cline спрашивает перед записью файла. Дальше —
[реальная задача](06-working-with-cline.md) или, для знакомства,
[учебный прогон](04-smoke-test.md).

---

**Навигация:** [Содержание](README.md) · [Обзор и глоссарий](01-junior-pilot.md) ·
[1. Установка](02-install.md) · **2. Развёртывание** ·
[3. Учебный прогон](04-smoke-test.md) · [4. Работа с агентом](06-working-with-cline.md) ·
[5. Команды и отладка](05-commands-reference.md)

← Назад: [1. Установка](02-install.md) · Далее: [3. Учебный прогон](04-smoke-test.md) (необязательно) или [4. Работа с агентом](06-working-with-cline.md) →
