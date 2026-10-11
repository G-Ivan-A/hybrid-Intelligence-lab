---
status: draft
version: 0.1
updated: 2026-10-10
temperature: 0.1
type: experiment
---

# exp: day1-methodology-659

Evidence container для правок версии 0.3 документов Дня 1, начиная с
[`../../2026-10-07-day1-rationale-and-method-653.md`](../../2026-10-07-day1-rationale-and-method-653.md),
и сквозной проверки домена по issue
[#659](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/659).
Результаты проверки — в
[аудите согласованности](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/audit/2026-10-10-reputation-technologies-consistency-audit.md).

> **Ссылки.** Issue #659 требует абсолютных ссылок. Относительная ссылка на
> родительский отчёт выше — вынужденное исключение: её форму машинно проверяет
> [`tools/validate-evidence-structure.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/validate-evidence-structure.sh).
> По той же причине `absolutize-links.py` не запускают на README в `exp/`.

## Что здесь лежит

| Файл | Что делает |
| --- | --- |
| `absolutize-links.py` | Переписывает относительные ссылки markdown на абсолютные URL ветки `main`. Якоря внутри страницы, `http(s)` и `mailto` не трогает. Если цель ссылки не существует, сообщает и оставляет ссылку как есть |
| `scan-contradictions.sh` | Ищет в домене формулировки, которые противоречат модулю «Исследовательская модель GRA»: старую генеалогию, «дистанция = обратное доверию», «открытая исследовательская программа», относительные ссылки |

## Запуск

```bash
python3 -I research/reputation-technologies/exp/day1-methodology-659/absolutize-links.py . \
  research/reputation-technologies/*.md
bash research/reputation-technologies/exp/day1-methodology-659/scan-contradictions.sh .
python3 -I research/reputation-technologies/exp/gra-research-program-657/check-gra-anchors.py . \
  research/reputation-technologies/*.md research/reputation-technologies/gra-research-program/*.md
```

Ожидаемый результат на 2026-10-10: `scan-contradictions.sh` печатает `hits: 0`,
`check-gra-anchors.py` — `bad: 0`.
