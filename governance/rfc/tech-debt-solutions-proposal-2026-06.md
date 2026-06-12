---
status: draft
version: 0.1
updated: 2026-06-11
temperature: 0.1
---

# RFC: Предложения по решению техдолга

**Дата:** 2026-06-11
**Автор:** @konard
**Статус:** Draft

## Executive Summary

Аудит задач 1-4 показывает, что основные deliverables выполнены, но вокруг них
накопился операционный техдолг: не до конца формализован handover prompt, Smart
Sync проверяется локальным experiment script без fixture-spoke контракта,
политика generated artifacts противоречива, а backlog нуждается в актуализации
после серии закрытых задач.

Предлагаемое решение: закрыть два P1-долга отдельными малыми задачами, затем
формализовать правила generated artifacts и обновить backlog как отражение
факта, а не плана.

## Текущее состояние техдолга

| # | Проблема | Приоритет | Оценка |
| --- | --- | --- | --- |
| 1 | Нет стандарта требований к `AI_SESSION_HANDOVER_PROMPT.md` | P1 | M |
| 2 | Нет fixture-spoke проверки Smart Sync для HTOM/spoke templates | P1 | M |
| 3 | Не создан `templates/task-for-konard.md` | P2 | S |
| 4 | Политика generated HTML/PNG artifacts не формализована | P2 | S |
| 5 | `governance/backlog.md` может не отражать уже закрытые CE-задачи | P2 | M |
| 6 | Выводы JS CI/CD research не связаны с минимальным spoke CI contract | P3 | M |

## Анализ проблем

### Проблема 1: Handover prompt не имеет отдельного стандарта

**Описание:** `templates/htom/AI_SESSION_HANDOVER_PROMPT.md` существует и
семантически отделён от onboarding protocol, но требования к его структуре,
обязательным секциям, readback и границам копируемого текста не вынесены в
отдельный standard/RFC.

**Влияние:** новые handover prompt изменения будут оцениваться ad hoc, без
единого review checklist.

**Корневая причина:** issue #207 правильно разделил артефакты, но не должен был
одновременно создавать полноценный стандарт для каждого из них.

### Проблема 2: Smart Sync не проверяется на реалистичном spoke-fixture

**Описание:** есть `experiments/test-smart-sync.sh`, но нет отдельного
минимального fixture, который моделирует downstream HTOM/spoke repository и
проверяет, что шаблоны применяются без порчи локальных правок.

**Влияние:** изменения `templates/htom/`, `templates/spoke/`,
`templates/sync-metadata.json` и `templates/manifest.json` могут проходить
локальные проверки, но ломать downstream bootstrap/sync сценарий.

**Корневая причина:** Smart Sync был создан как инфраструктурный пакет, а не как
полноценная интеграционная test harness для нескольких типов репозиториев.

### Проблема 3: Нет `templates/task-for-konard.md`

**Описание:** issue #213 указывает шаблон задачи для Конарда как техдолг, но
такого файла в текущем дереве нет.

**Влияние:** задачи для AI-исполнителя продолжают зависеть от issue template и
ручного контекста, хотя повторяемый формат можно вынести в шаблон.

**Корневая причина:** приоритет был ниже, чем у HTOM/spoke и Smart Sync
разделения.

### Проблема 4: Политика generated artifacts противоречива

**Описание:** `.gitignore` исключает `/site/`, но не `*.html` или `*.png`. В
репозитории уже есть committed HTML в `research/mango/` и PNG screenshots в
`docs/screenshots/`. При этом issue #213 запрещает коммитить generated HTML/PNG.

**Влияние:** review-скриншоты полезны, но без политики каждый PR заново решает,
является ли PNG исходным evidence artifact или запрещённым generated output.

**Корневая причина:** правила для MkDocs build output, research exports и PR
review screenshots смешаны в одну категорию "generated files".

### Проблема 5: Backlog может быть неактуален

**Описание:** `governance/backlog.md` содержит CE-задачи со статусом TODO, хотя
часть соответствующих issues уже закрыта и замержена.

**Влияние:** backlog перестаёт быть источником фактического состояния и требует
повторной ручной проверки перед планированием.

**Корневая причина:** backlog обновлялся как план, а не синхронизировался после
каждого merged PR.

### Проблема 6: JS CI/CD research не превращён в spoke CI contract

**Описание:** анализ CI/CD шаблона оформлен как research, но связь с
`templates/spoke/.github/workflows/ci.yml` и минимальными expectations для
production-spoke не формализована.

