---
status: draft
version: 0.1
updated: 2026-06-05
ai-generated: true
executable: false
scope: repo-wide
related_standards:
  - "PROJECT_STRUCTURE_INHERITANCE.md"
  - "FILE_NAMING.md"
  - "RESEARCH_PROFILE.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/159"
---

# Portal Repository Structure

Версия: 0.1

Дата: 2026-06-05

Статус: **черновик стандарта (`draft`)**, предложен на утверждение фаундеру (см.
RFC [governance/proposals/open-ai-portal-concept-rfc.md](../governance/proposals/open-ai-portal-concept-rfc.md),
§14). До утверждения — рекомендация, не обязательное правило. Принятие стандарта
как обязательного для порталов — решение человека (AI_GOVERNANCE, правило 4).

## Назначение

Стандарт описывает структуру репозитория **портала** — особого класса
spoke-проекта, который служит «единой точкой сборки» (витриной и инструментом
коммуникации) нескольких spoke-проектов экосистемы Хаба. Первый кандидат —
`open-ai.ru`.

Стандарт **наследует** геном спока (`templates/spoke/`) и принципы
[standards/PROJECT_STRUCTURE_INHERITANCE.md](PROJECT_STRUCTURE_INHERITANCE.md), и
**добавляет** портал-специфичные каталоги. Он не вводит обязательных
зависимостей для других споков (портал-каталоги опциональны и создаются по
операционной потребности — Anti-Inflation).

Обоснование структуры и альтернативы: [research/portal/repository-structure-design-2026-06.md](../research/portal/repository-structure-design-2026-06.md).

## Когда применять

Репозиторий — портал (а не обычный спок или каталог в `/projects`), если
выполнены критерии spoke-репозитория из [projects/README.md](../projects/README.md)
**И** проект играет роль витрины/точки сборки нескольких проектов:

| Признак портала | Пояснение |
| --- | --- |
| Production-код | Свой деплой, публичный сайт. |
| Своя команда / долгий жизненный цикл | Не разовый артефакт. |
| Витрина ≥2 проектов | Связывает/показывает spoke-проекты (Reputation Engineering, BA Prompts, …). |
| Коммуникационная роль | Презентации, коллаборации, обучение, база знаний. |

Если проект не витринирует другие проекты — это обычный спок (`templates/spoke/`),
а не портал.

## Дерево каталогов

```text
<portal>/                            # spoke-репозиторий портала (напр. open-ai.ru)
├── README.md                        # [наследие] визитка + связь с Хабом
├── AI_GOVERNANCE.md                 # [наследие] конституция спока
├── AI_QUICK_RULES.md                # [наследие] правила для AI-агента
├── AI_HANDOVER_PROMPT.md            # [наследие] runtime-онбординг агента
├── CONTRIBUTING.md                  # [наследие] workflow вклада (issue → PR → review)
├── CHANGELOG.md                     # [наследие] журнал изменений
├── docs/
│   ├── adr/                         # [наследие] Architecture Decision Records
│   ├── audit/                       # [наследие] ревизии и аудиты
│   └── architecture.md              # [расширение] C4-обзор (Mermaid) — опц.
├── .github/ISSUE_TEMPLATE/          # [наследие] шаблон задач
├── tools/                           # [наследие] валидатор-«иммунная система»
├── projects/                        # [портал] витрина/модули spoke-проектов
│   └── <project>/                   #          карточка, ссылки, демо проекта
├── presentations/                   # [портал] презентации, демо, публичные материалы
├── collaborations/                  # [портал] координация с командами/партнёрами
├── learning/                        # [портал] обучение пользователей (Diátaxis)
├── knowledge-base/                  # [портал] FAQ, интеграционные гайды
└── src/                             # [код] исходники портала (конвенция фреймворка)
```

Каталоги создаются **по мере появления операционной боли**. Портал не носит
пустые «органеллы»: например, `collaborations/` появляется, когда есть первая
реальная коллаборация.

