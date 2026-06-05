---
status: draft
version: 0.1
updated: 2026-06-05
ai-generated: true
type: internal-analysis
context: [portal, repository-structure, hub-and-spoke, governance-inheritance, spoke-template]
method: comparative-analysis
scope: portal
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/159"
related_artifacts:
  - "research/portal/architecture-and-stack-comparison-2026-06.md"
  - "standards/PORTAL_REPOSITORY_STRUCTURE.md"
  - "standards/PROJECT_STRUCTURE_INHERITANCE.md"
  - "templates/spoke/README.md"
  - "projects/README.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/159"
---

# Исследование 3: Дизайн структуры репозитория портала open-ai.ru

Версия: 0.1

Дата: 2026-06-05

Статус: черновик исследования (`draft`). Выход — проект стандарта
[standards/PORTAL_REPOSITORY_STRUCTURE.md](../../standards/PORTAL_REPOSITORY_STRUCTURE.md);
утверждение стандарта — за человеком.

## Вопрос, гипотеза, метод

| Поле | Значение |
| --- | --- |
| **Вопрос** | Какой должна быть структура репозитория портала `open-ai.ru`, чтобы наследовать governance Хаба и при этом поддержать роль «единой точки сборки» 10+ проектов? |
| **Гипотеза** | Портал — это **spoke-репозиторий** (production-код, своя команда, долгий жизненный цикл) по критериям [projects/README.md](../../projects/README.md); значит, его структура = геном спока (`templates/spoke/`) **плюс** портал-специфичные каталоги, оформленные новым наследующим стандартом, а не новый каталог в `/projects` Хаба. |
| **Метод** | Внутренний анализ (`internal-analysis`) структуры Хаба, генома спока и правил наследования; сравнение 3 альтернатив размещения; вывод в стандарт. |
| **Критерий успеха** | Выбрана структура, каждое её решение трассируется к существующему правилу Хаба (`REPO_MODEL`, `PROJECT_STRUCTURE_INHERITANCE`, `FILE_NAMING`, спок-шаблон). |
| **Ограничения** | Структура существующего `open-ai.ru` неизвестна детально → migration-план в стандарте даёт обобщённый путь адаптации. |

## Часть 1. Анализ структуры Хаба

Ключевые факты (из чтения репозитория):

