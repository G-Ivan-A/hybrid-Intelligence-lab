---
status: draft
version: 0.1
updated: 2026-11-04
temperature: 0.1
type: experiment
---

# exp: independent-tech-debt-723

Контейнер доказательств для анализа
[`../../../../docs/analysis/2026-11-04-independent-tech-debt-sprint-selection.md`](../../../../docs/analysis/2026-11-04-independent-tech-debt-sprint-selection.md),
issue [#723](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/723).

## Что здесь проверяется

1. **Разрывы Спринта 23 открыты на текущем `main`.** Валидатор размера
   по-прежнему завершается с ошибкой выше 9K (F-1). Геном HTOM по-прежнему
   называет `Structured` режимом по умолчанию (F-2…F-5).
2. **Какие закрепления затронет правка.** Версии файлов генома в
   валидаторе структуры и в `templates/manifest.json`.
3. **Независимость от экосистемы.** Меняет ли открытый PR Хаба файлы
   спринта. Читает ли CI спиц `mango_ba_prompts`, `mango-ba-ai-runtime` и
   `aether-orbis-gra` файлы Хаба при прогоне. На каком SHA закреплён синк
   каждой спицы.

## Файлы

| Файл | Назначение |
| --- | --- |
| [`independence-check.sh`](independence-check.sh) | Скрипт только для чтения: `git`, `grep`, `gh`. Ничего не меняет ни в Хабе, ни в спицах |
| [`independence-check.log`](independence-check.log) | Вывод скрипта 2026-11-04 при Хабе `195fd38` (ветка от `main@4fb085b`) |

## Воспроизведение

```bash
research/hub/exp/independent-tech-debt-723/independence-check.sh \
  > research/hub/exp/independent-tech-debt-723/independence-check.log 2>&1
```

Без `gh` выполняются только локальные разделы. «Hub fetch steps» — число
строк workflow, которые клонируют Хаб или скачивают его файлы. Ноль значит,
что CI спицы от текущего `main` Хаба не зависит.
