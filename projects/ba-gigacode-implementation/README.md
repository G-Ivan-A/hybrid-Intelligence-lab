---
status: draft
version: 0.1
updated: 2026-09-11
temperature: 0.1
scope: mango-only
type: research
---

# BA GigaCode Implementation — реализация БА-процессов КК Манго в GigaCode

Направление отвечает на вопрос **«как БА-процессы КК Манго исполняются в среде
GigaCode»**: какая мета-модель описывает работу, какими процессами и операциями
она разложена и в какой форме поставляется агенту.

Это **дом проектных артефактов**, а не общая рамка. Все три модуля несут
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

Модули лежат прямо в корне направления, а не в подкаталоге из списка стандарта:
это **не** проектная документация, стандарт или база знаний, а исследовательские
модули [Reference Research Pattern](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/rfc/2026-07-17-rfc-reference-research-pattern.md)
(шесть файлов `00…50`), у которых своя форма. Отклонение объявлено, а не скрыто.

## Модули

- [`ba-meta-model/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/00-introduction.md)
  — каноническая мета-модель БА (issue
  [#563](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/563),
  версия 0.2 — [#571](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571)):
  одиннадцать канонических сущностей, закон производства `MM-1`…`MM-4`,
  четыре канонические таксономии, реестр депрекации режимов запуска
  `DP-1`…`DP-5`, правила работы с наследием `LG-1`…`LG-6`, контракт
  `SKILL.md` (`SK-0`…`SK-10`), маршрутный лист, Golden Set и план вертикального
  MVP-среза с метриками `M-1`…`M-5`.
- [`ba-process-taxonomy/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/00-introduction.md)
  — таксономия процессов на индустриальном базисе: `L0` (шесть областей знаний
  BABOK Guide v3) → `L1` (шесть семейств работ) → `L2` (десять процессов
  `P-01`…`P-10`) → `L3` (33 навыка-подпроцесса), где `L0`/`L1` наследуются, а
  `L2`/`L3` объявлены дельтой с обоснованием каждого отклонения.
- [`ba-operation-taxonomy/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-operation-taxonomy/00-introduction.md)
  — таксономия операций той же пересборки: 31 операция в пяти классах
  (`extract`, `transform`, `generate`, `check`, `assess`) и правила атомарности
  `OA-1`…`OA-6`.

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
