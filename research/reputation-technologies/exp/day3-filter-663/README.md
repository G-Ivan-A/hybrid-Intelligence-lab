---
status: draft
version: 0.1
updated: 2026-10-11
temperature: 0.1
type: experiment
---

# exp: day3-filter-663

Evidence container для пакета Дня 3 курса, начиная с
[`../../2026-11-02-day3-rationale-and-method.md`](../../2026-11-02-day3-rationale-and-method.md),
по issue [#663](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/663).

> **Ссылки.** Issue #663 требует абсолютных ссылок. Относительная ссылка на
> родительский отчёт выше — вынужденное исключение: её форму машинно проверяет
> [`tools/validate-evidence-structure.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/validate-evidence-structure.sh).

## Что здесь лежит

| Файл | Что делает |
| --- | --- |
| `check-day3.sh` | Проверяет три документа Дня 3: нет оценочных прилагательных из запрета issue, нет относительных ссылок, все пять дословных тегов есть в сценарии, 30 слайдов в презентации и сценарии, формулировки программы Дня 3 есть в документах 1 и 2. Печатает число произносимых слов по слотам сценария для проверки плотности |

## Запуск

```bash
bash research/reputation-technologies/exp/day3-filter-663/check-day3.sh
python3 -I research/reputation-technologies/exp/gra-research-program-657/check-gra-anchors.py . \
  research/reputation-technologies/2026-11-02-day3-*.md
```

Ожидаемый результат на 2026-10-11: `check-day3.sh` завершается с кодом 0 и не
печатает строк `FAIL`. Самый плотный слот сценария — 18:44–18:52, около 400
слов на 8 минут: при темпе 120–130 слов в минуту речь занимает чуть больше
3 минут, остальное — голосование и паузы. `check-gra-anchors.py` до слияния
[PR #662](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/662) печатает
`bad: 1` — ссылку документа 1 на обоснование Дня 2, которого ещё нет в `main`.
