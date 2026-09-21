---
status: draft
version: 0.4
updated: 2026-09-21
temperature: 0.1
scope: mango-only
type: research
---

# BA GigaCode Implementation — реализация БА-процессов КК Манго в GigaCode

Направление отвечает на вопрос **«как БА-процессы КК Манго исполняются в среде
GigaCode»**: какая мета-модель описывает работу, какими процессами и операциями
она разложена и в какой форме поставляется агенту.

Это **дом проектных артефактов**, а не общая рамка. Все четыре модуля несут
`scope: mango-only`: переносимость — проверяемая гипотеза (задача `B-158`), а не
объявленное свойство. Переносимая часть исследования остаётся в
[`research/ba-requirements/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/README.md).

## Почему модули живут здесь

Правило размещения задано
[`standards/project-structure-inheritance.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/standards/project-structure-inheritance.md):
артефакт конкретного направления живёт в `projects/<направление>/`, а общий
каталог `research/` остаётся за переносимой рамкой. Расхождение признано в
[PR #572](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/572),
подтверждено владельцем и выполнено задачей `B-155`
([#573](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/573)).

Каноническая модель использует форму
[Reference Research Pattern](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/rfc/2026-07-17-rfc-reference-research-pattern.md),
а инструкции, тесты и пакет имеют форму своей операции. Таксономии процессов и
операций вложены в `ba-meta-model/`: это части одной канонической модели, а не
самостоятельные верхнеуровневые модули.

## Четыре операционных модуля

- [`ba-meta-model/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/00-introduction.md)
  — каноническая мета-модель БА (issue
  [#563](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/563),
  версия 0.2 — [#571](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571)):
  одиннадцать канонических сущностей, закон производства `MM-1`…`MM-4`,
  четыре канонические таксономии, реестр депрекации режимов запуска
  `DP-1`…`DP-5`, правила работы с наследием `LG-1`…`LG-6`, контракт
  `SKILL.md` (`SK-0`…`SK-10`), маршрутный лист, Golden Set и план вертикального
  MVP-среза с метриками `M-1`…`M-5`. Вложенные
  [`process-taxonomy/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/process-taxonomy/00-introduction.md)
  и [`operation-taxonomy/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/operation-taxonomy/00-introduction.md)
  задают соответственно 33 навыка-подпроцесса и 31 атомарную операцию.
- [`meta-model-guides/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/meta-model-guides/README.md)
  — инструкции человеку: подготовка чистой директории, локальной KB,
  Confluence MCP, запуск/возобновление task и изолированный debug.
- [`execution-package-tests/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/execution-package-tests/README.md)
  — mock-fixtures, assertions и детерминированная эмуляция графа без LLM и MCP.
- [`execution-package-gigacode-cli/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/execution-package-gigacode-cli/README.md)
  — копируемый пакет с `.gigacode/skills/`, явным dispatcher, debug-механизмом,
  контрактами, графом, Golden Set и машинным гейтом `G-mach`.

Пакет — артефакт компиляции, а не новый RRP-модуль. Состав скопированного,
преобразованного и отброшенного объявлен в
[манифесте](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/execution-package-gigacode-cli/compilation-manifest.yaml).
Его `docs/kb/.gitkeep` и `meta-model/.gitkeep` обозначают copy-time входы; пакет
не ссылается в Хаб во время прогона.

## Решение о GigaCode CLI

Предложение и доказательства среды сохранены в
[`docs/rfc/2026-09-mango-ba-ai-runtime-cli-deployment.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/docs/rfc/2026-09-mango-ba-ai-runtime-cli-deployment.md).
Issue [#593](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/593)
реализует проверяемую часть внутри Хаба и не изменяет внешний
`mango-ba-ai-runtime-cli`.

## Доказательная база

Датированные снимки и воспроизводимые эксперименты **не переносятся**: они
остаются в [`research/ba-requirements/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/README.md)
как свидетельства о состоянии корпуса на дату замера. Модули ссылаются на них,
а не наоборот:

- [`2026-09-08-meta-model-inputs-facts.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-08-meta-model-inputs-facts.md);
- [`2026-09-09-legacy-normative-influence-facts.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-09-legacy-normative-influence-facts.md);
- [`2026-09-10-process-taxonomy-defects-facts.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-10-process-taxonomy-defects-facts.md);
- [`2026-09-10-gigacode-environment-facts.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-10-gigacode-environment-facts.md);
- [`2026-09-10-skill-granularity-format-facts.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-10-skill-granularity-format-facts.md).

## Решения

- [ADR-013](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-013-run-modes-deprecation.md)
  — депрекация режимов запуска как идентичности способности;
- [ADR-014](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-014-legacy-evidence-not-baseline.md)
  — наследие является свидетельством, а не базисом новой нормы;
- [ADR-015](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-015-process-operation-taxonomy-rebuild.md)
  — пересборка таксономии процессов и операций от индустриального базиса;
- [ADR-016](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-016-skill-form-and-contract-format.md)
  — навык как форма поставки, формат контракта как вычисляемое свойство.

## Политика ссылок

Ссылки **абсолютные** (полные URL), как и во всём направлении `ba-requirements`.
Единственное исключение — обязательные внутримодульные относительные ссылки в
`40-practice-and-cases.md`, которых требует машинная проверка правила P2
([`tools/validate-rrp-links.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/validate-rrp-links.sh)).
