---
status: canonical
version: 1.0
updated: 2026-05-26
temperature: 0.1
ai-generated: false
source: frameworks/README-old.md
---

# Frameworks

Каталог для методологий и фреймворков, которые могут использоваться
международным сообществом, образовательными программами и проектными командами.

## Правило создания нового фреймворка

Новый фреймворк создается только если:

| Условие | Требование |
| --- | --- |
| Existing frameworks insufficient | Есть сравнительная таблица существующих подходов. |
| Gap formally identified | Ясно, какой разрыв не покрывается внешними фреймворками. |
| Extension impossible or weak | Объяснено, почему нельзя просто сослаться на внешний фреймворк. |
| Hybrid-team relevance | Показано, зачем фреймворк нужен human + AI командам. |
| Reusable artifact | Есть шаблон, методика или пример, который можно переиспользовать. |

## Рекомендуемая структура будущего фреймворка

```text
frameworks/<framework-slug>/
  README.ru.md
  README.en.md
  comparison.md
  method.md
  examples/
```

Для черновика допустим один `README.ru.md`, если issue явно ограничивает
результат русским языком. Для публичного framework итоговая версия должна иметь
ru/en пару или зафиксированное исключение.

Правило Anti-Inflation и критерий сравнения с существующими подходами
зафиксированы в [governance/repo-model.md](../governance/repo-model.md).
