---
status: draft
version: 0.1
updated: 2026-06-06
ai-generated: true
type: rfc
context: [repository-quality, audit, cleanup, governance, traceability, archive]
method: repository-audit + validator-baseline + link-scan + duplicate-scan
scope: repo-wide
related_artifacts:
  - "governance/ARTIFACT_MAP.md"
  - "governance/BACKLOG.md"
  - "governance/REPO_MODEL.md"
  - "standards/file-naming.md"
  - "standards/research-profile.md"
  - "standards/research-documentation-standard.md"
  - "tools/validate-repository-structure.sh"
  - "tools/validate-frontmatter.sh"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/171"
---

# RFC: Repository Quality Improvement Plan

Версия: 0.1

Дата: 2026-06-06

Статус: черновик для согласования. Это RFC фиксирует аудит и план, а не
выполняет физическую очистку репозитория. Решение о применении фаз и создании
отдельных задач принимает человек.

## 1. Executive Summary

### 1.1. Контекст

После merge PR #170 репозиторий в целом приведён к новой структуре, но аудит
показывает несколько классов долга:

- naming-контракт и валидатор покрывают не все вложенные каталоги;
- часть документов дублирует `status` / `version` / `updated` из frontmatter в
  теле;
- карта артефактов и валидатор всё ещё делают архив Mango обязательным;
- после миграций остались stale-ссылки на удалённые `projects/mango/` и
  `*-old.md` пути;
- 52 документа имеют `status: draft` во frontmatter и требуют явного решения:
  согласовать, оставить как draft с exit-plan, объединить, удалить или вынести
  в отдельную задачу.

Концепция портала `open-ai.ru` не анализируется по смыслу: это отдельный scope.
В этом RFC учитываются только repository-quality факты, например битые ссылки в
файлах `research/portal/`.

### 1.2. Метод аудита

Проверки:

- `git ls-files` по всем tracked files;
- scan naming для `standards/`, `governance/rfc/`, `research/` и broader nested
  exceptions;
- exact duplicate scan по tracked text files;
- high-overlap scan по Markdown body без frontmatter;
- scan повторов metadata в body;
- scan локальных Markdown links и frontmatter relation fields;
- scan `status: draft` во frontmatter;
- baseline validators:
  - `./tools/validate-frontmatter.sh .`;
  - `./tools/validate-repository-structure.sh`.

Baseline validation до удаления PR-заглушки:

| Проверка | Результат | Комментарий |
| --- | --- | --- |
| `./tools/validate-frontmatter.sh .` | exit 0, 15 warnings | Warnings уже существуют: root/docs without frontmatter, template placeholders `{{date}}`, template issue body. |
| `./tools/validate-repository-structure.sh` | exit 1 | Единственный FAIL: tracked root `.gitkeep` из auto-generated PR placeholder. |

### 1.3. Приоритеты

| Направление | Вывод | Приоритет |
| --- | --- | --- |
| Именование | `standards/`, `governance/rfc/`, `research/` чистые; broader nested CAPS/underscore exceptions не согласованы явно. | P1 |
| Дубли | Exact duplicate content найден только в пустых `.gitkeep` архива; semantic overlap в основном ожидаемый (standard/template, research/standard), но нужен decision по research profile vs research documentation standard. | P1 |
| Metadata duplication | Повтор `version`/`updated`/`status` найден во многих standards/governance/research docs. | P1 |
| Трассировка | Есть реальные stale-ссылки и stale frontmatter relations после миграций. | P1 |
| Draft-документы | 52 draft frontmatter documents; часть draft является нормальной, часть требует human review или cleanup. | P2 |
| `archive/projects/mango/` | 17 tracked files, 4 `.gitkeep`; архив уже мигрировал во внешний spoke и должен быть удалён после согласования. | P1 |

## 2. Найденные Проблемы

### 2.1. Ошибки именования

Правило именования задано в [standards/file-naming.md](../../standards/file-naming.md):
корень репозитория допускает `UPPERCASE_WITH_HYPHENS.md`, вложенные каталоги
используют `lowercase-with-hyphens.md`; для `standards/` CAPS запрещён явно
(`standards/file-naming.md:20-30`).

