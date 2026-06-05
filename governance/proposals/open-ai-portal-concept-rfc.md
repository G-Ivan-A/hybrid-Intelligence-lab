---
status: draft
version: 0.1
updated: 2026-06-05
ai-generated: true
type: rfc
context: [portal, open-ai-ru, communication-hub, architecture, tech-stack, documentation-standards, repository-structure, roadmap, ai-integration, mango-ba-prompts]
method: independent-research-synthesis + comparative-analysis + cross-variant-evaluation
scope: repo-wide
related_artifacts:
  - "research/portal/documentation-standards-comparison-2026-06.md"
  - "research/portal/architecture-and-stack-comparison-2026-06.md"
  - "research/portal/repository-structure-design-2026-06.md"
  - "research/portal/ai-and-mango-integration-patterns-2026-06.md"
  - "standards/PORTAL_REPOSITORY_STRUCTURE.md"
  - "projects/README.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/159"
---

# RFC: концепция портала open-ai.ru — «универсального инструмента коммуникации»

Версия: 0.1

Дата: 2026-06-05

Статус: черновик для согласования (RFC, режим `creative`). **Решение — за
человеком** (см. §14). Это **предложение**, а не старт реализации: issue #159
прямо требует только research, analysis и proposal. Портал здесь **не пишется**.

> Нормативный язык — по RFC 2119 / BCP 14: **ДОЛЖНО (MUST)**, **СЛЕДУЕТ
> (SHOULD)**, **МОЖНО (MAY)**.

## 1. Введение

`open-ai.ru` задуман как **«универсальный инструмент коммуникации»** — единая
точка сборки spoke-проектов экосистемы Хаба `hybrid-Intelligence-lab`. На старте
он связывает 2–3 проекта (Reputation Engineering и автоматизация бизнес-анализа
Mango через `mango_ba_prompts` + Yandex GPT), с перспективой 10+ open-source
проектов.

Этот RFC синтезирует **независимые исследования с нуля** (Исследования 1–4) в
предложение по: стандарту документации, архитектуре и стеку, структуре
репозитория, дорожной карте и интеграции с `mango_ba_prompts`. Варианты команды
G и фаундера рассматриваются как **входные данные, не догма** (§7).

**Что НЕ входит в этот RFC:** реализация портала, фиксация коммерческих условий,
финальный выбор фреймворка — это решения фаундера по итогам согласования.

## 2. Резюме для фаундера (TL;DR)

- **Портал — это spoke-репозиторий** (production-код + своя команда + долгий
  цикл), а не каталог в Хабе. Он **витринирует и связывает** проекты, а не
  поглощает их код (hub-and-spoke).
- **Документация:** ядро **ADR + C4 (Mermaid)**; RFC и frontmatter наследуются от
  Хаба; Diátaxis и arc42-lite — по мере роста (Исследование 1).
- **Архитектура:** модульный монолит, рендеринг **SSG + острова (islands) +
  progressive enhancement**, serverless static hosting; тонкий backend (BaaS +
  функции) — с Phase 2 (Исследование 2).
- **Стек (рекомендация исполнителя):** Astro 6 + islands, Tailwind + shadcn/ui,
  Cloudflare Pages, Supabase (Phase 2), Yandex GPT через serverless-proxy,
  PostHog, n8n. **Фреймворк — продуктовое решение фаундера**: Angular
  (предпочтение фаундера) и Next.js (вариант команды G) рабочие; их trade-off
  показаны честно (§7, §11).
- **Структура:** геном спока + 5 портал-каталогов (`projects/`, `presentations/`,
  `collaborations/`, `learning/`, `knowledge-base/`), оформлено новым стандартом
  [PORTAL_REPOSITORY_STRUCTURE.md](../../standards/PORTAL_REPOSITORY_STRUCTURE.md).
- **Roadmap:** Phase 0 (фундамент) → Phase 1 (витрина 2–3 проектов + инструмент
  BA Prompts) → Phase 2 (кабинет + маскирование) → Phase 3 (AI-агенты) → Phase 4
  (масштаб до 10+). Согласовано с фазовым видением фаундера.
- **Принципы:** open-source-first, serverless-first для старта, production-ready;
  Anti-Inflation ≠ экономия на качестве; приватные данные и ключи защищены.
- **Нужно от фаундера:** ответы на 7 вопросов §14.

## 3. Выбранный стандарт документации

Из Исследования 1 ([documentation-standards-comparison-2026-06.md](../../research/portal/documentation-standards-comparison-2026-06.md)):
единого победителя нет — оптимум это **минимальная композиция docs-as-code**:

