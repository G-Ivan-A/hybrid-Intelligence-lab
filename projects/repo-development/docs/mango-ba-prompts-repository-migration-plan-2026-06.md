---
status: draft
version: 0.2
updated: 2026-06-15
temperature: 0.1
---

# Migration Plan for mango_ba_prompts Repository

This document closes Issue #241 by producing a reviewable migration plan for
`mango_ba_prompts`. It does not execute the migration in the project
repository. Execution must happen in a separate PR in
`G-Ivan-A/mango_ba_prompts` using the merged Task 2 RFC as input. If the RFC is
later delegated into active standards/templates, revalidate this plan against
those operational artifacts before execution.

Related artifacts:

- Issue #241:
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/241>
- Task 2 issue #240:
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/240>
- Task 2 RFC PR #243:
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/243>
- Task 2 RFC file:
  `governance/rfc/repository-archetypes-template-release.md`
- Completed dependency PR #238:
  <https://github.com/G-Ivan-A/hybrid-Intelligence-lab/pull/238>
- Target repository:
  <https://github.com/G-Ivan-A/mango_ba_prompts>

## 0. Dependency Status and Scope

Status checked on 2026-06-15:

| Dependency | Status | Impact |
| --- | --- | --- |
| PR #238 | Merged on 2026-06-15 | Dependency satisfied. |
| Task 2 RFC issue #240 | Closed on 2026-06-15 | Dependency satisfied. |
| Task 2 RFC PR #243 | Merged on 2026-06-15 as `d4d9f39` | This plan uses the merged file `governance/rfc/repository-archetypes-template-release.md` as its source input. |

Execution gate:

1. Treat every structural recommendation below as a plan for human review, not
   as an automatic mandate to move files.
2. If the RFC is later promoted into an active standard or template, compare
   those operational artifacts against the RFC sections listed below before
   opening the Mango migration PR.
3. If Mango changes materially before execution, refresh the repository
   snapshot and gap analysis.

RFC sections used from the merged Task 2 RFC:

| RFC section | How this plan uses it |
| --- | --- |
| Proposal / Decision Scope | Confirms that the RFC defines archetypes and release rules, but does not itself refactor Mango. |
| Repository Archetypes | Classifies `mango_ba_prompts` as a Prompt & Pattern Library rather than a generic product runtime. |
| Project Template: Prompt & Pattern Library | Provides required and optional directories for the gap analysis. |
| Ambiguous Zones | Drives the decision on root `experiments/` vs `prompts/experiments/`. |
| Governance Sync Rule | Separates Hub-synced governance genome from local Mango decisions. |
| Release Engineering Strategy | Uses GitHub Flow + trunk discipline, with production deployment only from `main`. |

## 1. Current Repository Snapshot

Snapshot reviewed:

| Item | Observed state |
| --- | --- |
| Repository | `G-Ivan-A/mango_ba_prompts` |
| Branch | `main` |
| Latest inspected commit | `35ff7df` |
| GitHub Pages | Built from `gh-pages`, published at <https://g-ivan-a.github.io/mango_ba_prompts/> |
| Active PRs | PR #90 is draft and changes GitHub Pages behavior. |
| Active issues | Issues #82 and #87 are open and overlap with site/widget work. |

High-level structure found:

- Root contracts exist: `README.md`, `AI_GOVERNANCE.md`, `CONTRIBUTING.md`,
  `CHANGELOG.md`.
- Prompt assets exist under `prompts/`, including `prompts/archive/` and
  `prompts/experiments/`.
- Pattern assets exist under `patterns/`.
- Domain documentation exists under `docs/`, including
  `docs/ba-processes/00-index.md` and `docs/hub-research-dependencies.md`.
- Local standards exist under `standards/`.
- Site generation exists through `scripts/generate-pages-data.mjs`, `site/`,
  and `.github/workflows/github-pages.yml`.
- Governance records exist under `governance/`, including local migration
  manifests and `governance/BACKLOG.md`.
- Root `experiments/` contains executable Python validation scripts named
  `validate_issue_*.py`.

## 2. RFC Template Applied to Mango

The merged RFC defines `mango_ba_prompts` as a Prompt & Pattern Library. The
template requirements map to Mango as follows:

