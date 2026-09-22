---
status: draft
version: 2.1
updated: 2026-09-22
temperature: 0.1
---

# Пакет исполнения BCREQ для GigaCode CLI

Компиляция вертикального среза `A-IN → A-CORE → A-BCREQ` для продуктового
класса «контакт-центр» в копируемую и проверяемую форму для GigaCode CLI.

Пакет — **артефакт компиляции**, а не ещё один исследовательский модуль:
исследовательские тексты в нём не дублируются, их нормативные следствия
перенесены в навыки, схемы и правила. Состав скопированного, преобразованного и
отброшенного объявлен в `package-manifest.yaml`.

## Состав

| Каталог | Содержание |
| --- | --- |
| `.gigacode/skills/` | явный dispatcher, изолированный debug-оркестратор и 11 `SKILL.md` узлов маршрута |
| `.gigacode/settings.example.json` | безопасный capability-пример Confluence MCP без URL и секретов |
| `docs/kb/` | место для локальной базы знаний, дополняющей Confluence |
| `meta-model/` | место для канонической модели, добавляемой при подготовке копии |
| `taxonomy/` | закрытые словари артефактов, процессов, операций, продуктов, источников, проекций и терминов |
| `contracts/` | `C-IN`, `C-CORE`, `C-CL`, `C-OUT`, `C-RK` как JSON Schema |
| `routes/` | граф `RG-BCREQ-v1` и шаблон append-only листа прогона |
| `templates/` | скелеты пользовательских артефактов и Markdown checkpoint |
| `golden/` | утверждённые эталоны и отдельное место для ручных кандидатов |
| `evaluation/` | метрики и чек-листы гейтов |
| `runs/` | task-rooted состояние и изолированные `DEBUG-*` прогоны; в Git хранится только placeholder |
| `tools/` | shell entrypoint и Python-гейт `G-mach` |
| `AGENTS.md` | загрузочный контракт GigaCode CLI с исполняемыми правилами |

## Как развернуть

```sh
cp -R projects/ba-ai-process/dist/execution-package-gigacode-cli/. <clean-directory>/
cd <clean-directory> && pip install pyyaml && sh tools/validate-package.sh
```

Пакет может исполняться без доступа к репозиторию модели. Поэтому он содержит
физические копии, а не runtime-ссылки наружу. При подготовке конкретной копии
человек наполняет `meta-model/` и `docs/kb/` разрешёнными материалами.

## Как проверить

```sh
sh projects/ba-ai-process/dist/execution-package-gigacode-cli/tools/validate-package.sh
```

Валидатор проверяет layout и manifest hashes, нативный путь `.gigacode/skills/`, обязательные
оркестраторы, закрытость словарей, разрешимость графа, zero-correction policy,
микро-событийный trace, структуру навыков, Golden Set, метрики, дополняющую
маршрутизацию источников, согласованность run template с `C-RK` и отсутствие
runtime-ссылок на Source
[`G-Ivan-A/hybrid-Intelligence-lab`](https://github.com/G-Ivan-A/hybrid-Intelligence-lab),
а также отсутствие RRP, ADR/RFC, backlog и прочего Source rationale.

## Как запустить

1. Наполнить `meta-model/` и `docs/kb/`, не меняя скомпилированные правила.
2. При необходимости создать локальный `.gigacode/settings.json` по example и
   включить одобренный Confluence MCP без коммита секретов.
3. В GigaCode CLI явно вызвать `/skills rg-bcreq-v1-dispatcher`, затем передать
   `TASK-NNNN`. Новая сессия продолжает тот же task по файлам состояния.
4. Читать и подтверждать checkpoints в `runs/<TASK_ID>/evidence/*.md`;
   машинный YAML остаётся журналом, а не пользовательским интерфейсом.

Для проверки механики без LLM и внешних систем используется
`/skills ba-debug-orchestrator`; он пишет только в
`runs/DEBUG-<TIMESTAMP>/`. Автоматическое продвижение run в Golden Set
запрещено. Пакет автономен: необходимые команды запуска и диагностики приведены
здесь и в `AGENTS.md`; внешняя conceptual-документация не является
runtime-зависимостью.

## Отклонение от исходной таксономии

Исходная постановка относила к `P-01` три навыка; сборка `A-CORE` оставалась
без исполнителя. Пакет сохраняет принятое решение: 11 навыков узлов, включая
`core-assembly-contact-center`, плюс два служебных оркестратора.

## Источник истины

Развивающаяся модель живёт в этом репозитории. Правка нормативного содержания в
развёрнутой копии — дефект процесса: наблюдение возвращается задачей сюда,
после чего пакет компилируется заново со сменой `source.revision` и
`compiled_at`.