| Слой | Стандарт | Статус для портала |
| --- | --- | --- |
| Решения | **ADR** | ДОЛЖНО (ядро; уже в геноме спока) |
| Визуализация | **C4** (Mermaid `C4Context`/`C4Container`) | ДОЛЖНО (ядро) |
| Предложения | **RFC** (RFC 2119) | наследуется от Хаба |
| Метаданные | **Concept Doc / frontmatter Хаба** | наследуется (валидатор) |
| Обзор архитектуры | **arc42-lite** | МОЖНО (по росту) |
| Документация пользователя | **Diátaxis** | МОЖНО (`learning/`, `knowledge-base/`) |

Формула: **«ADR + C4 как ядро; RFC и frontmatter по наследованию; arc42-lite и
Diátaxis по мере роста»** — закрывает все 5 критериев issue (AI-native,
итеративность, трассируемость, простота, визуализация) при минимальной церемонии.

## 4. Слоганы (3–5, ≤15 слов)

Передают: **человек создаёт вместе с AI внутри чётких контрактов** (human + AI =
команда). Без формулировок вроде «AI генерирует» / «AI пишет код».

1. **«open-ai.ru — где человек и AI работают одной командой внутри чётких контрактов»**
2. **«Человек задаёт смысл, AI ускоряет путь — вместе по правилам»**
3. **«Открытая сборочная площадка проектов: люди, AI и прозрачные контракты»**
4. **«Создаём вместе с AI — по чётким контрактам, с открытым кодом»**
5. **«Единая точка сборки проектов: человек ведёт, AI помогает»**

> Слоганы — черновик; выбор и финальная редактура (в т.ч. ru/en пара перед
> публикацией) — за фаундером.

## 5. Результаты исследований (сводка)

| # | Исследование | Главный вывод |
| --- | --- | --- |
| 1 | [Стандарты документации](../../research/portal/documentation-standards-comparison-2026-06.md) | ADR + C4 — ядро; Diátaxis/arc42-lite — по росту. |
| 2 | [Архитектура и стек](../../research/portal/architecture-and-stack-comparison-2026-06.md) | Модульный монолит, SSG+islands, Cloudflare Pages; Astro 6 лидирует по профилю (10/12), Angular/Next — рабочие альтернативы с trade-off. |
| 3 | [Структура репозитория](../../research/portal/repository-structure-design-2026-06.md) | Портал = спок + стандарт-расширение (вариант C из 3). |
| 4 | [AI и `mango_ba_prompts`](../../research/portal/ai-and-mango-integration-patterns-2026-06.md) | Только serverless-proxy для ключей; Phase 1 — санитизированные шаблоны промптов; маскирование — сердце Phase 2. |

Все version-sensitive факты (версии фреймворков, лимиты free-tier) помечены в
исследованиях как «проверять перед фиксацией».

## 6. Вариант исполнителя (Variant 4, синтез)

Независимый синтез на основе Исследований 1–4 (не копия чужого варианта):

- **Архитектура:** модульный монолит; **SSG + islands + progressive
  enhancement**; serverless static hosting; backend (BaaS + функции) с Phase 2.
- **Фреймворк (рекомендация по профилю):** **Astro 6 + islands** — контент-first,
  MD/MDX-native (продолжение docs-as-code культуры Хаба), минимальный JS, острова
  на любом компонентном фреймворке. **Но выбор за фаундером** (см. §7, §11).
- **Хостинг:** **Cloudflare Pages** (безлимитный bandwidth, коммерция разрешена,
  функции на Workers); GitHub Pages для чисто статического Phase 0.
- **Данные/Auth:** Supabase (Postgres + Auth + Storage) с Phase 2.
- **AI:** Yandex GPT 5 через **serverless-proxy** (ключи не на клиенте),
  провайдеро-агностичный слой.
- **Структура:** портал-спок + стандарт [PORTAL_REPOSITORY_STRUCTURE.md](../../standards/PORTAL_REPOSITORY_STRUCTURE.md).
- **Roadmap:** фазовый, согласованный с видением фаундера (§9).

## 7. Сравнительный анализ 4 вариантов

**Варианты:**

- **V1 — Industry Best Practices:** типовой индустриальный дефолт (Next.js/React
  на Vercel, BaaS, готовность к микросервисам). Базовая точка отсчёта.
- **V2 — Команда G:** Next.js (App Router) + TS; Tailwind + shadcn/ui + Radix;
  Zustand / TanStack Query; Supabase; n8n; PostHog. Треки **Product** +
  **Governance**; Educational & Research — в отдельный репозиторий
  `research-and-edu-ai-lab`.
