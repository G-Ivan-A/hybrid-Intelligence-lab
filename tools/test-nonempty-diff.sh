#!/usr/bin/env bash
# Регрессионный тест валидатора непустого диффа (стресс-тест S5 RFC #470):
# доказывает, что валидатор ПАДАЕТ на пустом диффе, проходит на непустом
# и корректно обрабатывает escape-метку `no-diff-expected`.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VALIDATOR="$ROOT_DIR/tools/validate-nonempty-diff.sh"

work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT

failures=0

report() {
  local status="$1" name="$2"
  printf '%s %s\n' "$status" "$name"
  [[ "$status" == "FAIL" ]] && failures=$((failures + 1))
  return 0
}

# Прогон валидатора в изолированном репозитории; печатает код возврата.
run_validator() {
  local repo="$1"
  shift
  set +e
  env NONEMPTY_DIFF_REPO="$repo" "$@" bash "$VALIDATOR" >"$work_dir/out.log" 2>&1
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

# Изолированный репозиторий: main + ветка feature без содержательных изменений.
repo="$work_dir/repo"
mkdir -p "$repo"
git -C "$repo" init --quiet --initial-branch=main
git -C "$repo" config user.email "test@example.com"
git -C "$repo" config user.name "Test"
printf 'base\n' >"$repo/README.md"
git -C "$repo" add README.md
git -C "$repo" commit --quiet -m "base"

git -C "$repo" checkout --quiet -b empty-pr
# Пустой дифф: коммит без изменений содержимого репозитория.
git -C "$repo" commit --quiet --allow-empty -m "empty work"

expect_fail "валидатор падает на пустом диффе (S5)" "$repo" \
  "не содержит полезного диффа" BASE_REF=main

# Дифф только в служебном файле-заглушке тоже считается пустым.
git -C "$repo" checkout --quiet -b placeholder-pr main
printf 'placeholder\n' >"$repo/pull-request-bootstrap.md"
git -C "$repo" add pull-request-bootstrap.md
git -C "$repo" commit --quiet -m "placeholder only"

expect_fail "дифф только в служебной заглушке считается пустым" "$repo" \
  "не содержит полезного диффа" BASE_REF=main

# Непустой дифф проходит.
git -C "$repo" checkout --quiet -b real-pr main
printf 'real change\n' >>"$repo/README.md"
git -C "$repo" commit --quiet -am "real work"

expect_pass "валидатор проходит на непустом диффе" "$repo" BASE_REF=main

# Проверка устойчивости к движению base: base ушёл вперёд после ветвления.
git -C "$repo" checkout --quiet main
printf 'base moved\n' >>"$repo/README.md"
git -C "$repo" commit --quiet -am "base moved"
git -C "$repo" checkout --quiet real-pr

expect_pass "three-dot дифф устойчив к движению base" "$repo" BASE_REF=main

# Escape-метка от авторизованного пользователя пропускает пустой дифф.
git -C "$repo" checkout --quiet empty-pr
expect_pass "метка no-diff-expected от owner пропускает проверку" "$repo" \
  BASE_REF=main PR_LABELS="no-diff-expected" NO_DIFF_LABEL_ACTOR_ROLE=OWNER

expect_pass "метка no-diff-expected от admin пропускает проверку" "$repo" \
  BASE_REF=main PR_LABELS="ops, no-diff-expected" NO_DIFF_LABEL_ACTOR_ROLE=admin

# Escape-метка от неавторизованного пользователя не пропускает.
expect_fail "метка от неавторизованного пользователя не пропускает" "$repo" \
  "неавторизованным пользователем" \
  BASE_REF=main PR_LABELS="no-diff-expected" NO_DIFF_LABEL_ACTOR_ROLE=CONTRIBUTOR

expect_fail "метка без роли не пропускает" "$repo" \
  "неавторизованным пользователем" \
  BASE_REF=main PR_LABELS="no-diff-expected"

# Посторонняя метка не даёт escape.
expect_fail "посторонняя метка не даёт escape" "$repo" \
  "не содержит полезного диффа" \
  BASE_REF=main PR_LABELS="ops,ci" NO_DIFF_LABEL_ACTOR_ROLE=OWNER

# Недоступная base-ревизия диагностируется явно, а не молча проходит.
expect_fail "недоступная base-ревизия диагностируется" "$repo" \
  "недоступна" BASE_REF=no-such-branch

if ((failures > 0)); then
  printf 'ERROR: nonempty diff validator regression tests failed: %s\n' "$failures" >&2
  exit 1
fi

printf 'Nonempty diff validator regression tests passed.\n'