| RFC template element | Required by RFC? | Mango state | Planning conclusion |
| --- | --- | --- | --- |
| `README.md` | Yes | Present | Keep. Update only if migration changes paths. |
| `AI_GOVERNANCE.md` | Yes | Present | Keep. Mark sync provenance against Hub during the Mango migration PR. |
| `CONTRIBUTING.md` | Yes | Present | Keep. Update if validation paths move. |
| `CHANGELOG.md` | Yes | Present | Keep. Record migration phases. |
| `governance/artifact-map.md` | Yes | Present | Keep. Fill missing path ownership after moves. |
| `prompts/` | If prompts exist | Present | Keep as primary library surface. |
| `patterns/` | If pattern-backed | Present | Keep as primary pattern surface. |
| `docs/` | If domain context supports prompt selection | Present | Keep. `docs/ba-processes/00-index.md` is justified because it is populated. |
| `standards/` | If validation depends on local rules | Present | Keep, but mark each file as synced, forked, or local. |
| `scripts/` or `tools/` | If automation exists | Present via `scripts/` | Expand to include validation scripts currently in root `experiments/`. |
| `tests/` or `experiments/` | If checks or evals exist | Present as root `experiments/` and `prompts/experiments/` | Split executable validation from prompt-run provenance. |
| `kb/` | Optional | Exists mostly as placeholder/local context area | Fill with real reusable context or remove placeholder. |
| `examples/` | Optional | Pattern examples exist under `patterns/*/examples/` | Keep local to patterns; no root `examples/` needed unless examples become cross-library. |
| `site/` | Optional | Present | Keep. It is part of Pages publication. |
| `infra/` | Optional | Absent | No action needed. |
| `.github/workflows/` | Optional | Present | Keep. Align workflow with release strategy. |

## 3. Gap Analysis

| Class | Current path or behavior | Action | Rationale |
| --- | --- | --- | --- |
| Match | `README.md`, `AI_GOVERNANCE.md`, `CONTRIBUTING.md`, `CHANGELOG.md` | Keep | Required root contracts already exist. |
| Match | `prompts/` | Keep | Main Prompt & Pattern Library asset surface. |
| Match | `patterns/` | Keep | Pattern-backed library content exists and has examples. |
| Match | `docs/ba-processes/00-index.md` | Keep | File is populated and supports prompt selection; it is not an empty placeholder. |
| Match | `docs/hub-research-dependencies.md` | Keep | Documents Hub-to-project knowledge boundary. |
| Match | `scripts/generate-pages-data.mjs`, `site/`, `.github/workflows/github-pages.yml` | Keep | Existing site pipeline supports the optional `site/` part of the archetype. |
| Rename / normalize | `governance/BACKLOG.md` | Consider rename to `governance/backlog.md` only in the execution PR | Hub naming convention favors lowercase kebab-case in nested governance paths. Rename requires link audit. |
| Rename / normalize | `standards/GLOSSARY.md` | Consider rename to `standards/glossary.md` only if sync provenance is preserved | Hub standard path is lowercase. This is a potentially disruptive path change and needs explicit review. |
| Move | `experiments/validate_issue_*.py` | Move to `scripts/validation/` or `tests/validation/`; recommended target is `scripts/validation/` | These are executable repository checks invoked by workflows, not research experiments or prompt-run evidence. |
| Keep in place | `prompts/experiments/*.md` | Keep under `prompts/experiments/` and add a short README/index | These files are prompt-specific run evidence and promotion provenance, which the RFC explicitly allows in prompt-local experiments. |
| Create | `scripts/validation/README.md` | Create if validators move | Documents what belongs in executable validation vs prompt experiments. |
| Create | `prompts/experiments/README.md` | Create or update | Makes the prompt-run evidence boundary explicit and removes reliance on `.gitkeep`. |
| Fill or delete | `kb/` | Fill with real reusable context or remove placeholder | RFC allows `kb/`, but empty placeholders violate Anti-Inflation. |
| Delete | Placeholder `.gitkeep` files in non-empty directories | Delete during execution PR | Once content exists, placeholder files add noise. |
| Fill | `governance/artifact-map.md` | Update after every move/rename | Must remain the source for local path ownership. |
| Governance sync | `AI_GOVERNANCE.md`, `AI_QUICK_RULES.md`, `AI_SESSION_HANDOVER_PROMPT.md`, `CONTRIBUTING.md`, `standards/*` | Mark each as Hub-synced, forked, or local, with source SHA or rationale | Required by the RFC Governance Sync Rule. |
| Release strategy | `.github/workflows/github-pages.yml` deploys to `gh-pages` only from `main` | Keep this production rule; update validator paths if scripts move | This matches GitHub Flow + trunk discipline. |

Gap summary:

- The repository is already close to the Prompt & Pattern Library archetype.
- The primary structural gap is semantic, not volume-based: executable checks
  are mixed into root `experiments/`, while prompt-run provenance correctly
  belongs in `prompts/experiments/`.
- The primary governance gap is provenance: local files should state whether
  they are Hub-synced, locally extended, or forked.