## Назначение каталогов

| Каталог | Слой | Назначение |
| --- | --- | --- |
| `docs/adr/` | наследие | Записи решений: контекст → решение → последствия. |
| `docs/audit/` | наследие | Ревизии соответствия, аудиты. |
| `docs/architecture.md` | расширение | Обзор архитектуры портала (C4 через Mermaid). |
| `projects/` | портал | По подкаталогу на витринируемый проект: карточка, ссылки на его spoke-репозиторий, демо. Портал **связывает**, а не поглощает чужой код. |
| `presentations/` | портал | Презентации, демо-материалы, публичные выступления. |
| `collaborations/` | портал | Артефакты координации с командами/партнёрами проектов. |
| `learning/` | портал | Обучающие материалы для пользователей портала (структура — Diátaxis: tutorials/how-to/reference/explanation). |
| `knowledge-base/` | портал | FAQ, интеграционные гайды, справочник. |
| `src/` | код | Исходный код портала по конвенции выбранного фреймворка. |

## Обязательные файлы (governance, наследуются от спока)

Портал **обязан** содержать полный геном спока (`templates/spoke/`):

| Файл | Роль |
| --- | --- |
| `README.md` | Визитка + связь с Хабом (источник истины). |
| `AI_GOVERNANCE.md` | Операционный контракт: роли, правила, эскалация, DoD. |
| `AI_QUICK_RULES.md` | Одностраничные правила для AI-агента. |
| `AI_HANDOVER_PROMPT.md` | Handover Prompt для запуска агента (Кейс 1). |
| `CONTRIBUTING.md` | Workflow вклада. |
| `CHANGELOG.md` | Журнал значимых изменений. |
| `docs/adr/` | ADR (каталог решений). |
| `docs/audit/` | Аудиты. |
| `.github/ISSUE_TEMPLATE/` | Шаблон постановки задач. |
| `tools/validate-repository-structure.sh` | Локальный структурный валидатор. |

Все `.md`-файлы несут обязательный frontmatter Хаба
(`status`, `version`, `updated`, `ai-generated`; опц. `executable`, `entrypoint`).

## Опциональные файлы и каталоги (портал-специфичные)

Создаются по потребности; не являются зависимостью для других споков:

- `docs/architecture.md` — обзор C4 (когда портал перерастает «несколько ADR»).
- `projects/<project>/` — по витринируемому проекту.
- `presentations/`, `collaborations/`, `learning/`, `knowledge-base/` — по мере
  появления реального контента.
- `src/` — при старте реализации (вне рамок research-стадии).

## Принципы наследования от Хаба

1. **Геном спока — в корне.** Портал рождается из `templates/spoke/` (через
   `init.sh`) и сохраняет весь обязательный набор.
2. **Хаб — источник истины.** Governance, стандарты и фундаментальные знания
   живут в Хабе; в споке `research/` **не создаётся** (см. `templates/spoke/README.md`).
3. **Frontmatter и lifecycle.** Те же `status/version/updated/ai-generated` и
   правила именования ([FILE_NAMING.md](FILE_NAMING.md)).
4. **Иммунная система.** Свой `tools/validate-repository-structure.sh`,
   проверяемый перед каждым PR (Definition of Done).
5. **Anti-Inflation.** Каталог создаётся, только когда снижает реальную боль.

## Принципы расширения для порталов

1. **Расширение, не подмена.** Портал-каталоги добавляются *поверх* генома, не
   заменяя его.
2. **Витрина связывает, не поглощает.** `projects/<project>/` ссылается на
   spoke-репозиторий проекта (hub-and-spoke), храня лишь карточку/демо. Реальный
   production-код проекта живёт в его собственном репозитории.
3. **Без обязательных зависимостей.** Наличие портал-каталогов не обязывает
   другие споки их повторять (наследует
   [PROJECT_STRUCTURE_INHERITANCE.md](PROJECT_STRUCTURE_INHERITANCE.md)).
