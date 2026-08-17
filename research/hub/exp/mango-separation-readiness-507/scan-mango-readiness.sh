#!/usr/bin/env bash
# Сканер готовности mango_ba_prompts к разделению репозиториев и к BA-прогонам.
# Измерения для отчёта docs/analysis/2026-08-13-mango-separation-and-runs-readiness.md
#
# Использование:
#   git clone https://github.com/G-Ivan-A/mango_ba_prompts /tmp/mango-clone
#   ./scan-mango-readiness.sh /tmp/mango-clone [путь-к-клону-Хаба]
#
# Скрипт только читает: он не изменяет ни один репозиторий.
set -uo pipefail

MANGO="${1:-/tmp/mango-clone}"
HUB="${2:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)}"

if [ ! -d "$MANGO/.git" ]; then
  echo "ОШИБКА: $MANGO не является git-клоном mango_ba_prompts" >&2
  exit 1
fi

echo "=== 0. Снимок ==="
echo "mango HEAD: $(git -C "$MANGO" rev-parse --short HEAD) ($(git -C "$MANGO" log -1 --format=%cd --date=short))"
echo "hub   HEAD: $(git -C "$HUB" rev-parse --short HEAD) ($(git -C "$HUB" log -1 --format=%cd --date=short))"

echo
echo "=== 1. Инвентаризация: файлы и бренд по каталогам верхнего уровня ==="
total=0
brand=0
for d in $(git -C "$MANGO" ls-files | awk -F/ '{print $1}' | sort -u); do
  n=$(git -C "$MANGO" ls-files "$d" | wc -l)
  b=$(git -C "$MANGO" grep -lie 'mango' -- "$d" 2>/dev/null | wc -l)
  total=$((total + n))
  brand=$((brand + b))
  printf '%-16s файлов=%-6s с упоминанием бренда=%s\n' "$d" "$n" "$b"
done
echo "ИТОГО: файлов=$total, с упоминанием бренда=$brand"

echo
echo "=== 2. Контракт прогонов: обязательные поля metadata.yaml и наполнение ==="
for f in "$MANGO"/runs/*/*/metadata.yaml "$MANGO"/runs/*/metadata.yaml; do
  [ -e "$f" ] || continue
  run=$(basename "$(dirname "$f")")
  miss=""
  for k in run_id process version date author model status; do
    grep -q "^${k}:" "$f" || miss="$miss $k"
  done
  model=$(sed -n 's/^model: *//p' "$f" | tr -d '"')
  # .gitkeep не считается содержимым: пустой каталог с .gitkeep == нет данных
  fb=$(find "$(dirname "$f")/feedback" -type f ! -name .gitkeep 2>/dev/null | wc -l)
  lg=$(find "$(dirname "$f")/logs" -type f ! -name .gitkeep 2>/dev/null | wc -l)
  printf '%-10s missing=[%s] model=%-14s feedback=%s logs=%s\n' \
    "$run" "${miss:- нет}" "${model:-—}" "$fb" "$lg"
done

echo
echo "=== 3. Контракт промптов: ровно 6 обязательных полей frontmatter ==="
for f in $(git -C "$MANGO" ls-files 'prompts/*.md'); do
  p="$MANGO/$f"
  head -1 "$p" | grep -q '^---$' || { echo "БЕЗ FRONTMATTER: $f"; continue; }
  fields=$(awk 'NR>1{if($0=="---")exit; if($0 ~ /^[a-z_-]+:/) print $1}' "$p" | tr -d ':')
  extra=$(echo "$fields" | grep -vxE 'id|title|status|version|updated|temperature' | tr '\n' ' ')
  [ -n "${extra// /}" ] && echo "ЛИШНИЕ ПОЛЯ: $f ->$extra"
done

echo
echo "=== 4. Битые относительные ссылки в markdown ==="
echo "(ссылки-плейсхолдеры вида <path> и ... считаются отдельно и не являются дефектом)"
broken=0
placeholder=0
while IFS= read -r f; do
  dir=$(dirname "$MANGO/$f")
  while IFS= read -r link; do
    [ -z "$link" ] && continue
    case "$link" in http*|"#"*|mailto:*) continue ;; esac
    target="${link%%#*}"
    [ -z "$target" ] && continue
    if [ ! -e "$dir/$target" ]; then
      case "$target" in
        *"<"*|*"..."*) placeholder=$((placeholder + 1)) ;;
        *) echo "БИТАЯ: $f -> $link"; broken=$((broken + 1)) ;;
      esac
    fi
  done < <(grep -oE '\]\([^)]+\)' "$MANGO/$f" | sed 's/^](//;s/)$//')
done < <(git -C "$MANGO" ls-files '*.md')
echo "ВСЕГО битых относительных ссылок: $broken (плейсхолдеров, исключённых из счёта: $placeholder)"

echo
echo "=== 5. Дрейф Хаба относительно последней синхронизации mango ==="
if [ -f "$MANGO/.hub-profile.json" ]; then
  sync_sha=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['last_sync']['hub_sha'])" "$MANGO/.hub-profile.json")
  sync_date=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['last_sync']['date'])" "$MANGO/.hub-profile.json")
  echo "last_sync: $sync_date @ ${sync_sha:0:7}"
  echo "коммитов в Хабе с момента синхронизации: $(git -C "$HUB" rev-list --count "$sync_sha"..HEAD 2>/dev/null || echo '?')"
  echo "--- новые каталоги методологии в Хабе:"
  git -C "$HUB" diff --name-only "$sync_sha"..HEAD -- ai-rules ai-governance 2>/dev/null || true
else
  echo "ВНИМАНИЕ: .hub-profile.json отсутствует"
fi

echo
echo "=== 6a. Модули research/ai-education: базовые модули и прикладные артефакты ==="
for d in "$HUB"/research/ai-education/*/; do
  m=$(basename "$d")
  base=$(ls "$d" | grep -cE '^[0-5]0-')
  applied=$(ls "$d" | grep -cE '^[0-9]{4}-[0-9]{2}-[0-9]{2}-')
  printf '%-42s базовых модулей=%s прикладных артефактов=%s\n' "$m" "$base" "$applied"
done

echo
echo "=== 6. Наличие целевых каталогов ADR-009 в mango ==="
for d in prompts kb runs evals internal-rfc internal-docs education site .github; do
  if [ -d "$MANGO/$d" ]; then echo "есть        $d/"; else echo "ОТСУТСТВУЕТ $d/"; fi
done
