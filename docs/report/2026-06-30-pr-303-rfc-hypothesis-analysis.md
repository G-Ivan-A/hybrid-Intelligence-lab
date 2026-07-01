---
status: draft
version: 0.1
updated: 2026-06-30
temperature: 0.1
owner: G-Ivan-A
type: report
context: [hub, rfc, review, pr-303, hypothesis-analysis]
method: hypothesis-testing
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/306"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/306"
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/303"
related_artifacts:
  - "governance/rfc/2026-06-30-rfc-research-structure.md"
  - "standards/rfc-structure-standard.md"
---

# Отчет по гипотезе проблемы PR #303

## Контекст

Источник задачи: [issue #306](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/306).
Проверяемый источник проблемы: [PR #303](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/303).
Гипотеза: приложенный к issue файл `clarify_error_pr_303.txt`.

Проверяемый артефакт PR #303:
[`governance/rfc/2026-06-30-rfc-research-structure.md`](../../governance/rfc/2026-06-30-rfc-research-structure.md).
Нормативный контракт проверки:
[`standards/rfc-structure-standard.md`](../../standards/rfc-structure-standard.md).

## Вердикт

Ошибка генерации RFC не подтверждена: PR #303 был успешно смержен, локальные
валидаторы и CI для PR #303 проходили, а основной RFC-артефакт существует в
`main`.

Гипотеза проблемы подтверждена частично. Это не техническая ошибка генерации,
а minor completeness gap перед ADR B-017: RFC уже содержит обязательный
`## RFC Metadata`, но не выделял отдельные блоки для матрицы дельт A/B/C/D и
Boundary RFC/ADR. Эти блоки полезны для review и согласуются с
`standards/rfc-structure-standard.md`, поэтому RFC доработан.

## Проверка гипотезы

| Утверждение из гипотезы | Результат проверки | Решение |
| --- | --- | --- |
| `RFC Metadata` отсутствует как отдельная секция. | Не подтверждено. В смерженном файле есть `## RFC Metadata` сразу после заголовка RFC. | Правка не нужна. |
| Нет матрицы архетипных дельт A/B/C/D. | Подтверждено. В RFC был только `Archetype scope: A` в metadata, без явной матрицы последствий для B/C/D. | Добавлена секция `## Матрица дельт A/B/C/D`. |
| P5 слишком детален для RFC. | Не признано ошибкой. Issue #302 прямо просил предложить эвристические критерии классификации; P5 остается proposal-level материалом, а нормативное сжатие уйдет в B-018. | Оставить P5 без упрощения. |
| Boundary RFC/ADR не выделена таблицей. | Подтверждено как полезное уточнение. Граница была описана в Motivation, Impacted Artifacts и Lifecycle, но не отдельной таблицей. | Добавлена секция `## Boundary RFC/ADR`. |

## Причина расхождения

Причина не в сбое инструмента генерации. PR #303 выполнил DoD issue #302:
описал `exp/`, запрет `outputs/`, routing Research / Analysis / Audit, границу
с `runs/`, Critical Analysis и последствия для B-017..B-023.

Расхождение возникло из-за разной интерпретации RFC Structure Standard:
список required body sections не включает отдельные top-level секции
`Archetype Deltas` и `Boundary RFC/ADR`, но сам стандарт и recent accepted RFC
patterns ожидают, что для governance RFC эти аспекты будут явно отражены. Для
подготовки к ADR B-017 явная форма лучше скрытого упоминания в metadata и
lifecycle.

## Внесенная доработка

В RFC `governance/rfc/2026-06-30-rfc-research-structure.md`:

- версия draft повышена с `0.1` до `0.2`;
- добавлена матрица дельт A/B/C/D с границами применения proposal для Hub,
  prompt/pattern library, product spoke/runtime и education package;
- добавлена таблица Boundary RFC/ADR для цепочки B-016..B-023;
- P5 сохранен, потому что эвристики классификации были прямым требованием
  issue #302 и останутся proposal input для будущего стандарта B-018.

В валидатор структуры добавлены точечные проверки, чтобы эти две секции не
пропали из research-structure RFC при последующих правках.

## Проверка

Локальная проверка:

```bash
bash experiments/test-frontmatter-validator.sh      # pass
./tools/validate-file-naming.sh                     # pass
./tools/validate-frontmatter.sh .                   # pass
./tools/validate-repository-structure.sh            # pass
python3 tools/generate-manifest.py --check          # pass
bash -n tools/*.sh templates/htom/tools/*.sh templates/spoke/tools/*.sh  # pass
```

`./tools/validate-mkdocs-site.sh` локально не выполнен до конца: в окружении нет
`mkdocs` (`mkdocs: command not found`). GitHub Actions workflow устанавливает
`mkdocs-material` перед этим шагом, поэтому CI остается источником проверки
сайта.
