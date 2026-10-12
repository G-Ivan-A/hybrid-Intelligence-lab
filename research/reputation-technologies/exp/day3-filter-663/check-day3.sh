#!/usr/bin/env bash
# Проверки пакета Дня 3 (issue #663): запрещённые оценочные прилагательные,
# относительные ссылки, дословные теги, 30 слайдов и плотность речи по слотам.
set -euo pipefail
dir="$(cd "$(dirname "$0")/../.." && pwd)"
d1="$dir/2026-11-02-day3-rationale-and-method.md"
d2="$dir/2026-11-02-day3-presentation.md"
d3="$dir/2026-11-02-day3-lecturer-script.md"
fail=0

hits=$(grep -n -i -E 'честн|реалистичн|правдив' "$d1" "$d2" "$d3" || true)
if [ -n "$hits" ]; then echo "FAIL forbidden adjectives:"; echo "$hits"; fail=1; else echo "ok   forbidden adjectives: 0"; fi

rel=$(grep -n -o -E '\]\([^h#)][^)]*\)' "$d1" "$d2" "$d3" || true)
if [ -n "$rel" ]; then echo "FAIL relative links:"; echo "$rel"; fail=1; else echo "ok   relative links: 0"; fi

for t in '[ПАУЗА]' '[ВОПРОС В ЧАТ: выберите узел для действия]' '[ДЕМОНСТРАЦИЯ ЭКРАНА: промпт-фильтр]' '[ЮМОР/РАЗРЯДКА]' '[САМОСТОЯТЕЛЬНАЯ РАБОТА: примените фильтр к кейсу]'; do
  n=$(grep -c -F "$t" "$d3" || true)
  if [ "$n" -eq 0 ]; then echo "FAIL tag missing: $t"; fail=1; else echo "ok   tag x$n: $t"; fi
done

slides=$(grep -o -E '\[СЛАЙД [0-9]+\]' "$d3" | sort -u | wc -l)
pres=$(grep -c -E '^\*\*Слайд [0-9]+\.' "$d2")
if [ "$slides" -ne 30 ] || [ "$pres" -ne 30 ]; then echo "FAIL slides: script=$slides presentation=$pres"; fail=1; else echo "ok   slides: script=$slides presentation=$pres"; fi

for p in 'Теория заинтересованных сторон' 'Активность в коммуникации' 'доступность, значимость, качество, возможный вред' 'прямой разговор снимает противоречие' 'опасна для публичного действия' 'активное воздействие против пассивного потребления' 'смена полярности'; do
  if grep -q -i -F "$p" "$d1" && grep -q -i -F "$p" "$d2"; then echo "ok   program phrase: $p"; else echo "FAIL program phrase: $p"; fail=1; fi
done

# Разметка достоверности (комментарий владельца в PR #664): правило о причине
# статуса в Промпте-фильтре и в Промпте-разведчике Дня 2, достижимые индикаторы
# кейса 1. Строки промпта перенесены, поэтому текст склеивается в одну строку.
flat() { tr '\n' ' ' < "$1" | tr -s ' '; }
d2s="$dir/2026-10-30-day2-lecturer-script.md"
for p in 'РАЗМЕТКА ДОСТОВЕРНОСТИ' 'ты обязан явно указать причину низкого уровня достоверности' 'https://kad.arbitr.ru/' 'https://fssp.gov.ru/iss/ip' 'тендер и ассортиментный комитет'; do
  if flat "$d1" | grep -q -F -- "$p"; then echo "ok   reliability markup: $p"; else echo "FAIL reliability markup: $p"; fail=1; fi
done
if flat "$d2s" | grep -q -F 'ты обязан явно указать причину низкого уровня достоверности'; then echo "ok   reliability markup: Day 2 Разведчик"; else echo "FAIL reliability markup: Day 2 Разведчик"; fail=1; fi

# «Плата за вход» — коммерческое условие без источника; допустимо только
# упоминание в самопроверке документа 1, где оно взято в кавычки.
hits=$(grep -n -i -E 'плат[аеиоуыю]+ за вход' "$d1" "$d2" "$d3" | grep -v -F '«плате за вход»' || true)
if [ -n "$hits" ]; then echo "FAIL unsourced commercial term:"; echo "$hits"; fail=1; else echo "ok   unsourced commercial term «плата за вход»: 0"; fi

# Сверка с юристом в подготовке лектора охватывает все нормы, которые документ 1
# помечает как границу для юриста: в Дне 3 — и нормы кейса 1 (381-ФЗ, 98-ФЗ),
# в Дне 2 версии 0.2 — и 98-ФЗ из разметки достоверности.
d2r="$dir/2026-10-30-day2-rationale-and-method.md"
laws() { grep -o -E '[0-9]+-ФЗ' | LC_ALL=C sort -u; }
for day in 'Day 3' 'Day 2'; do
  if [ "$day" = 'Day 3' ]; then r="$d1"; s="$d3"; else r="$d2r"; s="$d2s"; fi
  need=$(grep -m1 -E '^([0-9]+\.|-) (\*\*)?Правовые нормы' "$r" | laws || true)
  have=$(grep -m1 -E '^[0-9]+\. Сверьте с юристом' "$s" | laws || true)
  missing=$(LC_ALL=C comm -23 <(printf '%s\n' "$need") <(printf '%s\n' "$have") | tr '\n' ' ')
  if [ -z "$need" ]; then echo "FAIL lawyer check: $day — no «Правовые нормы» line in document 1"; fail=1
  elif [ -n "${missing// /}" ]; then echo "FAIL lawyer check: $day — prep item misses ${missing% }"; fail=1
  else echo "ok   lawyer check: $day covers" $need; fi
done

# Вертикальная черта внутри кода в строке таблицы делит ячейку (GFM).
pipes=$(awk '
  FNR==1 {fence=0}
  /^```/ {fence=!fence; next}
  fence || !/^\|/ {next}
  {
    incode=0
    for (i=1; i<=length($0); i++) {
      c=substr($0,i,1)
      if (c=="`") incode=!incode
      else if (c=="|" && incode && substr($0,i-1,1)!="\\") {print FILENAME ":" FNR; break}
    }
  }' "$d1" "$d2" "$d3")
if [ -n "$pipes" ]; then echo "FAIL pipe inside code in table row:"; echo "$pipes"; fail=1; else echo "ok   pipe inside code in table rows: 0"; fi

echo "--- spoken words per slot (script, without directions, tags, tables, code)"
awk '
  /^## Приложение/ {exit}
  /^## [0-9][0-9]:[0-9][0-9]/ {if (slot!="") printf "%5d  %s\n", w, slot; slot=$2; w=0; next}
  /^```/ {code=!code; next}
  code || /^\|/ || /^#/ {next}
  slot!="" {
    line=$0
    gsub(/\*\[[^]]*\]\*/, "", line); gsub(/`[^`]*`/, "", line); gsub(/\*/, "", line)
    w+=split(line, a, /[ \t]+/) - (line ~ /^[ \t]/ ? 1 : 0)
  }
  END {if (slot!="") printf "%5d  %s\n", w, slot}
' "$d3"

exit $fail
