#!/usr/bin/env bash
# Runs linters and formatters on Python code.

set -euxo pipefail

ROOT="${GITHUB_WORKSPACE:-$(git rev-parse --show-toplevel)}"

cd "$ROOT"
pip install -r vision/requirements.txt

set +x

EXIT_CODE=0

if ! ruff check vision; then
    >&2 echo "❌ Failed some lint checks. See above."
    export EXIT_CODE=1
else
    echo "✅ Passed all lint checks."
fi

if ! ruff format --check vision; then
    >&2 echo "❌ Some files need formatting. See above."
    export EXIT_CODE=1
else
    echo "✅ All files are formatted."
fi

exit $EXIT_CODE