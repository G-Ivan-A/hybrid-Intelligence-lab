---
status: draft
version: 0.1
updated: 2026-06-29
temperature: 0.1
type: audit
context: [hub, research, audit, artifacts, experiments, governance]
method: manual-review
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/290"
scope: repo
based_on: "standards/research-profile.md; docs/adr/2026-06-adr-002-artifact-document-methodology.md; issue #290 DoD"
audit_target: "Research artifact format contract: standards/research-profile.md, ADR-001/ADR-002, file naming standards and issue #290 DoD"
evidence_model: "manual-review + git-history + issue-pr-review"
verdict: conditional
severity_scale: "P0/P1/P2/P3"
follow_up: "Clarify exp-<slug>/outputs/ vs runs/ boundary in downstream governance cleanup"
related_norm: "standards/research-profile.md; standards/file-naming.md; docs/adr/2026-06-adr-002-artifact-document-methodology.md"
related_artifacts:
  - "research/hub/2026-06-28-research-analysis-audit-inventory.md"
  - "research/hub/exp-research-analysis-audit-288/"
  - "governance/rfc/2026-06-30-rfc-research-structure.md"
---

# Audit: Research artifact format contract

## Summary / BLUF

Вердикт: **conditional**. Аудит не нашёл единого решения "research-артефакт:
Markdown -> папка"; действующая практика соответствует dual report + experiment
model. Отклонение остаётся в границе `exp-<slug>/outputs/` vs `runs/`: это не
ломает текущий репозиторий, но требует явного downstream-уточнения.

## Scope / Target

Проверка выполнена против issue #290, `standards/research-profile.md`,
`standards/file-naming.md`, `standards/file-naming-convention.md`, ADR-001,
ADR-002, AI governance, README/index files and PR/issue history for first
`research/hub/exp-*` usages. Scope: Hub repository and its research artifact
format contract.

## Method / Evidence

