---
status: draft
version: 0.1
updated: 2026-09-10
temperature: 0.3
type: research
context: [ba, taxonomy, process, subprocess, babok, cbap, mango, delta, agent-executability, issue-571]
method: standard-decomposition + delta-design + defect-audit
scope: mango-only
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571"
based_on:
  - research/ba-requirements/2026-09-10-process-taxonomy-defects-facts.md
  - projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md
  - research/ai-education/task-processing/20-taxonomy.md
related_artifacts:
  - "projects/ba-gigacode-implementation/ba-operation-taxonomy/00-introduction.md"
  - "projects/ba-gigacode-implementation/ba-meta-model/00-introduction.md"
  - "docs/adr/2026-09-adr-015-process-operation-taxonomy-rebuild.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/563"
---

# Таксономия процессов БА: индустриальный базис и дельта Манго КК

> **Модуль** оформлен по
> [Reference Research Pattern](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/rfc/2026-07-17-rfc-reference-research-pattern.md):
> `00` — рамка и навигация, `10` — почему таксономия процессов обязана стоять на
> индустриальном базисе и что такое дельта, `20` — четыре уровня `L0`–`L3` и
> реестр депрекации прежних девяти процессов, `30` — правила выбора процесса,
> контракт объявления нового и привязка гейтов, `40` — сквозные кейсы и метрики,
> `50` — незакрытое.
> **Ссылки абсолютные** (требование issue #571). Единственное исключение —
> внутримодульные ссылки в
> [`40-practice-and-cases.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/40-practice-and-cases.md):
> правило `P2` требует относительной ссылки и проверяется машинно
> ([`tools/validate-rrp-links.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/validate-rrp-links.sh)).

## Зачем модуль существует

Действующая таксономия процессов в
[`ba-meta-model/20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md), §4
унаследована из спицы целиком, по правилу `T-4` («значение наследуется, если у
него есть индустриальный источник»). Проверка показала, что условие правила не
выполнялось: у унаследованных девяти процессов индустриального источника нет, а
у первого из них — `fr-generation`, «от сырого запроса до черновика ФТ/ТЗ» —
определение содержит две ошибки сразу.

Замер
[`2026-09-10-process-taxonomy-defects-facts.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-10-process-taxonomy-defects-facts.md)
фиксирует восемь дефектов `D1`–`D8`. Три из них разрушают именно таксономию
процессов: ФТ и ТЗ названы одним выходом (`D1`) при том, что онтология спицы
объявляет их разными типами артефакта; «черновик» назван границей процесса
(`D2`) при том, что `draft` — состояние жизненного цикла; словарь процессов не
использован ни одним прогоном из 67, кроме одного (`D7`).

Модуль не правит формулировки. Он **пересобирает** таксономию: строит уровни
`L0` и `L1` из BABOK Guide v3 и объявляет уровни `L2` и `L3` явной дельтой
предметной области Манго КК, где каждый унаследованный элемент либо подтверждён
поимённо, либо депрекирован с основанием.

## BLUF: девять утверждений

1. **Таксономия процессов четырёхуровневая: `L0 → L1 → L2 → L3`.** `L0` —
   области знаний BABOK Guide v3, `L1` — семейства работ ИТ/телеком, `L2` —
   процессы Манго КК, `L3` — навыки (подпроцессы), которыми процесс исполняется
   ([`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/20-taxonomy.md), §2–§5).
2. **`L0` и `L1` не изобретаются.** Шесть областей знаний BABOK — внешняя
   норма; отклонение от неё требует основания, а не наоборот
   ([`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/10-theory.md), §2).
3. **`L2` — дельта, а не копия.** Десять процессов Манго КК объявлены как
   различие между индустриальным базисом и практикой контакт-центра;
   у каждого указана область знаний-родитель и причина существования отдельно
   от неё.
4. **Процесс имеет один целевой класс выхода.** Строка «выход: `A-FR`, `A-TZ`»
   не является контрактом. ФТ и ТЗ разведены в два процесса: `fr-detailing`
   производит `A-FR`, `tz-composition` производит `A-TZ`.
