---
status: draft
version: 0.1
updated: 2026-06-19
temperature: 0.1
---

# RFC: Независимое видение структуры репозитория(ев) `mango_ba_prompts` (ИБ, внешнее хранилище, экосистема) / Independent Vision of `mango_ba_prompts` Repository Structure

## Proposal / Предложение

Зафиксировать результат **независимого анализа** (Operating Mode `Creative`,
lifecycle `Research → RFC`) структуры репозитория `mango_ba_prompts` и предложить
оптимальную целевую архитектуру с учётом **информационной безопасности (ИБ /
information security)**, **внешнего хранилища (external storage)** и связи с
экосистемой (Hub `hybrid-Intelligence-lab`, портал `open-ai.ru`,
`clarify-engine-ai`).

Документ синтезирует **четыре независимые оценки** (видения команд C, Q, G и
фаундера / founder), сверяет их с **реальным состоянием** репозитория на
2026-06-19 и формулирует **собственное решение архитектора**, а не выбирает одно
из четырёх видений. RFC фиксирует исследование, синтез и обоснование (rationale);
обязательная норма после решения Пользователя (human decision) должна быть
делегирована в active artifact самого спока (`standards/`, validators,
операционный контракт), а до этого остаётся рекомендацией
([docs/rfc/README.md](../../docs/rfc/README.md)).

## Decision Scope / Границы решения

- Это **RFC по архитектуре спока** `mango_ba_prompts`. Хаб
  (`hybrid-Intelligence-lab`) — источник методологии; физическая
  реструктуризация Mango выполняется **отдельным PR в самом споке**, не здесь
  (ср. [projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md](../../projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md)).
- Это **не** немедленное создание private-репозитория или Object Storage — RFC
  определяет, **что** туда выносить и **в каком порядке**, решение и исполнение —
  за Пользователем.
- Это **не** оптимизация документации по токенам. Проблема токеновой инфляции
  только **фиксируется** (раздел ФТ-8), решение — отдельная задача, зависящая от
  результатов этого RFC (по требованию фаундера).
- Все 4 прикреплённых видения — **входные данные**, а не директива. Комментарии
  фаундера в файлах («считаю сильным», «не считаю приоритетным») учтены как вес
  мнения, но не как обязательность.
- Источники-снимки: дерево `G-Ivan-A/mango_ba_prompts@main` и 4 файла видений,
  снятые 2026-06-19.

---

## 1. ФТ-1. Аудит реального репозитория `mango_ba_prompts` / Audit of the Real Repository

Ниже — фактическое состояние `main` на 2026-06-19 (проверено по дереву Git, а не
по пересказам видений). Это важно: часть видений ссылается на каталоги, которых
нет (или есть под другим именем).

### 1.1. Фактическое дерево (сокращённо) / Actual Tree (abridged)

```text
mango_ba_prompts/
├── README.md  AI_GOVERNANCE.md  AI_QUICK_RULES.md  AI_SESSION_HANDOVER_PROMPT.md
├── CHANGELOG.md  CONTRIBUTING.md  LICENSE  Makefile  .hub-profile.json
├── docs/
│   ├── adr/                 # 0001..0003 (4-значные) + 001..010 (3-значные) — РАЗНАЯ нумерация
│   ├── analysis/
│   ├── audit/
│   ├── ba-process/          # singular — реальный кейс multichannel-agent-workload/
│   │   └── multichannel-agent-workload/  # inputs/ steps/ prompts-chain.md experiment-log.md final-artifact.md
│   ├── ba-processes/        # plural — ВНУТРИ ТОЛЬКО 00-index.md (директория из 1 файла)
│   ├── reviews/  screenshots/
├── governance/
│   ├── BACKLOG.md  artifact-map.md  agent-onboarding-protocol.md  session-digests.md
│   ├── analysis-bcreq-1025-2026-06-17.md          # operational record, не governance
│   ├── audit-contracts-2026-06-17.md  audit-contracts-mango-2026-06-17.md
│   ├── audit-hub-2026-06-17.md  audit-research-1027.md
│   ├── sync-matrix-2026-06-17.md
│   ├── migration-issues-registry.md  migration-manifest.md  migration-phase1-issues.md
│   ├── rfc-process.md  rfc-register.md  rfc-to-hub-001-*.md  rfc-to-hub-002-*.md
│   ├── prompt-debugging-process.md  prompt-feedback.json
│   ├── knowledge-transfer-to-hub/  # README + ba-ontology + bcreq-process + operations-taxonomy + pages-ux
│   └── rfc/                        # prompt-improvement-*-proposal.md (×2)
├── kb/
│   ├── sources/  processed/  fragments/  practices/
├── patterns/  # asr-ingestion/ fr-generation/ ... каждый с examples/
├── prompts/
│   ├── archive/  experiments/   # ← experiments внутри prompts
│   └── *.md (~30 промптов: oneshot/stepwise/legacy)
├── experiments/  # ← root: ТОЛЬКО 2 .mjs-скрипта
├── scripts/kb/   site/data/   standards/  # ~13 standards + GLOSSARY.md
```

