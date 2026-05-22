# Классификация IT/Telecom SaaS-продуктов MANGO OFFICE

Дата среза: 22 мая 2026 г.

Цель документа: зафиксировать рабочую международную классификацию продуктов и сервисов MANGO OFFICE, чтобы бизнес-аналитик мог сравнивать входящие требования с эталонным каталогом и быстро понимать, относится ли требование к существующему продукту, смежной возможности или внешнему классу решений.

## Краткий вывод

Публичный каталог MANGO OFFICE покрывает пять крупных продуктовых семейств:

1. Корпоративная телефония и UCaaS: виртуальная АТС, IP-телефония, номера, SIP trunk, мобильная телефония, запись, IVR, распределение звонков, Mango Talker и видеоконференции.
2. Контакт-центр и CCaaS: входящие и исходящие обращения, омниканальность, рабочее место оператора, отчеты, WFM, управление персоналом, база знаний, чат для сайта, управление сделками и оценка эффективности.
3. Цифровые каналы и коммуникации: онлайн-чат, мессенджеры, email, SMS, мессенджер-маркетинг, единое окно оператора.
4. AI и автоматизация: голосовой робот, чат-бот, робот-администратор, речевая аналитика, управление качеством, робот-аналитик и робот-маркетолог.
5. Маркетинговая и бизнес-аналитика: коллтрекинг, мультиканальная и сквозная аналитика, email-трекинг, ROMI, товарная аналитика, анализ конкурентов и интеграции с CRM/1C/API/webhook.

Для стандартной классификации выбраны два взаимодополняющих фреймворка:

- **TM Forum Frameworx / Open APIs**: основной отраслевой фреймворк для телеком- и цифровых сервис-провайдеров. Он удобен для внутренней классификации требований через домены Market & Sales, Customer, Product, Service и Resource, а также через жизненный цикл каталога, заказа, обслуживания и эксплуатации.
- **UNSPSC**: глобальная товарно-сервисная классификация ООН/UNDP. Она удобна для закупочной, договорной и внешней классификации: к каждому продукту можно присвоить код commodity-класса и связать требование с международной номенклатурой.

Рекомендуемая схема для БА: одно требование получает два ключа классификации. Первый ключ отвечает на вопрос "какой это домен и capability в телеком/цифровом сервис-провайдере" по TM Forum. Второй ключ отвечает на вопрос "какой это товарно-сервисный класс для закупки, договора или сравнения поставщиков" по UNSPSC.

## Методика

- Источники по продуктам: публичный каталог и страницы продуктов MANGO OFFICE на `mango-office.ru`.
- Источники по стандартам: страницы TM Forum по eTOM, SID и TMF620; официальный обзор UNSPSC от UNDP; публичный экспорт UNSPSC из UNGM.
- Статус в колонке MANGO OFFICE:
  - **Есть**: продукт или возможность явно присутствует в публичном каталоге.
  - **Частично**: возможность есть как часть более крупного продукта, через модуль, интеграцию или ограниченный сценарий.
  - **Не выявлено**: в публичном каталоге не найден самостоятельный продукт такого класса.
  - **Вне SaaS-ядра**: предложение присутствует, но относится к оборудованию или смежной поставке, а не к SaaS-сервису.
- UNSPSC-коды приведены как рабочие коды для классификации требований. Для закупки или договора их стоит проверять по актуальному экспортному файлу UNGM/UNSPSC на дату использования.

## Анализ публичного каталога MANGO OFFICE

| Семейство | Продукты и возможности MANGO OFFICE | Роль в классификации требований |
| --- | --- | --- |
| Телефония и UCaaS | Виртуальная АТС, IP-телефония, виртуальные номера, 8-800, SIP trunk, запись разговоров, голосовое меню IVR, распределение звонков, автосекретарь, обратный звонок, SMS-рассылки, Mango Mobile, Mango Talker, видеоконференции | Базовый класс требований к корпоративной голосовой связи, унифицированным коммуникациям и номерной емкости |
| Контакт-центр и CCaaS | Омниканальный контакт-центр, исходящий обзвон, омниканальные коммуникации, рабочее место сотрудника, управление персоналом, WFM, конструктор отчетов, робот-администратор, база знаний, чат для сайта, управление сделками, оценка эффективности, API для УВК/CRM | Класс требований к обслуживанию клиентов, очередям, маршрутизации, outbound-кампаниям, SLA и рабочему месту оператора |
| Интеграции | Интеграции по API, webhook, 1C, LDAP/ОПДкРК, маркетплейс интеграций | Класс требований к обмену данными, embedding в CRM/ERP, событиям, синхронизации справочников и расширяемости |
| AI и контроль качества | Голосовой робот, чат-бот, искусственный интеллект, речевая аналитика, управление качеством, бизнес-аналитика | Класс требований к автоматизации диалогов, распознаванию речи, контролю качества, аналитике операторов и снижению ручной нагрузки |
| Маркетинговая аналитика | Коллтрекинг, мультиканальная аналитика, сквозная аналитика, email-трекинг, ROMI, товарная аналитика, анализ конкурентов, робот-аналитик, робот-маркетолог, мессенджер-маркетинг | Класс требований к атрибуции, источникам лидов, рекламной эффективности и маркетинговым отчетам |
| Оборудование и безопасность | SIP-телефоны, гарнитуры, устройства, информационная безопасность | Смежные классы: оборудование и защищенность сервиса. Не являются ядром SaaS-классификации, но важны для полного требования |

