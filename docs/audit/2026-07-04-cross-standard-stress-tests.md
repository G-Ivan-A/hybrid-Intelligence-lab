---
status: draft
version: 0.1
updated: 2026-07-04
temperature: 0.1
type: audit
context: [hub, standards, cross-standard, stress-test, raar, consistency, desync, governance]
method: cross-standard-stress-test
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/370"
scope: repo
based_on: "Принцип консистентности (issue #370): стандарт = полный набор разделов; асинхронность/отсутствие раздела = баг"
audit_target: "Принцип консистентности стандартов (issue #370): стандарт = полный набор разделов; асинхронность/отсутствие раздела = баг"
evidence_model: "direct-reading + Deep Think с перспективой 4 экспертов"
verdict: conditional
severity_scale: "P0/P1/P2"
follow_up: "Цепочка исправлений: B-NEW-2 (анализ вариантов) → B-NEW-3 (ADR) → B-NEW-4 (мета-стандарт) → B-NEW-5 (изменения в r/a/a/r)"
related_norm: "standards/research-standard.md, standards/analysis-standard.md, standards/audit-standard.md, standards/report-standard.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/370"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/296"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/288"
related_artifacts:
  - "standards/research-standard.md"
  - "standards/audit-standard.md"
  - "standards/report-standard.md"
  - "docs/rfc/2026-07-02-rfc-analysis-structure.md"
  - "docs/adr/2026-07-adr-006-analysis-structure.md"
  - "docs/adr/2026-07-adr-005-audit-structure.md"
  - "docs/adr/2026-07-adr-004-reports-structure.md"
  - "docs/adr/2026-07-adr-003-research-structure.md"
  - "pr-ops/backlog.md"
---

# Отчёт: кросс-стресс-тесты стандартов R/A/A/Report на рассинхрон, противоречия и неоднозначность

## Summary / BLUF

Проведён `Deep Think` кросс-стресс-тест четырёх стандартов цепочки
Research / Analysis / Audit / Report на структурный рассинхрон, противоречия,
конкуренцию источников, дублирование и неоднозначность интерпретации.

**Главный вывод:** цепочка **не является единой системой с предсказуемой
структурой** — она рассинхронизирована по составу разделов, их порядку, схеме
frontmatter, конвенции именования ключей и месту нормирования границ. Гипотеза
заказчика про `Subtype Profiles` **подтверждена и обобщена**: это лишь один из
классов рассинхрона.

