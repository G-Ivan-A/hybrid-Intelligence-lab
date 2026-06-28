---
status: draft
version: 0.1
updated: 2026-06-28
temperature: 0.1
type: experiment
context: [hub, mango, clarify, research, analysis, audit, issue-288]
method: repository-scan
---

# Experiment: Research/Analysis/Audit inventory for issue 288

Воспроизводимый scan для cross-repo анализа Research / Analysis / Audit
артефактов в issue #288.

## Scope

Сканируются tracked artifacts из:

- `hybrid-Intelligence-lab`: `research/**`, `docs/**`;
- `mango_ba_prompts`: `research/**`, `docs/**`;
- `clarify-engine-ai`: `research/**`, `docs/**`.

Классификация не опирается только на путь: скрипт использует путь,
frontmatter, первый заголовок и начальные content signals. Итоговый отчёт
использует этот scan как evidence base и дополнительно фиксирует дельты,
подмены понятий и план стандартизации.

Собственные deliverables issue #288 (`2026-06-28-research-analysis-audit-inventory.md`
и `exp-research-analysis-audit-288/`) исключены из Hub baseline, чтобы повторный
запуск после merge не менял матрицу из-за добавленных этим PR файлов.

## Reproduce

```bash
git clone --depth 1 https://github.com/G-Ivan-A/mango_ba_prompts.git /tmp/issue-288-mango_ba_prompts
git clone --depth 1 https://github.com/G-Ivan-A/clarify-engine-ai.git /tmp/issue-288-clarify-engine-ai
python3 research/hub/exp-research-analysis-audit-288/scan-artifacts.py \
  --mango-root /tmp/issue-288-mango_ba_prompts \
  --clarify-root /tmp/issue-288-clarify-engine-ai
```

## Outputs

| Output | Назначение |
| --- | --- |
| [artifact-classification.json](outputs/artifact-classification.json) | Полный machine-readable scan с SHA репозиториев, путями, source signals и классификацией. |
| [2026-06-28-artifact-classification-matrix.md](outputs/2026-06-28-artifact-classification-matrix.md) | Markdown-матрица для review и ссылок из основного отчёта. |