## Рассмотренные стандарты и фреймворки

| Стандарт или фреймворк | Что дает для этой задачи | Решение |
| --- | --- | --- |
| TM Forum Frameworx: eTOM, SID, Open APIs | Отраслевой язык телеком-провайдера: продукт, сервис, ресурс, клиент, заказ, каталог, эксплуатация, партнеры. Хорошо подходит для MANGO OFFICE как поставщика коммуникационных сервисов. | Выбран как основной доменный стандарт |
| UNSPSC | Международная иерархическая классификация продуктов и услуг. Хорошо подходит для внешнего сравнения, закупки и кодирования требований. | Выбран как второй стандарт |
| ITIL 4 / ISO/IEC 20000 | Сильный фреймворк управления IT-сервисами: SLA, инциденты, запросы, каталог услуг, эксплуатация. Полезен для NFR и процессов поддержки, но слабее классифицирует сами телеком/SaaS-продукты. | Не выбран для основной таблицы, использовать как дополнительный процессный слой |
| MEF LSO | Полезен для операторских сетевых сервисов и оркестрации connectivity/NaaS. Для ВАТС, контакт-центра, ботов и маркетинговой аналитики слишком узкий. | Не выбран для основной таблицы |
| NAICS/ISIC/ОКВЭД-подобные классификаторы | Классифицируют отрасли и компании, а не конкретные SaaS-продукты. | Не выбран |

## Правила применения двух выбранных стандартов

### TM Forum Frameworx / Open APIs

В этой работе TM Forum используется не как перечень "товарных карточек", а как доменная модель для телеком/SaaS-провайдера:

- **Market & Sales**: требования к продажам, маркетинговой аналитике, коммерческим предложениям, рекламным кампаниям и атрибуции.
- **Customer**: требования к клиенту, пользователю, обращению, коммуникации, SLA, качеству обслуживания и взаимодействию.
- **Product**: требования к продуктовой карточке, тарифу, опции, пакету, каталогу и заказу.
- **Service**: требования к логическому сервису: ВАТС, контакт-центр, IVR, робот, речевая аналитика, каналы коммуникаций.
- **Resource**: требования к ресурсам: номер, SIP trunk, канал, линия, устройство, запись разговора, интеграционный endpoint.

Open API слой нужен как ориентир для реализации и интеграций: продуктовые требования обычно связаны с каталогом и заказом, сервисные требования - с service inventory/order, клиентские обращения - с customer/party interaction, эксплуатационные требования - с trouble ticket, SLA, usage и monitoring.

### UNSPSC

UNSPSC используется как внешний кодировщик товарно-сервисного класса. Для SaaS-продукта часто нужны два уровня:

- обобщающий код **81162000 Cloud-based software as a service**;
- функциональный код, например **43232903 Contact center software**, **43232303 Customer relationship management CRM software**, **83111510 Interactive voice response service** или **80141501 Marketing analysis**.

Такой двойной подход уменьшает неоднозначность: требование "голосовой робот" является SaaS-сервисом, но функционально ближе к IVR, voice recognition и контакт-центру.

## Сравнительная таблица классификации

