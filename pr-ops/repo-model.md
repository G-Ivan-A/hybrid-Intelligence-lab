---
status: canonical
version: 1.4
updated: 2026-07-16
temperature: 0.1
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
| `practices/` | Fixed practice knowledge base: атомарные reusable practices, отделённые от research и docs. | Создавать practice node только после source-backed research или повторяющейся проектной боли. |
| `frameworks/` | Методологии для hybrid human + AI teams. | Создавать только после comparison, показывающего недостаточность existing approaches. |
| `projects/` | Project knowledge bases, prompts, process context и spoke links. | Использовать, когда работа относится к scoped initiative, но не к production code. Наследование структуры в проектах — см. `standards/project-structure-inheritance.md`. |
| `education/` | Open education programs, course materials и teaching scenarios. | Использовать для материалов, пригодных для обучения или partner delivery. |
| `ai-governance/` | Policy bucket: human decision rights, security/compliance, внешние ограничения и эскалация. | Добавлять только обязательства уровня политики по границе ADR-007. |
| `ai-rules/` | Правила поведения агента и быстрой синхронизации с контекстом проекта. | Добавлять только правила, которые уточняют поведение или quick-sync агента. |
| `pr-ops/` | Операции над репозиторием и PR: repo model, artifact map, backlog, реестры и session digests. | Добавлять operating files только когда они уточняют active decision-making. |
| `projects-sink/` | Приёмник контекста spoke-проектов, синхронизируемого в Хаб. | Добавлять только синхронизируемый из spoke контекст, не production-код. |
| `docs/rfc/` | RFC-предложения об изменении структуры, lifecycle и правил Хаба. | Создавать RFC только для активно обсуждаемого изменения, требующего review. |
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

## Исключения архетипа A из универсального ядра ADR-001

ADR-001 задает универсальное ядро экосистемы, включая `kb/` и `runs/`. Для
текущего Хаба эти каталоги не создаются в корне: issue #386 не нашел
операционной боли, которую они решают лучше существующих домов. Это явное
исключение архетипа A из физической структуры, а не отмена семантики ADR-001 для
других репозиториев экосистемы.

| Каталог ADR-001 | Статус в текущем Хабе | Активные дома в Хабе | Триггер пересмотра |
| --- | --- | --- | --- |
| `kb/` | Не создается в корне Хаба. | `ai-rules/`, `pr-ops/`, `standards/`, `practices/`, `docs/guides/`; при необходимости проект-специфичный `projects/<project>/kb/`. | Появились как минимум 2-3 reusable operational knowledge artifacts, которые регулярно потребляет агент/процесс и которые нельзя без дублирования разместить в существующих домах. |
| `runs/` | Не создается в корне Хаба. | GitHub issue/PR/CI records, `pr-ops/session-digests.md`, `docs/report/`, `research/<domain>/exp/<issue-slug>/` для research evidence. | Появились повторяющиеся non-research operational/business/pipeline runs, которым нужны стабильные repo-hosted metadata, inputs, outputs, feedback и logs. |

Обоснование и сравнение с экосистемными репозиториями зафиксированы в
[docs/analysis/2026-07-04-kb-runs-hub-applicability-analysis.md](../docs/analysis/2026-07-04-kb-runs-hub-applicability-analysis.md).
ADR-007 остается ближайшим decision record для целевой структуры корня Хаба.

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
| **Кейс 2 — *Bootstrap-клонирование*** | Из шаблонов Хаба рождается новый репозиторий: геном `templates/htom/` — для HTOM-команды (гибридная human + AI работа), `templates/spoke/` — для production-спока (код с собственным жизненным циклом). | Постоянный — однократный акт при создании. | `Project` |

- Определения терминов *Runtime-онбординг* и *Bootstrap-клонирование* — единый
  источник истины в [standards/glossary.md](../standards/glossary.md).
- Полная модель жизненного цикла spoke (аналогии, таблица-манифест,
  Mermaid-схема, привязка к ретроспективе) —
  [docs/rfc/rfc-two-cases-of-project-initialization.md](../docs/rfc/rfc-two-cases-of-project-initialization.md).

## Standards

- [standards/project-structure-inheritance.md](../standards/project-structure-inheritance.md)
  фиксирует наследование структуры каталогов в проектах и границы
  проект-специфичных стандартов.
- [standards/executable-documentation-standard.md](../standards/executable-documentation-standard.md)
  фиксирует границу descriptive documents, executable documents и practice graph.
- [standards/htom-documentation-structure.md](../standards/htom-documentation-structure.md)
  фиксирует рекомендуемую структуру `docs/` для HTOM-репозиториев.

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
