---
status: canonical
version: 0.1
updated: 2026-11-03
temperature: 0.1
executable: true
type: instruction
context: [governance, spokes, extraction, synchronization]
method: operating-contract
scope: repo-wide
related_artifacts:
  - "tools/spoke-extraction.py"
  - "tools/test-spoke-extraction.sh"
  - "templates/spoke/"
  - "docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md"
  - "docs/ecosystem-map.md"
related_issues:
  - "https://github.com/G-Ivan-A/hybrid-Intelligence-lab/issues/717"
---

# Контракт выноса проекта Хаба в спицу

> 🚦 **STOP — не анализируй, выполняй.**
> Ты — агент репозитория-спицы, в которую переносится проект Хаба. Твоя цель —
> сформировать структуру этого репозитория и перенести в него данные Хаба так,
> чтобы каждый перенесённый байт подтверждался хешем Хаба. Выполни один этап из
> раздела EXECUTION сейчас; обоснование — в разделе EXPLANATION ниже.

## ▶️ EXECUTION

Выполни ровно один этап: тот, что указан в параметре `STAGE` задачи, а без
`STAGE` — первый этап без отметки ✅ в журнале импорта. Один этап — один pull
request. Все значения бери только из блока параметров задачи и из вывода команд.

### Шаг 0. Общая подготовка (каждый этап)

1. Прочитай задачу и сохрани блок параметров: задача содержит ровно один блок
   кода с меткой `extraction-params` (формат — в разделе «Шаблон задачи»).

   ```bash
   set -euo pipefail
   ISSUE=<номер текущей задачи>
   WORK="$(mktemp -d)"   # рабочий каталог вне репозитория
   gh issue view "$ISSUE" --json body -q .body > "$WORK/issue.md"
   awk '/^```extraction-params$/{f=1;next} /^```$/{f=0} f' "$WORK/issue.md" > "$WORK/params.txt"
   param() { sed -n "s/^$1: //p" "$WORK/params.txt"; }
   HUB_REPO="$(param HUB_REPO)"; HUB_SHA="$(param HUB_SHA)"; STAGE="$(param STAGE)"
   mapfile -t MAPS < <(param MAP);         mapfile -t EXCLUDES < <(param EXCLUDE)
   mapfile -t DIRS < <(param DIR);         mapfile -t HEADINGS < <(param BACKLOG)
   mapfile -t CI_JOBS < <(param CI_JOB);   mapfile -t CI_STEPS < <(param CI_STEP)
   mapfile -t HISTORICAL < <(param HISTORICAL)
   MAP_ARGS=(); for m in "${MAPS[@]}"; do MAP_ARGS+=(--map "$m"); done
   EXCL_ARGS=(); for e in "${EXCLUDES[@]}"; do [[ -n "$e" ]] && EXCL_ARGS+=(--exclude "$e"); done
   ```

2. Получи Хаб и инструмент **из закреплённого коммита** `HUB_SHA`:

   ```bash
   HUB_URL="https://github.com/$HUB_REPO"
   TARGET_URL="$(gh repo view --json url -q .url)"
   TARGET_ROOT="$(git rev-parse --show-toplevel)"
   git clone --quiet --no-checkout "$HUB_URL.git" "$WORK/hub"
   [[ "$HUB_SHA" =~ ^[0-9a-f]{40}$ ]]
   git -C "$WORK/hub" merge-base --is-ancestor "$HUB_SHA" origin/main
   git -C "$WORK/hub" show "$HUB_SHA:tools/spoke-extraction.py" > "$WORK/spoke-extraction.py"
   X() { python3 -I "$WORK/spoke-extraction.py" --hub "$WORK/hub" "$@"; }
   EVID="docs/import/hub-${HUB_SHA:0:12}"
   ```

3. Проверь заморозку источника: команда выводит пустой список.

   ```bash
   SOURCES=(); for m in "${MAPS[@]}"; do SOURCES+=("${m%%=*}"); done
   git -C "$WORK/hub" log --oneline "$HUB_SHA..origin/main" -- "${SOURCES[@]}"
   ```

   Непустой вывод означает, что источник изменился после закрепления: опубликуй
   в задаче список коммитов и вопрос владельцу о новом `HUB_SHA`, затем
   остановись. Новый `HUB_SHA` выбирает только владелец.

