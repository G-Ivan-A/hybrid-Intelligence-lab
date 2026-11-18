---
status: draft
version: 0.4
updated: 2026-11-17
temperature: 0.1
type: experiment
---

# exp: ba-extraction-717

Контейнер доказательств для анализа
[`../../../../docs/analysis/2026-11-03-ba-meta-model-extraction-step1.md`](../../../../docs/analysis/2026-11-03-ba-meta-model-extraction-step1.md)
и контракта
[`../../../../ops/hub-project-extraction-contract.md`](../../../../ops/hub-project-extraction-contract.md),
issue [#717](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/717).
Возобновление выноса (B-243, Ш3.0) — issue
[#738](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/738),
анализ [`../../../../docs/analysis/2026-11-16-hub-optimization-start.md`](../../../../docs/analysis/2026-11-16-hub-optimization-start.md).

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
| `drift-54face1.log` | Снимок B-243 при `54face1` и `main` экосистемы на 2026-11-16, с разделом `## since c06075d` (коммиты и файлы источников после базового снимка) |
| `rehearse-contract-54face1.log` | Итог репетиции E1, E2, E3, E5 и сканирования E4 при `HUB_SHA` = `54face1` (инструмент — из `HUB_SHA`, как в контракте) |
| `freeze-window-2026-11-16.log` | Окно заморозки: открытые PR и issue каждого репозитория экосистемы, дерево `ba-ai-metamodel`, дома согласованного чтения спиц |
| `pin-spoke-links.py` | B-249: переписывает плавающие ссылки на вынесенные пути Хаба (`blob|tree|raw/<ветка>/…`) на тот же объект в `ba-ai-metamodel` при закреплённом SHA; `--check` и `--verify-target` |
| `tombstone.py` | B-249: генерирует надгробия `projects/ba-ai-process/README.md`, `research/mango/README.md` (манифест redirect: прежний путь → путь в спице при SHA приёмки E6) и `docs/ba-meta-model-overview.md`; `--check` сравнивает без записи |
| `tombstone-e1f67e2.log` | Вывод `tombstone.py --check` при SHA спицы `e1f67e2` |

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

```bash
# надгробия B-249: клон ba-ai-metamodel в отдельном пустом каталоге
python3 -I research/hub/exp/ba-extraction-717/tombstone.py --hub . \
  --spoke /tmp/eco/ba-ai-metamodel --spoke-sha e1f67e267beb73809e1edb26313691a5c769c92a --check
# плавающие ссылки спицы экосистемы (без --check переписывает)
python3 -I research/hub/exp/ba-extraction-717/pin-spoke-links.py --repo /tmp/eco/mango_ba_prompts \
  --sha e1f67e267beb73809e1edb26313691a5c769c92a --verify-target /tmp/eco/ba-ai-metamodel --check
```

```bash
# заморозка источников на стороне Хаба (шаг CI validate до B-249)
bash tools/check-extraction-freeze.sh research/hub/exp/ba-extraction-717/ba-instance-params.txt
bash tools/test-extraction-freeze.sh
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

## Сверка B-243 (`HUB_SHA` = `54face1`, 2026-11-16)

Триггер B-243 — решение владельца в issue
[#738](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/738): работа
над `mango_ba_prompts` и связанными репозиториями на паузе два дня. Новый
`HUB_SHA` — `main` на момент решения (`54face1`, merge PR #737).

| Строка разницы с базовым снимком | Куда отнесена |
| --- | --- |
| Источники 322 → 324 файла: 2 коммита #719 (правило PT-5), `M ba-meta-model/20-taxonomy.md`, `A experiments/issue_719_runtime_compile_check.{log,sh}` | Покрыто `MAP: projects/ba-ai-process/=`; параметры не меняются |
| `dir experiments`: 34 → 36 файлов | Каталог объявлен в `DIR`; без изменений |
| Хаб: 85 → 91 файл упоминает источники (ADR-022, анализ шага 1, RFC #721, `docs/ecosystem-map.md`, этот контейнер) | Исторические записи остаются; живые указатели — в B-249 |
| Бэклог: раздел «Спринт 30» упоминает источники (34 строки) | Раздел остаётся в Хабе (задачи выноса); `BACKLOG` не меняется |
| `mango_ba_prompts`: плавающих ссылок 48 в 21 файле → 162 в 78 файлах; по SHA — 556 без изменений | B-249: закрепить или переписать до удаления источников |
| `mango-ba-ai-runtime`: закрепление `dbf3baa` → `b3a9e16` | B-248 переводит закрепление на коммит нового репозитория |
| CI: шаги и задания | Без изменений: `CI_STEP` и `CI_JOB` действуют |

| Проверка | Результат |
| --- | --- |
| Шаг 0 | Заморозка: 0 коммитов в источниках после `HUB_SHA`; манифест — 324 файла |
| E1 | Геном — 9 файлов; пересечение с переносом и расхождение каталогов с `DIR` пусты; валидаторы генома проходят |
| E2 | 193 исторических пути; 234 коммита; конфликт — `README.md` |
| E3 | 75 файлов: `url-in` 490, `file-out` 64; повторный `--check` — 0 файлов |
| E4 | `scan` — 366 строк |
| E5 | 13 разделов, 100 строк `B-`; валидаторы проходят |
| Цель | `ba-ai-metamodel@bc1249f` — один `README.md`, один коммит |
| Окно | Открытых PR и issue, меняющих источники, нет ни в одном репозитории экосистемы |

Заморозку держит шаг CI Хаба «Check BA meta-model extraction source freeze»
(`tools/check-extraction-freeze.sh`): любой коммит в путях `MAP` после
`HUB_SHA` роняет `validate`. Шаг удаляет PR надгробия B-249 (см. ниже). Задача выноса —
[ba-ai-metamodel#1](https://github.com/G-Ivan-A/ba-ai-metamodel/issues/1);
её блок `extraction-params` побайтно совпадает с `ba-instance-params.txt`.

## Надгробие B-249 (2026-11-17)

Приёмка E1–E6 в спице — PR #2–#7, коммит `e1f67e2` (merge PR #7). Перед
удалением источников последняя проверка заморозки на `main` Хаба:
`extraction freeze OK: 8 source path(s) unchanged in 54face1..24cd7ff`.

| Шаг | Результат |
| --- | --- |
| Сверка путей | Все 318 путей источников при `54face1` есть в спице при `e1f67e2` (`tombstone.py` падает, если хоть одной цели нет) |
| Удаление | `projects/ba-ai-process/`, `research/mango/`, `docs/ba-meta-model-overview.md`, пять тестов `MAP` и `tools/test-ba-requirements-forensics.sh` (проверял удалённые анализ и RFC проекта, в CI не входил) |
| Надгробия | `projects/ba-ai-process/README.md` — 304 строки манифеста, `research/mango/README.md` — 12, обзор — совместимый редирект; `--check` — `tombstone-e1f67e2.log` |
| `path_migrations` | Два префикса в `.hub-profile.json` с архивом `archive/ba-ai-process-2026-11` и `archive/mango-research-2026-11` при `54face1`; относительные ссылки исторических документов разрешает манифест (0 битых ссылок валидатора структуры) |
| CI Хаба | Сняты 7 шагов `CI_STEP`, 3 задания `CI_JOB` и шаг заморозки; общий `tools/check-extraction-freeze.sh` с тестом остаются для следующих выносов |
| Живые указатели | `README.md`, `projects/README.md`, `research/README.md`, `docs/ecosystem-map.md`, `ops/artifact-map.md`, гайд `education-ba-prompt` (14 ссылок закреплены на спицу) |
| `mango-ba-ai-runtime` | B-248: [PR #24](https://github.com/G-Ivan-A/mango-ba-ai-runtime/pull/24) — `source_ssot`/`source_commit` на `ba-ai-metamodel@e1f67e2` |
| `mango_ba_prompts` | 162 плавающие ссылки в 78 файлах: 61 в 33 файлах закреплена ([PR #489](https://github.com/G-Ivan-A/mango_ba_prompts/pull/489)); 101 в 45 файлах под побайтовыми замками опубликованных промптов, черновиков, архива и входов замеров — [issue #488](https://github.com/G-Ivan-A/mango_ba_prompts/issues/488), регрессионный валидатор не даёт числу расти |

Остаток: 101 плавающая ссылка `mango_ba_prompts` до выпуска промптов отвечает
404 на `main` Хаба; адрес того же объекта — манифест надгробия. Архивные теги
ставит workflow `archive-tag` после слияния; при отказе прав `GITHUB_TOKEN`
тег ставит владелец (B-281).
