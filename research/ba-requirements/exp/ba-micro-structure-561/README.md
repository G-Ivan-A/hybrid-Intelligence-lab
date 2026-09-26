---
status: draft
version: 0.2
updated: 2026-09-08
temperature: 0.1
type: experiment
---

# exp: ba-micro-structure-561

Evidence container для датированного замера
[`../../2026-09-08-artifact-structure-variance-facts.md`](../../2026-09-08-artifact-structure-variance-facts.md)
и модуля
[`research/ba-requirements/artifact-micro-structure/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/research/ba-requirements/artifact-micro-structure),
issue [#561](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/561).

> **Ссылки.** Issue #561 требует абсолютных ссылок. Относительная ссылка на
> родительский отчёт выше — вынужденное исключение: её форму машинно проверяет
> [`tools/validate-evidence-structure.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/validate-evidence-structure.sh).

## Что здесь измеряется

Контракты 2 и 3 issue #561 требуют классификации допустимых структур артефакта
и синтеза Golden Set там, где исторические прогоны не покрывают продуктовые
случаи. Оба вывода зависят от одного факта: **насколько устойчива структура
результирующего документа в корпусе `runs/`**. Написанный руками ответ на этот
вопрос непроверяем, поэтому он вычисляется: скрипт обходит `outputs/` всех
прогонов, отображает подписи разделов в закрытый словарь слотов и считает
расхождение скелетов внутри одной задачи и одного процесса.

Машинно проверяемые утверждения родительского отчёта: размер корпуса,
сегментация `outputs/` на три класса файлов, число результирующих документов и
число различных скелетов среди них, коэффициенты Жаккара по группам,
частота и позиционное распределение слотов, классы формата, продуктовое
покрытие.

Содержательной интерпретации (что означает расхождение, какой должна быть
норма) здесь нет — она в родительском отчёте и в модуле.

## Состав

