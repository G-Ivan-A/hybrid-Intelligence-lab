#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

tmp_root="$(mktemp -d)"
trap 'rm -rf "$tmp_root"' EXIT

fixture="$tmp_root/agent-work-rules.md"

make_fixture() {
  # 3.2 байта на токен: нужное число байт задаётся напрямую.
  head -c "$1" /dev/zero | tr '\0' 'a' > "$fixture"
}

# 1. Ниже обоих порогов: успех без предупреждений.
make_fixture 3200
if ! TARGET_FILE="$fixture" ./tools/check-agent-work-rules-size.sh \
    >"$tmp_root/out" 2>"$tmp_root/err"; then
  printf 'Expected pass for small file.\n' >&2
  cat "$tmp_root/err" >&2
  exit 1
fi
if grep -q 'WARNING' "$tmp_root/err"; then
  printf 'Unexpected warning for small file.\n' >&2
  exit 1
fi

# 2. Между порогами: успех с предупреждением.
make_fixture 25600  # ~8000 токенов
if ! TARGET_FILE="$fixture" ./tools/check-agent-work-rules-size.sh \
    >"$tmp_root/out" 2>"$tmp_root/err"; then
  printf 'Expected pass with warning for mid-size file.\n' >&2
  cat "$tmp_root/err" >&2
  exit 1
fi
if ! grep -Fq 'WARNING' "$tmp_root/err"; then
  printf 'Expected warning for mid-size file.\n' >&2
  cat "$tmp_root/err" >&2
  exit 1
fi

# 3. Выше жёсткого порога: падение.
make_fixture 32000  # ~10000 токенов
if TARGET_FILE="$fixture" ./tools/check-agent-work-rules-size.sh \
    >"$tmp_root/out" 2>"$tmp_root/err"; then
  printf 'Expected failure for oversized file.\n' >&2
  exit 1
fi
if ! grep -Fq 'exceeds the hard budget' "$tmp_root/err"; then
  printf 'Expected hard budget error message.\n' >&2
  cat "$tmp_root/err" >&2
  exit 1
fi

# 4. Отсутствующий файл — тоже ошибка (fail-closed).
if TARGET_FILE="$tmp_root/missing.md" ./tools/check-agent-work-rules-size.sh \
    >"$tmp_root/out" 2>"$tmp_root/err"; then
  printf 'Expected failure for missing target.\n' >&2
  exit 1
fi
if ! grep -Fq 'budget invariant target not found' "$tmp_root/err"; then
  printf 'Expected missing-target error message.\n' >&2
  cat "$tmp_root/err" >&2
  exit 1
fi

# 5. Реальный файл репозитория проходит проверку.
./tools/check-agent-work-rules-size.sh >/dev/null

printf 'Agent work rules size check regression tests passed.\n'
