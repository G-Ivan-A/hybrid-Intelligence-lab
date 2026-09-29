---
status: draft
version: 1.0
updated: 2026-09-29
temperature: 0.1
---

# 5. Справочник команд и режим отладки

**Цель:** справочник. Все команды пакета — с человеческим названием, как
устроен маршрут, как читать журнал прогона и как разбирать сбои. Читать
целиком не обязательно: сюда ведут ссылки из других документов.

Все команды выполняются в [терминале B](01-junior-pilot.md#term-terminal-b)
— окне PowerShell в папке пакета `$env:USERPROFILE\bcreq-pilot\runtime`.
В примерах номер задачи — `TASK-0002`; подставьте свой. Пути в аргументах
`python` записаны через `/`: Windows понимает их так же, как `\`, и runner
печатает пути в том же виде.

## Содержание

1. [Команды человеческим языком](#команды-человеческим-языком)
2. [Описание команд](#описание-команд)
3. [Контроль прогонов: один TASK ID — один прогон](#контроль-прогонов-один-task-id--один-прогон)
4. [Процесс формирования бизнес-спецификации](#процесс-формирования-бизнес-спецификации)
5. [Как читать журнал прогона (trace)](#как-читать-журнал-прогона-trace)
6. [Папки пакета](#папки-пакета)
7. [Режим отладки](#режим-отладки)
8. [Чего в пилоте нет](#чего-в-пилоте-нет)

## Команды человеческим языком

| Человеческое название | Команда | Когда |
|-----------------------|---------|-------|
| [Проверить пакет](#проверить-пакет) | `python tools/validate-package.py` | После развёртывания, после копирования статей KB, при любом сомнении |
| [Начать задачу](#начать-задачу) | `python tools/run-task.py start TASK-0002` | Один раз в начале каждой задачи |
| [Выполнить переход](#выполнить-переход) | `python tools/run-task.py advance TASK-0002 --to <узел> --artifact <файл>` | Когда артефакт текущего узла готов |
| [Показать состояние задачи](#показать-состояние-задачи) | `python tools/run-task.py metrics TASK-0002` | В любой момент: где задача и сколько шагов подтверждено |
| [Проверить вход A-IN](#проверить-вход-a-in) | `python tools/validate-package.py --input <файл>` | До перехода `n0 → n1`, чтобы не заблокировать задачу |
| [Посчитать binding_digest](#посчитать-binding_digest) | `python -c "…"` (см. раздел) | При подтверждении продуктовой привязки на `n0` |
| [Запечатать Working](#запечатать-working) | `@' … '@ \| python - <файл>` (см. раздел) | После каждой правки `working.json` |
| [Проверить Working](#проверить-working) | `python tools/bcreq_pipeline.py validate-working <файл>` | После запечатывания, до перехода `n12 → n13` |
| [Собрать Release](#собрать-release) | `python tools/bcreq_pipeline.py compile <файл> --output runs/TASK-0002/release` | На узле `n13` |
| [Проверить Release](#проверить-release) | `python tools/bcreq_pipeline.py validate-release …` | После сборки, до перехода `n13 → exit` |

Три нижние команды и «Проверить вход A-IN» ничего не меняют в состоянии
задачи: это та же машинная проверка, которую runner запускает при переходе,
но без записи в журнал. Ошибку, найденную ими, можно исправить без потери
TASK ID.

## Описание команд

### Проверить пакет

- **Команда:** `python tools/validate-package.py`
- **Что делает:** запускает [G-mach](01-junior-pilot.md#term-g-mach):
  сверяет файлы пакета с контрольными суммами в `package-manifest.yaml` и
  проверяет навыки, маршрут, словари, схемы и эталоны.
- **Ожидаемый результат:**
  `G-mach: пакет принят (навыков: 16, узлов маршрута: 15).`
- **Если нет:** строки `ERROR: …` и последняя строка
  `G-mach: пакет отвергнут, ошибок: N.` Разбор частых ошибок — в
  [развёртывании](03-deploy-package.md#проверьте-целостность-пакета).

### Начать задачу

- **Команды:**

  ```powershell
  python tools/run-task.py start TASK-0002
  New-Item -ItemType Directory -Force runs\TASK-0002\evidence | Out-Null
  ```

- **Что делают:** runner проверяет пакет и создаёт `runs/TASK-0002/` с
  `state.json` (текущий узел `entry`) и пустым `trace.jsonl`. Вторая
  команда создаёт папку для файлов задачи.
- **Ожидаемый результат:**
  `TASK-0002: started at entry; next transition requires G-mach`
- **Отказы:** `BLOCKED: task already exists; use a new task id`,
  `BLOCKED: task id must have form TASK-NNNN`,
  `BLOCKED: package preflight failed: …` (пакет не прошёл проверку —
  выполните «Проверить пакет»).

### Выполнить переход

- **Команда (узел без G-human):**

  ```powershell
  python tools/run-task.py advance TASK-0002 --to n2 --artifact runs/TASK-0002/evidence/normalized-text.md
  ```

- **Команда (узел с G-human** — `n0`, `n4`, `n7`, `n8`, `n10a`, `n12`,
  `n13`**):** добавьте `--checkpoint runs/TASK-0002/evidence/checkpoint-<узел>.md`.
- **Что делает:** по порядку:
  1. проверяет, что переход из текущего узла в `--to` есть в маршруте;
  2. проверяет, что `--artifact` существует и не пуст, а на узлах `entry`,
     `n0`, `n4`, `n5`, `n6`, `n8`, `n12`, `n13` — что это JSON по
     контракту узла;
  3. для развилок сам вычисляет, куда должна идти задача, и отказывает,
     если `--to` другой (`predicate selects n9, not n5`);
  4. запускает G-mach (на `n0` — с `--input`, на `n12` — с `--working`, на
     `n13` — с `--working`, `--release`, `--manifest`);
  5. на узле с G-human печатает путь checkpoint и строку подтверждения и
     ждёт, пока вы её введёте;
  6. записывает строку в `trace.jsonl` и меняет текущий узел.
- **Ожидаемый результат:**
  `TASK-0002: n1 -> n2; G-mach exit 0; trace seq 3`
- **Подтверждение на узле с G-human.** После проверки runner печатает:

  ```text
  Review C:\Users\<логин>\bcreq-pilot\runtime\runs\TASK-0002\evidence\checkpoint-n0.md
  Type exactly: APPROVE TASK-0002:n0 sha256:<64 символа>
  ```

  Прочитайте checkpoint, скопируйте строку после `Type exactly: ` целиком,
  вставьте и нажмите Enter. В окне PowerShell строка копируется так:
  выделите её мышью и нажмите Enter (или `Ctrl+C`), вставляется — правой
  кнопкой мыши (или `Ctrl+V`). Контрольная сумма в строке — это SHA-256
  файла checkpoint: если его изменить, строка станет другой. Команда
  должна работать в обычном терминале, а не через `!` в GigaCode
  ([О-5](01-junior-pilot.md#ограничения-текущей-версии-пакета)).
- **Отказ:** `BLOCKED: <причина>`. Задача остановлена, см.
  [контроль прогонов](#контроль-прогонов-один-task-id--один-прогон) и
  [типичные ситуации](06-working-with-gigacode.md#типичные-ситуации).

### Показать состояние задачи

- **Команда:** `python tools/run-task.py metrics TASK-0002`
- **Ожидаемый результат** (пример после двух переходов):

  ```text
  {"current": "n1", "deterministic_share": 1.0, "deterministic_steps": 2, "expected_steps": 2, "status": "active", "task_id": "TASK-0002"}
  ```

| Поле | Значение |
|------|----------|
| `current` | Текущий узел |
| `status` | `active` — идёт, `blocked` — остановлена отказом, `completed` — дошла до `exit` |
| `expected_steps` | Сколько попыток перехода записано в журнал |
| `deterministic_steps` | Сколько из них подтверждено G-mach с кодом `0` |
| `deterministic_share` | Доля подтверждённых. `null` — переходов ещё не было, `1.0` — все подтверждены |

Сразу после «Начать задачу» результат —
`{"current": "entry", "deterministic_share": null, "deterministic_steps": 0, "expected_steps": 0, "status": "active", "task_id": "TASK-0002"}`.
После успешного выхода — `"current": "exit"`, `"status": "completed"`.

### Проверить вход A-IN

- **Команда:**
  `python tools/validate-package.py --input runs/TASK-0002/evidence/A-IN-confirmed.json`
- **Что делает:** то же, что «Проверить пакет», плюс проверку A-IN: схема
  `contracts/c-in.schema.json`, продуктовая цепочка по словарю
  `taxonomy/mango-products.yaml`, совпадение `binding_digest`.
- **Ожидаемый результат:** `G-mach: пакет принят …`.

### Посчитать binding_digest

- **Команда** (одной строкой):

  ```powershell
  python -c "import json,hashlib,sys; p=json.load(open(sys.argv[1],encoding='utf-8-sig'))['products']; print('sha256:'+hashlib.sha256(json.dumps(p,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest())" runs/TASK-0002/evidence/A-IN-confirmed.json
  ```

- **Что делает:** печатает контрольную сумму массива `products` из A-IN.
  Это значение записывается в `product_attribution.binding_digest` после
  того, как вы подтвердили продуктовую цепочку. Если цепочку потом
  изменить, сумма перестанет совпадать, и проверка входа это покажет.
- **Ожидаемый результат:** строка `sha256:` и 64 символа.

### Запечатать Working

В пакете нет отдельной команды для этого шага
([О-8](01-junior-pilot.md#ограничения-текущей-версии-пакета)). Пока её нет,
вставьте в PowerShell блок целиком — от `@'` до последней строки с
`python -`. Пока вы не вставили строку `'@ | …`, PowerShell показывает
приглашение `>>`: это нормально. Строка `'@` должна начинаться с начала
строки, без пробелов.

```powershell
@'
import hashlib, json, sys
sys.path.insert(0, "tools")
import bcreq_pipeline
path = sys.argv[1]
working = json.load(open(path, encoding="utf-8-sig"))
for item in working.get("evidence", []):
    item["checksum"] = "sha256:" + hashlib.sha256(item["excerpt"].encode("utf-8")).hexdigest()
working["working_digest"] = bcreq_pipeline.working_digest(working)
text = json.dumps(working, ensure_ascii=False, indent=2) + "\n"
open(path, "w", encoding="utf-8", newline="\n").write(text)
print("sealed:", path)
'@ | python - runs/TASK-0002/evidence/working.json
```

- **Что делает:** пересчитывает контрольную сумму каждой цитаты
  (`evidence[].checksum`) и общую сумму черновика (`working_digest`) и
  перезаписывает файл. Смысл текста не меняется.
- **Ожидаемый результат:** `sealed: runs/TASK-0002/evidence/working.json`
- **Когда:** после **каждой** правки `working.json` — вашей или GigaCode.
  Без этого проверка отвечает
  `ERROR: BASELINE Working digest does not match canonical content` или
  `ERROR: SCHEMA Working.working_digest has invalid format`.

### Проверить Working

- **Команда:**
  `python tools/bcreq_pipeline.py validate-working runs/TASK-0002/evidence/working.json`
- **Что делает:** проверяет черновик: схема, ссылки между пунктами,
  цитаты и их контрольные суммы, продуктовая цепочка, `working_digest`.
- **Ожидаемый результат:** `G-mach: BCREQ accepted`
- **Если нет:** строки `ERROR: <КОД> <описание>`. Передайте их GigaCode:
  «Исправь в working.json ошибки проверки: <вставьте строки>», затем
  снова запечатайте и проверьте.

### Собрать Release

- **Команда:**
  `python tools/bcreq_pipeline.py compile runs/TASK-0002/evidence/working.json --output runs/TASK-0002/release`
- **Что делает:** детерминированно (одинаковый вход — одинаковый
  результат) собирает из одобренного Working документ
  `runs/TASK-0002/release/release.json` и `release-manifest.json`.
- **Ожидаемый результат:** `G-mach: BCREQ accepted`

### Проверить Release

- **Команда** (одной строкой):

  ```powershell
  python tools/bcreq_pipeline.py validate-release runs/TASK-0002/evidence/working.json --release runs/TASK-0002/release/release.json --manifest runs/TASK-0002/release/release-manifest.json
  ```

- **Что делает:** проверяет, что Release и manifest собраны именно из
  этого Working и никто их не правил.
- **Ожидаемый результат:** `G-mach: BCREQ accepted`

## Контроль прогонов: один TASK ID — один прогон

- Каждая задача получает новый [TASK ID](01-junior-pilot.md#term-task-id):
  `TASK-` и 4 цифры. Ведите список выданных номеров, например в карточке
  задачи.
- Runner не начинает задачу с номером, для которого уже есть папка
  `runs/TASK-ID/`: `BLOCKED: task already exists; use a new task id`.
  Так журнал защищён от перезаписи.
- **Любой отказ `advance` останавливает задачу:** в журнал пишется строка
  со `"status": "reject"`, а состояние становится `blocked`
  ([О-6](01-junior-pilot.md#ограничения-текущей-версии-пакета)). Следующая
  команда `advance` ответит `BLOCKED: task is blocked or finished`.
- Что делать после отказа:
  1. Прочитайте причину после `BLOCKED:` и последнюю строку
     `runs/TASK-ID/trace.jsonl` (см. [ниже](#как-читать-журнал-прогона-trace)).
  2. Исправьте причину.
  3. Начните задачу с **новым** TASK ID и скопируйте в его `evidence/`
     готовые файлы старой задачи. В A-IN замените `task.id` на новый номер.
  4. Пройдите переходы заново. Старую папку не удаляйте: это журнал
     неудачной попытки.
- Чтобы не терять задачи, проверяйте артефакт **до** перехода: «Проверить
  вход A-IN», «Проверить Working», «Проверить Release».
- Если задача прервалась (закрыли терминал, перезагрузили АРМ), ничего не
  потеряно: состояние лежит в `runs/TASK-ID/state.json`. Покажите
  состояние задачи и продолжайте с текущего узла. Если runner ответил
  `BLOCKED: another runner command is active or its lock needs review`, а
  другая команда точно не идёт, передайте это ответственному.

## Процесс формирования бизнес-спецификации

Маршрут `RG-BCREQ-v1` (`routes/rg-bcreq-v1.yaml`) — это 15 рабочих узлов (`n0`…`n13` и `n10a`) трёх
процессов: P-01 «вход и ядро», P-02 «вопросы Заказчику», P-03
«спецификация». На каждом переходе runner запускает G-mach, а на узлах с
G-human ещё и спрашивает вас.

```text
entry → n0 → n1 → n2 → n3 → n4 ─┬─(нет blocker)──────────────────────→ n9 → n10 → n10a → n11 → n12 → n13 → exit
                                └─(есть blocker)→ n5 → n6 → n7 → n8 ─┘
                                                            ↑        │ (остались blocker)
                                                            └── n5 ←─┘
```

| Узел | Что делается | Навык | Артефакт для перехода | G-human |
|------|--------------|-------|-----------------------|---------|
| `entry` | Вход задачи | — | A-IN (JSON) | — |
| `n0` | Тип работы и продуктовая привязка | `product-attribution` | A-IN с подтверждённой привязкой (JSON) | Да |
| `n1` | Нормализация текста источников | `transcript-normalization` | Нормализованный текст | — |
| `n2` | Разметка элементов контекста | `context-extraction` | Размеченные элементы | — |
| `n3` | Поиск неоднозначностей | `ambiguity-detection` | Список неоднозначностей | — |
| `n4` | Сборка ядра требований | `core-assembly` | A-CORE (JSON) | Да |
| `n5` | Формулировка вопросов | `question-formation` | A-QUEST (JSON) | — |
| `n6` | Приоритизация вопросов | `question-prioritization` | A-QUEST (JSON) | — |
| `n7` | Отправка вопросов Заказчику и ответы | нет навыка: это делаете вы | `{"answers": [...]}` (JSON) | Да |
| `n8` | Встраивание ответов в ядро | `answer-integration` | A-CORE (JSON) | Да |
| `n9` | Постановка проблемы | `problem-statement` | Текст проблемы | — |
| `n10` | Гипотеза ценности | `value-hypothesis` | Текст гипотезы | — |
| `n10a` | Предварительная проверка реестров | `bcreq-preflight` | `{"preflight_registers": {"valid": true}}` (JSON) | Да |
| `n11` | Декомпозиция требований | `bcreq-decomposition` | Пункты BCREQ | — |
| `n12` | Сборка Working | `bcreq-assembly` | Запечатанный `working.json` со `"state": "approved"` | Да |
| `n13` | Сборка и проверка Release | `bcreq-release` | `release.json` + `--working` + `--manifest` | Да |

Развилки выбирает runner, а не вы:

| Узел | Условие | Куда |
|------|---------|------|
| `n0` | `work_type` = `external-spec` | `handoff-p08` (оценка внешнего ТЗ — другой процесс, BCREQ не формируется) |
| `n0` | Иначе, привязка подтверждена | `n1` |
| `n4` | В A-CORE есть неоднозначность `"severity": "blocker"` | `n5` |
| `n4` | Нет | `n9` |
| `n7` | Массив `answers` не пуст | `n8` |
| `n7` | Пуст | `halt` — задача остановлена до ответа Заказчика |
| `n8` | Остались `blocker` без `resolved_by` | `n5` (ещё круг вопросов) |
| `n8` | Нет | `n9` |
| `n10a` | `preflight_registers.valid` = `true` | `n11` |
| `n10a` | `false` | `halt` |

Как пройти узлы вместе с GigaCode — в
[работе с агентом](06-working-with-gigacode.md#шаг-5-пройдите-узлы-маршрута).

## Как читать журнал прогона (trace)

`runs/TASK-ID/trace.jsonl` — одна строка JSON на каждую попытку перехода.
Пишет только runner; руками файл не правьте: runner сверяет цепочку
контрольных сумм и при расхождении отказывает
(`runner state differs from trace`). Посмотреть последнюю строку:

```powershell
Get-Content -Encoding UTF8 -Tail 1 runs\TASK-0002\trace.jsonl
```

| Поле | Что значит |
|------|------------|
| `seq` | Номер попытки: 1, 2, 3… |
| `from`, `to` | Из какого узла в какой пытались перейти |
| `status` | `pass` — переход выполнен, `reject` — отказ |
| `reason` | Причина отказа (пусто при `pass`) — тот же текст, что после `BLOCKED:` |
| [`script_invoked`](01-junior-pilot.md#term-script-invoked) | `true` — G-mach на этом шаге запускался |
| [`step_skipped`](01-junior-pilot.md#term-step-skipped) | `true` — до G-mach дело не дошло: runner отказал раньше (нет перехода, нет файла, не тот контракт, нет checkpoint) |
| [`exit_code`](01-junior-pilot.md#term-exit-code) | Код G-mach: `0` — успех. Есть только при `script_invoked: true` |
| `gate_output` | Последние строки вывода G-mach — здесь `ERROR: …` |
| `command` | Какая именно проверка запускалась |
| [`contract_mode`](01-junior-pilot.md#term-contract-mode) | Всегда `false`: в пилоте каждый шаг проверяется программой |
| `output_ref`, `output_digest` | Путь и SHA-256 артефакта узла |
| `checkpoint_ref`, `checkpoint_digest` | Путь и SHA-256 checkpoint (узлы с G-human) |
| `recorded_by` | Всегда `runner` |
| `ts` | Время записи (UTC) |
| `previous_digest`, `event_digest` | Цепочка контрольных сумм, защищающая журнал от правок |

Как читать отказ:

| Сочетание | Что случилось |
|-----------|---------------|
| `status: reject`, `step_skipped: true` | Runner отказал до проверки: смотрите `reason` |
| `status: reject`, `script_invoked: true`, `exit_code` не `0` | Проверка нашла ошибки: смотрите `gate_output` |
| `status: reject`, `script_invoked: true`, `exit_code: 0` | Проверка прошла, но вы не подтвердили или файл изменился во время проверки: смотрите `reason` |

## Папки пакета

| Папка или файл | Что в ней | Можно менять? |
|----------------|-----------|---------------|
| `AGENTS.md` | Загрузочный контракт GigaCode: исполняемые правила пакета | Нет |
| `README.md`, `package-manifest.yaml` | Описание пакета и контрольные суммы всех файлов | Нет |
| `docs/guides/` | Эти инструкции | Нет |
| `.gigacode/skills/` | [Навыки](01-junior-pilot.md#term-skill) узлов и отладки | Нет |
| `.gigacode/settings.example.json` | Пример подключения Confluence MCP | Нет. Ваша копия — `.gigacode/settings.json` |
| `contracts/` | Схемы артефактов (JSON Schema) | Нет |
| `taxonomy/` | Словари: продукты MANGO, типы работ, уровни источников | Нет |
| `routes/` | Маршрут `RG-BCREQ-v1` | Нет |
| `templates/` | Скелеты артефактов и checkpoint (`checkpoint-skeleton.md`) | Нет |
| [`golden/`](01-junior-pilot.md#term-golden) | Эталоны для самопроверки пакета | Нет. `golden/candidates/` — для ручных кандидатов |
| `evaluation/` | Чек-листы G-mach и G-human, метрики | Нет |
| `tools/` | Runner, проверка пакета, сборка Release | Нет |
| `docs/kb/` | Отобранные статьи базы знаний | Да, только файлы из `sections/` KB |
| `meta-model/` | Место для канонической модели при подготовке копии | Только ответственный |
| `runs/` | Задачи `TASK-*` и отладочные прогоны `DEBUG-*`. Исключена из Git | Да, только `runs/TASK-ID/evidence/` и `runs/TASK-ID/release/` |

## Режим отладки

Режим отладки нужен, чтобы понять, почему переход не прошёл или почему
агент ведёт себя не так, и подготовить улучшение
[мета-модели](01-junior-pilot.md#term-meta-model). Он требует знания
устройства пакета: маршрута, контрактов, навыков.

Между командами runner можно в любой момент перейти в режим отладки и
вернуться: состояние задачи хранится в `runs/TASK-ID/`, а не в чате
GigaCode.

### Как войти в режим отладки

1. В терминале A завершите текущую сессию (`/quit`) и запустите
   `gigacode` заново — отладка идёт в **новой** сессии.
2. Напишите GigaCode `/skills ba-debug-orchestrator` и опишите сценарий,
   например:

   ```text
   Отладка на учебных данных. Проверь ребро n4 -> n5: A-CORE с одной неоднозначностью
   severity blocker. Реальные данные и MCP не используй.
   ```

3. **Ожидаемый результат:** GigaCode создаёт папку
   `runs/DEBUG-<время UTC>/` с журналом `events.yaml`, отчётом
   `DEBUG-REPORT.md` и, если дошёл до узла с G-human, checkpoint в
   `evidence/`. Папки `runs/TASK-*` он не создаёт и не трогает, MCP и
   внешние системы не вызывает.
4. Выйти из режима — `/quit` и новая сессия.

Навык [`rg-bcreq-v1-dispatcher`](01-junior-pilot.md#term-dispatcher)
(`/skills rg-bcreq-v1-dispatcher`) подсказывает следующий узел по
маршруту. Он ведёт свой ручной журнал и **не меняет** состояние runner
([О-3](01-junior-pilot.md#ограничения-текущей-версии-пакета)): переходы
реальной задачи выполняйте только командой «Выполнить переход».

### Отдельные машинные шаги

Каждую проверку можно запустить отдельно, не трогая состояние задачи:

| Что проверить | Команда |
|---------------|---------|
| Пакет | `python tools/validate-package.py` |
| A-IN | `python tools/validate-package.py --input <файл>` |
| Working (через проверку пакета) | `python tools/validate-package.py --working <файл>` |
| Working (только черновик) | `python tools/bcreq_pipeline.py validate-working <файл>` |
| Release | `python tools/bcreq_pipeline.py validate-release <working> --release <release.json> --manifest <release-manifest.json>` |

Именно эти команды runner запускает при переходе — их точный вид есть в
поле `command` журнала. Повторите проверку вручную, исправьте артефакт и
только потом начинайте задачу с новым TASK ID.

### Если нужно изменить правила пакета

Файлы пакета не правьте: проверка пакета сразу покажет изменённый файл, и
runner перестанет начинать задачи. Правила меняются в
[исходном репозитории](01-junior-pilot.md#term-source):

1. Опишите проблему: TASK ID или `DEBUG-*`, узел, текст отказа, строку
   журнала, `DEBUG-REPORT.md`.
2. Передайте описание ответственному за пакет или создайте задачу в
   исходном репозитории
   [hybrid-Intelligence-lab](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues).
3. После исправления пакет собирается заново. Обновите его на АРМ по
   варианту Б из [развёртывания](03-deploy-package.md#получите-пакет):
   скачайте новую версию и скопируйте файлы пакета поверх `runtime`.
   Папки `runs\`, `docs\kb\` и файл `.gigacode\settings.json` при этом
   сохраняются. Затем выполните «Проверить пакет».

   ```powershell
   Set-Location "$env:USERPROFILE\bcreq-pilot"
   git -C source-lab pull
   Copy-Item -Recurse -Force source-lab\projects\ba-ai-process\dist\execution-package-gigacode-cli\* runtime\
   Set-Location runtime
   python tools/validate-package.py
   ```

   Если новая версия удалила какой-то файл, проверка покажет
   `immutable-выход не объявлен: <файл>`: удалите этот файл из `runtime\`
   и повторите проверку. Для варианта А выполните `git pull` в папке
   `runtime`.

## Чего в пилоте нет

- Команды, которая сама запечатывает Working
  ([О-8](01-junior-pilot.md#ограничения-текущей-версии-пакета)).
- Навыка, который сам ведёт задачу по всем узлам и выполняет переходы
  ([О-9](01-junior-pilot.md#ограничения-текущей-версии-пакета)).
- Продолжения задачи после отказа: только новый TASK ID
  ([О-6](01-junior-pilot.md#ограничения-текущей-версии-пакета)).
- Автоматической отправки вопросов Заказчику и публикации Release: оба
  действия выполняете вы.

---

**Навигация:** [Содержание](README.md) · [Обзор и глоссарий](01-junior-pilot.md) ·
[1. Установка](02-install.md) · [2. Развёртывание](03-deploy-package.md) ·
[3. Учебный прогон](04-smoke-test.md) · [4. Работа с агентом](06-working-with-gigacode.md) ·
**5. Команды и отладка**

← Назад: [4. Работа с агентом](06-working-with-gigacode.md) · [Содержание](README.md)