| Scope | Результат | Приоритет | Рекомендация |
| --- | --- | --- | --- |
| `standards/` | Нарушений нет. Все `.md` кроме `README.md` используют kebab-case. | P0 закрыт | Ничего не менять. |
| `governance/rfc/` | Нарушений нет: все RFC используют kebab-case. | P0 закрыт | Ничего не менять. |
| `research/` | Нарушений lowercase/hyphen для tracked `.md`/`.html` нет. | P0 закрыт | Ничего не менять. |
| broader nested governance | `governance/AGENT_ONBOARDING.md`, `governance/ARTIFACT_MAP.md`, `governance/BACKLOG.md`, `governance/EXECUTABLE_DOCUMENTS_ISSUES.md`, `governance/REPO_MODEL.md` остаются CAPS style inside nested directory. | P1 | Human decision: либо переименовать в kebab-case, либо явно закрепить legacy/governance exception в `file-naming.md` и validator. |
| templates/spoke root-like files | `templates/spoke/AI_GOVERNANCE.md`, `AI_HANDOVER_PROMPT.md`, `AI_QUICK_RULES.md`, `CONTRIBUTING.md` выглядят как violations во вложенном каталоге, но при копировании в spoke становятся root files. | P2 | Зафиксировать template-root exception явно, чтобы scanner не считал это silent violation. |
| `archive/projects/mango/` | 8 файлов с `_` в имени (`*_exp`, `*_simple`, `user-story_gen...`, `usecase_gen...`). | P1 | Не переименовывать архив; удалить весь `archive/projects/mango/` после approval. |

Пробел валидатора: [tools/validate-repository-structure.sh](../../tools/validate-repository-structure.sh)
проверяет kebab-case только для `standards/` (`validate_standards_file_naming`,
строки 150-166). Для `governance/rfc/`, `research/` и broader nested paths
автоматической проверки пока нет.

### 2.2. Дублирующие и перекрывающиеся документы

Exact duplicates:

| Файлы | Тип | Приоритет | Рекомендация |
| --- | --- | --- | --- |
| `archive/projects/mango/decisions/.gitkeep`, `docs/.gitkeep`, `experiments/.gitkeep`, `kb/.gitkeep` | Пустые identical files | P1 | Удаляются вместе с archive. |

Semantic overlap:

| Пара | Наблюдение | Приоритет | Рекомендация |
| --- | --- | --- | --- |
| `standards/research-profile.md` + `standards/research-documentation-standard.md` | Не exact duplicate. `research-profile.md:45-84` задаёт артефакты, naming, frontmatter и воспроизводимость. `research-documentation-standard.md:35-43` явно говорит, что дополняет профиль и отвечает только за порядок body. | P1 | Human decision: оставить пару как `profile + body standard`, либо слить draft body-standard в `research-profile.md` и удалить отдельный draft. |
| `research/governance/*-format-2026-06.md` + `standards/*-standard.md` | Ожидаемая пара research -> standard. | P2 | Оставить, но добавить явное правило "research source не является duplicate standard". |
| `standards/webportal-concept-standard.md` + `templates/webportal-concept-template.md` | Ожидаемая пара standard -> copyable template. | P2 | Оставить; в template frontmatter решить placeholder-warning отдельно. |
| `AI_GOVERNANCE.md` + `templates/spoke/AI_GOVERNANCE.md` | Ожидаемая hub contract -> spoke template пара. | P2 | Оставить; relation должна быть описана как inheritance/template, не duplicate. |
| `research/hub/ai-collaboration-retrospective-2026-06.md` + `research/hub/ai-collaboration-retrospective-mango-migration-2026-06.md` | Высокое пересечение темы ретроспектив, но разные события. | P2 | При следующем изменении добавить cross-link "общая ретроспектива / Mango migration retrospective", не объединять автоматически. |

### 2.3. Дублирование метаданных

Паттерн: frontmatter содержит `status`, `version`, `updated`, а тело повторяет
`Версия:`, `Дата:` и иногда `Статус:`. Это повышает риск рассинхрона.

