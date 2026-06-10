---
status: canonical
version: 1.0
updated: 2026-06-09
ai-generated: true
type: rfc
context: [hub-and-spoke, htom, spoke, terminology, governance, templates, migration]
method: creative-analysis + concept-separation + migration-mapping
scope: repo-wide
related_artifacts:
  - "templates/htom/README.md"
  - "templates/spoke/README.md"
  - "governance/repo-model.md"
  - "governance/rfc/rfc-two-cases-of-project-initialization.md"
  - "standards/glossary.md"
  - "projects/README.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/201"
---

# RFC: разделение концепций «HTOM-команда» и «spoke-репозиторий»

Решение по RFC — за человеком (см. финальный блок «Решение за человеком»).

## 1. Проблема и контекст

Фаундер зафиксировал концептуальную ошибку в терминологии Хаба. До сих пор
«проекты» Хаба и «ДНК-шаблон» `templates/spoke/` неявно отождествляли **два
разных явления**:

- **гибридную команду** (люди + ИИ-агенты), которая работает итеративно по
  governance-контрактам и имеет минимальную структуру;
- **production-репозиторий продукта** с кодом, тестами и CI/CD.

Это разные сущности с разным жизненным циклом. Слово «spoke» применялось к
команде, тогда как настоящий spoke — это **отдельный продукт**. Первый настоящий
spoke Хаба — портал `open-ai.ru`.

Этот RFC разделяет понятия, фиксирует определения, даёт сравнительную таблицу,
обоснование, классификацию текущих проектов и карту переименований (миграции).

> ⚠️ **Что этот RFC НЕ делает.** Он не вводит новых тяжёлых процессов и не
> переименовывает всё разом. Миграция — поэтапная, с сохранением обратной
> совместимости (старые пути задокументированы в разделе «Карта переименований»
> и в `CHANGELOG.md`).

## 2. HTOM-команда (определение)

**HTOM-команда** (*Hybrid Team Operating Model team*) — это **гибридная команда
людей и ИИ-агентов**, которая работает итеративно по governance-контрактам Хаба.
Это **команда, а не продукт**.

- **Артефакты-ядро (HTOM-контракты).** `AI_GOVERNANCE.md` (конституция команды),
  `AI_SESSION_HANDOVER_PROMPT.md` (готовая «доверенность» для запуска агента),
  `AI_QUICK_RULES.md` (одностраничные правила агента).
- **Цикл.** Итеративный; минимальная структура «по запросу» (Anti-Inflation):
  каталоги появляются при операционной боли, а не «на вырост».
- **Структура.** Минимальный геном: контракты + `README.md`, `CONTRIBUTING.md`,
  `CHANGELOG.md`, каркасы `docs/adr/`, `docs/audit/`. **Без `src/`, `tests/`,
  тяжёлого CI/CD** — это не продукт.
- **Шаблон.** [`templates/htom/`](../../templates/htom/README.md) (бывший
  `templates/spoke/`).
- **Примеры.** `mango_ba_prompts`, `repo-development`, сам Хаб
  `hybrid-Intelligence-lab`.

## 3. Spoke-репозиторий (определение)

**Spoke-репозиторий** — это **отдельный продукт с production-кодом**, связанный с
Хабом, но живущий своим жизненным циклом. Это **продукт, а не команда** (хотя над
ним может работать своя HTOM-команда).

- **Артефакты-ядро.** Production-код в `src/`, автотесты в `tests/`, продуктовая
  документация в `docs/`, **CI/CD** в `.github/workflows/`.
- **Цикл.** Полный SDLC отдельного продукта: ветки, релизы, деплой, secrets,
  runtime.
- **Структура.** Полная структура продукта (`src/`, `docs/`, `tests/`, CI/CD).
- **Шаблон.** [`templates/spoke/`](../../templates/spoke/README.md) (создан
  заново в рамках этого RFC).
- **Пример.** `open-ai.ru` — первый настоящий spoke Хаба. Продуктовая концепция
  (L2) и решения (L3) описываются стандартами
  `standards/webportal-product-concept-standard.md` и
  `standards/webportal-solution-concept-standard.md`.

## 4. Сравнительная таблица

| Критерий | HTOM-команда | Spoke-репозиторий |
| --- | --- | --- |
| **Что это** | Гибридная команда людей + ИИ | Отдельный продукт с production-кодом |
| **Команда** | Команда и есть сущность | Над продуктом работает (HTOM-)команда |
| **Цикл** | Итеративный, минимальная структура «по запросу» | Полный SDLC: ветки, релизы, деплой |
| **Структура** | Минимальный геном: HTOM-контракты, README/CONTRIBUTING/CHANGELOG, каркасы docs | Полная: `src/`, `tests/`, `docs/`, CI/CD |
| **Ядро-артефакты** | `AI_GOVERNANCE.md`, `AI_SESSION_HANDOVER_PROMPT.md`, `AI_QUICK_RULES.md` | `src/`, `tests/`, `.github/workflows/` (CI/CD) |
| **Код** | Кода нет (или вспомогательный) | Production-код с первого дня |
| **Шаблон** | `templates/htom/` | `templates/spoke/` |
| **Примеры** | `mango_ba_prompts`, `repo-development`, Хаб | `open-ai.ru` |
| **Когда использовать** | Нужно организовать гибридную работу по правилам Хаба | Нужно строить и поставлять отдельный продукт |

## 5. Обоснование разделения

