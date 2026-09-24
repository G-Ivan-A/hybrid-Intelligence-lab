---
name: product-attribution
description: >-
  Используй первым для каждой задачи: сопоставь предмет задачи с полной
  цепочкой портфеля MANGO и запроси явное подтверждение бизнес-аналитика.
packs: P-01/SK-product-attribution
interaction: human-checkpointed
inputs: [A-IN]
outputs: [A-IN]
contracts: [C-IN]
gates: [G-self, G-mach, G-human]
compiled_from: { package: execution-package-gigacode-cli, route: RG-BCREQ-v1 }
derived_from: [taxonomy/products.yaml, taxonomy/mango-products.yaml, taxonomy/telecom-products.yaml, contracts/c-in.schema.json]
compiled_at: 2026-09-23
status: draft
version: 1.0
updated: 2026-09-23
temperature: 0.1
---

# Навык: продуктовая атрибуция

## Когда применять

Применяй в `n0` до любого основного узла генерации. Входной `A-IN` может иметь
`product_attribution.status: pending`; выход — тот же `A-IN` с подтверждённым
реестром продуктов и неизменяемым digest привязки.

## Предусловия

1. Вход объявлен как `A-IN` и содержит материал задачи с разрешимым источником.
2. Доступны закрытые `taxonomy/mango-products.yaml` и `taxonomy/products.yaml`.
3. Бизнес-аналитик доступен для решения `G-human`; агент не подтверждает свою
   гипотезу сам и не выводит подтверждение из текста задачи.

## Шаги

0. Classify `work_type` from the goal, input, and requested outcome. Use
   `mango` as primary axis for MANGO change or KB search and `industry` for
   industry practice or external-spec evaluation. For an external spec,
   hand off to `P-08`; it does not create a BCREQ. Retain all matched,
   unmatched, and uncertain requirement mappings. Do not apply an 80% template
   threshold without a versioned template catalog and counting rule.

1. Извлеки кандидатов, но считай их гипотезой: для каждого продукта предложи
   `marker`, `domain`, `capability`, `feature`, `atomic_function`, `profile` и
   `owner`.
2. Разреши `domain/capability` и `atomic_function` в одной записи каталога
   `taxonomy/mango-products.yaml`; `feature` обязан принадлежать той же
   capability. Не смешивай уровни разных ветвей.
3. Покажи бизнес-аналитику полный реестр, названия из каталога, основание
   выбора, primary axis, routing rule, отраслевую цепочку, evidence, риск и
   альтернативы. Запроси одно из решений: `confirm`, `reject` или
   исправленный реестр.
4. Только после `confirm` установи `status: confirmed`, запиши `confirmed_by`,
   `confirmed_at`, `decision_ref` и `binding_digest`. Digest — префикс
   `sha256:` плюс SHA-256 канонического JSON массива `products` с
   `sort_keys=true` и разделителями `(',', ':')`.
5. Передай `products` и `product_attribution` без изменения в `A-CORE`,
   `A-QUEST`, `A-BCREQ` и `C-RK`. Передай также work type и routing decision.
   Любая смена привязки требует нового решения
   `G-human` и нового прогона, а не скрытой правки downstream-артефакта.

## Обязательные слоты выхода

- `products[]` — одна или несколько полных цепочек каталога MANGO.
- `product_attribution.status` — только `confirmed` для перехода к `n1`.
- `product_attribution.confirmed_by`, `confirmed_at`, `decision_ref` — след
  человеческого решения.
- `product_attribution.binding_digest` — контроль неизменности контекста.

## Самопроверка (G-self)

- Каждая цепочка разрешается в одну ветвь `mango-products.yaml` — да/нет.
- У каждой записи есть профиль, владелец и уникальный marker — да/нет.
- Решение принял бизнес-аналитик, а не агент — да/нет.
- Digest пересчитан из точного массива `products` и совпадает — да/нет.
- Ни один основной узел маршрута ещё не исполнялся — да/нет.

## Отказ

Останови маршрут в `n0`, если цепочка неполна, уровень не найден в каталоге,
уровни принадлежат разным ветвям, бизнес-аналитик отверг привязку или явного
подтверждения нет. Не выбирай ближайший домен и не переходи к `n1` по догадке.