Standards с повтором metadata:

| Файл | Повтор в body | Приоритет |
| --- | --- | --- |
| `standards/contract-documentation-standard.md` | `19: Версия`, `21: Дата`, `23: Статус` | P1 |
| `standards/education-profile.md` | `10: Версия`, `12: Дата` | P1 |
| `standards/executable-contract-standard.md` | `19: Версия`, `21: Дата`, `23: Статус` | P1 |
| `standards/file-naming.md` | `10: Версия`, `12: Дата` | P1 |
| `standards/glossary.md` | `10: Версия`, `12: Дата` | P1 |
| `standards/issue-workflow.md` | `11: Версия`, `13: Дата` | P1 |
| `standards/portal-repository-structure.md` | `18: Версия`, `20: Дата`, `22: Статус` | P1 |
| `standards/product-profile.md` | `10: Версия`, `12: Дата` | P1 |
| `standards/research-documentation-standard.md` | `19: Версия`, `21: Дата`, `23: Статус` | P1 |
| `standards/research-profile.md` | `10: Версия`, `12: Дата` | P1 |
| `standards/team-contract.md` | `10: Версия`, `12: Дата` | P1 |
| `standards/webportal-concept-standard.md` | `26: Версия`, `28: Дата`, `30: Статус` | P1 |

`standards/project-structure-inheritance.md` уже не дублирует body metadata и
может служить эталоном минимального формата.

Broader repeated metadata exists in root, governance, project, research and
archive docs; phase 2 should remove it by class, not random one-off edits.

### 2.4. Нарушения трассировки

Confirmed broken or stale local references:

| Файл | Строка | Проблема | Приоритет | Рекомендация |
| --- | --- | --- | --- | --- |
| `projects/repo-development/docs/contract-violations-self-report-2026-06.md` | 105 | Link points to deleted `../../../docs/analysis/contract-executability-rfc.md`. | P1 | Replace with `../../../governance/rfc/contract-executability-rfc.md`. |
| `research/mango/taxonomy-concept-2026-05.md` | 43-45 | Links point to deleted `classification-old.md`, `classification-tz-old.md`, `requirements-flow-old.md`. | P1 | Replace with active `classification.md`, `classification-tz.md`, `requirements-flow.md` or mark as historical source without link. |
| `governance/rfc/rfc-creative-template-design.md` | 12 | Frontmatter points to `research/project-context-and-bootstrap-patterns-2026-05.md`; actual file is under `research/hub/`. | P1 | Replace with `research/hub/project-context-and-bootstrap-patterns-2026-05.md`. |
| `research/mango/capability-decomposition-2026-05.md` | 11-12 | `related_artifacts` includes `classification.md v3.0` and `classification-glossary.md`; one value mixes path and version, the other does not resolve locally. | P1 | Use path-only relation values; move version into prose if needed. |
| `research/portal/ai-and-mango-integration-patterns-2026-06.md` | 13, 168 | References deleted `projects/mango/README.md`. | P1, portal-deferred | Decide whether to point to `archive/projects/mango/README.md` or external `mango_ba_prompts`; do not alter portal concept semantics here. |
| `research/portal/repository-structure-design-2026-06.md` | 157 | References deleted `projects/mango/README.md`. | P1, portal-deferred | Same decision as above. |

Artifact map and validator inconsistencies:

| Файл | Строки | Проблема | Приоритет |
| --- | --- | --- | --- |
| `governance/ARTIFACT_MAP.md` | 128 | Related artifacts include deleted `projects/mango/README.md`. | P1 |
| `governance/ARTIFACT_MAP.md` | 136-149, 175 | Archive Mango is documented as present and mostly mandatory. | P1 |
| `tools/validate-repository-structure.sh` | 187-192, 244-260 | Archive Mango directories and files are required by validation. | P1 |
| `README.md` | 58 | Root README points reviewers to archive copy. | P1 |
| `projects/README.md` | 65 | Project index says archive copy exists. | P1 |
| `governance/ARTIFACT_MAP.md` | none for `projects/education-ba-prompt/*` | `README.md` and validator know this project, but artifact map has no row for `projects/education-ba-prompt/README.md` or `docs/course-ideas.md`. | P2 |

