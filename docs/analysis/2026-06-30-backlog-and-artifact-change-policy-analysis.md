---
status: draft
version: 0.2
updated: 2026-07-04
temperature: 0.1
type: internal-analysis
context: [hub, backlog, pr-ops, governance, artifact-lifecycle, issue-297, issue-392]
method: dialogue-analysis + repository-review + industry-practice-comparison
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/297"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/392"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/297"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/294"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/290"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/288"
related_artifacts:
  - "pr-ops/backlog.md"
  - "pr-ops/backlog-instruction.md"
  - "docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md"
  - "docs/adr/2026-06-adr-002-artifact-document-methodology.md"
  - "research/hub/2026-06-28-research-analysis-audit-inventory.md"
  - "docs/audit/2026-06-29-research-artifact-format-contract-audit.md"
  - "standards/file-naming.md"
  - "standards/frontmatter-docs-standard.md"
---

# Анализ: бэклог и политика изменений артефактов

> В issue указан путь `docs/analisis`. В активных контрактах Хаба используется
> `docs/analysis/`: этот путь закреплен в ADR-001/ADR-002, стандарте именования
> и валидаторе. Поэтому артефакт размещен в `docs/analysis/` как минимальная
> коррекция опечатки без создания параллельного каталога.

## 1. Введение

### 1.1. Причина

Диалог из issue #297 фиксирует две связанные гипотезы:

1. текущий `pr-ops/backlog.md` стал неудобен как рабочий backlog для
   AI-агента: он объединяет правила, активные спринты, исторические данные и
   объяснения в одном файле;
2. для изменений в согласованных артефактах не хватает легкой политики
   поправок: полный цикл `Analysis -> RFC -> ADR -> Standard` нужен не всегда,
   но автоматические правки без границ создают риск drift.

Текущий backlog действительно вырос до крупного документа: на момент анализа в
нем 1391 строка, включая контрактные правила, открытые вопросы, сводные таблицы,
детальные описания задач и новый sprint issue #294. Это уже не только список
работ, а смешанный planning + contract + history artifact.

Актуализация issue #392 от 2026-07-04 принимает backlog-specific часть этого
анализа: `pr-ops/backlog.md` остаётся active backlog, правила вынесены в
`pr-ops/backlog-instruction.md`, а история выполненных задач остаётся в GitHub
Issues/PR, `CHANGELOG.md` и самих артефактах. Отдельный архивный файл бэклога
не создаётся.

### 1.2. Цель

Зафиксировать анализ гипотез как базу для дальнейшей цепочки
`analysis -> proposal -> artifact`: подтвердить проблемы, отделить немедленные
действия от будущих решений, сравнить варианты с индустриальными практиками и
не создавать в этом PR новые RFC, ADR, стандарты или миграции.

### 1.3. Связанные артефакты

| Артефакт | Роль в анализе |
| --- | --- |
| [pr-ops/backlog.md](../../pr-ops/backlog.md) | До issue #392: доказательство смешения contract/data/history; после issue #392: active backlog. |
| [pr-ops/backlog-instruction.md](../../pr-ops/backlog-instruction.md) | Правила ведения бэклога, созданные по issue #392. |
| [ADR-001](../adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md) | Целевая структура с `pr-ops/` для задач, PR и review. |
| [ADR-002](../adr/2026-06-adr-002-artifact-document-methodology.md) | Lifecycle artifact changes и правило human decision gate. |
| [Research / Analysis / Audit inventory](../../research/hub/2026-06-28-research-analysis-audit-inventory.md) | Контекст различения research, analysis и audit. |
| [Research artifact format audit](../audit/2026-06-29-research-artifact-format-contract-audit.md) | Пример, где audit выявил drift между профилем и ADR-002. |
| Issue #294 / PR #295 | Последний пример: изменение зафиксировано в backlog, но не исполняет миграцию. |

### 1.4. Метод

Анализ основан на:

