---
status: draft
version: 0.1
updated: 2026-08-21
temperature: 0.1
---

# Evidence: аудит противоречий Хаба (issue #529)

Воспроизводимые проверки для родительского отчёта
[docs/audit/2026-08-21-hub-structural-normative-contradictions-audit.md](../../../../docs/audit/2026-08-21-hub-structural-normative-contradictions-audit.md).

| Скрипт | Что проверяет | Результат (базовая линия 2026-08-21, до добавления самого отчёта) |
| --- | --- | --- |
| `link-check.py` | Все относительные markdown-ссылки в отслеживаемых `*.md` | `BROKEN=19 FILES=313`; 18 из 19 — легитимные `{{hub_url}}`-плейсхолдеры шаблонов, 1 реальная поломка (`templates/spoke/README.md:29`, находка G-03) |
| `artifact-map-coverage.py` | Сверка `pr-ops/artifact-map.md` с `git ls-files '*.md'` в обе стороны | `MISSING = 0` (висящих путей в карте нет), `UNREGISTERED = 62 из 313` (находка G-09) |

Запуск из любого каталога репозитория:

```bash
python3 research/hub/exp/hub-contradictions-audit-529/link-check.py
python3 research/hub/exp/hub-contradictions-audit-529/artifact-map-coverage.py
```

Логи прогонов сохранены рядом: `link-check.log`, `artifact-map-coverage.log`.
Числа сдвинутся при любых последующих правках дерева — это базовая линия аудита,
а не постоянно верный факт.
