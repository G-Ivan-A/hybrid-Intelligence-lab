---
status: canonical
version: 1.18
updated: 2026-06-06
ai-generated: false
---

# Artifact Map

Версия: 1.18

Дата: 2026-06-06

Карта артефактов — единая точка входа в репозиторий `hybrid-Intelligence-lab`.
Она показывает, что где лежит, зачем нужно и как связано, чтобы новые участники
и AI-агенты быстро ориентировались без чтения всех файлов подряд.

Карта дополняет [README.md](../README.md), а не дублирует его: README дает
краткую визитку и ключевые ссылки, карта дает структурированную навигацию по
типам артефактов, их обязательности и связям.

## Условные обозначения

Колонка «Тип» использует контролируемый словарь, согласованный с терминами
[standards/glossary.md](../standards/glossary.md):

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
| `исследование` | Artifact | Source-backed результат исследования, анализа корпуса или доменного моделирования. |
| `утилита` | Artifact (script) | Воспроизводимая локальная проверка. |
| `журнал` | — | Date-based журнал governance-изменений. |
| `лицензия` | — | Governance placeholder до решения Founder & PO. |
| `каталог` | — | Раздел репозитория с собственным назначением. |

Колонка «Обязательный?»: `✅ Да` — файл или каталог проверяется в
[tools/validate-repository-structure.sh](../tools/validate-repository-structure.sh);
`⚠️ По необходимости` — добавляется по Anti-Inflation principle, когда снижает
операционную боль (см. [governance/REPO_MODEL.md](REPO_MODEL.md)).

Колонка «🚦 Исполнимый?» использует стандарт
[governance/rfc/contract-executability-rfc.md](rfc/contract-executability-rfc.md)
и фиксирует фактическую роль документа:

| Пометка | Что означает |
| --- | --- |
| `🚦 entrypoint` | Исполнимый входной документ: при получении ссылки агент выполняет протокол, а не анализирует текст. |
| `🚦 да` | Исполнимый документ или шаблон: его правила/промпт применяются как действие. |
| `справка` | Справочный контракт, стандарт или RFC: читать как контекст и источник правил, без немедленного исполнения всего файла. |
| `—` | Исполнимость не применяется к этому артефакту. |

## Карта артефактов

