#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

failures=0

fail() {
  printf 'FAIL: %s\n' "$1" >&2
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
    standards/research-documentation-standard.md | \
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
    archive/projects/mango/README.md | \
    archive/projects/mango/experiments/user-story_gen-from-raw-request_2026-05-26.md | \
    archive/projects/mango/experiments/tz-stats-prototype-2026-05.md | \
    archive/projects/mango/experiments/usecase_gen-stepwise-alignment_2026-05-26.md | \
    archive/projects/mango/experiments/prompts-audit-2026-05-26.md | \
    archive/projects/mango/experiments/prompts-selftest-2026-05-26.md | \
    archive/projects/mango/prompts/tz-stats-generator_exp-2026-05.md | \
    archive/projects/mango/prompts/tz-stats-generator_simple-2026-05.md | \
    archive/projects/mango/prompts/user-story-generator_exp-2026-05.md | \
    archive/projects/mango/prompts/user-story-generator_simple-2026-05.md | \
    archive/projects/mango/prompts/usecase-stepwise-generator_exp-2026-05.md | \
    archive/projects/mango/prompts/usecase-stepwise-generator_simple-2026-05.md | \
    archive/projects/mango/standards/classification-glossary.md | \
    archive/projects/mango/kb/.gitkeep | \
    archive/projects/mango/docs/.gitkeep | \
    archive/projects/mango/experiments/.gitkeep | \
    archive/projects/mango/decisions/.gitkeep | \
    projects/education-ba-prompt/README.md | \
    projects/education-ba-prompt/docs/course-ideas.md | \
    projects/repo-development/README.md | \
    projects/repo-development/docs/migration-audit-2026-05.md | \
    projects/repo-development/docs/contract-violations-self-report-2026-06.md | \
    governance/AGENT_ONBOARDING.md | \
    governance/REPO_MODEL.md | \
    governance/ARTIFACT_MAP.md | \
    governance/BACKLOG.md | \
    governance/EXECUTABLE_DOCUMENTS_ISSUES.md | \
    governance/rfc/README.md | \
    governance/rfc/rfc-creative-template-design.md | \
    governance/rfc/rfc-agent-onboarding-protocol.md | \
    governance/rfc/rfc-two-cases-of-project-initialization.md | \
    governance/rfc/contract-executability-rfc.md | \
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

validate_standards_file_naming() {
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
      fail "standards file must use kebab-case: $file"
    fi
  done < <(find standards -maxdepth 1 -type f)
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
  "archive"
  "archive/projects"
  "archive/projects/mango/standards"
  "archive/projects/mango/kb"
  "archive/projects/mango/prompts"
  "archive/projects/mango/docs"
  "archive/projects/mango/experiments"
  "archive/projects/mango/decisions"
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
  "standards/research-documentation-standard.md"
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
  "archive/projects/mango/README.md"
  "archive/projects/mango/experiments/user-story_gen-from-raw-request_2026-05-26.md"
  "archive/projects/mango/experiments/tz-stats-prototype-2026-05.md"
  "archive/projects/mango/experiments/usecase_gen-stepwise-alignment_2026-05-26.md"
  "archive/projects/mango/experiments/prompts-audit-2026-05-26.md"
  "archive/projects/mango/experiments/prompts-selftest-2026-05-26.md"
  "archive/projects/mango/prompts/tz-stats-generator_exp-2026-05.md"
  "archive/projects/mango/prompts/tz-stats-generator_simple-2026-05.md"
  "archive/projects/mango/prompts/user-story-generator_exp-2026-05.md"
  "archive/projects/mango/prompts/user-story-generator_simple-2026-05.md"
  "archive/projects/mango/prompts/usecase-stepwise-generator_exp-2026-05.md"
  "archive/projects/mango/prompts/usecase-stepwise-generator_simple-2026-05.md"
  "archive/projects/mango/standards/classification-glossary.md"
  "archive/projects/mango/kb/.gitkeep"
  "archive/projects/mango/docs/.gitkeep"
  "archive/projects/mango/experiments/.gitkeep"
  "archive/projects/mango/decisions/.gitkeep"
  "projects/repo-development/README.md"
  "projects/repo-development/docs/migration-audit-2026-05.md"
  "projects/repo-development/docs/contract-violations-self-report-2026-06.md"
  "governance/AGENT_ONBOARDING.md"
  "governance/REPO_MODEL.md"
  "governance/ARTIFACT_MAP.md"
  "governance/BACKLOG.md"
  "governance/EXECUTABLE_DOCUMENTS_ISSUES.md"
  "governance/rfc/README.md"
  "governance/rfc/rfc-creative-template-design.md"
  "governance/rfc/rfc-agent-onboarding-protocol.md"
  "governance/rfc/rfc-two-cases-of-project-initialization.md"
  "governance/rfc/contract-executability-rfc.md"
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

validate_standards_file_naming

while IFS= read -r file; do
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
require_text "README.md" "governance/AGENT_ONBOARDING.md"
require_text "README.md" "governance/REPO_MODEL.md"
require_text "README.md" "governance/ARTIFACT_MAP.md"
require_text "README.md" "projects/education-ba-prompt/README.md"
require_text "README.md" "research/mango/README.md"
require_text "README.md" "./tools/validate-frontmatter.sh"
require_text "README.md" "./tools/validate-repository-structure.sh"
require_text "README.md" "Человек задаёт смысл, AI ускоряет путь — вместе по правилам"

require_text "CONCEPT.md" "governance/REPO_MODEL.md"
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
require_text "AI_GOVERNANCE.md" "governance/AGENT_ONBOARDING.md"
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
require_text "standards/README.md" "ARTIFACT_MAP.md"
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
require_text "standards/issue-workflow.md" "Версия: 1.1"
require_text "standards/issue-workflow.md" "Дата: 2026-06-04"
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
require_text "standards/issue-workflow.md" "governance/ARTIFACT_MAP.md"
require_text "standards/issue-workflow.md" "validate-frontmatter.sh"
require_text "standards/issue-workflow.md" "validate-repository-structure.sh"
require_text "standards/file-naming.md" "status: canonical"
require_text "standards/file-naming.md" "version: 1.1"
require_text "standards/file-naming.md" "updated: 2026-06-06"
require_text "standards/file-naming.md" "ai-generated: false"
require_text "standards/file-naming.md" "Корень репозитория"
require_text "standards/file-naming.md" "UPPERCASE_WITH_HYPHENS.md"
require_text "standards/file-naming.md" "Вложенные каталоги"
require_text "standards/file-naming.md" "lowercase-with-hyphens.md"
require_text "standards/file-naming.md" "Правила именования файлов в standards/"
require_text "standards/file-naming.md" '`CAPS_LOCK` запрещён'
require_text "standards/file-naming.md" "classification-glossary.md"
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

require_text "governance/REPO_MODEL.md" "Артефакт только при операционной боли"
require_text "governance/REPO_MODEL.md" "Anti-Inflation"
require_text "governance/REPO_MODEL.md" "tools/"
require_text "governance/REPO_MODEL.md" "status: canonical"
require_text "governance/REPO_MODEL.md" "version: 1.1"
require_text "governance/REPO_MODEL.md" "updated: 2026-06-04"
require_text "governance/REPO_MODEL.md" "ai-generated: false"
require_text "governance/REPO_MODEL.md" "executable: false"
require_text "governance/REPO_MODEL.md" "Версия: 1.1"
require_text "governance/REPO_MODEL.md" "Дата: 2026-06-04"
require_text "governance/REPO_MODEL.md" "Decision Rules — исполнимая часть справочного документа"

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
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "AGENT_ONBOARDING.md"
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" '```mermaid'
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "Решение за человеком"
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "Модель процесса"
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "rfc-two-cases-of-project-initialization.md"
require_text "governance/rfc/rfc-agent-onboarding-protocol.md" "{{REPO_NAME}}"

require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "status: draft"
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

require_text "governance/AGENT_ONBOARDING.md" "status: canonical"
require_text "governance/AGENT_ONBOARDING.md" "version: 1.1"
require_text "governance/AGENT_ONBOARDING.md" "updated: 2026-06-04"
require_text "governance/AGENT_ONBOARDING.md" "executable: true"
require_text "governance/AGENT_ONBOARDING.md" "entrypoint: true"
require_text "governance/AGENT_ONBOARDING.md" "ИСПОЛНИМЫЙ ДОКУМЕНТ — НЕ АНАЛИЗИРУЙ, ВЫПОЛНЯЙ"
require_text "governance/AGENT_ONBOARDING.md" "EXECUTION"
require_text "governance/AGENT_ONBOARDING.md" "EXPLANATION"
require_text "governance/AGENT_ONBOARDING.md" "Handover Prompt"
require_text "governance/AGENT_ONBOARDING.md" "{{REPO_NAME}}"
require_text "governance/AGENT_ONBOARDING.md" "Readback"
require_text "governance/AGENT_ONBOARDING.md" "Что может пойти не так"
require_text "governance/AGENT_ONBOARDING.md" "standards/glossary.md"
require_text "governance/AGENT_ONBOARDING.md" "rfc-agent-onboarding-protocol.md"
require_text "governance/AGENT_ONBOARDING.md" "rfc-two-cases-of-project-initialization.md"
require_text "governance/AGENT_ONBOARDING.md" "templates/spoke/README.md"

require_text "governance/ARTIFACT_MAP.md" "status: canonical"
require_text "governance/ARTIFACT_MAP.md" "version: 1.18"
require_text "governance/ARTIFACT_MAP.md" "templates/spoke/AI_GOVERNANCE.md"
require_text "governance/ARTIFACT_MAP.md" "updated: 2026-06-06"
require_text "governance/ARTIFACT_MAP.md" "ai-generated: false"
require_text "governance/ARTIFACT_MAP.md" "governance/rfc/rfc-creative-template-design.md"
require_text "governance/ARTIFACT_MAP.md" "governance/rfc/contract-executability-rfc.md"
require_text "governance/ARTIFACT_MAP.md" "| Путь | Тип | 🚦 Исполнимый? | Назначение | Обязательный? | Связанные артефакты |"
require_text "governance/ARTIFACT_MAP.md" "🚦 entrypoint"
require_text "governance/ARTIFACT_MAP.md" "standards/project-structure-inheritance.md"
require_text "governance/ARTIFACT_MAP.md" "Как использовать карту"
require_text "governance/ARTIFACT_MAP.md" "Как обновлять карту"
require_text "governance/ARTIFACT_MAP.md" "glossary.md"
require_text "governance/ARTIFACT_MAP.md" "research/mango/classification.md"
require_text "governance/ARTIFACT_MAP.md" "research/mango/rag-mapping-roadmap-2026-05.md"
require_text "governance/ARTIFACT_MAP.md" "research/hub/project-context-and-bootstrap-patterns-2026-05.md"
require_text "governance/ARTIFACT_MAP.md" "research/hub/team-c-governance-strategy-audit-2026-05.md"
require_text "governance/ARTIFACT_MAP.md" "research/hub/user-prompts-analysis-2026-05.md"
require_text "governance/ARTIFACT_MAP.md" "mango_ba_prompts"
require_text "governance/ARTIFACT_MAP.md" "archive/projects/mango/"
require_text "governance/ARTIFACT_MAP.md" "projects/README.md"
require_text "governance/ARTIFACT_MAP.md" "governance/BACKLOG.md"
require_text "governance/ARTIFACT_MAP.md" "governance/EXECUTABLE_DOCUMENTS_ISSUES.md"

require_text "governance/BACKLOG.md" "status: canonical"
require_text "governance/BACKLOG.md" "type: backlog"
require_text "governance/BACKLOG.md" "standards/glossary.md"
require_text "governance/BACKLOG.md" "| ID | Название | Приоритет | Зависимости | Статус | Issue | Источник | Обоснование приоритета |"
require_text "governance/BACKLOG.md" "Бэклог: Внедрение стандарта исполнимых документов"
require_text "governance/BACKLOG.md" "CE-001"
require_text "governance/BACKLOG.md" "CE-010"

require_text "governance/EXECUTABLE_DOCUMENTS_ISSUES.md" "status: canonical"
require_text "governance/EXECUTABLE_DOCUMENTS_ISSUES.md" "type: registry"
require_text "governance/EXECUTABLE_DOCUMENTS_ISSUES.md" "contract-executability-rfc.md"
require_text "governance/EXECUTABLE_DOCUMENTS_ISSUES.md" "CE-001"
require_text "governance/EXECUTABLE_DOCUMENTS_ISSUES.md" "CE-010"
require_text "governance/EXECUTABLE_DOCUMENTS_ISSUES.md" "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/138"
require_text "governance/EXECUTABLE_DOCUMENTS_ISSUES.md" "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/147"
require_text "governance/BACKLOG.md" "North Star"
require_text "governance/BACKLOG.md" "Триггеры для пересмотра бэклога"
require_text "governance/BACKLOG.md" "Критический путь"
require_text "governance/BACKLOG.md" '```mermaid'
require_text "governance/BACKLOG.md" "Анализ рекомендаций команд С и Q"

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
require_text "projects/README.md" "archive/projects/mango/"
require_text "projects/README.md" "repo-development/"

require_text "archive/projects/mango/README.md" "research/mango/README.md"
require_text "archive/projects/mango/README.md" "standards/classification-glossary.md"
require_text "archive/projects/mango/README.md" 'Все исследования Mango используют термины из `standards/classification-glossary.md`'

prompt_file_count="$(find archive/projects/mango/prompts -maxdepth 1 -type f | wc -l | tr -d '[:space:]')"
if [[ "$prompt_file_count" != "6" ]]; then
  fail "archive/projects/mango/prompts must contain exactly 6 files, found $prompt_file_count"
fi

prompt_files=(
  "archive/projects/mango/prompts/tz-stats-generator_exp-2026-05.md"
  "archive/projects/mango/prompts/tz-stats-generator_simple-2026-05.md"
  "archive/projects/mango/prompts/user-story-generator_exp-2026-05.md"
  "archive/projects/mango/prompts/user-story-generator_simple-2026-05.md"
  "archive/projects/mango/prompts/usecase-stepwise-generator_exp-2026-05.md"
  "archive/projects/mango/prompts/usecase-stepwise-generator_simple-2026-05.md"
)

for prompt_file in "${prompt_files[@]}"; do
  require_text "$prompt_file" "type:"
  require_text "$prompt_file" "variant:"
  require_text "$prompt_file" "scope: mango-only"
  require_text "$prompt_file" "based_on:"
  require_text "$prompt_file" "# РОЛЬ"
  require_text "$prompt_file" "# КАК РАБОТАЕМ"
  require_text "$prompt_file" "# ПРАВИЛА"
  require_text "$prompt_file" "# НАЧНЕМ?"
done

require_text "archive/projects/mango/prompts/tz-stats-generator_exp-2026-05.md" "variant: exp"
require_text "archive/projects/mango/prompts/user-story-generator_exp-2026-05.md" "variant: exp"
require_text "archive/projects/mango/prompts/usecase-stepwise-generator_exp-2026-05.md" "variant: exp"
require_text "archive/projects/mango/prompts/tz-stats-generator_simple-2026-05.md" "variant: simple"
require_text "archive/projects/mango/prompts/user-story-generator_simple-2026-05.md" "variant: simple"
require_text "archive/projects/mango/prompts/usecase-stepwise-generator_simple-2026-05.md" "variant: simple"

require_text "archive/projects/mango/experiments/prompts-audit-2026-05-26.md" "type: prompt-audit"
require_text "archive/projects/mango/experiments/prompts-audit-2026-05-26.md" "Что работает"
require_text "archive/projects/mango/experiments/prompts-audit-2026-05-26.md" 'Упрощения для `_simple`'
require_text "archive/projects/mango/experiments/prompts-audit-2026-05-26.md" 'Критичные ссылки для `_exp`'

require_text "archive/projects/mango/experiments/prompts-selftest-2026-05-26.md" "type: prompt-selftest"
require_text "archive/projects/mango/experiments/prompts-selftest-2026-05-26.md" "Результаты self-test"
require_text "archive/projects/mango/experiments/prompts-selftest-2026-05-26.md" "Идеи на будущее"
require_text "archive/projects/mango/experiments/prompts-selftest-2026-05-26.md" "Вопросы для согласования"

require_text "archive/projects/mango/standards/classification-glossary.md" "status: draft"
require_text "archive/projects/mango/standards/classification-glossary.md" "version: 0.1"
require_text "archive/projects/mango/standards/classification-glossary.md" "updated: 2026-05-26"
require_text "archive/projects/mango/standards/classification-glossary.md" "ai-generated: false"
require_text "archive/projects/mango/standards/classification-glossary.md" "scope: mango-only"
require_text "archive/projects/mango/standards/classification-glossary.md" "Domain (Семейство)"
require_text "archive/projects/mango/standards/classification-glossary.md" "Capability (Класс)"
require_text "archive/projects/mango/standards/classification-glossary.md" "Feature (Подкласс)"
require_text "archive/projects/mango/standards/classification-glossary.md" "Atomic Function (Функция)"
require_text "archive/projects/mango/standards/classification-glossary.md" "Термин Mango | Международный аналог | Источник | Пример использования"
require_text "archive/projects/mango/standards/classification-glossary.md" "⚠️ Требуется уточнение"

require_text "education/README.md" "status: canonical"
require_text "education/README.md" "standards/education-profile.md"

require_text "frameworks/README.md" "status: canonical"
require_text "frameworks/README.md" "governance/REPO_MODEL.md"

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
require_text "templates/spoke/AI_HANDOVER_PROMPT.md" "governance/AGENT_ONBOARDING.md"
require_text "templates/spoke/AI_HANDOVER_PROMPT.md" "version: 0.2"
require_text "templates/spoke/AI_HANDOVER_PROMPT.md" "executable: true"
require_text "templates/spoke/AI_HANDOVER_PROMPT.md" "ИСПОЛНИМЫЙ HANDOVER PROMPT — СКОПИРУЙ И ВЫПОЛНИ"
require_text "templates/spoke/AI_HANDOVER_PROMPT.md" "EXECUTION"
require_text "templates/spoke/AI_HANDOVER_PROMPT.md" "EXPLANATION"
require_text "templates/spoke/README.md" "AI_HANDOVER_PROMPT.md"
require_text "templates/spoke/README.md" "{{project_name}}"
require_text "templates/spoke/README.md" "governance/AGENT_ONBOARDING.md"
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
