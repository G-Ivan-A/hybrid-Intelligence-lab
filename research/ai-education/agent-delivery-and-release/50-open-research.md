---
status: draft
version: 0.1
updated: 2026-08-18
temperature: 0.6
---

# Открытые вопросы, связи и образовательный срез

## 1. Отношение к открытому вопросу `evaluation/`

Модуль [`evaluation/`](../evaluation/00-introduction.md) оставил открытым
вопрос, как обнаруживаются дрейф и production escapes, и
[gap-анализ жизненного цикла](../../../docs/analysis/2026-08-17-agent-lifecycle-rrp-gap-analysis.md)
зафиксировал, что у стадий L10+L12 нет модуля-владельца. Этот модуль забирает
вопрос себе, но **делит его надвое**, и граница принципиальна:

| | Остаётся в [`evaluation/`](../evaluation/00-introduction.md) | Переходит сюда |
| --- | --- | --- |
| Вопрос | стал ли агент хуже и на сколько | нужно ли останавливать выкат и что возвращать |
| Объект | метрика, набор кейсов, доверительный интервал | ворота, экспозиция, откат, петля возврата |
| Сигнал дрейфа | не рассматривался | вход в процедуру проверки, не основание для отката ([`30-decision-framework.md §7`](30-decision-framework.md)) |

Аналогично закрывается отложенное место в
[`agent-context-engineering/30-decision-framework.md`](../agent-context-engineering/30-decision-framework.md):
как устроены ворота изменения промпта по содержанию — там; как версия промпта
выпускается в прод и откатывается по метрике — [§4.1 рамки](30-decision-framework.md)
этого модуля.

## 2. Что осталось открытым