4. Построй манифест переноса и сравни его с журналом (начиная с этапа E2):

   ```bash
   X manifest --sha "$HUB_SHA" "${MAP_ARGS[@]}" "${EXCL_ARGS[@]}" -o "$WORK/manifest.tsv"
   [[ ! -f "$EVID/manifest.tsv" ]] || cmp "$WORK/manifest.tsv" "$EVID/manifest.tsv"
   ```

### Этап E1. Скелет генома

1. Построй манифест генома из шаблонов Хаба на `HUB_SHA`:

   ```bash
   X manifest --sha "$HUB_SHA" \
     --map templates/spoke/= \
     --map templates/htom/.github/ISSUE_TEMPLATE/=.github/ISSUE_TEMPLATE/ \
     --map templates/htom/tools/validate-agents-bootstrap.sh=tools/validate-agents-bootstrap.sh \
     --exclude templates/spoke/README.md -o "$WORK/genome.tsv"
   ```

2. Убедись, что геном и перенос не пересекаются по путям, а список
   проектных каталогов совпадает с параметрами `DIR`. Обе команды выводят
   пустой результат:

   ```bash
   comm -12 <(grep -v '^#' "$WORK/genome.tsv" | cut -f3 | sort) \
            <(grep -v '^#' "$WORK/manifest.tsv" | cut -f3 | sort)
   CANON="$( { grep -v '^#' "$WORK/genome.tsv" | cut -f3 | grep / | cut -d/ -f1; echo ops; } | sort -u)"
   diff <(grep -v '^#' "$WORK/manifest.tsv" | cut -f3 | grep / | cut -d/ -f1 | sort -u | grep -vxF "$CANON") \
        <(printf '%s\n' "${DIRS[@]}" | cut -d'|' -f1 | sed 's/ *$//' | sort -u)
   ```

3. Запиши геном в репозиторий:

   ```bash
   X materialize --manifest "$WORK/genome.tsv" --target "$TARGET_ROOT" \
     --substitute project_name="$(basename "$TARGET_URL")" \
     --substitute hub_url="$HUB_URL" --substitute date="$(date -u +%F)"
   ```

   Вывод `placeholder left` перечисли в описании pull request.

4. Заполни профиль: проектные каталоги из `DIR` и запись синхронизации.

   ```bash
   printf '%s\n' "${DIRS[@]}" > "$WORK/dirs.txt"
   python3 -I - "$TARGET_ROOT/.hub-profile.json" "$WORK/dirs.txt" "$HUB_SHA" "$(date -u +%F)" <<'PY'
   import json, sys
   path, dirs, sha, day = sys.argv[1:5]
   profile = json.load(open(path, encoding="utf-8"))
   rows = [line.split("|", 1) for line in open(dirs, encoding="utf-8") if line.strip()]
   profile["project_specific_directories"] = [
       {"path": p.strip(), "reason": r.strip()} for p, r in sorted(rows)]
   profile["last_sync"] = {"hub_sha": sha, "date": day, "scope": "genome",
                           "tool": "tools/spoke-extraction.py@" + sha[:12]}
   open(path, "w", encoding="utf-8").write(json.dumps(profile, ensure_ascii=False, indent=2) + "\n")
   PY
   ```

5. Создай журнал импорта и сохрани манифесты:

   ```bash
   mkdir -p "$EVID"
   cp "$WORK/manifest.tsv" "$WORK/genome.tsv" "$EVID/"
   ```

   Журнал `$EVID/README.md` создай по шаблону из раздела «Журнал импорта»;
   строку E1 отметь ✅.

6. Проверь результат: обе команды завершаются с кодом 0.

   ```bash
   bash tools/validate-agents-bootstrap.sh "$TARGET_ROOT"
   ./tools/validate-file-naming.sh
   ```

7. Открой pull request «E1: скелет генома» с выводом команд шагов 1–6.

### Этап E2. Импорт с историей

1. Установи `git filter-repo` закреплённой версии в рабочий каталог:

   ```bash
   python3 -m venv "$WORK/venv" && "$WORK/venv/bin/pip" install --quiet git-filter-repo==2.47.0
   ```

