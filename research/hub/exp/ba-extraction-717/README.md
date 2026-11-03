---
status: draft
version: 0.1
updated: 2026-11-03
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

## Файлы

| Файл | Назначение |
| --- | --- |
| `name-availability.py` | Зонд имён: GitHub (точное имя, итог поиска `in:name`, собственное пространство с переадресацией), GitLab, Codeberg, Hugging Face, PyPI, npm. Только публичные API на чтение |
| `name-availability.log` | Вывод зонда: строка JSON на имя и итоговая таблица |
| `2026-11-03-web-search.md` | Веб-поиск точных фраз для трёх имён из постановки и ведущей альтернативы |
| `ba-instance-params.txt` | Блок `extraction-params` проекта метамодели БА: `MAP`, `DIR`, `CI_JOB`, `CI_STEP`, `BACKLOG`, `HISTORICAL` |
| `rehearse-contract.sh` | Репетиция этапов E1, E2, E3, E5 и сканирования E4 в локальном git-репозитории |
| `rehearse-contract.log` | Вывод репетиции (без построчного JSONL журнала ссылок) |

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
