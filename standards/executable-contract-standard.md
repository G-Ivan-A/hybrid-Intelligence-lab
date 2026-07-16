---
status: accepted
version: 1.1
updated: 2026-06-13
temperature: 0.1
owner: G-Ivan-A
executable: false
scope: repo-wide
related_standards:
  - "research-standard.md"
  - "contract-documentation-standard.md"
  - "glossary.md"
  - "file-naming.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/165"
---

# Executable Contract Standard

Документ предложен на утверждение Пользователю. До утверждения — рекомендация, не
обязательное правило (AI_GOVERNANCE, правило 4).

Стандарт фиксирует формат **исполнимых контрактов** — документов, которые ИИ-агент
должен **выполнять**, а не читать как описание. Цель: модель и человек **сразу**
понимают, как документ запускается и что надо делать; первая видимая строка —
команда к действию, а не заголовок.

Обоснование, сравнение практик и источники:
[research/governance/2026-06-06-executable-contract-format.md](../research/governance/2026-06-06-executable-contract-format.md).
Кодифицирует утверждённое Пользователем «Видение 3» из
[docs/rfc/contract-executability-rfc.md](../docs/rfc/contract-executability-rfc.md).

## Назначение

Стандарт описывает **трёхслойную** структуру исполнимого документа
(`директива → EXECUTION → EXPLANATION`) и условия её применения. Он переводит
решение RFC в нормативную (RFC 2119) форму и не вводит новых требований сверх RFC.

