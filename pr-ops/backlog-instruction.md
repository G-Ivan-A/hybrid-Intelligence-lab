---
status: canonical
version: 1.0
updated: 2026-07-04
temperature: 0.1
type: instruction
context: [governance, backlog, pr-ops, synchronization]
method: operating-contract
scope: repo-wide
related_artifacts:
  - "pr-ops/backlog.md"
  - "pr-ops/artifact-map.md"
  - "pr-ops/repo-model.md"
  - "CHANGELOG.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/392"
---

# Инструкция по ведению бэклога

`pr-ops/backlog.md` отвечает на вопрос: что делать, в какой логической
последовательности и с каким текущим статусом. Он не описывает подробно, как
выполнять задачу: детали живут в issue, PR, RFC, ADR, стандартах и changelog.

## Роли файлов

| Файл или система | Роль |
| --- | --- |
| `pr-ops/backlog.md` | Только активные задачи, сгруппированные в логические спринты. |
| `pr-ops/backlog-instruction.md` | Правила ведения бэклога, статусы, формат спринтов и archiving policy. |
| GitHub Issues/PR | Источник истины для выполненной истории, обсуждений, review and implementation evidence. |
| `CHANGELOG.md` | Историческая запись governance-изменений после merge. |
| `pr-ops/artifact-map.md` | Навигация по активным артефактам и связям. |

Архивный файл бэклога не создаётся. Дублировать GitHub history в отдельном
Markdown-архиве не нужно.

## Принципы

- **Синхронизация, не энциклопедия.** Бэклог нужен для координации founder -
  исполнитель - команда Q, а не для хранения полного rationale.
- **Факты вместо догадок.** Если нет источника для значения, ставь `null`.
- **Активное вместо исторического.** Выполненные задачи не остаются в активном
  backlog view после архивации спринта.
- **Логические цепочки вместо приоритетных корзин.** Спринт собирается вокруг
  причинно связанной работы, даже если внутри есть разные P-levels.
- **Traceability обязательна.** Каждая задача должна указывать issue, PR,
  артефакт, analysis, ADR/RFC или другой источник.
- **Anti-Inflation.** Новый файл, каталог, статус или validator semantics
  добавляются только при реальной операционной боли или explicit human decision.

## Формат спринта

Каждый спринт в `backlog.md` имеет такой каркас:

```markdown
## Спринт N: <Название>

**Story.**
2-3 абзаца контекста: почему задачи связаны и какую боль закрывает спринт.

**Цель.**
1-2 предложения с измеримым результатом.

**Критерий закрытия.**
Когда спринт считается done.

| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Краткое содержание | Режим запуска |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

Колонка «Краткое содержание» содержит 1-2 предложения: что делаем и зачем.
Колонка «Режим запуска» использует только `Structured`, `Hybrid`, `Creative` или
`null`.

## Поля задачи

| Поле | Правило |
| --- | --- |
| ID | `B-XXX`; не переиспользовать номер для несвязанной задачи. |
| Название | Короткий action-oriented заголовок из issue/backlog source. |
| Приоритет | `P0`, `P1`, `P2`, `P3`; при отсутствии факта - `null`. |
| Зависимости | Существующие task IDs или `-`; не добавлять speculative blockers. |
| Статус | `TODO`, `in-progress`, `review`, `DONE`, `ЧАСТИЧНО`; в active backlog обычно остаются не-`DONE`. |
| Issue | GitHub issue/PR link, если есть; иначе `- (planned)`, `- (deferred)` or `null` according to source. |
| Источник | Проверяемый источник: issue, PR, artifact, analysis, ADR/RFC, validator or human decision. |
| Краткое содержание | 1-2 предложения без implementation recipe. |
| Режим запуска | `Structured`, `Hybrid`, `Creative`; если источник даёт другой тип или не даёт режим - `null`. |

## Lifecycle

Задача проходит путь:

```text
idea -> backlog -> in-progress -> review -> DONE -> archived
```

- `idea`: есть сигнал, но нет трассируемого backlog item.
- `backlog`: задача добавлена в активный sprint.
- `in-progress`: есть текущий исполнитель или открытый implementation PR.
- `review`: работа выполнена в PR and awaits review/merge.
- `DONE`: merged/accepted state confirmed by issue/PR/artifact evidence.
- `archived`: строка удалена из active backlog после закрытия sprint rules.

## Правила архивации спринтов

Спринт удаляется из `backlog.md`, когда выполнены оба условия:

1. Все задачи спринта имеют статус `DONE`.
2. Итоговый артефакт или decision outcome имеет статус «согласовано» или
   «отклонено» в issue, PR, ADR/RFC, artifact frontmatter or review record.

После архивации остаются:

- GitHub issues/PR with discussion, review and implementation history.
- Запись в `CHANGELOG.md`.
- Артефакты в репозитории.
- Ссылки из `artifact-map.md`, если артефакт активен.

Отдельный archive/backlog file не создаётся.

## Обновление связанных артефактов

При изменении backlog structure или task set проверь:

- `CHANGELOG.md`: есть запись о governance/change-management изменении.
- `pr-ops/artifact-map.md`: новые или изменённые active artifacts отражены в
  карте.
- `pr-ops/README.md`: список PR-Ops artifacts актуален.
- `tools/validate-repository-structure.sh`: active/required files and pinned
  text синхронизированы.
- `updated` and `version` в frontmatter изменённых Markdown-файлов обновлены.

## Локальная проверка

Минимальный набор после правки:

```bash
./tools/validate-frontmatter.sh .
./tools/validate-file-naming.sh
./tools/validate-repository-structure.sh
python3 tools/generate-manifest.py --check
```

Если изменение затрагивает shell scripts, добавь `bash -n tools/*.sh
templates/**/tools/*.sh`.
