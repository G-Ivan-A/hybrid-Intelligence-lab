---
status: draft
version: 0.1
updated: 2026-11-11
temperature: 0.1
type: experiment
contributors: [konard]
ai-models: [claude-opus-5-5]
---

# exp: ai-team-management-program-732

Контейнер воспроизводимости итерации 2 паспорта проекта
[«ИИ в работе с командой»](../../../../projects/ai-team-management-program/README.md),
issue [#732](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/732).
Экономика варианта 2 посчитана в той же модели, что и вариант 1:
[`../ai-team-management-program-730/economics-model.py`](../ai-team-management-program-730/economics-model.py)
(правка на месте, без копии модели).

Родительские отчёты итерации 2: аудит каналов кандидатов
[`2026-11-11-candidate-public-channels-audit.md`](../../2026-11-11-candidate-public-channels-audit.md)
и остальные отчёты от 2026-11-11 в каталоге
[`research/ai-team-management-program/`](../../README.md); бриф
[`2026-11-11-brief-common.md`](2026-11-11-brief-common.md) задаёт им общий формат.

## Состав

| Файл | Что это |
| --- | --- |
| [`2026-11-11-brief-common.md`](2026-11-11-brief-common.md) | общий бриф исследовательских потоков итерации 2: формат отчёта, правила сбора только публичных профессиональных сведений, шкала доступности контакта К0–К3 |
| [`render-customer-response.py`](render-customer-response.py) | вёрстка [ответа заказчику](../../../../projects/ai-team-management-program/docs/passport/customer-response.md) в PDF A4 через headless Chrome; завершается ошибкой, если страниц больше двух |

## Воспроизведение

```bash
# из корня репозитория; нужен Chrome или Chromium (переменная CHROME — путь к браузеру)
python3 -I research/ai-team-management-program/exp/ai-team-management-program-732/render-customer-response.py
# PDF: projects/ai-team-management-program/docs/passport/customer-response.pdf — страниц: 2
```

Скрипт использует только стандартную библиотеку Python 3 и браузер; сеть не
нужна. Markdown переводится в HTML собственным конвертером ограниченного
подмножества (заголовки, абзацы, списки, таблицы, жирный шрифт, ссылки),
поэтому внешние библиотеки вёрстки не требуются.

## Ограничения

Число страниц определяется вёрсткой Chrome и установленными шрифтами
(«PT Sans», при отсутствии — «Liberation Sans» или Arial). На машине с
другими шрифтами текст может сместиться; проверка «не больше двух страниц»
в скрипте ловит такой случай.
