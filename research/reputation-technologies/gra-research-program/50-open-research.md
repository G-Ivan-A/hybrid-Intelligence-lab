---
status: draft
version: 0.1
updated: 2026-10-10
temperature: 0.6
type: research
context: [reputation-technologies, gra, research-program, open-questions, sources, self-audit]
method: gap-analysis + source-traceability
scope: reputation-technologies
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/657"
based_on:
  - research/reputation-technologies/gra-research-program/10-theory.md
  - research/reputation-technologies/gra-research-program/20-taxonomy.md
  - research/reputation-technologies/gra-research-program/30-decision-framework.md
  - research/reputation-technologies/gra-research-program/40-practice-and-cases.md
related_artifacts:
  - "research/reputation-technologies/2026-09-30-course-sources-and-presentations-650.md"
  - "research/reputation-technologies/2026-10-07-day1-rationale-and-method-653.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/657"
---

# Открытые вопросы, пробелы корпуса, словарь и источники

> **Модуль.** Файл `50-open-research.md` модуля
> [`research/reputation-technologies/gra-research-program/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/research/reputation-technologies/gra-research-program).
> Здесь собрано то, чего программа пока не знает, и то, что в корпусе
> репозитория расходится с модулем.

## 1. Открытые вопросы

| ID | Вопрос | Связанная гипотеза | Что нужно для ответа |
| --- | --- | --- | --- |
| OQ-1 | Независимы ли физическая (D1) и информационная (D2) оси дистанции? | HD1, MVP-требование «минимум две оси» | Кейсы, где D1 и D2 расходятся: далеко, но с каналом; близко, но без канала |
| OQ-2 | Нужно ли сводить оси дистанции в одно число, и если да, то как? | HD3, H3 | Сравнение моделей с раздельными осями и со свёрткой по K3 и K6 |
| OQ-3 | Как агрегировать массу системы (холдинг, ассоциация, клан) из масс её частей? | §3.2 таксономии | Кейсы с известной внутренней структурой агрегата |
| OQ-4 | Как наблюдать направление потока (P2, P3)? | HP-D, H4 | Кандидаты: кто кого пересылает, цитирует, приглашает; согласие разметчиков (K2) |
| OQ-5 | Какая степень дистанции в социальных данных — 2, 1 или иная? Различимы ли H1 и H2 при малых данных? | H1, H2 | Количественные данные о взаимодействиях; ориентир — α ≈ 1 в торговле `[650:Г3]` |
| OQ-6 | Устойчивее ли структурные модели при переносе между контекстами, чем экспертная оценка и статистика? | HS | Одни и те же кейсы, три метода, сравнение ошибок прогноза |
| OQ-7 | Есть ли инерция массивных узлов и устойчив ли лаг «поле → рынок» (в отчёте фаундера — 30–180 дней)? | HM-I | Временные ряды событий поля и рыночных показателей |
| OQ-8 | Достижима ли надёжная порядковая разметка массы и дистанции двумя независимыми людьми? | K2 | Двойная разметка кейсов соисследователей |
| OQ-9 | Объясняет ли модель конкурентных возможностей (H5) исходы лучше гравитационных? | H5 | Кейсы, где между узлами есть альтернативные посредники |
| OQ-10 | Какие ещё физические или математические структуры дают проверяемые отношения уровня L1? | Эвристика программы | Регулярный разбор аналогий по таблице §6 таксономии |

## 2. Ранжирование гипотез для первой проверки

Порядок задан тем, что можно проверить на кейсах соисследователей Дня 1 без
больших данных.

| Ранг | Гипотеза | Почему первой | Минимальные данные |
| --- | --- | --- | --- |
| 1 | Структурная гипотеза против H0 (K3) | Это главная гипотеза (в) таблицы трассировки Дня 1; её проверяют все кейсы | 1–2 кейса соисследователей с исходом |
| 2 | HP-D, направленность | Кейсы Б и В на неё опираются; качественно проверяема | Те же кейсы + разметка «кто кому передаёт» |
| 3 | HD1, независимость D1 и D2 | MVP-требование зависит от ответа | Кейсы с расхождением D1 и D2 |
| 4 | Разведение массы и влияния (T4) | Проверяется разметкой, не требует чисел | Двойная разметка |
| 5 | H1 против H2, HS, HM-I | Требуют количественных данных и временных рядов | Отдельный исследовательский проект |

## 3. Пробелы корпуса

Ранние артефакты GRA содержат формулировки, которые модуль исправляет. По
условиям задачи #657 они не редактировались: правка ограничена SSOT Дня 1.
Расхождения зафиксированы здесь и вынесены в предложение §5.

| Артефакт | Место | Формулировка | Расхождение с модулем |
| --- | --- | --- | --- |
| [Отчёт о концепции фаундера](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-20-founders-vision-and-framework.ru.md) | Раздел о формуле и научных основаниях | «Это соединяет гравитационную модель торговли (Tinbergen, 1962) и анализ силового поля»; «Научные основания: Gravity Model of Trade (Tinbergen, 1962) для «масса/дистанция²»» | Генеалогия (F1): торговая модель — параллельный прецедент. Квадрат дистанции у Тинбергена не заложен `[650:Г1]` |
| Тот же отчёт | Лаг «поле опережает рынок» | 30–180 дней как свойство поля | Это гипотеза HM-I, OQ-7 |
| [White paper (en)](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-20-white-paper.en.md) | Описание модели | «This unifies the Gravity Model of Trade (Tinbergen, 1962) with Force Field Analysis» | F1 |
| [Framework standard (en)](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-20-framework-standard.en.md) | Описание модели | «Grounded in the Gravity Model of Trade (Tinbergen, 1962)» | F1, F2 |
| [Глоссарий ru-en](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-20-glossary.ru-en.md) | Статьи «Масса», «Дистанция», «Гравитация» | Дистанция «обратна доверию»; масса и гравитация со ссылкой на Gravity Model (Tinbergen 1962) | F3, F1 |

## 4. Словарь

| Термин | Значение в модуле |
| --- | --- |
| Структурное соответствие | Совпадение отношений (не свойств) между физической или математической системой и социальной системой; предмет исследования GRA, а не её предпосылка |
| Лестница переноса | L0 закономерность → L1 структура → L2 социальная гипотеза → L3 прикладная модель; каждый переход — отдельная гипотеза |
| Ядро программы | Утверждение, которое пересматривается последним; тоже гипотеза |
| Защитный пояс | Операционализации, формы модели, степени, аналогии; пересматриваются в первую очередь |
| Операционализация | Способ сделать конструкт наблюдаемым: индикатор, источник данных, шкала |
| Базовая линия H0 | Оптика образа: охват и тональность. С ней сравнивается любая модель GRA |
| Гипотеза H1 | Формула фаундера F(t) = (M_A × M_B) / D² × P(t); один из кандидатов на модель связи |
| Направленность (HP-D) | Гипотеза: связь A→B не равна B→A, сигнал против потока среды без достаточной массы не достигает цели |
| Масса и влияние | Масса — наблюдаемые характеристики узла; влияние — масса относительно конкретного решения |
| Предварительная проверка ИИ | Вывод ИИ-агента на доступных данных; не эмпирическое подтверждение |

## 5. Предложения

> **Я предлагаю скорректировать ранние артефакты GRA (отчёт о концепции фаундера, white paper, framework standard, глоссарий), потому что вариант «исправить только День 1» оставляет в корпусе неверную генеалогию и формулу «дистанция = обратное доверие», а вариант «синхронизировать корпус отдельной задачей» эффективнее решает задачу единого источника истины: правки в ранних документах затрагивают двуязычные тексты и требуют решения фаундера, а не исполнителя Дня 1.** Перечень мест — §3.

> **Я предлагаю скорректировать порядок исследований, начав с проверки структурной гипотезы против базовой линии H0 на кейсах соисследователей, потому что вариант «сначала откалибровать формулу H1» эффективнее отложить: для калибровки нужны количественные данные, которых у лаборатории нет, а сравнение с H0 даёт ответ на главный вопрос программы уже на одном-двух кейсах.** Ранжирование — §2.

## 6. Источники

Ссылки `[650:X]` ведут на проверенные записи
[исследования #650](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-09-30-course-sources-and-presentations-650.md),
раздел «Источники», ссылки `[653:X]` — на раздел «Источники»
[обоснования Дня 1](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-10-07-day1-rationale-and-method-653.md#источники).
Там приведены библиография, страницы, цитаты и статусы. Модуль использует
`[650:Г1]`, `[650:Г2]`, `[650:Г3]`, `[650:Г5]`, `[650:Г6]`, `[650:Г8]`,
`[650:Г9]`, `[650:Г10]`, `[650:Г11]`, `[650:Г12]`, `[650:Г13]`, `[650:Г16]`,
`[653:М2]`, `[653:М3]`, `[653:М5]`, `[653:М6]`, `[653:М7]`, `[653:М8]`.

Новые источники модуля проверены 2026-10-10. Переводы и пересказы наши.

**Статусы:**

- VERIFIED-FULLTEXT — фраза сверена с текстом аннотации или страницы
  первоисточника;
- VERIFIED-SECONDARY — содержание взято из названного вторичного источника,
  потому что первоисточник закрыт; приводится пересказ, не цитата;
- BIBLIOGRAPHIC — подтверждена только библиографическая запись по вторичным
  источникам; используется как факт существования и общей идеи работы, без
  цитат и номеров страниц.

| ID | Источник | Что используется | Статус |
| --- | --- | --- | --- |
| R:Simini | Simini F., González M. C., Maritan A., Barabási A.-L. A universal model for mobility and migration patterns // Nature. 2012. Vol. 484. P. 96–100. arXiv:1111.0586: https://arxiv.org/abs/1111.0586 | О гравитационной модели: «Despite its widespread use, it relies on adjustable parameters that vary from region to region»; о предлагаемой модели: «Given its parameter-free nature, the model can be applied in areas where we lack previous mobility measurements» | VERIFIED-FULLTEXT (аннотация arXiv; nature.com требует авторизации) |
| R:Gentner | Gentner D. Structure-Mapping: A Theoretical Framework for Analogy // Cognitive Science. 1983. Vol. 7, No. 2. P. 155–170 | По обзору: «Argues that the core of analogy is the mapping of relationships»; «the key to analogy is not just relationships but systems of interconnected relationships». Пересказ наш: переносятся отношения между объектами, а не их свойства | VERIFIED-SECONDARY (обзор CogSci Summaries: https://www.jimdavies.org/summaries/gentner1983.html; PDF первоисточника не извлечён) |
| R:Lakatos | Lakatos I. Falsification and the Methodology of Scientific Research Programmes // Lakatos I., Musgrave A. (eds.). Criticism and the Growth of Knowledge. Cambridge: Cambridge University Press, 1970 | Пересказ: ядро и защитный пояс; прогрессивный и вырождающийся сдвиг проблем | VERIFIED-SECONDARY (пересказ по справочным обзорам; первоисточник не открыт) |
| R:Wilson | Wilson A. G. A statistical theory of spatial distribution models // Transportation Research. 1967. Vol. 1. P. 253–269 | Факт: гравитационная модель пространственного взаимодействия выводится из максимизации энтропии, без ньютоновской аналогии | BIBLIOGRAPHIC |
| R:Zipf | Zipf G. K. The P1 P2/D Hypothesis: On the Intercity Movement of Persons // American Sociological Review. 1946. Vol. 11, No. 6. P. 677–686 | Факт: поток между городами пропорционален произведению населений и обратно пропорционален расстоянию в первой степени | BIBLIOGRAPHIC |
| R:Stewart | Stewart J. Q. Demographic Gravitation: Evidence and Applications // Sociometry. 1948 | Факт: «социальная физика» Стюарта переносит ньютоновскую форму N₁N₂/d² на взаимодействие населённых пунктов | BIBLIOGRAPHIC (выходные данные тома и страницы не сверены) |

## 7. Самоаудит против условий задачи #657

| Требование | Где выполнено |
| --- | --- |
| RRP-исследование с полным методологическим обоснованием GRA как открытой программы | Шесть файлов модуля; выбор M2 — в [00-introduction.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/00-introduction.md#почему-модель-m2-rrp-а-не-m3) |
| GRA возникла как гипотеза о структурных аналогах | [10-theory.md, §1](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/10-theory.md#1-происхождение-gra) |
| GRA не наследует физические законы, а исследует соответствие | [10-theory.md, §2](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/10-theory.md#2-принцип-структурного-соответствия) |
| Роль ИИ-агентов и независимая проверка | [10-theory.md, §6](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/10-theory.md#6-роль-ии-агентов), [30-decision-framework.md, §5](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/30-decision-framework.md#5-гейт-для-выводов-ии-агентов) |
| Восемь правок SSOT Дня 1 | [Обоснование и метод Дня 1](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-10-07-day1-rationale-and-method-653.md), таблица статусов; соответствие правок формулировкам — [30-decision-framework.md, §2](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/30-decision-framework.md#2-формулировки-запрещённые-и-допустимые) |
| Синхронизация презентации и сценария | [Презентация](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-10-07-day1-presentation-653.md), [сценарий лектора](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-10-07-day1-lecturer-script-653.md) |
| Неизменные элементы Дня 1 | [30-decision-framework.md, §6](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/30-decision-framework.md#6-уровень-аудитории), решение A7 |
| Абсолютные ссылки | Все ссылки модуля абсолютные |
