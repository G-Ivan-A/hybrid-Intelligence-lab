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