1. **Разный жизненный цикл.** Команда живёт итерациями и минимальной структурой;
   продукт живёт релизами, тестами и деплоем. Один шаблон не может обслуживать оба
   режима без противоречий (например, Anti-Inflation запрещает пустые `src/` в
   команде, но для продукта `src/` нужен сразу).
2. **Корректная терминология.** «Spoke» в модели hub-and-spoke — это **спица**,
   отдельный продукт-репозиторий. Называть так команду — концептуальная ошибка,
   которая путает агентов и людей.
3. **Чистота валидации.** Валидатор может проверять *разные* вещи: для
   HTOM-команды — наличие HTOM-контрактов; для spoke — наличие CI/CD. Слияние
   понятий делало проверки двусмысленными.
4. **Масштабирование.** По мере появления настоящих споков (первый — `open-ai.ru`)
   Хабу нужен отдельный, честный шаблон production-репозитория.

## 6. Классификация текущих проектов

| Проект | Тип | Обоснование |
| --- | --- | --- |
| `mango_ba_prompts` | **HTOM-команда** | Гибридная работа над промптами/знаниями; не production-продукт с кодом. |
| `repo-development` | **HTOM-команда** | Развитие самого Хаба: governance, проверки; команда, а не продукт. |
| `hybrid-Intelligence-lab` (Хаб) | **HTOM-команда** (хаб) | Сам Хаб — гибридная команда governance-уровня, центр модели hub-and-spoke. |
| `open-ai.ru` | **Spoke-репозиторий** | Первый настоящий spoke: отдельный продукт-портал с кодом и CI/CD. |

## 7. Карта переименований (миграция, old → new)

Геном HTOM-команды переехал из `templates/spoke/` в `templates/htom/`. Старое имя
`templates/spoke/` переиспользовано под **новый** шаблон production-спока. Старые
пути в исторических записях (`CHANGELOG.md`, бэклог) сохраняются как ледджер;
активные ссылки переключены на новые пути.

| Старый путь (genome) | Новый путь (genome) |
| --- | --- |
| `templates/spoke/AI_GOVERNANCE.md` | `templates/htom/AI_GOVERNANCE.md` |
| `templates/spoke/AI_QUICK_RULES.md` | `templates/htom/AI_QUICK_RULES.md` |
| `templates/spoke/AI_SESSION_HANDOVER_PROMPT.md` | `templates/htom/AI_SESSION_HANDOVER_PROMPT.md` |
| `templates/spoke/README.md` (genome) | `templates/htom/README.md` |
| `templates/spoke/CONTRIBUTING.md` (genome) | `templates/htom/CONTRIBUTING.md` |
| `templates/spoke/CHANGELOG.md` | `templates/htom/CHANGELOG.md` |
| `templates/spoke/docs/adr/.gitkeep` | `templates/htom/docs/adr/.gitkeep` |
| `templates/spoke/docs/audit/.gitkeep` | `templates/htom/docs/audit/.gitkeep` |
| `templates/spoke/.github/ISSUE_TEMPLATE/task.md` | `templates/htom/.github/ISSUE_TEMPLATE/task.md` |
| `templates/spoke/tools/validate-repository-structure.sh` | `templates/htom/tools/validate-repository-structure.sh` |
| `templates/spoke/init.sh` | `templates/htom/init.sh` |

**Новый шаблон production-спока** (создан заново, не миграция):

| Новый путь (spoke) | Роль |
| --- | --- |
| `templates/spoke/README.md` | Визитка spoke-продукта: структура `src/`/`tests/`/CI-CD, связь с Хабом. |
| `templates/spoke/CONTRIBUTING.md` | Workflow вклада в spoke, требования к тестам и зелёному CI. |
| `templates/spoke/.github/workflows/ci.yml` | Базовый CI/CD: линт + тесты на push и pull request. |

## 8. План поэтапной миграции (итеративно, с проверкой)

1. **Шаг 1 (этот PR).** `git mv templates/spoke → templates/htom`; реврайт
   терминологии в геноме; создание нового `templates/spoke/` (production);
   синхронное обновление валидаторов; обновление активных docs и ссылок; этот RFC.
2. **Шаг 2 (после согласования).** При появлении работы над `open-ai.ru` —
   bootstrap первого настоящего спока из `templates/spoke/`.
3. **Шаг 3 (по запросу).** Чистка исторических планов (бэклог, RFC-планы) по мере
   их естественного пересмотра — без массового переписывания ledger-записей.

Каждый шаг проверяется локально:
[`tools/validate-repository-structure.sh`](../../tools/validate-repository-structure.sh)
и [`tools/validate-frontmatter.sh`](../../tools/validate-frontmatter.sh).

## 9. Связь с другими артефактами

- Термины — единый источник истины [standards/glossary.md](../../standards/glossary.md)
  (термины «HTOM-команда» и «Spoke-репозиторий» добавлены туда).
- Два кейса инициализации — [rfc-two-cases-of-project-initialization.md](rfc-two-cases-of-project-initialization.md).
- Модель репозитория — [governance/repo-model.md](../repo-model.md).
- Когда выносить проект в отдельный spoke — [projects/README.md](../../projects/README.md).

## 10. Решение за человеком

Финальные решения остаются за фаундером и human reviewer:

- утверждение разделения понятий и терминов;
- утверждение классификации проектов (раздел 6);
- момент bootstrap первого настоящего спока `open-ai.ru`;
- глубина чистки исторических планов (Шаг 3).

ИИ-агент не принимает эти решения самостоятельно: он готовит изменение,
фиксирует rationale и запрашивает review.
