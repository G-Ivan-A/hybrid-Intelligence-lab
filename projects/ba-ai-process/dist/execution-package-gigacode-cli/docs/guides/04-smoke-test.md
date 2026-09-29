---
status: draft
version: 1.0
updated: 2026-09-29
temperature: 0.1
---

# 3. Учебный прогон (необязательно)

**Цель:** один раз пройти первые два перехода маршрута на учебной задаче
`TASK-0001` без корпоративных данных. Вы увидите, как начинается задача,
как runner проверяет вход, как выглядит ваше подтверждение на узле с
[G-human](01-junior-pilot.md#term-g-human) и как посмотреть состояние
задачи.

Этот шаг **не обязателен** и не открывает доступ к реальным задачам: после
[развёртывания](03-deploy-package.md) можно сразу переходить к
[реальной задаче](06-working-with-gigacode.md).

## Содержание

1. [Что такое учебный прогон](#что-такое-учебный-прогон)
2. [Шаг 1. Начните учебную задачу](#шаг-1-начните-учебную-задачу)
3. [Шаг 2. Подготовьте учебный вход](#шаг-2-подготовьте-учебный-вход)
4. [Шаг 3. Попросите GigaCode объяснить вход](#шаг-3-попросите-gigacode-объяснить-вход)
5. [Шаг 4. Выполните первый переход](#шаг-4-выполните-первый-переход)
6. [Шаг 5. Подтвердите вход и выполните второй переход](#шаг-5-подтвердите-вход-и-выполните-второй-переход)
7. [Шаг 6. Посмотрите состояние задачи](#шаг-6-посмотрите-состояние-задачи)
8. [Повторить учебный прогон](#повторить-учебный-прогон)

## Что такое учебный прогон

- Учебная задача: «клиент хочет двустороннюю синхронизацию контактов с
  CRM». Продуктовая цепочка вымышленная, но проходит проверки пакета:
  `platform` → `platform-integration` → `crm-connectors` →
  `crm-bidirectional-sync`. Источник — строка-заглушка `smoke`, а не
  корпоративный документ.
- Готового учебного входа [A-IN](01-junior-pilot.md#term-a-in) в пакете нет
  ([О-4](01-junior-pilot.md#ограничения-текущей-версии-пакета)). Поэтому
  три файла учебной задачи вы создадите командами из этого документа.
- Вы пройдёте переходы `entry → n0` (проверка входа) и `n0 → n1`
  (ваше подтверждение продуктовой привязки). Дальше учебная задача не
  идёт: полный маршрут показан в [работе с агентом](06-working-with-gigacode.md).

Все команды ниже выполняются в [терминале B](01-junior-pilot.md#term-terminal-b)
в папке пакета `~/bcreq-pilot/runtime` с включённым окружением Python
(`. ~/bcreq-pilot/venv/bin/activate`). Вставляйте каждый блок целиком.

## Шаг 1. Начните учебную задачу

**Действие: «Начать задачу»** (`sh tools/run-task start TASK-0001`)

- **Где:** терминал B, папка пакета.
- **Команды:**

  ```sh
  sh tools/run-task start TASK-0001
  mkdir -p runs/TASK-0001/evidence
  ```

- **Что делают:** runner проверяет целостность пакета
  ([G-mach](01-junior-pilot.md#term-g-mach)) и создаёт папку
  `runs/TASK-0001/` с состоянием задачи. Вторая команда создаёт в ней папку
  `evidence/` для файлов задачи.
- **Ожидаемый результат:**

  ```text
  TASK-0001: started at entry; next transition requires G-mach
  ```

- **Проверьте:** `ls runs/TASK-0001` показывает `evidence`, `state.json`,
  `trace.jsonl`.

Если runner ответил `BLOCKED: task already exists; use a new task id`, вы
уже начинали учебную задачу — см. [Повторить учебный прогон](#повторить-учебный-прогон).

## Шаг 2. Подготовьте учебный вход

**Действие: «Записать учебный вход»**

Три блока ниже создают три файла в `runs/TASK-0001/evidence/`. Каждый блок
начинается с `cat >` и заканчивается строкой `EOF`: вставьте его целиком и
нажмите Enter. Команды ничего не печатают.

1. **Вход до подтверждения** — `A-IN.json`. Продуктовая привязка
   предложена, но ещё не подтверждена (`"status": "pending"`):

   ```sh
   cat > runs/TASK-0001/evidence/A-IN.json <<'EOF'
   {
     "artifact_class": "A-IN",
     "state": "raw",
     "task": {"id": "TASK-0001", "title": "Учебная задача: синхронизация контактов с CRM", "requested_by": "analyst"},
     "work_type": "mango-change",
     "routing": {"primary_axis": "mango", "rule": "mango-change", "decision": "pending", "decision_ref": "evidence/checkpoint-n0.md"},
     "products": [{"marker": "A", "domain": "platform", "capability": "platform-integration", "feature": "crm-connectors", "atomic_function": "crm-bidirectional-sync", "profile": "P-API", "owner": "platform-owner"}],
     "product_attribution": {"status": "pending"},
     "sources": [{"id": "SRC-01", "kind": "transcript", "tier": "ST-1-ATTACHED", "locator": "smoke", "content": "smoke"}],
     "language": "ru"
   }
   EOF
   ```

2. **Checkpoint узла `n0`** — `checkpoint-n0.md`. Это то, что вы читаете
   перед подтверждением ([checkpoint](01-junior-pilot.md#term-checkpoint)):

   ```sh
   cat > runs/TASK-0001/evidence/checkpoint-n0.md <<'EOF'
   # Checkpoint TASK-0001 / n0

   ## Задача
   Учебная задача: синхронизация контактов с CRM.

   ## Узел
   n0 — классификация входа и подтверждение продуктовой привязки.

   ## Продуктовый контекст
   - Цепочка A: platform / platform-integration / crm-connectors / crm-bidirectional-sync (P-API).
   - Статус: подтверждено аналитиком.

   ## Источники
   | Заголовок | Раздел | Страница-anchor | Цитата | Locator |
   |-----------|--------|-----------------|--------|---------|
   | Учебная заглушка | — | — | smoke | smoke |

   ## Решение человека
   Одобрено: привязка к продукту верна для учебной задачи.
   EOF
   ```

3. **Вход после подтверждения** — `A-IN-confirmed.json`. От первого файла
   он отличается двумя полями: `routing.decision` стало `confirmed`, а в
   `product_attribution` записаны кто и когда подтвердил, ссылка на
   checkpoint и `binding_digest` — контрольная сумма продуктовой цепочки.
   Поле `state` у A-IN всегда `raw`: так требует контракт
   `contracts/c-in.schema.json`.

   ```sh
   cat > runs/TASK-0001/evidence/A-IN-confirmed.json <<'EOF'
   {
     "artifact_class": "A-IN",
     "state": "raw",
     "task": {"id": "TASK-0001", "title": "Учебная задача: синхронизация контактов с CRM", "requested_by": "analyst"},
     "work_type": "mango-change",
     "routing": {"primary_axis": "mango", "rule": "mango-change", "decision": "confirmed", "decision_ref": "evidence/checkpoint-n0.md"},
     "products": [{"marker": "A", "domain": "platform", "capability": "platform-integration", "feature": "crm-connectors", "atomic_function": "crm-bidirectional-sync", "profile": "P-API", "owner": "platform-owner"}],
     "product_attribution": {"status": "confirmed", "confirmed_by": "analyst", "confirmed_at": "2026-09-29T12:00:00Z", "decision_ref": "evidence/checkpoint-n0.md", "binding_digest": "sha256:af9fe155106dfbcbecd1ae1fb7a05c2b28781a2ada6b499c2e1d828172e2de0b"},
     "sources": [{"id": "SRC-01", "kind": "transcript", "tier": "ST-1-ATTACHED", "locator": "smoke", "content": "smoke"}],
     "language": "ru"
   }
   EOF
   ```

**Проверьте:** `ls runs/TASK-0001/evidence` показывает `A-IN.json`,
`A-IN-confirmed.json`, `checkpoint-n0.md`. Контрольную сумму цепочки можно
пересчитать командой [«Посчитать binding_digest»](05-commands-reference.md#посчитать-binding_digest):
для учебной цепочки она печатает то же значение
`sha256:af9fe155…2de0b`, что записано в файле.

## Шаг 3. Попросите GigaCode объяснить вход

- **Где:** [терминал A](01-junior-pilot.md#term-terminal-a), режим
  `/approval-mode plan` (только разговор, файлы не меняются).
- **Напишите GigaCode:**

  ```text
  Это учебная задача, а не реальная.
  Прочитай @runs/TASK-0001/evidence/A-IN.json и объясни простыми словами:
  1. Какую задачу он описывает.
  2. К какому продукту она привязана (домен, возможность, функция).
  3. Какие источники указаны.
  4. Что изменится в файле A-IN-confirmed.json после моего подтверждения.
  Отвечай нумерованным списком. Файлы не меняй.
  ```

- **Ожидаемый результат:** нумерованный ответ: синхронизация контактов с
  CRM; цепочка `platform` / `platform-integration` / `crm-connectors` /
  `crm-bidirectional-sync`; один источник-заглушка `SRC-01`; после
  подтверждения меняются `routing.decision` и `product_attribution`.
- **Проверьте:** GigaCode не придумал других источников и не предложил
  изменить файлы. После ответа верните режим `/approval-mode default`.

## Шаг 4. Выполните первый переход

**Действие: «Выполнить переход»** `entry → n0`

- **Где:** терминал B, папка пакета.
- **Команда:**

  ```sh
  sh tools/run-task advance TASK-0001 --to n0 --artifact runs/TASK-0001/evidence/A-IN.json
  ```

- **Что делает:** runner проверяет, что переход `entry → n0` есть в
  маршруте, что файл A-IN соответствует контракту и относится к
  `TASK-0001`, запускает G-mach и записывает строку в
  [журнал прогона](01-junior-pilot.md#term-trace).
- **Ожидаемый результат** (через несколько секунд):

  ```text
  TASK-0001: entry -> n0; G-mach exit 0; trace seq 1
  ```

- **Проверьте:** нет строки `BLOCKED:`.

## Шаг 5. Подтвердите вход и выполните второй переход

**Действие: «Выполнить переход»** `n0 → n1` с вашим подтверждением

- **Где:** терминал B, папка пакета.
- **Команда:**

  ```sh
  sh tools/run-task advance TASK-0001 --to n1 --artifact runs/TASK-0001/evidence/A-IN-confirmed.json --checkpoint runs/TASK-0001/evidence/checkpoint-n0.md
  ```

- **Что делает:** на узле `n0` стоит G-human. Runner проверяет, что
  привязка подтверждена, запускает G-mach с проверкой входа и только после
  этого спрашивает ваше решение. Он печатает две строки:

  ```text
  Review /home/<логин>/bcreq-pilot/runtime/runs/TASK-0001/evidence/checkpoint-n0.md
  Type exactly: APPROVE TASK-0001:n0 sha256:<64 символа>
  ```

- **Ваше действие:**
  1. Прочитайте checkpoint (например, `cat runs/TASK-0001/evidence/checkpoint-n0.md`
     в другом окне или попросите GigaCode пересказать его).
  2. Скопируйте из терминала текст после `Type exactly: ` — всю строку от
     `APPROVE` до последнего символа контрольной суммы.
  3. Вставьте её и нажмите Enter.
- **Ожидаемый результат:**

  ```text
  TASK-0001: n0 -> n1; G-mach exit 0; trace seq 2
  ```

- **Проверьте:** нет строки `BLOCKED:`. Если вы ошиблись в строке
  подтверждения, runner ответит `BLOCKED: human gate was not approved`, и
  учебную задачу нужно [повторить](#повторить-учебный-прогон).

## Шаг 6. Посмотрите состояние задачи

**Действие: «Показать состояние задачи»** (`sh tools/run-task metrics TASK-0001`)

- **Где:** терминал B, папка пакета.
- **Команда:**

  ```sh
  sh tools/run-task metrics TASK-0001
  ```

- **Ожидаемый результат:**

  ```text
  {"current": "n1", "deterministic_share": 1.0, "deterministic_steps": 2, "expected_steps": 2, "status": "active", "task_id": "TASK-0001"}
  ```

- **Проверьте:** `current` — `n1`, `status` — `active`, оба шага
  подтверждены G-mach (`deterministic_share` — `1.0`). Разбор полей — в
  [справочнике](05-commands-reference.md#показать-состояние-задачи).

**Готово**, если оба перехода прошли и `metrics` показывает `"current": "n1"`.
Разбор журнала `runs/TASK-0001/trace.jsonl` нужен в
[режиме отладки](05-commands-reference.md#как-читать-журнал-прогона-trace).

## Повторить учебный прогон

Повторный `start` с номером `TASK-0001` runner отклонит:
`BLOCKED: task already exists; use a new task id` — так он защищает журнал
от перезаписи ([один TASK ID — один прогон](05-commands-reference.md#контроль-прогонов-один-task-id--один-прогон)).
Только для учебной задачи можно удалить её папку и начать заново с
[шага 1](#шаг-1-начните-учебную-задачу):

```sh
rm -rf runs/TASK-0001
```

Для реальных задач папки `runs/` не удаляйте — берите новый TASK ID.

---

**Навигация:** [Содержание](README.md) · [Обзор и глоссарий](01-junior-pilot.md) ·
[1. Установка](02-install.md) · [2. Развёртывание](03-deploy-package.md) ·
**3. Учебный прогон** · [4. Работа с агентом](06-working-with-gigacode.md) ·
[5. Команды и отладка](05-commands-reference.md)

← Назад: [2. Развёртывание](03-deploy-package.md) · Далее: [4. Работа с агентом](06-working-with-gigacode.md) →
