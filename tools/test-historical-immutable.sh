#!/usr/bin/env bash
# Регрессионный тест валидатора иммутабельности исторических документов:
# доказывает, что валидатор ПАДАЕТ на изменении существующего RFC/ADR,
# проходит на добавлении нового и корректно обрабатывает allowlist
# совместимых редиректов (deprecated артефакты).
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VALIDATOR="$ROOT_DIR/tools/validate-historical-immutable.sh"

work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT

failures=0

report() {
  local status="$1" name="$2"
  printf '%s %s\n' "$status" "$name"
  [[ "$status" == "FAIL" ]] && failures=$((failures + 1))
  return 0
}

run_validator() {
  local repo="$1"
  shift
  set +e
  env HISTORICAL_IMMUTABLE_REPO="$repo" "$@" bash "$VALIDATOR" >"$work_dir/out.log" 2>&1
  local code=$?
  set -e
  printf '%s' "$code"
}

expect_pass() {
  local name="$1" repo="$2"
  shift 2
  local code
  code="$(run_validator "$repo" "$@")"
  if [[ "$code" == "0" ]]; then
    report "PASS" "$name"
  else
    report "FAIL" "$name (ожидался успех, код $code)"
    sed 's/^/    /' "$work_dir/out.log"
  fi
}

expect_fail() {
  local name="$1" repo="$2" expected_text="$3"
  shift 3
  local code
  code="$(run_validator "$repo" "$@")"
  if [[ "$code" == "0" ]]; then
    report "FAIL" "$name (валидатор прошёл там, где должен был упасть)"
    sed 's/^/    /' "$work_dir/out.log"
  elif ! grep -qF "$expected_text" "$work_dir/out.log"; then
    report "FAIL" "$name (нет ожидаемого сообщения: $expected_text)"
    sed 's/^/    /' "$work_dir/out.log"
  else
    report "PASS" "$name"
  fi
}

git_in() { git -C "$repo" "$@"; }

# Изолированный репозиторий с историческими документами в main.
repo="$work_dir/repo"
mkdir -p "$repo/docs/rfc" "$repo/docs/adr"
git_in init --quiet --initial-branch=main
git_in config user.email "test@example.com"
git_in config user.name "Test"
cat >"$repo/docs/rfc/2026-01-01-rfc-historical.md" <<'EOF'
---
status: accepted
---

# RFC: историческое решение

Тело исторического RFC.
EOF
cat >"$repo/docs/adr/2026-01-adr-001-historical.md" <<'EOF'
---
status: accepted
---

# ADR-001: историческое решение

Тело исторического ADR.
EOF
printf 'base\n' >"$repo/README.md"
git_in add .
git_in commit --quiet -m "base"

# 1. Изменение существующего RFC — падение.
git_in checkout --quiet -b modify-rfc
printf '\nПереписанный абзац.\n' >>"$repo/docs/rfc/2026-01-01-rfc-historical.md"
git_in commit --quiet -am "rewrite historical rfc"

expect_fail "валидатор падает на изменении существующего RFC" "$repo" \
  "изменение существующего исторического документа" BASE_REF=main

# 2. Изменение существующего ADR — падение.
git_in checkout --quiet -b modify-adr main
printf '\nПереписанный абзац.\n' >>"$repo/docs/adr/2026-01-adr-001-historical.md"
git_in commit --quiet -am "rewrite historical adr"

expect_fail "валидатор падает на изменении существующего ADR" "$repo" \
  "docs/adr/2026-01-adr-001-historical.md" BASE_REF=main

# 3. Удаление существующего RFC — падение.
git_in checkout --quiet -b delete-rfc main
git_in rm --quiet "docs/rfc/2026-01-01-rfc-historical.md"
git_in commit --quiet -m "delete historical rfc"

expect_fail "валидатор падает на удалении существующего RFC" "$repo" \
  "удаление существующего исторического документа" BASE_REF=main

# 4. Добавление нового RFC — проход.
git_in checkout --quiet -b add-rfc main
cat >"$repo/docs/rfc/2026-02-01-rfc-new.md" <<'EOF'
---
status: proposed
---

# RFC: новое решение

Новое решение вместо старого.
EOF
git_in add docs/rfc/2026-02-01-rfc-new.md
git_in commit --quiet -m "add new rfc"

expect_pass "валидатор проходит на добавлении нового RFC" "$repo" BASE_REF=main

