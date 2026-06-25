---
status: canonical
version: 0.2
updated: {{date}}
temperature: 0.1
ai-generated: true
---

# Docs

Документация spoke-репозитория хранит продуктовые, архитектурные и аналитические
артефакты, которые относятся к конкретному продукту.

## Хронологические артефакты

Файлы в `docs/analysis/`, `docs/rfc/` и `docs/adr/` используют дату в начале
имени.

- `YYYY-MM-DD-name.md` для `docs/analysis/`;
- `YYYY-MM-name.md` или `YYYY-name.md` для `docs/rfc/`;
- `YYYY-MM-adr-NNN-name.md` для ADR с номером.

Для `docs/analysis/` день берётся из git history создания файла. Если
достоверно известен только месяц, используется день `01`.

Исключения без даты: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`,
`CODE_OF_CONDUCT.md`, `LICENSE.md`, `AI_GOVERNANCE.md`, `*-registry.md` и
`*-index.md`.

Проверка:

```bash
./tools/validate-file-naming.sh
```
