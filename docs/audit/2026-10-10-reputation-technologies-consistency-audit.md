---
status: draft
version: 0.1
updated: 2026-10-10
temperature: 0.1
type: audit
context: [reputation-technologies, gra, gra-research-model, day1, issue-659, issue-657]
method: corpus-scan + manual-review + anchor-check + validator-run
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/659"
scope: slice
audit_target: "Все markdown-файлы домена `research/reputation-technologies/` (ранние артефакты GRA от 2026-06-20, стратегия партнёров, исследования #610 и #650, три документа Дня 1, модуль `gra-research-program/`) против восьми методологических правок F1–F8 и дословной формулировки происхождения GRA из issue #659; дополнительно — реестры Хаба и смежные модули, которые цитируют модель GRA"
evidence_model: "скрипт поиска противоречивых формулировок и относительных ссылок `research/reputation-technologies/exp/day1-methodology-659/scan-contradictions.sh` + проверка якорей `research/reputation-technologies/exp/gra-research-program-657/check-gra-anchors.py` + сравнение с `origin/main` по строкам + прогон валидаторов репозитория"
verdict: conditional
severity_scale: "Major/Minor/Info"
follow_up: "Все найденные противоречия исправлены в PR #661. Остаются вне аудита: юридическая проверка формулировок кейсов и эмпирическая проверка гипотез HP-D и HM-I — задачи бэклога Sprint 29."
related_norm: "standards/audit-standard.md, research/reputation-technologies/gra-research-program/30-decision-framework.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/659"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/657"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/653"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/661"
related_artifacts:
  - "research/reputation-technologies/README.md"
  - "research/reputation-technologies/gra-research-program/30-decision-framework.md"
  - "research/reputation-technologies/gra-research-program/40-practice-and-cases.md"
  - "research/reputation-technologies/gra-research-program/50-open-research.md"
  - "research/reputation-technologies/exp/day1-methodology-659/README.md"
---

# Сквозная проверка согласованности домена «Репутационные технологии» (issue #659)

## Summary / BLUF

Вердикт — **условно соответствует**. До правок корпус домена
противоречил собственной теоретической базе. Модуль
[«Исследовательская модель GRA»](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/00-introduction.md)
и его таблица формулировок
[F1–F10](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/30-decision-framework.md)
уже действовали, но ранние артефакты 2026-06-20 и исследование #650 их не
соблюдали. Эти тексты по-прежнему выводили GRA из гравитационной модели
торговли, определяли дистанцию как обратное доверие, а массу — как влияние.
Лаг «поле опережает рынок на 30–180 дней» и цепочку «репутационного ROI» они
подавали как свойства модели. Ни одно из этих утверждений не проверено.

Найдено **20 расхождений** в 19 файлах:

- 9 серьёзных (Major) — меняют смысл модели GRA;
- 9 мелких (Minor) — терминология, ссылки, реестры, одна внутренняя
  неточность нормы;
- 2 информационных (Info) — правка не нужна.

Все серьёзные и мелкие **исправлены в этом же PR**. Для информационных
записано, почему текст оставлен как есть.

Вердикт условный по одной причине: аудит проверяет согласованность текстов
между собой, а не истинность модели. Гипотезы H1, HP-D и HM-I остаются
непроверенными, а формулировки кейсов не прошли юридическую проверку. Эти
задачи вынесены в бэклог, а не закрыты.

## Scope / Target

