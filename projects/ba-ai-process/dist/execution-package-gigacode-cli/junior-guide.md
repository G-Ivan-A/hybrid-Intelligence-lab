---
status: draft
version: 1.0
updated: 2026-09-26
temperature: 0.1
---

# Запуск задачи: инструкция для бизнес-аналитика

Работайте в отдельной копии пакета для одной задачи. Все команды ниже запускайте
из корня этой копии. Сохраните исходные материалы в разрешённом локальном
каталоге; не помещайте секреты и рабочие прогоны в Git.

## 1. Подготовьте рабочее место

Установите GigaCode CLI по корпоративной инструкции и Python 3. Проверьте:

```sh
gigacode --version
python3 --version
python3 -m pip install -r requirements.txt
sh tools/validate-package.sh
```

Проверка пакета должна завершиться строкой `G-mach: пакет принят`. Если она
завершилась ошибкой, остановитесь и передайте текст ошибки ответственному за
пакет. Не исправляйте скомпилированные файлы прямо в рабочей копии.

При необходимости наполните `meta-model/` и `docs/kb/` разрешёнными
материалами. Доступ к Confluence настраивается локально через
`.gigacode/settings.json` по `.gigacode/settings.example.json` с данными от
администратора. Адреса и ключи в пакет не записываются.

## 2. Создайте задачу

Выберите свободный номер, например `TASK-0001`. Подготовьте исходный `A-IN` в
YAML или JSON по `contracts/c-in.schema.json`. В начале
`product_attribution.status` может быть `pending`.

```sh
sh tools/run-task start TASK-0001
sh tools/run-task advance TASK-0001 --to n0 --artifact /путь/к/A-IN.yaml
```

Runner создаст `runs/TASK-0001/state.json` и `trace.jsonl`. Вторую команду он
пропустит только после вызова `G-mach` и проверки входного контракта. Если
получен `BLOCKED`, переход не выполнен. Для исправленного входа создайте новый
номер задачи: отклонённая попытка сохраняется как свидетельство.

## 3. Проверьте и подтвердите продуктовую цепочку

В GigaCode CLI вызовите навык продуктовой атрибуции. Проверьте Domain →
Capability → Feature → Atomic Function, тип работы и источник. Сохраните
подтверждение в Markdown checkpoint, а `A-IN` со статусом `confirmed`,
`confirmed_by`, `confirmed_at`, `decision_ref` и `binding_digest` — отдельным
файлом. Только после собственного решения запустите:

```sh
sh tools/run-task advance TASK-0001 --to n1 --artifact /путь/к/A-IN-confirmed.yaml \
  --checkpoint /путь/к/checkpoint-n0.md
```

Runner покажет путь и digest checkpoint и попросит ввести строку подтверждения
в терминале. Сверьте файл с тем, что видите в диалоге, затем введите показанную
строку самостоятельно. Без интерактивного ответа переход блокируется.

## 4. Проходите следующие узлы

Смотрите `routes/rg-bcreq-v1.yaml`: текущий узел напечатан командой
`sh tools/run-task metrics TASK-0001`. Агент подготавливает артефакт текущего
узла; вы проверяете его и запускаете один переход:

```sh
sh tools/run-task advance TASK-0001 --to n2 --artifact /путь/к/результату-n1.json
```

Укажите файл результата **текущего** узла и следующий узел из графа.
Runner сам вызывает `G-mach` при каждом переходе, проверяет exit code и
добавляет строку в `trace.jsonl`. Для узла с `G-human` приложите читаемый
checkpoint и ответьте на приглашение терминала. При ветвлении `n4`, `n7`,
`n8`, `n10a` runner читает структурированные поля артефакта и блокирует
ребро, не соответствующее их значениям. При `BLOCKED` прекратите работу с
этим run и передайте checkpoint, trace и сообщение об ошибке на разбор.

Перед `n12 → n13` нужен утверждённый Working JSON:

```sh
sh tools/run-task advance TASK-0001 --to n13 --artifact /путь/к/Working.json \
  --checkpoint /путь/к/checkpoint-n12.md
```

После компиляции Release командой `python3 tools/bcreq_pipeline.py compile`
проверьте результат и завершите маршрут:

```sh
sh tools/run-task advance TASK-0001 --to exit --artifact /путь/к/release.json \
  --working /путь/к/Working.json --manifest /путь/к/release-manifest.json \
  --checkpoint /путь/к/checkpoint-n13.md
```

Runner проверяет Release и manifest отдельным процессом. Смысл текста и
достоверность источников остаются предметом вашего ревью.

## 5. Посмотрите след

```sh
sh tools/run-task metrics TASK-0001
```

`deterministic_share` — успешные вызовы gate самим runner, делённые на число
запрошенных шагов. Значение `null` означает, что шагов ещё не было.
`trace.jsonl` содержит на каждый запрошенный шаг ровно одно истинное состояние:
`script_invoked`, `contract_mode` либо `step_skipped`, а также `recorded_by`.
Отказ gate сохраняет `script_invoked=true` и его ненулевой `exit_code`, но
переход не выполняет. Отсутствие строки trace блокирует продолжение.

## Ручная отладка

`/skills rg-bcreq-v1-dispatcher` и `/skills ba-debug-orchestrator` остаются
способом ручного пилота и диагностики. Dispatcher помогает прочитать маршрут,
но его текстовые указания не разрешают переход в runner. Отладочный прогон
держите в `runs/DEBUG-<TIMESTAMP>/`; его нельзя выдавать за подтверждённый
рабочий run.
