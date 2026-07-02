---
status: accepted
version: 1.2
updated: 2026-07-02
temperature: 0.1
owner: G-Ivan-A
decision-type: methodology
---

# ADR-002: Методология создания и управления артефактами

## Контекст

Issue #276 требует зафиксировать методологию создания артефактов, прежде всего
документов, с учетом согласованных исследований, всех инициированных в
экосистеме типов документации и принципов human/AI управления.

Входящие документы:

- [research/hub/2026-06-23-repository-structure-concept.md](../../research/hub/2026-06-23-repository-structure-concept.md);
- [research/hub/2026-06-25-artifact-inventory-and-classification.md](../../research/hub/2026-06-25-artifact-inventory-and-classification.md);
- [standards/frontmatter-standard.md](../../standards/frontmatter-standard.md);
- [standards/frontmatter-docs-standard.md](../../standards/frontmatter-docs-standard.md);
- [standards/file-naming.md](../../standards/file-naming.md).

Исследования показали риск смешения research, RFC, ADR, standard, contract,
prompt и run-record в одном каталоге или под одной "L1-L4" лестницей. Этот ADR
фиксирует общий lifecycle и правила маршрутизации.

## Решение

Принять графовую методологию управления артефактами:

```text
observation/source
  -> research/analysis
  -> RFC/proposal
  -> ADR/decision
  -> standard/policy/template/validator/practice
  -> operational artifact/run
```

Это не жесткий конвейер. Допустимы возвраты: ADR может потребовать новое
исследование, стандарт может породить валидатор, run-record может открыть новый
analysis. Но переход "исследование стало нормой" всегда проходит через явное
решение человека: RFC или ADR.

## Оси классификации

Каждый новый активный артефакт классифицируется минимум по пяти вопросам:

| Вопрос | Ось | Примеры значений |
| --- | --- | --- |
| Что это делает? | Тип/функция | research, analysis, report, RFC, ADR, standard, policy, contract, template, prompt, practice, manifest, run |
| Кто или что это исполняет? | Уровень исполнимости | IL-0, IL-1, IL-2, IL-3 |
| Где это применимо? | Scope/архетип | repo-wide, hub, spoke, archetype A-D, project-specific |
| Насколько это зрелое или принятое? | Lifecycle status | Knowledge: `draft`, `reviewed`, `canonical`, `superseded`; Governance: `draft`, `proposed`, `accepted`, `rejected`, `deprecated`, `superseded` |
| Кто принимает решение? | Governance owner | human decision, AI draft, validator check, project owner |

Уровни исполнимости принимаются в формулировке issue #276:

| Уровень | Формат | Сущности | Размещение |
| --- | --- | --- | --- |
| IL-0 | YAML/JSON манифесты | реестры, artifact-map, README | корень каталога |
| IL-1 | машинно-валидируемый формат | контракты, правила, таксономии | корень контекста исполнения |
| IL-2 | executable Markdown | промпты, инструкции | рядом с IL-1 в процессе |
| IL-3 | explanatory Markdown | стандарты, RFC, ADR, аналитика | `docs/`, `standards/`, `research/` |

IL-1 не ограничивается YAML/JSON. Допустимы Rego, JSON Schema, OpenAPI,
Markdown с RFC 2119/BCP 14, IDL и другие форматы, если они реально проверяемы
человеком, AI-агентом или инструментом.

## Правила маршрутизации документов

| Тип артефакта | Каноническое размещение | Правило |
| --- | --- | --- |
| Research Хаба | `research/{domain}/YYYY-MM-DD-name.md` | Evidence и варианты, не норма. |
| Analysis в проекте/spoke | `docs/analysis/YYYY-MM-DD-name.md` | Исследование локального контекста без статуса решения. |
| Report | `docs/reports/` | Результат проверки, аудита, статистики или выполнения. |
| RFC | `docs/rfc/` для новых HTOM/spoke; текущий Хаб сохраняет `governance/rfc/` до миграции | Proposal до решения. |
| ADR | `docs/adr/YYYY-MM-adr-NNN-name.md` | Принятое решение и rationale. |
| Standard | `standards/` | Повторяемая норма формата, качества или review-критерия. |
| AI rule | `ai-rules/` | Правило поведения AI-агента; плоско, если нет 2FA-обоснования. |
| Operational knowledge | `kb/` | Операционно применимые знания для процесса, агента или валидатора. |
| Process prompt | `kb/processes/{name}/prompt.md` | Промпт связан с процессом и исполняется вместе с ним. |
| Standalone prompt | `prompts/` в архетипе B | Промпт является самостоятельным библиотечным активом. |
| Run record | `runs/` | Факт выполнения, данные, результаты эксперимента или task run. |
| Template | `templates/` | Копируемая поверхность для bootstrap или повторяемого артефакта. |
| Tool/validator | `tools/` | Воспроизводимая проверка или maintenance script. |

Если файл не попадает в таблицу, исполнитель сначала добавляет вопрос в issue
или RFC. Не создавать новый корневой каталог только ради визуальной полноты.

## Addendum B-019: граница `exp/` vs `runs/`

