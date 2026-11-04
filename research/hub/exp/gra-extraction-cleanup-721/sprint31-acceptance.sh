#!/usr/bin/env bash
# Проверка приёмки выноса GRA (issue #725, B-284; критерии Ш6.2 RFC #721) тем же
# инструментом, которым измерялся вход.
# Только чтение. Клон спицы — недоверенные данные: python3 -I, код спицы не исполняется.
# Использование: sprint31-acceptance.sh <hub-root> <spoke-clone> [ci-run-id]
#   ci-run-id — прогон workflow validate на ветке PR для A-5 (длительность задания).
set -u
HUB=${1:?hub root}
SPOKE=${2:?spoke clone}
RUN=${3:-}
DOMAIN=research/reputation-technologies
D=research/hub/exp/gra-extraction-cleanup-721
REPO=G-Ivan-A/hybrid-Intelligence-lab
cd "$HUB" || exit 2
status=0
fail() { echo "FAIL $*"; status=1; }

echo "== A-1. Повтор инвентаря: в дереве только надгробие"
echo "hub_HEAD=$(git rev-parse HEAD)"
python3 -I "$D/gra-inventory.py" . "$SPOKE" --tsv "${TMPDIR:-/tmp}/sprint31-acceptance.tsv" \
  | grep -E "^(domain files|files by disposition|  [A-Z-]+:|units with a CI step)"
files=$(git ls-files -- "$DOMAIN" | tr '\n' ' ')
echo "domain_tree_files=$files"
[[ "$files" == "$DOMAIN/README.md " ]] || fail "в домене остались файлы кроме надгробия"

echo "== A-2. git grep $DOMAIN: только надгробие, path_migrations, история и закреплённые адреса"
python3 -I "$D/grep-classify.py" . || fail "живые ссылки на выведенные пути"

echo "== A-3. Manifest redirect: полнота по archive_commit, разрешение путей"
python3 -I tools/path-migration-manifest.py check || fail "manifest redirect"
for path in "$DOMAIN/2026-06-20-glossary.ru-en.md" "$DOMAIN/2026-06-29-partner-attraction-strategy.ru.md" "$DOMAIN/no-such-file.md"; do
  if python3 -I tools/path-migration-manifest.py resolve "$path" >/dev/null 2>&1; then r=resolved; else r=unresolved; fi
  echo "resolve $path: $r"
done
python3 -I tools/archive-tags.py plan || fail "archive tag plan"

echo "== A-4. Шаги CI курса в validate.yml"
course=$(grep -cE "reputation-technologies|presentation-rfc" .github/workflows/validate.yml)
echo "course_steps_mentions=$course"
[[ "$course" == 0 ]] || fail "в validate.yml остались проверки курса"

echo "== A-5. Задание validate в CI (база — 135 с, из них 38 с курса)"
if [[ -n "$RUN" ]]; then
  gh api "repos/$REPO/actions/runs/$RUN/jobs" \
    --jq '.jobs[] | "\(.name) \(.conclusion) \(((.completed_at|fromdate) - (.started_at|fromdate)))s steps=\(.steps|length)"' 2>/dev/null \
    || echo "n/a"
else
  echo "n/a (ci-run-id не передан)"
fi

echo "== A-6. Ссылки спицы на коммиты Хаба отвечают 200 и существуют в git"
# URL без пути после SHA — префикс, из которого код спицы собирает адреса:
# GitHub отвечает на него 302 на tree, поэтому редиректы проходятся (-L).
total=0; bad=0; missing=0
while read -r url; do
  total=$((total + 1))
  rest=${url#https://github.com/$REPO/}; rest=${rest#*/}
  sha=${rest%%/*}; path=${rest#*/}; path=${path%/}
  git cat-file -e "$sha:$path" 2>/dev/null || { missing=$((missing + 1)); echo "missing $sha:$path"; }
  code=$(curl -s -L -o /dev/null -I -w '%{http_code}' --max-time 20 "$url")
  [[ "$code" == 200 ]] || { bad=$((bad + 1)); echo "http $code $url"; }
done < <(grep -rhoE "https://github.com/$REPO/(blob|tree)/[0-9a-f]{7,40}/[^ )\"'>#]*" "$SPOKE" --exclude-dir=.git \
  | sed -E 's#[.,;:]$##' | sort -u)
echo "spoke_pinned_urls=$total http_not_200=$bad missing_in_git=$missing"
((bad == 0 && missing == 0)) || fail "закреплённые ссылки спицы"

echo "== Итог"
((status == 0)) && echo "acceptance passed" || echo "acceptance FAILED"
exit $status
