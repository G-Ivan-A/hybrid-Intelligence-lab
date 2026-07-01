---
status: draft
version: 0.1
updated: 2026-07-01
temperature: 0.1
type: experiment
context: [hub, mango, clarify, reports, audit-report, general-report, statistical-report, issue-310]
method: repository-scan
---

# Experiment: Reports inventory for issue 310

Воспроизводимый scan для cross-repo анализа Reports-артефактов в issue #310.
Скрипт создаёт evidence layer для основного анализа
[2026-07-01-reports-artifacts-inventory.md](../../../../docs/analysis/2026-07-01-reports-artifacts-inventory.md).

## Scope

Сканируются tracked text artifacts из:

- `hybrid-Intelligence-lab`: `reports/**`, `docs/**`, `research/**`,
  `governance/**`;
- `mango_ba_prompts`: `reports/**`, `docs/**`, `research/**`,
  `governance/**`;
- `clarify-engine-ai`: `reports/**`, `docs/**`, `research/**`,
  `governance/**`.

Классификация не опирается только на путь: `scan-reports.py` использует path,
frontmatter и первый заголовок, чтобы выделить report-like candidates по
подтипам `audit`, `report`, `statistics` и relation `output-for-audit`,
`output-for-analysis`, `standalone-report`.

Собственные deliverables issue #310 (`2026-07-01-reports-artifacts-inventory.md`
и `exp/reports-inventory-310/`) исключены из Hub baseline, чтобы повторный
запуск после merge не менял матрицу из-за добавленных этим PR файлов.

## Reproduce

```bash
git clone https://github.com/G-Ivan-A/mango_ba_prompts.git /tmp/issue-310-mango_ba_prompts
git clone https://github.com/G-Ivan-A/clarify-engine-ai.git /tmp/issue-310-clarify-engine-ai
git -C /tmp/issue-310-mango_ba_prompts checkout 995c16d175f916ae397d0efc2231f8d30f82c518
git -C /tmp/issue-310-clarify-engine-ai checkout 96c288fd13a2d7cc7c3e3cdd52574944858e6255

python3 research/hub/exp/reports-inventory-310/scan-reports.py \
  --mango-root /tmp/issue-310-mango_ba_prompts \
  --clarify-root /tmp/issue-310-clarify-engine-ai
```

## Outputs

Контейнер `exp/` использует плоскую структуру без вложенного `outputs/`
(RFC B-016 v0.2, P2): evidence-файлы лежат рядом с `README.md` и скриптом.

| Output | Назначение |
| --- | --- |
| [reports-inventory.json](reports-inventory.json) | Полный machine-readable scan с SHA репозиториев, path buckets, frontmatter signals, subtype, relation and routing hints. |
| [2026-07-01-reports-artifact-matrix.md](2026-07-01-reports-artifact-matrix.md) | Markdown-матрица для review и ссылок из основного отчёта. |
