---
status: draft
version: 0.2
updated: 2026-06-01
temperature: 0.1
ai-generated: true
type: internal-analysis
context: [mango, context-handoff, project-bootstrap, recommendations, governance-strategy]
method: retrospective-analysis + minimal-pattern-design + interpretive-synthesis
scope: repo-wide
related_artifacts:
  - "mango_ba_prompts/README.md"
  - "mango_ba_prompts/prompts/experiments/tz-stats-prototype-2026-05.md"
  - "mango_ba_prompts/prompts/experiments/user-story_gen-from-raw-request_2026-05-26.md"
  - "mango_ba_prompts/prompts/experiments/usecase_gen-stepwise-alignment_2026-05-26.md"
  - "mango_ba_prompts/prompts/experiments/prompts-audit-2026-05-26.md"
  - "mango_ba_prompts/prompts/experiments/prompts-selftest-2026-05-26.md"
  - "research/mango/2026-05-rag-mapping-roadmap.md"
  - "research/hub/2026-05-team-c-governance-strategy-audit.md"
  - "standards/project-structure-inheritance.md"
  - "governance/repo-model.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/81"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/87"
---

# Как передавать контекст и создавать проекты предсказуемо

Документ остается черновиком для согласования.

Цель исследования - на опыте Mango предложить минимальный способ передавать
контекст между чатами, создавать новые project areas без неожиданных папок и
не терять рекомендации, которые появляются в экспериментах и исследованиях.
Версия 0.2 дополняет выводы интерпретацией аудита стратегии governance от
команды C из issue #87.

Основное ограничение: не создавать новые корневые папки, не вводить глубокую
вложенность и не превращать один проектный опыт в большой стандарт раньше
времени.

## 🔹 Опыт проекта Mango (кратко)

Mango дал полезный контраст: репозиторий уже умеет разделять research,
project-context и prompt assets, но переход от исследования к следующему
действию пока держится на ручной памяти участника.

Что сработало:

| Наблюдение | Где видно | Вывод |
| --- | --- | --- |
| Project context живет рядом с проектом, а не в общем промпте. | `mango_ba_prompts/README.md` описывает проект, стандарты, prompt assets и связь с `research/mango/`. | README проекта подходит как первый источник контекста для нового чата. |
| Research и project artifacts разделены по ответственности. | `research/mango/` хранит классификацию, lifecycle и RAG-roadmap; `mango_ba_prompts/` хранит prompts, experiments и Mango-only glossary. | Новому проекту не нужно копировать все research-артефакты внутрь себя. |
| Экспериментальные отчеты сохраняют rationale, а готовые prompt assets короткие. | `prompts-audit-2026-05-26.md` отделил длинные эксперименты от шести copy-paste prompts. | Хороший паттерн: эксперимент длинный, готовый рабочий артефакт короткий. |
| `_exp` и `_simple` варианты решают проблему доступности контекста. | `mango_ba_prompts/prompts/*_exp-2026-05.md` ссылаются на repo context, а `*_simple-2026-05.md` работают через вопросы. | Если контекст недоступен, ИИ должен перейти к диалогу, а не выдумывать missing knowledge. |
| RAG-roadmap начинает с одного Markdown registry, а не с инфраструктуры. | `research/mango/2026-05-rag-mapping-roadmap.md` предлагает `kb/product-matrix.md` как будущий навигатор. | Минимальный файл с контрактом полезнее преждевременной платформы. |

Что создавало трение:

