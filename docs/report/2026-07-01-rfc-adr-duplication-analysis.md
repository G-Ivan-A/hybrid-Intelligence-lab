---
status: draft
version: 0.1
updated: 2026-07-01
temperature: 0.1
report-subtype: report
scope: repo
based_on: "docs/adr/2026-07-adr-003-research-structure.md + docs/rfc/2026-06-30-rfc-research-structure.md"
owner: G-Ivan-A
type: report
context: [hub, adr, rfc, governance, ssot, root-cause-analysis]
method: root-cause-analysis
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/316"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/316"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/314"
related_artifacts:
  - "docs/adr/2026-07-adr-003-research-structure.md"
  - "docs/rfc/2026-06-30-rfc-research-structure.md"
  - "standards/adr-structure-standard.md"
  - "standards/rfc-structure-standard.md"
  - "standards/report-standard.md"
---

# Отчёт: анализ причины дублирования RFC B-016 ↔ ADR-003

## Контекст

Источник задачи: [issue #316](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/316).
Проверяемый артефакт:
[`docs/adr/2026-07-adr-003-research-structure.md`](../adr/2026-07-adr-003-research-structure.md)
(ADR-003, v0.1, создан в рамках B-017 —
[issue #314](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/314)).
Источник решения:
[`docs/rfc/2026-06-30-rfc-research-structure.md`](../rfc/2026-06-30-rfc-research-structure.md)
(RFC B-016, v0.2).
Применённые контракты:
[`standards/adr-structure-standard.md`](../../standards/adr-structure-standard.md)
(v1.0) и
[`standards/rfc-structure-standard.md`](../../standards/rfc-structure-standard.md)
(v1.0).

Задача — не просто зафиксировать факт дублирования, а установить **причину**:
почему decision record (ADR) воспроизвёл содержание proposal (RFC), нарушив
SSOT и границу «предложение vs принятое решение».

Метод — симуляция команды экспертов (архитектор документации, governance-эксперт,
validator-инженер) поверх пословного сравнения секций ADR-003 и RFC B-016.

## Вердикт

Дублирование **подтверждено**. Первопричина — **ошибка интерпретации границы
RFC/ADR на уровне секций, а не на уровне документа**. Исполнитель верно выбрал
маршрут RFC → ADR → standard (document-level boundary применён корректно), но при
заполнении обязательных body-секций ADR (`Decision`, `Alternatives Considered`,
`Consequences`) истолковал требование «секция ОБЯЗАНА присутствовать» как «секция
обязана быть самодостаточной и повторить суть», а не «секция фиксирует решение и
делегирует детали в исходный RFC».

Это не сознательное задокументированное решение и не дефект самой границы в
стандарте. Ключевое доказательство интерпретационной природы ошибки: ADR-003
**одновременно** содержит корректные disclaimer'ы о границе и **всё же** дублирует
RFC. Например, в `Decision` сказано «Детальная модель … остаются в RFC B-016 и не
дублируются здесь. Этот ADR — decision record, а не proposal», но выше в той же
секции полностью пересказаны четыре решения P1–P4. Исполнитель знал правило
абстрактно и применил его непоследовательно — это интерпретация, а не незнание.

Усиливающие факторы: (1) стандарт фиксирует границу RFC/ADR только на уровне
документа, а его минимальный шаблон приглашает заполнять секции содержанием;
(2) отсутствует автоматический guard против RFC↔ADR overlap; (3) инстинкт
«перестраховаться» ради самодостаточного, читаемого без RFC ADR.

## Где возникло дублирование

Пословное сопоставление секций ADR-003 (до правки) и RFC B-016:

| Секция ADR-003 | Что содержит | Дублирует в RFC B-016 | Характер |
| --- | --- | --- | --- |
| `Decision`, п.1 «Целевая структура `research/<domain>/`» | Дата-первый отчёт + единый контейнер `exp/<issue-slug>/`, обязательный номер issue в slug. | Proposal **P1** (та же модель, почти дословно). | Пересказ proposal. |
| `Decision`, п.2 «Запрет `outputs/`» | Плоская структура, опциональный `data/`, запрет обязательной `outputs/`. | Proposal **P2**. | Пересказ proposal. |
| `Decision`, п.3 «Граница `exp/` vs `runs/`» | Evidence corpus vs operational run + «один вопрос исполнителю». | Proposal **P3** (включая тот же критерий-вопрос). | Пересказ proposal. |
| `Decision`, п.4 «Маршрутизация R/A/A» | Research → `research/`, Analysis → `docs/analysis/`, Audit → `docs/audit/`, run → `runs/`. | Proposal **P4**. | Пересказ proposal. |
| `Alternatives Considered` | Таблица из 5 отклонённых вариантов с причинами. | Раздел **Alternatives** (A1–A6) и **Critical Analysis**. | Дублирование таблицы. |
| `Consequences`, блок «Архитектурные следствия для downstream» | Список B-018..B-023 (стандарт, addendum, glossary, удаление профиля, миграция, валидаторы). | Раздел **Impacted Artifacts** и таблица downstream chain B-017..B-023. | Пересказ плана задач. |

Секции `Context`, `Decision Drivers`, `Compliance and Validation`, `Lifecycle`,
`Related Artifacts` дублирования не создавали: они держат ADR-уровень (проблема,
почему решение нужно сейчас, как проверяется, lifecycle, ссылки).

## Почему возникло: анализ команды экспертов

**Архитектор документации.** Минимальный шаблон ADR в стандарте показывает
`Alternatives Considered` как **заполненную таблицу** `| Alternative | Why
rejected |`, а `Consequences` — как «Positive effects, trade-offs, and follow-up
work». Форма шаблона напрямую приглашает вписать содержание, а ближайший источник
готового содержания — исходный RFC. Между абстрактным принципом границы и
конкретным шаблоном образуется зазор: принцип говорит «делегируй в RFC», а шаблон
показывает «заполни таблицу». Исполнитель заполнил.

**Governance-эксперт.** Раздел `Boundary RFC/ADR` в обоих стандартах
сформулирован на **уровне документа**: он отвечает на вопрос «это должно быть RFC
или ADR?» (инвариант «RFC answers should we accept; ADR answers what was
accepted»). Нет **посекционного** правила «когда исходный RFC существует,
`Decision` фиксирует только что принято и ссылается на RFC; `Alternatives
Considered` делегирует в RFC; `Consequences` — только архитектурные последствия,
не список задач». Document-level граница применена верно (ADR создан правомерно
как human decision gate B-017), но section-level поведение оказалось
неопределённым — и заполнилось содержимым RFC.

**Validator-инженер.** Валидаторы по стандарту проверяют только frontmatter,
именование и реестры; расширение зафиксировано как tech debt в
`pr-ops/backlog.md`. Проверки RFC↔ADR overlap нет. Поэтому дублирование
прошло локальную валидацию и CI молча, а человеческое review на B-017 его не
поймало. Граница enforced только людьми — и здесь человек её не проверил
посекционно.

Сводно: **первопричина — интерпретационная (генерация)**: правило границы
понято на уровне документа, но не применено на уровне секций. Усилено формой
стандарта (граница только document-level + шаблон, приглашающий заполнение) и
отсутствием автоматического backstop'а. Инстинкт «сделать ADR самодостаточным»
довершил дублирование.

## Какие контракты применял исполнитель и как интерпретировал

- **`standards/adr-structure-standard.md`** → раздел `Required Body Sections`
  (9 обязательных секций в фиксированном порядке) и минимальный шаблон.
  *Интерпретация исполнителя:* «каждая секция должна быть заполнена по существу и
  быть понятной без открытия RFC». *Корректная интерпретация:* «секции фиксируют
  решение; детали, альтернативы и trade-offs делегируются в RFC (см. `Boundary
  RFC/ADR`, инвариант ADR = что принято и почему)».
- **`standards/adr-structure-standard.md`** → раздел `Boundary RFC/ADR`:
  «Accepted RFC already contains … alternatives, consequences … do not duplicate
  it as ADR». *Интерпретация исполнителя:* применил на уровне «создавать ли ADR
  вообще» (создал — верно), но не перенёс запрет дублирования внутрь секций.
- **`standards/rfc-structure-standard.md`** → RFC остаётся носителем `Proposal`,
  `Alternatives`, `Trade-offs`. Исполнитель это понимал (в ADR есть ссылки «см.
  RFC»), но параллельно скопировал суть — противоречие между заявленным
  намерением и фактическим текстом.

## Рекомендации по предотвращению повторения

Рекомендации; изменение стандартов/RFC вне scope этой задачи (запрещено issue
#316) и выносится в backlog как отдельные пункты.

1. **Посекционное правило делегирования в стандарт ADR (future backlog).** Явно
   зафиксировать: при наличии source RFC `Decision` = короткое «что принято» +
   ссылка на RFC за моделью; `Alternatives Considered` = «см. RFC, раздел
   Alternatives»; `Consequences` = только архитектурные последствия, без списка
   задач (он живёт в RFC Impacted Artifacts и `pr-ops/backlog.md`).
2. **Шаблон «ADR с source RFC».** Дать вариант шаблона, где секции предзаполнены
   delegation-указателями, а не пустыми таблицами, чтобы форма не приглашала
   пересказ.
3. **Лёгкий guard на overlap (validator tech debt).** Эвристика для
   reviewer/валидатора: флаг, когда ADR воспроизводит крупный непрерывный
   фрагмент своего source RFC; трекать в существующем tech-debt на расширение
   валидаторов.
4. **Пункт review-чеклиста на acceptance ADR.** «Пересказывает ли ADR proposal
   из RFC? Если да — делегировать, а не дублировать».

## Внесённая правка ADR-003

В рамках issue #316 ADR-003 приведён к decision-record без дублирования RFC
(версия поднята `0.1` → `0.2`, решение и статус `proposed` не изменены):

- `Decision` — вместо пересказа P1–P4 краткая фиксация «принять модель RFC B-016
  без корректировок» + перечень принятого одной строкой на пункт со ссылкой на
  разделы RFC за деталями.
- `Alternatives Considered` — таблица заменена делегированием в RFC B-016
  (Alternatives A1–A6, Critical Analysis) с указанием ключевой закрытой развилки.
- `Consequences` — убран список задач B-018..B-023 (он в RFC Impacted Artifacts и
  backlog); оставлены только архитектурные последствия с делегирующей ссылкой.

RFC B-016 и стандарты ADR/RFC не изменялись (они корректны, ограничение issue
#316).

## Проверка

Локальная проверка:

```bash
./tools/validate-frontmatter.sh .                   # pass
./tools/validate-file-naming.sh                     # pass
./tools/validate-repository-structure.sh            # pass
python3 tools/generate-manifest.py --check          # pass
```
