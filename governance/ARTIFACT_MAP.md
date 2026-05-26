---
status: canonical
version: 1.0
updated: 2026-05-26
ai-generated: false
---

# Artifact Map

Версия: 1.0

Дата: 2026-05-26

Карта артефактов — единая точка входа в репозиторий `hybrid-Intelligence-lab`.
Она показывает, что где лежит, зачем нужно и как связано, чтобы новые участники
и AI-агенты быстро ориентировались без чтения всех файлов подряд.

Карта дополняет [README.md](../README.md), а не дублирует его: README дает
краткую визитку и ключевые ссылки, карта дает структурированную навигацию по
типам артефактов, их обязательности и связям.

## Условные обозначения

Колонка «Тип» использует контролируемый словарь, согласованный с терминами
[standards/GLOSSARY.md](../standards/GLOSSARY.md):

| Тип | Термин GLOSSARY | Что означает |
| --- | --- | --- |
| `навигация` | — | Точка входа и карта связей между артефактами. |
| `концепция` | Concept | Цель, границы, аудитории и операционная модель. |
| `контракт` | Contract | Операционное соглашение между ролями и режимами работы. |
| `правило` | Policy | Обязательное правило размещения, поведения или решения. |
| `руководство` | Guideline | Рекомендация по работе с возможными исключениями. |
| `стандарт` | Standard | Обязательный формат, словарь или критерии оформления. |
| `профиль` | Profile | Контекстная адаптация стандартов под класс проектов. |
| `шаблон` | Standard (template) | Образец для копирования и адаптации в проектах. |
| `утилита` | Artifact (script) | Воспроизводимая локальная проверка. |
| `журнал` | — | Date-based журнал governance-изменений. |
| `лицензия` | — | Governance placeholder до решения Founder & PO. |
| `каталог` | — | Раздел репозитория с собственным назначением. |

Колонка «Обязательный?»: `✅ Да` — файл или каталог проверяется в
[tools/validate-repository-structure.sh](../tools/validate-repository-structure.sh);
`⚠️ По необходимости` — добавляется по Anti-Inflation principle, когда снижает
операционную боль (см. [governance/REPO_MODEL.md](REPO_MODEL.md)).

## Карта артефактов

