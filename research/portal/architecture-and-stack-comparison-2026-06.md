---
status: draft
version: 0.1
updated: 2026-06-05
ai-generated: true
type: external-analysis
context: [portal, architecture, tech-stack, serverless, ssg, open-source, hosting, ai-integration]
method: comparative-analysis
scope: portal
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/159"
related_artifacts:
  - "research/portal/documentation-standards-comparison-2026-06.md"
  - "research/portal/repository-structure-design-2026-06.md"
  - "research/portal/ai-and-mango-integration-patterns-2026-06.md"
  - "research/portal/open-ai-portal-concept-rfc.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/159"
---

# Исследование 2: Архитектура и технологический стек портала open-ai.ru

Версия: 0.1

Дата: 2026-06-05

Статус: черновик исследования (`draft`). Выбор архитектуры и стека — за человеком
(см. «Решение за человеком»). Варианты команды G и фаундера — входные данные, не
догма; ниже независимый анализ с нуля.

## Вопрос, гипотеза, метод

| Поле | Значение |
| --- | --- |
| **Вопрос** | Какой архитектурный подход и стек оптимальны для портала `open-ai.ru` — «инструмента коммуникации» и единой точки сборки spoke-проектов, при принципах open-source-first, serverless-first для старта и production-ready качества? |
| **Гипотеза** | Phase 1 портала — это контент-ориентированный мульти-проектный хаб с *островами* интерактивности (инструмент BA Prompts), а не SPA-приложение; значит, оптимум — content-first рендеринг (SSG + islands) на serverless static hosting, с тонким backend (BaaS + serverless-функции), вводимым по мере появления реальной потребности (Phase 2+). |
| **Метод** | Сравнительный анализ архитектурных подходов и стеков по 12 критериям с таблицами; проверка version-sensitive фактов по официальным источникам (июнь 2026). |
| **Критерий успеха** | Выбран архитектурный подход + стек по слоям, каждый выбор трассируется к критерию/источнику; зафиксированы trade-off вариантов фаундера (Angular) и команды G (Next.js). |
| **Ограничения** | Лимиты free-tier и версии фреймворков меняются — помечены как «проверять перед фиксацией». Оценки кривой обучения экспертные. |

> ⚠️ **Version-sensitive факты (проверено июнь 2026, перепроверять перед
> фиксацией):** Next.js 16.2; Angular 21 LTS (Angular 22 — июнь 2026); Astro 6.x.
> Лимиты free-tier хостингов меняются — см. раздел «Хостинг» и источники.

## Часть A. Архитектурные подходы

### A1. Модель рендеринга

| Подход | Суть | Плюсы | Минусы | Для портала Phase 1 |
| --- | --- | --- | --- | --- |
| **SSG** (static site generation) | Страницы рендерятся при сборке. | Максимальная скорость, дешёвый хостинг, безопасность (нет рантайма), отлично для контента. | Динамика только через клиент/функции. | 🟢 Базис: контент проектов, лендинг, документация. |
| **SSR** (server-side rendering) | Рендер на запрос. | Свежие данные, персонализация, SEO для динамики. | Нужен рантайм-сервер/функции, дороже, сложнее. | 🟡 Точечно: личный кабинет (Phase 2). |
| **CSR** (client-side, SPA) | Всё рендерит браузер. | Богатый интерактив, app-like. | Тяжёлый JS, хуже SEO/первая отрисовка для контента. | 🟡 Только для app-частей (кабинет, агенты). |
| **Islands / partial hydration** | Статическая страница + точечные интерактивные «острова». | Минимальный JS, контент быстр, интерактив там, где нужен. | Нужен фреймворк с поддержкой (Astro). | 🟢 Идеально: инструмент BA Prompts как остров на статической странице проекта. |
| **Progressive enhancement** | Базовая функциональность без JS, улучшения сверху. | Доступность, устойчивость. | Дисциплина разработки. | 🟢 Принцип поверх любого выбора. |

**Вывод A1:** для Phase 1 оптимум — **SSG + islands + progressive enhancement**;
SSR/CSR вводятся точечно под app-части в Phase 2–3.

### A2. Структура системы