5. **Границей процесса является состояние артефакта, а не его качество.**
   «Черновик» границей быть не может: процесс завершается переходом артефакта в
   объявленное состояние жизненного цикла, подтверждённым гейтом.
6. **Навык — подпроцесс, а не реализация операции.** `Process → Skill (1:N) →
   Operation (1:N)`: навык оркеструет атомарные операции, имеет собственные
   вход, выход и гейт и является наименьшей единицей, которую можно поручить
   актору целиком
   ([`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/10-theory.md), §4).
7. **Маршрут — ориентированный граф.** Процесс задаёт множество допустимых
   переходов, условия которых вычисляются на гейтах; прогон — одна конкретная
   траектория в этом графе. Обнаружение неоднозначности, переводящее работу в
   `clarification-management`, — исполнение маршрута, а не его изменение
   ([`30-decision-framework.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/30-decision-framework.md), §3).
8. **Исполнимость агентом — критерий, а не пожелание.** Процесс включается в
   `L2`, только если для каждого его навыка объявлены вход, выход, гейт и ярус
   контроля по шкале `G1`–`G7`
   ([`research/ai-education/task-processing/20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ai-education/task-processing/20-taxonomy.md), §3).
   Работа, для которой это не выполняется, остаётся человеческой и помечается
   `Actor=human`, а не исчезает из модели.
9. **Прежние девять процессов не удаляются, а разбираются поимённо.** Реестр
   депрекации указывает для каждого: подтверждён, переименован, разделён,
   поглощён или депрекирован — с основанием
   ([`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/20-taxonomy.md), §6).

## Что закрывают файлы модуля

| Контракт issue #571 | Где закрыт |
| --- | --- |
| 1. Индустриальный базис BABOK/CBAP + дельта Манго | [`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/10-theory.md) §2–§3, [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/20-taxonomy.md) §2–§4 |
| 1. Разделение ФТ / ТЗ / BCREQ | [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/20-taxonomy.md) §4, [`ba-meta-model/20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md) §2 |
| 2. Заземление на реальность AI-агента | [`30-decision-framework.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/30-decision-framework.md) §4 (ярусы `G1`–`G7`), §5 (контракт исполнимости) |
| 3. Гранулярность: навык как подпроцесс | [`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/10-theory.md) §4, [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/20-taxonomy.md) §5 |
| 4. Синтетические кейсы вместо загрязнённой истории | [`40-practice-and-cases.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/40-practice-and-cases.md) §2–§3 |
| Аудит наследия и депрекация ошибочных определений | [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/20-taxonomy.md) §6 |
| Не выполнено и вопросы | [`50-open-research.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/50-open-research.md) |

## Доказательная база

- [`2026-09-10-process-taxonomy-defects-facts.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-10-process-taxonomy-defects-facts.md)
  — датированный замер восьми дефектов `D1`–`D8` на коммитах `8cbf82a` (спица) и
  `15aa76f` (Хаб).
- [`exp/ba-process-taxonomy-571/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/research/ba-requirements/exp/ba-process-taxonomy-571)
  — измеритель дефектов, синтетические кейсы и машинный валидатор новых
  словарей.
- [`2026-09-08-meta-model-inputs-facts.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-08-meta-model-inputs-facts.md)
  — снимок входов мета-модели, из которого взято число прогонов и промптов.

## Чего в модуле нет

- **Нет каталога значений предметной области.** Домены, capability и features
  остаются в споке (`T-5`); модуль владеет формой уровней и именами процессов.
- **Нет словаря операций.** Он вынесен в отдельный модуль
  [`ba-operation-taxonomy/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-operation-taxonomy/00-introduction.md),
  потому что критерий атомарности — самостоятельный предмет.
- **Нет универсальности.** Уровни `L2` и `L3` специализированы под предметную
  область Манго КК и среду GigaCode. Переносимость — гипотеза, а не свойство
  ([`50-open-research.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/50-open-research.md), §1).
