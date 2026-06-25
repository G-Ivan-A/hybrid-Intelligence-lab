---
status: canonical
version: 1.0
updated: 2026-06-25
temperature: 0.1
ai-generated: false
---

# File Naming Convention

Этот файл фиксирует compatibility entry для задач и внешних ссылок, которые
ожидают путь `standards/file-naming-convention.md`. Нормативный источник правил —
[standards/file-naming.md](file-naming.md).

## Хронологические файлы

Хронологические Markdown-артефакты используют дату в начале имени:

- `YYYY-MM-name.md`, если известен месяц;
- `YYYY-name.md`, если известен только год;
- `YYYY-MM-adr-NNN-name.md` для spoke ADR.

Области применения:

- Hub: `research/<domain>/` и вложенные тематические каталоги research;
- spoke: `docs/analysis/`, `docs/rfc/`, `docs/adr/`.

Исключения без даты: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`,
`CODE_OF_CONDUCT.md`, `LICENSE`, `LICENSE.md`, `AI_GOVERNANCE.md`,
`*-registry.md`, `*-index.md` и существующий суффикс уровня `*-Index.md`.

Проверка:

```bash
./tools/validate-file-naming.sh
```
