---
status: accepted
version: 1.2
updated: 2026-07-01
temperature: 0.1
owner: G-Ivan-A
---

# File Naming Convention

Этот файл фиксирует compatibility entry для задач и внешних ссылок, которые
ожидают путь `standards/file-naming-convention.md`. Нормативный источник правил —
[standards/file-naming.md](file-naming.md).

## Хронологические файлы

Хронологические Markdown-артефакты используют дату в начале имени.

- `YYYY-MM-DD-name.md` для Hub `research/`, Hub `docs/report/` и spoke
  `docs/analysis/`;
- `YYYY-MM-name.md` или `YYYY-name.md` для spoke `docs/rfc/`;
- `YYYY-MM-adr-NNN-name.md` для spoke ADR.

Области применения:

- Hub: `research/<domain>/`, вложенные тематические каталоги research и
  `docs/report/`;
- spoke: `docs/analysis/`, `docs/rfc/`, `docs/adr/`.

Для research/analysis-файлов день берётся из git history создания файла. Если
достоверно известен только месяц, используется день `01`.

Исключения без даты: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`,
`CODE_OF_CONDUCT.md`, `LICENSE`, `LICENSE.md`, `GOVERNANCE.md`,
`*-registry.md`, `*-index.md` и существующий суффикс уровня `*-Index.md`.

Проверка:

```bash
./tools/validate-file-naming.sh
```