Нормативные термины — по [RFC 2119 / BCP 14](https://www.rfc-editor.org/info/bcp14)
(ДОЛЖНО/MUST, СЛЕДУЕТ/SHOULD, МОЖНО/MAY).

## Когда применять

| Документ | `executable` | Стандарт |
| --- | --- | --- |
| Агент должен **выполнить** процедуру (онбординг, runbook, handover) | `true` | ✅ этот стандарт |
| Точка входа агента (единственная «первая» исполнимая инструкция) | `true` + `entrypoint: true` | ✅ этот стандарт |
| Документ читается для знания/решения | `false`/нет | [research-standard.md](research-standard.md) |
| Документ фиксирует обязательства сторон | `false` | [contract-documentation-standard.md](contract-documentation-standard.md) |

Эталон применения — [ai-rules/agent-onboarding-protocol.md](../ai-rules/agent-onboarding-protocol.md)
(`executable: true`, `entrypoint: true`).

## Три слоя (defense in depth)

Исполнимый документ **ДОЛЖЕН** реализовывать три независимых слоя сигнала
исполнимости. Слои независимы: пропуск одного компенсируется следующим.

### Слой 1 — frontmatter-маркер

Документ **ДОЛЖЕН** нести `executable: true` во frontmatter; точка входа
**ДОЛЖНА** дополнительно нести `entrypoint: true`. Маркер ортогонален
`Operating Mode` (см. [standards/glossary.md](glossary.md)) и машиночитаем.

### Слой 2 — директивный блок (🚦)

Сразу после frontmatter и заголовка документ **ДОЛЖЕН** содержать **директивный
блок** — blockquote, открывающийся знаком 🚦, который выполняет роль «системного
промпта» документа и содержит:

- **стоп-сигнал** — явное «не анализируй — выполняй»;
- **роль/цель (User-Story)** — кто агент в этом запуске и какой результат нужен;
- **запрет анализа вместо исполнения** — прямой запрет «обсуждать вместо делать».

Директивный блок **ДОЛЖЕН** быть указателем на исполнимую часть, а **НЕ ДОЛЖЕН**
копировать канонический текст (например, целиком Handover Prompt) — копия
рассинхронизируется с каноном (см. «Директивный блок» в
[glossary.md](glossary.md)).

### Слой 3 — EXECUTION → EXPLANATION

Тело документа **ДОЛЖНО** идти в порядке:

1. **▶️ EXECUTION** — первая строка = **императивная команда**; затем
   пронумерованные шаги по порядку. Здесь **НЕ ДОЛЖНО** быть «контекста»,
   мешающего немедленному исполнению.
2. **ℹ️ EXPLANATION** — *ниже*: контекст, обоснование, краевые случаи — всё, что
   **не** нужно для немедленного исполнения.

## Скелет документа

```markdown
---
status: …
version: …
updated: …
executable: true
entrypoint: true        # только для точки входа
---

# <Имя процедуры>

> 🚦 **STOP — не анализируй, выполняй.**
> Ты — <роль>. Твоя цель — <результат>. Выполни шаги ниже сейчас; не превращай
> исполнение в обсуждение.

## ▶️ EXECUTION
1. <первая команда — императив>
2. …

## ℹ️ EXPLANATION
<контекст, обоснование, краевые случаи — ниже команды>
```

## Краевые случаи и границы

- **Справочный документ.** При `executable: false`/отсутствии маркера директивный
  блок **НЕ ДОЛЖЕН** ставиться: ложный сигнал хуже отсутствия сигнала.
- **Частично исполнимый документ.** **СЛЕДУЕТ** помечать `executable: false`, а
  исполнимой делать только выделенную процедуру (или выносить её в отдельный
  `executable: true` файл).
- **Точка входа единственна.** `entrypoint: true` **ДОЛЖЕН** быть ровно у одного
  документа (в Хабе — `ai-rules/agent-onboarding-protocol.md`); валидатор frontmatter
  допускает только значение `true`.

## Зеркальность с форматом исследований

Исполнимый контракт и исследование подчинены одному метапринципу — **важнейшее
наверх** — но «важнейшее» у них разное:

| Признак | Исполнимый контракт | Исследование |
| --- | --- | --- |
| Что сверху | **команда** | **выводы** |
| Режим читателя | исполнять | читать/решать |
| Маркер | `executable: true` | `executable: false`/нет |

## Миграция

Существующие исполнимые документы **НЕ ДОЛЖНЫ** переписываться массово
(Anti-Inflation). `ai-rules/agent-onboarding-protocol.md` — эталон; шаблоны спока
(`AI_QUICK_RULES.md`, `AI_SESSION_HANDOVER_PROMPT.md`) уже несут 🚦. Прочие приводятся к
формату при следующем существенном изменении.

## Проверка соответствия

- `executable: true` стоит во frontmatter (и `entrypoint: true` для точки входа)? →
  иначе документ не опознаётся как исполнимый.
- Директивный блок 🚦 присутствует сразу после заголовка и содержит стоп-сигнал +
  роль + запрет анализа? → иначе добавить.
- Директивный блок указывает на канон, а не копирует его? → иначе заменить копию
  ссылкой.
- Первая строка EXECUTION — команда, а не заголовок/контекст? → иначе переставить.
- EXPLANATION идёт *после* EXECUTION? → иначе переставить.

## Источники

- [research/governance/2026-06-06-executable-contract-format.md](../research/governance/2026-06-06-executable-contract-format.md) — исследование-обоснование (system prompts, SRE runbooks, man SYNOPSIS, README Quick Start).
- [docs/rfc/contract-executability-rfc.md](../docs/rfc/contract-executability-rfc.md) — утверждённое «Видение 3» и трёхслойная защита.
- [ai-rules/agent-onboarding-protocol.md](../ai-rules/agent-onboarding-protocol.md) — эталонный исполнимый документ.
- [standards/glossary.md](glossary.md) — «Директивный блок», «Operating Mode», 🚦.
- [standards/research-standard.md](research-standard.md), [standards/contract-documentation-standard.md](contract-documentation-standard.md) — смежные форматы.
- IETF RFC 2119 / BCP 14 — нормативные ключевые слова.
- [AI Governance](../ai-governance/ai-governance.md) — правило 4.