| Трение | Где видно | Почему важно |
| --- | --- | --- |
| Быстрый контекст не выделен отдельным блоком. | `mango_ba_prompts/README.md` богатый, но новому чату нужно вручную выжимать цель, статус и следующий шаг. | При смене чата растут затраты токенов и риск потерять актуальное состояние. |
| В прототипах естественно появляется глубокая структура. | `tz-stats-prototype-2026-05.md` предлагает `experiments/tz-stats/prompts/reports/logs/runs/`. | Для прототипа это понятно, но как стандарт проекта такая вложенность становится дорогой. |
| Placeholder-папки выглядят как обязательный шаблон. | Прежний Mango-контекст показывал `kb/`, `docs/`, `experiments/`, `decisions/` как точки расширения. | Новый проект может скопировать больше папок, чем реально нужно в первые часы. |
| Рекомендации остаются в конце отдельных документов. | `prompts-selftest-2026-05-26.md` и эксперименты содержат идеи на будущее и вопросы для согласования. | Следующий проект может не найти эти идеи и повторить тот же путь. |
| Нет короткого маршрута от согласованной идеи к issue. | В Mango есть много полезных `future ideas`, но нет единого поля "создать задачу". | Согласованные улучшения легко остаются рекомендациями без владельца и next action. |

Ключевой вывод: Mango не требует нового большого стандарта. Достаточно двух
легких паттернов - блок "Быстрый контекст" в README проекта и маленькая таблица
рекомендаций с маршрутом в GitHub issue.

## 🔹 Дополнение команды C: governance как ограничитель bootstrap

Аудит команды C подтверждает направление этого исследования, но добавляет
важный governance-ограничитель: развитие структуры должно идти через реальные
workflow и операционную боль, а не через заранее построенную методологию.

Суммаризация результатов команды C:

| Результат | Как это влияет на bootstrap и context handoff |
| --- | --- |
| Репозиторий уже выглядит как governed hybrid intelligence repository ecosystem, а не как набор разрозненных промптов. | Новый проект должен получать контекст через существующие README, governance contracts и research links, а не через копирование большого шаблона папок. |
| Governance становится first-class architecture layer. | AI-агент при bootstrap должен читать `AI_GOVERNANCE.md`, `CONTRIBUTING.md`, `governance/repo-model.md` и ближайший README до создания артефактов. |
| Переход `framework-first -> practice-first` снижает abstraction inflation. | Не создавать framework или новый standard из одного кейса; сначала фиксировать recommendation и проверять ее на втором workflow. |
| Модель `research -> recommendation -> standard` сильна, если evidence отделено от идеи. | Таблица recommendations должна показывать источник, боль, статус, next action и критерий перевода в issue. |
| README-driven architecture остается правильным паттерном. | Блок "Быстрый контекст" лучше сначала пилотировать в README проекта, а не выносить в новый обязательный документ. |
| Главный риск - governance overgrowth. | Правило по умолчанию: "нет governance artifact без operational pain". |

Предложения команды C, которые нужно учитывать в следующих задачах:

| Направление | Предложение | Почему не делать прямо в этом PR |
| --- | --- | --- |
| Governance minimum | Закрепить правило "нет governance artifact без operational pain". | Требуется human review, потому что это меняет decision rule репозитория. |
| Governance hierarchy | Уточнить отношение `CONCEPT`, `AI_GOVERNANCE`, `CONTRIBUTING`, standards, practices и frameworks. | Это отдельная governance-задача, а не research-only изменение. |
| Research lifecycle | Согласовать переходы `draft -> reviewed -> published/canonical/superseded`. | Нужен общий lifecycle contract, чтобы не размножать статусы. |
| Semantic cleanup | Проверить термины `meta`, `tests`, `TEAM_CONTRACT`, `framework`, `practice`, `policy`. | Переименования требуют отдельного issue и могут затронуть много ссылок. |
| Operational examples | Добавить 2-3 примера полного цикла `issue -> research -> recommendation -> backlog issue`. | Сначала нужно выбрать пилотные workflow и owner. |
| Machine-readable governance | Вернуться к YAML/structured governance после появления повторной automation need. | Сейчас это premature complexity. |

## 🔹 Проблемы (5 пунктов, как выше)