| Файл | Что это |
| --- | --- |
| [`measure-artifact-structure.py`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-micro-structure-561/measure-artifact-structure.py) | измеритель; словарь слотов, продуктовые правила и правила формата — именованные константы в шапке |
| [`artifact-structure.json`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-micro-structure-561/artifact-structure.json) | результат: сводка + запись на каждый просмотренный артефакт |
| [`measure-artifact-structure.log`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-micro-structure-561/measure-artifact-structure.log) | вывод прогона, фиксирующий опубликованные цифры и коммит корпуса |
| [`2026-09-08-golden-set-contact-center-ivr-settings.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-micro-structure-561/2026-09-08-golden-set-contact-center-ivr-settings.md) | синтетический эталон, продуктовый класс `contact-center` (функция с настройками) |
| [`2026-09-08-golden-set-self-service-lk.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-micro-structure-561/2026-09-08-golden-set-self-service-lk.md) | синтетический эталон, продуктовый класс `self-service-lk` (функция без настроек) |
| [`probe-kb-slot-fit.py`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-micro-structure-561/probe-kb-slot-fit.py) | проба словаря слотов на корпусе [runtime KB](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/main/docs/kb): отображение разделов, доли по профилям, порядковые утверждения |
| [`kb-slot-fit.json`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-micro-structure-561/kb-slot-fit.json) | исторический результат пробы на `mango_ba_prompts@8cbf82a`: сводка, запись на каждый документ, полный список разделов, ушедших в слот по умолчанию |
| [`probe-kb-slot-fit.log`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-micro-structure-561/probe-kb-slot-fit.log) | вывод прогона пробы, фиксирующий опубликованные цифры и коммит корпуса |
| [`2026-09-08-golden-set-vpbx-api.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-micro-structure-561/2026-09-08-golden-set-vpbx-api.md) | синтетический эталон, профиль `P-API`, продуктовый класс `voice-ucaas` |
| [`2026-09-08-golden-set-hardware-gateway.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-micro-structure-561/2026-09-08-golden-set-hardware-gateway.md) | синтетический эталон, профиль `P-DEVICE`, продуктовый класс `hardware` |
| [`2026-09-08-golden-set-security-access.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-micro-structure-561/2026-09-08-golden-set-security-access.md) | синтетический эталон, продуктовый класс `security` (профиль `P-SETTINGS`) |
| [`2026-09-08-golden-set-multi-product.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-micro-structure-561/2026-09-08-golden-set-multi-product.md) | синтетический эталон на два продукта с разными профилями в одной задаче (`MP-1`…`MP-6`) |
| [`2026-09-08-bcreq-document-skeleton.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-micro-structure-561/2026-09-08-bcreq-document-skeleton.md) | единый скелет документа BCREQ: слоты × классы формата × проекции в одном файле, словарь причин пустоты |

## Воспроизведение

```bash
git clone https://github.com/G-Ivan-A/mango_ba_prompts.git /tmp/mango
python3 measure-artifact-structure.py --mango /tmp/mango
```

Коммит, на котором получены опубликованные цифры, записан в поле
`corpus.commit` результата: `8cbf82aa73129ec5747af07f790aaf438b0fb6e9`.
На других коммитах цифры будут другими — это ожидаемо, отчёт датирован.

## Воспроизведение пробы на корпусе знаний

```bash
git clone https://github.com/G-Ivan-A/mango-ba-ai-runtime.git /tmp/mango-runtime
git -C /tmp/mango-runtime checkout ed42b3cd0eed2774c9b080232ca00484d9a4f7cd
python3 probe-kb-slot-fit.py --runtime /tmp/mango-runtime --out /tmp/kb-slot-fit.json
```

Опубликованный `kb-slot-fit.json` остаётся снимком исходного корпуса
`mango_ba_prompts@8cbf82aa73129ec5747af07f790aaf438b0fb6e9`; новый прогон
записывается отдельно, чтобы не заменить историческое свидетельство.
KB перемещена в [runtime `docs/kb`](https://github.com/G-Ivan-A/mango-ba-ai-runtime/tree/main/docs/kb).
Проверка перенесённого снимка `ed42b3c` дала те же `summary`, порядковые
утверждения и записи пяти документов, за исключением путей и метаданных корпуса.

Проба отвечает на пункт 3 комментария фаундера к PR
[#562](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/562):
проверяет словарь слотов на **независимом** корпусе KB, из которого
словарь не выводился. Интерпретация — в отчёте
[`../../2026-09-08-kb-slot-fit-facts.md`](../../2026-09-08-kb-slot-fit-facts.md).

## Статус Golden Set

Шесть эталонов в этом каталоге **синтетические**. Они покрывают все четыре
профиля (`P-SETTINGS`, `P-NO-SETTINGS`, `P-API`, `P-DEVICE`), классы `security`
и `hardware`, для которых исторических данных нет вовсе, и случай двух
продуктов с разными профилями в одной задаче. Эталоны не извлечены из корпуса и не
являются поставленными заказчику документами: замер (§6 родительского отчёта)
показал, что чистых продуктовых выборок в `runs/` нет, поэтому индукция по
истории невозможна. Эталоны собраны как модель ожидаемой структуры по правилам
модуля и подлежат проверке человеком до любого применения в качестве few-shot
образца. До прохождения этой проверки их статус — `draft`, и они не являются
нормой.

## Границы измерения

- Учитываются только заголовки уровня `##`. Документ, у которого структура
  выражена жирным текстом без заголовков, будет измерен как малоструктурный —
  это занижает оценку структурности, а не завышает её.
- Слот присваивается по первому сработавшему правилу; раздел со смешанным
  содержанием получает один слот, поэтому смешение (например, ФТ и UI в одном
  разделе) измерением **занижается**.
- Продуктовая разметка лексическая и множественная. Она пригодна для ответа
  «чистых выборок нет» и непригодна для утверждений о долях.
- Корпус — одна спица. Переносимость выводов на другие предметные области
  здесь не проверяется.