2. Собери пути истории: текущие источники и их прошлые имена.

   ```bash
   X history-paths --manifest "$EVID/manifest.tsv" > "$WORK/history.txt"
   { printf '%s\n' "${SOURCES[@]}"; cat "$WORK/history.txt"; } | sort -u > "$WORK/paths.txt"
   ```

3. Отфильтруй копию Хаба, закреплённую на `HUB_SHA`:

   ```bash
   git clone --quiet --no-local --single-branch --branch main "$WORK/hub" "$WORK/filtered"
   git -C "$WORK/filtered" reset --quiet --hard "$HUB_SHA"
   RENAMES=(); for m in "${MAPS[@]}"; do s="${m%%=*}"; d="${m#*=}"; [[ "$s" == "$d" ]] || RENAMES+=(--path-rename "$s:$d"); done
   (cd "$WORK/filtered" && "$WORK/venv/bin/git-filter-repo" --force --preserve-commit-hashes \
      --paths-from-file "$WORK/paths.txt" "${RENAMES[@]}" \
      --message-callback "return re.sub(rb'(?<![\\w/.-])#(\\d+)', rb'$HUB_REPO#\\1', message)")
   ```

   При непустом `EXCLUDE` выполни второй проход с `--invert-paths
   --paths-from-file` по списку `EXCLUDE`.

4. Сверь отфильтрованное дерево с манифестом: отчёт `"ok"` равен числу
   файлов, списки пусты.

   ```bash
   X verify --manifest "$EVID/manifest.tsv" --target "$WORK/filtered" --extra-scope "" > "$WORK/verify-filtered.json"
   ```

5. Влей историю в текущую ветку:

   ```bash
   git fetch --quiet "$WORK/filtered" main:refs/hub-import/main
   git merge --allow-unrelated-histories --no-ff --no-edit \
     -m "import: $HUB_REPO@${HUB_SHA:0:12} с историей" refs/hub-import/main
   ```

   Единственный допустимый конфликт — `README.md`, созданный GitHub при
   создании репозитория: прими версию импорта (`git checkout --theirs
   README.md && git add README.md && git commit --no-edit`). Любой другой
   конфликт опубликуй в задаче как вопрос и остановись.

6. Сверь рабочее дерево и сохрани доказательства:

   ```bash
   X verify --manifest "$EVID/manifest.tsv" --target "$TARGET_ROOT" > "$EVID/verify-import.json"
   cp "$WORK/verify-filtered.json" "$WORK/history.txt" "$EVID/"
   cp "$WORK/filtered/.git/filter-repo/commit-map" "$EVID/commit-map.txt"
   git -C "$WORK/filtered" rev-list --count HEAD > "$EVID/commit-count.txt"
   ```

7. Запиши ADR импорта по шаблону «ADR импорта» в
   `docs/adr/<YYYY-MM>-adr-<NNN>-hub-import.md`, где `NNN` — наибольший номер
   ADR в `docs/adr/` плюс один (`001`, если ADR нет). Отметь E2 ✅ в журнале.
8. Открой pull request «E2: импорт с историей». В описании укажи способ
   слияния **Create a merge commit**: он сохраняет импортированную историю.

### Этап E3. Ссылки

1. Перепиши ссылки и сохрани журнал преобразований:

   ```bash
   X rewrite-links --manifest "$EVID/manifest.tsv" --target "$TARGET_ROOT" \
     --hub-url "$HUB_URL" --target-url "$TARGET_URL" --log "$EVID/rewrite-links.jsonl"
   ```

2. Проверь идемпотентность и итог: обе команды завершаются с кодом 0.

   ```bash
   X rewrite-links --manifest "$EVID/manifest.tsv" --target "$TARGET_ROOT" \
     --hub-url "$HUB_URL" --target-url "$TARGET_URL" --check
   X verify --manifest "$EVID/manifest.tsv" --target "$TARGET_ROOT" --links \
     --hub-url "$HUB_URL" --target-url "$TARGET_URL" > "$EVID/verify-links.json"
   ```

3. Внеси в журнал счётчики событий по видам (`file-in`, `dir-in`, `file-out`,
   `dir-out`, `url-in`, `unresolved`, `outside-repo`) и отметь E3 ✅.
4. Открой pull request «E3: ссылки».

### Этап E4. Код и CI

1. Получи список остатков старых путей:

   ```bash
   X scan --manifest "$EVID/manifest.tsv" --target "$TARGET_ROOT" > "$EVID/scan-before.txt"
   ```

