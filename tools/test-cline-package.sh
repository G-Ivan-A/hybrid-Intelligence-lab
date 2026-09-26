#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$root/projects/ba-ai-process/build/compile-cline-package.py" --check
python3 "$root/projects/ba-ai-process/tests/cline-package/test_package.py"
python3 "$root/projects/ba-ai-process/dist/execution-package-cline-vscode/tools/run_task.py" verify-ci
