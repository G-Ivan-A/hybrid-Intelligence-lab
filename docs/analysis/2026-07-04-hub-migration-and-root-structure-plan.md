---
status: draft
version: 0.1
updated: 2026-07-04
temperature: 0.1
type: internal-analysis
context: [hub, migration, root-structure, archetype-a, provisional-standards, issue-372, b-034]
method: source-of-truth-tracing + as-is-inventory + delta-mapping
scope: repo
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/372"
based_on: "docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md + docs/adr/2026-06-adr-002-artifact-document-methodology.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/372"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/296"
related_artifacts:
  - "docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md"
  - "docs/adr/2026-06-adr-002-artifact-document-methodology.md"
  - "docs/adr/2026-07-adr-003-research-structure.md"
  - "docs/adr/2026-07-adr-004-reports-structure.md"
  - "docs/adr/2026-07-adr-005-audit-structure.md"
  - "docs/adr/2026-07-adr-006-analysis-structure.md"
  - "research/hub/2026-06-23-repository-structure-concept.md"
  - "standards/analysis-standard.md"
  - "standards/project-structure-inheritance.md"
  - "governance/repo-model.md"
  - "governance/backlog.md#b-034-rfc-план-миграции-репо-хаба-после-стандартов-researchanalysisaudit"
---

# Hub migration and root-structure plan (документ-план для B-034)