| Элемент Хаба | Что задаёт | Источник |
| --- | --- | --- |
| **Модель hub-and-spoke** | Хаб — governance-knowledge-hub, **не** production-кодовая база; production-код живёт в spoke-репозиториях. | [CONCEPT.md](../../CONCEPT.md), [governance/REPO_MODEL.md](../../governance/REPO_MODEL.md) |
| **Критерии spoke vs `/projects`** | Отдельный spoke-репозиторий, если: production-код, своя команда, закрытый контекст, долгий жизненный цикл. Иначе — каталог в `/projects`. | [projects/README.md](../../projects/README.md) |
| **Геном спока (`templates/spoke/`)** | Минимальный обязательный набор: `AI_GOVERNANCE.md`, `AI_QUICK_RULES.md`, `AI_HANDOVER_PROMPT.md`, `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `docs/adr/`, `docs/audit/`, `.github/ISSUE_TEMPLATE/`, `tools/`, `init.sh`. **Без `research/`** (фундаментальные знания живут в Хабе). | [templates/spoke/README.md](../../templates/spoke/README.md) |
| **Наследование структуры** | Проекты создают подкаталоги итеративно, наследуя правила, **без обязательных зависимостей** для других; явная метка `scope`. | [standards/PROJECT_STRUCTURE_INHERITANCE.md](../../standards/PROJECT_STRUCTURE_INHERITANCE.md) |
| **Anti-Inflation** | Артефакт создаётся, только когда снижает операционную боль; не плодить пустые каталоги. | [governance/REPO_MODEL.md](../../governance/REPO_MODEL.md) |
| **Именование** | Корень спока — `UPPERCASE_WITH_HYPHENS.md`; вложенные — `lowercase-with-hyphens.md`. | [standards/FILE_NAMING.md](../../standards/FILE_NAMING.md) |
| **Иммунная система** | Спок несёт собственный `tools/validate-repository-structure.sh`. | [templates/spoke/tools/validate-repository-structure.sh](../../templates/spoke/tools/validate-repository-structure.sh) |

**Вывод части 1:** Хаб уже предоставляет всё для рождения нового спока
(`templates/spoke/` + `init.sh`). Чего **нет** — расширения генома под класс
«портал»: каталогов для витрины проектов, презентаций, коллабораций, обучения и
базы знаний.

## Часть 2. Требования портала к структуре

Из issue #159 и роли «инструмент коммуникации / точка сборки»:

| Требование | Структурное следствие |
| --- | --- |
| Витрина 2–3 проектов в Phase 1 → 10+ позже | Каталог `projects/` внутри портала — по модулю/витрине на проект. |
| Публичные презентации, демо, материалы | Каталог `presentations/`. |
| Координация с командами/партнёрами проектов | Каталог `collaborations/`. |
| Обучение пользователей портала (онбординг, гайды) | Каталог `learning/` (Diátaxis — см. Исследование 1). |
| База знаний (FAQ, интеграционные гайды) | Каталог `knowledge-base/`. |
| Production-код портала (Astro/Angular/Next) | Каталог `src/` (по конвенции фреймворка). |
| Наследовать governance Хаба | Полный геном спока в корне. |
| Документация архитектуры | `docs/adr/` (ADR) + `docs/architecture.md` (C4) — см. Исследование 1. |

## Часть 3. Альтернативы размещения

| Вариант | Описание | Плюсы | Минусы | Вердикт |
| --- | --- | --- | --- | --- |
| **A. Каталог в Хабе** (`projects/open-ai-portal/`) | Портал живёт внутри Хаба. | Просто, всё в одном месте. | Нарушает критерии: портал = production-код + своя команда + долгий цикл → должен быть споком. Раздувает Хаб production-кодом (anti-pattern по CONCEPT). | 🔴 Отклонить |
| **B. Спок «как есть»** (`templates/spoke/` без расширений) | Клонировать геном спока, портал-каталоги создавать ad-hoc. | Не нужен новый стандарт. | Нет единого правила для порталов → каждый портал изобретает структуру; теряется консистентность и наследование при росте до 10+ проектов. | 🟡 Частично |
| **C. Спок + стандарт-расширение** (`PORTAL_REPOSITORY_STRUCTURE.md`) | Геном спока **плюс** наследующий стандарт с портал-каталогами (`projects/`, `presentations/`, `collaborations/`, `learning/`, `knowledge-base/`). | Наследует весь governance Хаба; единое, переиспользуемое правило для класса «портал»; масштабируется; trace к `PROJECT_STRUCTURE_INHERITANCE`. | Нужен новый стандарт (но это и есть deliverable issue #159; comparison закрывает эскалацию AI_GOVERNANCE). | 🟢 **Выбрать** |

## Часть 4. Выбранная структура (обоснование)

**Портал = spoke-репозиторий, рождённый из `templates/spoke/`, расширенный
стандартом `PORTAL_REPOSITORY_STRUCTURE.md`.**

```text
open-ai.ru/                         # spoke-репозиторий портала
├── README.md                       # [наследие] визитка + связь с Хабом
├── AI_GOVERNANCE.md                # [наследие] конституция спока
├── AI_QUICK_RULES.md               # [наследие] правила выживания агента
├── AI_HANDOVER_PROMPT.md           # [наследие] runtime-онбординг
├── CONTRIBUTING.md                 # [наследие] workflow вклада
├── CHANGELOG.md                    # [наследие] журнал
├── docs/
│   ├── adr/                        # [наследие] ADR (стандарт документации, Иссл. 1)
│   ├── audit/                      # [наследие] аудиты
│   └── architecture.md             # [расширение] C4-обзор (Mermaid)
├── .github/ISSUE_TEMPLATE/         # [наследие] шаблон задач
├── tools/                          # [наследие] валидатор-«иммунная система»
├── projects/                       # [портал] витрина/модули spoke-проектов
│   ├── reputation-engineering/
│   └── ba-prompts/
├── presentations/                  # [портал] презентации, демо, публичные материалы
├── collaborations/                 # [портал] координация с командами/партнёрами
├── learning/                       # [портал] обучение пользователей (Diátaxis)
├── knowledge-base/                 # [портал] FAQ, интеграционные гайды
└── src/                            # [код] исходники портала (конвенция фреймворка)
```

**Трассировка решений:**

- Портал — спок → критерии [projects/README.md](../../projects/README.md)
  (production-код, своя команда, долгий цикл).
- Геном в корне → [templates/spoke/README.md](../../templates/spoke/README.md).
- Портал-каталоги как итеративное расширение **без** обязательных зависимостей
  для других споков → принцип [standards/PROJECT_STRUCTURE_INHERITANCE.md](../../standards/PROJECT_STRUCTURE_INHERITANCE.md).
- `docs/adr/` + `docs/architecture.md` → стандарт документации Исследования 1.
- `learning/` структурируется по Diátaxis → Исследование 1.
- Каждый портал-каталог создаётся по мере реальной потребности → Anti-Inflation,
  [governance/REPO_MODEL.md](../../governance/REPO_MODEL.md).

## Часть 5. Связь со стандартом

Этот дизайн материализован в проекте стандарта
[standards/PORTAL_REPOSITORY_STRUCTURE.md](../../standards/PORTAL_REPOSITORY_STRUCTURE.md),
который описывает: дерево каталогов, назначение каждого каталога, обязательные
(governance) и опциональные (портал-специфичные) файлы, принципы наследования от
Хаба, принципы расширения для порталов, примеры использования и migration-гайд
для адаптации существующего `open-ai.ru`.

## Решение за человеком

Структура и стандарт рекомендованы; утверждение стандарта как обязательного для
порталов — за фаундером (RFC, §14). Эскалация AI_GOVERNANCE «нужен новый
обязательный standard, но нет comparison» закрыта этим исследованием +
Исследованием 1.

### Вопросы для согласования

1. Принять вариант **C** (спок + стандарт-расширение) как канон для порталов?
2. Имена портал-каталогов (`projects/`, `presentations/`, `collaborations/`,
   `learning/`, `knowledge-base/`) — финальные, или скорректировать?
3. Витрина проектов: портал **ссылается** на их репозитории (рекомендация,
   hub-and-spoke) или **содержит** их код? (Рекомендация: ссылается +
   карточка/демо.)

## Источники (внутренние)

- [CONCEPT.md](../../CONCEPT.md) — модель hub-and-spoke, границы Хаба.
- [governance/REPO_MODEL.md](../../governance/REPO_MODEL.md) — размещение артефактов, Anti-Inflation.
- [projects/README.md](../../projects/README.md) — критерии spoke vs `/projects`.
- [standards/PROJECT_STRUCTURE_INHERITANCE.md](../../standards/PROJECT_STRUCTURE_INHERITANCE.md) — наследование структуры.
- [standards/FILE_NAMING.md](../../standards/FILE_NAMING.md) — именование.
- [templates/spoke/README.md](../../templates/spoke/README.md) — геном спока.
- [projects/mango/README.md](../../projects/mango/README.md) — пример прикладного спок-проекта.