- полном чтении диалога из attachment issue #297;
- review текущего `pr-ops/backlog.md`, ADR-001, ADR-002, issue #288/#290/#294
  и PR #289/#291/#295;
- сопоставлении с industry patterns: native issue/project trackers, sprint
  backlog separation, small change review, ADR/RFC decision records and tiered
  change management.

Ограничение: исходный issue #297 был internal analysis. Он не принимал решение
за человека и не менял backlog, стандарты или целевую структуру. Addendum
issue #392 фиксирует отдельное принятое решение о backlog split.

## 2. Результаты анализа

### 2.1. Главный вывод

Обе гипотезы подтверждаются, но с разным уровнем срочности.

Проблема backlog подтверждена как **role overload**, а не как поломка
исполнения. В рамках issue #297 разбиение не выполнялось, но issue #392 позже
приняло минимальную декомпозицию без нового каталога: `pr-ops/backlog.md`
показывает только активные задачи, а `pr-ops/backlog-instruction.md` хранит
правила ведения. Исторический слой не дублируется в отдельном Markdown-файле:
источником истории остаются GitHub Issues/PR, `CHANGELOG.md` и сами артефакты.

Проблема политики изменений подтверждена сильнее. В ADR-002 есть общий lifecycle
`observation/source -> research/analysis -> RFC/proposal -> ADR/decision ->
standard/policy/template/validator/practice -> operational artifact/run`, но нет
операционного правила, когда допустима упрощенная правка, а когда нужен полный
цикл. Это создает два риска: governance paralysis для механических изменений и
неконтролируемый drift для "маленьких" смысловых правок.

### 2.2. Подтвержденные проблемы

| # | Проблема | Подтверждение | Вывод |
| --- | --- | --- | --- |
| 1 | Backlog смешивает contract, active work и history. | В одном `pr-ops/backlog.md` находятся правила обновления, открытые вопросы, активные задачи, закрытые элементы и детальные описания. | Нужна будущая декомпозиция, но не в этом PR. |
| 2 | Backlog не является native execution tracker. | Для B-016..B-023 есть planned rows, но нет отдельных issues; статусы живут в Markdown, а не в GitHub-native workflow. | Markdown backlog лучше держать как planning/rationale layer, execution вести issue/project-native. |
| 3 | Физический SSOT ошибочно приравнивается к одному файлу. | Диалог корректно указывает: logical SSOT может быть парой active file + instruction, если роли файлов явно закреплены. | Issue #392 изменяет правило "backlog = one file" на минимальную пару `backlog.md` + `backlog-instruction.md`, без архивного файла. |
| 4 | Нет amendment policy для правок канонических документов. | Последние задачи #288/#290/#294 показывают разный вес изменений: analysis-only, audit-only, backlog-only, future RFC/ADR/standard chain. | Нужна tiered policy, иначе один процесс пытается покрыть все случаи. |
| 5 | Валидаторы закрепляют текущую форму быстрее, чем методология успевает уточняться. | `tools/validate-repository-structure.sh` содержит allowlist активных файлов; новые валидируемые пути требуют явной регистрации. | Validator update должен быть частью каждого tier, но не должен сам принимать governance decision. |

### 2.3. Что не подтверждено

| Гипотеза | Почему не подтверждена |
| --- | --- |
| "SSOT теряется, если backlog перестаёт быть одним файлом." | SSOT - логическое свойство. Issue #392 сохраняет один active backlog и выносит только правила в соседний instruction-файл. |
| "Любой перенос backlog в `pr-ops/` требует нового RFC." | Если перенос только исполняет уже принятое ADR-001/ADR-007 target decision и меняет ссылки/пути без изменения смысла, это механическая поправка. Разделение ролей backlog всё равно требует явного human-approved решения; issue #392 стало таким решением. |
| "Нужен отдельный новый standard только для amendment process." | Сейчас достаточно будущего легкого policy section в существующем governance artifact after review. Новый стандарт будет оправдан только если правило начнет повторно применяться и вызывать review pain. |
| "Надо было менять backlog прямо в issue #297." | Issue #297 просил analysis report, а не миграцию. Backlog split корректно выполнен позже отдельным issue #392. |

