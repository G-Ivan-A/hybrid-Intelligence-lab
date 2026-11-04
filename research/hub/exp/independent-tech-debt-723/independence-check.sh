#!/usr/bin/env bash
# Read-only evidence for issue #723: is Sprint 23 (B-196, B-197) independent of
# mango_ba_prompts, mango-ba-ai-runtime and aether-orbis-gra, and is the gap
# from docs/analysis/2026-09-28-adr-021-downstream-contract-gaps.md still open?
# Usage: research/hub/exp/independent-tech-debt-723/independence-check.sh
# Needs: git, grep, gh (authenticated) for the PR and spoke sections.
set -u
root="$(git rev-parse --show-toplevel)"
cd "$root" || exit 1
owner="G-Ivan-A"
sprint_files=(
  tools/check-agent-work-rules-size.sh
  tools/test-check-agent-work-rules-size.sh
  templates/htom/AI_SESSION_HANDOVER_PROMPT.md
  templates/htom/AI_GOVERNANCE.md
  templates/manifest.json
)

echo "# Hub HEAD: $(git rev-parse --short HEAD) ($(git log -1 --format=%cs))"

echo
echo "## F-1. Size validator: hard failure above 9K"
grep -n 'ERROR_TOKENS=\|exceeds the hard budget\|exit 1' tools/check-agent-work-rules-size.sh
grep -n 'hard budget' tools/test-check-agent-work-rules-size.sh
grep -n '9K — рекомендация' docs/adr/2026-09-adr-021-agent-collaboration-layer.md
./tools/check-agent-work-rules-size.sh 2>&1 | sed 's/^/  run: /'

echo
echo "## F-2…F-5. Default operating mode wording (canon vs genome)"
grep -n 'по умолчанию — Hybrid' ai-rules/agent-onboarding-protocol.md
grep -n 'Hybrid — режим по умолчанию' ai-rules/agent-work-rules.md
grep -n 'defaults to Hybrid' templates/htom/AGENTS.md | cut -c1-120
grep -n -A1 'Operating Mode бери из issue' templates/htom/AI_SESSION_HANDOVER_PROMPT.md
grep -n '^| Structured\|^| Hybrid' templates/htom/AI_GOVERNANCE.md
grep -n 'Structured mode по\|Operating Mode: `' templates/htom/.github/ISSUE_TEMPLATE/task.md
grep -n '^Operating mode:' templates/sync-project-with-hub-prompt.md

echo
echo "## Pins that a B-197 edit must update"
grep -n 'require_text "templates/htom/AI_\(SESSION_HANDOVER_PROMPT\|GOVERNANCE\).md" "\(version\|temperature\|Обоснованный\)' tools/validate-repository-structure.sh
grep -n -B2 -A2 'htom-ai-session-handover-prompt\|htom-ai-governance' templates/manifest.json | grep -n '"id"\|"version"'

echo
echo "## Backlog rows of Sprint 23"
grep -n '^| \*\*B-19[67]\*\*' ops/backlog.md | cut -d'|' -f2,5,6,7

if ! command -v gh >/dev/null 2>&1; then
  echo "gh not found: PR and spoke sections skipped"; exit 0
fi

echo
echo "## Open Hub PRs touching Sprint 23 files"
for n in $(gh pr list --repo "$owner/hybrid-Intelligence-lab" --state open --json number --jq '.[].number'); do
  files="$(gh pr view "$n" --repo "$owner/hybrid-Intelligence-lab" --json files --jq '.files[].path')"
  hits=""
  for f in "${sprint_files[@]}"; do grep -qx "$f" <<<"$files" && hits="$hits $f"; done
  echo "PR #$n:${hits:- none}"
done

echo
echo "## Spokes: open PRs and whether CI reads Hub files at run time"
for r in mango_ba_prompts mango-ba-ai-runtime aether-orbis-gra; do
  echo "### $r"
  gh pr list --repo "$owner/$r" --state open --json number,title --jq '.[] | "open PR #\(.number): \(.title)"' | cut -c1-120
  for wf in $(gh api "repos/$owner/$r/contents/.github/workflows" --jq '.[].path' 2>/dev/null); do
    body="$(gh api "repos/$owner/$r/contents/$wf" --jq .content | base64 -d 2>/dev/null)"
    fetch="$(grep -c -E 'git clone .*hybrid-Intelligence-lab|repository: *G-Ivan-A/hybrid-Intelligence-lab|raw.githubusercontent.com/G-Ivan-A/hybrid-Intelligence-lab' <<<"$body")"
    echo "$wf: Hub fetch steps = $fetch"
  done
  prof="$(gh api "repos/$owner/$r/contents/.hub-profile.json" --jq .content 2>/dev/null | base64 -d 2>/dev/null)"
  if [ -n "$prof" ]; then
    echo ".hub-profile.json pin: $(grep -o -E '"hub_(commit|sha)": *"[^"]*"' <<<"$prof" | head -1)"
    for f in templates/htom tools/check-agent-work-rules-size.sh AI_SESSION_HANDOVER_PROMPT.md AI_GOVERNANCE.md; do
      echo "  synced path mentions $f: $(grep -c -F "$f" <<<"$prof")"
    done
  else
    echo ".hub-profile.json: absent"
  fi
done
