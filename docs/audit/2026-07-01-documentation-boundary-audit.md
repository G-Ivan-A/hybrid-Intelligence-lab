---
status: draft
version: 0.1
updated: 2026-07-01
temperature: 0.1
type: audit
context: [hub, rfc, adr, standard, il-3, ssot, governance, boundary, terminology]
method: manual-review
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/320"
scope: repo
based_on: "issue #320; standards/adr-structure-standard.md; standards/rfc-structure-standard.md; standards/glossary.md"
audit_target: "RFC/ADR/Standard boundary and SSOT conformance for five IL-3 governance artifacts named in issue #320"
evidence_model: "manual-review + deep-think stress-tests + local grep validation"
verdict: conditional
severity_scale: "blocker/cause/consequence/observation"
follow_up: "Tier 2 remediation tracked by issue #322 / PR #323; no blocking residual violations in audited artifacts"
related_norm: "standards/adr-structure-standard.md; standards/rfc-structure-standard.md; standards/glossary.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/320"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/316"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/314"
related_artifacts:
  - "standards/research-standard.md"
  - "governance/rfc/2026-06-30-rfc-research-structure.md"
  - "docs/adr/2026-07-adr-003-research-structure.md"
  - "standards/adr-structure-standard.md"
  - "standards/rfc-structure-standard.md"
  - "docs/report/2026-07-01-rfc-adr-duplication-analysis.md"
  - "standards/glossary.md"
---

# Аудит: коллизии интерпретации стандартов RFC/ADR/Standard (B-039)

## Summary / BLUF

Вердикт: **conditional**. Пять проверенных IL-3 артефактов не содержат
блокирующих остаточных нарушений, а цепочка `research-standard` / RFC B-016 /
ADR-003 проверена чисто на дублирование. Условность verdict связана с
причинными дефектами в шаблонах ADR/RFC и терминологическими рисками, которые
вынесены в follow-up remediation.

## Scope / Target

Audit target: соответствие пяти артефактов issue #320 стандартам структуры,
SSOT-дисциплине и границам RFC/ADR/Standard:
`standards/research-standard.md`,
`governance/rfc/2026-06-30-rfc-research-structure.md`,
`docs/adr/2026-07-adr-003-research-structure.md`,
`standards/adr-structure-standard.md` and
`standards/rfc-structure-standard.md`.

## Method / Evidence