2. Разбери каждую строку `scan-before.txt` по первому подходящему правилу:
   - путь файла начинается с префикса из `HISTORICAL` — запись решения,
     остаётся дословной;
   - файл порождается компилятором проекта (каталог, который компилятор пишет
     и проверяет флагом `--check`) — изменяется только перекомпиляцией в шаге 4;
   - иначе — исправь выражение так, чтобы оно указывало на новое место по
     правилам `MAP`, а адрес репозитория, собираемый с путём из набора, — на
     `TARGET_URL`. Других изменений в этих файлах нет.
3. Перенеси CI: из `.github/workflows/validate.yml` Хаба на `HUB_SHA`
   (`git -C "$WORK/hub" show "$HUB_SHA:.github/workflows/validate.yml"`)
   скопируй задания из `CI_JOB` целиком, а шаги из `CI_STEP` (шаг `name` в
   задании `id`) — в задание `test` файла `.github/workflows/ci.yml`; пути в командах приведи по правилам
   `MAP`. Шаги-заглушки `TODO` заданий `lint` и `test` замени перенесёнными
   командами; шаг `Validate documentation file naming` сохрани.
4. Перекомпилируй порождённые каталоги компиляторами проекта с ревизией
   коммита этого pull request, который содержит исправленные исходники
   (`--source-revision "$(git rev-parse HEAD)"`), закоммить результат и
   запусти каждый компилятор с `--check`: все завершаются с кодом 0.
5. Запусти все команды перенесённого CI локально, где это позволяет среда;
   остальное подтверждает CI pull request.
6. Сохрани итог: остаток должен состоять только из строк `HISTORICAL`.

   ```bash
   X scan --manifest "$EVID/manifest.tsv" --target "$TARGET_ROOT" > "$EVID/scan-after.txt"
   git diff --name-only "$(git merge-base HEAD origin/main)" -- . ':!docs/import' | sort > "$EVID/adapted.txt"
   ```

7. Отметь E4 ✅ в журнале и открой pull request «E4: код и CI».

### Этап E5. Бэклог

1. Извлеки разделы бэклога Хаба дословно:

   ```bash
   H_ARGS=(); for h in "${HEADINGS[@]}"; do H_ARGS+=(--heading "$h"); done
   X sections --sha "$HUB_SHA" --source ops/backlog.md --manifest "$EVID/manifest.tsv" \
     --target-path ops/backlog.md --hub-url "$HUB_URL" --target-url "$TARGET_URL" \
     "${H_ARGS[@]}" -o "$WORK/sections.md"
   ```

2. Создай `ops/backlog.md`: шапка по шаблону «Шапка бэклога», затем
   содержимое `$WORK/sections.md` без изменений. ID задач сохраняются (карта
   ID — тождественная); новые задачи нумеруются от наибольшего ID плюс один.
3. Проверь перенос: команда завершается с кодом 0.

   ```bash
   X sections --sha "$HUB_SHA" --source ops/backlog.md --manifest "$EVID/manifest.tsv" \
     --target-path ops/backlog.md --hub-url "$HUB_URL" --target-url "$TARGET_URL" \
     "${H_ARGS[@]}" --check ops/backlog.md
   grep -o '^| \*\*B-[0-9]*\*\*' ops/backlog.md | tr -d '|* ' > "$EVID/backlog-ids.txt"
   ```

4. Отметь E5 ✅ в журнале (число строк из `backlog-ids.txt`) и открой pull
   request «E5: бэклог».

### Этап E6. Проверка

1. Повтори Шаг 0 (заморозка и манифест) и выполни:

   ```bash
   X verify --manifest "$EVID/manifest.tsv" --target "$TARGET_ROOT" --links \
     --hub-url "$HUB_URL" --target-url "$TARGET_URL" > "$WORK/verify-final.json" || true
   python3 -I -c 'import json,sys; r=json.load(open(sys.argv[1])); a=set(open(sys.argv[2]).read().split()); bad=[f for f in r["mismatch"]+r["mode_mismatch"] if f not in a]; print(json.dumps({"missing": r["missing"], "unexplained": bad})); sys.exit(1 if r["missing"] or bad else 0)' \
     "$WORK/verify-final.json" "$EVID/adapted.txt"
   X sections --sha "$HUB_SHA" --source ops/backlog.md --manifest "$EVID/manifest.tsv" \
     --target-path ops/backlog.md --hub-url "$HUB_URL" --target-url "$TARGET_URL" \
     "${H_ARGS[@]}" --check ops/backlog.md
   bash tools/validate-agents-bootstrap.sh "$TARGET_ROOT" && ./tools/validate-file-naming.sh
   ```

   Каждое расхождение с файлом вне `adapted.txt` верни дословной копией из
   Хаба (`X materialize --overwrite` по манифесту из одного файла) или
   опиши в задаче как вопрос.
