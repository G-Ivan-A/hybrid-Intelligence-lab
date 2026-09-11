---
status: draft
version: 0.1
updated: 2026-09-08
temperature: 0.1
type: experiment
---

# exp: ba-meta-model-563

Evidence container для датированного замера
[`../../2026-09-08-meta-model-inputs-facts.md`](../../2026-09-08-meta-model-inputs-facts.md)
и модуля
[`projects/ba-gigacode-implementation/ba-meta-model/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/projects/ba-gigacode-implementation/ba-meta-model),
issue [#563](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/563).

> **Ссылки.** Issue #563 требует абсолютных ссылок. Относительная ссылка на
> родительский отчёт выше — вынужденное исключение: её форму машинно проверяет
> [`tools/validate-evidence-structure.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/validate-evidence-structure.sh).

## Что здесь измеряется

Issue #563 требует двух решений, которые нельзя принять на основании текста:
перевести режимы запуска `stepwise`, `oneshot`, `legacy` в статус
`deprecated` и синтезировать четыре канонические таксономии (артефакты,
операции, процессы, продукты). Оба решения зависят от одного вопроса: **что в
корпусе спицы действительно является идентичностью артефакта, а что —
исторической формой доставки**.

Машинно проверяемые утверждения родительского отчёта: число активных промптов и
их распределение по режимам, кратность дублирования способности по режимам,
расхождение скелетов режимных вариантов одной способности, доля промптов, ни
разу не упомянутых прогонами, покрытие словаря операций промптами, доля меток
`process:` вне словаря процессов, доля прогонов с объявленным продуктом.

Второй замер отвечает на вопрос комментария фаундера к PR
[#564](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/564): способен
ли исторический корпус быть базисом новой нормы. Проверяется присутствие
двенадцати нормативных конструкций мета-модели (объявленный вход и выход,
продуктовый класс, три гейта, условие отказа, контракт, след, эталон, закрытый
словарь, версия во frontmatter) в 24 промптах и 67 прогонах. Родительский
отчёт —
[`../../2026-09-09-legacy-normative-influence-facts.md`](../../2026-09-09-legacy-normative-influence-facts.md),
решение —
[ADR-014](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-014-legacy-evidence-not-baseline.md).

Содержательной интерпретации здесь нет — она в родительских отчётах, в модуле и
в [ADR-013](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/docs/adr/2026-09-adr-013-run-modes-deprecation.md).

## Состав

| Файл | Что это |
| --- | --- |
| [`measure-meta-model-inputs.py`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-meta-model-563/measure-meta-model-inputs.py) | измеритель; словари режимов, операций, процессов и доменов — именованные константы в шапке |
| [`meta-model-inputs.json`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-meta-model-563/meta-model-inputs.json) | результат: сводка + запись на каждую способность и каждый прогон |
| [`measure-meta-model-inputs.log`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-meta-model-563/measure-meta-model-inputs.log) | вывод прогона, фиксирующий опубликованные цифры и коммит корпуса |
| [`measure-legacy-normative-influence.py`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-meta-model-563/measure-legacy-normative-influence.py) | второй измеритель: присутствие двенадцати нормативных конструкций мета-модели в промптах и прогонах; маркеры — именованные константы в шапке |
| [`legacy-normative-influence.json`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-meta-model-563/legacy-normative-influence.json) | результат: сводка по конструкциям + запись на каждый промпт и каждый прогон |
| [`measure-legacy-normative-influence.log`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-meta-model-563/measure-legacy-normative-influence.log) | вывод второго прогона |

## Воспроизведение

```bash
git clone https://github.com/G-Ivan-A/mango_ba_prompts.git /tmp/mango
python3 measure-meta-model-inputs.py --mango /tmp/mango --json meta-model-inputs.json
python3 measure-legacy-normative-influence.py --mango /tmp/mango --json legacy-normative-influence.json
```

Коммит, на котором получены опубликованные цифры, записан в поле
`corpus.commit` результата: `8cbf82aa73129ec5747af07f790aaf438b0fb6e9`.
На других коммитах цифры будут другими — это ожидаемо, отчёт датирован.

## Границы измерения

- Режим определяется **суффиксом имени файла**, а не содержанием промпта.
- Скелет промпта строится только по нумерованным строкам; промпт, размеченный
  маркированным списком, измеряется как малоструктурный, что **занижает**
  совпадение вариантов.
- Ссылка прогона на промпт берётся из `related_artifacts` и является
  объявлением, а не фактом исполнения: замер доказывает отсутствие
  прослеживаемости, а не отсутствие применения.
- Второй измеритель ищет **лексический маркер** конструкции, а не её смысл:
  он доказывает отсутствие объявленной конструкции, а не отсутствие намерения
  автора. Маркеры намеренно широкие, поэтому покрытие корпуса скорее завышено.
- Лексические маркеры продуктовых доменов неразделяющие (66 прогонов из 67
  попадают более чем в один домен) и пригодны ровно для вывода «по тексту
  продукт не определяется».