| Подход | Для портала | Оценка |
| --- | --- | --- |
| **Монолит** (один деплой) | Один репозиторий-портал, проекты как модули/разделы. | 🟢 Оптимум для старта: просто, дёшево, быстрый MVP. |
| **Модульный монолит** | Монолит с чёткими границами модулей-проектов (по проекту — каталог/коллекция). | 🟢 Целевое: масштабируется до 10+ проектов без оверхеда микросервисов. |
| **Микросервисы** | Каждый проект — свой сервис/деплой. | 🔴 Преждевременно: оверхед инфраструктуры, противоречит Anti-Inflation и serverless-first. |

**Вывод A2:** **модульный монолит** (портал-оболочка + проект-модули). Каждый
spoke-проект, у которого есть собственный репозиторий, портал **витринирует и
связывает** (карточка, ссылки, демо), а не поглощает — это соответствует
hub-and-spoke модели Хаба и роли «инструмент коммуникации».

### A3. Хостинг (serverless-first)

Проверено июнь 2026 (⚠️ лимиты меняются — сверять с официальными прайсингами):

| Платформа | Bandwidth (free) | Сборки/функции (free) | Коммерческое использование | Заметки |
| --- | --- | --- | --- | --- |
| **GitHub Pages** | ~100 ГБ/мес (soft), сайт ≤1 ГБ | Только статика (GH Actions для сборки) | Разрешено для публичных репо | Самый дешёвый, но только статика; нет serverless-функций. |
| **Cloudflare Pages** | **Безлимит, без egress-платы** | 500 сборок/мес; Workers 100K запросов/день | **Разрешено** | Лучшее соотношение для масштаба; функции на Workers. |
| **Netlify** | 100 ГБ/мес | 300 мин сборки/мес; 125K вызовов функций | Разрешено (free) | Зрелый DX, формы, identity. |
| **Vercel (Hobby)** | 100 ГБ transfer; 1M edge-запросов | Ограничения по сборке/функциям | ⚠️ **Hobby запрещает коммерческое использование** → Pro $20/seat/мес | Лучший DX для Next.js, но коммерция требует платного плана. |

**Вывод A3:** для open-source портала, который может стать коммерческим,
**Cloudflare Pages** — наиболее безопасный дефолт (безлимитный bandwidth, нет
egress-платы, коммерция разрешена на free, serverless-функции на Workers).
**GitHub Pages** — отличный нулевой вариант для чисто статического Phase 0/MVP.
**Vercel Hobby** непригоден для коммерческого портала без перехода на Pro — это
критично зафиксировать (особенно если портал монетизируется).

## Часть B. Технологический стек по слоям

| Слой | Кандидаты (open-source) | Заметки |
| --- | --- | --- |
| **Frontend-фреймворк** | Astro 6 (+islands), Next.js 16, Angular 21, Docusaurus/Astro Starlight | Главный выбор; разбор ниже. |
| **UI / компоненты** | Tailwind CSS + shadcn/ui + Radix; Angular Material; PrimeNG; vanilla CSS | shadcn/ui (копируемые компоненты, MIT) — гибко и open-source. |
| **State** | TanStack Query + Zustand (React-мир); Angular Signals + RxJS; nanostores (Astro-agnostic) | Для islands — nanostores; для SPA-частей — по фреймворку. |
| **Backend (когда нужен)** | Serverless-функции (Cloudflare Workers / Netlify Functions); опционально Node/Nest | Вводится в Phase 2; Phase 1 — без своего сервера. |
| **DB / BaaS** | Supabase (Postgres + Auth + Storage, open-source); Pocketbase (self-host); Appwrite | Supabase — зрелый open-source BaaS, закрывает БД+auth+storage. |
| **Auth** | Supabase Auth; Auth.js (NextAuth); Clerk (proprietary, есть free) | Open-source-first → Supabase Auth / Auth.js. |
| **AI-интеграция** | Yandex GPT 5 (Lite/Pro) через serverless-proxy; провайдеро-агностичный слой | Детали — [ai-and-mango-integration-patterns-2026-06.md](ai-and-mango-integration-patterns-2026-06.md). |
| **Аналитика/observability** | PostHog (open-source, self-host или cloud); Plausible; Sentry | PostHog — продуктовая аналитика open-source. |
| **Автоматизация** | n8n (open-source workflow automation, self-host) | Для агентных/интеграционных пайплайнов (Phase 3). |