4. **Стандарт repo-wide не ссылается на проект.** Во избежание циклов этот
   стандарт описывает *класс* порталов, а не конкретный `open-ai.ru`.
5. **Приватность.** Секреты, реальные клиентские данные и несанитизированные
   production-промпты **не коммитятся** (AI_GOVERNANCE, правило 6); AI-ключи —
   только через серверный proxy, не на клиенте.

## Примеры использования

### Пример 1. Минимальный портал (Phase 0)

```text
open-ai.ru/
├── README.md, AI_GOVERNANCE.md, AI_QUICK_RULES.md, AI_HANDOVER_PROMPT.md
├── CONTRIBUTING.md, CHANGELOG.md
├── docs/adr/, docs/audit/
├── .github/ISSUE_TEMPLATE/
├── tools/
└── src/                  # лендинг (SSG)
```

### Пример 2. Портал с витриной 2 проектов (Phase 1)

```text
open-ai.ru/
├── … (геном спока) …
├── docs/architecture.md          # C4-обзор
├── projects/
│   ├── reputation-engineering/   # карточка + ссылка на spoke
│   └── ba-prompts/               # карточка + демо инструмента (остров)
├── learning/                     # онбординг пользователей
└── knowledge-base/               # FAQ, гайды
```

## Гайд по миграции существующего `open-ai.ru`

Обобщённый путь (точная структура текущего сайта не предполагается):

1. **Инвентаризация.** Зафиксировать текущее содержимое и деплой `open-ai.ru`.
2. **Привить геном спока.** Добавить обязательные governance-файлы (можно через
   `templates/spoke/init.sh` в отдельной ветке) **без** удаления рабочего кода.
3. **Внести `tools/validate-repository-structure.sh`** и адаптировать allowlist
   под реальные файлы портала.
4. **Разложить контент по портал-каталогам.** Перенести существующие материалы в
   `projects/`, `presentations/`, `learning/`, `knowledge-base/` по смыслу.
5. **Документировать решения.** Завести `docs/adr/` и зафиксировать ключевые
   решения миграции; при необходимости — `docs/architecture.md` (C4).
6. **Связать с Хабом.** В `README.md` указать Хаб как источник истины; добавить
   ссылки на витринируемые проекты.
7. **Прогнать валидатор** до зелёного и открыть PR (малыми шагами).

> Миграция — отдельная инициатива; этот стандарт описывает целевую структуру, а
> *решение* мигрировать и его сроки — за фаундером (RFC §12, §14).

## Проверка соответствия

- Геном спока на месте? → иначе это не валидный портал-спок.
- Портал-каталог создан без реальной потребности? → удалить (Anti-Inflation).
- `projects/<project>/` содержит чужой production-код вместо ссылки? → вынести в
  его spoke-репозиторий.
- В репозитории есть секреты/реальные клиентские данные? → отклонить (правило 6).
- Этот стандарт ссылается на конкретный портал? → исправить (repo-wide ≠ проект).

## Источники

- [standards/PROJECT_STRUCTURE_INHERITANCE.md](PROJECT_STRUCTURE_INHERITANCE.md) — родительский принцип наследования.
- [standards/FILE_NAMING.md](FILE_NAMING.md) — правила именования.
- [templates/spoke/README.md](../templates/spoke/README.md) — геном спока.
- [projects/README.md](../projects/README.md) — критерии spoke vs `/projects`.
- [governance/REPO_MODEL.md](../governance/REPO_MODEL.md) — Anti-Inflation, размещение артефактов.
- [AI_GOVERNANCE.md](../AI_GOVERNANCE.md) — правила 4 и 6.
- [research/portal/repository-structure-design-2026-06.md](../research/portal/repository-structure-design-2026-06.md) — обоснование и альтернативы.
- [research/portal/documentation-standards-comparison-2026-06.md](../research/portal/documentation-standards-comparison-2026-06.md) — ADR + C4 + Diátaxis.
