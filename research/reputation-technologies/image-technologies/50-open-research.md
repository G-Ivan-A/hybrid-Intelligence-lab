---
status: draft
version: 0.2
updated: 2026-10-22
temperature: 0.3
type: research
context: [reputation-technologies, image-technologies, open-research, source-gaps, deviations, self-audit, bibliography, gra-markup]
method: gap-analysis + self-audit + source-traceability + gra-epistemic-markup
scope: reputation-technologies
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/693; https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/695"
based_on:
  - research/reputation-technologies/image-technologies/00-introduction.md
  - research/reputation-technologies/image-technologies/10-theory.md
  - research/reputation-technologies/image-technologies/20-taxonomy.md
  - research/reputation-technologies/image-technologies/30-decision-framework.md
  - research/reputation-technologies/image-technologies/40-practice-and-cases.md
related_artifacts:
  - "research/reputation-technologies/2026-11-03-day4-presentation-gamma-v4.md"
  - "research/reputation-technologies/2026-11-03-rfc-presentation-update-v5.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/693"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/695"
---

# Имидж-технологии: открытые вопросы, отклонения и источники

> **Модуль.** Файл `50-open-research.md` модуля
> [`image-technologies`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/research/reputation-technologies/image-technologies).
> Версия 0.2 по [#695](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/695): пробелы v0.1 пересмотрены после полного анализа первоисточника НИА «Гид по стилю» — справочника «Кодекс стиля», 2007 ([PDF](https://github.com/user-attachments/files/33784962/kodeks_stilya.pdf)); добавлены отклонения от постановки #695, самоаудит по #695 и очищенный список источников, где блоги и файловые библиотеки сняты с опоры.

## 1. Пробелы источников

Таблица показывает, что из пробелов v0.1 закрыто первоисточниками, что осталось открытым и что нашлось нового при поиске по #695. Статус пробела дан словами: **закрыт**, **закрыт частично**, **открыт**.

| # | Пробел | Статус | Что найдено | Как отражено | Что закроет пробел |
| --- | --- | --- | --- | --- | --- |
| 1 | Четыре типа фигур «Гида по стилю» | **закрыт** | Справочник НИА описывает женские типы фигур, крой для каждого и частную коррекцию ([PDF, с. 33–41](https://github.com/user-attachments/files/33784962/kodeks_stilya.pdf)), а также мужские типы фигур, подбор сорочки и галстука ([PDF, с. 41–46](https://github.com/user-attachments/files/33784962/kodeks_stilya.pdf)). | Карточки 2.14 и 2.15 в [таксономии](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md#ось-2-форма); опора — **К**, первоисточник. В RFC v5 слайд 10 переписан по первоисточнику. | — |
| 2 | Шесть стилей Драма — Романтизм — Натуральный — Наивная романтика — Классика — Спорт | **закрыт частично** | Справочник НИА описывает четыре стиля — классический, романтический, драматический и натуральный — с чертами лица и правилом их смешения в деловом коде ([PDF, с. 50–62](https://github.com/user-attachments/files/33784962/kodeks_stilya.pdf)). Все шесть типов от драматического до инженю есть в американской линии ян — инь ([McJimsey, 1963](https://archive.org/details/artinclothingsel0000mcji); [McJimsey, 1973](https://archive.org/details/artfashioninclot00harr)). | Раздел «[Шесть стилей](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md#шесть-стилей-черты-лица-линии-и-искусство)» собран по двум книжным линиям вместо блогов. Соответствие русских названий американским типам и искусствоведческие параллели — уровень **А**, статус `?`. | Учебное пособие, где все шесть русских названий описаны одним автором с чертами лица. |
| 3 | Атрибуция и текст книги Ватерман и Цингель | **закрыт частично** | Справочник НИА прямо называет немецких авторов основой своей системы цветотипов и излагает четыре типа ([PDF, с. 22–23](https://github.com/user-attachments/files/33784962/kodeks_stilya.pdf)). Атрибуция расходится: библиотечный каталог называет автором книги *Die neue Farbberatung*, 1994, Gisela Watermann ([eurobuch](https://www.eurobuch.com/buch/isbn/3806847827.html); [каталог библиотеки Фрайберга](https://www.bibliothek-freiberg.de/title/Title/getTitle/334939)), НИА пишет «Ф. Цингель и Г. Ватерман», версия 0.1 модуля — «М. Ваттерман и А. Цингель». | Карточка 1.9: атрибуция — `PARTIAL`; в RFC v5 на слайде 5 инициалы не ставятся, фамилии даны в форме справочника НИА. | Экземпляр книги 1994 года или немецкий библиотечный каталог с полным списком авторов. |
| 4 | Полный текст Иттена в открытом доступе | **закрыт частично** | Английское издание *The Art of Color* оцифровано в библиотечной коллекции archive.org ([archive.org](https://archive.org/details/artofcolorsubjec00itte)); испанская загрузка v0.1 пользовательская, права не проверены. | Карточка 1.3 ссылается на английское издание; в RFC v5 подвал слайда 4 переведён на него, ссылка на Wikipedia снята. | Ссылка на издание из национального библиотечного каталога. |
| 5 | Надёжность определения цветотипа | **открыт** | Рецензируемых исследований согласия разных стилистов при определении цветотипа одного человека не найдено. Есть эксперименты над логикой цветотипов: выбор тёплых или холодных цветов к лицу устойчив ([Perrett, Sprengelmeyer, 2021](https://doi.org/10.1177/20416695211053361)), но цвет глаз важнее оттенка кожи ([Perrett и соавт., 2023](https://doi.org/10.1037/aca0000626)); практические трудности описаны в российской статье ([Поступаева, 2021](https://cyberleninka.ru/article/n/slozhnosti-opredeleniya-tsvetotipa-vneshnosti)). Корейские количественные модели пытаются измерить цветотип ([Kim и соавт., 2018](https://doi.org/10.5850/JKSCT.2018.42.1.121)). | Сезонные системы — `PARTIAL` и `CONFLICT` в карточках 1.6–1.10. | Исследование межэкспертного согласия при определении цветотипа. |
| 6 | Эффект аксессуаров на первое впечатление | **открыт** | Есть отдельные эффекты: очки ([Leder и соавт., 2011](https://doi.org/10.1024/1421-0185/a000059)), марки люкса ([Nelissen, Meijers, 2011](https://doi.org/10.1016/j.evolhumbehav.2010.12.002)), громкий и тихий логотип ([Han, Nunes, Drèze, 2010](https://doi.org/10.1509/jmkg.74.4.015); [Berger, Ward, 2010](https://doi.org/10.1086/655445)), нонконформизм ([Bellezza и соавт., 2014](https://doi.org/10.1086/674870)). Экспериментальной проверки правил «аксессуар по форме лица» не найдено ни для одной школы. | Правила подбора — **К/П**, статус `?`; научные эффекты — **Э** с `VERIFIED` или `PARTIAL`; в карточках 4.1–4.9 они разведены. | Эксперимент на соответствие формы аксессуара чертам лица. |
| 7 | Система «Larson» из географии поиска #695 | **открыт** | По запросу постановки «системы Kibbe, Larson» искали книги, статьи и пособия с механизмом выбора стиля или типа фигуры под фамилией Larson на английском, французском и итальянском языках: в библиотечной коллекции archive.org, в каталоге Google Books (поиск остановлен лимитом запросов) и в общем веб-поиске. Нашлась только не относящаяся к одежде книга о цвете ауры другого автора; системы стиля, цвета или фигуры под этим именем с первоисточником не найдено. Вся найденная в выдаче информация о типологиях рядом с Kibbe — блоги и журнальные заметки, которые по критерию #695 исключены. | Отдельной карточки нет. Линия ян — инь, в которой обычно упоминаются американские типологии стиля, покрыта первоисточниками: карточка 3.1 (Нортроп — Мортон — Маккимзи) и карточка 3.2 (Кибби). | Название книги или пособия, которое постановка имела в виду под «Larson». |
| 8 | Сайты, недоступные из среды проверки | **открыт** | При проверке ссылок v0.2 каталог Open Library не ответил из среды исследования (соединение не установлено), страница короткого курса London College of Fashion вернула 403 — защита сайта от автоматических запросов. Ссылки ведут на постоянные адреса и сохранены как библиографические; содержание по ним в v0.2 не перепроверялось. | Open Library — только дополнительная библиографическая ссылка рядом с archive.org или страницей издательства; программа LCF — сигнал насыщения в пуле цвета, а не опора утверждения. | Повторная проверка из браузера. |

## 2. Отклонения от постановки

Обе постановки разрешают отклонение, если строгое следование ограничению ухудшает результат. Каждое отклонение ниже сформулировано по правилу постановки: «Я предлагаю скорректировать [Ограничение X], потому что вариант [Y] эффективнее решает задачу [Z]».

### Отклонения v0.1 по #693

1. **Тезис о цвете.** Я предлагаю скорректировать [Ограничение «цвет не сообщает характер, а является гипотезой о первом впечатлении»], потому что вариант [«цвет не сообщает характер; он слабо и в зависимости от контекста сдвигает первое впечатление, поэтому выбор цвета — гипотеза»] эффективнее решает задачу [научно точной карты гипотез]. Исходный тезис подтверждён, но без уточнения его легко прочитать как «цвет ни на что не влияет». Это противоречит данным о сдвиге впечатления ([Elliot, Maier, 2012](https://doi.org/10.1016/B978-0-12-394286-9.00002-0); [Lehmann и соавт., 2018](https://doi.org/10.1177/1474704918802412)).
2. **Атрибуция четырёх типов фигур.** Я предлагаю скорректировать [Ограничение «подход НИА „Гид по стилю“, где рассматривают 4 типа фигур»], потому что вариант [«четыре типа фигур из постановки в логике учебной программы школы; официальное описание не найдено»] эффективнее решает задачу [проверяемости каждого тезиса]. Приписать школе классификацию, которой нет в её открытых материалах, — значит выдать практику за первоисточник.
   **Статус в v0.2: снято.** Первоисточник найден — справочник НИА описывает женские типы фигур с коррекцией ([PDF, с. 33–41](https://github.com/user-attachments/files/33784962/kodeks_stilya.pdf)) и мужские типы ([PDF, с. 41–46](https://github.com/user-attachments/files/33784962/kodeks_stilya.pdf)). Ограничение постановки #693 теперь выполняется буквально: слайд 10 в RFC v5 опирается на первоисточник, а не на программу школы. Текст отклонения сохранён для истории решений.
3. **Искусствоведческие ассоциации стилей.** Я предлагаю скорректировать [Ограничение «учёт искусствоведческих ассоциаций» в виде утверждения], потому что вариант [ассоциации как явно помеченная аналогия рядом с линиями лица и фигуры] эффективнее решает задачу [методологической чистоты]. Параллель «Наивная романтика — рококо» помогает лектору, но не является результатом исследования.
4. **Изображения.** Я предлагаю скорректировать [правило #691 о чередовании тем «архитектура — арт — мода»], потому что вариант [только высокая мода, как требует #693] эффективнее решает задачу [единого визуального языка колоды v4]. Требование #693 новее и прямо говорит «исключительно высокая мода». Архитектурный и арт-слой перенесён в фон и материалы кадра: ар-деко, Баухауз, Neue Sachlichkeit.

### Отклонения v0.2 по #695

5. **Стандарт профиля исследования.** Я предлагаю скорректировать [Ограничение «SSOT: `standards/research-profile.md`»], потому что вариант [действующий стандарт [`standards/research-standard.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/research-standard.md)] эффективнее решает задачу [работы по реально существующему стандарту]. Файла `standards/research-profile.md` в репозитории нет; стандарт исследований с контрактом RRP лежит в `research-standard.md`, и модуль оформлен по нему вместе со [стандартом исполнимого контракта](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/executable-contract-standard.md).
6. **Имя файла RFC.** Я предлагаю скорректировать [Ограничение «имя файла rfc-presentation-update-v5.md»], потому что вариант [2026-11-03-rfc-presentation-update-v5.md в той же папке] эффективнее решает задачу [соответствие стандарту именования файлов research/ (YYYY-MM-DD-name.md), группировка с артефактами Дня 4 и зелёный CI]. Файлы `research/reputation-technologies/` начинаются с даты по [стандарту именования](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/file-naming.md), а дата 2026-11-03 — дата Дня 4, под которой лежат колода v4 и прежние RFC Дня 4. Смысловая часть имени сохранена дословно.
7. **Джексон на слайде 6.** Я предлагаю скорректировать [состав колоды v4 «Иттен, Ваттерман и Цингель, сезонные цветотипы Джексон»], потому что вариант [Иттен, Ватерман и Цингель в изложении НИА, шкала цветовых образов Кобаяси] эффективнее решает задачу [«для презентации отберите 2–3, отражающие принципиально разные подходы»]. Сезонная система Джексон и система Ватерман и Цингель — одна парадигма: обе выводят палитру из природного колорита человека по четырём временам года (карточки 1.7 и 1.9). Кобаяси выводит цвет из образа, который нужно передать аудитории, — это третье основание рядом с цветом как таковым у Иттена и цветом человека у Ватерман и Цингель ([карточка 1.5](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md#ось-1-цвет)).
8. **Моллой на слайде 22.** Я предлагаю скорректировать [состав колоды v4 «аксессуары: ВШСДТ, Школа Туркенич, дресс-код Моллоя»], потому что вариант [НИА «Гид по стилю», элементы и принципы дизайна UKY, громкий и тихий сигнал статуса] эффективнее решает задачу [принципиально разных подходов и опоры на эксперимент]. ВШСДТ и Школа Туркенич по #695 в колоду не идут. Деловая норма аксессуаров теперь представлена первоисточником НИА: главный критерий — соответствие статусу владельца ([PDF, с. 16–18](https://github.com/user-attachments/files/33784962/kodeks_stilya.pdf)), и Моллой с той же логикой «деталь как знак среды» её повторяет. Громкий и тихий сигнал выводит аксессуар из того, кто его читает, и опирается на эксперименты ([карточка 4.7](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md#ось-4-аксессуары)). Моллой остаётся в модуле карточками 3.4 и 4.6.
9. **Метод Трубецковой.** Я предлагаю скорректировать [Ограничение «найти и проанализировать книги Трубецковой, описать как отдельный метод»] в части авторства, потому что вариант [«метод Трубецковой и Найденской», названный в тексте по первому автору, как в постановке] эффективнее решает задачу [точной атрибуции]. Основные книги метода написаны в соавторстве Инессы Трубецковой и Наталии Найденской ([страница авторов в Эксмо](https://eksmo.ru/authors/naydenskaya-n-g-trubetskova-i-a-ID10677/)); приписать соавторскую формулу одному автору — неточность. В v0.1 инициалы авторов были даны с ошибкой («Е.» и «И.»); в v0.2 они исправлены по страницам издательств.
10. **Блоги и файловые библиотеки в опоре v0.1 и v4.** Я предлагаю скорректировать [решение v0.1 и колоды v4 опирать таблицу шести стилей и аксессуары на практические публикации], потому что вариант [снять блоги, личные журналы и файловые библиотеки с опоры и заменить их первоисточниками] эффективнее решает задачу [критерия #695 «блоги исключаются»]. Что снято и чем заменено — в разделе «[Исключённые источники](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md#исключённые-источники)» таксономии и в разделе 4 ниже.
11. **Размеченный уровень опоры на слайде.** Я предлагаю скорректировать [формат строки «Вывод» на слайдах технологий v4 — только уровень опоры **Э / К / П / А**], потому что вариант [уровень опоры и профиль GRA-статусов технологии в одной строке] эффективнее решает задачу [этапа 2 #695 — разметки достоверности утверждений]. Слушатель видит не только откуда правило, но и проверено ли оно, а статусы `PARTIAL` и `CONFLICT` сопровождаются формулой постановки о контексте. Статусы — эпистемическая проверка утверждений, они не используются для выбора образа.

Решений, которые нарушают абсолютные запреты постановок, нет. Логика и термины модели сбора данных курса к выбору образа не применяются: GRA-статусы проверяют утверждения технологий, а не выбирают цвет, линию или стиль. Кейсы курса стоят только в трёх слайдах сборки и в [`40-practice-and-cases.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/40-practice-and-cases.md). Колода v4 не перегенерирована: изменения описаны в [RFC к презентации v5](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-11-03-rfc-presentation-update-v5.md).

## 3. Самоаудит по постановке

### Самоаудит по #695

| Требование #695 | Где выполнено |
| --- | --- |
| Подтвердить получение и полный анализ PDF | [`00-introduction.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/00-introduction.md#этап-1-отчёт-о-найденных-методиках-и-авторах), карта 82 страниц по главам |
| Глубокий поиск: США, Италия, Франция и Россия; программы школ дизайна и стилистов | пулы кандидатов и разделы «Насыщение поиска» на каждой оси [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md) |
| Критерий технологии: источник и механизм; блоги исключены | [`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/10-theory.md#1-что-считается-технологией); [исключённые источники](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md#исключённые-источники) |
| Не менее шести технологий на ось, стоп по насыщению | 14 / 15 / 9 / 9 карточек при пулах 23 / 27 / 26 / 26 кандидатов; признаки насыщения — в конце каждой оси |
| Две-три принципиально разные технологии на ось для презентации | раздел «Выбор для презентации» каждой оси в `20-taxonomy.md`; диффы — в RFC v5 |
| НИА «Гид по стилю»: стили, типы фигур М/Ж, коррекция, без повтора цвета, без авторов, обязательная формулировка | карточки 1.9, 2.14, 2.15, 3.8, 4.9; в RFC v5 — слайды 5, 10, 14, 16, 20 |
| ВШСДТ и Школа Туркенич — данность, не в колоду | строки «данность» в пулах `20-taxonomy.md`; в RFC v5 слайды 14, 15, 20 и 21 переведены на другие технологии |
| Беляева-Экземплярская — отдельная технология | карточка 2.2 |
| Трубецкова — отдельный метод по книгам | карточка 3.9 |
| GRA-разметка VERIFIED / PARTIAL / CONFLICT / ? для каждой технологии | таблица «GRA-разметка» и «Профиль статусов» в каждой из 47 карточек; логика — [`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/10-theory.md#8-gra-разметка-достоверности-утверждений) |
| GRA не диктует выбор образа | правило разметки в `20-taxonomy.md` и `10-theory.md`; проверка терминов модели сбора данных в чекере RFC |
| RFC: обоснование, таблица замен, визуальные правила | [RFC к презентации v5](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-11-03-rfc-presentation-update-v5.md) |
| Колода v4 не перегенерирована | файл v4 в PR не изменён |
| Полные URL | все ссылки модуля и RFC — полные адреса; проверка — чекер RFC |

### Самоаудит по #693

| Требование #693 | Где выполнено |
| --- | --- |
| Исследование по контракту RRP в отдельном модуле | этот модуль, файлы `00`–`50` |
| Изучены вложения: диалог и PDF-образец | [`00-introduction.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/00-introduction.md#этап-1-отчёт-о-найденных-методиках-и-авторах) |
| Цвет: Иттен и Ваттерман — Цингель; проверка тезиса | [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md#ось-1-цвет); [`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/10-theory.md#3-проверка-тезиса-о-цвете) |
| Форма: Беляева-Экземплярская и «Гид по стилю» | [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md#ось-2-форма) |
| Стиль: ВШСДТ и «Гид по стилю», шесть стилей, черты лица, линии, искусство | [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md#шесть-стилей-черты-лица-линии-и-искусство) |
| Аксессуары: ВШСДТ против «подбора в тон» | [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md#ось-4-аксессуары) |
| От двух до четырёх технологий на ось | три на каждую ось; критерии — в `20-taxonomy.md` |
| Интерпретация через гармонию и контраст | [`30-decision-framework.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/30-decision-framework.md) |
| Четыре аналитических маркера как управленческие выводы | `30-decision-framework.md`, таблицы «Аналитические маркеры» |
| Три сценария сборки на кейсах курса | [`40-practice-and-cases.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/40-practice-and-cases.md) |
| Колода Gamma v4 | [`2026-11-03-day4-presentation-gamma-v4.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-11-03-day4-presentation-gamma-v4.md) |

**Вне постановки.** Сценарий лектора к v4 и v5 постановки не запрашивают. Колода самостоятельна: каждый слайд читается без речи лектора.

## 4. Источники

Полные списки источников по каждой технологии стоят в карточках и в таблицах «Пул» четырёх осей [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md). Здесь собраны общие источники модуля и опора технологий, выбранных в колоду.

### Первое впечатление, самопрезентация, мода

- Goffman E. *The Presentation of Self in Everyday Life*. 1959 — [archive.org](https://archive.org/details/the-presentation-of-self-in-everyday-life-the-presentation-erving-goffman-1959-a)
- Willis J., Todorov A. First impressions: making up your mind after a 100-ms exposure to a face. *Psychological Science*, 2006 — [PubMed](https://pubmed.ncbi.nlm.nih.gov/16866745/)
- Howlett N. et al. The influence of clothing on first impressions. *Journal of Fashion Marketing and Management*, 17(1), 2013, 38–48 — [doi:10.1108/13612021311305128](https://doi.org/10.1108/13612021311305128)
- Horton, Adam H., Galinsky A. D. Evaluating the Evidence for Enclothed Cognition: Z-Curve and Meta-Analyses. *Personality and Social Psychology Bulletin*, 2023 — [doi:10.1177/01461672231182478](https://doi.org/10.1177/01461672231182478)
- Adam H., Galinsky A. D. Enclothed cognition. *Journal of Experimental Social Psychology*, 48(4), 2012 — [doi:10.1016/j.jesp.2012.02.008](https://doi.org/10.1016/j.jesp.2012.02.008)
- Simmel G. Fashion. *American Journal of Sociology*, 62(6), 1957, 541–558 — [doi:10.1086/222102](https://doi.org/10.1086/222102)
- Blumer H. Fashion: From Class Differentiation to Collective Selection. *The Sociological Quarterly*, 10(3), 1969, 275–291 — [doi:10.1111/j.1533-8525.1969.tb01292.x](https://doi.org/10.1111/j.1533-8525.1969.tb01292.x)
- Pantone Color of the Year 2026 Cloud Dancer — [NBC News](https://www.nbcnews.com/pop-culture/pop-culture-news/pantone-names-2026-color-year-rcna247366)

### Векторы: гармония и контраст

- Brewer M. B. The Social Self: On Being the Same and Different at the Same Time. *PSPB*, 17(5), 1991, 475–482 — [doi:10.1177/0146167291175001](https://doi.org/10.1177/0146167291175001)
- Chartrand T. L., Bargh J. A. The Chameleon Effect. *JPSP*, 76(6), 1999 — [PDF](https://pages.ucsd.edu/~pwinkiel/chameleon.pdf)
- Burgoon J. K., Hale J. L. Nonverbal Expectancy Violations. *Communication Monographs*, 55(1), 1988, 58–79 — [doi:10.1080/03637758809376158](https://doi.org/10.1080/03637758809376158)
- Burgoon J. K. Expectancy Violations Theory. 2015 — [University of Arizona](https://experts.arizona.edu/en/publications/expectancy-violations-theory/)
- Bellezza S., Gino F., Keinan A. The Red Sneakers Effect. *Journal of Consumer Research*, 41(1), 2014, 35–54 — [doi:10.1086/674870](https://doi.org/10.1086/674870)
- Wölfflin H. *Principles of Art History* — [archive.org](https://archive.org/details/princarth00wlff)

### Первоисточник НИА «Гид по стилю»

- «Кодекс стиля. Справочник делового дресс-кода». НИА «Гид по стилю», 2007, 82 с. — [PDF](https://github.com/user-attachments/files/33784962/kodeks_stilya.pdf). Технологии, используемые в НИА "Гид по стилю" (на базе которых впоследствии образовался ряд профильных школ): цвет — с. 8–10 и 22–32, типы фигур — с. 33–46, аксессуары — с. 16–18 и 47–49, стили — с. 50–62, типичные ошибки — с. 63–69, мода — с. 70–73. Имена авторов справочника в модуле не воспроизводятся.

### Цвет

- Itten J. *The Art of Color: The Subjective Experience and Objective Rationale of Color*. 1961 — [archive.org](https://archive.org/details/artofcolorsubjec00itte); [Open Library](https://openlibrary.org/works/OL3134338W)
- Kobayashi S. The aim and method of the Color Image Scale. *Color Research & Application*, 6(2), 1981 — [doi:10.1002/col.5080060210](https://doi.org/10.1002/col.5080060210); *Color Image Scale*. 1991 — [archive.org](https://archive.org/details/colorimagescale00koba)
- *Die neue Farbberatung*. Falken, 1994 — [каталог библиотеки Фрайберга](https://www.bibliothek-freiberg.de/title/Title/getTitle/334939); [eurobuch](https://www.eurobuch.com/buch/isbn/3806847827.html); атрибуция — пробел 3
- Курс «Колористика для стилистов. Система 16 колоритов» — [программа](https://tatyana-mamenko.ru/services/stylist/kurs-koloristika-dlya-stilistov/)
- Jackson C. *Color Me Beautiful*. 1980 — [archive.org](https://archive.org/details/colormebeautiful00jack_2); [Open Library](https://openlibrary.org/works/OL4995954W)
- Caygill S. *Color: The Essence of You*. 1980 — [Cornell eCommons](https://ecommons.cornell.edu/handle/1813/55002)
- Поступаева. Сложности определения цветотипа внешности. 2021 — [КиберЛенинка](https://cyberleninka.ru/article/n/slozhnosti-opredeleniya-tsvetotipa-vneshnosti)
- Perrett D. I., Sprengelmeyer R. Clothing Aesthetics: Consistent Colour Choices to Match Fair and Tanned Skin Tones. *i-Perception*, 12(6), 2021 — [doi:10.1177/20416695211053361](https://doi.org/10.1177/20416695211053361); Perrett D. I. et al. Eye color is more important than skin color for clothing color aesthetics. *Psychology of Aesthetics, Creativity, and the Arts* — [doi:10.1037/aca0000626](https://doi.org/10.1037/aca0000626)
- Elliot A. J., Maier M. A. Color-in-Context Theory. *Advances in Experimental Social Psychology*, 45, 2012, 61–125 — [doi:10.1016/B978-0-12-394286-9.00002-0](https://doi.org/10.1016/B978-0-12-394286-9.00002-0)
- Labrecque L. I., Milne G. R. Exciting red and competent blue. *JAMS*, 40, 2012, 711–727 — [doi:10.1007/s11747-010-0245-y](https://doi.org/10.1007/s11747-010-0245-y)
- Lehmann G. K., Elliot A. J., Calin-Jageman R. J. Meta-Analysis of the Effect of Red on Perceived Attractiveness. *Evolutionary Psychology*, 16(4), 2018 — [doi:10.1177/1474704918802412](https://doi.org/10.1177/1474704918802412)

### Форма

- Беляева-Экземплярская С. Н. *Моделирование одежды по законам зрительного восприятия*. 1934; переиздания 1996, 2016 — [URSS](https://urss.ru/cgi-bin/db.pl?lang=Ru&blang=ru&page=Book&id=325972)
- Simmons K., Istook C. L. Body measurement techniques. *Journal of Fashion Marketing and Management*, 7(3), 2003 — [doi:10.1108/13612020310484852](https://doi.org/10.1108/13612020310484852)
- Sokolowski S., Bettencourt C. Modification of the Female Figure Identification Technique (FFIT) Formulas to Include Plus Size Bodies. *3DBODY.TECH*, 2020 — [doi:10.15221/20.22](https://doi.org/10.15221/20.22)
- Thompson P., Mikellidou K. Applying the Helmholtz illusion to fashion. *i-Perception*, 2(1), 2011, 69–76 — [doi:10.1068/i0405](https://doi.org/10.1068/i0405)
- Koutsoumpis A. et al. 2021 — [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8438770/)
- Шипков. 2017 — [статья](https://zh-szf.ru/en/nauka/article/19053/jats)
- ВШСДТ — [программа стилиста-консультанта](https://styleschool.ru/education/style-consultant) (данность)
- Школа Туркенич — [программа имиджмейкера-стилиста](https://style-school.com/training/imagemaker/stylist) (данность)

### Стиль

- McJimsey H. T. *Art in Clothing Selection*. 1963 — [archive.org](https://archive.org/details/artinclothingsel0000mcji); *Art and Fashion in Clothing Selection*. 1973 — [archive.org](https://archive.org/details/artfashioninclot00harr)
- Kibbe D. *Metamorphosis*. 1987 — [archive.org](https://archive.org/details/bwb_0-689-11847-3); [Open Library](https://openlibrary.org/works/OL4972581W)
- Трубецкова И., Найденская Н. «Золотые правила стиля. Дресс-код успешной женщины». Эксмо, 2016 — [страница издательства](https://eksmo.ru/book/zolotye-pravila-stilya-dress-kod-uspeshnoy-zhenshchiny-ITD816396/); «Мода. Цвет. Стиль». Эксмо, 2011 — [страница издательства](https://eksmo.ru/book/moda-tsvet-stil-ITD87445/); «Код внешности от головы до пальцев ног». АСТ — [страница издательства](https://ast.ru/book/kod-vneshnosti-ot-golovy-do-paltsev-nog-856038/); «Грамотный гардероб». АСТ — [страница издательства](https://ast.ru/book/gramotnyy-garderob-must-have-dlya-tekh-kto-khochet-byt-stilnym-833512/); «Фигура & лицо». АСТ, 2021 — [страница издательства](https://ast.ru/book/figura-litso-podcherkni-dostoinstva-i-skroy-nedostatki-praktikum-856589/)
- ВШСДТ — [программа fashion-стилиста](https://styleschool.ru/education/fashion-stylist) (данность)

### Аксессуары

- Baker M. M. *Accessories: The Finishing Touch*. University of Kentucky Cooperative Extension Service, FCS2-347, 2020 — [PDF](https://publications.mgcafe.uky.edu/sites/publications.ca.uky.edu/files/FCS2347.pdf)
- Han Y. J., Nunes J. C., Drèze X. Signaling Status with Luxury Goods: The Role of Brand Prominence. *Journal of Marketing*, 74(4), 2010 — [doi:10.1509/jmkg.74.4.015](https://doi.org/10.1509/jmkg.74.4.015)
- Berger J., Ward M. Subtle Signals of Inconspicuous Consumption. *Journal of Consumer Research*, 37(4), 2010 — [doi:10.1086/655445](https://doi.org/10.1086/655445)
- Molloy J. T. *Dress for Success*. 1975 — [Open Library](https://openlibrary.org/works/OL3266029W)
- Nelissen R. M. A., Meijers M. H. C. Social benefits of luxury brands as costly signals of wealth and status. *Evolution and Human Behavior*, 32(5), 2011, 343–355 — [doi:10.1016/j.evolhumbehav.2010.12.002](https://doi.org/10.1016/j.evolhumbehav.2010.12.002)
- Leder H., Forster M., Gerger G. The Glasses Stereotype Revisited. *Swiss Journal of Psychology*, 70(4), 2011, 211–222 — [doi:10.1024/1421-0185/a000059](https://doi.org/10.1024/1421-0185/a000059)

### Исключённые ссылки v0.1

По критерию #695 «блоги исключаются» из списка источников v0.1 сняты: публикация магазина украшений о стилевых типажах, три записи личных журналов о шести стилях, страница файловой библиотеки с книгами справочника НИА, страница Wikipedia об Иттене как ссылка «об авторе», страницы читательского каталога и книжного магазина о книгах Беляевой-Экземплярской и Трубецковой. Адреса снятых публикаций и то, чем они заменены, — в разделе «[Исключённые источники](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/image-technologies/20-taxonomy.md#исключённые-источники)» таксономии. Страница выпускников МПГУ о Беляевой-Экземплярской и старый адрес URSS по протоколу http заменены постоянной страницей издания на URSS по https.
