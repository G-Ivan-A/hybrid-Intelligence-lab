---
status: canonical
version: 1.0
updated: 2026-09-19
temperature: 0.1
---

# Дельты сред и model adapters

Среда выполнения определяется только `.hub-profile.json`. `environment` задаёт
primary environment, `secondary_environments` — дополнительные; допустимые
значения — `local`, `gigacode`, `serverless`. Cursor и Copilot — model/tool
adapters, а не значения этой оси. Наличие случайного IDE-файла не доказывает,
что adapter поддерживается проектом.

| Среда или adapter | Условие включения | Допустимая дельта | Нельзя включать |
| --- | --- | --- | --- |
| GigaCode | `gigacode` объявлен primary или secondary environment. | Сгенерированный adapter/import на `/AGENTS.md`; команды проверки, реально доступные в GigaCode environment; абсолютные Hub links. | GigaCode-specific workflow, если профиль содержит только `local`; копию general rules. |
| Cursor adapter | В bootstrap/task проекта явно выбран Cursor adapter и репозиторий реально его поддерживает. | Generated `.cursor/rules/` pointer на `/AGENTS.md`, защищённый check-режимом. | Ручную копию правил или включение только потому, что contributor использует Cursor. |
| Copilot adapter | В bootstrap/task проекта явно выбран Copilot adapter и репозиторий реально его поддерживает. | Generated `.github/copilot-instructions.md` pointer на `/AGENTS.md`, защищённый check-режимом. | Самостоятельный набор agent rules в инструкции Copilot. |

Cursor и Copilot могут быть механизмами чтения, но не становятся значениями
профиля. Их adapters создаются только по явному scope bootstrap/task и остаются
тонкими указателями. Неизвестное значение profile environment — ошибка, а не
повод выбрать ближайшую среду.

## Пример adapter

Adapter содержит только generated marker, указатель на `/AGENTS.md` и при
необходимости нативную import-директиву инструмента. Нормативная фраза вроде
«всегда запускай тест X» принадлежит `AGENTS.md` или routed local contract, но
не adapter.

## Проверка изоляции

Для каждого adapter проверить:

1. runtime environment объявлен и разрешён, а model adapter входит в явный scope;
2. adapter не содержит копий `<hard_rules>`/`<forbidden>`;
3. удаление или изменение generated marker обнаруживает check-режим;
4. проект без этой среды не получает её файлы или правила;
5. отключение adapter не меняет canonical content `/AGENTS.md`.