### 1.2. Что работает хорошо / What Works Well

- **`prompts/` уже зрелый**: организован (`archive/`, `experiments/`), промпты с
  frontmatter-контрактом (status, version, updated, temperature), осмысленное
  именование `[biz-process]-[mode].md` (oneshot/stepwise/legacy). Это
  подтверждает команда Q и опровергает радикальное предложение команды C
  «ликвидировать `prompts/`».
- **`standards/` как отдельный нормативный слой** — ~13 стандартов, отделены от
  ADR. Сильный фундамент (команда G).
- **`patterns/`** — чёткое разделение «паттерн (reusable) vs промпт
  (executable)», по операциям с `examples/`.
- **`kb/`** — заложен hybrid-pipeline (`sources/ → processed/ → fragments/`),
  есть `scripts/kb/` для извлечения из PDF (сценарий 1).
- **GitHub Pages (`site/`)** и наследование генома Хаба (`.hub-profile.json`,
  `AI_GOVERNANCE.md`).

### 1.3. Что работает плохо / What Works Badly (подтверждено по дереву)

| # | Проблема | Факт из дерева (а не пересказ) | Кто заметил |
| --- | --- | --- | --- |
| P1 | **Коллизия имён `ba-process` vs `ba-processes`** | `docs/ba-process/` (singular, реальный кейс) и `docs/ba-processes/` (plural, **только** `00-index.md`) сосуществуют | G (точно), C/Q (косвенно) |
| P2 | **Каталог = имя задачи, а не процесса** | `docs/ba-process/multichannel-agent-workload/` — имя задачи (BCREQ), не процесса | C, Q, founder |
| P3 | **Смешение Definition / Run** | в одном каталоге `prompts-chain.md`, `steps/` (определение) рядом с `experiment-log.md`, `final-artifact.md`, `inputs/` (результат) | C (P8), Q |
| P4 | **Нет единого `runs/`** | результаты расползаются по `governance/analysis-*`, `prompts/experiments/`, `docs/ba-process/.../experiment-log.md` | C (P12), Q, G |
| P5 | **`governance/` как свалка operational records** | `analysis-bcreq-1025-*`, `audit-*` (×4), `sync-matrix-*`, `migration-*` (×3) лежат рядом с правилами | C (P3/P4), G, Q, founder |
| P6 | **Дубль имён `experiments/`** | root `experiments/` (2 `.mjs`) и `prompts/experiments/` (10+ записей прогонов) | G (точно), C |
| P7 | **Файлы синхронизации с Хабом** | `sync-matrix-*`, `audit-hub-*`, `knowledge-transfer-to-hub/`, `rfc-to-hub-00X-*` противоречат принципу «проекты независимы, один мост» | founder (Вывод 1), Q |
| P8 | **Непоследовательная нумерация ADR** | `docs/adr/` содержит и `0001..0003` (4-значные), и `001..010` (3-значные) | (выявлено в этом аудите) |
| P9 | **Директории из одного файла** | `docs/ba-processes/` = 1 файл; `governance/knowledge-transfer-to-hub/` оправдан слабо | C (P13), G |
| P10 | **Нет контракта записи результатов** | нельзя однозначно ответить «куда сохранять результат прогона» | C (P14), Q, G |
| P11 | **Размноженный RFC-механизм в governance** | `rfc-process.md` + `rfc-register.md` + `rfc-to-hub-*` + подкаталог `rfc/` — четыре места для одной сущности | (выявлено), пересекается с C (P5) |

**Главный риск (синтез):** не качество промптов, а **отсутствие модели данных** —
через 3–6 месяцев и 300+ кейсов станет невозможно понять, где источник истины
(source of truth) и куда писать результат очередного прогона. Это совпадает с
выводом команды C и подтверждается фактическим деревом.

---

## 2. ФТ-2. Независимый анализ 4 видений / Independent Analysis of the Four Visions

### 2.1. Ключевые тезисы каждого видения / Key Theses

- **Команда C (founder: «сильное»):** радикальная модель из 5 классов данных
  (Knowledge, Standards, Processes, Runs, Governance). Главный вклад — диагноз
  «смешение 6 доменов», концепт `runs/` + контракт записи, трёхконтурная ИБ
  (Public repo / Private repo / Object Storage), список «что нельзя в публичном
  GitHub». Радикальные предложения: ликвидировать `prompts/`, `experiments/`,
  слить ADR в Standards.
