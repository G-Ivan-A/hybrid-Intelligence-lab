---
status: canonical
version: 1.0
updated: 2026-05-26
ai-generated: false
---

# Отчёт аудита миграции — май 2026

Версия: 1.0

Дата: 2026-05-26

Связанная задача: [issue #47](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/47)

Operating Mode: `creative` — аудит проверяет согласованность новой структуры и
**предлагает** улучшения. Изменения в существующие файлы не вносятся, кроме
создания этого проекта и навигационной ссылки в корневом `README.md`.

## 🔍 Методология аудита

Аудит выполнен воспроизводимыми проверками над фактическим состоянием
репозитория (`git ls-files`), а не над планами. Применены четыре метода:

1. **Согласованность принципов.** Каждый принцип из
   [CONCEPT.md](../../../CONCEPT.md) сверен с местом его реализации в активных
   артефактах.
2. **Матрица перекрёстных ссылок.** Из всех активных `.md` (без суффикса
   `-old`) извлечены относительные ссылки и проверено существование целей.
   Содержимое внутри fenced code blocks (```` ``` ````) исключено, так как там
   находятся шаблонные примеры, а не реальная навигация.
3. **Анализ миграции `-old`.** Для ключевых исторических файлов прочитано
   содержание и сопоставлено с активными артефактами (что перенесено, что
   отброшено и почему).
4. **Терминология.** Термины сверены с эталоном
   [standards/GLOSSARY.md](../../../standards/GLOSSARY.md).

Объём на момент аудита: **20** активных файлов, **43** файла с суффиксом
`-old`. Проверены оба валидатора: `tools/validate-frontmatter.sh` (soft) и
`tools/validate-repository-structure.sh` (hard).

## ✅ Чек-лист согласованности с CONCEPT.md

Проверены все восемь принципов из раздела «Принципы» `CONCEPT.md`. Принцип
issue «Evidence-driven» соответствует принципу `Traceability` в `CONCEPT.md`.

| Принцип | Реализован? | Где проверено | Комментарий |
|---------|-------------|---------------|-------------|
| Governance before scale | ✅ | `governance/REPO_MODEL.md`, `tools/validate-repository-structure.sh` | Структура и правила зафиксированы и проверяются скриптом до роста артефактов. |
| Separation of concerns | ✅ | `README.md` (таблица «Структура»), `governance/REPO_MODEL.md` | `standards / research / frameworks / projects / education / governance / tools` имеют разные дома. |
| Existing frameworks first | ✅ | `governance/REPO_MODEL.md`, `frameworks/README-old.md` | Активного framework нет; `frameworks/` содержит только `-old` вход — преждевременная методология не создана. |
| Traceability (Evidence-driven) | ⚠️ | frontmatter, ссылки на `-old`, `CHANGELOG.md` (issue refs), `standards/GLOSSARY.md` | Источники и issue прослеживаются. Замечание: frontmatter присутствует не во всех canonical файлах (см. предложение 1). |
| Operating Mode | ✅ | `AI_GOVERNANCE.md` (Operating Modes), `standards/GLOSSARY.md`, `.github/ISSUE_TEMPLATE/task.yml` | Режим задаётся явно; данный аудит выполнен в `creative`. |
| Human-in-control | ✅ | `AI_GOVERNANCE.md` (Роли, Эскалация) | Решения остаются за Founder & PO и reviewers; аудит откладывает реализацию до согласования. |
| Safe publication | ✅ | `AI_GOVERNANCE.md` (правило 6) | Секреты и sensitive data в активных файлах не обнаружены; репозиторий — документация. |
| Anti-Inflation | ✅ | `governance/REPO_MODEL.md`, `governance/ARTIFACT_MAP.md` (колонка «Обязательный?») | Артефакт оправдан только при операционной боли; обязательность артефактов размечена. |

Итог: 7 из 8 принципов реализованы без замечаний; 1 (`Traceability`) — с минорным
замечанием по полноте frontmatter.

## 🔗 Матрица перекрёстных ссылок

| Проверка | Результат |
|----------|-----------|
| Относительных ссылок в активных файлах (без code fences) | 131 |
| Битых ссылок в активной навигации | **0** ✅ |
| Активные файлы, ссылающиеся на `-old` входы | 1 ⚠️ |
| Ложные срабатывания внутри шаблонных code fences | 7 (не битые ссылки) |

Детали:

- **Битых ссылок нет.** Все 131 относительная ссылка между активными
  артефактами ведут на существующие цели.
- **⚠️ Активная ссылка на `-old`.** `archive/projects/mango/README.md` в разделе
  «Связанные артефакты» ссылается на `projects/README-old.md`. Это исторический
  вход, а не активный контракт. Последствие: `projects/README-old.md` нельзя
  удалить, пока ссылка не заменена или не убрана (см. раздел удаления).
- **Ложные срабатывания.** Наивный поиск ссылок отметил 7 «битых» целей
  (`standards/EDUCATION_PROFILE.md` и `standards/RESEARCH_PROFILE.md`) — все
  находятся внутри fenced шаблонов (`module-01/`, `lesson-01.md`,
  `2026-05-topic.md` и т. п.) и являются примерами структуры курса/исследования,
  а не реальной навигацией. Конфликтом не считаются.
- **Циклы.** Двунаправленные ссылки (например, `README.md` ↔ `CONCEPT.md` ↔
  `governance/REPO_MODEL.md`) — это намеренная hub-навигация, а не вредные
  циклы.

## 📦 Таблица миграции `-old`

| Старый путь | Новый путь / Статус | Что сохранено | Что отброшено + почему |
|------------|---------------------|---------------|------------------------|
| `README-old.md` | `README.md` | Позиционирование hub-and-spoke, таблицы ключевых документов и структуры | Ссылки на `PRODUCT_VISION.md`, `docs/concept/*`, отдельные каталоги `meta/`, `experiments/`, `docs/` — заменены новой моделью |
| `docs-old/concept/repository-structure-old.md` | `CONCEPT.md` + `governance/REPO_MODEL.md` | Модель hub-and-spoke, separation of concerns, обоснование структуры | Детальная таблица сравнения 5 вариантов структуры (осталась как контекст в `-old`) |
| `docs-old/concept/vision-standard-old.md` | `standards/PRODUCT_PROFILE.md` (+ профили research/education) | Product Vision Board как основа `PRODUCT_VISION.md` | Полное сравнение PRD/Lean/ADR/RFC-lite/IMRAD перенесено выборочно |
| `docs-old/governance/hybrid-team-collaboration-old.md` | `AI_GOVERNANCE.md` + `standards/ISSUE_WORKFLOW.md` | Роли, 7-шаговый workflow, правила постановки задач для ИИ | Терминология «Команда C» обобщена до ролей reviewer/contributor |
| `research/repository-governance/*-old.md` | `CONCEPT.md`, `governance/REPO_MODEL.md` | Governance-as-you-grow → Anti-Inflation; «операционный костяк сначала»; статусы зрелости | Промежуточные межкомандные обсуждения (ценность архивная) |
| `meta-old/README-old.md` | `governance/ARTIFACT_MAP.md` + frontmatter `status` | Идея artifact map; maturity model (`draft/reviewed/published/superseded`) | Каталог `meta/` как слой — заменён на `governance/` |
| `standards/README-old.md` | `standards/README.md` | Реестр стандартов; «будущие стандарты» → строки `Planned` | Прямая ссылка на `docs/concept/vision-standard.md` |
| `projects/README-old.md` | `archive/projects/mango/README.md` + `projects/repo-development/README.md` | Критерии «когда `/projects` vs spoke», рекомендуемая структура | Единый каталоговый `README` пока не воссоздан (см. предложение 2) |
| `tests-old/validate-repository-structure-old.sh` | `tools/validate-repository-structure.sh` | Логика проверки структуры и `-old` миграции | Путь `tests/` → `tools/` |
| `.github/ISSUE_TEMPLATE/{ai_implementation_task,config,governance_change,research_task}-old` | `.github/ISSUE_TEMPLATE/task.yml` | Структура постановки задач + operating mode | 4 шаблона объединены в один focused шаблон |
| `.github/pull_request_template-old.md` | ⚠️ Активный PR-шаблон не воссоздан | — | Решить: нужен ли активный PR-шаблон |
| `PRODUCT_VISION-old.md` | `standards/PRODUCT_PROFILE.md` (шаблон) | Структура продуктового видения | Корневой `PRODUCT_VISION.md` убран: видение — артефакт spoke-проекта |
| `AI_GOVERNANCE-old.md`, `CONTRIBUTING-old.md`, `CHANGELOG-old.md`, `LICENSE-old` | `AI_GOVERNANCE.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE` | Контракты, workflow, журнал, лицензия-placeholder | Сокращены до коротких активных контрактов |
| `education/**-old`, `experiments-old/mango/tz-corpus/**` | `standards/EDUCATION_PROFILE.md`; контекст `archive/projects/mango/` | Профиль курсов; решение «`tz-corpus` → Mango» | Сам учебный/экспериментальный контент пока не перенесён в активные артефакты |
| `research/mango/**-old`, `frameworks/README-old.md` | Каталоги сохранены; активного контента нет | Доменные каталоги зарезервированы | Перенос отложен до операционной потребности (Anti-Inflation) |

## 💡 Лучшее из `-old`: что учтено

Не менее пяти конкретных примеров переноса ценного содержания:

1. **Модель hub-and-spoke.** Из `docs-old/concept/repository-structure-old.md`
   (сравнение пяти вариантов структуры) выбрана и зафиксирована в
   `CONCEPT.md` («Модель репозитория») и `governance/REPO_MODEL.md`.
2. **Статусы зрелости.** Решение #5 в
   `research/repository-governance/final-vision-old.md` и «Maturity model» в
   `meta-old/README-old.md` (`draft/reviewed/published/superseded`)
   реализованы как frontmatter `status:` и проверяются в
   `tools/validate-frontmatter.sh` (добавлен `canonical`).
3. **Governance-as-you-grow → Anti-Inflation.** «Сначала операционный костяк,
   `/governance/`-дерево позже по триггеру» (решения #2–#3 final-vision)
   превратилось в Anti-Inflation principle в `governance/REPO_MODEL.md`.
4. **Роли и workflow.** Ролевая модель и 7-шаговый поток из
   `docs-old/governance/hybrid-team-collaboration-old.md` перенесены в
   `AI_GOVERNANCE.md` (Роли, Правила) и `standards/ISSUE_WORKFLOW.md`.
5. **Artifact map.** Идея реестра ключевых документов из
   `meta-old/README-old.md` реализована как `governance/ARTIFACT_MAP.md`.
6. **Структурная проверка.** `tests-old/validate-repository-structure-old.sh`
   перенесён и развит в `tools/validate-repository-structure.sh`.
7. **`tz-corpus` → Mango.** Решение #7 final-vision о переносе эксперимента в
   контекст Mango отражено в позиционировании `archive/projects/mango/`.

## 🚀 Предложения по улучшениям (НЕ реализованы, только рекомендации)

Каждое предложение: проблема → идея → ожидаемая польза → оценка сложности.
Фокус на минимализме: ни одно предложение не должно усложнять систему без явной
пользы.

### Предложение 1. Полнота frontmatter в canonical файлах

- **Проблема.** Из 16 активных `.md` 6 не имеют frontmatter
  (`README.md`, `AI_GOVERNANCE.md`, `CONTRIBUTING.md`, `CHANGELOG.md`,
  `governance/REPO_MODEL.md`, `standards/README.md`), тогда как остальные 10
  имеют. `validate-frontmatter.sh` — soft (только warnings), поэтому
  несогласованность сохраняется незаметно.
- **Идея.** Принять явную политику: либо (a) добавить frontmatter во все
  canonical документы, либо (b) задокументировать в стандарте, какие типы
  артефактов обязаны иметь frontmatter (например, стандарты и профили — да;
  корневая навигация — опционально).
- **Польза.** Согласованные машиночитаемые метаданные; warnings валидатора
  становятся осмысленными.
- **Сложность.** Низкая (добавить 4-строчные блоки) — Средняя (решение по
  политике + правка 6 файлов).

### Предложение 2. Дрейф `governance/ARTIFACT_MAP.md` по `projects/`

- **Проблема.** Строка `/projects/` в карте помечена «сейчас — `-old` входы»,
  но активные project README уже существуют (`archive/projects/mango/README.md`, теперь
  `projects/repo-development/README.md`). Собственное правило карты требует
  отражать фактическое состояние и добавлять строку на каждый новый активный
  артефакт. ⚠️ Найдено расхождение.
- **Идея.** Обновить примечание строки `/projects/` и/или добавить строки на
  активные project README; либо ввести правило, что project README индексируются
  через индекс `projects/`, а не построчно в карте.
- **Польза.** Карта остаётся точной (её прямое назначение); не вводит в
  заблуждение новых участников и ИИ.
- **Сложность.** Низкая.

### Предложение 3. Ручное сопровождение whitelist `is_active_file`

- **Проблема.** Каждый новый активный файл нужно вручную добавлять в
  `is_active_file` в `tools/validate-repository-structure.sh`, иначе проверка
  падает (`tracked legacy file without -old suffix`). Это дублирует
  `required_files` и легко забывается. Данный аудит тоже потребовал ручной
  правки скрипта.
- **Идея.** Распознавать «активные опциональные» файлы по соглашению (например,
  любой `.md` без `-old` внутри `projects/<slug>/` считать активным) или
  генерировать whitelist из `governance/ARTIFACT_MAP.md` / манифеста.
- **Польза.** Меньше ручных правок, меньше случайно «красных» PR, единый
  источник истины.
- **Сложность.** Средняя (правка скрипта + выбор источника истины).

### Предложение 4. Авто-проверка ссылок, игнорирующая code fences

- **Проблема.** Нет автоматической проверки битых внутренних ссылок. Наивный
  проверяющий даёт ложные срабатывания на шаблонных примерах внутри fenced
  блоков (в этом аудите — 7 штук).
- **Идея.** Добавить `tools/validate-links.sh`, который вырезает fenced code
  blocks перед проверкой относительных ссылок, и включить его в локальные
  проверки `CONTRIBUTING.md`.
- **Польза.** Раннее обнаружение реально битой навигации без ложных
  срабатываний.
- **Сложность.** Низкая — Средняя.

### Предложение 5. Локальные проверки не запускаются в CI

- **Проблема.** Каталога `.github/workflows/` нет; оба валидатора запускаются
  только локально. Регрессия структуры или frontmatter может попасть в `main`
  незамеченной — например, авто-генерируемый stray `.gitkeep`, который дважды
  ломал структурную проверку (issues #17/#45) и снова появился в issue #47.
- **Идея.** Добавить лёгкий GitHub Actions workflow, запускающий
  `validate-frontmatter.sh` и `validate-repository-structure.sh` на PR.
- **Польза.** Definition of Done из `AI_GOVERNANCE.md` проверяется
  автоматически; повторяющаяся регрессия `.gitkeep` была бы поймана.
- **Сложность.** Низкая.

## Статус предложений

Все предложения в разделе «💡 Предложения по улучшениям» имеют статус
**«На рассмотрении»**. Реализация возможна только после: (1) обсуждения в Issue,
(2) ревью, (3) явного согласования (`human-in-control`,
[AI_GOVERNANCE.md](../../../AI_GOVERNANCE.md)).

**Предложения не реализованы.** Данный отчёт не вносит изменений в существующие
артефакты; он только фиксирует наблюдения и рекомендации.

## 🧹 Рекомендация по удалению `-old`

Категории отражают готовность к удалению на момент аудита. Финальное решение —
за Founder & PO и reviewers.

### ✅ Готово к удалению (содержание перенесено, уникальной ценности не осталось)

- `README-old.md` → `README.md`
- `CONTRIBUTING-old.md` → `CONTRIBUTING.md`
- `AI_GOVERNANCE-old.md` → `AI_GOVERNANCE.md`
- `CHANGELOG-old.md` → `CHANGELOG.md`
- `standards/README-old.md` → `standards/README.md`
- `meta-old/README-old.md` → `governance/ARTIFACT_MAP.md` + frontmatter `status`
- `tests-old/validate-repository-structure-old.sh` → `tools/validate-repository-structure.sh`
- `.github/ISSUE_TEMPLATE/ai_implementation_task-old.yml`,
  `config-old.yml`, `governance_change-old.md`, `research_task-old.md` →
  `.github/ISSUE_TEMPLATE/task.yml`

### ⚠️ Требует ручной проверки (перенос частичный или ссылка не разорвана)

- `projects/README-old.md` — на него **ссылается активный**
  `archive/projects/mango/README.md`. Сначала заменить/убрать ссылку, затем удалять.
- `docs-old/concept/repository-structure-old.md`,
  `docs-old/concept/vision-standard-old.md` — обоснования перенесены частично;
  сверить, что таблицы сравнения не нужны как архив.
- `docs-old/governance/hybrid-team-collaboration-old.md` — проверить, что
  правила external-contributor отражены в активных контрактах.
- `PRODUCT_VISION-old.md` — убедиться, что структура видения отражена в
  `standards/PRODUCT_PROFILE.md`.
- `.github/pull_request_template-old.md` — решить, нужен ли активный
  PR-шаблон, до удаления.
- `education/**-old`, `experiments-old/mango/tz-corpus/**`,
  `research/mango/**-old`, `frameworks/README-old.md` — профили выведены, но сам
  контент/эксперименты ещё не перенесены в активные артефакты.

### ❌ Не удалять (сохранить как архив / решение отложено)

- `LICENSE-old` — решение по лицензии ещё за Founder & PO (`LICENSE` —
  placeholder). Сохранить до выбора финальной лицензии.
- `research/repository-governance/*-old.md` — межкомандное governance-исследование
  имеет traceability/архивную ценность; рекомендуется переместить в `/archive/`,
  а не удалять.
- `.gitkeep-old` — безвредный исторический placeholder; удаление низкоприоритетно.

## Связанные артефакты

- [CONCEPT.md](../../../CONCEPT.md)
- [governance/REPO_MODEL.md](../../../governance/REPO_MODEL.md)
- [governance/ARTIFACT_MAP.md](../../../governance/ARTIFACT_MAP.md)
- [standards/GLOSSARY.md](../../../standards/GLOSSARY.md)
- [standards/ISSUE_WORKFLOW.md](../../../standards/ISSUE_WORKFLOW.md)
- [projects/repo-development/README.md](../README.md)