**Норма.** Правки F1–F8 из
[`30-decision-framework.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/30-decision-framework.md)
и дословная формулировка происхождения из issue
[#659](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/659):

> «GRA возникла исключительно как авторская гипотеза фаундера о возможности
> структурного описания социальных и информационных связей по аналогии с
> физическими закономерностями. Любые математические или экономические модели
> (включая гравитационные) рассматриваются лишь как одна из возможных
> практических сред исследования или реализации этой гипотезы, не имеющая
> статуса первоисточника или особого ориентира»

Из нормы проверены шесть следствий:

1. **Происхождение (F1, F2).** Торговая модель Тинбергена — прецедент, а не источник GRA.
2. **Дистанция (F3).** Дистанция многомерна (оси D1–D5), её минимум две оси, и они не сводятся в одно число.
3. **Масса (F4).** Масса — наблюдаемые характеристики узла (M1–M4). Влияние на конкретное решение фиксируется отдельно.
4. **Полярность (F5).** Полярность — это {+1, 0, −1, ?} и направление потока (гипотеза HP-D).
5. **Формула и прогноз (F6, F8).** Формула — гипотеза H1 из ряда H0–H6. Лаг поля перед рынком — гипотеза HM-I.
6. **Граница домена (F7).** Тексты не обещают бизнес-эффекта. GRA — не калькулятор.

Дополнительно проверена терминология: «исследовательская модель GRA» вместо
«открытой исследовательской программы». Проверена и форма ссылок: issue
требует полных абсолютных URL.

**Охват.**

- Все 20 markdown-файлов домена, включая README экспериментов.
- Реестры Хаба, которые описывают эти файлы: `ops/artifact-map.md`,
  `research/README.md`, `CHANGELOG.md`.
- Один смежный модуль, который цитирует модель GRA:
  `research/ba-requirements/normalization/20-taxonomy.md`.

**Вне охвата.**

- Истинность модели.
- Правовая оценка кейсов.
- Каталоги `standards/` и `docs/adr/`: правила репозитория запрещают их менять,
  а модель GRA они не цитируют.

## Method / Evidence

1. **Сравнение по строкам.** Каждый файл домена прочитан в версии `origin/main`
   на коммите `2fad164`. Найденные формулировки сопоставлены с нормой по
   строкам. Цитаты в Findings — дословные строки из этой версии.
2. **Скрипт поиска.**
   [`scan-contradictions.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/exp/day1-methodology-659/scan-contradictions.sh)
   ищет запрещённые формулировки и относительные ссылки. После правок он
   печатает `hits: 0`. Строки, где старая формулировка приведена как
   исправленная или запрещённая, скрипт пропускает.
3. **Перевод ссылок.**
   [`absolutize-links.py`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/exp/day1-methodology-659/absolutize-links.py)
   переводит относительные ссылки в абсолютные URL ветки `main` и сообщает о
   несуществующих целях. Таких целей не найдено.

   Исключение — README в `exp/`. Там относительная ссылка на родительский
   отчёт обязательна: её форму машинно проверяет
   `tools/validate-evidence-structure.sh`. Это вынужденное расхождение с
   требованием issue, оно объявлено в самих README.
4. **Проверка якорей.**
   [`check-gra-anchors.py`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/exp/gra-research-program-657/check-gra-anchors.py)
   проверяет все ссылки с якорями на файлы домена. Результат после правок —
   `bad: 0`.
5. **Валидаторы репозитория.** После правок проходят `validate-frontmatter`,
   `validate-file-naming`, `validate-repository-structure`,
   `validate-evidence-structure`, `validate-rrp-links` и
   `generate-manifest.py --check`.

## Findings / Verdict

Каждая запись построена по форме, которую требует issue #659: файл, найденное
противоречие, предлагаемая правка и статус.

### Ранние артефакты GRA (2026-06-20)

**A-01 — Major — F1, F2.** В файле
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-20-founders-vision-and-framework.ru.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-20-founders-vision-and-framework.ru.md)
обнаружено противоречие: «Это соединяет **гравитационную модель торговли**
(Tinbergen, 1962) и **анализ силового поля**…», а в §IV.1 написано «Научные
основания: Gravity Model of Trade (Tinbergen, 1962) для «масса/дистанция²»». Так
текст выводит GRA из торговой модели. Предлагаемая правка: заменить
генеалогию дословной формулировкой фаундера. Модель Тинбергена и анализ поля
Левина назвать прецедентами переноса, а не источником. Добавить оговорку: в
торговле степень расстояния оценивается по данным и близка к 1, а Левин
считал абсолютную силу социальных сил неопределимой. **Выполнено**
(версия 0.2, ядро п. 2 и §IV.1; строка Тинбергена в библиографии помечена
«прецедент, не источник GRA»).

