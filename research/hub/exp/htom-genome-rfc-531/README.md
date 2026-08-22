---
status: draft
version: 0.2
updated: 2026-08-22
temperature: 0.1
---

# Evidence: черновик правок генома HTOM (issue #531)

Контейнер держит **исполнимый черновик** предложения из
[docs/rfc/2026-08-21-rfc-htom-genome-structure-and-ci.md](../../../../docs/rfc/2026-08-21-rfc-htom-genome-structure-and-ci.md)
по находкам G-01 и G-02 родительского аудита
[docs/audit/2026-08-21-hub-structural-normative-contradictions-audit.md](../../../../docs/audit/2026-08-21-hub-structural-normative-contradictions-audit.md).

Черновик живёт здесь, а не в `templates/htom/`, намеренно: до human decision gate
геном не изменяется, но предложение должно быть проверяемым, а не описательным.

| Файл | Что это |
| --- | --- |
| `htom-validate-repository-structure-draft.sh` | Предлагаемая редакция `templates/htom/tools/validate-repository-structure.sh` (решение G-01 + требование CI из G-02) |
| `htom-validate-workflow-draft.yml` | Предлагаемый `templates/htom/.github/workflows/validate.yml` (решение G-02) |
| `hub-profile-example.json` | Пример `.hub-profile.json` спицы с декларацией специфичных каталогов (`project_specific_directories`) и льготным сроком (`structure_grandfather_until`) — механизм из RFC v0.2 (issue #535) |
| `validate-draft.sh` | Гарнитура из тринадцати сценариев: собирает синтетические HTOM-команды из текущего генома и сверяет фактический exit code с ожидаемым |
| `validate-draft.log` | Лог прогона `validate-draft.sh` от 2026-08-22 |

Скрипты работают только во временном каталоге (`mktemp -d`) и ничего не меняют
ни в репозитории Хаба, ни в геноме.

## Сценарии и результат прогона 2026-08-22

| # | Сценарий | Ожидание | Факт |
| --- | --- | --- | --- |
| A | Корневая раскладка управляющих файлов (как сейчас в спицах) | pass | pass |
| B | Раскладка `governance/` (целевая в [mango PR #292](https://github.com/G-Ivan-A/mango_ba_prompts/pull/292)) | pass | pass |
| C | Раскладка `ai-governance/` + `ai-rules/` (фактическая раскладка Хаба после B-056) | pass | pass |
| D | Управляющего контракта нет ни в одном из разрешённых мест | fail | fail |
| E | Один контракт лежит в двух местах сразу (два SSOT) | fail | fail |
| F | В HTOM-команде нет `.github/workflows/validate.yml` (собственно G-02) | fail | fail |
| G | Handover-промпт переехал и потерял `{{REPO_NAME}}` | fail | fail |
| H | Недекларированный каталог проекта (limbo state после реструктуризации) | fail | fail |
| I | Тот же каталог задекларирован в `.hub-profile.json` как специфичный | pass | pass |
| J | Декларация без `reason` (объявление без обоснования) | fail | fail |
| K | Льготный период (`structure_grandfather_until`) активен | pass (warn) | pass |
| L | Льготный период истёк | fail | fail |
| M | `.archive/` без `README.md` | fail | fail |
| N | `.archive/` с `README.md` (легитимный архив переходного каталога) | pass | pass |

Итог прогона: `Draft validation passed: 13/13 сценариев совпали с ожиданием.`

Сценарии A и C вместе доказывают ключевое утверждение RFC: предлагаемое правило
одновременно легализует раскладку самого Хаба и не ломает ни одну существующую
спицу, то есть не является breaking change.

Сценарии H–N (добавлены в v0.2 по issue #535) доказывают вторую половину
баланса: специфичный для проекта каталог **сохраняется** при реструктуризации,
если он задекларирован с причиной (I), но недекларированный переходный каталог
становится машинно наблюдаемой ошибкой (H, L), а не молчаливым техническим
долгом. Льготный период (K) даёт существующим спицам один цикл синхронизации на
декларацию, после чего правило становится жёстким (L).

Запуск из любого каталога репозитория:

```bash
./research/hub/exp/htom-genome-rfc-531/validate-draft.sh
```
