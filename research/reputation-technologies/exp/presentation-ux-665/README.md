---
status: draft
version: 0.1
updated: 2026-10-14
temperature: 0.1
---

# Presentation UX: проверка issue #665

Родительский отчёт — [RFC от 2026-10-12](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/gra-research-program/presentation-rfc/2026-10-12-rfc-presentation-ux-days-1-3.md), задача — [#665](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/665). Контейнер проверяет редакционные признаки самостоятельного чтения, не обучающий эффект. Родительский RFC отклонён фаундером в [#667](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/667); проверка оставлена в CI, пока презентации не пересобраны по [новому RFC](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/2026-10-12-rfc-days-1-3-logic.md). Презентация Дня 2 пересобрана по RFC v0.3 в [#673](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/673): её проверяет [check-day2.py](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/reputation-technologies/exp/day2-rebuild-673/README.md), а здесь остались Дни 1 и 3.

Исходный датированный исследовательский материал для сравнения — [презентация Дня 1](../../2026-10-07-day1-presentation-653.md); обоснование программы — [метод Дня 1](../../2026-10-07-day1-rationale-and-method-653.md). Подробный результат проверки всех трёх дней находится в родительском RFC выше.

| Артефакт | Назначение |
| --- | --- |
| `check-presentation-ux.py` | 74 слайда Дней 1 и 3, сохранность исходных заголовков/визуалов/промптов, восемь инструментов в каждом дне и полное профильное ревью на 111 строк; 16 повреждений в режиме self-test |
| `render-preview.py` | Воспроизводимый HTML-макет трёх плотных слайдов Д1/7, Д2/10, Д3/13 из текущего Markdown; Д2/10 — из `16e2577`, последней версии до #673; исходный вариант берётся из `6428ade` |
| `before.png`, `after.png` | Снимки браузера с одинаковой сеткой 1920×1080; контекст добавлен на экран, вывод выделен отдельно |

## Запуск из корня

```bash
python3 research/reputation-technologies/exp/presentation-ux-665/check-presentation-ux.py --self-test
python3 research/reputation-technologies/exp/presentation-ux-665/render-preview.py --before --output /tmp/presentation-ux-665/before.html
python3 research/reputation-technologies/exp/presentation-ux-665/render-preview.py --output /tmp/presentation-ux-665/after.html
python3 -m http.server 8765 --bind 127.0.0.1 --directory /tmp/presentation-ux-665
```

Открыть обе страницы в браузере с viewport 1920×1080 и снять full-page screenshot. После проверки остановить сервер. Проверить у `.text` `scrollHeight <= clientHeight` и у каждого `.slide` высоту 1080. Основные тезисы и поясняющий абзац — 32 CSS px (24 pt); схема дублирует цвет словами и формой. Шрифты и плотность в реальном PPTX/PDF требуют отдельного просмотра.

Это прототип текстовой иерархии, а не финальный дизайн всей колоды. SVG-схемы построены кодом по выбранным спецификациям; AI-изображения не генерировались. Из трёх макетов нельзя выводить отсутствие переполнения всех 111 слайдов. Длинные восемь строк упражнений ещё требуют двух панелей при окончательном экспорте.

Скрипты находятся в каноническом `research/<domain>/exp/<issue-slug>/`, а не в новых верхнеуровневых `examples/` или `experiments/`: это воспроизводимая исследовательская проверка, не расширение структуры Hub. Генерация моделей не нужна; память ограничивается небольшими Markdown/HTML и одним браузером. HTML и временные журналы не коммитятся.