> Режим: **Analysis (recommendation / matrix)** для issue
> [#372](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/372) и
> backlog [B-034](../../governance/backlog.md).
> Deep Think, три экспертные оптики: **Ecosystem Architect**,
> **Data Migration Specialist**, **Governance Auditor**.
> Короткая граница: **этот документ не переносит файлы, не переделывает
> валидаторы и не создаёт RFC/ADR.** Он фиксирует интерпретацию источника
> истины, целевую архитектуру корня, механизм provisional-стандартов и матрицу
> миграции As-Is → To-Be как upstream-вход для будущего миграционного RFC B-034.

## 1. Summary / BLUF

**Крайний (наиболее поздний авторитетный) документ, фиксирующий структуру
каталогов для архетипов, — это принятое решение
[ADR-001 «Методология инфраструктуры проектов экосистемы»](../adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md)**
(`status: accepted`, 2026-06-27), а не стандарты Research / Analysis / Audit.
Его операционным спутником по маршрутизации артефактов является
[ADR-002](../adr/2026-06-adr-002-artifact-document-methodology.md) (`accepted`,
v1.4, 2026-07-02). Исполнитель искал источник независимо и **не** предполагал,
что им являются R/A/A-стандарты: R/A/A-стандарты нормируют **внутреннюю**
структуру артефактов и их целевой каталог по типу, но **не** предписывают
физическую реструктуризацию репозитория (это прямо разведено в issue #296 и в
DoD B-034).

Ключевые выводы:

1. **Хаб — это архетип A (Governance & Knowledge Hub), а не Portal.** Специфичные
   корневые каталоги (`research/`, `practices/`, `projects/`) — это
   **архитектурная способность архетипа A**, а не признак Portal. Portal —
   отдельный проект-профиль архетипа C в отдельном репозитории. Наличие в Хабе
   `website/` (рендер mkdocs-сайта) **не** делает его Portal.
2. ADR-001 уже содержит раздел
   [«Переходный режим для текущего Хаба»](../adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md),
   который **прямо требует** отдельный PR с картой перехода, обновлением ссылок
   и валидаторов для любого переименования корневых каталогов. Настоящий
   документ — эта карта на уровне анализа/плана.
3. Целевой корень = **универсальное ядро** ADR-001 **плюс** дельта архетипа A.
   Значительная часть текущего дерева уже совпадает с целью (`standards/`,
   `docs/adr/`, `docs/analysis/`, `docs/audit/`, `docs/report/`, `templates/`,
   `tools/`, `research/`, `practices/`, `projects/`). Основная дельта — расщепить
   `governance/` на `ai-governance/` + `pr-ops/` (+ `GOVERNANCE.md`), ввести
   `kb/`, `runs/`, `ai-rules/` и мигрировать `governance/rfc/` → `docs/rfc/`.
4. Часть маппингов **однозначна** (fixed decision в ADR-001/002), часть —
   **неоднозначна** и вынесена на человеческое решение (`frameworks/`, `guides/`,
   `education/`, `experiments/`, `website/`, `CONCEPT.md`,
   `AI_PROJECT_CONTEXT-Summary.md`, граница `practices/` ↔ `docs/practice/`,
   `knowledge/` ↔ `kb/`). Двусмысленные цели **явно помечены** 🟡.
5. **Механизм provisional-стандартов** рекомендуется реализовать через
   **lifecycle-статус** (`draft`/`proposed` governance-словаря) без нового
   подкаталога — это соответствует anti-inflation и правилу 2FA для плоского
   `standards/`. Подкаталог `standards/provisional/` резервируется как эскалация
   только при доказанной review-pain.

Рекомендуемое движение: **B-034 → review** как upstream-анализ; собственно
миграционный RFC + серия физических PR остаются отдельными задачами по DoD.

## 2. Context / Scope

### 2.1. Причина и границы

Issue #296 методологически разделило **стандартизацию** артефактов и
**физическую миграцию** репозитория. B-034 фиксирует, что физическая
реструктуризация — отдельный RFC **после** трёх стандартов (Research/Analysis/
Audit), а не этап стандартизации. Issue #372 просит **раньше RFC** подготовить
document-plan: найти источник истины, вывести целевую архитектуру корня,
спроектировать механизм provisional-стандартов и построить матрицу миграции.

Что этот документ делает: интерпретирует источник истины, строит целевую модель
корня и матрицу As-Is → To-Be, помечает неоднозначные цели для координации.

Что он **не** делает (жёсткие ограничения из блока «Галлюцинации команды Q»
issue #372):

- не превращает Хаб в Portal и не мигрирует Хаб в Portal (Portal — отдельный
  проект);
- не считает R/A/A-стандарты источником решения о физической структуре;
- не перемещает и не переименовывает файлы (только план);
- не переделывает валидаторы (отдельная задача после миграции);
- не создаёт RFC/ADR (это B-034 и последующий decision gate).

### 2.2. Снимок As-Is (корень текущего Хаба)

Снимок tracked-дерева ветки `issue-372-5f0239fd0514`. Корневые каталоги:

| Каталог/файл | Файлов | Роль сейчас |
| --- | ---: | --- |
| `standards/` | — | Плоские стандарты формата/качества/review. |
| `docs/` (`adr/`, `analysis/`, `audit/`, `report/`, `rfc?`) | — | ADR, Analysis, Audit-report, Report. `docs/rfc/` пока нет (RFC в `governance/rfc/`). |
| `research/` | — | Хронологический research по доменам (`hub/`, `mango/`, …). |
| `practices/` | 14 | Практики агентной работы, ai-governance и т.п. |
| `frameworks/` | 1 | Плейсхолдер (только `README.md`). |
| `projects/` | 7 | Проектные споки/подпроекты Хаба. |
| `education/` | 1 | Плейсхолдер (только `README.md`). |
| `guides/` | 11 | Человеко-ориентированные руководства (quick-start, deploy, …). |
| `website/` | 5 | Зеркало/исходники публикуемого mkdocs-сайта. |
| `experiments/` | 2 | Тест-скрипты валидаторов (`test-*.sh`). |
| `governance/` | — | `backlog.md`, `artifact-map.md`, `repo-model.md`, `rfc/`, политики. |
| `templates/` | — | `htom/`, `spoke/` и шаблоны артефактов. |
| `tools/` | — | Валидаторы и maintenance-скрипты. |
| `.github/` | — | CI и issue-templates. |
| root-файлы | 10 | `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`, `AI_GOVERNANCE.md`, `AI_PROJECT_CONTEXT-Summary.md`, `CONCEPT.md`, `mkdocs.yml`, `.gitignore`, `.gitkeep`. |

## 3. Найденный «крайний документ» и его интерпретация

### 3.1. Как искали и почему это именно ADR-001

Критерий поиска: **наиболее поздний по lifecycle документ, который фиксирует
как принятое решение структуру каталогов для архетипов** (а не описывает её как
rationale и не нормирует внутреннюю форму одного типа артефакта). Кандидаты и
вердикт:

| Кандидат | Тип / статус | Вердикт |
| --- | --- | --- |
| [research/hub/2026-06-23-repository-structure-concept.md](../../research/hub/2026-06-23-repository-structure-concept.md) | Research, `reviewed` | **Источник rationale, не норма.** ADR-001 явно перевёл его в `reviewed` «как источник вариантов, а не canonical-норму». |
| [ADR-001](../adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md) | ADR, `accepted` | **Источник истины.** Фиксирует универсальное ядро, архетипы A–D, правила размещения и переходный режим Хаба. |
| [ADR-002](../adr/2026-06-adr-002-artifact-document-methodology.md) | ADR, `accepted` v1.4 | **Спутник по маршрутизации артефактов** (target-каталог по типу). Не про физическую структуру корня. |
| [ADR-003](../adr/2026-07-adr-003-research-structure.md)/[004](../adr/2026-07-adr-004-reports-structure.md)/[005](../adr/2026-07-adr-005-audit-structure.md)/[006](../adr/2026-07-adr-006-analysis-structure.md) + R/A/A-стандарты | ADR/standard | **Нормируют внутреннюю форму и routing по типу** (`docs/analysis/`, `docs/audit/`, `docs/report/`, `research/<domain>/`), но **не** предписывают реструктуризацию корня. Уточняют ADR-002, не заменяют ADR-001. |
| [governance/repo-model.md](../../governance/repo-model.md) | canonical (описание) | **Описывает ДЕЙСТВУЮЩУЮ структуру** (As-Is), не целевую. Полезен как baseline для дельты. |

Вывод: **источник истины о целевой структуре корня — ADR-001**; ADR-002 —
источник целевого каталога по типу артефакта. R/A/A-цепочка — не источник
решения о физической структуре (соответствует ограничению issue #372).

### 3.2. Что именно фиксирует ADR-001

1. **Универсальное базовое ядро** для любого репозитория экосистемы (см. §4.1).
2. **Архетипы A–D** с расширениями «базовое / рекомендуемое / профильное».
   Хаб = **A. Governance & Knowledge Hub**; базовые расширения A — `research/`,
   `practices/`; рекомендуемые — `projects/`, `knowledge/`; профильные — каталоги
   доменных research-направлений.
3. **Web Portal и Library/SDK — профили архетипа C, а не отдельные архетипы.**
   Это прямая опора против галлюцинации «Хаб → Portal».
4. **Правило 2FA** для плоских каталогов (`ai-rules/`, `standards/`, `pr-ops/`):
   подкаталог только при операционной боли + повторяемом использовании.
5. **Переходный режим Хаба:** исторические пути (`governance/`, `AI_GOVERNANCE.md`,
   `practices/`, `standards/`, `templates/htom/`, `governance/rfc/`) остаются
   активными до отдельного решения; **любое переименование корневых каталогов =
   отдельный PR с картой перехода, обновлением ссылок и валидаторов.** Настоящий
   документ — этот план на уровне анализа.

## 4. Архитектура корневых каталогов (delta from base)

### 4.1. Универсальное ядро (To-Be, из ADR-001) → дельта Хаба

| To-Be (ядро ADR-001) | Назначение | As-Is в Хабе | Дельта |
| --- | --- | --- | --- |
| `ai-rules/` | Правила поведения AI-агента, плоско (2FA) | Разбросано в `AI_GOVERNANCE.md`, `practices/agent-work/` | 🟠 Ввести; наполнить при выделении явных AI-правил |
| `ai-governance/` | Политики, compliance, риски AI | `AI_GOVERNANCE.md` (root), `practices/ai-governance/` | 🟠 Расщепить из `governance/` + root-файла |
| `pr-ops/` | Управление задачами, PR, review, плоско (2FA) | `governance/backlog.md`, часть `governance/` | 🟠 Расщепить из `governance/` |
| `standards/` | Стандарты формата/качества/review, плоско | `standards/` | 🟢 Совпадает |
| `docs/analysis/` | Analysis-артефакты | `docs/analysis/` | 🟢 Совпадает |
| `docs/reports/` *(ADR-001 набросок)* → **`docs/report/` + `docs/audit/`** *(реконсилировано ADR-004/ADR-002 v1.4)* | Reports и Audit-reports | `docs/report/`, `docs/audit/` | 🟢 Совпадает с реконсилированной целью |
| `docs/adr/` | Принятые решения | `docs/adr/` | 🟢 Совпадает |
| `docs/rfc/` | Proposal до решения | `governance/rfc/` (Хаб) | 🟠 Мигрировать `governance/rfc/` → `docs/rfc/` |
| `docs/practice/` | Практики как docs | `practices/` (корень) | 🟡 Неоднозначность: `practices/` (базовое расширение A) vs `docs/practice/` |
| `kb/` | Операционно применимые знания | — (нет явного) | 🟠 Ввести; наполнять по мере операционной боли |
| `runs/` | Записи выполнения / run-records | — (частично `experiments/`, `projects/*/`) | 🟠 Ввести (пусто/по факту) |
| `templates/` | Копируемые поверхности | `templates/` | 🟢 Совпадает |
| `tools/` | Проверки и maintenance | `tools/` | 🟢 Совпадает |
| `app/` | Runtime, если репозиторий его содержит | — | ⚪ Не применимо для архетипа A |
| `GOVERNANCE.md` | Якорь org-governance | `AI_GOVERNANCE.md` | 🟠 Ввести якорь; согласовать с `AI_GOVERNANCE.md` |
| `README/CHANGELOG/CONTRIBUTING/LICENSE/.gitignore` | Корневые файлы | Присутствуют | 🟢 Совпадает |
| `.gitattributes` | Атрибуты git | — | ⚪ Опционально |

Легенда: 🟢 совпадает · 🟠 однозначная дельта (fixed decision) · 🟡 неоднозначно →
человеческое решение · ⚪ не применимо/опционально.

### 4.2. Дельта архетипа A (специфичные корневые каталоги)

**Это ключевой раздел против смешения Hub и Portal.** Специфичные корневые
каталоги Хаба — не признак Portal, а **архитектурная способность архетипа A** по
таблице архетипов ADR-001:

| Каталог | Уровень расширения A | As-Is | Целевой статус |
| --- | --- | --- | --- |
| `research/` | Базовое расширение A | `research/` | 🟢 Оставить (дом доменного research) |
| `practices/` | Базовое расширение A | `practices/` | 🟡 Оставить как расширение A **или** свести в `docs/practice/` — human decision |
| `projects/` | Рекомендуемое расширение A | `projects/` | 🟢 Оставить (правила — [project-structure-inheritance.md](../../standards/project-structure-inheritance.md)) |
| `knowledge/` | Рекомендуемое расширение A | — | 🟡 Реконсилировать с `kb/`: ADR-001 в ядре называет `kb/`, в расширениях A — `knowledge/`; выбрать один термин — human decision |
| доменные research-каталоги | Профильное расширение A | `research/hub/`, `research/mango/`, … | 🟢 Оставить |

> **Portal ≠ Hub (фиксация против галлюцинации).** Web Portal — профиль
> архетипа C (ADR-001: «Web Portal и Library/SDK не создают отдельные архетипы…
> являются профилями архетипа C»). Хаб — архетип A. Наличие в Хабе `website/`
> (рендер mkdocs) и специфичных корневых каталогов — **ожидаемая способность
> архетипа A**, а не сигнал миграции Хаба в Portal. Никакой строки этой матрицы
> не следует трактовать как «Хаб становится Portal».

### 4.3. Неоднозначные корневые сущности (→ human decision)

Ниже — корневые каталоги/файлы As-Is, для которых ADR-001/002 **не** дают
однозначной цели. По правилу issue #372 они **явно помечены** для координации и
не мигрируются без человеческого решения:

| As-Is | Наблюдение | Вопрос на решение (🟡) |
| --- | --- | --- |
| `frameworks/` | Плейсхолдер (1 `README.md`), нет в ядре и в расширениях A | Удалить/законсервировать, или это будущий дом какого профиля? |
| `guides/` | 11 человеко-ориентированных руководств; во фронтматтер-валидаторе есть класс `guide` | Оставить как удобство архетипа A или свести в `docs/`? |
| `education/` | Плейсхолдер (1 `README.md`); контент архетипа D | Профиль обучения Хаба или отдельный спок архетипа D? |
| `experiments/` | 2 тест-скрипта валидаторов | `tools/` (тесты инструментов) или `runs/`? |
| `website/` | Зеркало публикуемого mkdocs-сайта | Публикационный артефакт: оставить/инфраструктура; **не** признак Portal |
| `CONCEPT.md` (root) | Концептуальный документ | `docs/` или `research/`? Тип и дом на решение |
| `AI_PROJECT_CONTEXT-Summary.md` (root) | Сводка контекста проекта | `kb/` (operational) или `docs/`? |
| `practices/` ↔ `docs/practice/` | Оба существуют в цели | Единый дом практик: расширение A `practices/` или ядро `docs/practice/`? |
| `knowledge/` ↔ `kb/` | Термины расходятся в ADR-001 | Выбрать один термин операционных знаний |

## 5. Механизм provisional-стандартов

**Проблема.** Нужна форма для стандарта, который ещё не прошёл human decision gate
(«provisional»), не смешивая его с `accepted`-стандартом, и без инфляции
структуры плоского `standards/` (правило 2FA ADR-001).

**Наблюдение.** Governance-словарь статусов уже различает зрелость: стандарт
класса `standards/*.md` подчиняется словарю `draft → proposed → accepted →
rejected → deprecated → superseded` (frontmatter-валидатор enforce'ит это по
классу документа). То есть «provisional» = стандарт в статусе `draft`/`proposed`
до `accepted`. Отдельная сущность для этого **не обязательна**.

Опции:

| Опция | Как выглядит | Плюсы | Минусы |
| --- | --- | --- | --- |
| **A. Только lifecycle-статус** (рекоменд.) | `standards/<name>.md` с `status: draft`/`proposed`; `accepted` = gate | Ноль новой структуры; уже enforced валидатором; anti-inflation | Нет визуальной группировки provisional |
| B. Именной префикс | `standards/provisional-<name>.md` | Заметно в листинге | Дублирует статус; при `accepted` — переименование и rewrite ссылок |
| C. Подкаталог | `standards/provisional/<name>.md` | Явная группировка | Требует 2FA-обоснования для подкаталога в плоском `standards/`; переезд при `accepted` |

**Рекомендация.** Базово — **Опция A** (статус `draft`/`proposed` как маркер
provisional), при желании дополненная строкой в реестре/`README` стандартов и
пометкой в [artifact-map](../../governance/artifact-map.md). Опция C
резервируется как эскалация **только** при доказанной review-pain (порог 2FA),
по тому же принципу anti-inflation, что и профили в
[analysis-standard.md](../../standards/analysis-standard.md) (триггер B).
Переход provisional → accepted оформляется отдельным decision gate (RFC/ADR), а
не правкой файла на месте.

## 6. Матрица миграции артефактов (As-Is → To-Be)

Целевые каталоги по **типу артефакта** взяты из таблицы маршрутизации
[ADR-002 §«Правила маршрутизации документов»](../adr/2026-06-adr-002-artifact-document-methodology.md);
структурная цель корня — из
[ADR-001](../adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md).
Матрица — по **классам артефактов**, не по каждому файлу (пофайловый инвентарь —
задача исполнения RFC B-034; content-over-path остаётся принципом routing).

| Класс артефакта | As-Is путь (Хаб) | To-Be путь | Обоснование (источник) | Статус |
| --- | --- | --- | --- | --- |
| ADR | `docs/adr/YYYY-MM-adr-NNN-name.md` | `docs/adr/…` | ADR-002 (ADR → `docs/adr/`) | 🟢 Совпадает |
| Analysis | `docs/analysis/YYYY-MM-DD-name.md` | `docs/analysis/…` | ADR-002; ADR-006/analysis-standard | 🟢 Совпадает |
| Audit-report | `docs/audit/…` | `docs/audit/…` | ADR-002 + ADR-004 v0.3 (split от `docs/report/`) | 🟢 Совпадает |
| Report / statistics | `docs/report/…` | `docs/report/…` | ADR-002 + ADR-004 (реконсиляция `docs/reports/`→`docs/report/`) | 🟢 Совпадает |
| Research | `research/<domain>/YYYY-MM-DD-name.md` | `research/<domain>/…` | ADR-002; ADR-003 | 🟢 Совпадает |
| Research evidence | `research/<domain>/exp/<issue-slug>/` | без изменений | ADR-002 addendum B-019; ADR-003 | 🟢 Совпадает |
| Standard | `standards/<name>.md` | `standards/…` | ADR-001 ядро; ADR-002 (Standard → `standards/`) | 🟢 Совпадает |
| RFC (Хаб) | `governance/rfc/…` | `docs/rfc/…` | ADR-002 (RFC → `docs/rfc/`; Хаб держит `governance/rfc/` до миграции) | 🟠 Мигрировать |
| AI rule | `AI_GOVERNANCE.md`, `practices/agent-work/*` | `ai-rules/` | ADR-002 (AI rule → `ai-rules/`); ADR-001 ядро | 🟠 Выделить |
| AI policy / compliance | `AI_GOVERNANCE.md`, `practices/ai-governance/*` | `ai-governance/` (+ `GOVERNANCE.md`) | ADR-001 ядро | 🟠 Расщепить |
| Task/PR/review mgmt | `governance/backlog.md`, часть `governance/` | `pr-ops/` | ADR-001 ядро (`pr-ops/`) | 🟠 Расщепить |
| Operational knowledge | — / рассыпано | `kb/` (`taxonomy/roles/rules/processes/{name}/patterns/`) | ADR-002 (Operational knowledge → `kb/`) | 🟠 Ввести по факту |
| Run record | `experiments/`, `projects/*/` частично | `runs/` | ADR-002 (Run record → `runs/`); граница `exp/` vs `runs/` (B-019) | 🟡 Уточнить пофайлово |
| Template | `templates/…` | `templates/…` | ADR-002; ADR-001 ядро | 🟢 Совпадает |
| Tool/validator | `tools/…` | `tools/…` | ADR-002; ADR-001 ядро | 🟢 Совпадает |
| Practice | `practices/…` | `practices/` **или** `docs/practice/` | ADR-001: `practices/` — базовое расширение A; ядро — `docs/practice/` | 🟡 Human decision |
| Guides | `guides/…` | `guides/` **или** `docs/` | Нет fixed decision в ADR-001/002 | 🟡 Human decision |
| Placeholder-каталоги | `frameworks/`, `education/` | — | Нет fixed decision | 🟡 Human decision |
| Published site | `website/`, `mkdocs.yml` | инфраструктура (оставить) | Публикационный слой; **не** признак Portal | 🟡 Подтвердить |
| Root-документы | `CONCEPT.md`, `AI_PROJECT_CONTEXT-Summary.md` | `docs/` / `research/` / `kb/` | Нет fixed decision | 🟡 Human decision |

**Замечание о реконсиляции набросков ADR-001.** ADR-001 в наброске ядра называет
`docs/reports/` (мн. ч.) и `docs/practice/`. Более поздние принятые решения
(ADR-004 v0.3 и ADR-002 v1.4) реконсилировали Reports-домен как **`docs/report/`
(ед. ч.) + `docs/audit/`**. Поэтому целевой строкой считается реконсилированный
вариант; текстовый набросок ADR-001 рекомендуется поправить в исполнении RFC
B-034 (мелкая правка, не архитектурное изменение).

## 7. Recommendations: рекомендуемые фазы внедрения

Физические перемещения выполняются **не здесь**, а сериями отдельных PR после
принятия миграционного RFC (DoD B-034: «separate plan, human decision and
physical migration PRs»). Рекомендуемая последовательность:

1. **Фаза 0 — Decision gate (RFC + ADR).** Оформить миграционный RFC на основе
   этого анализа; закрыть все 🟡-вопросы §4.3/§6 человеческим решением; при
   принятии — ADR о целевом корне Хаба. Без этого физическая миграция не
   стартует.
2. **Фаза 1 — Neutral introductions (низкий риск).** Ввести пустые/якорные
   целевые каталоги, не ломающие ссылки: `kb/`, `runs/`, `ai-rules/`,
   `GOVERNANCE.md`-якорь. Наполнение — по факту операционной боли (anti-inflation).
3. **Фаза 2 — RFC-переезд.** `governance/rfc/` → `docs/rfc/` с картой перехода и
   массовым rewrite ссылок; `governance/rfc/` держать как алиас/редирект до
   стабилизации ссылок.
4. **Фаза 3 — Governance split.** Расщепить `governance/` на `ai-governance/` +
   `pr-ops/`; перенести `backlog.md`, `artifact-map.md`, политики согласно §6.
5. **Фаза 4 — Reconcile 🟡-сущностей.** Практики (`practices/` ↔ `docs/practice/`),
   `knowledge/` ↔ `kb/`, `guides/`, `frameworks/`, `education/`, `experiments/`,
   root-документы — каждая по принятому в Фазе 0 решению, отдельными PR.
6. **Фаза 5 — Validators & map.** Обновить валидаторы, `artifact-map.md`,
   `repo-model.md`, `mkdocs.yml` под новую структуру (**отдельная задача**, вне
   границ issue #372 — «валидаторы не переделываем»).

Каждый физический PR — атомарный, с явным rollback (revert PR), и не смешивает
несколько фаз.

## 8. Стратегия обновления перекрёстных ссылок

1. **Инвентарь ссылок перед переездом.** Для каждого мигрируемого пути собрать
   входящие ссылки: markdown-ссылки на `*.md`, frontmatter
   `related_artifacts`/`based_on`, строки `require_text` в валидаторах,
   `mkdocs.yml` nav, `artifact-map.md`, `backlog.md`.
2. **Rewrite вместе с переносом.** Ссылки обновляются в том же PR, что и
   перемещение файла, чтобы валидатор
   `validate_internal_markdown_links` (все `*.md`-ссылки должны резолвиться) не
   ломался ни в одном промежуточном состоянии.
3. **Алиасы/редиректы на переходный период.** Пока `governance/rfc/` и
   `docs/rfc/` сосуществуют (ADR-001/002 допускают), держать редиректы/README-
   указатели, чтобы внешние ссылки не рвались.
4. **Синхронные реестры.** `artifact-map.md` (колонка пути + «Связанные
   артефакты»), `repo-model.md` (описание структуры), `mkdocs.yml` nav и
   `required_files`/allowlist валидатора обновляются в одном PR с переносом — иначе
   карта и дерево разойдутся (ADR-002 «Компромиссы»).
5. **Проверка после каждого PR.** Локальная валидация обязательна:
   `./tools/validate-frontmatter.sh .`, `./tools/validate-file-naming.sh`,
   `./tools/validate-repository-structure.sh`.
6. **Rollback.** Каждый PR обратим revert'ом; карта перехода в описании PR
   документирует As-Is → To-Be, чтобы revert восстанавливал ссылки согласованно.

## 9. Deep Think: сведение трёх экспертных оптик

| Оптика | Главный вклад | Ключевое ограничение, которое держит |
| --- | --- | --- |
| **Ecosystem Architect** | Хаб = архетип A; корневые каталоги — способность архетипа, не Portal; целевой корень = ядро + дельта A | Не смешивать Hub и Portal; Portal — профиль C в отдельном репозитории |
| **Data Migration Specialist** | Матрица As-Is → To-Be, фазность, rewrite ссылок в том же PR, rollback | Ни одного «большого взрыва»; атомарные обратимые PR; ссылки не рвутся в промежуточных состояниях |
| **Governance Auditor** | Разделение fixed decision vs ambiguity; provisional-стандарты через lifecycle; anti-inflation и 2FA | 🟡-цели не мигрируются без human gate; валидаторы не переделываются в рамках issue #372 |

## 10. Соответствие DoD issue #372

| Требование issue #372 | Где закрыто |
| --- | --- |
| Найден «крайний документ» и дана интерпретация | §1, §3 (ADR-001 + спутник ADR-002) |
| Архитектура корня с дельтой от базы, без смешения Hub/Portal | §4 (особенно §4.2 фиксация Portal ≠ Hub) |
| Механизм provisional-стандартов | §5 |
| Матрица миграции As-Is → To-Be с обоснованием по источнику | §6 |
| Рекомендуемые фазы внедрения | §7 |
| Стратегия обновления перекрёстных ссылок | §8 |
| Deep Think: Ecosystem Architect / Data Migration Specialist / Governance Auditor | §9 (и сквозь §4–§8) |
| Не двигать файлы, не переделывать валидаторы, не считать R/A/A источником | §2.1 границы; §3.1 вердикт; §7 Фаза 5 вынесена за границы |
| Двусмысленные цели явно помечены на координацию | 🟡 в §4.3, §6 |
| Отчёт-план как `docs/analysis/YYYY-MM-DD-hub-migration-and-root-structure-plan.md` | Этот файл (2026-07-04) |

## 11. Related Artifacts

- [ADR-001: Методология инфраструктуры проектов экосистемы](../adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md)
  — источник истины о целевой структуре корня, архетипах A–D и переходном режиме Хаба.
- [ADR-002: Методология создания и управления артефактами](../adr/2026-06-adr-002-artifact-document-methodology.md)
  — целевой каталог по типу артефакта (routing), граница `exp/` vs `runs/`.
- [ADR-003: Структура research](../adr/2026-07-adr-003-research-structure.md),
  [ADR-004: Reports](../adr/2026-07-adr-004-reports-structure.md),
  [ADR-005: Audit](../adr/2026-07-adr-005-audit-structure.md),
  [ADR-006: Analysis](../adr/2026-07-adr-006-analysis-structure.md)
  — уточняют routing по типам (нормируют внутреннюю форму, не структуру корня).
- [research/hub/2026-06-23-repository-structure-concept.md](../../research/hub/2026-06-23-repository-structure-concept.md)
  — источник rationale архетипов (reviewed, не норма).
- [standards/analysis-standard.md](../../standards/analysis-standard.md)
  — формат этого Analysis-документа (interpretation layer, границы).
- [standards/project-structure-inheritance.md](../../standards/project-structure-inheritance.md)
  — правила подкаталогов в `projects/{project}/`.
- [governance/repo-model.md](../../governance/repo-model.md)
  — описание действующей (As-Is) структуры и anti-inflation.
- [governance/artifact-map.md](../../governance/artifact-map.md)
  — карта артефактов, синхронизируемая при миграции.
- [governance/backlog.md](../../governance/backlog.md)
  — B-034 (этот план), зависимости B-018/B-027/B-032, координация с B-028/B-033/B-044.
- Issues
  [#372](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/372) (эта задача),
  [#296](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/296)
  (разделение стандартизации и физической миграции).
</content>