| Путь | Тип | Назначение | Обязательный? | Связанные артефакты |
| --- | --- | --- | --- | --- |
| `/README.md` | навигация | Визитка репозитория, ключевые документы и структура. | ✅ Да | `CONCEPT.md`, `standards/README.md`, `governance/ARTIFACT_MAP.md` |
| `/CONCEPT.md` | концепция | Актуальная концепция, аудитории, границы и модель hub-and-spoke. | ✅ Да | `governance/REPO_MODEL.md`, `standards/README.md` |
| `/AI_GOVERNANCE.md` | контракт | Роли, правила, operating modes, эскалация и Definition of Done для AI-assisted work. | ✅ Да | `CONCEPT.md`, `CONTRIBUTING.md`, `standards/README.md` |
| `/CONTRIBUTING.md` | руководство | Workflow вклада, локальные проверки и PR checklist. | ✅ Да | `AI_GOVERNANCE.md`, `governance/REPO_MODEL.md`, `standards/README.md` |
| `/CHANGELOG.md` | журнал | Date-based журнал governance-изменений репозитория. | ✅ Да | `README.md`, `CONCEPT.md` |
| `/LICENSE` | лицензия | Текущий license placeholder и pending-решение Founder & PO. | ✅ Да | `CONCEPT.md`, `AI_GOVERNANCE.md` |
| `/governance/REPO_MODEL.md` | правило | Модель структуры репозитория и Anti-Inflation principle. | ✅ Да | `CONCEPT.md`, `standards/README.md`, `tools/validate-repository-structure.sh` |
| `/governance/ARTIFACT_MAP.md` | навигация | Эта карта: навигация по артефактам, типам, обязательности и связям. | ✅ Да | `README.md`, `governance/REPO_MODEL.md`, `standards/GLOSSARY.md` |
| `/standards/README.md` | навигация | Плоский реестр активных и планируемых стандартов и инструкция применения. | ✅ Да | `governance/REPO_MODEL.md`, `standards/GLOSSARY.md` |
| `/standards/GLOSSARY.md` | стандарт | Единый словарь терминов для standards, governance и AI-assisted work. | ✅ Да | `standards/README.md`, все стандарты |
| `/standards/FILE_NAMING.md` | стандарт | Единые паттерны именования файлов и каталогов для research, standards, экспериментов, профилей и курсов. | ✅ Да | `standards/README.md`, `standards/GLOSSARY.md` |
| `/standards/ISSUE_WORKFLOW.md` | стандарт | Жизненный цикл задач: 7 статусов, правила переходов и связи между артефактами. | ✅ Да | `standards/README.md`, `governance/ARTIFACT_MAP.md`, `CHANGELOG.md` |
| `/standards/TEAM_CONTRACT.md` | шаблон | Шаблон и инструкция для создания project-level `CONTRIBUTING.md` и `AI_GOVERNANCE.md`. | ✅ Да | `standards/RESEARCH_PROFILE.md`, `standards/PRODUCT_PROFILE.md`, `standards/EDUCATION_PROFILE.md` |
| `/standards/RESEARCH_PROFILE.md` | профиль | Профиль исследовательских проектов: именование, frontmatter, эксперименты. | ✅ Да | `standards/README.md`, `standards/TEAM_CONTRACT.md` |
| `/standards/PRODUCT_PROFILE.md` | профиль | Профиль продуктовых проектов: обязательные артефакты и шаблон `PRODUCT_VISION.md`. | ✅ Да | `standards/README.md`, `standards/TEAM_CONTRACT.md` |
| `/standards/EDUCATION_PROFILE.md` | профиль | Профиль образовательных проектов: модули, уроки, упражнения и адаптация форматов. | ✅ Да | `standards/README.md`, `standards/TEAM_CONTRACT.md` |
| `/tools/validate-frontmatter.sh` | утилита | Soft-проверка обязательных полей frontmatter в Markdown. | ✅ Да | `CONTRIBUTING.md`, `standards/README.md` |
| `/tools/validate-repository-structure.sh` | утилита | Проверка активной структуры, навигационных ссылок и `-old` миграции. | ✅ Да | `governance/REPO_MODEL.md`, `governance/ARTIFACT_MAP.md` |
| `/.github/ISSUE_TEMPLATE/task.yml` | шаблон | GitHub-native структура постановки задач с operating mode. | ✅ Да | `AI_GOVERNANCE.md`, `standards/GLOSSARY.md` |
| `/research/mango/taxonomy-concept-2026-05.md` | концепция | Draft-концепция Unified Capability Taxonomy для Mango: мета-модель, mapping фич, процесс нормализации, интерфейс команд, метрики, пилот и риски. | ⚠️ По необходимости | `research/mango/classification-old.md`, `research/mango/classification-tz-old.md`, `research/mango/requirements-flow-old.md`, `projects/mango/README.md`, `standards/GLOSSARY.md`, `governance/REPO_MODEL.md` |
| `/standards/` | каталог | Плоский реестр стандартов, шаблонов и правил оформления артефактов. | ✅ Да | `standards/README.md`, `governance/REPO_MODEL.md` |
| `/governance/` | каталог | Модель репозитория, навигация и сквозные governance-правила. | ✅ Да | `governance/REPO_MODEL.md`, `governance/ARTIFACT_MAP.md` |
| `/tools/` | каталог | Локальные validation и maintenance скрипты. | ✅ Да | `tools/validate-frontmatter.sh`, `tools/validate-repository-structure.sh` |
| `/research/` | каталог | Доменные исследования и source-backed analysis; содержит активную Mango taxonomy-концепцию и сохраненные `-old` исторические входы. | ✅ Да | `standards/RESEARCH_PROFILE.md`, `governance/REPO_MODEL.md` |
| `/frameworks/` | каталог | Методологии, создаваемые только после доказанного gap (сейчас — `-old` входы). | ✅ Да | `governance/REPO_MODEL.md`, `standards/README.md` |
| `/projects/` | каталог | Project knowledge bases и контекст spoke-репозиториев (сейчас — `-old` входы). | ✅ Да | `standards/PRODUCT_PROFILE.md`, `governance/REPO_MODEL.md` |
| `/education/` | каталог | Open education: программы и учебные материалы (сейчас — `-old` входы). | ✅ Да | `standards/EDUCATION_PROFILE.md`, `governance/REPO_MODEL.md` |
| `/.github/ISSUE_TEMPLATE/` | каталог | GitHub-native структура постановки задач. | ✅ Да | `.github/ISSUE_TEMPLATE/task.yml` |

