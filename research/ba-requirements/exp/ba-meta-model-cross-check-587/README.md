---
status: draft
version: 0.1
updated: 2026-09-15
temperature: 0.1
type: experiment
---

# exp: ba-meta-model-cross-check-587

Evidence container аудита
[`../../../../docs/audit/2026-09-15-ba-meta-model-cross-check-audit.md`](../../../../docs/audit/2026-09-15-ba-meta-model-cross-check-audit.md),
issue [#587](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/587).

> **Ссылки.** Относительная ссылка на родительский аудит выше — вынужденное
> исключение из правила абсолютных ссылок: её форму машинно проверяет
> [`tools/validate-evidence-structure.sh`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/tools/validate-evidence-structure.sh).

## Что здесь измеряется

Задача #587 требует эмпирической валидации мета-модели на реальных сырых
требованиях и прямо запрещает валидацию через воспроизведение согласованного
результата. Поэтому здесь два независимых замера.

| Файл | Вопрос замера | Ответ |
| --- | --- | --- |
| [`measure-slot-coverage.py`](measure-slot-coverage.py) | даёт ли действующая практика БА воспроизводимый скелет и какие слоты в ней не возникают | три прогона — три разных скелета, `M-1 = 0.0`; семь из четырнадцати слотов не встретились ни разу |
| [`validate-instances.py`](validate-instances.py) | исполнимы ли контракты пакета на сыром входе реальной практики, а не только на синтетическом Golden Set | оба входа и оба выхода проходят `C-IN` и `C-OUT` без ошибок |
| [`2026-09-15-historical-vs-new-comparison.md`](2026-09-15-historical-vs-new-comparison.md) | в чём новый результат расходится с историческим и обосновано ли расхождение | три обоснованных расхождения, одно содержательное совпадение, один маршрутный тупик |

## Состав

- [`historical-structure.yaml`](historical-structure.yaml) — подписи разделов
  итоговых артефактов прогонов `RUN-0013`, `RUN-0017`, `RUN-0021` корпуса
  [`mango_ba_prompts`](https://github.com/G-Ivan-A/mango_ba_prompts/tree/main/runs/2026)
  с локаторами. Цитируются только заголовки и минимальные фрагменты входа:
  корпус БЗ `kb/processed` в Хаб не копируется, его перенос — отдельная задача
  прямо в spoke `mango-ba-ai-runtime`.
- [`slot-coverage.json`](slot-coverage.json),
  [`measure-slot-coverage.log`](measure-slot-coverage.log) — результат первого замера.
- `runs/bcreq-1059/`, `runs/bcreq-975/` — экземпляры `A-IN` и `A-BCREQ`,
  собранные по действующим контрактам из сырых входов задач 1059 и 975.
- [`validate-instances.log`](validate-instances.log) — результат второго замера.

## Результат первого замера

```
слотов в скелете: 14
RUN-0013: разделов 7, покрытие 0.429, слитых заголовков 1
    слит: «4. Функциональные требования и сценарии использования» → S-FR, S-SCENARIO
RUN-0017: разделов 7, покрытие 0.5, слитых заголовков 1
    слит: «Функциональные требования и сценарии использования» → S-FR, S-SCENARIO
RUN-0021: разделов 5, покрытие 0.286, слитых заголовков 0
прогонов 3, различных скелетов 3, M-1 = 0.0
слоты, не встретившиеся ни разу: S-AC, S-INTEGRATION, S-OPEN, S-SCOPE, S-SETTINGS, S-TRACE, S-UI
```

Замер подтверждает базовое значение `M-1 = 0` метрики пакета уже не на корпусе
из 17 документов, а на трёх завершённых прогонах с обратной связью БА, и даёт
дополнительный факт: слитый заголовок «ФТ **и** сценарии использования»
встречается в двух прогонах из трёх, то есть это устойчивый образец практики,
а не случайность одного документа.

## Воспроизведение

```sh
pip install jsonschema pyyaml
python3 measure-slot-coverage.py
python3 validate-instances.py
```
