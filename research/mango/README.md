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
| [classification.md](classification.md) | Рабочая международная и российская классификация IT/Telecom SaaS-продуктов MANGO OFFICE. |
| [classification-tz.md](classification-tz.md) | Проверка классификатора на корпусе из 30 ТЗ и рекомендации по дополнениям. |
| [requirements-flow.md](requirements-flow.md) | Flow требований для AI-анализа тендерных ТЗ MANGO OFFICE. |
| [requirements-lifecycle-uncertainty-2026-05.md](requirements-lifecycle-uncertainty-2026-05.md) | Жизненный цикл требования на доработку: обработка неопределенности, декомпозиция и сравнение с международной практикой. |
| [rag-mapping-roadmap-2026-05.md](rag-mapping-roadmap-2026-05.md) | Маппинг продуктов/фич как RAG-навигатор, roadmap автоматизации БА и карта применения PlantUML-диаграмм. |
| [capability-decomposition-2026-05.md](capability-decomposition-2026-05.md) | Справочник атомарных функций пилотных доменов (`voice-ucaas`, `contact-center`, `digital-channels`): параметры, международные источники, примеры ТЗ и связь с НФТ-классами. |
| [requirements-engineering-ai-era-2026.md](requirements-engineering-ai-era-2026.md) | RFC для спок-проекта `mango_ba_prompts`: синхронизация независимо извлечённой системы требований Вигерса с ADR-003..010 (карта сравнения, каталог «велосипедов» 🔴/🟡/🟢), исправленная классификация AI-эры (Prompt = интерфейс к Tool, инжиниринг промптов = подпроцесс, Prompt specification как артефакт), процессы/подпроцессы разработки AI-агента (Фаза 2) и предложение синхронизации С1–С5 под человеческим решением. |
| [ai-classifications-formalization-2026-06.md](ai-classifications-formalization-2026-06.md) | Формализация 4 новых AI-подпроцессов (инжиниринг промптов, RAG, оркестрация агентов, тестирование AI), эволюция операций в роадмапе Mango (4 фазы) и подготовка синхронизации с `mango_ba_prompts` (С1/С2/С3). |
| [token-optimization-proposal-2026-06.md](token-optimization-proposal-2026-06.md) | RFC для спок-проекта `mango_ba_prompts` (issue #255, Creative + Research): независимые предложения по оптимизации потребления токенов. Аудит сценариев A/B/D/F и топ-5 точек кипения (handover ~6000 токенов перерасхода, кластер `ba-ontology` ~63 KB в 3 местах, bootstrap-набор ~46k), сравнение подходов к разделению Full/Executable (файлы/слои/ссылки/динамическая загрузка/frontmatter-разметка), стратегии устранения дублирования с сохранением истории (SSOT через `artifact-map`, намеренный split ADR↔Standard), контентные/процессные/технические меры, метрики успеха и план сбора baseline. Совместимо с PR #254. Только RFC — файлы спока не меняются, решение за человеком. |
| [repository-structure-vision-2026-06.md](repository-structure-vision-2026-06.md) | RFC для спок-проекта `mango_ba_prompts` (issue #253, Creative): независимое видение оптимальной структуры репозитория(ев). Аудит реального репозитория (коллизия `ba-process`/`ba-processes`, смешение Definition/Run, свалка в `governance/`, непоследовательная нумерация ADR), синтез 4 командных видений (C/Q/G/founder) с таблицей сравнения, варианты A/B/C и независимое решение — Вариант B фазово (Public `mango_ba_framework` + Private `mango_ba_operations` + Yandex Object Storage). Деревья каталогов, три уровня ИБ (Public/Private/Confidential), единый контракт записи прогонов (`runs/RUN-XXXX/` + `metadata.yaml`) для 3 сценариев, один мост к Хабу, переиспользование портала open-ai.ru и фиксация токеновой инфляции без оптимизации. Решение за человеком. |

## Воспроизводимость

Исторические HTML-exports публикуются через MkDocs/GitHub Pages и не хранятся
в репозитории. Исторические scripts для корпуса ТЗ удалены в cleanup issue #49 вместе с
`experiments-old/`. Метод извлечения и ограничения корпуса сохранены в
[classification-tz.md](classification-tz.md). Если эксперимент потребуется
восстановить, новый воспроизводимый контур должен жить в
`research/mango/exp-tz-corpus/` по
[standards/research-profile.md](../../standards/research-profile.md).
