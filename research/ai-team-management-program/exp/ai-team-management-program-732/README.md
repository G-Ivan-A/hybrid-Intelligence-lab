---
status: draft
version: 0.2
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
| [`2026-11-11-brief-common.md`](2026-11-11-brief-common.md) | общий бриф исследовательских потоков итерации 2: формат отчёта, правила сбора только публичных профессиональных сведений, шкала доступности контакта К0–К3 (в пуле — Д0–Д3, чтобы не путать с кейсами К1–К5) |
| [`render-customer-response.py`](render-customer-response.py) | вёрстка [ответа заказчику](../../../../projects/ai-team-management-program/docs/passport/project-summary-6m.md) в PDF A4 через headless Chrome; завершается ошибкой, если страниц больше двух или слов больше 900, и если остались подстановки `{N_...}` |
| [`project-summary-6m-preview.png`](project-summary-6m-preview.png), [`project-summary-3m-preview.png`](project-summary-3m-preview.png) | снимки HTML-вёрстки резюме проекта на 6 и 3 месяца (режим `--html-only`) для визуальной проверки без просмотрщика PDF |

## Воспроизведение

```bash
# из корня репозитория; нужен Chrome или Chromium (переменная CHROME — путь к браузеру)
python3 -I research/ai-team-management-program/exp/ai-team-management-program-732/render-customer-response.py
# PDF: projects/ai-team-management-program/docs/passport/project-summary-6m.pdf — страниц: 2
```

Скрипт использует только стандартную библиотеку Python 3 и браузер; сеть не
нужна. Markdown переводится в HTML собственным конвертером ограниченного
подмножества (заголовки, абзацы, списки, таблицы, жирный шрифт, ссылки),
поэтому внешние библиотеки вёрстки не требуются.

## Бюджет исследовательских токенов

Предел задачи — 800 тыс. токенов на исследования. Учтены пять
исследовательских потоков (данные о расходе — из отчётов агентов-исполнителей);
работа над паспортом, вёрсткой и проверками в предел не входит.

| Поток | Отчёт | Токены |
| --- | --- | ---: |
| Аудит публичных каналов кандидатов | [`2026-11-11-candidate-public-channels-audit.md`](../../2026-11-11-candidate-public-channels-audit.md) | 45 986 |
| Стартапы: ИИ-агенты и прикладной ИИ | [`2026-11-11-ru-startups-ai-agents.md`](../../2026-11-11-ru-startups-ai-agents.md) | 95 842 |
| Пять кейсов: внедрения в России и за рубежом | [`2026-11-11-ai-management-use-cases-evidence.md`](../../2026-11-11-ai-management-use-cases-evidence.md) | 91 436 |
| Несколько кейсов в группе, формат ответа, мотивация | [`2026-11-11-multi-case-design-and-proposal-format-evidence.md`](../../2026-11-11-multi-case-design-and-proposal-format-evidence.md) | 92 954 |
| Источники стартап-баз; робототехника и автоматизация процессов | [`2026-11-11-ru-startups-sources-robotics-bpa.md`](../../2026-11-11-ru-startups-sources-robotics-bpa.md) | 98 710 |
| **Итого** | | **≈ 424 928 (53% предела)** |

Предел не превышен. Что не закрыто кабинетным исследованием (сверка
27 стартапов с ЕГРЮЛ, подтверждение ролей по сниппетам, кейс К5) требует не
токенов, а доступа к реестрам и контакта; предложение по дополнительному
исследованию — в описании PR #733 и в бэклоге.

## Ограничения

Число страниц определяется вёрсткой Chrome и установленными шрифтами
(«PT Sans», при отсутствии — «Liberation Sans» или Arial). На машине с
другими шрифтами текст может сместиться; проверка «не больше двух страниц»
в скрипте ловит такой случай.
