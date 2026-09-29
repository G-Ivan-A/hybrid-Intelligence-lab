---
status: draft
version: 0.1
updated: 2026-09-29
temperature: 0.3
type: presentation
scope: mango-only
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/646"
based_on: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/projects/ba-ai-process/ba-meta-model"
related_artifacts:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/presentation/2026-09-29-meta-model-presentation-speaker-script.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-29-ba-ai-process-runtime-options.md"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-requirements-run-forensics.md"
  - "https://github.com/G-Ivan-A/mango_ba_prompts"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/ba-meta-model-overview.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/646"
---

# Мета-модель бизнес-анализа и среды её исполнения: слайды

Пакет из двух документов для презентации Руководителю отдела AI-разработки
Mango. Этот документ — слайды. Устный текст, мостики между слайдами и ответы
на вопросы — в
[сценарии для диктора](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/presentation/2026-09-29-meta-model-presentation-speaker-script.md);
номера слайдов в обоих документах совпадают.

## Как собран пакет

- **Assertion-Evidence.** Заголовок слайда — законченное утверждение, которое
  можно оспорить. Тело — доказательство: схема, число или ссылка, а не
  пересказ заголовка.
- **Один слайд — одна мысль.** 3–5 тезисов, одна выделенная метрика. Всё, что
  не помещается, уходит в сценарий или в ответы на вопросы.
- **Каждое число проверяемо.** У каждой метрики есть абсолютная ссылка на
  артефакт, где она измерена. Числа без источника в пакет не попали.
- **Статус не завышается.** Для этапов конвейера и сред показано, что работает,
  что в пилоте и что спроектировано. Для технического руководителя
  переоценка готовности дороже, чем честный пробел.
- **Сквозная метафора:** хаос сырых запросов проходит через стандарт и
  превращается в контракт, пригодный для передачи.

### Соответствие смысловым блокам постановки

| Блок постановки | Слайд |
| --- | --- |
| — (титул) | 1 |
| 1. Область применения | 2 |
| 2. Боль | 3 |
| — (эмпирика: от промптов к модели) | 4 |
| 3. Концепция мета-модели | 5 |
| 4. Ключевой прорыв | 6 |
| 5. Конвейер | 7 |
| 6. Среда исполнения | 8 |
| 7. Масштабирование | 9 |
| — (путь и решения) | 10 |

Слайд 4 добавлен сверх постановки: без него прорыв на слайде 6 выглядит как
тезис, а не как вывод из 60+ прогонов.

### Единый визуальный стиль для промптов

Все промпты ниже написаны на английском: генераторы изображений понимают его
точнее. Каждый промпт заканчивается общим стилевым суффиксом, чтобы слайды
выглядели как одна серия:

```text
STYLE: clean isometric technical illustration, deep navy background,
off-white linework, single amber accent colour for the key element,
generous negative space, no text, no letters, no logos, 16:9
```

Для Midjourney добавьте `--ar 16:9 --style raw`; для DALL-E укажите формат
1792×1024. Надписи на изображении не генерируются: текст слайда накладывается
в редакторе, иначе генератор исказит кириллицу.

---

## Слайд 1. Требования для крупных клиентов можно производить как инженерный продукт, а не как авторский текст

**Подзаголовок:** Мета-модель бизнес-анализа Mango: от 60+ прогонов промптов к
контракту с fail-closed проверкой.

- От репозитория промптов к мета-модели: апрель — сентябрь 2026.
- 69 зафиксированных прогонов на реальных задачах, 583 коммита.
- Мета-модель v0.4: 11 сущностей, 4 инварианта, 3 гейта.
- Пилот на АРМ бизнес-аналитика, вектор — серверное ядро.

> **Ключевая мысль:** мы не автоматизируем мышление аналитика. Мы делаем его
> результат проверяемым.

**Промпт для изображения:**

