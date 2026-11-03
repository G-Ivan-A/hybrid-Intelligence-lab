#!/usr/bin/env bash
# Rehearsal of ops/hub-project-extraction-contract.md stages E1, E2, E3 and E5
# for the BA instance parameters (ba-instance-params.txt), issue #717.
#
# Mirrors the contract commands with three substitutions that a rehearsal
# needs: the parameter block is read from a file instead of `gh issue view`,
# the target is a fresh local git repository instead of the new GitHub
# repository, and the tool comes from this branch because HUB_SHA predates it.
#
# Usage: bash rehearse-contract.sh PARAMS HUB_CLONE TOOL OUT_DIR
#   PARAMS     the extraction-params block (ba-instance-params.txt)
#   HUB_CLONE  a clone of the Hub with origin/main containing HUB_SHA
#   TOOL       path to tools/spoke-extraction.py
#   OUT_DIR    new empty directory for the rehearsal target and logs
# Requires: git, python3, a git-filter-repo 2.47.0 executable in $GFR.
set -euo pipefail
PARAMS="$(realpath "$1")"; HUB="$(realpath "$2")"; TOOL_SRC="$(realpath "$3")"; OUT="$4"
GFR="${GFR:?set GFR to a git-filter-repo 2.47.0 executable}"
mkdir "$OUT"; OUT="$(realpath "$OUT")"
WORK="$OUT/work"; mkdir "$WORK"

# --- Step 0 ---------------------------------------------------------------
param() { sed -n "s/^$1: //p" "$PARAMS"; }
HUB_REPO="$(param HUB_REPO)"; HUB_SHA="$(param HUB_SHA)"
mapfile -t MAPS < <(param MAP);       mapfile -t EXCLUDES < <(param EXCLUDE)
mapfile -t DIRS < <(param DIR);       mapfile -t HEADINGS < <(param BACKLOG)
MAP_ARGS=(); for m in "${MAPS[@]}"; do MAP_ARGS+=(--map "$m"); done
EXCL_ARGS=(); for e in "${EXCLUDES[@]}"; do [[ -n "$e" ]] && EXCL_ARGS+=(--exclude "$e"); done
HUB_URL="https://github.com/$HUB_REPO"
TARGET_URL="https://github.example/owner/spoke-rehearsal"
git clone --quiet --no-checkout "$HUB" "$WORK/hub"
git -C "$WORK/hub" fetch --quiet "$HUB" "+refs/remotes/origin/main:refs/remotes/origin/main"
[[ "$HUB_SHA" =~ ^[0-9a-f]{40}$ ]]
git -C "$WORK/hub" merge-base --is-ancestor "$HUB_SHA" origin/main
cp "$TOOL_SRC" "$WORK/spoke-extraction.py"
X() { python3 -I "$WORK/spoke-extraction.py" --hub "$WORK/hub" "$@"; }
SOURCES=(); for m in "${MAPS[@]}"; do SOURCES+=("${m%%=*}"); done
echo "freeze: $(git -C "$WORK/hub" log --oneline "$HUB_SHA..origin/main" -- "${SOURCES[@]}" | wc -l) commit(s) touch the sources after HUB_SHA"
X manifest --sha "$HUB_SHA" "${MAP_ARGS[@]}" "${EXCL_ARGS[@]}" -o "$WORK/manifest.tsv"

TARGET_ROOT="$OUT/target"
git init --quiet -b main "$TARGET_ROOT"
cd "$TARGET_ROOT"
git config user.email rehearsal@example.invalid; git config user.name rehearsal
printf '# spoke-rehearsal\n' > README.md; git add README.md; git commit --quiet -m "Initial commit"
EVID="docs/import/hub-${HUB_SHA:0:12}"

# --- E1 -------------------------------------------------------------------
X manifest --sha "$HUB_SHA" \
  --map templates/spoke/= \
  --map templates/htom/.github/ISSUE_TEMPLATE/=.github/ISSUE_TEMPLATE/ \
  --map templates/htom/tools/validate-agents-bootstrap.sh=tools/validate-agents-bootstrap.sh \
  --exclude templates/spoke/README.md -o "$WORK/genome.tsv"
echo "E1 genome/import path intersection:"
comm -12 <(grep -v '^#' "$WORK/genome.tsv" | cut -f3 | sort) \
         <(grep -v '^#' "$WORK/manifest.tsv" | cut -f3 | sort)
CANON="$( { grep -v '^#' "$WORK/genome.tsv" | cut -f3 | grep / | cut -d/ -f1; echo ops; } | sort -u)"
echo "E1 DIR check (empty = equal):"
diff <(grep -v '^#' "$WORK/manifest.tsv" | cut -f3 | grep / | cut -d/ -f1 | sort -u | grep -vxF "$CANON") \
     <(printf '%s\n' "${DIRS[@]}" | cut -d'|' -f1 | sed 's/ *$//' | sort -u)
X materialize --manifest "$WORK/genome.tsv" --target "$TARGET_ROOT" \
  --substitute project_name="$(basename "$TARGET_URL")" \
  --substitute hub_url="$HUB_URL" --substitute date="$(date -u +%F)"
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
mkdir -p "$EVID"; cp "$WORK/manifest.tsv" "$WORK/genome.tsv" "$EVID/"
bash tools/validate-agents-bootstrap.sh "$TARGET_ROOT"
./tools/validate-file-naming.sh
git add -A; git commit --quiet -m "E1: скелет генома"
echo "E1 OK"