| # | Проблема | Проявление на опыте Mango | Риск |
| --- | --- | --- | --- |
| 1 | Потеря контекста при смене чата. | Контекст проекта распределен между `mango_ba_prompts/README.md`, `research/mango/`, prompt files и experiments. | Новый ИИ получает неполную историю или тратит время на повторное чтение всего дерева. |
| 2 | Непредсказуемое создание папок. | Прототипы легко предлагают вложенные `prompts/`, `reports/`, `logs/`, `runs/` внутри эксперимента. | Репозиторий теряет плоскую навигацию, а review начинает обсуждать дерево вместо результата. |
| 3 | Новые папки вне стандарта репо. | Для Mango уже есть project-only `kb/`, `prompts/`, `docs/`, `experiments/`, `standards/`, `decisions/`, но граница их копирования в новый проект не очевидна. | Локальное решение начинает выглядеть как repo-wide standard без согласования. |
| 4 | Рекомендации "в никуда". | Идеи фиксируются в self-test и экспериментах, но не агрегируются в одно место с owner/status. | Следующие проекты заново открывают те же улучшения. |
| 5 | Нет явного механизма "идея -> задача". | После согласования рекомендации нет короткого формата issue draft и ссылки назад на источник идеи. | Хорошие предложения не доходят до реализации или оформляются заново вручную. |

## 🔹 Предложенные решения (минималистичные, с обоснованием)

### 1. Потеря контекста при смене чата

Проблема: новому чату нужно быстро понять цель проекта, текущий статус,
важные артефакты и ближайшее действие.

Вариант А: добавить в `projects/{project}/README.md` блок `## Быстрый контекст`
из 5 строк:

```markdown
## Быстрый контекст

- Цель: ...
- Сейчас: ...
- Ключевые артефакты: ...
- Следующее действие: ...
- Открытые вопросы: ...
```

Вариант Б: при активном PR добавлять в описание PR короткий блок `Context
handoff`, который копируется в следующий чат вместе со ссылкой на PR.

Рекомендация: вариант А как default. Он не создает новый файл, живет в
естественной точке входа проекта и помогает людям так же, как ИИ. Вариант Б
использовать только для долгих PR, где состояние меняется быстрее README.

### 2. Непредсказуемое создание папок

Проблема: запрос "создай структуру проекта" часто провоцирует ИИ создать
визуально полный каталог, хотя пользователь просил только старт.

Вариант А: правило bootstrap по умолчанию - создать только
`projects/{project}/README.md`. Подкаталоги добавлять только если пользователь
явно попросил или есть немедленный артефакт, который некуда положить.

Вариант Б: перед созданием дерева показать proposed tree в issue/PR comment и
попросить подтверждение, если дерево содержит больше README или подпапки не из
`standards/project-structure-inheritance.md`.

Рекомендация: вариант А для обычного старта проекта. Вариант Б включать при
любой новой папке вне уже разрешенного списка. Это сохраняет плоскую философию
и не блокирует быстрый старт.

### 3. Новые папки вне стандарта репо

Проблема: локальная папка внутри проекта может быть полезной, но без правила
непонятно, это исключение, эксперимент или новый стандарт для всех проектов.

Вариант А: не создавать нестандартную папку сразу. Зафиксировать ее как
candidate в README проекта:

```markdown
## Кандидаты на структуру

| Папка | Зачем нужна | Scope | Решение |
| --- | --- | --- | --- |
| `archive/` | ... | project-only | не создавать до повторной потребности |
```

Вариант Б: если folder pattern повторился в двух проектах, создать отдельное
issue на обновление `standards/project-structure-inheritance.md`.

Рекомендация: вариант А для первого случая, вариант Б только после повторения.
Так локальное решение не становится стандартом без evidence.

### 4. Рекомендации "в никуда"

Проблема: идеи по улучшению появляются в research и experiments, но их сложно
собрать перед новым проектом.

Вариант А: в README проекта добавить компактный раздел
`## Рекомендации и открытые решения` с максимум 10 активными строками.

