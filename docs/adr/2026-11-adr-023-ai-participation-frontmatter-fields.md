---
status: accepted
version: 1.0
updated: 2026-11-04
temperature: 0.1
owner: G-Ivan-A
decision-type: governance
contributors: [G-Ivan-A, konard]
ai-models: [claude-opus-5-5]
---

# ADR-023: Участие ИИ во frontmatter — поля `contributors` и `ai-models`, а не метка `ai-generated`

## Decision Metadata

| Field | Value |
| --- | --- |
| ADR id | ADR-023 |
| Decision type | governance |
| Decision status | accepted (машиночитаемый canon — frontmatter `status`); владелец выбрал вариант C в комментарии к PR [#728](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/728): «Q-1…Q-6 принимаю по рекомендациям» (Q-5) |
| Decision date | 2026-11-04 (принято; дата вступления — merge PR [#728](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/728)) |
| Owner | G-Ivan-A |
| Source | issue [#727](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/727), строка B-154 [`ops/backlog.md`](../../ops/backlog.md); предложение №9 [журнала решений](../analysis/2026-09-10-agents-md-hybrid-work-contract-analysis.md#recommendations) (issue [#569](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/569)); [выбор спринта](../analysis/2026-11-04-sprint-13-hub-normative-debt-selection.md) (F-5, Q-5) |
| Impacted artifacts | [`standards/frontmatter-standard.md`](../../standards/frontmatter-standard.md) (SSOT полей, v1.2), девять производных стандартов, `CONTRIBUTING.md`, `AGENTS.md`, `templates/htom/AGENTS.md`, `templates/spoke/AGENTS.md`, `tools/validate-frontmatter.sh`, `tools/test-frontmatter-validator.sh` |
| Supersedes | none |
| Superseded by | none |
| Дополняет | [ADR-002](2026-06-adr-002-artifact-document-methodology.md) — frontmatter остаётся necessary and sufficient; [ADR-008](2026-07-adr-008-standard-meta-structure.md) — правило поля живёт в одном стандарте, остальные ссылаются на него |

## Context

Запрет `ai-generated` во frontmatter действует с v1.0
[Frontmatter Standard](../../standards/frontmatter-standard.md): метка «создано
ИИ» ничего не говорит о том, кто проверил содержание. Валидатор отклоняет поле
в любом классе документа.

Владелец репозитория предложил разрешить `ai-generated`, если frontmatter
называет людей-участников (команды, роли) и конкретную модель ИИ
(предложение №9, issue #569). PR #570 предложение не реализовал: запрет записан
не в одном файле, и правка одного `AGENTS.md` расколола бы геном.

| Пробел | Наблюдение |
| --- | --- |
| G-1. Нет места для участников | Кто вёл работу и какая модель участвовала, сейчас видно только в issue, PR и changelog. Из самого документа этого не узнать |
| G-2. Норма размножена | Запрет записан в 14 местах: 10 стандартов, `CONTRIBUTING.md`, `AGENTS.md` и два `AGENTS.md` генома (находка F-5 выбора спринта). Любое решение меняет их все разом |
| G-3. Метка не равна ответственности | `ai-generated: true` не называет ни ответственного, ни модель. Поэтому запрет и введён |

## Decision

**Вариант C.** Метка `ai-generated` остаётся запрещённой. Участие ИИ
записывается двумя полями:

| Поле | Значение | Правило |
| --- | --- | --- |
| `contributors` | Люди, команды или роли, которые вели работу и отвечают за результат. Скаляр или inline-список `[a, b]` | Непустое; обобщённая метка (`ai`, `llm`, `bot`, `true`, `unknown` и т. п.) не допускается |
| `ai-models` | Конкретные модели ИИ, участвовавшие в работе. Скаляр или inline-список | Только вместе с `contributors`; каждый элемент — идентификатор модели с версией (`claude-opus-5-5`, `gpt-5.1`), а не семейство (`claude`, `gpt`) |

Правила:

1. Оба поля **необязательны**. Документ без них валиден, как и раньше.
   Provenance в issue, PR и changelog по-прежнему достаточна.
2. Если указано `ai-models`, **ДОЛЖНО** быть указано и `contributors`. У вывода
   модели всегда есть названный ответственный.
3. Поля допустимы во всех собственных классах метаданных Хаба (knowledge,
   audit, governance, RFC, ADR, standard, template, guide, practice, default).
   Внешние форматы — issue form, команда OpenCode, пакет исполнения GigaCode —
   задают свой набор полей сами, и новые поля там не допускаются.
4. Нормативный текст полей живёт в одном месте — обязательство 5
   [Frontmatter Standard](../../standards/frontmatter-standard.md#обязательства)
   v1.2. Остальные стандарты, `CONTRIBUTING.md` и три `AGENTS.md` ссылаются на
   него и называют замену метки, а не повторяют правило.

## Decision Drivers

- Предложение владельца требовало именно двух сведений: названных людей и
  конкретной модели. Вариант C даёт оба, а вариант B к ним добавляет метку,
  которая не несёт информации.
- Индустрия описывает происхождение через агента и роль, а не через бинарный
  флаг. В [W3C PROV-O](https://www.w3.org/TR/prov-o/) это
  `prov:wasAttributedTo` и `prov:wasAssociatedWith` с агентом-исполнителем. В git
  соавторов называют трейлером
  [`Co-authored-by`](https://docs.github.com/en/pull-requests/committing-changes-to-your-project/creating-and-editing-commits/creating-a-commit-with-multiple-authors).
- [EU AI Act, ст. 50](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)
  требует раскрывать сгенерированный ИИ контент в публичных текстах. Поле
  `ai-models` даёт для этого машиночитаемый источник, без бинарной метки.
- Валидатор уже ловит запрещённое поле. Новые поля проверяются там же, а
  обобщённые значения отклоняются машинно. Иначе поля выродились бы в ту же
  метку `ai-models: ai`.

## Alternatives Considered

| Вариант | Суть | Почему не выбран |
| --- | --- | --- |
| A. Оставить запрет без полей | Provenance только в issue, PR и changelog | Не закрывает G-1: из документа не видно ни ответственных, ни модели. Предложение владельца остаётся без ответа |
| B. Разрешить `ai-generated` с обязательными участниками | Метка плюс поля людей и модели | Метка дублирует `ai-models` и снова подсказывает, что «сгенерировано» — свойство качества. Нужны три поля там, где хватает двух |
| **C. Поля `contributors` и `ai-models`, метка запрещена** | Названные люди и конкретная модель | **Выбран** |

## Consequences

- Frontmatter Standard v1.2 определяет поля в обязательстве 5. Запрет
  `ai-generated` сохраняется дословно.
- Девять производных стандартов, `CONTRIBUTING.md` и три `AGENTS.md` (Хаб,
  `templates/htom/`, `templates/spoke/`) ссылаются на поля как на замену метки.
  Геном получает правку через `sync-metadata.json` и манифест.
- `tools/validate-frontmatter.sh` разрешает поля в собственных классах,
  проверяет форму значения и связку `ai-models` → `contributors`. Сообщение о
  запрете `ai-generated` подсказывает замену.
- Блочные YAML-списки в этих полях не поддерживаются. Построчный разбор
  валидатора видит только inline-значения, и форма `[a, b]` записана в
  стандарте явно.
- Существующие документы не правятся. Поля добавляются при следующем
  существенном изменении документа, если участие ИИ влияет на review.

## Compliance and Validation

| Проверка | Как |
| --- | --- |
| Метка запрещена | `tools/test-frontmatter-validator.sh`, случай «ai-generated ban»: `frontmatter field is forbidden: ai-generated` |
| Пара полей проходит | Случаи «ai participation fields (ADR-023)» (knowledge) и «ai participation fields on ADR» |
| `ai-models` без ответственного отклоняется | Случай «ai-models requires contributors» |
| Обобщённые и неверсионированные значения отклоняются | Случаи «ai-models generic label», «ai-models without version», «contributors generic label», «contributors block list» |
| Внешние форматы закрыты | Случай «ai participation fields outside own metadata formats» (команда OpenCode) |
| Геном согласован | `tools/validate-repository-structure.sh` закрепляет ссылки на ADR-023 в стандарте, `CONTRIBUTING.md` и трёх `AGENTS.md` |

## Lifecycle

| Переход | Условие |
| --- | --- |
| `accepted → superseded` | Хаб переходит на машиночитаемую provenance вне frontmatter (например, sidecar PROV-документ или аттестацию сборки), и поля дублируют её |
| Пересмотр | Обязательное раскрытие ИИ-контента по EU AI Act начинает касаться документов Хаба, и необязательных полей становится недостаточно |

## Related Artifacts

- [Frontmatter Standard](../../standards/frontmatter-standard.md) — нормативный текст полей.
- [Журнал решений AGENTS.md, предложение №9](../analysis/2026-09-10-agents-md-hybrid-work-contract-analysis.md#recommendations) — варианты A, B, C и рекомендация.
- [Выбор нормативного долга Спринта 13](../analysis/2026-11-04-sprint-13-hub-normative-debt-selection.md) — F-5 и Q-5.
- [`tools/validate-frontmatter.sh`](../../tools/validate-frontmatter.sh) и [`tools/test-frontmatter-validator.sh`](../../tools/test-frontmatter-validator.sh) — исполнимый контракт.
