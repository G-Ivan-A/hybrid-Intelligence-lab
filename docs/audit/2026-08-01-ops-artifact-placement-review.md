---
status: draft
version: 0.1
updated: 2026-08-01
temperature: 0.1
type: audit
context: [hub, routing, research, analysis, audit, artifact-placement, pr-462, ops]
method: contract-reading + registry-scan + precedent-comparison
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/465"
scope: repo
audit_target: "Маршрутизация Research / Analysis / Audit: `standards/research-standard.md` §«Маршрутизация Research / Analysis / Audit» и §«Классификация на этапе создания задачи»; `standards/analysis-standard.md` §Boundaries; `standards/audit-standard.md` §Boundaries; `standards/report-standard.md` §Boundaries; `standards/glossary.md` (Research / Analysis / Audit); ADR-007 §структура корня; `pr-ops/artifact-map.md` §«Как обновлять карту»"
evidence_model: "contract-reading + registry-scan (grep по репозиторию) + прогон локальных валидаторов + сравнение с прецедентом"
verdict: pass
severity_scale: "Critical/Major/Minor/Info"
follow_up: "—"
related_norm: "standards/research-standard.md, standards/analysis-standard.md, standards/audit-standard.md, standards/report-standard.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/465"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/461"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/288"
related_artifacts:
  - "research/hub/2026-07-31-ops-task-strategy-validation.md"
  - "research/hub/exp/ops-task-strategy-461/README.md"
  - "research/hub/2026-07-04-hub-as-agent-system-global-analysis.md"
  - "standards/research-standard.md"
  - "standards/analysis-standard.md"
  - "standards/audit-standard.md"
  - "standards/report-standard.md"
  - "standards/glossary.md"
  - "docs/adr/2026-07-adr-007-hub-root-structure.md"
  - "pr-ops/artifact-map.md"
---

# Аудит размещения артефактов PR #462: `research/hub/` vs `docs/`

## Summary / BLUF