**Критический факт, обнаруженный первым:** из четырёх стандартов **физически
существуют только три**. `standards/analysis-standard.md` (B-027) не создан
(статус `TODO` в [backlog](../../pr-ops/backlog.md#L235)), при этом уже
принятый `report-standard.md` **нормативно ссылается на его секцию** («Analysis
§3») как на источник граничных таблиц. То есть система стандартов неполна, а
существующие стандарты уже содержат «висящие» ссылки на ненаписанный стандарт.

Найдено **22 бага рассинхрона**: 1 × P0, 9 × P1, 12 × P2. Ни один из багов не
требует правки стандартов в рамках этой задачи (ограничение issue #370) —
отчёт фиксирует их для последующих фиксов.

| Критичность | Кол-во | Классы |
| --- | --- | --- |
| **P0** (блокер системности) | 1 | отсутствующий стандарт + висящая ссылка |
| **P1** (структурный рассинхрон / competing sources) | 9 | состав разделов, порядок, границы, frontmatter-ключи, профили, standard↔валидатор |
| **P2** (дублирование / неоднозначность / дрейф) | 12 | температура, supersedes, cross-links, дубли, термины |

> Найдено при валидации самого отчёта: `report-standard.md` §Frontmatter предписывает
> обязательный (для process outputs) ключ `report-subtype`, но `tools/validate-frontmatter.sh`
> отвергает его как «not approved for this document class». Это баг **VAL-02** (см. таблицу):
> нормативное правило стандарта и его enforcement противоречат друг другу.

## Scope / Context

- **Дата:** 2026-07-04. **Автор:** AI-агент (`Hybrid` + `Deep Think`), контроль — человек.
- **Границы охвата (`scope`):** 4 стандарта, объявленные в issue #370 как зависимости:
  - [`standards/research-standard.md`](../../standards/research-standard.md) (B-018, `draft`)
  - `standards/analysis-standard.md` (B-027, **не существует**)
  - [`standards/audit-standard.md`](../../standards/audit-standard.md) (B-032, `draft`)
  - [`standards/report-standard.md`](../../standards/report-standard.md) (B-043, `draft`)
- **Норма проверки (`based_on`):** ключевой принцип консистентности из issue #370 —
  «Стандарт = полный набор разделов; асинхронность разделов/логики в одном типе
  артефакта = баг; отсутствие раздела (даже с `null`-значением) = баг».
- **Метод:** сравнение фактического содержимого стандартов (не пересказ RFC/ADR).
  Для планируемого `analysis-standard.md` использована его нормативная спецификация
  из [RFC B-025](../rfc/2026-07-02-rfc-analysis-structure.md) и
  [ADR-006](../../docs/adr/2026-07-adr-006-analysis-structure.md) — это единственный
  доступный источник его будущей структуры.
- **Ограничения (issue #370):** стандарты НЕ меняются, новые стандарты НЕ создаются,
  аудит состояния артефактов НЕ проводится. Результат — только отчёт о рассинхроне.

### Симуляция команды экспертов

Анализ вёлся с четырёх перспектив, каждая искала свой класс дефектов:

| Эксперт | Фокус поиска | Основные находки |
| --- | --- | --- |
| **Архитектор информации** | состав и порядок разделов, полнота каркаса | STRUCT-01…05, ORDER |
| **Аудитор логики/непротиворечивости** | competing sources, висящие ссылки, противоречия норм | META-01, BND-01…03 |
| **Специалист по AI-контрактам** | машиночитаемость frontmatter, конвенции ключей | FM-01…04, PROF-01 |
| **UX-читатель** | сможет ли человек предсказать структуру, найти правило | STRUCT-03, VAL/COP-дубли, NAM-01 |

## Result / Findings

### Матрица 1. Структурная консистентность (состав и **порядок** разделов)

Порядковый номер `##`-раздела в каждом стандарте. `—` = раздел отсутствует.
`analysis-standard.md` не существует; колонка отражает нормативную структуру,
предписанную RFC B-025 / ADR-006 (профили `inventory/matrix/options/recommendation`,
frontmatter `analysis-subtype`, routing `docs/analysis/`).

| Раздел (нормализованный) | Research | Analysis (план) | Audit | Report |
| --- | :---: | :---: | :---: | :---: |
| Назначение | 1 | + | 1 | 1 |
| Область применения | 2 | + | 2 | 2 |
| Identification and Placement | 3 | + | 3 | 3 |
| **Профильный/модельный блок** | **—** | Subtype Profiles | 4 (4-компонентная модель) | 6 (Subtype Profiles) |
| Frontmatter | 4 | + | 5 | 4 |
| **Minimum Body Sections** | **—** | + | 6 | 5 |
| Evidence Container `exp/` | 5 | — | — | — |
| Граница `exp/` vs `runs/` | 6 | — | — | — |
| Специфический процесс-раздел | — | — | 7 (Audit vs report output) | — |
| **Границы / Маршрутизация** | 7–8 (Маршрутизация + Классификация) | Boundaries | 9 (Boundaries) | 8 (Boundaries) |
| Переходный режим legacy | 9 | — | — | — |
| Lifecycle | 10 | + | 8 | 7 |
| Validation | 11 | + | 10 | 9 |
| Related Artifacts | 12 | + | 11 | 10 |

**Наблюдения:**
- Общего инвариантного «полного набора разделов» между стандартами **нет**.
- Совпадающие разделы стоят в **разном порядке** (см. Тест B).
- Профильный блок и «Minimum Body Sections» присутствуют не везде (Тест A).
- Границы нормируются под **тремя разными именами** и в разных позициях (Тест A/E).

### Матрица 2. `Subtype Profiles` (гипотеза заказчика, обобщённая)

| Стандарт | Раздел `Subtype Profiles`? | Профили | Явно зафиксировано «профилей нет»? |
| --- | :---: | --- | :---: |
| Research | ❌ нет | — | ❌ нет (раздел отсутствует) |
| Analysis (план) | ✅ (по RFC B-025) | `inventory / matrix / options / recommendation` | n/a |
| Audit | ❌ нет (есть «4-компонентная модель») | нет подтипов | ❌ нет (не объявлено, что подтипов нет) |
| Report | ✅ | `audit / report / statistics` | n/a |

Согласно принципу issue #370: **раздел `Subtype Profiles` должен быть в каждом
стандарте**, даже если явно фиксирует отсутствие профилей. Research и Audit
нарушают это (см. STRUCT-01, PROF-01).

### Матрица 3. Пересечение нормативных правил (frontmatter / lifecycle / routing / boundaries)

| Правило | Research | Analysis (план) | Audit | Report |
| --- | --- | --- | --- | --- |
| Frontmatter-ядро | status/version/updated/temperature | то же | то же | то же |
| `temperature` в примере | **0.3** | 0.1 (по RFC) | 0.1 | 0.1 |
| Ключ подтипа | — | `analysis-subtype` (kebab) | — (компонентные ключи) | `report-subtype` (kebab) |
| Спец. обязательные ключи | — | — | `audit_target`, `evidence_model`, `verdict` (snake) | — |
| `supersedes` в примере frontmatter | ❌ | ? | ❌ | ✅ |
| Lifecycle нормируемого артефакта | knowledge (draft→reviewed→canonical→superseded) | knowledge | knowledge | knowledge |
| Lifecycle самого стандарта | governance | governance | governance | governance |
| Где нормируются границы | «Маршрутизация» §7 + «Классификация» §8 | «Boundaries» | «Boundaries» §9 | «Boundaries» §8 |
| Источник граничной таблицы | владелец (сам) | ? | делегирует «Research §10» | делегирует «Analysis §3» + «Research §10» |
| Тай-брейкер «один вопрос» | ✅ (2 вопроса: exp/runs + класс) | ? | ✅ (свой порядок 4 типов) | ✅ (свой порядок 4 типов) |

**Согласовано (не баги):** lifecycle-словари (knowledge для артефактов, governance
для стандартов) и разграничительная врезка «lifecycle vs frontmatter» присутствуют
и идентичны по смыслу во всех трёх существующих стандартах; routing-пути
(`docs/audit/`, `docs/report/`, `research/<domain>/`) не конфликтуют; physical
routing split audit-report в `docs/audit/` согласован между Audit и Report.

### Матрица 4. Профили подтипов (inventory/matrix/options/recommendation/audit/report/statistics)

| Профиль | Владелец-стандарт | Ключ | Индустриальный якорь |
| --- | --- | --- | --- |
| `inventory` | Analysis (план) | `analysis-subtype` | — |
| `matrix` | Analysis (план) | `analysis-subtype` | — |
| `options` | Analysis (план) | `analysis-subtype` | — |
| `recommendation` | Analysis (план) | `analysis-subtype` | — |
| `audit` | **Report** (форма выхода) | `report-subtype` | ISO 19011 / ISA 700 |
| `report` | Report | `report-subtype` | ANSI/NISO Z39.18 |
| `statistics` | Report | `report-subtype` | SDMX (ISO 17369) |
| — (нет подтипов) | Audit → 4-компонентная модель | — | — |
| — (нет подтипов) | Research | — | — |

**Наблюдение:** token `audit` живёт одновременно как значение `report-subtype`, как
самостоятельный тип артефакта (`audit-standard.md`) и как каталог (`docs/audit/`) —
источник неоднозначности (PROF-02).

### Стресс-тесты

**Тест A — структурный рассинхрон (совпадает ли набор разделов).**
❌ Провален. Три существующих стандарта имеют разный набор обязательных разделов:
Research не имеет «Minimum Body Sections» и «Subtype Profiles»; Audit заменяет
профили на «4-компонентную модель»; «Boundaries» у Research названы иначе и
разбиты на два раздела. → STRUCT-01, STRUCT-02, STRUCT-03.

**Тест B — порядок разделов.**
❌ Провален. Профильный/модельный блок стоит **до** Frontmatter в Audit (§4) и
**после** «Minimum Body Sections» в Report (§6). Блок границ стоит в **конце** у
Audit/Report (§8–9) и в **середине** у Research (§7–8). → STRUCT-04.

**Тест C — противоречия (нормируют ли два стандарта одно и то же по-разному).**
⚠️ Частично. Research характеризует доказательную базу Analysis как «inline или
ссылка на `runs/`», тогда как планируемый analysis-standard (RFC B-025) для профиля
`matrix` предписывает `exp/`. → BND-03. Ключ подтипа записан как kebab-case
(`report-subtype`), а соседние обязательные ключи — snake_case (`audit_target`).
→ FM-02.

**Тест D — конкуренция источников (competing sources).**
❌ Провален. Одно и то же routing-правило R/A/A/Report нормируется в трёх местах
(Research «Маршрутизация», Audit «Boundaries», Report «Boundaries») с тремя
**разными** тай-брейкер-вопросами, перечисляющими 4 типа в разном порядке.
Граничные таблицы делегируются на «Research §10» (это Lifecycle, а не
маршрутизация — маршрутизация в §7) и «Analysis §3» (стандарт не существует).
→ BND-01, BND-02, META-01.

**Тест E — дублирование (одни и те же правила в разных местах).**
❌ Провален. Секция «Validation» (3 bash-команды + абзац про делегирование
валидаторам) практически идентична в трёх стандартах. Принцип content-over-path
(issue #288) повторён во всех трёх (и несколько раз внутри Audit). Врезка «lifecycle
vs frontmatter» дублируется дословно. → VAL-01, COP-01.

**Тест F — неоднозначность интерпретации.**
⚠️ Частично. H1-заголовки разнятся («Research **Structure** Standard» vs «Audit
Standard» vs «Report Standard»). Аналогичные body-секции названы по-разному
(«Evidence links» в Report vs «Method / Evidence» в Audit). `related_standards`
между сиблингами асимметричны. → NAM-01, XREF-01, BODY-01.

### Таблица найденных багов

| ID | Тип | Стандарты | Описание | Критичность |
| --- | --- | --- | --- | :---: |
| **META-01** | Отсутствующий стандарт + висящая ссылка | Analysis, Report | `analysis-standard.md` (B-027) не создан, но `report-standard.md` уже нормативно ссылается на «Analysis §3» как на источник граничных таблиц. Система из 4 стандартов неполна; принятый стандарт форвард-референсит ненаписанный. | **P0** |
| **STRUCT-01** | Отсутствие раздела | Research, Audit | Раздел `Subtype Profiles` отсутствует; нет явной фиксации «профилей нет». Прямое нарушение принципа issue #370. | **P1** |
| **STRUCT-02** | Отсутствие раздела | Research | Нет раздела «Minimum Body Sections», который есть у Audit и Report. Body-требования разбросаны по Frontmatter/exp-правилам. | **P1** |
| **STRUCT-03** | Рассинхрон имён раздела | Research vs Audit/Report | Одна и та же нормативная сущность «границы типов» названа «Маршрутизация R/A/A» + «Классификация» (Research) vs «Boundaries» (Audit, Report). Читатель не найдёт «Boundaries» в Research. | **P1** |
| **STRUCT-04** | Рассинхрон порядка | все 3 | Профильный/модельный блок и блок границ стоят в разных позициях (см. Тест B). Прямо назван багом в issue #370. | **P1** |
| **FM-02** | Конвенция ключей frontmatter | Report, Analysis(план) vs Audit | Ключ подтипа kebab-case (`report-subtype`, `analysis-subtype`) при snake_case соседях (`audit_target`, `evidence_model`, `related_norm`, `related_artifacts`). Ломает единообразие парсинга для AI-контракта. | **P1** |
| **BND-01** | Висящая/неверная ссылка | Audit, Report | «Research §10» указывает на Lifecycle (маршрутизация — §7); «Analysis §3» ссылается на несуществующий стандарт. Нормативное делегирование границ разорвано. | **P1** |
| **BND-02** | Competing sources | Research, Audit, Report | Routing R/A/A/Report нормирован трижды, с тремя разными тай-брейкер-вопросами (разный порядок 4 типов). Агент может классифицировать по-разному в зависимости от точки входа. | **P1** |
| **PROF-01** | Рассинхрон оси подтипов | все | 2 стандарта имеют профили с разными ключами/числом (3 vs 4), 1 заменяет концепт компонентной моделью, 1 молчит. Нет единой методологии «профили есть/нет». | **P1** |
| **VAL-02** | Standard ↔ валидатор противоречие | Report, Analysis(план) vs tooling | `report-standard.md` предписывает обязательный `report-subtype` (и RFC B-025 — `analysis-subtype`), но `tools/validate-frontmatter.sh` отвергает эти ключи как «not approved». Нормативное правило неисполнимо валидатором; enforcement и стандарт рассинхронизированы (частично покрыто tech-debt B-044). | **P1** |
| **FM-01** | Неоднозначность значения | Research vs Audit/Report | `temperature: 0.3` в примере Research vs `0.1` в Audit/Report без объяснения — какое значение ожидается для класса. | P2 |
| **FM-03** | Рассинхрон схемы vs lifecycle | Research, Audit | Lifecycle требует backlink при `superseded`, но ключ `supersedes` во frontmatter-примере есть только у Report. | P2 |
| **XREF-01** | Асимметрия cross-links | все | `related_standards`: Audit→{Research,Report}, Report→{Research}, Research→{ни один сиблинг}. Граф соседей зависит от точки входа; никто не ссылается на Analysis. | P2 |
| **LC-01** | Рассинхрон охвата раздела | Research vs Audit/Report | Секция «Lifecycle» у Research документирует только lifecycle самого стандарта; у Audit/Report — сначала lifecycle нормируемого артефакта, затем стандарта. Разный объём одноимённой секции. | P2 |
| **VAL-01** | Дублирование | все 3 | Почти идентичная секция «Validation» триплицирована (различие лишь в ID cleanup-задачи). Будет дрейфовать. | P2 |
| **COP-01** | Дублирование правила | все 3 | Принцип content-over-path (#288) повторён во всех трёх и многократно внутри Audit вместо делегирования одному источнику. | P2 |
| **NAM-01** | Рассинхрон заголовка | Research vs Audit/Report | H1 «Research **Structure** Standard» против «Audit Standard» / «Report Standard». | P2 |
| **PROF-02** | Перегрузка термина | Audit, Report | `audit` = значение `report-subtype` + тип артефакта + каталог `docs/audit/`. Риск смешения `report-subtype: audit` с полноценным Audit. | P2 |
| **BODY-01** | Неоднозначность имён body-секций | Audit, Report | Аналогичные секции названы по-разному («Evidence links» vs «Method / Evidence»); «Related Artifacts» играет двойную роль (секция стандарта и обязательная секция нормируемого артефакта). | P2 |
| **BND-03** | Форвард-противоречие | Research vs Analysis(план) | Research описывает evidence Analysis как `runs/`, но analysis-standard (RFC B-025) для `matrix` предписывает `exp/`. | P2 |
| **FM-04** | Рассинхрон опц. поля | Research vs Audit/Report | `owner` объявлен опциональным полем нормируемого артефакта у Research, но вовсе не упомянут во frontmatter-примерах Audit/Report. | P2 |
| **SCOPE-01** | Дублирование границы | Audit | Разграничение «Audit-процесс vs audit-report output» присутствует и отдельной секцией (§7), и в «Boundaries» (§9), и в «Identification» — тройное изложение одной границы внутри одного стандарта. | P2 |

## Recommendations

### Немедленные фиксы (Tier 1, отдельные задачи — не в рамках issue #370)

1. **META-01 (P0):** приоритизировать B-027 (`analysis-standard.md`) или временно
   заменить висящие ссылки «Analysis §3» в `report-standard.md` на явную пометку
   «(будущий analysis-standard, B-027)», чтобы принятый стандарт не форвард-референсил
   несуществующий нормативный источник.
2. **BND-01 (P1):** заменить неточные ссылки «Research §10» на корректный якорь
   раздела маршрутизации (`#маршрутизация-research--analysis--audit`); ссылки на
   номера секций заменить на именованные якоря, устойчивые к перенумерации.
3. **STRUCT-01/PROF-01 (P1):** ввести обязательный раздел `Subtype Profiles` во все
   стандарты; для Research и Audit — с явной фиксацией «подтипов нет; ось вариативности —
   <exp-контейнер / 4-компонентная модель>».

### Долгосрочные улучшения (Tier 2)

4. **Канонический скелет стандарта артефакт-класса.** Зафиксировать единый
   инвариантный список разделов и их порядок (мета-стандарт «структура стандарта»),
   которому обязаны следовать Research/Analysis/Audit/Report. Это лечит STRUCT-01…04,
   NAM-01, BODY-01 причинно, а не симптоматически.
5. **Единая конвенция ключей frontmatter** (snake_case) — устранить `report-subtype`/
   `analysis-subtype` kebab-аномалию (FM-02); добавить `supersedes` во все схемы (FM-03).
6. **Один владелец границ.** Вынести routing-таблицу R/A/A/Report и единый
   тай-брейкер-вопрос в один канонический источник (Research или `glossary.md`),
   остальные стандарты — делегируют ссылкой (лечит BND-02, COP-01, SCOPE-01).
7. **Общий контракт `Validation`** — вынести идентичный блок в один источник и
   ссылаться (VAL-01).
8. **Симметризовать `related_standards`** и включить `analysis-standard.md` после
   его создания (XREF-01).

## Remediation / Deviation

Раздел фиксирует четвёртый компонент audit-модели (deviation handling) для findings
выше; сами правки стандартов в объём этой проверки не входят (ограничение issue #370 —
стандарты не меняются).

- **Severity-распределение:** 1 × P0, 9 × P1, 12 × P2 (см. таблицу найденных багов).
  `severity_scale` — `P0/P1/P2`; вердикт аудита — `conditional`: система стандартов
  используема, но структурно рассинхронизирована и содержит один блокер системности (META-01).
- **Deviation (осознанное отклонение в рамках задачи):** ни один баг не ремедиируется здесь;
  правки стандартов и валидатора вынесены в отдельные задачи. Это явный no-op-ремонт в границах
  проверки, а не пропуск — findings зафиксированы для последующих фиксов.
- **Follow-up (цепочка исправлений):** B-NEW-2 (анализ вариантов структурного рассинхрона) →
  B-NEW-3 (ADR / мета-решение) → B-NEW-4 (мета-стандарт структуры стандартов) →
  B-NEW-5 (приведение R/A/A/Report к мета-стандарту). Немедленные Tier 1-фиксы (META-01,
  BND-01, STRUCT-01/PROF-01) и долгосрочные Tier 2-улучшения перечислены в разделе
  «Recommendations» выше и являются нормативным входом для этой цепочки.
- **Acceptance:** до выполнения цепочки стандарты остаются в статусе `draft`; отчёт
  принимается как evidence-база рассинхрона, а не как решение о его устранении.

## Входные данные для будущего стандарта процесса стресс-тестирования

Артефакты для бэклога (после миграции), обобщённые из этого прогона:

- **Классы рассинхрона как чек-лист:** (1) состав разделов, (2) порядок разделов,
  (3) имена разделов для одного концепта, (4) competing sources одного правила,
  (5) дублирование правила, (6) висящие/номерные cross-references, (7) конвенция
  ключей frontmatter, (8) схема vs lifecycle рассинхрон, (9) перегрузка терминов,
  (10) асимметрия cross-links, (11) форвард-ссылки на несуществующие артефакты.
- **Матрицы как инструмент:** структурная (состав+порядок), профильная, нормативных
  правил, профилей подтипов — переиспользуемый каркас теста.
- **Перспективы экспертов** (архитектор информации / аудитор логики / AI-контракты /
  UX-читатель) как обязательные линзы прогона.
- **Правило именованных якорей вместо номеров секций** — обязательное, чтобы
  cross-references не ломались при перенумерации (корень BND-01).
- **Правило «полного набора разделов»**: отсутствие раздела (даже `null`) — баг;
  каждый стандарт обязан явно объявлять пустые секции.

## Evidence links

Отчёт основан на прямом чтении содержимого стандартов (а не пересказе RFC/ADR):

- [`standards/research-standard.md`](../../standards/research-standard.md) — секции
  и правила Research (Frontmatter `temperature: 0.3`, «Маршрутизация» §7, отсутствие
  «Minimum Body Sections» и «Subtype Profiles»).
- [`standards/audit-standard.md`](../../standards/audit-standard.md) — «4-компонентная
  модель» §4 до Frontmatter, «Boundaries» §9, ссылка «Research §10».
- [`standards/report-standard.md`](../../standards/report-standard.md) — «Subtype
  Profiles» §6, ключ `report-subtype`, ссылки «Analysis §3» / «Research §10».
- [RFC B-025 (analysis-structure)](../rfc/2026-07-02-rfc-analysis-structure.md)
  и [ADR-006](../../docs/adr/2026-07-adr-006-analysis-structure.md) — нормативная
  спецификация ненаписанного `analysis-standard.md` (профили, `analysis-subtype`).
- [`pr-ops/backlog.md`](../../pr-ops/backlog.md) — статус B-027 = `TODO`
  (analysis-standard не создан), B-018/B-032/B-043 = `DONE (draft)`.

## Related Artifacts

- [issue #370](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/370) —
  источник задачи (кросс-стресс-тесты стандартов).
- [issue #296](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/296) —
  зонтичная задача стандартизации Research / Analysis / Audit.
- [issue #288](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/288) —
  размытие типов R/A/A (первопричина content-over-path).
- [ADR-003](../adr/2026-07-adr-003-research-structure.md),
  [ADR-004](../adr/2026-07-adr-004-reports-structure.md),
  [ADR-005](../adr/2026-07-adr-005-audit-structure.md),
  [ADR-006](../adr/2026-07-adr-006-analysis-structure.md) — доказательная база
  принятых решений по каждой цепочке.
- [`standards/glossary.md`](../../standards/glossary.md) — каноническое определение
  типов артефактов (кандидат на роль единого владельца routing-словаря).

> **Примечание о маршрутизации самого отчёта.** По собственному routing-правилу
> стандартов этот документ имеет audit-природу (проверка против нормы консистентности
> + findings + критичность). Изначально он был размещён в `docs/report/` согласно DoD
> issue #370; в рамках issue #396 (B-049) документ перемещён в `docs/audit/` и снабжён
> audit-specific frontmatter (`audit_target`/`evidence_model`/`verdict`/`severity_scale`/
> `follow_up`/`related_norm`) без изменения содержательных findings. Нормативный аудит
> состояния артефактов в задачу по-прежнему не входит (ограничение issue #370) — отчёт
> фиксирует структурный рассинхрон, а не устраняет его.
</content>
</invoke>
