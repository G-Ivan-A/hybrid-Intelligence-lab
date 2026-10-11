#!/usr/bin/env bash
# Самопроверка check-day3.sh (issue #663): на копии документов по одной вносит
# нарушение разметки достоверности или сверки с юристом и ждёт от check-day3.sh
# код 1 и нужную строку FAIL. Исходные документы не меняются.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
src="$(cd "$here/../.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
fail=0

setup() {
  rm -rf "$tmp/case"
  mkdir -p "$tmp/case/exp/day3-filter-663"
  cp "$here/check-day3.sh" "$tmp/case/exp/day3-filter-663/"
  cp "$src"/2026-11-02-day3-*.md "$src/2026-10-30-day2-lecturer-script.md" \
    "$src/2026-10-30-day2-rationale-and-method.md" "$tmp/case/"
}

# mutate <файл> <регулярное выражение Python> <замена>
mutate() {
  python3 -I -c '
import re, sys
path, pattern, repl = sys.argv[1:]
text = open(path, encoding="utf-8").read()
new, n = re.subn(pattern, repl, text)
if n == 0:
    sys.exit("pattern not found: " + pattern)
open(path, "w", encoding="utf-8").write(new)
' "$tmp/case/$1" "$2" "$3"
}

# expect <название> <ожидаемая строка FAIL>
expect() {
  local out code=0
  out=$(bash "$tmp/case/exp/day3-filter-663/check-day3.sh" 2>&1) || code=$?
  if [ "$code" -eq 1 ] && grep -q -F -- "$2" <<<"$out"; then
    echo "ok   $1"
  else
    echo "FAIL $1: exit=$code, no line «$2»"; fail=1
  fi
}

setup
if bash "$tmp/case/exp/day3-filter-663/check-day3.sh" >/dev/null 2>&1; then echo "ok   baseline passes"; else echo "FAIL baseline"; fail=1; fi

setup; mutate 2026-11-02-day3-rationale-and-method.md 'обязан\s+явно\s+указать' 'должен указать'
expect 'filter without the reason rule' 'FAIL reliability markup: ты обязан явно указать причину'

setup; mutate 2026-10-30-day2-lecturer-script.md 'обязан\s+явно\s+указать' 'должен указать'
expect 'Day 2 Разведчик without the reason rule' 'FAIL reliability markup: Day 2 Разведчик'

setup; mutate 2026-11-02-day3-rationale-and-method.md 'https://kad\.arbitr\.ru/' 'https://example.org/'
expect 'case 1 without kad.arbitr.ru' 'FAIL reliability markup: https://kad.arbitr.ru/'

setup; mutate 2026-11-02-day3-rationale-and-method.md '\Z' '\n| 9 | Сеть | тендер, плата за вход |\n'
expect 'unsourced «плата за вход» in a table' 'FAIL unsourced commercial term'

setup; mutate 2026-11-02-day3-presentation.md '\Z' '\n| Выход | Таблица `Узел | Статус` |\n'
expect 'pipe inside code in a table row' 'FAIL pipe inside code in table row'

setup; mutate 2026-11-02-day3-lecturer-script.md '381-ФЗ \(ст\. 9\) и 98-ФЗ \(ст\. 3, ст\. 5\) в кейсе 1 и в разметке достоверности, ' ''
expect 'Day 3 lawyer check without case 1 norms' 'FAIL lawyer check: Day 3 — prep item misses 381-ФЗ 98-ФЗ'

setup; mutate 2026-10-30-day2-lecturer-script.md '98-ФЗ \(ст\. 3\) в кейсе 1 и в правилах Промпта-разведчика о коммерческих условиях, ' ''
expect 'Day 2 lawyer check without 98-ФЗ' 'FAIL lawyer check: Day 2 — prep item misses 98-ФЗ'

# Слова «Правовые нормы» вне пункта списка выше настоящего пункта не подменяют его.
setup; mutate 2026-11-02-day3-rationale-and-method.md '\A' 'Правовые нормы кейса 2: 259-ФЗ.\n'
mutate 2026-11-02-day3-lecturer-script.md '381-ФЗ \(ст\. 9\) и ' ''
expect 'Day 3 lawyer check with a decoy line above the norms item' 'FAIL lawyer check: Day 3 — prep item misses 381-ФЗ'

exit $fail