2. Сохрани `verify-final.json` в `$EVID/`, заполни таблицу «Итог» журнала и
   отметь E6 ✅.
3. Открой pull request «E6: проверка» с закрывающим ключевым словом задачи и
   постоянными ссылками на журнал.

## ℹ️ EXPLANATION

### Почему этапы и инструмент

Копирование «по памяти» модели порождает галлюцинации: пропущенные файлы,
пересказ вместо текста, выдуманные пути. Поэтому байты переносит
детерминированный инструмент Хаба `tools/spoke-extraction.py`, а агент пишет
вручную только перечисленное в таблице ниже. Каждый этап завершается
проверкой, которая сравнивает результат с Хабом по хешу git blob.

| Этап | Что переносит инструмент | Что пишет агент | Проверка |
| --- | --- | --- | --- |
| E1 | Геном спицы на `HUB_SHA` | Профиль (скриптом), журнал | `validate-agents-bootstrap.sh`, `validate-file-naming.sh` |
| E2 | Файлы и история источников | ADR импорта, журнал | `verify` (дословно) на дереве и на фильтре |
| E3 | Переписанные ссылки | Журнал | `rewrite-links --check`, `verify --links` |
| E4 | — | Выражения из `scan`, CI | `--check` компиляторов, CI, `scan-after` ⊆ `HISTORICAL` |
| E5 | Разделы бэклога | Шапка бэклога, журнал | `sections --check` |
| E6 | — | Журнал | `verify --links` ⊆ `adapted.txt`, `sections --check`, валидаторы |

### Правила копирования

1. **Один источник значений.** Пути, SHA, каталоги, задания CI и разделы
   бэклога берутся из блока `extraction-params`. Значение, которого там нет,
   агент запрашивает в задаче.
2. **Один закреплённый коммит.** Все чтения Хаба идут через `HUB_SHA`;
   инструмент отвергает ветку вместо SHA. Плавающая `main` используется только
   для проверки заморозки в Шаге 0.
3. **Байты — командой.** Файлы проекта, история, ссылки и разделы бэклога
   переносятся подкомандами инструмента; их вывод прикладывается к pull request.
4. **Утверждение — с доказательством.** Каждое число в журнале и pull request
   — вывод команды, сохранённый в `docs/import/hub-<sha12>/`.
5. **Расхождение — вопрос.** Ненулевой код проверки останавливает этап: агент
   публикует в задаче вывод и вопрос с вариантами и рекомендацией.
6. **Запись решения неизменна.** ADR, RFC, анализы и прочие префиксы из
   `HISTORICAL` переносятся дословно: ссылки в них переписывает только E3.

### Правила ссылок

- **L1 (Markdown).** Относительная ссылка разрешается от места файла в Хабе.
  Цель внутри набора получает относительный путь к новому месту; цель вне
  набора — постоянную ссылку на Хаб `blob/<HUB_SHA>` или `tree/<HUB_SHA>`;
  отсутствующая цель остаётся как есть и попадает в журнал (`unresolved`).
  Блоки и фрагменты кода не изменяются.
- **L2 (любой текст).** URL `<HUB_URL>/(blob|tree)/main/<путь из набора>`
  становится `<TARGET_URL>/(blob|tree)/main/<новый путь>`. Постоянные ссылки на
  SHA Хаба остаются: они продолжают открывать тот же текст.

### Шаблон задачи

Владелец создаёт в новом репозитории задачу с таким телом:

````markdown
Выполни контракт выноса:
https://github.com/G-Ivan-A/hybrid-Intelligence-lab/blob/<HUB_SHA>/ops/hub-project-extraction-contract.md

