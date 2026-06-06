---
status: draft
version: 0.1
updated: 2026-06-06
ai-generated: true
type: internal-analysis
context: [portal, review-tool, decision-matrix, founder-review]
method: manual-review
scope: portal
related_artifacts:
  - "research/portal/README.md"
  - "research/portal/ai-and-mango-integration-patterns-2026-06.md"
  - "research/portal/architecture-and-stack-comparison-2026-06.md"
  - "research/portal/concept-standards-comparison-2026-06.md"
  - "research/portal/documentation-standards-comparison-2026-06.md"
  - "research/portal/open-ai-portal-concept-rfc.md"
  - "research/portal/repository-structure-design-2026-06.md"
  - "standards/portal-repository-structure.md"
  - "standards/webportal-concept-standard.md"
  - "templates/webportal-concept-template.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/191"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/159"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/166"
---

# Review: 10 portal-документов open-ai.ru

Документ собирает в одном месте 10 portal-артефактов, которые RFC
[repository-quality-improvement-plan.md](../../governance/rfc/repository-quality-improvement-plan.md)
отнес к категории "Отложить". Цель - ускорить human review: быстро увидеть
роль каждого документа, спорные вопросы, зависимости и место для решения
фаундера.

Это review-tool, а не новое исследование и не утверждение портальной концепции.
Содержимое исходных 10 документов не меняется.

HTML-версия для браузера:
[portal-documents-review-2026-06.html](portal-documents-review-2026-06.html).

## Навигация

