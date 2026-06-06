#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

failures=0

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  failures=$((failures + 1))
}

require_dir() {
  local path="$1"
  [[ -d "$path" ]] || fail "missing directory: $path"
}

require_file() {
  local path="$1"
  [[ -f "$path" ]] || fail "missing file: $path"
}

require_text() {
  local path="$1"
  local text="$2"
  if [[ -f "$path" ]] && ! grep -Fq "$text" "$path"; then
    fail "$path must contain: $text"
  fi
}

is_active_file() {
  case "$1" in
    README.md | \
    CONCEPT.md | \
    CONTRIBUTING.md | \
    AI_GOVERNANCE.md | \
    CHANGELOG.md | \
    LICENSE | \
    standards/README.md | \
    standards/file-naming.md | \
    standards/research-profile.md | \
    standards/glossary.md | \
    standards/education-profile.md | \
    standards/product-profile.md | \
    standards/team-contract.md | \
    standards/issue-workflow.md | \
    standards/project-structure-inheritance.md | \
    standards/portal-repository-structure.md | \
    standards/executable-contract-standard.md | \
    standards/contract-documentation-standard.md | \
    standards/webportal-concept-standard.md | \
    research/mango/taxonomy-concept-2026-05.md | \
    research/mango/requirements-lifecycle-uncertainty-2026-05.md | \
    research/mango/rag-mapping-roadmap-2026-05.md | \
    research/mango/capability-decomposition-2026-05.md | \
    research/hub/project-context-and-bootstrap-patterns-2026-05.md | \
    research/hub/ai-collaboration-retrospective-2026-06.md | \
    research/hub/ai-collaboration-retrospective-mango-migration-2026-06.md | \
    research/hub/prompts-classification-audit-2026-05.md | \
    research/hub/prompts-classification-standard-2026-05.md | \
    research/hub/team-c-governance-strategy-audit-2026-05.md | \
    research/hub/external-governance-patterns-review-2026-06.md | \
    research/hub/user-prompts-analysis-2026-05.md | \
    research/README.md | \
    research/hub/README.md | \
    research/mango/README.md | \
    research/governance/README.md | \
    research/governance/research-documentation-format-2026-06.md | \
    research/governance/executable-contract-format-2026-06.md | \
    research/governance/contract-documentation-format-2026-06.md | \
    research/governance/governance-folder-structure-decisions-2026-06.md | \
    research/portal/README.md | \
    research/portal/documentation-standards-comparison-2026-06.md | \
    research/portal/concept-standards-comparison-2026-06.md | \
    research/portal/architecture-and-stack-comparison-2026-06.md | \
    research/portal/repository-structure-design-2026-06.md | \
    research/portal/ai-and-mango-integration-patterns-2026-06.md | \
    research/portal/open-ai-portal-concept-rfc.md | \
    research/mango/classification.md | \
    research/mango/classification.html | \
    research/mango/classification-tz.md | \
    research/mango/classification-tz.html | \
    research/mango/requirements-flow.md | \
    research/mango/requirements-flow.html | \
    frameworks/README.md | \
    education/README.md | \
    projects/README.md | \
    projects/education-ba-prompt/README.md | \
    projects/education-ba-prompt/docs/course-ideas.md | \
    projects/repo-development/README.md | \
    projects/repo-development/docs/migration-audit-2026-05.md | \
    projects/repo-development/docs/contract-violations-self-report-2026-06.md | \
    governance/agent-onboarding.md | \
    governance/repo-model.md | \
    governance/artifact-map.md | \
    governance/backlog.md | \
    governance/executable-documents-issues.md | \
    governance/rfc/README.md | \
    governance/rfc/rfc-creative-template-design.md | \
    governance/rfc/rfc-agent-onboarding-protocol.md | \
    governance/rfc/rfc-two-cases-of-project-initialization.md | \
    governance/rfc/contract-executability-rfc.md | \
    governance/rfc/repository-quality-improvement-plan.md | \
    governance/rfc/draft-triage-and-exit-plan.md | \
    .github/ISSUE_TEMPLATE/task.yml | \
    templates/spoke/AI_GOVERNANCE.md | \
    templates/spoke/AI_QUICK_RULES.md | \
    templates/spoke/AI_HANDOVER_PROMPT.md | \
    templates/spoke/README.md | \
    templates/spoke/CONTRIBUTING.md | \
    templates/spoke/CHANGELOG.md | \
    templates/spoke/docs/adr/.gitkeep | \
    templates/spoke/docs/audit/.gitkeep | \
    templates/spoke/.github/ISSUE_TEMPLATE/task.md | \
    templates/spoke/tools/validate-repository-structure.sh | \
    templates/spoke/init.sh | \
    templates/webportal-concept-template.md | \
    tools/validate-frontmatter.sh | \
    tools/validate-repository-structure.sh)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

is_old_file() {
  local name="${1##*/}"
  [[ "$name" == *-old || "$name" == *-old.* ]]
}

validate_kebab_case_file_naming() {
  local dir="$1"
  local file
  local basename

  while IFS= read -r file; do
    basename="${file##*/}"

    case "$basename" in
      README.md | LICENSE | CHANGELOG.md)
        continue
        ;;
    esac

    if [[ ! "$basename" =~ ^[a-z0-9]+(-[a-z0-9]+)*\.md$ ]]; then
      fail "$dir file must use kebab-case: $file"
    fi
  done < <(find "$dir" -maxdepth 1 -type f)
}

validate_metadata_not_duplicated() {
  local file

  while IFS= read -r file; do
    if awk '
      NR == 1 {
        if ($0 != "---") {
          exit 1
        }
        next
      }

      !frontmatter_done {
        if ($0 == "---") {
          frontmatter_done = 1
          next
        }
        if ($0 ~ /^(status|version|updated):[[:space:]]*/) {
          has_metadata = 1
        }
        next
      }

      frontmatter_done {
        if (!has_metadata) {
          exit 1
        }
        body_lines += 1
        if (body_lines > 20) {
          exit 1
        }
        if ($0 ~ /^[[:space:]]*(Версия|Дата|Статус|Version|Date|Status):/) {
          found_duplicate = 1
          exit 0
        }
      }

      END {
        if (found_duplicate) {
          exit 0
        }
        exit 1
      }
    ' "$file"; then
      fail "Metadata duplicated in body of $file. Keep it only in frontmatter."
    fi
  done < <(find standards governance -type f -name '*.md' | sort)
}

