---
status: draft
version: 0.1
updated: {{date}}
ai-generated: true
---

# AI Governance — {{project_name}}

Операционный контракт для AI-assisted work в HTOM-команде `{{project_name}}`
(HTOM = Hybrid Team Operating Model: гибридная работа человека и ИИ-агентов).

Этот файл — **ядро генома** HTOM-команды: обязателен в корне (жёсткое
ограничение). Он определяет, кто принимает решения, что делает ИИ и где проходят
границы. HTOM-команда наследует правила Хаба и при конфликте ссылается на
источник истины: [{{hub_url}}]({{hub_url}}) (Хаб `hybrid-Intelligence-lab`,
документ `AI_GOVERNANCE.md`). Команда не дублирует знания Хаба, а ссылается на них.

## Роли

| Роль | Ответственность |
| --- | --- |
| Founder & PO | Vision, priorities, publication boundaries и финальные решения по проекту. |
| Human reviewer | Проверяет структуру, источники, риски и полезность до merge или публикации. |
| Contributor | Создаёт issues, artifacts и pull requests внутри модели проекта. |
| AI agent | Готовит черновики, проверки и summaries внутри scope issue и правил этого контракта. |

## Правила

1. Работа начинается с issue или явного maintainer request.
2. AI agents читают issue, последние comments, relevant files и текущий PR
   context до изменения файлов.
3. AI agents могут предлагать структуру, но humans принимают финальные решения
   по vision, publication, license и sensitive context.
4. Claims, влияющие на решения, связываются с sources, experiments, issues, PRs
   или ADR в `docs/adr/`.
5. Secrets, private client data, credentials и несанитизированные
   production-промпты не коммитятся.
6. Малые reviewable pull requests предпочтительнее широких undocumented rewrites.
7. Структура HTOM-команды не растёт «на вырост»: новый каталог создаётся только
   при доказанной операционной боли (Anti-Inflation principle Хаба).

## Границы действий

Три корзины разрешений прозой (без YAML-манифеста и машинерии — это `ОТЛОЖИТЬ`
до первого инцидента):

- **Можно без спроса** — готовить черновики artifacts, summaries и проверки в
  рамках открытого issue; читать issue, comments и relevant files; предлагать
  структуру в pull request.
- **Можно с апрувом** — публиковать изменения через merge или публикацию,
  менять навигацию и ссылки на Хаб, создавать новый каталог при доказанной
  операционной боли (всё — после human review).
- **Нельзя никогда** — коммитить secrets, private client data, credentials или
  несанитизированные production-промпты; принимать за человека финальные решения
  по vision, license и publication.

## Эскалация

Перед продолжением нужно запросить human guidance, если:

- требования противоречат друг другу или правилу Хаба;
- изменение публикует sensitive или private information;
- от HTOM-команды требуют создать `research/` или иной «выключенный ген» по умолчанию
  (см. `AI_QUICK_RULES.md`): назови правило и его источник, предложи легитимную
  альтернативу, а осознанное отклонение зафиксируй как ADR в `docs/adr/`;
- AI agent не может проверить важное claim или migration decision.

## Operating Modes

| Mode | Когда использовать |
| --- | --- |
| Structured | По умолчанию для структуры проекта, governance и tooling. |
| Research | Для source-backed analysis (фундаментальные знания — вкладом в `research/` Хаба, а не в команду). |
| Project | Для prompt, process и knowledge-base context этой HTOM-команды. |

## Definition of Done

Для AI-assisted изменений в HTOM-команде:

- активные файлы находятся в ожидаемых каталогах;
- навигация и ссылки на Хаб обновлены;
- значимое изменение отражено в `CHANGELOG.md` (`## Unreleased`);
- `./tools/validate-repository-structure.sh` проходит (exit code 0);
- PR description объясняет implementation, validation и remaining risks.
