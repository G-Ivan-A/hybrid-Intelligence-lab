---
status: draft
version: 0.1
updated: 2026-09-08
temperature: 0.1
type: research
context: [ba, meta-model, taxonomy, run-modes, deprecation, execution-package, empirical-snapshot]
method: corpus-measurement + name-decomposition + reference-graph-count
scope: mango-only
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/563"
based_on:
  - research/ba-requirements/exp/ba-meta-model-563/meta-model-inputs.json
related_artifacts:
  - "projects/ba-gigacode-implementation/ba-meta-model/00-introduction.md"
  - "projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md"
  - "research/ba-requirements/exp/ba-meta-model-563/README.md"
  - "docs/adr/2026-09-adr-013-run-modes-deprecation.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/563"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/561"
---

# Снимок входов BA Meta-Model на 2026-09-08

> **Назначение.** Датированное **измерение** того, из чего собирается
> каноническая мета-модель: режимы запуска промптов, покрытие словарей операций
> и процессов, продуктовая привязка прогонов. Интерпретация и решения — в модуле
> [`projects/ba-gigacode-implementation/ba-meta-model/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/00-introduction.md)
> и в
> [ADR-013](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-013-run-modes-deprecation.md).
> Снимок отделён от модуля, потому что корпус растёт: на другом коммите числа
> будут другими.

**Корпус.** [`mango_ba_prompts`](https://github.com/G-Ivan-A/mango_ba_prompts)
на коммите `8cbf82aa73129ec5747af07f790aaf438b0fb6e9`: 67 прогонов `runs/`,
24 активных промпта `prompts/` (архив `prompts/archive/` и исполняемые файлы
`*.executable.md` исключены).

**Измеритель.**
[`exp/ba-meta-model-563/measure-meta-model-inputs.py`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-meta-model-563/measure-meta-model-inputs.py),
сырой результат —
[`meta-model-inputs.json`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-meta-model-563/meta-model-inputs.json),
лог —
[`measure-meta-model-inputs.log`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-meta-model-563/measure-meta-model-inputs.log).

## 1. Режим запуска встроен в идентичность промпта

Имя активного промпта разбирается как `<предмет>-<операция>-<режим>`. Разбор
удался для всех 24 файлов: **режим является частью имени артефакта**, а не его
параметром.

| Режим | Промптов |
| --- | --- |
| `stepwise` | 10 |
| `oneshot` | 9 |
| `legacy` | 5 |
| **Итого** | **24** |

Различных способностей (пара «предмет + операция») — **13**. Кратность
дублирования: **1.85 промпта на способность**. У **9 из 13** способностей есть
более одного режимного варианта.

## 2. Режимные варианты одной способности не имеют общего скелета

Для каждой пары вариантов одной способности сравнивались подписи нумерованных
разделов промпта (подпись огрублена до части строки до первого двоеточия).

| Величина | Значение |
| --- | --- |
| Пар вариантов одной способности | 13 |
| Средний коэффициент Жаккара по подписям разделов | **0.077** |
| Пар с совпадающим множеством подписей | **0** |
| Пар с совпадающим порядком разделов | **0** |
| Максимум по парам | 0.4 (`fr-validation`, `oneshot` ↔ `stepwise`) |
| Отношение объёмов в паре | от 1.22 до 3.30 |

Восемь из тринадцати пар дали Жаккар `0.0` — общих подписей разделов нет вовсе.

## 3. Маршрутизация по режимам не подтверждается прогонами

Ссылки прогонов на промпты взяты из `related_artifacts` в `metadata.yaml`.

| Величина | Значение |
| --- | --- |
| Прогонов всего | 67 |
| Прогонов без единой ссылки на промпт | **50** |
| Прогонов со ссылкой на `stepwise`-промпт | 14 |
| Прогонов со ссылкой на `oneshot`-промпт | 3 |
| Прогонов со ссылкой на `legacy`-промпт | 3 |
| Активных промптов, ни разу не упомянутых прогонами | **11 из 24** |

## 4. Словарь операций покрыт наполовину

Объявлено 13 операций. Промпты покрывают **6**: `documentation`, `ingestion`,
`modeling`, `solution_design`, `understanding`, `validation`.

Без единого промпта — **7**: `governance`, `impact_analysis`, `quality`,
`release_readiness`, `research`, `reverse_requirements`, `risk_analysis`.
Операций, употреблённых вне словаря, нет: имена промптов словарь не нарушают.

## 5. Словарь процессов не используется для идентификации прогона

Объявлено 9 процессов. В поле `process:` метаданных прогонов встретился **один**
из них — `fr-generation`. Остальные **65** значений поля лежат вне словаря: это
метки задач (`task-930-amocrm-comment-and-tag-fields`), а не имена процессов.

| Величина | Значение |
| --- | --- |
| Процессов объявлено | 9 |
| Объявленных процессов, встреченных в прогонах | 1 |
| Меток `process:` вне словаря | 65 |

## 6. Продуктовая привязка артефакта отсутствует

| Величина | Значение |
| --- | --- |
| Прогонов, объявляющих домен продукта в метаданных | **5 из 67** |
| Прогонов, где лексические маркеры дают ровно один домен | 1 |
| Прогонов, где маркеры дают более одного домена | 66 |
| Прогонов без маркеров | 0 |

## 7. Границы измерения

- **Разбор имени, а не содержания.** Режим определяется суффиксом файла.
  Промпт, в котором режим объявлен внутри текста, а в имени нет, измерением не
  учитывается — таких в корпусе нет, но правило зависит от соглашения об именах.
- **Скелет — только нумерованные строки.** Промпт, структурированный
  маркированным списком или жирным текстом, будет измерен как малоструктурный.
  Это **занижает** совпадение вариантов, а не завышает его.
- **Ссылка прогона на промпт — объявление, а не факт исполнения.** Прогон мог
  использовать промпт и не объявить его. Поэтому §3 доказывает отсутствие
  **прослеживаемости** режима, а не отсутствие его применения.
- **Лексические маркеры доменов неразделяющие.** 66 прогонов из 67 попадают
  более чем в один домен. Величина пригодна ровно для одного вывода —
  «по тексту продукт не определяется» — и непригодна для долей по доменам.
- **Одна спица.** Все числа получены на `mango_ba_prompts`. Переносимость на
  другие предметные области здесь не проверяется.
