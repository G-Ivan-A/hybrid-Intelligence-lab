---
status: proposed
version: 0.2
updated: 2026-07-17
temperature: 0.1
owner: G-Ivan-A
executable: false
scope: repo-wide
related_standards:
  - "frontmatter-docs-standard.md"
  - "file-naming.md"
  - "glossary.md"
  - "evals-contract-standard.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/374"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/417"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/423"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/435"
---

# Standard Meta-Structure Standard

## Purpose

Этот мета-стандарт задаёт единый нормативный каркас F10 explicit для **всех
стандартов экосистемы**. Он превращает решение
[ADR-008](../docs/adr/2026-07-adr-008-standard-meta-structure.md) в reusable
контракт создания, review и последующей автоматической валидации стандартов.

Стандарт фиксирует только принятую структуру. Он не меняет содержание
существующих стандартов и не принимает новых архитектурных решений.

## Scope

Правила обязательны для **каждого стандарта экосистемы** — любого документа
класса `Standard` по [Frontmatter Docs Standard](frontmatter-docs-standard.md),
то есть файла в `standards/`, который нормирует форму артефакта или процесса.
Область не ограничена Research/Analysis/Audit/Report: ADR-008 распространяет
F10 на все стандарты, включая Evals Contract.

| Группа | Файлы | Состояние |
| --- | --- | --- |
| Sibling standards R/A/A/Report | `standards/research-standard.md`, `standards/analysis-standard.md`, `standards/audit-standard.md`, `standards/report-standard.md` | Мигрируются в B-053 |
| Evals Contract | `standards/evals-contract-standard.md` | Уже применил F10 добровольно как forward-compatible форму; вопрос Q5 этого файла закрыт настоящим scope |
| Прочие стандарты `standards/` | Остальные файлы класса `Standard` | Приводятся к F10 при следующем существенном изменении либо отдельной задачей |
| Новые стандарты | Любой стандарт, создаваемый после принятия этого документа | F10 обязателен с первой версии |

Мета-стандарт нормирует **структуру**, а не содержание: он не переписывает
правила существующих стандартов. Физическая миграция четырёх sibling standards
и реализация их структурной проверки относятся к B-053 и находятся вне scope
B-052. Этот файл также не заменяет общие правила создания и маршрутизации
артефактов из
[ADR-002](../docs/adr/2026-06-adr-002-artifact-document-methodology.md).

## Identification and Placement

| Элемент | Правило |
| --- | --- |
| Canonical path | `standards/standard-meta-structure.md`. |
| Artifact class | Governance standard, IL-3 explanatory Markdown в `standards/`. |
| Governed artifacts | Все стандарты экосистемы — файлы класса `Standard` в `standards/`, см. `Scope`. |
| Naming | kebab-case по [file-naming.md](file-naming.md); стандарт не является date-first артефактом, потому что это живой контракт, а не датированное наблюдение. |
| Normative source | ADR-008; при расхождении ADR-008 имеет приоритет. |
| General artifact methodology | ADR-002. |

Название файла является стабильным адресом мета-стандарта. Governed standards
ДОЛЖНЫ ссылаться на него после приведения к F10.

## Frontmatter

Каждый governed standard ДОЛЖЕН использовать necessary and sufficient
frontmatter для класса `Standard` из
[Frontmatter Docs Standard](frontmatter-docs-standard.md):

```yaml
---
status: draft
version: 0.1
updated: YYYY-MM-DD
temperature: 0.1
owner: Human owner or owning group
---
```

Дополнительные поля разрешены только когда их потребляет validator, index,
template или другой активный governance contract. `ai-generated` во
frontmatter ЗАПРЕЩЁН. `status` ДОЛЖЕН использовать governance vocabulary:
`draft`, `proposed`, `accepted`, `rejected`, `deprecated` или `superseded`.

## Minimum Body Sections

После H1-заголовка каждый governed standard ДОЛЖЕН содержать ровно по одному
экземпляру следующих десяти инвариантных H2-разделов и строго в указанном
порядке:

1. `Purpose`;
2. `Scope`;
3. `Identification and Placement`;
4. `Frontmatter`;
5. `Minimum Body Sections`;
6. `Type Model`;
7. `Lifecycle`;
8. `Boundaries`;
9. `Validation`;
10. `Related Artifacts`.

Все десять разделов обязательны. Если для любого инвариантного раздела нет
применимого содержания, раздел ДОЛЖЕН содержать `N/A` и краткое rationale,
объясняющее неприменимость. Пустой раздел или отсутствие раздела недопустимы.

Specific tail разрешён только после `Related Artifacts`. Каждый дополнительный
H2-раздел ДОЛЖЕН в первом абзаце содержать формально проверяемую Markdown
cross-reference на конкретное утверждение в `Purpose` или конкретную границу в
`Scope`, которую этот раздел реализует. Cross-reference должна указывать имя
целевого раздела и работоспособную ссылку на его heading anchor, например
`[Purpose](#purpose)` или `[Scope](#scope)`; простого упоминания недостаточно.

## Type Model

