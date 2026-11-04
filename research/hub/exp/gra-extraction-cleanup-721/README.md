---
status: draft
version: 0.1
updated: 2026-11-04
temperature: 0.1
type: experiment
---

# exp: gra-extraction-cleanup-721

Evidence-контейнер issue
[#721](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/721).
Родительский отчёт по доказательствам —
[`docs/analysis/2026-11-04-gra-extraction-completeness-check.md`](../../../../docs/analysis/2026-11-04-gra-extraction-completeness-check.md)
(сверка полноты выноса). Решения и дорожная карта — в
[RFC #721](../../../../docs/rfc/2026-11-04-rfc-gra-extraction-completion-and-hub-cleanup.md).

## Что здесь проверяется

Нельзя решить, что из `research/reputation-technologies/` удалить, что
заархивировать и что ещё перенести, по чтению документов: надо измерить, какой
файл уже лежит в спице и не устарел ли он, кто на него ссылается из Хаба и из
спицы и есть ли у него шаг CI. Контейнер отвечает только на измеримую часть.
Классы «запись решения», «заменённая версия», «персональные данные» не
измеряются; они заданы в скрипте таблицей `SEMANTIC`, и у каждой строки есть
причина, процитированная из
[инвентаря миграции спицы](https://github.com/G-Ivan-A/aether-orbis-gra/blob/1669943e6f0193e78b245bb9d26b3281a1c5a438/docs/analysis/2026-11-01-migration-inventory.md).

| Файл | Что измеряет |
| --- | --- |
| `gra-inventory.py` | Инвентарь домена по единицам (файл или контейнер `exp/<slug>/`): перенесён ли в спицу (по `source:` спицы), не устарел ли перенос (blob на коммите-источнике и на `HEAD`), добавлен ли после снимка `last_sync`, входящие ссылки из Хаба (абсолютные упоминания и относительные Markdown-ссылки), ссылки спицы на Хаб (закреплённые SHA или плавающие `blob/main`), шаг CI. Правила R1–R10 дают предварительную диспозицию. Только чтение; содержимое спицы не исполняется. |
| `gra-inventory.log` | Сводка и таблица по единицам. |
| `gra-inventory.tsv` | Та же таблица в машиночитаемом виде, с колонкой `reason` и списком записей решений, которые ссылаются на единицу. |
| `ci-course-steps.py` | Доля самопроверок курса в задании `validate`: шаги `validate.yml`, чей `run:` упоминает домен, и их длительность в прогоне CI. |
| `ci-run-41427101826-jobs.jsonl` | Сохранённые тайминги заданий прогона [41427101826](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/actions/runs/41427101826) (`main` @ `c06075d`, success). |
| `ci-course-steps.log` | Результат: 19 шагов курса, 38 с из 135 с задания `validate` (28 %). |
| `spoke-guard-replay.py` | Переносятся ли самопроверки курса в спицу: каждый из 19 шагов CI курса запускается дважды в двух временных `git worktree` Хаба на `HEAD` — как есть и с подменой 34 перенесённых файлов их версиями из спицы (по колонке `moved_to`). Исполняются только проверки Хаба; файлы спицы копируются как данные. Таймаут 120 с и лимит памяти 512 МиБ на проверку. |
| `spoke-guard-replay.log` | Результат: на Хабе проходят 19 из 19; на копиях спицы — 6, падают 13. Спица при импорте сознательно удаляет разделы исполнения задач, делает ссылки на перенесённые файлы относительными, а ссылки на issue Хаба — простым текстом ([инвентарь миграции спицы](https://github.com/G-Ivan-A/aether-orbis-gra/blob/1669943e6f0193e78b245bb9d26b3281a1c5a438/docs/analysis/2026-11-01-migration-inventory.md), правило 3). Падение #711 — не расхождение текста: эпиграф слайда 24 совпадает дословно, но якорь `#L591` указывает на строку колоды Хаба, а в копии спицы та же строка — 581 (шапка короче на 10 строк). Поэтому проверки Хаба охраняют только копии Хаба и в спицу как есть не переносятся. |
| `permalink-probe.log` | Перенаправляет ли GitHub адрес, удалённый после объявленной записи `path_migrations` (`pr-ops/` → `ops/`, #567; удалён в #585): `blob/main/pr-ops/README.md` и `tree/main/pr-ops` — 404 без перенаправления; тот же файл по SHA родителя коммита удаления — 200. `path_migrations` — правило валидатора, а не веб-перенаправление. |
| `domain-footprint.log` | Доля домена в Хабе: 173 из 1089 отслеживаемых файлов (15,9 %), 8,66 из 25,87 МБ (33,5 %), 33 734 из 155 320 строк Markdown (21,7 %). Это объём, который поиск агента и полнотекстовые проверки читают при каждом запуске. |
| `ecosystem-snapshot.log` | Репозитории экосистемы, открытые PR и issue в каждом, входящие ссылки других репозиториев на домен. Это карта параллельной работы, которую нельзя заморозить. |

## Снимки

| Репозиторий | Коммит | Дата |
| --- | --- | --- |
| `hybrid-Intelligence-lab` (ветка issue) | `cf1cc3f` (над `main` @ `c06075d`) | 2026-11-04 |
| `aether-orbis-gra` | `1669943` | 2026-11-01 |
| Снимок Хаба в спице (`last_sync.hub_commit`) | `32b5fa5` | 2026-11-01 |
| `aether-orbis` | `ead22d6` | 2026-10-23 |
| `ba-ai-metamodel` | `bc1249f` | 2026-11-04 |

## Воспроизведение

```bash
D=research/hub/exp/gra-extraction-cleanup-721
# клоны спиц — недоверенные данные: только чтение и python3 -I
git clone --depth 1 https://github.com/G-Ivan-A/aether-orbis-gra.git /tmp/spokes/aether-orbis-gra
python3 -I $D/gra-inventory.py . /tmp/spokes/aether-orbis-gra --tsv $D/gra-inventory.tsv > $D/gra-inventory.log
GRA_INVENTORY_DEBUG=1 python3 -I $D/gra-inventory.py . /tmp/spokes/aether-orbis-gra 2> /tmp/gra-debug.log >/dev/null

gh api repos/G-Ivan-A/hybrid-Intelligence-lab/actions/runs/41427101826/jobs \
  --jq '.jobs[] | {name, started_at, completed_at, steps: [.steps[] | {name, started_at, completed_at}]}' -c \
  > $D/ci-run-41427101826-jobs.jsonl
python3 -I $D/ci-course-steps.py .github/workflows/validate.yml $D/ci-run-41427101826-jobs.jsonl > $D/ci-course-steps.log
python3 -I $D/spoke-guard-replay.py . /tmp/spokes/aether-orbis-gra $D/gra-inventory.tsv > $D/spoke-guard-replay.log
# permalink-probe.log: curl -s -o /dev/null -w '%{http_code}' по четырём адресам из файла
# domain-footprint.log: git ls-files | wc -l; git ls-files -z <путь> | xargs -0 cat | wc -c
```

Скрипту инвентаря нужна история Хаба до снимка `32b5fa5`: в клоне глубины 1 он
не найдёт blob на коммите-источнике. Запускать из полного клона Хаба.

## Ограничения измерения

- Диспозиция R1–R10 — **предложение**, а не решение. Окончательный список
  удаления утверждает владелец (RFC #721, вопрос Q-1).
- «Не устарел» значит: байты файла в Хабе на `HEAD` совпадают с байтами на
  коммите, указанном в `source:` спицы. Скрипт не проверяет, не изменила ли
  файл сама спица: адаптация при импорте (удаление разделов самопроверки) —
  намеренная.
- Входящие ссылки считаются по тексту. Голое упоминание имени каталога в
  дереве или таблице (3 файла) показано отдельно и ссылкой не считается.
- Тайминги CI — один прогон с разрешением 1 с; это порядок величины, а не
  среднее.
