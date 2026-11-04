---
status: draft
version: 0.2
updated: 2026-11-04
temperature: 0.1
type: experiment
---

# exp: ba-extraction-717

Контейнер доказательств для анализа
[`../../../../docs/analysis/2026-11-03-ba-meta-model-extraction-step1.md`](../../../../docs/analysis/2026-11-03-ba-meta-model-extraction-step1.md)
и контракта
[`../../../../ops/hub-project-extraction-contract.md`](../../../../ops/hub-project-extraction-contract.md),
issue [#717](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/717).

## Что здесь проверяется

1. **Имя репозитория.** Свободно ли имя-кандидат дословно на хостингах кода и
   в реестрах пакетов и насколько оно различимо (сколько репозиториев делят его
   токены).
2. **Исполнимость контракта выноса.** Проходят ли команды этапов E1, E2, E3 и
   E5 контракта на реальных данных проекта метамодели БА при закреплённом
   `HUB_SHA` и что остаётся агенту на этапе E4.
3. **Дрейф до возобновления.** Вынос отложен (решение владельца 2026-11-04,
   B-243). Перед возобновлением снимок при новом коммите Хаба сравнивается со
   снимком при `c06075d`: изменилось ли то, от чего зависят параметры
   выноса, в Хабе, в целевом репозитории и в репозиториях экосистемы.

## Файлы

| Файл | Назначение |
| --- | --- |
| `name-availability.py` | Зонд имён: GitHub (точное имя, итог поиска `in:name`, собственное пространство с переадресацией), GitLab, Codeberg, Hugging Face, PyPI, npm. Только публичные API на чтение |
| `name-availability.log` | Вывод зонда: строка JSON на имя и итоговая таблица |
| `2026-11-03-web-search.md` | Веб-поиск точных фраз для трёх имён из постановки и ведущей альтернативы |
| `ba-instance-params.txt` | Блок `extraction-params` проекта метамодели БА: `MAP`, `DIR`, `CI_JOB`, `CI_STEP`, `BACKLOG`, `HISTORICAL` |
| `rehearse-contract.sh` | Репетиция этапов E1, E2, E3, E5 и сканирования E4 в локальном git-репозитории |
| `rehearse-contract.log` | Вывод репетиции (без построчного JSONL журнала ссылок) |
| `drift-snapshot.py` | Снимок зависимостей параметров при одном коммите Хаба: источники (число, дайджест, каталоги против `DIR`), файлы Хаба с упоминанием источников, шаги CI против `CI_STEP`/`CI_JOB`, разделы бэклога против `BACKLOG`, файлы целевого репозитория, ссылки репозиториев экосистемы на источники (по SHA и плавающие) и закрепления `hub_commit`. Только чтение |
| `drift-baseline.log` | Базовый снимок при `c06075d` и `main` экосистемы на 2026-11-04 |

## Воспроизведение

```bash
# имена (нужен токен GitHub для колонки GitHub)
GH_TOKEN=$(gh auth token) python3 -I research/hub/exp/ba-extraction-717/name-availability.py

# контракт: клон Хаба в отдельном пустом каталоге и git-filter-repo 2.47.0 в venv
git clone --no-checkout https://github.com/G-Ivan-A/hybrid-Intelligence-lab.git /tmp/hub-clone
python3 -m venv /tmp/gfr && /tmp/gfr/bin/pip install git-filter-repo==2.47.0
GFR=/tmp/gfr/bin/git-filter-repo bash research/hub/exp/ba-extraction-717/rehearse-contract.sh \
  research/hub/exp/ba-extraction-717/ba-instance-params.txt /tmp/hub-clone \
  tools/spoke-extraction.py /tmp/rehearsal-out
```

```bash
# дрейф: клоны main экосистемы и целевого репозитория в отдельных пустых каталогах
python3 -I research/hub/exp/ba-extraction-717/drift-snapshot.py \
  --params research/hub/exp/ba-extraction-717/ba-instance-params.txt \
  --hub /tmp/hub-clone --ref NEW_SHA --since c06075d0b45da70cb68e2df3851b861b5ec3aed1 \
  --target /tmp/eco/ba-ai-metamodel \
  --spoke mango_ba_prompts=/tmp/eco/mango_ba_prompts \
  --spoke mango-ba-ai-runtime=/tmp/eco/mango-ba-ai-runtime \
  --spoke aether-orbis=/tmp/eco/aether-orbis \
  --spoke aether-orbis-gra=/tmp/eco/aether-orbis-gra > /tmp/drift-new.log
diff <(grep -v '^#' research/hub/exp/ba-extraction-717/drift-baseline.log) \
  <(sed '/^## since/,$d' /tmp/drift-new.log | grep -v '^#')
```

Репетиция отличается от контракта тремя подстановками: параметры читаются из
файла, а не из задачи; цель — локальный репозиторий с начальным `README.md`
(как у нового репозитория GitHub); инструмент берётся из ветки, потому что
`HUB_SHA` старше инструмента.

## Результаты зонда имён

Проверено 14 имён (2026-11-03). Дословно занято одно — `ai-ba-playbooks`:
переадресация на `G-Ivan-A/mango-ba-ai-runtime`. Ноль похожих на GitHub
(`in:name`) у `ba-ai-metamodel`, `universal-ba-ai-framework`,
`gra-ba-ai-framework` и `aether-orbis-ba`; у `ba-ai-process` — 282. PyPI и npm
свободны для всех имён. Codeberg ответил 504 на 7 имён; для `ba-ai-metamodel`
ответ получен. Выбор имени — в анализе, раздел «Имя репозитория».

## Результаты репетиции (`HUB_SHA` = `c06075d`)

| Этап | Результат |
| --- | --- |
| Шаг 0 | Заморозка: 0 коммитов в источниках после `HUB_SHA`; манифест — 322 файла (303 проекта, 13 `research/mango`, обзор метамодели, 5 тестов) |
| E1 | Геном — 9 файлов; пересечение с переносом пусто; каталоги корня совпали с `DIR`; валидаторы генома проходят |
| E2 | 193 исторических пути; 231 коммит; единственный конфликт — `README.md`, разрешён в пользу импорта; `verify` — дословное совпадение всех 322 файлов |
| E3 | 75 файлов изменено: `url-in` 490, `file-out` 64; повторный запуск `--check` — 0 файлов |
| E4 | `scan` — 365 строк: 276 в `dist/` (перекомпиляция), 32 в `HISTORICAL`, 57 — исходники, тесты и руководства для ручной правки |
| E5 | 13 разделов, 100 строк `B-`; `sections --check` проходит |

Ограничения: E4 (правка кода и CI) и E6 требуют работы агента и CI нового
репозитория, поэтому здесь не репетируются; зонд имён проверяет точное
совпадение и не проверяет товарные знаки.

## Базовый снимок дрейфа (`c06075d`, 2026-11-04)

| Раздел | Значение |
| --- | --- |
| Источники | 322 файла; все каталоги корня цели объявлены в `DIR` или входят в геном |
| Хаб | 85 файлов вне источников упоминают их пути (надмножество 75 файлов, которые правит E3) |
| CI | 24 шага: 17 в трёх заданиях из `CI_JOB` и 7 шагов задания `validate` из `CI_STEP`; необъявленных шагов, упоминающих источники, нет |
| Бэклог | 13 объявленных разделов; раздел «Источники активного порядка» упоминает источники и не переносится |
| Цель | `ba-ai-metamodel` — один файл `README.md`: предусловие E2 выполнено |
| `mango_ba_prompts` | 556 ссылок по SHA (переживут надгробие), 48 плавающих в 21 файле (сломаются на Ш3.6) |
| `mango-ba-ai-runtime` | 0 ссылок; `hub_commit: dbf3baa…` |
| `aether-orbis`, `aether-orbis-gra` | 0 ссылок |

Пустой `diff` нового снимка с базовым означает, что параметры и задачи выноса
действуют без правки; иначе каждая строка разницы — пункт сверки в B-243.