Вариант Б: если строк больше 10 или проект уже использует `docs/`, вынести
таблицу в `projects/{project}/docs/recommendations.md` и оставить ссылку из
README.

Рекомендация: вариант А для Mango и новых проектов. Вариант Б нужен только
после реального роста списка. Это дает 80% пользы без нового обязательного
артефакта.

### 5. Механизм "идея -> задача"

Проблема: даже согласованная идея требует ручного превращения в issue.

Вариант А: каждая рекомендация получает статус и next action:
`idea`, `agreed`, `issue-draft`, `issue-created`, `done`, `rejected`.

Вариант Б: для `agreed` рекомендации автор сразу готовит короткий issue draft
в том же PR или issue comment.

Рекомендация: объединить А и Б. Статус показывает, что делать дальше, а issue
draft снижает стоимость создания задачи до копирования текста в GitHub.

## 🔹 Чек-лист для ИИ (≤10 пунктов)

- [ ] Прочитал issue, последние comments, ближайший README проекта и релевантный standard до создания файлов.
- [ ] Пользователь явно попросил вложенные папки? Если нет - начинаю с README или одного целевого файла.
- [ ] Новая папка есть в `standards/project-structure-inheritance.md`? Если нет - предлагаю ее как candidate, а не создаю.
- [ ] Можно ли закодировать смысл в имени файла вместо новой папки? Если да - выбираю файл.
- [ ] Обновил или предложил блок `Быстрый контекст`, если проектный статус изменился.
- [ ] Не смешал experiment report и готовый copy-paste prompt в одном артефакте.
- [ ] Зафиксировал рекомендации в README или существующем `docs/`, указав статус и next action.
- [ ] Для согласованной рекомендации подготовил issue draft и ссылку на источник.
- [ ] Запустил локальные validators и не оставил служебные файлы вроде root `.gitkeep`.

## 🔹 Механизм «рекомендация → задача»

### Где фиксировать рекомендации

Минимальный порядок:

| Scope рекомендации | Где фиксировать по умолчанию | Когда выносить отдельно |
| --- | --- | --- |
| Только один проект | `projects/{project}/README.md`, раздел `Рекомендации и открытые решения`. | Когда активных строк больше 10 или README становится шумным. |
| Один проект с уже активным `docs/` | `projects/{project}/docs/recommendations.md`. | Сразу, если recommendations являются рабочим журналом проекта. |
| Repo-wide улучшение | GitHub issue с ссылкой на source research/experiment. | Не создавать отдельный root backlog, пока GitHub issues закрывают задачу. |
| Новый structural pattern | Сначала recommendation, затем issue на `standards/project-structure-inheritance.md` после повторения. | После второго независимого проекта или повторяющегося review comment. |

Рекомендуемый формат таблицы:

| ID | Источник | Рекомендация | Scope | Польза | Усилие | Статус | Следующее действие | Issue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `REC-001` | `mango_ba_prompts/prompts/experiments/prompts-selftest-2026-05-26.md` | Добавить единый prompt с режимом `exp | simple`. | mango-only | medium | small | idea | обсудить с PO | - |

Поля `Польза` и `Усилие` держат 80/20-фильтр видимым. Если польза не выше
усилия, рекомендация остается `idea` или закрывается как `rejected`.

### Как превращать рекомендацию в issue

1. Зафиксировать recommendation в таблице с источником и статусом `idea`.
2. Получить human-согласование и поменять статус на `agreed`.
3. Подготовить issue draft:

```markdown
## Context
Source: <путь к research/experiment/README и короткая причина>

## Problem
Что болит и где это повторилось.

## Proposal
Минимальное изменение на 1-2 часа.

## Acceptance Criteria
- [ ] ...

## Forbidden Changes
- Не создавать новые root folders.
- Не добавлять глубокую вложенность без отдельного согласования.
```