Evidence model: manual section-by-section review, Deep Think stress-tests,
expert-role simulation and local grep checks. Reproducible command snippets are
listed in [7. Проверка (воспроизводимо)](#7-проверка-воспроизводимо).

## Findings / Verdict

Findings:

- No audited artifact has a blocker-level residual violation.
- ADR-003 duplication against RFC B-016 is remediated.
- ADR/RFC structure standards remain valid documents, but carry cause-level
  template risks that can reproduce duplication or stale references.

Final verdict: **conditional**, with no acceptance blockers and explicit
follow-up for cause remediation.

## Remediation / Deviation

Deviation handling: treat F-07/F-07-parallel/F-01 as cause-level remediation,
not as blockers for the audited artifacts. Tier 2 remediation is tracked by
issue #322 / PR #323; no file migration or deletion is performed by this audit.

## Related Artifacts

- Issue [#320](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/320)
  and root-cause report
  [`docs/report/2026-07-01-rfc-adr-duplication-analysis.md`](../report/2026-07-01-rfc-adr-duplication-analysis.md).
- `standards/research-standard.md`,
  `governance/rfc/2026-06-30-rfc-research-structure.md`,
  `docs/adr/2026-07-adr-003-research-structure.md`,
  `standards/adr-structure-standard.md`,
  `standards/rfc-structure-standard.md`.
- `standards/glossary.md`.

## 1. Введение

### 1.1 Причина

В ходе анализа ADR-003 (B-017) выявлена **системная проблема интерпретации
стандартов**: исполнитель верно понял границу RFC/ADR на уровне документа
(создал ADR правомерно как human decision gate), но **не перенёс запрет
дублирования на уровень секций**. Root-cause зафиксирован в отдельном отчёте
[`docs/report/2026-07-01-rfc-adr-duplication-analysis.md`](../report/2026-07-01-rfc-adr-duplication-analysis.md).

Гипотеза постановки задачи ([issue #320](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/320)):
если стандарт задаёт структуру (набор обязательных секций), но не регламентирует
**границы наполнения** при наличии предшествующего артефакта (source RFC для ADR,
source ADR для Standard), исполнители будут читать «секция обязательна» как
«секция должна быть самодостаточной», что порождает дублирование и нарушает SSOT.
Смежная гипотеза: **любая незначительная терминологическая неоднозначность будет
порождать ошибки в управлении проектом экспоненциально — на горизонте 100
итераций**.

### 1.2 Цель (триединая)

1. **Аудит** — проверить 5 артефактов на соответствие стандартам структуры и SSOT
   (внутри артефактов, на переходах, cross-cutting).
2. **Фиксация проблем** — по каждой находке зафиксировать: артефакт-источник,
   артефакт-жертву, тип нарушения, секцию/поле, критичность, root-cause гипотезу;
   классифицировать находки как **причины** (стандарты, шаблоны) vs **последствия**
   (артефакты).
3. **Лечение причин** — рекомендации трёх уровней (стандарты / шаблоны /
   валидация), приоритизированные «что блокирует» vs «что улучшает».

### 1.3 Область аудита

| # | Артефакт | Тип | IL | Source | Что проверялось |
| --- | --- | --- | --- | --- | --- |
| 1 | [`standards/research-standard.md`](../../standards/research-standard.md) (B-018, v1.0) | Standard | IL-3 | ADR-003 + RFC B-016 | proposal-обёртка; дублирование RFC |
| 2 | [`governance/rfc/2026-06-30-rfc-research-structure.md`](../../governance/rfc/2026-06-30-rfc-research-structure.md) (RFC B-016, v0.2) | RFC | IL-3 | inventory #288 + audit #290 | дублирование Research (benchmark/inventory) |
| 3 | [`docs/adr/2026-07-adr-003-research-structure.md`](../adr/2026-07-adr-003-research-structure.md) (ADR-003, v0.2) | ADR | IL-3 | RFC B-016 | посекционное дублирование RFC (Decision, Alternatives, Consequences) |
| 4 | [`standards/adr-structure-standard.md`](../../standards/adr-structure-standard.md) (v1.0) | Standard | IL-3 | — | двусмысленности шаблона |
| 5 | [`standards/rfc-structure-standard.md`](../../standards/rfc-structure-standard.md) (v1.0) | Standard | IL-3 | — | двусмысленности шаблона |

Дополнительные входы: root-cause отчёт
[`docs/report/2026-07-01-rfc-adr-duplication-analysis.md`](../report/2026-07-01-rfc-adr-duplication-analysis.md),
canonical глоссарий [`standards/glossary.md`](../../standards/glossary.md),
концепция структуры репозитория
[`research/hub/2026-06-23-repository-structure-concept.md`](../../research/hub/2026-06-23-repository-structure-concept.md)
(IL-модель).

### 1.4 Метод (Deep Think)

Аудит проведён в режиме `Research` + `Creative` + `Deep Think`: пословное
сопоставление секций на переходах, симуляция команды из четырёх экспертов
(§4.1) и четыре стресс-теста для каждой находки (§4.2). Метод — `manual-review`.
Каждый вердикт снабжён воспроизводимой командой проверки (§7).

### 1.5 Ограничения (scope)

Согласно [issue #320](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/320)
(раздел «ОГРАНИЧЕНИЯ»), эта задача:

- ❌ **НЕ исправляет** выявленные проблемы в артефактах — это отдельные задачи;
- ❌ **НЕ меняет** стандарты структуры — это Tier 2 amendment, отдельные задачи;
- ❌ **НЕ выполняет** миграцию, удаление, перемещение файлов;
- ✅ **только** аудит, фиксация вердиктов и рекомендации по лечению причин.

Поэтому все находки ниже — **вердикты и рекомендации**, а не правки. В частности,
терминологическая находка F-01 (§5) **флагуется как риск**, а не устраняется.

---

## 2. Вердикты по артефактам (Цель 1)

### 2.1 Сводная таблица

| Артефакт | Вердикт | Блокирует acceptance? | Находки |
| --- | --- | --- | --- |
| `standards/research-standard.md` | ✅ **Соответствует** IL-3: proposal-обёртки нет, образцовая дисциплина делегирования | Нет | N-02 (clean); F-01 (term); F-09 |
| `governance/rfc/2026-06-30-rfc-research-structure.md` | ✅ **Соответствует**: Research не дублирован (делегирование, не копия) | Нет | N-03 (clean); F-02 |
| `docs/adr/2026-07-adr-003-research-structure.md` | ✅ **Соответствует**: посекционное дублирование RFC **ремедиировано** (v0.1→v0.2) | Нет | N-01 (remediated); F-03 |
| `standards/adr-structure-standard.md` | ⚠️ **Причинный дефект**: шаблон приглашает наполнение → рецидив дублирования | Нет (сам стандарт валиден); является причиной рецидива | F-07 (cause); F-01 (term) |
| `standards/rfc-structure-standard.md` | ⚠️ **Причинный риск**: шаблон «not yet» приглашает stale-refs; term-конфляция | Нет | F-01 (term); F-07-parallel |

**Итог Цели 1:** ни один из пяти артефактов не содержит **блокирующего**
остаточного нарушения. Три артефакта цепочки (research-standard, RFC B-016,
ADR-003) прошли проверку на дублирование чисто. Два стандарта структуры
(adr/rfc-structure-standard) валидны как документы, но несут **причинные
дефекты** (шаблон + терминология), из-за которых нарушение может воспроизвестись
в будущих артефактах. Это смещает фокус лечения с «жертв» на «причины» (§6).

### 2.2 `standards/research-standard.md` — ✅ соответствует

**Проверка «нет proposal-обёртки» (IL-3-дисциплина):** пройдена. Стандарт
**явно запрещает** дублирование proposal-контекста:
строки 31–34 — «Стандарт является нормативным контрактом (IL-3, документ для
человека)… Proposal-контекст, рассмотренные альтернативы, отклонённые варианты и
trade-offs остаются в RFC B-016 и ЗАПРЕЩЕНО дублировать их здесь». Секций
`Alternatives`/`Trade-offs` в теле нет. Источник решения назван (ADR-003) с
делегированием rationale в RFC (строки 26–29).

**Дуальные словари статусов:** обработаны образцово. Стандарт разводит
**свой** governance-статус (`draft`) и **knowledge-словарь**, который он
предписывает нормируемым research-отчётам. Смешения нет (см. §3.3).

Этот файл — **позитивный эталон** для рекомендации по шаблону «Standard с source
ADR» (§6.2).

Остаточные наблюдения: F-01 (терминологическая формула «нормативный контракт» в
строке 31 — общая для всех трёх стандартов, §5) и F-09 (версия v1.0 при status
`draft` и upstream в статусе `proposed`/`draft`, §5).

### 2.3 `governance/rfc/2026-06-30-rfc-research-structure.md` (RFC B-016) — ✅ соответствует

**Проверка «RFC не дублирует Research (benchmark, inventory)»:** пройдена.
Раздел `Motivation` (строки 40–70) **ссылается** на audit #290 и inventory #288,
но **не воспроизводит** их таблицы benchmark/инвентаризации — это делегирование,
а не копия. Все 12 обязательных секций стандарта RFC присутствуют; три
дополнительные секции («Матрица дельт A/B/C/D», «Critical Analysis», «Boundary
RFC/ADR») — **аддитивны** и не нарушают контракт (стандарт задаёт минимум, а не
максимум).

**Уточнение scope (важно для трактовки issue).** Проверочный пункт #4 issue
называет источник RFC B-016 как «reports-industry-norms». Фактический upstream
RFC B-016 — это **inventory #288 + audit #290**, а не Reports-исследование
([`research/hub/2026-06-30-reports-industry-norms-and-standardization-scope.md`](../../research/hub/2026-06-30-reports-industry-norms-and-standardization-scope.md)),
которое относится к **отдельной** Reports-цепочке (#310 / B-038). Проверка
проведена против фактического upstream; дублирования Research нет по факту, а
несовпадение имён источников зафиксировано как отдельное наблюдение (§5, часть
F-01 как терминологический риск неточной атрибуции).

Остаточное: F-02 (устаревшие forward-refs `not yet — будущий`, §5).

### 2.4 `docs/adr/2026-07-adr-003-research-structure.md` (ADR-003) — ✅ соответствует (ремедиировано)

**Проверка «ADR не дублирует RFC (посекционно)»:** пройдена. Дублирование,
описанное в root-cause отчёте
[`docs/report/2026-07-01-rfc-adr-duplication-analysis.md`](../report/2026-07-01-rfc-adr-duplication-analysis.md),
**устранено** в версии v0.2. Посекционно:

| Секция ADR-003 | Состояние в v0.2 | Вердикт |
| --- | --- | --- |
| `Decision` (строки 57–74) | 4 решения одной строкой + делегирование в RFC P1–P6; явный disclaimer «Этот ADR — decision record, а не proposal: он фиксирует, что модель RFC принята, но не пересказывает её» (строки 72–74). | ✅ не дублирует |
| `Alternatives Considered` (строки 85–95) | Делегирует полный разбор в RFC (Alternatives A1–A6, Critical Analysis); называет только ключевую закрытую развилку. | ✅ не дублирует |
| `Consequences` (строки 97–128) | Только архитектурные последствия; список задач B-018..B-023 делегирован в RFC Impacted Artifacts и `backlog.md` (строки 99–101, 122–128). | ✅ не дублирует |

Секции `Context`, `Decision Drivers`, `Compliance and Validation`, `Lifecycle`,
`Related Artifacts` держат ADR-уровень и не создают коллизий.

Остаточное: F-03 (в `Impacted artifacts`, строка 22, `standards/research-standard.md`
помечен `(B-018, будущий)`, хотя файл уже создан — пограничная stale-ref, §5).

### 2.5 `standards/adr-structure-standard.md` — ⚠️ причинный дефект шаблона

Как **документ** стандарт валиден: 9 обязательных секций (строки 79–87), раздел
`Boundary RFC/ADR` с инвариантом «RFC answers "should we accept this change and
how?", ADR answers "what decision was accepted and why?"» (строки 185–186) и
прямой запрет «do not duplicate it as ADR» (строка 180).

Но **минимальный шаблон** несёт причинный дефект (F-07, §5): граница RFC/ADR
зафиксирована только **на уровне документа**, тогда как форма шаблона на **уровне
секций** приглашает наполнение содержанием:

- `Alternatives Considered` показан как **заполненная таблица**
  `| Alternative | Why rejected |` (строки 121–125) — форма зовёт вписать
  альтернативы, ближайший источник которых — исходный RFC;
- `Consequences` = «Positive effects, trade-offs, and **follow-up work**»
  (строка 129) — «follow-up work» прямо приглашает список задач, который канонично
  живёт в RFC Impacted Artifacts и `backlog.md`.

Это **причина** (cause), а не последствие: зазор между принципом («делегируй в
RFC») и формой («заполни таблицу») и породил дублирование ADR-003. Остаётся
активным для любого будущего ADR с source RFC. Также несёт F-01 (term).

### 2.6 `standards/rfc-structure-standard.md` — ⚠️ причинный риск шаблона

Как документ валиден: 12 обязательных секций (строки 81–94), `Boundary RFC/ADR`
с оговоркой «The boundary is functional, not folder-based» (строки 202–203).

Параллель к F-07: минимальный шаблон содержит поля
`| Decision record | ADR/RFC link or "not yet" |` и
`| Implementation link | PR/tool/standard link or "not yet" |` (строки 109–110).
Значение-заглушка `"not yet"` **не сопровождается правилом обновления** при
появлении референта — форма приглашает оставить stale-значение, что и реализовано
в RFC B-016 (F-02). Кроме того, у стандарта **нет** симметричного правила для
перехода **Research → RFC** (что цитировать, а что не воспроизводить из
benchmark/inventory), — сейчас это соблюдается де-факто (RFC B-016 чист), но не
закреплено нормой. Также несёт F-01 (term).

---

## 3. Проверка по трём измерениям (детализация Цели 1)

### 3.1 Внутри артефактов

| Проверка | Результат | Доказательство |
| --- | --- | --- |
| Стандарты (IL-3) не содержат proposal-обёртку | ✅ Чисто | research-standard строки 31–34 (явный запрет); в adr/rfc-structure-standard proposal-контекст также вынесен «остаётся в RFC» (adr стр. 17–18, rfc стр. 17–19) |
| ADR не дублирует RFC (посекционно) | ✅ Ремедиировано | ADR-003 §Decision/§Alternatives/§Consequences делегируют (см. §2.4) |
| RFC не дублирует Research | ✅ Чисто | RFC B-016 `Motivation` цитирует #288/#290 без таблиц |
| Frontmatter consistency (type, status, related) | ✅ В основном | все IL-3; decision-type/rfc-scope на месте; исключения — stale «будущий»/«not yet» (F-02, F-03) |
| Lifecycle consistency (статусы согласованы) | ⚠️ Наблюдение | RFC `draft` v0.2 → ADR `proposed` v0.2 → standard `draft` **v1.0** — версия downstream обгоняет статус upstream (F-09) |

### 3.2 На переходах между артефактами

| Переход | Проверка | Результат |
| --- | --- | --- |
| **RFC → ADR** | нет ли пересказа proposal в decision record | ✅ Ремедиировано (ADR-003 делегирует, §2.4). **Причина рецидива активна** (F-07: шаблон ADR) |
| **ADR → Standard** | нет ли proposal-обёртки в стандарте | ✅ Чисто (research-standard явно запрещает, §2.2) |
| **Research → RFC** | нет ли дублирования benchmark в proposal | ✅ Чисто де-факто; **норма не закреплена** (F-07-parallel: у RFC-стандарта нет правила Research→RFC, §2.6) |
| **Analysis → RFC** | нет ли смешения инвентаризации и proposal | ✅ Чисто (RFC B-016 отделяет `Motivation`-цитаты от `Proposal`) |

Ключевой вывод по переходам: **фактические** артефакты цепочки чисты (в т.ч.
после ремедиации ADR-003), но **правила**, гарантирующие эту чистоту на уровне
секций, зафиксированы только на уровне документа — поэтому чистота держится на
дисциплине исполнителя, а не на контракте. Это и есть причинный слой (§6).

### 3.3 Cross-cutting concerns

| Проверка | Результат | Доказательство |
| --- | --- | --- |
| Cross-references корректны и симметричны | ✅ В основном | ADR-003 ↔ RFC B-016 ↔ audit #290 ↔ inventory #288 взаимно ссылаются; все внутренние ссылки резолвятся |
| Supersedes / superseded-by согласованы | ⚠️ Minor | ADR-003 `Supersedes research-profile.md (effective после B-021)` (стр. 23) и research-standard как «replacement» профиля — **двойное** объявление supersession одного файла (F-10, §5); не конфликт (оба отложены до B-021), но точка рассинхронизации при масштабировании |
| Словари статусов не смешиваются (knowledge vs governance) | ✅ Чисто | research-standard образцово разводит governance-словарь (свой `draft`) и knowledge-словарь (для нормируемых research-отчётов); ADR/RFC используют governance-словарь корректно |
| **Терминология: Стандарт vs Контракт** | ❌ **Конфляция** | Все три стандарта отождествляют «стандарт» и «контракт» (F-01, §5) — cross-cutting причинный риск |

---

## 4. Deep Think: команда экспертов и стресс-тесты

### 4.1 Четыре эксперта

**1. Архитектор документации** — «Где заканчивается один артефакт и начинается
другой?»
Граница RFC/ADR/Standard на уровне **документа** определена корректно (инвариант
adr-standard стр. 185–186; «boundary is functional» rfc-standard стр. 202–203).
Но на уровне **секций** граница не проведена: `Alternatives Considered` в ADR и
`Alternatives` в RFC — это одна смысловая зона, и стандарт не говорит, кто из них
носитель, а кто указатель. Отсюда вывод: **дефект не в границе, а в её
разрешении (resolution) — она задана «крупным зерном» (документ), а конфликты
возникают «мелким зерном» (секция)**.

**2. Governance-эксперт** — «Если удалить source-артефакт, останется ли смысл в
target?» (см. стресс-тест 1).
После ремедиации ADR-003 удаление RFC B-016 оставляет ADR осмысленным как
запись решения, но лишает деталей — это **корректное делегирование**, SSOT
соблюдён. research-standard при удалении ADR-003/RFC теряет rationale, но
сохраняет норму — тоже корректно. **Вывод: единственность утверждений (SSOT)
сейчас соблюдена; риск — в том, что она не гарантирована правилом.**

**3. Validator-инженер** — «Где нужен guard, а где достаточно чеклиста?»
Точное посекционное дублирование трудно детектировать машиной надёжно (высокий
риск false positives на легитимных коротких цитатах-указателях). Поэтому:
детерминированный **чеклист-пункт** на acceptance — дёшево и немедленно
(«Пересказывает ли ADR proposal из RFC?»); **эвристический guard** (флаг крупного
непрерывного совпадающего фрагмента source↔target) — полезен, но требует
калибровки и выносится в существующий validator tech debt (B-023/B-015). Машина
проверяет frontmatter/naming/registry; **семантическая граница остаётся за
человеком** (rfc-standard стр. 215–216).

**4. Лингвист-аналитик** — «Как исполнитель мог понять это правило иначе?»
Два очага неоднозначности. (а) «Секция ОБЯЗАНА присутствовать» допускает
прочтение «секция обязана быть самодостаточной» — что и произошло в ADR-003
до правки. (б) Формула «**Стандарт является нормативным контрактом**» отождествляет
два термина, которые глоссарий (стр. 22–23, правило #3) требует использовать «как
разные уровни обязательности, а не как взаимозаменяемые слова». Показательно, что
**неоднозначность воспроизводится даже в постановке задачи**: issue называет
контракт «IL-2», тогда как каноническая IL-модель относит контракт к **IL-1**
([`research/hub/2026-06-23-repository-structure-concept.md`](../../research/hub/2026-06-23-repository-structure-concept.md),
строки 861–865, 923–924: «IL-3 (обоснование) → порождает → IL-1 (контракт) + IL-2
(промпт)»). Это не ошибка автора, а **симптом самой аудируемой неоднозначности**:
если IL-уровень контракта путается на входе, тем более он спутается на 100-й
итерации.

### 4.2 Четыре стресс-теста

**Тест 1 «Удаление source».** Мысленно убираем RFC B-016.
- ADR-003 v0.2 `Decision` остаётся осмысленным («принять модель RFC B-016 без
  корректировок» + 4 пункта), но детали недоступны → **корректное делегирование**,
  не дублирование. ✅
- До правки (v0.1) `Decision` пересказывал P1–P4 целиком → был бы самодостаточен
  без RFC → это было **дублирование**. Тест подтверждает, что ремедиация
  устранила именно нарушение SSOT.

**Тест 2 «Инверсия интерпретации».** Берём правило «секция `Alternatives
Considered` обязательна» и применяем противоположное прочтение «секция может
делегировать/быть указателем при наличии source RFC».
- Оба прочтения дают **разный результат** (полная таблица альтернатив vs
  delegation-указатель) → правило **двусмысленно на уровне секции** (F-07). ✅
- Аналогично формула «стандарт задаёт контракт» допускает прочтения «стандарт
  **и есть** контракт» (ошибочно) и «стандарт **лежит в основе** контракта»
  (корректно, глоссарий стр. 65: «Policy → Contract») → **двусмысленно** (F-01). ✅

**Тест 3 «Масштабирование до 10 артефактов»** (Research → RFC → ADR → Standard →
Addendum → Glossary → Delete-profile → Migrate → Validators → …).
- **Масштабируется:** document-level граница (каждая пара знает свою роль по
  инварианту) и SSOT-принцип.
- **Ломается:** section-level наполнение — каждый переход, где обязательная секция
  target смыслово совпадает с секцией source (Decision↔Proposal,
  Alternatives↔Alternatives, Consequences↔Impacted), воспроизводит зазор F-07.
  При 10 артефактах таких стыков — десятки; без посекционного правила дрейф
  дублирования накапливается. Терминологическая конфляция (F-01) при
  масштабировании даёт **экспоненциальный** эффект: стандарт по определению
  переиспользуется «для группы артефактов» (глоссарий стр. 33), поэтому дефект в
  нём тиражируется в каждый порождённый контракт/шаблон/валидатор.

**Тест 4 «Новичок без контекста».** Даём артефакт исполнителю, не видевшему source.
- ADR-003 v0.2: увидит «Модель — RFC B-016, P1» — **явный delegation-указатель**,
  поймёт, что делегировано. ✅ (позитивный контраст к v0.1, где P1–P4 выглядели
  как собственное содержание ADR).
- Шаблон adr-structure-standard: новичок увидит **пустую таблицу**
  `| Alternative | Why rejected |` и **не поймёт**, что при наличии source RFC её
  надо заменить указателем, а не заполнять → **нужно явное delegation-указание** в
  шаблоне (F-07 → рекомендация §6.2). ✅
- Формула «Стандарт является нормативным контрактом»: новичок, сверяясь с
  глоссарием, получит **противоречие** (Standard и Contract — разные термины) →
  нужна однозначная формулировка (F-01 → рекомендация §6.1). ✅

---

## 5. Фиксация проблем (Цель 2)

### 5.1 Реестр находок

Легенда критичности: **[BLOCK]** — блокирует acceptance; **[FIX]** — требует
правки (отдельная задача); **[REC]** — рекомендация. Класс: **CAUSE** —
причина (стандарт/шаблон/процесс); **CONSEQ** — последствие (артефакт).

| ID | Источник | Жертва | Тип нарушения | Секция/поле | Критичность | Класс | Root-cause (гипотеза) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **F-01** | 3 стандарта структуры (research-, adr-, rfc-standard); распространение в CHANGELOG, artifact-map | SSOT терминологии; glossary как canon | Смешение словарей (category error «Стандарт = Контракт») | `Назначение`: research стр. 23/31; adr стр. 13/17; rfc стр. 13/17; CHANGELOG стр. 16; artifact-map стр. 160 | **[FIX]** (системный риск) | **CAUSE** (терминологический) | «Контракт» использован как усилитель нормативности; спутаны уровень артефакта (IL-3 vs IL-1) и роль (norma vs agreement) |
| **F-07** | `standards/adr-structure-standard.md` | любой будущий ADR с source RFC | Двусмысленность шаблона (приглашает наполнение → дублирование) | Минимальный шаблон: `Alternatives Considered` стр. 121–125 (заполненная таблица); `Consequences` стр. 129 («follow-up work») | **[FIX]** | **CAUSE** (структурный) | Граница RFC/ADR задана на уровне документа, не секции; форма шаблона зовёт заполнять, а не делегировать |
| **F-08** | Валидаторы + процесс review | SSOT (дублирование проходит молча) | Недостаток валидации (нет overlap-guard и чеклиста) | `Validation` (rfc-standard стр. 215–216); отсутствие RFC↔ADR overlap-проверки | **[REC]** | **CAUSE** (валидационный) | Граница enforced только людьми; на B-017 review посекционно не проверена |
| **F-02** | `governance/rfc/2026-06-30-rfc-research-structure.md` | сам RFC (внутр. согласованность) + читатель | Устаревшая ссылка (stale forward-ref) | `RFC Metadata` стр. 20–21 (`not yet — будущий ADR (B-017)`, `будущий research-standard.md (B-018)`) | **[FIX]** | **CONSEQ** | RFC написан 2026-06-30 до появления ADR-003/стандарта (2026-07-01); поля `not yet` не обновлены (усилено шаблоном F-07-parallel) |
| **F-03** | `docs/adr/2026-07-adr-003-research-structure.md` | читатель | Пограничная stale-ref | `Decision Metadata`, `Impacted artifacts` стр. 22 (`research-standard.md (B-018, будущий)`) | **[REC]** | **CONSEQ** | Синхронное создание ADR и стандарта 2026-07-01; «будущий» формально ещё верно (B-018 в review, не accepted), но файл существует |
| **F-09** | Цепочка RFC→ADR→Standard | читатель (семантика зрелости) | Несогласованность семантики версий | research-standard `version: 1.0` при `status: draft`; upstream ADR `proposed`, RFC `draft` | **[REC]** | **CONSEQ** | Нет guidance по версионированию downstream относительно статуса upstream; пара (v1.0, draft) допустима, но шумна |
| **F-10** | ADR-003 + research-standard | research-profile.md (объект supersession) | Двойное объявление supersession | ADR-003 стр. 23 `Supersedes research-profile.md`; research-standard как «replacement» | **[REC]** | **CONSEQ** | Два артефакта объявляют замену одного файла; не конфликт (оба отложены до B-021), но точка рассинхронизации |

### 5.2 Детализация ключевых находок

#### F-01 — Терминологическая конфляция «Стандарт = Контракт» (headline, CAUSE)

**Факт.** Формула повторяется дословно во всех трёх стандартах структуры:

- `standards/research-standard.md` стр. 23: «Этот стандарт задаёт обязательный
  **контракт** структуры research-артефактов Хаба»; стр. 31: «Стандарт является
  нормативным **контрактом** (IL-3, документ для человека).»
- `standards/adr-structure-standard.md` стр. 13: «Этот стандарт задаёт
  обязательный **контракт** ADR»; стр. 17: «Стандарт является нормативным
  **контрактом**.»
- `standards/rfc-structure-standard.md` стр. 13: «Этот стандарт задаёт
  обязательный **контракт** RFC-like документов»; стр. 17: «Стандарт является
  нормативным **контрактом**.»
- Распространение (вторичные жертвы): `CHANGELOG.md` стр. 16 «нормативный контракт
  (IL-3)»; `governance/artifact-map.md` стр. 160 «Нормативный контракт (IL-3)».

**Почему это ошибка.** Canonical глоссарий
[`standards/glossary.md`](../../standards/glossary.md) определяет термины как
**разные уровни обязательности**:

- Standard (стр. 33) — «переиспользуемое правило или шаблон, который задаёт
  обязательный формат… для группы артефактов»;
- Contract (стр. 36) — «операционное соглашение между ролями, системами или
  репозиториями: обязанности, входы, выходы, lifecycle и критерии готовности…
  **Contract может включать policies, standards и escalation rules**»;
- правило #3 (стр. 22–23): «Используй `Policy`, `Standard`, `Contract` и
  `Guideline` как разные уровни обязательности, а не как взаимозаменяемые слова»;
- связь (стр. 65): «Policy → Contract | …contract собирает несколько правил,
  ролей и ожиданий в рабочее соглашение».

То есть **контракт может включать стандарт**, но стандарт **не является**
контрактом — это отношение «часть/целое», а не тождество. Каноническая
IL-модель ([концепция](../../research/hub/2026-06-23-repository-structure-concept.md),
стр. 861–865, 923–924) относит Standard к **IL-3** (explanatory MD, документ для
человека), а Contract — к **IL-1** (машинно-валидируемое соглашение), причём
«IL-3 (обоснование) → **порождает** → IL-1 (контракт)». Утверждение «Стандарт
является контрактом» отождествляет **порождающий** артефакт (IL-3) с
**порождаемым** (IL-1) — category error.

**Мета-наблюдение (лингвист-аналитик).** Неоднозначность настолько тонкая, что
воспроизводится и в постановке задачи ([issue #320](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/320):
«контракт — IL-2»), и в истории самой концепции (ранняя формула «IL-1 = 100 %
YAML/JSON» была позже **опровергнута** — [концепция](../../research/hub/2026-06-23-repository-structure-concept.md)
стр. 1087). Каноническое разрешение: **Contract ≈ IL-1** (машинно-валидируемое
соглашение, форма следует функции — может быть и Markdown+RFC-2119, не только
YAML/JSON). Само расхождение меток (задача: IL-2; canon: IL-1) — **живой образец**
того риска, о котором предупреждает issue: «любая незначительная терминологическая
неоднозначность будет порождать экспоненциально ошибки… через 100 итераций».

**Стресс-тесты:** Тест 2 (инверсия) — формула допускает прочтения «есть контракт»
vs «в основе контракта», разные результаты → двусмысленно. Тест 3
(масштабирование) — стандарт переиспользуется «для группы артефактов», поэтому
дефект тиражируется экспоненциально.

**Критичность:** **[FIX]** — не блокирует формальную acceptance текущих
артефактов (валидаторы терминологию не проверяют), но это **системный причинный
риск** с наибольшим горизонтом ущерба. Устранение — Tier 2 amendment стандартов +
B-020 (обновление глоссария). **В рамках этой задачи только флагуется** (см. §1.5).

#### F-07 — Шаблон ADR приглашает дублирование (CAUSE)

**Факт.** В `standards/adr-structure-standard.md` минимальный шаблон (стр. 91–142)
показывает `Alternatives Considered` как **заполненную таблицу**
`| Alternative | Why rejected |` (стр. 121–125), а `Consequences` — как «Positive
effects, trade-offs, and **follow-up work**» (стр. 129).

**Почему это причина.** Стандарт формулирует границу RFC/ADR только на уровне
документа (`Boundary RFC/ADR`, стр. 175–186). На уровне секций возникает зазор:
принцип говорит «делегируй детали в RFC», а форма шаблона показывает «заполни
таблицу»; ближайший источник готового содержания — исходный RFC. Именно этот
зазор реализован как дублирование в ADR-003 (v0.1), что подтверждено root-cause
отчётом. Дефект **активен** для любого будущего ADR с source RFC — поэтому это
причина, а не разовое последствие.

**Критичность:** **[FIX]** — Tier 2 amendment (§6.1) + шаблон (§6.2).

### 5.3 Классификация: причины vs последствия

| Класс | Находки | Смысл |
| --- | --- | --- |
| **Причины** (лечить в первую очередь) | **F-01** (терминология в стандартах), **F-07** (шаблон ADR), **F-08** (нет guard/чеклиста), F-07-parallel (нет правила Research→RFC + шаблон «not yet» в rfc-standard) | Дефекты **стандартов, шаблонов и процесса**; порождают нарушения в артефактах и масштабируются |
| **Последствия** (лечить как отдельные задачи, не блокеры) | **F-02** (stale-refs RFC B-016), **F-03** (stale «будущий» ADR-003), **F-09** (семантика версий цепочки), **F-10** (двойная supersession профиля) | Проявления в **конкретных артефактах**; устраняются точечно, но без лечения причин будут воспроизводиться |
| **Проверено чисто** (позитивные вердикты) | **N-01** ADR-003 посекционное дублирование — ремедиировано; **N-02** research-standard proposal-обёртка — отсутствует; **N-03** RFC B-016 дублирование Research — отсутствует; **N-04** словари статусов — не смешаны; **N-05** cross-references — симметричны (кроме minor F-10) | Подтверждает, что фокус лечения — на **причинах**, а не на «жертвах» |

**Главный вывод классификации:** на уровне **артефактов** цепочка находится в
приемлемом состоянии (блокеров нет, ADR-003 ремедиирован). Реальный риск —
**причинный слой**: правила границы заданы на уровне документа, терминология
конфлатирует Standard/Contract, а автоматический backstop отсутствует. Без лечения
причин те же нарушения воспроизведутся на следующих переходах цепочки (Тест 3).

---

## 6. Рекомендации по лечению причин (Цель 3)

> Все рекомендации ниже — **предложения для отдельных задач**. Изменение стандартов
> структуры — Tier 2 amendment, **вне scope** этой задачи (§1.5). Ничего из
> перечисленного здесь **не применяется**.

### 6.1 Уровень 1: Стандарты (Tier 2 amendment)

- **R1.1 — Посекционное правило делегирования в `adr-structure-standard.md`**
  *(лечит F-07).* Добавить: при наличии source RFC — `Decision` = «что принято» +
  ссылка на RFC за моделью; `Alternatives Considered` = «см. RFC, раздел
  Alternatives»; `Consequences` = только архитектурные последствия, без списка
  задач (он в RFC Impacted Artifacts и `backlog.md`). Добавить **negative
  constraints** для этих трёх секций («НЕ пересказывать proposal», «НЕ копировать
  таблицу альтернатив», «НЕ дублировать план задач»).
- **R1.2 — Симметричное правило Research → RFC в `rfc-structure-standard.md`**
  *(лечит F-07-parallel).* Зафиксировать: `Motivation` **цитирует** benchmark/
  инвентаризацию, но **не воспроизводит** их таблицы; `Proposal` не пересказывает
  research-данные. Плюс правило обновления полей `Decision record`/`Implementation
  link` при появлении референта (лечит корневую форму F-02).
- **R1.3 — Устранение терминологической конфляции «Стандарт = Контракт»**
  *(лечит F-01, headline).* Во всех трёх стандартах структуры заменить формулу
  «Стандарт является нормативным контрактом» на согласованную с глоссарием: стандарт
  — **IL-3 переиспользуемое правило о форме** артефактов; он **не является**
  контрактом, но контракт (IL-1) **может включать** стандарты. Синхронно вычистить
  распространение в `CHANGELOG.md` (стр. 16) и `governance/artifact-map.md`
  (стр. 160). Скоординировать с **B-020** (обновление глоссария Research/Analysis/
  Audit/RFC/ADR/Standard). Заодно уточнить IL-уровень контракта (canon: IL-1).

### 6.2 Уровень 2: Шаблоны

- **R2.1 — Шаблон «ADR с source RFC»** *(лечит F-07, Тест 4).* Секции
  предзаполнены **delegation-указателями** («Полный разбор альтернатив — RFC
  §Alternatives»), а не пустыми таблицами. Готовый образец делегирования —
  ADR-003 v0.2, `Alternatives Considered` (строки 85–95).
- **R2.2 — Шаблон «Standard с source ADR»** *(лечит превентивно ADR→Standard).*
  С явным запретом proposal-обёртки. Готовый позитивный образец —
  `standards/research-standard.md`, строки 31–34.

### 6.3 Уровень 3: Валидация (tech debt)

- **R3.1 — Лёгкий overlap-guard** *(частично лечит F-08).* Эвристика-флаг для
  reviewer/валидатора: сигнал, когда target воспроизводит **крупный непрерывный
  фрагмент** source (RFC↔ADR, ADR↔Standard). Трекать в существующем validator tech
  debt (**B-023 / B-015**); требует калибровки против false positives (короткие
  цитаты-указатели легитимны).
- **R3.2 — Пункт review-чеклиста на acceptance** *(лечит F-08, дёшево).*
  «Пересказывает ли ADR proposal из RFC? Если да — делегировать, а не дублировать»
  и симметрично «Содержит ли Standard proposal-обёртку из ADR?». Детерминированно,
  человекочитаемо, внедряется немедленно.

### 6.4 Приоритизация

| Приоритет | Что | Почему |
| --- | --- | --- |
| **Блокирует масштабирование (делать первым)** | **R1.3** (терминология), **R1.1** (посекционное правило ADR) | F-01 даёт экспоненциальный риск (Тест 3); F-07 — прямая причина воспроизведения дублирования |
| **Дешёвый немедленный backstop** | **R3.2** (чеклист-пункт) | Минимальная цена, ловит рецидив на acceptance до появления guard |
| **Улучшает (следом)** | **R2.1**, **R2.2** (шаблоны), **R1.2** (симметрия Research→RFC) | Закрепляют правило в форме, чтобы дисциплина не зависела от исполнителя |
| **Отложенное (по мере роста)** | **R3.1** (guard-эвристика) | Полезно, но требует калибровки; включать по триггеру роста цепочки |
| **Точечные последствия (отдельные задачи)** | обновить `not yet`→ссылки в RFC B-016 (F-02); `будущий`→факт в ADR-003 (F-03); guidance по версиям (F-09); единый носитель supersession (F-10) | Не блокеры; устраняются после/параллельно лечению причин |

---

## 7. Проверка (воспроизводимо)

Команды, воспроизводящие ключевые вердикты (запускать из корня репозитория):

```bash
# F-01 — терминологическая конфляция «Стандарт = контракт» (3 стандарта + распространение)
grep -rn "является нормативным контрактом\|задаёт обязательный контракт" standards/
grep -rn "нормативный контракт" CHANGELOG.md governance/artifact-map.md

# F-07 — шаблон ADR приглашает наполнение (заполненная таблица + follow-up work)
sed -n '121,129p' standards/adr-structure-standard.md

# F-07-parallel / F-02 — «not yet» без правила обновления (шаблон RFC-стандарта)
sed -n '109,110p' standards/rfc-structure-standard.md
sed -n '20,21p' governance/rfc/2026-06-30-rfc-research-structure.md

# N-01 (verified clean) — делегирование вместо дублирования в ADR-003
sed -n '85,95p' docs/adr/2026-07-adr-003-research-structure.md

# N-02 (verified clean) — явный запрет proposal-обёртки в research-standard
sed -n '31,34p' standards/research-standard.md

# Локальная валидация репозитория (регистрация этого аудита)
./tools/validate-frontmatter.sh .
./tools/validate-file-naming.sh
./tools/validate-repository-structure.sh
python3 tools/generate-manifest.py --check
```

---

## 8. Источники

- [`docs/adr/2026-07-adr-003-research-structure.md`](../adr/2026-07-adr-003-research-structure.md) — ADR-003, v0.2 (проверяемый target; ремедиирован).
- [`governance/rfc/2026-06-30-rfc-research-structure.md`](../../governance/rfc/2026-06-30-rfc-research-structure.md) — RFC B-016, v0.2 (source ADR-003).
- [`standards/research-standard.md`](../../standards/research-standard.md) — B-018, v1.0 (target ADR→Standard).
- [`standards/adr-structure-standard.md`](../../standards/adr-structure-standard.md) — v1.0 (контракт ADR; носитель F-07).
- [`standards/rfc-structure-standard.md`](../../standards/rfc-structure-standard.md) — v1.0 (контракт RFC).
- [`docs/report/2026-07-01-rfc-adr-duplication-analysis.md`](../report/2026-07-01-rfc-adr-duplication-analysis.md) — root-cause анализ дублирования (вход).
- [`standards/glossary.md`](../../standards/glossary.md) — canonical термины Standard/Contract (основание F-01).
- [`research/hub/2026-06-23-repository-structure-concept.md`](../../research/hub/2026-06-23-repository-structure-concept.md) — IL-модель (IL-1/IL-2/IL-3).
- [`docs/audit/2026-06-29-research-artifact-format-contract-audit.md`](2026-06-29-research-artifact-format-contract-audit.md) — формат-образец audit-отчёта.
- [issue #320](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/320) — постановка задачи B-039.
- [issue #316](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/316) — источник root-cause отчёта.