# 5. Изменения вне защищаемых каталогов — проход.
git_in checkout --quiet -b other-change main
printf 'unrelated\n' >>"$repo/README.md"
git_in commit --quiet -am "unrelated change"

expect_pass "изменения вне docs/rfc и docs/adr не блокируются" "$repo" BASE_REF=main

# 6. Allowlist: совместимый редирект (deprecated) — проход.
git_in checkout --quiet -b redirect main
cat >"$repo/docs/rfc/2026-01-01-rfc-historical.md" <<'EOF'
---
status: deprecated
---

# RFC: историческое решение (deprecated)

Актуальная версия: [RFC 2026-02-01](2026-02-01-rfc-new.md).
EOF
git_in commit --quiet -am "deprecate via compatibility redirect"

expect_pass "совместимый редирект deprecated разрешён" "$repo" BASE_REF=main

# 6b. superseded — тоже совместимый редирект.
git_in checkout --quiet -b redirect-superseded main
cat >"$repo/docs/adr/2026-01-adr-001-historical.md" <<'EOF'
---
status: superseded
---

# ADR-001 (superseded)

Заменён: [ADR-002](2026-02-adr-002-new.md).
EOF
git_in commit --quiet -am "supersede via compatibility redirect"

expect_pass "совместимый редирект superseded разрешён" "$repo" BASE_REF=main

# 7. Переписывание документа под видом deprecated (длинное тело) — падение.
git_in checkout --quiet -b fake-redirect main
{
  printf -- '---\nstatus: deprecated\n---\n\n# RFC: переписанный\n\n'
  printf 'Ссылка: [новый](2026-02-01-rfc-new.md)\n\n'
  for i in $(seq 1 60); do printf 'Содержательный абзац %s.\n\n' "$i"; done
} >"$repo/docs/rfc/2026-01-01-rfc-historical.md"
git_in commit --quiet -am "fake redirect with full rewrite"

expect_fail "deprecated с длинным телом не считается редиректом" "$repo" \
  "изменение существующего исторического документа" BASE_REF=main

# 8. deprecated без ссылки не считается редиректом.
git_in checkout --quiet -b redirect-no-link main
cat >"$repo/docs/rfc/2026-01-01-rfc-historical.md" <<'EOF'
---
status: deprecated
---

# RFC: историческое решение

Устарело.
EOF
git_in commit --quiet -am "deprecated without link"

expect_fail "deprecated без ссылки не считается редиректом" "$repo" \
  "изменение существующего исторического документа" BASE_REF=main

# 9. Явный allowlist по glob пропускает изменение.
git_in checkout --quiet modify-rfc
expect_pass "явный allowlist пропускает изменение" "$repo" \
  BASE_REF=main HISTORICAL_IMMUTABLE_ALLOWLIST="docs/rfc/2026-01-01-rfc-historical.md"

expect_fail "посторонний allowlist не пропускает изменение" "$repo" \
  "изменение существующего исторического документа" \
  BASE_REF=main HISTORICAL_IMMUTABLE_ALLOWLIST="docs/rfc/other-*.md"

# 9b. Переименование существующего RFC — падение (оба пути защищены).
git_in checkout --quiet -b rename-rfc main
git_in mv "docs/rfc/2026-01-01-rfc-historical.md" "docs/rfc/2026-01-01-rfc-renamed.md"
git_in commit --quiet -m "rename historical rfc"

expect_fail "валидатор падает на переименовании существующего RFC" "$repo" \
  "переименование существующего исторического документа" BASE_REF=main

# 10. three-dot дифф устойчив к движению base-ветки.
git_in checkout --quiet main
printf '\nБаза ушла вперёд.\n' >>"$repo/docs/rfc/2026-01-01-rfc-historical.md"
git_in commit --quiet -am "base moved historical doc"
git_in checkout --quiet add-rfc

expect_pass "three-dot дифф устойчив к движению base" "$repo" BASE_REF=main

# 11. Недоступная base-ревизия диагностируется явно.
expect_fail "недоступная base-ревизия диагностируется" "$repo" \
  "недоступна" BASE_REF=no-such-branch

if ((failures > 0)); then
  printf 'ERROR: historical immutability validator regression tests failed: %s\n' "$failures" >&2
  exit 1
fi

printf 'Historical immutability validator regression tests passed.\n'
