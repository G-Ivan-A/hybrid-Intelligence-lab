---
status: canonical
version: 1.1
updated: 2026-06-04
ai-generated: false
executable: false
---

# Repository Model

Документ фиксирует активную структуру репозитория и Anti-Inflation principle
для `hybrid-Intelligence-lab`.

## Структура

| Путь | Назначение | Правило создания |
| --- | --- | --- |
| `standards/` | Плоский реестр standards, templates и artifact format rules. | Добавлять standard после повторяющейся review или coordination problem. |
| `research/` | Domain-based research и source-backed analysis. | Использовать `research/<domain>/` для домена или topic area. |
| `frameworks/` | Методологии для hybrid human + AI teams. | Создавать только после comparison, показывающего недостаточность existing approaches. |
| `projects/` | Project knowledge bases, prompts, process context и spoke links. | Использовать, когда работа относится к scoped initiative, но не к production code. Наследование структуры в проектах — см. `standards/project-structure-inheritance.md`. |
| `education/` | Open education programs, course materials и teaching scenarios. | Использовать для материалов, пригодных для обучения или partner delivery. |
| `governance/` | Repository model и cross-cutting operating decisions. | Добавлять governance files только когда они уточняют active decision-making. |
| `tools/` | Локальные validation и maintenance scripts. | Добавлять scripts, которые делают проверки воспроизводимыми. |
| `.github/ISSUE_TEMPLATE/` | GitHub-native task intake. | Держать templates focused на качестве issue и reviewability. |

Именование файлов для корня репозитория и вложенных каталогов описано в
[standards/file-naming.md](../standards/file-naming.md).

## Anti-Inflation Principle

**Артефакт только при операционной боли.**

Артефакт оправдан, когда снижает наблюдаемую операционную проблему:
повторяющуюся путаницу, повторяющиеся review comments, дублирование решений,
неясную ownership, нестабильные links или unverifiable work.

Артефакт не оправдан, если он только делает дерево визуально полным.

## Decision Rules — исполнимая часть справочного документа

> Применяй эти правила при создании и изменении структуры репозитория. Весь
> документ остается справочным policy/reference (`executable: false`), а таблица
> ниже является decision checklist к применению.

| Ситуация | Действие |
| --- | --- |
| Создается новый файл. | Проверить имя по [standards/file-naming.md](../standards/file-naming.md). |
| Новый документ повторяет existing standard. | Сослаться на standard и держать документ коротким. |
| Формат нужен один раз. | Встроить нужную структуру прямо в artifact. |
| Формат нужен повторно. | Создать или обновить standard в `standards/`. |
| Governance text распадается на несколько активных областей. | Выделить только область, где уже есть active use и review pain. |
| Production code получает собственный lifecycle. | Перенести его в spoke repository и ссылаться назад на этот hub. |
| Historical content может быть полезным. | Переносить выборочно через reviewable PR и указывать source path из audit/history. |

## Spoke Lifecycle: два кейса инициализации

Слово «инициализация проекта» в модели hub-and-spoke скрывает **два
ортогональных процесса**. Их нельзя смешивать — иначе повторяется
терминологическая путаница (ошибка №5 ретроспективы). Канон фиксирует разделение
кратко и ссылается на источники; полное обоснование, аналогии и Mermaid-схема
жизненного цикла — в RFC-манифесте, а определения терминов — в глоссарии.

| Кейс | Суть | Долговечность | Operating Mode |
| --- | --- | --- | --- |
| **Кейс 1 — *Runtime-онбординг*** | Агент в чате загружает контекст проекта из репозитория в оперативную память диалога; файлы не создаются (read-only до апрува человека). | Эфемерный — повторяется при каждом чате. | `Structured` |
| **Кейс 2 — *Bootstrap-клонирование*** | Из шаблонов Хаба (`templates/spoke/`) рождается новый spoke-репозиторий с правильной структурой. | Постоянный — однократный акт при создании spoke. | `Project` |

- Определения терминов *Runtime-онбординг* и *Bootstrap-клонирование* — единый
  источник истины в [standards/glossary.md](../standards/glossary.md).
- Полная модель жизненного цикла spoke (аналогии, таблица-манифест,
  Mermaid-схема, привязка к ретроспективе) —
  [governance/rfc/rfc-two-cases-of-project-initialization.md](rfc/rfc-two-cases-of-project-initialization.md).

## Standards

- [standards/project-structure-inheritance.md](../standards/project-structure-inheritance.md)
  фиксирует наследование структуры каталогов в проектах и границы
  проект-специфичных стандартов.

## Migration Handling

Cleanup issue #49 удалил или перенес legacy files с суффиксом `-old`. Новые
tracked `-old` файлы не добавляются без отдельного migration issue и явного
обоснования. Если содержание переносится из historical input, active artifact
указывает source path, а PR объясняет, почему содержание остается полезным.

## Validation

Активная структура проверяется командой:

```bash
./tools/validate-repository-structure.sh
```
