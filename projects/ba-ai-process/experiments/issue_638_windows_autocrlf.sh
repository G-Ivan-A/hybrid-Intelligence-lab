#!/usr/bin/env sh
# Issue #638: Git for Windows installs with core.autocrlf=true. Clone the
# GigaCode package the way the deploy guide does and run G-mach on the result.
set -eu
repo="$(git rev-parse --show-toplevel)"
package="projects/ba-ai-process/dist/execution-package-gigacode-cli"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
mkdir "$work/runtime-src"
cp -R "$repo/$package/." "$work/runtime-src/"
git -C "$work/runtime-src" init -q
git -C "$work/runtime-src" -c core.autocrlf=false add -A
git -C "$work/runtime-src" -c user.name=t -c user.email=t@t commit -qm package
git -c core.autocrlf=true clone -q "$work/runtime-src" "$work/runtime"
if grep -q "$(printf '\r')" "$work/runtime/AGENTS.md"; then echo "AGENTS.md has CRLF"; else echo "AGENTS.md keeps LF"; fi
python3 "$work/runtime/tools/validate-package.py" "$work/runtime" 2>&1 | tail -3