- The primary release risk is path churn in a repository that already has a
  GitHub Pages workflow and an active draft Pages PR (#90).

## 4. Scenario Comparison

### Scenario A - In-place Refactoring

Description:

- Open a short-lived branch in `G-Ivan-A/mango_ba_prompts`.
- Apply targeted path cleanup and documentation updates in the existing
  repository.
- Merge through PR into `main` after validation and review.
- Keep the current repository URL, issue history, PR history, and Pages URL.

Pros:

- Preserves history, links, issues, PRs, and existing GitHub Pages URL.
- Matches the merged RFC release model: GitHub Flow + trunk discipline.
- Smaller blast radius because the current structure already mostly matches the
  archetype.
- Easier for ongoing work, including PR #90, to rebase or merge.

Cons:

- Path moves can conflict with active PR #90 and any local scripts that call
  `experiments/validate_issue_*.py`.
- Reviewers must inspect renames carefully to avoid accidental content loss.
- Existing links to uppercase files such as `governance/BACKLOG.md` and
  `standards/GLOSSARY.md` may break if renamed without redirects or exhaustive
  link updates.

Risks and mitigations:

| Risk | Mitigation |
| --- | --- |
| PR #90 conflicts with workflow or site files | Freeze, merge, or rebase PR #90 before structural migration. |
| GitHub Pages deploy breaks | Keep production deploy limited to push on `main`; run PR validation before merge. |
| Broken Markdown links after moves | Run a link check and grep for old paths before review. |
| Governance files drift silently from Hub | Record synced/forked/local status and source SHA in artifact map or migration manifest. |

### Scenario B - New Repository plus Redirect

Description:

- Create a new clean repository from the archetype.
- Copy or migrate current Mango assets into the new structure.
- Freeze the old repository or turn it into a redirect/index.
- Reconfigure Pages, settings, branch protection, and documentation links.

Pros:

- Clean history for the new structure.
- No disruptive path moves in the existing repository while building the new
  structure.
- Easier to reject legacy placeholders because only intentional files are
  copied.

Cons:

- Splits issues, PRs, discussion history, and blame context.
- Changes or complicates the public Pages URL.
- Requires migration of repository settings, Actions permissions, branch
  protection, Pages source, and any secrets.
- Creates user confusion: old repo, new repo, redirect repo, and potentially
  two active issue trackers.

Risks and mitigations:

| Risk | Mitigation |
| --- | --- |
| Users keep opening issues in the old repository | Make old repository read-only and pin a redirect README. |
| Published Pages URL changes | Preserve old Pages with redirect content or configure a custom domain. |
| History becomes hard to audit | Use `git filter-repo` or subtree history import, but accept operational complexity. |

## 5. Recommendation

Recommend Scenario A: in-place refactoring.

Reasoning:

- The inspected repository already satisfies most Prompt & Pattern Library
  requirements.
- The needed changes are mostly path semantics, provenance, and documentation,
  not a wholesale rebuild.
- Keeping the existing repository preserves the value of current issues, PRs,
  history, and the public Pages URL.
- Scenario B creates more governance and release risk than it removes.

Execution no longer waits on the Task 2 RFC merge. It still requires a fresh
Mango pre-migration snapshot and human review before moving files. If the RFC is
later promoted into active standards/templates and those artifacts materially
change the Prompt & Pattern Library template, the Governance Sync Rule, or the
Release Engineering Strategy, revisit the recommendation before touching Mango.

## 6. Step-by-step Checklist

### Phase 0 - Gate and Freeze

1. Confirm the current Mango branch, open PRs, and issue state immediately
   before execution.
2. Compare any active standard/template derived from the Task 2 RFC against the
   sections used by this plan.
3. Decide the status of PR #90: merge first, pause, or require rebase after the
   structural PR.
4. Open a short-lived Mango branch for the migration. Do not introduce a
   long-lived `dev` branch.
5. Capture a pre-migration snapshot:
   - `git rev-parse HEAD`
   - `find . -maxdepth 3 -type f | sort`
   - current Pages URL and workflow status
   - current open PRs/issues that touch moved paths

### Phase 1 - Inventory and Provenance

1. Build a path inventory for `prompts/`, `patterns/`, `docs/`, `standards/`,
   `governance/`, `scripts/`, `experiments/`, `site/`, and `.github/`.
2. Classify governance files:
   - Hub-synced: copied from Hub and expected to follow Hub updates.
   - Local extension: project-specific decisions, migration manifests, local
     artifact map, local backlog.
   - Forked: intentionally diverged from Hub with recorded rationale.
3. Record source SHA or rationale for synced/forked files.
4. Decide whether `governance/BACKLOG.md` and `standards/GLOSSARY.md` should be
   renamed in the same PR or deferred to reduce blast radius.

### Phase 2 - Structure Cleanup

1. Move executable validation scripts from `experiments/validate_issue_*.py` to
   `scripts/validation/` unless reviewers choose `tests/validation/`.
2. Add `scripts/validation/README.md` explaining that this directory contains
   executable repository checks.
3. Keep `prompts/experiments/` for prompt-specific run evidence.
4. Add or update `prompts/experiments/README.md` and delete redundant
   `.gitkeep` files.
5. Fill `kb/` with real reusable context or delete the placeholder directory.
6. Update `.github/workflows/github-pages.yml` to call validators from their new
   paths.
7. If approved, rename uppercase nested files and update every reference:
   - `governance/BACKLOG.md` -> `governance/backlog.md`
   - `standards/GLOSSARY.md` -> `standards/glossary.md`

### Phase 3 - Documentation and Governance

1. Update Mango `README.md` navigation for any moved paths.
2. Update Mango `CONTRIBUTING.md` validation commands.
3. Update Mango `CHANGELOG.md` with the migration entry.
4. Update Mango `governance/artifact-map.md` with every new, moved, renamed, or
   removed artifact.
5. Update or close the migration manifest if the old migration phase is done.
6. Add an ADR under `docs/adr/` if reviewers approve a non-trivial naming or
   release decision.

### Phase 4 - Testing

Run at minimum:

```bash
node scripts/generate-pages-data.mjs
python3 scripts/validation/validate_issue_74_github_pages.py
python3 scripts/validation/validate_issue_86_mango_widget.py
find . -name '*.md' -print0 | xargs -0 grep -n 'experiments/validate_issue_' || true
find . -name '*.md' -print0 | xargs -0 grep -n 'standards/GLOSSARY.md\\|governance/BACKLOG.md' || true
```

If the migration renames files, add a Markdown link check before review. If the
site output changes, capture a before/after screenshot or Pages artifact for
the PR description.

### Phase 5 - Merge and Deploy

1. Open the migration PR against Mango `main`.
2. Include:
   - reproduction or pre-migration snapshot
   - path-move summary
   - checks run
   - Pages screenshot or artifact if visual output changed
3. Merge only after review and green CI.
4. Let production deploy happen only from `main`.
5. Verify the public Pages URL after merge.
6. Rebase or unfreeze dependent PRs such as PR #90.

### Phase 6 - Post-migration

1. Monitor GitHub Pages and issue reports for broken links.
2. Close or update migration issues in Mango.
3. Record any final sync drift from Hub in the local migration manifest.
4. Schedule the next Smart Sync from Hub once the RFC is canonical.

## 7. Dev / Prod Strategy

Use the RFC release strategy directly:

- `main` is production-ready.
- Work happens in short-lived issue branches.
- Pull requests run validation and review.
- Production deploys only from `main`.
- No long-lived `dev` branch is introduced for this migration.

For non-production review, use PR checks, workflow artifacts, or a temporary
preview artifact. Do not use a permanent `dev` branch as a second production
track.

## 8. GitHub Actions Example

If validators move from root `experiments/` to `scripts/validation/`, the Mango
Pages workflow can keep its current release behavior and only update paths:

```yaml
name: GitHub Pages

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build-and-validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: node scripts/generate-pages-data.mjs
      - run: python3 scripts/validation/validate_issue_74_github_pages.py
      - run: python3 scripts/validation/validate_issue_86_mango_widget.py

  deploy:
    needs: build-and-validate
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: node scripts/generate-pages-data.mjs
      - name: Prepare Pages output
        run: |
          mkdir -p pages-dist
          cp -R site/* pages-dist/
      - name: Deploy to gh-pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./pages-dist
```

This example intentionally keeps deployment conditional on push to `main`. Pull
requests validate the build but do not publish production content.

## 9. Definition of Done for the Future Mango Migration PR

The future Mango migration PR is complete when:

1. Final Task 2 RFC text has been reviewed and cited in the PR.
2. Gap analysis decisions are implemented or explicitly deferred.
3. Executable validators are no longer mislabeled as root experiments unless
   reviewers choose a documented exception.
4. `prompts/experiments/` remains the prompt-run evidence area.
5. Empty placeholders are removed or replaced with real indexes.
6. Governance files are marked synced, forked, or local.
7. Workflow paths match the final file layout.
8. Local validation and GitHub Actions pass.
9. The PR description includes reproduction, checks, and Pages evidence if the
   site changed.

## 10. Open Review Decisions

These decisions should be made by the Mango maintainers before execution:

| Decision | Recommended default |
| --- | --- |
| Move root validation scripts to `scripts/validation/` or `tests/validation/` | `scripts/validation/`, because they are repository automation scripts. |
| Rename `governance/BACKLOG.md` now or later | Defer if PR #90 or open issues touch governance docs; otherwise rename with full link audit. |
| Rename `standards/GLOSSARY.md` now or later | Defer unless Hub sync provenance can be recorded cleanly. |
| Keep or delete `kb/` | Keep only if real reusable context is added; otherwise delete placeholder. |
| Require Pages screenshot in migration PR | Yes if visual output or generated data changes; no for pure path-only changes. |
