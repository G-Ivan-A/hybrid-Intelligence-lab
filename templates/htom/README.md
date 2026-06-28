---
status: canonical
version: 0.4
updated: {{date}}
temperature: 0.1
---

# {{project_name}}

> HTOM-команда, развёрнутая из Хаба `hybrid-Intelligence-lab` по «ДНК-шаблону»
> (`templates/htom/`). Минимальный, но «правильный» геном: правила гибридной
> работы человека и ИИ, контакт с Хабом и каркас для роста по запросу.
>
> **HTOM = Hybrid Team Operating Model.** Это команда, а не продукт: люди и
> ИИ-агенты работают итеративно по контрактам. Если вам нужен production-код
> отдельного продукта с `src/`, `tests/` и CI/CD — это spoke-репозиторий, и для
> него есть отдельный шаблон `templates/spoke/`.
>
> **Слоган (наследуется от Хаба):** «Человек задаёт смысл, AI ускоряет путь — вместе по правилам».

TODO: добавьте краткое описание проекта после инициализации.

## 🧬 Связь с Хабом

| Что | Где |
| --- | --- |
| Источник истины (governance, стандарты, research) | [{{hub_url}}]({{hub_url}}) |
| Фундаментальные знания | `research/` Хаба (в HTOM-команде `research/` **не создаётся**) |
| Операционный контракт команды | [AI_GOVERNANCE.md](AI_GOVERNANCE.md) |
| Быстрые правила для агента | [AI_QUICK_RULES.md](AI_QUICK_RULES.md) |
| «Доверенность» для запуска агента (Handover Prompt) | [AI_SESSION_HANDOVER_PROMPT.md](AI_SESSION_HANDOVER_PROMPT.md) |

## 🗂️ Структура (сейчас)

| Путь | Роль |
| --- | --- |
| `AI_GOVERNANCE.md` | Конституция команды: роли, правила, эскалация, DoD. |
| `AI_QUICK_RULES.md` | Одностраничная инструкция для AI-агента. |
| `AI_SESSION_HANDOVER_PROMPT.md` | Готовый *Handover Prompt* (`{{REPO_NAME}}`) для запуска агента; копия хабового шаблона по `standards/session-handover-standard.md`. |
| `CONTRIBUTING.md` | Workflow вклада: issue → PR → review. |
| `CHANGELOG.md` | Память команды: журнал значимых изменений. |
| `docs/adr/` | Architecture Decision Records — «почему», а не только «что». |
| `docs/audit/` | Ревизии, аудиты и проверки соответствия. |
| `.github/ISSUE_TEMPLATE/` | Шаблоны постановки задач: structured `task.md` и creative `task-creative.md` (язык Хаба). |
| `tools/` | Локальные проверки структуры репозитория. |

Каталоги создаются по запросу, при появлении операционной боли (Anti-Inflation
principle Хаба). Пустые «органеллы» HTOM-команда с собой не носит.

## Template Placeholder Policy

Source templates may contain placeholders only when the placeholder is part of
the approved HTOM-team template lifecycle. Generated repositories must not keep
unresolved source placeholders after initialization.

| Placeholder | Lifecycle | Rule |
| --- | --- | --- |
| `{{date}}` | Source template → generated repository | Allowed in source-template frontmatter. `init.sh` replaces it with the initialization date (`YYYY-MM-DD`). |
| `{{project_name}}` | Source template → generated repository | Allowed for repository-local names. `init.sh` replaces it during initialization. |
| `{{hub_url}}` | Source template → generated repository | Allowed for links back to the Hub. `init.sh` replaces it during initialization. |
| `{{REPO_NAME}}` | Runtime handover prompt | Allowed only where a copied prompt must name the current repository at execution time. `init.sh` intentionally leaves it untouched. |

No other `{{...}}` placeholders are approved for `templates/htom/` source
templates. New placeholders require an explicit policy update in this section
and matching validator behavior before they are introduced.

Generated-repository Definition of Done:

- `{{date}}`, `{{project_name}}`, and `{{hub_url}}` are replaced by `init.sh` or
  manually before the first commit.
- Generated repositories must not keep unresolved source placeholders.
- `{{REPO_NAME}}` may remain as the documented runtime placeholder for copy/paste
  handover. The active placeholder lives in `AI_SESSION_HANDOVER_PROMPT.md`; README
  guidance may reference it only to explain that exception.

`init.sh` also fills the README description line from `--description`; that field
is not a `{{...}}` placeholder and is outside the placeholder whitelist.

## 🛠️ Как адаптировать `{{...}}`-плейсхолдеры

Файлы шаблона содержат `{{...}}`-плейсхолдеры — «гены», которые нужно подставить
под конкретную HTOM-команду **один раз**, сразу после клонирования:

| Плейсхолдер | Что подставить | Кто заполняет |
| --- | --- | --- |
| `{{project_name}}` | Имя проекта/команды | `init.sh` / вручную |
| `{{hub_url}}` | Ссылка на Хаб (источник истины) | `init.sh` / вручную |
| `{{date}}` | Текущая дата (`YYYY-MM-DD`) во frontmatter | `init.sh` (автоген) |
| `{{REPO_NAME}}` | Имя репозитория в *Handover Prompt* | **вручную** (см. ниже) |

**Самый простой путь — скрипт `init.sh`** (он заменяет строчные `{{...}}` во всех
файлах, проставляет дату и затем удаляет себя как одноразовый):

```bash
# интерактивно (спросит значения)
./init.sh

# неинтерактивно (для CI): все значения через флаги
./init.sh -n "My HTOM Team" -d "Краткое описание" -u "https://github.com/ORG/HUB" --yes
```

> **Почему `{{REPO_NAME}}` — отдельно.** `init.sh` заменяет только строчные
> плейсхолдеры (`{{[a-z_]*}}`) и **не трогает** `{{REPO_NAME}}` в
> [AI_SESSION_HANDOVER_PROMPT.md](AI_SESSION_HANDOVER_PROMPT.md): по умолчанию там остаётся
> `hybrid-Intelligence-lab`. Подставьте имя своего репозитория вручную или оставьте
> дефолт, если работаете в Хабе.

Если правите вручную — найдите остатки плейсхолдеров по дереву перед коммитом:

```bash
grep -RIn '{{[a-z_]*}}' . --exclude-dir=.git   # должно остаться пусто после init.sh
```

## ✅ Как валидировать структуру

После адаптации (и далее — перед каждым PR) прогоните локальный структурный
валидатор. Он проверяет, что геном HTOM-команды на месте, плейсхолдеры заполнены,
а дерево не «раздулось» сверх контракта:

```bash
./tools/validate-repository-structure.sh
```

Скрипт завершается с ненулевым кодом и печатает `FAIL: …` при нарушениях —
почините их **до** отправки PR (Definition of Done из [CONTRIBUTING.md](CONTRIBUTING.md)).

## 🧭 Две точки входа (Кейс 1 ↔ Кейс 2)

Этот README — точка входа **Кейса 2** (*Bootstrap-клонирование*): как **развернуть**
новую HTOM-команду из «ДНК-шаблона» Хаба. Есть ортогональный **Кейс 1**
(*Runtime-онбординг*): как ИИ-агенту **войти в уже существующий** репозиторий до
первого изменения файлов. Попав в любую точку входа, держите в поле зрения вторую:

| Куда | Зачем |
| --- | --- |
| Хаб [`governance/agent-onboarding-protocol.md`]({{hub_url}}/blob/main/governance/agent-onboarding-protocol.md) | **Кейс 1**: протокол *Runtime-онбординга* агента (Handover Prompt, Readback, стоп до апрува). |
| Хаб [`standards/session-handover-standard.md`]({{hub_url}}/blob/main/standards/session-handover-standard.md) | Draft-стандарт структуры `AI_SESSION_HANDOVER_PROMPT.md`: контекст проекта, чат-диалог, канал репо и проверка шаблонов. |
| Хаб [`rfc-two-cases-of-project-initialization.md`]({{hub_url}}/blob/main/governance/rfc/rfc-two-cases-of-project-initialization.md) | Манифест двух кейсов: чем Кейс 2 (этот файл) отличается от Кейса 1. |
| Этот README, раздел [Design Decisions & Rationale](#design-decisions--rationale) | Дизайн «ДНК-шаблона» HTOM-команды: почему геном именно такой. |

## Design Decisions & Rationale

Раздел сохраняет rationale из утверждённого дизайн-предложения, которое
предшествовало этому шаблону. После слияния именно этот README является
canonical-точкой входа для bootstrap-клонирования HTOM-команды.

### ДНК клетки, а не чемодан переезжающего

Шаблон HTOM-команды устроен как компактный геном: он задаёт, кем команда может
стать и по каким правилам растёт, но не тащит с собой все возможные каталоги «на
всякий случай». Поэтому `research/`, `prompts/`, `experiments/`, `kb/`,
`standards/` и другие тяжёлые разделы не создаются на старте. Они появляются
только при операционной боли и с явным rationale.

### Почему путь `templates/htom/`

| Решение | Почему |
| --- | --- |
| `templates/`, а не `blueprints/` | Имя прямо подсказывает действие: копировать и адаптировать. `blueprints/` звучит как чертёж, но не как готовый минимальный набор файлов. |
| `templates/`, а не `genesis/` | `genesis/` провоцирует избыточность и желание «сотворить мир» вместо минимального bootstrap. |
| Namespace `htom/` | Отделяет геном HTOM-команды от шаблона production-спока (`templates/spoke/`) без раздувания корня. |
| Kebab-case имена | Совместимо с [file-naming.md]({{hub_url}}/blob/main/standards/file-naming.md), даёт стабильные ссылки и хорошо читается AI-агентами. |

### Почему минимальный набор остаётся малым

Исходный дизайн выбрал 9 стартовых ролей. Позже *Handover Prompt* был вынесен в
отдельный файл для самодостаточности команды, но принцип не изменился: каждый
артефакт должен нести отдельную стартовую роль, а не создавать структуру «на
вырост».

| Файл | Дизайн-роль |
| --- | --- |
| `AI_GOVERNANCE.md` | Конституция команды: роли, решения человека, границы AI. |
| `AI_QUICK_RULES.md` | Fail-closed инструкция для агента: куда смотреть и чего не делать. |
| `AI_SESSION_HANDOVER_PROMPT.md` | Самодостаточный запуск Runtime-онбординга в новом репозитории. |
| `README.md` | Визитка команды, карта текущей структуры и связь с Хабом. |
| `CONTRIBUTING.md` | Минимальный workflow issue → PR → review. |
| `CHANGELOG.md` | Память изменений с первого значимого шага. |
| `docs/adr/.gitkeep` | Каркас для решений: почему выбран путь, а не только что изменено. |
| `docs/audit/.gitkeep` | Каркас для ревизий и проверок соответствия. |
| `.github/ISSUE_TEMPLATE/task.md`, `.github/ISSUE_TEMPLATE/task-creative.md` и `tools/validate-repository-structure.sh` | Единый язык structured/creative задач и локальная защита от структурного разрастания. |

### Антипаттерны bootstrap

1. **Копировать всё, вдруг пригодится.** Пустые папки и TODO-заглушки создают шум,
   который новый агент принимает за реальную структуру.
2. **Вшивать research в команду.** Фундаментальные знания должны оставаться в Хабе,
   иначе появляются расходящиеся копии source of truth.
3. **Строить структуру на вырост.** Глубокая вложенность до появления работы
   становится налогом для каждой новой HTOM-команды.

Если человек осознанно просит нарушить правило (например, создать `research/` на
старте), агент должен назвать правило, предложить легитимную альтернативу
ссылкой на Хаб или ADR, и только после явного решения человека фиксировать
отклонение как documented decision.