- **Команда Q (founder: «сильное»):** комментатор-арбитр. Принимает диагноз и
  `runs/`, но **корректирует фактические ошибки C** (есть `experiments/`,
  `prompts/` зрелый, ADR ≠ дубликат Standards). Добавляет семантику Experiment ≠
  Run, эволюционное (не революционное) переименование KB, инструментальный
  аспект (Codex для Private, GitHub Private бесплатен).
- **Команда G (founder: «не приоритетное»):** «полевой» аудит. Сильная сторона —
  точные наблюдения по дереву (коллизия `experiments/`, `ba-process` vs
  `ba-processes`, дубли матриц/индексов, директории-пустышки). Слабая —
  рекомендации поверхностные («объединить, обрезать boilerplate»), частично
  залезают в запрещённую сейчас токен-оптимизацию.
- **Видение фаундера (итог):** независимые решения по спорным точкам:
  `multichannel-agent-workload/` → имя процесса; ADR → `standards/decisions/`;
  `docs/` остаётся; убрать файлы синхронизаций, оставив один мост
  `docs/hub-research-dependencies.md`; промпт синхронизации →
  `governance/prompts/hub-sync-prompt.md`; два репо (`mango_ba_framework` Public +
  `mango_ba_operations` Private); сначала хранилище в Яндексе, потом VPS.

### 2.2. Таблица сравнения видений / Comparison Table

Легенда: ✅ предложено/поддержано · ❌ против/ликвидировать · ⚠️ частично/с
условием · — не затрагивает.

| # | Тезис | C | Q | G | Founder | **Решение RFC (независимое)** |
| --- | --- | :-: | :-: | :-: | :-: | --- |
| 1 | Диагноз «смешение доменов данных» | ✅ | ✅ | ✅ | ✅ | **Принять** — подтверждено деревом |
| 2 | Создать единый `runs/` + контракт записи | ✅ | ✅ | ✅ | ✅ | **Принять** (ядро решения) |
| 3 | Ликвидировать `prompts/` (в `processes/*/prompts.md`) | ❌(за) | ❌(против) | ⚠️ | ❌(против) | **Отклонить** — `prompts/` зрелый; добавить cross-links |
| 4 | Ликвидировать `experiments/` | ❌(за) | ⚠️(против) | ⚠️ | ❌(против) | **Отклонить, но переопределить** как метаданные группы Runs |
| 5 | Слить ADR в Standards / ликвидировать ADR-слой | ❌(за) | ❌(против) | — | ❌(против) | **Отклонить слияние; принять** ADR → `standards/decisions/` |
| 6 | `docs/` удалить из корня | ❌(косв.) | ❌(против) | ⚠️ | ❌(против) | **Отклонить** — `docs/` остаётся |
| 7 | Каталог-кейс → имя процесса; split Definition/Run | ✅ | ✅ | ✅ | ✅ | **Принять** |
| 8 | Очистить `governance/` от operational records | ✅ | ✅ | ✅ | ✅ | **Принять** |
| 9 | Убрать sync-файлы, оставить один мост к Хабу | ⚠️ | ✅ | ⚠️ | ✅ | **Принять** (`docs/hub-research-dependencies.md`) |
| 10 | Промпт синхронизации → `governance/prompts/` | — | ✅ | — | ✅ | **Принять** |
| 11 | Три контура ИБ: Public / Private / Object Storage | ✅ | ✅ | — | ✅ | **Принять** |
| 12 | Эволюционное переименование KB (sources→raw…) | ❌(жёстко) | ⚠️(мягко) | ⚠️ | — | **Принять Q-версию** (эволюционно, отдельной задачей) |
| 13 | Слой `context-contracts/` (KB↔Prompt) | ✅ | — | — | — | **Отклонить сейчас** (Anti-Inflation; вернуть при RAG-фазе) |
| 14 | В GitHub — только агрегаты прогонов, не сырьё | ✅ | ⚠️ | ✅ | ⚠️ | **Принять как целевое** (агрегаты-статистика в Public) |
| 15 | Имя репо `mango_ba_prompts`→`mango_ba_framework` | ✅ | ✅ | — | ✅(при обосновании) | **Условно** — переименование не блокирует реформу (см. §3) |
| 16 | Token Inflation как корневая проблема | ✅ | ✅ | ✅ | ✅ | **Только зафиксировать** (ФТ-8), не решать |

### 2.3. Пересечения и противоречия / Overlaps and Contradictions

- **Сильное согласие (4/4):** диагноз, `runs/` + контракт, split Definition/Run,
  очистка governance, трёхконтурная ИБ. Это — фундамент, риск здесь минимален.
