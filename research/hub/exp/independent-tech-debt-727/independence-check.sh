#!/usr/bin/env bash
# Read-only evidence for issue #727: which open Hub tech-debt rows can run
# without touching mango_ba_prompts, mango-ba-ai-runtime and aether-orbis-gra,
# and what is still open in the Hub part of Sprint 13 on current main.
# Usage: research/hub/exp/independent-tech-debt-727/independence-check.sh
# Needs: git, grep, awk; gh (authenticated) for the PR and spoke sections.
set -u
root="$(git rev-parse --show-toplevel)"
cd "$root" || exit 1
owner="G-Ivan-A"
genome_validator="templates/htom/tools/validate-repository-structure.sh"
sprint_files=(
  standards/contract-documentation-standard.md
  ops/repo-model.md
  standards/issue-workflow.md
  .github/ISSUE_TEMPLATE/task.md
  .github/ISSUE_TEMPLATE/task.yml
  templates/htom/.github/ISSUE_TEMPLATE/task.md
  templates/htom/tools/validate-repository-structure.sh
  templates/htom/tools/validate-agents-bootstrap.sh
  tools/validate-frontmatter.sh
  tools/validate-repository-structure.sh
  standards/frontmatter-standard.md
)

echo "# Hub HEAD: $(git rev-parse --short HEAD) ($(git log -1 --format=%cs))"

echo
echo "## Previous steps: backlog rows still in review although their PR is merged"
grep -n '^| \*\*B-\(19[67]\|269\|27[5-9]\|28[0-5]\)\*\*' ops/backlog.md | cut -d'|' -f2,6,7 | sed 's/ \+/ /g'

echo
echo "## F-1. B-169: contract home is normed in AGENTS.md, not in the standard"
grep -n 'Do not create `docs/contracts/`\|^| Agent contract\|^| Process contract' AGENTS.md
echo "contract-documentation-standard.md mentions ai-rules/: $(grep -c 'ai-rules/' standards/contract-documentation-standard.md)"
echo "contract-documentation-standard.md mentions docs/contracts: $(grep -c 'docs/contracts' standards/contract-documentation-standard.md)"
echo "ops/repo-model.md mentions контракт/contract: $(grep -c -i 'контракт\|contract' ops/repo-model.md)"
grep -n '^version:\|^updated:' standards/contract-documentation-standard.md ops/repo-model.md

echo
echo "## F-2. B-114: five levels exist, wording rules are declared missing"
grep -n '### Пять уровней постановки задачи\|отдельным стандартом пока не\|B-114' standards/issue-workflow.md
grep -n 'Keep the levels distinct' AGENTS.md | cut -c1-90
echo "issue-workflow.md mentions измерим/проверяем: $(grep -c -i 'измерим\|проверяем' standards/issue-workflow.md)"
echo "issue-workflow.md mentions антипаттерн: $(grep -c -i 'антипаттерн' standards/issue-workflow.md)"

echo
echo "## F-3. B-115: Hub template has five levels, genome template does not"
for f in .github/ISSUE_TEMPLATE/task.md templates/htom/.github/ISSUE_TEMPLATE/task.md; do
  echo "$f: $(grep -m1 '^version:' "$f"), level headings = $(grep -c '^## Уровень [1-5]\.' "$f")"
done
rfc="docs/rfc/2026-08-06-rfc-task-statement-architecture.md"
echo "$rfc: $(grep -m1 '^status:' "$rfc"), $(grep -m1 '^version:' "$rfc")"
grep -n 'HISTORICAL_IMMUTABLE_PATHS:-' tools/validate-historical-immutable.sh

