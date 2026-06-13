---
status: draft
version: 0.1
updated: 2026-06-13
temperature: 0.1
ai-generated: true
---

# Research: External Knowledge

Направление фиксирует **систему интеграции внешних знаний** Хаба: единый реестр
внешних источников и механизм хранения извлечённых инсайтов с привязкой к
жизненному циклу знаний. Цель — превратить ad-hoc исследование внешних статей,
репозиториев и международных практик в воспроизводимый поток
`внешний источник → инсайт → валидация → практика`, общий для всей экосистемы.

`scope: repo-wide` — механизм применяется ко всему репозиторию и транслируется в
проекты экосистемы через Base Registry (Хаб) + Local Extension (проекты).

> 🧭 **Назначение в одну строку.** Внешние источники — это
> Observation/Research, а не практика: они живут в `research/`, пока не пройдут
> валидацию и не будут переведены в `practices/`/`standards/` по
> [governance/rfc/knowledge-lifecycle-proposal.md](../../governance/rfc/knowledge-lifecycle-proposal.md).

## Документы

| Документ | Назначение |
| --- | --- |
| [external-sources-registry.md](external-sources-registry.md) | Единый реестр внешних источников с минимальными метаданными (id, тип, теги, lifecycle-статус, релевантные проекты) для фильтрации и синхронизации. |
| [external-insights/](external-insights/) | Механизм хранения извлечённых инсайтов: один инсайт — один файл со статусом lifecycle и связью с источником из реестра. |

## Как это связано

- **RFC интеграции** —
  [governance/rfc/external-knowledge-integration.md](../../governance/rfc/external-knowledge-integration.md):
  модель Base Registry + Local Extension, Smart Sync, применение для 4 проектов.
- **Lifecycle знаний** —
  [governance/rfc/knowledge-lifecycle-proposal.md](../../governance/rfc/knowledge-lifecycle-proposal.md):
  правило перехода `Observation → Research → ... → Standard`.
- **Профиль исследований** —
  [standards/research-profile.md](../../standards/research-profile.md):
  именование, frontmatter и правила цитирования источников.
- **Fixed practices** — [practices/README.md](../../practices/README.md):
  место, куда инсайт попадает только после валидации.

## Политики направления

- **Anti-Inflation.** Реестр и инсайты создаются по факту ценности, без
  CI-скраперов и автоматического сбора. Метаданные — только те, что нужны для
  фильтрации и синхронизации.
- **Минимальные метаданные.** Полный набор полей описан в
  [external-sources-registry.md](external-sources-registry.md); расширять состав
  полей можно только при доказанной операционной потребности.
- **Цитирование.** Каждый инсайт ссылается на запись реестра и на первоисточник
  (см. правила цитирования в
  [standards/research-profile.md](../../standards/research-profile.md)).
- **kebab-case** для всех файлов и подкаталогов.