- [1. Документы в review](#1-документы-в-review)
- [2. Быстрый маршрут согласования](#2-быстрый-маршрут-согласования)
- [3. Сводная матрица вопросов](#3-сводная-матрица-вопросов)
- [4. Карточки документов](#4-карточки-документов)
- [5. Рекомендуемый порядок review](#5-рекомендуемый-порядок-review)
- [6. Definition of Done для согласования](#6-definition-of-done-для-согласования)
- [7. Источники](#7-источники)

## 1. Документы в review

| # | Документ | Роль | Что нужно решить |
| ---: | --- | --- | --- |
| 1 | [research/portal/README.md](README.md) | Навигация направления portal | Оставить направление как draft-навигацию или перевести после решения по пакету. |
| 2 | [ai-and-mango-integration-patterns-2026-06.md](ai-and-mango-integration-patterns-2026-06.md) | AI/Mango integration research | Подтвердить границы приватности, формат подключения `mango_ba_prompts` и владельца Yandex Cloud. |
| 3 | [architecture-and-stack-comparison-2026-06.md](architecture-and-stack-comparison-2026-06.md) | Architecture and stack research | Выбрать framework/hosting/backend timing или отправить стек на доработку. |
| 4 | [concept-standards-comparison-2026-06.md](concept-standards-comparison-2026-06.md) | Research source for concept standard | Принять гибрид PRD + Vision + TOGAF-модульность как основу стандарта. |
| 5 | [documentation-standards-comparison-2026-06.md](documentation-standards-comparison-2026-06.md) | Documentation standard comparison | Утвердить ADR + C4 как обязательное ядро portal-документации. |
| 6 | [open-ai-portal-concept-rfc.md](open-ai-portal-concept-rfc.md) | Main portal concept RFC | Ответить на 7 founder questions: framework, hosting, repo model, Phase 1 scope, privacy, resources. |
| 7 | [repository-structure-design-2026-06.md](repository-structure-design-2026-06.md) | Research source for repository standard | Подтвердить вариант C: portal = spoke + portal-specific extension. |
| 8 | [standards/portal-repository-structure.md](../../standards/portal-repository-structure.md) | Draft standard for portal repositories | Перевести в canonical/reviewed, оставить draft или изменить каталоговую модель. |
| 9 | [standards/webportal-concept-standard.md](../../standards/webportal-concept-standard.md) | Draft standard for portal concepts | Утвердить модульный standard или изменить обязательное ядро/границы применения. |
| 10 | [templates/webportal-concept-template.md](../../templates/webportal-concept-template.md) | Copyable concept template | Принять как шаблон после стандарта или доработать placeholder/lifecycle-подход. |

## 2. Быстрый маршрут согласования

| Пакет решений | Документы | Рекомендация исполнителя | Почему это спорно |
| --- | --- | --- | --- |
| Концепция портала | 1, 6 | Сначала согласовать RFC как направление, не как старт реализации. | RFC уже синтезирует пакет решений, но переводит их в product/governance choices фаундера. |
| Структура документации | 5 | Принять ADR + C4 как минимальное ядро. | C4 не хранит причины решений, ADR не визуализирует архитектуру; нужен именно набор, а не один стандарт. |
| Структура портального репозитория | 7, 8 | Принять portal as spoke + extension. | Это создает новый repo-wide draft standard, но он ограничен классом порталов и опирается на existing spoke genome. |
| Стандарт концепции | 4, 9, 10 | Принять модульный standard и template после review. | Универсальный standard снижает bootstrap-боль, но пока может быть преждевременным без первого применения. |
| Стек и roadmap реализации | 2, 3, 6 | Выбрать framework/hosting/privacy перед Phase 0. | Astro лидирует по content-first профилю, но founder/team могут выбрать Angular/Next по team fit. |

## 3. Сводная матрица вопросов

| ID | Вопрос для решения | Рекомендация исполнителя | Затрагивает | Решение фаундера |
| --- | --- | --- | --- | --- |
| Q01 | Считать ли portal package отдельным направлением, которое пока остается `draft`? | Да, до ответов по RFC. | 1, 6 | - [ ] Принять - [ ] Доработать - [ ] Отложить |
| Q02 | Утвердить ли портал как отдельный spoke-репозиторий, а не каталог в Хабе? | Да, portal имеет production-код, команду и долгий lifecycle. | 6, 7, 8 | - [ ] Принять - [ ] Доработать - [ ] Отложить |
| Q03 | Утвердить ли ADR + C4 как обязательное ядро документации портала? | Да, это минимальная композиция для traceability + visualization. | 5, 6, 8 | - [ ] Принять - [ ] Доработать - [ ] Отложить |
| Q04 | Нужен ли Structurizr DSL вместо Mermaid C4? | Нет для старта; Mermaid достаточно проще для docs-as-code. | 5, 6 | - [ ] Принять Mermaid - [ ] Нужен Structurizr - [ ] Отложить |
| Q05 | Утвердить ли `portal-repository-structure.md` как canonical/reviewed standard? | Да после подтверждения portal as spoke. | 7, 8 | - [ ] Canonical - [ ] Reviewed - [ ] Draft |
| Q06 | Утвердить ли `webportal-concept-standard.md` как standard для будущих portal concepts? | Да после проверки обязательного ядра и границ. | 4, 9, 10 | - [ ] Canonical - [ ] Reviewed - [ ] Draft |
| Q07 | Какой framework выбрать для Phase 0-1? | Astro + islands по content-first профилю; Angular/Next допустимы как product decision. | 3, 6 | - [ ] Astro - [ ] Angular - [ ] Next.js |
| Q08 | Какой hosting выбрать? | Cloudflare Pages как дефолт для commercial-safe serverless start. | 3, 6 | - [ ] Cloudflare - [ ] Vercel - [ ] Netlify |
| Q09 | Вводить ли auth/backend в Phase 1? | Нет; backend/BaaS/Auth с Phase 2, кроме serverless AI proxy. | 2, 3, 6 | - [ ] Phase 2 - [ ] Phase 1 - [ ] Доработать |
| Q10 | Как подключать `mango_ba_prompts` в Phase 1? | Санитизированная content-collection; direct private access не использовать. | 2, 6 | - [ ] Content copy - [ ] Submodule/sync - [ ] API |
| Q11 | Где граница приватности и кто владелец Yandex Cloud key/folder? | Зафиксировать до любых AI calls; ключи только serverless secret-store. | 2, 6 | - [ ] Зафиксировано - [ ] Нужна доработка - [ ] Отложить |
| Q12 | Принимать ли шаблон webportal concept сейчас? | Принимать вместе со standard; placeholder-date warning оставить как template behavior до отдельного решения. | 9, 10 | - [ ] Принять - [ ] Доработать - [ ] Отложить |

## 4. Карточки документов

### D01. `research/portal/README.md`

Ссылка: [README.md](README.md)

**Саммари.** Навигационный документ задает границы направления portal: это
исследовательская область для концепции `open-ai.ru`, а не место реализации
портала. Он связывает пять research-документов и два standards/templates
артефакта, фиксируя русский язык результата, независимость исследования и
решение фаундера как условие перевода в `reviewed`.

**Спорные вопросы исполнителя.**

- [ ] Оставить README в `draft`, пока весь portal package не согласован.
- [ ] После согласования пакета обновить статус README отдельно, без изменения
      исследовательских выводов.
- [ ] Не редактировать сейчас, чтобы не нарушить ограничение issue #191.

**Место для решения фаундера.**

- Решение: [ ] принять как навигацию [ ] запросить правки [ ] оставить draft
- Комментарий:
  >

### D02. `ai-and-mango-integration-patterns-2026-06.md`

Ссылка: [ai-and-mango-integration-patterns-2026-06.md](ai-and-mango-integration-patterns-2026-06.md)

**Саммари.** Документ предлагает безопасный паттерн AI-интеграции: Yandex GPT
вызывается только через serverless-proxy, а `mango_ba_prompts` в Phase 1
подключается как санитизированная content-collection. Основная граница - не
коммитить реальные клиентские промпты, не отправлять PII без маскирования и
ввести auth/персистентность только в Phase 2.

**Спорные вопросы исполнителя.**

- [ ] Подтвердить, доступен ли `mango_ba_prompts` для sync/submodule, или Phase 1
      ограничивается санитизированной копией.
- [ ] Зафиксировать список приватных полей, которые не уходят в LLM без
      маскирования.
- [ ] Назначить владельца Yandex Cloud folder/key и место хранения secret.

**Место для решения фаундера.**

- Решение: [ ] принять pattern [ ] доработать privacy model [ ] отложить
- Комментарий:
  >

### D03. `architecture-and-stack-comparison-2026-06.md`

Ссылка: [architecture-and-stack-comparison-2026-06.md](architecture-and-stack-comparison-2026-06.md)

**Саммари.** Исследование сравнивает architecture/stack для content-first
портала и рекомендует modular monolith, SSG + islands, Cloudflare Pages,
Supabase с Phase 2 и serverless functions для AI proxy. Astro + islands
выигрывает по профилю Phase 1, но документ явно оставляет Angular и Next.js как
рабочие alternatives, если team fit или app-heavy сценарий важнее.

**Спорные вопросы исполнителя.**

- [ ] Выбрать framework: Astro, Angular или Next.js.
- [ ] Подтвердить hosting: Cloudflare Pages или альтернатива.
- [ ] Зафиксировать, что Phase 1 не получает полноценный backend/auth, кроме AI
      proxy.

**Место для решения фаундера.**

- Решение: [ ] Astro [ ] Angular [ ] Next.js [ ] нужен новый comparison pass
- Комментарий:
  >

### D04. `concept-standards-comparison-2026-06.md`

Ссылка: [concept-standards-comparison-2026-06.md](concept-standards-comparison-2026-06.md)

**Саммари.** Исследование сравнивает восемь подходов к структуре концепции
портала и приходит к гибриду PRD-ядра, Vision-слоя и TOGAF-модульности. Оно
разделяет "концепцию" и "структуру репозитория": концепция отвечает на
"зачем/что", а структура выбирается по политике Хаба.

**Спорные вопросы исполнителя.**

- [ ] Принять 6 обязательных разделов концепции как минимальное ядро.
- [ ] Решить, Roadmap всегда раздел концепции или может быть отдельным
      документом.
- [ ] Не создавать отдельный микро-профиль для простых сайтов до повторяющейся
      боли.

**Место для решения фаундера.**

- Решение: [ ] принять основу standard [ ] изменить ядро [ ] оставить research draft
- Комментарий:
  >

### D05. `documentation-standards-comparison-2026-06.md`

Ссылка: [documentation-standards-comparison-2026-06.md](documentation-standards-comparison-2026-06.md)

**Саммари.** Документ сравнивает C4, arc42, ADR, RFC, Diátaxis, Concept Doc и
IEEE 42010 для portal documentation. Главный вывод - не выбирать один монолит,
а принять минимальную композицию ADR + C4 как обязательное ядро, оставляя RFC,
arc42-lite и Diátaxis по мере роста.

**Спорные вопросы исполнителя.**

- [ ] Утвердить ADR + C4 как обязательное ядро для портала.
- [ ] Решить, достаточно ли Mermaid C4 или нужен Structurizr DSL.
- [ ] Вводить Diátaxis сразу или только после появления пользовательских
      материалов.

**Место для решения фаундера.**

- Решение: [ ] ADR+C4 accepted [ ] изменить набор [ ] отложить
- Комментарий:
  >

### D06. `open-ai-portal-concept-rfc.md`

Ссылка: [open-ai-portal-concept-rfc.md](open-ai-portal-concept-rfc.md)

**Саммари.** RFC синтезирует portal research в предложение: портал как
spoke-репозиторий, ADR + C4, SSG + islands, Cloudflare, Supabase с Phase 2,
Yandex GPT через serverless-proxy и roadmap Phase 0-4. Документ уже содержит
семь вопросов к фаундеру и должен быть основным entrypoint для решения, но не
запускает реализацию.

**Спорные вопросы исполнителя.**

- [ ] Ответить на framework/hosting/resources до Phase 0.
- [ ] Подтвердить Phase 1 project scope: Reputation Engineering + BA Prompts.
- [ ] Решить, остается ли Educational & Research в Хабе или выделяется в новый
      репозиторий.

**Место для решения фаундера.**

- Решение: [ ] принять направление [ ] доработать RFC [ ] закрыть portal direction
- Комментарий:
  >

### D07. `repository-structure-design-2026-06.md`

Ссылка: [repository-structure-design-2026-06.md](repository-structure-design-2026-06.md)

**Саммари.** Исследование доказывает, что `open-ai.ru` должен быть отдельным
spoke-репозиторием, потому что это production portal с собственным lifecycle, а
не каталог внутри Хаба. Выбран вариант C: spoke genome из `templates/spoke/`
плюс portal-specific extension (`projects/`, `presentations/`,
`collaborations/`, `learning/`, `knowledge-base/`).

**Спорные вопросы исполнителя.**

- [ ] Подтвердить вариант C как канон для порталов.
- [ ] Утвердить имена portal-каталогов или переименовать до canonical status.
- [ ] Подтвердить, что портал ссылается на project spokes и не поглощает их
      production-код.

**Место для решения фаундера.**

- Решение: [ ] вариант C accepted [ ] изменить структуру [ ] оставить draft
- Комментарий:
  >

### D08. `standards/portal-repository-structure.md`

Ссылка: [standards/portal-repository-structure.md](../../standards/portal-repository-structure.md)

**Саммари.** Draft standard формализует portal repository как класс
spoke-проекта: полный genome спока в корне плюс portal-specific catalogs по
операционной потребности. Он задает migration guide, проверки соответствия и
границу приватности, но до решения фаундера не является обязательным правилом.

**Спорные вопросы исполнителя.**

- [ ] Перевести в `canonical`/`reviewed` после подтверждения portal as spoke.
- [ ] Проверить, не слишком ли широкий scope: standard repo-wide, но только для
      класса portals.
- [ ] Уточнить, когда optional `governance/rfc/` нужен внутри portal spoke.

**Место для решения фаундера.**

- Решение: [ ] canonical [ ] reviewed [ ] оставить draft [ ] переписать scope
- Комментарий:
  >

### D09. `standards/webportal-concept-standard.md`

Ссылка: [standards/webportal-concept-standard.md](../../standards/webportal-concept-standard.md)

**Саммари.** Draft standard задает модульную структуру concept document для
web portals: 6 обязательных разделов и 9 optional layers. Он закрывает спектр
от сайта-визитки до app-портала, но явно не применяется к лендингам, mobile apps,
backend services и microservices.

**Спорные вопросы исполнителя.**

- [ ] Подтвердить обязательное ядро из 6 разделов.
- [ ] Проверить границы применения: не становится ли standard слишком широким.
- [ ] Решить, принимать ли standard до первого применения на реальном portal
      concept.

**Место для решения фаундера.**

- Решение: [ ] canonical [ ] reviewed [ ] оставить draft [ ] изменить ядро
- Комментарий:
  >

### D10. `templates/webportal-concept-template.md`

Ссылка: [templates/webportal-concept-template.md](../../templates/webportal-concept-template.md)

**Саммари.** Шаблон дает копируемый Markdown skeleton для concept document по
webportal standard: обязательное ядро, optional layers, prompts для scope,
roadmap, risks, metrics, integrations and privacy. Он зависит от решения по
standard и содержит `{{date}}`, поэтому template placeholder lifecycle остается
отдельным governance вопросом.

**Спорные вопросы исполнителя.**

- [ ] Принять template только вместе с webportal concept standard.
- [ ] Решить, должен ли placeholder `{{date}}` оставаться допустимым warning в
      frontmatter validation.
- [ ] Уточнить, должен ли template включать все optional sections по умолчанию
      или просить удалять ненужные.

**Место для решения фаундера.**

- Решение: [ ] принять template [ ] доработать placeholders [ ] отложить
- Комментарий:
  >

## 5. Рекомендуемый порядок review

1. Прочитать [open-ai-portal-concept-rfc.md](open-ai-portal-concept-rfc.md) как
   главный synthesis document и ответить на Q01-Q12 в матрице выше.
2. Если направление портала подтверждено, рассмотреть
   [documentation-standards-comparison-2026-06.md](documentation-standards-comparison-2026-06.md)
   и [architecture-and-stack-comparison-2026-06.md](architecture-and-stack-comparison-2026-06.md)
   как decision support для Phase 0-1.
3. После этого решать статус
   [standards/portal-repository-structure.md](../../standards/portal-repository-structure.md)
   и [standards/webportal-concept-standard.md](../../standards/webportal-concept-standard.md):
   `canonical`, `reviewed` или оставить `draft` с exit-plan.
4. Шаблон [templates/webportal-concept-template.md](../../templates/webportal-concept-template.md)
   принимать только после решения по standard, чтобы template не стал
   самостоятельным источником правил.
5. Не менять исходные 10 документов во время этого review pass; правки должны
   идти отдельной issue/PR после решений.

## 6. Definition of Done для согласования

- [ ] Все 10 документов просмотрены в Markdown или HTML.
- [ ] По Q01-Q12 есть решение: accepted, revise или defer.
- [ ] Для standards D08-D09 выбран status target: `canonical`, `reviewed` или
      `draft with exit-plan`.
- [ ] Для D02/D06 зафиксирована privacy boundary и владелец Yandex Cloud key.
- [ ] Для D03/D06 выбран framework и hosting или явно создан follow-up.
- [ ] Для D10 принято решение по template placeholders.
- [ ] Follow-up issues созданы для правок исходных документов, если они нужны.

## 7. Источники

- Issue source: [#191](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/191).
- Audit source:
  [governance/rfc/repository-quality-improvement-plan.md](../../governance/rfc/repository-quality-improvement-plan.md),
  section 2.5 "Draft-документы".
- Source documents: D01-D10 links in [section 1](#1-документы-в-review).
