# Changelog

All notable repository governance changes are documented here.

## Unreleased

### Added

- Canonical glossary в `standards/GLOSSARY.md` для единых терминов standards,
  governance и AI-assisted work.
- Issue #17 migration structure: `CONCEPT.md`, обновленные root governance
  files, `standards/README.md`, `governance/REPO_MODEL.md` и `tools/`.
- Repository structure validation в `tools/validate-repository-structure.sh`.
- Active documentation для Anti-Inflation principle: артефакт создается только
  когда снижает операционную боль.
- `standards/TEAM_CONTRACT.md` как шаблон и инструкция для создания
  project-level `CONTRIBUTING.md` и `AI_GOVERNANCE.md` в spoke-проектах.

### Changed

- Previous tracked files сохранены с суффиксом `-old` для анализа и выборочной
  миграции.
- Active navigation теперь указывает на `governance/` вместо `meta/` и на
  `tools/` вместо `tests/`.
- Standards рассматриваются как плоский registry, пока operational use не
  докажет потребность в более глубокой taxonomy.

### Removed

- Old content не удалялся в этой миграции; previous files были переименованы
  для review.

## Связанные документы

- [README.md](README.md)
- [CONCEPT.md](CONCEPT.md)
- [AI_GOVERNANCE.md](AI_GOVERNANCE.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [standards/README.md](standards/README.md)
- [standards/GLOSSARY.md](standards/GLOSSARY.md)
- [standards/TEAM_CONTRACT.md](standards/TEAM_CONTRACT.md)
- [governance/REPO_MODEL.md](governance/REPO_MODEL.md)

## TODO

- Проанализировать `-old` files и перенести только содержание, которое остается
  операционно полезным.
- Добавить concrete artifact templates после появления повторяющихся работ и
  стабильных потребностей.
- Заменить license placeholder после решения Founder & PO.