**A-02 — Major — F3, F4, F5, F6.** В том же файле обнаружено противоречие:
«Масса — влияние/ресурс/репутационный капитал, Дистанция — обратна доверию,
Полярность ∈ {+1, 0, −1}». Формула при этом подана без статуса гипотезы.
Предлагаемая правка:

- формулу назвать рабочей гипотезой H1 из ряда H0–H6;
- массу определить как наблюдаемые характеристики узла (ресурс, позиция, сеть,
  репутационный капитал), а влияние на решение фиксировать отдельно;
- дистанцию описать как многомерную величину: физическая и временная,
  информационная, доверие, ценности, институциональная;
- к полярности добавить «?» и направление потока.

**Выполнено** (ядро п. 2, §III.1, §IV.1).

**A-03 — Major — F7, F8.** В том же файле обнаружено противоречие: «изменения в
поле проявляются на рынке с лагом **30–180 дней**. Это даёт прогностический
горизонт…» и «**Репутационный ROI**: Репутация → Доверие → ↓CAC → ↑LTV →
Прибыль». Непроверенный лаг подан как свойство модели, а цепочка ROI читается
как обещание бизнес-эффекта. Предлагаемая правка: пометить лаг как гипотезу
HM-I, а цепочку ROI — как гипотетическую, «не обещание эффекта». **Выполнено**
(ядро п. 3, таблица ключевых идей, §III.3, резюме RU/EN).

**A-04 — Major — F1–F8.** В файле
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-20-white-paper.en.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-20-white-paper.en.md)
обнаружено противоречие. Текст содержит «This unifies the **Gravity Model of
Trade** (Tinbergen, 1962) with **Force Field Analysis**», «Mass — influence/…»,
«Distance — inverse of trust» и «leads it by roughly 30–180 days». В конце
стоит «Key anchors: Tinbergen 1962». Предлагаемая правка — та же, что в
A-01…A-03, на английском:

- статус H1;
- наблюдаемая масса;
- многомерная дистанция;
- полярность с направлением потока;
- абзац Origin с переводом формулировки фаундера, помеченным «translation
  ours»;
- лаг как HM-I;
- цепочку ROI считать гипотезой.

**Выполнено** (версия 0.2).

**A-05 — Major — F1–F5, F8.** В файле
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-20-framework-standard.en.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-20-framework-standard.en.md)
обнаружено противоречие: «Grounded in the Gravity Model of Trade (Tinbergen,
1962), Force Field Analysis (Lewin, 1947)…», «Mass — influence/resource/
reputation capital», «Distance — inverse of trust», «leads the market (lag
30–180 days)». Для проекта стандарта это особенно опасно: определения из
раздела Terms переходят в чужие тексты как нормативные. Предлагаемая правка:
заменить определения Mass, Distance и Polarity нормой модуля, вместо
«Grounded in…» указать происхождение и прецеденты, лаг пометить как HM-I.
**Выполнено** (версия 0.2).

**A-06 — Major — F1, F3, F4, F7, F8.** В файле
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-20-glossary.ru-en.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-20-glossary.ru-en.md)
обнаружено противоречие:

- статья «Масса»: аналог «Gravity Model (Tinbergen 1962)», определение
  «Влияние/ресурс/репутационный капитал узла»;
- статья «Дистанция» определяет её через доверие;
- статья «Гравитация»: аналог «Tinbergen 1962»;
- статья поля: «содержит и опережает рынок (лаг 30–180 дней)»;
- статья «Репутационный ROI» подана как готовая цепочка.

Предлагаемая правка:

- переписать статьи «Масса», «Дистанция», «Полярность», «Сила связи» и
  «Гравитация» по норме модуля, со ссылками на таксономию;
