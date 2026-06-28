---
status: draft
version: 0.1
updated: 2026-06-01
temperature: 0.1
type: internal-analysis
scope: repo-wide
context: [governance, repository-strategy, research-lifecycle, team-c]
method: interpretive-synthesis
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/87"
related_artifacts:
  - "research/hub/2026-05-28-project-context-and-bootstrap-patterns.md"
  - "governance/repo-model.md"
  - "standards/research-profile.md"
  - "standards/team-contract.md"
---

# Интерпретация аудита стратегии governance от команды C

## 1. Назначение

Документ фиксирует интерпретацию предложений команды C из issue #87 и переводит
их в проверяемые выводы для развития governance, research lifecycle и маршрута
`research -> recommendation -> standard`.

Граница анализа: это не независимая внешняя валидация рынка или OSS-практик, а
структурирование входного исследования команды C для дальнейшего human review.
Внешние сравнения, упомянутые в исходном тексте команды C, здесь используются
как контекст предложений, но не как проверенные факты.

## 2. Ключевой вывод

Команда C оценивает репозиторий как систему, которая уже выходит за рамки
"папки с промптами" и начинает формировать управляемую экосистему гибридной
работы людей и ИИ. Практическая интерпретация: сильнейший актив репозитория
сейчас - не отдельные промпты и не будущий универсальный фреймворк, а
governance-архитектура для human + AI collaboration.

Из этого следует рабочее ограничение: следующая фаза должна стабилизировать
минимальный governance-набор на реальных workflow, а не расширять дерево
артефактов заранее.

## 3. Что команда C считает сильным

| Наблюдение команды C | Интерпретация для репозитория | Практическое следствие |
| --- | --- | --- |
| Governance становится first-class architecture layer. | Контракты, lifecycle и правила участия уже являются частью архитектуры знания, а не вторичной документацией. | Сохранять governance в активной карте артефактов и проверять его через issues/PR, но не плодить новые документы без боли. |
| Переход от framework-first к practice-first зрелый. | Репозиторий правильно строит практики через исследования, а не через раннее объявление большой методологии. | Держать `frameworks/` пустым/минимальным до повторяемых доказанных кейсов. |
| Модель `research -> recommendation -> standard` перспективна. | Стандарт должен появляться после накопленного evidence и согласованной рекомендации. | В каждом research-файле отделять наблюдение, рекомендацию, next action и критерий перевода в issue/standard. |
| README-driven architecture удобна людям и ИИ. | Локальные README работают как короткие точки входа и уменьшают стоимость context handoff. | Развивать блоки "быстрый контекст" в проектах через пилоты, а не через обязательный стандарт сразу. |
| Разделение concept/product vision/standards/practices/governance полезно. | Таксономия сущностей уже снижает смешение уровней. | Зафиксировать hierarchy и словарь ролей артефактов до масштабирования. |
| Repository maturity analysis может стать продуктовым вектором. | Будущий AI-аудит репозиториев возможен, если текущие governance-паттерны будут проверены на практике. | Не превращать это в продуктовую roadmap до 2-3 пилотных циклов. |

## 4. Риски и ограничения

| Риск | Как проявляется | Что контролировать |
| --- | --- | --- |
| Governance overgrowth | Контракты, standards и policies растут быстрее реальных operational scenarios. | Правило "нет governance-артефакта без операционной боли". |
| Semantic noise | Термины `meta`, `tests`, `TEAM_CONTRACT`, `framework`, `practice`, `methodology` могут пересекаться. | Отдельный semantic cleanup через issue, без переименований в текущем research PR. |
| Неявная governance hierarchy | Не до конца ясно, что выше: `AI_GOVERNANCE`, `CONTRIBUTING`, `TEAM_PRACTICES`, standards или practices. | Согласовать lightweight hierarchy перед новыми обязательными нормами. |
| Research entropy | Research быстро растет и может стать архивом несвязанных выводов. | Легкий lifecycle: draft/reviewed/published или draft/reviewed/canonical/archived после human review. |
| Сложный onboarding | Новому участнику нужно прочитать много governance-concepts до действия. | README-driven навигация, краткие точки входа и operational examples. |
| Недостаток operational examples | Много теории, мало демонстраций реального цикла issue -> artifact -> review -> standard. | Добавить 2-3 пилотных сценария перед расширением стандартов. |
| Premature enterprise architecture | Структура начинает выглядеть как платформа governance до проверки практической пользы. | Сначала стабилизация, затем формализация. |
| Machine-readable governance premature | YAML/structured governance полезен в будущем, но сейчас может добавить complexity. | Зафиксировать как later-stage candidate, не внедрять сейчас. |

## 5. Предложения команды C в операционном виде

### 5.1 Governance minimum

Сейчас полезнее определить минимальный набор активных governance-артефактов и
границы их роли, чем создавать новые уровни. Минимум уже есть:
`AI_GOVERNANCE.md`, `CONTRIBUTING.md`, `governance/repo-model.md`,
`standards/README.md`, `standards/research-profile.md`,
`standards/issue-workflow.md` и `governance/artifact-map.md`.