### Сравнение frontend-стеков (12 критериев)

Шкала: 🟢 сильно / 🟡 средне / 🔴 слабо.

| Критерий | **Astro 6 + islands** | **Next.js 16 + React** | **Angular 21** | **Docusaurus / Starlight** |
| --- | :---: | :---: | :---: | :---: |
| 1. Open-source / лицензия | 🟢 MIT | 🟢 MIT | 🟢 MIT | 🟢 MIT |
| 2. Качество / зрелость | 🟢 | 🟢 | 🟢 | 🟢 |
| 3. Кривая обучения | 🟢 низкая | 🟡 средняя | 🔴 высокая (DI, RxJS) | 🟢 низкая |
| 4. Сообщество | 🟢 | 🟢 очень большое | 🟢 большое | 🟡 (нишевое, docs) |
| 5. Масштаб по качеству (SSR/observability) | 🟢 (SSR-адаптеры) | 🟢 (зрелый SSR/RSC) | 🟢 (enterprise SSR) | 🔴 (только docs) |
| 6. Масштаб по числу проектов (контент) | 🟢 content collections | 🟡 | 🟡 | 🟢 (но только docs) |
| 7. Стоимость старта | 🟢 (любой статик-хост) | 🟡 (лучший на Vercel; Hobby = некоммерч.) | 🟢 | 🟢 |
| 8. Time to MVP | 🟢 | 🟢 | 🟡 | 🟢 (но узкая ниша) |
| 9. Alignment с методологией Хаба (Markdown/docs-as-code) | 🟢 (MD/MDX-native) | 🟡 | 🔴 | 🟢 (MD-native) |
| 10. Производительность (JS payload / CWV) | 🟢 (минимальный JS) | 🟡 | 🔴 (тяжелее) | 🟢 |
| 11. AI-интеграция (proxy + BaaS) | 🟢 (islands + endpoints) | 🟢 (route handlers) | 🟢 (SSR endpoints) | 🔴 (нет backend) |
| 12. Гибкость интерактивных островов | 🟢 (React/Vue/Svelte/Solid в одном проекте) | 🟡 (только React) | 🔴 (только Angular) | 🔴 |
| **Итог (🟢)** | **10** | **5** | **3** | **6** |

### Чтение таблицы (честные trade-off)

- **Astro + islands** выигрывает по 10/12 критериев именно для *этого* профиля
  (контент-first мульти-проектный портал с точечным интерактивом). Он
  MD/MDX-native (прямое продолжение docs-as-code культуры Хаба), грузит минимум
  JS, и допускает острова на любом компонентном фреймворке — команда может
  писать интерактив на том, что знает.
- **Next.js 16 (вариант команды G)** — сильный универсал, лучший выбор, если
  портал с самого начала app-heavy (много SSR/персонализации). Минус для старта:
  лучший хостинг (Vercel) на Hobby запрещает коммерцию; на Cloudflare/Netlify
  работает, но часть DX-преимуществ теряется. React-only острова.
- **Angular 21 (вариант фаундера)** — мощный enterprise-фреймворк с сильной
  структурой (DI, типизация, Signals). Минусы для контент-портала: высокий порог
  входа, тяжелее по JS, не MD-native, контент-страницы избыточно «приложение».
  Оправдан, если команда уже сильна в Angular и портал быстро станет app-heavy.
- **Docusaurus / Astro Starlight** — отличны как *чистый* docs/портал-витрина,
  но без backend-слоя не закрывают интерактив (BA Prompts) и кабинет — это
  ограничивает их ролью под-слоя (документация), а не всем порталом.

## Выбор: оптимальный стек (синтез)

**Архитектура:** модульный монолит, рендеринг **SSG + islands + progressive
enhancement**, serverless static hosting; тонкий backend (serverless-функции +
BaaS) вводится в Phase 2 под кабинет/маскирование.

**Рекомендуемый стек (executor-вариант):**