```text
A chaotic cloud of loose paper notes, chat bubbles and voice waveforms
on the left flows through a precise geometric gate in the centre and
leaves on the right as a neat stack of identical, bound specification
documents, each linked by thin lines back to its source note.
STYLE: clean isometric technical illustration, deep navy background,
off-white linework, single amber accent colour for the key element,
generous negative space, no text, no letters, no logos, 16:9
```

**Источники:**
[мета-модель](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/projects/ba-ai-process/ba-meta-model),
[репозиторий прогонов `mango_ba_prompts`](https://github.com/G-Ivan-A/mango_ba_prompts).

---

## Слайд 2. В командах крупных клиентов требование — это обязательство, а не заметка

**Блок 1. Область применения.**

- Клиент приходит с бизнес-обращением; на выходе — ТЗ, по которому
  разрабатывают и которое подписывают в договоре.
- Продуктовый ландшафт широк: ВАТС, контакт-центр, API, личный кабинет —
  42 продуктовые возможности Mango в 8 доменах, каждая сопоставлена с
  отраслевыми каталогами.
- Комплаенс: ошибка в требовании становится спором о приёмке, а не правкой
  документа.
- Одно обращение проходит минимум три передачи: клиент → БА → системный
  анализ → разработка.

> **Метрика:** 42 продуктовые возможности в 8 доменах — у каждой свой
> словарь, ограничения и типовые ошибки.

**Визуальное доказательство:** цепочка передач «клиент → БА → СА →
разработка → договор» с точками, где теряется контекст.

**Промпт для изображения:**

```text
A relay race of four stylised figures passing a glowing document baton
along a long corridor of server racks and contract folders; at every
hand-off a few fragments of the baton drift away into the dark.
STYLE: clean isometric technical illustration, deep navy background,
off-white linework, single amber accent colour for the key element,
generous negative space, no text, no letters, no logos, 16:9
```

**Источники:**
[таксономия продуктов Mango](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/product-taxonomy/mango-products.yaml),
[таксономия продуктов IT/телеком](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/product-taxonomy/telecom-products.yaml).

---

## Слайд 3. Между сырым запросом и ТЗ стандарт теряется на каждом ручном шаге

**Блок 2. Боль.** Факты из разбора всех 67 прогонов `mango_ba_prompts`.

- 17 документов с требованиями — 17 разных структур: воспроизводимость
  структуры `M-1 = 0.0`.
- 50 из 67 прогонов не объявляют входной артефакт: результат нельзя
  воспроизвести.
- ИИ заполняет пустоты правдоподобным: в RUN-0015 выдуманы целевые значения
  NFR (5 мин, 100 мс, 2 с, 24/7) — все отклонены человеком.
- Контекст смещается: в RUN-0063 пять из шести FR описывали уже существующее
  поведение, а не изменение.
- Итог ручной сборки: без содержательной правки принято 2 из 32 прогонов с
  вердиктом — 6%.

> **Метрика:** `M-1 = 0.0` — ни один результирующий документ не повторил
> структуру другого.

**Визуальное доказательство:** сетка из 17 миниатюр документов с разным
составом разделов; ни одна строка не совпадает.

**Промпт для изображения:**

```text
Seventeen specification documents laid out in a grid, each with a
different internal skeleton of blocks and sections, none of them
matching; a single empty template frame hovers above, unused.
STYLE: clean isometric technical illustration, deep navy background,
off-white linework, single amber accent colour for the key element,
generous negative space, no text, no letters, no logos, 16:9
```

**Источники:**
[форензика 67 прогонов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-requirements-run-forensics.md),
[замер структуры артефактов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-08-artifact-structure-variance-facts.md),
[базовая линия метрик](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/40-practice-and-cases.md),
[базовая линия 6%](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/methodology-unification/40-practice-and-cases.md).

---

## Слайд 4. Улучшение промптов перестало давать результат: 60+ прогонов показали, что дефект сидит до текста

**Эмпирика.** Эволюция от репозитория промптов к мета-модели.

- **Апрель — июнь:** прогоны в веб-чате; один черновой промпт «для БА»
  разделён на 23 стандартных файла. После первой реальной сессии правки
  откатили: промпт меняется только через эксперимент.
- **Август:** 56 прогонов на реальных задачах; признано, что evals и
  эталонов нет.
- **Сентябрь:** форензика 67 прогонов — четыре класса отказов. Варианты
  одного промпта совпадают по структуре на 0.077 по Жаккару; 10 из 12
  конструкций мета-модели нет ни в одном из 24 промптов.
- **Вывод:** наследие — свидетельство, а не норма. Модель строится заново,
  прогоны служат доказательной базой.

> **Из форензики:** «Лечение только prompt-ом эти отказы не закрывает. Нужен
> исполняемый контракт […] и тремя гейтами: детерминированным, семантическим
> и человеческим».

**Визуальное доказательство:** шкала времени «RUN-0001 → RUN-0069» с тремя
вехами: промпты → форензика → мета-модель.

**Промпт для изображения:**

```text
A timeline running left to right: on the left a tangled heap of
handwritten prompt cards, in the middle a forensic magnifying glass
over a row of numbered run folders, on the right a clean architectural
blueprint of connected blocks rising from the same folders.
STYLE: clean isometric technical illustration, deep navy background,
off-white linework, single amber accent colour for the key element,
generous negative space, no text, no letters, no logos, 16:9
```

**Источники:**
[каталог прогонов](https://github.com/G-Ivan-A/mango_ba_prompts/tree/main/runs),
[журнал изменений `mango_ba_prompts`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/CHANGELOG.md),
[разбор эксперимента 1027](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/analysis/experiment-1027-analysis.md),
[входы мета-модели и Жаккар 0.077](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-08-meta-model-inputs-facts.md),
[промпты трёх режимов](https://github.com/G-Ivan-A/mango_ba_prompts/tree/main/prompts),
[влияние наследия на норму](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-09-legacy-normative-influence-facts.md),
[ADR-014: наследие — свидетельство](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-014-legacy-evidence-not-baseline.md),
[ADR-013: отказ от режимов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-013-run-modes-deprecation.md),
[форензика прогонов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-requirements-run-forensics.md).

---

## Слайд 5. Мета-модель раскладывает работу БА до уровня, на котором её можно проверить

**Блок 3. Концепция мета-модели.**

- Строгая декомпозиция: **Продукт → Процесс → Операция → Артефакт**.
  Процесс состоит из навыков, навык — из атомарных операций.
- Закрытые словари: 33 навыка-подпроцесса, 31 атомарная операция; значение
  вне словаря — отказ на входе, а не импровизация.
- Закон производства: вход × продукт × система × операция × актор —
  через контракт и гейт — выход + след.
- Четыре инварианта: нет шага без входа (`MM-1`), нет гейта без контракта
  (`MM-2`), каждый выход несёт след (`MM-3`), продукт объявлен до шага
  (`MM-4`).

> **Формула:** `Artifact_in × Product × System × Operation × Actor ──
> Contract ──▶ Gate ──▶ Artifact_out + Trace`

**Визуальное доказательство:** четырёхуровневая пирамида с атомарной
операцией в основании и контрактом на каждой грани.

**Промпт для изображения:**

```text
An exploded architectural diagram of four stacked translucent layers:
a product layer on top, a process layer, a layer of many small identical
operation cubes, and at the bottom a row of finished artefacts; thin
vertical threads connect every artefact back up to its operation and
product.
STYLE: clean isometric technical illustration, deep navy background,
off-white linework, single amber accent colour for the key element,
generous negative space, no text, no letters, no logos, 16:9
```

**Источники:**
[теория мета-модели](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/10-theory.md),
[таксономия сущностей](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/20-taxonomy.md),
[таксономия процессов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/process-taxonomy/20-taxonomy.md),
[таксономия операций](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/operation-taxonomy/20-taxonomy.md).

---

## Слайд 6. Мы не автоматизируем мысль: мы оцифровываем когнитивную операцию и ставим на её выход контракт

**Блок 4. Ключевой прорыв.**

- **Гипотеза:** когнитивная работа БА плохо поддаётся прямой генерации.
  Даже строгий пошаговый промпт даёт правдоподобный текст, а не проверяемое
  требование.
- **Решение:** работа разложена на 31 атомарную операцию пяти когнитивных
  классов. Каждый класс задаёт свой механизм контроля.
- Извлечение сверяется с источником, преобразование — со схемой, порождение
  идёт через источник и человека, выбор — через обоснование.
- **Fail-closed:** нет входа, источника или продукта — шаг останавливается и
  задаёт вопрос. Пустой слот с причиной лучше выдуманного значения.

> **Гипотеза на прогонах:** RUN-0018 — промпт из 8 шагов с самопроверками,
> 8 галлюцинаций, одна дошла до результата: «Механика промпта соблюдена,
> достоверность фактов не обеспечена». RUN-0059 с fail-closed правилом
> оставил пробел вместо выдуманных endpoint'ов.

**Визуальное доказательство:** таблица «класс операции → механизм контроля →
риск» (5 строк).

| Класс операции | Контроль | Риск без контроля |
| --- | --- | --- |
| извлечение | сверка с источником | пропуск |
| преобразование | схема выхода | потеря при переносе |
| порождение | источник + человек | галлюцинация |
| проверка | схема вердикта | ложное «соответствует» |
| оценка и выбор | обоснование + человек | немотивированный выбор |

**Промпт для изображения:**

```text
A human brain rendered as a loose, glowing nebula on the left; on the
right the same energy is split into five precise crystalline modules,
each sealed inside its own transparent inspection chamber with a
closed lock that only opens when a checklist lights up.
STYLE: clean isometric technical illustration, deep navy background,
off-white linework, single amber accent colour for the key element,
generous negative space, no text, no letters, no logos, 16:9
```

**Источники:**
[пять когнитивных классов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/operation-taxonomy/10-theory.md),
[золотые формы BCREQ и опровержение «улучшить промпт»](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-bcreq-golden-forms-and-feasibility.md),
[форензика прогонов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-requirements-run-forensics.md),
[кейс RUN-0018](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/methodology-unification/40-practice-and-cases.md).

---

## Слайд 7. Конвейер превращает сырой запрос в проверенный документ за пять шагов и два гейта

**Блок 5. Решение как цель.**

1. **Нормализация:** транскрипт и переписка приводятся к входному контракту
   `C-IN`; без объявленного продукта шаг не стартует.
2. **Сверка:** факты привязываются к документации и кейсам; неясности
   становятся вопросами заказчику, а не допущениями.
3. **Генерация по золотому шаблону:** одна форма BCREQ из 7 разделов для
   API, личного кабинета и контакт-центра; у каждого требования — ссылка на
   источник.
4. **Гейты:** `G-mach` проверяет структуру и схему, `G-human` принимает
   смысл и спорные выборы.
5. **Проекция:** один рабочий документ детерминированно собирается в
   представления для бизнеса, согласования, разработки и договора.

> **Метрика:** две сборки одного рабочего документа дают побайтно одинаковый
> Release — машинный отрезок детерминирован.

**Готовность этапов:**

| Этап | Статус |
| --- | --- |
| Нормализация, сверка, генерация | в пилоте на АРМ (срез `contact-center`) |
| `G-mach`, сборка и проверка Release | работает, воспроизводимо |
| `G-human` | чек-лист есть, работает в пилоте |
| Проекции V-BIZ, V-APPROVE, V-DEV, V-CONTRACT | словарь и правила раскрытия в пакете; выдача каждой проекции не измерена |

**Промпт для изображения:**

```text
A clean horizontal production line: raw crumpled requests enter on the
left, pass a sorting station, a library shelf where each item is
stamped with a source tag, a golden mould that shapes identical
documents, a machine scanner gate, a human inspector's desk, and exit
on the right as four neatly labelled output trays.
STYLE: clean isometric technical illustration, deep navy background,
off-white linework, single amber accent colour for the key element,
generous negative space, no text, no letters, no logos, 16:9
```

**Источники:**
[вертикальный срез BCREQ](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/40-practice-and-cases.md),
[RFC Working → Release](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-bcreq-working-release-pipeline.md),
[золотые кейсы](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/projects/ba-ai-process/dist/execution-package-gigacode-cli/golden),
[гипотеза Г-16 о детерминизме Release](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-29-cline-package-expectation-gap.md).

---

## Слайд 8. Пилот на АРМ доказал модель; для гарантий переходами должен управлять код, а не модель

**Блок 6. Среда исполнения.**

- **Сейчас:** пакет исполнения на АРМ БА — GigaCode CLI и Cline + Mango AI.
  Один Source, два скомпилированных пакета.
- **Главный пробел:** у роли оркестратора нет исполнителя. В CLI переходы
  набирает БА, в Cline правила читает модель.
- **Проба это подтвердила:** «lorem ipsum» прошёл узлы n1–n3, потому что
  гейт проверял пакет, а не выход шага.
- **Вектор:** runner на АРМ как лидер, затем серверная Среда 4 — то же ядро
  как сервис: свой конечный автомат, журнал с цепочкой хешей, Mango AI по
  OpenAI-совместимому API.

> **Принцип:** агент готовит содержимое узла, контроллер владеет переходом
> («own your control flow»).

**Визуальное доказательство:** две колонки «АРМ сегодня» и «Среда 4»; общий
блок ядра runner по центру.

**Промпт для изображения:**

```text
On the left a single analyst's desk with a laptop and a small engine
block glowing on it; an arrow leads to the right where the very same
engine block is installed at the centre of a compact server room,
now connected by clean cables to several desks and a secure vault.
STYLE: clean isometric technical illustration, deep navy background,
off-white linework, single amber accent colour for the key element,
generous negative space, no text, no letters, no logos, 16:9
```

**Источники:**
[мета-модель → среды → инструменты](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-29-ba-ai-process-runtime-options.md),
[ADR-017: Source → Distribution → Runtime](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/decisions/2026-09-adr-017-ba-ai-process-source-distribution.md),
[ADR-018: граница GigaCode CLI](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/adr/2026-09-adr-018-gigacode-cli-execution-boundary.md),
[ADR-019: пилот Cline + Mango AI](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/adr/2026-09-adr-019-cline-mango-ai-pilot.md).

---

## Слайд 9. Масштабируется не генерация, а стандарт выхода: его соблюдение делает передачу в разработку бесшовной

**Блок 7. Масштабирование.**

- Контракт выхода один для всех продуктов: новая продуктовая линия добавляет
  словарь и золотые кейсы, а не новый промпт. 860 разделов базы знаний пяти
  продуктов легли в 14 слотов без единого нового.
- Системный аналитик получает документ с известной структурой и следом до
  источника, а не пересказ.
- Качество измеряется, а не оценивается на глаз: `M-1` структура, `M-2`
  отказы `G-mach`, `M-3` правки человека, `M-4` полнота следа = 100%.
- Каждое отличие от нормы, найденное в работе, возвращается в Source с
  происхождением и доходит до всех пакетов через перекомпиляцию.

> **Порог решения:** срез успешен, если `M-4` = 100% и `M-1` заметно выше
> базовой линии 0.0 при ненулевом `M-2`. Нулевой `M-2` означает, что гейт
> ничего не проверяет.

**Визуальное доказательство:** воронка «продуктовые линии → один контракт →
СА / разработка / договор» и строка метрик M-1…M-4.

**Промпт для изображения:**

```text
Several different product streams of varied shapes enter a single
precision-machined standard coupling; on the other side they leave as
identical, perfectly fitting connectors that plug directly into three
receiving machines representing analysis, development and a signed
contract.
STYLE: clean isometric technical illustration, deep navy background,
off-white linework, single amber accent colour for the key element,
generous negative space, no text, no letters, no logos, 16:9
```

**Источники:**
[860 разделов в 14 слотах](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-08-kb-slot-fit-facts.md),
[метрики M-1…M-5 и порог решения](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/40-practice-and-cases.md),
[ADR-017: обратная связь в Source](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/decisions/2026-09-adr-017-ba-ai-process-source-distribution.md),
[сходимость архитектуры](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-24-architecture-convergence-and-readiness.md).

---

## Слайд 10. От пилота к Среде 4 — три шага, критерий опровержения задан до старта

**Решения и следующий шаг.**

- **Шаг 1, без новой инфраструктуры:** runner ведёт маршрут на АРМ — считает
  условия переходов из YAML, проверяет выход каждого узла, умеет ждать и
  возобновлять (B-211…B-213).
- **Шаг 2, замер:** 10 задач. Гипотеза опровергнута, если доля шагов с
  проверенным контрактом узла ниже 95% или БА тратит на команды больше
  времени, чем на содержание.
- **Шаг 3, Среда 4:** то же ядро как серверная служба (B-216, B-218).
  Нужны решения руководителя: вызов Mango AI по API из кода и площадка.
- **Чего мы не делаем:** не строим ядро на n8n, Dify или Flowise и не
  отдаём управление переходами агенту.

> **Запрос:** не бюджет на «ИИ-аналитика», а площадка для проверки
> измеримой гипотезы.

**Промпт для изображения:**

```text
Three switches in a row on a clean control panel, each paired with a
small measuring gauge; a hand is turning on the first one, the other
two are still off; behind the panel a calm, dimly lit server room is
waiting to power up.
STYLE: clean isometric technical illustration, deep navy background,
off-white linework, single amber accent colour for the key element,
generous negative space, no text, no letters, no logos, 16:9
```

**Источники:**
[рекомендации по средам и порог опровержения](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-29-ba-ai-process-runtime-options.md),
[RFC проверки Source на пилоте](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/rfc/2026-09-source-pilot-verification.md),
[бэклог B-211…B-218](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ops/backlog.md).

---

## Приложение. Карта доказательств

| Утверждение | Где проверить |
| --- | --- |
| 69 прогонов (апрель — сентябрь 2026), 583 коммита | [`mango_ba_prompts/runs`](https://github.com/G-Ivan-A/mango_ba_prompts/tree/main/runs), [снимок корпуса](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-08-25-mango-runs-empirical-snapshot.md) |
| 67 прогонов разобраны по дефектам, 4 класса отказов | [форензика](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-requirements-run-forensics.md) |
| `M-1 = 0.0`, 17 документов — 17 структур | [замер структуры](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-08-artifact-structure-variance-facts.md) |
| 6% прогонов с вердиктом приняты без правки | [базовая линия](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/methodology-unification/40-practice-and-cases.md) |
| 10 из 12 конструкций отсутствуют в 24 промптах | [влияние наследия](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-09-legacy-normative-influence-facts.md) |
| Инварианты `MM-1`…`MM-4` | [теория мета-модели](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/10-theory.md) |
| 31 операция, 5 когнитивных классов | [теория операций](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/ba-meta-model/operation-taxonomy/10-theory.md) |
| Одна форма BCREQ из 7 разделов для трёх продуктов | [золотые формы](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-23-bcreq-golden-forms-and-feasibility.md) |
| Release побайтно воспроизводим | [Г-16](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-29-cline-package-expectation-gap.md) |
| У оркестратора нет исполнителя; «lorem ipsum» проходит n1–n3 | [мета-модель → среды → инструменты](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-ai-process/docs/analysis/2026-09-29-ba-ai-process-runtime-options.md) |