Рекомендация: следующий governance artifact создавать только при повторяющейся
операционной боли, зафиксированной в issue, PR review или research findings.

### 5.2 Lightweight hierarchy

Команда C предлагает прояснить hierarchy без тяжелой методологии. Рабочая
гипотеза для согласования:

| Layer | Роль | Пример в репозитории |
| --- | --- | --- |
| Concept | Зачем существует репозиторий и где его границы. | `CONCEPT.md` |
| Governance contracts | Как работают люди и ИИ, кто принимает решения. | `AI_GOVERNANCE.md`, `CONTRIBUTING.md` |
| Repository model | Где живут артефакты и когда создаются новые. | `governance/repo-model.md` |
| Standards / profiles | Обязательные форматы для повторяемых работ. | `standards/research-profile.md`, `standards/issue-workflow.md` |
| Practices | Рекомендации, проверяемые на workflow до стандартизации. | Research-рекомендации и будущие pilot examples |
| Frameworks | Методологии, появляющиеся только после доказанного gap. | `frameworks/` |

### 5.3 Lifecycle для research

Команда C отдельно предупреждает о риске research entropy. В текущем
репозитории уже есть `draft`, `reviewed`, `published`, `canonical`,
`superseded`, `experimental` в validator frontmatter. Нужно не расширять
статусы, а согласовать, какие из них применяются к research и что означает
переход между ними.

Минимальный вопрос для backlog: когда research считается достаточно проверенным,
чтобы перейти из `draft` в `reviewed`, и когда вывод из research становится
standard или practice?

### 5.4 Pilot cycles перед расширением

Команда C рекомендует провести 2-3 pilot cycles и проверить:

- какие governance artifacts реально открываются при работе;
- где возникают повторяющиеся вопросы review;
- какие recommendations доходят до GitHub issues;
- какие README-блоки экономят context handoff;
- какие документы не используются и могут остаться research, а не standard.

## 6. Рекомендации для backlog

| ID | Рекомендация | Почему это нужно | Следующее действие |
| --- | --- | --- | --- |
| `TC-GOV-001` | Закрепить принцип "нет governance-артефакта без операционной боли". | Снижает риск governance overgrowth. | Создать issue на уточнение `governance/repo-model.md` после review этого research. |
| `TC-GOV-002` | Согласовать lightweight governance hierarchy. | Убирает вопрос, что является обязательным контрактом, а что рекомендацией. | Создать issue с таблицей hierarchy и критериями конфликтов между артефактами. |
| `TC-GOV-003` | Провести semantic cleanup audit. | Снижает пересечение терминов `framework`, `practice`, `contract`, `profile`, `policy`. | Создать research/task issue без немедленных переименований. |
| `TC-GOV-004` | Описать research lifecycle transitions. | Предотвращает research entropy и случайную канонизацию черновиков. | Создать issue на правила перехода `draft -> reviewed -> published/canonical/superseded`. |
| `TC-GOV-005` | Добавить 2-3 operational examples. | Делает governance проверяемым в реальных workflow. | Начать с примера `issue -> research -> recommendation -> backlog issue`. |
| `TC-GOV-006` | Отложить machine-readable governance до появления повторной потребности. | Сохраняет простоту и избегает premature complexity. | Вернуться после pilot cycles или повторяющихся automation needs. |

## 7. Вопросы для human review

1. Согласен ли Founder & PO с принципом "нет governance-артефакта без
   операционной боли" как обязательным decision rule?
2. Нужна ли отдельная governance hierarchy сейчас, или достаточно встроить
   таблицу hierarchy в существующий `governance/repo-model.md`?
3. Какие lifecycle statuses считать применимыми именно к research:
   `draft/reviewed/published` или `draft/reviewed/canonical/archived`?
4. Какие 2-3 workflow выбрать как pilot cycles для проверки governance minimum?
5. Какие semantic cleanup candidates нужно вынести первыми:
   `meta -> governance`, `tests -> tools/validation`, `TEAM_CONTRACT ->
   COLLABORATION_CONTRACT` или другой список?
6. Когда возвращаться к machine-readable governance: после pilot cycles, после
   появления CI/automation или после внешнего spoke-проекта?

## 8. Связанные источники

| Источник | Использование |
| --- | --- |
| Issue #87 | Входные предложения команды C и acceptance criteria. |
| `research/hub/2026-05-28-project-context-and-bootstrap-patterns.md` | Механизм `recommendation -> issue`, context handoff и bootstrap patterns. |
| `governance/repo-model.md` | Anti-Inflation principle и правило размещения артефактов. |
| `standards/research-profile.md` | Требования к research frontmatter, traceability и ограничениям. |
| `standards/team-contract.md` | Контекст team contract, AI governance и project-level adaptation. |
