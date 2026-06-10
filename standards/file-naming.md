---
status: canonical
version: 1.2
updated: 2026-06-06
ai-generated: false
---

# Правило именования файлов

Стандарт фиксирует единое правило именования файлов для новых артефактов
репозитория. Цель — сохранить GitHub-конвенцию для корневых файлов и сделать
вложенные структуры читаемыми, удобными для терминала и устойчивыми к росту.

## Правило именования файлов

| Расположение | Стиль | Пример | Почему |
| --- | --- | --- | --- |
| **Корень репозитория** (`/`) | `UPPERCASE_WITH_HYPHENS.md` | `README.md`, `CONCEPT.md`, `CHANGELOG.md` | Конвенция GitHub, файлы видны сразу |
| **Вложенные каталоги** (`standards/`, `research/`, `projects/`, `kb/` и др.) | `lowercase-with-hyphens.md` | `classification-glossary.md`, `rag-mapping-roadmap.md` | Читаемость, сортировка, удобно в терминале, масштабируемость |

## Правила именования файлов в standards/ и governance/

- Все файлы в `standards/` и `governance/` должны быть в `kebab-case`: строчные
  буквы, цифры и дефисы.
- Исключения: только системные файлы `README.md`, `LICENSE`, `CHANGELOG.md`.
- `CAPS_LOCK` запрещён для документов внутри `standards/` и `governance/`.

### Примеры для standards/ и governance/

- Правильно: `research-profile.md`
- Правильно: `agent-onboarding-protocol.md`
- Правильно: `executable-contract-standard.md`
- Неправильно: `RESEARCH_DOCUMENTATION_STANDARD.md`
- Неправильно: `AGENT_ONBOARDING.md`
- Неправильно: `Research_Documentation_Standard.md`

### Исключения

- Файлы с версиями: `migration-audit-2026-05.md` (дата в имени)
- Файлы с префиксами: `README-old.md` (суффикс `-old` для унаследованных файлов)

### Проверка

- Новый файл не соответствует правилу? Отклонить в ревью.
- Существующий файл нарушает правило? Переименовать при следующем
  редактировании, не блокируя текущую работу.

## Правило для AI-ассистентов

В режиме `structured` строго следуй правилу: корневые файлы остаются в
`UPPERCASE_WITH_HYPHENS.md`, вложенные файлы создаются как
`lowercase-with-hyphens.md`. Не добавляй исключения без явного указания в issue,
PR comment или другом human-authored governance документе.