**Вердикт: `pass` — размещение корректно, перенос не требуется.** Артефакты
PR [#462](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/462)
(`research/hub/2026-07-31-ops-task-strategy-validation.md` и контейнер
`research/hub/exp/ops-task-strategy-461/`) соответствуют дому Research по
действующим контрактам маршрутизации.

Решающий пункт нормы — тай-брейкер `Research vs Analysis` в
[research-standard §«Классификация на этапе создания задачи»](../../standards/research-standard.md):
«наличие внешних источников, индустриального сравнения **или проверки гипотезы**
относит документ к Research». Работа PR #462 делает все три вещи: проверяет явно
сформулированную гипотезу, сравнивает результат с индустриальной базой
`research/ai-education/task-processing/` и производит воспроизводимый evidence
corpus в контейнере `exp/`, который нормируется **только** research-стандартом.
Audit исключён по 4-компонентной модели (нет compliance target и нет вердикта
pass/fail по норме), Analysis — по доминирующему deliverable (knowledge claim,
а не интерпретация локального состояния без внешнего знания).

Найдено одно отклонение вне вопроса размещения: артефакты PR #462 не были
зарегистрированы в `pr-ops/artifact-map.md` (Minor). Оно устранено в этом PR;
содержание артефактов PR #462 не изменялось.

## Scope / Target

Проверяется **только размещение** (routing) двух артефактов и разрешимость
ссылок на них. Содержание артефактов PR #462 вне границ проверки
(ограничение issue #465).

Нормы проверки (compliance target):

| # | Норма | Пункт |
| --- | --- | --- |
| N1 | [`standards/research-standard.md`](../../standards/research-standard.md) | §«Маршрутизация Research / Analysis / Audit» (таблица «Тип → Дом артефакта»), §«Классификация на этапе создания задачи» (порядок проверок 1–4 и тай-брейкеры) |
| N2 | [`standards/analysis-standard.md`](../../standards/analysis-standard.md) | §Boundaries, граница `Analysis ↔ Research` и нормативный тай-брейкер |
| N3 | [`standards/audit-standard.md`](../../standards/audit-standard.md) | §Boundaries, граница `Audit ↔ Research`; 4-компонентная модель ядра Audit |
| N4 | [`standards/report-standard.md`](../../standards/report-standard.md) | §Boundaries, граница Report ↔ Research/Analysis |
| N5 | [`standards/glossary.md`](../../standards/glossary.md) | канонические определения Research / Analysis / Audit и Evidence-контейнер |
| N6 | [ADR-007](../adr/2026-07-adr-007-hub-root-structure.md) | структура корня: `research/hub/` — Hub methodology and governance research; `docs/analysis/`, `docs/audit/` |
| N7 | [`pr-ops/artifact-map.md`](../../pr-ops/artifact-map.md) | §«Как обновлять карту»: новый активный артефакт регистрируется в карте и в валидаторе структуры |

Объекты проверки:

- `research/hub/2026-07-31-ops-task-strategy-validation.md`;
- `research/hub/exp/ops-task-strategy-461/` (17 файлов: README, 5 скриптов,
  логи и зафиксированные JSON-результаты).

## Method / Evidence

1. **Contract-reading.** Прочитаны N1–N6 целиком; выписаны нормативные
   формулировки routing и тай-брейкеры (цитаты — в §Findings).
2. **Признаковая разметка объекта.** Тело отчёта PR #462 сопоставлено с
   критериями каждого типа по фактическим секциям документа (§0 гипотеза,
   §3–4 эксперименты, §5 индустриальная матрица, §6 ответ на гипотезу).
3. **Precedent comparison.** Сравнение с
   [`research/hub/2026-07-04-hub-as-agent-system-global-analysis.md`](../../research/hub/2026-07-04-hub-as-agent-system-global-analysis.md)
   по тем же критериям.
4. **Registry-scan.** `grep` по репозиторию на упоминания обоих путей:
   `research/hub/README.md`, `CHANGELOG.md`,
   `tools/validate-repository-structure.sh` (`is_active_file`, `required_files`),
   `pr-ops/artifact-map.md`, `pr-ops/backlog.md`.
5. **Валидаторы.** `./tools/validate-frontmatter.sh .`,
   `./tools/validate-file-naming.sh`, `./tools/validate-evidence-structure.sh`,
   `./tools/validate-repository-structure.sh` — до и после изменений этого PR.

Доказательная база — сами нормы и репозиторий на коммите этого PR;
новых измерений не производилось.

## Findings / Verdict

### F1 — Тип работы PR #462 — Research (Info, определяющий finding)

Применён детерминированный порядок проверок N1 §«Классификация на этапе создания
задачи»:

| Шаг нормы | Проверка | Результат |
| --- | --- | --- |
| 1. Audit? | Проверяется ли текущее состояние против явной нормы/контракта/checklist? | **Нет.** Документ не имеет compliance target и не выносит pass/fail по норме; он проверяет гипотезу об эффективности постановки задач. По N3 4-компонентная модель не выполняется (нет компонентов 1 и 3). |
| 2. Research? | Генерируется ли новое знание / сравнение за границей репо? | **Да.** §0 фиксирует проверяемую гипотезу, §3–4 — четыре эксперимента с воспроизводимыми скриптами, §5 — сравнительная матрица «наша практика × эксперименты × индустриальная норма», §6 — вердикт по каждой части гипотезы. |
| 3. Analysis? | — | не достигается: шаг 2 уже разрешил классификацию. |
| 4. Operational run? | Главный результат — факт выполнения задачи? | **Нет.** Deliverable — knowledge claim и матрица вариантов для будущего RFC, а не запись прогона. |

Нормативные основания дословно:

- N1, тай-брейкер `Research vs Analysis`: «Наличие внешних источников,
  индустриального сравнения или проверки гипотезы относит документ к Research;
  чистое рассуждение о внутреннем состоянии — к Analysis».
- N2, граница `Analysis ↔ Research`: «Research генерирует новое внешнее/доменное
  знание (source-backed benchmark, гипотеза); Analysis интерпретирует
  локальный/внутренний контекст».
- N3, граница `Audit ↔ Research`: Research «становится Audit только когда эти
  практики применяются как норма/checklist к конкретному артефакту с findings» —
  условие не выполнено.
- N4, граница Report: документ не является descriptive execution log; он
  объясняет и обосновывает, а не фиксирует «что произошло».
- N5, глоссарий: Research «отличается от `Analysis` внешней новизной, а от
  `Audit` отсутствием проверки на соответствие норме».

**Возражение, которое нужно снять.** Корпус измерений (479 PR и 475 issue) —
внутренний, и это единственный аргумент в пользу Analysis. Он недостаточен по
двум причинам. Во-первых, норма N1 формулирует тай-брейкер дизъюнкцией: любой из
трёх признаков (внешние источники, индустриальное сравнение, проверка гипотезы)
относит документ к Research; в PR #462 присутствуют все три, а происхождение
данных признаком не является. Во-вторых, доминирующий deliverable (правило «один
артефакт запрещено нормировать как два типа сразу», N1/N2) — это ответ на
гипотезу и матрица вариантов A–E с индустриальной привязкой, то есть новое
знание, а не интерпретация текущего состояния Хаба.

**Подтверждение через evidence-контейнер.** Контейнер
`research/<domain>/exp/<issue-slug>/` определён N1 и N5 исключительно для
research evidence corpus; ни Analysis, ни Audit не имеют собственного контейнера
такого типа (N2: Analysis «ССЫЛАЕТСЯ и ЦИТИРУЕТ доказательную базу»; N3:
«сгенерированные матрицы/scan output — evidence, а не Audit»). Перенос отчёта в
`docs/analysis/` или `docs/audit/` оставил бы `exp/ops-task-strategy-461/` без
parent dated report в `research/`, что прямо нарушает N1: «Каждый эксперимент
ДОЛЖЕН ссылаться на родительский dated report». То есть перенос не нейтрален —
он произвёл бы новое нарушение.

**Вердикт F1: соответствует.** Дом артефакта по N1 —
`research/<domain>/YYYY-MM-DD-name.md` + опциональный
`research/<domain>/exp/<issue-slug>/`. Фактическое размещение совпадает.

### F2 — Соответствие форме research-артефакта (Info)

Проверка формы (N1 §Identification and Placement, §Evidence Container):

| Правило N1 | Факт | Итог |
| --- | --- | --- |
| Canonical path `research/<domain>/` | `research/hub/` | ✅ |
| Имя `YYYY-MM-DD-name.md` | `2026-07-31-ops-task-strategy-validation.md` | ✅ |
| Единый контейнер `exp/` (не sibling `exp-<slug>/`) | `research/hub/exp/ops-task-strategy-461/` | ✅ |
| `<issue-slug>` включает номер issue | `ops-task-strategy-461` (issue #461) | ✅ |
| Плоская структура, запрет `outputs/`/`inputs/` | 17 файлов плоско, `outputs/` отсутствует | ✅ |
| README эксперимента ссылается на parent dated report | `exp/ops-task-strategy-461/README.md` строки 12 и 77 | ✅ |
| knowledge-vocabulary в `status` | `status: draft` | ✅ |
| `ai-generated` запрещён | отсутствует | ✅ |
| Направление зарегистрировано в `research/hub/README.md` | строки 39 и 51 | ✅ |

Форма подтверждает классификацию: артефакт уже оформлен по research-стандарту, и
никакой другой стандарт его форму не описывает.

### F3 — Прецедент применим и не создаёт конфликта (Info)

Сравнение с
`research/hub/2026-07-04-hub-as-agent-system-global-analysis.md` (v0.4):

| Критерий | Прецедент (глобальный анализ) | PR #462 | Совпадение |
| --- | --- | --- | --- |
| Слово «анализ» в названии | да | нет («валидация») | — |
| `type` во frontmatter | `research` | `ops-task-strategy-validation` | ⚠️ см. F4 |
| Проверяемые гипотезы | 27 гипотез, 157 стресс-тестов | 1 гипотеза, 4 направления проверки | ✅ |
| Индустриальное сравнение | §10 индустриальный анализ | §5 сравнительная матрица | ✅ |
| Deliverable | вход для будущих стандартов/RFC, ничего не нормирует | вход для будущего RFC, ничего не нормирует | ✅ |
| Вердикт по норме (Audit-признак) | нет | нет | ✅ |
| Дом | `research/hub/` | `research/hub/` | ✅ |

Прецедент размещён в `research/hub/` не из-за слова «анализ» в заголовке, а
потому что его доминирующий deliverable — гипотезы и индустриальные нормы, то
есть новое знание (N1: тип определяется «содержательной ролью, а не именем
каталога»). Та же логика применима к PR #462: обе работы опираются на
внутренний материал Хаба, но производят knowledge claim, а не интерпретацию
состояния и не проверку нормы. Прецедент **подтверждает** размещение PR #462 и
не является контрпримером.

### F4 — Значение `type` во frontmatter идиосинкратично (Info, без ремедиации)

`research/hub/2026-07-31-ops-task-strategy-validation.md` использует
`type: ops-task-strategy-validation`, тогда как соседние research-отчёты Хаба
используют `type: research`. Нарушения нормы нет: по
[`frontmatter-docs-standard.md`](../../standards/frontmatter-docs-standard.md)
`type` для класса Research / report — **опциональное** поле без контролируемого
словаря, и `./tools/validate-frontmatter.sh .` проходит. Фиксируется как
наблюдение о консистентности; ремедиация не выполняется, поскольку issue #465
запрещает изменять содержание артефактов PR #462, а routing от этого поля не
зависит (N1: тип определяется содержательной ролью).

### F5 — Артефакты PR #462 не зарегистрированы в artifact-map (Minor, устранено)

`pr-ops/artifact-map.md` §«Как обновлять карту» требует: «При создании нового
активного артефакта → добавь строку в таблицу, укажи тип, обязательность и связи,
и зарегистрируй файл в `tools/validate-repository-structure.sh`». Registry-scan
показал:

| Реестр | `2026-07-31-ops-task-strategy-validation.md` | `exp/ops-task-strategy-461/` |
| --- | --- | --- |
| `research/hub/README.md` | ✅ зарегистрирован | ✅ зарегистрирован |
| `tools/validate-repository-structure.sh` (`is_active_file`, `required_files`) | ✅ зарегистрирован | ✅ зарегистрирован |
| `CHANGELOG.md` | ✅ запись есть | ✅ запись есть |
| `pr-ops/artifact-map.md` | ❌ строка отсутствовала | ❌ строка отсутствовала |

Отклонение не связано с размещением и не влияет на вердикт F1: оно одинаково
проявилось бы в любом каталоге. Severity Minor — карта отражает фактическое
состояние с пробелом, но ни один валидатор и ни одна ссылка не ломались.

### Итоговый вердикт

| Finding | Severity | Статус |
| --- | --- | --- |
| F1 — тип работы PR #462 = Research, размещение в `research/hub/` корректно | Info | соответствует |
| F2 — форма research-артефакта соблюдена | Info | соответствует |
| F3 — прецедент применим и подтверждает размещение | Info | соответствует |
| F4 — идиосинкратичное значение `type` | Info | отклонение принято (вне границ issue #465) |
| F5 — отсутствие строк в artifact-map | Minor | устранено в этом PR |

**Вердикт: `pass`.** Перенос артефактов PR #462 в `docs/analysis/` или
`docs/audit/` **не требуется и был бы нарушением** N1 (разрыв связи
`exp/` → parent dated report).

## Remediation / Deviation

| Finding | Действие | Где |
| --- | --- | --- |
| F1–F3 | Ремедиация не требуется; обоснование зафиксировано в этом отчёте (DoD 3 issue #465). | — |
| F4 | **Отклонение принято.** Ремедиация не выполняется: содержание артефактов PR #462 изменять запрещено (⛔ issue #465). Нормы не нарушено. Пересматривается, если в `frontmatter-docs-standard.md` появится контролируемый словарь `type`. | — |
| F5 | **Устранено в этом PR:** добавлены строки для отчёта, контейнера `exp/` и этого аудита в `pr-ops/artifact-map.md`; этот аудит зарегистрирован в `tools/validate-repository-structure.sh` (`is_active_file`) с проверками структуры (`audit_target`, `evidence_model`, `verdict`, обязательные секции). | `pr-ops/artifact-map.md`, `tools/validate-repository-structure.sh` |

Файлы PR #462 не перемещались и не редактировались; `git` не содержит изменений
в `research/hub/2026-07-31-ops-task-strategy-validation.md` и
`research/hub/exp/ops-task-strategy-461/`.

Валидация после изменений (DoD 5–6 issue #465): `./tools/validate-frontmatter.sh .`,
`./tools/validate-file-naming.sh`, `./tools/validate-evidence-structure.sh` и
`./tools/validate-repository-structure.sh` (включает проверку разрешимости
внутренних markdown-ссылок) проходят.

## Related Artifacts

- [`research/hub/2026-07-31-ops-task-strategy-validation.md`](../../research/hub/2026-07-31-ops-task-strategy-validation.md) — объект проверки (PR #462, issue #461).
- [`research/hub/exp/ops-task-strategy-461/README.md`](../../research/hub/exp/ops-task-strategy-461/README.md) — evidence-контейнер, объект проверки.
- [`research/hub/2026-07-04-hub-as-agent-system-global-analysis.md`](../../research/hub/2026-07-04-hub-as-agent-system-global-analysis.md) — прецедент размещения.
- [`standards/research-standard.md`](../../standards/research-standard.md) — N1, источник routing Research / Analysis / Audit.
- [`standards/analysis-standard.md`](../../standards/analysis-standard.md) — N2, граница Analysis ↔ Research.
- [`standards/audit-standard.md`](../../standards/audit-standard.md) — N3, граница Audit ↔ Research и форма этого отчёта.
- [`standards/report-standard.md`](../../standards/report-standard.md) — N4, граница Report.
- [`standards/glossary.md`](../../standards/glossary.md) — N5, канонические определения.
- [ADR-007: структура корня Хаба](../adr/2026-07-adr-007-hub-root-structure.md) — N6.
- [ADR-003: структура research и маршрутизация](../adr/2026-07-adr-003-research-structure.md) — источник принятого routing-решения.
- [`pr-ops/artifact-map.md`](../../pr-ops/artifact-map.md) — N7, реестр артефактов.
- [`docs/audit/2026-07-04-cross-standard-stress-tests.md`](2026-07-04-cross-standard-stress-tests.md) — смежный аудит цепочки R/A/A/Report.
