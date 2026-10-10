---
status: draft
version: 0.1
updated: 2026-10-10
temperature: 0.1
type: experiment
---

# exp: gra-research-program-657

Evidence container для модуля
[`research/reputation-technologies/gra-research-program/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/research/reputation-technologies/gra-research-program)
и правок версии 0.2 в
[`../../2026-10-07-day1-rationale-and-method-653.md`](../../2026-10-07-day1-rationale-and-method-653.md),
issue [#657](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/657).

> **Ссылки.** Issue #657 требует абсолютных ссылок. Относительная ссылка на
> родительский отчёт выше — вынужденное исключение: её форму машинно проверяет
> [`tools/validate-evidence-structure.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/validate-evidence-structure.sh).

## Что здесь проверяется

Модуль и материалы Дня 1 ссылаются друг на друга абсолютными URL с якорями
разделов (`…/10-theory.md#2-принцип-структурного-соответствия`).
`tools/validate-rrp-links.sh` проверяет только наличие ссылок 40 → 10/20/30, но
не существование якорей. `check-gra-anchors.py` проверяет, что каждая
абсолютная ссылка на файл Хаба ведёт на существующий файл и, если есть якорь,
на существующий заголовок по правилам GitHub-слагов.

## Запуск

```bash
python3 -I research/reputation-technologies/exp/gra-research-program-657/check-gra-anchors.py . \
  research/reputation-technologies/gra-research-program/*.md \
  research/reputation-technologies/2026-10-07-day1-*.md
```

Результат на 2026-10-10: `bad: 0` (9 файлов). Код возврата 1, если найдена
хотя бы одна битая ссылка или якорь.