## Исторические входы (`-old`)

Файлы и каталоги с суффиксом `-old` (например, `research/mango/*-old.md`,
`research/repository-governance/*-old.md`,
`education/ba-prompt-engineering/*-old.md`, `docs-old/`, `experiments-old/`,
`meta-old/`) — это сохраненные historical inputs предыдущей структуры. Они не
являются активным контрактом и не
перечислены построчно в карте.

Их содержание переносится в активные артефакты только через reviewable pull
request, который ссылается на source path (см. правило миграции в
[governance/REPO_MODEL.md](REPO_MODEL.md) и [CONCEPT.md](../CONCEPT.md)). После
переноса новый активный артефакт добавляется в карту выше.

## Как использовать карту

1. Не знаешь, где что лежит? → открой эту карту и найди артефакт по колонке
   «Путь».
2. Ищешь правило работы или формат? → смотри колонку «Тип»: `правило` и
   `контракт` задают обязательное поведение; `стандарт`, `профиль` и `шаблон`
   задают формат артефактов; `руководство` дает рекомендации.
3. Не уверен, обязателен ли файл? → смотри колонку «Обязательный?».
4. Нужно понять связи? → смотри колонку «Связанные артефакты».
5. Термин непонятен? → сверься со [standards/GLOSSARY.md](../standards/GLOSSARY.md).

## Как обновлять карту

- При создании нового активного артефакта → добавь строку в таблицу, укажи
  тип, обязательность и связи, и зарегистрируй файл в
  [tools/validate-repository-structure.sh](../tools/validate-repository-structure.sh)
  (`is_active_file` и, если файл обязателен, `required_files`).
- При удалении артефакта → удали строку или пометь как `❌ Удалён` и обнови
  валидатор структуры.
- При изменении назначения → обнови колонки «Назначение» и «Связанные
  артефакты».
- При переносе содержания из `-old` файла → добавь новый активный артефакт в
  карту и сошлись на source path в pull request.
- После любого изменения → обнови поле `updated` во frontmatter и запусти
  локальную проверку (`./tools/validate-frontmatter.sh .` и
  `./tools/validate-repository-structure.sh`).
- Не добавляй в карту артефакты, которых нет в репозитории: карта отражает
  фактическое состояние, а не планы (Anti-Inflation principle,
  [governance/REPO_MODEL.md](REPO_MODEL.md)).

## Связанные контракты

| Документ | Роль |
| --- | --- |
| [README.md](../README.md) | Точка входа и краткая навигация. |
| [CONCEPT.md](../CONCEPT.md) | Концепция, аудитории и границы репозитория. |
| [governance/REPO_MODEL.md](REPO_MODEL.md) | Правила структуры и Anti-Inflation principle. |
| [standards/README.md](../standards/README.md) | Реестр активных и планируемых стандартов. |
| [standards/GLOSSARY.md](../standards/GLOSSARY.md) | Canonical источник терминов для колонки «Тип». |