| Слой | Выбор | Дополнение/альтернатива |
| --- | --- | --- |
| Frontend | **Astro 6** (content shell) + islands | Острова BA Prompts — на React или Svelte (по силе команды). |
| UI | Tailwind CSS + shadcn/ui (Radix) | Angular Material — если выбран Angular. |
| State | nanostores (islands) | По фреймворку острова. |
| Hosting | **Cloudflare Pages** (Workers для функций) | GitHub Pages для чисто статического Phase 0. |
| Backend | Cloudflare Workers / serverless-функции (Phase 2) | Nest/Node — только при доказанной потребности. |
| DB/BaaS | **Supabase** (Postgres+Auth+Storage) | Pocketbase (self-host) как lite-альтернатива. |
| Auth | Supabase Auth (Phase 2) | Auth.js. |
| AI | Yandex GPT 5 через **serverless-proxy** (ключи не на клиенте) | Провайдеро-агностичный слой — см. соседнее исследование. |
| Аналитика | PostHog | Plausible (легче). |
| Автоматизация | n8n (Phase 3) | — |

**Почему не «механически Angular» и не «механически Next.js»:** issue #159 прямо
просит независимое исследование и «обоснованную альтернативу» Angular. Для
контент-first портала Astro+islands объективно сильнее по профилю задачи
(производительность, alignment с Markdown-культурой Хаба, минимальная церемония,
свобода островов). Однако выбор фреймворка — **продуктовое решение фаундера**:
если приоритет — единый app-стек и команда сильна в Angular/Next, эти варианты
рабочие (их trade-off честно показаны выше). Поэтому вопрос вынесен в RFC.

## Решение за человеком

Архитектура и стек рекомендованы, но не зафиксированы как обязательные. Выбор —
за фаундером в RFC
[open-ai-portal-concept-rfc.md](open-ai-portal-concept-rfc.md).

### Вопросы для согласования

1. **Фреймворк:** Astro+islands (рекомендация по профилю), Angular (предпочтение
   фаундера) или Next.js (вариант команды G)?
2. **Хостинг:** Cloudflare Pages (рекомендация — безлимит, коммерция-OK) против
   Vercel/Netlify? Будет ли портал коммерческим (влияет на пригодность Vercel
   Hobby)?
3. **Backend-слой:** подтвердить «без своего сервера в Phase 1, BaaS+функции с
   Phase 2»?
4. **BaaS:** Supabase (managed) против self-host (Pocketbase/Appwrite) — есть ли
   требование self-host из-за приватности данных Mango?

## Источники

- Next.js — [nextjs.org/blog](https://nextjs.org/blog), upgrade v16 — [nextjs.org/docs/app/guides/upgrading/version-16](https://nextjs.org/docs/app/guides/upgrading/version-16).
- Angular releases — [angular.dev/reference/releases](https://angular.dev/reference/releases).
- Astro — [astro.build](https://astro.build), islands — [docs.astro.build/en/concepts/islands](https://docs.astro.build/en/concepts/islands/).
- Cloudflare Pages limits — [developers.cloudflare.com/pages/platform/limits](https://developers.cloudflare.com/pages/platform/limits/).
- Vercel pricing (Hobby non-commercial) — [vercel.com/pricing](https://vercel.com/pricing).
- Netlify pricing — [netlify.com/pricing](https://www.netlify.com/pricing/).
- GitHub Pages limits — [docs.github.com/pages/getting-started-with-github-pages/about-github-pages](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages).
- Supabase — [supabase.com](https://supabase.com); PostHog — [posthog.com](https://posthog.com); n8n — [n8n.io](https://n8n.io).
- Tailwind — [tailwindcss.com](https://tailwindcss.com); shadcn/ui — [ui.shadcn.com](https://ui.shadcn.com); Radix — [radix-ui.com](https://www.radix-ui.com).
- Yandex GPT 5 — [yandex.cloud/docs/foundation-models](https://yandex.cloud/en/docs/foundation-models/) (детали — соседнее исследование).
- Внутренние: [CONCEPT.md](../../CONCEPT.md), [governance/REPO_MODEL.md](../../governance/REPO_MODEL.md), [projects/README.md](../../projects/README.md).
