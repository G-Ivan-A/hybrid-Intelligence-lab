---
status: draft
version: 0.5
updated: 2026-10-07
temperature: 0.1
---

# 5. Справочник команд и режим отладки

**Цель:** объяснить, какие действия есть в пакете, что делает каждая
команда, когда её выполнять и как понять результат; описать режим отладки.

В [режиме прогона](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-run-mode) этот справочник нужен
только как расшифровка: какую команду выполнить, подскажут
[инструкция по работе с агентом](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md) и сам Cline.

## Содержание

1. [Команды человеческим языком](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#команды-человеческим-языком)
2. [Описание команд](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#описание-команд)
3. [Контроль прогонов: один TASK ID — один прогон](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#контроль-прогонов-один-task-id--один-прогон)
4. [Процесс формирования бизнес-спецификации](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#процесс-формирования-бизнес-спецификации)
5. [Как читать журнал прогона (trace)](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#как-читать-журнал-прогона-trace)
6. [Папки пакета](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#папки-пакета)
7. [Режим отладки](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#режим-отладки)
8. [Чего в пилоте нет](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#чего-в-пилоте-нет)

## Команды человеческим языком

Все команды выполняются в
[терминале VS Code](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-vscode-terminal) (``Ctrl+` ``,
Git Bash) в папке пакета `C:\Users\<логин>\bcreq-pilot\runtime` — в Git Bash
`~/bcreq-pilot/runtime`. Проверить папку: строка над приглашением `$`
заканчивается на `MINGW64 ~/bcreq-pilot/runtime`.

| Действие | Команда (кратко) | Когда |
|----------|------------------|-------|
| [Проверить пакет](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#проверить-пакет) | `python tools/run_task.py check-package` | После развёртывания; при любых сомнениях в пакете |
| [Подготовить учебный пример](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#подготовить-учебный-пример) | `cp golden/TASK-0001.json submissions/TASK-0001.json` | Только для [учебного прогона](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/04-smoke-test.md) |
| [Запечатать черновик](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#запечатать-черновик) | `python tools/run_task.py seal submissions/TASK-ID.json` | После каждой правки черновика, перед проверкой |
| [Запустить проверку задачи](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#запустить-проверку-задачи) | `python tools/run_task.py run TASK-ID submissions/TASK-ID.json` | Черновик согласован и запечатан |
| [Убрать неудачный черновик](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#убрать-неудачный-черновик) | `mv submissions/TASK-ID.json runs/TASK-ID/working.json` | Проверка задачи дала `FAIL` |
| [Проверить всё перед отправкой](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#проверить-всё-перед-отправкой) | `python tools/run_task.py verify-ci` | Перед отправкой черновиков в Git |
| [Прочитать журнал прогона](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#прочитать-журнал-прогона) | открыть `runs/TASK-ID/trace.jsonl` | Непонятно, на каком шаге остановилась проверка |

`TASK-ID` в командах замените на свой номер, например `TASK-0002`.
Команды не меняют файлы пакета: они пишут только в `submissions/` и `runs/`.

## Описание команд

### Проверить пакет

- **Команда:** `python tools/run_task.py check-package`
- **Что делает:** сверяет каждый файл пакета с контрольными суммами из
  `package-manifest.yaml`. Файлы в `submissions/`, `runs/`, `docs/kb/`,
  `meta-model/` не проверяются — их менять можно.
- **Ожидаемый результат:** `package: PASS`.
- **Если иначе:** `ERROR: package hash mismatch: <файл>` — файл пакета
  изменён; `ERROR: immutable file list differs: missing=[…], extra=[…]` —
  файла не хватает (`missing`) или появился лишний (`extra`).
  Таблица действий — в [развёртывании](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/03-deploy-package.md).

Эту же проверку выполняют «Запустить проверку задачи» и «Проверить всё перед
отправкой» перед началом работы.

### Подготовить учебный пример

- **Команда:** `cp golden/TASK-0001.json submissions/TASK-0001.json`
- **Что делает:** копирует учебный черновик из `golden/` в `submissions/`.
- **Ожидаемый результат:** ничего не печатается; в `submissions/` появился
  `TASK-0001.json`.

### Запечатать черновик

- **Команда** (`TASK-0002` замените на свой номер):

  ```bash
  python tools/run_task.py seal submissions/TASK-0002.json
  ```

- **Что делает:** пересчитывает контрольные суммы черновика
  ([запечатывание](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-seal)): для каждой цитаты
  источника (`evidence`) и для черновика в целом (`working_digest`). Смысл
  черновика не меняется.
- **Зачем:** runner отклоняет черновик, если суммы не совпадают с
  содержимым. Так он замечает, что черновик изменили после согласования.
  Cline эти суммы надёжно посчитать не может.
- **Ожидаемый результат:** `sealed: submissions/TASK-0002.json`.
- **Важно:** запечатывайте **после** того, как в черновик записано ваше
  согласование, и заново — после любой правки.

### Запустить проверку задачи

- **Команда:** `python tools/run_task.py run TASK-0002 submissions/TASK-0002.json`
- **Что делает:** [runner](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-runner) проверяет пакет,
  затем по очереди — черновик (`validate-working`), собирает Release
  (`compile`) и проверяет Release (`validate-release`). Результаты пишет в
  `runs/TASK-0002/`.
- **Ожидаемый результат:** `TASK-0002: PASS`. В `runs/TASK-0002/` — файлы
  `trace.jsonl`, `release.json`, `release-manifest.json`.
- **Если иначе:** `TASK-0002: FAIL` и строки `ERROR: …` выше — черновик не
  прошёл; см. [типичные ситуации](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#типичные-ситуации).
  `ERROR: run already exists` — номер уже использован
  ([контроль прогонов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#контроль-прогонов-один-task-id--один-прогон)).

### Убрать неудачный черновик

- **Команда** (`TASK-0002` замените на свой номер):

  ```bash
  mv submissions/TASK-0002.json runs/TASK-0002/working.json
  ```

- **Что делает:** переносит черновик, не прошедший проверку, в папку его
  прогона. Черновик не теряется и лежит рядом с журналом.
- **Зачем:** «Проверить всё перед отправкой» проверяет **все** файлы в
  `submissions/` и даёт `FAIL`, если хотя бы один не проходит.
- **Ожидаемый результат:** ничего не печатается; файла нет в
  `submissions/`, он есть в `runs/TASK-0002/`.

### Проверить всё перед отправкой

- **Команда:** `python tools/run_task.py verify-ci`
- **Что делает:** то же, что CI после отправки в Git: во временной папке
  проверяет учебный пример и каждый файл в `submissions/`. Папку `runs/` не
  трогает.
- **Ожидаемый результат:** по строке на файл, все с `PASS`:

  ```text
  golden/TASK-0001.json: PASS
  submissions/TASK-0002.json: PASS
  ```

- **Если иначе:** строка с `FAIL` — уберите этот черновик
  ([команда](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#убрать-неудачный-черновик)).
  `ERROR: unexpected submission: <имя>` — в `submissions/` лежит файл не с
  именем `TASK-NNNN.json` (например, `BCREQ-123.json`); переименуйте его или
  уберите.

### Прочитать журнал прогона

- **Как:** откройте `runs/TASK-ID/trace.jsonl` в VS Code или **напишите
  Cline** (режим Plan): «Прочитай runs/TASK-0002/trace.jsonl и объясни по
  строкам, какой шаг не прошёл».
- Расшифровка — в разделе [Как читать журнал прогона](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#как-читать-журнал-прогона-trace).

## Контроль прогонов: один TASK ID — один прогон

**Правило.** Каждый запуск «Запустить проверку задачи» получает новый
[TASK ID](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-task-id). Повторный запуск с тем же
номером runner отклоняет: `ERROR: run already exists`.

**Зачем.** Папка `runs/TASK-ID/` — журнал именно этой попытки: какой черновик
проверялся (контрольная сумма), какая версия пакета, какой результат.
Если бы журнал можно было перезаписать, нельзя было бы доказать, что
проверено именно то, что согласовано.

**Что делать при повторной попытке:**

1. Уберите неудачный черновик: [команда](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#убрать-неудачный-черновик).
2. Исправленный черновик получает следующий свободный номер, например
   `submissions/TASK-0003.json`.
3. Запечатайте и запустите проверку с новым номером.
4. Для себя отметьте: «BCREQ-123 → TASK-0002 (FAIL), TASK-0003 (PASS)».

**Чего не делать:** не удаляйте папки `runs/` реальных задач и не
переименовывайте их. Удалять `runs/TASK-0001` допустимо только для
[учебного примера](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/04-smoke-test.md#повторить-учебный-прогон).

## Процесс формирования бизнес-спецификации

В пилоте один процесс — «Сформировать бизнес-спецификацию по задаче BCREQ»
(технический код `RG-BCREQ-v1/synthetic-working-release`, описание в
`routes/pilot.json`).

```text
 Вы + Cline (диалог)            Runner (машинная проверка, G-mach)          Вы (G-human)
 ─────────────────────          ─────────────────────────────────────       ──────────────
 входные данные → согласование  validate-working → compile → validate-release   чек-лист,
 → черновик submissions/…json   (черновик)        (сборка)  (Release)           решение
 → запечатать
```

- **Вход:** согласованный и запечатанный черновик BCREQ Working (JSON).
- **Выход:** BCREQ Release и его manifest в `runs/TASK-ID/`.
- **Если машинный шаг не прошёл:** следующие шаги не выполняются
  (`step_skipped`), проверка останавливается.
- **Если нет источника:** явная ошибка или открытый вопрос, но не догадка.
- **Открытые вопросы:** пока они есть, Release не собирается.
- **Проверка человеком:** чек-лист `evaluation/g-human-checklist.md`.

## Как читать журнал прогона (trace)

Файл `runs/TASK-ID/trace.jsonl` пишет только runner. Одна строка — один шаг.
Главные поля строки:

| Поле | Значение |
|------|----------|
| `node` | Шаг: `validate-working`, `compile`, `validate-release` или `G-human` |
| `state` | Что произошло с шагом (см. ниже) |
| `exit_code` | Итог программы шага: `0` — прошёл, `1` — не прошёл |
| `input_sha256` | Контрольная сумма проверенного черновика |
| `detail` | Пояснение |

Значения `state` простыми словами:

| `state` | Значит | Пример |
|---------|--------|--------|
| [`script_invoked`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-script-invoked) | Программа шага действительно запускалась. Прошла ли — смотрите `exit_code` | `validate-working`, `exit_code: 1` — черновик не прошёл проверку |
| [`step_skipped`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-step-skipped) | Шаг не выполнялся, потому что предыдущий не прошёл | `compile`, `detail: previous machine gate failed` |
| [`contract_mode`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-contract-mode) | Дальше нужна проверка человеком; машина её не делает и не засчитывает | Всегда последняя строка, `node: G-human` |

Журнал неудачного прогона (сокращённо):

```text
validate-working   script_invoked  exit_code 1
compile            step_skipped    previous machine gate failed
validate-release   step_skipped    previous machine gate failed
G-human            contract_mode   semantic and publication review required
```

Читается так: «черновик не прошёл проверку, Release не собирался, до
проверки человеком дело не дошло». Причину показывают строки `ERROR: …` в
терминале; в журнал текст ошибок не записывается.

## Папки пакета

| Папка или файл | Что это | Кто меняет |
|----------------|---------|------------|
| [`submissions/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-submissions) | Черновики задач `TASK-ID.json`. Единственная папка, куда пишет Cline | Вы и Cline (с вашего разрешения) |
| [`runs/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-runs) | Результаты прогонов `runs/TASK-ID/`. В Git не отправляется | Runner; вы — только перенос неудачного черновика |
| [`golden/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-golden) | Учебный пример `TASK-0001.json`, эталон для самопроверки пакета | Никто |
| `docs/kb/` | Локальная [база знаний](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-kb). В Git не отправляется | Вы (копирование KB) |
| `docs/kb-policy.md` | Правила выбора источников: сначала корпоративные, затем KB | Никто |
| `meta-model/` | Место для разрешённых материалов мета-модели. Runner его не читает | Вы, по указанию ответственного |
| `contracts/` | Правила формата черновика и Release (JSON-схемы) | Никто |
| `taxonomy/` | Справочники продуктов Mango и TMF для продуктовой привязки | Никто |
| `routes/pilot.json` | Описание процесса | Никто |
| `templates/working-prompt.md` | Базовый запрос для учебного черновика | Никто |
| `evaluation/g-human-checklist.md` | Ваш чек-лист проверки | Никто |
| `tools/` | Программы runner и проверок | Никто |
| `AGENTS.md`, `.clinerules/` | Правила для Cline | Никто |
| `package-manifest.yaml` | Контрольные суммы файлов пакета | Никто |

«Никто» означает: изменение ломает «Проверить пакет». Предложения по
изменению — через ответственного (см. [режим отладки](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/05-commands-reference.md#режим-отладки)).

## Режим отладки

[Режим прогона](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-run-mode) — диалог с Cline и три
готовые команды. [Режим отладки](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-debug-mode) нужен,
когда непонятно, **почему** проверка не проходит или почему агент ведёт
себя не так, как ожидается. В нём вы работаете с командами и файлами
напрямую.

### Как войти в режим отладки

Войти можно в любой момент: проверка задачи — одна команда, которая
завершается сама, поэтому прерывать ничего не нужно.

1. В панели Cline начните **новую** задачу (или `/newtask`, чтобы перенести
   краткое содержание текущей). Режим **Plan**.
2. **Напишите Cline:**

   ```text
   Режим отладки. Файлы не меняй, команды не запускай.
   Прогон: TASK-0002. Черновик: runs/TASK-0002/working.json
   (или submissions/TASK-0002.json).
   Ошибки runner: <вставьте строки ERROR>.
   Прочитай trace runs/TASK-0002/trace.jsonl, черновик и нужные схемы
   в contracts/. Объясни по пунктам: какой шаг не прошёл, какое поле
   черновика виновато и какое правило пакета его проверяет (файл и место).
   Предложи исправление, но не применяй.
   ```

3. Чтобы вернуться в режим прогона — продолжите исходную задачу Cline
   (список задач — кнопка истории в панели Cline) или начните новую со
   [стартовой фразы](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#стартовая-фраза).

### Отдельные машинные шаги

«Запустить проверку задачи» выполняет три шага подряд. В режиме отладки их
можно выполнить по одному, чтобы увидеть результат каждого. Ручные запуски
**в журнал не попадают** и прогоном не считаются; номер TASK ID они не
занимают.

Сначала создайте папку для отладочных результатов вне пакета (один раз):

```bash
mkdir -p "$HOME/bcreq-pilot/debug"
```

Затем выполните шаги по одному (строки блока — по порядку):

```bash
python tools/bcreq_pipeline.py validate-working submissions/TASK-0002.json
python tools/bcreq_pipeline.py compile submissions/TASK-0002.json --output "$HOME/bcreq-pilot/debug/TASK-0002"
python tools/bcreq_pipeline.py validate-release submissions/TASK-0002.json --release "$HOME/bcreq-pilot/debug/TASK-0002/release.json" --manifest "$HOME/bcreq-pilot/debug/TASK-0002/release-manifest.json"
```

| Шаг | Команда | Проверяет |
|-----|---------|-----------|
| Проверить черновик | `validate-working` (первая строка) | Формат, ссылки на источники, контрольные суммы, согласование |
| Собрать Release | `compile` (вторая строка) | Сборку Release в `~/bcreq-pilot/debug/TASK-0002/`; открытые вопросы её блокируют |
| Проверить Release | `validate-release` (третья строка) | Release соответствует черновику и формату |

- **Ожидаемый результат каждого шага:** `G-mach: BCREQ accepted`.
- **Если иначе:** строки `ERROR: …`. Первое слово строки указывает раздел
  правил (`BASELINE`, `EVID-03`, `RELEASE` …) — покажите строку Cline в
  режиме отладки.
- **Проверьте:** после отладки `python tools/run_task.py check-package`
  по-прежнему даёт `package: PASS`.

Пути `submissions/TASK-0002.json` замените на `runs/TASK-0002/working.json`,
если черновик уже убран.

### Если нужно изменить правила пакета

Файлы пакета в папке `runtime` не правьте: «Проверить пакет» это
обнаружит, а CI отклонит. Правила пакета собираются из исходников
([Source](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-source)) и
[мета-модели](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#term-meta-model). Если отладка показала,
что ошибка в правилах, а не в черновике:

1. Запишите: TASK ID, строки `ERROR`, фрагмент черновика, объяснение Cline.
2. Передайте ответственному за пакет. Изменение вносится в исходники
   (`source-lab`), пакет пересобирается и выдаётся заново.

Готовых отладочных сценариев для Cline в пакете нет
([О-5](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#ограничения-текущей-версии-пакета)): порядок выше —
обычный диалог и ручные команды.

## Чего в пилоте нет

- Нет других процессов, кроме «Сформировать бизнес-спецификацию по задаче
  BCREQ». Узлов вида `intake`, `source-scan` в пакете нет.
- Нет переменных окружения: TASK ID передаётся в команде.
- Нет команд пакета для Cline вида `/bcreq-…`
  ([О-4](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md#ограничения-текущей-версии-пакета)). Встроенные
  команды Cline (`/newtask`, `/smol`) работают, но процесс BCREQ не ведут;
  его ведёт [стартовая фраза](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md#стартовая-фраза), а
  проверки — команды из этого справочника.
- Корпоративное подключение Jira/Confluence **только на чтение** настраивает
  администратор в Cline (MCP Servers). Пока его нет — источник
  `docs/kb/` и текст, который вы вставили в диалог.

---

**Навигация:** [Содержание](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/README.md) · [Обзор и глоссарий](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/01-junior-pilot.md) ·
[1. Установка](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/02-install.md) · [2. Развёртывание](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/03-deploy-package.md) ·
[3. Учебный прогон](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/04-smoke-test.md) · [4. Работа с агентом](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md) ·
**5. Команды и отладка**

← Назад: [4. Работа с агентом](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/06-working-with-cline.md) · В начало: [Содержание](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/9a65744776a0e703dccbf742b226c1e155bcdd66/projects/ba-ai-process/build/adapters/cline-vscode/docs/guides/README.md)
