---
status: canonical
version: 1.4
updated: 2026-06-12
temperature: 0.1
executable: false
---

> **🛫 Директива pre-flight (обязательно перед любой работой).** ИИ-агент
> выполняет предполётный протокол *Runtime-онбординга* по
> [governance/agent-onboarding-protocol.md](governance/agent-onboarding-protocol.md): чек-лист
> governance -> чек-лист контекста -> *Readback* -> стоп до апрува человека. Этот
> файл - контракт-справка (`executable: false`): он описывает *что* можно делать;
> онбординг - *как* безопасно начать.

> **Кейс 2 - Bootstrap-клонирование.** Для новой **HTOM-команды** (гибридная
> human + AI работа) используйте геном [`templates/htom/`](templates/htom/);
> для **production-спока** (репозиторий с собственным кодом) -
> [`templates/spoke/`](templates/spoke/). Различие определено в
> [RFC htom-vs-spoke](governance/rfc/htom-vs-spoke-clarification-2026-06.md).

# AI Governance

Операционный контракт для AI-assisted work в `hybrid-Intelligence-lab`.

> **Слоган Хаба (зафиксирован):** «Человек задаёт смысл, AI ускоряет путь — вместе по правилам».
> Это формула гибридной работы человек + AI: человек отвечает за смысл, цели и
> решения (правило 4), AI ускоряет путь к ним внутри правил. Слоган - primary
> для Хаба и наследуется всеми HTOM-командами (геном `templates/htom/`).

Хаб является источником рекомендаций, reusable governance-практик, стандартов и
шаблонов для ecosystem repositories. Он помогает downstream-командам принимать
решения, но не является механическим блокером их работы: локальная команда может
адаптировать рекомендацию под свой риск, зрелость и контекст, если решение
явно зафиксировано.

RFC в `governance/rfc/` - это рекомендации и proposals. Они становятся
обязательными только после human decision и переноса нормативной части в
canonical standard, policy, template или другой active artifact.

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
   context до изменения файлов - по предполётному протоколу
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
8. Минимальный frontmatter для активных Markdown-артефактов описан в
   [standards/frontmatter-standard.md](standards/frontmatter-standard.md):
   `status`, `version`, `updated`, `temperature`.

## Operating Modes

| Mode | Когда использовать |
| --- | --- |
| Structured | По умолчанию для governance, структуры репозитория, standards и migration work. |
| Creative | Для задач с заданной целью и свободой выбора структуры, вариантов решения или governance-синтеза. |
| Research | Для source-backed analysis, domain research, methods, limitations и reproducibility. |
| Education | Для programs, lessons, scenarios и teaching artifacts. |

## Обоснованный обход в Creative Mode

Structured mode работает fail-closed: если нужное действие не описано правилами
или задача противоречива, агент останавливается и запрашивает human guidance.

Creative mode допускает обоснованный обход рекомендации Хаба, когда это нужно
для достижения цели задачи и не нарушает жёсткие запреты. Обход допустим только
если соблюдены все условия:

1. Задача явно задана как Creative или содержит открытый результат без
   предписанного способа выполнения.
2. Обход минимален: изменяется только то, что нужно для результата.
3. Не нарушены hard bans: secrets, private data, credentials,
   несанитизированные production-промпты, публикация, лицензия, удаление
   пользовательской работы без явного разрешения.
4. В PR, ADR/RFC или audit записаны: какое правило или рекомендация обойдена,
   почему это полезно, какой артефакт изменён и чем проверено решение.
5. Если обход меняет архитектуру, governance-практику или downstream-шаблон, он
   оформляется как ADR/RFC или обновление canonical standard после human review.

Такой обход не отменяет правила Хаба для всех последующих задач. Он создаёт
traceable precedent, который человек может принять, сузить или отклонить.

## Специфика работы с AI-агентами

- Каждый запуск агента начинается как новая рабочая сессия: агент не помнит
  прошлые чаты, если summary, issue, PR или handover prompt не переданы явно.
- GitHub comments, review comments и CI failures не мониторятся агентом
  автоматически после остановки сессии. Для продолжения нужен manual restart
  или новый запрос человеку.
- Issue/PR comment без перезапуска агента не является поручением к действию для
  уже остановленной сессии.
- Молчание после PR трактуется как ожидание human review. Merge означает
  принятие результата; comment + manual restart означает итерацию в том же PR;
  close без merge означает отклонение или отмену.
- Агент не заполняет пустые поля задачи выдуманными значениями. Если контекст
  неполон, он фиксирует gap и спрашивает человека.

## Эскалация

Перед продолжением нужно запросить human guidance, если:

- требования противоречат друг другу;
- изменение публикует sensitive или private information;
- нужен новый обязательный standard, но нет comparison;
- репозиторий смещается к production-code ownership;
- Creative override затрагивает hard bans, publication, license, security или
  права на пользовательский контент;
- AI agent не может проверить важное claim или migration decision.

## Definition of Done

Для AI-assisted repository changes:

- active files находятся в ожидаемых каталогах;
- historical material удален, перенесен или сохранен только с явным rationale;
- navigation, standards links и artifact map обновлены, если изменяется active
  artifact;
- новые или существенно изменённые Markdown-артефакты имеют четыре поля
  frontmatter: `status`, `version`, `updated`, `temperature`;
- Creative override, если он был, явно записан в PR, ADR/RFC или audit;
- `./tools/validate-frontmatter.sh .` и
  `./tools/validate-repository-structure.sh` запущены;
- PR description объясняет implementation, validation и remaining risks.