- лаг пометить как HM-I;
- ROI определить как «гипотетическую цепочку… не обещание эффекта для бизнеса
  и не расчётную метрику курса».

**Выполнено** (версия 0.2).

**A-07 — Major — F3, F4, F7, F8.** В файле
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-20-executive-summary.ru-en.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-20-executive-summary.ru-en.md)
обнаружено противоречие: «Масса — влияние/ресурс/капитал; Дистанция обратна
доверию… Поле **опережает рынок на 30–180 дней**, поэтому управление
репутацией — это опережающий индикатор выручки». То же утверждение повторено в
EN-части. Предлагаемая правка: переписать абзацы модели на обоих языках:

- статус H1;
- наблюдаемая масса;
- многомерная дистанция;
- гипотеза HM-I;
- явное «Это не обещание эффекта».

**Выполнено** (версия 0.2).

### Исследования курса

**A-08 — Major — F1, F3.** В файле
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-09-30-course-sources-and-presentations-650.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-09-30-course-sources-and-presentations-650.md)
обнаружено противоречие: «Масса — влияние и ресурс узла; дистанция — обратная
величина доверия… Происхождение метафоры — гравитационная модель торговли
`[Г1][Г2][Г4]`». Предлагаемая правка:

- масса — наблюдаемые характеристики, дистанция многомерна, доверие — одна
  из её осей;
- модель торговли и анализ поля — прецеденты, а не происхождение;
- источники `[Г1]…[Г11]` сохранить как опоры для ограничений метафоры.

**Выполнено** (версия 0.2):

- примечание после заголовка;
- колонка карты связей «Дистанция по доверию (одна из осей)»;
- тезис 2 Дня 1;
- строки структуры презентации, пояснения к `[Г1]` и `[Г11]`.

**A-09 — Minor.** В том же файле обнаружено противоречие: «держать все четыре
дня на **одном сквозном обезличенном кейсе** (продуктовая сеть «Р»)». День 1
версии 0.3 работает на трёх сквозных кейсах:

- 1 — производитель консервов;
- 2 — deep-tech стартап;
- 3 — массажист-эксперт.

Предлагаемая правка: не переписывать исследование задним числом. Это
рекомендация на дату 2026-09-30, и её логику (артефакт одного дня — вход
следующего) кейсы 1–3 сохраняют. В примечание версии 0.2 добавлено, что
сквозные кейсы курса теперь заданы в
[`40-practice-and-cases.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/40-practice-and-cases.md#как-устроены-сквозные-кейсы).
**Выполнено.**

**A-10 — Info.** Файл
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-09-24-introductory-course-options-610.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-09-24-introductory-course-options-610.md)
проверен, противоречий не найдено. Формулу он подаёт как эвристику: «нельзя
преподавать её как валидированный прогноз». Это совпадает с F6 и F7. **Правка не
требуется.**

**A-11 — Minor.** В файле
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-29-partner-attraction-strategy.ru.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-06-29-partner-attraction-strategy.ru.md)
обнаружено расхождение с требованием issue к ссылкам: ссылки на отчёт
фаундера и на executive summary относительные. Содержательных противоречий нет:
«масса» встречается только в кавычках, как метафора масштаба, а влияние в
критериях названо отдельно от массы. Предлагаемая правка: перевести ссылки в
абсолютные URL. **Выполнено.**

### Документы Дня 1 и модуль GRA

**A-12 — Major — F1, F2.** В файле
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-10-07-day1-lecturer-script-653.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-10-07-day1-lecturer-script-653.md)
версии 0.2 обнаружено противоречие: «GRA выросла не из учебника физики, а из
практики PR и GR и из гипотезы…». Генеалогия только сместилась: источником
теперь названа практика PR и GR, а не формулировка фаундера. Та же
формулировка была в
[обосновании Дня 1](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-10-07-day1-rationale-and-method-653.md)
(«GRA выросла из опыта фаундера в PR/GR…»). Предлагаемая правка: на слайде 8 и
в реплике лектора дать дословную формулировку фаундера. PR и GR назвать
прикладной областью, где гипотезу применяют, а не её источником. **Выполнено**
(версия 0.3 всех трёх документов Дня 1, Направление 1).

**A-13 — Minor.** В трёх документах Дня 1 обнаружено противоречие с модулем:

- «открытая исследовательская программа»;
- «4 микро-кейса»;
- кейсы А–Г вместо трёх сквозных кейсов;
- в обосновании направление потока опиралось на «кейсы Б и В».

Предлагаемая правка:

- термин — «исследовательская модель GRA»;
- кейсы 1 → 3 → 2 на слайдах 10–17, 20–21 и 22–26;
- Промпт-фреймер — на слайде 28.

Тайминг, механики вовлечения, таблица статусов и значки ●◐○ не меняются.
**Выполнено** (версия 0.3; номера слайдов сверены между презентацией и
сценарием лектора).

**A-14 — Minor.** В файле
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/40-practice-and-cases.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/40-practice-and-cases.md)
обнаружено противоречие с новой структурой Дня 1. Файл размечал четыре
микро-кейса А–Г, его SSOT-ссылка вела на якорь `#микро-кейсы` обоснования, а
влияние было записано как компонент массы M5. Предлагаемая правка: три
сквозных кейса, собственный кейс слушателя и Промпт-фреймер Дня 1; влияние на
решение фиксируется отдельно от массы. **Выполнено** (Направление 2).

**A-15 — Minor.** В файле
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/50-open-research.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/50-open-research.md)
обнаружено противоречие. Ранжирование опиралось на «Кейсы Б и В», которых больше
нет. В §3 ранние артефакты описаны как ещё не исправленные. В §5 правка корпуса
отложена до «решения фаундера», хотя issue #659 прямо поручает исправить
противоречия. Предлагаемая правка:

- «Кейсы 2 и 3…»;
- колонка «Статус (#659)» со значением «Исправлено» и ссылкой на этот аудит;
- предложение 1 в §5 — «принято и выполнено»;
- новый §8 — самоаудит против условий #659.

**Выполнено** (версия 0.2).

**A-16 — Minor.** В файле
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/README.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/README.md)
обнаружено противоречие:

- ссылка на исследование #610 вела на рабочую ветку `issue-610-0ac7e285f2ac`,
  а не на `main`;
- строка Дня 1 обещала «4 микро-кейса»;
- модуль был назван «GRA как открытая исследовательская программа»;
- часть ссылок была относительной.

Предлагаемая правка: ссылка на `main`; три сквозных кейса и версия 0.3;
«Исследовательская модель GRA»; абсолютные URL; ссылка на этот аудит.
**Выполнено** (версия 1.5).

**A-20 — Minor — F4.** В файле
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/20-taxonomy.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/20-taxonomy.md#3-масса)
обнаружено противоречие внутри самой нормы. Определение в §3 говорит: «Влияние
на решение — это проявление массы в конкретном контексте, а не её
определение». При этом таблица «Компоненты массы» перечисляет M5 «Контекстная
(влияние на решение)» как компонент массы. Предлагаемая правка: компоненты
массы — M1–M4, а строку M5 подписать «Не компонент массы: влияние на конкретное
решение». ID M5 сохранить: на него ссылаются `30-decision-framework.md` и
разметка кейсов. **Выполнено.**

### Реестры Хаба и смежные модули

**A-17 — Minor.** В файлах
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ops/artifact-map.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ops/artifact-map.md)
и
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/README.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/README.md)
обнаружено противоречие:

- описания модуля — «GRA как открытая исследовательская программа»;
- обоснование Дня 1 — «4 микро-кейса»;
- файл практики — «Разметка четырёх микро-кейсов»;
- файл 50 — «старые артефакты с «дистанция обратна доверию»», как будто
  противоречие не устранено.

Предлагаемая правка: привести описания к текущему состоянию и
зарегистрировать новые артефакты (этот аудит и `exp/day1-methodology-659/`).
**Выполнено.**

