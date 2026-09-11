---
status: draft
version: 0.1
updated: 2026-09-10
temperature: 0.3
type: research
context: [ba, taxonomy, operation, atomicity, skill, contract, issue-571]
method: defect-driven-redesign + contract-design
scope: mango-only
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571"
based_on:
  - research/ba-requirements/2026-09-10-process-taxonomy-defects-facts.md
  - projects/ba-gigacode-implementation/ba-process-taxonomy/20-taxonomy.md
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/571"
---

# Таксономия операций: введение

## BLUF

1. Прежний словарь из тринадцати «операций» — не операции, а **классы работы**:
   семь из тринадцати производят более одного класса выхода, восемь из
   тринадцати перечисляют разнородные результаты в собственном определении
   (`D3`, `D4`,
   [факты](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-10-process-taxonomy-defects-facts.md)).
2. Операция здесь — **атомарное, но семантически завершённое когнитивное
   действие** со строгим контрактом входа и выхода, как требует issue #571:
   «Извлечение сущностей», «Проверка на атомарность», а не «прочитать» и не
   «нажать».
3. Атомарность объявлена шестью проверяемыми критериями `OA-1`–`OA-6`, а не
   ощущением размера. Ключевые: ровно один контракт выхода, отсутствие
   ветвления, ровно один тип когнитивной работы.
4. Всё, что требует последовательности или ветвления, — **навык (подпроцесс)**
   или процесс, а не операция. Разграничение оформлено машинно проверяемым
   тестом уровня.
5. Словарь **закрытый**: 31 операция в пяти когнитивных классах — извлечение,
   преобразование, порождение, проверка, оценка и выбор. Значение вне словаря
   не используется, а открывает задачу на расширение (`T-2`).
6. Каждый из **33 навыков** таксономии процессов разложен на операции этого
   словаря. Навык без разложения не считается определённым (`EX-4`).
7. Класс операции определяет, каким механизмом контроля она проверяется:
   порождение и оценка не проверяются схемой, извлечение и преобразование
   проверяются.
8. Микродействия («прочитать файл», «вызвать инструмент») из словаря
   исключены: это вызовы инструментов среды исполнения, у них нет
   собственного предмета анализа.
9. Словарь специализирован под предметную область Манго КК и среду GigaCode.
   Переносимость — гипотеза
   ([`50-open-research.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-operation-taxonomy/50-open-research.md), §1).

## Что закрывает модуль

| Контракт issue #571 | Где закрыт |
| --- | --- |
| Новая таксономия операций с корректной гранулярностью | [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-operation-taxonomy/20-taxonomy.md), §2–§3 |
| Привязка операций к навыкам и подпроцессам | [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-operation-taxonomy/20-taxonomy.md), §4 |
| Критерии атомарности вместо интуиции | [`10-theory.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-operation-taxonomy/10-theory.md), §2 |
| Разграничение «операция / навык / процесс» | [`30-decision-framework.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-operation-taxonomy/30-decision-framework.md), §1 |
| Исполнимость агентом, а не только человеком | [`30-decision-framework.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-operation-taxonomy/30-decision-framework.md), §3 |
| Проверка на синтетических кейсах | [`40-practice-and-cases.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-operation-taxonomy/40-practice-and-cases.md), §2 |
| Депрекация прежних тринадцати значений | [`20-taxonomy.md`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-operation-taxonomy/20-taxonomy.md), §5 |

## Основания

| Источник | Что взято |
| --- | --- |
| [Измерение дефектов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ba-requirements/2026-09-10-process-taxonomy-defects-facts.md) | `D3`, `D4` — числовое основание для пересборки словаря |
| [Таксономия процессов](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-process-taxonomy/20-taxonomy.md) | 10 процессов и 33 навыка, которые разлагаются на операции |
| [Механизмы контроля `G1`–`G7`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/research/ai-education/task-processing/20-taxonomy.md) | шкала ярусов и правило «необратимое действие не удерживается ниже `G5`» |
| [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) | характеристики качества требования — предмет операций класса «проверка» |
| [Мета-модель БА](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/main/projects/ba-gigacode-implementation/ba-meta-model/20-taxonomy.md) | правила словаря `T-1`–`T-5`, классы артефактов, контракты `C-*` |

## Чего в модуле нет

- **Нет реализаций.** Операция описана контрактом, а не промптом: текст
  промпта — артефакт исполняющей среды, а не таксономии.
- **Нет вызовов инструментов.** `read_file`, `search`, `write` — уровень среды,
  не уровень анализа.
- **Нет утверждения об универсальности.** Словарь выведен из работы КК Манго.
