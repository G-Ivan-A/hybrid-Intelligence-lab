---
status: draft
version: 0.5
updated: 2026-10-07
temperature: 0.1
---

# 1. Установка ПО на АРМ и проверка

**Цель:** установить четыре программы и убедиться, что они работают. Задачи
на этом шаге не запускаются, файлы пакета не нужны.

## Содержание

1. [Что установить и зачем](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/02-install.md#что-установить-и-зачем)
2. [Установка на Windows 10/11 x64](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/02-install.md#установка-на-windows-1011-x64)
3. [Терминал Git Bash в VS Code](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/02-install.md#терминал-git-bash-в-vs-code)
4. [Подключение модели в Cline](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/02-install.md#подключение-модели-в-cline)
5. [Команды из инструкции AI Core](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/02-install.md#команды-из-инструкции-ai-core)
6. [Проверка установки](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/02-install.md#проверка-установки)
7. [Если что-то не так](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/02-install.md#если-что-то-не-так)

## Что установить и зачем

| Программа | Зачем | Что ставить дополнительно |
|-----------|-------|---------------------------|
| [VS Code](https://code.visualstudio.com/download) | Редактор: в нём открыт пакет, [терминал VS Code](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-vscode-terminal) и [панель Cline](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-cline-panel) | Ничего |
| [Cline](https://docs.cline.bot/getting-started/installing-cline) | Расширение VS Code — ИИ-агент, с которым вы ведёте диалог | Ничего |
| [Git](https://git-scm.com/download/win) | Скачать пакет и базу знаний; Git Bash из состава Git — терминал для всех команд инструкций | Ничего |
| [Python 3.11 или новее](https://www.python.org/downloads/windows/) | На Python написаны [runner](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-runner) и проверки пакета | **Ничего.** Runner использует только стандартную библиотеку, которая входит в установщик Python. Команду `pip install` выполнять не нужно |

Если на АРМ нет прав администратора, попросите администратора установить
программы из корпоративного каталога ПО.

## Установка на Windows 10/11 x64

1. **VS Code.** Скачайте «Windows x64 User Installer», запустите. На шаге
   «Дополнительные задачи» отметьте «Добавить в PATH».
2. **Git.** Если Git уже установлен на АРМ, повторно ставить его не нужно.
   Иначе скачайте «64-bit Git for Windows Setup» и установите с настройками
   по умолчанию. Git Bash входит в Git; все команды инструкций выполняются
   в нём.
3. **Python.** Скачайте «Windows installer (64-bit)» версии 3.11 или новее.
   На первом экране **обязательно** отметьте **Add python.exe to PATH**, затем
   нажмите **Install Now**.
4. **Cline 4.1.21.** Откройте VS Code → на левой панели значок Extensions
   (`Ctrl+Shift+X`) → в поиске введите **Cline** (издатель — Cline) →
   **Install**. Если установлена другая версия, откройте меню шестерёнки
   расширения → **Install Another Version…** → `4.1.21`. На левой панели
   появится значок Cline.
5. Закройте VS Code и откройте снова, чтобы он увидел новые программы.

## Терминал Git Bash в VS Code

Зачем: команды инструкций написаны для Git Bash — того же терминала, в
котором вы уже работаете с `git`. VS Code сам находит Git Bash, если Git
установлен; достаточно один раз выбрать его терминалом по умолчанию.

1. В VS Code нажмите `Ctrl+Shift+P`, введите `Terminal: Select Default Profile`
   и выберите эту команду.
2. В списке выберите **Git Bash**.
3. Если терминал уже открыт, закройте его значком корзины и откройте новый
   (``Ctrl+` ``).
4. **Проверьте:** справа вверху терминала написано **bash**, над строкой
   ввода — строка вида `<логин>@<компьютер> MINGW64 ~`, сама строка ввода
   начинается с `$`.

Если **Git Bash** нет в списке, Git не установлен или VS Code запущен до
установки Git: выполните шаг 2 установки и перезапустите VS Code.

Пути в Git Bash записываются через `/`, а диск — как `/c`:

| В Проводнике Windows | В Git Bash |
|----------------------|------------|
| `C:\Users\<логин>` | `~` или `$HOME` (полный вид — `/c/Users/<логин>`) |
| `C:\Users\<логин>\bcreq-pilot\runtime` | `~/bcreq-pilot/runtime` |
| `D:\Мои задачи` | `"/d/Мои задачи"` — путь с пробелами берите в двойные кавычки |

## Подключение модели в Cline

Зачем: Cline сам по себе не содержит модель — он обращается к серверу
Mango AI ([модель](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-model)).

1. Откройте панель Cline (значок Cline на левой панели) → значок настроек
   (шестерёнка).
2. **API Provider:** `OpenAI Compatible`.
3. **Base URL:** адрес, выданный администратором AI Core.
4. **API Key:** ваш личный ключ `sk-…`.
5. **Model ID:** `gpu-default`.
6. **Context Window:** `114688`; **Max Output Tokens:** `16384`.
7. **Supports Images:** выключить.
8. Сохраните настройки. Для доступа к серверу может понадобиться VPN.

Ключ хранится только в настройках Cline. Не вставляйте его в чат, файлы и
снимки экрана.

## Команды из инструкции AI Core

Для Cline достаточно заполнить поля из раздела выше: **команды из инструкции
AI Core для терминала Cline не нужны**. Они настраивают консольные клиенты
модели и записаны для Linux и macOS: `&&`, `mkdir -p`, `printf`, `chmod`,
`~/…`, `/path/to/…`.

Если такие команды всё же понадобились на АРМ:

1. Выполняйте их только в **Git Bash**. Windows PowerShell 5.1 не понимает
   `&&`, а командная строка `cmd` — `mkdir -p`, `printf` и `~`.
2. Перед вставкой замените заглушку `sk-...` своим ключом. Кавычки вокруг
   ключа не удаляйте.
3. `~` в Git Bash — ваша папка профиля `C:\Users\<логин>`; файл
   `~/.<папка>/settings.json` окажется в `C:\Users\<логин>\.<папка>\settings.json`.
4. Вместо `cd /path/to/your-project` укажите реальную папку в записи Git Bash,
   например `cd ~/bcreq-pilot/runtime` (правило записи путей — в таблице
   раздела [Терминал Git Bash в VS Code](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/02-install.md#терминал-git-bash-в-vs-code)).
5. `chmod 600` в Git Bash завершается без ошибки, но права Windows на файл
   не меняет: Git для Windows подключает диски без поддержки прав POSIX
   (`noacl`). Доступ к файлу определяют права вашей папки профиля. Поэтому не
   кладите файл с ключом в папку пакета, в репозиторий или в общую папку и не
   отправляйте его в чат.

Другие модели (например, DeepSeek) подключить технически можно — см.
[Внешняя модель](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#можно-ли-подключить-внешнюю-модель-например-deepseek).
Для пилота используйте модель Mango AI.

## Проверка установки

### Проверить версии программ

- **Где:** [терминал VS Code](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-vscode-terminal)
  (``Ctrl+` ``). Папка пока не важна.
- **Команды** — по одной, после каждой нажмите Enter:

  ```bash
  code --version
  git --version
  python --version
  uname -s
  ```

  В заголовке расширения Cline проверьте версию `4.1.21`.

- **Ожидаемый результат:**

  | Команда | Что должно появиться |
  |---------|----------------------|
  | `code --version` | Номер версии VS Code, например `1.9x.x`, и строка `x64` |
  | `git --version` | `git version 2.x.x.windows.x` |
  | `python --version` | `Python 3.11.x` или новее (3.12, 3.13 …) |
  | `uname -s` | Строка, начинающаяся с `MINGW64_NT` — команды выполняются в Git Bash |

- **Проверьте:** ни одна команда не ответила `command not found`.

### Проверить связь с моделью

- **Где:** [панель Cline](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-cline-panel).
- **Напишите Cline:** `Ответь одним словом: готов`
- **Ожидаемый результат:** ответ модели в панели, например `Готов`.
- **Проверьте:** нет сообщения об ошибке 401/403 или таймауте. Файлы при
  этом не создаются и не меняются: это не задача, а проверка связи.

## Если что-то не так

| Симптом | Что сделать |
|---------|-------------|
| `python: command not found`, `Python was not found` или открывается Microsoft Store | Переустановите Python с галочкой **Add python.exe to PATH** и перезапустите VS Code. Либо используйте `py -3` вместо `python` во всех командах инструкции |
| `uname -s` показал не `MINGW64_NT…`, приглашение начинается с `PS`, или ошибка `The token '&&' is not a valid statement separator` | Терминал — PowerShell, а не Git Bash. Выполните шаги раздела [Терминал Git Bash в VS Code](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/02-install.md#терминал-git-bash-в-vs-code) и откройте новый терминал |
| `Python 3.10` или старше | Установите 3.11 или новее |
| `code` или `git` не найден | Перезапустите VS Code; если не помогло — переустановите с добавлением в PATH |
| Cline отвечает ошибкой 401/403 | Проверьте ключ; обратитесь к администратору AI Core |
| Cline не отвечает / таймаут | Включите VPN, проверьте Base URL |
| Cline пишет «Выполнение сценариев отключено в этой системе» или `Windows hook failed` | Cline сам запускает hooks пакета (`.ps1`) через Windows PowerShell с параметром `-ExecutionPolicy Bypass`; это сообщение значит, что сценарии запрещены групповой политикой или Python недоступен. Проверьте `python --version` в Git Bash и передайте текст администратору; не меняйте политику исполнения самостоятельно |

**Готово**, если команды показали версии, `uname -s` — `MINGW64_NT…`, и Cline ответил. Переходите к
[развёртыванию пакета](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/03-deploy-package.md).

---

**Навигация:** [Содержание](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/README.md) · [Обзор и глоссарий](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md) ·
**1. Установка** · [2. Развёртывание](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/03-deploy-package.md) ·
[3. Учебный прогон](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/04-smoke-test.md) · [4. Работа с агентом](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md) ·
[5. Команды и отладка](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md)

← Назад: [Обзор и глоссарий](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md) · Далее: [2. Развёртывание](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/abd20fa7fac5750edf0af78f2c87999676368bdf/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/03-deploy-package.md) →
