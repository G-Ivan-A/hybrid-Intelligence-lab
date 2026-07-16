---
status: draft
version: 0.1
updated: 2026-06-02
temperature: 0.1
type: external-analysis
context: [governance, hub, external-patterns, agent-ecosystems, applicability-matrix]
method: comparative-analysis
scope: repo-wide
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/101"
related_artifacts:
  - "ai-rules/agent-onboarding-protocol.md"
  - "docs/rfc/rfc-two-cases-of-project-initialization.md"
  - "research/hub/2026-06-02-ai-collaboration-retrospective.md"
  - "research/hub/2026-06-01-team-c-governance-strategy-audit.md"
  - "standards/glossary.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/101"
---

# Анализ external governance patterns и матрица применимости для Хаба

Документ остается черновиком исследования (`draft`). Перевод в `reviewed` и решения по
внедрению — за человеком (см. раздел «Решение за человеком»).

> В этом документе используются термины из
> [standards/glossary.md](../../standards/glossary.md): *Operating Mode*,
> *Policy*, *Standard*, *Practice*, *Artifact*, *Canonical*, *Draft*,
> *Bootstrap-клонирование*, *Runtime-онбординг*. Два новых рабочих термина —
> **North Star** и **Триггер внедрения** — добавлены в глоссарий в рамках этой
> задачи, чтобы они имели единый источник истины, а не жили только здесь.

---

## 1. Введение

### 1.1. Зачем проведён review

В рамках проектирования протокола онбординга ИИ-агента
([ai-rules/agent-onboarding-protocol.md](../../ai-rules/agent-onboarding-protocol.md))
внешняя экспертная группа (далее — **Команда С**) выполнила архитектурный review
дизайна через призму emerging governance-паттернов в agent ecosystems. Цель
этого файла — зафиксировать рекомендации Команды С как **исследовательский
артефакт** (`Artifact`, см. глоссарий) и предложить матрицу применимости, которая
отвечает на один вопрос: *что брать сейчас, что отложить и что отклонить*, не
перегружая текущую реализацию.

Принцип фильтрации всего документа — **«практика первична, документация растёт
по факту боли»**. Это прямое следствие Anti-Inflation principle
([pr-ops/repo-model.md](../../pr-ops/repo-model.md)) и вывода аудита
Команды С: «нет governance-артефакта без операционной боли»
([research/hub/2026-06-01-team-c-governance-strategy-audit.md](2026-06-01-team-c-governance-strategy-audit.md)).

### 1.2. Источники, на которые ссылается Команда С

