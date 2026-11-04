#!/usr/bin/env bash
# Experiment for issue #719: checks the runtime compilation of rule PT-5.
# 1. The runtime manifest pins a Hub commit that contains PT-5.
# 2. The runtime smoke test and unittests pass on the compiled branch.
# 3. Mutation: an invented atomic_function in a golden case is refused.
# Usage: issue_719_runtime_compile_check.sh [runtime-checkout]
# Without an argument the runtime PR branch is cloned into a temporary folder;
# the Hub and the given checkout are not modified (the mutation runs on a copy).
set -u
HUB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RUNTIME_URL=https://github.com/konard/G-Ivan-A-mango-ba-ai-runtime.git
RUNTIME_REF=issue-719-1e389db848b1
W=$(mktemp -d)
if [ $# -ge 1 ]; then cp -r "$1" "$W/runtime"; else
  git clone -q --depth 1 --branch "$RUNTIME_REF" "$RUNTIME_URL" "$W/runtime"
fi
cd "$W/runtime"
echo "runtime HEAD: $(git rev-parse HEAD)"
hub_commit=$(sed -n 's/^hub_commit: //p' compilation-manifest.yaml)
echo "manifest hub_commit: $hub_commit"
echo "manifest meta_model_version: $(sed -n 's/^meta_model_version: //p' compilation-manifest.yaml)"
skill=$(grep -o 'hub_commit: [0-9a-f]*' skills/transcript-normalization-contact-center.md | cut -d' ' -f2)
[ "$skill" = "$hub_commit" ] && echo "ok - n1 skill compiled from the manifest hub_commit" || echo "not ok - n1 skill hub_commit $skill"
if git -C "$HUB" cat-file -e "$hub_commit^{commit}" 2>/dev/null; then
  git -C "$HUB" show "$hub_commit:projects/ba-ai-process/ba-meta-model/20-taxonomy.md" | grep -q '^| `PT-5` |' \
    && echo "ok - Hub commit contains PT-5" || echo "not ok - Hub commit has no PT-5"
else
  echo "not ok - Hub commit $hub_commit not found in $HUB"
fi
grep -rln 'hybrid-Intelligence-lab' --exclude-dir=.git . | grep -v '^./compilation-manifest.yaml$' \
  && echo "not ok - runtime artifact references the Hub" || echo "ok - only the manifest references the Hub"
echo "--- runtime smoke"
sh tests/runtime-smoke.sh 2>&1 | tail -4
echo "--- runtime unittest"
python3 -m unittest discover -s tests -p 'test_*.py' 2>&1 | tail -3
echo "--- mutation: GS-CC-02 declares the invented id handling-report-export"
sed -i 's#atomic_function: report-builder/function/report-create#atomic_function: handling-report-export#' golden/cases.yaml
python3 -m unittest tests.test_catalog_binding 2>&1 | grep -E 'AssertionError|^FAILED|^OK'
sh tests/runtime-smoke.sh 2>&1 | grep -E '^not ok|failed'
rm -rf "$W"