| № | Продукт/сервис | MANGO OFFICE: есть/нет | Стандарт 1: TM Forum Frameworx / Open APIs (обоснование) | Стандарт 2: UNSPSC (обоснование) |
| ---: | --- | --- | --- | --- |
| 1 | Виртуальная АТС / облачная телефония | Есть | Product Offering в Product domain; Service domain для голосового сервиса; Resource domain для номеров, линий и правил маршрутизации. | 81162000 Cloud-based software as a service + 83111500 Local and long distance telephone communications. |
| 2 | IP-телефония и SIP trunk | Есть | Service/Resource: логический голосовой сервис поверх SIP-ресурсов; удобно отделять заказ продукта от ресурсов подключения. | 83111500 Local and long distance telephone communications; 43232901 Access software или 43232915 Platform interconnectivity software для софтверной части. |
| 3 | Виртуальные номера, 8-800, мобильные номера | Есть | Resource domain: номерная емкость как ресурс, привязанный к продукту ВАТС или контакт-центру. | 83111501 Local telephone service, 83111502 Long distance telephone services, 83111603 Cellular telephone services. |
| 4 | Голосовое меню IVR, автосекретарь, автоинформатор | Есть | Service capability внутри голосового сервиса; требования относятся к service specification, routing и customer interaction. | 83111510 Interactive voice response service + 43232703 Interactive voice response software. |
| 5 | Распределение звонков, очереди, правила маршрутизации | Есть | Customer/Service: управление взаимодействием и исполнением сервиса; для требований важны SLA, skill groups и правила маршрутизации. | 43232903 Contact center software или 43231501 Helpdesk or call center software. |
| 6 | Запись разговоров, журнал звонков, статистика | Есть | Service assurance и usage: фиксация использования сервиса, контроль качества и доказательная база для обращений. | 43232300 Data management and query software + 43232605 Analytical or scientific software. |
| 7 | Обратный звонок с сайта | Есть | Market & Sales + Customer interaction: лидогенерация превращается в коммуникацию и заказ обратного вызова. | 80141603 Telemarketing + 83111500 Telephone communications. |
| 8 | Mango Talker: корпоративный мессенджер и softphone | Есть | Customer interaction и Service: единое рабочее пространство коммуникаций; Resource - пользовательские endpoint-устройства и приложения. | 43232702 Desktop communications software + 43223204 Unified messaging platform. |
| 9 | Видеоконференции | Есть | Service domain для UCaaS-сервиса; Product domain для опции или отдельного предложения в каталоге. | 43233502 Video conferencing software + 81162000 Cloud-based software as a service. |
| 10 | SMS-рассылки | Есть | Customer interaction и Campaign/Market & Sales: массовые уведомления и коммуникации с клиентами. | 43223202 Short message service center + 81161600 Electronic mail and messaging services. |
| 11 | Омниканальный контакт-центр / CCaaS | Есть | Product/Service: отдельное Product Offering с capability обслуживания обращений; Customer domain для клиента и обращения. | 43232903 Contact center software + 43231501 Helpdesk or call center software. |
| 12 | Входящие обращения, очереди, рабочее место оператора | Есть | Customer interaction и Service assurance: управление обращением, оператором, каналом и SLA. | 43232903 Contact center software. |
| 13 | Исходящий обзвон и кампании | Есть | Market & Sales + Customer interaction: outbound-кампания как коммерческое взаимодействие, исполняемое контакт-центром. | 80141603 Telemarketing + 43232903 Contact center software. |
| 14 | Омниканальные коммуникации: чат, мессенджеры, соцсети, email | Есть | Customer interaction across channels; полезно классифицировать канал отдельно от бизнес-сценария обращения. | 43223204 Unified messaging platform, 43223205 Instant messaging platform, 81161600 Electronic mail and messaging services. |
| 15 | Чат для сайта | Есть | Customer interaction: цифровой канал обращения, связанный с контакт-центром и карточкой клиента. | 43233504 Instant messaging software + 81161600 Electronic mail and messaging services. |
| 16 | Чат-бот | Есть | Service automation внутри Customer domain; бот исполняет часть interaction flow до передачи оператору. | 43231511 Expert system software + 43223205 Instant messaging platform. |
| 17 | Голосовой робот / voice bot | Есть | Service automation для голосового канала; связывает IVR, customer interaction и orchestration сценариев. | 43233413 Voice recognition software + 83111510 Interactive voice response service. |
| 18 | Робот-администратор | Есть | Service orchestration: автоматизирует операционные действия контакт-центра и обращения клиента. | 81112106 Application service providers + 43232403 Enterprise application integration software. |
| 19 | Речевая аналитика / conversation intelligence | Есть | Service assurance и Customer insight: анализ записей, транскриптов и качества коммуникаций. | 43233413 Voice recognition software + 43232605 Analytical or scientific software. |
| 20 | Управление качеством операторов (QM) | Есть | Service assurance: контроль качества, чек-листы, оценки и обратная связь по обслуживанию. | 43232606 Compliance software + 43231501 Helpdesk or call center software. |
| 21 | Workforce Management / управление рабочими ресурсами | Есть | Resource/Enterprise management: планирование операторов как ресурса сервиса контакт-центра. | 43231505 Human resources software + 43232903 Contact center software. |
| 22 | База знаний и скрипты операторов | Есть | Customer/Service support: knowledge artifacts поддерживают выполнение service interaction. | 43232200 Content management software + 43232201 Content workflow software. |
| 23 | Управление сделками / легкий CRM-сценарий | Есть | Customer + Market & Sales: связка клиента, сделки, коммуникации и коммерческого процесса. | 43232303 Customer relationship management CRM software. |
| 24 | Полноценная CRM как самостоятельная платформа | Частично | TM Forum классифицирует как Customer/Sales capability, но в MANGO OFFICE публично виден скорее встроенный сценарий управления сделками и интеграции с внешними CRM. | 43232303 Customer relationship management CRM software. |
| 25 | Интеграции с CRM, 1C, LDAP, marketplace | Есть | Product/Service integration: интеграционные endpoints и партнерские системы вокруг основного продукта. | 43232403 Enterprise application integration software + 81112106 Application service providers. |
| 26 | Open API, webhook, API для УВК/CRM | Есть | Open API слой соответствует интеграционному подходу TM Forum: отделить продуктовый каталог, заказ, сервис и клиентские события от конкретного UI. | 43232403 Enterprise application integration software + 43232915 Platform interconnectivity software. |
| 27 | Коллтрекинг | Есть | Market & Sales: атрибуция звонков к рекламным источникам; Service/Resource: динамические номера как ресурс. | 80141501 Marketing analysis + 83111500 Telephone communications. |
| 28 | Сквозная аналитика и ROMI | Есть | Market & Sales analytics: связывает коммуникации, расходы, лиды, сделки и выручку. | 80141501 Marketing analysis + 43232605 Analytical or scientific software. |
| 29 | Мультиканальная аналитика и атрибуция | Есть | Market & Sales + Customer insight: классифицирует требования к источникам, каналам и конверсиям. | 80141501 Marketing analysis. |
| 30 | Email-трекинг | Есть | Customer interaction + Market & Sales: email как канал коммуникации и атрибуции. | 43233501 Electronic mail software + 81161600 Electronic mail and messaging services. |
| 31 | Товарная аналитика / ecommerce analytics | Есть | Market & Sales: анализ спроса, товарных позиций и эффективности продаж. | 80141501 Marketing analysis + 43232307 Data mining software. |
| 32 | Анализ конкурентов | Есть | Market intelligence в Market & Sales domain; не является core-телеком сервисом, но поддерживает коммерческие решения. | 80141501 Marketing analysis + 80141500 Market research. |
| 33 | Мессенджер-маркетинг | Есть | Market & Sales + Customer interaction: кампании в цифровых каналах, связанные с клиентскими событиями. | 43223205 Instant messaging platform + 81161601 Instant Messaging Administration Service. |
| 34 | CPaaS / программируемые голосовые и messaging API | Частично | TM Forum позволяет оформить как API-enabled Product/Service; у MANGO OFFICE есть API/webhook, но публично не выделен полный CPaaS как отдельная товарная линейка. | 81112106 Application service providers + 43232403 Enterprise application integration software. |
| 35 | Service desk / ITSM helpdesk | Частично | В TM Forum соответствует assurance, trouble ticket и customer problem; у MANGO OFFICE это ближе к контакт-центру, а не к самостоятельному ITSM-продукту. | 43231501 Helpdesk or call center software. |
| 36 | Информационная безопасность | Есть | Enterprise/Security capability, поддерживающая доверие и эксплуатацию сервиса; не основной коммуникационный продукт. | 43233200 Security and protection software или смежные security-коды по актуальному UNSPSC. |
| 37 | SIP-телефоны, гарнитуры и устройства | Вне SaaS-ядра | Resource domain: физические ресурсы доступа к сервису. В требованиях лучше отделять от SaaS-функциональности. | 43222800 Telephony equipment; 43222900 Telephony equipment accessories. |

