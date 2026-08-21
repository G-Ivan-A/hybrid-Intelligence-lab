---
status: draft
version: 0.1
updated: 2026-08-21
temperature: 0.1
type: audit
context: [hub, governance, architecture, structure, genome, htom, adr-007, b-056, issue-529]
method: keyword-scan + contract-reading + validator-run + cross-reference-check
source: "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/529"
scope: repo
audit_target: "Структурная, нормативная и терминологическая согласованность Хаба после реструктуризации B-048/B-056: геном `templates/htom/` (включая `templates/htom/tools/validate-repository-structure.sh`), шаблоны `templates/spoke/` и `templates/sync-project-with-hub-prompt.md`, стандарты `standards/`, решения `docs/adr/` и `docs/rfc/`, руководства `guides/`, реестры `pr-ops/artifact-map.md` и `pr-ops/backlog.md`, валидаторы `tools/` и `.github/workflows/validate.yml`"
evidence_model: "прямое чтение файлов репозитория с указанием путей и номеров строк + систематический grep-поиск по маркерам устаревшей структуры (`AI_GOVERNANCE`, `governance/`, `mkdocs`, `в корне`) + прогон всех локальных валидаторов Хаба и генома + два воспроизводимых скрипта в `experiments/`"
verdict: fail
severity_scale: "Critical/Major/Minor/Info"
follow_up: "Gap-Report ниже: 12 противоречий, из них 2 Critical требуют нового ADR (правки `docs/adr/` запрещены `tools/validate-historical-immutable.sh`), 7 закрываются микро-правками, 3 требуют решения человека."
related_norm: "standards/audit-standard.md, standards/issue-workflow.md, standards/file-naming.md, standards/adr-structure-standard.md, standards/htom-documentation-structure.md, standards/glossary.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/529"
  - "https://github.com/G-Ivan-A/mango_ba_prompts/pull/292"
related_artifacts:
  - "templates/htom/tools/validate-repository-structure.sh"
  - "templates/sync-project-with-hub-prompt.md"
  - "templates/spoke/README.md"
  - "templates/manifest.json"
  - "standards/htom-documentation-structure.md"
  - "standards/adr-structure-standard.md"
  - "standards/glossary.md"
  - "standards/issue-workflow.md"
  - "docs/adr/2026-07-adr-007-hub-root-structure.md"
  - "pr-ops/artifact-map.md"
  - "pr-ops/backlog.md"
  - "guides/deploy-project.md"
  - "guides/sync-from-hub.md"
  - "tools/validate-repository-structure.sh"
  - "tools/validate-file-naming.sh"
  - "research/hub/exp/hub-contradictions-audit-529/link-check.py"
  - "research/hub/exp/hub-contradictions-audit-529/artifact-map-coverage.py"
---

# Аудит структурных, нормативных и терминологических противоречий Хаба

## Summary / BLUF

**Verdict: fail.** Найдено **12 противоречий**, оставшихся после реструктуризации
(B-048 «физическая миграция», B-056 «разделение governance/»): 2 **Critical**,
5 **Major**, 5 **Minor**.

Ключевой вывод: **все три валидатора Хаба и валидатор генома проходят с exit 0**,
то есть ни одно из найденных противоречий сейчас не видно CI. Расхождение живёт
не в коде проверок, а в текстовом корпусе и в области, которую проверки не
покрывают.

