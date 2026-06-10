#!/usr/bin/env bash
#
# sync-from-hub.sh — Smart Sync client for spoke / HTOM repositories.
#
# Pulls the Hub template registry (templates/manifest.json), filters it by the
# local project profile (.hub-profile.json), reports which templates are new or
# updated, and applies them safely. By default local edits are NEVER
# overwritten: an updated template is written alongside the local file as
# `<name>.hub-new.<ext>` (e.g. `README.hub-new.md`) so a human can merge
# consciously. `--force` overwrites the local file instead.
#
# See issue #207 and guides/sync-from-hub.md.
#
# Usage:
#   tools/sync-from-hub.sh --init                 # create .hub-profile.json
#   tools/sync-from-hub.sh --report               # show sync report (default)
#   tools/sync-from-hub.sh --apply                # safe apply (.hub-new.* files)
#   tools/sync-from-hub.sh --apply --force        # overwrite local files
#
# Source selection:
#   --hub <url>       Hub repository URL (default from profile or the lab Hub)
#   --local <dir>     Use a local Hub working copy instead of fetching over HTTP
#   --manifest <path> Use an explicit manifest.json (overrides --hub/--local)
#   --profile <path>  Path to the project profile (default ./.hub-profile.json)
#
set -euo pipefail

DEFAULT_HUB_URL="https://github.com/G-Ivan-A/hybrid-Intelligence-lab"
PROFILE_PATH="./.hub-profile.json"
HUB_URL=""
LOCAL_DIR=""
MANIFEST_OVERRIDE=""
MODE="report"
FORCE=0
DO_INIT=0

PY="${PYTHON:-python3}"

die() { printf 'Error: %s\n' "$*" >&2; exit 1; }
info() { printf '%s\n' "$*"; }

usage() {
  sed -n '3,30p' "$0" | sed 's/^# \{0,1\}//'
}

command -v "$PY" >/dev/null 2>&1 || die "$PY is required (JSON parsing). Install Python 3 or set \$PYTHON."

# --- argument parsing ------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --init) DO_INIT=1 ;;
    --report) MODE="report" ;;
    --apply) MODE="apply" ;;
    --force) FORCE=1 ;;
    --hub) HUB_URL="${2:?--hub needs a value}"; shift ;;
    --local) LOCAL_DIR="${2:?--local needs a value}"; shift ;;
    --manifest) MANIFEST_OVERRIDE="${2:?--manifest needs a value}"; shift ;;
    --profile) PROFILE_PATH="${2:?--profile needs a value}"; shift ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1 (try --help)" ;;
  esac
  shift
done

[[ "$FORCE" -eq 1 && "$MODE" != "apply" ]] && die "--force only makes sense with --apply"

# --- raw URL helper --------------------------------------------------------
raw_base() {
  # Convert a github.com repo URL into a raw.githubusercontent.com base.
  local url="$1"
  url="${url%.git}"
  url="${url%/}"
  case "$url" in
    https://github.com/*)
      printf 'https://raw.githubusercontent.com/%s/main' "${url#https://github.com/}" ;;
    *) printf '%s/main' "$url" ;;
  esac
}

# --- interactive init ------------------------------------------------------
init_profile() {
  if [[ -f "$PROFILE_PATH" ]]; then
    printf '📋 Hub Profile уже существует (%s). Перезаписать? [y/N] ' "$PROFILE_PATH"
    read -r ans || true
    case "${ans:-}" in y|Y|yes|Yes) ;; *) info "Отменено."; return 0 ;; esac
  else
    printf '📋 Hub Profile не найден. Создать новый? [Y/n] '
    read -r ans || true
    case "${ans:-Y}" in n|N|no|No) info "Отменено."; return 0 ;; esac
  fi

  printf 'Введите название проекта: '; read -r name || true
  printf 'Выберите тип проекта: 1. HTOM / 2. Spoke [2]: '; read -r type_choice || true
  printf 'Выберите стек: 1. Python / 2. JS / 3. Rust / 4. C# / 5. all [5]: '; read -r stack_choice || true
  printf 'Текущая фаза: 0. Init / 1. MVP / 2. Development / 3. Production [0]: '; read -r phase_choice || true

  local target_type stack phase hub
  case "${type_choice:-2}" in 1) target_type="HTOM" ;; *) target_type="Spoke" ;; esac
  case "${stack_choice:-5}" in 1) stack="python" ;; 2) stack="js" ;; 3) stack="rust" ;; 4) stack="csharp" ;; *) stack="all" ;; esac
  case "${phase_choice:-0}" in 1) phase=1 ;; 2) phase=2 ;; 3) phase=3 ;; *) phase=0 ;; esac
  hub="${HUB_URL:-$DEFAULT_HUB_URL}"

  PROFILE_PATH="$PROFILE_PATH" P_NAME="${name:-unnamed-project}" P_TYPE="$target_type" \
  P_STACK="$stack" P_PHASE="$phase" P_HUB="$hub" "$PY" - <<'PY'