- **Главное противоречие — судьба `prompts/` и `experiments/`:** C хочет
  ликвидировать, Q/founder против. **Решение RFC встаёт на сторону Q/founder**, и
  это обоснованно фактом: `prompts/` уже несёт frontmatter-контракт и
  переиспользуется между процессами; ликвидация ломает рабочую структуру без
  выигрыша.
- **Фактические ошибки C, на которые опирались бы решения:** «нет
  `experiments/`», «ADR дублирует Standards», «`prompts/` неорганизован» —
  опровергнуты деревом. Поэтому **радикальную 5-слойную модель C принимаем как
  целевой словарь сущностей, но не как немедленный снос текущей структуры**
  (founder Вывод 3: «опыт наследования потерпел частичный крах, требует
  переосмысления»).
- **G полезен фактами, слаб рекомендациями:** его наблюдения (P1, P6, P8 выше)
  встроены в аудит, но его советы про «обрезать boilerplate» отклонены как
  преждевременная токен-оптимизация (нарушает запрет фаундера).

---

## 3. ФТ-3. Варианты структуры и независимое решение / Structure Options and Decision

### 3.1. Сравнение вариантов / Options

**Вариант A — один репозиторий (Public) + внешнее хранилище.**
Один публичный репо хранит методологию + агрегаты; всё «боевое» (raw runs,
артефакты, клиентские данные) — в Object Storage с аутентификацией.
- *Плюсы:* минимум инфраструктуры; один источник для Конарда (работает только с
  Public); проще навигация для нового сотрудника.
- *Минусы:* промежуточные `runs/` без сырья всё равно тянут метаданные прогонов в
  Public; нет защищённого Git-контура для версионирования feedback/аудита.

**Вариант B — два репозитория (Public framework + Private operations) +
внешнее хранилище.**
Public: методология, стандарты, процессы, промпты, публичная KB, агрегаты.
Private: `runs/`, feedback, артефакты, аудит. Object Storage: сырьё (PDF/DOCX),
полные диалоги LLM, готовые ТЗ, логи прогонов.
- *Плюсы:* чистое разделение ИБ-контуров; Private версионирует
  feedback/аудит в Git; Codex от OpenAI работает с Private; GitHub Private
  бесплатен для personal account. Совпадает с выводом всех 4 видений.
- *Минусы:* два репо = два набора genome-файлов для синхронизации; больше
  операционной дисциплины.

**Вариант C — мульти-репо «по доменам» (framework + operations + knowledge-vault
как отдельный repo) или монорепо с строгими CODEOWNERS.**
- *Минусы:* избыточная дробность (нарушает Anti-Inflation,
  [pr-ops/repo-model.md](../../pr-ops/repo-model.md)); knowledge-vault логичнее как
  Object Storage, а не Git-репо (бинарные PDF/DOCX/транскрипты).

### 3.2. Независимое решение / Decision

**Рекомендуется Вариант B как целевая архитектура, реализуемый поэтапно
(phased), начиная с Phase 0 внутри текущего одного репозитория.**

Обоснование (независимый синтез, а не выбор одного видения):

1. **B — единственный, поддержанный всеми 4 видениями**, и он напрямую закрывает
   ИБ-риск №1 (боевые прогоны = «датасет обучения корпоративного аналитика»,
   формулировка C, поддержана Q).
2. **Но переход к B не требует немедленного раскола репозитория.** Главную боль
   (нет модели данных) решает не второй репо, а **контракт `runs/` и очистка**,
   которые можно ввести уже в текущем Public-репо (Phase 0). Это снимает риск
   «большого взрыва» и согласуется с принципом последовательности (НФТ-9) и
   Anti-Inflation.
3. **Object Storage — приоритетный первый инфраструктурный шаг** (фаундер: «реали-
   зации хранилища — приоритетно»), потому что именно сырьё (raw) и полные
   диалоги несут максимальный ИБ-риск и максимальный объём (бинарники не место в
   Git).
4. **Переименование `mango_ba_prompts → mango_ba_framework` — необязательное и не
   блокирующее.** Имя `mango_ba_prompts` сужает смысл (репо шире промптов), но
   переименование ломает внешние ссылки/Pages. Рекомендация: переименовать только
   вместе с расколом на Phase 2, не раньше; до тех пор имя — косметика.

**Фазовая дорожная карта / Phased roadmap (последовательность, НФТ-9):**

