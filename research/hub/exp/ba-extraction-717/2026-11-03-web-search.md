---
status: draft
version: 0.1
updated: 2026-11-03
temperature: 0.1
type: experiment
---

# Веб-поиск имён-кандидатов (issue #717)

Поиск выполнен 2026-11-03 общим веб-поиском (режим standard) по точной фразе.
Таблица реестров и хостингов — в `name-availability.log`; здесь только то, что
API хостингов не покрывают: страницы, блоги, курсы, статьи.

| Запрос | Точные совпадения | Ближайшие соседи по смыслу |
| --- | --- | --- |
| `"ba-ai-process"` | нет | Общая фраза «AI-процесс бизнес-аналитика»: курсы и блоги про AI в работе БА (Learning Tree, QA, Techademy, freeacademy.ai, BA Copilot) |
| `"ba-ai-metamodel"` / `"BA AI metamodel"` | нет | «Business Analysis Metamodel» как понятие (пост LinkedIn), Business Architecture Copilot (ER25, CEUR-WS Vol-4099) |
| `"universal-ba-ai-framework"` / `"gra-ba-ai-framework"` | нет | «Universal AI …» — другие предметные области (этика, управление ИИ); **OpenBA** (`github.com/FraCox85/OpenBA`) — «Business Analyst-first spec framework for AI coding assistants» |

## Выводы

1. Ни одно имя не занято дословно ни в вебе, ни на хостингах из
   `name-availability.log`: критерий «нет дублей» выполняют все кандидаты.
2. Различие — в **различимости**. `ba-ai-process` и `ba-ai-framework` — общие
   фразы: поиск GitHub `in:name` даёт 282 и 265 репозиториев с теми же
   токенами, веб-поиск — поток материалов про «AI в процессе БА».
   `ba-ai-metamodel`, `universal-ba-ai-framework` и `gra-ba-ai-framework` дают 0.
3. OpenBA — ближайший по назначению открытый проект (спецификационный
   фреймворк БА для AI-ассистентов). Имена с `framework` сближают проект с ним
   по названию; `metamodel` называет то, чем проект отличается, — инвариантное
   ядро метамодели.

## Источники

- https://www.learningtree.com/blog/ai-driven-business-analyst-popit-model/
- https://www.qa.com/course-catalogue/courses/ai-for-business-analysts-qaaiba/
- https://bacopilot.featurebase.app/changelog/ai-process-mapping-tools-benchmark
- https://nz.linkedin.com/in/chris-greenham
- https://ceur-ws.org/Vol-4099/ER25_PET_Oaj.pdf
- https://github.com/FraCox85/OpenBA
