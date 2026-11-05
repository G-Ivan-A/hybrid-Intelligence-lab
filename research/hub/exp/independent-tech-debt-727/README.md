---
status: draft
version: 0.2
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
| [`issue-statement-sweep.sh`](issue-statement-sweep.sh) | Ретро-прогон гейта постановки `tools/validate-issue-statement.sh` (B-116 (d)) по 150 последним issue Хаба и по нулевому пациенту mango#353. Только чтение: `gh issue list/view` |
| [`issue-statement-sweep.log`](issue-statement-sweep.log) | Вывод ретро-прогона от 2026-11-04 при Хабе `83acba5` |

## Ретро-прогон гейта постановки (B-116 (d))

Гейт должен ловить нулевого пациента F7 и не мешать текущим постановкам.
Итог прогона по 150 issue Хаба: 130 проходят, 20 красные.

- **mango#353 красный.** Гейт ловит `docs/contracts/` в «5. Готово, когда»
  (строка 86). Это ровно тот путь, который породил F2/F7.
- **hub#605 красный по делу.** В «Критериях готовности» предписан
  `docs/contracts/`.
- **17 issue (#425…#557) красные из-за каталога `pr-ops`.** Он перенесён в
  `ops/` (#567), гейт подсказывает новый путь.
- **3 случая неоднозначны** (#446 `kb/processes/`, #599 `.gigacode/skills/` и
  `meta-model/.gitkeep`). Это пути относительно проекта, названного выше в тексте.
  Гейт краснит их, потому что из свободного текста не видно корня.
  Цена — правка постановки или эскалация.
- **Все issue от #606 до #727 проходят.** Гейт не мешает действующей практике.

## Воспроизведение

```bash
research/hub/exp/independent-tech-debt-727/independence-check.sh \
  > research/hub/exp/independent-tech-debt-727/independence-check.log 2>&1
```

```bash
research/hub/exp/independent-tech-debt-727/issue-statement-sweep.sh \
  > research/hub/exp/independent-tech-debt-727/issue-statement-sweep.log 2>&1
```

Без `gh` выполняются только локальные разделы. «Hub fetch steps» — число
строк workflow, которые клонируют Хаб или скачивают его файлы. Ноль значит,
что CI спицы не зависит от текущего `main` Хаба.
