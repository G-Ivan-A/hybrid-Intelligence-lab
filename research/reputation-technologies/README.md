---
status: superseded
version: 2.0
updated: 2026-11-04
temperature: 0.1
---

# Research: Reputation Technologies (GRA) — выведен из Хаба

> **Historical compatibility path. Do not use as an active artifact.** Домен
> репутационных технологий (GRA) и курса «Технограда» выведен из дерева Хаба.
> **Замена:** спица [`G-Ivan-A/aether-orbis-gra`](https://github.com/G-Ivan-A/aether-orbis-gra); задачи курса
> ведутся только в её бэклоге (исключение A-4 снято). **Причина:** домен
> перенесён в спицу, а Хаб хранит только глобальные исследования и методологию.
> **Решение:** [RFC #721](../../docs/rfc/2026-11-04-rfc-gra-extraction-completion-and-hub-cleanup.md),
> [ADR-022](../../docs/adr/2026-11-adr-022-hub-archive-and-extraction-redirect.md),
> [issue #725](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/725) (ответы владельца Q-1…Q-6).

Здесь — только манифест redirect по
[стандарту выбытия](../../standards/artifact-deprecation-standard.md#manifest-redirect):
куда ушёл каждый прежний путь под `research/reputation-technologies/`. Ссылки исторических документов на
эти пути валидатор разрешает по этой таблице
(`path_migrations` в [`.hub-profile.json`](../../.hub-profile.json)).

## Где теперь содержимое

- **Перенесённое в спицу** — SHA-ссылка на копию в спице на коммите
  `b49acde`; актуальная версия — по тому же пути на `main` спицы.
- **Архив** — аннотированный тег
  [`archive/reputation-technologies-2026-11`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/archive/reputation-technologies-2026-11/research/reputation-technologies/): коммит Хаба, где домен лежит целиком,
  без удалённого по мандату и без персональных данных.
- **Удалённое** — рабочие черновики R9 по мандату Q-2 и файл с персональными
  данными по Q-4. В тег не входят; история git не переписана, последняя версия —
  коммит `48ebe52`.
- **Стратегия партнёров (#292)** — осталась в Хабе как глобальное исследование:
  [research/education/2026-06-29-partner-attraction-strategy.ru.md](../education/2026-06-29-partner-attraction-strategy.ru.md).

| Диспозиция | Файлов |
| --- | --- |
| архив: тег | 59 |
| архив: тег; перенос в спицу — GRA-003 (Q-3) | 1 |
| перенесён в Хаб: глобальное исследование (Q-3) | 1 |
| перенесён в спицу | 37 |
| удалён по мандату (Q-2) | 73 |
| удалён: персональные данные (Q-4), в тег не входит | 1 |
| **Итого** | **172** |

## Манифест

| Прежний путь | Диспозиция | Адрес |
| --- | --- | --- |
| `research/reputation-technologies/2026-06-20-executive-summary.ru-en.md` | перенесён в спицу | [docs/history/2026-06-20-executive-summary.ru-en.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/docs/history/2026-06-20-executive-summary.ru-en.md) |
| `research/reputation-technologies/2026-06-20-founders-vision-and-framework.ru.md` | перенесён в спицу | [docs/history/2026-06-20-founders-vision-and-framework.ru.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/docs/history/2026-06-20-founders-vision-and-framework.ru.md) |
| `research/reputation-technologies/2026-06-20-framework-standard.en.md` | перенесён в спицу | [docs/history/2026-06-20-framework-standard.en.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/docs/history/2026-06-20-framework-standard.en.md) |
| `research/reputation-technologies/2026-06-20-glossary.ru-en.md` | перенесён в спицу | [docs/history/2026-06-20-glossary.ru-en.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/docs/history/2026-06-20-glossary.ru-en.md) |
| `research/reputation-technologies/2026-06-20-white-paper.en.md` | перенесён в спицу | [docs/history/2026-06-20-white-paper.en.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/docs/history/2026-06-20-white-paper.en.md) |
| `research/reputation-technologies/2026-06-29-partner-attraction-strategy.ru.md` | перенесён в Хаб: глобальное исследование (Q-3) | [research/education/2026-06-29-partner-attraction-strategy.ru.md](../education/2026-06-29-partner-attraction-strategy.ru.md) |
| `research/reputation-technologies/2026-09-24-introductory-course-options-610.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/2026-09-24-introductory-course-options-610.md) |
| `research/reputation-technologies/2026-09-30-course-sources-and-presentations-650.md` | архив: тег; перенос в спицу — GRA-003 (Q-3) | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/2026-09-30-course-sources-and-presentations-650.md) |
| `research/reputation-technologies/2026-10-07-day1-lecturer-script-653.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/2026-10-07-day1-lecturer-script-653.md) |
| `research/reputation-technologies/2026-10-07-day1-presentation-653.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/2026-10-07-day1-presentation-653.md) |
| `research/reputation-technologies/2026-10-07-day1-rationale-and-method-653.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-01/rationale-and-method.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-01/rationale-and-method.md) |
| `research/reputation-technologies/2026-10-12-rfc-days-1-3-logic.md` | перенесён в спицу | [education/technograd-reputation-engineering/course-logic.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/course-logic.md) |
| `research/reputation-technologies/2026-10-13-day1-rebuild-task-671.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/2026-10-13-day1-rebuild-task-671.md) |
| `research/reputation-technologies/2026-10-14-day1-lecturer-gra-research.md` | удалён: персональные данные (Q-4), в тег не входит | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/2026-10-14-day1-lecturer-script.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-01/lecturer-script.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-01/lecturer-script.md) |
| `research/reputation-technologies/2026-10-14-day1-presentation-gamma.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-01/presentation.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-01/presentation.md) |
| `research/reputation-technologies/2026-10-15-day1-slide-standard-and-gate-677.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-01/slide-standard-and-gate.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-01/slide-standard-and-gate.md) |
| `research/reputation-technologies/2026-10-24-handout-materials-master-prompt-registry-days-1-4.md` | перенесён в спицу | [education/technograd-reputation-engineering/handouts/prompt-and-handout-registry.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/handouts/prompt-and-handout-registry.md) |
| `research/reputation-technologies/2026-10-30-day1-osint-pipeline-design.md` | перенесён в спицу | [education/technograd-reputation-engineering/handouts/osint-pipeline-design.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/handouts/osint-pipeline-design.md) |
| `research/reputation-technologies/2026-10-30-day2-lecturer-script.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-02/lecturer-script.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-02/lecturer-script.md) |
| `research/reputation-technologies/2026-10-30-day2-presentation-gamma.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-02/presentation.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-02/presentation.md) |
| `research/reputation-technologies/2026-10-30-day2-presentation.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/2026-10-30-day2-presentation.md) |
| `research/reputation-technologies/2026-10-30-day2-rationale-and-method.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-02/rationale-and-method.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-02/rationale-and-method.md) |
| `research/reputation-technologies/2026-11-01-course-quotes-days-1-4-alce.md` | перенесён в спицу | [education/technograd-reputation-engineering/handouts/course-quotes-days-1-4-alce.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/handouts/course-quotes-days-1-4-alce.md) |
| `research/reputation-technologies/2026-11-02-day3-lecturer-script.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-03/lecturer-script.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-03/lecturer-script.md) |
| `research/reputation-technologies/2026-11-02-day3-presentation-gamma.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-03/presentation.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-03/presentation.md) |
| `research/reputation-technologies/2026-11-02-day3-presentation.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/2026-11-02-day3-presentation.md) |
| `research/reputation-technologies/2026-11-02-day3-rationale-and-method.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-03/rationale-and-method.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-03/rationale-and-method.md) |
| `research/reputation-technologies/2026-11-02-day3-slide-standard-and-gate.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-03/slide-standard-and-gate.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-03/slide-standard-and-gate.md) |
| `research/reputation-technologies/2026-11-03-day4-ai-interpretation-analysis.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/2026-11-03-day4-ai-interpretation-analysis.md) |
| `research/reputation-technologies/2026-11-03-day4-crisis-mitigation-rfc.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/2026-11-03-day4-crisis-mitigation-rfc.md) |
| `research/reputation-technologies/2026-11-03-day4-image-prompts-v5-couturier-constructor.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-04/image-prompts.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-04/image-prompts.md) |
| `research/reputation-technologies/2026-11-03-day4-lecturer-script-v3.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/2026-11-03-day4-lecturer-script-v3.md) |
| `research/reputation-technologies/2026-11-03-day4-lecturer-script-v5.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-04/lecturer-script.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-04/lecturer-script.md) |
| `research/reputation-technologies/2026-11-03-day4-lecturer-script.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/2026-11-03-day4-presentation-gamma-v2.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/2026-11-03-day4-presentation-gamma-v3.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/2026-11-03-day4-presentation-gamma-v4.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/2026-11-03-day4-presentation-gamma-v4.md) |
| `research/reputation-technologies/2026-11-03-day4-presentation-gamma-v5.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-04/presentation.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-04/presentation.md) |
| `research/reputation-technologies/2026-11-03-day4-presentation-gamma.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/2026-11-03-day4-presentation-gamma.md) |
| `research/reputation-technologies/2026-11-03-day4-rationale-and-method-v2.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/2026-11-03-day4-rationale-and-method.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/2026-11-03-rfc-presentation-update-v5.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/2026-11-03-rfc-presentation-update-v5.md) |
| `research/reputation-technologies/exp/day1-methodology-659/README.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day1-methodology-659/README.md) |
| `research/reputation-technologies/exp/day1-methodology-659/absolutize-links.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day1-methodology-659/absolutize-links.py) |
| `research/reputation-technologies/exp/day1-methodology-659/scan-contradictions.sh` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day1-methodology-659/scan-contradictions.sh) |
| `research/reputation-technologies/exp/day1-osint-709/2026-10-30-ten-company-example.md` | перенесён в спицу | [education/technograd-reputation-engineering/handouts/ten-company-example.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/handouts/ten-company-example.md) |
| `research/reputation-technologies/exp/day1-osint-709/README.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day1-osint-709/README.md) |
| `research/reputation-technologies/exp/day1-osint-709/after.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day1-osint-709/after.log) |
| `research/reputation-technologies/exp/day1-osint-709/before.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day1-osint-709/before.log) |
| `research/reputation-technologies/exp/day1-osint-709/check-graph-709.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day1-osint-709/check-graph-709.py) |
| `research/reputation-technologies/exp/day1-osint-709/check-pipeline-709.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day1-osint-709/check-pipeline-709.py) |
| `research/reputation-technologies/exp/day1-osint-709/feedback-before.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day1-osint-709/feedback-before.log) |
| `research/reputation-technologies/exp/day1-rebuild-675/README.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day1-rebuild-675/check-day1.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day1-rebuild-675/issue-675-after.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day1-rebuild-675/issue-675-before.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day1-rebuild-677/README.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day1-rebuild-677/README.md) |
| `research/reputation-technologies/exp/day1-rebuild-677/check-day1-677.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day1-rebuild-677/check-day1-677.py) |
| `research/reputation-technologies/exp/day1-rebuild-677/issue-677-after.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day1-rebuild-677/issue-677-after.log) |
| `research/reputation-technologies/exp/day1-rebuild-677/issue-677-before.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day1-rebuild-677/issue-677-before.log) |
| `research/reputation-technologies/exp/day2-gamma-679/README.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day2-gamma-679/check-day2-679.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day2-gamma-679/issue-679-after.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day2-gamma-679/issue-679-before.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day2-rebuild-673/README.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day2-rebuild-673/check-day2.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day2-rebuild-673/issue-673-after.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day2-rebuild-673/issue-673-before.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day3-filter-663/README.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day3-filter-663/check-day3.sh` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day3-filter-663/test-check-day3.sh` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day3-gamma-681/README.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day3-gamma-681/README.md) |
| `research/reputation-technologies/exp/day3-gamma-681/check-day3-681.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day3-gamma-681/check-day3-681.py) |
| `research/reputation-technologies/exp/day3-gamma-681/day3_links_681.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day3-gamma-681/day3_links_681.py) |
| `research/reputation-technologies/exp/day3-gamma-681/deck_words_681.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day3-gamma-681/deck_words_681.py) |
| `research/reputation-technologies/exp/day3-gamma-681/issue-681-after.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day3-gamma-681/issue-681-after.log) |
| `research/reputation-technologies/exp/day3-gamma-681/issue-681-before.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day3-gamma-681/issue-681-before.log) |
| `research/reputation-technologies/exp/day3-gamma-681/mutation_reasons_681.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day3-gamma-681/mutation_reasons_681.py) |
| `research/reputation-technologies/exp/day3-rationale-683/README.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day3-rationale-683/check-day3-rationale-683.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day3-rationale-683/issue-683-after.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day3-rationale-683/issue-683-before.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-correction-689/README.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-correction-689/build_deck_v2_689.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-correction-689/check-day4-689.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-correction-689/findings-days-1-4-689.json` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-correction-689/issue-689-after.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-correction-689/issue-689-before.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-correction-689/mutation_reasons_689.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-correction-689/verify_deck_quotes_689.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-gamma-687/README.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-gamma-687/check-day4-687.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-gamma-687/issue-687-after.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-gamma-687/issue-687-before.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-gamma-687/mutation_reasons_687.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-image-prompts-v5-699/README.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-image-prompts-v5-699/check-day4-image-prompts-699.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-image-prompts-v5-699/issue-699-after.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-image-prompts-v5-699/issue-699-before.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-image-prompts-v5-699/mutation_reasons_699.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-rationale-685/README.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-rationale-685/check-day4-685.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-rationale-685/issue-685-after.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-rationale-685/issue-685-before.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-rationale-685/mutation_reasons_685.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-v3-691/README.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-v3-691/check-day4-691.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-v3-691/issue-691-after.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-v3-691/issue-691-before.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-v3-691/mutation_reasons_691.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-v4-693/README.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-v4-693/check-day4-693.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-v4-693/issue-693-after.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-v4-693/issue-693-before.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-v4-693/mutation_reasons_693.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/day4-v5-697/README.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day4-v5-697/README.md) |
| `research/reputation-technologies/exp/day4-v5-697/check-day4-697.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day4-v5-697/check-day4-697.py) |
| `research/reputation-technologies/exp/day4-v5-697/issue-697-after.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day4-v5-697/issue-697-after.log) |
| `research/reputation-technologies/exp/day4-v5-697/issue-697-before.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day4-v5-697/issue-697-before.log) |
| `research/reputation-technologies/exp/day4-v5-697/mutation_reasons_697.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/day4-v5-697/mutation_reasons_697.py) |
| `research/reputation-technologies/exp/gra-research-program-657/README.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/gra-research-program-657/README.md) |
| `research/reputation-technologies/exp/gra-research-program-657/check-gra-anchors.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/gra-research-program-657/check-gra-anchors.py) |
| `research/reputation-technologies/exp/handout-registry-700/README.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/handout-registry-700/check-handout-700.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/handout-registry-700/issue-700-after.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/handout-registry-700/issue-700-before.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/handout-registry-700/mutation_reasons_700.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/presentation-ux-665/README.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/presentation-ux-665/after.png` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/presentation-ux-665/before.png` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/presentation-ux-665/check-presentation-ux.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/presentation-ux-665/render-preview.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/quotes-711/README.md` | перенесён в спицу | [education/technograd-reputation-engineering/handouts/course-quotes-provenance/README.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/handouts/course-quotes-provenance/README.md) |
| `research/reputation-technologies/exp/quotes-711/build_quotes_711.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/quotes-711/build_quotes_711.py) |
| `research/reputation-technologies/exp/quotes-711/check-quotes-711.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/quotes-711/check-quotes-711.py) |
| `research/reputation-technologies/exp/quotes-711/expand_titles_711.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/quotes-711/expand_titles_711.py) |
| `research/reputation-technologies/exp/quotes-711/extract_650.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/quotes-711/extract_650.py) |
| `research/reputation-technologies/exp/quotes-711/interpretations-711.json` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/quotes-711/interpretations-711.json) |
| `research/reputation-technologies/exp/quotes-711/inventory-650.json` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/quotes-711/inventory-650.json) |
| `research/reputation-technologies/exp/quotes-711/issue-711-after.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/quotes-711/issue-711-after.log) |
| `research/reputation-technologies/exp/quotes-711/issue-711-before.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/quotes-711/issue-711-before.log) |
| `research/reputation-technologies/exp/quotes-711/mutation_reasons_711.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/quotes-711/mutation_reasons_711.py) |
| `research/reputation-technologies/exp/quotes-711/names-evidence-711.json` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/quotes-711/names-evidence-711.json) |
| `research/reputation-technologies/exp/quotes-711/quotes_711_data.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/quotes-711/quotes_711_data.py) |
| `research/reputation-technologies/exp/quotes-711/source-excerpts-711.txt` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/quotes-711/source-excerpts-711.txt) |
| `research/reputation-technologies/exp/rfc-days-logic-667/README.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/rfc-days-logic-667/README.md) |
| `research/reputation-technologies/exp/rfc-days-logic-667/check-rfc-logic.py` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/rfc-days-logic-667/check-rfc-logic.py) |
| `research/reputation-technologies/exp/rfc-days-logic-667/issue-669-after.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/rfc-days-logic-667/issue-669-after.log) |
| `research/reputation-technologies/exp/rfc-days-logic-667/issue-669-before.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/rfc-days-logic-667/issue-669-before.log) |
| `research/reputation-technologies/exp/rfc-days-logic-667/issue-671-after.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/rfc-days-logic-667/issue-671-after.log) |
| `research/reputation-technologies/exp/rfc-days-logic-667/issue-671-before.log` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/exp/rfc-days-logic-667/issue-671-before.log) |
| `research/reputation-technologies/exp/rfc-v5-695/README.md` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/rfc-v5-695/build-rfc-695.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/rfc-v5-695/check-rfc-695.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/rfc-v5-695/issue-695-after.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/rfc-v5-695/issue-695-before.log` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/exp/rfc-v5-695/mutation_reasons_695.py` | удалён по мандату (Q-2) | удалён; последняя версия — `48ebe52` |
| `research/reputation-technologies/gra-research-program/00-introduction.md` | перенесён в спицу | [methodology/research-program/00-introduction.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/methodology/research-program/00-introduction.md) |
| `research/reputation-technologies/gra-research-program/10-theory.md` | перенесён в спицу | [methodology/research-program/10-theory.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/methodology/research-program/10-theory.md) |
| `research/reputation-technologies/gra-research-program/20-taxonomy.md` | перенесён в спицу | [methodology/research-program/20-taxonomy.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/methodology/research-program/20-taxonomy.md) |
| `research/reputation-technologies/gra-research-program/30-decision-framework.md` | перенесён в спицу | [methodology/research-program/30-decision-framework.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/methodology/research-program/30-decision-framework.md) |
| `research/reputation-technologies/gra-research-program/40-practice-and-cases.md` | перенесён в спицу | [methodology/research-program/40-practice-and-cases.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/methodology/research-program/40-practice-and-cases.md) |
| `research/reputation-technologies/gra-research-program/50-open-research.md` | перенесён в спицу | [methodology/research-program/50-open-research.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/methodology/research-program/50-open-research.md) |
| `research/reputation-technologies/gra-research-program/presentation-rfc/2026-10-12-rfc-presentation-ux-days-1-3.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/gra-research-program/presentation-rfc/2026-10-12-rfc-presentation-ux-days-1-3.md) |
| `research/reputation-technologies/gra-research-program/presentation-rfc/README.md` | архив: тег | [тег](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/archive/reputation-technologies-2026-11/research/reputation-technologies/gra-research-program/presentation-rfc/README.md) |
| `research/reputation-technologies/image-technologies/00-introduction.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-04/resources/image-technologies/00-introduction.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-04/resources/image-technologies/00-introduction.md) |
| `research/reputation-technologies/image-technologies/10-theory.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-04/resources/image-technologies/10-theory.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-04/resources/image-technologies/10-theory.md) |
| `research/reputation-technologies/image-technologies/20-taxonomy.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-04/resources/image-technologies/20-taxonomy.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-04/resources/image-technologies/20-taxonomy.md) |
| `research/reputation-technologies/image-technologies/30-decision-framework.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-04/resources/image-technologies/30-decision-framework.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-04/resources/image-technologies/30-decision-framework.md) |
| `research/reputation-technologies/image-technologies/40-practice-and-cases.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-04/resources/image-technologies/40-practice-and-cases.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-04/resources/image-technologies/40-practice-and-cases.md) |
| `research/reputation-technologies/image-technologies/50-open-research.md` | перенесён в спицу | [education/technograd-reputation-engineering/day-04/resources/image-technologies/50-open-research.md](https://github.com/G-Ivan-A/aether-orbis-gra/blob/b49acde5af86629eb781015f4338b5ec834f27c8/education/technograd-reputation-engineering/day-04/resources/image-technologies/50-open-research.md) |
