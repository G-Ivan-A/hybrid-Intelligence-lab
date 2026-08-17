---
status: draft
version: 0.1
updated: 2026-08-08
temperature: 0.5
---

# Agentic Evaluation: теория и ограничения измерения

<!-- CROSS-REVIEW [Codex-validation]: P5 RFC (обратная связь «практика → теория») не имеет носителя: в файле нет ни одной ссылки на 40-practice-and-cases.md, а таблицы проверяемых гипотез — в отличие от 10-theory.md модулей tool-use (H1–H8) и information-extraction-graph-modeling (H1–H16) — здесь нет вовсе. Без гипотез и без обратной ссылки практике нечего опровергать: триггер «воспроизведённое расхождение практики с рамкой — дефект рамки» не может сработать. Сработавших триггеров P5 в модуле: 0. -->

## 1. Единица оценки

Eval case — это не только prompt/answer. Минимальная запись содержит snapshot
input и источников, ожидаемые инварианты или reference, actual output, trace,
grader и его версию, score/reason, стоимость, latency и решение reviewer.
Иначе результат нельзя воспроизвести после смены модели, prompt или корпуса.

## 2. Четыре слоя доказательства

| Слой | Вопрос | Пример |
| --- | --- | --- |
| deterministic | Формат и обязательные инварианты соблюдены? | JSON Schema, ID, provenance span |
| reference-based | Совпал результат с размеченным ожидаемым объектом? | entity/relation F1, exact match |
| semantic judge | Эквивалентен ли смысл / соблюдена ли rubric? | groundedness, plan adherence |
| human outcome | Полезен ли результат для решения и приемлем ли риск? | blinded review, task success |

Слои дополняют друг друга. Детерминированный check дешёв и воспроизводим, но не
понимает смысл; judge покрывает смысл, но привносит model-specific variance;
человек лучше видит доменную цену ошибки, но дорог и также расходится с другими
аннотаторами.

## 3. LLM-as-judge

### Паттерны

- pointwise rubric: один output получает ordinal/binary score;
- pairwise: judge выбирает A/B/tie; полезно для регрессии между версиями;
- reference-based: сравнение с gold/evidence;
- reference-free: проверка по rubric без эталонного ответа;
- ensemble/panel: несколько judges с независимым порядком и агрегацией.

В MT-Bench GPT-4 judge достиг более 80% согласия с человеческими preferences на
контрольной выборке, близко к согласию между людьми, но авторы также измерили
position, verbosity и self-enhancement bias. Chatbot Arena снизила зависимость
от одного judge через blind randomized pairwise human votes, однако arena
ranking — preference, а не factual correctness
([Zheng et al.](https://arxiv.org/abs/2306.05685)).

### Минимальные контрмеры

1. фиксировать rubric и требовать evidence/reason, не «оцени качество»;
2. случайно менять A/B и повторять спорные pairwise cases в обратном порядке;
3. нормализовать стиль/длину либо отдельно измерять verbosity;
4. скрывать model/vendor identity;
5. калибровать на double-reviewed human sample и считать confusion matrix;
6. отправлять disagreement и high-risk cases человеку;
7. pin model/prompt, сохранять raw judge output и регулярно переоценивать drift.

Нельзя интерпретировать judge score как вероятность истинности без отдельной
calibration. Cohen's kappa/Krippendorff's alpha нужны для agreement сверх
случайности; correlation сама по себе может скрывать систематический bias.

## 4. Golden sets как data product

Golden set включает:

- corpus/source snapshot и лицензионную/PII границу;
- label schema, ontology и annotation guide;
- positive, negative, boundary, adversarial и abstention cases;
- business impact и slice tags (язык, тип документа, сложность, редкий класс);
- independent annotation, adjudication и disagreement;
- train/dev/test разделение и закрытый regression holdout;
- version, change log и provenance каждого label.

Manual annotation даёт доменную валидность, synthetic generation расширяет
покрытие, а active learning направляет человека на uncertain/disagreement
cases. Синтетический case не становится gold до проверки человеком: генератор
может воспроизвести bias будущего judge.

В adjacent high-stakes domains полезны не готовые thresholds, а образцы
контрактов: LegalBench формулирует legal reasoning tasks с domain experts
([Guha et al.](https://arxiv.org/abs/2308.11462)); MultiMedQA сочетает medical
QA datasets и human evaluation dimensions
([Singhal et al.](https://www.nature.com/articles/s41586-023-06291-2));
FinQA связывает financial questions с evidence и executable reasoning programs
([Chen et al.](https://aclanthology.org/2021.emnlp-main.300/)).

## 5. Threshold и статистика

Threshold выбирается по loss function, а не по круглому числу:

`Expected loss = C_FP × FP + C_FN × FN + C_review × Reviews + C_run × Runs`.

Для critical slice задаётся отдельный gate; macro average не должен компенсировать
провал редкого high-impact класса. Наряду с point estimate нужны sample size,
bootstrap confidence interval и baseline (human, предыдущая версия, простой
детерминированный метод). При множественных prompt/model comparisons нужен
закрытый test set, иначе оптимизация превращает eval в training data.
