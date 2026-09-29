#!/usr/bin/env sh
# Experiment for issue #638: follow docs/guides/03-deploy-package.md in a
# throw-away HOME. Copies the package with hidden files, installs requirements
# into a venv outside runtime/, runs the package check, then checks how the KB
# may be used: a venv or clone inside runtime/ breaks G-mach, selected text
# articles in docs/kb/ keep it green. Requires git and python3 with venv + pip.
set -u
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
HOME="$(mktemp -d)"; export HOME
gate() { (cd "$HOME/bcreq-pilot/runtime" && sh tools/validate-package.sh > "$HOME/gate.log" 2>&1; echo "exit=$?"; sort -u "$HOME/gate.log" | tail -3); }

mkdir -p ~/bcreq-pilot && cd ~/bcreq-pilot || exit 1
# The guide clones the public repository; the experiment uses the working tree
# so that it checks the package of this branch.
mkdir -p source-lab/projects/ba-ai-process/dist
cp -R "$HERE/../dist/execution-package-gigacode-cli" source-lab/projects/ba-ai-process/dist/
mkdir -p runtime
cp -R source-lab/projects/ba-ai-process/dist/execution-package-gigacode-cli/. runtime/
echo "== hidden entries in runtime:"; ls -A runtime | grep '^\.'
python3 -m venv venv && . venv/bin/activate
python3 -m pip install -q -r runtime/requirements.txt > "$HOME/pip.log" 2>&1; echo "pip exit=$?"
echo "== python3 is $(command -v python3 | sed "s#$HOME#~#")"
echo "== gate after deploy"; gate

echo "== sh tools/run-task works from runtime"
(cd runtime && sh tools/run-task start TASK-0009; sh tools/run-task metrics TASK-0009; rm -rf runs/TASK-0009)

echo "== venv inside runtime (wrong place)"
python3 -m venv runtime/.venv-wrong; gate; rm -rf runtime/.venv-wrong

git clone -q --depth 1 https://github.com/G-Ivan-A/mango-ba-ai-runtime-cli.git kb-source
echo "== KB products:"; ls kb-source/docs/kb | tr '\n' ' '; echo
echo "== one article in docs/kb"
mkdir -p runtime/docs/kb/vpbx-api
cp kb-source/docs/kb/vpbx-api/sections/02-osnovnye-svedeniya.md runtime/docs/kb/vpbx-api/
gate
echo "== all sections of one product in docs/kb"
cp kb-source/docs/kb/vpbx-api/sections/*.md runtime/docs/kb/vpbx-api/
gate
echo "== product index.md in docs/kb (links to Source standards)"
cp kb-source/docs/kb/vpbx-api/index.md runtime/docs/kb/vpbx-api/
gate
rm -rf "$HOME"
