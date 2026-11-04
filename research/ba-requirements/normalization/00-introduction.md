---
status: draft
version: 0.1
updated: 2026-08-25
temperature: 0.7
type: research
context: [ba, requirements, normalization, taxonomy, introduction, reading-map, mango]
method: literature-survey + corpus-measurement + taxonomy-building + adversarial-hypotheses
scope: repo-wide
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/539"
based_on:
  - research/ba-requirements/2026-08-25-mango-runs-empirical-snapshot.md
  - research/mango/2026-08-17-mango-ba-processes-and-dod-ontology.md
  - research/reputation-technologies/2026-06-20-founders-vision-and-framework.ru.md
related_artifacts:
  - "research/ba-requirements/normalization/10-theory.md"
  - "research/ba-requirements/normalization/20-taxonomy.md"
  - "research/ba-requirements/normalization/30-decision-framework.md"
  - "research/ba-requirements/normalization/40-practice-and-cases.md"
  - "research/ba-requirements/normalization/50-open-research.md"
  - "docs/rfc/2026-07-17-rfc-reference-research-pattern.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/539"
---

# Нормализация входящих обращений в требования: введение и карта чтения

> **Модуль.** Это файл `00-introduction.md` модуля
> [`research/ba-requirements/normalization/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/research/ba-requirements/normalization),
> оформленного по **Reference Research Pattern** (статус паттерна: Experimental,
> см. [RFC: Reference Research Pattern](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/rfc/2026-07-17-rfc-reference-research-pattern.md)
> и [`standards/research-standard.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/research-standard.md)).
>
> **Политика ссылок.** Все ссылки модуля — абсолютные (требование issue
> [#539](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/539)).
> Единственное исключение объявлено в
> [`40-practice-and-cases.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/40-practice-and-cases.md):
> там относительные внутримодульные ссылки обязательны по машинной проверке
> правила P2.
>
> **Статус.** `draft`. Модуль является исследовательским входом для переписывания
> BA-процессов; сам он ничего не переписывает и не отменяет ни одного
> действующего стандарта.

## BLUF

1. **Термин.** Родовым термином для входа BA-процессов принимается
   **«инициирующий артефакт» (Initiating Artifact)** с обязательной
   типизацией на семь классов IA-1…IA-7. «Запрос» отвергается как омоним,
   `Change Request` — как термин, предполагающий уже существующий baseline,
   `Demand` — как портфельная, а не единичная сущность. Разбор —
   [§4 файла 10-theory.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/10-theory.md#4-решение-t1--термин-для-входа-ba-процессов).
2. **Главная потеря — не в генерации текста требований, а в оценке покрытия.**
   Слова «покрыт*» встречаются в 41 из 56 прогонов Mango, а `discoverab*` — в
   нуле: команда постоянно решает задачу «есть ли это уже в продукте» и ни разу
   не назвала её. Это делает **оценку покрытия отдельной операцией с гейтом**, а
   не подшагом анализа.
3. **Человеческий гейт не является надёжным по умолчанию.** В 9 прогонах из 56
   зафиксировано `hallucinations_shipped > 0` — вымысел модели дошёл до
   артефакта, пройдя ревью. Любая гипотеза реализации (ручная, автоматическая,
   гибридная) обязана иметь **машинно-проверяемый** критерий заземления, а не
   только человеческую подпись.
4. **Две таксономии, а не одна.** Универсальная (переносимая на IT/B2B SaaS) и
   Mango-специализированная разделены жёстко и связаны **матрицей корреляции**
   ([§1 файла 30-decision-framework.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/30-decision-framework.md#1-матрица-корреляции-универсальная--mango-таксономия)).
   Сцепка идёт через цепочку `domain → capability → feature → function`.
5. **Рекомендация по реализации — гибрид (H-H)**, но не как компромисс: ручной
   режим не масштабируется на 56+ прогонов, автоматический не имеет заземления,
   которое требуется по п. 3. Разбор последствий каждой гипотезы для таксономии,
   артефактов и библиотеки промптов —
   [§4 файла 30-decision-framework.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/30-decision-framework.md#4-три-гипотезы-реализации).
6. **Статистика требований — отдельный процесс, а не побочный эффект решения о
   включении в продукт.** Реестр фиксирует **все** инициирующие артефакты,
   включая отклонённые; решение о включении — самостоятельный гейт с другим
   владельцем и другим ритмом
   ([§5 файла 30-decision-framework.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/30-decision-framework.md#5-процесс-статистики-и-реестр-требований)).
7. **Репутационная методология GRA поверх таксономии стейкхолдеров — гипотеза
   (H6), а не индустриальная практика.** Она явно помечена как нестандартная и
   вынесена в
   [§4 файла 20-taxonomy.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/20-taxonomy.md#4-гипотеза-h6--репутационный-слой-поверх-таксономии-стейкхолдеров)
   с абсолютной ссылкой на
   [`research/reputation-technologies`](https://github.com/G-Ivan-A/aether-orbis-gra).
8. **Атомарные операции на этой итерации не меняются.** Переписыванию подлежат
   процессы, которые эти операции компонуют: маршрут входа, гейты, критерии
   перехода состояний, реестр. Обоснование —
   [§6 файла 30-decision-framework.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/30-decision-framework.md#6-основание-для-переписывания-ba-процессов).

## Карта чтения

| Файл | Что внутри | Кому обязателен |
| --- | --- | --- |
| [`00-introduction.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/00-introduction.md) | BLUF, границы, вопросы исследования, метод, ограничения | всем |
| [`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/10-theory.md) | рамка нормализации, объектная модель, индустриальные основания, решение по термину, гипотезы H1–H10 | тем, кто принимает решения или спорит с ними |
| [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/20-taxonomy.md) | таксономии IA-1…IA-7, оси O1–O6, стейкхолдеры (контуры), гипотеза GRA, универсальные процессы U1–U9, срез Mango | всем, кто пользуется рамкой решений |
| [`30-decision-framework.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/30-decision-framework.md) | матрица корреляции, цикл нормализации и гейты, выбор модели решения, три гипотезы реализации, реестр и статистика, основание для переписывания процессов | архитекторам процессов и авторам промптов |
| [`40-practice-and-cases.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/40-practice-and-cases.md) | корпус 56 прогонов, четыре граничных кейса на реальных данных, разбор «что сработало / что нет» | тем, кому нужны прецеденты |
| [`50-open-research.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/50-open-research.md) | открытые вопросы, ранжирование гипотез, вход для RFC, глоссарий, источники, самоаудит | ревьюеру и автору RFC |

Короткие маршруты:

- **«мне нужен только термин»** — `10-theory.md` §4;
- **«мне нужно классифицировать входящее»** — `20-taxonomy.md` §1–§2;
- **«мне нужно решить, продукт это или кастом»** — `30-decision-framework.md` §3;
- **«я переписываю BA-процессы»** — `30-decision-framework.md` целиком + §6.

## 1. Проблема

Вход процессов бизнес-анализа не имеет ни имени, ни типа, ни измеряемого
качества. На вход приходят: реплика в чате, письмо клиента, тикет, выгрузка
диалога, готовое ТЗ, «сделайте как у конкурента», требование регулятора.
Все они называются «запросом», обрабатываются одним маршрутом и на выходе дают
артефакты несопоставимого качества.

Из этого следуют четыре наблюдаемые проблемы:

| # | Проблема | Наблюдение в корпусе |
| --- | --- | --- |
| P1 | Невозможно оценить качество входа, значит нельзя выбрать маршрут | 32 из 56 прогонов начинаются с уже упакованного `task-`; исходное обращение почти не наблюдаемо |
| P2 | Оценка «есть ли это уже в продукте» делается неявно | «покрыт*» — 41 прогон, `discoverab*` — 0 прогонов |
| P3 | Ревью человеком пропускает вымысел | `hallucinations_shipped > 0` в 9 прогонах |
| P4 | Решение «продукт или кастом» принимается без фиксированных критериев | «кастом» — 10 прогонов, критерии в них не формализованы |

Числа и ограничения замера —
[`2026-08-25-mango-runs-empirical-snapshot.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-08-25-mango-runs-empirical-snapshot.md).

## 2. Границы исследования

**Входит в границы:**

- терминология входного артефакта и её обоснование;
- универсальная таксономия (широкий IT / B2B SaaS), не ограниченная телекомом;
- Mango-специализированная таксономия (телеком + корпоративный сегмент +
  эмпирика `runs/`);
- матрица корреляции между ними;
- таксономия стейкхолдеров по контурам и гипотеза репутационного слоя;
- процесс сбора статистики требований и реестр;
- три гипотезы реализации и их последствия;
- четыре граничных кейса.

**Не входит в границы:**

- изменение 13 атомарных когнитивных операций Mango — на этой итерации они
  зафиксированы (см.
  [`docs/taxonomy.md`](https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/docs/taxonomy.md));
- выбор инструментов, трекеров и хранилищ;
- нормативные acceptance-пороги для метрик — их назначение требует отдельного
  решения владельца процесса;
- переписывание самих промптов: модуль даёт основание и требования к ним, но не
  их текст.

**Строгое разделение областей.** Универсальная и Mango-часть не смешиваются
внутри одного раздела. Каждое утверждение помечено областью: `[U]` —
универсальное, `[M]` — Mango-специализированное, `[H]` — гипотеза.

## 3. Вопросы исследования

| # | Вопрос | Где ответ |
| --- | --- | --- |
| RQ-1 | Как индустриально корректно назвать вход BA-процессов? | `10-theory.md` §4 |
| RQ-2 | Что такое нормализация как функция и где её границы? | `10-theory.md` §1–§2 |
| RQ-3 | Какие классы инициирующих артефактов существуют и по каким осям они различаются? | `20-taxonomy.md` §1–§2 |
| RQ-4 | Как устроена таксономия стейкхолдеров по контурам? | `20-taxonomy.md` §3 |
| RQ-5 | Применима ли методология репутационных технологий к стейкхолдерам BA? | `20-taxonomy.md` §4, гипотеза H6 |
| RQ-6 | Какие универсальные BA-процессы работают со входом? | `20-taxonomy.md` §5 |
| RQ-7 | Как универсальная таксономия соотносится с Mango? | `30-decision-framework.md` §1 |
| RQ-8 | Как выглядит цикл нормализации и какие в нём гейты? | `30-decision-framework.md` §2 |
| RQ-9 | Как принимается решение «продукт / доработка / кастом»? | `30-decision-framework.md` §3 |
| RQ-10 | Каковы последствия трёх гипотез реализации? | `30-decision-framework.md` §4 |
| RQ-11 | Как устроен процесс статистики требований и чем он отличается от решения о включении в продукт? | `30-decision-framework.md` §5 |
| RQ-12 | Что именно даёт основание переписать BA-процессы? | `30-decision-framework.md` §6 |
| RQ-13 | Как система реагирует на четыре граничных кейса? | `40-practice-and-cases.md` §3 |
| RQ-14 | Как таксономия эволюционирует и кто это подтверждает? | `30-decision-framework.md` §7 |

## 4. Метод

Четыре независимых источника доказательств, чтобы ни один вывод не опирался
только на один из них:

1. **Индустриальные стандарты** — BABOK Guide v3, IREB CPRE, ISO/IEC/IEEE
   29148:2018, ISO/IEC 25010, ITIL 4, PMBOK, SAFe, ГОСТ 34.602-2020, TM Forum
   SID/eTOM. Полный список с URL —
   [§1 файла 50-open-research.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/50-open-research.md#1-источники).
2. **Действующая онтология Mango** — 13 операций, 9 процессов, 30 типов
   артефактов, 8 состояний, правила С1–С8.
3. **Эмпирика корпуса `runs/`** — 56 прогонов, измерены воспроизводимо
   ([evidence container](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/research/ba-requirements/exp/ba-requirements-normalization-539)).
4. **SSOT-диалог задачи** — приложение к issue
   [#539](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/539),
   из которого взяты спектр качества входа, контуры, коммерческая рамка и
   требование обратной связи для эволюции таксономии.

Каждая гипотеза сформулирована **фальсифицируемо**: в
[§5 файла 10-theory.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/10-theory.md#5-гипотезы-h1h10)
для каждой указано наблюдение, которое её опровергает.

## 5. Ограничения и честные пробелы

1. **`runs/` смещён к поздним стадиям.** 32 из 56 прогонов начинаются с
   `task-`, то есть с уже нормализованного артефакта. Утверждения о самом раннем
   участке входа опираются на диалог задачи и на 4 прогона `bcreq-`, а не на
   массовую статистику.
2. **Граничный кейс «устаревший контекст» эмпирически не подтверждён.** Ноль
   упоминаний `deprecat`/«вывод из эксплуатации» в корпусе. Он оставлен в
   рамке как **гипотеза H9** и явно помечен как непроверенный.
3. **Метрики корпуса разнородны** (три разных ключа для галлюцинаций, две схемы
   размещения), заполнены от 10 до 41 прогона из 56; `success_rate` несопоставим
   между прогонами по признанию самих метаданных.
4. **Часть индустриальных источников недоступна анонимно** (iso.org,
   tmforum.org, pmi.org отвечают HTTP 403 на автоматический запрос). Ссылки
   даны на официальные страницы стандартов; статус проверки указан в
   [§1 файла 50-open-research.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/50-open-research.md#1-источники).
5. **Репутационный слой (H6) не имеет прецедентов в BA-практике.** Это
   заявленная новизна, а не заимствование; риск переусложнения зафиксирован.
6. **Модуль не заменяет решения.** Ни одна таблица здесь не является
   утверждённым стандартом: канонизация проходит через RFC/ADR Хаба.