Scanner false positives excluded from the problem list:

- example links in standards (`2026-05-topic.md`, `module-01/`, `lesson-01.md`);
- template placeholders such as `{{hub_url}}`;
- external shorthand references to `mango_ba_prompts` when used as prose, not
  Markdown local links.

### 2.5. Draft-документы

Frontmatter scan found 52 draft documents:

| Группа | Count | Recommendation |
| --- | ---: | --- |
| `archive/` | 11 | Delete with `archive/projects/mango/`. |
| `governance/` | 5 | Keep as RFC until human decision; each needs accept/reject/update status. |
| `projects/` | 2 | Keep draft sandbox or promote to reviewed after education-scope decision. |
| `research/` | 22 | Review by domain; classify as `reviewed`, keep `draft` with exit-plan, or supersede. |
| `standards/` | 5 | Human approval required; accepted standards become `reviewed`/`canonical`, rejected/merged drafts are removed. |
| `templates/` | 7 | Decide whether template placeholder frontmatter should remain draft or be exempted from strict date validation. |

Full draft list:

| Файл | Линия | Рекомендация |
| --- | ---: | --- |
| `archive/projects/mango/experiments/prompts-audit-2026-05-26.md` | 2 | Delete with archive. |
| `archive/projects/mango/experiments/prompts-selftest-2026-05-26.md` | 2 | Delete with archive. |
| `archive/projects/mango/experiments/usecase_gen-stepwise-alignment_2026-05-26.md` | 2 | Delete with archive. |
| `archive/projects/mango/experiments/user-story_gen-from-raw-request_2026-05-26.md` | 2 | Delete with archive. |
| `archive/projects/mango/prompts/tz-stats-generator_exp-2026-05.md` | 2 | Delete with archive. |
| `archive/projects/mango/prompts/tz-stats-generator_simple-2026-05.md` | 2 | Delete with archive. |
| `archive/projects/mango/prompts/usecase-stepwise-generator_exp-2026-05.md` | 2 | Delete with archive. |
| `archive/projects/mango/prompts/usecase-stepwise-generator_simple-2026-05.md` | 2 | Delete with archive. |
| `archive/projects/mango/prompts/user-story-generator_exp-2026-05.md` | 2 | Delete with archive. |
| `archive/projects/mango/prompts/user-story-generator_simple-2026-05.md` | 2 | Delete with archive. |
| `archive/projects/mango/standards/classification-glossary.md` | 2 | Delete with archive. |
| `governance/rfc/README.md` | 2 | Keep draft navigation unless human promotes RFC catalog policy. |
| `governance/rfc/contract-executability-rfc.md` | 2 | Decide if accepted parts should become canonical standard/backlog only. |
| `governance/rfc/rfc-agent-onboarding-protocol.md` | 2 | Review against implemented `AGENT_ONBOARDING.md`; possibly supersede. |
| `governance/rfc/rfc-creative-template-design.md` | 2 | Review against implemented `templates/spoke/`. |
| `governance/rfc/rfc-two-cases-of-project-initialization.md` | 2 | Decide whether to keep as RFC-mанифест or promote term decisions elsewhere. |
| `projects/education-ba-prompt/README.md` | 2 | Keep sandbox draft or promote after education scope review. |
| `projects/education-ba-prompt/docs/course-ideas.md` | 2 | Keep sandbox draft or split into course artifacts after approval. |
| `research/governance/README.md` | 2 | Review navigation status. |
| `research/governance/contract-documentation-format-2026-06.md` | 2 | Review with derived standard. |
| `research/governance/executable-contract-format-2026-06.md` | 2 | Review with derived standard. |
| `research/governance/governance-folder-structure-decisions-2026-06.md` | 2 | Review and mark decisions as reviewed/canonical if accepted. |
| `research/governance/research-documentation-format-2026-06.md` | 2 | Review with derived standard. |
| `research/hub/external-governance-patterns-review-2026-06.md` | 2 | Review or keep draft with open questions. |
| `research/hub/project-context-and-bootstrap-patterns-2026-05.md` | 2 | Review after Mango archive deletion decision. |
| `research/hub/prompts-classification-audit-2026-05.md` | 2 | Review against external `mango_ba_prompts` state. |
| `research/hub/prompts-classification-standard-2026-05.md` | 2 | Merge into a standard or keep as draft research. |
| `research/hub/team-c-governance-strategy-audit-2026-05.md` | 2 | Review or supersede by backlog/external-governance analysis. |
| `research/hub/user-prompts-analysis-2026-05.md` | 2 | Review against prompt migration state. |
| `research/mango/capability-decomposition-2026-05.md` | 2 | Fix relations, then review. |
| `research/mango/rag-mapping-roadmap-2026-05.md` | 2 | Review after external Mango repo decision. |
| `research/mango/requirements-lifecycle-uncertainty-2026-05.md` | 2 | Review or keep draft with exit criteria. |
| `research/mango/taxonomy-concept-2026-05.md` | 2 | Fix stale links, then review. |
| `research/portal/README.md` | 2 | Portal-specific review outside this RFC. |
| `research/portal/ai-and-mango-integration-patterns-2026-06.md` | 2 | Portal-specific review outside this RFC; fix stale links separately. |
| `research/portal/architecture-and-stack-comparison-2026-06.md` | 2 | Portal-specific review outside this RFC. |
| `research/portal/concept-standards-comparison-2026-06.md` | 2 | Portal-specific review outside this RFC. |
| `research/portal/documentation-standards-comparison-2026-06.md` | 2 | Portal-specific review outside this RFC. |
| `research/portal/open-ai-portal-concept-rfc.md` | 2 | Out of scope for this cleanup; separate portal discussion. |
| `research/portal/repository-structure-design-2026-06.md` | 2 | Portal-specific review outside this RFC; fix stale links separately. |
| `standards/contract-documentation-standard.md` | 2 | Approve, merge, or reject. |
| `standards/executable-contract-standard.md` | 2 | Approve, merge, or reject. |
| `standards/portal-repository-structure.md` | 2 | Portal-specific approval. |
| `standards/research-documentation-standard.md` | 2 | Decide relation to `research-profile.md`. |
| `standards/webportal-concept-standard.md` | 2 | Portal-specific approval. |
| `templates/spoke/AI_GOVERNANCE.md` | 2 | Keep draft template; decide placeholder validation rule. |
| `templates/spoke/AI_HANDOVER_PROMPT.md` | 2 | Keep draft template; decide placeholder validation rule. |
| `templates/spoke/AI_QUICK_RULES.md` | 2 | Keep draft template; decide placeholder validation rule. |
| `templates/spoke/CHANGELOG.md` | 2 | Keep draft template; decide placeholder validation rule. |
| `templates/spoke/CONTRIBUTING.md` | 2 | Keep draft template; decide placeholder validation rule. |
| `templates/spoke/README.md` | 2 | Keep draft template; decide placeholder validation rule. |
| `templates/webportal-concept-template.md` | 2 | Keep draft template; decide placeholder validation rule. |

