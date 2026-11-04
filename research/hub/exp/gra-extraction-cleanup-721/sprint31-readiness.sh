#!/usr/bin/env bash
# Проверка готовности Спринта 31 (issue #725): выполнены ли предусловия очистки
# Хаба от домена GRA, которые RFC #721 ставит перед шагами 3–6.
# Только чтение. Клон спицы — недоверенные данные: python3 -I, код спицы не исполняется.
# Использование: sprint31-readiness.sh <hub-root> <spoke-clone> [pin-sha]
set -u
HUB=${1:?hub root}
SPOKE=${2:?spoke clone}
PIN=${3:-48ebe5230be87ca5bf8a08b385e296a2987e9958}
DOMAIN=research/reputation-technologies
D=research/hub/exp/gra-extraction-cleanup-721
REPO=G-Ivan-A/hybrid-Intelligence-lab
SPOKE_REPO=G-Ivan-A/aether-orbis-gra
cd "$HUB" || exit 2

echo "== P-1. PR спицы по S-1 слит (B-271, B-272, B-273 и сторона спицы B-274)"
gh pr view 4 --repo "$SPOKE_REPO" --json state,mergedAt,mergeCommit \
  --jq '"state=\(.state) mergedAt=\(.mergedAt) merge=\(.mergeCommit.oid)"' 2>/dev/null || echo "n/a"
echo "spoke_clone_HEAD=$(git -C "$SPOKE" rev-parse HEAD)"

echo "== P-2. Ссылки спицы на домен Хаба: плавающие (blob/main) и закреплённые по SHA"
floating=$(grep -rhoE "hybrid-Intelligence-lab/(blob|tree)/main/$DOMAIN[^ )\"'>]*" "$SPOKE" --exclude-dir=.git | wc -l)
echo "floating_domain_links=$floating"
grep -rhoE "hybrid-Intelligence-lab/(blob|tree)/[0-9a-f]{7,40}/$DOMAIN" "$SPOKE" --exclude-dir=.git \
  | sed -E 's#.*/(blob|tree)/([0-9a-f]+)/.*#\2#' | sort | uniq -c | sed 's/^ */pinned /'

echo "== P-3. Каждый закреплённый путь домена существует на своём коммите Хаба"
missing=0; total=0
while IFS=$'\t' read -r sha path; do
  total=$((total + 1))
  if ! git cat-file -e "$sha:$path" 2>/dev/null; then
    missing=$((missing + 1)); echo "missing $sha:$path"
  fi
done < <(grep -rhoE "hybrid-Intelligence-lab/(blob|tree)/[0-9a-f]{7,40}/$DOMAIN[^ )\"'>#]*" "$SPOKE" --exclude-dir=.git \
  | sed -E 's#.*/(blob|tree)/([0-9a-f]+)/(.*)#\2\t\3#; s#[.,;:]$##; s#/$##' | sort -u)
echo "pinned_paths=$total missing=$missing"

echo "== P-4. Строки бэклога спицы для задач, переносимых из Спринта 29 Хаба, и для Q-3/Q-4"
for id in B-230 B-231 B-233 GRA-003 GRA-004; do
  line=$(grep -n "^| \*\*$id\*\*" "$SPOKE/ops/backlog.md" | cut -d: -f1)
  echo "$id: ops/backlog.md#L${line:-none}"
done

echo "== P-5. Домен Хаба не менялся после PIN_SHA (заморозка началась с закрепления)"
echo "main=$(git rev-parse origin/main)"
echo "changed_files_since_pin=$(git diff --name-only "$PIN" origin/main -- "$DOMAIN" | wc -l)"
echo "commits_since_pin=$(git rev-list --count "$PIN"..origin/main -- "$DOMAIN")"

echo "== P-6. Открытые PR Хаба, которые трогают домен (параллельная работа)"
for n in $(gh pr list --repo "$REPO" --state open --json number --jq '.[].number' 2>/dev/null); do
  c=$(gh pr diff "$n" --repo "$REPO" --name-only 2>/dev/null | grep -c "^$DOMAIN/")
  echo "PR #$n domain_files=$c"
done

echo "== P-7. CI validate на main"
gh run list --repo "$REPO" --branch main --workflow validate --limit 1 \
  --json conclusion,headSha --jq '.[] | "validate main@\(.headSha[0:7]) \(.conclusion)"' 2>/dev/null || echo "n/a"

echo "== P-8. Права исполнителя и rulesets (Q-6 требует администратора)"
gh api "repos/$REPO" --jq '"admin=\(.permissions.admin) push=\(.permissions.push)"' 2>/dev/null || echo "n/a"
echo "rulesets=$(gh api "repos/$REPO/rulesets" --jq 'length' 2>/dev/null || echo n/a)"
echo "archive_tags=$(git ls-remote --tags origin 'archive/*' | wc -l)"

echo "== P-9. Повтор инвентаря на текущей спице: какие диспозиции сдвинулись"
python3 -I "$D/gra-inventory.py" . "$SPOKE" --tsv /tmp/sprint31-inventory-now.tsv > /dev/null 2>&1
python3 -I - "$D/gra-inventory.tsv" /tmp/sprint31-inventory-now.tsv <<'PY'
import csv, sys
def load(p):
    with open(p, encoding="utf-8") as f:
        return {r["unit"]: r for r in csv.DictReader(f, delimiter="\t")}
base, now = load(sys.argv[1]), load(sys.argv[2])
print(f"units base={len(base)} now={len(now)}")
moved = [(u, base[u]["disposition"], now[u]["disposition"], now[u]["files"]) for u in sorted(base)
         if u in now and base[u]["disposition"] != now[u]["disposition"]]
for u, a, b, f in moved:
    print(f"  {u}: {a} -> {b} ({f} files; spoke_floating {base[u]['spoke_floating']} -> {now[u]['spoke_floating']})")
mandate = [u for u, r in base.items() if r["disposition"] == "DELETE"]
print(f"mandate_Q2_units={len(mandate)} files={sum(int(base[u]['files']) for u in mandate)}")
PY