4. Создать GitHub issue и вставить ссылку в колонку `Issue`.
5. В PR сослаться на исходную recommendation и закрыть issue.
6. Если recommendation повторилась в нескольких проектах, создать отдельную
задачу на standard update, а не расширять локальный README задним числом.

### Применение к Mango без новых файлов

Для Mango после миграции достаточно одного будущего изменения в
`mango_ba_prompts/README.md`: добавить блок `Быстрый контекст` и короткую
таблицу рекомендаций. Отдельный `docs/recommendations.md` пока не нужен:
текущий список идей можно держать в README, пока он помещается в 10 строк и не
становится рабочим backlog.

### Backlog candidates по аудиту команды C

Эти рекомендации не нужно выполнять внутри текущего research PR. Их полезнее
оформлять отдельными GitHub issues после human review, чтобы не расширять
governance быстрее, чем появляются operational scenarios.

| ID | Источник | Рекомендация | Scope | Польза | Усилие | Статус | Следующее действие | Issue |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `TC-GOV-001` | `research/hub/2026-05-team-c-governance-strategy-audit.md` | Закрепить принцип "нет governance artifact без operational pain". | repo-wide | high | small | idea | согласовать формулировку с Founder & PO | - |
| `TC-GOV-002` | `research/hub/2026-05-team-c-governance-strategy-audit.md` | Описать lightweight governance hierarchy. | repo-wide | high | medium | idea | подготовить issue на `governance/repo-model.md` или отдельный раздел в existing governance | - |
| `TC-GOV-003` | `research/hub/2026-05-team-c-governance-strategy-audit.md` | Провести semantic cleanup audit для `framework/practice/policy/profile/contract`. | repo-wide | medium | medium | idea | собрать термины и конфликтующие места без переименований | - |
| `TC-GOV-004` | `research/hub/2026-05-team-c-governance-strategy-audit.md` | Согласовать lifecycle transitions для research. | research | high | medium | idea | определить критерии `draft -> reviewed` и `reviewed -> standard/practice` | - |
| `TC-GOV-005` | `research/hub/2026-05-team-c-governance-strategy-audit.md` | Провести 2-3 pilot cycles перед новыми standards/frameworks. | repo-wide | high | medium | idea | выбрать pilot workflow и метрики использования артефактов | - |
| `TC-GOV-006` | `research/hub/2026-05-team-c-governance-strategy-audit.md` | Отложить machine-readable governance до повторной automation need. | repo-wide | medium | small | idea | вернуться после pilot cycles или появления CI/automation pain | - |

## ❓ Вопросы для согласования

1. Нужно ли добавить блок `Быстрый контекст` во все текущие project README или
   начать только с Mango и новых проектов?
2. Держим рекомендации сначала в README проекта или сразу используем
   `projects/{project}/docs/recommendations.md` для проектов с активным `docs/`?
3. Должен ли ИИ всегда запрашивать подтверждение перед созданием любой папки
   вне `standards/project-structure-inheritance.md`?
4. Когда переносить этот чек-лист из research в standard: после review этого
   документа или после проверки на втором проекте?
5. Какой статус считать достаточным для создания GitHub issue:
   `agreed` от PO в comment, PR review approval или отдельное issue label?
6. Согласуем ли принцип "нет governance artifact без operational pain" как
   обязательный decision rule?
7. Нужна ли отдельная governance hierarchy сейчас, или достаточно встроить ее в
   существующий `governance/repo-model.md`?
8. Какие lifecycle statuses применять к research после human review:
   `draft/reviewed/published`, `draft/reviewed/canonical/superseded` или иной
   минимальный набор?
9. Какие 2-3 workflow выбрать для pilot cycles перед расширением standards или
   frameworks?
10. Какие semantic cleanup candidates выносить первыми в backlog:
    `meta`, `tests`, `TEAM_CONTRACT` или пересечение `framework/practice/policy`?