| Путь | Тип | 🚦 Исполнимый? | Назначение | Обязательный? | Связанные артефакты |
| --- | --- | --- | --- | --- | --- |
| `/README.md` | навигация | — | Визитка репозитория, ключевые документы и структура. | ✅ Да | `CONCEPT.md`, `standards/README.md`, `governance/ARTIFACT_MAP.md`, `governance/AGENT_ONBOARDING.md` |
| `/CONCEPT.md` | концепция | — | Актуальная концепция, аудитории, границы и модель hub-and-spoke. | ✅ Да | `governance/REPO_MODEL.md`, `standards/README.md` |
| `/AI_GOVERNANCE.md` | контракт | справка | Роли, правила, operating modes, эскалация и Definition of Done для AI-assisted work. | ✅ Да | `CONCEPT.md`, `CONTRIBUTING.md`, `standards/README.md`, `governance/AGENT_ONBOARDING.md`, `governance/rfc/contract-executability-rfc.md` |
| `/CONTRIBUTING.md` | руководство | — | Workflow вклада, локальные проверки и PR checklist. | ✅ Да | `AI_GOVERNANCE.md`, `governance/REPO_MODEL.md`, `standards/README.md` |
| `/CHANGELOG.md` | журнал | — | Date-based журнал governance-изменений репозитория. | ✅ Да | `README.md`, `CONCEPT.md` |
| `/LICENSE` | лицензия | — | Текущий license placeholder и pending-решение Founder & PO. | ✅ Да | `CONCEPT.md`, `AI_GOVERNANCE.md` |
| `/governance/AGENT_ONBOARDING.md` | правило | 🚦 entrypoint | Рабочая инструкция *Runtime-онбординга* (Кейс 1): единый входной артефакт для нового агента — *Handover Prompt* с `{{REPO_NAME}}`, 4-шаговый протокол (governance → контекст → *Readback* → стоп до апрува) и раздел threat awareness «Что может пойти не так». Операционная пара к дизайн-RFC (`rfc/`). Точки входа — `README.md` и `AI_GOVERNANCE.md`. | ✅ Да | `README.md`, `AI_GOVERNANCE.md`, `governance/rfc/rfc-agent-onboarding-protocol.md`, `governance/rfc/rfc-two-cases-of-project-initialization.md`, `governance/rfc/contract-executability-rfc.md`, `templates/spoke/README.md`, `standards/glossary.md` |
| `/governance/REPO_MODEL.md` | правило | справка | Модель структуры репозитория и Anti-Inflation principle. | ✅ Да | `CONCEPT.md`, `standards/README.md`, `tools/validate-repository-structure.sh`, `governance/rfc/contract-executability-rfc.md` |
| `/governance/ARTIFACT_MAP.md` | навигация | справка | Эта карта: навигация по артефактам, типам, обязательности, исполнимости и связям. | ✅ Да | `README.md`, `governance/REPO_MODEL.md`, `standards/glossary.md`, `governance/rfc/contract-executability-rfc.md` |
| `/governance/BACKLOG.md` | навигация | — | Единый бэклог работ Хаба (Sprint 3): сводная таблица задач, приоритеты P0–P3, зависимости и критический путь, источники, креативный анализ рекомендаций команд С и Q, North Star и триггеры пересмотра. Ортогонален этой карте: карта показывает «что есть», бэклог — «что осталось». Решение по приоритетам за человеком. | ✅ Да | `governance/rfc/rfc-agent-onboarding-protocol.md`, `governance/rfc/rfc-two-cases-of-project-initialization.md`, `research/hub/external-governance-patterns-review-2026-06.md`, `standards/glossary.md` |
| `/governance/EXECUTABLE_DOCUMENTS_ISSUES.md` | навигация | — | Реестр GitHub Issues CE-001..CE-010 для внедрения стандарта исполнимых документов по RFC §6.1: URL задач, файлы, приоритеты, зависимости, статусы и обязательные метки. | ✅ Да | `governance/rfc/contract-executability-rfc.md`, `governance/BACKLOG.md`, `standards/glossary.md` |
| `/governance/rfc/README.md` | навигация | — | Индекс каталога RFC Хаба: что попадает в `governance/rfc/`, таблица четырёх RFC и статус каталога (опциональный, создаётся по необходимости — решение Q3, issue #165). Каталог переименован из `governance/proposals/` (решение Q1). | ✅ Да | `governance/ARTIFACT_MAP.md`, `governance/REPO_MODEL.md`, `research/governance/governance-folder-structure-decisions-2026-06.md` |
| `/governance/rfc/rfc-creative-template-design.md` | RFC | — | Креативное предложение "ДНК-шаблона" для клонирования spoke-проектов: аналогия, сравнительная матрица имён (`templates`/`blueprints`/`genesis`), минимальная карта файлов, краевые случаи и Mermaid-схема. Решение за человеком. | ⚠️ По необходимости | `governance/REPO_MODEL.md`, `research/project-context-and-bootstrap-patterns-2026-05.md`, `standards/project-structure-inheritance.md` |
| `/governance/rfc/rfc-agent-onboarding-protocol.md` | RFC | — | Креативное предложение "Протокола бесшовной передачи проекта": аналогия предполётного чек-листа и readback, обоснование с трассировкой к провалам холодного старта, готовый Handover Prompt, 4-шаговый алгоритм агента (governance → контекст → readback → стоп до апрува), Mermaid-схема и выбор места для будущего `AGENT_ONBOARDING.md`. Решение за человеком. | ⚠️ По необходимости | `AI_GOVERNANCE.md`, `governance/REPO_MODEL.md`, `research/hub/project-context-and-bootstrap-patterns-2026-05.md`, `standards/project-structure-inheritance.md` |
| `/governance/rfc/rfc-two-cases-of-project-initialization.md` | RFC | — | Концептуальный манифест разделения двух ортогональных кейсов инициализации проекта: Кейс 1 (Runtime-онбординг) и Кейс 2 (Bootstrap-клонирование). Аналогии из 4 смежных областей, таблица-манифест (13 строк), Mermaid-схема жизненного цикла, обоснование с трассировкой к ретроспективе, follow-up. Термины — только из `standards/glossary.md`. Решение за человеком. | ⚠️ По необходимости | `governance/rfc/rfc-agent-onboarding-protocol.md`, `governance/rfc/rfc-creative-template-design.md`, `research/hub/ai-collaboration-retrospective-2026-06.md`, `standards/glossary.md` |
| `/governance/rfc/contract-executability-rfc.md` | RFC | справка | RFC архитектуры исполнимых документов: анализ инцидента «анализ вместо исполнения», утверждённое Видение 3, маркер `executable: true\|false`, план внедрения P0 → P3 и решения фаундера Human Review 2026-06. | ⚠️ По необходимости | `governance/ARTIFACT_MAP.md`, `governance/AGENT_ONBOARDING.md`, `AI_GOVERNANCE.md`, `standards/issue-workflow.md`, `templates/spoke/AI_QUICK_RULES.md`, `templates/spoke/AI_HANDOVER_PROMPT.md`, `standards/glossary.md` |
| `/templates/spoke/AI_GOVERNANCE.md` | шаблон | справка | Шаблон конституции спока: роли, правила, operating modes, эскалация и DoD. Ядро генома (обязателен в корне спока). Плейсхолдеры `{{project_name}}`, `{{hub_url}}`, `{{date}}`. | ⚠️ По необходимости | `governance/rfc/rfc-creative-template-design.md`, `AI_GOVERNANCE.md`, `templates/spoke/AI_QUICK_RULES.md` |
| `/templates/spoke/AI_QUICK_RULES.md` | шаблон | 🚦 да | Шаблон одностраничной "инструкции по выживанию" агента в новом споке: куда смотреть, чего не делать (включая запрет `research/`), как звать человека. | ⚠️ По необходимости | `templates/spoke/AI_GOVERNANCE.md`, `templates/spoke/README.md`, `governance/rfc/contract-executability-rfc.md` |
| `/templates/spoke/AI_HANDOVER_PROMPT.md` | шаблон | 🚦 да | Копия *Handover Prompt* (с плейсхолдером `{{REPO_NAME}}`) в геноме спока: готовая «доверенность» для запуска агента (Runtime-онбординг). Источник истины — хабовый `governance/AGENT_ONBOARDING.md`; спок хранит копию для самодостаточности. | ⚠️ По необходимости | `governance/rfc/rfc-agent-onboarding-protocol.md`, `templates/spoke/AI_QUICK_RULES.md`, `templates/spoke/README.md`, `governance/rfc/contract-executability-rfc.md` |
| `/templates/spoke/README.md` | шаблон | — | Шаблон визитки спока с плейсхолдерами и связью с Хабом: цель, структура "сейчас", ссылки на governance. | ⚠️ По необходимости | `templates/spoke/AI_GOVERNANCE.md`, `templates/spoke/CONTRIBUTING.md` |
| `/templates/spoke/CONTRIBUTING.md` | шаблон | — | Шаблон workflow вклада спока: issue → PR → review, PR checklist, AI-assisted work. | ⚠️ По необходимости | `templates/spoke/AI_GOVERNANCE.md`, `templates/spoke/.github/ISSUE_TEMPLATE/task.md` |
| `/templates/spoke/CHANGELOG.md` | шаблон | — | Шаблон журнала спока: каркас с секцией `## Unreleased` (Keep a Changelog). | ⚠️ По необходимости | `templates/spoke/README.md` |
| `/templates/spoke/docs/adr/.gitkeep` | шаблон | — | Каркас каталога Architecture Decision Records спока с поясняющим комментарием. | ⚠️ По необходимости | `templates/spoke/AI_GOVERNANCE.md` |
| `/templates/spoke/docs/audit/.gitkeep` | шаблон | — | Каркас каталога аудитов и проверок соответствия спока с поясняющим комментарием. | ⚠️ По необходимости | `templates/spoke/AI_GOVERNANCE.md` |
| `/templates/spoke/.github/ISSUE_TEMPLATE/task.md` | шаблон | — | Шаблон задачи спока (Markdown), наследующий поля Хаба из `standards/issue-workflow.md`: Мета, Контекст, Артефакты, Готово когда. | ⚠️ По необходимости | `standards/issue-workflow.md`, `.github/ISSUE_TEMPLATE/task.yml` |
| `/templates/spoke/tools/validate-repository-structure.sh` | шаблон | — | Минимальный валидатор структуры спока ("иммунная система"): проверяет 9 базовых артефактов и предупреждает о `research/` и незаменённых плейсхолдерах. | ⚠️ По необходимости | `templates/spoke/AI_GOVERNANCE.md`, `tools/validate-repository-structure.sh` |
| `/templates/spoke/init.sh` | шаблон | — | Скрипт инициализации спока (креативное улучшение UX): интерактивная/CLI-замена плейсхолдеров `{{...}}`, автоген `{{date}}`, портабельный `sed`, самоудаление после запуска. | ⚠️ По необходимости | `templates/spoke/README.md`, `templates/spoke/tools/validate-repository-structure.sh` |
| `/templates/webportal-concept-template.md` | шаблон | — | Копируемый Markdown-шаблон концепции веб-портала по `standards/webportal-concept-standard.md`: обязательное ядро (разделы 1–6) плюс опциональные слои (7–15) с подсказками по заполнению и плейсхолдерами. | ⚠️ По необходимости | `standards/webportal-concept-standard.md`, `research/portal/concept-standards-comparison-2026-06.md` |
| `/standards/README.md` | навигация | — | Плоский реестр активных и планируемых стандартов и инструкция применения. | ✅ Да | `governance/REPO_MODEL.md`, `standards/glossary.md` |
| `/standards/glossary.md` | стандарт | справка | Единый словарь терминов для standards, governance и AI-assisted work. | ✅ Да | `standards/README.md`, `governance/rfc/contract-executability-rfc.md`, все стандарты |
| `/standards/file-naming.md` | стандарт | — | Единые паттерны именования файлов и каталогов для research, standards, экспериментов, профилей и курсов. | ✅ Да | `standards/README.md`, `standards/glossary.md` |
| `/standards/issue-workflow.md` | стандарт | справка | Жизненный цикл задач: 7 статусов, правила переходов и связи между артефактами. | ✅ Да | `standards/README.md`, `governance/ARTIFACT_MAP.md`, `CHANGELOG.md`, `governance/rfc/contract-executability-rfc.md` |
| `/standards/project-structure-inheritance.md` | стандарт | справка | Правило наследования структуры каталогов в `projects/{project}/`, границы проектных подкаталогов и review-проверки для структуры проектов. | ✅ Да | `governance/REPO_MODEL.md`, `standards/file-naming.md`, `standards/glossary.md`, `governance/rfc/contract-executability-rfc.md` |
| `/standards/portal-repository-structure.md` | стандарт | справка | Структура репозитория портала (класс spoke-проекта — «единая точка сборки»): геном спока плюс портал-каталоги (`projects/`, `presentations/`, `collaborations/`, `learning/`, `knowledge-base/`), принципы наследования и расширения, примеры и migration-гайд. Статус `draft` (предложен на утверждение фаундеру, RFC §14). | ⚠️ По необходимости | `standards/project-structure-inheritance.md`, `templates/spoke/README.md`, `research/portal/open-ai-portal-concept-rfc.md`, `research/portal/repository-structure-design-2026-06.md` |
| `/standards/research-documentation-standard.md` | стандарт | справка | Стандарт оформления research-документации Хаба: обязательная структура Введение → Результаты → Детализация (BLUF / «перевёрнутая пирамида» / IMRaD), требования к цитированию источников и frontmatter. Обоснование — `research/governance/research-documentation-format-2026-06.md`. | ✅ Да | `research/governance/research-documentation-format-2026-06.md`, `standards/research-profile.md`, `standards/glossary.md` |
| `/standards/executable-contract-standard.md` | стандарт | справка | Стандарт формата исполнимых контрактов: блок EXECUTION (команда первой строкой) над блоком EXPLANATION, маркеры `executable`/`entrypoint`, директивный блок. Обоснование — `research/governance/executable-contract-format-2026-06.md`. | ✅ Да | `research/governance/executable-contract-format-2026-06.md`, `governance/rfc/contract-executability-rfc.md`, `standards/glossary.md` |
| `/standards/contract-documentation-standard.md` | стандарт | справка | Стандарт документирования контрактов Хаба (governance, API, SLA): нормативный язык RFC 2119 / BCP 14, обязательные секции, версионирование и обратная совместимость. Обоснование — `research/governance/contract-documentation-format-2026-06.md`. | ✅ Да | `research/governance/contract-documentation-format-2026-06.md`, `standards/README.md`, `standards/glossary.md` |
| `/standards/webportal-concept-standard.md` | стандарт | справка | Универсальный модульный стандарт структуры концепции веб-портала: обязательное ядро (6 разделов) плюс опциональные слои (9), профили сложности (сайт-визитка / контентный портал / app-портал), связи с roadmap, исследованиями и структурой репозитория (выбирается из политики Хаба, не из концепции). Границы: не для лендингов, мобильных приложений, бэкенд-сервисов и микросервисов. Статус `draft` (предложен на утверждение фаундеру). Обоснование — `research/portal/concept-standards-comparison-2026-06.md`. | ⚠️ По необходимости | `research/portal/concept-standards-comparison-2026-06.md`, `templates/webportal-concept-template.md`, `standards/portal-repository-structure.md`, `standards/README.md`, `standards/glossary.md` |
| `/standards/team-contract.md` | шаблон | — | Шаблон и инструкция для создания project-level `CONTRIBUTING.md` и `AI_GOVERNANCE.md`. | ✅ Да | `standards/research-profile.md`, `standards/product-profile.md`, `standards/education-profile.md` |
| `/standards/research-profile.md` | профиль | — | Профиль исследовательских проектов: именование, frontmatter, эксперименты. | ✅ Да | `standards/README.md`, `standards/team-contract.md` |
| `/standards/product-profile.md` | профиль | — | Профиль продуктовых проектов: обязательные артефакты и шаблон `PRODUCT_VISION.md`. | ✅ Да | `standards/README.md`, `standards/team-contract.md` |
| `/standards/education-profile.md` | профиль | — | Профиль образовательных проектов: модули, уроки, упражнения и адаптация форматов. | ✅ Да | `standards/README.md`, `standards/team-contract.md` |
| `/tools/validate-frontmatter.sh` | утилита | — | Soft-проверка обязательных полей frontmatter в Markdown. | ✅ Да | `CONTRIBUTING.md`, `standards/README.md` |
| `/tools/validate-repository-structure.sh` | утилита | — | Проверка активной структуры, навигационных ссылок и `-old` миграции. | ✅ Да | `governance/REPO_MODEL.md`, `governance/ARTIFACT_MAP.md` |
| `/.github/ISSUE_TEMPLATE/task.yml` | шаблон | — | GitHub-native структура постановки задач с operating mode. | ✅ Да | `AI_GOVERNANCE.md`, `standards/glossary.md` |
| `/research/mango/taxonomy-concept-2026-05.md` | концепция | — | Draft-концепция Unified Capability Taxonomy для Mango: мета-модель, mapping фич, процесс нормализации, интерфейс команд, метрики, пилот и риски. | ⚠️ По необходимости | `research/mango/classification-old.md`, `research/mango/classification-tz-old.md`, `research/mango/requirements-flow-old.md`, `mango_ba_prompts`, `standards/glossary.md`, `governance/REPO_MODEL.md` |
| `/research/mango/requirements-lifecycle-uncertainty-2026-05.md` | исследование | — | Жизненный цикл требования на доработку Mango: бенчмарк международной практики, моделирование кейсов (`0 → 1`), обработка неопределенности, декомпозиция и рекомендации для стандарта процесса БА. | ⚠️ По необходимости | `research/mango/requirements-flow.md`, `research/mango/taxonomy-concept-2026-05.md`, `research/mango/classification.md`, `mango_ba_prompts`, `standards/glossary.md` |
| `/research/mango/rag-mapping-roadmap-2026-05.md` | исследование | — | Маппинг продуктов/фич Mango как RAG-навигатор: структура `kb/product-matrix.md`, оценка источников документации, roadmap автоматизации БА и карта PlantUML-диаграмм. | ⚠️ По необходимости | `research/mango/taxonomy-concept-2026-05.md`, `research/mango/requirements-lifecycle-uncertainty-2026-05.md`, `mango_ba_prompts`, `standards/research-profile.md` |
| `/research/mango/capability-decomposition-2026-05.md` | исследование | — | Справочник атомарных функций пилотных доменов Mango (`voice-ucaas`, `contact-center`, `digital-channels`): параметры, международные источники, примеры ТЗ, критерии атомарности и связь с НФТ-классами. | ⚠️ По необходимости | `research/mango/classification.md`, `research/mango/classification-tz.md`, `research/mango/rag-mapping-roadmap-2026-05.md`, `mango_ba_prompts/standards/GLOSSARY.md` |
| `/research/hub/project-context-and-bootstrap-patterns-2026-05.md` | исследование | — | Паттерны передачи контекста, предсказуемого project bootstrap и маршрута "рекомендация -> задача" на опыте Mango. Scope: repo-wide. | ⚠️ По необходимости | `archive/projects/mango/README.md`, `archive/projects/mango/experiments/`, `research/mango/`, `mango_ba_prompts`, `standards/project-structure-inheritance.md` |
| `/research/hub/prompts-classification-audit-2026-05.md` | исследование | — | Аудит входных данных для классификации промптов: инвентаризация типов, паттерны отладки, пробелы. Scope: repo-wide. | ⚠️ По необходимости | `research/hub/prompts-classification-standard-2026-05.md`, `mango_ba_prompts/prompts/`, `mango_ba_prompts/prompts/experiments/prompts-audit-2026-05-26.md` |
| `/research/hub/prompts-classification-standard-2026-05.md` | исследование | — | Стандарт классификации промптов: таксономия (6 осей), матрица «тип × зрелость × сценарий» (10 ячеек), шаблоны отладки (A/B/C), план интеграции и вопросы для согласования. Scope: repo-wide. | ⚠️ По необходимости | `research/hub/prompts-classification-audit-2026-05.md`, `mango_ba_prompts/prompts/`, `standards/research-profile.md` |
| `/research/hub/team-c-governance-strategy-audit-2026-05.md` | исследование | — | Интерпретация аудита стратегии governance от команды C: сильные стороны, риски overgrowth, lightweight hierarchy, research lifecycle и backlog candidates. Scope: repo-wide. | ⚠️ По необходимости | `research/hub/project-context-and-bootstrap-patterns-2026-05.md`, `governance/REPO_MODEL.md`, `standards/research-profile.md` |
| `/research/hub/external-governance-patterns-review-2026-06.md` | исследование | — | Анализ external governance patterns (GitAgent/EGAProtocol/IETF AgentID) и матрица применимости рекомендаций команды С: что ценного (8 идей), «взять сейчас / отложить / отклонить», North Star проекта и триггеры пересмотра. Scope: repo-wide. | ⚠️ По необходимости | `governance/rfc/rfc-agent-onboarding-protocol.md`, `governance/rfc/rfc-two-cases-of-project-initialization.md`, `research/hub/team-c-governance-strategy-audit-2026-05.md`, `standards/glossary.md` |
| `/research/hub/user-prompts-analysis-2026-05.md` | исследование | — | Анализ 18 пользовательских промптов по стандарту классификации: матрица, оценка актуальности, дубли, рекомендации и план интеграции с `projects/mango/prompts/`. Scope: user-specific + repo-integration. | ⚠️ По необходимости | `research/hub/prompts-classification-standard-2026-05.md`, `projects/mango/prompts/`, `projects/mango/experiments/prompts-audit-2026-05-26.md` |
| `/research/governance/README.md` | навигация | — | Индекс исследований governance-форматов: формат research-документации, формат исполнимых контрактов, формат документации контрактов и решения по структуре каталога governance (Q1/Q2/Q3). Scope: repo-wide. | ✅ Да | `research/README.md`, `standards/research-documentation-standard.md`, `standards/executable-contract-standard.md`, `standards/contract-documentation-standard.md` |
| `/research/governance/research-documentation-format-2026-06.md` | исследование | — | Исследование оптимального формата research-документации (Введение → Результаты → Детализация): IMRaD, BLUF, «перевёрнутая пирамида», принцип Минто, RFC 7322, ADR, Diátaxis. Выход — `standards/research-documentation-standard.md`. Scope: repo-wide. | ✅ Да | `standards/research-documentation-standard.md`, `research/governance/README.md` |
| `/research/governance/executable-contract-format-2026-06.md` | исследование | — | Исследование формата исполнимых контрактов (EXECUTION → EXPLANATION, команда первой строкой): системные промпты, инструкции, SRE-runbooks, SYNOPSIS man(7), README Quick Start, Makefile. Выход — `standards/executable-contract-standard.md`. Scope: repo-wide. | ✅ Да | `standards/executable-contract-standard.md`, `governance/rfc/contract-executability-rfc.md`, `research/governance/README.md` |
| `/research/governance/contract-documentation-format-2026-06.md` | исследование | — | Исследование best practices документации контрактов (API-контракты, SLA/SLO, governance): OpenAPI, RFC 2119 / BCP 14, Design by Contract, ADR, Pact. Выход — `standards/contract-documentation-standard.md`. Scope: repo-wide. | ✅ Да | `standards/contract-documentation-standard.md`, `research/governance/README.md` |
| `/research/governance/governance-folder-structure-decisions-2026-06.md` | исследование | — | Решения по спорным вопросам структуры каталога governance: Q1 (`proposals/` → `rfc/`), Q2 (размещение концепции проекта в `research/{project}/`) и Q3 (опциональность `governance/rfc/`) с обоснованием и учётом мнения команды Q. Scope: repo-wide. | ✅ Да | `governance/rfc/README.md`, `standards/portal-repository-structure.md`, `research/governance/README.md` |
| `/research/portal/README.md` | навигация | — | Индекс исследований направления «портал `open-ai.ru`»: 5 исследований (стандарты документации, сравнение подходов к концепции, архитектура и стек, структура репозитория, AI и `mango_ba_prompts`), политики и связанные артефакты. Scope: portal. | ✅ Да | `research/README.md`, `research/portal/open-ai-portal-concept-rfc.md` |
| `/research/portal/documentation-standards-comparison-2026-06.md` | исследование | — | Сравнение стандартов документации (C4, arc42, ADR, RFC, Diátaxis, Concept Doc, IEEE 42010) по 5 критериям; вывод — ядро ADR плюс C4, RFC и frontmatter по наследованию, Diátaxis и arc42-lite по росту. Scope: portal. | ⚠️ По необходимости | `research/portal/open-ai-portal-concept-rfc.md`, `standards/research-profile.md` |
| `/research/portal/concept-standards-comparison-2026-06.md` | исследование | — | Сравнение 8 подходов к стандартизации структуры концепции (ISO/IEC/IEEE 42010, TOGAF, BABOK, Continuous Discovery, PRD, RFC, Concept Doc, Vision Document) по 7 критериям; вывод — гибрид «PRD-ядро плюс Vision-слой плюс TOGAF-модульность». Выход — `standards/webportal-concept-standard.md`. Scope: portal. | ⚠️ По необходимости | `standards/webportal-concept-standard.md`, `research/portal/documentation-standards-comparison-2026-06.md`, `standards/research-profile.md` |
| `/research/portal/architecture-and-stack-comparison-2026-06.md` | исследование | — | Независимое сравнение архитектур и стеков портала: рендеринг (SSG плюс islands), структура (модульный монолит), хостинг (Cloudflare Pages); 12-критериальная матрица frontend (Astro, Next, Angular, Docusaurus). Scope: portal. | ⚠️ По необходимости | `research/portal/open-ai-portal-concept-rfc.md`, `research/portal/ai-and-mango-integration-patterns-2026-06.md` |
| `/research/portal/repository-structure-design-2026-06.md` | исследование | — | Дизайн структуры репозитория портала: анализ Хаба, требования портала, 3 альтернативы размещения; вывод — спок плюс стандарт-расширение. Выход — `standards/portal-repository-structure.md`. Scope: portal. | ⚠️ По необходимости | `standards/portal-repository-structure.md`, `projects/README.md`, `templates/spoke/README.md` |
| `/research/portal/ai-and-mango-integration-patterns-2026-06.md` | исследование | — | Паттерны AI-интеграции (Yandex GPT через serverless-proxy), подключения `mango_ba_prompts` (санитизированные шаблоны для Phase 1), auth и маскирования данных по фазам; карта рисков приватности. Scope: portal. | ⚠️ По необходимости | `research/portal/architecture-and-stack-comparison-2026-06.md`, `projects/mango/README.md`, `research/portal/open-ai-portal-concept-rfc.md` |
| `/research/portal/open-ai-portal-concept-rfc.md` | RFC | справка | RFC концепции портала `open-ai.ru` («универсальный инструмент коммуникации»): синтез независимых исследований (документация, архитектура и стек, структура, AI и `mango_ba_prompts`), 5 слоганов, сравнение 4 вариантов по 14 критериям, оптимальное решение, roadmap Phase 0–4, структура репозитория, план миграции и запрос на согласование с 7 вопросами. Решение за человеком. | ⚠️ По необходимости | `standards/portal-repository-structure.md`, `research/portal/README.md`, `projects/README.md`, `AI_GOVERNANCE.md` |
| `/standards/` | каталог | — | Плоский реестр стандартов, шаблонов и правил оформления артефактов. | ✅ Да | `standards/README.md`, `governance/REPO_MODEL.md` |
| `/governance/` | каталог | — | Модель репозитория, навигация и сквозные governance-правила. | ✅ Да | `governance/REPO_MODEL.md`, `governance/ARTIFACT_MAP.md` |
| `/tools/` | каталог | — | Локальные validation и maintenance скрипты. | ✅ Да | `tools/validate-frontmatter.sh`, `tools/validate-repository-structure.sh` |
| `/governance/rfc/` | каталог | — | RFC и предложения по governance до принятия решения человеком. | ⚠️ По необходимости | `governance/REPO_MODEL.md`, `AI_GOVERNANCE.md` |
| `/research/` | каталог | — | Доменные исследования и source-backed analysis; содержит активную Mango taxonomy-концепцию, классификацию промптов и сохраненные `-old` исторические входы. | ✅ Да | `standards/research-profile.md`, `governance/REPO_MODEL.md` |
| `/frameworks/` | каталог | — | Методологии, создаваемые только после доказанного gap (сейчас — `-old` входы). | ✅ Да | `governance/REPO_MODEL.md`, `standards/README.md` |
| `/projects/` | каталог | — | Project knowledge bases и контекст spoke-репозиториев; Mango вынесен в `mango_ba_prompts`, архивная копия хранится в `archive/projects/mango/`. | ✅ Да | `standards/product-profile.md`, `governance/REPO_MODEL.md`, `projects/README.md` |
| `/education/` | каталог | — | Open education: программы и учебные материалы (сейчас — `-old` входы). | ✅ Да | `standards/education-profile.md`, `governance/REPO_MODEL.md` |
| `/projects/README.md` | навигация | — | Правило выбора `/projects` vs spoke-репозиторий, список активных project areas и реестр мигрировавших проектов. | ✅ Да | `standards/product-profile.md`, `governance/REPO_MODEL.md`, `mango_ba_prompts`, `archive/projects/mango/` |
| `https://github.com/G-Ivan-A/mango_ba_prompts` | каталог | — | Внешний spoke-репозиторий Mango: рабочие prompt assets, эксперименты, `standards/GLOSSARY.md` и migration manifest. | ⚠️ По необходимости | `projects/README.md`, `research/mango/README.md`, `archive/projects/mango/` |
| `/archive/projects/mango/README.md` | навигация | — | Архивная версия Hub-каталога Mango после миграции в `mango_ba_prompts`; только для истории, не для разработки. | ✅ Да | `projects/README.md`, `research/mango/README.md`, `mango_ba_prompts` |
| `/archive/projects/mango/standards/classification-glossary.md` | стандарт | — | Архивный Mango-only глоссарий уровней Domain, Capability, Feature и Atomic Function; рабочая версия перенесена в `mango_ba_prompts/standards/GLOSSARY.md`. | ✅ Да | `archive/projects/mango/README.md`, `research/mango/classification.md`, `research/mango/taxonomy-concept-2026-05.md`, `mango_ba_prompts/standards/GLOSSARY.md` |
| `/archive/projects/mango/experiments/prompts-audit-2026-05-26.md` | исследование | — | Архивная копия аудита экспериментальных Mango prompt-прототипов; рабочая копия перенесена в `mango_ba_prompts/prompts/experiments/`. | ✅ Да | `archive/projects/mango/experiments/tz-stats-prototype-2026-05.md`, `archive/projects/mango/experiments/user-story_gen-from-raw-request_2026-05-26.md`, `archive/projects/mango/experiments/usecase_gen-stepwise-alignment_2026-05-26.md`, `mango_ba_prompts/prompts/` |
| `/archive/projects/mango/experiments/prompts-selftest-2026-05-26.md` | исследование | — | Архивная копия dry-run шести Mango prompt assets; рабочая копия перенесена в `mango_ba_prompts/prompts/experiments/`. | ✅ Да | `mango_ba_prompts/prompts/`, `archive/projects/mango/experiments/prompts-audit-2026-05-26.md` |
| `/archive/projects/mango/prompts/tz-stats-generator_exp-2026-05.md` | шаблон | — | Архивная копия RAG-enabled prompt для генерации статистики по ТЗ; рабочая версия: `mango_ba_prompts/prompts/tz-stats-generator.md`. | ✅ Да | `archive/projects/mango/experiments/tz-stats-prototype-2026-05.md`, `research/mango/classification.md`, `mango_ba_prompts/prompts/tz-stats-generator.md` |
| `/archive/projects/mango/prompts/tz-stats-generator_simple-2026-05.md` | шаблон | — | Архивная копия standalone prompt для генерации статистики по ТЗ; рабочая версия: `mango_ba_prompts/prompts/tz-stats-generator-simple.md`. | ✅ Да | `archive/projects/mango/experiments/tz-stats-prototype-2026-05.md`, `mango_ba_prompts/prompts/tz-stats-generator-simple.md` |
| `/archive/projects/mango/prompts/user-story-generator_exp-2026-05.md` | шаблон | — | Архивная копия RAG-enabled prompt для генерации User Story; рабочая версия: `mango_ba_prompts/prompts/user-story-generator.md`. | ✅ Да | `archive/projects/mango/experiments/user-story_gen-from-raw-request_2026-05-26.md`, `research/mango/classification.md`, `mango_ba_prompts/standards/GLOSSARY.md` |
| `/archive/projects/mango/prompts/user-story-generator_simple-2026-05.md` | шаблон | — | Архивная копия standalone prompt для генерации User Story; рабочая версия: `mango_ba_prompts/prompts/user-story-generator-simple.md`. | ✅ Да | `archive/projects/mango/experiments/user-story_gen-from-raw-request_2026-05-26.md`, `mango_ba_prompts/prompts/user-story-generator-simple.md` |
| `/archive/projects/mango/prompts/usecase-stepwise-generator_exp-2026-05.md` | шаблон | — | Архивная копия RAG-enabled prompt для пошаговой генерации Use Case; рабочая версия: `mango_ba_prompts/prompts/usecase-stepwise-generator.md`. | ✅ Да | `archive/projects/mango/experiments/usecase_gen-stepwise-alignment_2026-05-26.md`, `research/mango/classification.md`, `mango_ba_prompts/prompts/usecase-stepwise-generator.md` |
| `/archive/projects/mango/prompts/usecase-stepwise-generator_simple-2026-05.md` | шаблон | — | Архивная копия standalone prompt для пошаговой генерации Use Case; рабочая версия: `mango_ba_prompts/prompts/usecase-stepwise-generator-simple.md`. | ✅ Да | `archive/projects/mango/experiments/usecase_gen-stepwise-alignment_2026-05-26.md`, `mango_ba_prompts/prompts/usecase-stepwise-generator-simple.md` |
| `/projects/repo-development/README.md` | навигация | — | Развитие структуры, governance и локальных проверок самого репозитория. | ✅ Да | `projects/README.md`, `governance/REPO_MODEL.md` |
| `/projects/repo-development/docs/migration-audit-2026-05.md` | исследование | — | Аудит миграции: согласованность, ссылки, таблица `-old` и рекомендации cleanup. | ✅ Да | `projects/repo-development/README.md`, `CONCEPT.md` |
| `/projects/repo-development/docs/contract-violations-self-report-2026-06.md` | исследование | — | Операционный self-report (`type: audit`) шести ошибок исполнения контрактов в сессии миграции Mango: обоснование выбора таргета, реестр нарушений, системные выводы для контрактов и анализ размещения существующих ретроспектив (без перемещения). | ⚠️ По необходимости | `projects/repo-development/README.md`, `standards/project-structure-inheritance.md`, `standards/file-naming.md`, `research/hub/ai-collaboration-retrospective-mango-migration-2026-06.md` |
| `/research/README.md` | навигация | — | Навигация по исследовательским направлениям, правило запрета файлов в корне `research/` и правила воспроизводимости. | ✅ Да | `standards/research-profile.md`, `governance/REPO_MODEL.md` |
| `/research/hub/README.md` | навигация | — | Индекс фундаментальных (`scope: repo-wide`) исследований работы Хаба. | ✅ Да | `research/README.md`, `governance/REPO_MODEL.md` |
| `/research/mango/README.md` | навигация | — | Индекс активных исследований MANGO OFFICE и их HTML-export. | ✅ Да | `research/README.md`, `mango_ba_prompts` |
| `/research/mango/classification.md` | исследование | — | Классификация IT/Telecom SaaS-продуктов MANGO OFFICE. | ✅ Да | `research/mango/README.md`, `standards/research-profile.md` |
| `/research/mango/classification-tz.md` | исследование | — | Проверка классификатора на корпусе тендерных ТЗ и рекомендации по дополнениям. | ✅ Да | `research/mango/classification.md`, `research/mango/README.md` |
| `/research/mango/requirements-flow.md` | исследование | — | Flow требований для AI-анализа тендерных ТЗ MANGO OFFICE. | ✅ Да | `research/mango/classification.md`, `mango_ba_prompts` |
| `/research/mango/rag-mapping-roadmap-2026-05.md` | исследование | — | RAG-навигатор продуктов/фич, roadmap автоматизации БА и карта применения диаграмм для Mango. | ⚠️ По необходимости | `research/mango/taxonomy-concept-2026-05.md`, `research/mango/requirements-lifecycle-uncertainty-2026-05.md`, `mango_ba_prompts` |
| `/research/mango/classification.html` | исследование | — | HTML-export классификации MANGO OFFICE. | ✅ Да | `research/mango/classification.md` |
| `/research/mango/classification-tz.html` | исследование | — | HTML-export проверки классификатора на корпусе ТЗ. | ✅ Да | `research/mango/classification-tz.md` |
| `/research/mango/requirements-flow.html` | исследование | — | HTML-export flow требований. | ✅ Да | `research/mango/requirements-flow.md` |
| `/education/README.md` | навигация | — | Граница open education и ссылка на профиль образовательных пакетов. | ✅ Да | `standards/education-profile.md`, `governance/REPO_MODEL.md` |
| `/frameworks/README.md` | навигация | — | Правила создания фреймворков и будущая структура framework artifacts. | ✅ Да | `governance/REPO_MODEL.md`, `standards/README.md` |
| `/standards/` | каталог | — | Плоский реестр стандартов, шаблонов и правил оформления артефактов. | ✅ Да | `standards/README.md`, `governance/REPO_MODEL.md` |
| `/governance/` | каталог | — | Модель репозитория, навигация и сквозные governance-правила. | ✅ Да | `governance/REPO_MODEL.md`, `governance/ARTIFACT_MAP.md` |
| `/tools/` | каталог | — | Локальные validation и maintenance скрипты. | ✅ Да | `tools/validate-frontmatter.sh`, `tools/validate-repository-structure.sh` |
| `/research/` | каталог | — | Доменные исследования и source-backed analysis; файлы размещаются только в тематических подкаталогах (`hub/`, `mango/`, `portal/`), корень содержит лишь `README.md`. | ✅ Да | `research/README.md`, `standards/research-profile.md`, `governance/REPO_MODEL.md` |
| `/research/hub/` | каталог | — | Фундаментальные исследования работы Хаба (`scope: repo-wide`): bootstrap, governance-стратегия, классификация промптов. | ✅ Да | `research/hub/README.md`, `standards/research-profile.md`, `governance/REPO_MODEL.md` |
| `/research/mango/` | каталог | — | Доменные исследования MANGO OFFICE (`scope: mango-only`). | ✅ Да | `research/mango/README.md`, `standards/research-profile.md`, `governance/REPO_MODEL.md` |
| `/research/portal/` | каталог | — | Исследования направления «портал `open-ai.ru`» (`scope: portal`): документация, архитектура и стек, структура репозитория, AI и `mango_ba_prompts`. | ✅ Да | `research/portal/README.md`, `standards/research-profile.md`, `governance/REPO_MODEL.md` |
| `/research/governance/` | каталог | — | Исследования governance-форматов Хаба (`scope: repo-wide`): формат research-документации, формат исполнимых контрактов, формат документации контрактов и решения по структуре каталога governance (Q1/Q2/Q3). | ✅ Да | `research/governance/README.md`, `standards/research-profile.md`, `governance/REPO_MODEL.md` |
| `/frameworks/` | каталог | — | Методологии, создаваемые только после доказанного gap; сейчас содержит active navigation. | ✅ Да | `frameworks/README.md`, `governance/REPO_MODEL.md`, `standards/README.md` |
| `/projects/` | каталог | — | Project knowledge bases и контекст spoke-репозиториев; сейчас содержит активные project areas и реестр мигрировавших проектов. | ✅ Да | `projects/README.md`, `standards/product-profile.md`, `governance/REPO_MODEL.md`, `mango_ba_prompts` |
| `/archive/projects/mango/` | каталог | — | Архивная копия бывшего Hub-каталога Mango после миграции в `mango_ba_prompts`; только для истории, не для разработки. | ✅ Да | `projects/README.md`, `governance/ARTIFACT_MAP.md`, `mango_ba_prompts` |
| `/education/` | каталог | — | Open education: программы и учебные материалы; сейчас содержит active navigation. | ✅ Да | `education/README.md`, `standards/education-profile.md`, `governance/REPO_MODEL.md` |
| `/.github/ISSUE_TEMPLATE/` | каталог | — | GitHub-native структура постановки задач. | ✅ Да | `.github/ISSUE_TEMPLATE/task.yml` |
| `/templates/` | каталог | — | Образцы («ДНК-шаблоны») для клонирования новых проектов из Хаба. | ⚠️ По необходимости | `templates/spoke/AI_GOVERNANCE.md`, `governance/rfc/rfc-creative-template-design.md` |
| `/templates/spoke/` | каталог | — | Минимальный геном spoke-проекта: базовые артефакты, шаблон задачи, валидатор и `init.sh`. Без `research/` (фундаментальные знания живут в Хабе). | ⚠️ По необходимости | `templates/spoke/AI_GOVERNANCE.md`, `templates/spoke/init.sh`, `governance/REPO_MODEL.md` |

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
Cleanup issue #49 удалил или перенес tracked files с суффиксом `-old`.
Исторический контекст предыдущей структуры зафиксирован в
[projects/repo-development/docs/migration-audit-2026-05.md](../projects/repo-development/docs/migration-audit-2026-05.md)
и PR history. Новые `-old` files не добавляются без отдельного migration issue
и явного rationale; validator структуры должен ловить такие регрессии.

## Как использовать карту

1. Не знаешь, где что лежит? → открой эту карту и найди артефакт по колонке
   «Путь».
2. Ищешь правило работы или формат? → смотри колонку «Тип»: `правило` и
   `контракт` задают обязательное поведение; `стандарт`, `профиль` и `шаблон`
   задают формат артефактов; `руководство` дает рекомендации.
3. Нужно понять, выполнять документ или читать как справку? → смотри колонку
   «🚦 Исполнимый?».
4. Не уверен, обязателен ли файл? → смотри колонку «Обязательный?».
5. Нужно понять связи? → смотри колонку «Связанные артефакты».
6. Термин непонятен? → сверься со [standards/glossary.md](../standards/glossary.md).

## Как обновлять карту

- При создании нового активного артефакта → добавь строку в таблицу, укажи
  тип, обязательность и связи, и зарегистрируй файл в
  [tools/validate-repository-structure.sh](../tools/validate-repository-structure.sh)
  (`is_active_file` и, если файл обязателен, `required_files`).
- При удалении артефакта → удали строку или пометь как `❌ Удалён` и обнови
  валидатор структуры.
- При изменении назначения → обнови колонки «Назначение», «🚦 Исполнимый?» и
  «Связанные артефакты».
- При переносе historical material → добавь новый активный артефакт в карту и
  сошлись на source path во frontmatter или pull request.
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
| [standards/glossary.md](../standards/glossary.md) | Canonical источник терминов для колонки «Тип». |
| [governance/rfc/contract-executability-rfc.md](rfc/contract-executability-rfc.md) | Утверждённый источник стандарта `executable: true\|false`, директивных блоков и колонки «🚦 Исполнимый?». |
