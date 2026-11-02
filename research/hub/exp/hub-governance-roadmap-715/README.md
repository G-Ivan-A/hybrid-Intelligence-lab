---
status: draft
version: 0.1
updated: 2026-11-02
temperature: 0.1
type: experiment
---

# exp: hub-governance-roadmap-715

Evidence-контейнер для
[`docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md`](../../../../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md),
issue [#715](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/715).

Родительские отчёты по доказательствам — анализы issue #713:
[mango_ba_prompts](../../../../docs/analysis/2026-11-02-mango-ba-prompts-hub-practice-transfer-check.md)
и [aether-orbis-gra](../../../../docs/analysis/2026-11-02-aether-orbis-gra-hub-practice-transfer-check.md).
Контейнер расширяет их проверку двух спиц до матрицы всех семи репозиториев
экосистемы и добавляет измерения самого Хаба. Отдельный Analysis не создаётся:
по постановке #715 результат — один артефакт, RFC.

## Что здесь проверяется

RFC предлагает упорядоченную дорожную карту оптимизации Хаба и управления
спицами. Порядок шагов и число задач на шаге нельзя обосновать чтением
документов: нужно измерить, **где именно** сосредоточены объём, бэклог, CI и
расхождения спиц. Контейнер отвечает только на измеримую часть. Приоритизация,
обоснование и решения — в родительском RFC.

| Файл | Что измеряет |
| --- | --- |
| `backlog-census.py` | Строки `ops/backlog.md` по спринтам: статусы, повторяющиеся ID. Только чтение. |
| `backlog-census.log` | Прогон на `main` @ `3d25a38` (2026-11-02). |
| `hub-status-census.py` | Статусы frontmatter Markdown-файлов Хаба по областям и пул «открытых» (draft/proposed/review) документов без обновления с отсечки. Только чтение. |
| `hub-status-census.log` | Прогон с отсечкой `2026-09-01` на `3d25a38`. |
| `spoke-consistency-matrix.py` | Матрица согласованного чтения: наличие домов Хаба (AGENTS.md, `.hub-profile.json`, `ops/backlog.md`, шаблоны задач, CI, инструмент синка) в каждом репозитории экосистемы. Только чтение файлов; содержимое спиц не исполняется. |
| `spoke-consistency-matrix.log` | Прогон по клонам depth 1 (снимки ниже). |

## Снимки

| Репозиторий | Коммит | Дата |
| --- | --- | --- |
| `hybrid-Intelligence-lab` | `3d25a38` | 2026-11-02 |
| `mango_ba_prompts` | `1bd4829` | 2026-11-02 |
| `mango-ba-ai-runtime` | `5d8c201` | 2026-11-01 |
| `aether-orbis-gra` | `1669943` | 2026-11-01 |
| `aether-orbis` | `ead22d6` | 2026-10-23 |
| `open-ai.ru` | `cbc0d40` | 2026-06-09 |
| `clarify-engine-ai` | `96c288f` | 2026-05-21 |

## Воспроизведение

```bash
python3 research/hub/exp/hub-governance-roadmap-715/backlog-census.py > research/hub/exp/hub-governance-roadmap-715/backlog-census.log
python3 research/hub/exp/hub-governance-roadmap-715/hub-status-census.py 2026-09-01 > research/hub/exp/hub-governance-roadmap-715/hub-status-census.log
# клоны спиц — недоверенные данные: только чтение и python3 -I
python3 -I research/hub/exp/hub-governance-roadmap-715/spoke-consistency-matrix.py . /tmp/spokes/<repo> ...
```

Ручные подсчёты, которые RFC использует дополнительно (команды приведены для
повторения):

| Факт | Команда | Значение на `3d25a38` |
| --- | --- | --- |
| Файлов в `projects/ba-ai-process/` | `git ls-files projects/ba-ai-process \| wc -l` | 303 |
| Файлов в `research/reputation-technologies/` | `git ls-files research/reputation-technologies \| wc -l` | 173 |
| Явных путей в списках разрешений `tools/validate-repository-structure.sh` | `grep -cE '^\s+[a-zA-Z._/-][^ ]* \| \\$' tools/validate-repository-structure.sh` | ~800 из 3397 строк |
| Шагов `run:` в `.github/workflows/validate.yml` | `grep -c 'run:' .github/workflows/validate.yml` | 69 |
| Из них самопроверок курса (`research/reputation-technologies/exp/...`) | `grep -c 'research/reputation-technologies' .github/workflows/validate.yml` | 22 |
| Из них шагов BA-пакетов (`projects/ba-ai-process`, `*-package`, `bcreq`, `ba-meta`) | см. RFC | 25 |

## Ограничения измерения

- Статус `draft` для `research/` — нормальное состояние жизненного цикла, а не
  дефект. Пул из 207 документов — **верхняя граница кандидатов** на триаж
  шага 5 RFC, а не список на удаление.
- Классификация строк бэклога по направлениям (BA / Хаб / курс) сделана по
  заголовку спринта; строки внутри спринта не переклассифицировались.
- Матрица спиц проверяет наличие файла, а не качество содержимого. Качество
  передачи практик измерено в анализах issue #713.
