---
status: draft
version: 0.1
updated: 2026-07-02
temperature: 0.1
type: experiment-output
---

# Test 2 — интерпретация практических issue без контекста

> Evidence for [research report](../../2026-07-02-task-execution-modes-research.md), issue [#330](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/330). Regenerate with `python3 research/hub/exp/task-execution-modes-330/classify.py`.

Тип: **5/5** верно. Режим: **5/5** верно. GT = фактически выполненный артефакт.

| Issue | Вход (усечён) | GT тип | Pred тип | T? | GT режим | Pred режим | M? | Примечание |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| #310 | Инвентаризация Reports-артефактов в Хабе, Mango, C | Analysis | Analysis | ✅ | Creative | Creative | ✅ | Executed as docs/analysis/ inventory. |
| #316 | Определить причину дублирования RFC/ADR, сформиров | Analysis/Chore | Chore | ✅ | Hybrid | Hybrid | ✅ | Mixed: root-cause report (Analysis) + fix (Chore). |
| #320 | Проверка документации на коллизии интерпретации ст | Audit | Audit | ✅ | Structured | Structured | ✅ | Executed as docs/audit/. |
| #322 | Принять ADR-003 и устранить причинные дефекты стан | ADR/Standard | ADR | ✅ | Hybrid | Hybrid | ✅ | Mixed: decision (ADR) + standard edits. |
| #324 | Исправить точечные последствия аудита B-039 | Chore | Chore | ✅ | Structured | Structured | ✅ | Point fixes only. |