### 2.6. Устаревшие и ненужные файлы

| Artifact | Evidence | Recommendation | Priority |
| --- | --- | --- | --- |
| `archive/projects/mango/` | 17 tracked files, 4 `.gitkeep`; `projects/README.md:63-65` says Mango migrated to `mango_ba_prompts`. | Delete after approval; update references, map and validator in same PR. | P1 |
| Archive `.gitkeep` placeholders | `archive/projects/mango/decisions`, `docs`, `kb` contain only `.gitkeep`; `experiments/.gitkeep` duplicates empty content. | Delete with archive. | P1 |
| Root PR placeholder `.gitkeep` | Auto-generated branch placeholder; structure validator rejects it as unknown tracked file. | Remove in this PR because it is not part of repo state and blocks validation. | Done in this PR |
| `projects/education-ba-prompt/*` missing from `ARTIFACT_MAP.md` | Validator and README include it, map does not. | Add rows or decide it is non-public sandbox and remove from README/validator. | P2 |
| Frontmatter `source: *-old.md` fields | `education/README.md`, `frameworks/README.md`, `projects/README.md`, `research/README.md`, `research/mango/*.md` reference historical paths that no longer exist. | Decide whether historical source references are allowed as non-resolving provenance, or replace with PR/history references. | P2 |