- **V3 — Фаундер:** Angular (frontend); фазовый roadmap (Phase 1 — multi-page,
  2–3 проекта, инструмент BA Prompts; Phase 2 — личный кабинет + маскирование;
  Phase 3 — AI-агенты).
- **V4 — Исполнитель (синтез):** §6 (Astro + islands, Cloudflare, Supabase
  Phase 2, serverless-proxy для Yandex GPT, портал-спок + стандарт).

### Матрица сравнения (14 критериев)

Шкала: 🟢 сильно / 🟡 средне / 🔴 слабо (оценка под *профиль контент-first портала
Phase 1* по issue #159).

| # | Критерий | V1 Best Practices | V2 Команда G | V3 Фаундер (Angular) | V4 Исполнитель (синтез) |
| --- | --- | :---: | :---: | :---: | :---: |
| 1 | Архитектура | 🟡 микросервис-готовность преждевременна | 🟢 модульный монолит на Next | 🟡 SPA-уклон | 🟢 модульный монолит, SSG+islands |
| 2 | Стек frontend | 🟡 React/Next дефолт | 🟢 Next 16 + TS | 🟡 Angular 21 (тяжелее для контента) | 🟢 Astro 6 + islands (MD-native) |
| 3 | Стек backend | 🟡 разное | 🟢 Supabase + n8n | 🟡 не специфицирован | 🟢 BaaS+функции с Phase 2 (serverless-first) |
| 4 | AI integration | 🟡 общая | 🟡 не детализирована | 🟢 фаза AI-агентов | 🟢 serverless-proxy + провайдеро-агностично (Иссл. 4) |
| 5 | Roadmap | 🔴 не задан | 🟡 треки, без фаз MVP | 🟢 чёткие фазы | 🟢 Phase 0–4 с критериями (§9) |
| 6 | Governance | 🟡 вне Хаба | 🟢 отдельный Governance-трек | 🟡 неявно | 🟢 наследование Хаба + новый стандарт |
| 7 | Scalability (качество/проекты) | 🟡 | 🟢 | 🟡 | 🟢 content collections → 10+ проектов |
| 8 | Cost | 🟡 Vercel платно для коммерции | 🟡 то же при Vercel | 🟢 нейтрально | 🟢 Cloudflare free, коммерция-OK |
| 9 | Time to MVP | 🟡 | 🟢 | 🟡 (порог Angular) | 🟢 SSG быстрый старт |
| 10 | Alignment с методологией Хаба | 🔴 не учитывает | 🟡 частично (вынос edu/research) | 🟡 | 🟢 docs-as-code, Anti-Inflation, спок-геном |
| 11 | Open-source first | 🟡 | 🟢 | 🟡 (Angular OK) | 🟢 весь стек OSS |
| 12 | Portal as communication hub | 🟡 | 🟡 | 🟢 явная цель | 🟢 5 портал-каталогов + витрина-связь |
| 13 | Repository structure | 🔴 не задан | 🟡 multi-repo | 🟡 не задан | 🟢 портал-спок + стандарт |
| 14 | Learning curve | 🟡 | 🟡 React-экосистема | 🔴 Angular высокий порог | 🟢 Astro низкий порог |

**Чтение матрицы (честно):** V4 ведёт по *профилю Phase 1* (контент-first
витрина с островами интерактива), потому что синтезирует выводы независимых
исследований именно под этот профиль. **Но:**

- **V2 (Команда G)** сильнее, если портал с самого старта app-heavy (много
  SSR/персонализации) — Next.js это закрывает; идея отдельного Governance-трека
  ценна. Вынос Educational & Research в отдельный репозиторий — **отдельное
  governance-решение** (вопрос §14.3), здесь не предрешается.
- **V3 (Фаундер)** даёт лучший **roadmap-каркас** (фазы) и явную
  коммуникационную цель — они приняты в V4. Angular оправдан, если команда сильна
  в нём и портал быстро станет app-heavy.
- **V4 не отменяет V2/V3**, а вбирает их сильные стороны (фазы фаундера +
  Supabase/n8n/PostHog команды G) и добавляет недостающее (структура, стандарт,
  AI-proxy, alignment с Хабом).

## 8. Оптимальное решение (синтез)

**ДОЛЖНО:**

1. Признать портал **spoke-репозиторием** и применить стандарт
   [PORTAL_REPOSITORY_STRUCTURE.md](../../standards/PORTAL_REPOSITORY_STRUCTURE.md).
2. Принять документацию **ADR + C4** как ядро (наследуя RFC/frontmatter Хаба).
3. Архитектура — **модульный монолит, SSG + islands**, serverless static
   hosting; backend вводится с Phase 2.
4. AI-вызовы — **только через serverless-proxy**; Phase 1 — санитизированные
   шаблоны `mango_ba_prompts` (правило 6 AI_GOVERNANCE).

**СЛЕДУЕТ:**

5. Выбрать стек по §11 (рекомендация: Astro + islands + Cloudflare + Supabase);
   фреймворк — решение фаундера.
6. Взять фазовый roadmap фаундера как каркас (§9), дополнив критериями
   готовности.

**МОЖНО:**

7. Рассмотреть отдельный репозиторий `research-and-edu-ai-lab` (идея команды G)
   как **самостоятельное** governance-решение (вопрос §14.3).

## 9. Дорожная карта (Phase 0–4)

| Фаза | Цель | Ключевые deliverables | Зависимости | Критерии готовности | Ресурсы |
| --- | --- | --- | --- | --- | --- |
| **Phase 0 — Фундамент** | Каркас портал-спока | Геном спока (init.sh), `tools/validate-*`, `docs/adr/`, лендинг (SSG), CI-деплой | Утверждение стандарта (§14.4), выбор фреймворка (§14.1) | Валидатор зелёный; лендинг задеплоен; 1-й ADR записан | 1 разработчик, неск. дней |
| **Phase 1 — Витрина + BA Prompts** | Multi-page витрина 2–3 проектов + инструмент промптов | Страницы Reputation Engineering и BA Prompts; **остров BA Prompts**: вызов санитизированных промптов для скрининга/копирования + загрузка результата для отладки (через proxy к Yandex GPT) | Phase 0; доступность шаблонов `mango_ba_prompts` (§14.6); Yandex GPT folder/ключ (§14.6) | 2–3 проекта видны; инструмент промптов работает через proxy; ключи не на клиенте | команда + BA-эксперт по промптам |
| **Phase 2 — Кабинет + маскирование** | Персонализация и приватность | Supabase Auth; личный кабинет; история; **маскирование PII на клиенте до отправки**; RLS; обезличенный аудит | Phase 1; решение по границе приватности (§14.6) | Логин работает; данные изолированы (RLS); PII маскируется до LLM | + backend-разработчик |
| **Phase 3 — AI-агенты** | Агентные сценарии | Агентные пайплайны (n8n), действия с согласиями и аудитом | Phase 2 (auth, маскирование) | Агент выполняет сценарий под контролем человека; полный аудит | + AI-инженер |
| **Phase 4 — Масштаб** | Рост до 10+ проектов | Онбординг новых проектов в витрину; observability; перф-бюджет | Phase 1–3 | Добавление проекта = предсказуемый процесс; метрики качества в норме | команда |

Каждая фаза завершается human review; переход — по критериям готовности, не по
календарю. Точные сроки зависят от состава команды и приоритетов фаундера.

## 10. Структура репозитория

Геном спока + 5 портал-каталогов (полное дерево и обоснование —
[PORTAL_REPOSITORY_STRUCTURE.md](../../standards/PORTAL_REPOSITORY_STRUCTURE.md)
и [Исследование 3](../../research/portal/repository-structure-design-2026-06.md)):

```text
open-ai.ru/
├── (геном спока: README, AI_GOVERNANCE, AI_QUICK_RULES, AI_HANDOVER_PROMPT,
│    CONTRIBUTING, CHANGELOG, docs/adr/, docs/audit/, .github/, tools/)
├── docs/architecture.md         # C4-обзор (Mermaid)
├── projects/                    # витрина spoke-проектов (связь, не поглощение)
├── presentations/               # презентации, демо
├── collaborations/              # координация с командами/партнёрами
├── learning/                    # обучение пользователей (Diátaxis)
├── knowledge-base/              # FAQ, интеграционные гайды
└── src/                         # код портала (по фреймворку)
```

## 11. Стек технологий

| Слой | Рекомендация (V4) | Альтернатива фаундера/команды G |
| --- | --- | --- |
| Frontend | **Astro 6 + islands** | Angular 21 (фаундер) / Next.js 16 (команда G) |
| UI | Tailwind + shadcn/ui (Radix) | Angular Material (если Angular) |
| State | nanostores (островам) | Signals/RxJS (Angular) / Zustand+TanStack (Next) |
| Hosting | **Cloudflare Pages** | Vercel (⚠️ Hobby запрещает коммерцию) / Netlify |
| Backend | Cloudflare Workers / функции (Phase 2) | Node/Nest при доказанной потребности |
| DB/BaaS | **Supabase** | Pocketbase/Appwrite (self-host) |
| Auth | Supabase Auth (Phase 2) | Auth.js |
| AI | Yandex GPT 5 через **serverless-proxy** | провайдеро-агностичный слой |
| Аналитика | PostHog | Plausible |
| Автоматизация | n8n (Phase 3) | — |

⚠️ Версии и лимиты free-tier — **проверять перед фиксацией** (Исследование 2).

## 12. План миграции open-ai.ru

Обобщённый путь (детали — раздел «Миграция» в
[PORTAL_REPOSITORY_STRUCTURE.md](../../standards/PORTAL_REPOSITORY_STRUCTURE.md)):
инвентаризация → привить геном спока (`init.sh`, отдельная ветка, без удаления
рабочего кода) → внести валидатор → разложить контент по портал-каталогам →
завести `docs/adr/` (+ `docs/architecture.md`) → связать с Хабом в README →
прогнать валидатор → PR малыми шагами. **Решение и сроки миграции — за
фаундером.**

## 13. Бэклог Phase 0

| ID | Задача | Приоритет | Зависит от |
| --- | --- | --- | --- |
| P0-1 | Создать портал-спок из `templates/spoke/` (`init.sh`) | P0 | §14.1, §14.4 |
| P0-2 | Адаптировать `tools/validate-repository-structure.sh` под портал | P0 | P0-1 |
| P0-3 | Первый ADR: «выбор фреймворка и хостинга» (фиксация решения §14) | P0 | §14.1, §14.2 |
| P0-4 | `docs/architecture.md` — C4 Context/Container (Mermaid) | P1 | P0-1 |
| P0-5 | Лендинг (SSG) + CI-деплой на выбранный хостинг | P0 | P0-1, §14.2 |
| P0-6 | Каркас `projects/` для 2–3 проектов Phase 1 | P1 | P0-1, §14.5 |
| P0-7 | Спецификация serverless-proxy для Yandex GPT (без ключей в репо) | P1 | §14.6 |

## 14. Запрос на согласование (решение за человеком)

Согласно AI_GOVERNANCE (правило 4 и эскалация «нужен новый обязательный standard,
но нет comparison» — закрыта Исследованием 1), **финальные решения принимает
фаундер**. Прошу ответить:

1. **Фреймворк:** Astro + islands (рекомендация по профилю), **Angular**
   (предпочтение фаундера) или Next.js (вариант команды G)?
2. **Хостинг и коммерция:** Cloudflare Pages (рекомендация) против
   Vercel/Netlify? Будет ли портал коммерческим (влияет на пригодность Vercel
   Hobby)?
3. **Educational & Research:** оставить в Хабе со ссылкой-витриной из портала,
   или выделить в отдельный репозиторий `research-and-edu-ai-lab` (идея команды G)?
4. **Стандарт структуры:** утвердить [PORTAL_REPOSITORY_STRUCTURE.md](../../standards/PORTAL_REPOSITORY_STRUCTURE.md)
   как обязательный для порталов (перевести `draft` → `canonical`)?
5. **Проекты Phase 1:** подтвердить состав витрины — Reputation Engineering +
   BA Prompts (`mango_ba_prompts`)?
6. **`mango_ba_prompts` и приватность:** доступен ли репозиторий порталу
   (submodule/синк) или Phase 1 ограничиваемся санитизированными шаблонами? Где
   проходит граница приватности (что никогда не коммитится и не уходит в LLM без
   маскирования)? Кто владелец Yandex Cloud folder/ключа?
7. **Бюджет/ресурсы:** какой бюджет и состав команды на Phase 0–1; есть ли
   ограничения (self-host из-за приватности, регион данных)?

## 15. Приложения

- Приложение A — Исследование 1: [стандарты документации](../../research/portal/documentation-standards-comparison-2026-06.md).
- Приложение B — Исследование 2: [архитектура и стек](../../research/portal/architecture-and-stack-comparison-2026-06.md).
- Приложение C — Исследование 3: [структура репозитория](../../research/portal/repository-structure-design-2026-06.md).
- Приложение D — Исследование 4: [AI и `mango_ba_prompts`](../../research/portal/ai-and-mango-integration-patterns-2026-06.md).
- Приложение E — Стандарт: [PORTAL_REPOSITORY_STRUCTURE.md](../../standards/PORTAL_REPOSITORY_STRUCTURE.md).
- Навигация направления: [research/portal/README.md](../../research/portal/README.md).

---

> **Решение за человеком.** Этот RFC — предложение в режиме `creative`. Он не
> вводит обязательных правил и не начинает реализацию. Перевод стандарта в
> `canonical`, выбор стека и старт работ — за фаундером по ответам §14.
