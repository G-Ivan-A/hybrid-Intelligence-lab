# Changelog

All notable repository governance changes are documented here.

## Unreleased

### Added

- Issue #133: созданы отдельные GitHub Issues CE-001..CE-010
  ([#138](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/138)–[#147](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/147))
  для каждого файла из плана внедрения стандарта исполнимых документов
  `governance/proposals/contract-executability-rfc.md` §6.1. В
  `governance/BACKLOG.md` добавлен отдельный backlog-раздел с приоритетами,
  зависимостями и ссылками на issues; создан реестр
  `governance/EXECUTABLE_DOCUMENTS_ISSUES.md`; реестр зарегистрирован в
  `governance/ARTIFACT_MAP.md` и структурном валидаторе. Физический рефакторинг
  файлов из RFC §6.1 не выполнялся.

- Issue #124: новый research-артефакт
  `research/hub/ai-collaboration-retrospective-mango-migration-2026-06.md` —
  ретроспектива ошибок AI-агента в сессии проектирования миграции Mango
  (Хаб → спок): реестр из 5 ошибок (режимы, pre-flight контекст, Anti-Inflation,
  формат issue, архитектурное размещение артефактов), их корневые причины и
  4 системных вывода для будущего onboarding/governance proposal (режим
  `Research`, governance-файлы не меняются). Имя файла осознанно отличается от
  запрошенного в issue `ai-collaboration-retrospective-2026-06.md`: тот файл уже
  существует в `main` и описывает другую сессию (проектирование шаблонов споков,
  #95) — перезапись уничтожила бы прежний артефакт. Новые термины «Ретроспектива»
  и «Корневая причина» добавлены в `standards/GLOSSARY.md` (версия 1.0 → 1.1) как
  единый источник определений. Артефакт зарегистрирован как active в
  `tools/validate-repository-structure.sh` (`is_active_file`) и в навигации
  `research/hub/README.md`. Удалён сгенерированный харнессом корневой `.gitkeep`
  (его нет в `main`), снимавший FAIL структурного валидатора.
- Issue #113 (B-007): в шаблон генома спока `templates/spoke/AI_GOVERNANCE.md`
  добавлена секция «Границы действий» — простая capability taxonomy из трёх
  корзин разрешений **прозой** («можно без спроса / можно с апрувом / нельзя
  никогда») с 1–2 примерами на корзину. Сознательно без YAML-машинерии и
  таблиц: формальный Capability Manifest (YAML) `ОТЛОЖЕН` до первого инцидента
  (решение Конарда, упрощающее «ментальный список» команды Q сильнее; источники
  — Q «взять сейчас», команда С `[C5]`, внешний паттерн `[GAP]`). Секция даёт
  агенту ясные границы между корзинами «Правила» и «Эскалация» без новой
  структуры (Anti-Inflation).
- Issue #115 (B-005): шаблон `templates/spoke/README.md` (точка входа **Кейса 2**,
  *Bootstrap-клонирование*) дополнен разделами «🛠️ Как адаптировать
  `{{...}}`-плейсхолдеры» (таблица плейсхолдеров, запуск `init.sh`, ручная правка,
  пояснение про `{{REPO_NAME}}`) и «✅ Как валидировать структуру» (запуск
  `./tools/validate-repository-structure.sh` перед PR). Замкнуты перекрёстные
  ссылки между двумя точками входа (follow-up #4, #5 RFC-манифеста двух кейсов):
  спок-README → Хаб `governance/AGENT_ONBOARDING.md` (Кейс 1),
  `rfc-two-cases-of-project-initialization.md` и `rfc-creative-template-design.md`
  через `{{hub_url}}`; обратная ссылка (онбординг → спок-README) уже существовала.
  Структурный валидатор расширен проверками контента спок-README
  (`tools/validate-repository-structure.sh`: ссылка на `governance/AGENT_ONBOARDING.md`
  и наличие раздела валидации). Удалён сгенерированный харнессом корневой
  `.gitkeep` (его нет в `main`), снимавший FAIL структурного валидатора.

- Issue #114 (B-003): новый артефакт генома спока
  `templates/spoke/AI_HANDOVER_PROMPT.md` — копия *Handover Prompt* с
  плейсхолдером `{{REPO_NAME}}` (по умолчанию `hybrid-Intelligence-lab`), готовая
  «доверенность» для запуска агента (*Runtime-онбординг*) прямо из склонированного
  спока. Источник истины зафиксирован за Хабом
  ([`governance/AGENT_ONBOARDING.md`](governance/AGENT_ONBOARDING.md), создаётся в
  B-001 → #109): файл явно помечен как копия шаблона со ссылкой на хабовый
  оригинал, чтобы избежать рассинхронизации. Файл зарегистрирован как active в
  обоих валидаторах (`tools/validate-repository-structure.sh` — `is_active_file`,
  `required_files` и проверки контента; `templates/spoke/tools/validate-repository-structure.sh`
  — `required_files` и проверка сохранности `{{REPO_NAME}}`) и в
  `governance/ARTIFACT_MAP.md` (тип `шаблон`, версия карты 1.9 → 1.10).
  Перекрёстные ссылки добавлены в `templates/spoke/README.md`; шаблонный
  `templates/spoke/CHANGELOG.md` упоминает *Handover Prompt* в составе генома.
  Удалён сгенерированный харнессом корневой `.gitkeep` (его нет в `main`),
  снимавший FAIL структурного валидатора.

### Changed

- Issue #111 (B-004): в канон `governance/REPO_MODEL.md` добавлен раздел
  «Spoke Lifecycle: два кейса инициализации», фиксирующий разделение
  *Runtime-онбординг* (Кейс 1) ⟂ *Bootstrap-клонирование* (Кейс 2) как часть
  модели жизненного цикла spoke. Operating Mode привязан к кейсу (Кейс 1 →
  `Structured`, Кейс 2 → `Project`). Раздел сознательно краткий: определения
  терминов вынесены в `standards/GLOSSARY.md`, полное обоснование с аналогиями и
  Mermaid-схемой — в RFC-манифесте
  `governance/proposals/rfc-two-cases-of-project-initialization.md`; канон
  ссылается на источники, а не дублирует их (Anti-Inflation). Снят риск
  повторения терминологической путаницы (ошибка №5 ретроспективы). Удалён
  сгенерированный харнессом корневой `.gitkeep`, снимавший FAIL структурного
  валидатора.

- Issue #110 (B-002): связаны входные точки репозитория с онбордингом. В
  `README.md` добавлены предполётный блок «🛫 Новый агент? Начни здесь →
  `governance/AGENT_ONBOARDING.md`» и строка в таблице «Ключевые документы»; в
  `AI_GOVERNANCE.md` онбординг закреплён как обязательный pre-flight шаг (нота в
  шапке + ссылка в правиле 2 «читай до изменения файлов»). Это ссылки, а не
  копии протокола (Anti-Inflation, риск дублирования снят). Навигационные связи
  зафиксированы в валидаторе (`require_text` на `governance/AGENT_ONBOARDING.md`
  в `README.md` и `AI_GOVERNANCE.md`) и в `governance/ARTIFACT_MAP.md` (связи у
  строк `README.md`, `AI_GOVERNANCE.md` и `AGENT_ONBOARDING.md`; версия карты
  1.10 → 1.11). Замыкает Кейс 1: артефакт B-001 (#109) теперь виден из двух
  очевидных точек входа.
- Issue #116 (B-011): в RFC-манифест
  `governance/proposals/rfc-two-cases-of-project-initialization.md` добавлен
  раздел «Evidence trail: git history + issues + PRs как след доказательств»,
  явно называющий уже работающую способность (тезис команды С `[C5]`, метка
  «взять сейчас» из матрицы применимости) и связывающий её ссылкой с
  `research/hub/external-governance-patterns-review-2026-06.md` (разделы 1.3 и
  3.1). Имя evidence trail закреплено рядом с моделью жизненного цикла; новый
  формат/обёртка сознательно не вводятся (Anti-Inflation). Версия RFC `0.1 → 0.2`,
  во frontmatter добавлены external-review в `related_artifacts` и #116 в
  `related_issues`. Статус B-011 в `governance/BACKLOG.md`: `ЧАСТИЧНО → DONE`.
  Удалён сгенерированный харнессом корневой `.gitkeep`, снимавший FAIL
  структурного валидатора.

- Issue #107 (B-013): `governance/BACKLOG.md` промоутнут из `draft` в `canonical`
  (`version 0.1 → 1.0`) по команде Human Review. Замкнут маршрут «бэклог →
  issues»: по всем открытым задачам бэклога заведены отдельные issues со ссылкой
  на строку-источник — B-001 → #109, B-002 → #110, B-004 → #111, B-006 → #112,
  B-007 → #113, B-003 → #114, B-005 → #115, B-011 → #116. Задача B-014 (P3)
  намеренно отложена и не заведена; задачи `DONE` (B-010 → #105, B-008 → #91) уже
  имеют issues. В бэклог добавлена колонка «Issue» в сводной таблице, маппинг в
  разделе 3 (B-013), обновлены `related_issues` во frontmatter и разделы 6/8.
  Удалён сгенерированный харнессом корневой `.gitkeep` (его нет в `main`),
  снимавший FAIL структурного валидатора.

### Added

- Issue #109 (B-001): рабочая инструкция `governance/AGENT_ONBOARDING.md`
  (`status: canonical`, тип `правило`) — единый входной артефакт *Runtime-онбординга*
  (Кейс 1) по дизайну `proposals/rfc-agent-onboarding-protocol.md`. Содержит:
  *Handover Prompt* с плейсхолдером `{{REPO_NAME}}`, 4-шаговый протокол агента
  (чек-лист governance → чек-лист контекста → *Readback* → стоп до апрува), шаблон
  *Readback* и раздел threat awareness «Что может пойти не так» (5 рисков холодного
  старта) — реализация рекомендации команды Q без отдельного файла (Anti-Inflation).
  Все термины — со ссылкой на `standards/GLOSSARY.md`; добавлены перекрёстные ссылки
  на `templates/spoke/README.md` (Кейс 2) и на RFC-манифест двух кейсов. Граница с
  RFC явная: RFC остаётся *проектом* (`proposals/`), а `AGENT_ONBOARDING.md` —
  *рабочей инструкцией*. Файл зарегистрирован как active в
  `tools/validate-repository-structure.sh` (`is_active_file`, `required_files` и
  набор `require_text`) и `governance/ARTIFACT_MAP.md` (версия карты 1.9 → 1.10).
- Issue #99: RFC-манифест `governance/proposals/rfc-two-cases-of-project-initialization.md`
  — концептуальное разделение двух ортогональных кейсов инициализации проекта:
  Кейс 1 (Runtime-онбординг) и Кейс 2 (Bootstrap-клонирование). Ведущая аналогия
  «сертификация самолёта ≠ лицензия пилота» + анализ ещё трёх смежных областей
  (медицина, юриспруденция, DevOps) с выводами для модели; таблица-манифест из 13
  строк; Mermaid-схема жизненного цикла проекта с явным разделением кейсов;
  обоснование с трассировкой к `research/hub/ai-collaboration-retrospective-2026-06.md`;
  фиксация будущих README по каждому кейсу и follow-up-список. Манифест
  намеренно не определяет термины — только использует их со ссылкой на глоссарий.
  Файл зарегистрирован как active в `tools/validate-repository-structure.sh` и
  `governance/ARTIFACT_MAP.md` (тип `RFC`, версия карты 1.6 → 1.7).

### Changed

- Issue #99: уточнён `governance/proposals/rfc-agent-onboarding-protocol.md` —
  добавлен раздел «Модель процесса» (без блока терминологии, только ссылки на
  `standards/GLOSSARY.md` и на RFC-манифест), фиксирующий, что агент работает в
  *Среде работы агента* (чат) и обращается к *Источнику контекста* (репозиторий);
  *Handover Prompt* параметризован плейсхолдером `{{REPO_NAME}}` и
  переформулирован без ложной модели «агент в репозитории».
- Issue #99: в `standards/GLOSSARY.md` добавлены 6 терминов (Bootstrap-клонирование,
  Runtime-онбординг, Handover Prompt, Readback, Среда работы агента, Источник
  контекста) со ссылками на вводящие их RFC, плюс две строки связей терминов.


  — «Протокол бесшовной передачи проекта» (Seamless Project Handover Protocol)
  против ошибок холодного старта. Аналогия предполётного чек-листа и «читки
  обратно» (readback); обоснование с дословной трассировкой к 5 провалам
  ретроспективы `research/hub/project-context-and-bootstrap-patterns-2026-05.md`
  и аудиту команды C; готовый к копированию Handover Prompt для пользователя;
  4-шаговый алгоритм агента (чек-лист governance → чек-лист контекста → readback
  → стоп до апрува); Mermaid-схема потока инициализации и сравнение мест для
  будущего `AGENT_ONBOARDING.md` (рекомендация — `governance/`). RFC намеренно не
  создаёт `AGENT_ONBOARDING.md` и завершается блоком «Решение за человеком».
  Файл зарегистрирован как active в `tools/validate-repository-structure.sh` и
  `governance/ARTIFACT_MAP.md` (тип `RFC`, версия карты 1.5 → 1.6).
- Issue #93: «ДНК-шаблон» `templates/spoke/` — минимальный геном для клонирования
  новых spoke-проектов из Хаба. Девять базовых артефактов: `AI_GOVERNANCE.md`
  (конституция спока со ссылкой на Хаб), `AI_QUICK_RULES.md` (инструкция по
  выживанию агента), `README.md`, `CONTRIBUTING.md` (issue → PR → review),
  `CHANGELOG.md` (каркас с `## Unreleased`), `docs/adr/.gitkeep`,
  `docs/audit/.gitkeep`, `.github/ISSUE_TEMPLATE/task.md` (наследует поля Хаба
  из `standards/ISSUE_WORKFLOW.md`) и исполняемый `tools/validate-repository-structure.sh`
  (минимальный валидатор с предупреждением о `research/`). Шаблон по умолчанию
  не содержит `research/`: фундаментальные знания остаются в Хабе. Креативное
  улучшение UX инициализации — исполняемый `templates/spoke/init.sh`:
  интерактивная/CLI-замена плейсхолдеров (`{{project_name}}`,
  `{{project_description}}`, `{{hub_url}}`), автоген `{{date}}` (`updated:` во
  frontmatter), портабельный `sed` (без `sed -i`) и самоудаление после запуска.
  Артефакты зарегистрированы как active в `tools/validate-repository-structure.sh`
  и `governance/ARTIFACT_MAP.md` (тип `шаблон`, версия карты 1.4 → 1.5).
- Issue #89: креативный RFC `governance/proposals/rfc-creative-template-design.md`
  — проект "ДНК-шаблона" для клонирования spoke-проектов: концептуальная аналогия
  (геном, а не чемодан), сравнительная матрица имён корневого каталога
  (`templates`/`blueprints`/`genesis`), минимальная карта файлов с креативными
  комментариями, три антипаттерна, обработка краевых случаев ("А что, если...") и
  Mermaid-схема процесса клонирования. RFC соблюдает запрет на создание `research/`
  в споках по умолчанию (`docs/adr/`, `docs/audit/` только) и завершается блоком
  "Решение за человеком". Создан каталог `governance/proposals/`. Файл
  зарегистрирован как active в `tools/validate-repository-structure.sh` и
  `governance/ARTIFACT_MAP.md`.
- Issue #81: исследование `research/project-context-and-bootstrap-patterns-2026-05.md`
  с минималистичными паттернами передачи контекста между чатами, предсказуемого
  создания project areas и маршрута "рекомендация -> задача" на опыте Mango.
  Файл зарегистрирован как active в `tools/validate-repository-structure.sh`,
  `governance/ARTIFACT_MAP.md` и `research/README.md`.
- Issue #79: исследование `research/prompts-classification-audit-2026-05.md`
  (аудит входных данных: инвентаризация 6 Mango промптов, паттерны отладки,
  пробелы классификации) и `research/prompts-classification-standard-2026-05.md`
  (стандарт классификации промптов: таксономия из 6 осей, матрица «тип × зрелость
  × сценарий» с 10 ячейками, 3 шаблона для отладки формата (Simple/System/Agent),
  план интеграции к Mango промптам и вопросы для согласования). Scope: repo-wide.
  Файлы зарегистрированы как active в `tools/validate-repository-structure.sh`,
  `governance/ARTIFACT_MAP.md` и `research/README.md`.
- Issue #77: аудит `projects/mango/experiments/prompts-audit-2026-05-26.md`,
  self-test `projects/mango/experiments/prompts-selftest-2026-05-26.md` и
  шесть готовых Mango prompt assets в `projects/mango/prompts/`: TZ Stats,
  User Story и Use Case в вариантах `_exp` и `_simple`. Prompt assets
  зарегистрированы в `tools/validate-repository-structure.sh`,
  `projects/mango/README.md` и `governance/ARTIFACT_MAP.md`.
- Issue #69: справочник `research/mango/capability-decomposition-2026-05.md`
  (`status: draft`, `scope: mango-only`) — детализация уровня `Atomic Function`
  для трёх пилотных доменов (`voice-ucaas`, `contact-center`,
  `digital-channels`): 54 функции с параметрами, ≥2 международными источниками
  и примерами требований из реальных ТЗ, критерии атомарности, модель связи с
  НФТ-классами, интеграция с `kb/product-matrix.md` и процесс обновления.
  Файл зарегистрирован как active в `tools/validate-repository-structure.sh`,
  `governance/ARTIFACT_MAP.md` и `research/mango/README.md`.
- Issue #75: эксперимент `projects/mango/experiments/usecase_gen-stepwise-alignment_2026-05-26.md`
  и промпт `projects/mango/prompts/usecase-stepwise-generator_exp-2026-05.md`
  для пошаговой генерации Use Case с согласованием акторов, компонентов,
  controlled output, логами и тестами на 4 кейсах.
- Issue #67: четырёхуровневая иерархия `Domain → Capability → Feature →
  Atomic Function` в `research/mango/classification.md` (v3.0): семь доменов
  пилота, явные слои `📊 Product Layer` и `🛒 Commercial Layer` со связью через
  `related_commercial_fields`, пять новых `Capability` (R2.1–R2.5) и раздел
  `🚀 Возможные улучшения (не активны в v3.0)` с отложенными атрибутами
  R2.6–R2.8 (обоснование и критерии активации).
- Issue #65: Mango-only `projects/mango/standards/classification-glossary.md`
  with the Domain -> Capability -> Feature -> Atomic Function hierarchy,
  source-backed definitions, Mango examples, mapping table and terms requiring
  clarification.
- Issue #59: каркас подкаталогов `projects/mango/` (`kb/`, `prompts/`, `docs/`,
  `experiments/`, `decisions/`) как точки расширения для будущей документации
  промптов и базы знаний. Пустые папки отслеживаются в Git через `.gitkeep` и
  зарегистрированы как active в `tools/validate-repository-structure.sh`.

### Changed

- Issue #91: рефакторинг структуры `research/` (namespacing). Фундаментальные
  (`scope: repo-wide`) исследования перенесены через `git mv` из корня в новый
  подкаталог `research/hub/` (`project-context-and-bootstrap-patterns-2026-05.md`,
  `prompts-classification-audit-2026-05.md`,
  `prompts-classification-standard-2026-05.md`,
  `team-c-governance-strategy-audit-2026-05.md`,
  `user-prompts-analysis-2026-05.md`); добавлен `research/hub/README.md`.
  `research/README.md` получил строгое правило о запрете файлов в корне
  `research/` и актуализированное оглавление; пути обновлены в
  `governance/ARTIFACT_MAP.md` (v1.4). Валидатор структуры теперь требует
  подкаталоги `research/hub` и `research/mango` и запрещает любые файлы в корне
  `research/`, кроме `README.md`.
- Issue #77: прототипные `_exp` prompt-файлы для User Story и Use Case
  заменены короткими copy-paste промптами; валидатор структуры теперь проверяет
  наличие ровно 6 файлов в `projects/mango/prompts/` и лимиты длины prompt body
  для `_exp` / `_simple`.
- Issue #67: `research/mango/classification.md` обновлён с версии 2 до v3.0
  аддитивно — все 37 существующих строк сохранены и переструктурированы под
  новую модель; сравнительная таблица международной классификации дополнена
  колонками `Domain → Capability (v3.0)` и `BABOK` и строками 38–42; HTML-экспорт
  `research/mango/classification.html` перегенерирован.
- Issue #65: `projects/mango/README.md`, `governance/ARTIFACT_MAP.md` and
  `tools/validate-repository-structure.sh` now register the Mango
  classification glossary as an active project artifact.
- Issue #59: раздел «Шаблон структуры» в `projects/mango/README.md` (v1.1)
  дополнен папкой `decisions/` и пометкой о том, что подкаталоги уже созданы как
  placeholder-точки.

### Removed

- Issue #81: повторно удалён служебный корневой `.gitkeep`, восстановленный при
  создании PR-ветки, чтобы `tools/validate-repository-structure.sh` проходил
  без ошибок.
- Issue #77: удалены root `.gitkeep` из служебного PR-initial commit и
  `projects/mango/prompts/.gitkeep`, потому что `prompts/` теперь содержит
  шесть активных prompt files.
- Issue #69: повторно удалён служебный корневой `.gitkeep`, восстановленный при
  создании PR-ветки, чтобы `tools/validate-repository-structure.sh` проходил без
  ошибок.
- Issue #75: повторно удалён служебный корневой `.gitkeep`, восстановленный при
  создании PR-ветки, чтобы `tools/validate-repository-structure.sh` проходил без
  ошибок.
- Issue #67: повторно удалён служебный корневой `.gitkeep`, восстановленный при
  создании PR-ветки, чтобы `tools/validate-repository-structure.sh` проходил без
  ошибок.
- Issue #59: служебный корневой `.gitkeep`, автогенерированный при создании PR,
  чтобы `tools/validate-repository-structure.sh` снова проходил без ошибок.

## [1.1] - 2026-05-26

### Added

- Issue #52: draft-концепция `research/mango/taxonomy-concept-2026-05.md`
  для Unified Capability Taxonomy Mango: обзор применимых стандартов,
  мета-модель capability, mapping реальных фич, процесс нормализации,
  интерфейс продуктовых команд, метрики, план пилота и риски.
- Issue #49: active directory indexes for `projects/`, `research/`,
  `education/` and `frameworks/` after cleanup of legacy `-old` inputs.
- Issue #49: active Mango research artifacts in `research/mango/`
  (`README.md`, `classification.md`, `classification-tz.md`,
  `requirements-flow.md` and HTML exports) with frontmatter and source
  traceability.
- Issue #47: проект `projects/repo-development/` с навигационным `README.md` и
  отчётом аудита миграции `docs/migration-audit-2026-05.md` (чек-лист
  согласованности с `CONCEPT.md`, матрица перекрёстных ссылок, таблица миграции
  `-old`, ≥5 примеров переноса ценного содержания, ≥3 предложения по улучшениям
  со статусом «На рассмотрении» и рекомендация по удалению `-old` в категориях
  ✅/⚠️/❌). Новые активные файлы зарегистрированы в
  `tools/validate-repository-structure.sh` и связаны из корневого `README.md`.
- Issue #43: `governance/ARTIFACT_MAP.md` — canonical карта артефактов для
  навигации (таблица «Путь | Тип | Назначение | Обязательный? | Связанные
  артефакты», разделы «Как использовать карту» и «Как обновлять карту»).
  Зарегистрирована как active в `tools/validate-repository-structure.sh` и
  связана из `README.md` и `standards/README.md`.
- Canonical file naming standard в `standards/FILE_NAMING.md` для
  исследований, standards, экспериментов, профилей и курсов; зарегистрирован
  в `standards/README.md` и structure validation.
- Canonical education project profile в `standards/EDUCATION_PROFILE.md` для
  структуры курсов, модулей, уроков, упражнений и адаптации под open,
  commercial и internal learning formats.
- Canonical glossary в `standards/GLOSSARY.md` для единых терминов standards,
  governance и AI-assisted work.
- Issue #17 migration structure: `CONCEPT.md`, обновленные root governance
  files, `standards/README.md`, `governance/REPO_MODEL.md` и `tools/`.
- Repository structure validation в `tools/validate-repository-structure.sh`.
- Issue #35: soft frontmatter validation в `tools/validate-frontmatter.sh`
  для проверки обязательных полей `status`, `version`, `updated` и
  `ai-generated` без блокирующего exit code.
- Active documentation для Anti-Inflation principle: артефакт создается только
  когда снижает операционную боль.
- Issue #31: `standards/RESEARCH_PROFILE.md` — canonical профиль
  исследовательских проектов (именование `YYYY-MM-topic.md`, frontmatter
  исследований, организация экспериментов `exp-<slug>/`, чек-лист публикации и
  цитируемые best practices). Зарегистрирован как active в `standards/README.md`
  и проверяется в `tools/validate-repository-structure.sh`.
- `standards/PRODUCT_PROFILE.md` (issue #29): профиль для продуктовых проектов
  с обязательными артефактами, шаблоном `PRODUCT_VISION.md` и матрицей
  адаптации по стадиям MVP / Pilot / Production; зарегистрирован в реестре
  standards и в structure validation.
- `standards/TEAM_CONTRACT.md` как шаблон и инструкция для создания
  project-level `CONTRIBUTING.md` и `AI_GOVERNANCE.md` в spoke-проектах.
- Issue #41: `standards/ISSUE_WORKFLOW.md` — canonical жизненный цикл задач
  (7 статусов: `draft`, `ready`, `in-progress`, `review`, `merged`, `closed`,
  `blocked`), правила переходов, связи между артефактами (`User Story / ФТ`,
  `CHANGELOG.md`, `governance/ARTIFACT_MAP.md`) и точки автоматизации.
  Зарегистрирован как active в `standards/README.md` и проверяется в
  `tools/validate-repository-structure.sh`.

### Changed

- Issue #49: migration state updated from "legacy files preserved for analysis"
  to "legacy files removed or promoted"; `projects/mango/README.md` now links
  to active project/research navigation instead of `projects/README-old.md`.
- Issue #49: `tools/validate-repository-structure.sh` now registers promoted
  active files and fails if tracked `-old` files are reintroduced.
- Issue #47: previous tracked files were renamed with suffix `-old` for audit
  and selective migration before cleanup issue #49.
- Active navigation теперь указывает на `governance/` вместо `meta/` и на
  `tools/` вместо `tests/`.
- Standards рассматриваются как плоский registry, пока operational use не
  докажет потребность в более глубокой taxonomy.

### Removed

- Issue #49: removed legacy root files, old GitHub templates, `docs-old/`,
  `meta-old/`, `tests-old/`, `experiments-old/`, old education package files,
  repository-governance archive candidates, `.gitkeep` placeholders and other
  superseded `-old` inputs according to the migration audit categories.

## Связанные документы

- [README.md](README.md)
- [CONCEPT.md](CONCEPT.md)
- [AI_GOVERNANCE.md](AI_GOVERNANCE.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [standards/README.md](standards/README.md)
- [standards/GLOSSARY.md](standards/GLOSSARY.md)
- [standards/FILE_NAMING.md](standards/FILE_NAMING.md)
- [standards/EDUCATION_PROFILE.md](standards/EDUCATION_PROFILE.md)
- [standards/TEAM_CONTRACT.md](standards/TEAM_CONTRACT.md)
- [standards/ISSUE_WORKFLOW.md](standards/ISSUE_WORKFLOW.md)
- [governance/REPO_MODEL.md](governance/REPO_MODEL.md)
- [governance/ARTIFACT_MAP.md](governance/ARTIFACT_MAP.md)

## TODO

- Добавить concrete artifact templates после появления повторяющихся работ и
  стабильных потребностей.
- Заменить license placeholder после решения Founder & PO.