validate_internal_markdown_links() {
  local file
  local link_target
  local target_without_anchor
  local target_path
  local file_dir

  while IFS= read -r file; do
    file_dir="$(dirname "$file")"

    while IFS= read -r link_target; do
      case "$link_target" in
        http://* | https://* | mailto:* | tel:* | ftp://* | "#"* )
          continue
          ;;
      esac

      if [[ "$link_target" == *"{{"* || "$link_target" == *"}}"* ]]; then
        continue
      fi

      target_without_anchor="${link_target%%#*}"
      target_without_anchor="${target_without_anchor%%\?*}"

      if [[ -z "$target_without_anchor" || "$target_without_anchor" != *.md ]]; then
        continue
      fi

      if [[ "$target_without_anchor" == /* ]]; then
        target_path=".${target_without_anchor}"
      else
        target_path="$file_dir/$target_without_anchor"
      fi

      if [[ ! -f "$target_path" ]]; then
        fail "Broken link in $file -> $link_target"
      fi
    done < <(perl -ne 'while (/\[[^\]]+\]\(([^)\s]+)(?:\s+"[^"]*")?\)/g) { print "$1\n" }' "$file")
  done < <(find . -path ./.git -prune -o -type f -name '*.md' -print | sed 's#^\./##' | sort)
}

validate_artifact_map_paths() {
  local artifact_path
  local target_path
  declare -A seen_paths=()

  while IFS= read -r artifact_path; do
    if [[ -n "${seen_paths[$artifact_path]:-}" ]]; then
      fail "Duplicate artifact-map path: $artifact_path"
      continue
    fi
    seen_paths["$artifact_path"]=1

    case "$artifact_path" in
      http://* | https://* )
        continue
        ;;
    esac

    target_path=".$artifact_path"
    if [[ ! -e "$target_path" ]]; then
      fail "Broken artifact-map path: $artifact_path"
    fi
  done < <(
    awk -F'|' '
      /^## Карта артефактов/ {
        in_map = 1
        next
      }
      /^## Исторические/ {
        in_map = 0
      }
      in_map && /^\| `/ {
        path = $2
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", path)
        gsub(/`/, "", path)
        print path
      }
    ' governance/artifact-map.md
  )
}

required_directories=(
  ".github/ISSUE_TEMPLATE"
  "templates"
  "templates/spoke"
  "templates/spoke/docs/adr"
  "templates/spoke/docs/audit"
  "templates/spoke/.github/ISSUE_TEMPLATE"
  "templates/spoke/tools"
  "standards"
  "research"
  "research/hub"
  "research/mango"
  "research/governance"
  "research/portal"
  "frameworks"
  "projects"
  "education"
  "governance"
  "governance/rfc"
  "tools"
)

required_files=(
  "README.md"
  "CONCEPT.md"
  "CONTRIBUTING.md"
  "AI_GOVERNANCE.md"
  "CHANGELOG.md"
  "LICENSE"
  "standards/README.md"
  "standards/file-naming.md"
  "standards/research-profile.md"
  "standards/glossary.md"
  "standards/education-profile.md"
  "standards/product-profile.md"
  "standards/team-contract.md"
  "standards/issue-workflow.md"
  "standards/project-structure-inheritance.md"
  "standards/portal-repository-structure.md"
  "standards/executable-contract-standard.md"
  "standards/contract-documentation-standard.md"
  "standards/webportal-concept-standard.md"
  "research/README.md"
  "research/hub/README.md"
  "research/mango/README.md"
  "research/governance/README.md"
  "research/governance/research-documentation-format-2026-06.md"
  "research/governance/executable-contract-format-2026-06.md"
  "research/governance/contract-documentation-format-2026-06.md"
  "research/governance/governance-folder-structure-decisions-2026-06.md"
  "research/portal/README.md"
  "research/portal/documentation-standards-comparison-2026-06.md"
  "research/portal/concept-standards-comparison-2026-06.md"
  "research/portal/architecture-and-stack-comparison-2026-06.md"
  "research/portal/repository-structure-design-2026-06.md"
  "research/portal/open-ai-portal-concept-rfc.md"
  "research/mango/classification.md"
  "research/mango/classification.html"
  "research/mango/classification-tz.md"
  "research/mango/classification-tz.html"
  "research/mango/requirements-flow.md"
  "research/mango/requirements-flow.html"
  "research/mango/rag-mapping-roadmap-2026-05.md"
  "frameworks/README.md"
  "education/README.md"
  "projects/README.md"
  "projects/repo-development/README.md"
  "projects/repo-development/docs/migration-audit-2026-05.md"
  "projects/repo-development/docs/contract-violations-self-report-2026-06.md"
  "governance/agent-onboarding.md"
  "governance/repo-model.md"
  "governance/artifact-map.md"
  "governance/backlog.md"
  "governance/executable-documents-issues.md"
  "governance/rfc/README.md"
  "governance/rfc/rfc-creative-template-design.md"
  "governance/rfc/rfc-agent-onboarding-protocol.md"
  "governance/rfc/rfc-two-cases-of-project-initialization.md"
  "governance/rfc/contract-executability-rfc.md"
  "governance/rfc/repository-quality-improvement-plan.md"
  "governance/rfc/draft-triage-and-exit-plan.md"
  "projects/education-ba-prompt/README.md"
  "projects/education-ba-prompt/docs/course-ideas.md"
  ".github/ISSUE_TEMPLATE/task.yml"
  "templates/spoke/AI_GOVERNANCE.md"
  "templates/spoke/AI_QUICK_RULES.md"
  "templates/spoke/AI_HANDOVER_PROMPT.md"
  "templates/spoke/README.md"
  "templates/spoke/CONTRIBUTING.md"
  "templates/spoke/CHANGELOG.md"
  "templates/spoke/docs/adr/.gitkeep"
  "templates/spoke/docs/audit/.gitkeep"
  "templates/spoke/.github/ISSUE_TEMPLATE/task.md"
  "templates/spoke/tools/validate-repository-structure.sh"
  "templates/spoke/init.sh"
  "templates/webportal-concept-template.md"
  "tools/validate-frontmatter.sh"
  "tools/validate-repository-structure.sh"
)

for dir in "${required_directories[@]}"; do
  require_dir "$dir"
done

for file in "${required_files[@]}"; do
  require_file "$file"
done

for kebab_case_dir in standards governance; do
  validate_kebab_case_file_naming "$kebab_case_dir"
done

validate_metadata_not_duplicated
validate_internal_markdown_links
validate_artifact_map_paths

while IFS= read -r file; do
  if [[ ! -e "$file" ]]; then
    continue
  fi

  if is_active_file "$file"; then
    continue
  fi

  if is_old_file "$file"; then
    fail "tracked legacy -old file after migration cleanup: $file"
    continue
  fi

  fail "tracked legacy file without -old suffix: $file"
done < <(git ls-files)

require_text "README.md" "CONCEPT.md"
require_text "README.md" "standards/README.md"
require_text "README.md" "standards/glossary.md"
require_text "README.md" "standards/team-contract.md"
require_text "README.md" "governance/agent-onboarding.md"
require_text "README.md" "governance/repo-model.md"
require_text "README.md" "governance/artifact-map.md"
require_text "README.md" "projects/education-ba-prompt/README.md"
require_text "README.md" "research/mango/README.md"
require_text "README.md" "./tools/validate-frontmatter.sh"
require_text "README.md" "./tools/validate-repository-structure.sh"
require_text "README.md" "Человек задаёт смысл, AI ускоряет путь — вместе по правилам"

require_text "CONCEPT.md" "governance/repo-model.md"
require_text "CONCEPT.md" "standards/README.md"
require_text "CONCEPT.md" "Anti-Inflation"
require_text "CONCEPT.md" "status: canonical"
require_text "CONCEPT.md" "version: 1.0"
require_text "CONCEPT.md" "updated: 2026-05-26"
require_text "CONCEPT.md" "ai-generated: false"
require_text "CONCEPT.md" "Версия: 1.0"
require_text "CONCEPT.md" "Operating Mode"
require_text "CONCEPT.md" "structured mode"
require_text "CONCEPT.md" "creative mode"
require_text "CONCEPT.md" "standards/team-contract.md"
require_text "CONCEPT.md" "Шаблон командного соглашения"
require_text "CONCEPT.md" "glossary.md"
require_text "CONCEPT.md" "единой терминологии"

require_text "CONTRIBUTING.md" "AI_GOVERNANCE.md"
require_text "CONTRIBUTING.md" "standards/README.md"
require_text "CONTRIBUTING.md" "./tools/validate-frontmatter.sh"
require_text "CONTRIBUTING.md" "./tools/validate-repository-structure.sh"

require_text "AI_GOVERNANCE.md" "status: canonical"
require_text "AI_GOVERNANCE.md" "version: 1.2"
require_text "AI_GOVERNANCE.md" "updated: 2026-06-06"
require_text "AI_GOVERNANCE.md" "ai-generated: false"
require_text "AI_GOVERNANCE.md" "executable: false"
require_text "AI_GOVERNANCE.md" "Версия: 1.2"
require_text "AI_GOVERNANCE.md" "Дата: 2026-06-06"
require_text "AI_GOVERNANCE.md" "Директива pre-flight"
require_text "AI_GOVERNANCE.md" "Founder & PO"
require_text "AI_GOVERNANCE.md" "Human reviewer"
require_text "AI_GOVERNANCE.md" "standards/README.md"
require_text "AI_GOVERNANCE.md" "governance/agent-onboarding.md"
require_text "AI_GOVERNANCE.md" "Человек задаёт смысл, AI ускоряет путь — вместе по правилам"

require_text "CHANGELOG.md" "## Unreleased"
require_text "CHANGELOG.md" "## [1.1] - 2026-05-26"
require_text "CHANGELOG.md" "### Added"
require_text "CHANGELOG.md" "### Changed"
require_text "CHANGELOG.md" "### Removed"

require_text "standards/README.md" "| Стандарт | Статус | Где применяется | Источник |"
require_text "standards/README.md" "Как пользоваться"
require_text "standards/README.md" "file-naming.md"
require_text "standards/README.md" "research-profile.md"
require_text "standards/README.md" "team-contract.md"
require_text "standards/README.md" "standards/glossary.md"
require_text "standards/README.md" "standards/education-profile.md"
require_text "standards/README.md" "product-profile.md"
require_text "standards/README.md" "project-structure-inheritance.md"
require_text "standards/README.md" "artifact-map.md"
require_text "standards/README.md" "issue-workflow.md"

require_text "standards/team-contract.md" "status: canonical"
require_text "standards/team-contract.md" "version: 1.0"
require_text "standards/team-contract.md" "updated: 2026-05-26"
require_text "standards/team-contract.md" "ai-generated: false"
require_text "standards/team-contract.md" "Назначение"
require_text "standards/team-contract.md" "не является контрактом для прямого использования"
require_text "standards/team-contract.md" "CONTRIBUTING.md"
require_text "standards/team-contract.md" "AI_GOVERNANCE.md"
require_text "standards/team-contract.md" "Definition of Done"
require_text "standards/team-contract.md" "operating modes"
require_text "standards/team-contract.md" "disclosure"
require_text "standards/team-contract.md" "self-review checklist"
require_text "standards/team-contract.md" "research-profile.md"
require_text "standards/team-contract.md" "product-profile.md"
require_text "standards/team-contract.md" "education-profile.md"
require_text "standards/team-contract.md" "Источники"

require_text "standards/issue-workflow.md" "status: canonical"
require_text "standards/issue-workflow.md" "version: 1.1"
require_text "standards/issue-workflow.md" "updated: 2026-06-04"
require_text "standards/issue-workflow.md" "ai-generated: false"
require_text "standards/issue-workflow.md" "executable: false"
require_text "standards/issue-workflow.md" "## Назначение"
require_text "standards/issue-workflow.md" "## Статусы задач"
require_text "standards/issue-workflow.md" "## Правила переходов"
require_text "standards/issue-workflow.md" "## Связи между артефактами"
require_text "standards/issue-workflow.md" "## Точки автоматизации"
require_text "standards/issue-workflow.md" "## Источники и адаптация"
require_text "standards/issue-workflow.md" '`draft`'
require_text "standards/issue-workflow.md" '`ready`'
require_text "standards/issue-workflow.md" '`in-progress`'
require_text "standards/issue-workflow.md" '`review`'
require_text "standards/issue-workflow.md" '`merged`'
require_text "standards/issue-workflow.md" '`closed`'
require_text "standards/issue-workflow.md" '`blocked`'

require_text "standards/project-structure-inheritance.md" "status: canonical"
require_text "standards/project-structure-inheritance.md" "version: 1.1"
require_text "standards/project-structure-inheritance.md" "updated: 2026-06-04"
require_text "standards/project-structure-inheritance.md" "ai-generated: false"
require_text "standards/project-structure-inheritance.md" "executable: false"
require_text "standards/project-structure-inheritance.md" "Разрешённые подкаталоги"
require_text "standards/project-structure-inheritance.md" "Правила связывания стандартов"
require_text "standards/project-structure-inheritance.md" "scope: mango-only"
require_text "standards/project-structure-inheritance.md" "Пример структуры проекта"
require_text "standards/project-structure-inheritance.md" "Репозиторий-широкий стандарт НЕ должен ссылаться на проектный"
require_text "standards/issue-workflow.md" "User Story / ФТ"
require_text "standards/issue-workflow.md" "CHANGELOG.md"
require_text "standards/issue-workflow.md" "governance/artifact-map.md"
require_text "standards/issue-workflow.md" "validate-frontmatter.sh"
require_text "standards/issue-workflow.md" "validate-repository-structure.sh"
require_text "standards/file-naming.md" "status: canonical"
require_text "standards/file-naming.md" "version: 1.2"
require_text "standards/file-naming.md" "updated: 2026-06-06"
require_text "standards/file-naming.md" "ai-generated: false"
require_text "standards/file-naming.md" "Корень репозитория"
require_text "standards/file-naming.md" "UPPERCASE_WITH_HYPHENS.md"
require_text "standards/file-naming.md" "Вложенные каталоги"
require_text "standards/file-naming.md" "lowercase-with-hyphens.md"
require_text "standards/file-naming.md" "Правила именования файлов в standards/ и governance/"
require_text "standards/file-naming.md" '`CAPS_LOCK` запрещён'
require_text "standards/file-naming.md" "classification-glossary.md"
require_text "standards/file-naming.md" "agent-onboarding.md"
require_text "standards/file-naming.md" "Исключения"
require_text "standards/file-naming.md" "Новый файл не соответствует правилу"

require_text "standards/research-profile.md" "status: canonical"
require_text "standards/research-profile.md" "version: 1.0"
require_text "standards/research-profile.md" "updated: 2026-05-26"
require_text "standards/research-profile.md" "ai-generated: false"
require_text "standards/research-profile.md" "Назначение"
require_text "standards/research-profile.md" "Обязательные артефакты"
require_text "standards/research-profile.md" "YYYY-MM-topic.md"
require_text "standards/research-profile.md" "exp-<slug>"
require_text "standards/research-profile.md" "Шаблон frontmatter исследования"
require_text "standards/research-profile.md" "external-analysis | internal-analysis | experiment"
require_text "standards/research-profile.md" "Как организовать исследование"
require_text "standards/research-profile.md" "Порядок изложения"
require_text "standards/research-profile.md" "Введение → Результаты → Детализация"
require_text "standards/research-profile.md" "Чек-лист готовности к публикации"
require_text "standards/research-profile.md" "Правила цитирования источников"
require_text "standards/research-profile.md" "FAIR Principles"

require_text "standards/glossary.md" "status: canonical"
require_text "standards/glossary.md" "version: 1.2"
require_text "standards/glossary.md" "updated: 2026-06-04"
require_text "standards/glossary.md" "ai-generated: false"
require_text "standards/glossary.md" "Standard"
require_text "standards/glossary.md" "Concept"
require_text "standards/glossary.md" "Policy"
require_text "standards/glossary.md" "Contract"
require_text "standards/glossary.md" "Practice"
require_text "standards/glossary.md" "Framework"
require_text "standards/glossary.md" "Guideline"
require_text "standards/glossary.md" "Artifact"
require_text "standards/glossary.md" "Canonical"
require_text "standards/glossary.md" "Draft"
require_text "standards/glossary.md" "Operating Mode"
require_text "standards/glossary.md" "Profile"
require_text "standards/glossary.md" "Исполнимый документ"
require_text "standards/glossary.md" "Директивный блок"
require_text "standards/glossary.md" "Как использовать"
require_text "standards/glossary.md" "Связи терминов"
require_text "standards/glossary.md" "Источники"

require_text "standards/education-profile.md" "status: canonical"
require_text "standards/education-profile.md" "version: 1.0"
require_text "standards/education-profile.md" "updated: 2026-05-26"
require_text "standards/education-profile.md" "ai-generated: false"
require_text "standards/education-profile.md" "## Назначение"
require_text "standards/education-profile.md" "product-profile.md"
require_text "standards/education-profile.md" "research-profile.md"
require_text "standards/education-profile.md" "| Артефакт | Назначение | Где размещать | Пример/Шаблон |"
require_text "standards/education-profile.md" "CONCEPT.md"
require_text "standards/education-profile.md" "module-XX/"
require_text "standards/education-profile.md" "lesson-01.md"
require_text "standards/education-profile.md" "exercise-01.md"
require_text "standards/education-profile.md" "solution.md"
require_text "standards/education-profile.md" "## Стандарт именования"
require_text "standards/education-profile.md" "## Шаблон структуры модуля"
require_text "standards/education-profile.md" "## Как адаптировать под формат обучения"
require_text "standards/education-profile.md" "Открытый курс"
require_text "standards/education-profile.md" "Коммерческий продукт"
require_text "standards/education-profile.md" "Внутреннее обучение"
require_text "standards/education-profile.md" "## Гибридный формат: чат-бот и LMS"
require_text "standards/education-profile.md" "## Источники и адаптация"
require_text "standards/education-profile.md" "Carnegie Mellon University Eberly Center"
require_text "standards/education-profile.md" "CAST Universal Design for Learning"
require_text "standards/education-profile.md" "UNESCO Open Educational Resources"
require_text "standards/education-profile.md" "1EdTech Common Cartridge"
require_text "standards/education-profile.md" "ADL Experience API"
require_text "standards/product-profile.md" "status: canonical"
require_text "standards/product-profile.md" "ai-generated: false"
require_text "standards/product-profile.md" "PRODUCT_VISION.md"
require_text "standards/product-profile.md" "Обязательные артефакты"
require_text "standards/product-profile.md" "Метрики успеха"

require_text "governance/repo-model.md" "Артефакт только при операционной боли"
require_text "governance/repo-model.md" "Anti-Inflation"
require_text "governance/repo-model.md" "tools/"
require_text "governance/repo-model.md" "status: canonical"
require_text "governance/repo-model.md" "version: 1.1"
require_text "governance/repo-model.md" "updated: 2026-06-04"
require_text "governance/repo-model.md" "ai-generated: false"
require_text "governance/repo-model.md" "executable: false"
require_text "governance/repo-model.md" "Decision Rules — исполнимая часть справочного документа"

require_text "governance/rfc/rfc-creative-template-design.md" "status: draft"
require_text "governance/rfc/rfc-creative-template-design.md" "ai-generated: true"
require_text "governance/rfc/rfc-creative-template-design.md" "Концептуальная аналогия"
require_text "governance/rfc/rfc-creative-template-design.md" "Сравнительная матрица"
require_text "governance/rfc/rfc-creative-template-design.md" "templates/spoke/"
require_text "governance/rfc/rfc-creative-template-design.md" "AI_GOVERNANCE.md"
require_text "governance/rfc/rfc-creative-template-design.md" "Антипаттерны"
require_text "governance/rfc/rfc-creative-template-design.md" "А что, если"
require_text "governance/rfc/rfc-creative-template-design.md" '```mermaid'
require_text "governance/rfc/rfc-creative-template-design.md" "Решение за человеком"

require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "status: draft"
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "ai-generated: true"
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "Концептуальная аналогия"
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "Обоснование"
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "Handover Prompt"
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "ai-collaboration-retrospective-2026-06.md"
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "agent-onboarding.md"
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" '```mermaid'
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "Решение за человеком"
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "Модель процесса"
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "rfc-two-cases-of-project-initialization.md"
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "{{REPO_NAME}}"

require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "status: canonical"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "ai-generated: true"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "Концептуальная аналогия"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "Таблица-манифест"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "Runtime-онбординг"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "Bootstrap-клонирование"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "standards/glossary.md"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "ai-collaboration-retrospective-2026-06.md"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "rfc-agent-onboarding-protocol.md"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "rfc-creative-template-design.md"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" '```mermaid'
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "Follow-up"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "Решение за человеком"

require_text "governance/rfc/contract-executability-rfc.md" "status: draft"
require_text "governance/rfc/contract-executability-rfc.md" "version: 1.1"
require_text "governance/rfc/contract-executability-rfc.md" "Решения фаундера по RFC"
require_text "governance/rfc/contract-executability-rfc.md" "executable: true|false"
require_text "governance/rfc/contract-executability-rfc.md" "governance/rfc/"
require_text "governance/rfc/contract-executability-rfc.md" "Дата утверждения"

require_text "governance/rfc/repository-quality-improvement-plan.md" "status: draft"
require_text "governance/rfc/repository-quality-improvement-plan.md" "version: 0.2"
require_text "governance/rfc/repository-quality-improvement-plan.md" "archive/projects/mango/"
require_text "governance/rfc/repository-quality-improvement-plan.md" "Phase 1"
require_text "governance/rfc/repository-quality-improvement-plan.md" "Запрос На Согласование"
require_text "governance/rfc/repository-quality-improvement-plan.md" "Задачи Для Создания После Согласования"

require_text "governance/rfc/draft-triage-and-exit-plan.md" "status: draft"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "version: 0.1"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "Template Placeholders"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "approval_target"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "estimated_effort"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "Questions To Founder And PO"

require_text "governance/agent-onboarding.md" "status: canonical"
require_text "governance/agent-onboarding.md" "version: 1.1"
require_text "governance/agent-onboarding.md" "updated: 2026-06-04"
require_text "governance/agent-onboarding.md" "executable: true"
require_text "governance/agent-onboarding.md" "entrypoint: true"
require_text "governance/agent-onboarding.md" "ИСПОЛНИМЫЙ ДОКУМЕНТ — НЕ АНАЛИЗИРУЙ, ВЫПОЛНЯЙ"
require_text "governance/agent-onboarding.md" "EXECUTION"
require_text "governance/agent-onboarding.md" "EXPLANATION"
require_text "governance/agent-onboarding.md" "Handover Prompt"
require_text "governance/agent-onboarding.md" "{{REPO_NAME}}"
require_text "governance/agent-onboarding.md" "Readback"
require_text "governance/agent-onboarding.md" "Что может пойти не так"
require_text "governance/agent-onboarding.md" "standards/glossary.md"
require_text "governance/agent-onboarding.md" "rfc-agent-onboarding-protocol.md"
require_text "governance/agent-onboarding.md" "rfc-two-cases-of-project-initialization.md"
require_text "governance/agent-onboarding.md" "templates/spoke/README.md"

require_text "governance/artifact-map.md" "status: canonical"
require_text "governance/artifact-map.md" "version: 1.21"
require_text "governance/artifact-map.md" "templates/spoke/AI_GOVERNANCE.md"
require_text "governance/artifact-map.md" "updated: 2026-06-06"
require_text "governance/artifact-map.md" "ai-generated: false"
require_text "governance/artifact-map.md" "governance/rfc/rfc-creative-template-design.md"
require_text "governance/artifact-map.md" "governance/rfc/contract-executability-rfc.md"
require_text "governance/artifact-map.md" "governance/rfc/repository-quality-improvement-plan.md"
require_text "governance/artifact-map.md" "governance/rfc/draft-triage-and-exit-plan.md"
require_text "governance/artifact-map.md" "| Путь | Тип | 🚦 Исполнимый? | Назначение | Обязательный? | Связанные артефакты |"
require_text "governance/artifact-map.md" "🚦 entrypoint"
require_text "governance/artifact-map.md" "standards/project-structure-inheritance.md"
require_text "governance/artifact-map.md" "Как использовать карту"
require_text "governance/artifact-map.md" "Как обновлять карту"
require_text "governance/artifact-map.md" "glossary.md"
require_text "governance/artifact-map.md" "research/mango/classification.md"
require_text "governance/artifact-map.md" "research/mango/rag-mapping-roadmap-2026-05.md"
require_text "governance/artifact-map.md" "research/hub/project-context-and-bootstrap-patterns-2026-05.md"
require_text "governance/artifact-map.md" "research/hub/team-c-governance-strategy-audit-2026-05.md"
require_text "governance/artifact-map.md" "research/hub/user-prompts-analysis-2026-05.md"
require_text "governance/artifact-map.md" "mango_ba_prompts"
require_text "governance/artifact-map.md" "projects/README.md"
require_text "governance/artifact-map.md" "governance/backlog.md"
require_text "governance/artifact-map.md" "governance/executable-documents-issues.md"

require_text "governance/backlog.md" "status: canonical"
require_text "governance/backlog.md" "type: backlog"
require_text "governance/backlog.md" "standards/glossary.md"
require_text "governance/backlog.md" "| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Обоснование приоритета |"
require_text "governance/backlog.md" "Бэклог: Внедрение стандарта исполнимых документов"
require_text "governance/backlog.md" "CE-001"
require_text "governance/backlog.md" "CE-010"

require_text "governance/executable-documents-issues.md" "status: canonical"
require_text "governance/executable-documents-issues.md" "type: registry"
require_text "governance/executable-documents-issues.md" "contract-executability-rfc.md"
require_text "governance/executable-documents-issues.md" "CE-001"
require_text "governance/executable-documents-issues.md" "CE-010"
require_text "governance/executable-documents-issues.md" "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/138"
require_text "governance/executable-documents-issues.md" "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/147"
require_text "governance/backlog.md" "North Star"
require_text "governance/backlog.md" "Триггеры для пересмотра бэклога"
require_text "governance/backlog.md" "Критический путь"
require_text "governance/backlog.md" '```mermaid'
require_text "governance/backlog.md" "Анализ рекомендаций команд С и Q"

require_text "research/README.md" "status: canonical"
require_text "research/README.md" "standards/research-profile.md"
require_text "research/README.md" "research/<domain>/exp-<slug>/"
require_text "research/README.md" "project-context-and-bootstrap-patterns-2026-05.md"
require_text "research/README.md" "prompts-classification-audit-2026-05.md"
require_text "research/README.md" "prompts-classification-standard-2026-05.md"
require_text "research/README.md" "team-c-governance-strategy-audit-2026-05.md"
require_text "research/README.md" "user-prompts-analysis-2026-05.md"
require_text "research/README.md" "Размещение файлов исследований в корне каталога"

# Namespacing: no research files allowed in the research/ root except README.md.
while IFS= read -r research_root_file; do
  base="${research_root_file##*/}"
  if [[ "$base" != "README.md" ]]; then
    fail "research root must only contain README.md; found: $research_root_file"
  fi
done < <(find research -maxdepth 1 -type f)

require_text "research/hub/README.md" "status: canonical"
require_text "research/hub/README.md" "project-context-and-bootstrap-patterns-2026-05.md"
require_text "research/hub/README.md" "prompts-classification-audit-2026-05.md"
require_text "research/hub/README.md" "prompts-classification-standard-2026-05.md"
require_text "research/hub/README.md" "team-c-governance-strategy-audit-2026-05.md"
require_text "research/hub/README.md" "user-prompts-analysis-2026-05.md"

require_text "research/mango/README.md" "status: canonical"
require_text "research/mango/README.md" "classification.md"
require_text "research/mango/README.md" "requirements-flow.md"
require_text "research/mango/README.md" "rag-mapping-roadmap-2026-05.md"
require_text "research/mango/README.md" "research/mango/exp-tz-corpus/"

require_text "research/mango/classification.md" "status: reviewed"
require_text "research/mango/classification.md" "source: research/mango/classification-old.md"
require_text "research/mango/classification-tz.md" "status: reviewed"
require_text "research/mango/classification-tz.md" "source: research/mango/classification-tz-old.md"
require_text "research/mango/requirements-flow.md" "status: reviewed"
require_text "research/mango/requirements-flow.md" "source: research/mango/requirements-flow-old.md"
require_text "research/mango/rag-mapping-roadmap-2026-05.md" "status: draft"
require_text "research/mango/rag-mapping-roadmap-2026-05.md" "type: process-research"
require_text "research/mango/rag-mapping-roadmap-2026-05.md" "Маппинг продуктов/фич"
require_text "research/mango/rag-mapping-roadmap-2026-05.md" "Roadmap реализации проекта"
require_text "research/mango/rag-mapping-roadmap-2026-05.md" "PlantUML"
require_text "research/mango/rag-mapping-roadmap-2026-05.md" "Вопросы для согласования"

require_text "research/hub/project-context-and-bootstrap-patterns-2026-05.md" "status: draft"
require_text "research/hub/project-context-and-bootstrap-patterns-2026-05.md" "type: internal-analysis"
require_text "research/hub/project-context-and-bootstrap-patterns-2026-05.md" "scope: repo-wide"
require_text "research/hub/project-context-and-bootstrap-patterns-2026-05.md" "Опыт проекта Mango"
require_text "research/hub/project-context-and-bootstrap-patterns-2026-05.md" "Проблемы (5 пунктов"
require_text "research/hub/project-context-and-bootstrap-patterns-2026-05.md" "Предложенные решения"
require_text "research/hub/project-context-and-bootstrap-patterns-2026-05.md" "Чек-лист для ИИ"
require_text "research/hub/project-context-and-bootstrap-patterns-2026-05.md" "Механизм «рекомендация → задача»"
require_text "research/hub/project-context-and-bootstrap-patterns-2026-05.md" "Вопросы для согласования"

require_text "research/hub/prompts-classification-audit-2026-05.md" "status: draft"
require_text "research/hub/prompts-classification-audit-2026-05.md" "type: internal-analysis"
require_text "research/hub/prompts-classification-audit-2026-05.md" "scope: repo-wide"
require_text "research/hub/prompts-classification-audit-2026-05.md" "Преобладающие типы"
require_text "research/hub/prompts-classification-audit-2026-05.md" "Паттерны отладки"
require_text "research/hub/prompts-classification-audit-2026-05.md" "Пробелы"
require_text "research/hub/prompts-classification-audit-2026-05.md" "Выводы для классификации"

require_text "research/hub/prompts-classification-standard-2026-05.md" "status: draft"
require_text "research/hub/prompts-classification-standard-2026-05.md" "type: classification-standard"
require_text "research/hub/prompts-classification-standard-2026-05.md" "scope: repo-wide"
require_text "research/hub/prompts-classification-standard-2026-05.md" "Таксономия промптов"
require_text "research/hub/prompts-classification-standard-2026-05.md" "Матрица"
require_text "research/hub/prompts-classification-standard-2026-05.md" "Когда использовать"
require_text "research/hub/prompts-classification-standard-2026-05.md" "Шаблоны промптов"
require_text "research/hub/prompts-classification-standard-2026-05.md" "План интеграции"
require_text "research/hub/prompts-classification-standard-2026-05.md" "Вопросы для согласования"

require_text "research/hub/team-c-governance-strategy-audit-2026-05.md" "status: draft"
require_text "research/hub/team-c-governance-strategy-audit-2026-05.md" "type: internal-analysis"
require_text "research/hub/team-c-governance-strategy-audit-2026-05.md" "scope: repo-wide"
require_text "research/hub/team-c-governance-strategy-audit-2026-05.md" "Интерпретация аудита стратегии governance"
require_text "research/hub/team-c-governance-strategy-audit-2026-05.md" "Governance overgrowth"
require_text "research/hub/team-c-governance-strategy-audit-2026-05.md" "Предложения команды C"
require_text "research/hub/team-c-governance-strategy-audit-2026-05.md" "Рекомендации для backlog"
require_text "research/hub/team-c-governance-strategy-audit-2026-05.md" "Вопросы для human review"

require_text "research/hub/external-governance-patterns-review-2026-06.md" "status: draft"
require_text "research/hub/external-governance-patterns-review-2026-06.md" "type: external-analysis"
require_text "research/hub/external-governance-patterns-review-2026-06.md" "scope: repo-wide"
require_text "research/hub/external-governance-patterns-review-2026-06.md" "Что ценного в рекомендациях Команды С"
require_text "research/hub/external-governance-patterns-review-2026-06.md" "Матрица применимости"
require_text "research/hub/external-governance-patterns-review-2026-06.md" "ВЗЯТЬ СЕЙЧАС"
require_text "research/hub/external-governance-patterns-review-2026-06.md" "ОТЛОЖИТЬ"
require_text "research/hub/external-governance-patterns-review-2026-06.md" "ОТКЛОНИТЬ"
require_text "research/hub/external-governance-patterns-review-2026-06.md" "North Star"
require_text "research/hub/external-governance-patterns-review-2026-06.md" "Триггеры для пересмотра матрицы"

require_text "research/hub/user-prompts-analysis-2026-05.md" "status: draft"
require_text "research/hub/user-prompts-analysis-2026-05.md" "type: prompt-analysis"
require_text "research/hub/user-prompts-analysis-2026-05.md" "scope: user-specific + repo-integration"
require_text "research/hub/user-prompts-analysis-2026-05.md" "Таблица классификации 18 промптов"
require_text "research/hub/user-prompts-analysis-2026-05.md" "Признаки устаревших паттернов"
require_text "research/hub/user-prompts-analysis-2026-05.md" "Дубли/уникальная ценность"
require_text "research/hub/user-prompts-analysis-2026-05.md" "Рекомендации по действиям"
require_text "research/hub/user-prompts-analysis-2026-05.md" "План интеграции"
require_text "research/hub/user-prompts-analysis-2026-05.md" "Вопросы для согласования"

require_text "research/mango/capability-decomposition-2026-05.md" "status: draft"
require_text "research/mango/capability-decomposition-2026-05.md" "type: atomic-functions-reference"
require_text "research/mango/capability-decomposition-2026-05.md" "scope: mango-only"
require_text "research/mango/capability-decomposition-2026-05.md" "Критерии атомарности"
require_text "research/mango/capability-decomposition-2026-05.md" "Связь с НФТ-классами"
require_text "research/mango/capability-decomposition-2026-05.md" "Интеграция с"
require_text "research/mango/capability-decomposition-2026-05.md" "Как обновлять справочник"
require_text "research/mango/capability-decomposition-2026-05.md" "Вопросы для согласования с PO/Founder"
require_text "research/mango/capability-decomposition-2026-05.md" "Domain: voice-ucaas"
require_text "research/mango/capability-decomposition-2026-05.md" "Domain: contact-center"
require_text "research/mango/capability-decomposition-2026-05.md" "Domain: digital-channels"

require_text "projects/README.md" "status: canonical"
require_text "projects/README.md" "Мигрировавшие проекты"
require_text "projects/README.md" "mango_ba_prompts"
require_text "projects/README.md" "repo-development/"

require_text "education/README.md" "status: canonical"
require_text "education/README.md" "standards/education-profile.md"

require_text "frameworks/README.md" "status: canonical"
require_text "frameworks/README.md" "governance/repo-model.md"

require_text "projects/education-ba-prompt/README.md" "status: draft"
require_text "projects/education-ba-prompt/README.md" "version: 0.1"
require_text "projects/education-ba-prompt/README.md" "updated: 2026-05-26"
require_text "projects/education-ba-prompt/README.md" "ai-generated: false"
require_text "projects/education-ba-prompt/README.md" "docs/course-ideas.md"
require_text "projects/education-ba-prompt/README.md" "standards/education-profile.md"

require_text "projects/education-ba-prompt/docs/course-ideas.md" "status: draft"
require_text "projects/education-ba-prompt/docs/course-ideas.md" "version: 0.1"
require_text "projects/education-ba-prompt/docs/course-ideas.md" "updated: 2026-05-26"
require_text "projects/education-ba-prompt/docs/course-ideas.md" "ai-generated: false"
require_text "projects/education-ba-prompt/docs/course-ideas.md" "## 🔹 Термины и концепции"
require_text "projects/education-ba-prompt/docs/course-ideas.md" "## 🔹 Практические кейсы БА"
require_text "projects/education-ba-prompt/docs/course-ideas.md" "## 🔹 Шаблоны промптов (рабочие)"
require_text "projects/education-ba-prompt/docs/course-ideas.md" "## 🔹 Идеи модулей курса"
require_text "projects/education-ba-prompt/docs/course-ideas.md" "## 🔹 Форматы подачи"
require_text "projects/education-ba-prompt/docs/course-ideas.md" "## 🔹 Вопросы для обсуждения"

require_text ".github/ISSUE_TEMPLATE/task.yml" "📋 Task Implementation"
require_text ".github/ISSUE_TEMPLATE/task.yml" "structured"
require_text ".github/ISSUE_TEMPLATE/task.yml" "creative"
require_text ".github/ISSUE_TEMPLATE/task.yml" "⚠️ **Для ИИ**"
require_text ".github/ISSUE_TEMPLATE/task.yml" "🎯 Контекст"
require_text ".github/ISSUE_TEMPLATE/task.yml" "📄 Артефакты для создания/изменения"
require_text ".github/ISSUE_TEMPLATE/task.yml" "✅ Готово, когда"

# Spoke "ДНК-шаблон" (templates/spoke/): минимальный геном для клонирования.
require_text "templates/spoke/AI_GOVERNANCE.md" "{{project_name}}"
require_text "templates/spoke/AI_GOVERNANCE.md" "Эскалация"
require_text "templates/spoke/AI_QUICK_RULES.md" "{{project_name}}"
require_text "templates/spoke/AI_QUICK_RULES.md" "Не создавай"
require_text "templates/spoke/AI_HANDOVER_PROMPT.md" "{{REPO_NAME}}"
require_text "templates/spoke/AI_HANDOVER_PROMPT.md" "governance/agent-onboarding.md"
require_text "templates/spoke/AI_HANDOVER_PROMPT.md" "version: 0.2"
require_text "templates/spoke/AI_HANDOVER_PROMPT.md" "executable: true"
require_text "templates/spoke/AI_HANDOVER_PROMPT.md" "ИСПОЛНИМЫЙ HANDOVER PROMPT — СКОПИРУЙ И ВЫПОЛНИ"
require_text "templates/spoke/AI_HANDOVER_PROMPT.md" "EXECUTION"
require_text "templates/spoke/AI_HANDOVER_PROMPT.md" "EXPLANATION"
require_text "templates/spoke/README.md" "AI_HANDOVER_PROMPT.md"
require_text "templates/spoke/README.md" "{{project_name}}"
require_text "templates/spoke/README.md" "governance/agent-onboarding.md"
require_text "templates/spoke/README.md" "Как валидировать структуру"
require_text "templates/spoke/README.md" "Человек задаёт смысл, AI ускоряет путь — вместе по правилам"
require_text "templates/spoke/CONTRIBUTING.md" "issue → PR → review"
require_text "templates/spoke/CHANGELOG.md" "## Unreleased"
require_text "templates/spoke/.github/ISSUE_TEMPLATE/task.md" "🎯 Контекст"
require_text "templates/spoke/.github/ISSUE_TEMPLATE/task.md" "✅ Готово, когда"
require_text "templates/spoke/tools/validate-repository-structure.sh" "AI_GOVERNANCE.md"

# Hard constraint: research/ must NOT be baked into the spoke template.
if [[ -e templates/spoke/research ]]; then
  fail "templates/spoke must not contain research/ (knowledge lives in the hub research/)"
fi

if [[ -e meta/README.md ]]; then
  fail "active meta/README.md should move to governance/"
fi

if [[ -e tests/validate-repository-structure.sh ]]; then
  fail "active tests/validate-repository-structure.sh should move to tools/"
fi

if [[ "$failures" -gt 0 ]]; then
  printf '\nRepository structure validation failed with %d issue(s).\n' "$failures" >&2
  exit 1
fi

printf 'Repository structure validation passed.\n'