import json, os
profile = {
    "project_name": os.environ["P_NAME"],
    "target_type": os.environ["P_TYPE"],
    "stack": os.environ["P_STACK"],
    "phase": int(os.environ["P_PHASE"]),
    "hub_url": os.environ["P_HUB"],
    "last_sync": {},
}
with open(os.environ["PROFILE_PATH"], "w", encoding="utf-8") as fh:
    fh.write(json.dumps(profile, ensure_ascii=False, indent=2) + "\n")
PY
  info "✅ Создан $PROFILE_PATH"
}

if [[ "$DO_INIT" -eq 1 ]]; then
  init_profile
  exit 0
fi

# --- load profile ----------------------------------------------------------
[[ -f "$PROFILE_PATH" ]] || die "Профиль $PROFILE_PATH не найден. Запустите: $0 --init"

# Resolve hub URL from profile if not given on the CLI.
if [[ -z "$HUB_URL" ]]; then
  HUB_URL="$("$PY" - "$PROFILE_PATH" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as fh:
    print(json.load(fh).get("hub_url", ""))
PY
)"
fi
[[ -z "$HUB_URL" ]] && HUB_URL="$DEFAULT_HUB_URL"

# --- locate / fetch the manifest ------------------------------------------
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

MANIFEST=""
if [[ -n "$MANIFEST_OVERRIDE" ]]; then
  MANIFEST="$MANIFEST_OVERRIDE"
elif [[ -n "$LOCAL_DIR" ]]; then
  MANIFEST="$LOCAL_DIR/templates/manifest.json"
  [[ -f "$MANIFEST" ]] || die "manifest не найден в локальном Хабе: $MANIFEST"
else
  MANIFEST="$WORKDIR/manifest.json"
  url="$(raw_base "$HUB_URL")/templates/manifest.json"
  command -v curl >/dev/null 2>&1 || die "curl требуется для загрузки манифеста (или используйте --local/--manifest)"
  curl -fsSL "$url" -o "$MANIFEST" || die "не удалось загрузить манифест: $url"
fi

# --- plan: filter by profile + compare versions ---------------------------
# Emits TSV: status\tid\tpath\tcriticality\tcur_version\tnew_version\tdescription
PLAN="$WORKDIR/plan.tsv"
MANIFEST="$MANIFEST" PROFILE="$PROFILE_PATH" "$PY" - >"$PLAN" <<'PY'
import json, os

def semver(v):
    out = []
    for part in str(v).split("."):
        num = "".join(ch for ch in part if ch.isdigit())
        out.append(int(num) if num else 0)
    while len(out) < 3:
        out.append(0)
    return tuple(out[:3])

with open(os.environ["MANIFEST"], encoding="utf-8") as fh:
    manifest = json.load(fh)
with open(os.environ["PROFILE"], encoding="utf-8") as fh:
    profile = json.load(fh)

ptype = profile.get("target_type", "Spoke")
pstack = profile.get("stack", "all")
pphase = int(profile.get("phase", 0))
last_sync = profile.get("last_sync", {}) or {}

for tpl in manifest.get("templates", []):
    targets = tpl.get("target_type", [])
    if ptype not in targets:
        continue
    stacks = tpl.get("stack", ["all"])
    if "all" not in stacks and pstack not in stacks and pstack != "all":
        continue
    if int(tpl.get("min_phase", 0)) > pphase:
        continue

    tid = tpl.get("id", "")
    new_v = str(tpl.get("version", "0.0.0"))
    cur_v = last_sync.get(tid, "")
    if not cur_v:
        status = "new"
    elif semver(cur_v) < semver(new_v):
        status = "update"
    else:
        status = "uptodate"

    fields = [
        status, tid, tpl.get("path", ""),
        tpl.get("criticality", "RECOMMENDED"),
        cur_v or "-", new_v,
        (tpl.get("description", "") or "").replace("\t", " ").replace("\n", " "),
    ]
    print("\t".join(fields))
PY

PROJECT_NAME="$("$PY" - "$PROFILE_PATH" <<'PY'
import json, sys
with open(sys.argv[1], encoding="utf-8") as fh:
    print(json.load(fh).get("project_name", "spoke"))
PY
)"