| Код | Источник | Краткое описание (по позиционированию источника) |
| --- | --- | --- |
| `[GAP]` | [GitAgent Protocol (Open GAP)](https://www.gitagent.sh/) | Открытый стандарт для git-native AI-агентов: governance и провенанс действий агента поверх git. |
| `[EGA]` | [EGAProtocol (5AG Governance Model)](https://egaprotocol.org/) | Открытый governance-протокол для AI-агентов: модель управления жизненным циклом и доверием. |
| `[AID]` | [AgentID Draft (IETF)](https://datatracker.ietf.org/doc/html/draft-gudlab-agentid-protocol-00) | Черновик стандарта идентичности агента (agent identity) в рамках IETF. |

> ⚖️ **Граница анализа (юридически точно).** Это не независимая внешняя
> валидация рынка или указанных стандартов. Источники `[GAP]`, `[EGA]`, `[AID]`
> приведены **так, как на них ссылается Команда С**, и используются как
> *контекст* её рекомендаций, а не как проверенные мной факты. Их зрелость,
> статус и точные формулировки требуют отдельной верификации до любого
> внедрения. Эта оговорка повторяет границу, уже принятую в
> [2026-06-01-team-c-governance-strategy-audit.md](2026-06-01-team-c-governance-strategy-audit.md)
> (раздел «Назначение»), и соблюдает принцип «не выдумывать несуществующий
> источник» из
> [ai-rules/agent-onboarding-protocol.md](../../ai-rules/agent-onboarding-protocol.md).

### 1.3. Ключевые выводы Команды С (сводка)

| # | Вывод Команды С | Код |
| --- | --- | --- |
| `[C1]` | Проект движется в правильном направлении: governance-first architecture, а не agent framework. | — |
| `[C2]` | Git-native governance — сильный архитектурный выбор. | `[GAP]` |
| `[C3]` | Есть зачаток formal trust lifecycle. | `[EGA]` |
| `[C4]` | Сильный фокус на anti-drift (защита от дрейфа стандартов). | — |
| `[C5]` | Выявлено 6 критических архитектурных gaps: identity model, capability model, fail-closed semantics, threat model, approval semantics, evidence model. | `[GAP]`, `[EGA]`, `[AID]` |
| `[C6]` | Стратегический вывод: проект может стать *early governance substrate for auditable agent ecosystems*, а не «очередным AI-agent framework». | — |

### 1.4. Текущее состояние Хаба (контекст фильтрации)

Рекомендации Команды С описывают **целевое состояние** production-grade agent
infrastructure. Фактическое состояние Хаба на дату документа иное:

- один пользователь (Founder & PO);
- 3 проекта в горизонте месяца (`mango_ba_prompts`, `portal`, `vector-core`);
- `templates/htom/` создан как геном, но ни один спок ещё не клонирован
  (`Bootstrap-клонирование` пока не выполнялось на реальном проекте);
- нет ни одного реального кейса работы внешнего агента в `Runtime-онбординге`.

Отсюда главный риск: внедрить всё сразу — значит «убить проект под весом
governance-машины» (classic enterprise-architecture-astronaut anti-pattern;
ср. риск *Premature enterprise architecture* в
[2026-06-01-team-c-governance-strategy-audit.md](2026-06-01-team-c-governance-strategy-audit.md)).

---

## 2. Что ценного в рекомендациях Команды С

Таблица фиксирует ценные идеи (минимум 8). Колонка «Источник» обеспечивает
трассируемость: каждая строка ссылается либо на вывод Команды С (`[C#]`), либо
на внешний стандарт (`[GAP]`/`[EGA]`/`[AID]`).

| Идея | Суть | Почему ценно | Источник |
| --- | --- | --- | --- |
| Fail-closed semantics | DENY BY DEFAULT: что не разрешено явно — запрещено. | Защита от галлюцинаций агента: при неопределённости агент останавливается, а не действует. | `[C5]`, `[EGA]` |
| Capability taxonomy | Явный список разрешённых действий агента. | Ясность границ: агент знает, что можно без спроса, что — с апрувом, что — никогда. | `[C5]`, `[GAP]` |
| Threat model | Список рисков и сценариев злоупотребления. | Awareness *до* старта: риски названы, а не обнаруживаются постфактум. | `[C5]` |
| Evidence model | Git history + issues + PRs как след доказательств. | У нас это **уже есть** — нужно лишь назвать явно как evidence trail. | `[C5]`, `[GAP]` |
| Approval semantics | Кто, когда и что утвердил. | Трассируемость решений: апрув перестаёт быть устным. | `[C5]`, `[EGA]` |
| Formal state machine | `UNREGISTERED → … → REVOKED` как жизненный цикл агента. | Масштабируемость на 3+ агента, где нужен формальный trust lifecycle. | `[C3]`, `[EGA]` |
| Signed onboarding artifacts | Криптографическая верификация артефактов онбординга. | Enterprise compliance: доказуемая подлинность для внешнего аудита. | `[AID]` |
| Delegation chain | Агент делегирует задачу агенту с сохранением цепочки. | Основа multi-agent оркестрации с прослеживаемой ответственностью. | `[C5]`, `[GAP]` |

---

## 3. Матрица применимости

Матрица — ядро документа. Три колонки соответствуют трём решениям: **взять
сейчас**, **отложить**, **отклонить**. Каждая строка трассируется к идее из
раздела 2 и к источнику. «Куда встроить» указывает *целевой* артефакт; сами
файлы улучшений в этой задаче **не создаются** (см. ограничение Anti-Inflation в
разделе 6).

### 3.1. ВЗЯТЬ СЕЙЧАС (бесплатно, без усложнения)

Критерий: идея реализуется одной формулировкой или одним полем, не добавляет
машинерии и снижает риск уже сегодня.

| Идея | Как взять | Куда встроить (целевой артефакт) | Источник |
| --- | --- | --- | --- |
| Fail-closed semantics | Одна фраза: «Если действие не описано в контракте — агент не выполняет, а запрашивает human review». Операционно это уже заложено в Шаг 4 (стоп до апрува) протокола онбординга. | `templates/htom/AI_QUICK_RULES.md` | `[C5]`, `[EGA]` |
| Capability taxonomy (простая) | Ментальный список из трёх корзин: «можно без спроса», «можно с апрувом», «никогда». Без YAML, в прозе. | `templates/htom/AI_GOVERNANCE.md` | `[C5]`, `[GAP]` |
| Threat awareness | Раздел «Что может пойти не так»: 3–5 рисков в человекочитаемом виде. | `ai-rules/agent-onboarding-protocol.md` (проектируется в RFC онбординга) | `[C5]` |
| Evidence model (назвать явно) | Зафиксировать тезис: «git history + issues + PRs = evidence trail». Функция уже есть — нужно дать ей имя. | RFC-манифест `docs/rfc/rfc-two-cases-of-project-initialization.md` | `[C5]`, `[GAP]` |
| Approval semantics (простые) | Поле `approved_by:` во frontmatter критичных файлов как явный след апрува. | `standards/file-naming.md` | `[C5]`, `[EGA]` |

### 3.2. ОТЛОЖИТЬ (взять, когда появится боль)

Критерий: идея ценна, но её стоимость оправдана только при конкретном триггере.
До триггера — не внедряем.

| Идея | Триггер для внедрения | Источник |
| --- | --- | --- |
| Formal state machine (`UNREGISTERED → REVOKED`) | 3+ агента одновременно работают с одним репо → коллизии состояний. | `[C3]`, `[EGA]` |
| Capability Manifest (YAML, машиночитаемый) | Первый инцидент: агент сделал то, что не должен был. | `[C5]`, `[GAP]` |
| Signed onboarding artifacts | Первое требование compliance от партнёра/клиента. | `[AID]` |
| Delegation chain | Появится реальная multi-agent оркестрация. | `[C5]`, `[GAP]` |
| Approval TTL / replay policy | Первый инцидент replay-атаки или применение устаревшего approval. | `[EGA]`, `[AID]` |
| OpenTelemetry traces | Первый серьёзный failure, где нужно восстановить chain of events. | `[GAP]` |

### 3.3. ОТКЛОНИТЬ (или радикально упростить)

Критерий: для текущей реальности (один пользователь, локальные репо, git как
источник истины) идея дублирует существующую функцию или решает несуществующую
проблему.

| Идея | Почему не подходит сейчас | Источник |
| --- | --- | --- |
| Cryptographic agent identity | Один пользователь, один агент, локальные репо — проблемы spoofing нет. Радикальное упрощение: identity = git author + апрув человека. | `[AID]` |
| Governance Metadata Envelope (JSON) | Взаимодействие human-to-agent: достаточно markdown + git, JSON-обёртка добавляет машинерию без потребителя. | `[GAP]`, `[EGA]` |
| Hash-chained events | Git уже даёт immutable history — это дублирование функции. | `[GAP]` |
| Multi-party approval | Единственный владелец принимает решения — кворум не нужен. | `[EGA]` |

---

## 4. North Star проекта

> **North Star** (см. глоссарий): «Проект движется в сторону
> **governance-grade provenance-aware hybrid intelligence infrastructure** — не
> очередной AI-agent framework, а *early governance substrate for auditable
> agent ecosystems*».

Обоснование (трассируется к выводу `[C6]` Команды С):

- **Рынок orchestration переполнён.** Конкурировать фреймворком оркестрации —
  значит выходить на занятый рынок поздно.
- **Рынок governance / provenance / trust lifecycle / auditability только
  формируется.** Здесь есть незанятая ниша.
- **У Хаба есть актив early mover:** git-native governance (`[C2]`), зачаток
  trust lifecycle (`[C3]`) и фокус на anti-drift (`[C4]`) — это и есть фундамент
  «governance substrate», а не ещё один agent framework.

North Star не отменяет принцип фильтрации: он задаёт *направление*, а матрица
раздела 3 задаёт *темп*. Двигаться к North Star нужно по факту боли, а не по
факту красоты целевой архитектуры.

---

## 5. Триггеры для пересмотра матрицы

Условия, при наступлении любого из которых нужно вернуться к разделу 3 и
пересмотреть строки «Отложить»/«Отклонить» (минимум 5; см. термин **Триггер
внедрения** в глоссарии):

- [ ] Появится **3+ активных spoke-проекта** одновременно (риск коллизий →
      пересмотреть Formal state machine).
- [ ] Появится **команда > 2 человек** (риск размытой ответственности →
      пересмотреть Approval semantics и multi-party approval).
- [ ] **Первый инцидент безопасности**: агент выполнил несанкционированное
      действие (→ Capability Manifest, fail-closed как жёсткое Policy).
- [ ] **Первое требование compliance** от внешнего партнёра/клиента (→ Signed
      onboarding artifacts, agent identity).
- [ ] Появится **multi-agent оркестрация** (→ Delegation chain, OpenTelemetry
      traces).
- [ ] **Первый replay-инцидент** или применение устаревшего approval (→ Approval
      TTL / replay policy).

При срабатывании триггера: создаётся issue со ссылкой на эту строку матрицы и на
источник идеи (маршрут «идея → задача» из
[ai-rules/agent-onboarding-protocol.md](../../ai-rules/agent-onboarding-protocol.md)).

---

## 6. Ограничения

- Документ **не создаёт** файлы улучшений (`AI_QUICK_RULES.md`,
  `AI_GOVERNANCE.md`, `agent-onboarding-protocol.md` и т.д.). Колонка «Куда встроить» в
  разделе 3 — это *проект* интеграции, физическое внедрение «бесплатных»
  улучшений выполняется отдельными задачами (Anti-Inflation principle).
- Внешние источники `[GAP]`, `[EGA]`, `[AID]` не верифицированы независимо (см.
  «Граница анализа» в разделе 1.2) и используются как контекст рекомендаций
  Команды С.
- Матрица отражает состояние Хаба на 2026-06-02. Её пересмотр — по триггерам
  раздела 5, а не по календарю.

---

## 7. Связь с другими артефактами

| Артефакт | Роль в контексте этого документа |
| --- | --- |
| [ai-rules/agent-onboarding-protocol.md](../../ai-rules/agent-onboarding-protocol.md) | Canonical-контракт онбординга (Кейс 1), дизайн которого учитывает рекомендации Команды С. |
| [docs/rfc/rfc-two-cases-of-project-initialization.md](../../docs/rfc/rfc-two-cases-of-project-initialization.md) | RFC-манифест двух кейсов инициализации (в работе); целевое место для «Evidence model — назвать явно». |
| [research/hub/2026-06-02-ai-collaboration-retrospective.md](2026-06-02-ai-collaboration-retrospective.md) | Контекст ошибок холодного старта; обоснование fail-closed и threat awareness. |
| [research/hub/2026-06-01-team-c-governance-strategy-audit.md](2026-06-01-team-c-governance-strategy-audit.md) | Предыдущий аудит Команды С; источник принципа «нет governance-артефакта без боли» и границы анализа. |
| [standards/glossary.md](../../standards/glossary.md) | Единый источник терминов; сюда добавлены **North Star** и **Триггер внедрения**. |

---

## 8. Решение за человеком

Этот документ — исследование, а не финальное решение
([AI_GOVERNANCE.md](../../ai-governance/ai-governance.md): humans принимают финальные решения
по governance). Прошу:

1. **Подтвердить матрицу** раздела 3 (распределение «взять/отложить/отклонить»)
   или скорректировать строки.
2. **Утвердить формулировку North Star** (раздел 4) как рабочее стратегическое
   видение.
3. **Согласовать триггеры** раздела 5 как условия возврата к отложенным идеям.
4. **Решить о следующих задачах** на физическое внедрение «бесплатных»
   улучшений из раздела 3.1 (каждое — отдельный issue/PR).