**Влияние:** spoke template остаётся провайдер-агностичным skeleton без
явного пути развития.

**Корневая причина:** исходная задача была исследовательской, а не
implementation/standardization task.

## Предложения по решению

### Решение 1: Стандарт `AI_SESSION_HANDOVER_PROMPT.md`

**Описание:** создать короткий standard или RFC, который фиксирует обязательные
секции handover prompt: назначение, copied block boundaries, required context,
readback, ограничения, проверка актуальности ссылок.

**Плюсы:** снижает риск разъезда onboarding protocol и handover prompt; даёт
review checklist.

**Минусы:** добавляет один governance artifact, который нужно поддерживать.

**Оценка:** M
**Приоритет:** P1

### Решение 2: Fixture-spoke проверка Smart Sync

**Описание:** расширить `experiments/test-smart-sync.sh` или добавить отдельный
fixture в `experiments/`, который создаёт временный HTOM/spoke repo profile,
запускает `tools/sync-from-hub.sh --report`, `--apply`, `--force` и проверяет
локальные правки.

**Плюсы:** ловит реальные регрессии Smart Sync до merge; сохраняет тест как
исполняемую документацию.

**Минусы:** увеличивает время локальной проверки и требует аккуратного fixture
cleanup.

**Оценка:** M
**Приоритет:** P1

### Решение 3: Шаблон задачи для Конарда

**Описание:** создать `templates/task-for-konard.md` как lightweight wrapper над
issue template: входной контекст, expected autonomy, required checks, PR update
rules, evidence requirements.

**Плюсы:** уменьшает ручное копирование инструкций в будущих AI-задачах.

**Минусы:** риск дублирования с `.github/ISSUE_TEMPLATE/task.md`, если не
сделать его тонким и ссылочным.

**Оценка:** S
**Приоритет:** P2

### Решение 4: Generated artifacts policy

**Описание:** зафиксировать три класса файлов:

- build output: `/site/`, cache, временные exports; не коммитить;
- source-like research exports: допустимы только если являются самостоятельным
  артефактом и зарегистрированы;
- review evidence screenshots: допустимы в `docs/screenshots/` или отдельном
  agreed path, если нужны PR/issue verification.

**Плюсы:** снимает противоречие между запретом PNG и требованием screenshots в
визуальных PR.

**Минусы:** требует точного wording, чтобы не открыть дверь для мусорных
generated files.

**Оценка:** S
**Приоритет:** P2

### Решение 5: Backlog status refresh

**Описание:** отдельной задачей сверить `governance/backlog.md` с закрытыми
issues/merged PR и обновить только статусы/ссылки, без добавления новых
архитектурных планов.

**Плюсы:** возвращает backlog роль factual planning source.

**Минусы:** ручная работа, которую легко снова устарить без правила обновления.

**Оценка:** M
**Приоритет:** P2

### Решение 6: Minimal spoke CI contract

**Описание:** на основе `research/cicd/2026-06-js-cicd-template-analysis.md`
описать минимальные expectations для spoke CI: lint/test hooks, dependency
install policy, provider-neutral defaults, extension points.

**Плюсы:** превращает research в применимый template evolution path.

**Минусы:** преждевременная стандартизация может быть лишней до появления
нескольких production-spoke.

**Оценка:** M
**Приоритет:** P3

## Рекомендуемый план действий

**Фаза 1 (срочно):**

- Создать стандарт требований к `AI_SESSION_HANDOVER_PROMPT.md`.
- Добавить fixture-spoke проверку Smart Sync.

**Фаза 2 (важно):**

- Формализовать generated artifacts policy.
- Обновить `governance/backlog.md` по фактически закрытым issues.
- Создать `templates/task-for-konard.md` только если он будет ссылочным, без
  копирования всего issue template.

**Фаза 3 (желательно):**

- Подготовить minimal spoke CI contract на базе research/cicd.
- Связать contract с `templates/spoke/.github/workflows/ci.yml`.

## Открытые вопросы

- Должны ли committed research HTML в `research/mango/` считаться исходными
  артефактами или generated output для удаления?
- Являются ли screenshots в `docs/screenshots/` постоянной review evidence
  policy или временным исключением для PR #210?
- Нужен ли `templates/task-for-konard.md` как отдельный файл, если
  `templates/htom/.github/ISSUE_TEMPLATE/task.md` уже содержит AI-блок?
- Должен ли backlog обновляться в каждом PR, закрывающем backlog item, или
  отдельными periodic audit tasks?

---

**Для обсуждения:** Фаундер, Команда Q