# --- report ----------------------------------------------------------------
print_report() {
  info "🔄 Hub Sync Report for \`$PROJECT_NAME\`"
  info ""

  local uptodate updates n
  uptodate="$(awk -F'\t' '$1=="uptodate"' "$PLAN" || true)"
  updates="$(awk -F'\t' '$1=="update" || $1=="new"' "$PLAN" || true)"

  info "✅ Актуально (нет изменений):"
  if [[ -n "$uptodate" ]]; then
    while IFS=$'\t' read -r _ id path crit cur new desc; do
      info "- $(basename "$path") (v$new)"
    done <<< "$uptodate"
  else
    info "- (нет)"
  fi
  info ""

  if [[ -n "$updates" ]]; then
    info "⚠️ Найдены релевантные обновления:"
    n=0
    while IFS=$'\t' read -r status id path crit cur new desc; do
      n=$((n+1))
      if [[ "$status" == "new" ]]; then
        info "$n. [$crit] $(basename "$path") (Новый файл)"
        info "   - Версия: v$new"
        [[ -n "$desc" ]] && info "   - Описание: $desc"
      else
        info "$n. [$crit] $(basename "$path")"
        info "   - Текущая: v$cur | Новая: v$new"
        [[ -n "$desc" ]] && info "   - Изменения: $desc"
      fi
    done <<< "$updates"
    info ""
    info "💡 Действия:"
    if [[ "$MODE" == "report" ]]; then
      info "Запустите с флагом --apply для безопасного копирования (.hub-new.*),"
      info "или --apply --force для перезаписи локальных файлов."
    fi
  else
    info "✨ Обновлений нет — всё синхронизировано."
  fi
}

# --- apply -----------------------------------------------------------------
# Map a hub-relative template path to its local destination by stripping the
# templates/{htom,spoke}/ prefix (root templates keep their basename location).
local_dest() {
  local path="$1"
  path="${path#templates/htom/}"
  path="${path#templates/spoke/}"
  path="${path#templates/}"
  printf '%s' "$path"
}

fetch_template() {
  # $1 = hub-relative path, $2 = destination temp file
  local path="$1" out="$2"
  if [[ -n "$LOCAL_DIR" ]]; then
    cp "$LOCAL_DIR/$path" "$out"
  elif [[ -n "$MANIFEST_OVERRIDE" ]]; then
    # Manifest given explicitly: read sibling files relative to its repo root.
    local root="${MANIFEST_OVERRIDE%/templates/manifest.json}"
    cp "$root/$path" "$out"
  else
    curl -fsSL "$(raw_base "$HUB_URL")/$path" -o "$out"
  fi
}

apply_updates() {
  local applied=0 changed_ids=""
  while IFS=$'\t' read -r status id path crit cur new desc; do
    [[ "$status" == "update" || "$status" == "new" ]] || continue
    local dest tmp
    dest="$(local_dest "$path")"
    tmp="$WORKDIR/$(basename "$path").src"
    fetch_template "$path" "$tmp" || { info "⚠️ Не удалось получить $path — пропуск."; continue; }

    mkdir -p "$(dirname "$dest")" 2>/dev/null || true
    if [[ -e "$dest" && "$FORCE" -ne 1 ]]; then
      local ext base side
      base="$(basename "$dest")"
      if [[ "$base" == *.* ]]; then
        ext="${base##*.}"
        side="${dest%.*}.hub-new.$ext"
      else
        side="$dest.hub-new"
      fi
      cp "$tmp" "$side"
      info "📝 $dest существует — сохранено как $side (не затёрто)."
    else
      cp "$tmp" "$dest"
      info "✅ Записан $dest (v$new)."
    fi
    applied=$((applied+1))
    changed_ids="$changed_ids $id=$new"
  done < "$PLAN"

  # Update last_sync for every relevant template to the manifest version, so the
  # profile reflects the current sync point (safe-mode copies are merged by a
  # human; --force-applied files match the hub immediately).
  if [[ "$applied" -gt 0 ]]; then
    MANIFEST="$MANIFEST" PROFILE="$PROFILE_PATH" PLAN="$PLAN" "$PY" - <<'PY'
import json, os
with open(os.environ["PROFILE"], encoding="utf-8") as fh:
    profile = json.load(fh)
last_sync = profile.setdefault("last_sync", {})
with open(os.environ["PLAN"], encoding="utf-8") as fh:
    for line in fh:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 6:
            continue
        status, tid, _path, _crit, _cur, new = parts[:6]
        if status in ("update", "new") and tid:
            last_sync[tid] = new
with open(os.environ["PROFILE"], "w", encoding="utf-8") as fh:
    fh.write(json.dumps(profile, ensure_ascii=False, indent=2) + "\n")
PY
    info ""
    info "🗂️  Профиль обновлён: last_sync синхронизирован ($applied шаблон(ов))."
  fi
}

print_report
if [[ "$MODE" == "apply" ]]; then
  info ""
  info "▶️  Применение обновлений ($([[ "$FORCE" -eq 1 ]] && echo "перезапись" || echo "безопасный режим"))..."
  apply_updates
fi
