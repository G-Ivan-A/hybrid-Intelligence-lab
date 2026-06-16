---
status: draft
version: 0.6
updated: 2026-06-16
temperature: 0.1
ai-generated: true
type: external-analysis
context: [external-knowledge, registry, hub, ecosystem, lifecycle]
method: comparative-analysis
scope: repo-wide
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/227"
related_artifacts:
  - "research/external-knowledge/README.md"
  - "research/external-knowledge/external-insights/README.md"
  - "governance/rfc/external-knowledge-integration.md"
  - "governance/rfc/knowledge-lifecycle-proposal.md"
  - "governance/rfc/repository-archetypes-template-release.md"
  - "governance/rfc/methodology-research-and-proposals.md"
  - "standards/research-profile.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/227"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/240"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/245"
---

# Реестр внешних источников

Единый **Base Registry** внешних источников знаний экосистемы. Реестр отвечает
на один вопрос: *какие внешние источники мы считаем ценными, в какой они стадии
жизненного цикла и каким проектам релевантны* — без загрузки полного текста
источников в контекст агента.

> 🧭 **Принцип фильтрации.** Агент читает не весь реестр, а строки, отобранные по
> колонке «Теги» и «Проекты». Это держит контекст компактным (Anti-Inflation,
> см. [governance/repo-model.md](../../governance/repo-model.md)).

> ⛔ **Статус ≠ практика.** Запись в реестре означает «источник замечен и
> оценён», а не «практика принята». Перевод инсайта в `practices/`/`standards/`
> идёт только через валидацию по
> [governance/rfc/knowledge-lifecycle-proposal.md](../../governance/rfc/knowledge-lifecycle-proposal.md).

## Минимальные метаданные

Каждая запись использует ровно столько полей, сколько нужно для **фильтрации** и
**синхронизации**. Расширять состав можно только при доказанной операционной
потребности (Anti-Inflation).

| Поле | Назначение | Значения |
| --- | --- | --- |
| `id` | Стабильный якорь для ссылок из инсайтов и проектов. | `ext-NNN` (сквозная нумерация). |
| Источник | Человекочитаемое имя + ссылка на первоисточник. | Markdown-ссылка. |
| Тип | Класс источника для грубой фильтрации. | `github` · `blog` · `habr` · `standard` · `paper` · `docs`. |
| Язык | Язык первоисточника — для фильтрации и Traceability. | `ru` · `en` · др. |
| Теги | Тематические метки для отбора агентами и проектами. | `kebab-case`, через запятую. |
| Теги будущих фаз / тем | Опциональные метки для источников, полезных не сейчас, а для будущих фаз или смежных тем. | `future-phase: agents`, `topic: orchestration`, `use-case: training-courses`. |
| Stage | Стадия жизненного цикла знания (см. lifecycle). | `observation` · `research` · `hypothesis` · `deprecated` · `rejected`. |
| Проекты | Кому источник релевантен. | `hub` · `mango` · `open-ai.ru` · `clarify-engine-ai` · `all`. |
| Запись в БЗ | Есть ли извлечённый инсайт в базе знаний и ссылка на него. | `✅` + путь в `external-insights/` · `❌` (не извлечён/отклонено). |

> 📌 **Почему `stage` не идёт дальше `hypothesis` в реестре.** Реестр фиксирует
> только стадии «наблюдения и исследования» плюс служебные терминальные статусы
> `deprecated` и `rejected`. Стадии `rfc → pattern → standard` живут в
> `governance/rfc/`, `practices/` и `standards/` — у реестра нет права
> «протащить» источник в практику в обход валидации человеком.

## Реестр