**A-18 — Minor — F3.** В файле
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/20-taxonomy.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/normalization/20-taxonomy.md)
обнаружено противоречие: в таблице переноса GRA на вход BA-процесса сказано
«Дистанция | обратна доверию и близости». Модуль BA-нормализации берёт это
значение из старого отчёта фаундера, поэтому ошибка корпуса GRA перешла в
другой домен. Предлагаемая правка: описать дистанцию как многомерную.
BA-интерпретацию «цена и длительность получения уточнения» сохранить и
привязать к физической/временной и канальной осям: так она точнее, чем через
доверие. Гипотезу H6 этого модуля правка не меняет. **Выполнено** (одна ячейка
таблицы; в `related_issues` добавлен #659).

**A-19 — Info.** В файле
[https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/CHANGELOG.md](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/CHANGELOG.md)
запись issue #657 называет модуль «GRA как открытая исследовательская
программа». **Правка не требуется:** CHANGELOG — журнал событий, и
переписывать историю нельзя. Переименование зафиксировано новой записью issue
#659.

**Info — исключение по ссылкам.** README в
[`exp/gra-research-program-657/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/exp/gra-research-program-657/README.md)
и `exp/day1-methodology-659/` содержат по одной относительной ссылке на
родительский отчёт. Это не противоречие, а объявленное исключение по п. 3
раздела Method.

**Итоговый вердикт: условно соответствует.** После правок противоречий между
текстами нет: скрипт поиска печатает `hits: 0`, проверка якорей — `bad: 0`,
валидаторы проходят. Условие вердикта относится к содержанию модели: её
гипотезы не проверены эмпирически, и аудит согласованности этого не заменяет.

## Remediation / Deviation

| Что | Тип | Решение |
| --- | --- | --- |
| A-01…A-09, A-11…A-18, A-20 | remediation | Исправлено в [PR #661](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/661). Версии ранних артефактов подняты до 0.2, в каждом есть пометка «Правка версии 0.2 (issue #659)». Остальной текст не переписан: это исторические отчёты, и правка касается только модели GRA |
| A-10, A-19 | explicit no-op | Противоречия нет, или текст является журналом событий |
| Относительные ссылки в README `exp/` | exception | Форму ссылки проверяет `tools/validate-evidence-structure.sh`; исключение объявлено в README |
| Эмпирическая проверка HP-D и HM-I | follow-up | [Бэклог, Спринт 29](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ops/backlog.md#спринт-29-курс-по-репутационным-технологиям-после-дня-1), B-231 |
| Юридическая проверка формулировок кейсов: массаж — медицинская услуга или нет; реклама; инвестиционные формулировки; 381-ФЗ | follow-up | [Бэклог, Спринт 29](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ops/backlog.md#спринт-29-курс-по-репутационным-технологиям-после-дня-1), B-230. Кейсы синтетические и не используют имён, но проверка нужна до записи эфира |
| Имя каталога `gra-research-program/` расходится с термином «исследовательская модель» | deviation | Имя сохранено ради стабильности ссылок. Переименование вынесено в [бэклог](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/ops/backlog.md#спринт-29-курс-по-репутационным-технологиям-после-дня-1), B-232: оно затрагивает ссылки во всём Хабе |

## Related Artifacts

- Issue [#659](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/659), родительская работа [#657](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/657), материалы Дня 1 — [#653](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/653).
- Норма: [`30-decision-framework.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/30-decision-framework.md), [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/20-taxonomy.md), [`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/10-theory.md#1-происхождение-gra).
- Доказательная база: [`exp/day1-methodology-659/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/exp/day1-methodology-659/README.md), [`exp/gra-research-program-657/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/exp/gra-research-program-657/README.md).
- Стандарт: [`standards/audit-standard.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/audit-standard.md).
- Пример формы: [аудит мета-модели БА](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/audit/2026-09-15-ba-meta-model-cross-check-audit.md).
