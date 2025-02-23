#!/usr/bin/env bash
# Validates that the compiled Python requirements are up to date.

set -euxo pipefail

ROOT="${GITHUB_WORKSPACE:-$(git rev-parse --show-toplevel)}"

cd "$ROOT"
make compile-requirements

set +x

if ! git diff --exit-code; then
    echo "❌ Python requirements need updating. See diff output above."
    exit 1
fi

echo "✅ Python requirements are up to date."