```extraction-params
HUB_REPO: G-Ivan-A/hybrid-Intelligence-lab
HUB_SHA: <40 hex>
MAP: <путь в Хабе>/=<путь в спице>/ или пусто для корня
DIR: <каталог корня> | <причина>
CI_JOB: <id задания validate.yml>
CI_STEP: <id задания validate.yml> / <name шага в нём>
BACKLOG: <префикс заголовка раздела бэклога, например «## Спринт 14:»>
HISTORICAL: <префикс пути в спице, переносимый дословно>
EXCLUDE: <путь в Хабе, исключаемый из переноса>
STAGE: <E1…E6 или пусто>
```
````

Каждый параметр, кроме `HUB_REPO`, `HUB_SHA` и `STAGE`, повторяется строкой
на значение. Контракт читается по той же постоянной ссылке `HUB_SHA`, что и
инструмент.

### Журнал импорта

`docs/import/hub-<sha12>/README.md`:

```markdown
# Импорт из Хаба <HUB_REPO>@<sha12>

Контракт: <постоянная ссылка на контракт на HUB_SHA>. Задача: #<ISSUE>.

| Этап | Статус | Pull request | Доказательство |
| --- | --- | --- | --- |
| E1 Скелет генома | ⬜ | | `genome.tsv`, `manifest.tsv` |
| E2 Импорт с историей | ⬜ | | `verify-import.json`, `verify-filtered.json`, `commit-map.txt`, `commit-count.txt`, `history.txt` |
| E3 Ссылки | ⬜ | | `rewrite-links.jsonl`, `verify-links.json` |
| E4 Код и CI | ⬜ | | `scan-before.txt`, `scan-after.txt`, `adapted.txt` |
| E5 Бэклог | ⬜ | | `backlog-ids.txt` |
| E6 Проверка | ⬜ | | `verify-final.json` |

## Итог

| Показатель | Значение |
| --- | --- |
| Файлов в манифесте | |
| Коммитов истории | |
| Событий ссылок по видам | |
| Адаптированных файлов | |
| Строк бэклога | |
```

### ADR импорта

```markdown
---
status: accepted
version: 1.0
updated: <YYYY-MM-DD>
temperature: 0.1
---

# ADR-<NNN>: импорт проекта из Хаба

## Context

Проект перенесён из <HUB_URL> по контракту выноса
(<постоянная ссылка на контракт на HUB_SHA>) по задаче #<ISSUE>.

## Decision

Источник — коммит `<HUB_SHA>`. Правила переноса (`MAP`):
<строки MAP из параметров>. История импортирована `git filter-repo 2.47.0`
(<число из commit-count.txt> коммитов); ссылки `#NNN` в сообщениях
коммитов указывают на задачи Хаба (`<HUB_REPO>#NNN`); карта старых и новых
хешей — `docs/import/hub-<sha12>/commit-map.txt`.

## Consequences

Файлы проекта сверены с Хабом по хешу (`verify-import.json`). Дальнейшее
развитие ведётся в этом репозитории; Хаб хранит историю до `<HUB_SHA>`.
```

### Шапка бэклога

```markdown
---
status: canonical
version: 1.0
updated: <YYYY-MM-DD>
temperature: 0.1
---

# Бэклог

Разделы ниже перенесены из бэклога Хаба на `<HUB_SHA>` (<постоянная ссылка на
ops/backlog.md Хаба на HUB_SHA>) без изменений текста; ID сохранены. Формат
строк — по инструкции бэклога Хаба (<постоянная ссылка на
ops/backlog-instruction.md на HUB_SHA>).
```

### Границы контракта

- Контракт — **временное исключение** до принятия контракта наследования
  (шаг 2 [RFC #715](../docs/rfc/2026-11-02-rfc-hub-governance-optimization-roadmap.md)).
  После него геном нового репозитория создаёт канонический инструмент
  синхронизации (I-4), а E1 этого контракта заменяется им.
- Изменения на стороне Хаба после E6 — перевод закрепления runtime на новый
  репозиторий и «надгробие» в Хабе — выполняются отдельными задачами Хаба по
  журналу импорта.
- Инструмент проверяется регрессионным тестом `tools/test-spoke-extraction.sh`
  в CI Хаба; поведение, на которое опирается этот контракт, покрыто тестом.
