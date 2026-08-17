---
status: draft
version: 0.1
updated: 2026-08-17
temperature: 0.6
---

# Открытые вопросы, связи и образовательный срез

## 1. Отношение к deferred-триггеру B-091

Триггер [B-091](../../../pr-ops/backlog.md) («Проверить Reference Pattern на
не-AI доменах», P2, deferred (triggered)) называет среди доменов проверки
**Prompt Engineering**. Этот модуль его **не закрывает** и не отменяет — предметы
разные:

| | B-091 | Этот модуль |
| --- | --- | --- |
| Вопрос | переносится ли **форма** Reference Research Pattern на домены за пределами AI-инженерии | что известно индустрии по **содержанию** L2-темы «промпт и контекст агента» |
| Объект проверки | методология Хаба (шесть файлов, теория→практика) | предметная область |
| Домены | Business Analysis, Requirements Engineering, Prompt Engineering | только граница «Человек → Агент» |
| Зависимости | B-089, B-090 (валидация на Memory и Agents) | закрытие L2-пробела из [gap-анализа](../../../docs/analysis/2026-08-17-agent-lifecycle-rrp-gap-analysis.md) |

Фактическое влияние на B-091 — два уточнения, которые фиксируются здесь, а
решение по ним принимает фаундер (AI Governance, Rule 4):

1. **Prompt Engineering перестал быть «не-AI доменом»** в смысле B-091. Как
   показывает [`10-theory.md`](10-theory.md), предмет к 2025–2026 растворился в
   context engineering и остался внутри AI-инженерии. Если B-091 запускается
   ради проверки переносимости паттерна **вне** AI, этот домен из его выборки
   стоит исключить — иначе проверка тавтологична.