Корневая причина инцидента-триггера
([mango_ba_prompts PR #292](https://github.com/G-Ivan-A/mango_ba_prompts/pull/292)) —
**асимметрия между Хабом и геномом**: Хаб, который сам является HTOM-командой
(`standards/glossary.md:65` — «Примеры: `mango_ba_prompts`, `repo-development`,
сам Хаб»), по B-056 вынес `AI_GOVERNANCE.md` из корня в `ai-governance/` и
`ai-rules/`, но геном `templates/htom/tools/validate-repository-structure.sh:65`
до сих пор жёстко требует `AI_GOVERNANCE.md` **в корне** каждой HTOM-команды,
называя это «жёстким ограничением Хаба». Хаб нарушает собственный геном.

## Scope / Target

**В границах аудита:**

| Область | Что проверялось |
| --- | --- |
| `templates/htom/` | геном: жёсткие требования (`require_file`, `require_dir`, structure checks), тексты `AI_QUICK_RULES.md`, `README.md`, отсутствие CI |
| `templates/spoke/`, `templates/*.md`, `templates/manifest.json` | ссылки на пути Хаба, criticality-разметка Smart Sync |
| `standards/` | нормативная согласованность между стандартами и с ADR |
| `docs/adr/`, `docs/rfc/` | устаревшие структурные допущения, артефакты переписывания ссылок |
| `guides/` | процедуры, ссылающиеся на выведенные из эксплуатации механизмы |
| `pr-ops/` | `artifact-map.md`, `backlog.md` как реестры-SSOT |
| `tools/`, `.github/workflows/validate.yml` | что именно машинно проверяется, а что нет |

**Вне границ:** содержательная корректность research-корпуса; состояние
внешних репозиториев (mango, open-ai.ru, clarify-engine-ai) — они упоминаются
только как контекст триггера.

## Method / Evidence

1. **Систематический keyword-scan** по маркерам устаревшей структуры:
   `AI_GOVERNANCE`, `governance/` (корневой, не `ai-governance/`), `mkdocs`,
   `website/`, `experiments/`, `в корне`, `kb/`, `runs/`.
2. **Contract-reading**: сплошное чтение генома `templates/htom/` (все файлы),
   `standards/*.md`, ADR-007, `pr-ops/artifact-map.md`, `guides/*.md`.
3. **Прогон валидаторов** — фактическое состояние, а не декларируемое:

   | Валидатор | Результат |
   | --- | --- |
   | `tools/validate-repository-structure.sh` | passed, exit 0 |
   | `tools/validate-file-naming.sh` | passed, exit 0 |
   | `tools/validate-frontmatter.sh .` | passed, exit 0 |
   | `templates/htom/tools/validate-repository-structure.sh` (in place) | passed, exit 0, 1 warning (незаменённые `{{...}}`) |

4. **Воспроизводимые скрипты** (сохранены как evidence):
   - `research/hub/exp/hub-contradictions-audit-529/link-check.py` — проверка всех относительных
     markdown-ссылок в отслеживаемых `*.md`. Результат: 19 нерезолвящихся, из
     них 18 — легитимные `{{hub_url}}`-плейсхолдеры шаблонов, 1 — реальная
     устаревшая ссылка (G-03).
   - `research/hub/exp/hub-contradictions-audit-529/artifact-map-coverage.py` — сверка `pr-ops/artifact-map.md`
     с `git ls-files '*.md'`. Результат: **0** висящих путей в карте,
     **62 из 313** отслеживаемых md-файлов не зарегистрированы (G-09).

**Ограничение доказательной базы:** номера строк соответствуют состоянию ветки
`issue-529-d4443a24abe8` на 2026-08-21 и сдвинутся при последующих правках.

## Findings / Verdict — Gap-Report

| # | Тип противоречия | Локация в Хабе | Суть конфликта (старое правило vs новое правило) | Рекомендуемое действие |
| --- | --- | --- | --- | --- |
| G-01 | Структурное | `templates/htom/tools/validate-repository-structure.sh:43`, `:64-65` (дубль `require_file "AI_GOVERNANCE.md"`) | **Старое:** «`AI_GOVERNANCE.md` обязателен в корне каждой HTOM-команды (жёсткое ограничение Хаба)». **Новое:** B-056 + ADR-007 (`docs/adr/2026-07-adr-007-hub-root-structure.md:239`) вынесли policy-материал в `ai-governance/`, а правила агента — в `ai-rules/`; в корне Хаба файла больше нет. Хаб — сам HTOM-команда (`standards/glossary.md:65`), то есть **нарушает собственный геном**. Прямая причина отказа в [mango PR #292](https://github.com/G-Ivan-A/mango_ba_prompts/pull/292). | **Создать RFC**: решить, остаётся ли `AI_GOVERNANCE.md` корневым контрактом генома или геном допускает `ai-governance/`+`ai-rules/`. Решение — за человеком: это выбор архитектуры, не микро-правка. Затем обновить валидатор генома (и убрать дублирующий `require_file` на строке 65). **Critical** |
| G-02 | Структурное | `templates/manifest.json` (`templates/htom/tools/validate-repository-structure.sh` = `RECOMMENDED`); отсутствие `templates/htom/.github/workflows/` (подтверждено `git ls-files templates/htom`) | **Старое/фактическое:** «иммунная система» генома объявлена в `templates/htom/README.md` и в `pr-ops/artifact-map.md:160`, но поставляется как `RECOMMENDED` и **без CI-workflow** — в клонированной HTOM-команде она никогда не запускается автоматически. Ср. `templates/spoke/.github/workflows/ci.yml`, который у спока есть и помечен `CORE`. **Новое:** ADR-007 требует синхронизации валидаторов с целевой структурой. | **Обновить**: добавить `templates/htom/.github/workflows/validate.yml`, вызывающий валидатор генома, и поднять criticality валидатора до `CORE` в `templates/sync-metadata.json` (с последующей регенерацией `templates/manifest.json`). Иначе противоречие G-01 будет и дальше обнаруживаться только вручную в PR споков. **Critical** |
| G-03 | Структурное | `templates/spoke/README.md:29` | **Старое:** ссылка на `governance/rfc/htom-vs-spoke-clarification-2026-06.md`. **Новое:** файл живёт в `docs/rfc/htom-vs-spoke-clarification-2026-06.md` (Phase 3 ADR-007). Ссылка ведёт в 404 у каждого нового спока. | **Обновить** путь на `docs/rfc/...`. Микро-правка. **Major** |
| G-04 | Структурное | `templates/sync-project-with-hub-prompt.md:27-28` | **Старое:** исполнимый (`executable: true`, `status: canonical`) промпт синхронизации указывает агенту точки входа `governance/artifact-map.md` и `governance/repo-model.md`. **Новое:** каталоги — `pr-ops/artifact-map.md` и `pr-ops/repo-model.md`. Агент, исполняющий канонический контракт, гарантированно не найдёт реестры. | **Обновить** оба пути на `pr-ops/`. Микро-правка, но приоритет высокий: документ исполнимый. **Major** |
| G-05 | Структурное | `guides/sync-from-hub.md:53` | **Старое:** `git diff HEAD hub/main -- templates/ standards/ governance/` — pathspec `governance/` больше не существует, diff молча теряет весь мигрированный корпус (`ai-governance/`, `ai-rules/`, `pr-ops/`, `docs/rfc/`). **Новое:** структура ADR-007. Отказ тихий: git не сообщает об отсутствующем pathspec в этой форме. | **Обновить** pathspec: `templates/ standards/ ai-governance/ ai-rules/ pr-ops/`. **Major** |
| G-06 | Нормативное | `guides/deploy-project.md:46,49,56,77`; `guides/troubleshooting.md:60` | **Старое:** руководства учат `pip install mkdocs-material`, `mkdocs serve`, `mkdocs build --strict`, `mkdocs --version`. **Новое:** ADR-007 (`docs/adr/2026-07-adr-007-hub-root-structure.md:244-245`) — «Веб-стратегия Хаба отменена», `mkdocs.yml` removed; `tools/validate-repository-structure.sh:921` содержит `reject_path "mkdocs.yml"`, то есть возврат файла заблокирован CI. Руководство описывает процедуру, которую валидатор запрещает завершить. | **Обновить** или **удалить** mkdocs-разделы обоих руководств. Решение (полностью удалить публикацию или заменить на актуальный механизм) — за человеком. **Major** |
| G-07 | Нормативное | `standards/htom-documentation-structure.md:35`, `:62` (status `accepted`, v1.0, 2026-06-12) | **Старое:** ADR HTOM-команды именуются `docs/adr/NNNN-title.md` («monotonically increasing four-digit prefix», пример `0001-short-title.md`); стандарт также закрепляет соседей `prompts/`, `kb/`, `templates/` как рекомендуемую структуру. **Новое:** `standards/adr-structure-standard.md:46` требует `YYYY-MM-adr-NNN-short-title.md`; `templates/htom/AI_QUICK_RULES.md:34` и `templates/htom/README.md:151` прямо **запрещают** создавать `prompts/`, `experiments/`, `kb/`, `research/` «на вырост» (Anti-Inflation). Два `accepted`-документа дают взаимоисключающие указания. | **Обновить** `standards/htom-documentation-structure.md`: привести именование ADR к `adr-structure-standard.md` и снять рекомендацию каталогов, запрещённых геномом. Альтернатива — перевести стандарт в `superseded`. **Major** |
| G-08 | Терминологическое | `pr-ops/artifact-map.md:114,118,173,215,222,231,242,327,328,331,342` (11 строк колонки «Связи») | **Старое:** связи артефактов указывают на `AI_GOVERNANCE.md` как на существующий файл Хаба. **Новое:** файла в корне нет; его содержимое разошлось по `ai-governance/ai-governance.md` и `ai-rules/agent-work-rules.md` — что сама карта и фиксирует в строках 102-103 («Мигрирован из root `AI_GOVERNANCE.md` по B-056»). Карта одновременно утверждает, что файл мигрирован, и ссылается на него как на живой. Отдельно: `pr-ops/backlog.md:126` (B-056, статус DONE) утверждает «Ссылки, validator и artifact map синхронизированы» — это не соответствует фактам. | **Обновить**: заменить голые `AI_GOVERNANCE.md` на конкретный целевой файл в каждой из 11 строк; скорректировать формулировку итога B-056. Исключение — `pr-ops/artifact-map.md:189` (`standards/team-contract.md`), где речь о **project-level** `AI_GOVERNANCE.md` в чужом репозитории: это корректно и правки не требует. **Major** |
| G-09 | Нормативное | `standards/issue-workflow.md:154-169` vs фактическое состояние `pr-ops/artifact-map.md` | **Старое/действующее правило:** каждый новый или изменённый активный артефакт обязан быть зарегистрирован в `pr-ops/artifact-map.md`, `standards/README.md` и `README.md`. **Факт:** 62 из 313 отслеживаемых md-файлов не зарегистрированы, включая **все** `guides/*`, `docs/vision.md`, `docs/product-concept.md`, `docs/ecosystem-map.md`, `docs/project-summaries/*`, `ai-governance/README.md`, `ai-rules/README.md`, `pr-ops/README.md`, `projects-sink/*` (evidence: `research/hub/exp/hub-contradictions-audit-529/artifact-map-coverage.py`). При этом висящих путей в карте — 0. Норма существует, но не соблюдается и не проверяется. | **Обновить**: либо дорегистрировать 62 файла, либо явно сузить норму в `standards/issue-workflow.md` (например, исключить README-навигацию). Объём — отдельная задача бэклога, не микро-правка. **Minor** (нет функционального отказа, но норма фиктивна) |
| G-10 | Структурное | `docs/adr/2026-07-adr-007-hub-root-structure.md:167`, `:237`, `:241` | Артефакты автоматического переписывания ссылок при миграции: «Phase 2: перенести `docs/rfc/` в `docs/rfc/`» (строка 167), строка As-Is→To-Be «\| `docs/rfc/` \| `docs/rfc/` \|» (237) и «\| `docs/concept.md` \| `docs/concept.md` \|» (241). Исходные пути (`governance/rfc/`, корневой `concept.md`) затёрты, план миграции стал самореферентным и нечитаемым для будущего агента. | **Создать ADR** (не править на месте): `docs/adr/` защищён `tools/validate-historical-immutable.sh` — допустимы только новые записи или короткие `superseded`-заглушки. Новый ADR фиксирует фактические переносы Phase 2 и восстанавливает историческую трассируемость. **Minor** |
| G-11 | Терминологическое | `standards/executable-contract-standard.md:21`, `standards/contract-documentation-standard.md:21`, `standards/evals-contract-standard.md:26` | **Старое:** три стандарта ссылаются на норму как «(AI_GOVERNANCE, правило 4)». **Новое:** правило сохранилось — это пункт 4 раздела `## Политики` в `ai-governance/ai-governance.md` (canonical v2.2), — но цитируемого имени файла в репозитории больше нет, и порядковый номер теперь привязан к разделу, а не к документу. Ссылка нерезолвима для агента. | **Обновить** цитату на `ai-governance/ai-governance.md`, §«Политики», п. 4. Микро-правка ×3. **Minor** |
| G-12 | Структурное | `tools/validate-file-naming.sh` (покрывает только `research`, `docs/analysis`, `docs/report`, `docs/audit`, `docs/adr`) vs `standards/file-naming.md` | **Норма:** `standards/file-naming.md` задаёт правило «UPPERCASE в корне / lowercase во вложенных каталогах» и суффиксные соглашения. **Факт:** ни один валидатор это правило не проверяет; `is_exception` в `tools/validate-file-naming.sh` не знает суффикса `*-Summary.md` (при этом `docs/project-summaries/*-Summary.md` и `projects-sink/AI_PROJECT_CONTEXT-Summary.md` существуют и живут только за счёт того, что их каталоги вне `validate_tree`). `docs/rfc/` намеренно не валидируется на Хабе. Норма держится на дисциплине, а не на CI. | **Обновить** `tools/validate-file-naming.sh`: добавить `*-Summary.md` в `is_exception` и покрыть корневое/вложенное правило регистра. Расширение на `docs/rfc/` — решение человека (там исторические имена). **Minor** |

### Проверено и противоречий не найдено (явные no-op)

Фиксируется, чтобы следующий аудит не проверял это повторно:

| Проверка | Результат |
| --- | --- |
| Полнота реестра `standards/README.md` | Двусторонне полон: каждый файл `standards/*.md` в реестре, каждая строка реестра резолвится |
| Висящие пути в `pr-ops/artifact-map.md` | 0 (`research/hub/exp/hub-contradictions-audit-529/artifact-map-coverage.py`) |
| Два дома руководств: `guides/` vs `docs/guides/` | Не находка: отклонение уже отслеживается задачей **B-054** в `pr-ops/backlog.md` и явно оставлено открытым в ADR-007 |
| Отсутствие `kb/` и `runs/` (ядро ADR-001) | Не находка: документированное исключение архетипа A, зафиксировано в `docs/adr/2026-07-adr-007-hub-root-structure.md:243` и в `pr-ops/repo-model.md` |
| Относительные markdown-ссылки во всём корпусе | 18 из 19 нерезолвящихся — легитимные `{{hub_url}}`-плейсхолдеры шаблонов; единственная реальная поломка — G-03 |
| Прогон всех валидаторов Хаба и генома | Все проходят, exit 0 — то есть 12 находок выше **невидимы для CI** |

## Remediation / Deviation

**Порядок устранения (от корня к следствиям):**

1. **G-01 + G-02 вместе** — это одна проблема: геном требует того, чего Хаб не
   делает, и не может это проверить у споков. Требуется **новый RFC** с
   человеческим decision gate. Пока он не принят, отказы вида
   [mango PR #292](https://github.com/G-Ivan-A/mango_ba_prompts/pull/292)
   будут повторяться в каждой новой HTOM-команде.
2. **Микро-правки, не требующие решения человека** (можно одним PR):
   G-03, G-04, G-05, G-08, G-11 — устаревшие пути и имена файлов.
3. **Требуют решения человека:** G-06 (судьба mkdocs-разделов), G-07 (обновить
   или объявить `superseded`), G-09 (дорегистрировать 62 файла или сузить норму),
   G-12 (расширять ли валидацию на `docs/rfc/`).
4. **G-10** — только новым ADR.

**Deviation handling / ограничения аудита:**

- `docs/adr/` и `docs/rfc/` **иммутабельны** (`tools/validate-historical-immutable.sh`
  в `.github/workflows/validate.yml`): любой дефект в них исправляется **новой
  записью**, а не правкой на месте. Это прямо ограничивает G-10.
- Данный аудит **ничего не исправляет**: по `standards/audit-standard.md` аудит
  фиксирует расхождение и передаёт решение человеку. Исправления — предмет
  отдельных задач.
- Аудит не покрывает содержание внешних репозиториев: состояние mango
  оценивалось только по PR #292 как контекст триггера.

## Related Artifacts

- Issue: <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/529>
- Триггер: <https://github.com/G-Ivan-A/mango_ba_prompts/pull/292>
- Норма формата: `standards/audit-standard.md`
- Решение о структуре корня: `docs/adr/2026-07-adr-007-hub-root-structure.md`
- Реестры: `pr-ops/artifact-map.md`, `pr-ops/backlog.md` (B-047, B-048, B-054, B-056)
- Evidence-контейнер: `research/hub/exp/hub-contradictions-audit-529/` (`link-check.py`, `artifact-map-coverage.py` и логи прогонов)
