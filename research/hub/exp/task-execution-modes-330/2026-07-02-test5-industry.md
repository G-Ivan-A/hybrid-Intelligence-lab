---
status: draft
version: 0.1
updated: 2026-07-02
temperature: 0.1
type: experiment-output
---

# Test 5 — применение индустриальных паттернов к нашим задачам

> Evidence for [research report](../../2026-07-02-task-execution-modes-research.md), issue [#330](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/330). Regenerate with `python3 research/hub/exp/task-execution-modes-330/classify.py`.

Сопоставление нашего эмпирического режима с рекомендацией трёх индустриальных рамок (Cynefin, Bloom, cognitive load). Согласовано: **6/6**.

| Задача | Наш режим | Cynefin домен | Cynefin отклик | Bloom уровень | Вердикт |
| --- | --- | --- | --- | --- | --- |
| B-039 audit RFC/ADR collisions | Structured | Complicated | sense-analyze-respond (expert/good practice) | Evaluate | match |
| B-016 RFC research structure | Creative | Complex | probe-sense-respond (emergent practice) | Create | match |
| B-020 update glossary | Structured | Clear | sense-categorize-respond (best practice) | Apply | match |
| #330 research execution modes | Creative | Complex | probe-sense-respond (emergent practice) | Create/Analyze | match |
| B-018 create research-standard | Hybrid | Complicated | sense-analyze-respond (good practice) | Create | match (Hybrid ~ constrained Complicated) |
| #316 root-cause + fix | Hybrid | Complex->Complicated | probe then analyze | Analyze+Apply | match (mixed maps to Hybrid) |

Чтение: Cynefin *Clear* -> Structured (best practice), *Complicated* -> Structured/Hybrid (good practice, экспертный анализ), *Complex* -> Creative (emergent practice, probe-sense-respond). Наш Hybrid систематически ложится на *Complicated с жёстким контейнером* и на смешанные задачи.
