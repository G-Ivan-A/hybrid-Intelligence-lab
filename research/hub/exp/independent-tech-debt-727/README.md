---
status: draft
version: 0.1
updated: 2026-11-04
temperature: 0.1
type: experiment
---

# exp: independent-tech-debt-727

Контейнер доказательств для анализа
[`../../../../docs/analysis/2026-11-04-sprint-13-hub-normative-debt-selection.md`](../../../../docs/analysis/2026-11-04-sprint-13-hub-normative-debt-selection.md),
issue [#727](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/727).

## Что здесь проверяется

1. **Полнота предшествующих шагов.** Какие строки бэклога остались в
   `review`, хотя их PR (#724, #726) уже смёржены.
2. **Разрывы нормативной части Спринта 13 открыты на текущем `main`.**
   Для каждой выбранной строки есть отдельная проверка: B-169 (F-1),
   B-114 (F-2), B-115 (F-3), B-116 (F-4), B-154 (F-5).
   *Это снимок до реализации. Реализация ждёт комментария владельца в
   PR #728.*
3. **Пересечения и гигиена.** Пересекаются ли выбранные строки с шагами
   RFC #715 (B-239, B-240, B-241, B-259, B-260). Нет ли у выбранных строк
   дублирующихся ID.
4. **Независимость от экосистемы.** Меняет ли открытый PR Хаба файлы
   спринта. Касаются ли открытые PR спиц путей Хаба. Читает ли CI спиц
   `mango_ba_prompts`, `mango-ba-ai-runtime` и `aether-orbis-gra` файлы
   Хаба при прогоне. На каком SHA закреплён синк каждой спицы.

## Файлы

| Файл | Назначение |
| --- | --- |
| [`independence-check.sh`](independence-check.sh) | Скрипт только для чтения: `git`, `grep`, `awk`, `gh`. Ничего не меняет ни в Хабе, ни в спицах |
| [`independence-check.log`](independence-check.log) | Вывод скрипта от 2026-11-04 при Хабе `7dc6df2` (ветка от `main@6ab5e9b`) |

## Воспроизведение

```bash
research/hub/exp/independent-tech-debt-727/independence-check.sh \
  > research/hub/exp/independent-tech-debt-727/independence-check.log 2>&1
```

Без `gh` выполняются только локальные разделы. «Hub fetch steps» — число
строк workflow, которые клонируют Хаб или скачивают его файлы. Ноль значит,
что CI спицы не зависит от текущего `main` Хаба.
