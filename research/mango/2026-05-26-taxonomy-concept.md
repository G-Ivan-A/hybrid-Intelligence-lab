---
status: draft
version: 0.1
updated: 2026-05-26
temperature: 0.1
type: concept-proposal
context: [taxonomy, telecom, product-management]
method: standards-analysis + gap-mapping
---

# Концепция Единой таксономии функциональности Mango

Документ предлагает практичную модель Unified Capability Taxonomy для Mango:
единый язык описания функциональности, входящих требований, продуктового
покрытия и маршрутизации к командам. Целевой результат пилота - не заменить
продуктовый каталог и не внедрить полный enterprise architecture процесс, а
дать БА и PO стабильный слой классификации, который можно применить за 1-2
спринта к ВАТС, контакт-центру и связанным AI/analytics capabilities.

## Назначение и границы

Таксономия нужна, чтобы одинаково классифицировать:

1. публичные и внутренние фичи Mango;
2. требования заказчиков из ТЗ, RFI/RFP и discovery;
3. функции конкурентов и best-practice capabilities;
4. gap и roadmap-гипотезы;
5. маршрутизацию к продуктовым командам и SME.

Таксономия не должна становиться вторым продуктовым каталогом. Каталог отвечает
на вопрос "что продаем и как упаковано", а taxonomy отвечает на вопрос "какая
capability требуется, как она связана со стандартами, продуктом, командой,
качеством, compliance и evidence".

## Основание в текущих исследованиях

