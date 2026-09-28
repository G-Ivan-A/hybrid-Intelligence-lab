---
status: draft
version: 0.2
updated: 2026-09-28
temperature: 0.1
---

# Шаг 2. Развёртывание пакета и базы знаний на АРМ

**Цель:** получить на АРМ рабочую папку с пакетом, положить в неё KB, открыть
в VS Code и убедиться, что пакет цел.

Назад: [установка](02-install.md) · Далее: [тестовый прогон](04-smoke-test.md)

## Содержание

1. [Как всё устроено](#как-всё-устроено)
2. [Получите пакет](#получите-пакет)
3. [Скопируйте KB отдельно](#скопируйте-kb-отдельно)
4. [Откройте пакет в VS Code](#откройте-пакет-в-vs-code)
5. [Проверьте целостность пакета](#проверьте-целостность-пакета)

## Как всё устроено

Работа идёт **локально**, на вашем АРМ. Нужны два источника:

| Что | Откуда | Куда на АРМ |
|-----|--------|-------------|
| Пакет | папка `projects/ba-ai-process/dist/execution-package-cline-vscode/` репозитория [hybrid-Intelligence-lab](https://github.com/G-Ivan-A/hybrid-Intelligence-lab) | корень вашей рабочей папки, например `C:\work\bcreq-runtime\` |
| KB | папка `docs/kb/` репозитория [mango-ba-ai-runtime](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/main/docs/kb) | `docs\kb\` внутри рабочей папки |

Зачем KB отдельно: это рабочие материалы, а не часть пакета. Пакет не проверяет
их хэши и не отправляет их в Git (папка `docs/kb/` указана в `.gitignore`).
Так пакет остаётся неизменным, а KB можно обновлять.

Используйте короткий путь без пробелов и кириллицы, например `C:\work\`.

## Получите пакет

Если администратор уже создал для вас закрытый (private) runtime-репозиторий
с пакетом, просто склонируйте его и переходите к разделу про KB:

```powershell
cd C:\work
git clone <адрес-вашего-runtime-репозитория> bcreq-runtime
```

Иначе скопируйте пакет из исходного репозитория сами:

```powershell
mkdir C:\work -Force
cd C:\work
git clone --depth 1 https://github.com/G-Ivan-A/hybrid-Intelligence-lab.git source-lab
mkdir bcreq-runtime
Copy-Item -Recurse -Force source-lab\projects\ba-ai-process\dist\execution-package-cline-vscode\* bcreq-runtime\
Copy-Item -Recurse -Force source-lab\projects\ba-ai-process\dist\execution-package-cline-vscode\.clinerules bcreq-runtime\
Copy-Item -Recurse -Force source-lab\projects\ba-ai-process\dist\execution-package-cline-vscode\.github bcreq-runtime\
Copy-Item -Force source-lab\projects\ba-ai-process\dist\execution-package-cline-vscode\.gitignore bcreq-runtime\
```

Что важно: копируется **содержимое** папки пакета, включая скрытые
`.clinerules`, `.github` и `.gitignore` — поэтому их копируем отдельно.
Без `.clinerules` не будет hooks, без `.github` — проверки CI.

Проверьте, что скрытые папки на месте:

```powershell
cd C:\work\bcreq-runtime
Get-ChildItem -Force
```

В списке должны быть `.clinerules`, `.github`, `.gitignore`, `AGENTS.md`,
`README.md`, `package-manifest.yaml`, `tools`, `contracts` и другие папки.
Папку `source-lab` после копирования можно удалить.

## Скопируйте KB отдельно

KB скачивается в отдельную временную папку, затем её содержимое копируется в
`docs\kb\` пакета:

```powershell
cd C:\work
git clone --depth 1 https://github.com/G-Ivan-A/mango-ba-ai-runtime.git kb-source
Copy-Item -Recurse -Force kb-source\docs\kb\* bcreq-runtime\docs\kb\
```

Не удаляйте файл `docs\kb\.gitkeep` — runner проверяет, что он есть.

Проверьте:

```powershell
Get-ChildItem -Force C:\work\bcreq-runtime\docs\kb
```

Видны `.gitkeep`, `README.md`, `MAP.json` и папки продуктов
(например `sip-trunk`, `speech-analytics`) — KB на месте.

Как KB связана с пакетом: Cline ищет в `docs/kb/` подтверждения для
требований, если корпоративное подключение к Jira/Confluence недоступно.
Правила — в `docs/kb-policy.md`: у каждого утверждения должен быть точный
источник (путь к файлу и якорь), иначе — открытый вопрос, а не догадка.

Обновить KB позже: `cd C:\work\kb-source; git pull`, затем повторите
`Copy-Item`.

## Откройте пакет в VS Code

1. VS Code → **File → Open Folder…** → выберите `C:\work\bcreq-runtime`.
   Открывайте именно эту папку, а не `C:\work`: пакет должен быть
   **корнем** проекта, иначе Cline не увидит правила и hooks.
2. Если VS Code спросит «Do you trust the authors?» — ответьте **Yes, I trust**.
3. Откройте терминал (`Ctrl+``). В приглашении должен быть путь
   `C:\work\bcreq-runtime`.

## Проверьте целостность пакета

```powershell
python tools/run_task.py check-package
```

Что делает команда: сверяет каждый файл пакета с контрольной суммой (SHA-256)
из `package-manifest.yaml`. Так вы узнаёте, что пакет скопирован полностью
и никто его не менял.

| Результат | Значение |
|-----------|----------|
| `package: PASS` | Пакет цел, можно продолжать |
| `ERROR: package hash mismatch: <файл>` | Файл изменён или повреждён при копировании |
| `ERROR: immutable file list differs: missing=[…]` | Не хватает файлов — чаще всего не скопированы `.clinerules` или `.github` |
| `ERROR: … extra=[…]` | Лишние файлы вне разрешённых папок — удалите их |
| `ERROR: missing runtime placeholder` | Удалён `.gitkeep` в `runs`, `submissions`, `docs/kb` или `meta-model` |

Файлы в `docs/kb/`, `meta-model/`, `submissions/` и `runs/` проверка
не учитывает: это ваши рабочие папки.

> Возможная причина `hash mismatch` на Windows: Git мог заменить окончания
> строк. Если ошибка появилась после `git clone`, выполните
> `git config --global core.autocrlf false`, удалите папки и повторите
> копирование. Если не помогло — передайте ошибку ответственному.

Готово, если `check-package` показал `package: PASS`, а KB лежит в
`docs\kb\`. Переходите к [тестовому прогону](04-smoke-test.md).
