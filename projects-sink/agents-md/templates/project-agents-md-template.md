---
status: canonical
version: 1.0
updated: 2026-09-19
temperature: 0.1
---

# Каркас проектного `AGENTS.md`

Этот файл — инструкция сборки, а не копируемый `AGENTS.md`. General layer нельзя
дублировать здесь: исполнитель берёт его из актуального
`templates/{{archetype_template}}/AGENTS.md` на зафиксированном Hub commit.

## Параметры сборки

| Параметр | Источник |
| --- | --- |
| `project_name` | локальный README/concept |
| `archetype`, `environment`, `secondary_environments` | `.hub-profile.json` |
| `hub_commit_sha` | задача синхронизации |
| `project_specific_rules` | принятые локальные контракты |
| local routes/homes/validation | существующие файлы и команды проекта |

## Обязательная форма результата

```text
frontmatter: status, version, updated, temperature, entrypoint
<scope>profile values + layer contract</scope>
<hard_rules>general layer из Hub template без ослабления</hard_rules>
<forbidden>general layer из Hub template без ослабления</forbidden>
<guidelines>general layer из Hub template</guidelines>
<hybrid_work>general layer из Hub template</hybrid_work>
<project_specific_rules>только подтверждённая локальная дельта</project_specific_rules>
<routing>absolute Hub URLs + существующие local routes</routing>
<artifact_homes>реальные canonical homes проекта</artifact_homes>
<issue_levels>general layer из Hub template</issue_levels>
<missing_tags>general layer из Hub template</missing_tags>
<context_scope>локальный порядок загрузки контекста</context_scope>
<validation>реальные команды проекта</validation>
<models>единственная точка входа + generated adapters</models>
<escalation>general layer из Hub template</escalation>
```

## Проверка перед записью

- выбрана ровно одна архетипная основа: `htom` или `spoke`;
- profile существует и не содержит неизвестных значений;
- нет правил, источником которых является этот каркас;
- средовая дельта прошла условия
  [environment-specific.md](../environment-specific.md);
- происхождение фиксируется точным commit SHA в механизме B-111/PR, но не
  неразрешённым frontmatter field.
