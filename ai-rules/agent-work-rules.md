---
status: canonical
version: 1.0
updated: 2026-07-16
temperature: 0.1
executable: false
---

> **🛫 Директива pre-flight.** Перед любой работой ИИ-агент выполняет
> [Runtime-онбординг](agent-onboarding-protocol.md): governance checklist →
> context checklist → Readback → стоп до апрува человека.

# Agent Work Rules

Правила поведения AI-агента и быстрой синхронизации с контекстом Хаба.
Политические ограничения и human decision rights находятся в
[AI Governance](../ai-governance/ai-governance.md).

Для новой HTOM-команды используется геном [`templates/htom/`](../templates/htom/),
для production-спока — [`templates/spoke/`](../templates/spoke/). Различие
определено в [RFC htom-vs-spoke](../docs/rfc/htom-vs-spoke-clarification-2026-06.md).

## Правило авто-заполнения Мета

AI-агент достраивает отсутствующий контекст по active contracts, но не
выдумывает факты и не повышает lifecycle stage без human decision. Приоритет:

1. явная Мета в issue или комментарии;
2. Operating Mode;
3. [`GOVERNANCE.md`](../GOVERNANCE.md), [`CONTRIBUTING.md`](../CONTRIBUTING.md),
   [Standards](../standards/README.md),
   [Artifact Map](../pr-ops/artifact-map.md) и
   [Knowledge Lifecycle](../docs/rfc/knowledge-lifecycle-proposal.md);
4. [artifact resolver](../docs/rfc/resolve-artifact-location-proposal.md).

Если явная Мета нарушает policy, агент фиксирует конфликт и запрашивает human
guidance. Неполный контекст записывается как допущение или gap.

## Разделение Framework vs Methodology

| Слой | Уровень | Где живёт | Назначение |
| --- | --- | --- | --- |
| Framework | L1-L2 | `docs/vision.md`, `docs/product-concept.md`, `docs/ecosystem-map.md` | Границы, видение и продуктовая роль. |
| Methodology | L3-L4 | `ai-governance/`, `ai-rules/`, `pr-ops/`, `standards/`, `practices/`, `templates/`, `tools/` | Policies, rules, lifecycle, reusable practices и проверки. |

Framework указывает переход к Methodology; Methodology не переопределяет L1-L2.

## Правила

1. Работа начинается с issue или явного maintainer request.
2. До изменения файлов агент читает issue, последние comments, relevant files и
   текущий PR context по [предполётному протоколу](agent-onboarding-protocol.md).
3. Изменения следуют [concept](../docs/concept.md),
   [repository model](../pr-ops/repo-model.md) и
   [standards](../standards/README.md).
4. Агент работает внутри прав решений и ограничений из
   [AI Governance](../ai-governance/ai-governance.md).
5. Изменения остаются малыми и reviewable; широкие undocumented rewrites
   недопустимы.
6. Новый артефакт размещается по Knowledge Lifecycle и artifact resolver.

## Operating Modes

| Mode | Когда использовать |
| --- | --- |
| Structured | По умолчанию для governance, структуры, standards и migration work. |
| Creative | Когда задана цель и разрешён выбор структуры или варианта решения. |
| Research | Для source-backed analysis, methods, limitations и reproducibility. |
| Education | Для programs, lessons, scenarios и teaching artifacts. |

Structured mode работает fail-closed: при противоречии или отсутствии
необходимого правила агент запрашивает human guidance. Creative override
выполняется только по условиям [AI Governance](../ai-governance/ai-governance.md).

## Специфика работы с AI-агентами

- каждый запуск — новая сессия без памяти прошлых чатов, если контекст не передан;
- comments, reviews и CI не мониторятся после остановки автоматически;
- comment без manual restart не является поручением остановленному агенту;
- merge означает принятие, comment + restart — итерацию, close — отмену;
- агент не заполняет пустые поля выдуманными значениями, а фиксирует gap.

## Definition of Done

- active files находятся в ожидаемых каталогах;
- lifecycle stage и L1-L4 связь зафиксированы;
- historical material сохранён, перенесён или удалён с rationale;
- navigation, links и artifact map синхронизированы;
- новые или существенно изменённые Markdown-файлы имеют необходимый frontmatter;
- Creative override, если был, записан;
- локальные validators запущены;
- PR описывает implementation, validation и remaining risks.
