---
status: draft
version: 0.1
updated: 2026-07-01
temperature: 0.1
report-subtype: report
scope: repo
based_on: "docs/analysis/2026-07-01-reports-artifacts-inventory.md + standards/research-standard.md"
owner: G-Ivan-A
type: report
context: [hub, reports, review, pr-312, issue-310, placement-analysis, rfc-b-016]
method: root-cause-analysis
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/310"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/310"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/312"
related_artifacts:
  - "docs/rfc/2026-06-30-rfc-research-structure.md"
  - "docs/analysis/2026-07-01-reports-artifacts-inventory.md"
  - "research/hub/exp/reports-inventory-310/README.md"
  - "standards/research-standard.md"
  - "pr-ops/backlog.md"
  - "standards/report-standard.md"
---

# Отчёт: анализ размещения deliverables инвентаризации Reports (issue #310)

## Контекст

Источник задачи: [issue #310](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/310)
(backlog B-038), доработка в рамках [PR #312](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/312).

При review PR #312 фаундер зафиксировал, что сам контент инвентаризации хороший,
но PR не может быть смержен, пока не устранены два дефекта размещения:

1. **Legacy-формат exp-контейнера.** Executor создал новый воспроизводимый
   корпус в старом sibling-формате `research/hub/exp-reports-inventory-310/`,
   тогда как целевой формат по RFC B-016 v0.2 (P1) — контейнер
   `research/hub/exp/reports-inventory-310/`. Создание нового контейнера в
   старом формате плодит legacy-дрейф.
2. **Неверная маршрутизация Analysis.** Файл
   `research/hub/2026-07-01-reports-artifacts-inventory.md` — это инвентаризация,
   то есть Analysis, а не Research. По RFC B-016 v0.2 (P4) Analysis
   маршрутизируется в `docs/analysis/YYYY-MM-DD-name.md`.

Нормативные контракты проверки: legacy `standards/research-profile.md`
(действующий legacy-профиль), [`docs/rfc/2026-06-30-rfc-research-structure.md`](../rfc/2026-06-30-rfc-research-structure.md)
(RFC B-016 v0.2, status:draft, но формат контейнера принят в `main` через
PR #303), [ADR-001](../adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md),
[ADR-002](../adr/2026-06-adr-002-artifact-document-methodology.md) и видение
фаундера §3 (`research/hub/2026-06-23-repository-structure-concept.md`).

## Вердикт

Оба дефекта размещения подтверждены. Контент deliverables корректен, но их
физическое расположение нарушало действующий целевой контракт структуры
research (RFC B-016 v0.2) в двух местах: формат exp-контейнера (P1/P2) и
маршрутизация Analysis (P4). Оба дефекта исправлены в этом PR перед merge;
контент инвентаризации и матрицы не менялся.

## Фактические причины размещения

Ниже зафиксированы действительные причины, по которым executor выбрал исходное
размещение, а не идеализированное объяснение.

| Решение executor'а | Фактическая причина | Оценка |
| --- | --- | --- |
| exp-корпус создан как `research/hub/exp-reports-inventory-310/`. | Executor копировал паттерн уже существующих в `main` sibling-контейнеров (`exp/rfc-adr-industry-norms-278/`, `exp/ripple-effects-282/`, `exp/research-analysis-audit-288/`) как наиболее близкий пример. `research-profile.md` описывает именно legacy sibling-форму, а RFC B-016 (целевой контейнер `exp/<slug>/`) имеет status:draft. При выборе между «как в соседних папках» и «как в draft RFC» executor выбрал наблюдаемый прецедент. | Причина понятна, но ошибочна: формат контейнера `exp/<slug>/` уже принят в `main` через PR #303, поэтому новый корпус должен был создаваться в целевом формате, а не в legacy. |
| Вложенный `outputs/` внутри exp-корпуса. | Тот же копипаст legacy-примеров, где evidence лежит в `outputs/`. | Ошибочно: RFC B-016 v0.2 (P2) прямо запрещает вложенный `outputs/` и требует плоскую структуру внутри `exp/<slug>/`. Legacy sibling-папки ещё используют `outputs/`, их миграция отложена в B-022, но новый контейнер не должен воспроизводить запрещённый паттерн. |
| Инвентаризация размещена в `research/hub/2026-07-01-reports-artifacts-inventory.md`. | Задача B-038 трактовалась как продолжение research-цепочки Reports (предыдущий артефакт `2026-06-30-reports-industry-norms-and-standardization-scope.md` лежит в `research/hub/`), поэтому executor разместил следующий шаг рядом. | Ошибочно: сам файл во frontmatter имеет `type: internal-analysis` и по содержанию является инвентаризацией/классификацией (Analysis). По RFC B-016 v0.2 (P4) Analysis маршрутизируется в `docs/analysis/`, а не в `research/<domain>/`. Соседство с предыдущим research-файлом не является контрактным основанием для маршрутизации. |

Ключевая улика по второму дефекту: frontmatter самого файла заявляет
`type: internal-analysis`. Это подтверждает, что артефакт — Analysis, и
опровергает выбор research-маршрута.

## Анализ соответствия контрактам

| Контракт | Что требует | Исходное состояние | Итог |
| --- | --- | --- | --- |
| RFC B-016 v0.2, P1 | Контейнер `research/<domain>/exp/<issue-slug>/`. | `research/hub/exp-reports-inventory-310/` (legacy sibling). | Не соответствовало. |
| RFC B-016 v0.2, P2 | Плоская структура внутри `exp/<issue-slug>/`, запрет вложенного `outputs/`. | Внутри был вложенный `outputs/`. | Не соответствовало. |
| RFC B-016 v0.2, P4 | Analysis → `docs/analysis/YYYY-MM-DD-name.md`. | Инвентаризация лежала в `research/hub/`. | Не соответствовало. |
| `standards/research-profile.md` (legacy) | Описывает sibling-форму `exp-<slug>/` с `outputs/`. | Исходное размещение формально соответствовало legacy-профилю. | Соответствовало legacy, но legacy — источник дрейфа; целевой контракт приоритетнее. |
| ADR-001 / ADR-002 | Разделение методологической инфраструктуры и артефактной методологии; `exp/` = research evidence corpus, `runs/` = operational run record. | exp-корпус — корректно evidence corpus, не `runs/`. | Соответствовало по существу; дефект только в форме пути. |
| Видение фаундера §3 | Reports — базовый подкаталог `docs/`; аккуратная маршрутизация артефактов. | Инвентаризация вне `docs/`. | Не соответствовало духу маршрутизации. |

Расхождение между `research-profile.md` (legacy sibling-форма) и RFC B-016 v0.2
(целевой контейнер) — корневая причина обоих дефектов: executor опирался на
действующий профиль и наблюдаемые соседние папки, а не на уже принятый в `main`
целевой формат контейнера.

## Внесённые исправления

1. **Перемещение и flatten exp-контейнера.**
   `research/hub/exp-reports-inventory-310/` → `research/hub/exp/reports-inventory-310/`
   (P1). Вложенный `outputs/` удалён, evidence-файлы (`reports-inventory.json`,
   `2026-07-01-reports-artifact-matrix.md`) перенесены рядом с `README.md` и
   `scan-reports.py` (P2). В `README.md` и `scan-reports.py` обновлены
   self-ссылки, путь `--out-dir` и `SELF_PREFIXES`.

   Flatten выходит за пределы буквальной формулировки review (там был назван
   только P1), но применён сознательно: сохранить `outputs/` в новом целевом
   контейнере означало бы воспроизвести ровно тот дрейф, который запрещает P2, и
   создать новый legacy внутри уже целевой формы. Это согласуется с намерением
   review «не плодить дрейф».

2. **Перемещение инвентаризации.**
   `research/hub/2026-07-01-reports-artifacts-inventory.md` →
   [`docs/analysis/2026-07-01-reports-artifacts-inventory.md`](../analysis/2026-07-01-reports-artifacts-inventory.md)
   (P4). Обновлены внутренние ссылки на матрицу и скрипт корпуса, на research
   Variant-C и обратные ссылки из корпуса.

3. **Синхронизация реестров и навигации.** Обновлены `pr-ops/artifact-map.md`
   (строки инвентаризации и exp-контейнера перенесены в блоки `docs/analysis` и
   `research/hub/exp/`, добавлена строка этого отчёта), `pr-ops/backlog.md`
   (frontmatter `related_artifacts` и ссылка B-038), `research/README.md`,
   `research/hub/README.md`, `mkdocs.yml` (инвентаризация в раздел «Анализы»,
   отчёт в «Отчёты», удалена запись из Hub), `CHANGELOG.md` и
   `tools/validate-repository-structure.sh` (allowlist, `required_files`,
   per-file `require_text`).

## Рекомендации по уточнению контрактов

Чтобы предотвратить повтор, рекомендуется (решение за фаундером, без создания
норм в этом PR):

1. **Пометить legacy sibling-форму в `standards/research-profile.md` как
   deprecated-on-create.** Явно указать, что новые корпуса создаются только в
   формате `exp/<issue-slug>/` (RFC B-016 v0.2), а `exp-*` sibling-папки — только
   существующие, ожидающие миграции в B-022. Сейчас профиль описывает legacy как
   действующую форму, что и спровоцировало копирование.
2. **Поднять статус RFC B-016** (или зафиксировать принятый P1/P2/P4 в ADR
   B-017), чтобы целевой контракт структуры имел приоритет над наблюдаемым
   legacy-прецедентом на уровне статуса, а не только фактического merge PR #303.
3. **Добавить в чек-лист DoR/DoR-check для research/analysis задач явный шаг
   маршрутизации по типу** (Research → `research/<domain>/`, Analysis →
   `docs/analysis/`, Audit → `docs/audit/`, Report → `docs/report/`) со сверкой с
   `type` во frontmatter. Frontmatter `type: internal-analysis` должен был сразу
   привести к `docs/analysis/`.
4. **Расширить `tools/validate-repository-structure.sh` эвристикой**, которая
   предупреждает при создании нового `research/hub/exp-*` sibling-каталога
   (вне уже известного legacy-списка) и при появлении `outputs/` внутри
   `research/**/exp/**`.

## Проверка

Локальная проверка после исправлений:

```bash
bash experiments/test-frontmatter-validator.sh      # frontmatter tests
./tools/validate-file-naming.sh                     # date-first naming
./tools/validate-frontmatter.sh .                   # frontmatter
./tools/validate-repository-structure.sh            # structure + links + map
python3 tools/generate-manifest.py --check          # manifest
bash -n tools/*.sh templates/htom/tools/*.sh templates/spoke/tools/*.sh
```

`./tools/validate-mkdocs-site.sh` требует установленного `mkdocs-material`;
финальная проверка сайта выполняется в CI, где зависимость устанавливается перед
шагом сборки.