Evidence model: manual review, git history search, issue/PR review and local
repository inspection. Reproducible commands are listed in
[3.3. Evidence commands](#33-evidence-commands); the evidence corpus includes PR
#279, PR #285, PR #289 and issue #290.

## Findings / Verdict

Основные findings:

- Report file + experiment corpus is an intentional model inherited from the
  historical research profile.
- The real drift is not "folder instead of Markdown", but unclear ownership of
  curated experiment outputs vs operational run records.
- No immediate rollback to md-only is recommended.

Итоговый verdict: **conditional** until the `exp-<slug>/outputs/` vs `runs/`
boundary is clarified.

## Remediation / Deviation

Deviation handling: preserve the dual model as an accepted current practice and
route the unresolved boundary into follow-up governance work. No immediate file
migration is required by this audit.

## Related Artifacts

- Issue [#290](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/290).
- `standards/research-profile.md`, `standards/file-naming.md`,
  `standards/file-naming-convention.md`.
- `docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md` and
  `docs/adr/2026-06-adr-002-artifact-document-methodology.md`.
- PR #279, PR #285 and PR #289.

## 1. Введение

**Причина.** Issue
[#290](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/290)
зафиксировала видимое расхождение: свежие research-артефакты в `research/hub/`
появились как каталоги `exp-*` с `README.md` и `outputs/`, тогда как
ADR-001/002 и `standards/file-naming.md` говорят о хронологических Markdown-файлах
`YYYY-MM-DD-name.md`.

**Цель.** Найти источник изменения формата, процесс или контракт, который
разрешает каталоги, отделить сознательное решение от дрейфа практики и дать
рекомендацию: сохранять папочную структуру или возвращаться к md-only.

**Связанные артефакты.** `standards/research-profile.md`,
`standards/file-naming.md`, `standards/file-naming-convention.md`,
`docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md`,
`docs/adr/2026-06-adr-002-artifact-document-methodology.md`,
`AI_GOVERNANCE.md`, `research/README.md`, `research/hub/README.md`,
`governance/artifact-map.md`, issue #278, issue #284, issue #288, PR #279,
PR #285 and PR #289.

**Метод.** Manual review of active standards, templates, AI governance files, ADR,
RFC, changelog and artifact-map records, plus git history over `research/hub/` and
the PR/issue bodies that introduced the current experiment folders.

## 2. Результаты исследования

### 2.1. Главный вывод

Перехода "research-артефакт: md -> папка" как единого решения не найдено.
Текущий контракт задает **двухчастную модель**:

1. основной результат исследования или анализа остается хронологическим
   Markdown-файлом `research/<domain>/YYYY-MM-DD-name.md`;
2. воспроизводимая доказательная база может жить рядом как
   `research/<domain>/exp-<slug>/` с `README.md`, скриптом и `outputs/`.

Источником этой модели является не ADR/RFC, а
`standards/research-profile.md`. Она присутствовала уже в первой версии профиля
от 2026-05-26: профиль одновременно требовал `YYYY-MM-topic.md` для отчета и
`exp-<slug>/` для воспроизводимого эксперимента. Позднее naming-стандарт
перевел отчеты на `YYYY-MM-DD-name.md`, но не отменил experiment folders.
Практический shorthand для этого контракта: dual report + experiment model.

Фактическое использование `exp-*` в `research/hub/` началось позже:

| Дата | Commit / PR | Что произошло |
| --- | --- | --- |
| 2026-05-26 | `a7760da` | Добавлен `standards/RESEARCH_PROFILE.md` с моделью report file + `exp-<slug>/outputs/`. |
| 2026-06-25 | PR #268 / PR #272 | Хронологические research-файлы нормализованы к date-first `YYYY-MM-DD-name.md`; experiment folders не отменены. |
| 2026-06-27 | `8d76658`, PR #279 | Первое visible применение в `research/hub/`: `exp-rfc-adr-industry-norms/` как reproducible evidence corpus для issue #278. |
| 2026-06-28 | `6d0aae1`, PR #285 | Повторение паттерна: `exp-ripple-effects-282/` для baseline frontmatter scan. |
| 2026-06-28 | `1329169`, PR #289 | Повторение паттерна: `exp-research-analysis-audit-288/` для матрицы Research / Analysis / Audit. |
| 2026-06-28 | `3b3b655` | `standards/research-profile.md` переведен в `status: accepted`, но `exp-<slug>/` был в профиле уже раньше. |

### 2.2. Что именно зафиксировано контрактами

| Scope из issue #290 | Результат проверки |
| --- | --- |
| `standards/research-profile.md` | Явно фиксирует `YYYY-MM-DD-topic.md` как отчет и `exp-<slug>/` как воспроизводимый эксперимент. В структуре эксперимента указаны `README.md`, `run.sh`, `inputs/`, `outputs/`. |
| `standards/file-naming.md` / `file-naming-convention.md` | Фиксируют имена хронологических Markdown-файлов в `research/<domain>/` как `YYYY-MM-DD-name.md`. Они валидируют файлы, а не запрещают каталоги `exp-*`. |
| `docs/adr/2026-06-adr-001...` | Определяет целевую инфраструктуру с `runs/` и правилом размещения результатов выполнения, но для Research Hub сохраняет `research/` как расширение архетипа A. |
| `docs/adr/2026-06-adr-002...` | Для Research Hub указывает `research/{domain}/YYYY-MM-DD-name.md`, а для run record - `runs/`. Не описывает, как это соотносится с `research-profile.md` `exp-<slug>/outputs/`. |
| `templates/` | Issue templates требуют traceability, frontmatter, navigation/artifact-map/changelog updates. HTOM templates запрещают создавать `research/` и `experiments/` "на вырост" в командах без operational pain. Прямого правила "создавать research-папку вместо md" нет. |
| `ai-rules/` и `AI_GOVERNANCE.md` | В текущем Хабе каталога `ai-rules/` нет; ADR-001 называет его целевым каталогом для будущей структуры. `AI_GOVERNANCE.md` требует связывать значимые claims с sources, experiments, issues, PRs или migration records. |
| `governance/rfc/` | Не найден RFC, который отдельно меняет формат research artifacts с md на папки. `resolve-artifact-location-proposal.md` маршрутизирует source-backed analysis в `research/<domain>/`, но не решает report-vs-experiment boundary. |
| `CHANGELOG.md` | Отражает добавление experiment folders в PR #279/#285/#289 как reproducible evidence/baseline/scan, рядом с основными dated reports. |
| История `research/hub/` | До 2026-06-27 Hub research был в основном набором dated Markdown reports; после PR #279 появились повторяемые experiment folders для задач с reproducible scan/evidence. |
| Issue #288 и связанные | #288/PR #289 продолжили уже возникший паттерн: основной artifact - dated Markdown inventory; папка - воспроизводимый scan corpus. |

### 2.3. Сознательное решение или дрейф

**Сознательное решение:** `standards/research-profile.md` с 2026-05-26 задает
experiment folders как часть research-профиля. Это было не случайное имя
каталога, а заранее описанная модель воспроизводимости.

**Практический дрейф:** первые реальные `research/hub/exp-*` каталоги появились
только 2026-06-27 и стали повторяться как implementation pattern в PR #279, #285
и #289. Эти PR описывали папки как reproducible evidence или scan baseline, но не
создавали отдельный RFC/ADR, который reconciles `exp-<slug>/outputs/` с ADR-002
`runs/`.

**Оставшаяся коллизия:** `research-profile.md` разрешает хранить outputs
внутри research experiment folder, а ADR-002 отдельно говорит, что результаты
выполнения и экспериментов относятся к `runs/`. Это не ломает текущий репозиторий,
потому что ADR-001 сохраняет переходный режим для Хаба, но создает ambiguous
future contract.

### 2.4. Рекомендации

| # | Рекомендация | Куда фиксируется |
| --- | --- | --- |
| 1 | Сохранить двухчастную модель: dated Markdown report как основной research artifact; `exp-<slug>/` только для воспроизводимого evidence corpus. | `standards/research-profile.md` |
| 2 | Не возвращаться к md-only как общему правилу: это ухудшит воспроизводимость задач вроде #278/#284/#288. | PR #291 / future RFC if human decision needed |
| 3 | Явно развести три класса: research report, research experiment corpus, operational run record. Кандидат: `exp-<slug>/outputs/` хранит curated evidence for a report; `runs/` хранит execution/run records outside a specific research report. | ADR-002 addendum or research-profile update |
| 4 | Обновить `research/README.md` recommended structure так, чтобы code block тоже показывал optional `exp-<slug>/`, а не только Markdown reports. | follow-up PR |
| 5 | Усилить validator: разрешать `research/<domain>/exp-<slug>/` только если есть `README.md` и ссылка на parent dated report; все Markdown files внутри `research/` продолжают проходить date-first naming unless they are allowed exceptions like `README.md`. | `tools/validate-repository-structure.sh` / `tools/validate-file-naming.sh` |
| 6 | Не мигрировать существующие `exp-*` каталоги до решения по ADR-002 vs research-profile boundary. | future migration issue |

### 2.5. Открытые вопросы

1. Нужно ли делать отдельный ADR-002 addendum для границы `exp-<slug>/outputs/`
   vs `runs/`, или достаточно уточнить `standards/research-profile.md`?
2. Должны ли future experiment folders использовать issue-number slug
   (`exp-...-290`) как mandatory traceability convention?
3. Должны ли experiment folders регистрироваться в artifact-map всегда или только
   когда outputs являются durable evidence for a reviewed/canonical report?

## 3. Детализация

### 3.1. Почему это не "папка вместо md"

Во всех трех свежих случаях папка появилась **рядом** с основным Markdown
отчетом:

| Issue / PR | Main report | Experiment folder |
| --- | --- | --- |
| #278 / #279 | `2026-06-27-rfc-industry-norms-and-variants.md`, `2026-06-27-adr-industry-norms-and-variants.md` | `exp-rfc-adr-industry-norms/` |
| #284 / #285 | `2026-06-28-ripple-effects-282-research.md` | `exp-ripple-effects-282/` |
| #288 / #289 | `2026-06-28-research-analysis-audit-inventory.md` | `exp-research-analysis-audit-288/` |

Поэтому наблюдаемая практика - не замена report file на folder artifact, а
добавление sibling evidence corpus. Если future work создает только папку без
parent report, это уже будет нарушением intent текущего research-profile.

### 3.2. Почему issue #290 выглядела как конфликт

Конфликт возник из-за разных уровней правил:

- `standards/file-naming.md` отвечает за имена файлов, а не за структуру
  воспроизводимых experiment folders;
- ADR-002 фиксирует high-level routing and lifecycle, но не детализирует
  research experiment package;
- `standards/research-profile.md` детализирует research work and reproducibility
  and therefore contains the concrete `exp-<slug>/outputs/` shape;
- artifact-map and README files later registered actual experiment folders,
  making the practice visible as active repository structure.

Это значит, что источник папочной структуры есть, но он находится в профильном
standard, а не в ADR/RFC. Недостающая часть - explicit reconciliation между
standard-level experiment folder и ADR-level `runs/`.

### 3.3. Evidence commands

The audit used these reproducible checks:

```bash
git log --all --date=iso-strict --name-status -- research/hub
git log --all --date=iso-strict -S'exp-<slug>' -- standards/research-profile.md research/hub research/README.md tools/validate-repository-structure.sh
git show a7760da6b878fbc954e0de2d4c8795ef2595b535:standards/RESEARCH_PROFILE.md
gh issue view 278 --repo G-Ivan-A/hybrid-Intelligence-lab --json number,title,body,url
gh pr view 279 --repo G-Ivan-A/hybrid-Intelligence-lab --json number,title,body,files,url
gh issue view 284 --repo G-Ivan-A/hybrid-Intelligence-lab --json number,title,body,url
gh pr view 285 --repo G-Ivan-A/hybrid-Intelligence-lab --json number,title,body,files,url
gh issue view 288 --repo G-Ivan-A/hybrid-Intelligence-lab --json number,title,body,url
gh pr view 289 --repo G-Ivan-A/hybrid-Intelligence-lab --json number,title,body,files,url
```

## 4. Источники

- [Issue #290](https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/290) -
  audit request.
- `standards/research-profile.md` - active Research Profile and earliest
  standard source for `exp-<slug>/outputs/`.
- `standards/file-naming.md` and `standards/file-naming-convention.md` -
  date-first file naming contracts.
- `docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md` - target
  repository infrastructure and transition mode.
- `docs/adr/2026-06-adr-002-artifact-document-methodology.md` - artifact
  lifecycle and routing rules.
- `AI_GOVERNANCE.md` - AI-assisted work traceability and source/experiment
  requirements.
- `research/README.md`, `research/hub/README.md` and `governance/artifact-map.md`
  - active repository navigation and artifact registry.
- PR #279, PR #285 and PR #289 - first concrete Hub uses of `research/hub/exp-*`.