`model`. Собственная модель типа этого мета-стандарта имеет одну форму: он
описывает структуру стандартов и не разделяется на subtype profiles. Все
governed standards подчиняются одному и тому же F10-скелету независимо от того,
что именно они нормируют; отдельная форма для «стандарта о стандартах» не
вводится.

Нормативное правило для governed standards: раздел `Type Model` ДОЛЖЕН иметь
ровно одну из двух форм:

1. `model` — стандарт определяет модель типа; таблица subtype profiles, если
   она нужна, является частью этой формы;
2. `N/A` — модель типа неприменима; по общему правилу раздел также содержит
   краткое rationale.

Отдельная форма `profiles`, пустой раздел и любая третья форма запрещены.
Anti-inflation trigger относится либо к общей policy внутри формы `model`, либо
к конкретному разделу specific tail; выбранная привязка ДОЛЖНА быть явной.

## Lifecycle

Этот мета-стандарт использует governance-словарь из Frontmatter Docs Standard:

```mermaid
flowchart LR
  draft --> proposed --> accepted
```

До human acceptance его статус — `proposed`; merge PR является acceptance gate.
После принятия B-052 переходит в `review` и разблокирует B-053.

Governed standards используют тот же governance-словарь для собственного
`status`. Артефакты, которые они нормируют, живут в knowledge-словаре
(`draft → reviewed → canonical → superseded`) по
[ADR-002](../docs/adr/2026-06-adr-002-artifact-document-methodology.md);
смешивать эти два словаря в одном поле ЗАПРЕЩЕНО.

Изменение F10-инварианта, двух форм `Type Model`, правила `N/A + rationale`,
specific-tail rule или canonical boundary owner требует нового либо
superseding human decision record. Переход в `deprecated` или `superseded`
ДОЛЖЕН содержать ссылку на замену или rationale.

## Boundaries

Локальная delta этого мета-стандарта ограничена **структурой** стандартов
экосистемы из `Scope`: он задаёт их инвариантные H2-разделы, порядок, формы
`Type Model` и правило specific tail. Содержание норм каждого стандарта
остаётся за самим стандартом; мета-стандарт не решает, что стандарт нормирует.

[ADR-002](../docs/adr/2026-06-adr-002-artifact-document-methodology.md) остаётся
canonical owner общей таблицы artifact boundary и routing. Этот стандарт и
governed sibling standards НЕ ДОЛЖНЫ дублировать или переопределять общую
routing/boundary table; их `Boundaries` содержат только локальную delta и ссылку
на ADR-002.

## Validation

Validator применяется к каждому файлу класса `Standard` в `standards/` (см.
`Scope`) и ДОЛЖЕН проверять:

1. наличие всех десяти инвариантных H2-разделов;
2. уникальность каждого из десяти разделов;
3. их строгий порядок;
4. отсутствие дополнительных H2-разделов до `Related Artifacts`;
5. наличие в первом абзаце каждого specific-tail раздела формально проверяемой
   Markdown cross-reference на `Purpose` или `Scope`;
6. что `Type Model` использует только форму `model` или `N/A`;
7. что каждый пустой по смыслу инвариантный раздел содержит `N/A` и краткое
   rationale.

Validator проверяет наличие, позицию и формальную корректность specific-tail
cross-reference, но НЕ проверяет семантическую корректность связи с конкретным
утверждением `Purpose` или границей `Scope`. Эту корректность обязательно
подтверждает human review.

Порядок приведения к F10 не является правом validator: пока конкретный стандарт
не мигрирован, его несоответствие — известный долг B-053 или отдельной задачи, а
не скрытый дефект. Включение структурной проверки для файла ДОЛЖНО происходить
вместе с его миграцией, иначе validator блокирует репозиторий на работе, которая
ещё не запланирована.

До реализации B-053 текущий meta-standard проверяется общими локальными
командами:

```bash
bash tools/test-frontmatter-validator.sh
bash tools/test-smart-sync.sh
./tools/validate-file-naming.sh
./tools/validate-frontmatter.sh .
./tools/validate-repository-structure.sh
python3 tools/generate-manifest.py --check
```

## Related Artifacts

- [ADR-008: Мета-структура стандартов R/A/A/Report](../docs/adr/2026-07-adr-008-standard-meta-structure.md)
- [ADR-001: Методология инфраструктуры экосистемы](../docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md)
- [ADR-002: Методология создания и управления артефактами](../docs/adr/2026-06-adr-002-artifact-document-methodology.md)
- [Frontmatter Docs Standard](frontmatter-docs-standard.md)
- [File naming](file-naming.md)
- [Glossary](glossary.md)
- [Research Standard](research-standard.md)
- [Analysis Standard](analysis-standard.md)
- [Audit Standard](audit-standard.md)
- [Report Standard](report-standard.md)
- [Evals Contract Standard](evals-contract-standard.md) — прецедент
  добровольного применения F10 за пределами R/A/A/Report; его вопрос Q5 закрыт
  областью применения этого документа
- [Backlog](../pr-ops/backlog.md)
- [Artifact Map](../pr-ops/artifact-map.md)
- [Issue #423 / B-052: создание мета-стандарта](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/423)
- [Issue #435 / B-052: расширение области F10 на все стандарты экосистемы](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/435)
- [Issue #417: решение фаундера F10 explicit](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/417)
