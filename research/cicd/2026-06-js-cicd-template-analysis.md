---
status: draft
version: 0.1
updated: 2026-06-09
temperature: 0.1
ai-generated: false
type: external-analysis
context: [cicd, javascript, typescript, ai-driven-development, github-actions]
method: manual-review
---

# Исследование: JS CI/CD Template — Анализ шаблона link-foundation

## 1. Введение

**Причина.** Команда нуждается в проверенных CI/CD паттернах для AI-native JS/TS проектов. Репозиторий `open-ai.ru` (Next.js) требует наладки CI/CD. Шаблон Константина — наиболее близкий к целевому стеку источник.

**Цель.** Выделить применимые паттерны CI/CD из `js-ai-driven-development-pipeline-template` для внедрения в `open-ai.ru`, оценить применимость к `mango_ba_prompts` (Python) и `hybrid-Intelligence-lab` (хаб).

**Связанные артефакты.**
- Issue: [G-Ivan-A/hybrid-Intelligence-lab#202](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/202)
- Источник: [link-foundation/js-ai-driven-development-pipeline-template](https://github.com/link-foundation/js-ai-driven-development-pipeline-template)
- Стандарт: [standards/research-profile.md](../../standards/research-profile.md)
- Backlog: [governance/backlog.md](../../governance/backlog.md)

**Метод.** Manual review: полное дерево файлов, все workflow YAML, конфигурации инструментов, документация `BEST-PRACTICES.md`.

---

## 2. Результаты исследования

### 2.1. Главный вывод

Шаблон реализует **три ключевых AI-native CI/CD паттерна**:

1. **Fast-fail ordering** — быстрые проверки (~7–30 с) идут перед медленными тестами, давая AI-агенту быструю обратную связь.
2. **File size ceiling (1 500 строк)** — ограничение на размер файлов обеспечивает вместимость в контекстное окно модели и ускоряет ревью.
3. **Defence-in-depth автоматизация** — три слоя: pre-commit hooks → CI fast checks → CI slow matrix тесты.

Шаблон готов к применению в `open-ai.ru` с минимальными адаптациями. Большинство паттернов универсальны и применимы к Python и другим стекам.

### 2.2. Рекомендации

| # | Рекомендация | Куда фиксируется |
|---|---|---|
| 1 | Внедрить fast-fail job ordering в CI `open-ai.ru` | Issue в `open-ai.ru` |
| 2 | Установить лимит 1 500 строк на JS/MD файлы в `open-ai.ru` | `open-ai.ru` `.github/workflows/` |
| 3 | Настроить Changesets для версионирования `open-ai.ru` | Issue в `open-ai.ru` |
| 4 | Использовать OIDC trusted publishing для npm вместо токенов | `open-ai.ru` CI config |
| 5 | Добавить Secretlint в CI `open-ai.ru` и `mango_ba_prompts` | Issues в обоих репозиториях |
| 6 | Внедрить Wayback Machine fallback в проверку ссылок `hybrid-Intelligence-lab` | Issue в хабе |
| 7 | Применить паттерн `!cancelled()` вместо `always()` в CI workflows | Все репозитории |
| 8 | Вынести паттерны 1–3 в стандарт после проверки в `open-ai.ru` | `standards/cicd-profile.md` (новый) |

### 2.3. Открытые вопросы

- Нужна ли мультиплатформенная матрица тестов (Ubuntu/macOS/Windows) для `open-ai.ru`? Или достаточно Ubuntu?
- Применять ли Changesets в `mango_ba_prompts` (Python) или использовать семантически эквивалентный инструмент (`python-semantic-release`)?
- Целесообразен ли анализ Python-шаблона Константина после применения JS-паттернов?

### 2.4. Учёт мнения команды

Данное исследование является первым в направлении `cicd`; мнений предыдущих ревьюеров нет.

---

## 3. Детализация

### 3.1. Структура репозитория

```text
root/
├── .changeset/config.json           # Changesets: версионирование и changelog
├── .github/
│   └── workflows/
│       ├── release.yml              # Главный CI/CD пайплайн
│       ├── example-app.yml          # Сборка и деплой приложения
│       └── links.yml                # Валидация ссылок
├── .husky/pre-commit                # Git hook: lint-staged перед коммитом
├── src/
│   ├── index.js                     # Основной модуль (ES modules)
│   └── index.d.ts                   # TypeScript определения
├── bin/example-package-name.js      # CLI точка входа
├── tests/index.test.js              # Тесты (test-anywhere)
├── examples/                        # Примеры использования и universal app
├── scripts/                         # 20+ скриптов автоматизации
├── docs/
│   ├── BEST-PRACTICES.md            # Руководство по AI-driven dev
│   └── case-studies/                # 13+ кейсов внедрения
├── .prettierrc                      # Prettier конфигурация
├── .lycheeignore                    # Исключения для lychee
├── .secretlintrc.json               # Secretlint конфигурация
├── package.json                     # Метаданные проекта
└── CHANGELOG.md                     # История версий
```

**Ключевые наблюдения:**
- `scripts/` содержит 20+ MJS-скриптов; каждый решает одну задачу (SRP).
- `docs/case-studies/` — 13+ реализованных примеров; хорошая база для онбординга.
- `experiments/` присутствует в дереве — совпадает с нашей конвенцией в хабе.

### 3.2. GitHub Workflows

#### 3.2.1. `release.yml` — Главный CI/CD пайплайн

**Триггеры:** `push` → main, `pull_request` (opened/synchronized/reopened), `workflow_dispatch`

**Архитектура jobs (последовательность fast-fail):**

| Этап | Job | Время | Назначение |
|---|---|---|---|
| 1. Быстрые проверки | `check-syntax` | ~7–15 с | ESM синтаксис JS/MJS файлов |
| 1. Быстрые проверки | `check-line-limits` | ~10–30 с | Лимит 1 500 строк на JS/MD |
| 1. Быстрые проверки | `check-version` | ~10–20 с | Валидация версии в package.json |
| 2. Качество | `lint` | ~30–60 с | ESLint |
| 2. Качество | `format` | ~30–60 с | Prettier |
| 2. Качество | `secretlint` | ~20–40 с | Сканирование секретов |
| 2. Качество | `check-changesets` | ~20–30 с | Валидация changesets |
| 3. Тесты | `test-matrix` | ~3–10 мин | 9 комбинаций: Node/Bun/Deno × Ubuntu/macOS/Windows |
| 4. Релиз | `release` | ~5 мин | Публикация на npm (только main) |

**Паттерн concurrency:**
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}
```
Main-ветка: релизы не отменяются. PR-ветки: устаревшие прогоны отменяются автоматически.

**Паттерн merge simulation:**
```yaml
- name: Simulate fresh merge
  run: |
    git fetch origin ${{ github.base_ref }}
    git merge origin/${{ github.base_ref }} --no-commit --no-ff
```
Проверяет фактическое состояние после merge, а не изолированную ветку.

**Explicit timeouts:**
```yaml
timeout-minutes: 10  # на каждый job
```

**Proper cancellation:**
```yaml
if: ${{ !cancelled() }}  # вместо always()
```

#### 3.2.2. `example-app.yml` — Сборка приложения

**Триггеры:** push/PR (только при изменении `examples/` или `src/`), `workflow_dispatch`

**Jobs:**
- `web-build`: Node.js 24.x, артефакты для GitHub Pages
- `pages-deploy`: деплой на GitHub Pages
- `desktop-build`: Electron (Ubuntu/macOS/Windows, Node.js 20.x)
- `android-build`: опционально, Android SDK, Java 21
- `ios-build`: опционально, macOS
- `preview-regen`: Playwright + browser-commander → автообновление скриншотов в README

**Паттерн conditional jobs:**
```yaml
if: ${{ vars.BUILD_ANDROID == 'true' }}
```
Дорогостоящие jobs включаются через переменные репозитория.

#### 3.2.3. `links.yml` — Валидация ссылок

**Триггеры:** push/PR (изменения `.md`/`.html`/`.yml`), `workflow_dispatch`

**Инструмент:** lychee-action
**Scope:** все `.md` и `.html` файлы
**Параметры:** retry: 3, timeout: 30 с, cache: 1 день, общий timeout: 10 мин

**Паттерн Wayback Machine fallback:**
```yaml
- name: Check Wayback Machine for broken links
  if: steps.lychee.outputs.exit_code != 0
  run: node scripts/check-web-archive.mjs
```
Broken links не ломают CI, если существует архивная копия.

### 3.3. CI/CD скрипты

Все скрипты в `scripts/` написаны на ES modules (`.mjs`), без внешних зависимостей (кроме `node-fetch` при необходимости).

| Скрипт | Назначение |
|---|---|
| `check-version.mjs` | Валидация format версии в package.json |
| `check-mjs-syntax.sh` | Bash-обёртка: `node --check` для каждого MJS файла |
| `check-file-line-limits.sh` | `wc -l` для JS/MD файлов; fail если > 1 500 |
| `changeset-version.mjs` | Wrapper над `@changesets/cli` для bump версии |
| `create-github-release.mjs` | Парсинг CHANGELOG.md + `gh api` для создания release |
| `publish-to-npm.mjs` | OIDC publishing с retry (3 попытки) |
| `check-web-archive.mjs` | Wayback Machine API lookup для broken links |
| `format-release-notes.mjs` | Форматирование release notes |

**AI-паттерн:** Каждый скрипт — одна задача, максимум ~100–200 строк. Легко вместить в контекстное окно модели.

### 3.4. Конфигурации инструментов

#### Prettier (`.prettierrc`)
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

#### ESLint (`.eslintrc.json`)
ESLint v9 flat config, рекомендуемый ruleset.

#### Секреты (`.secretlintrc.json`)
```json
{
  "rules": [{ "id": "@secretlint/secretlint-rule-preset-recommend" }]
}
```
Стандартный preset покрывает AWS keys, GitHub tokens, generic API keys.

#### Changesets (`.changeset/config.json`)
```json
{
  "access": "public",
  "baseBranch": "main",
  "commit": false,
  "updateInternalDependencies": "patch"
}
```

#### Husky + lint-staged
Pre-commit: ESLint + Prettier только на staged файлах (`.js`, `.md`).

#### jscpd
Детекция дублирования кода; порог не указан явно, но интегрирован в CI.

### 3.5. Управление секретами

**OIDC Trusted Publishing** — ключевой паттерн:
- npm токены не хранятся в GitHub Secrets
- Используется OpenID Connect между GitHub Actions и npm registry
- Ротация не требуется: токен генерируется per-job

**GitHub Secrets** используются только для опциональных интеграций:
- `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` — Docker Hub
- Secrets не требуются для базового npm publishing

### 3.6. Branch protection (наблюдения)

В самом шаблоне branch protection rules не описаны явно, но пайплайн предполагает:
- `main` — защищённая ветка
- PR-процесс обязателен (есть merge simulation в CI)
- Релиз только из `main`

### 3.7. PR Templates

В дереве репозитория PR template явно не обнаружен. Checklist для PR описан косвенно через `BEST-PRACTICES.md` и CI validation.

### 3.8. AI-специфические практики

| Практика | Реализация | Применимость |
|---|---|---|
| Лимит 1 500 строк/файл | `check-file-line-limits.sh` | Универсальная |
| Fast-fail feedback loop | Порядок jobs в `release.yml` | Универсальная |
| Merge simulation | `git fetch + merge` в CI | Универсальная |
| Скрипты с одной задачей | `scripts/*.mjs` по 100–200 строк | Универсальная |
| `BEST-PRACTICES.md` | Явный AI-контекст для агентов | Универсальная |
| Explicit timeouts | `timeout-minutes` на каждый job | Универсальная |
| Cross-runtime matrix | Node/Bun/Deno × 3 OS | JS-специфика |
| Changeset versioning | `@changesets/cli` | JS-специфика (аналог: `semantic-release`) |
| OIDC npm publishing | `NODE_AUTH_TOKEN` через OIDC | JS-специфика |

### 3.9. Документация

| Файл | Содержание |
|---|---|
| `README.md` | Quick start, конфигурация, ссылки на BEST-PRACTICES |
| `docs/BEST-PRACTICES.md` | 10 AI-driven dev практик с обоснованием |
| `CHANGELOG.md` | Полная история версий с описанием каждого изменения |
| `docs/case-studies/` | 13+ примеров реализации |

**Оценка:** Документация выше среднего; особенно ценен `BEST-PRACTICES.md` — явная AI-контекстная документация.

### 3.10. Best Practices

#### 3.10.1. Что хорошо (берём на вооружение)

- **Fast-fail job ordering**: Быстрые проверки (синтаксис, формат) перед медленными тестами. Снижает время обратной связи с 10 мин до 30 с при ошибке форматирования.
- **Файловый лимит 1 500 строк**: Дисциплинирует декомпозицию кода и гарантирует вместимость файлов в контекстное окно LLM.
- **OIDC Trusted Publishing**: Устраняет проблему ротации токенов; нет secrets в GitHub — нет утечки.
- **Secretlint в CI**: Сканирование секретов на CI-уровне как дополнение к `.gitignore`.
- **Wayback Machine fallback**: Broken links в документации не ломают CI, если есть архивная копия — разумный компромисс.
- **Concurrency controls**: Главная ветка не теряет в-процессе релизов; PR-ветки не тратят ресурсы на устаревшие прогоны.
- **`!cancelled()` вместо `always()`**: Правильная семантика отмены jobs; предотвращает ложные "успехи" при отмене.
- **Merge simulation**: Проверяет фактическое состояние кода после merge, а не изолированную ветку.
- **Скрипты одной задачи**: Каждый `scripts/*.mjs` решает одно дело; хорошо читаются и тестируются отдельно.

#### 3.10.2. Что можно улучшить

- **Нет явного PR template**: Checklist требований к PR не формализован; для AI-агентов это было бы полезно.
- **Branch protection rules не документированы**: Ожидаемые настройки защиты веток нигде не зафиксированы.
- **Нет примера CODEOWNERS**: Автоназначение ревьюеров не настроено.
- **Нет SECURITY.md**: Политика disclosure не описана.
- **Cross-platform matrix может быть дорогой**: 9 комбинаций для небольшого проекта — возможно избыточно.

#### 3.10.3. Что специфично для JS (не применимо напрямую)

- `@changesets/cli` — аналог для Python: `python-semantic-release` или `commitizen`
- `test-anywhere` — специфичен для Node/Bun/Deno; аналог для Python: `pytest` с tox
- OIDC npm publishing — аналог для PyPI: `trusted publishing` (OIDC также поддерживается PyPI)
- Husky + lint-staged — аналог для Python: `pre-commit` framework
- `node --check` для синтаксиса — аналог: `python -m py_compile`

#### 3.10.4. Что универсально (применимо к другим стекам)

- Fast-fail job ordering
- Файловый лимит (1 500 строк или аналогичный)
- Merge simulation в CI
- Secretlint/аналог на уровне CI
- Wayback Machine fallback для link checking
- Concurrency controls в GitHub Actions
- `!cancelled()` семантика
- Explicit `timeout-minutes` на jobs
- Скрипты одной задачи
- Явная AI-контекстная документация (`BEST-PRACTICES.md` или аналог)

### 3.11. Применение в наших проектах

#### 3.11.1. `open-ai.ru` (Next.js)

| Паттерн | Применимость | Приоритет | Примечание |
|---|---|---|---|
| Fast-fail ordering | Высокая | P1 | Прямой перенос |
| Лимит 1 500 строк | Высокая | P1 | Адаптировать под JS/MD/TSX |
| Changesets | Высокая | P1 | Прямой перенос |
| Prettier + ESLint | Высокая | P1 | Уже может быть; проверить конфиг |
| Husky + lint-staged | Высокая | P2 | Прямой перенос |
| Secretlint | Высокая | P2 | Добавить в CI |
| OIDC npm publishing | Средняя | P2 | Если планируется npm публикация |
| Cross-platform matrix | Низкая | P3 | Для Next.js веб-приложения не нужно |
| Wayback fallback | Низкая | P3 | Если есть внешние ссылки в README |

#### 3.11.2. `mango_ba_prompts` (Python)

| Паттерн | Применимость | Примечание |
|---|---|---|
| Fast-fail ordering | Высокая | Универсальный; перенести на Python CI |
| Лимит строк | Высокая | Применить к `.py` и `.md` файлам |
| Secretlint | Средняя | Использовать `detect-secrets` или аналог |
| Merge simulation | Высокая | Универсальный GitHub Actions паттерн |
| Changesets | Не применимо | Использовать `python-semantic-release` |
| OIDC | Средняя | PyPI поддерживает OIDC trusted publishing |

#### 3.11.3. `hybrid-Intelligence-lab` (хаб)

| Паттерн | Применимость | Примечание |
|---|---|---|
| Wayback fallback в link checking | Высокая | Много внешних ссылок в документации |
| Secretlint | Средняя | Добавить базовую защиту |
| Лимит строк для MD | Высокая | Ограничить размер документов |
| Fast-fail для документации | Средняя | Синтаксис Markdown, валидация frontmatter |

---

## 4. Источники

| # | Источник | Описание |
|---|---|---|
| 1 | [link-foundation/js-ai-driven-development-pipeline-template](https://github.com/link-foundation/js-ai-driven-development-pipeline-template) | Анализируемый репозиторий (v0.11.4, январь 2026) |
| 2 | [docs/BEST-PRACTICES.md](https://github.com/link-foundation/js-ai-driven-development-pipeline-template/blob/main/docs/BEST-PRACTICES.md) | AI-driven dev руководство, 10 практик |
| 3 | [.github/workflows/release.yml](https://github.com/link-foundation/js-ai-driven-development-pipeline-template/blob/main/.github/workflows/release.yml) | Главный CI/CD workflow |
| 4 | [standards/research-profile.md](../../standards/research-profile.md) | Стандарт для структуры этого документа |
| 5 | [npm — OIDC Trusted Publishing](https://docs.npmjs.com/generating-provenance-statements) | Документация OIDC publishing |
| 6 | [lychee-action](https://github.com/lycheeverse/lychee-action) | GitHub Action для валидации ссылок |
| 7 | [@changesets/cli](https://github.com/changesets/changesets) | Инструмент управления версиями |

---

**Версия:** 0.1
**Дата:** 2026-06-09
**Статус:** Draft
**Автор анализа:** @konard