| Фаза | Что | Где | ИБ-контур |
| --- | --- | --- | --- |
| **Phase 0** (P0) | Ввести `runs/` + контракт записи; почистить `governance/`; split Definition/Run; убрать sync-файлы, оставить один мост; ADR → `standards/decisions/`; устранить коллизии имён (P1/P6/P8) | текущий Public repo | Public |
| **Phase 1** (P0→P1) | Поднять Object Storage (Yandex S3) для сырья/диалогов; перенести raw KB и полные прогоны туда | Object Storage | Confidential |
| **Phase 2** (P1) | Создать `mango_ba_operations` (Private); перенести `runs/`, feedback, артефакты, аудит; в Public оставить агрегаты; при желании переименовать framework | Public + Private | Public/Private |
| **Phase 3** (P2) | Опционально VPS для автоматизации (issue-triggered прогоны, sync) | VPS | — |

---

## 4. ФТ-4. Детальная структура каталогов / Detailed Directory Trees

### 4.1. `mango_ba_framework` (Public) — целевое дерево

```text
mango_ba_framework/                 # (текущий mango_ba_prompts; переименование — Phase 2, опц.)
├── README.md  CHANGELOG.md  CONTRIBUTING.md  LICENSE  Makefile
├── AI_GOVERNANCE.md  .hub-profile.json
│
├── standards/                      # КАК работаем (нормативка / normative — what)
│   ├── decisions/                  # ADR (ПОЧЕМУ решили / why) — переезд из docs/adr/
│   │   ├── adr-003-ba-ontology.md  # ЕДИНАЯ нумерация adr-NNN (устранение P8)
│   │   ├── adr-004-operations-taxonomy.md
│   │   ├── ...                      # adr-005..adr-010
│   │   └── README.md               # индекс + правило нумерации
│   ├── ba-ontology.md  operation-taxonomy.md  artifact-naming-standard.md
│   ├── prompt-standard.md  pattern-standard.md  kb-standard.md
│   ├── bcreq-process-standard.md  experiment-log-standard.md
│   ├── run-contract-standard.md    # НОВЫЙ: контракт записи результатов (ФТ-7)
│   └── GLOSSARY.md
│
├── docs/                           # ОБЩАЯ документация — остаётся в корне (founder)
│   ├── taxonomy.md  kb-conversion.md
│   └── hub-research-dependencies.md   # ЕДИНСТВЕННЫЙ мост к Хабу (один bridge)
│
├── processes/                      # ОПРЕДЕЛЕНИЯ процессов (Process Definition) — НЕ результаты
│   ├── 00-index.md                 # единая матрица процесс↔паттерн↔промпт (устраняет дубли)
│   ├── multichannel-agent-processing/   # имя ПРОЦЕССА, не задачи (устранение P2)
│   │   ├── process.md              # шаги/контекст определения
│   │   ├── prompts.md              # ссылки на prompts/* (cross-link, не копия)
│   │   └── outputs.md              # ожидаемые артефакты + куда писать run
│   └── ...                         # fr-generation/ fr-validation/ glossary-understanding/ ...
│
├── prompts/                        # ИСПОЛНЯЕМЫЕ промпты (методология) — ОСТАЁТСЯ как есть
│   ├── README.md
│   ├── archive/
│   └── *.md                        # oneshot/stepwise/legacy, frontmatter-контракт
│                                   # (НЕ держим здесь experiments/ — см. §4.4)
│
├── experiments/                    # МЕТАДАННЫЕ серии Runs (гипотеза → N runs) — переопределено
│   └── EXP-YYYY-<slug>.md          # frontmatter + ссылки на runs/RUN-XXXX (в Private/Storage)
│
├── patterns/                       # паттерны БА (reusable) — как есть
│   └── <operation>/{README.md, examples/}
│
├── kb/                             # ПУБЛИЧНАЯ часть базы знаний
│   ├── README.md  USAGE.md
│   ├── sources/                    # (эволюц. → raw/, отдельной задачей; Q-вариант)
│   ├── processed/                  # (→ extracted/)
│   ├── fragments/                  # (→ curated/)
│   └── practices/
│
├── governance/                     # управление проектом — НЕ свалка
│   ├── BACKLOG.md  artifact-map.md  agent-onboarding-protocol.md
│   ├── rfc/                         # RFC спока (предложения изменений)
│   ├── decisions-log/               # rfc-register объединён сюда (устранение P11)
│   └── prompts/
│       └── hub-sync-prompt.md       # СЛУЖЕБНЫЙ промпт синхронизации (не в списке prompts/)
│
├── scripts/  site/                  # KB-извлечение, GitHub Pages — как есть
└── stats/                           # АГРЕГАТЫ прогонов из Private (success_rate, avg_rating) — Public
    └── <process>-stats.json
```

