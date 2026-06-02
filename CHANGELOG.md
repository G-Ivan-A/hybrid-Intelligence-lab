# Changelog

All notable repository governance changes are documented here.

## Unreleased

### Changed

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
