---
status: canonical
version: 0.1
updated: {{date}}
temperature: 0.1
---

# {{project_name}}

> Spoke-репозиторий, связанный с Хабом `hybrid-Intelligence-lab`. **Spoke — это
> отдельный продукт с production-кодом**, а не HTOM-команда: здесь живут `src/`,
> `tests/`, документация и CI/CD. Геном гибридной работы (HTOM-команды) лежит в
> отдельном шаблоне `templates/htom/`.
>
> Первый настоящий spoke Хаба — портал `open-ai.ru`.

TODO: добавьте краткое описание продукта после инициализации.

## 🧭 Spoke ≠ HTOM-команда

| | HTOM-команда (`templates/htom/`) | Spoke-репозиторий (`templates/spoke/`) |
| --- | --- | --- |
| Что это | Гибридная команда: люди + ИИ-агенты | Отдельный продукт с production-кодом |
| Артефакт | Контракты работы с ИИ, итеративные задачи | `src/`, `tests/`, docs, CI/CD |
| Цикл | Итеративный, минимальная структура | Полный SDLC отдельного продукта |
| Пример | `mango_ba_prompts`, `repo-development` | `open-ai.ru` |

Полное обоснование различия — в RFC Хаба
[`governance/rfc/htom-vs-spoke-clarification-2026-06.md`]({{hub_url}}/blob/main/governance/rfc/htom-vs-spoke-clarification-2026-06.md).

## 🔗 Связь с Хабом

| Что | Где |
| --- | --- |
| Источник истины (governance, стандарты, research) | [{{hub_url}}]({{hub_url}}) |
| Концепция продукта (L2) и решения (L3) | стандарты `webportal-*-concept-standard.md` Хаба |
| Правила участия в этом spoke | [CONTRIBUTING.md](CONTRIBUTING.md) |

Spoke не дублирует фундаментальные знания Хаба, а ссылается на них. Продуктовые
и архитектурные решения фиксируются локально (в `docs/`), governance-правила
наследуются от Хаба.

## 🗂️ Целевая структура

| Путь | Роль |
| --- | --- |
| `src/` | Production-код продукта. |
| `tests/` | Автотесты (unit, integration, e2e). |
| `docs/` | Продуктовая и техническая документация, ADR; локальные правила — в `docs/README.md`. |
| `tools/` | Локальные проверки, включая наследуемый валидатор именования файлов. |
| `.github/workflows/` | CI/CD: линт, тесты, сборка, деплой. |
| `README.md` | Визитка продукта и точка входа. |
| `CONTRIBUTING.md` | Workflow вклада и требования к PR. |

> В отличие от HTOM-команды, spoke создаёт `src/` и `tests/` сразу — это
> production-репозиторий, и код в нём ожидаем с первого дня. Anti-Inflation
> по-прежнему действует для вспомогательной обвязки: не плодите пустые каталоги
> «на вырост».

## 🛠️ Плейсхолдеры

Шаблон содержит `{{project_name}}`, `{{hub_url}}` и `{{date}}` (frontmatter).
Подставьте их под конкретный spoke сразу после клонирования и убедитесь, что
незаменённых плейсхолдеров не осталось:

```bash
grep -RIn '{{[a-z_]*}}' . --exclude-dir=.git   # должно быть пусто
```

## ✅ CI/CD

Базовый pipeline лежит в [`.github/workflows/ci.yml`](.github/workflows/ci.yml):
он запускает линт и тесты на каждый push и pull request. Адаптируйте шаги под
стек продукта (язык, менеджер пакетов, команды сборки/тестов).

В pipeline уже включена проверка именования хронологических документов:
`./tools/validate-file-naming.sh`.
