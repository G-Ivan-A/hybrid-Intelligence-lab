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
  if [[ -f "$path" ]] && ! grep -Fq -e "$text" "$path"; then
    fail "$path must contain: $text"
  fi
}

reject_text() {
  local path="$1"
  local text="$2"
  if [[ -f "$path" ]] && grep -Fq -e "$text" "$path"; then
    fail "$path must not contain: $text"
  fi
}

is_active_file() {
  case "$1" in
    README.md | \
    .gitignore | \
    CONCEPT.md | \
    CONTRIBUTING.md | \
    AI_GOVERNANCE.md | \
    AI_PROJECT_CONTEXT-Summary.md | \
    CHANGELOG.md | \
    LICENSE | \
    docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md | \
    docs/adr/2026-06-adr-002-artifact-document-methodology.md | \
    standards/README.md | \
    standards/frontmatter-standard.md | \
    standards/file-naming.md | \
    standards/file-naming-convention.md | \
    standards/research-profile.md | \
    standards/glossary.md | \
    standards/education-profile.md | \
    standards/product-profile.md | \
    standards/team-contract.md | \
    standards/issue-workflow.md | \
    standards/session-handover-standard.md | \
    standards/project-structure-inheritance.md | \
    standards/executable-contract-standard.md | \
    standards/contract-documentation-standard.md | \
    standards/frontmatter-docs-standard.md | \
    standards/executable-documentation-standard.md | \
    standards/htom-documentation-structure.md | \
    standards/webportal-product-concept-standard.md | \
    standards/webportal-solution-concept-standard.md | \
    research/mango/2026-05-26-taxonomy-concept.md | \
    research/mango/2026-05-26-requirements-lifecycle-uncertainty.md | \
    research/mango/2026-05-26-rag-mapping-roadmap.md | \
    research/mango/2026-05-27-capability-decomposition.md | \
    research/hub/2026-05-28-project-context-and-bootstrap-patterns.md | \
    research/hub/2026-06-02-ai-collaboration-retrospective.md | \
    research/hub/2026-06-02-ai-collaboration-retrospective-mango-migration.md | \
    research/hub/2026-05-28-prompts-classification-audit.md | \
    research/hub/2026-05-28-prompts-classification-standard.md | \
    research/hub/2026-06-01-team-c-governance-strategy-audit.md | \
    research/hub/2026-06-02-external-governance-patterns-review.md | \
    research/hub/2026-06-12-ecosystem-governance-audit.md | \
    research/hub/2026-06-20-ecosystem-architecture-research.md | \
    research/hub/2026-06-12-external-practice-intake.md | \
    research/hub/2026-06-12-international-ai-governance-practices.md | \
    research/external-knowledge/2026-06-18-wigers-requirements-analysis.md | \
    research/hub/2026-05-28-user-prompts-analysis.md | \
    research/hub/2026-06-23-repository-structure-concept.md | \
    research/hub/2026-06-25-artifact-inventory-and-classification.md | \
    research/hub/2026-06-27-rfc-industry-norms-and-variants.md | \
    research/hub/2026-06-27-adr-industry-norms-and-variants.md | \
    research/README.md | \
    research/hub/README.md | \
    research/hub/exp-rfc-adr-industry-norms/README.md | \
    research/hub/exp-rfc-adr-industry-norms/collect-evidence.py | \
    research/hub/exp-rfc-adr-industry-norms/outputs/collect-evidence.log | \
    research/hub/exp-rfc-adr-industry-norms/outputs/local-rfc-adr-audit.json | \
    research/hub/exp-rfc-adr-industry-norms/outputs/rfc-external-tree-summary.json | \
    research/hub/exp-rfc-adr-industry-norms/outputs/adr-external-tree-summary.json | \
    research/hub/exp-rfc-adr-industry-norms/outputs/2026-06-27-local-rfc-adr-audit.md | \
    research/hub/exp-rfc-adr-industry-norms/outputs/2026-06-27-rfc-external-tree-summary.md | \
    research/hub/exp-rfc-adr-industry-norms/outputs/2026-06-27-adr-external-tree-summary.md | \
    research/mango/README.md | \
    research/governance/README.md | \
    research/governance/2026-06-06-research-documentation-format.md | \
    research/governance/2026-06-06-executable-contract-format.md | \
    research/governance/2026-06-06-contract-documentation-format.md | \
    research/governance/2026-06-06-governance-folder-structure-decisions.md | \
    research/cicd/README.md | \
    research/cicd/2026-06-09-js-cicd-template-analysis.md | \
    research/open-ai-ru/README.md | \
    research/open-ai-ru/2026-06-20-open-ai-ru-repository-architecture-and-l3-l4.md | \
    research/reputation-technologies/README.md | \
    research/reputation-technologies/2026-06-20-founders-vision-and-framework.ru.md | \
    research/reputation-technologies/2026-06-20-framework-standard.en.md | \
    research/reputation-technologies/2026-06-20-white-paper.en.md | \
    research/reputation-technologies/2026-06-20-executive-summary.ru-en.md | \
    research/reputation-technologies/2026-06-20-glossary.ru-en.md | \
    research/mango/2026-05-22-classification.md | \
    research/mango/2026-05-22-classification-tz.md | \
    research/mango/2026-05-22-requirements-flow.md | \
    research/external-knowledge/README.md | \
    research/external-knowledge/external-sources-registry.md | \
    research/external-knowledge/external-insights/README.md | \
    research/external-knowledge/external-insights/2026-06-13-building-effective-agents.md | \
    research/external-knowledge/external-insights/2026-06-13-12-factor-agents.md | \
    research/external-knowledge/external-insights/2026-06-13-spec-driven-development.md | \
    research/external-knowledge/external-insights/2026-06-15-agent-local-memory-context.md | \
    research/external-knowledge/external-insights/2026-06-15-structured-prompt-driven-development.md | \
    practices/README.md | \
    practices/agent-work/README.md | \
    practices/agent-work/hybrid-search-before-action.md | \
    practices/agent-work/definition-of-ready-check.md | \
    practices/agent-work/plan-verify-ship-loop.md | \
    practices/agent-work/skills-as-reusable-workflows.md | \
    practices/agent-work/skill-catalog-token-budget.md | \
    practices/ai-governance/README.md | \
    practices/ai-governance/nist-ai-rmf-profile-loop.md | \
    practices/ai-governance/eu-ai-act-risk-tiering.md | \
    practices/ai-governance/iso-42001-management-loop.md | \
    practices/ai-governance/openai-evaluation-and-feedback-loop.md | \
    practices/ai-governance/anthropic-capability-thresholds.md | \
    practices/ai-governance/google-saif-agent-security.md | \
    frameworks/README.md | \
    education/README.md | \
    projects/README.md | \
    projects/education-ba-prompt/README.md | \
    projects/education-ba-prompt/docs/course-ideas.md | \
    projects/repo-development/README.md | \
    projects/repo-development/docs/migration-audit-2026-05.md | \
    projects/repo-development/docs/contract-violations-self-report-2026-06.md | \
    projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md | \
    governance/agent-onboarding-protocol.md | \
    governance/repo-model.md | \
    governance/artifact-map.md | \
    governance/backlog.md | \
    governance/executable-documents-issues.md | \
    governance/session-digests.md | \
    governance/rfc/README.md | \
    governance/rfc/rfc-two-cases-of-project-initialization.md | \
    governance/rfc/contract-executability-rfc.md | \
    governance/rfc/repository-quality-improvement-plan.md | \
    governance/rfc/tech-debt-solutions-proposal-2026-06.md | \
    governance/rfc/draft-triage-and-exit-plan.md | \
    governance/rfc/htom-vs-spoke-clarification-2026-06.md | \
    governance/rfc/hub-vision-concept-proposal-2026-06.md | \
    governance/rfc/knowledge-lifecycle-proposal.md | \
    governance/rfc/resolve-artifact-location-proposal.md | \
    governance/rfc/external-knowledge-integration.md | \
    governance/rfc/documentation-architecture-balance.md | \
    governance/rfc/research-memory-source-intelligence.md | \
    governance/rfc/repository-archetypes-template-release.md | \
    governance/rfc/product-concept-template-proposal.md | \
    governance/rfc/solution-concept-template-proposal.md | \
    governance/rfc/methodology-research-and-proposals.md | \
    governance/rfc/2026-06-27-rfc-adr-standard.md | \
    governance/rfc/2026-06-27-rfc-rfc-standard.md | \
    research/mango/2026-06-18-requirements-engineering-ai-era.md | \
    research/mango/2026-06-18-ai-classifications-formalization.md | \
    research/mango/2026-06-19-repository-structure-vision.md | \
    research/mango/2026-06-19-token-optimization-proposal.md | \
    docs/vision.md | \
    docs/product-concept.md | \
    docs/ecosystem-map.md | \
    docs/ecosystem-map-Index.md | \
    docs/project-summaries/README.md | \
    docs/project-summaries/mango-ba-prompts-context-Summary.md | \
    docs/project-summaries/open-ai-ru-context-Summary.md | \
    docs/project-summaries/clarify-engine-ai-context-Summary.md | \
    docs/audit/task-execution-audit-2026-06.md | \
    guides/README.md | \
    guides/quick-start.md | \
    guides/init-spoke-repo.md | \
    guides/sync-from-hub.md | \
    guides/sync-with-projects.md | \
    guides/interact-with-ai.md | \
    guides/deploy-project.md | \
    guides/rollback-sync.md | \
    guides/contribute-template.md | \
    guides/troubleshooting.md | \
    guides/glossary.md | \
    mkdocs.yml | \
    website/index.md | \
    website/stylesheets/extra.css | \
    website/docs | \
    website/guides | \
    website/research | \
    .github/workflows/deploy-docs.yml | \
    .github/workflows/update-manifest.yml | \
    .github/workflows/validate.yml | \
    .github/ISSUE_TEMPLATE/task.yml | \
    .github/ISSUE_TEMPLATE/task.md | \
    .github/ISSUE_TEMPLATE/task-creative.md | \
    templates/htom/AI_GOVERNANCE.md | \
    templates/htom/AI_QUICK_RULES.md | \
    templates/htom/AI_SESSION_HANDOVER_PROMPT.md | \
    templates/htom/README.md | \
    templates/htom/CONTRIBUTING.md | \
    templates/htom/CHANGELOG.md | \
    templates/htom/docs/adr/.gitkeep | \
    templates/htom/docs/audit/.gitkeep | \
    templates/htom/.github/ISSUE_TEMPLATE/task.md | \
    templates/htom/.github/ISSUE_TEMPLATE/task-creative.md | \
    templates/htom/tools/validate-repository-structure.sh | \
    templates/htom/init.sh | \
    templates/spoke/README.md | \
    templates/spoke/CONTRIBUTING.md | \
    templates/spoke/docs/README.md | \
    templates/spoke/.github/workflows/ci.yml | \
    templates/spoke/tools/validate-file-naming.sh | \
    templates/webportal-product-concept-template.md | \
    templates/webportal-solution-concept-template.md | \
    templates/sync-project-with-hub-prompt.md | \
    templates/manifest.json | \
    templates/sync-metadata.json | \
    tools/generate-manifest.py | \
    tools/sync-from-hub.sh | \
    tools/validate-mkdocs-site.sh | \
    experiments/test-frontmatter-validator.sh | \
    experiments/test-smart-sync.sh | \
    tools/validate-frontmatter.sh | \
    tools/validate-file-naming.sh | \
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

validate_metadata_single_source() {
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
        if ($0 ~ /^(status|version|updated|temperature):[[:space:]]*/) {
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
  done < <(find standards governance research -type f -name '*.md' | sort)
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

validate_template_placeholders() {
  local file
  local line
  local placeholder

  while IFS=: read -r file line placeholder; do
    case "$placeholder" in
      "{{date}}" | "{{project_name}}" | "{{hub_url}}" | "{{REPO_NAME}}")
        ;;
      *)
        fail "unapproved template placeholder in $file:$line: $placeholder"
        ;;
    esac
  done < <(grep -RIno '{{[A-Za-z_][A-Za-z_]*}}' templates || true)
}

required_directories=(
  ".github/ISSUE_TEMPLATE"
  "docs"
  "docs/adr"
  "templates"
  "templates/htom"
  "templates/htom/docs/adr"
  "templates/htom/docs/audit"
  "templates/htom/.github/ISSUE_TEMPLATE"
  "templates/htom/tools"
  "templates/spoke"
  "templates/spoke/docs"
  "templates/spoke/.github/workflows"
  "templates/spoke/tools"
  "standards"
  "research"
  "research/hub"
  "research/mango"
  "research/governance"
  "research/external-knowledge"
  "research/external-knowledge/external-insights"
  "practices"
  "practices/agent-work"
  "practices/ai-governance"
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
  "docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md"
  "docs/adr/2026-06-adr-002-artifact-document-methodology.md"
  "standards/README.md"
  "standards/frontmatter-standard.md"
  "standards/file-naming.md"
  "standards/file-naming-convention.md"
  "standards/research-profile.md"
  "standards/glossary.md"
  "standards/education-profile.md"
  "standards/product-profile.md"
  "standards/team-contract.md"
  "standards/issue-workflow.md"
  "standards/session-handover-standard.md"
  "standards/project-structure-inheritance.md"
  "standards/executable-contract-standard.md"
  "standards/contract-documentation-standard.md"
  "standards/frontmatter-docs-standard.md"
  "standards/executable-documentation-standard.md"
  "standards/htom-documentation-structure.md"
  "standards/webportal-product-concept-standard.md"
  "standards/webportal-solution-concept-standard.md"
  "research/README.md"
  "research/hub/README.md"
  "research/hub/2026-06-12-ecosystem-governance-audit.md"
  "research/hub/2026-06-20-ecosystem-architecture-research.md"
  "research/hub/2026-06-12-external-practice-intake.md"
  "research/hub/2026-06-12-international-ai-governance-practices.md"
  "research/hub/2026-06-23-repository-structure-concept.md"
  "research/hub/2026-06-25-artifact-inventory-and-classification.md"
  "research/hub/2026-06-27-rfc-industry-norms-and-variants.md"
  "research/hub/2026-06-27-adr-industry-norms-and-variants.md"
  "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md"
  "research/mango/README.md"
  "research/governance/README.md"
  "research/governance/2026-06-06-research-documentation-format.md"
  "research/governance/2026-06-06-executable-contract-format.md"
  "research/governance/2026-06-06-contract-documentation-format.md"
  "research/governance/2026-06-06-governance-folder-structure-decisions.md"
  "research/mango/2026-05-22-classification.md"
  "research/mango/2026-05-22-classification-tz.md"
  "research/mango/2026-05-22-requirements-flow.md"
  "research/mango/2026-05-26-rag-mapping-roadmap.md"
  "research/external-knowledge/README.md"
  "research/external-knowledge/external-sources-registry.md"
  "research/external-knowledge/external-insights/README.md"
  "research/external-knowledge/external-insights/2026-06-13-building-effective-agents.md"
  "research/external-knowledge/external-insights/2026-06-13-12-factor-agents.md"
  "research/external-knowledge/external-insights/2026-06-13-spec-driven-development.md"
  "research/external-knowledge/external-insights/2026-06-15-agent-local-memory-context.md"
  "research/external-knowledge/external-insights/2026-06-15-structured-prompt-driven-development.md"
  "practices/README.md"
  "practices/agent-work/README.md"
  "practices/agent-work/hybrid-search-before-action.md"
  "practices/agent-work/definition-of-ready-check.md"
  "practices/agent-work/plan-verify-ship-loop.md"
  "practices/agent-work/skills-as-reusable-workflows.md"
  "practices/agent-work/skill-catalog-token-budget.md"
  "practices/ai-governance/README.md"
  "practices/ai-governance/nist-ai-rmf-profile-loop.md"
  "practices/ai-governance/eu-ai-act-risk-tiering.md"
  "practices/ai-governance/iso-42001-management-loop.md"
  "practices/ai-governance/openai-evaluation-and-feedback-loop.md"
  "practices/ai-governance/anthropic-capability-thresholds.md"
  "practices/ai-governance/google-saif-agent-security.md"
  "frameworks/README.md"
  "education/README.md"
  "projects/README.md"
  "projects/repo-development/README.md"
  "projects/repo-development/docs/migration-audit-2026-05.md"
  "projects/repo-development/docs/contract-violations-self-report-2026-06.md"
  "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md"
  "governance/agent-onboarding-protocol.md"
  "governance/repo-model.md"
  "governance/artifact-map.md"
  "governance/backlog.md"
  "governance/executable-documents-issues.md"
  "governance/session-digests.md"
  "governance/rfc/README.md"
  "governance/rfc/rfc-two-cases-of-project-initialization.md"
  "governance/rfc/contract-executability-rfc.md"
  "governance/rfc/repository-quality-improvement-plan.md"
  "governance/rfc/draft-triage-and-exit-plan.md"
  "governance/rfc/htom-vs-spoke-clarification-2026-06.md"
  "governance/rfc/knowledge-lifecycle-proposal.md"
  "governance/rfc/resolve-artifact-location-proposal.md"
  "governance/rfc/external-knowledge-integration.md"
  "governance/rfc/documentation-architecture-balance.md"
  "governance/rfc/research-memory-source-intelligence.md"
  "governance/rfc/repository-archetypes-template-release.md"
  "governance/rfc/product-concept-template-proposal.md"
  "governance/rfc/solution-concept-template-proposal.md"
  "research/mango/2026-06-18-requirements-engineering-ai-era.md"
  "research/mango/2026-06-19-repository-structure-vision.md"
  ".github/ISSUE_TEMPLATE/task.yml"
  ".github/ISSUE_TEMPLATE/task.md"
  ".github/ISSUE_TEMPLATE/task-creative.md"
  "templates/htom/AI_GOVERNANCE.md"
  "templates/htom/AI_QUICK_RULES.md"
  "templates/htom/AI_SESSION_HANDOVER_PROMPT.md"
  "templates/htom/README.md"
  "templates/htom/CONTRIBUTING.md"
  "templates/htom/CHANGELOG.md"
  "templates/htom/docs/adr/.gitkeep"
  "templates/htom/docs/audit/.gitkeep"
  "templates/htom/.github/ISSUE_TEMPLATE/task.md"
  "templates/htom/.github/ISSUE_TEMPLATE/task-creative.md"
  "templates/htom/tools/validate-repository-structure.sh"
  "templates/htom/init.sh"
  "templates/spoke/README.md"
  "templates/spoke/CONTRIBUTING.md"
  "templates/spoke/docs/README.md"
  "templates/spoke/.github/workflows/ci.yml"
  "templates/spoke/tools/validate-file-naming.sh"
  "templates/webportal-product-concept-template.md"
  "templates/webportal-solution-concept-template.md"
  "templates/sync-project-with-hub-prompt.md"
  "templates/manifest.json"
  "templates/sync-metadata.json"
  ".github/workflows/validate.yml"
  ".github/workflows/update-manifest.yml"
  "tools/generate-manifest.py"
  "tools/sync-from-hub.sh"
  "tools/validate-mkdocs-site.sh"
  "experiments/test-frontmatter-validator.sh"
  "tools/validate-frontmatter.sh"
  "tools/validate-file-naming.sh"
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

validate_metadata_single_source
validate_internal_markdown_links
validate_artifact_map_paths
validate_template_placeholders
if ! ./tools/validate-file-naming.sh; then
  fail "file naming validation failed"
fi

while IFS= read -r file; do
  if [[ ! -e "$file" ]]; then
    continue
  fi

  if is_active_file "$file"; then
    continue
  fi

  if [[ "${file##*/}" == ".gitkeep" ]]; then
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
require_text "README.md" "standards/file-naming.md"
require_text "README.md" "standards/glossary.md"
require_text "README.md" "standards/team-contract.md"
require_text "README.md" "governance/agent-onboarding-protocol.md"
require_text "README.md" "governance/repo-model.md"
require_text "README.md" "governance/artifact-map.md"
require_text "README.md" "projects/education-ba-prompt/README.md"
require_text "README.md" "research/mango/README.md"
require_text "README.md" "practices/README.md"
require_text "README.md" "./tools/validate-frontmatter.sh"
require_text "README.md" "./tools/validate-file-naming.sh"
require_text "README.md" "./tools/validate-repository-structure.sh"
require_text "README.md" "Человек задаёт смысл, AI ускоряет путь — вместе по правилам"

require_text "CONCEPT.md" "governance/repo-model.md"
require_text "CONCEPT.md" "standards/README.md"
require_text "CONCEPT.md" "Anti-Inflation"
require_text "CONCEPT.md" "status: canonical"
require_text "CONCEPT.md" "version: 1.0"
require_text "CONCEPT.md" "updated: 2026-05-26"
require_text "CONCEPT.md" "Operating Mode"
require_text "CONCEPT.md" "structured mode"
require_text "CONCEPT.md" "creative mode"
require_text "CONCEPT.md" "standards/team-contract.md"
require_text "CONCEPT.md" "Шаблон командного соглашения"
require_text "CONCEPT.md" "glossary.md"
require_text "CONCEPT.md" "единой терминологии"

require_text "CONTRIBUTING.md" "AI_GOVERNANCE.md"
require_text "CONTRIBUTING.md" "standards/README.md"
require_text "CONTRIBUTING.md" "status: canonical"
require_text "CONTRIBUTING.md" "version: 1.7"
require_text "CONTRIBUTING.md" "Консолидация открытых вопросов"
require_text "CONTRIBUTING.md" "Работа с внешними источниками"
require_text "CONTRIBUTING.md" "governance/backlog.md"
require_text "CONTRIBUTING.md" "updated: 2026-06-25"
require_text "CONTRIBUTING.md" "temperature: 0.1"
require_text "CONTRIBUTING.md" ".github/ISSUE_TEMPLATE/task.md"
require_text "CONTRIBUTING.md" ".github/ISSUE_TEMPLATE/task-creative.md"
require_text "CONTRIBUTING.md" "Специфика работы с AI-агентами"
require_text "CONTRIBUTING.md" "manual restart"
require_text "CONTRIBUTING.md" "standards/frontmatter-standard.md"
require_text "CONTRIBUTING.md" "governance/rfc/knowledge-lifecycle-proposal.md"
require_text "CONTRIBUTING.md" "governance/rfc/resolve-artifact-location-proposal.md"
require_text "CONTRIBUTING.md" "Правило авто-заполнения Мета"
require_text "CONTRIBUTING.md" "./tools/validate-frontmatter.sh"
require_text "CONTRIBUTING.md" "./tools/validate-file-naming.sh"
require_text "CONTRIBUTING.md" "./tools/validate-repository-structure.sh"
require_text "CONTRIBUTING.md" "File Naming"
require_text "CONTRIBUTING.md" "future-phase: X"
require_text "CONTRIBUTING.md" "topic: Y"
require_text "CONTRIBUTING.md" "Повторный анализ инициирует только Пользователь"
require_text "CONTRIBUTING.md" "отклонено"

require_text "AI_GOVERNANCE.md" "status: canonical"
require_text "AI_GOVERNANCE.md" "version: 1.6"
require_text "AI_GOVERNANCE.md" "updated: 2026-06-13"
require_text "AI_GOVERNANCE.md" "temperature: 0.1"
require_text "AI_GOVERNANCE.md" "executable: false"
require_text "AI_GOVERNANCE.md" "Директива pre-flight"
require_text "AI_GOVERNANCE.md" "Пользователь"
require_text "AI_GOVERNANCE.md" "Human reviewer"
require_text "AI_GOVERNANCE.md" "Creative"
require_text "AI_GOVERNANCE.md" "Хаб является источником рекомендаций"
require_text "AI_GOVERNANCE.md" "Обоснованный обход в Creative Mode"
require_text "AI_GOVERNANCE.md" "Специфика работы с AI-агентами"
require_text "AI_GOVERNANCE.md" "standards/frontmatter-standard.md"
require_text "AI_GOVERNANCE.md" "standards/README.md"
require_text "AI_GOVERNANCE.md" "governance/rfc/knowledge-lifecycle-proposal.md"
require_text "AI_GOVERNANCE.md" "governance/rfc/resolve-artifact-location-proposal.md"
require_text "AI_GOVERNANCE.md" "Правило авто-заполнения Мета"
require_text "AI_GOVERNANCE.md" "Разделение Framework vs Methodology"
require_text "AI_GOVERNANCE.md" "governance/agent-onboarding-protocol.md"
require_text "AI_GOVERNANCE.md" "Человек задаёт смысл, AI ускоряет путь — вместе по правилам"

require_text "CHANGELOG.md" "## Unreleased"
require_text "CHANGELOG.md" "issue #237"
require_text "CHANGELOG.md" "issue #241"
require_text "CHANGELOG.md" "issue #240"
require_text "CHANGELOG.md" "issue #278"
require_text "CHANGELOG.md" "## [1.1] - 2026-05-26"
require_text "CHANGELOG.md" "### Added"
require_text "CHANGELOG.md" "### Changed"
require_text "CHANGELOG.md" "### Removed"
require_text "mkdocs.yml" "2026-06-27-rfc-industry-norms-and-variants.md"
require_text "mkdocs.yml" "2026-06-27-adr-industry-norms-and-variants.md"

require_text "standards/README.md" "| Стандарт | Статус | Где применяется | Источник |"
require_text "standards/README.md" "status: accepted"
require_text "standards/README.md" "version: 1.4"
require_text "standards/README.md" "updated: 2026-06-25"
require_text "standards/README.md" "temperature: 0.1"
require_text "standards/README.md" "owner: G-Ivan-A"
require_text "standards/README.md" "Как пользоваться"
require_text "standards/README.md" "frontmatter-standard.md"
require_text "standards/README.md" "file-naming.md"
require_text "standards/README.md" "file-naming-convention.md"
require_text "standards/README.md" "research-profile.md"
require_text "standards/README.md" "team-contract.md"
require_text "standards/README.md" "standards/glossary.md"
require_text "standards/README.md" "standards/education-profile.md"
require_text "standards/README.md" "product-profile.md"
require_text "standards/README.md" "project-structure-inheritance.md"
require_text "standards/README.md" "frontmatter-docs-standard.md"
require_text "standards/README.md" "executable-documentation-standard.md"
require_text "standards/README.md" "htom-documentation-structure.md"
require_text "standards/README.md" "artifact-map.md"
require_text "standards/README.md" "issue-workflow.md"
require_text "standards/README.md" "session-handover-standard.md"
require_text "standards/README.md" "knowledge-lifecycle-proposal.md"
require_text "standards/README.md" "Artifact location resolver"
require_text "standards/README.md" "resolve-artifact-location-proposal.md"

require_text "standards/frontmatter-standard.md" "status: accepted"
require_text "standards/frontmatter-standard.md" "version: 1.1"
require_text "standards/frontmatter-standard.md" "updated: 2026-06-28"
require_text "standards/frontmatter-standard.md" "temperature: 0.1"
require_text "standards/frontmatter-standard.md" "owner: G-Ivan-A"
require_text "standards/frontmatter-standard.md" '`status`'
require_text "standards/frontmatter-standard.md" '`version`'
require_text "standards/frontmatter-standard.md" '`updated`'
require_text "standards/frontmatter-standard.md" '`temperature`'
require_text "standards/frontmatter-standard.md" '`ai-generated` **ЗАПРЕЩЕН** во frontmatter'
require_text "standards/frontmatter-standard.md" "NIST AI Risk Management Framework"

require_text "standards/frontmatter-docs-standard.md" "status: accepted"
require_text "standards/frontmatter-docs-standard.md" "version: 1.1"
require_text "standards/frontmatter-docs-standard.md" "updated: 2026-06-28"
require_text "standards/frontmatter-docs-standard.md" "temperature: 0.1"
require_text "standards/frontmatter-docs-standard.md" "owner: G-Ivan-A"
require_text "standards/frontmatter-docs-standard.md" "standards/frontmatter-standard.md"
require_text "standards/frontmatter-docs-standard.md" "Standard"
require_text "standards/frontmatter-docs-standard.md" "Guide"
require_text "standards/frontmatter-docs-standard.md" "RFC"
require_text "standards/frontmatter-docs-standard.md" "ADR"
require_text "standards/frontmatter-docs-standard.md" "Research"
require_text "standards/frontmatter-docs-standard.md" "Template"
require_text "standards/frontmatter-docs-standard.md" "necessary and sufficient"

require_text "standards/executable-documentation-standard.md" "status: accepted"
require_text "standards/executable-documentation-standard.md" "version: 1.2"
require_text "standards/executable-documentation-standard.md" "updated: 2026-06-15"
require_text "standards/executable-documentation-standard.md" "temperature: 0.1"
require_text "standards/executable-documentation-standard.md" "Descriptive documents"
require_text "standards/executable-documentation-standard.md" "Executable documents"
require_text "standards/executable-documentation-standard.md" "Atomization"
require_text "standards/executable-documentation-standard.md" "Framework vs Template"
require_text "standards/executable-documentation-standard.md" "Template = один воспроизводимый артефакт"
require_text "standards/executable-documentation-standard.md" "Framework = набор связанных Standards, Templates, Patterns"
require_text "standards/executable-documentation-standard.md" "Practice graph"
require_text "standards/executable-documentation-standard.md" "research/hub/2026-06-12-international-ai-governance-practices.md"
require_text "standards/executable-documentation-standard.md" "Detail-level naming"
require_text "standards/executable-documentation-standard.md" "[file-naming.md](file-naming.md)"

require_text "standards/htom-documentation-structure.md" "status: accepted"
require_text "standards/htom-documentation-structure.md" "version: 1.0"
require_text "standards/htom-documentation-structure.md" "updated: 2026-06-12"
require_text "standards/htom-documentation-structure.md" "temperature: 0.1"
require_text "standards/htom-documentation-structure.md" "Mango docs error pattern"
require_text "standards/htom-documentation-structure.md" "docs/README.md"
require_text "standards/htom-documentation-structure.md" "docs/adr/"
require_text "standards/htom-documentation-structure.md" "docs/rfc/"
require_text "standards/htom-documentation-structure.md" "templates/sync-project-with-hub-prompt.md"


require_text "standards/team-contract.md" "status: accepted"
require_text "standards/team-contract.md" "version: 1.1"
require_text "standards/team-contract.md" "updated: 2026-06-13"
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

require_text "standards/issue-workflow.md" "status: accepted"
require_text "standards/issue-workflow.md" "version: 1.2"
require_text "standards/issue-workflow.md" "updated: 2026-06-12"
require_text "standards/issue-workflow.md" "temperature: 0.1"
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

require_text "standards/session-handover-standard.md" "status: draft"
require_text "standards/session-handover-standard.md" "version: 0.2"
require_text "standards/session-handover-standard.md" "updated: 2026-06-13"
require_text "standards/session-handover-standard.md" "AI_SESSION_HANDOVER_PROMPT.md"
require_text "standards/session-handover-standard.md" "Контекст проекта"
require_text "standards/session-handover-standard.md" "Ключевые решения"
require_text "standards/session-handover-standard.md" "Роль и иерархия"
require_text "standards/session-handover-standard.md" "Контекст чата диалога"
require_text "standards/session-handover-standard.md" "Канал взаимодействия с репо"
require_text "standards/session-handover-standard.md" "Проверка шаблонов"
require_text "standards/session-handover-standard.md" "Формат постановки задач"
require_text "standards/session-handover-standard.md" "Протокол бесшовной передачи проекта"

require_text "standards/project-structure-inheritance.md" "status: accepted"
require_text "standards/project-structure-inheritance.md" "version: 1.1"
require_text "standards/project-structure-inheritance.md" "updated: 2026-06-04"
require_text "standards/project-structure-inheritance.md" "executable: false"
require_text "standards/project-structure-inheritance.md" "Разрешённые подкаталоги"
require_text "standards/project-structure-inheritance.md" "Правила связывания стандартов"
require_text "standards/project-structure-inheritance.md" "scope: mango-only"
require_text "standards/project-structure-inheritance.md" "Пример структуры проекта"
require_text "standards/project-structure-inheritance.md" "Репозиторий-широкий стандарт НЕ должен ссылаться на проектный"
require_text "standards/issue-workflow.md" "User Story / ФТ"
require_text "standards/issue-workflow.md" ".github/ISSUE_TEMPLATE/task.md"
require_text "standards/issue-workflow.md" ".github/ISSUE_TEMPLATE/task-creative.md"
require_text "standards/issue-workflow.md" "CHANGELOG.md"
require_text "standards/issue-workflow.md" "governance/artifact-map.md"
require_text "standards/issue-workflow.md" "validate-frontmatter.sh"
require_text "standards/issue-workflow.md" "validate-repository-structure.sh"
require_text "standards/file-naming.md" "status: accepted"
require_text "standards/file-naming.md" "version: 1.6"
require_text "standards/file-naming.md" "updated: 2026-06-25"
require_text "standards/file-naming.md" "Корень репозитория"
require_text "standards/file-naming.md" "UPPERCASE_WITH_HYPHENS.md"
require_text "standards/file-naming.md" "Вложенные каталоги"
require_text "standards/file-naming.md" "lowercase-with-hyphens.md"
require_text "standards/file-naming.md" "Правила именования файлов в standards/ и governance/"
require_text "standards/file-naming.md" '`CAPS_LOCK` запрещён'
require_text "standards/file-naming.md" "classification-glossary.md"
require_text "standards/file-naming.md" "agent-onboarding-protocol.md"
require_text "standards/file-naming.md" "Исключения"
require_text "standards/file-naming.md" "Новый файл не соответствует правилу"
require_text "standards/file-naming.md" "Правило суффиксов уровня детализации"
require_text "standards/file-naming.md" '`-Index`'
require_text "standards/file-naming.md" '`-Summary`'
require_text "standards/file-naming.md" '`-Full`'
require_text "standards/file-naming.md" "Формат датировки"
require_text "standards/file-naming.md" "ISO 8601: YYYY-MM-DD"
require_text "standards/file-naming.md" "Хронологические артефакты"
require_text "standards/file-naming.md" "YYYY-MM-DD-name.md"
require_text "standards/file-naming.md" "YYYY-MM-adr-NNN-name.md"
require_text "standards/file-naming.md" "tools/validate-file-naming.sh"

require_text "standards/file-naming-convention.md" "status: accepted"
require_text "standards/file-naming-convention.md" "version: 1.1"
require_text "standards/file-naming-convention.md" "updated: 2026-06-25"
require_text "standards/file-naming-convention.md" "file-naming.md"
require_text "standards/file-naming-convention.md" "YYYY-MM-DD-name.md"
require_text "standards/file-naming-convention.md" "YYYY-MM-adr-NNN-name.md"
require_text "standards/file-naming-convention.md" "./tools/validate-file-naming.sh"

require_text "standards/research-profile.md" "status: accepted"
require_text "standards/research-profile.md" "version: 1.3"
require_text "standards/research-profile.md" "updated: 2026-06-28"
require_text "standards/research-profile.md" "Назначение"
require_text "standards/research-profile.md" "Обязательные артефакты"
require_text "standards/research-profile.md" "YYYY-MM-DD-topic.md"
require_text "standards/research-profile.md" "exp-<slug>"
require_text "standards/research-profile.md" "Шаблон frontmatter исследования"
require_text "standards/research-profile.md" "external-analysis | internal-analysis | experiment"
require_text "standards/research-profile.md" "Как организовать исследование"
require_text "standards/research-profile.md" "Body Structure: Введение → Результаты → Детализация"
require_text "standards/research-profile.md" "Введение → Результаты → Детализация"
require_text "standards/research-profile.md" "Чек-лист готовности к публикации"
require_text "standards/research-profile.md" "Правила цитирования источников"
require_text "standards/research-profile.md" "FAIR Principles"

require_text "standards/glossary.md" "status: accepted"
require_text "standards/glossary.md" "version: 1.4"
require_text "standards/glossary.md" "updated: 2026-06-11"
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
require_text "standards/glossary.md" "HTOM-команда"
require_text "standards/glossary.md" "Spoke-репозиторий"
require_text "standards/glossary.md" "Как использовать"
require_text "standards/glossary.md" "Связи терминов"
require_text "standards/glossary.md" "Источники"

require_text "standards/education-profile.md" "status: accepted"
require_text "standards/education-profile.md" "version: 1.0"
require_text "standards/education-profile.md" "updated: 2026-05-26"
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
require_text "standards/product-profile.md" "status: accepted"
require_text "standards/product-profile.md" "PRODUCT_VISION.md"
require_text "standards/product-profile.md" "Обязательные артефакты"
require_text "standards/product-profile.md" "Метрики успеха"

require_text "standards/webportal-product-concept-standard.md" "status: draft"
require_text "standards/webportal-product-concept-standard.md" "level: L2"
require_text "standards/webportal-product-concept-standard.md" "Product Concept (L2)"
require_text "standards/webportal-product-concept-standard.md" "User Personas"
require_text "standards/webportal-product-concept-standard.md" "User Stories / Jobs-to-Be-Done"
require_text "standards/webportal-product-concept-standard.md" "Key Features (MVP Scope)"
require_text "standards/webportal-product-concept-standard.md" "User Flows"
require_text "standards/webportal-product-concept-standard.md" "Success Metrics"
require_text "standards/webportal-product-concept-standard.md" "Roadmap (High-Level)"
require_text "standards/webportal-product-concept-standard.md" "webportal-solution-concept-standard.md"
if grep -Eiq 'hub-and-spoke|spoke|repository|Yandex GPT|provider|technology stack|C4|Mermaid' "standards/webportal-product-concept-standard.md"; then
  fail "standards/webportal-product-concept-standard.md must stay L2/product-only and must not include L3/provider/repository language"
fi

require_text "standards/webportal-solution-concept-standard.md" "status: draft"
require_text "standards/webportal-solution-concept-standard.md" "level: L3"
require_text "standards/webportal-solution-concept-standard.md" "Solution Concept (L3)"
require_text "standards/webportal-solution-concept-standard.md" "System Architecture (C4 Model)"
require_text "standards/webportal-solution-concept-standard.md" "Technology Stack"
require_text "standards/webportal-solution-concept-standard.md" "Integration Points"
require_text "standards/webportal-solution-concept-standard.md" "Data Model"
require_text "standards/webportal-solution-concept-standard.md" "Non-Functional Requirements"
require_text "standards/webportal-solution-concept-standard.md" "Deployment Strategy"
require_text "standards/webportal-solution-concept-standard.md" "Provider-Agnostic Architecture"
require_text "standards/webportal-solution-concept-standard.md" "Yandex GPT"
require_text "standards/webportal-solution-concept-standard.md" '```mermaid'
require_text "templates/webportal-product-concept-template.md" "{{project_name}}"
require_text "templates/webportal-product-concept-template.md" "{{date}}"
require_text "templates/webportal-product-concept-template.md" "{{hub_url}}"
require_text "templates/webportal-product-concept-template.md" "Product Concept: {{project_name}}"
require_text "templates/webportal-solution-concept-template.md" "{{project_name}}"
require_text "templates/webportal-solution-concept-template.md" "{{date}}"
require_text "templates/webportal-solution-concept-template.md" "{{hub_url}}"
require_text "templates/webportal-solution-concept-template.md" "Solution Concept: {{project_name}}"
require_text "templates/webportal-solution-concept-template.md" "Provider-agnostic AI boundary"
require_text "templates/sync-project-with-hub-prompt.md" "status: canonical"
require_text "templates/sync-project-with-hub-prompt.md" "version: 0.1"
require_text "templates/sync-project-with-hub-prompt.md" "updated: 2026-06-12"
require_text "templates/sync-project-with-hub-prompt.md" "temperature: 0.1"
require_text "templates/sync-project-with-hub-prompt.md" "executable: true"
require_text "templates/sync-project-with-hub-prompt.md" "{{project_name}}"
require_text "templates/sync-project-with-hub-prompt.md" "{{hub_url}}"
require_text "templates/sync-project-with-hub-prompt.md" "Compare local project practices with Hub practices"
require_text "templates/sync-project-with-hub-prompt.md" "Do not overwrite project-specific decisions"

require_text "docs/vision.md" "version: 0.3"
require_text "docs/vision.md" "Связь миров: экосистема гибридных команд"
require_text "docs/vision.md" "Core Innovation"
require_text "docs/vision.md" "обеспечивает обмен опытом"
require_text "docs/vision.md" "связующий слой экосистемы проектов"
require_text "docs/vision.md" "Метафора «Связь миров»"
require_text "docs/vision.md" "Цикл обмена практиками"
require_text "docs/vision.md" "Связь L1-L4"
require_text "docs/vision.md" "governance/rfc/knowledge-lifecycle-proposal.md"
require_text "docs/vision.md" "governance/rfc/resolve-artifact-location-proposal.md"
require_text "docs/product-concept.md" "version: 0.3"
require_text "docs/product-concept.md" "collaborative environment"
require_text "docs/product-concept.md" "AI_SESSION_HANDOVER_PROMPT.md"
require_text "docs/product-concept.md" "несколько чатов"
require_text "docs/product-concept.md" "быстрее входить в рабочее пространство"
require_text "docs/product-concept.md" "Связь L1-L4"
require_text "docs/product-concept.md" "governance/rfc/product-concept-template-proposal.md"
require_text "docs/product-concept.md" "governance/rfc/resolve-artifact-location-proposal.md"
require_text "docs/ecosystem-map.md" "version: 0.4"
require_text "docs/ecosystem-map.md" "обмен практиками"
require_text "docs/ecosystem-map.md" "practices/README.md"
require_text "docs/ecosystem-map.md" "templates/sync-project-with-hub-prompt.md"
require_text "docs/ecosystem-map.md" "связующий слой"
require_text "docs/ecosystem-map.md" "Knowledge Lifecycle"
require_text "docs/ecosystem-map.md" "governance/rfc/resolve-artifact-location-proposal.md"
require_text "docs/ecosystem-map.md" "Связь L1-L4"

require_text "governance/repo-model.md" "Артефакт только при операционной боли"
require_text "governance/repo-model.md" "Anti-Inflation"
require_text "governance/repo-model.md" "tools/"
require_text "governance/repo-model.md" "practices/"
require_text "governance/repo-model.md" "status: canonical"
require_text "governance/repo-model.md" "version: 1.2"
require_text "governance/repo-model.md" "updated: 2026-06-12"
require_text "governance/repo-model.md" "executable: false"
require_text "governance/repo-model.md" "Decision Rules — исполнимая часть справочного документа"

require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "status: accepted"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "owner: G-Ivan-A"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "rfc-scope: A"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "Концептуальная аналогия"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "Таблица-манифест"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "Runtime-онбординг"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "Bootstrap-клонирование"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "standards/glossary.md"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "2026-06-02-ai-collaboration-retrospective.md"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "governance/agent-onboarding-protocol.md"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "templates/htom/README.md"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" '```mermaid'
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "Follow-up"
require_text "governance/rfc/rfc-two-cases-of-project-initialization.md" "Решение за человеком"

require_text "governance/rfc/contract-executability-rfc.md" "status: proposed"
require_text "governance/rfc/contract-executability-rfc.md" "version: 1.2"
require_text "governance/rfc/contract-executability-rfc.md" "owner: G-Ivan-A"
require_text "governance/rfc/contract-executability-rfc.md" "rfc-scope: A"
require_text "governance/rfc/contract-executability-rfc.md" "## Decision Status"
require_text "governance/rfc/contract-executability-rfc.md" '| Executable markers | accepted | `standards/executable-contract-standard.md` |'
require_text "governance/rfc/contract-executability-rfc.md" '| Directive block | accepted | `governance/agent-onboarding-protocol.md` |'
require_text "governance/rfc/contract-executability-rfc.md" '| Rollout plan | implemented | `governance/backlog.md` |'
require_text "governance/rfc/contract-executability-rfc.md" "| Open questions | deferred | — |"
require_text "governance/rfc/contract-executability-rfc.md" "Решения Пользователя по RFC"
require_text "governance/rfc/contract-executability-rfc.md" "executable: true|false"
require_text "governance/rfc/contract-executability-rfc.md" "governance/rfc/"
require_text "governance/rfc/contract-executability-rfc.md" "Дата утверждения"

require_text "governance/rfc/repository-quality-improvement-plan.md" "status: draft"
require_text "governance/rfc/repository-quality-improvement-plan.md" "version: 0.3"
require_text "governance/rfc/repository-quality-improvement-plan.md" "archive/projects/mango/"
require_text "governance/rfc/repository-quality-improvement-plan.md" "Phase 1"
require_text "governance/rfc/repository-quality-improvement-plan.md" "Запрос На Согласование"
require_text "governance/rfc/repository-quality-improvement-plan.md" "Задачи Для Создания После Согласования"

require_text "governance/rfc/draft-triage-and-exit-plan.md" "status: accepted"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "version: 0.3"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "updated: 2026-06-13"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "Template Placeholders"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "approval_target"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "estimated_effort"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "Questions To User"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "## 9. Масштабируемость и защита от бюрократии (Anti-Bureaucracy)"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "Unidirectional Links"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "Index over Frontmatter"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "Lazy Reconciliation"
require_text "governance/rfc/draft-triage-and-exit-plan.md" "Static Exit-Plans"

require_text "governance/rfc/htom-vs-spoke-clarification-2026-06.md" "status: accepted"
require_text "governance/rfc/htom-vs-spoke-clarification-2026-06.md" "owner: G-Ivan-A"
require_text "governance/rfc/htom-vs-spoke-clarification-2026-06.md" "rfc-scope: A"
require_text "governance/rfc/htom-vs-spoke-clarification-2026-06.md" "HTOM-команда"
require_text "governance/rfc/htom-vs-spoke-clarification-2026-06.md" "Spoke-репозиторий"
require_text "governance/rfc/htom-vs-spoke-clarification-2026-06.md" "open-ai.ru"
require_text "governance/rfc/htom-vs-spoke-clarification-2026-06.md" "templates/htom/"
require_text "governance/rfc/htom-vs-spoke-clarification-2026-06.md" "templates/spoke/"
require_text "governance/rfc/htom-vs-spoke-clarification-2026-06.md" "Сравнительная таблица"
require_text "governance/rfc/htom-vs-spoke-clarification-2026-06.md" "Обоснование разделения"
require_text "governance/rfc/htom-vs-spoke-clarification-2026-06.md" "Карта переименований"
require_text "governance/rfc/htom-vs-spoke-clarification-2026-06.md" "mango_ba_prompts"
require_text "governance/rfc/htom-vs-spoke-clarification-2026-06.md" "repo-development"
require_text "governance/rfc/htom-vs-spoke-clarification-2026-06.md" "Решение за человеком"

require_text "governance/rfc/knowledge-lifecycle-proposal.md" "status: draft"
require_text "governance/rfc/knowledge-lifecycle-proposal.md" "version: 0.2"
require_text "governance/rfc/knowledge-lifecycle-proposal.md" "Knowledge Lifecycle"
require_text "governance/rfc/knowledge-lifecycle-proposal.md" "standards/knowledge-lifecycle.md"
require_text "governance/rfc/knowledge-lifecycle-proposal.md" "Observation -> Research -> Hypothesis -> RFC -> Pattern -> Standard -> Template -> Framework -> Deprecation/Archive"
require_text "governance/rfc/knowledge-lifecycle-proposal.md" "Обратная трассируемость"
require_text "governance/rfc/knowledge-lifecycle-proposal.md" "traceability:"
require_text "governance/rfc/knowledge-lifecycle-proposal.md" "based_on:"
require_text "governance/rfc/knowledge-lifecycle-proposal.md" "supersedes:"
require_text "governance/rfc/knowledge-lifecycle-proposal.md" "used_by:"
require_text "governance/rfc/knowledge-lifecycle-proposal.md" "Проверка:"
require_text "governance/rfc/knowledge-lifecycle-proposal.md" "явное подтверждение Пользователя"
require_text "governance/rfc/resolve-artifact-location-proposal.md" "status: draft"
require_text "governance/rfc/resolve-artifact-location-proposal.md" "version: 0.2"
require_text "governance/rfc/resolve-artifact-location-proposal.md" "Resolve Artifact Location"
require_text "governance/rfc/resolve-artifact-location-proposal.md" "templates/resolve-artifact-location-prompt.md"
require_text "governance/rfc/resolve-artifact-location-proposal.md" "Hard violations"
require_text "governance/rfc/resolve-artifact-location-proposal.md" "Scope Resolver-а"
require_text "governance/rfc/resolve-artifact-location-proposal.md" "Куда положить этот артефакт?"
require_text "governance/rfc/resolve-artifact-location-proposal.md" "Каких upstream-зависимостей не хватает?"
require_text "governance/rfc/resolve-artifact-location-proposal.md" "Out of Scope"
require_text "governance/rfc/resolve-artifact-location-proposal.md" "явное подтверждение Пользователя"
require_text "governance/rfc/product-concept-template-proposal.md" "status: draft"
require_text "governance/rfc/product-concept-template-proposal.md" "version: 0.2"
require_text "governance/rfc/product-concept-template-proposal.md" "Universal Product Concept Template"
require_text "governance/rfc/product-concept-template-proposal.md" "templates/product-concept-template.md"
require_text "governance/rfc/product-concept-template-proposal.md" "L2 Framework-layer"
require_text "governance/rfc/product-concept-template-proposal.md" "explicit User approval"
require_text "governance/rfc/solution-concept-template-proposal.md" "status: draft"
require_text "governance/rfc/solution-concept-template-proposal.md" "version: 0.2"
require_text "governance/rfc/solution-concept-template-proposal.md" "Universal Solution Concept Template"
require_text "governance/rfc/solution-concept-template-proposal.md" "templates/solution-concept-template.md"
require_text "governance/rfc/solution-concept-template-proposal.md" "L3 Methodology-layer"
require_text "governance/rfc/solution-concept-template-proposal.md" "explicit User approval"

require_text "governance/agent-onboarding-protocol.md" "status: canonical"
require_text "governance/agent-onboarding-protocol.md" "version: 1.3"
require_text "governance/agent-onboarding-protocol.md" "updated: 2026-06-11"
require_text "governance/agent-onboarding-protocol.md" "executable: true"
require_text "governance/agent-onboarding-protocol.md" "entrypoint: true"
require_text "governance/agent-onboarding-protocol.md" "ЭТО ПРОТОКОЛ (ИНСТРУКЦИЯ). Не копируйте в чат."
require_text "governance/agent-onboarding-protocol.md" "ИСПОЛНИМЫЙ ДОКУМЕНТ — НЕ АНАЛИЗИРУЙ, ВЫПОЛНЯЙ"
require_text "governance/agent-onboarding-protocol.md" "EXECUTION"
require_text "governance/agent-onboarding-protocol.md" "EXPLANATION"
require_text "governance/agent-onboarding-protocol.md" "Handover Prompt"
require_text "governance/agent-onboarding-protocol.md" "{{REPO_NAME}}"
require_text "governance/agent-onboarding-protocol.md" "Readback"
require_text "governance/agent-onboarding-protocol.md" "Определи тип проекта"
require_text "governance/agent-onboarding-protocol.md" "Контекст чата диалога"
require_text "governance/agent-onboarding-protocol.md" "Проверка шаблонов"
require_text "governance/agent-onboarding-protocol.md" "Что может пойти не так"
require_text "governance/agent-onboarding-protocol.md" "standards/glossary.md"
require_text "governance/agent-onboarding-protocol.md" "Design Rationale & History"
require_text "governance/agent-onboarding-protocol.md" "rfc-two-cases-of-project-initialization.md"
require_text "governance/agent-onboarding-protocol.md" "templates/htom/README.md"
require_text "governance/agent-onboarding-protocol.md" "standards/session-handover-standard.md"

require_text "governance/artifact-map.md" "status: canonical"
require_text "governance/artifact-map.md" "version: 1.51"
require_text "governance/artifact-map.md" "templates/htom/AI_GOVERNANCE.md"
require_text "governance/artifact-map.md" "templates/spoke/README.md"
require_text "governance/artifact-map.md" "governance/rfc/htom-vs-spoke-clarification-2026-06.md"
require_text "governance/artifact-map.md" "updated: 2026-06-27"
require_text "governance/artifact-map.md" "temperature: 0.1"
require_text "governance/artifact-map.md" "governance/agent-onboarding-protocol.md"
require_text "governance/artifact-map.md" "docs/adr/2026-06-adr-001-ecosystem-infrastructure-methodology.md"
require_text "governance/artifact-map.md" "docs/adr/2026-06-adr-002-artifact-document-methodology.md"
require_text "governance/artifact-map.md" "governance/rfc/contract-executability-rfc.md"
require_text "governance/artifact-map.md" "governance/rfc/repository-quality-improvement-plan.md"
require_text "governance/artifact-map.md" "governance/rfc/draft-triage-and-exit-plan.md"
require_text "governance/artifact-map.md" "| Путь | Тип | 🚦 Исполнимый? | Назначение | Обязательный? | Связанные артефакты |"
require_text "governance/artifact-map.md" "🚦 entrypoint"
require_text "governance/artifact-map.md" "standards/project-structure-inheritance.md"
require_text "governance/artifact-map.md" "Как использовать карту"
require_text "governance/artifact-map.md" "Как обновлять карту"
require_text "governance/artifact-map.md" "glossary.md"
require_text "governance/artifact-map.md" "research/mango/2026-05-22-classification.md"
require_text "governance/artifact-map.md" "research/mango/2026-05-26-rag-mapping-roadmap.md"
require_text "governance/artifact-map.md" "research/hub/2026-05-28-project-context-and-bootstrap-patterns.md"
require_text "governance/artifact-map.md" "research/hub/2026-06-01-team-c-governance-strategy-audit.md"
require_text "governance/artifact-map.md" "research/hub/2026-05-28-user-prompts-analysis.md"
require_text "governance/artifact-map.md" "mango_ba_prompts"
require_text "governance/artifact-map.md" "projects/README.md"
require_text "governance/artifact-map.md" "governance/backlog.md"
require_text "governance/artifact-map.md" "governance/executable-documents-issues.md"
require_text "governance/artifact-map.md" "standards/frontmatter-standard.md"
require_text "governance/artifact-map.md" "standards/frontmatter-docs-standard.md"
require_text "governance/artifact-map.md" "standards/file-naming-convention.md"
require_text "governance/artifact-map.md" "standards/executable-documentation-standard.md"
require_text "governance/artifact-map.md" "standards/htom-documentation-structure.md"
require_text "governance/artifact-map.md" "research/hub/2026-06-12-ecosystem-governance-audit.md"
require_text "governance/artifact-map.md" "research/hub/2026-06-20-ecosystem-architecture-research.md"
require_text "governance/artifact-map.md" "research/hub/2026-06-12-external-practice-intake.md"
require_text "governance/artifact-map.md" "research/hub/2026-06-12-international-ai-governance-practices.md"
require_text "governance/artifact-map.md" "research/hub/2026-06-27-rfc-industry-norms-and-variants.md"
require_text "governance/artifact-map.md" "research/hub/2026-06-27-adr-industry-norms-and-variants.md"
require_text "governance/artifact-map.md" "research/hub/exp-rfc-adr-industry-norms/"
require_text "governance/artifact-map.md" "practices/README.md"
require_text "governance/artifact-map.md" "practices/ai-governance/nist-ai-rmf-profile-loop.md"
require_text "governance/artifact-map.md" ".github/ISSUE_TEMPLATE/task.md"
require_text "governance/artifact-map.md" ".github/ISSUE_TEMPLATE/task-creative.md"
require_text "governance/artifact-map.md" "templates/htom/.github/ISSUE_TEMPLATE/task-creative.md"
require_text "governance/artifact-map.md" "templates/spoke/docs/README.md"
require_text "governance/artifact-map.md" "templates/spoke/tools/validate-file-naming.sh"
require_text "governance/artifact-map.md" "templates/sync-project-with-hub-prompt.md"
require_text "governance/artifact-map.md" "tools/validate-file-naming.sh"
require_text "governance/artifact-map.md" ".github/workflows/validate.yml"
require_text "governance/artifact-map.md" "Уровни документации: Framework vs Methodology"
require_text "governance/artifact-map.md" "governance/rfc/knowledge-lifecycle-proposal.md"
require_text "governance/artifact-map.md" "governance/rfc/resolve-artifact-location-proposal.md"
require_text "governance/artifact-map.md" "governance/rfc/product-concept-template-proposal.md"
require_text "governance/artifact-map.md" "governance/rfc/solution-concept-template-proposal.md"
require_text "governance/artifact-map.md" "явного подтверждения"
require_text "governance/artifact-map.md" "Обратная трассируемость"
require_text "governance/artifact-map.md" "Framework vs Template"
require_text "governance/artifact-map.md" "Scope Resolver-а"
require_text "governance/artifact-map.md" "governance/session-digests.md"
reject_text "governance/artifact-map.md" "Конард"
reject_text "governance/artifact-map.md" "Фаундера"

require_text "governance/artifact-map.md" "research/external-knowledge/README.md"
require_text "governance/artifact-map.md" "research/external-knowledge/external-sources-registry.md"
require_text "governance/artifact-map.md" "research/external-knowledge/external-insights/README.md"
require_text "governance/artifact-map.md" "governance/rfc/external-knowledge-integration.md"

require_text "governance/rfc/README.md" "status: accepted"
require_text "governance/rfc/README.md" "version: 1.12"
require_text "governance/rfc/README.md" "updated: 2026-06-28"
require_text "governance/rfc/README.md" "owner: G-Ivan-A"

# External knowledge integration (issue #227): Base Registry + insights + RFC.
require_text "research/external-knowledge/README.md" "status: draft"
require_text "research/external-knowledge/README.md" "version: 0.3"
require_text "research/external-knowledge/README.md" "scope: repo-wide"
require_text "research/external-knowledge/README.md" "Base Registry"
require_text "research/external-knowledge/README.md" "external-sources-registry.md"
require_text "research/external-knowledge/README.md" "external-insights/"
require_text "research/external-knowledge/README.md" "Anti-Inflation"
require_text "research/external-knowledge/README.md" "Правила работы с внешними источниками"
require_text "research/external-knowledge/README.md" "Распознавание задачи"
require_text "research/external-knowledge/README.md" "Фиксация результата"
require_text "research/external-knowledge/README.md" "Чистота записей"
require_text "research/external-knowledge/README.md" "устарел"
require_text "research/external-knowledge/README.md" "future-phase: X"
require_text "research/external-knowledge/README.md" "topic: Y"
require_text "research/external-knowledge/README.md" "Повторный анализ инициирует только Пользователь"
require_text "research/external-knowledge/README.md" "отклонено"

require_text "research/external-knowledge/external-sources-registry.md" "status: draft"
require_text "research/external-knowledge/external-sources-registry.md" "version: 0.9"
require_text "research/external-knowledge/external-sources-registry.md" "type: external-analysis"
require_text "research/external-knowledge/external-sources-registry.md" "scope: repo-wide"
require_text "research/external-knowledge/external-sources-registry.md" "Минимальные метаданные"
require_text "research/external-knowledge/external-sources-registry.md" "ext-001"
require_text "research/external-knowledge/external-sources-registry.md" "Anti-Inflation"
require_text "research/external-knowledge/external-sources-registry.md" "Запись в БЗ"
require_text "research/external-knowledge/external-sources-registry.md" "Теги будущих фаз / тем"
require_text "research/external-knowledge/external-sources-registry.md" "| \`id\` | Источник | Тип | Язык | Теги | Теги будущих фаз / тем | Stage | Проекты | Запись в БЗ |"
require_text "research/external-knowledge/external-sources-registry.md" "ext-009"
require_text "research/external-knowledge/external-sources-registry.md" "ext-011"
require_text "research/external-knowledge/external-sources-registry.md" "ext-015"
require_text "research/external-knowledge/external-sources-registry.md" "ext-016"
require_text "research/external-knowledge/external-sources-registry.md" "ext-024"
require_text "research/external-knowledge/external-sources-registry.md" "ext-025"
require_text "research/external-knowledge/external-sources-registry.md" "ext-048"
require_text "research/external-knowledge/external-sources-registry.md" "ext-066"
require_text "research/external-knowledge/external-sources-registry.md" "ext-075"
require_text "research/external-knowledge/external-sources-registry.md" "ext-126"

require_text "research/external-knowledge/external-insights/README.md" "status: draft"
require_text "research/external-knowledge/external-insights/README.md" "source_id"
require_text "research/external-knowledge/external-insights/README.md" "observation"
require_text "research/external-knowledge/external-insights/README.md" "candidate-practice"
require_text "research/external-knowledge/external-insights/README.md" "Стоп-правило"

require_text "governance/rfc/external-knowledge-integration.md" "status: draft"
require_text "governance/rfc/external-knowledge-integration.md" "version: 0.1"
require_text "governance/rfc/external-knowledge-integration.md" "Base Registry"
require_text "governance/rfc/external-knowledge-integration.md" "Local Extension"
require_text "governance/rfc/external-knowledge-integration.md" "Smart Sync"
require_text "governance/rfc/external-knowledge-integration.md" "Creative override"
require_text "governance/rfc/external-knowledge-integration.md" "clarify-engine-ai"
require_text "governance/rfc/external-knowledge-integration.md" "Open Decision"

# Documentation architecture balance (issue #231): Index/Summary/Full framework.
require_text "governance/artifact-map.md" "governance/rfc/documentation-architecture-balance.md"
require_text "governance/rfc/README.md" "documentation-architecture-balance.md"
require_text "governance/rfc/documentation-architecture-balance.md" "status: draft"
require_text "governance/rfc/documentation-architecture-balance.md" "version: 0.1"
require_text "governance/rfc/documentation-architecture-balance.md" "Anti-Inflation"
require_text "governance/rfc/documentation-architecture-balance.md" "Index"
require_text "governance/rfc/documentation-architecture-balance.md" "Summary"
require_text "governance/rfc/documentation-architecture-balance.md" "clarify-engine-ai"
require_text "governance/rfc/documentation-architecture-balance.md" "Open Decision"

# Research Memory & Source Intelligence (issue #239): object-centric memory layer.
require_text "governance/artifact-map.md" "governance/rfc/research-memory-source-intelligence.md"
require_text "governance/rfc/README.md" "research-memory-source-intelligence.md"
require_text "governance/rfc/research-memory-source-intelligence.md" "status: draft"
require_text "governance/rfc/research-memory-source-intelligence.md" "version: 0.1"
require_text "governance/rfc/research-memory-source-intelligence.md" "Knowledge Object первичен"
require_text "governance/rfc/research-memory-source-intelligence.md" "Анализ Необходимости"
require_text "governance/rfc/research-memory-source-intelligence.md" "Tier 1: External Trusted Sources"
require_text "governance/rfc/research-memory-source-intelligence.md" "Tier 2: Internal Research Memory"
require_text "governance/rfc/research-memory-source-intelligence.md" "Observed"
require_text "governance/rfc/research-memory-source-intelligence.md" "Candidate"
require_text "governance/rfc/research-memory-source-intelligence.md" "Applied"
require_text "governance/rfc/research-memory-source-intelligence.md" "Rejected"
require_text "governance/rfc/research-memory-source-intelligence.md" "Superseded"
require_text "governance/rfc/research-memory-source-intelligence.md" "Source Intelligence"
require_text "governance/rfc/research-memory-source-intelligence.md" "Context Engineering"
require_text "governance/rfc/research-memory-source-intelligence.md" "clarify-engine-ai"
require_text "governance/rfc/research-memory-source-intelligence.md" "Open Decisions"

# Repository archetypes, Prompt & Pattern Library template and release strategy (issue #240).
require_text "governance/artifact-map.md" "governance/rfc/repository-archetypes-template-release.md"
require_text "governance/rfc/README.md" "repository-archetypes-template-release.md"
require_text "governance/rfc/repository-archetypes-template-release.md" "status: draft"
require_text "governance/rfc/repository-archetypes-template-release.md" "version: 0.1"
require_text "governance/rfc/repository-archetypes-template-release.md" "Почему текущей ситуации недостаточно"
require_text "governance/rfc/repository-archetypes-template-release.md" "Анализ внешних эталонов структуры"
require_text "governance/rfc/repository-archetypes-template-release.md" "Анализ моделей Release Engineering"
require_text "governance/rfc/repository-archetypes-template-release.md" "Таксономия архетипов"
require_text "governance/rfc/repository-archetypes-template-release.md" "Project Template для Prompt & Pattern Library"
require_text "governance/rfc/repository-archetypes-template-release.md" "Маппинг mango_ba_prompts"
require_text "governance/rfc/repository-archetypes-template-release.md" "Правило синхронизации Governance"
require_text "governance/rfc/repository-archetypes-template-release.md" "GitHub Flow"
require_text "governance/rfc/repository-archetypes-template-release.md" "GitFlow"
require_text "governance/rfc/repository-archetypes-template-release.md" "Trunk-Based Development"
require_text "governance/rfc/repository-archetypes-template-release.md" "GitHub Pages"

# Methodology research & proposals for Hub/Mango/Open-AI (issue #245): six methodologies + three proposals.
require_text "governance/artifact-map.md" "governance/rfc/methodology-research-and-proposals.md"
require_text "governance/rfc/README.md" "methodology-research-and-proposals.md"
require_text "governance/rfc/methodology-research-and-proposals.md" "status: draft"
require_text "governance/rfc/methodology-research-and-proposals.md" "version: 0.1"
require_text "governance/rfc/methodology-research-and-proposals.md" "Почему текущей ситуации недостаточно"
require_text "governance/rfc/methodology-research-and-proposals.md" "Анализ шести методологий"
require_text "governance/rfc/methodology-research-and-proposals.md" "Enterprise Intelligence Methodology"
require_text "governance/rfc/methodology-research-and-proposals.md" "Opportunity Discovery Framework"
require_text "governance/rfc/methodology-research-and-proposals.md" "Human-AI Collaboration Model"
require_text "governance/rfc/methodology-research-and-proposals.md" "Trust & Evidence Framework"
require_text "governance/rfc/methodology-research-and-proposals.md" "Influence & Network Analysis"
require_text "governance/rfc/methodology-research-and-proposals.md" "AI Solution Architecture"
require_text "governance/rfc/methodology-research-and-proposals.md" "Сравнение с существующими RFC"
require_text "governance/rfc/methodology-research-and-proposals.md" "Подтверждение и расширение предложения фаундера"
require_text "governance/rfc/methodology-research-and-proposals.md" "Три независимых предложения"
require_text "governance/rfc/methodology-research-and-proposals.md" "Консистентность и переиспользование"
require_text "governance/rfc/methodology-research-and-proposals.md" "mango_ba_prompts"
require_text "governance/rfc/methodology-research-and-proposals.md" "open-ai.ru"
require_text "governance/rfc/methodology-research-and-proposals.md" "Open Decisions"

# Wigers requirements research + AI-era RFC (issue #247): independent extraction + mango sync.
require_text "governance/artifact-map.md" "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md"
require_text "governance/artifact-map.md" "research/mango/2026-06-18-requirements-engineering-ai-era.md"
require_text "research/external-knowledge/README.md" "2026-06-18-wigers-requirements-analysis.md"
require_text "research/mango/README.md" "2026-06-18-requirements-engineering-ai-era.md"
# Research doc: independent bilingual Wiegers extraction (FT-1..FT-4).
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "status: draft"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "version: 0.2"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "type: external-analysis"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "Requirement levels"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "Requirement types"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "Business rule"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "Quality attribute"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "Requirements development"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "Requirements management"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "Активаторы операций"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "Вычисления"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "Vision and Scope"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "Software Requirements Specification"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "ISO/IEC/IEEE 29148"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "MoSCoW"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "prompt engineering"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "User Story"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "Use Case"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "Candidate"
# Issue #249 additions: classifications comparison + open-questions-at-end.
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "BABOK"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "CrewAI"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "Сравнение классификаций"
require_text "research/external-knowledge/2026-06-18-wigers-requirements-analysis.md" "ОВ‑4"
# RFC: Wiegers <-> mango-ADR sync (FT-5) with honest reinvention gradation.
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "status: draft"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "version: 0.2"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "RFC: Requirements Engineering in the AI Era"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "Decision Scope"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "Карта сравнения"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "mango_ba_prompts"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "велосипед"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "requirement_level"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "Бизнес-правило"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "ГОСТ 34.602-2020"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "crosswalk"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "Trust & Evidence"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "Candidate"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "Anti-Inflation"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "Acceptance Criteria"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "Open Decisions"
# Issue #249 additions: prompt = interface to Tool, prompt-engineering subprocess, AI-agent processes.
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "Инжиниринг промптов"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "Prompt specification"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "Разработка AI-агента"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "Настройка RAG"
require_text "research/mango/2026-06-18-requirements-engineering-ai-era.md" "Оркестрация агентов"

# Index/Summary format improvement (issue #237): phase dates + future horizons.
require_text "docs/ecosystem-map-Index.md" "version: 0.2"
require_text "docs/ecosystem-map-Index.md" "Дата актуализации фазы"
require_text "docs/ecosystem-map-Index.md" "| Проект | URL | Текущая фаза | Дата актуализации фазы | Ключевые теги | Ссылка на Summary |"
require_text "docs/ecosystem-map-Index.md" "| hybrid-Intelligence-lab (Хаб) | [github](https://github.com/G-Ivan-A/hybrid-Intelligence-lab) | Sprint 3 «Hybrid Minimum Bootstrap» | 2026-06-15 |"
require_text "docs/ecosystem-map-Index.md" "| mango_ba_prompts | [github](https://github.com/G-Ivan-A/mango_ba_prompts) | Фаза 1 — миграция в standalone-спок | 2026-06-15 |"
require_text "docs/ecosystem-map-Index.md" "| open-ai.ru | [github](https://github.com/G-Ivan-A/open-ai.ru) | Phase 0 — Planning & Vision | 2026-06-15 |"
require_text "docs/ecosystem-map-Index.md" "| clarify-engine-ai | [github](https://github.com/G-Ivan-A/clarify-engine-ai) | MVP/Pilot — CONCEPT v2.6 Approved | 2026-06-15 |"
require_text "AI_PROJECT_CONTEXT-Summary.md" "version: 0.2"
require_text "AI_PROJECT_CONTEXT-Summary.md" "Горизонты / Актуально для будущих фаз"
require_text "AI_PROJECT_CONTEXT-Summary.md" "мультиагент"
require_text "AI_PROJECT_CONTEXT-Summary.md" "графовой структуре связей"

require_text "governance/session-digests.md" "status: draft"
require_text "governance/session-digests.md" "version: 0.3"
require_text "governance/session-digests.md" "updated: 2026-06-13"
require_text "governance/session-digests.md" "temperature: 0.1"
require_text "governance/session-digests.md" "Контекст"
require_text "governance/session-digests.md" "Решения"
require_text "governance/session-digests.md" "Открытые вопросы"
require_text "governance/session-digests.md" "Следующие шаги"
require_text "governance/session-digests.md" "Индекс"
require_text "governance/session-digests.md" "2026-06-13"
require_text "governance/session-digests.md" "Anti-Inflation"
require_text "governance/session-digests.md" "Разложение на проектные репо"
require_text "governance/session-digests.md" "governance/backlog.md"
reject_text "governance/session-digests.md" "Конард"

require_text "governance/backlog.md" "status: canonical"
require_text "governance/backlog.md" "version: 1.4"
require_text "governance/backlog.md" "type: backlog"
require_text "governance/backlog.md" "standards/glossary.md"
require_text "governance/backlog.md" "## Открытые вопросы"
require_text "governance/backlog.md" "| Дата | Источник | Суть | Статус | Связанные дайджесты | Связанный артефакт |"
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
reject_text "governance/backlog.md" "Конард"

require_text "research/README.md" "status: canonical"
require_text "research/README.md" "standards/research-profile.md"
require_text "research/README.md" "research/<domain>/exp-<slug>/"
require_text "research/README.md" "2026-05-28-project-context-and-bootstrap-patterns.md"
require_text "research/README.md" "2026-05-28-prompts-classification-audit.md"
require_text "research/README.md" "2026-05-28-prompts-classification-standard.md"
require_text "research/README.md" "2026-06-01-team-c-governance-strategy-audit.md"
require_text "research/README.md" "2026-05-28-user-prompts-analysis.md"
require_text "research/README.md" "2026-06-12-ecosystem-governance-audit.md"
require_text "research/README.md" "2026-06-20-ecosystem-architecture-research.md"
require_text "research/README.md" "2026-06-12-external-practice-intake.md"
require_text "research/README.md" "2026-06-12-international-ai-governance-practices.md"
require_text "research/README.md" "2026-06-27-rfc-industry-norms-and-variants.md"
require_text "research/README.md" "2026-06-27-adr-industry-norms-and-variants.md"
require_text "research/README.md" "Размещение файлов исследований в корне каталога"

# Namespacing: no research files allowed in the research/ root except README.md.
while IFS= read -r research_root_file; do
  base="${research_root_file##*/}"
  if [[ "$base" != "README.md" ]]; then
    fail "research root must only contain README.md; found: $research_root_file"
  fi
done < <(find research -maxdepth 1 -type f)

require_text "research/hub/README.md" "status: canonical"
require_text "research/hub/README.md" "2026-05-28-project-context-and-bootstrap-patterns.md"
require_text "research/hub/README.md" "2026-05-28-prompts-classification-audit.md"
require_text "research/hub/README.md" "2026-05-28-prompts-classification-standard.md"
require_text "research/hub/README.md" "2026-06-01-team-c-governance-strategy-audit.md"
require_text "research/hub/README.md" "2026-05-28-user-prompts-analysis.md"
require_text "research/hub/README.md" "2026-06-12-ecosystem-governance-audit.md"
require_text "research/hub/README.md" "2026-06-20-ecosystem-architecture-research.md"
require_text "research/hub/README.md" "2026-06-12-external-practice-intake.md"
require_text "research/hub/README.md" "2026-06-12-international-ai-governance-practices.md"
require_text "research/hub/README.md" "2026-06-27-rfc-industry-norms-and-variants.md"
require_text "research/hub/README.md" "2026-06-27-adr-industry-norms-and-variants.md"
require_text "research/hub/README.md" "exp-rfc-adr-industry-norms/"

require_text "research/hub/2026-06-27-rfc-industry-norms-and-variants.md" "status: draft"
require_text "research/hub/2026-06-27-rfc-industry-norms-and-variants.md" "version: 0.1"
require_text "research/hub/2026-06-27-rfc-industry-norms-and-variants.md" "updated: 2026-06-27"
require_text "research/hub/2026-06-27-rfc-industry-norms-and-variants.md" "temperature: 0.1"
require_text "research/hub/2026-06-27-rfc-industry-norms-and-variants.md" "issue #278"
require_text "research/hub/2026-06-27-rfc-industry-norms-and-variants.md" "Mango"
require_text "research/hub/2026-06-27-rfc-industry-norms-and-variants.md" "Архетип A"
require_text "research/hub/2026-06-27-rfc-industry-norms-and-variants.md" "lifecycle"
require_text "research/hub/2026-06-27-rfc-industry-norms-and-variants.md" "Rust"
require_text "research/hub/2026-06-27-rfc-industry-norms-and-variants.md" "Kubernetes"
require_text "research/hub/2026-06-27-rfc-industry-norms-and-variants.md" "2026-06-27-rfc-external-tree-summary.md"

require_text "research/hub/2026-06-27-adr-industry-norms-and-variants.md" "status: draft"
require_text "research/hub/2026-06-27-adr-industry-norms-and-variants.md" "version: 0.1"
require_text "research/hub/2026-06-27-adr-industry-norms-and-variants.md" "updated: 2026-06-27"
require_text "research/hub/2026-06-27-adr-industry-norms-and-variants.md" "temperature: 0.1"
require_text "research/hub/2026-06-27-adr-industry-norms-and-variants.md" "issue #278"
require_text "research/hub/2026-06-27-adr-industry-norms-and-variants.md" "Mango"
require_text "research/hub/2026-06-27-adr-industry-norms-and-variants.md" "decision records"
require_text "research/hub/2026-06-27-adr-industry-norms-and-variants.md" "superseded"
require_text "research/hub/2026-06-27-adr-industry-norms-and-variants.md" "MADR"
require_text "research/hub/2026-06-27-adr-industry-norms-and-variants.md" "Backstage"
require_text "research/hub/2026-06-27-adr-industry-norms-and-variants.md" "2026-06-27-adr-external-tree-summary.md"

require_text "research/hub/exp-rfc-adr-industry-norms/README.md" "status: draft"
require_text "research/hub/exp-rfc-adr-industry-norms/README.md" "type: experiment"
require_text "research/hub/exp-rfc-adr-industry-norms/README.md" "collect-evidence.py"
require_text "research/hub/exp-rfc-adr-industry-norms/README.md" "2026-06-27-local-rfc-adr-audit.md"
require_text "research/hub/exp-rfc-adr-industry-norms/README.md" "2026-06-27-rfc-external-tree-summary.md"
require_text "research/hub/exp-rfc-adr-industry-norms/README.md" "2026-06-27-adr-external-tree-summary.md"

require_text "research/hub/2026-06-12-ecosystem-governance-audit.md" "status: draft"
require_text "research/hub/2026-06-12-ecosystem-governance-audit.md" "version: 0.1"
require_text "research/hub/2026-06-12-ecosystem-governance-audit.md" "updated: 2026-06-12"
require_text "research/hub/2026-06-12-ecosystem-governance-audit.md" "temperature: 0.1"
require_text "research/hub/2026-06-12-ecosystem-governance-audit.md" "mango_ba_prompts"
require_text "research/hub/2026-06-12-ecosystem-governance-audit.md" "open-ai.ru"
require_text "research/hub/2026-06-12-ecosystem-governance-audit.md" "clarify-engine-ai"
require_text "research/hub/2026-06-12-ecosystem-governance-audit.md" "NIST AI RMF"
require_text "research/hub/2026-06-12-ecosystem-governance-audit.md" "EU AI Act"
require_text "research/hub/2026-06-12-ecosystem-governance-audit.md" "Creative override"

require_text "research/hub/2026-06-20-ecosystem-architecture-research.md" "status: draft"
require_text "research/hub/2026-06-20-ecosystem-architecture-research.md" "version: 0.1"
require_text "research/hub/2026-06-20-ecosystem-architecture-research.md" "updated: 2026-06-20"
require_text "research/hub/2026-06-20-ecosystem-architecture-research.md" "temperature: 0.1"
require_text "research/hub/2026-06-20-ecosystem-architecture-research.md" "open-ai.ru"
require_text "research/hub/2026-06-20-ecosystem-architecture-research.md" "mango_ba_prompts"
require_text "research/hub/2026-06-20-ecosystem-architecture-research.md" "clarify-engine-ai"
require_text "research/hub/2026-06-20-ecosystem-architecture-research.md" "репутационные технологии"
require_text "research/hub/2026-06-20-ecosystem-architecture-research.md" "Executable -> Summary -> Full -> Raw"
require_text "research/hub/2026-06-20-ecosystem-architecture-research.md" "Проверка требований issue #257"

require_text "research/hub/2026-06-12-external-practice-intake.md" "status: draft"
require_text "research/hub/2026-06-12-external-practice-intake.md" "version: 0.1"
require_text "research/hub/2026-06-12-external-practice-intake.md" "updated: 2026-06-12"
require_text "research/hub/2026-06-12-external-practice-intake.md" "temperature: 0.1"
require_text "research/hub/2026-06-12-external-practice-intake.md" "Artem Chirkov"
require_text "research/hub/2026-06-12-external-practice-intake.md" "slam"
require_text "research/hub/2026-06-12-external-practice-intake.md" "Research vs fixed practices"
require_text "research/hub/2026-06-12-external-practice-intake.md" "Mango docs error pattern"
require_text "research/hub/2026-06-12-external-practice-intake.md" "practices/agent-work/hybrid-search-before-action.md"

require_text "research/hub/2026-06-12-international-ai-governance-practices.md" "status: draft"
require_text "research/hub/2026-06-12-international-ai-governance-practices.md" "version: 0.1"
require_text "research/hub/2026-06-12-international-ai-governance-practices.md" "updated: 2026-06-12"
require_text "research/hub/2026-06-12-international-ai-governance-practices.md" "temperature: 0.1"
require_text "research/hub/2026-06-12-international-ai-governance-practices.md" "NIST AI RMF"
require_text "research/hub/2026-06-12-international-ai-governance-practices.md" "EU AI Act"
require_text "research/hub/2026-06-12-international-ai-governance-practices.md" "ISO/IEC 42001"
require_text "research/hub/2026-06-12-international-ai-governance-practices.md" "OpenAI"
require_text "research/hub/2026-06-12-international-ai-governance-practices.md" "Anthropic"
require_text "research/hub/2026-06-12-international-ai-governance-practices.md" "Google SAIF"
require_text "research/hub/2026-06-12-international-ai-governance-practices.md" "Executable implementation matrix"
require_text "research/hub/2026-06-12-international-ai-governance-practices.md" "practices/ai-governance/nist-ai-rmf-profile-loop.md"

require_text "research/governance/README.md" "status: reviewed"
require_text "research/governance/README.md" "version: 0.2"
require_text "research/governance/README.md" "Active standards"
require_text "research/governance/README.md" "Source research"
require_text "research/governance/README.md" "Derived standards"

require_text "research/mango/README.md" "status: canonical"
require_text "research/mango/README.md" "2026-05-22-classification.md"
require_text "research/mango/README.md" "2026-05-22-requirements-flow.md"
require_text "research/mango/README.md" "2026-05-26-rag-mapping-roadmap.md"
require_text "research/mango/README.md" "research/mango/exp-tz-corpus/"

require_text "research/mango/2026-05-22-classification.md" "status: reviewed"
require_text "research/mango/2026-05-22-classification.md" "source: git history before migration to research/mango/2026-05-22-classification.md"
require_text "research/mango/2026-05-22-classification-tz.md" "status: reviewed"
require_text "research/mango/2026-05-22-classification-tz.md" "source: git history before migration to research/mango/2026-05-22-classification-tz.md"
require_text "research/mango/2026-05-22-requirements-flow.md" "status: reviewed"
require_text "research/mango/2026-05-22-requirements-flow.md" "source: git history before migration to research/mango/2026-05-22-requirements-flow.md"
require_text "research/mango/2026-05-26-rag-mapping-roadmap.md" "status: draft"
require_text "research/mango/2026-05-26-rag-mapping-roadmap.md" "type: process-research"
require_text "research/mango/2026-05-26-rag-mapping-roadmap.md" "Маппинг продуктов/фич"
require_text "research/mango/2026-05-26-rag-mapping-roadmap.md" "Roadmap реализации проекта"
require_text "research/mango/2026-05-26-rag-mapping-roadmap.md" "PlantUML"
require_text "research/mango/2026-05-26-rag-mapping-roadmap.md" "Вопросы для согласования"

require_text "research/hub/2026-05-28-project-context-and-bootstrap-patterns.md" "status: draft"
require_text "research/hub/2026-05-28-project-context-and-bootstrap-patterns.md" "type: internal-analysis"
require_text "research/hub/2026-05-28-project-context-and-bootstrap-patterns.md" "scope: repo-wide"
require_text "research/hub/2026-05-28-project-context-and-bootstrap-patterns.md" "Опыт проекта Mango"
require_text "research/hub/2026-05-28-project-context-and-bootstrap-patterns.md" "Проблемы (5 пунктов"
require_text "research/hub/2026-05-28-project-context-and-bootstrap-patterns.md" "Предложенные решения"
require_text "research/hub/2026-05-28-project-context-and-bootstrap-patterns.md" "Чек-лист для ИИ"
require_text "research/hub/2026-05-28-project-context-and-bootstrap-patterns.md" "Механизм «рекомендация → задача»"
require_text "research/hub/2026-05-28-project-context-and-bootstrap-patterns.md" "Вопросы для согласования"

require_text "research/hub/2026-05-28-prompts-classification-audit.md" "status: draft"
require_text "research/hub/2026-05-28-prompts-classification-audit.md" "type: internal-analysis"
require_text "research/hub/2026-05-28-prompts-classification-audit.md" "scope: repo-wide"
require_text "research/hub/2026-05-28-prompts-classification-audit.md" "Преобладающие типы"
require_text "research/hub/2026-05-28-prompts-classification-audit.md" "Паттерны отладки"
require_text "research/hub/2026-05-28-prompts-classification-audit.md" "Пробелы"
require_text "research/hub/2026-05-28-prompts-classification-audit.md" "Выводы для классификации"

require_text "research/hub/2026-05-28-prompts-classification-standard.md" "status: draft"
require_text "research/hub/2026-05-28-prompts-classification-standard.md" "type: classification-standard"
require_text "research/hub/2026-05-28-prompts-classification-standard.md" "scope: repo-wide"
require_text "research/hub/2026-05-28-prompts-classification-standard.md" "Таксономия промптов"
require_text "research/hub/2026-05-28-prompts-classification-standard.md" "Матрица"
require_text "research/hub/2026-05-28-prompts-classification-standard.md" "Когда использовать"
require_text "research/hub/2026-05-28-prompts-classification-standard.md" "Шаблоны промптов"
require_text "research/hub/2026-05-28-prompts-classification-standard.md" "План интеграции"
require_text "research/hub/2026-05-28-prompts-classification-standard.md" "Вопросы для согласования"

require_text "research/hub/2026-06-01-team-c-governance-strategy-audit.md" "status: draft"
require_text "research/hub/2026-06-01-team-c-governance-strategy-audit.md" "type: internal-analysis"
require_text "research/hub/2026-06-01-team-c-governance-strategy-audit.md" "scope: repo-wide"
require_text "research/hub/2026-06-01-team-c-governance-strategy-audit.md" "Интерпретация аудита стратегии governance"
require_text "research/hub/2026-06-01-team-c-governance-strategy-audit.md" "Governance overgrowth"
require_text "research/hub/2026-06-01-team-c-governance-strategy-audit.md" "Предложения команды C"
require_text "research/hub/2026-06-01-team-c-governance-strategy-audit.md" "Рекомендации для backlog"
require_text "research/hub/2026-06-01-team-c-governance-strategy-audit.md" "Вопросы для human review"

require_text "research/hub/2026-06-02-external-governance-patterns-review.md" "status: draft"
require_text "research/hub/2026-06-02-external-governance-patterns-review.md" "type: external-analysis"
require_text "research/hub/2026-06-02-external-governance-patterns-review.md" "scope: repo-wide"
require_text "research/hub/2026-06-02-external-governance-patterns-review.md" "Что ценного в рекомендациях Команды С"
require_text "research/hub/2026-06-02-external-governance-patterns-review.md" "Матрица применимости"
require_text "research/hub/2026-06-02-external-governance-patterns-review.md" "ВЗЯТЬ СЕЙЧАС"
require_text "research/hub/2026-06-02-external-governance-patterns-review.md" "ОТЛОЖИТЬ"
require_text "research/hub/2026-06-02-external-governance-patterns-review.md" "ОТКЛОНИТЬ"
require_text "research/hub/2026-06-02-external-governance-patterns-review.md" "North Star"
require_text "research/hub/2026-06-02-external-governance-patterns-review.md" "Триггеры для пересмотра матрицы"

require_text "research/hub/2026-05-28-user-prompts-analysis.md" "status: draft"
require_text "research/hub/2026-05-28-user-prompts-analysis.md" "type: prompt-analysis"
require_text "research/hub/2026-05-28-user-prompts-analysis.md" "scope: user-specific + repo-integration"
require_text "research/hub/2026-05-28-user-prompts-analysis.md" "Таблица классификации 18 промптов"
require_text "research/hub/2026-05-28-user-prompts-analysis.md" "Признаки устаревших паттернов"
require_text "research/hub/2026-05-28-user-prompts-analysis.md" "Дубли/уникальная ценность"
require_text "research/hub/2026-05-28-user-prompts-analysis.md" "Рекомендации по действиям"
require_text "research/hub/2026-05-28-user-prompts-analysis.md" "План интеграции"
require_text "research/hub/2026-05-28-user-prompts-analysis.md" "Вопросы для согласования"

require_text "research/mango/2026-05-27-capability-decomposition.md" "status: draft"
require_text "research/mango/2026-05-27-capability-decomposition.md" "type: atomic-functions-reference"
require_text "research/mango/2026-05-27-capability-decomposition.md" "scope: mango-only"
require_text "research/mango/2026-05-27-capability-decomposition.md" "# Fixed per draft-triage RFC Phase 1"
require_text "research/mango/2026-05-27-capability-decomposition.md" "research/mango/2026-05-22-classification.md"
require_text "research/mango/2026-05-27-capability-decomposition.md" "https://github.com/G-Ivan-A/mango_ba_prompts/blob/main/standards/GLOSSARY.md"
require_text "research/mango/2026-05-27-capability-decomposition.md" "Критерии атомарности"
require_text "research/mango/2026-05-27-capability-decomposition.md" "Связь с НФТ-классами"
require_text "research/mango/2026-05-27-capability-decomposition.md" "Интеграция с"
require_text "research/mango/2026-05-27-capability-decomposition.md" "Как обновлять справочник"
require_text "research/mango/2026-05-27-capability-decomposition.md" "Вопросы для согласования с PO/Founder"
require_text "research/mango/2026-05-27-capability-decomposition.md" "Domain: voice-ucaas"
require_text "research/mango/2026-05-27-capability-decomposition.md" "Domain: contact-center"
require_text "research/mango/2026-05-27-capability-decomposition.md" "Domain: digital-channels"
if grep -Fq 'classification-glossary.md' "research/mango/2026-05-27-capability-decomposition.md"; then
  fail "research/mango/2026-05-27-capability-decomposition.md must not reference removed local classification-glossary.md"
fi
if grep -Fq '"2026-05-22-classification.md v3.0"' "research/mango/2026-05-27-capability-decomposition.md"; then
  fail "research/mango/2026-05-27-capability-decomposition.md related_artifacts must use path-only values"
fi

require_text "practices/README.md" "status: canonical"
require_text "practices/README.md" "version: 1.0"
require_text "practices/README.md" "updated: 2026-06-12"
require_text "practices/README.md" "temperature: 0.1"
require_text "practices/README.md" "Research vs fixed practices"
require_text "practices/README.md" "Practice catalog"
require_text "practices/README.md" "Source, author, link"
require_text "practices/README.md" "research/hub/2026-06-12-external-practice-intake.md"
require_text "practices/README.md" "research/hub/2026-06-12-international-ai-governance-practices.md"

require_text "practices/agent-work/README.md" "status: canonical"
require_text "practices/agent-work/README.md" "Hybrid search before action"
require_text "practices/agent-work/README.md" "Definition of Ready check"
require_text "practices/agent-work/README.md" "Plan-verify-ship loop"
require_text "practices/agent-work/README.md" "Skills as reusable workflows"
require_text "practices/agent-work/README.md" "Skill catalog token budget"
require_text "practices/agent-work/hybrid-search-before-action.md" "status: canonical"
require_text "practices/agent-work/hybrid-search-before-action.md" "Artem Chirkov"
require_text "practices/agent-work/hybrid-search-before-action.md" "structured search"
require_text "practices/agent-work/definition-of-ready-check.md" "status: canonical"
require_text "practices/agent-work/definition-of-ready-check.md" "Definition of Ready"
require_text "practices/agent-work/plan-verify-ship-loop.md" "status: canonical"
require_text "practices/agent-work/plan-verify-ship-loop.md" "Explore -> Plan -> Code -> Test -> Review -> Ship"
require_text "practices/agent-work/skills-as-reusable-workflows.md" "status: canonical"
require_text "practices/agent-work/skills-as-reusable-workflows.md" "slam"
require_text "practices/agent-work/skill-catalog-token-budget.md" "status: canonical"
require_text "practices/agent-work/skill-catalog-token-budget.md" "91,000+"

require_text "practices/ai-governance/README.md" "status: canonical"
require_text "practices/ai-governance/README.md" "NIST AI RMF profile loop"
require_text "practices/ai-governance/README.md" "EU AI Act risk tiering"
require_text "practices/ai-governance/README.md" "ISO/IEC 42001 management loop"
require_text "practices/ai-governance/README.md" "OpenAI evaluation and feedback loop"
require_text "practices/ai-governance/README.md" "Anthropic capability thresholds"
require_text "practices/ai-governance/README.md" "Google SAIF agent security"
require_text "practices/ai-governance/nist-ai-rmf-profile-loop.md" "status: canonical"
require_text "practices/ai-governance/nist-ai-rmf-profile-loop.md" "Map, Measure, Manage, Govern"
require_text "practices/ai-governance/eu-ai-act-risk-tiering.md" "status: canonical"
require_text "practices/ai-governance/eu-ai-act-risk-tiering.md" "risk tier"
require_text "practices/ai-governance/iso-42001-management-loop.md" "status: canonical"
require_text "practices/ai-governance/iso-42001-management-loop.md" "management system"
require_text "practices/ai-governance/openai-evaluation-and-feedback-loop.md" "status: canonical"
require_text "practices/ai-governance/openai-evaluation-and-feedback-loop.md" "evaluations"
require_text "practices/ai-governance/anthropic-capability-thresholds.md" "status: canonical"
require_text "practices/ai-governance/anthropic-capability-thresholds.md" "Responsible Scaling Policy"
require_text "practices/ai-governance/google-saif-agent-security.md" "status: canonical"
require_text "practices/ai-governance/google-saif-agent-security.md" "SAIF"

require_text "projects/README.md" "status: canonical"
require_text "projects/README.md" "Мигрировавшие проекты"
require_text "projects/README.md" "mango_ba_prompts"
require_text "projects/README.md" "repo-development/"

require_text "projects/repo-development/README.md" "mango-ba-prompts-repository-migration-plan-2026-06.md"
require_text "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md" "status: draft"
require_text "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md" "version: 0.2"
require_text "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md" "Issue #241"
require_text "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md" "Task 2 RFC"
require_text "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md" "Prompt & Pattern Library"
require_text "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md" "GitHub Flow + trunk discipline"
require_text "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md" "Scenario A"
require_text "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md" "Scenario B"
require_text "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md" "governance/BACKLOG.md"
require_text "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md" "scripts/validation/"
require_text "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md" "prompts/experiments/"
require_text "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md" "PR #90"
require_text "governance/artifact-map.md" "projects/repo-development/docs/mango-ba-prompts-repository-migration-plan-2026-06.md"

require_text "education/README.md" "status: canonical"
require_text "education/README.md" "standards/education-profile.md"

require_text "frameworks/README.md" "status: canonical"
require_text "frameworks/README.md" "governance/repo-model.md"

require_text "projects/education-ba-prompt/README.md" "status: draft"
require_text "projects/education-ba-prompt/README.md" "version: 0.1"
require_text "projects/education-ba-prompt/README.md" "updated: 2026-05-26"
require_text "projects/education-ba-prompt/README.md" "## Scope: Sandbox"
require_text "projects/education-ba-prompt/README.md" "Raw ideas area. Not a public project until owner + roadmap are assigned."
require_text "projects/education-ba-prompt/README.md" "docs/course-ideas.md"
require_text "projects/education-ba-prompt/README.md" "standards/education-profile.md"

require_text "projects/education-ba-prompt/docs/course-ideas.md" "status: draft"
require_text "projects/education-ba-prompt/docs/course-ideas.md" "version: 0.1"
require_text "projects/education-ba-prompt/docs/course-ideas.md" "updated: 2026-05-26"
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

require_text ".github/ISSUE_TEMPLATE/task.md" "status: canonical"
require_text ".github/ISSUE_TEMPLATE/task.md" "temperature: 0.1"
require_text ".github/ISSUE_TEMPLATE/task.md" 'Operating Mode: `Structured`'
require_text ".github/ISSUE_TEMPLATE/task.md" "Специфика AI-агентов"
require_text ".github/ISSUE_TEMPLATE/task.md" "Готово, когда"

require_text ".github/ISSUE_TEMPLATE/task-creative.md" "status: canonical"
require_text ".github/ISSUE_TEMPLATE/task-creative.md" "temperature: 0.7"
require_text ".github/ISSUE_TEMPLATE/task-creative.md" "Creative mode"
require_text ".github/ISSUE_TEMPLATE/task-creative.md" "Не писать, как именно реализовывать задачу"
require_text ".github/ISSUE_TEMPLATE/task-creative.md" "Обоснованный обход рекомендаций"

# HTOM-команда "ДНК-шаблон" (templates/htom/): минимальный геном для клонирования.
# HTOM-контракты (AI_GOVERNANCE / AI_QUICK_RULES / AI_HANDOVER_PROMPT) обязательны.
require_text "templates/htom/AI_GOVERNANCE.md" "{{project_name}}"
require_text "templates/htom/AI_GOVERNANCE.md" "Эскалация"
require_text "templates/htom/AI_GOVERNANCE.md" "temperature: 0.1"
require_text "templates/htom/AI_GOVERNANCE.md" "Хаб является источником рекомендаций"
require_text "templates/htom/AI_GOVERNANCE.md" "Обоснованный обход в Creative Mode"
require_text "templates/htom/AI_QUICK_RULES.md" "{{project_name}}"
require_text "templates/htom/AI_QUICK_RULES.md" "Не создавай"
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "{{REPO_NAME}}"
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "governance/agent-onboarding-protocol.md"
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "version: 0.7"
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "Периодическая суммаризация сессии"
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "governance/session-digests.md"
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "governance/BACKLOG.md"
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "executable: true"
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "ЭТО АРТЕФАКТ ДЛЯ КОПИРОВАНИЯ. Скопируйте в новый чат."
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "ИСПОЛНИМЫЙ HANDOVER PROMPT — СКОПИРУЙ И ВЫПОЛНИ"
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "EXECUTION"
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "EXPLANATION"
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "Определи тип проекта"
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "Контекст чата диалога"
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "Проверка шаблонов"
require_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "standards/session-handover-standard.md"
reject_text "templates/htom/AI_SESSION_HANDOVER_PROMPT.md" "Конард"
require_text "templates/htom/README.md" "AI_SESSION_HANDOVER_PROMPT.md"
require_text "templates/htom/README.md" "status: canonical"
require_text "templates/htom/README.md" "version: 0.4"
require_text "templates/htom/README.md" "## Template Placeholder Policy"
require_text "templates/htom/README.md" "Source templates may contain placeholders"
require_text "templates/htom/README.md" "Generated repositories must not keep unresolved source placeholders"
require_text "templates/htom/README.md" "{{date}}"
require_text "templates/htom/README.md" "{{project_name}}"
require_text "templates/htom/README.md" "{{hub_url}}"
require_text "templates/htom/README.md" "{{REPO_NAME}}"
require_text "templates/htom/README.md" "governance/agent-onboarding-protocol.md"
require_text "templates/htom/README.md" "Как валидировать структуру"
require_text "templates/htom/README.md" "Design Decisions & Rationale"
require_text "templates/htom/README.md" "Человек задаёт смысл, AI ускоряет путь — вместе по правилам"
require_text "templates/htom/CONTRIBUTING.md" "issue -> PR -> review"
require_text "templates/htom/CONTRIBUTING.md" "task-creative.md"
require_text "templates/htom/CONTRIBUTING.md" "manual restart"
require_text "templates/htom/CHANGELOG.md" "## Unreleased"
require_text "templates/htom/.github/ISSUE_TEMPLATE/task.md" "🎯 Контекст"
require_text "templates/htom/.github/ISSUE_TEMPLATE/task.md" "✅ Готово, когда"
require_text "templates/htom/.github/ISSUE_TEMPLATE/task.md" "temperature: 0.1"
require_text "templates/htom/.github/ISSUE_TEMPLATE/task.md" 'Operating Mode: `Structured`'
require_text "templates/htom/.github/ISSUE_TEMPLATE/task-creative.md" "temperature: 0.7"
require_text "templates/htom/.github/ISSUE_TEMPLATE/task-creative.md" "Creative mode"
require_text "templates/htom/.github/ISSUE_TEMPLATE/task-creative.md" "Обоснованный обход рекомендаций"
require_text "templates/htom/tools/validate-repository-structure.sh" "AI_GOVERNANCE.md"
require_text "templates/htom/tools/validate-repository-structure.sh" "task-creative.md"

# Spoke-репозиторий шаблон (templates/spoke/): production-код, отдельный продукт.
# Для spoke обязателен CI/CD (отличие от HTOM-команды).
require_text "templates/spoke/README.md" "status: canonical"
require_text "templates/spoke/README.md" "{{project_name}}"
require_text "templates/spoke/README.md" "{{hub_url}}"
require_text "templates/spoke/README.md" "production-код"
require_text "templates/spoke/README.md" "htom-vs-spoke-clarification-2026-06.md"
require_text "templates/spoke/README.md" ".github/workflows/ci.yml"
require_text "templates/spoke/README.md" "./tools/validate-file-naming.sh"
require_text "templates/spoke/CONTRIBUTING.md" "issue → PR → review"
require_text "templates/spoke/CONTRIBUTING.md" "spoke-репозиторий"
require_text "templates/spoke/CONTRIBUTING.md" "docs/analysis/"
require_text "templates/spoke/CONTRIBUTING.md" "YYYY-MM-DD-name.md"
require_text "templates/spoke/CONTRIBUTING.md" "./tools/validate-file-naming.sh"
require_text "templates/spoke/docs/README.md" "YYYY-MM-DD-name.md"
require_text "templates/spoke/docs/README.md" "YYYY-MM-adr-NNN-name.md"
require_text "templates/spoke/docs/README.md" "./tools/validate-file-naming.sh"
require_text "templates/spoke/.github/workflows/ci.yml" "name: ci"
require_text "templates/spoke/.github/workflows/ci.yml" "pull_request"
require_text "templates/spoke/.github/workflows/ci.yml" "Validate documentation file naming"
require_text "templates/spoke/tools/validate-file-naming.sh" "docs/analysis"
require_text "templates/spoke/tools/validate-file-naming.sh" "YYYY-MM-DD-name.md"

# Smart Sync infrastructure (issue #207): auto-generated manifest + registry +
# generator + sync CLI. manifest.json must never be hand-edited.
require_text "templates/sync-metadata.json" "auto-generated"
require_text "templates/sync-metadata.json" "sync-project-with-hub-prompt"
require_text "templates/manifest.json" "manifest_version"
require_text "templates/manifest.json" "target_type"
require_text "templates/manifest.json" "sync-project-with-hub-prompt"
require_text "experiments/test-frontmatter-validator.sh" "ai-generated ban"
require_text "experiments/test-frontmatter-validator.sh" "knowledge vocabulary"
require_text "experiments/test-frontmatter-validator.sh" "valid governance status and owner"
require_text "tools/generate-manifest.py" "templates/manifest.json"
require_text "tools/validate-frontmatter.sh" "invalid knowledge status"
require_text "tools/validate-frontmatter.sh" "invalid governance status"
require_text "tools/validate-frontmatter.sh" "frontmatter field is forbidden: ai-generated"
require_text "tools/validate-frontmatter.sh" "missing required frontmatter field for ADR artifact: decision-type"
require_text "tools/validate-frontmatter.sh" "missing required frontmatter field for RFC artifact: rfc-scope"
require_text ".github/workflows/validate.yml" "Validate file naming"
require_text ".github/workflows/validate.yml" "./tools/validate-file-naming.sh"
require_text ".github/workflows/validate.yml" "Test frontmatter validator"
require_text ".github/workflows/validate.yml" "bash experiments/test-frontmatter-validator.sh"
require_text ".github/workflows/update-manifest.yml" "chore: update manifest.json"
require_text ".github/workflows/update-manifest.yml" "templates/**"
require_text "tools/sync-from-hub.sh" "--report"
require_text "tools/sync-from-hub.sh" "--apply"
require_text "tools/sync-from-hub.sh" "--force"
require_text "tools/sync-from-hub.sh" "--init"
require_text "tools/sync-from-hub.sh" ".hub-profile.json"
require_text "tools/sync-from-hub.sh" ".hub-new.md"

# manifest.json must stay in sync with the templates/ tree and never be edited
# by hand. Enforce when python3 is available (skip gracefully otherwise).
if command -v python3 >/dev/null 2>&1; then
  if ! python3 tools/generate-manifest.py --check >/dev/null 2>&1; then
    fail "templates/manifest.json is out of date or hand-edited; run tools/generate-manifest.py --write"
  fi
else
  printf 'note: python3 not found; skipping manifest.json drift check.\n'
fi

# Hard constraint: research/ must NOT be baked into the templates.
if [[ -e templates/htom/research ]]; then
  fail "templates/htom must not contain research/ (knowledge lives in the hub research/)"
fi
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