## Рабочая таксономия для входящих требований

Для практического использования в backlog можно завести поля:

| Поле | Пример значения | Зачем нужно |
| --- | --- | --- |
| Product family | `CCaaS / Контакт-центр` | Быстрая маршрутизация требования к продуктовой зоне |
| Mango status | `Есть`, `Частично`, `Не выявлено` | Понимание, является ли требование развитием существующего продукта или новым классом |
| Mango product | `Омниканальный контакт-центр` | Привязка к публичному или внутреннему каталогу продуктов |
| TM Forum domain | `Customer`, `Product`, `Service`, `Resource`, `Market & Sales` | Единый доменный язык для аналитики и архитектуры |
| TM Forum capability | `Customer interaction`, `Product catalog`, `Service assurance`, `Usage`, `Resource management` | Уточнение типа требования |
| UNSPSC code | `43232903 Contact center software` | Внешняя классификация для сравнения поставщиков и закупки |
| Requirement relation | `Core feature`, `Option`, `Integration`, `Process`, `Hardware`, `Out of scope` | Связь требования с продуктом |

Примеры:

- "Нужно принимать обращения из Telegram, WhatsApp, сайта и email в одном окне": Product family `CCaaS / Digital channels`; Mango status `Есть`; TM Forum `Customer interaction`; UNSPSC `43223204 Unified messaging platform` и `43232903 Contact center software`.
- "Нужно автоматически оценивать все звонки операторов по чек-листу": Product family `AI / QM`; Mango status `Есть`; TM Forum `Service assurance`; UNSPSC `43233413 Voice recognition software` и `43232606 Compliance software`.
- "Нужно полноценное ITSM-решение для внутренних инцидентов ИТ": Product family `Adjacent ITSM`; Mango status `Частично/не core`; TM Forum `Assurance / trouble ticket`; UNSPSC `43231501 Helpdesk or call center software`; рекомендация - сравнивать с ITIL/ISO 20000 как дополнительным процессным слоем.

