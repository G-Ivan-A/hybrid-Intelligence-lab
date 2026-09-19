---
status: draft
version: 1.0
updated: 2026-09-19
temperature: 0.1
---

# Проверка правил на `aether-orbis`

## Scope и метод

Проверка выполнена read-only 2026-09-19 против default branch репозитория
[`G-Ivan-A/aether-orbis`](https://github.com/G-Ivan-A/aether-orbis). Через
GitHub Contents API проверены root tree, `.hub-profile.json` и `AGENTS.md`.
Ни один файл внешнего репозитория не изменялся.

## Наблюдения

| Проверка | Результат | Следствие по правилам |
| --- | --- | --- |
| Root tree | Есть `src/`, `tests/`, product docs и CI-related files. | Структура согласуется с production spoke, но profile всё равно остаётся SSOT archetype. |
| `.hub-profile.json` | Отсутствует (HTTP 404). | Нельзя подтвердить archetype/environment; сначала нужен profile или human decision. |
| `/AGENTS.md` | Отсутствует (HTTP 404). | Нужна initial delivery, а не drift update. |
| Root governance | Одновременно есть `GOVERNANCE.md` и другие root contracts. | Перед адаптацией нужен аудит локальных SSOT; нельзя автоматически переносить текст в project rules. |
| Среда/adapters | Runtime environment не объявлен; scope model adapters отсутствует. | Нельзя включать GigaCode delta или Cursor/Copilot adapters. |

## Применение процесса

1. **Проверка:** процесс останавливает угадывание среды из содержимого дерева.
2. **Сравнение:** `AGENTS.md` отсутствует, поэтому дельта классифицируется как
   `add`; возможные локальные нормы требуют отдельной классификации.
3. **Адаптация:** после создания profile вероятной основой будет
   `templates/spoke/AGENTS.md`, но это становится решением только после
   подтверждения archetype.
4. **Валидация:** до profile нельзя проверить совпадение `<scope>`; это
   блокирует delivery, но не сбор фактов и подготовку delta report.

## Что сработало и что уточнено

Сработало разделение general/profile/environment/project layers: оно не даёт
ошибочно включить средовые правила и не выдаёт структурную эвристику за
решение. По результату в правила добавлен явный fail-closed шаг: при отсутствии
profile блокируется средовая адаптация и финальная запись, а не весь read-only
preflight.

## Ограничения

Проверка не доказывает содержательную корректность будущих project rules и не
заменяет B-113. Репозиторий проверен как пример процесса, без клонирования,
запуска его тестов или изменения внешнего состояния.