### 2.7. `archive/projects/mango/`

Recommendation: approve full deletion of `archive/projects/mango/`.

Reasoning:

- Mango working assets moved to `https://github.com/G-Ivan-A/mango_ba_prompts`;
- git history preserves the old files;
- current archive creates stale local paths (`projects/mango/...`) and placeholder
  directories;
- validator and artifact map now treat the archive as required, which conflicts
  with the issue decision to remove it;
- keeping both archive and external spoke blurs source of truth.

Deletion is not a standalone `rm -rf`: it must update at least
`README.md`, `projects/README.md`, `governance/ARTIFACT_MAP.md`,
`tools/validate-repository-structure.sh`, and affected research/frontmatter links.

## 3. План Исправлений

### Phase 1: P0/P1, critical consistency

1. Remove `archive/projects/mango/` and update all active references.
2. Resolve naming-contract inconsistency:
   - either rename nested governance CAPS files to kebab-case;
   - or add explicit legacy/governance/template exceptions to `file-naming.md`
     and validator.
3. Fix confirmed stale links and frontmatter relations listed in section 2.4.
4. Decide `research-profile.md` vs `research-documentation-standard.md`:
   keep as complementary documents or merge body-order rules into one canonical
   profile.

### Phase 2: P1, validation and metadata

5. Remove body-level duplication of `Версия`, `Дата`, `Статус` where the same
   data is already in frontmatter.
6. Update `governance/ARTIFACT_MAP.md` to reflect actual state, including the
   education project decision.
7. Strengthen validators:
   - nested naming check beyond `standards/`;
   - local link check with allowlist for examples/placeholders;
   - relation-field path check;
   - metadata duplication check;
   - archive absence check after deletion.

### Phase 3: P2, draft lifecycle and cleanup

8. Triage all draft documents by class: approve, keep draft with exit-plan,
   supersede, merge, or delete.
9. Add a small "draft exit-plan" rule to standards for new draft documents.
10. Convert frontmatter warnings into either a documented allowlist or actionable
    failures, especially for template placeholders.
11. Remove empty/placeholder directories that are not part of a documented
    template.

## 4. Порядок Выполнения

| Step | Что сделать | Файлы | Зависимости | Риски | Rollback |
| --- | --- | --- | --- | --- | --- |
| 1 | Approve this RFC and choose archive decision. | This RFC, issue #171 | Human approval | Without decision, cleanup tasks should not start. | Keep RFC draft. |
| 2 | Delete `archive/projects/mango/` and update archive references. | `archive/projects/mango/**`, `README.md`, `projects/README.md`, `governance/ARTIFACT_MAP.md`, `tools/validate-repository-structure.sh`, selected research docs | Step 1 | Broken references if partial. | Revert deletion commit or restore from git history. |
| 3 | Fix stale links and relation values. | Files in section 2.4 | Step 1 | Portal links require scope discipline. | Revert link-only commit. |
| 4 | Resolve naming exception strategy. | `standards/file-naming.md`, validator, possibly renamed governance/template files | Step 1 | Renames touch many links. | Use `git mv` and revert if validation fails. |
| 5 | Decide research-profile split. | `standards/research-profile.md`, `standards/research-documentation-standard.md`, `standards/README.md`, map/validator | Step 1 | Removing a draft too early may lose useful body-order standard. | Keep both until explicit approval. |
| 6 | Remove metadata duplication by class. | `standards/**`, then governance/research batches | Steps 2-5 | Review churn across many docs. | Batch commits by directory. |
| 7 | Add validator improvements. | `tools/validate-repository-structure.sh`, possibly `tools/validate-frontmatter.sh` | Steps 2-6 | False positives for examples/templates. | Add explicit allowlist and fixture examples. |
| 8 | Triage drafts. | All files in section 2.5 | Steps 2-7 | Human review capacity. | Keep status draft with exit-plan. |