| Источник | Что уже полезно | Что нужно добавить в taxonomy |
| --- | --- | --- |
| [research/mango/2026-05-22-classification.md](2026-05-22-classification.md) | Пять продуктовых семейств Mango, рабочая связка TM Forum + UNSPSC + ОКПД 2, российский standards/compliance overlay, список реальных фич. | Стабильные capability ID, версии, ownership, отделение feature type от product family, явная модель зрелости. |
| [research/mango/2026-05-22-classification-tz.md](2026-05-22-classification-tz.md) | Проверка на корпусе 30 ТЗ, временный классификатор A/B/C, частотность требований, выявленные gaps: карусельные номера, голосовые SMS, self-service, mobile agent, commercial layer. | Единый процесс "сырое требование -> нормализация -> классификация -> маршрутизация", атрибуты uncertainty и multi-tagging. |
| [research/mango/2026-05-22-requirements-flow.md](2026-05-22-requirements-flow.md) | Flow AI-анализа ТЗ, атомаризация требований, статусы покрытия, evidence, BA review, статистика gap. | Формальный интерфейс для команд: какие поля попадают в backlog, кто принимает taxonomy change, как аудитить изменения. |
| [mango_ba_prompts](https://github.com/G-Ivan-A/mango_ba_prompts) | Mango описан как spoke-проект с mini-agent подходом и `kb/` как источником стабильного контекста. | Taxonomy должна стать одним из `kb/`-совместимых источников для controlled generation, но после пилота. |

Главный пробел текущей базы: уже есть богатая классификация продуктов и ТЗ, но
нет единой мета-модели, которая связывает capability, требование, evidence,
уровень зрелости, владельца и правила изменения.

## Обзор международных стандартов

| Стандарт / подход | Что применимо к Mango | Как использовать в пилоте | Что не переносить слепо |
| --- | --- | --- | --- |
| TM Forum Frameworx / ODA: eTOM, SID, Open APIs | Доменный язык telco/CSP: Customer, Product, Service, Resource, процессы lifecycle, common data model и Open API thinking. | Брать как верхний отраслевой слой: capability domain, связь product/service/resource, lifecycle заказа/обслуживания/эксплуатации. | Не внедрять полный Frameworx как обязательную структуру команд; для пилота достаточно mapping-полей и 7 Mango-доменов. |
| ISO/IEC 25010:2023 | Модель качества ICT/software product для NFR: functional suitability, performance, reliability, security, maintainability и другие характеристики. | Использовать как overlay для качества capability и acceptance criteria, особенно для NFR, зрелости и проверяемости. | Не смешивать quality characteristics с функциональными доменами: это отдельный слой оценки. |
| ISO/IEC/IEEE 29148:2018 | Requirements engineering: процессы и information items для требований, проверяемости и traceability. | Применять к нормализации: атомарность, sourceLocation, measurable result, criteria, связи requirement -> capability -> evidence. | Не превращать пилот в полный compliance-процесс requirements engineering. |
| BABOK Guide / IIBA standards | Язык BA: elicitation, requirements lifecycle management, strategy analysis, requirements analysis, solution evaluation. | Разделять business need, stakeholder requirement, solution requirement, transition requirement и NFR. | Не использовать BABOK как продуктовый классификатор: он описывает работу БА, а не telco capabilities. |
| TOGAF / ArchiMate | Связь capability с business architecture, application/service layer, work package и roadmap. | Использовать для ownership и roadmap views: capability -> product team -> application/service -> initiative. | Не требовать ArchiMate-модели для каждой строки taxonomy в пилоте. |
| UNSPSC / ОКПД 2 | Внешний закупочный и договорной слой для RFI/RFP и тендерных ТЗ. | Держать как optional procurement overlay рядом с Mango capability. | Не делать закупочный код главным ключом taxonomy: он слишком грубый для продуктового анализа. |

Вывод: для Mango базовым доменным стандартом остается TM Forum/ODA, но рабочая
таксономия должна быть адаптирована к продуктовой реальности Mango. ISO 25010,
ISO/IEC/IEEE 29148 и BABOK применяются как слои качества и requirements
discipline, а TOGAF/ArchiMate - как слой связи с архитектурой и командами.

## Принципы проектирования

| Принцип | Решение для taxonomy |
| --- | --- |
| Минимальная полезная глубина | Начать с 7 доменов и 20-30 pilot capabilities, не с полного каталога. |
| Multi-tagging | Одно требование может иметь основной capability и 1-3 дополнительных тега: compliance, commercial, integration, NFR. |
| Evidence required | Для статуса покрытия нужна ссылка на продуктовую страницу, KB, API, SME-комментарий или прошлое решение БА. |
| Uncertainty by design | Для неоднозначных требований фиксировать `uncertainty: low/medium/high` и вопрос на уточнение. |
| Версионирование | Каждая capability получает версию, дату введения, статус и миграционную заметку при изменении. |
| Разделение каталогов | Product package, feature, capability, NFR и commercial condition хранятся как разные поля. |
| Human ownership | Taxonomy owner и PO подтверждают изменения; AI предлагает, но не публикует canonical изменения без review. |

## Предлагаемая мета-модель таксономии

Минимальная запись taxonomy:

| Поле | Пример | Назначение |
| --- | --- | --- |
| `capability_id` | `MGO-CC-ROUTING-001` | Стабильный ID, не зависящий от названия продукта или тарифа. |
| `capability_name` | `Skill-based routing` | Короткое имя capability. |
| `domain` | `CCaaS & Customer Interaction` | Один из 7 доменов пилота. |
| `feature_type` | `core-feature` | Тип: core-feature, option, integration, process, nfr, compliance, commercial, hardware-edge. |
| `mango_product` | `Омниканальный контакт-центр` | Продуктовая упаковка или `TBD`, если capability gap. |
| `mango_status` | `Есть` | `Есть`, `Частично`, `Не выявлено`, `Вне SaaS-ядра`, `Требует SME-review`. |
| `tm_forum_mapping` | `Customer / Customer Interaction` | Доменный mapping на TM Forum/ODA language. |
| `quality_overlay` | `ISO 25010: reliability, usability` | Какие NFR особенно важны для capability. |
| `requirement_type` | `solution requirement` | BABOK/BA слой: business, stakeholder, solution, transition, NFR. |
| `owner_route` | `Contact Center PO + Platform API SME` | Команда или роль, которой уходит требование. |
| `evidence_refs` | `product page`, `KB`, `SME note` | Доказательства для покрытия или gap. |
| `uncertainty` | `medium` | Уровень неопределенности классификации. |
| `lifecycle_status` | `active` | `candidate`, `active`, `deprecated`, `merged`, `split`. |
| `introduced_in` | `taxonomy v0.1` | Версия taxonomy, где появилась запись. |

### Домены пилота

| Код | Домен | Что включает | Типичные владельцы |
| --- | --- | --- | --- |
| `VN` | Connectivity & Numbering | SIP, GSM, номера, 8-800, транки, дозваниваемость, карусель/этикетка. | Telephony / Operator services. |
| `UC` | UCaaS & Voice Collaboration | ВАТС, IVR, переадресация, запись, Mango Talker, видеосвязь. | UCaaS / Voice product. |
| `CC` | CCaaS & Customer Interaction | Очереди, ACD, routing, outbound, рабочее место оператора, WFM, база знаний. | Contact Center product. |
| `AI` | Conversational AI & Automation | Голосовой робот, чат-бот, no-code сценарии, TTS/ASR, робот-администратор. | AI / Automation product. |
| `AQ` | Analytics, QM & Marketing Attribution | Речевая аналитика, QM, BI, коллтрекинг, сквозная аналитика, ROMI. | Analytics / Marketing services. |
| `IP` | Integration Platform & Data Exchange | API, webhook, CRM/1C/LDAP integrations, marketplace, data export. | Platform / Integrations. |
| `GC` | Governance, Compliance & Commercial Controls | SLA, ПДн, реклама, тарифы, лицензии, procurement format, реестр российского ПО. | Legal, Security, Commercial, BA governance. |

### Уровни зрелости capability

| Уровень | Название | Критерий |
| --- | --- | --- |
| `L0` | Raw mention | Capability встречается в ТЗ или каталоге, но не нормализована. |
| `L1` | Candidate | Есть рабочее имя, домен и источник. |
| `L2` | Normalized | Есть ID, тип, определение, примеры включения/исключения. |
| `L3` | Mapped | Есть mapping к Mango product, TM Forum domain и requirement type. |
| `L4` | Evidence-backed | Есть evidence и правила статусов покрытия. |
| `L5` | Managed | Есть owner, метрики спроса, changelog и regression examples для AI. |

## Маппинг фич Mango -> таксономия

| Mango feature / capability | Домен | Тип | TM Forum / ODA mapping | Quality / BA overlay | Маршрутизация |
| --- | --- | --- | --- | --- | --- |
| Виртуальная АТС | `UC` | core-feature | Product + Service, service lifecycle | ISO 25010: reliability, usability; solution requirement | UCaaS PO |
| Виртуальные номера, 8-800, SIP trunk | `VN` | core-feature | Resource + Service | Reliability, availability; compliance trigger `услуга связи` | Telephony / Operator services |
| IVR / голосовое меню / автосекретарь | `UC`, `CC` | option | Customer interaction, service usage | Usability, functional suitability; solution requirement | UCaaS PO + Contact Center PO |
| Распределение звонков, очереди, callback | `CC` | core-feature | Customer interaction / Service assurance | Performance efficiency, reliability | Contact Center PO |
| Запись разговоров и архив | `UC`, `AQ`, `GC` | option + compliance | Service usage + customer interaction evidence | Security, privacy, auditability; NFR/compliance | UCaaS PO + Security review |
| Омниканальный контакт-центр | `CC` | product package | Customer + Product + Service | Usability, compatibility, scalability | Contact Center PO |
| Исходящий обзвон / кампании | `CC`, `AI`, `GC` | core-feature | Customer interaction, product/service usage | Reliability; compliance trigger `реклама/ПДн` | Contact Center PO + Legal if campaign rules |
| Голосовой робот с no-code сценариями | `AI` | core-feature | Customer interaction automation | Functional suitability, usability; сценарирование `customer-configured/vendor-managed/mixed` | AI PO |
| Чат-бот и цифровые каналы | `AI`, `CC` | core-feature | Customer interaction / digital channel | Usability, interoperability | AI PO + Contact Center PO |
| Речевая аналитика и QM | `AQ` | core-feature | Service assurance / customer interaction analytics | Accuracy, security, maintainability; evidence-heavy requirement | Analytics PO + Security review |
| WFM / управление рабочими ресурсами | `CC` | option/process | Workforce / customer operations support | Efficiency, operability; process requirement | Contact Center PO |
| API, webhook, CRM/1C integrations | `IP` | integration | Open API / application integration | Compatibility, security, maintainability | Platform Integrations SME |
| Коллтрекинг и сквозная аналитика | `AQ`, `GC` | core-feature | Market & Sales analytics | Accuracy, privacy, commercial attribution | Marketing Analytics PO + Legal if advertising data |

В пилоте достаточно выбрать 10-15 строк из этой таблицы и довести их до уровня
`L4 Evidence-backed`. Остальные строки могут оставаться `L1-L2`, чтобы не
перегружать классификацию.

## Процесс нормализации и маппинга

```text
Сырое требование
  -> сохранение sourceLocation и исходной формулировки
  -> декомпозиция на атомарные требования
  -> нормализация в проверяемую формулировку
  -> классификация: domain + capability + feature_type + requirement_type
  -> mapping: Mango product/status + TM Forum + quality/compliance overlays
  -> evidence lookup и confidence
  -> маршрутизация к owner_route
  -> BA/SME review
  -> статистика спроса, gap и change requests к taxonomy
```

Минимальная карточка нормализованного требования:

| Поле | Пример |
| --- | --- |
| `raw_text` | "Нужно автоматически оценивать все звонки операторов по чек-листу." |
| `normalized_requirement` | "Система должна выполнять автоматическую оценку записанных звонков операторов по настраиваемому чек-листу с сохранением результата оценки." |
| `capability_id` | `MGO-AQ-QM-001` |
| `domain` | `AQ` |
| `feature_type` | `core-feature` |
| `mango_status` | `Есть / Частично / Требует SME-review` |
| `coverage_status` | `Покрывается`, `Частично покрывается`, `Не покрывается`, `Требует уточнения`, `Вне области Mango` |
| `evidence_refs` | Ссылка на продуктовую страницу, KB или SME note. |
| `uncertainty` | `medium`, если неясны параметры чек-листа, точность и источник записи. |
| `owner_route` | `Analytics PO + Contact Center SME` |

Правило: AI может предложить классификацию, но финальный статус покрытия и
изменение taxonomy подтверждает БА или назначенный owner.

## Интерфейс для продуктовых команд

Командам не нужен отдельный тяжелый инструмент в пилоте. Достаточно добавить
контролируемые поля в текущий backlog-инструмент (Jira, YouTrack, Confluence
таблица или Markdown registry):

| Поле | Для чего команде |
| --- | --- |
| `capability_id` | Стабильная привязка требования и статистики спроса. |
| `domain` / `owner_route` | Автоматическая маршрутизация и фильтр команды. |
| `mango_status` / `coverage_status` | Понимание, является ли это existing feature, gap или уточнение. |
| `evidence_refs` | Быстрое review без повторного поиска источников. |
| `uncertainty` / `clarification_question` | Очередь вопросов к заказчику или SME. |
| `frequency_90d` | Сколько раз похожий demand встречался за последние 90 дней. |
| `commercial_overlay` | Видно, что требование относится к тарифу/договору, а не к feature gap. |

Операционный сценарий:

1. БА классифицирует требования ТЗ и получает suggested owner.
2. Команда видит входящие требования по своему `owner_route`.
3. PO подтверждает `coverage_status`, gap и priority.
4. Taxonomy owner раз в неделю смотрит новые `candidate` capabilities.
5. Раз в квартал выпускается taxonomy minor version и миграционная заметка.

## Метрики и аудит

| Метрика | Цель пилота |
| --- | --- |
| `% classified` | Не менее 80 % атомарных требований пилотного корпуса получают `domain` и `feature_type`. |
| `% evidence-backed` | Не менее 60 % требований с финальным статусом имеют evidence. |
| `routing lead time` | Медианное время от нормализации до owner_route - до 1 рабочего дня. |
| `SME override rate` | Доля исправлений классификации SME; если выше 25 %, taxonomy слишком неустойчива. |
| `uncertainty rate` | Доля требований `medium/high`; помогает понять, где нужны glossary и примеры. |
| `top gap frequency` | Топ-10 gap capabilities за период для product discovery. |
| `taxonomy change cycle time` | Сколько времени занимает добавление или изменение capability. |

Аудит ведется через changelog taxonomy: кто предложил изменение, какой source
подтверждает, что мигрировать, какие старые теги deprecated и какая команда
владеет строкой.

## Правила эволюции стандарта

| Изменение | Кто предлагает | Кто утверждает | SLA |
| --- | --- | --- | --- |
| Новый синоним или пример | БА, AI, SME | Taxonomy owner | До 5 рабочих дней. |
| Новая candidate capability | БА или PO на основе ТЗ/gap | Taxonomy owner + domain PO | До 10 рабочих дней. |
| Изменение домена или owner_route | Domain PO | Taxonomy owner + affected PO | До 10 рабочих дней. |
| Fast-track для тендера | БА или sales owner | Taxonomy owner + один SME | До 1 рабочего дня, статус `candidate`. |
| Deprecation / merge / split capability | Taxonomy owner | PO council / Founder if strategic | Квартальный release. |

После пилота можно создать `standards/feature-taxonomy.md`, но сейчас это было
бы преждевременно: по [governance/repo-model.md](../../governance/repo-model.md)
новый standard оправдан только после повторяющейся операционной боли и review.

## План пилота на 1-2 спринта

### Спринт 1: taxonomy v0.1 и проверка на малом корпусе

| Шаг | Результат |
| --- | --- |
| Выбрать 2 продукта: Виртуальная АТС и Омниканальный контакт-центр. | Зафиксирован scope пилота и owner_route. |
| Выбрать 20-30 требований из корпуса ТЗ, где есть voice, CCaaS, AI, analytics, integration и compliance. | Минимальный regression set для БА. |
| Создать 10-15 capability records уровня `L2-L3`. | Есть ID, домен, тип, mapping и owner. |
| Провести BA/PO review классификации. | Список исправлений и спорных терминов. |
| Добавить glossary deltas. | Снижение semantic drift. |

### Спринт 2: evidence, метрики и решение о стандарте

| Шаг | Результат |
| --- | --- |
| Довести 10 pilot capabilities до `L4 Evidence-backed`. | Есть evidence и правила покрытия. |
| Прогнать еще 30-50 требований или один свежий RFI/RFP. | Метрики `% classified`, `% evidence-backed`, override rate. |
| Настроить поля backlog-инструмента или Markdown registry. | Команды могут фильтровать свои требования. |
| Провести retrospective с БА, PO и Founder. | Решение: расширять taxonomy, создать `standards/feature-taxonomy.md` или оставить как research draft. |

Рекомендуемый пилотный scope: ВАТС/UCaaS + Омниканальный контакт-центр, потому
что эти зоны чаще всего встречаются в корпусе ТЗ и одновременно затрагивают
AI, аналитику, интеграции и compliance.

## Риски и митигации

| Риск | Что может пойти не так | Митигация |
| --- | --- | --- |
| Перегрузка классификации | Команды перестанут использовать taxonomy из-за слишком многих полей. | В пилоте обязательны только `capability_id`, `domain`, `feature_type`, `mango_status`, `owner_route`, `evidence_refs`, `uncertainty`. |
| Ригидность стандарта | Новые фичи и рыночные формулировки не попадают в taxonomy вовремя. | Квартальный release + fast-track `candidate` для тендеров. |
| Семантический дрейф | Одни и те же термины начинают значить разное в BA, PO и sales. | Все новые термины сверять со [standards/glossary.md](../../standards/glossary.md) и проектным Mango glossary после его создания. |
| Двойное ведение | Каталог продукта и taxonomy расходятся. | Product package не дублируется; taxonomy хранит capability ID и ссылку на evidence/catalog. |
| Ложная точность | AI присваивает уверенный mapping при неоднозначном требовании. | Multi-tagging, `uncertainty`, confidence threshold и обязательный BA review. |
| Ownership conflict | Требование затрагивает несколько команд. | Основной owner + secondary owners; конфликт решает Taxonomy owner и affected PO. |
| Устаревшие evidence | Статус покрытия основан на старой продуктовой странице или SME note. | Evidence получает дату среза; stale evidence старше 90 дней требует re-check для тендера. |
| Taxonomy становится бюрократией | Команды видят только дополнительное поле, а не пользу. | Метрики пилота должны показать сокращение routing lead time и повторного анализа. |

## Связанные артефакты и источники

Внутренние артефакты:

- [standards/glossary.md](../../standards/glossary.md) - контролируемый словарь
  governance и AI-assisted terms.
- [governance/repo-model.md](../../governance/repo-model.md) - правило
  размещения и Anti-Inflation principle.
- [governance/artifact-map.md](../../governance/artifact-map.md) - навигация
  по активным артефактам.
- [standards/research-profile.md](../../standards/research-profile.md) -
  профиль research-артефактов и правила source-backed analysis.
- [mango_ba_prompts](https://github.com/G-Ivan-A/mango_ba_prompts) - связь Mango как
  spoke-проекта с лабораторией.
- `standards/feature-taxonomy.md` - не создан в этом PR; рекомендуется только
  после пилота и review, если taxonomy станет повторяемым standard.

Внешние источники:

- TM Forum, Open Digital Architecture: <https://www.tmforum.org/open-digital-architecture/>
- TM Forum, how to apply ODA: <https://www.tmforum.org/open-digital-architecture/how-to-apply-oda/>
- ISO, ISO/IEC 25010:2023 product quality model: <https://www.iso.org/standard/78176.html>
- ISO, ISO/IEC/IEEE 29148:2018 requirements engineering: <https://www.iso.org/standard/72089.html>
- IIBA, BABOK Guide: <https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/>
- The Open Group, TOGAF Standard: <https://www.opengroup.org/togaf>
- The Open Group, ArchiMate and TOGAF complementarity: <https://help.opengroup.org/hc/en-us/articles/32115987894930-How-the-ArchiMate-Language-and-the-TOGAF-Standard-Complement-Each-Other>
- UNDP, UNSPSC: <https://www.undp.org/unspsc>
- MANGO OFFICE, Виртуальная АТС: <https://www.mango-office.ru/products/virtualnaya_ats/>
- MANGO OFFICE, Омниканальный контакт-центр: <https://www.mango-office.ru/products/contact-center/>
- MANGO OFFICE, Голосовой робот: <https://www.mango-office.ru/products/contact-center/ai/voice-robot/>

## Вопросы для обсуждения с PO/Founder

1. Какие два домена брать в пилот первыми: ВАТС + контакт-центр или контакт-центр + AI/analytics?
2. Кто будет Taxonomy owner на время пилота: BA lead, Product Operations или отдельный PO?
3. В каком инструменте фиксируем pilot taxonomy: Markdown registry, Confluence, Jira/YouTrack custom fields или Mango `kb/`?
4. Какие поля обязательны для первого пилота, а какие остаются optional, чтобы не перегрузить команды?
5. Какой threshold считать успехом: скорость маршрутизации, доля evidence-backed требований, снижение повторных вопросов или качество gap-статистики?
6. Когда создаем `standards/feature-taxonomy.md`: после первого успешного тендера, после 2 спринтов пилота или после review с Founder?
7. Какие данные нельзя использовать в taxonomy и evidence из-за NDA, ПДн или коммерческой чувствительности?
