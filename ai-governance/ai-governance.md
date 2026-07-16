---
status: canonical
version: 2.0
updated: 2026-07-16
temperature: 0.1
executable: false
---

# AI Governance

Политический контракт AI-assisted work в `hybrid-Intelligence-lab`.

> **Слоган Хаба (зафиксирован):** «Человек задаёт смысл, AI ускоряет путь — вместе по правилам».
> Человек отвечает за смысл, цели и решения, AI ускоряет путь к ним внутри
> правил. Слоган наследуется HTOM-командами через геном
> [`templates/htom/`](../templates/htom/).

Хаб является источником рекомендаций, reusable governance-практик, стандартов и
шаблонов для ecosystem repositories. Он помогает downstream-командам принимать
решения, но не является механическим блокером их работы: локальная команда может
адаптировать рекомендацию под свой риск, зрелость и контекст, если решение явно
зафиксировано.

RFC в [`docs/rfc/`](../docs/rfc/) — рекомендации и proposals. Они становятся
обязательными только после human decision и переноса нормативной части в
canonical standard, policy, template или другой active artifact. Жизненный цикл
описан в [Knowledge Lifecycle proposal](../docs/rfc/knowledge-lifecycle-proposal.md),
а место нового артефакта выбирается через
[Resolve Artifact Location proposal](../docs/rfc/resolve-artifact-location-proposal.md).

## Роли и права решений

| Роль | Ответственность |
| --- | --- |
| Пользователь | Формирует vision, priorities, publication boundaries и финальные product/governance decisions. |
| Human reviewer | Проверяет структуру, источники, риски и полезность до merge или публикации. |
| Contributor | Создаёт issues, artifacts и pull requests внутри repository model. |
| AI agent | Готовит черновики, миграции, проверки и summaries внутри scope issue и governance policy. |

AI agents могут предлагать структуру, но humans принимают финальные решения по
vision, publication, license и sensitive context.

## Политики

1. Claims, влияющие на решения, связываются с sources, experiments, issues,
   PRs или historical migration records.
2. Secrets, private client data, credentials и несанитизированные
   production-промпты не коммитятся.
3. RFC не становится обязательной политикой без human decision и продвижения в
   active normative artifact.
4. Значимые изменения governance-практики или downstream-шаблона проходят human
   review и оформляются через применимый ADR/RFC или canonical standard.

Минимальный frontmatter для активных Markdown-артефактов задан
[стандартом frontmatter](../standards/frontmatter-standard.md). Остальные
нормативные контракты перечислены в [Standards](../standards/README.md).

## Обоснованный обход в Creative Mode

Creative mode допускает обоснованный обход рекомендации Хаба, когда это нужно
для достижения цели задачи и не нарушает жёсткие запреты. Обход допустим, если:

1. задача явно задана как Creative или содержит открытый результат;
2. обход минимален;
3. не нарушены hard bans: secrets, private data, credentials,
   несанитизированные production-промпты, publication, license и права на
   пользовательский контент;
4. в PR, ADR/RFC или audit записаны rationale, изменённый артефакт и validation;
5. архитектурное или governance-изменение проходит human review.

Обход не отменяет политику Хаба для следующих задач, а создаёт traceable
precedent, который человек может принять, сузить или отклонить.

## Эскалация

Перед продолжением нужно запросить human guidance, если:

- требования противоречат друг другу;
- изменение публикует sensitive или private information;
- нужен новый обязательный standard, но нет comparison;
- репозиторий смещается к production-code ownership;
- Creative override затрагивает hard bans, publication, license, security или
  права на пользовательский контент;
- AI agent не может проверить важное claim или migration decision.

Правила исполнения этой политики находятся в
[Agent Work Rules](../ai-rules/agent-work-rules.md).