## Рекомендации по ведению стандарта

1. Вести классификацию как живой справочник в репозитории: один Markdown-источник и HTML-версию для просмотра без Markdown-рендера.
2. Для каждого нового требования сначала выбирать product family, затем Mango status, затем TM Forum domain/capability и UNSPSC-код.
3. Если требование не укладывается в текущие классы, добавлять строку в расширенный список со статусом `Не выявлено` или `Частично`, а не смешивать ее с существующим продуктом.
4. Для коммерческих и закупочных документов использовать UNSPSC; для архитектуры, интеграций и декомпозиции требований использовать TM Forum.
5. Для требований поддержки, SLA, инцидентов и service desk дополнительно помечать ITIL/ISO 20000, потому что эти фреймворки лучше описывают процессы эксплуатации, но не заменяют продуктовую классификацию.

## Источники

- MANGO OFFICE, публичный каталог продуктов: <https://www.mango-office.ru/products/>
- MANGO OFFICE, Виртуальная АТС: <https://www.mango-office.ru/products/virtualnaya_ats/>
- MANGO OFFICE, Контакт-центр: <https://www.mango-office.ru/products/contact-center/>
- MANGO OFFICE, Интеграции по API: <https://www.mango-office.ru/products/integraciya/api/>
- MANGO OFFICE, Голосовой робот: <https://www.mango-office.ru/products/contact-center/ai/voice-robot/>
- MANGO OFFICE, Чат-бот: <https://www.mango-office.ru/products/contact-center/vozmozhnosti/chat-bot/>
- MANGO OFFICE, Речевая аналитика: <https://www.mango-office.ru/products/virtualnaya_ats/vozmozhnosti/speech-analytics/>
- MANGO OFFICE, Коллтрекинг: <https://www.mango-office.ru/products/calltracking/>
- MANGO OFFICE, Мультиканальная аналитика: <https://www.mango-office.ru/products/calltracking/vozmozhnosti/multichannel-analytics/>
- TM Forum, Business Process Framework (eTOM): <https://www.tmforum.org/business-process-framework/>
- TM Forum, Information Framework (SID): <https://www.tmforum.org/oda/information-systems/information-framework-sid/>
- TM Forum, TMF620 Product Catalog Management API: <https://www.tmforum.org/resources/standard/tmf620-product-catalog-management-api-rest-specification-r14-5-0/>
- UNDP, United Nations Standard Products and Services Code: <https://www.undp.org/unspsc>
- UNGM, UNSPSC browser and Excel export: <https://www.ungm.org/Public/UNSPSC>
- PeopleCert, ITIL 4 practices overview: <https://www.peoplecert.org/ITIL4-practices>
- ISO, ISO/IEC 20000-1:2018 service management system requirements: <https://www.iso.org/standard/70636.html>
- MEF, Lifecycle Service Orchestration APIs: <https://www.mef.net/service-automation/lso-apis/>
