---
status: draft
version: 0.1
updated: 2026-09-10
temperature: 0.1
type: experiment
---

# exp: ba-process-taxonomy-571

Evidence container для датированного замера
[`../../2026-09-10-process-taxonomy-defects-facts.md`](../../2026-09-10-process-taxonomy-defects-facts.md)
и модулей
[`ba-process-taxonomy/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/projects/ba-gigacode-implementation/ba-process-taxonomy)
и
[`ba-operation-taxonomy/`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/tree/main/projects/ba-gigacode-implementation/ba-operation-taxonomy),
issue [#571](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571).

> **Ссылки.** Issue #571 требует абсолютных ссылок. Относительная ссылка на
> родительский отчёт выше — вынужденное исключение: её форму машинно проверяет
> [`tools/validate-evidence-structure.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/validate-evidence-structure.sh).

## Что здесь измеряется

Issue #571 требует не поправить формулировки, а **пересобрать** таксономию
процессов и операций. Такое решение нельзя принять по тексту: нужно показать,
что действующая таксономия дефектна **измеримо**, и что дефект не косметический,
а делает таксономию неисполнимой AI-агентом.

Третий измеритель отвечает на вопрос владельца к PR
[#572](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/572): равен ли
навык только подпроцессу и что различали исторические имена режимов. Он
измеряет 24 промпта спицы с суффиксами `-oneshot`, `-stepwise`, `-legacy` по
трём признакам (точка возврата управления актору, внутренний упорядоченный
алгоритм, число классов выхода) и каталог `L3` Хаба — по числу операций на
навык и по переиспользованию операций. Интерпретация — в отчёте
[`../../2026-09-10-skill-granularity-format-facts.md`](../../2026-09-10-skill-granularity-format-facts.md).

Второй измеритель отвечает на другой вопрос — чем ограничена среда исполнения.
Версия 0.1 мета-модели фиксировала форму `SKILL.md` как аналог практики навыков
агентов Claude, потому что документация GigaCode считалась недоступной.
Постановка issue #571 перечисляет одиннадцать страниц документации: снимок
проверяет их доступность и наличие 28 формулировок (`GC-1`–`GC-28`), на которые
опирается норма Хаба. Интерпретация — в отчёте
[`../../2026-09-10-gigacode-environment-facts.md`](../../2026-09-10-gigacode-environment-facts.md).

Измеритель дефектов проверяет восемь утверждений (`D1`–`D8`): слияние ФТ и ТЗ в одном
имени выхода при двух различных типах в онтологии спицы; «черновик» как граница
процесса при том, что `draft` — состояние жизненного цикла; число классов выхода
на одну операцию; перечисление разнородных результатов в определении операции;
наличие уровня подпроцесса в споке и его отсутствие в Хабе; отсутствие сущностей
«Система» и «Пользователь»; доля прогонов, чей процесс лежит вне закрытого
словаря; наличие ветвления в описании маршрута.

Содержательной интерпретации здесь нет — она в родительском отчёте и в двух
модулях таксономии.

## Состав

| Файл | Что это |
| --- | --- |
| [`audit-taxonomy-defects.py`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/audit-taxonomy-defects.py) | измеритель дефектов `D1`–`D8`; словари операций, процессов, сущностей и лексические маркеры — именованные константы в шапке |
| [`taxonomy-defects.json`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/taxonomy-defects.json) | результат: запись на каждый дефект с местами обнаружения |
| [`audit-taxonomy-defects.log`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/audit-taxonomy-defects.log) | вывод прогона, фиксирующий опубликованные цифры и коммиты обоих корпусов |
| [`2026-09-10-synthetic-cases.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/2026-09-10-synthetic-cases.md) | семь синтетических кейсов с эталонами: вход, шаги «процесс — навык — операции — гейт», ожидаемый результат |
| [`validate-new-taxonomy.py`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/validate-new-taxonomy.py) | проверка новой таксономии: словари читаются из модулей, эталоны — из кейсов; режим `--legacy` воспроизводит дефект прежнего словаря |
| [`taxonomy-validation.json`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/taxonomy-validation.json) | результат проверки: числа словарей, покрытие, перечень ошибок |
| [`validate-new-taxonomy.log`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/validate-new-taxonomy.log) | вывод обоих режимов проверки |
| [`fetch-gigacode-docs.py`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/fetch-gigacode-docs.py) | снимок документации среды GigaCode/GitVerse: HTTP-код, `sha256` HTML и наличие 28 контрольных формулировок `GC-1`–`GC-28` |
| [`gigacode-docs.json`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/gigacode-docs.json) | результат снимка: 11 страниц, заголовки разделов, хеши, статус каждого утверждения |
| [`measure-skill-format.py`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/measure-skill-format.py) | измеритель гранулярности и формата: гипотезы `H1`–`H3`; лексические маркеры точки возврата и порядка — именованные константы в шапке |
| [`skill-format.json`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/skill-format.json) | результат: разрез по режимам, разложение каталога `L3`, счётчики переиспользования операций |
| [`measure-skill-format.log`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/measure-skill-format.log) | вывод прогона с опубликованными цифрами |
| [`fetch-gigacode-docs.log`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/exp/ba-process-taxonomy-571/fetch-gigacode-docs.log) | вывод прогона снимка |

## Воспроизведение

```bash
git clone https://github.com/G-Ivan-A/mango_ba_prompts.git /tmp/mango
python3 audit-taxonomy-defects.py --mango /tmp/mango --hub ../../../.. --json taxonomy-defects.json
```

Проверка новой таксономии не требует спицы: словари читаются из модулей Хаба.

```bash
python3 validate-new-taxonomy.py --hub ../../../.. --json taxonomy-validation.json
python3 validate-new-taxonomy.py --hub ../../../.. --legacy
```

Снимок документации среды сети требует и в офлайне не воспроизводится:

```bash
python3 fetch-gigacode-docs.py --out gigacode-docs.json
```

Измеритель гранулярности требует спицы (разрез по режимам) и Хаба (каталог):

```bash
python3 measure-skill-format.py --mango /tmp/mango --hub ../../../.. --json skill-format.json
```

Код возврата `0` — точка возврата управления отделяет `stepwise` от `oneshot`
**и** утверждение «`oneshot` означает атомарность» опровергнуто; `1` — хотя бы
одно из двух не воспроизвелось, то есть правила `FM-1`–`FM-3` потеряли опору.

Код возврата `0` — все 28 контрольных формулировок найдены; `1` — какая-то из
них исчезла со страницы, то есть утверждение модуля потеряло опору и подлежит
пересмотру; `2` — страница недоступна. Копия чужой документации в Хабе не
хранится: воспроизводимость держится на дате снимка и `sha256` каждой страницы.

Первый прогон проходит только при полном покрытии: каждый навык разложен,
каждая операция вызвана, каждый шаг каждого кейса выражен словарями. Второй
прогон проходит только тогда, когда **все** шаги кейсов оказываются
невыразимыми в прежнем словаре — то есть дефект воспроизведён до исправления.

Коммиты, на которых получены опубликованные цифры, записаны в поле `corpus`
результата: спица `8cbf82aa73129ec5747af07f790aaf438b0fb6e9`, Хаб
`15aa76f88987511312cbf7cdb2c87b8912fb53f5`. На других коммитах цифры будут
другими — это ожидаемо, отчёт датирован.

## Границы измерения

- Снимок документации доказывает, что среда так **описана**, а не что она так
  работает: измерения поведения среды здесь нет.
- Точка возврата управления и внутренний порядок распознаются лексическими
  маркерами: замер доказывает наличие **объявленной** конструкции в тексте
  промпта, а не поведение среды на прогоне. Пропуск конструкции, выраженной
  иначе, занижает счётчик, но не создаёт ложного совпадения.
- Дефекты `D1`, `D2`, `D8` ищутся лексическими маркерами: замер доказывает
  наличие или отсутствие **объявленной конструкции**, а не намерение автора.
- `D4` считает маркеры перечисления, а не смысл; порог — два маркера и более,
  что занижает число дефектных определений.
- `D7` берёт объявленное поле процесса прогона: замер доказывает отсутствие
  привязки к словарю, а не отсутствие процесса как такового.
- Кейсы синтетические: они проверяют **выразимость** таксономии, а не качество
  работы БА на реальных данных. Утверждение «новая таксономия даёт лучший
  результат на реальном материале» этим экспериментом не проверяется.
