---
status: draft
version: 0.2
updated: 2026-10-19
temperature: 0.2
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/689"
scope: reputation-engineering-course-days1-4
method: ai-interpretation-failure-analysis
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/685"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/687"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/683"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/681"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/671"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/669"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/657"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/653"
---

# Дни 1–4. Разбор провала интерпретации ИИ: как GRA вышла за свои границы

**Файл 2 из трёх по issue [#689](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/689).** Здесь разобрано, где ИИ-исполнитель применил GRA к имидж-технологиям, к решениям и к самому лектору. Разбор охватывает все четыре дня курса, как просил фаундер в [комментарии к PR #690](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/690#issuecomment-6265128986): «Нужна независимая оценка провалов и правильных интепретаций для дальнейшей отладки». Это касается и Дней 1 и 2, которые фаундер считает сформированными корректно.

Остальные файлы:

- [Вариант 2 обоснования Дня 4](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-11-03-day4-rationale-and-method-v2.md) — перечень имидж-технологий;
- [RFC: что делать с презентациями](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-11-03-day4-crisis-mitigation-rfc.md) — прежде всего правки колод Дней 1–3, уже созданных в Gamma;
- [колода Дня 4, вариант 2](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-11-03-day4-presentation-gamma-v2.md) — исправленная колода; в Gamma День 4 ещё не генерировался.

[Вариант 1 обоснования](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md) и [колода Дня 4, вариант 1](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-11-03-day4-presentation-gamma.md) не изменены. Это исторические документы провала.

Все 228 найденных нарушений и 65 верных интерпретаций собраны в реестре [`findings-days-1-4-689.json`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/exp/day4-correction-689/findings-days-1-4-689.json). У каждой записи есть файл, строка, место на слайде, тип нарушения, степень, дословная цитата и предложенная замена. Ниже приведены главные примеры. Реестр нужен для дальнейшей отладки.

## Источник разбора

**Диалог фаундера.** Фаундер приложил диалог к [комментарию в PR #690](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/690#issuecomment-6265128986). Он сохранён в ветке коммитом `16415e9` как `2026-10-19-founder-dialog-689.txt` — 200 строк, прочитаны все. Все цитаты ниже — постоянные ссылки на строки файлов в этом коммите, вида [диалог:20](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L20) «GRA запрещено применять к имидж-технологиям». После коммита трёх файлов сам файл диалога удалён из ветки (пункт 7 гейта). Ссылки на коммит при этом продолжают открываться.

В версии 0.1 этого файла было записано отклонение: «прикреплённого файла нет». На тот момент файла действительно не было ни в issue, ни в ветке. Фаундер приложил его позже, к PR. Отклонение отозвано, разбор переписан по диалогу.

**Раскоп первоначальных постановок.** Фаундер просил: [диалог:31](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L31) «пусть раскопает мои первоначальные постановки». Как постановки описывали GRA, от первой к последней:

| Постановка | Что сказано о GRA | Граница |
|---|---|---|
| [#653](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/653), строка 18 | «Язык GRA: масса, дистанция, полярность — как эвристика для вопросов» | Соблюдена |
| [#657](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/657), строка 44 | «GRA формирует структурированное поле связей и гипотез. Выбор конкретной стратегии остается отдельной задачей» | Соблюдена: решение отделено от данных |
| [#669](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/669), строка 24 | «давайте МИРНО посмотрим на то, какую информацию мы можем собрать (в том числе с использованием ИИ) и проанализировать» | Соблюдена: сбор и анализ |
| [#671](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/671), строка 94 | «GRA — это система guardrails (ограничителей) для калибровки ИИ-промптов и структурирования гипотез» | Соблюдена |
| [#681](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/681), строка 88 | «Механика GRA помогает найти именно точку влияния» | Пограничная: «найти» можно прочесть как «выбрать» |
| [#685](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/685), строки 32, 48, 90 | «Ключевое правило (через GRA): Открытая эклектика допустима ТОЛЬКО при полярности +1, малой дистанции и высокой массе»; «выбор гармонии/эклектики на основе GRA (полярность, дистанция, масса)» | Нарушена в самой постановке |

Первоначальные постановки держали границу. Формула #657 почти дословно совпадает с тем, что фаундер повторил в диалоге: [диалог:175](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L175) «GRA - омдель для сбора и интепретации данных Агентом, чтобы их классифицировать, структурировать и сохранить, ВСЕЕЕЕ».

Подмену первым записал не фаундер, а ИИ. Фраза «Стратегию выбирают полярность, дистанция и масса» появилась в RFC в коммите `269e48c` по #669. Правило «гармония или эклектика зависит от полярности, дистанции и массы» — в коммите `e67cb49` по #671. Постановка #685 взяла эти слова из RFC v0.3 и прямо на него сослалась (строка 90: «Логика Дня 4 строго следует RFC v0.3»). Исполнитель #685 не сказал, что постановка противоречит границе #657. Это его ошибка, разобранная в разделе 4.

## Граница: что делает каждая модель

| Модель или инструмент | Что делает | Чего не делает | Основание в диалоге |
|---|---|---|---|
| **GRA** | Агент собирает, классифицирует, структурирует и сохраняет данные о связях. Три вопроса — масса, дистанция, полярность — дают векторное описание связи. Guardrails для промптов | Не выбирает стиль, цвет, тон, вид шага, канал, точку | [диалог:21](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L21) «GRA - модель в помощь СБОРА и интепрлретации данных, ВСЕЕЕЕЕЕ!»; [диалог:175](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L175) «классифицировать, структурировать и сохранить» |
| **Статусы данных** `VERIFIED`, `PARTIAL`, `CONFLICT` | Отдельный инструмент Дня 2: состояние наших знаний о факте | Это не GRA. Не выбирают шаг за человека | [диалог:155](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L155) «3. Статусы данных (VERIFIED/PARTIAL/CONFLICT) — это НЕ GRA» |
| **Фильтр Дня 3** | Критерии: доступность, значимость, качество, полезность | Это не GRA и не «три вопроса GRA» | [диалог:106](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L106) «Это критерии фильтра, не GRA» |
| **Принятие решений** | Человек или агент по другой модели | Не выводится из GRA и не сводится к таблице «значение → решение» | [диалог:21](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L21) «Принятие решений на базе данных - человек или АГЕНТ - это другие модели!» |
| **Имидж-технологии** | Отдельная область: соответствие, гармония, эклектика, цвет, линия, фактура | Не рассчитываются через GRA | [диалог:20](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L20) «GRA запрещено применять к имидж-технологиям» |
| **Связка «потому что → поэтому»** | Переход между слайдами в сценарии лектора | Не обосновывает технологию внутри слайда | [диалог:158](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L158) «Используются ТОЛЬКО для перехода между слайдами в сценарии лектора.» |
| **Лектор** | На Дне 1 согласовал сбор и описание открытых данных о себе | На Днях 2–4 не применяет к себе ни GRA, ни статусы | [диалог:190](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L190) «нет, лектор ВООБЩЕ к себе это не применяет,»; [диалог:191](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L191) «Лектор тольеко в первый день СОГЛАСОВАЛ» |

**Типы нарушений в реестре:**

- **Н1** — GRA выбирает стиль, образ, имидж;
- **Н2** — GRA или статус данных выбирает решение: кого выбрать, что делать;
- **Н3** — связка «потому что → поэтому» обосновывает выбор внутри слайда;
- **Н4** — лектор применяет к себе GRA или статусы данных;
- **Н5** — GRA подана как универсальная модель или формула;
- **пограничный** — формулировка тянет к одному из типов Н1–Н5 (поле `leaning`), но прямого нарушения нет. Обычно подлежащим стоят данные, а не человек.

**Степень** показывает, насколько далеко ошибка уходит в эфир и в работу слушателя. «Критично» — правило подмены видно на слайде, звучит в речи лектора или передано ИИ в промпт. «Низкая» — неудачная формулировка, при которой граница в целом сохранена. Аудиты Дней 1–3 вели три степени — критично, средняя, низкая. Степень «высокая» есть только у Дня 4 и RFC v0.3.

## 1. Суммаризация проблемы

ИИ расширил GRA с «собрать и описать» на «выбрать». В материалах курса GRA выбирает:

1. **Имидж и стиль.** Гармония или эклектика, контраст, одежда лектора, образ поставщика объявлены функцией полярности, дистанции и массы. На Дне 4 правило так и названо: [вариант 1:63](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L63) «Стиль выбирают полярность, дистанция и масса.».
2. **Решения.** Вид шага выводится из статуса данных, канал — из дистанции, порядок шагов — из знака связи. Пример из колоды Дня 4: [колода Д4 в1:691](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-presentation-gamma.md?plain=1#L691) «Вид шага: `CONFLICT` → разговор; `PARTIAL` → обратимый шаг; `VERIFIED` → предложение или знакомство.».
3. **Образ лектора.** Согласие Дня 1 описать данные о лекторе превратилось в правило выбора его костюма: [вариант 1:205](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L205) «Лектор применяет к себе правило слайда 19 до того, как оно прозвучит.».
4. **Нарративные связки внутри слайда.** Связка «потому что → поэтому» требовала причины, и причину давала GRA: [вариант 1:556](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L556) «Потому что три вопроса GRA из Дня 1 на Дне 3 выбирали точки, поэтому теперь они выбирают стиль первого шага.».

Ошибка не появилась на Дне 4. Она росла от дня ко дню:

| День | В Gamma | Нарушений | Критично | Н1 | Н2 | Н3 | Н4 | Н5 | Пограничных | Верных интерпретаций |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | сгенерирован | 25 | 3 | 2 | 7 | 0 | 0 | 0 | 16 | 10 |
| 2 | сгенерирован | 24 | 1 | 0 | 1 | 0 | 0 | 0 | 23 | 12 |
| 3 | сгенерирован | 66 | 15 | 22 | 17 | 0 | 0 | 1 | 26 | 10 |
| 4 | не генерировался | 83 | 23 | 45 | 22 | 7 | 20 | 6 | 0 | 12 |
| RFC v0.3 (каркас Дней 1–4) | — | 30 | 4 | 15 | 17 | 0 | 0 | 3 | 0 | 21 |
| **Итого** | | **228** | **46** | **84** | **64** | **7** | **20** | **10** | **65** | **65** |

У одной находки может быть несколько типов, поэтому сумма по типам больше числа нарушений.

На Дне 1 GRA почти везде остаётся языком вопросов, а три критичных нарушения лежат в обосновании, не в колоде. На Дне 3 подмена выходит на слайд-мост ко Дню 4 и в промпт для ИИ. На Дне 4 она становится правилом дня, заголовком слайда 19 и пунктом промпта для слушателей.

**Перепроверка по векторным представлениям.** Фаундер напомнил замысел: [диалог:55](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L55) «изначатьно всю концепцию тепутационных технологий м ставили для сбора анализа информации, чтобы создать векторные представления, в анализе это надо явно перепроверить». Проверка по дням:

- **День 1.** Колода строит векторное описание: карта связей кейса 1, три вопроса к каждой связи, «?» там, где данных нет. Решение остаётся человеку: [колода Д1:133](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-14-day1-presentation-gamma.md?plain=1#L133) «Решение принимает человек, а «?» снимает тот, кто проверил.» Замысел соблюдён.
- **День 2.** Векторное описание не трогают, рядом появляется отдельный инструмент — статусы: [сценарий Д2:283](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-30-day2-lecturer-script.md?plain=1#L283) «GRA на Дне 2 ничего не считает.» Замысел соблюдён.
- **День 3.** Описание точек остаётся векторным, но к значению полярности привязаны действия: [колода Д3:626](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-presentation-gamma.md?plain=1#L626) ««?» → +1: письмо с релевантным сигналом», [колода Д3:627](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-presentation-gamma.md?plain=1#L627) «−1 → +1: сначала через посредника узнаём причину». Вектор начинает работать как таблица решений.
- **День 4.** Вектор «полярность, дистанция, масса» стал входом правила стиля: [вариант 1:749](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L749) «2. Открытую эклектику предлагай только при полярности +1, малой дистанции и высокой массе говорящего.». От векторного представления осталось только имя.

## 2. Конкретные примеры провала: День 4

### 2.1. GRA выбирает стиль

Цитаты из Варианта 1 обоснования:

- [вариант 1:100](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L100) «Три вопроса выбирают стиль первого шага (слайд 19)» — отказ от формулы не отменяет подмены: расчёта нет, но выбирает по-прежнему GRA;
- [вариант 1:151](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L151) «полярность, дистанция, масса — правило слайда 19» — поле решения в карточке подписано как производное от полей данных;
- [вариант 1:157](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L157) «статус данных определяет вид, полярность и дистанция — стиль, направление потока — канал» — одна фраза передаёт данным три решения человека;
- [вариант 1:251](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L251) «Третья остановка — место, где три вопроса GRA выбирают стиль шага.» — блок «Гармония vs Эклектика» объявлен местом работы GRA;
- [вариант 1:394](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L394) «Дистанция по информационно-коммуникационной оси выбирает канал» — канал — решение, а не значение параметра;
- [вариант 1:538](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L538) «выбор стиля — функция связи, а не вкуса» — ложная дилемма: стиль — не функция GRA и не вкус, а экспертиза имидж-технологий;
- [вариант 1:540](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L540) «Масса и дистанция владельца сети и неизвестного поставщика противоположны» — рабочая куртка объяснена параметрами GRA вместо теорий ожиданий Burgoon и кредита Hollander;
- [вариант 1:546](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L546) «Стратегию выбирают полярность, дистанция, масса» — заголовок центрального слайда имидж-блока назван параметрами GRA;
- [вариант 1:558](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L558) «Превратить три вопроса GRA в решающее правило стиля без расчёта» — методическая задача слайда прямо формулирует подмену;
- [вариант 1:560](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L560) «полярность «?», дистанция большая, наша масса для него невелика — значит, гармония с одной деталью» — «значит» выводит стиль из данных;
- [вариант 1:638](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L638) «полярность и дистанция → стиль» — стрелка из данных в стиль;
- [вариант 1:727](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L727) «стиль — гармония, потому что масса нашего производителя для «С» средняя» — масса подменяет «вклад» из теории Hollander.

### 2.2. «Потому что → поэтому» объясняет выбор стиля внутри слайда

- [вариант 1:87](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L87) «поэтому** стратегию выбирают полярность, дистанция и масса» — первая половина звена 15 — Burgoon, вторая — подмена;
- [вариант 1:207](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L207) «полярность на старте «?», поэтому лектор выбирает гармонию» — образ лектора выведен из GRA;
- [вариант 1:536](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L536) «Потому что коммерческий директор — точка Дня 3 с полярностью «?» и большой дистанцией, поэтому контраст без основания читается не как смелость, а как игра» — восприятие контраста объяснено значениями GRA;
- [вариант 1:492](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L492) «Потому что базовый формат и заметность детали зависят от отношений с точкой, поэтому следующий блок — гармония или эклектика.» — связка внутри имидж-блока снова ссылается на «отношения» в терминах GRA;
- [вариант 1:556](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L556) «Потому что три вопроса GRA из Дня 1 на Дне 3 выбирали точки, поэтому теперь они выбирают стиль первого шага.» — связка по аналогии: «раз выбирали точки, пусть выбирают стиль». Это механизм провала в одной фразе;
- в сценарии лектора: [сценарий Д4:464](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-lecturer-script.md?plain=1#L464) «Потому что выбор стиля зависит от связи, а не от вкуса, поэтому следующий слайд даёт правило.».

Фаундер задал вопрос первым же сообщением диалога: [диалог:3](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L3) «Разве я просил применять цепочки "потому-что" к имидж-технологиям?» Не просил. Связка нужна для перехода между слайдами. ИИ стал вкладывать её внутрь объяснения стиля. Каждая такая связка требовала причины, и самой доступной причиной оказывалась GRA.

### 2.3. Лектор применяет к себе GRA и статусы данных

На Дне 1 лектор согласовал одно: GRA полезна, чтобы собрать и описать открытые данные о нём. Вариант 1 сделал из этого правило выбора образа:

- [вариант 1:201](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L201) «Для новой аудитории с полярностью «?» лектор выбирает гармонию»;
- [вариант 1:202](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L202) «Эклектику лектор оставляет для аудитории, где полярность +1, дистанция малая и его масса высокая»;
- [вариант 1:205](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L205) «Лектор применяет к себе правило слайда 19 до того, как оно прозвучит.»;
- [вариант 1:211](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L211) «Три вопроса GRA к связи «слушатель — лектор» — те же, что к коммерческому директору сети «Х»».

Колода Дня 4, вариант 1, вынесла это на слайд 2: [колода Д4 в1:131](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-presentation-gamma.md?plain=1#L131) «МЕТОД КУРСА, ПРИМЕНЁННЫЙ К ЛЕКТОРУ», [колода Д4 в1:136](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-presentation-gamma.md?plain=1#L136) «● факт (`VERIFIED`)», [колода Д4 в1:145](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-presentation-gamma.md?plain=1#L145) «Эклектику лектор оставляет для выпускников и коллег: там полярность +1, дистанция малая, а его масса высокая.». Сценарий заставляет лектора произнести это вслух: [сценарий Д4:124](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-lecturer-script.md?plain=1#L124) «Сначала данные. Со статусом `VERIFIED`: я экс-генеральный директор школы стилистики, дизайна и технологий»; [сценарий Д4:126](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-lecturer-script.md?plain=1#L126) «Теперь три вопроса к нашей связи. Полярность — «?», мы только знакомимся. Дистанция короткая: эфир, чат и Telegram без посредников. Моя масса для вас средняя.»; [сценарий Д4:126](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-lecturer-script.md?plain=1#L126) «По правилу, которое прозвучит на слайде 19, это гармония».

Фаундер ответил на это дважды: [диалог:190](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L190) «нет, лектор ВООБЩЕ к себе это не применяет,» и [диалог:191](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L191) «Лектор тольеко в первый день СОГЛАСОВАЛ что это можно применить и полезно при сборе данных и описании данных о лекторе, ВСЕ!» На Дне 4 лектор не применяет к себе ни GRA, ни статусы. Первая редакция Варианта 2 в этом PR ещё оставляла лектору статусы. Это исправлено отдельным коммитом.

### 2.4. GRA на каждом слайде: «или» стало «и»

Шаблон комментария в #685 просил объяснить, «как он связан с GRA или Кейсом 1» (строка 78). ИИ сделал из этого обязательное поле «*GRA и кейс 1.*» на каждом из 26 слайдов. Поле стоит даже там, где связи нет:

- [вариант 1:191](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L191) «На обложке нет ни кейса, ни терминов GRA» — поле есть и на обложке;
- [вариант 1:456](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L456) «*GRA и кейс 1.* Для письма коммерческому директору контраст» — слайд о цветовых контрастах;
- [вариант 1:476](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L476) «*GRA и кейс 1.* Для производителя «линия и фактура»» — слайд о линии и фактуре;
- [вариант 1:436](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L436) «Слайд прямо включает её в тот же ряд» — GRA поставлена в один ряд с методиками стиля.

### 2.5. Статус данных выбирает шаг

Статусы — не GRA, но и они не выбирают шаг за человека:

- [сценарий Д4:586](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-lecturer-script.md?plain=1#L586) «Вид шага задаёт статус: при `CONFLICT` — разговор, при `PARTIAL` — шаг, который можно отыграть назад, при `VERIFIED` — предложение или знакомство.»;
- [колода Д4 в1:691](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-presentation-gamma.md?plain=1#L691) «Вид шага: `CONFLICT` → разговор; `PARTIAL` → обратимый шаг; `VERIFIED` → предложение или знакомство.»;
- [сценарий Д4:746](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-lecturer-script.md?plain=1#L746) «Вид шага: разговор (CONFLICT → разговор).», [сценарий Д4:767](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-lecturer-script.md?plain=1#L767) «(VERIFIED → предложение или знакомство)», [сценарий Д4:792](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-lecturer-script.md?plain=1#L792) «(PARTIAL → обратимый шаг).».

### 2.6. Промпт закрепляет ошибку для слушателей

- [вариант 1:749](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-rationale-and-method.md?plain=1#L749) «2. Открытую эклектику предлагай только при полярности +1, малой дистанции и высокой массе говорящего.» — Вариант 1;
- [сценарий Д4:693](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-lecturer-script.md?plain=1#L693) «2. Открытую эклектику предлагай только при полярности +1, малой дистанции и высокой массе говорящего.» — сценарий, текст промпта для слушателей.

Промпт учит чужой ИИ той же подмене. Слушатель уносит её в свою работу после курса.

### 2.7. Колода Дня 4, вариант 1

Колода [#688](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/688) перенесла подмену в `[SLIDE_TEXT]`: [колода Д4 в1:546](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-presentation-gamma.md?plain=1#L546) «выбор стиля — функция связи, а не вкуса»; [колода Д4 в1:559](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-presentation-gamma.md?plain=1#L559) «Стратегию выбирают полярность, дистанция, масса»; [колода Д4 в1:561](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-presentation-gamma.md?plain=1#L561) «Три вопроса GRA на Дне 3 выбирали точки, сегодня они выбирают стиль первого шага — без расчёта.»; [колода Д4 в1:661](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-presentation-gamma.md?plain=1#L661) «Статус задаёт вид, связь — стиль, поток доверия — канал». По диалогу, [диалог:127](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L127) «Презентация Дня 4 ещё не создана»: в Gamma она не генерировалась. Поэтому колода не правится точечно. Вместо этого собран вариант 2 из нетронутого варианта 1. Замены в нём перечислены в RFC.

## 3. Независимая оценка по дням

Фаундер в диалоге оценил Дни 1 и 2 как корректные ([диалог:66](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L66) «День 1 — КОРРЕКТНО ✅», [диалог:86](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L86) «День 2 — КОРРЕКТНО ✅»), День 3 — как частично корректный, День 4 — как критическое нарушение. Ниже — оценка по текстам самих файлов. Там, где она расходится с диалогом, это сказано прямо.

### 3.1. День 1 — корректно с оговоркой: семя Дня 4 посажено в обосновании

**Верно.** Колода и сценарий держат GRA в границах вопросов:

- [колода Д1:274](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-14-day1-presentation-gamma.md?plain=1#L274) «GRA как guardrails (ограничители) для ИИ, а не формула»;
- [сценарий Д1:471](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-14-day1-lecturer-script.md?plain=1#L471) «Ты не консультант и не стратег: решение принимаю я. Черновик — это не вывод.»;
- [обоснование Д1:155](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-07-day1-rationale-and-method-653.md?plain=1#L155) «GRA формирует структурированное поле связей и гипотез. Выбор конкретной стратегии остается отдельной задачей.»;
- [разбор лектора Д1:57](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-14-day1-lecturer-gra-research.md?plain=1#L57) «По фото не делаются выводы о стиле, характере или личных качествах» — данные о лекторе собраны и описаны, как он согласовал.

**Провалы.** Все три критичных нарушения дня — в обосновании, методическом источнике курса:

- [обоснование Д1:219](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-07-day1-rationale-and-method-653.md?plain=1#L219) «Выбор между гармонией и эклектикой зависит от полярности, дистанции и массы и делается на Дне 4» — правило «GRA → стиль» записано на Дне 1, за три дня до провала;
- [обоснование Д1:436](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-07-day1-rationale-and-method-653.md?plain=1#L436) «День 4: выбор между гармонией и эклектикой — грамотным контрастом, «свой, но заметный», — по полярности, дистанции и массе» — то же в таблице связи с Днями 2–4;
- [обоснование Д1:314](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-07-day1-rationale-and-method-653.md?plain=1#L314) «Умная — отобрать по открытым данным и трём вопросам GRA 3–5 сетей и их ЛПР, где разговор вероятнее, и написать первыми только им.» — GRA отбирает сети, то есть выбирает за человека.

В колоде, уже созданной в Gamma, подлежащим местами стоят данные, а не человек: [колода Д1:101](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-14-day1-presentation-gamma.md?plain=1#L101) «определить массу, дистанцию и полярность связей вокруг будущего партнёра и превратить их в управленческое решение»; [колода Д1:107](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-14-day1-presentation-gamma.md?plain=1#L107) «Вес, дистанция и знак каждой связи, собранные по открытым источникам, становятся основой стратегии.»; [колода Д1:285](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-14-day1-presentation-gamma.md?plain=1#L285) «20 визиток → 3–5 сетей, которым производитель пишет первым.». Это пограничные случаи и одно нарушение Н2 средней степени. Заменой одного-двух слов они исправляются в редакторе Gamma (RFC).

**Расхождение с диалогом.** Для колоды и сценария вывод «День 1 выдержан методологически чисто» подтверждается. Для обоснования — нет: оно уже содержит правило, которое на Дне 4 стало заголовком слайда 19.

### 3.2. День 2 — корректно в главном, есть пограничные формулировки

**Верно.** Статусы отделены от GRA, GRA ничего не считает:

- [колода Д2:443](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-30-day2-presentation-gamma.md?plain=1#L443) «Статус — не оценка партнёра, а состояние наших знаний о нём.»;
- [сценарий Д2:283](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-30-day2-lecturer-script.md?plain=1#L283) «GRA на Дне 2 ничего не считает.»;
- [сценарий Д2:627](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-30-day2-lecturer-script.md?plain=1#L627) «Не делай вывода о том, «какая у кого репутация», и не выбирай, с кем говорить».

**Провалы.** Одно критичное — в обосновании: [обоснование Д2:348](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-30-day2-rationale-and-method.md?plain=1#L348) «На Дне 1 слушатель по открытым данным и трём вопросам GRA отобрал 3–5 сетей и их ЛПР с наибольшей вероятностью ответа.». Оно повторяет ошибку обоснования Дня 1.

**Пограничные случаи в колоде:**

- слайд 2 выходит за согласие лектора Дня 1: [колода Д2:124](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-30-day2-presentation-gamma.md?plain=1#L124) «МЕТОД КУРСА, ПРИМЕНЁННЫЙ К ЛЕКТОРУ»; [колода Д2:126](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-30-day2-presentation-gamma.md?plain=1#L126) ««Сначала метод проверяют на себе, потом — на партнёре»»;
- на слайде 16 решение принимает метка данных, а не человек: [колода Д2:456](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-30-day2-presentation-gamma.md?plain=1#L456) «УЧЕБНЫЙ КЕЙС 1 · СТАТУС МЕНЯЕТ РЕШЕНИЕ»; [колода Д2:457](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-30-day2-presentation-gamma.md?plain=1#L457) «Статус меняет решение: первое письмо — о сроках входа в матрицу и пилотной партии». Программа курса говорит мягче: [RFC v0.3:590](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-12-rfc-days-1-3-logic.md?plain=1#L590) «Как статусы данных дают возможность менять управленческое решение».

**Расхождение с диалогом.** Вывод [диалог:95](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L95) «✅ Корректно (это НЕ GRA, это статусы данных)» верен: статусы — не GRA. Но правило [диалог:21](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L21) «Принятие решений на базе данных - человек или АГЕНТ - это другие модели!» относится к любым данным. Поэтому «статус меняет решение» помечено как пограничный случай: подлежащим должен быть человек.

### 3.3. День 3 — частично корректно, но не по той причине, что в диалоге

**Верно.** Фильтр отделён от GRA. Колода прямо называет его последовательностью вопросов: [колода Д3:63](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-presentation-gamma.md?plain=1#L63) «фильтр — это последовательность вопросов, после каждого узел проходит дальше или откладывается с записанной причиной». Названия «GRA-фильтр» в колоде, сценарии и обосновании Дня 3 нет. Статусы применены к выбору точек, а решение остаётся человеку: [колода Д3:679](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-presentation-gamma.md?plain=1#L679) «Решение принимает человек.» Здесь оценка совпадает с [диалог:109](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L109) «✅ Корректно».

**Провалы, которых нет в диалоге:**

- **Слайд-мост 32 в Gamma** прямо связывает гармонию и эклектику со знаком связи: [колода Д3:866](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-presentation-gamma.md?plain=1#L866) «Полярность −1 или «?»: гармония или эклектика?»; [колода Д3:868](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-presentation-gamma.md?plain=1#L868) «Программа Дня 4 говорит: выбор имиджевой стратегии зависит от полярности, дистанции и массы точки.»; [колода Д3:872](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-presentation-gamma.md?plain=1#L872) «Что выбрать, если знак связи «?» или −1?». Это три критичных нарушения на уже созданном слайде.
- **Сценарий** произносит это вслух: [сценарий Д3:710](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-lecturer-script.md?plain=1#L710) «стратегия образа зависит от полярности, дистанции и массы точки».
- **Промпт для ИИ** велит обосновывать стиль и канал параметрами GRA: [сценарий Д3:952](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-lecturer-script.md?plain=1#L952) «— и почему (полярность, дистанция D4);»; [сценарий Д3:954](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-lecturer-script.md?plain=1#L954) «— и почему (дистанция D2, D3, D5, направление потока).». Это исполняемая инструкция: её вывод — вход промпта Дня 4.
- **Обоснование** даёт таблицу «вид, стиль, канал», где стиль выводится из полярности: [обоснование Д3:217](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-rationale-and-method.md?plain=1#L217) «От полярности и дистанции D4: при «?» или −1 — вопрос и данные, а не заявление». Отсюда правило перешло в Вариант 1. Ещё одно правило из полярности в образ: [обоснование Д3:887](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-rationale-and-method.md?plain=1#L887) «при полярности −1 или «?» резкий контраст образа разрушает доверие».
- **Рецепты «знак → действие»** на слайдах: [колода Д3:618](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-presentation-gamma.md?plain=1#L618) «Чтобы «?» стал +1, нужен релевантный сигнал»; [колода Д3:627](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-presentation-gamma.md?plain=1#L627) «−1 → +1: сначала через посредника узнаём причину».
- **Лектор** снова выходит за согласие Дня 1: [колода Д3:133](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-02-day3-presentation-gamma.md?plain=1#L133) «Сегодня применяем к лектору механику Дня 3».

**Расхождение с диалогом.** Диалог опасался «GRA-фильтра» ([диалог:110](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L110) «Если в презентации Дня 3 фильтр назван «GRA-фильтром»»). Это опасение не подтвердилось. Настоящее нарушение — мост ко Дню 4 и промпт. Его в диалоге нет.

### 3.4. День 4 — критическое нарушение, шире, чем в диалоге

Диалог называет три места в обосновании (слайды 2, 17–20). Реестр находит 25 нарушений в Варианте 1, 12 — в колоде варианта 1 и 46 — в сценарии лектора. Сценарий в диалоге не упомянут, а именно его лектор произносит в эфире. Подробности — в разделе 2.

**Верно.** Принцип «решение за человеком» в сценарии Дня 4 есть: [сценарий Д4:682](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-lecturer-script.md?plain=1#L682) «Ты пишешь черновики, решение принимает человек.» Есть и запрет судить человека по внешности: [сценарий Д4:695](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-11-03-day4-lecturer-script.md?plain=1#L695) «4. Не давай советов по моде и не делай выводов о человеке по фото, стилю или постам». Ошибка в том, что рядом с этими строками GRA выбирает за человека стиль.

**Расхождение с диалогом в предложенных там исправлениях:**

- исправление [диалог:136](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L136) «Лектор применяет метод Дня 4 к себе: факты VERIFIED и PARTIAL, «?» (это сбор данных).» фаундер отклонил в [диалог:190](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L190) «нет, лектор ВООБЩЕ к себе это не применяет,». В Варианте 2 лектор к себе ничего не применяет;
- пример [диалог:160](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L160) «при полярности +1 применяем эклектику» противоречит [диалог:20](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L20) «GRA запрещено применять к имидж-технологиям». Те же примеры стоят в теле issue #689. В Варианте 2 они не использованы, отклонение записано в его разделе «Отклонение от постановки».

### 3.5. RFC v0.3 — узел, через который прошла подмена

RFC v0.3 — каркас всех четырёх дней. Правильная граница в нём есть: [RFC v0.3:97](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-12-rfc-days-1-3-logic.md?plain=1#L97) «Мы не пытаемся планировать действия в жесткой конкурентной борьбе.»; [RFC v0.3:266](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-12-rfc-days-1-3-logic.md?plain=1#L266) «GRA — авторская гипотеза фаундера, курс работает с ней на уровне вопросов.»

Подмена тоже есть, и Вариант 1 взял её отсюда:

- [RFC v0.3:168](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-12-rfc-days-1-3-logic.md?plain=1#L168) «Выбор между гармонией и эклектикой — грамотным контрастом — зависит от полярности, дистанции и массы.»;
- [RFC v0.3:955](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-12-rfc-days-1-3-logic.md?plain=1#L955) «Стратегию выбирают полярность, дистанция и масса»;
- [RFC v0.3:957](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-12-rfc-days-1-3-logic.md?plain=1#L957) «Рабочее правило ◐: открытая эклектика — только при полярности +1, малой дистанции и высокой массе говорящего»;
- [RFC v0.3:958](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-12-rfc-days-1-3-logic.md?plain=1#L958) «три вопроса GRA из Дня 1, на которые на Дне 3 опирался выбор точек, теперь выбирают стиль первого шага.».

Источник этих строк — строка программы Технограда: [RFC v0.3:1029](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-12-rfc-days-1-3-logic.md?plain=1#L1029) «Выбор стратегии зависит от полярности связи, дистанции и массы в коммуникации». Программа говорит, что ситуация влияет на выбор. Она не говорит, что выбирает модель. ИИ прочитал «зависит» как «выбирают».

### 3.6. Где ещё ошибся ассистент в самом диалоге

- [диалог:9](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L9) «Имидж-технологии регулируются жесткими условными правилами на базе GRA (полярность, масса, дистанция)» — это та же подмена. Фаундер ответил: [диалог:20](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L20) «GRA запрещено применять к имидж-технологиям».
- [диалог:155](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L155) «Статусы данных (VERIFIED/PARTIAL/CONFLICT) — это НЕ GRA», а через тридцать строк [диалог:184](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L184) «(масса, дистанция, полярность как вопросы к связи, статусы VERIFIED/PARTIAL/CONFLICT)» — статусы снова внутри GRA. Верна строка 155. Версия 0.1 этого файла повторила ошибку строки 184 в таблице границ. В версии 0.2 это исправлено.
- [диалог:130](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L130) «Ничего менять не нужно. Материалы выдержаны методологически чисто.» Для Дня 3 это не так: подмена стоит на созданном в Gamma слайде 32 (раздел 3.3).

## 4. Корневая причина

**ИИ максимизировал «полезность» одного фреймворка.** Связность курса он мерил числом связей с GRA: чем больше слайдов опирается на GRA, тем «целостнее» курс. По этой мере 26 полей «GRA и кейс 1» из 26 — лучший результат. При этом ИИ проигнорировал ограничение, которое человек держит по умолчанию: модель сбора данных, модель принятия решений и экспертиза подачи — разные инструменты.

Причина складывается из пяти механизмов.

1. **Буквальное исполнение вместо экспертизы.** Постановка #685 содержала «Ключевое правило (через GRA)» и слайд лектора, который выбирает стиль, «опираясь на свои VERIFIED/PARTIAL данные». У исполнителя было право на отклонение. В Варианте 1 он им пользовался: две апелляции — к нумерации слайдов блока Б и к опорам на обоснование Дня 3. О противоречии с границей #657 он не сказал. Отклонение по границе модели было нужнее обоих.
2. **Наследование цепочки без проверки.** Подмена прошла по цепочке: строка программы → RFC v0.2 и v0.3 (коммиты `269e48c`, `e67cb49`) → обоснование Дня 1 (коммит `900025f`, [обоснование Д1:219](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-07-day1-rationale-and-method-653.md?plain=1#L219) «Выбор между гармонией и эклектикой зависит от полярности, дистанции и массы и делается на Дне 4») → обоснование и мост Дня 3 → постановка #685 → Вариант 1 → колода варианта 1. Каждое звено считало предыдущее источником истины и не спрашивало, где кончается область модели.
3. **Усиление, а не исполнение.** Постановка просила одно правило. ИИ распространил его на лектора, карту маршрута, карточку, кейс, промпт для слушателей, обязательное поле на каждом слайде и проверку CI. Каждое расширение по отдельности выглядело как «согласованность». Вместе они превратили модель данных в универсальный ответ.
4. **Принуждение к причинности.** Мостик «потому что → поэтому» требовал причины на каждом шаге. Где настоящей причиной была экспертиза имидж-технологий — Burgoon, Hollander, Brewer, теория аккомодации, — ИИ подставлял параметры GRA. Они уже стояли на слайде и звучали как данные.
5. **Подлежащее «данные» вместо «человек».** Во всех четырёх днях повторяется одна грамматика: «статус меняет решение», «знак подсказывает», «три вопроса выбирают». Фраза с данными в роли подлежащего незаметно передаёт им решение. Так появились 65 пограничных находок в Днях 1–3, и из них выросли прямые нарушения Дня 4.

**Можно ли доказать, что GRA — модель «всё для всех»?** Фаундер поставил вопрос прямо: [диалог:176](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L176) «ельзя создать модель все для всех, или ВЫ ОБЯЗАНЫ ДОКАЗАТЬ, ЧТО МОЖНО». Доказать нельзя. На входе GRA — три вопроса о связи. На выходе — описанная, классифицированная и сохранённая связь. Для выбора стиля нужны другие входы: формат встречи, принятый у партнёра дресс-код, палитра бренда, ожидания по Burgoon, накопленный вклад по Hollander. Ни один из них GRA не собирает. Значит, всякое «GRA выбирает стиль» — правило, взятое со стороны и подписанное именем GRA. Это подмена, а не вывод модели.

## 5. «Заставь дурака молиться, он и лоб расшибет»: что это значит для ИИ-агента

Фаундер поставил задачу так: [диалог:35](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L35) «Обяжите конарда интепретировать эту пословицу к возможносй работе Агента» и [диалог:36](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L36) «А потом пусть наложит на выполненный вариант 1 текущий исполнения задачи».

### 5.1. Интерпретация для агента

Пословица не про глупость и не про молитву. Она про исполнителя, который выполняет правило, не понимая, зачем оно дано. Молитва ценна смыслом. Усердие без меры превращает её в поклоны до разбитого лба: исполнитель старается сильнее всех, и именно поэтому калечит себя и дело.

| В пословице | В работе ИИ-агента |
|---|---|
| Молитва | Полезное правило в своей области. Здесь — GRA: сбор и описание данных о связях |
| Дурак | Агент, который понимает правило как «применять везде», а не «применять здесь» |
| Усердие | Каждый новый объект — стиль, лектор, канал, промпт, проверка CI — получает то же правило |
| Расшибленный лоб | Разрушенный смысл: курс учит, что модель данных выбирает цвет и костюм |

Как слепое применение одного правила разрушает смысл:

1. **Правило без области применения перестаёт различать.** Если GRA выбирает и точки, и стиль, и цвет, и канал, она больше ничего не объясняет. Инструмент, который подходит ко всему, ничего не измеряет.
2. **Усердие измеряется частотой, а не уместностью.** Агент считает успехом то, что правило есть везде. Правильный вопрос другой: где правило не нужно.
3. **Ошибка закрепляется собственной проверкой.** Агент пишет проверку, которая падает, если правила нет. Самопроверка превращается в машину повторения ошибки.
4. **Метод подрывает сам себя.** Курс помечает GRA знаком ○ — авторская гипотеза. Гипотеза, которая решает всё, перестаёт быть гипотезой и становится догмой.
5. **Агент совершает ту ошибку, которую курс учит находить.** Курс учит не выдавать предположение за факт. Агент выдал предположение о возможностях собственного метода за правило.

### 5.2. Наложение на Вариант 1

| В пословице | В Варианте 1 |
|---|---|
| Молитва | GRA из постановки: «правило через GRA» для одного слайда |
| Дурак | Исполнитель, который не задал вопрос «что эта модель не решает?» |
| Усердие | 26 полей «GRA и кейс 1» из 26; правило стиля на слайде 19; лектор, выбирающий себе галстук по полярности; карточка, где каждое решение «вычисляется» из данных; промпт для слушателей; проверка `check-day4-685.py`, которая требует GRA на каждом слайде |
| Расшибленный лоб | 25 нарушений в одном файле, 9 из них критичных. Центральный слайд имидж-блока учит обратному тому, что фаундер задал в #657 |

### 5.3. Наложение на Дни 1–3

Поклоны начались не на Дне 4. На Дне 1 это одна строка обоснования: [обоснование Д1:219](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-07-day1-rationale-and-method-653.md?plain=1#L219) «Выбор между гармонией и эклектикой зависит от полярности, дистанции и массы и делается на Дне 4». На Дне 3 — слайд-мост и промпт: 15 критичных нарушений. На Дне 4 — 23. Каждый день агент добавлял правилу ещё одну область и считал это развитием курса.

Пословица относится и к первой версии этого разбора. Версия 0.1 положила статусы внутрь GRA, оставила лектору статусы и утверждала, что колода Дня 4 уже в Gamma. Агент исправлял ошибку с тем же усердием, с каким её совершал, — не перечитав первоисточник. Версия 0.2 написана по диалогу, и каждая цитата сверена с файлом.

## 6. Рецепты: как этого избежать

Фаундер просил рецепты, [диалог:196](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L196) «как этого избегать, когда я задавал явно и четко, что такое GRA».

1. **Сначала граница, потом применение.** Перед тем как применить модель к новой сущности, ответить письменно: «Что эта модель не решает?» Нет ответа — модель применяют слишком широко.
2. **Подлежащее решения — человек.** Красные флаги в тексте: «выбирает», «задаёт», «определяет», «меняет решение», «значит», «→», если подлежащее — GRA, полярность, дистанция, масса, связь или статус. Такая фраза переписывается: подлежащим становится человек, данные остаются дополнением.
3. **Связка «потому что → поэтому» — только между слайдами.** Внутри описания технологии связки нет. Технологию описывают суть, условие и маркер.
4. **Каждому инструменту — своё имя.** GRA, статусы Дня 2, фильтр Дня 3, имидж-технологии и модель решения не называются друг другом и не ставятся в один ряд.
5. **Лектор — только в границах согласия Дня 1.** Данные о лекторе собирают и описывают. Ни GRA, ни статусы лектор к себе не применяет.
6. **Отклонение — обязанность, а не льгота.** Если постановка противоречит ранее заданной границе (#685 против #657), исполнитель пишет отклонение в формате фаундера: «Я предлагаю скорректировать [Ограничение X], потому что вариант [Y] эффективнее решает задачу [Z]». Промолчать о границе модели — то же, что бить поклоны до крови.
7. **Проверка ищет выход за границу, а не присутствие.** Автоматическая проверка падает на «GRA выбирает стиль», а не на «GRA нет на слайде». Так устроена проверка `check-day4-689.py`.
8. **Не генерировать без согласования.** [диалог:19](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L19) «запрещего перегенерировать или генеривать задачи, пока не согласовали и пока я не задал это, ЭТО ОСНОВНОЙ КОНТРАКТ». Поэтому RFC только предлагает правки Дней 1–3 и перегенерацию Дня 1, а не делает их.
9. **Универсальность доказывают, а не предполагают.** Тот, кто хочет применить модель к новой области, обязан показать, какие входы этой области модель собирает (раздел 4). Нет таких входов — нет применения.

## 7. Что исправлено и как будем крутиться

Фаундер спросил: [диалог:197](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L197) «что тепер ьделать с презентациями, учитывая что времени на исправления почти нет» и [диалог:198](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/16415e90abc2d6489ed0ea9582236a3af15bb648/research/reputation-technologies/2026-10-19-founder-dialog-689.txt?plain=1#L198) «как вы как сотрудникиЮ совершившие глупость, будете круиться ??»

**Что сделано в этом PR:**

1. [Вариант 2 обоснования](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-11-03-day4-rationale-and-method-v2.md) — перечень 21 имидж-технологии: название, суть, условие применения, визуальный маркер. В описаниях нет GRA, статусов и связок «потому что → поэтому». Лектор к себе ничего не применяет.
2. [Колода Дня 4, вариант 2](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-11-03-day4-presentation-gamma-v2.md) собрана из нетронутого варианта 1 скриптом с заменами. День 4 в Gamma ещё не генерировался, поэтому кредиты на правку не тратятся: в Gamma сразу идёт вариант 2.
3. [RFC](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-11-03-day4-crisis-mitigation-rfc.md) — прежде всего замены слов в созданных колодах Дней 1–3, вариант перегенерации Дня 1 с нуля и фраза для сценария Дня 4.
4. Реестр 228 нарушений и 65 верных интерпретаций — для дальнейшей отладки.
5. Проверка `check-day4-689.py` в CI. Она сверяет цитаты реестра с файлами и следит, чтобы Вариант 1 и колода варианта 1 остались байт в байт прежними.

**Как будем крутиться**, по убыванию срочности:

1. **День 4** — генерировать в Gamma вариант 2 колоды. Ничего не потеряно, кредиты не потрачены.
2. **День 3** — три замены на слайде-мосте 32 в редакторе Gamma, без перегенерации. Это единственные критичные нарушения на уже созданных слайдах.
3. **День 1** — замены 1–2 слов на слайдах 1, 9, 19, 21 и 30 в редакторе или перегенерация с нуля, если фаундер её согласует.
4. **День 2** — критичных нарушений на слайдах нет. Замены на слайдах 2 и 16 — по желанию.
5. **Сценарии и обоснования** — правки текста по RFC. Gamma они не затрагивают.

Ничего из пунктов 1–5 не запускается без команды фаундера.

## Гейт-проверка

- [x] Я полностью прочитал прикреплённый файл диалога и усвоил границы применения GRA: 200 строк файла `2026-10-19-founder-dialog-689.txt` из комментария к PR #690; границы — в таблице «Граница: что делает каждая модель».
- [x] Я создал Файл 2 `2026-11-03-day4-ai-interpretation-analysis.md`: честный разбор ошибок интерпретации по всем четырём дням с цитатами и номерами строк, анализ пословицы и её наложение на Вариант 1.
- [x] Я создал Файл 1 `2026-11-03-day4-rationale-and-method-v2.md` как чистый перечень имидж-технологий без применения GRA к стилю.
- [x] Я создал Файл 3 `2026-11-03-day4-crisis-mitigation-rfc.md`: фраза в сценарий и точечные замены 1–2 слов в слайдах, прежде всего для Дней 1–3.
- [x] Я не трогал и не удалял исходный файл `2026-11-03-day4-rationale-and-method.md` (Вариант 1): это проверяет хеш файла в `check-day4-689.py`.
- [x] Все 3 файла созданы в каталоге `research/reputation-technologies/`.
- [x] Я удалил прикреплённый файл с диалогом после того, как все три файла были созданы, проверены и закоммичены: удаление — отдельный последний коммит, цитаты ведут на коммит `16415e9`.