### 2.4. Рекомендации

| # | Рекомендация | Куда фиксировать дальше | Почему |
| --- | --- | --- | --- |
| 1 | Не менять `pr-ops/backlog.md` в рамках issue #297. | PR #299 body | Scope issue: только analysis report. |
| 2 | Добавить future backlog item на модернизацию backlog после стабилизации research/routing chain. | Выполнено issue #392 как B-035 | Избегает смешения restructuring repo и restructuring task management в issue #297. |
| 3 | Для backlog выбрать hybrid model: GitHub Issues/PR для execution/history, `pr-ops/backlog.md` для active planning, `pr-ops/backlog-instruction.md` для правил. | Принято issue #392 | Совмещает native workflow и docs-as-code traceability без отдельного backlog archive file. |
| 4 | Ввести tiered amendment policy как правило в существующем governance artifact, не как новый standard. | `AI_GOVERNANCE.md` или `CONTRIBUTING.md` after review | Закрывает governance paralysis без artifact inflation. |
| 5 | Установить stop criteria: новый каталог, новый artifact class, новый lifecycle/status или изменение validator semantics переводят изменение в полный decision path. | Future policy text | Защищает от тихого drift. |

### 2.5. Открытые вопросы после issue #392

1. Где лучше закрепить amendment policy: в `AI_GOVERNANCE.md` как правило для
   AI-агентов или в `CONTRIBUTING.md` как правило для всех contributors?
2. Нужен ли GitHub Project для Hub backlog после разделения planning layer и
   execution layer?
3. Как часто закрывать логический sprint в active backlog: сразу после merge
   всех строк или только после явного review outcome?

## 3. Детализация

### 3.1. Проблема backlog: не один файл, а перегрузка ролей

Текущий backlog содержит полезный context, но он выполняет сразу четыре роли:

| Роль | Сейчас | Риск |
| --- | --- | --- |
| Contract | Раздел "Правила обновления бэклога" внутри файла. | Агент вынужден читать operational data, чтобы найти правила. |
| Active work | Сводная таблица задач и planned sprint B-016..B-023. | Активные задачи смешаны с архивом и rationale. |
| History | DONE tasks, длинные описания прошлых работ, sources. | История увеличивает token load для текущего исполнения. |
| Rationale | Обоснования приоритетов, цепочки зависимостей, критический путь. | Полезно для review, но шумит при простом обновлении статуса. |

Диалог правильно оспаривает аргумент "не один файл разрушает SSOT". SSOT не
обязан быть физически одним Markdown-файлом. Issue #392 принимает минимальную
модель без нового каталога:

```text
pr-ops/backlog.md              # текущие незавершенные спринты и задачи
pr-ops/backlog-instruction.md  # правила, определения, lifecycle, routing
GitHub Issues/PR + CHANGELOG.md + артефакты  # history and implementation evidence
```

Для AI-агента это снижает context pollution: обычный run читает active backlog
и при необходимости instruction-файл. Выполненная история не копируется в
Markdown-архив, потому что GitHub-native history и changelog уже дают
проверяемый след.

### 3.2. Native backlog: GitHub Issues/Projects vs Markdown

Industry practice в GitHub/Jira-like workflow разделяет:

- execution items: issue/task с assignee, status, labels, links, comments,
  history and automation;
- planning view: backlog, sprint, board, roadmap, project fields;
- rationale/docs: decisions, RFC/ADR, standards, reports.

Markdown backlog хорош как durable planning/rationale artifact. Но он слабее как
execution tracker:

| Критерий | Markdown backlog | GitHub-native Issues/Projects |
| --- | --- | --- |
| Review rationale | Сильный: можно хранить обоснования и зависимости в одном PR. | Средний: rationale рассыпается по issue body/comments unless curated. |
| Status tracking | Ручной: статус в таблице легко устаревает. | Сильный: статус, labels, assignee and automation are native. |
| AI context | Может быть тяжелым при росте файла. | Легче фильтровать по query, labels, milestone, project fields. |
| Auditability | Хороший git history. | Хороший issue/project history, но хуже как single Markdown narrative. |
| Validation | Можно проверять shell validators. | Нужны GitHub API checks или manual discipline. |

Вывод: future state должен быть hybrid. После issue #392
`pr-ops/backlog.md` хранит active planning, `pr-ops/backlog-instruction.md`
хранит правила, а GitHub Issues/PR хранят execution state and discussion
history. Это не отменяет backlog Markdown, а уточняет его роль.

### 3.3. Политика изменений: почему полный lifecycle не должен быть единственным путем

ADR-002 уже задает правильную базовую цепочку:

```text
observation/source
  -> research/analysis
  -> RFC/proposal
  -> ADR/decision
  -> standard/policy/template/validator/practice
  -> operational artifact/run
```

Но реальная работа показывает три разных класса изменений:

| Класс | Пример из последних задач | Почему один процесс не подходит |
| --- | --- | --- |
| Механика | Обновить ссылки и validator allowlist после accepted artifact. | RFC/ADR здесь создает bureaucracy without new decision. |
| Уточнение | Добавить explanation, status wording, routing example. | Полный цикл слишком тяжелый, но нужна проверка ripple effects. |
| Структурное решение | Новый каталог, новый standard, новая граница `exp/` vs `runs/`. | Без RFC/ADR появится drift и конкурирующие источники истины. |

Диалог предлагает 3-tier model. Анализ подтверждает ее как практичный компромисс,
но с уточнением stop criteria.

### 3.4. Предлагаемая 3-tier amendment model

| Tier | Назначение | Процесс | Stop criteria |
| --- | --- | --- | --- |
| Tier 1: mechanical / traceability | Исполнить уже принятое решение: ссылки, пути, имена, changelog, validator allowlist. | Agent делает grep/ripple scan, правит связанные references, запускает валидаторы, PR review. RFC не нужен. | Если обнаружено изменение смысла, новый путь вне accepted structure or validator semantics change -> Tier 2/3. |
| Tier 2: bounded clarification | Уточнить правило внутри уже принятого контракта: пример, формулировка, local exception. | Agent фиксирует affected artifacts, вносит малую правку, PR требует human review. RFC обычно не нужен. | Если задеты >3 active artifacts, добавляется новое поле frontmatter/status/artifact type, меняется routing or lifecycle -> Tier 3. |
| Tier 3: structural / semantic | Изменить смысл, добавить новый каталог/тип артефакта, заменить стандарт, изменить decision boundary. | Analysis -> RFC/proposal -> ADR/decision -> standard/policy/template/validator, then migration. | No bypass: решение принимает человек. |

Пример применения:

- перенос ссылок после accepted ADR - Tier 1;
- добавление пояснения в `CONTRIBUTING.md`, что issue typo `analisis` maps to
  `analysis`, - Tier 2;
- разделение backlog на active file + instruction без отдельного history-файла
  - Tier 3, потому что меняется модель управления задачами;
- чистое обновление ссылок после принятого backlog split может быть Tier 1,
  если не меняет модель управления задачами.

### 3.5. Последовательность действий, которую поддерживает анализ

Диалог в issue приходит к правильной последовательности:

1. В рамках issue #297 не менять backlog format.
2. Сначала завершить уже зафиксированный research/routing sprint B-016..B-023.
3. Затем отдельно рассмотреть модернизацию backlog и amendment policy.
4. После human decision выполнить минимальную декомпозицию файлов, ссылок and
   validators.

Это согласуется с ADR-001 transition mode: текущий Хаб сохраняет старые пути до
отдельного решения о физической миграции. Это также согласуется с PR #295:
новый sprint записан как план, но сам не создает RFC/ADR/standard and does not
migrate files.

