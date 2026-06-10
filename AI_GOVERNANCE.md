---
status: canonical
version: 1.2
updated: 2026-06-06
ai-generated: false
executable: false
---

> **🛫 Директива pre-flight (обязательно перед любой работой).** ИИ-агент
> выполняет предполётный протокол *Runtime-онбординга* по
> [governance/agent-onboarding-protocol.md](governance/agent-onboarding-protocol.md): чек-лист
> governance → чек-лист контекста → *Readback* → стоп до апрува человека. Этот
> файл — контракт-справка (`executable: false`): он описывает *что* можно делать;
> онбординг — *как* безопасно начать.

> **Кейс 2 — Bootstrap-клонирование.** Для новой **HTOM-команды** (гибридная
> human + AI работа) используйте геном [`templates/htom/`](templates/htom/);
> для **production-спока** (репозиторий с собственным кодом) —
> [`templates/spoke/`](templates/spoke/). Различие определено в
> [RFC htom-vs-spoke](governance/rfc/htom-vs-spoke-clarification-2026-06.md).

# AI Governance

Версия: 1.2

Дата: 2026-06-06

Операционный контракт для AI-assisted work в `hybrid-Intelligence-lab`.

> **Слоган Хаба (зафиксирован):** «Человек задаёт смысл, AI ускоряет путь — вместе по правилам».
> Это формула гибридной работы человек + AI: человек отвечает за смысл, цели и
> решения (правило 4), AI ускоряет путь к ним внутри правил. Слоган — primary
> для Хаба и наследуется всеми HTOM-командами (геном `templates/htom/`).

## Роли

| Роль | Ответственность |
| --- | --- |
| Founder & PO | Формирует vision, priorities, publication boundaries и финальные product/governance decisions. |
| Human reviewer | Проверяет структуру, источники, риски и полезность до merge или публикации. |
| Contributor | Создает issues, artifacts и pull requests внутри repository model. |
| AI agent | Готовит черновики, миграции, проверки и summaries внутри scope issue и governance rules. |

## Правила

1. Работа начинается с issue или явного maintainer request.
2. AI agents читают issue, последние comments, relevant files и текущий PR
   context до изменения файлов — по предполётному протоколу
   [governance/agent-onboarding-protocol.md](governance/agent-onboarding-protocol.md).
3. Изменения должны следовать [CONCEPT.md](CONCEPT.md),
   [governance/repo-model.md](governance/repo-model.md) и
   [standards/README.md](standards/README.md).
4. AI agents могут предлагать структуру, но humans принимают финальные решения
   по vision, publication, license и sensitive context.
5. Claims, влияющие на решения, связываются с sources, experiments, issues,
   PRs или historical migration records.
6. Secrets, private client data, credentials и несанитизированные
   production-промпты не коммитятся.
7. Малые reviewable pull requests предпочтительнее широких undocumented
   rewrites.

## Operating Modes

| Mode | Когда использовать |
| --- | --- |
| Structured | По умолчанию для governance, структуры репозитория, standards и migration work. |
| Research | Для source-backed analysis, domain research, methods, limitations и reproducibility. |
| Education | Для programs, lessons, scenarios и teaching artifacts. |
| Project | Для prompt, process и knowledge-base context, связанных с scoped initiative. |

## Эскалация

Перед продолжением нужно запросить human guidance, если:

- требования противоречат друг другу;
- изменение публикует sensitive или private information;
- нужен новый обязательный standard, но нет comparison;
- репозиторий смещается к production-code ownership;
- AI agent не может проверить важное claim или migration decision.

## Definition of Done

Для AI-assisted repository changes:

- active files находятся в ожидаемых каталогах;
- historical material удален, перенесен или сохранен только с явным rationale;
- navigation и standards links обновлены;
- `./tools/validate-repository-structure.sh` проходит;
- PR description объясняет implementation, validation и remaining risks.