echo
echo "## F-4. B-116: machine gates"
echo "Hub: every tracked file must be on the allowlist (docs/contracts/* is not):"
grep -n '^is_active_file() {\|if is_active_file "\$file"; then' tools/validate-repository-structure.sh
echo "Hub allowlist mentions docs/contracts: $(grep -c 'docs/contracts' tools/validate-repository-structure.sh)"
grep -n 'frontmatter field is forbidden: ai-generated' tools/validate-frontmatter.sh
echo "Genome validator scans only the root:"
grep -n 'find \. -maxdepth 1 -type d' "$genome_validator"
echo "Genome validator mentions docs/contracts: $(grep -c 'docs/contracts' "$genome_validator")"
echo "Genome tools check ai-generated: $(cat templates/htom/tools/*.sh | grep -c 'ai-generated')"
echo "Any validator names model-specific rule files (.cursorrules, GEMINI.md, .windsurfrules): $(cat tools/*.sh templates/htom/tools/*.sh | grep -c -i 'cursorrules\|GEMINI\.md\|windsurfrules')"
# A statement gate must read issue bodies; template-presence checks do not count.
echo "Workflows triggered by issue events (inside the on: block): $(for wf in .github/workflows/*.yml; do awk '/^on:/{f=1;next} /^[^ #]/{f=0} f && /^  issues:/{print FILENAME; exit}' "$wf"; done | wc -l)"
echo "Tools reading issue bodies (gh issue view / event.issue.body): $(grep -l -E 'gh issue view|event\.issue\.body' tools/*.sh tools/*.py .github/workflows/*.yml 2>/dev/null | wc -l)"

echo
echo "## F-5. B-154: where the ai-generated ban is written"
grep -l 'ai-generated' standards/*.md CONTRIBUTING.md AGENTS.md templates/htom/AGENTS.md | sed 's/^/  /'
echo "files: $(grep -l 'ai-generated' standards/*.md CONTRIBUTING.md AGENTS.md templates/htom/AGENTS.md | wc -l)"

echo
echo "## Overlap with RFC #715 steps (Sprint 30 rows)"
grep -n '^| \*\*B-\(239\|240\|241\|259\|260\)\*\*' ops/backlog.md | cut -d'|' -f2,3,4,6 | sed 's/ \+/ /g'

echo
echo "## Duplicate IDs among the chosen rows (expect 1 each)"
for id in B-114 B-115 B-116 B-154 B-169; do
  echo "$id rows: $(grep -c "^| \*\*$id\*\*" ops/backlog.md)"
done

if ! command -v gh >/dev/null 2>&1; then
  echo "gh not found: PR and spoke sections skipped"; exit 0
fi

echo
echo "## Open Hub PRs touching the chosen files"
for n in $(gh pr list --repo "$owner/hybrid-Intelligence-lab" --state open --json number --jq '.[].number'); do
  files="$(gh pr view "$n" --repo "$owner/hybrid-Intelligence-lab" --json files --jq '.files[].path')"
  hits=""
  for f in "${sprint_files[@]}"; do grep -qx "$f" <<<"$files" && hits="$hits $f"; done
  echo "PR #$n:${hits:- none}"
done

echo
echo "## Spokes: open PRs, Hub paths they touch, whether CI reads Hub files at run time"
for r in mango_ba_prompts mango-ba-ai-runtime aether-orbis-gra; do
  echo "### $r"
  for n in $(gh pr list --repo "$owner/$r" --state open --json number --jq '.[].number'); do
    title="$(gh pr view "$n" --repo "$owner/$r" --json title --jq .title | cut -c1-80)"
    hub_paths="$(gh pr view "$n" --repo "$owner/$r" --json files --jq '.files[].path' | grep -c -E '^(standards|templates/htom|ops/backlog\.md)')"
    echo "open PR #$n: $title (files under standards/, templates/htom/, ops/backlog.md: $hub_paths)"
  done
  for wf in $(gh api "repos/$owner/$r/contents/.github/workflows" --jq '.[].path' 2>/dev/null); do
    body="$(gh api "repos/$owner/$r/contents/$wf" --jq .content | base64 -d 2>/dev/null)"
    fetch="$(grep -c -E 'git clone .*hybrid-Intelligence-lab|repository: *G-Ivan-A/hybrid-Intelligence-lab|raw.githubusercontent.com/G-Ivan-A/hybrid-Intelligence-lab' <<<"$body")"
    echo "$wf: Hub fetch steps = $fetch"
  done
  prof="$(gh api "repos/$owner/$r/contents/.hub-profile.json" --jq .content 2>/dev/null | base64 -d 2>/dev/null)"
  if [ -n "$prof" ]; then
    echo ".hub-profile.json pin: $(grep -o -E '"hub_(commit|sha)": *"[^"]*"' <<<"$prof" | head -1)"
  else
    echo ".hub-profile.json: absent"
  fi
done
