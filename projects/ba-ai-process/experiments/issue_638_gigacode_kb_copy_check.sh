#!/usr/bin/env sh
# Experiment for issue #638: does the runtime KB fit into docs/kb/ of the
# GigaCode package without breaking G-mach? Clones the KB source, copies it
# into a temp package copy and runs the gate twice: full KB, then text only.
# Requires git and python3 with PyYAML and jsonschema.
set -u
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
WORK="$(mktemp -d)"
git clone -q --depth 1 https://github.com/G-Ivan-A/mango-ba-ai-runtime-cli.git "$WORK/kb-source"
cp -R "$HERE/../dist/execution-package-gigacode-cli" "$WORK/runtime"
cp -R "$WORK/kb-source/docs/kb/." "$WORK/runtime/docs/kb/"
echo "== KB files by extension"
find "$WORK/runtime/docs/kb" -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
echo "== gate with full KB"
(cd "$WORK/runtime" && sh tools/validate-package.sh > "$WORK/gate.log" 2>&1; echo "exit=$?"; tail -1 "$WORK/gate.log")
find "$WORK/runtime/docs/kb" -type f \( -name '*.png' -o -name '*.jpeg' \) -delete
echo "== gate with KB text files only"
(cd "$WORK/runtime" && sh tools/validate-package.sh > "$WORK/gate.log" 2>&1; echo "exit=$?"; sort -u "$WORK/gate.log" | tail -4)
rm -rf "$WORK"