# --- E2 -------------------------------------------------------------------
X history-paths --manifest "$EVID/manifest.tsv" > "$WORK/history.txt"
{ printf '%s\n' "${SOURCES[@]}"; cat "$WORK/history.txt"; } | sort -u > "$WORK/paths.txt"
git clone --quiet --no-local --single-branch --branch main "$WORK/hub" "$WORK/filtered"
git -C "$WORK/filtered" reset --quiet --hard "$HUB_SHA"
RENAMES=(); for m in "${MAPS[@]}"; do s="${m%%=*}"; d="${m#*=}"; [[ "$s" == "$d" ]] || RENAMES+=(--path-rename "$s:$d"); done
(cd "$WORK/filtered" && "$GFR" --force --preserve-commit-hashes \
   --paths-from-file "$WORK/paths.txt" "${RENAMES[@]}" \
   --message-callback "return re.sub(rb'(?<![\\w/.-])#(\\d+)', rb'$HUB_REPO#\\1', message)") > "$OUT/filter-repo.log" 2>&1
X verify --manifest "$EVID/manifest.tsv" --target "$WORK/filtered" --extra-scope "" > "$WORK/verify-filtered.json"
git fetch --quiet "$WORK/filtered" main:refs/hub-import/main
if ! git merge --allow-unrelated-histories --no-ff --no-edit \
     -m "import: $HUB_REPO@${HUB_SHA:0:12} с историей" refs/hub-import/main > "$OUT/merge.log" 2>&1; then
  echo "E2 conflicts: $(git diff --name-only --diff-filter=U | tr '\n' ' ')"
  [[ "$(git diff --name-only --diff-filter=U)" == "README.md" ]]
  git checkout --theirs README.md && git add README.md && git commit --quiet --no-edit
fi
X verify --manifest "$EVID/manifest.tsv" --target "$TARGET_ROOT" > "$EVID/verify-import.json"
cp "$WORK/verify-filtered.json" "$WORK/history.txt" "$EVID/"
cp "$WORK/filtered/.git/filter-repo/commit-map" "$EVID/commit-map.txt"
git -C "$WORK/filtered" rev-list --count HEAD > "$EVID/commit-count.txt"
git add -A; git commit --quiet -m "E2: доказательства импорта"
echo "E2 OK: $(cat "$EVID/commit-count.txt") imported commits; $(git log --oneline | grep -c 'G-Ivan-A/hybrid-Intelligence-lab#') messages with qualified issue refs"

# --- E3 -------------------------------------------------------------------
X rewrite-links --manifest "$EVID/manifest.tsv" --target "$TARGET_ROOT" \
  --hub-url "$HUB_URL" --target-url "$TARGET_URL" --log "$EVID/rewrite-links.jsonl"
X rewrite-links --manifest "$EVID/manifest.tsv" --target "$TARGET_ROOT" \
  --hub-url "$HUB_URL" --target-url "$TARGET_URL" --check
X verify --manifest "$EVID/manifest.tsv" --target "$TARGET_ROOT" --links \
  --hub-url "$HUB_URL" --target-url "$TARGET_URL" > "$EVID/verify-links.json"
python3 -I -c 'import collections,json,sys; print("E3 events:", dict(collections.Counter(json.loads(l)["kind"] for l in open(sys.argv[1]))))' "$EVID/rewrite-links.jsonl"
git add -A; git commit --quiet -m "E3: ссылки"
echo "E3 OK"

# --- E4 (scan only: classification is agent work) ------------------------
X scan --manifest "$EVID/manifest.tsv" --target "$TARGET_ROOT" > "$EVID/scan-before.txt" || true
echo "E4 scan-before: $(wc -l < "$EVID/scan-before.txt") line(s)"

# --- E5 -------------------------------------------------------------------
H_ARGS=(); for h in "${HEADINGS[@]}"; do H_ARGS+=(--heading "$h"); done
X sections --sha "$HUB_SHA" --source ops/backlog.md --manifest "$EVID/manifest.tsv" \
  --target-path ops/backlog.md --hub-url "$HUB_URL" --target-url "$TARGET_URL" \
  "${H_ARGS[@]}" -o "$WORK/sections.md"
mkdir -p ops
{ printf -- '---\nstatus: canonical\nversion: 1.0\nupdated: %s\ntemperature: 0.1\n---\n\n# Бэклог\n\n' "$(date -u +%F)"; cat "$WORK/sections.md"; } > ops/backlog.md
X sections --sha "$HUB_SHA" --source ops/backlog.md --manifest "$EVID/manifest.tsv" \
  --target-path ops/backlog.md --hub-url "$HUB_URL" --target-url "$TARGET_URL" \
  "${H_ARGS[@]}" --check ops/backlog.md
grep -o '^| \*\*B-[0-9]*\*\*' ops/backlog.md | tr -d '|* ' > "$EVID/backlog-ids.txt"
echo "E5 OK: $(wc -l < "$EVID/backlog-ids.txt") backlog rows"
bash tools/validate-agents-bootstrap.sh "$TARGET_ROOT" >/dev/null && ./tools/validate-file-naming.sh >/dev/null && echo "validators OK after E5"