| `id` | Источник | Тип | Язык | Теги | Теги будущих фаз / тем | Stage | Проекты | Запись в БЗ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ext-001` | [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) | `blog` | `en` | `agents, workflow-patterns, orchestration, hybrid-collaboration` | `future-phase: agents, topic: orchestration` | `research` | `all` | ✅ [building-effective-agents-2026-06.md](external-insights/building-effective-agents-2026-06.md) |
| `ext-002` | [12-Factor Agents (HumanLayer)](https://github.com/humanlayer/12-factor-agents) | `github` | `en` | `agents, production, prompt-ownership, human-in-the-loop` | `future-phase: agents, topic: production-agents` | `research` | `all` | ✅ [12-factor-agents-2026-06.md](external-insights/12-factor-agents-2026-06.md) |
| `ext-003` | [GitHub Spec Kit (Spec-Driven Development)](https://github.com/github/spec-kit) | `github` | `en` | `spec-driven, requirements, agents, executable-spec` | `use-case: requirements-engineering` | `hypothesis` | `mango, clarify-engine-ai` | ✅ [spec-driven-development-2026-06.md](external-insights/spec-driven-development-2026-06.md) |
| `ext-004` | [Anthropic — Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) | `blog` | `en` | `agents, coding-agent, workflow, tooling` | `future-phase: agents, topic: coding-agent-workflow` | `observation` | `hub, open-ai.ru` | ❌ |
| `ext-005` | [OpenAI — A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | `paper` | `en` | `agents, guardrails, orchestration` | `future-phase: agents, topic: guardrails, topic: orchestration` | `observation` | `all` | ❌ |
| `ext-006` | [Diátaxis — documentation framework](https://diataxis.fr/) | `docs` | `en` | `documentation, tutorials, reference, knowledge-structure` | `use-case: training-courses` | `observation` | `hub` | ❌ |
| `ext-007` | [Habr — Контекст-инжиниринг для AI-агентов](https://habr.com/ru/companies/ru_mts/articles/) | `habr` | `ru` | `context-engineering, agents, ru-community` | `future-phase: agents, topic: context-engineering` | `observation` | `hub, mango` | ❌ |
| `ext-008` | [Anthropic — Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | `blog` | `en` | `context-engineering, agents, token-budget` | `future-phase: agents, topic: context-engineering` | `observation` | `all` | ❌ |
| `ext-009` | [Habr — Codex и локальная память на SQLite (Hermes Codex Plugin)](https://habr.com/ru/articles/1045262/) | `habr` | `ru` | `context-engineering, agent-memory, token-budget, mcp, project-rules` | `future-phase: agent-memory, topic: token-budget` | `research` | `hub, mango, open-ai.ru, clarify-engine-ai` | ✅ [agent-local-memory-context-2026-06.md](external-insights/agent-local-memory-context-2026-06.md) |
| `ext-010` | [Habr — Паттерн экономии токенов в Claude Code на правке файлов](https://habr.com/ru/articles/1045186/) | `habr` | `ru` | `token-budget, claude-code, file-editing, tool-specific` | `topic: tool-specific-file-editing` | `observation` | `hub` | ❌ (не извлечён) |
| `ext-011` | [Habr — Структурированная разработка на основе промптов (SPDD)](https://habr.com/ru/articles/1045060/) | `habr` | `ru` | `spec-driven, prompts-as-artifacts, reproducibility, workflow` | `use-case: training-courses, topic: prompt-artifacts` | `research` | `hub, mango, clarify-engine-ai, open-ai.ru` | ✅ [structured-prompt-driven-development-2026-06.md](external-insights/structured-prompt-driven-development-2026-06.md) |
| `ext-012` | [Communication with Zettelkastens](https://zettelkasten.de/communications-with-zettelkastens/) | `paper` | `en` | `research-memory, knowledge-management, zettelkasten, atomic-notes` | `topic: knowledge-object-primacy` | `research` | `hub` | ✅ [research-memory-source-intelligence.md](../../governance/rfc/research-memory-source-intelligence.md) |
| `ext-013` | [Andy Matuschak — Evergreen notes](https://notes.andymatuschak.org/z5E5QawiXCMbtNtupvxeoEX) | `docs` | `en` | `research-memory, pkm, evergreen-notes, atomic-notes` | `topic: cross-project-memory` | `research` | `hub` | ✅ [research-memory-source-intelligence.md](../../governance/rfc/research-memory-source-intelligence.md) |
| `ext-014` | [ResearchOps Community — About ResearchOps](https://researchops.community/about/) | `docs` | `en` | `researchops, knowledge-management, research-pipeline, operations` | `topic: research-operations` | `research` | `hub` | ✅ [research-memory-source-intelligence.md](../../governance/rfc/research-memory-source-intelligence.md) |
| `ext-015` | [Michael Nygard — Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | `blog` | `en` | `adr, decision-records, traceability, architecture-decisions` | `topic: decision-traceability` | `research` | `hub` | ✅ [research-memory-source-intelligence.md](../../governance/rfc/research-memory-source-intelligence.md) |
| `ext-016` | [LangChain — langchain-ai/langchain](https://github.com/langchain-ai/langchain) | `github` | `en` | `repository-architecture, agents, framework, integrations` | `topic: archetypes, topic: prompt-libraries` | `research` | `all` | ✅ [repository-archetypes-template-release.md](../../governance/rfc/repository-archetypes-template-release.md) |
| `ext-017` | [CrewAI examples](https://github.com/crewAIInc/crewAI-examples) | `github` | `en` | `repository-architecture, examples, agents, templates` | `topic: prompt-libraries, topic: examples` | `research` | `all` | ✅ [repository-archetypes-template-release.md](../../governance/rfc/repository-archetypes-template-release.md) |
| `ext-018` | [Microsoft Foundry samples](https://github.com/microsoft-foundry/foundry-samples) | `github` | `en` | `repository-architecture, samples, ai-foundry, documentation` | `topic: archetypes, topic: samples` | `research` | `all` | ✅ [repository-archetypes-template-release.md](../../governance/rfc/repository-archetypes-template-release.md) |
| `ext-019` | [Microsoft Foundry — AI solution templates](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/ai-template-get-started) | `docs` | `en` | `templates, ai-foundry, quickstart, deployment` | `topic: project-template, topic: production-readiness` | `research` | `all` | ✅ [repository-archetypes-template-release.md](../../governance/rfc/repository-archetypes-template-release.md) |
| `ext-020` | [Azure Samples — get-started-with-ai-chat](https://github.com/Azure-Samples/get-started-with-ai-chat) | `github` | `en` | `repository-architecture, ai-chat, sample, deployment` | `topic: product-spoke, topic: deployable-samples` | `research` | `all` | ✅ [repository-archetypes-template-release.md](../../governance/rfc/repository-archetypes-template-release.md) |
| `ext-021` | [GitHub Docs — GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow) | `docs` | `en` | `release-engineering, branching, github-flow, pull-requests` | `topic: dev-prod-strategy` | `research` | `all` | ✅ [repository-archetypes-template-release.md](../../governance/rfc/repository-archetypes-template-release.md) |
| `ext-022` | [Vincent Driessen — A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) | `blog` | `en` | `release-engineering, gitflow, branching, releases` | `topic: dev-prod-strategy` | `research` | `all` | ✅ [repository-archetypes-template-release.md](../../governance/rfc/repository-archetypes-template-release.md) |
| `ext-023` | [Trunk-Based Development](https://trunkbaseddevelopment.com/) | `docs` | `en` | `release-engineering, trunk-based-development, continuous-integration` | `topic: dev-prod-strategy` | `research` | `all` | ✅ [repository-archetypes-template-release.md](../../governance/rfc/repository-archetypes-template-release.md) |
| `ext-024` | [GitHub Docs — GitHub Pages publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) | `docs` | `en` | `release-engineering, github-pages, ci-cd, actions` | `topic: github-pages-deploy` | `research` | `all` | ✅ [repository-archetypes-template-release.md](../../governance/rfc/repository-archetypes-template-release.md) |
| `ext-025` | [OMG — BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2/About-BPMN) | `standard` | `en` | `enterprise-intelligence, bpmn, process-modeling` | `topic: ai-solution-architecture` | `research` | `all` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-026` | [The Open Group — TOGAF](https://www.opengroup.org/togaf) | `standard` | `en` | `enterprise-intelligence, enterprise-architecture, togaf` | `topic: ai-readiness` | `research` | `hub, open-ai.ru` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-027` | [The Open Group — ArchiMate](https://www.opengroup.org/archimate-forum/archimate-overview) | `standard` | `en` | `enterprise-intelligence, enterprise-architecture, archimate` | `topic: modeling` | `research` | `hub, open-ai.ru` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-028` | [Oxford Insights — Government AI Readiness Index 2025](https://oxfordinsights.com/ai-readiness/government-ai-readiness-index-2025/) | `docs` | `en` | `enterprise-intelligence, ai-readiness, maturity` | `topic: ai-transformation` | `research` | `hub, open-ai.ru` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-029` | [Microsoft — Agentic AI adoption maturity model](https://learn.microsoft.com/en-us/agents/adoption-maturity-model/) | `docs` | `en` | `enterprise-intelligence, ai-readiness, maturity-model` | `future-phase: agents` | `research` | `hub, open-ai.ru` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-030` | [Teresa Torres — Opportunity Solution Trees](https://www.producttalk.org/opportunity-solution-trees/) | `blog` | `en` | `opportunity-discovery, continuous-discovery, opportunity-solution-tree` | `use-case: requirements-engineering` | `research` | `hub, mango, open-ai.ru` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-031` | [Strategyn — Jobs-to-be-Done / Outcome-Driven Innovation](https://strategyn.com/jobs-to-be-done/) | `docs` | `en` | `opportunity-discovery, jobs-to-be-done, outcome-driven-innovation` | `use-case: requirements-engineering` | `research` | `mango, open-ai.ru` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-032` | [Eric Ries — The Lean Startup: Principles](https://theleanstartup.com/principles) | `docs` | `en` | `opportunity-discovery, lean-startup, validated-learning` | `topic: mvp` | `research` | `all` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-033` | [McKinsey — Economic Potential of Generative AI](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier) | `docs` | `en` | `opportunity-discovery, ai-use-cases, roi` | `topic: ai-transformation` | `observation` | `hub, open-ai.ru` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-034` | [Product School — Impact / Effort Matrix](https://productschool.com/blog/product-fundamentals/impact-effort-matrix) | `blog` | `en` | `opportunity-discovery, prioritization, impact-effort` | `topic: prioritization` | `research` | `mango, open-ai.ru` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-035` | [Parasuraman, Sheridan & Wickens — Types and Levels of Human Interaction with Automation (IEEE 2000)](https://dblp.org/rec/journals/tsmc/ParasuramanSW00.html) | `paper` | `en` | `human-ai-collaboration, levels-of-automation, human-in-the-loop` | `future-phase: agents` | `research` | `all` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-036` | [Vats et al. — Survey on Human-AI Collaboration with LFMs (arXiv:2403.04931)](https://arxiv.org/abs/2403.04931) | `paper` | `en` | `human-ai-collaboration, foundation-models, survey` | `future-phase: agents` | `research` | `hub, mango` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-037` | [Anthropic — Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) | `docs` | `en` | `human-ai-collaboration, mcp, tools, knowledge-sources` | `future-phase: agents, topic: ai-solution-architecture` | `research` | `all` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-038` | [OCEBM — Oxford Levels of Evidence (2009)](https://www.cebm.ox.ac.uk/resources/levels-of-evidence/oxford-centre-for-evidence-based-medicine-levels-of-evidence-march-2009) | `standard` | `en` | `trust-evidence, levels-of-evidence, evidence-grading` | `topic: knowledge-object` | `research` | `all` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-039` | [GRADE Working Group](https://www.gradeworkinggroup.org/) | `docs` | `en` | `trust-evidence, certainty-of-evidence, grade` | `topic: knowledge-object` | `research` | `all` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-040` | [W3C — PROV Data Model (PROV-DM)](https://www.w3.org/TR/prov-dm/) | `standard` | `en` | `trust-evidence, provenance, traceability` | `topic: knowledge-object` | `research` | `all` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-041` | [Stanford Encyclopedia of Philosophy — Argument (Toulmin)](https://plato.stanford.edu/entries/argument/) | `paper` | `en` | `trust-evidence, argumentation, toulmin` | `topic: reasoning` | `research` | `hub` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-042` | [Wasserman & Faust — Social Network Analysis](https://www.cambridge.org/core/books/social-network-analysis/90030086891EB3491D096034684EFFB8) | `paper` | `en` | `influence-network-analysis, social-network-analysis, centrality` | `future-phase: influence-analysis` | `observation` | `mango` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-043` | [Freeman — Centrality in Social Networks (1978)](https://www.bebr.ufl.edu/sites/default/files/Centrality%20in%20Social%20Networks.pdf) | `paper` | `en` | `influence-network-analysis, centrality, betweenness` | `future-phase: influence-analysis` | `observation` | `mango` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-044` | [Brin & Page — PageRank (Anatomy of a Large-Scale Hypertextual Web Search Engine)](https://snap.stanford.edu/class/cs224w-readings/Brin98Anatomy.pdf) | `paper` | `en` | `influence-network-analysis, pagerank, graph-ranking` | `future-phase: influence-analysis` | `observation` | `mango` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-045` | [Hogan et al. — Knowledge Graphs (ACM CSUR, DOI 10.1145/3447772)](https://doi.org/10.1145/3447772) | `paper` | `en` | `influence-network-analysis, knowledge-graphs, provenance` | `future-phase: knowledge-graph` | `observation` | `mango` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-046` | [Lewis et al. — Retrieval-Augmented Generation (arXiv:2005.11401)](https://arxiv.org/abs/2005.11401) | `paper` | `en` | `ai-solution-architecture, rag, knowledge-sources` | `future-phase: agents` | `research` | `all` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-047` | [Yao et al. — ReAct: Reasoning + Acting (arXiv:2210.03629)](https://arxiv.org/abs/2210.03629) | `paper` | `en` | `ai-solution-architecture, react, agent-loop` | `future-phase: agents` | `research` | `all` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |
| `ext-048` | [AWS — Well-Architected Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html) | `standard` | `en` | `ai-solution-architecture, well-architected, reference-architecture` | `topic: production-readiness` | `research` | `hub, open-ai.ru` | ✅ [methodology-research-and-proposals.md](../../governance/rfc/methodology-research-and-proposals.md) |

> 🔗 **Ссылки сознательно не загружаются автоматически.** Реестр — это карта, а
> не зеркало контента. Скрапинг и кэширование первоисточников запрещены
> (Anti-Inflation НФТ задачи); агент или человек открывает ссылку вручную, когда
> источник релевантен.

## Как добавить источник

1. Проверь, что источник действительно полезен экосистеме (не дублирует уже
   принятую практику).
2. Добавь строку в таблицу с новым `id` (`ext-NNN`), минимальными метаданными и
   `stage: observation`.
3. Если из источника извлечён конкретный вывод — создай инсайт в
   [external-insights/](external-insights/), проставь `✅` и ссылку в колонке
   «Запись в БЗ».
4. Если источник не полезен текущей фазе, но содержит идеи для будущих фаз или
   смежных тем — заполни колонку «Теги будущих фаз / тем» (`future-phase: X`,
   `topic: Y`, `use-case: Z`) и сохрани извлечённый вывод как задел на будущее.
5. Если источник имеет явные признаки хайпа/воды — поставь `stage: rejected`,
   оставь `❌ (отклонено)` и не создавай инсайт (Anti-Inflation).
6. Если источник относится только к одному проекту — он может жить в **Local
   Extension** проекта (`research/<project>/external-sources-registry.md` в споке),
   а в Base Registry попадает лишь при общей ценности (см.
   [governance/rfc/external-knowledge-integration.md](../../governance/rfc/external-knowledge-integration.md)).
7. Обнови `updated` во frontmatter.

## Как использовать (для агентов)

- Нужны паттерны агентов? → фильтруй по тегу `agents`.
- Работаешь над требованиями Mango? → фильтруй `Проекты ⊇ mango`.
- Нужен только зрелый материал? → бери `stage: research`, пропускай
  `observation`.
- Нашёл готовый вывод? → открывай связанный инсайт, а не первоисточник.

## Связанные артефакты

- [research/external-knowledge/README.md](README.md) — навигация направления.
- [external-insights/README.md](external-insights/README.md) — механизм инсайтов.
- [governance/rfc/external-knowledge-integration.md](../../governance/rfc/external-knowledge-integration.md) — RFC интеграции и Base + Local Extension.
- [governance/rfc/knowledge-lifecycle-proposal.md](../../governance/rfc/knowledge-lifecycle-proposal.md) — жизненный цикл знаний.
- [standards/research-profile.md](../../standards/research-profile.md) — правила цитирования и frontmatter.