2. **Существование этого модуля — слабое свидетельство в пользу гипотезы
   B-091**, но не её проверка: домен близкий, а не внешний. Настоящая проверка
   требует домена без корпуса arXiv и вендорских engineering-блогов, где
   evidence-классы из [`00-introduction.md`](00-introduction.md#объект-и-метод)
   пришлось бы пересобрать.

## 2. Что осталось открытым

| № | Вопрос | Почему не закрыт здесь | Что закрыло бы |
| --- | --- | --- | --- |
| O1 | Где проходит реальный потолок `U` для наших задач | пороги в [`30-decision-framework.md §1`](30-decision-framework.md) — инженерные дефолты, а не замер | прогон одной задачи при долях заполнения окна 30/50/70/90% на фиксированном наборе |
| O2 | Какая доля окна уходит на B5 в длинном прогоне | требуется телеметрия по блокам, которой нет | учёт токенов по блокам на 20+ шагах |
| O3 | Сколько теряет compaction (D2) | закрытые внутренние eval-наборы вендоров | сравнение результата при D2 против полной истории на задачах, укладывающихся в окно |
| O4 | Переносимы ли вендорские рекомендации о позиции инструкции между семействами моделей | руководства расходятся ([`10-theory.md §4`](10-theory.md)) | один промпт, два размещения, две модели, один набор кейсов |
| O5 | Насколько велик разброс от формы на агентных задачах | FormatSpread измерен на классификационных задачах, не на агентных циклах | ≥3 эквивалентных разметки одного агентного промпта на общем наборе |
| O6 | Окупается ли F3 (регрессионный набор) на нашем масштабе | нет данных о цене сборки golden set в Хабе | учёт времени на сборку набора против числа откатов промпта |
| O7 | Совместимы ли кэширование префикса и активное вытеснение | вытеснение меняет начало истории и обнуляет кэш | замер стоимости прогона при D1/D2 против отсутствия вытеснения |

O1–O3 приоритетнее остальных: без них рамка решений остаётся откалиброванной по
чужим числам.

## 3. Минимальный следующий эксперимент

Один прогон, закрывающий O1 и O5 сразу, реализуемый без новой инфраструктуры:

1. Взять задачу с проверяемым результатом и 20+ шагами.
2. Зафиксировать 3 семантически эквивалентные разметки системной инструкции.
3. Прогнать каждую при заполнении окна ≈30% и ≈70%.
4. Сравнить долю успешных прогонов; разброс между разметками — базис, ниже
   которого улучшения промпта не считаются улучшениями
   ([`30-decision-framework.md §7`](30-decision-framework.md)).

Результат либо подтверждает дефолты §1 рамки, либо заменяет их измеренными.
Инфраструктура замера — предмет [`evaluation/`](../evaluation/00-introduction.md),
а не этого модуля.

## 4. Связи с соседними модулями

| Модуль | Что он даёт этому модулю | Что этот модуль даёт ему |
| --- | --- | --- |
| [`task-processing/`](../task-processing/00-introduction.md) | ярусы G1–G7 и гипотезу H12 «промпт — худший носитель критического правила» | правило переноса требования из промпта на ярус по измеримому порогу |
| [`memory/`](../memory/00-introduction.md) | механизмы хранения и забывания | критерий «что обязано покинуть окно на этом шаге» (ось D) |
| [`retrieval/`](../retrieval/00-introduction.md) | релевантность найденного | момент попадания найденного в окно (ось C) |
| [`tool-use/`](../tool-use/00-introduction.md) | протокол вызова и восстановление после отказа | требования к тексту описания инструмента и текста ошибки (ось E) |
| [`multi-agent-orchestration/`](../multi-agent-orchestration/00-introduction.md) | цену параллелизма и слияния | изоляцию подзадачи как стратегию вытеснения (D5) |
| [`evaluation/`](../evaluation/00-introduction.md) | метрики и golden sets | зрелость F3 как ворота изменения промпта |
| [`observability/`](../observability/00-introduction.md) | телеметрию прогона | требование учитывать токены по блокам B1–B7 (вопросы O1–O2) |

## 5. Образовательный срез

Минимальный набор, который слушатель должен унести:

1. Контекст — бюджет, а не свободное место; «добавить в промпт» имеет цену.
2. Вход состоит из семи блоков с разными владельцами и скоростью изменения.
3. Конфликт правил решается уровнем иерархии, а не капслоком.
4. Улучшение промпта, меньшее разброса от переформатирования, — не улучшение.
5. Критическое требование из промпта переносится в код, а не переписывается.

Проверочное задание: взять существующий агентный промпт, разложить его на
B1–B7, найти в нём хотя бы одно требование, которому место на ярусе G2–G7, и
обосновать перенос порогом из [`30-decision-framework.md §3`](30-decision-framework.md).

## 6. Глоссарий

| Термин | Значение в этом модуле |
| --- | --- |
| Контекст-инжиниринг | курирование состава окна на каждом шаге агентного цикла |
| Окно `W` | максимальная длина входа модели в токенах |
| Рабочий потолок `U` | доля `W`, выше которой поведение не считается предсказуемым |
| Блоки B1–B7 | составляющие входа: инструкция, инструменты, знания, память, история, запрос, схема ответа |
| Compaction | замена фрагмента истории её кратким изложением |
| Вытеснение | удаление содержимого из окна для освобождения бюджета |
| Ярусы G1–G7 | шкала гарантий носителя требования из `task-processing/` |
| Уровни F0–F5 | зрелость работы с промптом как артефактом |

## 7. Источники

Первичные (вендоры и спецификации):
[Anthropic, Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) ·
[Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) ·
[Anthropic, Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) ·
[Anthropic, Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) ·
[Anthropic, Prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) ·
[Anthropic, System prompts](https://docs.claude.com/en/release-notes/system-prompts) ·
[OpenAI, A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) ·
[OpenAI, GPT-4.1 prompting guide](https://cookbook.openai.com/examples/gpt4-1_prompting_guide) ·
[OpenAI, Prompt caching](https://platform.openai.com/docs/guides/prompt-caching) ·
[OpenAI Model Spec](https://model-spec.openai.com/) ·
[LangChain, The rise of context engineering](https://blog.langchain.com/the-rise-of-context-engineering/) ·
[LangSmith, Prompt management](https://docs.langchain.com/langsmith/manage-prompts) ·
[CrewAI, Agents](https://docs.crewai.com/en/concepts/agents) ·
[Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/) ·
[promptfoo](https://www.promptfoo.dev/docs/intro) ·
[Cognition, Don't build multi-agents](https://cognition.com/blog/dont-build-multi-agents) ·
[Chroma, Context Rot](https://research.trychroma.com/context-rot).

Исследовательские:
[Liu et al., Lost in the Middle](https://arxiv.org/abs/2307.03172) ·
[RULER](https://arxiv.org/abs/2404.06654) ·
[NoLiMa](https://arxiv.org/abs/2502.05167) ·
[Sclar et al., FormatSpread](https://arxiv.org/abs/2310.11324) ·
[Wallace et al., Instruction Hierarchy](https://arxiv.org/abs/2404.13208) ·
[Schulhoff et al., The Prompt Report](https://arxiv.org/abs/2406.06608) ·
[Sahoo et al., Prompt engineering survey](https://arxiv.org/abs/2402.07927) ·
[Xi et al., The Rise and Potential of LLM Based Agents](https://arxiv.org/abs/2309.07864) ·
[Wei et al., Chain-of-Thought](https://arxiv.org/abs/2201.11903) ·
[Kojima et al., Zero-shot CoT](https://arxiv.org/abs/2205.11916) ·
[Wang et al., Self-Consistency](https://arxiv.org/abs/2203.11171) ·
[Yao et al., ReAct](https://arxiv.org/abs/2210.03629) ·
[Agarwal et al., Many-Shot ICL](https://arxiv.org/abs/2404.11018) ·
[Zhou et al., APE](https://arxiv.org/abs/2211.01910) ·
[Khattab et al., DSPy](https://arxiv.org/abs/2310.03714).

Реестр внешних источников:
[`research/external-knowledge/external-sources-registry.md`](../../external-knowledge/external-sources-registry.md).
