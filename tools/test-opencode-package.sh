#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$root/projects/ba-ai-process/build/compile-opencode-package.py" --check
python3 "$root/projects/ba-ai-process/tests/opencode-package/test_package.py"
python3 "$root/projects/ba-ai-process/dist/execution-package-opencode/tools/run_task.py" verify-ci