**Удаляется/мигрирует из текущего репо (Phase 0):** `docs/ba-processes/` (коллизия
→ слить `00-index.md` в `processes/00-index.md`); `docs/analysis/`,
`docs/audit/`, `governance/analysis-*`, `governance/audit-*`,
`governance/sync-matrix-*`, `governance/migration-*` → в Private (`audit/`) или в
историю PR; `governance/knowledge-transfer-to-hub/`, `rfc-to-hub-*` → заменяются
одним мостом `docs/hub-research-dependencies.md` + ручной инициацией через
`docs/rfc/`; root `experiments/*.mjs` → `scripts/` (это инструменты, не
эксперименты — устранение P6).

### 4.2. `mango_ba_operations` (Private) — целевое дерево

```text
mango_ba_operations/                # GitHub Private (бесплатно для personal; Codex-доступ)
├── README.md  CHANGELOG.md  .hub-profile.json
├── runs/                           # ГЛАВНЫЙ объект учёта — Process Run
│   └── 2026/
│       ├── RUN-0001/
│       │   ├── metadata.yaml       # run_id, process, version, date, author, model, scenario
│       │   ├── inputs/             # обезличенные/ссылки; сырьё крупное → Object Storage
│       │   ├── outputs/            # сгенерированный артефакт (ТЗ/FR/use-case)
│       │   ├── feedback/           # ревью аналитика, корректировки
│       │   └── logs/               # execution.json, токены, ошибки
│       └── RUN-0002/ ...
├── artifacts/                      # финальные коммерческие артефакты (если не в Storage)
├── audit/                          # бывшие governance/audit-* и analysis-*
└── reports/                        # сводные отчёты до агрегации в Public stats/
```

### 4.3. Object Storage (Yandex Object Storage, S3-совместимое) — «knowledge vault»

```text
s3://mango-vault/                   # доступ по аутентификации + audit доступа
├── raw/                            # PDF, DOCX, XLSX, meeting transcripts (сценарий 1, сырьё)
├── dialogs/                        # полные диалоги с внешними LLM (сценарий 2)
├── tz/                             # готовые ТЗ-артефакты (сценарий 3, коммерческие)
└── run-logs/                       # тяжёлые логи прогонов (prompt/input/output JSON)
```

### 4.4. Разделения, заложенные в дерево / Built-in Separations

- **`definition` vs `run`:** `processes/<name>/` (definition) ↔
  `runs/RUN-XXXX/` (run). Никогда не в одном каталоге (устранение P3).
- **`standards` vs `decisions`:** `standards/*.md` (как работаем) ↔
  `standards/decisions/adr-*.md` (почему решили). ADR рядом со стандартом, но
  «выше для доступа — результат (Standard), а не причина (ADR)» (решение
  фаундера). Цепочка `Анализ → RFC → ADR → Standard` сохраняется без разрастания
  подкаталогов: в `standards/decisions/` живёт только ADR, RFC остаётся в
  `docs/rfc/`.
- **`experiment` vs `run`:** Experiment (серия прогонов под гипотезу) —
  метаданные в Public `experiments/EXP-*`; Run (единичное выполнение) — в Private
  `runs/`. Семантика команды Q сохранена.

---

## 5. ФТ-5. Интеграция с экосистемой / Ecosystem Integration

### 5.1. Связь с Хабом (один мост) / One Bridge to the Hub

- **Единственный мост:** `docs/hub-research-dependencies.md` в Public-репо —
  перечень исследований Хаба, на которые опирается Mango, со ссылками. Никаких
  `sync-matrix`, `audit-hub`, `knowledge-transfer-to-hub`, `rfc-to-hub-*`
  (Вывод 1 фаундера; принцип «проекты независимы»).
- **Ручная инициация передачи опыта:** опыт спока → Хаб только через RFC,
  заводимый человеком; в споке — `docs/rfc/`, в Хабе — соответствующий
  `research/mango/` или [docs/rfc/](../../docs/rfc/README.md). Автосинхронизации нет.
- **Служебный промпт синхронизации:** `governance/prompts/hub-sync-prompt.md` —
  governance-инструмент, **не** в каталоге `prompts/` (там только БА-методология).
- Хаб остаётся источником рекомендаций, а не блокирующих правил
  ([AI_GOVERNANCE.md](../../ai-governance/ai-governance.md), [pr-ops/repo-model.md](../../pr-ops/repo-model.md)).

### 5.2. Связь с порталом `open-ai.ru` / Portal Integration (последовательно)

- Портал `open-ai.ru` — **публичный сайт**, которому на следующем этапе
  **потребуется хостинг или VPS** (неизбежно). Архитектура Mango должна быть к
  этому готова, но мы действуем **последовательно**: сначала оптимальная
  структура Mango, потом интеграция (НФТ-9).