Это addendum фиксирует в контексте ADR-002 принятое решение
[ADR-003](2026-07-adr-003-research-structure.md) по границе между
research evidence corpus и operational run record. Rationale, альтернативы и
trade-offs остаются в
[RFC B-016](../../governance/rfc/2026-06-30-rfc-research-structure.md), раздел
P3; здесь они не дублируются.

Routing-таблица выше сохраняет строку `Run record` для `runs/`: это контейнер
операционной записи о факте выполнения задачи, бизнес-процесса или pipeline.
ADR-003 добавляет уточнение: воспроизводимая доказательная база, которая
существует ради утверждения в research-отчёте, не является `Run record` по
семантике ADR-002 и размещается в `research/<domain>/exp/<issue-slug>/`.

| Контейнер | Назначение | Привязка | Семантика |
| --- | --- | --- | --- |
| `research/<domain>/exp/<issue-slug>/` | Research evidence corpus: воспроизводимая доказательная база, обосновывающая утверждение в research-отчёте. | Всегда ссылается на parent dated report. | «Докажи знание»: артефакт существует ради knowledge claim. |
| `runs/` | Operational run record: факт выполнения операционной/бизнес-задачи или pipeline, его данные и результаты. | Не обязан быть привязан к research-отчёту. | «Зафиксируй выполнение»: артефакт существует ради записи прогона. |

Нормативный критерий разведения — один вопрос исполнителю:

> Этот артефакт существует, чтобы **доказать утверждение в research-отчёте**
> (→ `exp/`), или чтобы **зафиксировать факт выполнения операционной/бизнес-задачи
> или pipeline** (→ `runs/`)?

Граничный случай: research-эксперимент технически тоже может быть прогоном, но
если его цель — доказательная база для knowledge claim, он идёт в `exp/`.
Операционная задача, которая производит данные для последующего анализа,
остаётся в `runs/`; research-отчёт может цитировать такой `runs/` как источник
данных, но не поглощает operational run record внутрь `exp/`.

Это addendum не меняет lifecycle `runs/`, не выполняет физическую миграцию
legacy `research/<domain>/exp-*` и не вводит новый корневой каталог. Нормативное
правило структуры research evidence кодифицируется в
[Research Standard](../../standards/research-standard.md), а ADR-002 сохраняет
границу маршрутизации артефактов.

## Правила создания артефакта

Перед созданием файла исполнитель фиксирует:

1. цель артефакта и потребителя;
2. тип/функцию и уровень исполнимости;
3. источник или upstream decision;
4. expected lifecycle status;
5. место размещения и ссылку на ближайший стандарт;
6. проверку, которая подтвердит корректность размещения.

Markdown-артефакт с frontmatter обязан иметь базовые поля `status`, `version`,
`updated`, `temperature` и обязательные поля своего класса из
[frontmatter-docs-standard.md](../../standards/frontmatter-docs-standard.md).
Governance-артефакты добавляют `owner`; ADR добавляет `decision-type`; RFC
добавляет `rfc-scope`. Дополнительные поля добавляются только если их
потребляет валидатор, шаблон, provenance rule или документный класс.

## Human/AI governance

| Действие | Human | AI | Валидатор |
| --- | --- | --- | --- |
| Создать draft/research/proposal | утверждает scope или issue | может подготовить текст и варианты | проверяет формат |
| Перевести knowledge `draft` в `reviewed` | выполняет или подтверждает review | может обновить ссылки и traceability | проверяет frontmatter и links |
| Перевести knowledge в `canonical` или governance в `accepted` | принимает решение | не принимает самостоятельно | проверяет структуру и регистрацию |
| Создать ADR | принимает решение или фиксирует уже принятое | оформляет record и rationale | проверяет naming/frontmatter/map |
| Создать standard/validator | подтверждает норму и scope | реализует и тестирует | исполняет проверку |

AI-авторство не является обязательным полем каждого документа. Если provenance
важен, он фиксируется в issue, PR, changelog или audit. Решение остается за
человеком, а AI может готовить анализ, варианты, черновики и механические
обновления ссылок.

## Статусы входящих документов

| Документ | Новый статус | Причина |
| --- | --- | --- |
| `research/hub/2026-06-23-repository-structure-concept.md` | `reviewed` | Выводы рассмотрены и зафиксированы в ADR-001. |
| `research/hub/2026-06-25-artifact-inventory-and-classification.md` | `reviewed` | Выводы рассмотрены и зафиксированы в ADR-002. |

Открытые вопросы из этих исследований не копируются целиком в ADR. Если вопрос
остается актуальным и требует выбора, он должен стать отдельным RFC или issue с
явной границей решения.

## Последствия

Положительные:

- research перестает выглядеть как действующая норма без decision gate;
- ADR становится местом принятых решений, а standards - местом обязательных
  форматов и критериев;
- AI-агенты получают проверяемый алгоритм выбора места для нового документа;
- статус `reviewed` у входящих исследований отражает, что они использованы как
  rationale и переведены в решение.

Компромиссы:

- часть текущих RFC Хаба пока остается в `governance/rfc/`, а новые целевые
  правила называют `docs/rfc/`;
- физическая миграция existing artifacts требует отдельного плана;
- валидаторы должны обновляться вместе с появлением новых accepted governance
  или canonical knowledge артефактов,
  иначе карта артефактов и дерево будут расходиться.
