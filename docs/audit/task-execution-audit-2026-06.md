---
status: draft
version: 0.1
updated: 2026-06-11
temperature: 0.1
---

# Аудит выполненных задач (1-4)

**Дата:** 2026-06-11
**Аудитор:** @konard
**Статус:** Draft

## Область аудита

Аудит покрывает четыре выполненные задачи, перечисленные в issue
[#213](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/213):

1. Vision/Concept Хаба + гайды + MkDocs.
2. Обновление шаблона `task.md`.
3. RFC по HTOM vs spoke.
4. Анализ JS CI/CD шаблона Константина.

Проверка основана на закрытых issues, merged PR, текущем состоянии `main` и
локальных проверках репозитория.

## Задача 1: Vision/Concept Хаба + гайды + MkDocs

**Issues:** [#203](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/203),
[#209](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/209)
**PR:** [#204](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/204),
[#210](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/210)
**Статус:** ✅ Выполнено с замечаниями

### Проверка Definition of Done

- [x] `docs/vision.md` создан и опубликован в MkDocs-навигации.
- [x] `docs/product-concept.md` создан и опубликован в MkDocs-навигации.
- [x] `docs/ecosystem-map.md` создан follow-up PR #210.
- [x] RFC `governance/rfc/hub-vision-concept-proposal-2026-06.md` присутствует.
- [x] Каталог `guides/` создан и подключён в `mkdocs.yml`.
- [x] MkDocs-конфигурация есть, сайт собирается из `website/`.
- [x] GitHub Pages workflow есть: `.github/workflows/deploy-docs.yml`.
- [x] CSS для таблиц и адаптивности есть: `website/stylesheets/extra.css`.
- [x] Локальная сборка заявлена в PR #210.

### Findings

- **F1.1: задача #203 была закрыта неполным пакетом и достраивалась issue #209.**
  Это не блокирует результат сейчас, но показывает, что исходная DoD была
  выполнена итеративно, а не одним завершённым пакетом.
- **F1.2: в репозитории остаются сгенерированные HTML-файлы.** Найдены
  `research/mango/requirements-flow.html`,
  `research/mango/classification.html`,
  `research/mango/classification-tz.html`. Это противоречит ограничению issue
  #213 "не коммитить сгенерированные файлы", если эти HTML считаются build
  output.
- **F1.3: `.gitignore` исключает `/site/`, но не исключает `*.html` и `*.png`.**
  При этом committed PNG-скриншоты лежат в `docs/screenshots/`. Для скриншотов
  PR #210 это осознанный review artifact, но политика в issue #213 сформулирована
  шире и требует явного решения.
- **F1.4: MkDocs публикует только часть репозитория.** Это соответствует
  комментариям в `mkdocs.yml`, но может быть неожиданным для читателя: governance
  и standards намеренно не входят в сайт.

### Рекомендации

- Зафиксировать политику generated artifacts: какие HTML/PNG допустимы как
  исходные артефакты или review evidence, а какие должны попадать только в
  `/site/` и игнорироваться.
- Если HTML в `research/mango/` больше не нужен как исходный материал, вынести
  удаление/миграцию в отдельную cleanup-задачу.
- Оставить scope MkDocs явным: published docs = `docs/`, `guides/`, `research/`;
  governance и standards остаются GitHub-first.

## Задача 2: Обновление шаблона `task.md`

**Issue:** [#211](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/211)
**PR:** [#212](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/212)
**Статус:** ✅ Выполнено

### Проверка Definition of Done

- [x] `templates/htom/.github/ISSUE_TEMPLATE/task.md` обновлён до полной
  структуры задачи.
- [x] `templates/sync-metadata.json` обновлён для Smart Sync.
- [x] `templates/manifest.json` обновлён через генератор, а не вручную.
- [x] Структурная и frontmatter-валидация заявлены в PR #212.
- [x] Все изменённые пути соответствуют kebab-case/действующим исключениям.

### Findings

- **F2.1: решение корректно адаптировало спецификацию под Smart Sync.**
  PR #212 не редактировал `manifest.json` вручную, а обновил источник
  `templates/sync-metadata.json` и перегенерировал manifest. Это соответствует
  архитектуре, введённой issue #207.
- **F2.2: issue template живёт в `templates/htom/`, а не в старом
  `templates/spoke/`.** Это ожидаемое следствие разделения HTOM/spoke, но
  downstream-инструкции должны ссылаться на новый путь.

### Рекомендации

- В future issues явно указывать, что `templates/manifest.json` является
  generated registry и меняется через `tools/generate-manifest.py`.
- Для задач по шаблонам добавлять проверку `python3 tools/generate-manifest.py
  --check` в DoD.

## Задача 3: RFC по HTOM vs spoke

**Issue:** [#201](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/201)
**PR:** [#206](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/206)
**Статус:** ✅ Выполнено с остаточным техдолгом

### Проверка Definition of Done

- [x] Создан RFC `governance/rfc/htom-vs-spoke-clarification-2026-06.md`.
- [x] `templates/spoke/` переосмыслен как шаблон production-spoke.
- [x] HTOM-геном перенесён в `templates/htom/`.
- [x] Основные ссылки в governance, standards, templates и README обновлены.
- [x] Классификация проектов отражена в `projects/README.md`.

### Findings

- **F3.1: концептуальное разделение проведено сквозным рефакторингом.**
  Текущая структура различает HTOM-команды (`templates/htom/`) и настоящие
  spoke-репозитории (`templates/spoke/`).
- **F3.2: техдолг "типы передачи контекста" частично снят, но не закрыт
  полностью.** Файлы `governance/agent-onboarding-protocol.md` и
  `templates/htom/AI_SESSION_HANDOVER_PROMPT.md` уже разделены, но нет отдельного
  стандарта требований к handover prompt.
- **F3.3: downstream-навигация зависит от Smart Sync.** После переименований
  spoke/HTOM любые старые ссылки во внешних репозиториях требуют синхронизации
  или ручной миграции.

### Рекомендации

- Завести отдельную задачу на стандарт `AI_SESSION_HANDOVER_PROMPT.md`: структура,
  обязательные секции, readback, границы копируемого текста.
- Добавить Smart Sync verification для шаблонов `templates/htom/` и
  `templates/spoke/` на fixture-репозитории.

## Задача 4: Анализ JS CI/CD шаблона Константина

**Issue:** [#202](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/202)
**PR:** [#205](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/205)
**Статус:** ✅ Выполнено

### Проверка Definition of Done

- [x] Создан research-документ
  `research/cicd/2026-06-09-js-cicd-template-analysis.md`.
- [x] Создан `research/cicd/README.md`.
- [x] Каталог `research/cicd/` добавлен в структурную модель репозитория.
- [x] В PR #210 был устранён pre-existing сбой allowlist/ссылки для
  `research/cicd`.

### Findings

- **F4.1: результат оформлен как research, а не как production workflow.**
  Это соответствует исследовательскому режиму задачи.
- **F4.2: интеграция `research/cicd/` в валидатор была доделана последующим PR.**
  В PR #210 отдельно отмечено исправление pre-existing structure-validator
  failures, связанных с `research/cicd`.
- **F4.3: нет отдельного стандарта применения CI/CD шаблона к spoke.**
  Research фиксирует паттерны, но не превращает их в обязательный контракт.

### Рекомендации

- Не внедрять CI/CD шаблон как стандарт автоматически. Сначала описать
  минимальный spoke CI contract и критерии применимости.
- Добавить будущую задачу на сопоставление выводов research/cicd с
  `templates/spoke/.github/workflows/ci.yml`.

## Проверка техдолга

### Подтверждённый техдолг

| # | Техдолг | Статус | Приоритет |
| --- | --- | --- | --- |
| 1 | Разделение онбординга и передачи контекста | Частично снят issue #207 | P1 |
| 2 | Шаблон задачи для Конарда `templates/task-for-konard.md` | Не найден | P2 |
| 3 | Стандарт требований к `AI_SESSION_HANDOVER_PROMPT.md` | Не найден | P1 |
| 4 | Проверка шаблонов в spoke-репо через Smart Sync | Частично покрыто `experiments/test-smart-sync.sh`, нет fixture-spoke CI | P1 |
| 5 | Политика generated HTML/PNG artifacts | Не формализована | P2 |
| 6 | Актуализация `governance/backlog.md` после закрытых CE-задач | Требует отдельной проверки: в видимом фрагменте есть TODO для уже закрытых CE issues | P2 |

## Проверка MkDocs и generated artifacts

- `mkdocs.yml` присутствует и использует `website/` как `docs_dir`.
- `.github/workflows/deploy-docs.yml` присутствует и публикует `/site/` в GitHub
  Pages.
- `.gitignore` содержит `/site/`.
- `.gitignore` не содержит глобальных исключений `*.html` и `*.png`.
- В репозитории есть committed HTML: `research/mango/*.html`.
- В репозитории есть committed PNG: `docs/screenshots/*.png`.

Вывод: MkDocs-инфраструктура рабочая, но политика generated artifacts требует
уточнения. Нельзя одновременно требовать committed screenshots для PR-review и
абсолютно запрещать PNG без исключений.

## Итоги аудита

**Общая оценка:** хорошо.

Задачи 1-4 в целом выполнены и замержены. Основные проблемы не в отсутствии
артефактов, а в операционной консистентности: часть DoD закрывалась follow-up
PR, generated artifacts policy не формализована, а Smart Sync/HTOM-spoke
изменения требуют downstream-проверок.

### Критические проблемы

- Нет P0-блокеров по текущему состоянию аудируемых задач.
- Есть P1-техдолг по handover prompt standard и Smart Sync verification.

### Рекомендации

- Сначала закрыть P1-техдолг: стандарт handover prompt и Smart Sync
  verification.
- Затем формализовать generated artifacts policy для HTML/PNG.
- Не менять существующие документы в рамках issue #213 сверх двух новых файлов:
  это соответствует критическому ограничению issue, несмотря на отдельный пункт
  про `CHANGELOG.md`.