- **Что переиспользуемо порталом из Public-контура Mango** (без переноса сейчас):
  публичные промпты (`prompts/`), стандарты (`standards/`, без `decisions/` при
  необходимости), определения процессов (`processes/`), публичная KB (`kb/`),
  агрегаты (`stats/`). Это естественный «публичный продукт» спока.
- **Готовность к хостингу:** Public-репо уже отдаёт GitHub Pages (`site/`); при
  появлении VPS портал может потреблять те же агрегаты/методологию через статичную
  публикацию или API `clarify-engine-ai` (исполняемый бэкенд). Никаких боевых
  данных Private/Storage портал не видит.

---

## 6. ФТ-6. ИБ-аспект и внешнее хранилище / Security and External Storage

### 6.1. Три уровня доступа / Three Access Tiers

| Контур | Где | Что хранит | Доступ | Обоснование ИБ |
| --- | --- | --- | --- | --- |
| **Public** | GitHub Public (`mango_ba_framework`) | методология, стандарты, процессы, промпты, публичная KB, агрегаты `stats/` | любой (read), Конард (write) | методология — публикуемый актив; данных клиентов нет |
| **Private** | GitHub Private (`mango_ba_operations`) | `runs/` (метаданные/обезличенное), feedback, артефакты, аудит | сотрудники Mango, Codex, фаундер | feedback/аудит требуют версионирования, но не публичны |
| **Confidential** | Yandex Object Storage (S3) | сырьё (PDF/DOCX), полные диалоги LLM, готовые ТЗ, тяжёлые логи | аутентификация + audit доступа | максимальный ИБ-риск и объём; бинарникам не место в Git |

### 6.2. Какие данные критичны и что выносить в Object Storage / What Goes to External Storage

Самостоятельное исследование (требование ФТ-6/НФТ): **наиболее опасная зона — не
PDF-документация и не промпты, а накопленные результаты прогонов**
`Input → Prompt → Output → Human correction → Final artifact` — фактически
**датасет обучения корпоративного аналитика** (формулировка C, поддержана Q).
Через год он ценнее всех промптов вместе взятых.

В **Yandex Object Storage** выносить:

1. **Сырьё (raw):** PDF/DOCX/XLSX документация Mango, meeting transcripts —
   крупные бинарники, не место в Git (сценарий 1).
2. **Полные диалоги с внешними LLM** — могут содержать требования, архитектуру,
   названия систем, ограничения клиента (сценарий 2).
3. **Готовые ТЗ-артефакты** — коммерческая информация (интеграции, архитектура,
   внутренние процессы клиента) (сценарий 3).
4. **Тяжёлые логи прогонов** — `{prompt, input, output}` JSON = интеллектуальная
   собственность и R&D по отладке промптов.

**Почему именно Yandex Object Storage:** S3-совместимое API (переносимость на
MinIO/другой S3), российская юрисдикция данных (релевантно для клиентских данных
Mango Office), оплата по объёму, аутентификация и audit доступа из коробки,
интеграция с будущим VPS. Альтернативы (MinIO self-hosted, Supabase, Azure Blob)
— как fallback; для первого шага Object Storage достаточно (VVS позже).

### 6.3. Что остаётся публичным / What Stays Public

Только то, что является методологией и публикуемо: стандарты, процессы, промпты,
публичная часть KB (документация с `docs.mango-office.ru`), обезличенные эталонные
кейсы (`examples/` с удалёнными реальными данными) и **агрегированная статистика**
прогонов (`{process, version, runs, success_rate, avg_rating}` вместо сырья).

---

## 7. ФТ-7. Контракт записи результатов / Result-Writing Contract

Единый контракт для всех сценариев. Норма после решения Пользователя
делегируется в `standards/run-contract-standard.md` (Public). Любой прогон создаёт
каталог `runs/RUN-XXXX/` с обязательным `metadata.yaml`:

```yaml
# runs/2026/RUN-0001/metadata.yaml
run_id: RUN-0001
process: fr-generation            # имя из processes/<name>/
version: 1.3                       # версия процесса/промпта
date: 2026-06-19
author: <analyst>
model: <provider/model>
scenario: kb-extraction | prompt-execution | artifact-generation
source_refs:                       # ссылки на сырьё в Object Storage
  - s3://mango-vault/raw/<file>
status: success | partial | failed
```

Подкаталоги (без исключений): `inputs/`, `outputs/`, `feedback/`, `logs/`.

