#!/usr/bin/env bash
# Проверки независимого экспертного разбора диалога владельца (PR #722, комментарий 2026-11-04 10:44 UTC).
# Только чтение. Клон спицы — недоверенные данные: python3 -I, без исполнения кода спицы.
# Использование: dialog-review-checks.sh <hub-root> <spoke-clone> [base-ref]
set -u
HUB=${1:?hub root}
SPOKE=${2:?spoke clone}
BASE=${3:-origin/main}
D=research/hub/exp/gra-extraction-cleanup-721
cd "$HUB" || exit 2

echo "== C-1. Файлы PR против базы ($BASE...HEAD): сколько всего и сколько в домене курса"
total=$(git diff --name-only "$BASE"...HEAD | wc -l)
domain=$(git diff --name-only "$BASE"...HEAD -- research/reputation-technologies | wc -l)
echo "files_total=$total files_in_research/reputation-technologies=$domain"

echo "== C-2. Есть ли файлы day1-framer / day2-scout в Хабе (рабочее дерево и вся история)"
echo "tree: $(git ls-files | grep -c -i -E 'framer|scout')"
echo "history: $(git log --all --name-only --format= | grep -c -i -E 'day1-framer|day2-scout')"

echo "== C-3. Поиск кода владельца G-Ivan-A на GitHub (gh search code)"
for q in day1-framer day2-scout; do
  n=$(gh search code --owner G-Ivan-A "$q" --json path --jq 'length' 2>/dev/null || echo "n/a")
  echo "$q: $n"
done

echo "== C-4. Что такое PR #710 и PR #722"
gh pr view 710 --json number,title,mergedAt --jq '"#\(.number) merged \(.mergedAt): \(.title)"' 2>/dev/null || echo "#710: n/a"
gh pr view 722 --json number,title --jq '"#\(.number): \(.title)"' 2>/dev/null || echo "#722: n/a"

echo "== C-5. Офлайн-режим и контакты в действующих материалах дня 1 (вопросы А и Б диалога)"
F=research/reputation-technologies/2026-10-30-day1-osint-pipeline-design.md
grep -n -o -E 'без него — запросы для ручного списка, никаких названий из памяти|ФИО и email не выводятся из шаблонов|несуществующий домен не конструируется|запрет выдуманных URL' "$F"

echo "== C-6. Спица: HEAD и last_sync.hub_commit"
echo "spoke HEAD: $(git -C "$SPOKE" rev-parse HEAD)"
python3 -I -c 'import json,sys; d=json.load(open(sys.argv[1])); print("last_sync.hub_commit:", d["last_sync"]["hub_commit"])' "$SPOKE/.hub-profile.json"
grep -n -E '^1\. \*\*Репозиторий|^2\. \*\*Хаб остаётся|Изменения материалов курса' "$SPOKE/docs/adr/2026-11-adr-001-separate-repository-and-ssot.md"

echo "== C-7. Коммиты в домене после снимка RFC (c06075d) и после снимка спицы (32b5fa5)"
echo "after c06075d: $(git log --oneline c06075d.."$BASE" -- research/reputation-technologies | wc -l)"
echo "after 32b5fa5: $(git log --oneline 32b5fa5.."$BASE" -- research/reputation-technologies | wc -l)"

echo "== C-8. Повтор инвентаря: отличаются ли диспозиции от gra-inventory.tsv"
tmp=$(mktemp)
python3 -I "$D/gra-inventory.py" . "$SPOKE" --tsv "$tmp" > /dev/null
# Колонка 15 — диспозиция; сравниваются путь и диспозиция.
if diff <(cut -f1,15 "$tmp") <(cut -f1,15 "$D/gra-inventory.tsv") > /dev/null; then
  echo "dispositions: identical ($(wc -l < "$tmp") rows)"
else
  echo "dispositions: DIFFER"; diff <(cut -f1,15 "$tmp") <(cut -f1,15 "$D/gra-inventory.tsv")
fi
echo "rows with changed reference counts only: $(diff "$tmp" "$D/gra-inventory.tsv" | grep -c '^<')"
rm -f "$tmp"
