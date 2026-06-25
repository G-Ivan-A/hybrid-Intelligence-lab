---
status: canonical
version: 1.0
updated: 2026-05-26
temperature: 0.1
ai-generated: false
source: research/mango/README-old.md
---

# Research: MANGO OFFICE

Исследовательские материалы по классификации продуктов, требований,
документационной стратегии и flow анализа тендерных ТЗ MANGO OFFICE.

## Документы

| Документ | Назначение |
| --- | --- |
| [2026-05-classification.md](2026-05-classification.md) | Рабочая международная и российская классификация IT/Telecom SaaS-продуктов MANGO OFFICE. |
| [2026-05-classification-tz.md](2026-05-classification-tz.md) | Проверка классификатора на корпусе из 30 ТЗ и рекомендации по дополнениям. |
| [2026-05-requirements-flow.md](2026-05-requirements-flow.md) | Flow требований для AI-анализа тендерных ТЗ MANGO OFFICE. |
| [2026-05-requirements-lifecycle-uncertainty.md](2026-05-requirements-lifecycle-uncertainty.md) | Жизненный цикл требования на доработку: обработка неопределенности, декомпозиция и сравнение с международной практикой. |
| [2026-05-rag-mapping-roadmap.md](2026-05-rag-mapping-roadmap.md) | Маппинг продуктов/фич как RAG-навигатор, roadmap автоматизации БА и карта применения PlantUML-диаграмм. |
| [2026-05-capability-decomposition.md](2026-05-capability-decomposition.md) | Справочник атомарных функций пилотных доменов (`voice-ucaas`, `contact-center`, `digital-channels`): параметры, международные источники, примеры ТЗ и связь с НФТ-классами. |
| [2026-requirements-engineering-ai-era.md](2026-requirements-engineering-ai-era.md) | RFC для спок-проекта `mango_ba_prompts`: синхронизация независимо извлечённой системы требований Вигерса с ADR-003..010 (карта сравнения, каталог «велосипедов» 🔴/🟡/🟢), исправленная классификация AI-эры (Prompt = интерфейс к Tool, инжиниринг промптов = подпроцесс, Prompt specification как артефакт), процессы/подпроцессы разработки AI-агента (Фаза 2) и предложение синхронизации С1–С5 под человеческим решением. |
| [2026-06-ai-classifications-formalization.md](2026-06-ai-classifications-formalization.md) | Формализация 4 новых AI-подпроцессов (инжиниринг промптов, RAG, оркестрация агентов, тестирование AI), эволюция операций в роадмапе Mango (4 фазы) и подготовка синхронизации с `mango_ba_prompts` (С1/С2/С3). |
| [2026-06-token-optimization-proposal.md](2026-06-token-optimization-proposal.md) | RFC для спок-проекта `mango_ba_prompts` (issue #255, Creative + Research): независимые предложения по оптимизации потребления токенов. Аудит сценариев A/B/D/F и топ-5 точек кипения (handover ~6000 токенов перерасхода, кластер `ba-ontology` ~63 KB в 3 местах, bootstrap-набор ~46k), сравнение подходов к разделению Full/Executable (файлы/слои/ссылки/динамическая загрузка/frontmatter-разметка), стратегии устранения дублирования с сохранением истории (SSOT через `artifact-map`, намеренный split ADR↔Standard), контентные/процессные/технические меры, метрики успеха и план сбора baseline. Совместимо с PR #254. Только RFC — файлы спока не меняются, решение за человеком. |
| [2026-06-repository-structure-vision.md](2026-06-repository-structure-vision.md) | RFC для спок-проекта `mango_ba_prompts` (issue #253, Creative): независимое видение оптимальной структуры репозитория(ев). Аудит реального репозитория (коллизия `ba-process`/`ba-processes`, смешение Definition/Run, свалка в `governance/`, непоследовательная нумерация ADR), синтез 4 командных видений (C/Q/G/founder) с таблицей сравнения, варианты A/B/C и независимое решение — Вариант B фазово (Public `mango_ba_framework` + Private `mango_ba_operations` + Yandex Object Storage). Деревья каталогов, три уровня ИБ (Public/Private/Confidential), единый контракт записи прогонов (`runs/RUN-XXXX/` + `metadata.yaml`) для 3 сценариев, один мост к Хабу, переиспользование портала open-ai.ru и фиксация токеновой инфляции без оптимизации. Решение за человеком. |

## Воспроизводимость

Исторические HTML-exports публикуются через MkDocs/GitHub Pages и не хранятся
в репозитории. Исторические scripts для корпуса ТЗ удалены в cleanup issue #49 вместе с
`experiments-old/`. Метод извлечения и ограничения корпуса сохранены в
[2026-05-classification-tz.md](2026-05-classification-tz.md). Если эксперимент потребуется
восстановить, новый воспроизводимый контур должен жить в
`research/mango/exp-tz-corpus/` по
[standards/research-profile.md](../../standards/research-profile.md).