| Сценарий | Где сохраняется результат | Метаданные | Связь с процессом |
| --- | --- | --- | --- |
| **С1. KB extraction (из PDF)** | сырьё → `s3://mango-vault/raw/`; извлечённое → Public `kb/processed`; прогон → Private `runs/RUN-XXXX/` (logs скрипта) | run_id, scenario=`kb-extraction`, source_refs на PDF | процесс извлечения в `processes/`; стандарт `kb-standard.md` |
| **С2. Prompt execution (внешняя модель)** | полный диалог → `s3://mango-vault/dialogs/`; прогон → Private `runs/RUN-XXXX/` (`inputs/`, `outputs/`, `feedback/`); агрегат → Public `stats/` | run_id, model, scenario=`prompt-execution` | промпт из `prompts/*`; серия → `experiments/EXP-*` |
| **С3. Artifact generation (через issue)** | ТЗ-артефакт → `s3://mango-vault/tz/` (коммерческое) или Private `artifacts/`; прогон → Private `runs/RUN-XXXX/`; агрегат → Public `stats/` | run_id, scenario=`artifact-generation`, ссылка на issue | процесс в `processes/<name>/outputs.md` |

Так все три сценария фаундера получают **единое место учёта (Run)** и однозначный
ответ «куда писать результат», что устраняет P4/P10.

---

## 8. ФТ-8. Фиксация проблемы токеновой инфляции / Token Inflation (Fixation Only)

> **Только фиксация. Решение — отдельная задача, зависящая от результатов этого
> RFC. По требованию фаундера здесь НЕ предлагаются разделение каталогов,
> сокращение текстов или иная оптимизация потребления токенов.**

Зафиксированный факт: в репозитории много документации, составленной как `full`
(полная, подробная), но используемой как `executable` (краткая, для LLM). Это
генерирует **перерасход токенов (token inflation)** при анализе моделью:

- одно знание может быть записано в нескольких местах (ADR → Standard → transfer
  → proposal → analysis), увеличивая retrieval noise и расход токенов (C, P16);
- обязательный frontmatter и provenance в каждом файле + длинные контракты со
  встроенным «почему» множат контекст при загрузке (G);
- полные диалоги/`experiment-log` без суммаризации раздувают контекст (G).

**Зависимость:** оптимизация документации по токенам (full vs executable,
Index/Summary/Full уровни) — следующая задача, опирающаяся на принятую здесь
структуру. Прямая аналогия с уже существующей в Хабе рамкой баланса
[docs/rfc/documentation-architecture-balance.md](../../docs/rfc/documentation-architecture-balance.md).

---

## 9. Открытые вопросы (для Пользователя) / Open Questions

1. **Когда начинать раскол Public/Private** — после Phase 0 (контракт+очистка) или
   сразу с Object Storage (Phase 1)? Рекомендация RFC: Phase 0 → Phase 1 → Phase 2.
2. **Переименовывать ли `mango_ba_prompts → mango_ba_framework`** и когда?
   Рекомендация: только на Phase 2, чтобы не ломать Pages/ссылки раньше времени.
3. **Эволюционное переименование KB** (`sources→raw`, `processed→extracted`,
   `fragments→curated`) — сейчас или отдельной задачей? Рекомендация: отдельной
   (Q-вариант, эволюционно).
4. **Object Storage:** Yandex Object Storage как первый шаг подтверждается? VPS —
   только на Phase 3 при необходимости автоматизации?
5. **Кто исполняет реструктуризацию спока** — Конард (Public) + Codex (Private)?

## 10. Definition of Done / Трассировка

| DoD пункт | Раздел RFC |
| --- | --- |
| Изучен реальный репозиторий | §1 (аудит по дереву Git) |
| Изучены 4 файла видений + таблица сравнения | §2.1–§2.2 |
| Независимое решение по структуре | §3.2 (Вариант B, фазово) |
| Дерево каталогов для каждого репо/хранилища | §4.1–§4.3 |
| Интеграция с экосистемой (Hub один мост, open-ai.ru) | §5 |
| ИБ-аспект (public/private/confidential) | §6.1 |
| Исследование внешнего хранилища (Yandex Object Storage) | §6.2 |
| Портал open-ai.ru (последовательно) | §5.2 |
| Контракт записи для 3 сценариев | §7 |
| Фиксация токеновой инфляции (без оптимизации) | §8 |
| Двуязычные термины (RU + EN) | весь документ |

## Источники / Sources

- Дерево `G-Ivan-A/mango_ba_prompts@main` (снимок 2026-06-19).
- 4 видения: команды C, Q, G, фаундера (вложения issue
  [#253](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/253)).
- Hub-контекст: [pr-ops/repo-model.md](../../pr-ops/repo-model.md) (Anti-Inflation),
  [docs/rfc/README.md](../../docs/rfc/README.md) (статус RFC),
  [research/mango/README.md](README.md),
  [projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md](../../projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md),
  [docs/project-summaries/mango-ba-prompts-context-Summary.md](../../docs/project-summaries/mango-ba-prompts-context-Summary.md).