### 3.6. Статус после issue #392

Issue #392 supersedes the earlier future-item draft for backlog modernization.
Текущий статус:

| Решение | Статус | Evidence |
| --- | --- | --- |
| Active backlog отделён от правил ведения | implemented | `pr-ops/backlog.md`, `pr-ops/backlog-instruction.md`, issue #392 |
| Отдельный архивный файл бэклога не создаётся | accepted | `pr-ops/backlog-instruction.md`, issue #392 |
| Amendment policy остаётся отдельной governance-задачей | active | B-036 в `pr-ops/backlog.md` |

## 4. Industry practices

| Практика | Что полезно для Хаба | Ограничение |
| --- | --- | --- |
| GitHub Issues/Projects | Native execution state: issue status, labels, project fields, comments, PR links and automation. | Не заменяет governance rationale; нужен curated docs layer. |
| Jira/Scrum backlog pattern | Разделяет product backlog, sprint backlog and completed work history. | Heavy process не нужен целиком; полезен принцип separation of active vs historical. |
| GitHub Flow / small PR review | Change goes through branch, PR, checks and review; small changes easier to reason about. | Не классифицирует governance severity; нужен local tier rule. |
| ADR/RFC practices | Structural decisions need explicit decision records and rationale. | Не стоит применять к mechanical link/path updates. |
| ITIL-style change classes | Standard/normal/emergency change classes show that not every change needs the same ceremony. | ITSM process too heavy for this repo; берем только идею tiering. |

Практический synthesis: для knowledge/governance repository нужен
docs-as-code workflow plus native issue tracking plus lightweight change
classification. Ни один внешний подход не надо копировать целиком.

## 5. Definition of Done issue #297

| Requirement | Status | Evidence |
| --- | --- | --- |
| Проанализировать диалог | done | sections 1-3 summarize and test both hypotheses. |
| Выявить проблемы | done | section 2.2. |
| Подтвердить проблемы | done | section 2.2 and 3.1-3.3 link problems to repository state. |
| Изучить варианты решений в индустриальных практиках | done | section 4. |
| Создать analytical report | done | this file. |
| Не создавать standards/RFC/other new decision artifacts | done | for issue #297: no backlog migration, RFC, ADR or standard created. Issue #392 addendum is tracked separately. |

## 6. Источники

### Internal

- Issue #297:
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/297>
- Current backlog:
  [pr-ops/backlog.md](../../pr-ops/backlog.md)
- ADR-001:
  [docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md](../adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md)
- ADR-002:
  [docs/adr/2026-06-adr-002-artifact-document-methodology.md](../adr/2026-06-adr-002-artifact-document-methodology.md)
- Research / Analysis / Audit inventory:
  [research/hub/2026-06-28-research-analysis-audit-inventory.md](../../research/hub/2026-06-28-research-analysis-audit-inventory.md)
- Research artifact format contract audit:
  [docs/audit/2026-06-29-research-artifact-format-contract-audit.md](../audit/2026-06-29-research-artifact-format-contract-audit.md)
- Issue #294:
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/294>
- PR #295:
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/295>

### External

- GitHub Docs - Issues:
  <https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues>
- GitHub Docs - Projects:
  <https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects>
- GitHub Docs - GitHub Flow:
  <https://docs.github.com/en/get-started/using-github/github-flow>
- Atlassian Support - Jira Software backlog:
  <https://support.atlassian.com/jira-software-cloud/docs/use-your-scrum-backlog/>
- Google Engineering Practices - Small CLs:
  <https://google.github.io/eng-practices/review/developer/small-cls.html>
- Michael Nygard - Documenting Architecture Decisions:
  <https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
- MADR:
  <https://github.com/adr/madr>
- Atlassian ITSM - Types of change management:
  <https://www.atlassian.com/itsm/change-management/types>