## 5. Предотвращение Повторов

### 5.1. Validation

Add checks to `tools/validate-repository-structure.sh`:

- `validate_nested_file_naming`: enforce lowercase hyphen names for nested docs,
  with explicit exceptions for root-like template files if approved.
- `validate_markdown_links`: resolve local Markdown links and frontmatter
  relation paths; ignore documented examples and `{{placeholder}}` URLs.
- `validate_metadata_single_source`: warn/fail when `Версия`, `Дата`, `Статус`
  duplicate frontmatter fields in the body.
- `validate_artifact_map_paths`: ensure local paths in `ARTIFACT_MAP.md` exist
  and required files are represented or intentionally excluded.
- `validate_no_archive_mango`: after approval, fail if
  `archive/projects/mango/` reappears.

### 5.2. Contracts

Update contracts after approval:

- `standards/file-naming.md`: add explicit section for governance legacy files
  and template-root files, or require renames.
- `standards/research-profile.md`: clarify relation to
  `research-documentation-standard.md`.
- `standards/contract-documentation-standard.md` and related standards: state
  that metadata lives in frontmatter; body may contain status prose only when it
  adds decision context not already represented by a field.
- Add rule: every new `status: draft` document must contain one of:
  `approval_target`, `supersedes`, `merge_candidate`, or a short "Exit plan"
  section in body.
- Add rule: do not create duplicate documents; update or extend existing
  standard unless the new document has a different responsibility.

### 5.3. CI/CD

Add GitHub Actions after validator improvements:

- run `./tools/validate-frontmatter.sh .`;
- run `./tools/validate-repository-structure.sh`;
- upload validator logs on failure;
- fail PRs on unknown tracked files, broken local links, stale archive paths,
  and forbidden naming patterns.

## 6. Запрос На Согласование

Questions for Founder & PO:

1. Approve this phased plan?
2. Approve Phase 1 execution first, before metadata and draft lifecycle cleanup?
3. Approve full deletion of `archive/projects/mango/`?
4. For nested CAPS governance files, choose one:
   - rename to kebab-case;
   - keep as explicit legacy exception;
   - defer decision.
5. For `research-profile.md` and `research-documentation-standard.md`, choose one:
   - keep as complementary profile + body standard;
   - merge into one canonical profile;
   - defer until standards review.
6. May I create the follow-up issues listed below after approval?

## 7. Задачи Для Создания После Согласования

No follow-up GitHub issues were created by this PR because the issue explicitly
requires approval of the RFC before physical fixes and task decomposition.

| Proposed issue title | Priority | Scope |
| --- | --- | --- |
| `cleanup: remove archive/projects/mango and stale archive references` | P1 | Delete archive, update README/projects/map/validator/research refs. |
| `fix: resolve nested governance file naming exceptions` | P1 | Rename or codify exceptions for uppercase governance/template files. |
| `fix: repair stale local links and frontmatter relations` | P1 | Section 2.4 link and relation issues. |
| `fix: decide research profile vs research documentation standard` | P1 | Keep complementary docs or merge. |
| `fix: remove metadata duplication from standards` | P1 | Remove body `Версия`/`Дата`/duplicate `Статус` from standards. |
| `fix: update artifact map coverage for education project` | P2 | Add rows or remove public registration. |
| `chore: strengthen repository structure validation` | P2 | Naming, link, relation, metadata, archive checks. |
| `governance: triage draft documents and add draft exit-plan rule` | P2 | Review 52 draft documents by class. |

## 8. Definition Of Done For This RFC

- Audit covers naming, duplicates, metadata duplication, traceability, draft
  statuses, obsolete files and Mango archive.
- Each finding has priority and recommendation.
- Phase 1-3 plan exists with order, dependencies, risks and rollback.
- Prevention plan covers validation, contracts and CI/CD.
- Approval questions are explicit.
- Local validators are run in the PR and results are reported.