| № | Вопрос | Почему не закрыт здесь | Что закрыло бы |
| --- | --- | --- | --- |
| O1 | Какое минимальное число прогонов на шаге canary даёт решение с приемлемой ошибкой | число в [§5 рамки](30-decision-framework.md) — инженерный дефолт, а не расчёт мощности | расчёт мощности на реальном разбросе метрики + проверка на истории выкатов |
| O2 | Информативнее ли shadow-прогон (S5), чем canary (S4), при равной стоимости для агентных задач | нет параллельного замера (H1) | одно изменение, обе схемы, заведомо внесённая регрессия, сравнение момента обнаружения |
| O3 | Какие пороги дрейфа применимы к текстовым входам агента | пороги PSI/JS взяты из табличного ML ([Evidently](https://docs.evidentlyai.com/metrics/explainer_drift)) и не откалиброваны на эмбеддингах | ретроспектива: доля срабатываний, совпавших с реальной деградацией |
| O4 | Какова доля ложных срабатываний у метрик, которым мы готовы отдать автооткат | без неё автооткат по [§6 рамки](30-decision-framework.md) не разрешён | прогон правила отката на истории без исполнения (dry-run) |
| O5 | Дешевле ли пин версии модели, чем незапланированный откат при плавающем алиасе (H3) | нет учёта стоимости миграций | учёт часов на миграции против числа и длительности инцидентов |
| O6 | Какая доля production escape'ов вызвана дрейфом среды и инструментов (D4), а не входов (D1) (H2) | инциденты не классифицированы по осям | разметка истории инцидентов по оси D |
| O7 | Что считать откатом для памяти (U6), которая накапливается в проде | R4 предполагает снапшот; у памяти он может быть неполным или разделяемым между пользователями | описание допустимых операций отката памяти совместно с [`memory/`](../memory/00-introduction.md) |
| O8 | Переносима ли шкала зрелости M0–M5 на команды вне Хаба | шкала собрана по образцу F0–F5, не проверена на внешних кейсах | применение шкалы к 3+ опубликованным описаниям релизных контуров |

O1, O3 и O4 приоритетнее: без них автоматическая часть контура работает на
чужих числах, что и есть риск, о котором предупреждает
[anti-trend #499](../../../docs/analysis/2026-08-17-agent-lifecycle-rrp-gap-analysis.md) —
воспроизведение формы вместо метода.

## 3. Минимальный следующий эксперимент

Один прогон, закрывающий O1 и O4 сразу, без новой инфраструктуры:

1. Взять регрессионный набор и заведомо внести в связку одну регрессию
   известного размера (правка промпта, ухудшающая один срез).
2. Прогонять набор порциями по N прогонов, N ∈ {10, 30, 100}, фиксируя, на
   какой порции правило отката из [§6 рамки](30-decision-framework.md)
   срабатывает.
3. Прогнать то же правило на **неизменённой** связке столько же раз — доля
   срабатываний здесь и есть частота ложных тревог (O4).
4. Минимальное N для шага canary — то, при котором обнаружение устойчиво, а
   ложные срабатывания ниже согласованного допуска.

Результат либо подтверждает дефолты §5–§6 рамки, либо заменяет их измеренными.
Инфраструктура замера — предмет [`evaluation/`](../evaluation/00-introduction.md),
а не этого модуля.

## 4. Связи с соседними модулями

| Модуль | Что он даёт этому модулю | Что этот модуль даёт ему |
| --- | --- | --- |
| [`evaluation/`](../evaluation/00-introduction.md) | пороги, наборы кейсов, правила прохождения | контур, в котором порог становится воротами, и путь возврата escape'а в набор |
| [`observability/`](../observability/00-introduction.md) | трассировку прогона и телеметрию | требование сравнимости канарейки с baseline и набор релизных метрик |
| [`task-processing/`](../task-processing/00-introduction.md) | ярусы G1–G7 и стоимость ошибки | правило «необратимое (R5) не выкатывается экспозицией трафика, только S5/S7» |
| [`agent-context-engineering/`](../agent-context-engineering/00-introduction.md) | устройство промпта и уровни F0–F5 | ворота выпуска и отката версии промпта ([§4.1](30-decision-framework.md)) |
| [`memory/`](../memory/00-introduction.md) | механизмы хранения и забывания | вопрос обратимости состояния памяти (O7, класс R4) |
| [`retrieval/`](../retrieval/00-introduction.md) | устройство индекса и релевантность | требование снапшота индекса как условия отката R4 |
| [`tool-use/`](../tool-use/00-introduction.md) | протокол вызова и восстановление после отказа | класс дрейфа D4 и контракт-тест инструмента как ворота |
| [`multi-agent-orchestration/`](../multi-agent-orchestration/00-introduction.md) | цену координации | конфигурацию оркестрации как единицу релиза U7 |
| [`research/cicd/`](../../cicd/README.md) | пайплайн сборки кода | место, где пайплайн заканчивается: ворота качества связки, а не сборка |

## 5. Образовательный срез

Минимальный набор, который слушатель должен унести:

1. Релизной единицей агента является связка версий U1–U7, а не изменённый файл.
2. Часть релизов инициирует провайдер: незапинованная версия модели — это чужой
   выкат в вашем проде.
3. Экспозиция — проектный параметр; для агента с побочными эффектами долю
   полномочий сокращать безопаснее, чем долю пользователей.
4. Класс отката определяется при проектировании: флаг и снапшот нужны **до**
   инцидента, а не во время.
5. Сдвиг распределения — повод замерить качество, а не откатить.
6. Инцидент не закрыт, пока не существует кейса, который бы его поймал.

Проверочное задание: взять один реальный выкат, выписать зафиксированные версии
U1–U7, назвать доступный класс отката для каждой единицы и найти ту, для которой
откат недоступен.

## 6. Глоссарий

| Термин | Значение в этом модуле |
| --- | --- |
| Релизный набор | зафиксированные версии всех единиц U1–U7 одновременно |
| CACE | Changing Anything Changes Everything: изолированных изменений в ML-системе нет |
| Ворота (W1–W5) | конъюнкция условий, без которых выкат не начинается |
| Экспозиция | доля пользователей **или** объём полномочий, доступных новой версии |
| Canary | выкат на подмножество трафика с анализом метрик перед расширением |
| Blue-green | две полные среды с переключением трафика ради мгновенного возврата |
| Shadow | прогон новой версии на копии трафика без выдачи ответа пользователю |
| Kill switch | переключатель аварийного выключения функции без передеплоя |
| Дрейф D1–D5 | классы расхождения прода с условиями, при которых система проверялась |
| Откат R1–R5 | классы возврата, от веса трафика до необратимого действия |
| Production escape | дефект, обнаруженный в проде и не пойманный воротами |
| MTTR / time to restore | время восстановления сервиса, одна из четырёх метрик DORA |

## 7. Источники

Первичные (вендоры, платформы, инженерные публикации):
[Google SRE Book, Release Engineering](https://sre.google/sre-book/release-engineering/) ·
[Google SRE Book, Postmortem Culture](https://sre.google/sre-book/postmortem-culture/) ·
[Google SRE Workbook, Canarying Releases](https://sre.google/workbook/canarying-releases/) ·
[Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) ·
[Anthropic, Model deprecations](https://docs.claude.com/en/docs/about-claude/model-deprecations) ·
[OpenAI, A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) ·
[OpenAI, Deprecations](https://platform.openai.com/docs/deprecations) ·
[Fowler, BlueGreenDeployment](https://martinfowler.com/bliki/BlueGreenDeployment.html) ·
[Fowler, CanaryRelease](https://martinfowler.com/bliki/CanaryRelease.html) ·
[Hodgson, Feature Toggles](https://martinfowler.com/articles/feature-toggles.html) ·
[LaunchDarkly, Flags](https://docs.launchdarkly.com/home/flags) ·
[Unleash, Activation strategies](https://docs.getunleash.io/reference/activation-strategies) ·
[Kubernetes, Rolling update](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment) ·
[Istio, Traffic shifting](https://istio.io/latest/docs/tasks/traffic-management/traffic-shifting/) ·
[Argo Rollouts](https://argoproj.github.io/argo-rollouts/) ·
[Flagger](https://docs.flagger.app/) ·
[DORA, Four keys](https://dora.dev/guides/dora-metrics-four-keys/) ·
[LangSmith](https://docs.langchain.com/langsmith/home) ·
[LangSmith, Prompt management](https://docs.langchain.com/langsmith/manage-prompts) ·
[Braintrust](https://www.braintrust.dev/docs) ·
[Arize Phoenix](https://arize.com/docs/phoenix) ·
[W&B Weave](https://weave-docs.wandb.ai/) ·
[promptfoo](https://www.promptfoo.dev/docs/intro) ·
[Evidently, Drift metrics](https://docs.evidentlyai.com/metrics/explainer_drift) ·
[Huyen, Data Distribution Shifts and Monitoring](https://huyenchip.com/2022/02/07/data-distribution-shifts-and-monitoring.html).

Исследовательские:
[Sculley et al., Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems) ·
[Breck et al., The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) ·
[Sclar et al., FormatSpread](https://arxiv.org/abs/2310.11324).

Реестр внешних источников:
[`research/external-knowledge/external-sources-registry.md`](../../external-knowledge/external-sources-registry.md).

## 8. Оформление доказательной базы

Постановка задачи допускала отдельный каталог `evidence/`; модуль следует
альтернативному оформлению «по образцу `agent-context-engineering/`», прямо
разрешённому постановкой: доказательная база — это §7 этого файла плюс строки в
[реестре внешних источников](../../external-knowledge/external-sources-registry.md).
Причина выбора: каталога `evidence/` в корпусе не существует ни у одного модуля,
а действующий валидатор `tools/validate-evidence-structure.sh` описывает только
`research/<domain>/exp/<issue-slug>/` — введение седьмого каталога создало бы
новое соглашение вне стандартов Хаба (Anti-Inflation). Экспериментальные данные,
когда они появятся по §3, размещаются в `research/ai-education/exp/` по
действующему стандарту.
