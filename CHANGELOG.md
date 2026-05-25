# Changelog

All notable changes to this repository will be documented here.

The format follows a simple date-based history until a release process is
selected.

## Unreleased

### Added

- Operational backbone for issue #15: `CHANGELOG.md`, `CONTRIBUTING.md`,
  `LICENSE`, GitHub issue templates, and a pull request template.
- GitHub issue templates for AI implementation tasks, research tasks, and
  governance changes.
- Pull request checklist aligned with the hybrid-team collaboration rules.
- Changelog entry connecting this implementation to the repository-governance
  research completed in issue #13.

### Changed

- Repository identity in core documents now uses `hybrid-Intelligence-lab`.
- Mango TZ corpus experiment moved from `experiments/tz-corpus/` to
  `experiments/mango/tz-corpus/`.
- Repository structure validation now checks the operational backbone files,
  current repository identity, and the Mango-scoped experiment path.

### Removed

- Legacy bootstrap `.gitkeep` from the repository root.
- Legacy root experiment path `experiments/tz-corpus/`.

## TODO

- Founder & PO to select and approve the final project license.
- Add artifact maturity frontmatter (`status:`) after the FR-7 trigger is
  confirmed.
- Add `meta/artifact-map.md` when the repository exceeds the agreed artifact
  navigation threshold.
- Introduce `/governance/` layering only when the specialized-policy trigger is
  met.
