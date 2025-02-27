#!/usr/bin/env bash
set -euo pipefail

# Check for root user
if [ "$(id -u)" -eq 0 ]; then
  SUDO=""
else
  SUDO="sudo"
fi

$SUDO apt update && $SUDO apt install -y make build-essential python3.12 python3.12-venv python3.12-dev
