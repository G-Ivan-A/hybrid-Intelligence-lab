---
status: draft
version: 0.1
updated: 2026-07-02
temperature: 0.1
type: experiment-output
---

# Test 4 — адаптация к изменению требований

> Evidence for [research report](../../2026-07-02-task-execution-modes-research.md), issue [#330](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/330). Regenerate with `python3 research/hub/exp/task-execution-modes-330/classify.py`.

Классификатор переклассифицирует задачу при смене формулировки в **3/3** сценариях (переключение типа зафиксировано). Это показывает: тип/режим — функция текущей формулировки, а не «залипшего» состояния.

| Сценарий | Before (тип/режим) | After (тип/режим) | Переключение | After верен? |
| --- | --- | --- | --- | --- |
| E-1 | RFC/Creative | ADR/Hybrid | тип+режим | ✅ |
| E-2 | Analysis/Creative | Audit/Structured | тип+режим | ✅ |
| E-3 | Research/Creative | Chore/Structured | тип+режим | ✅ |
