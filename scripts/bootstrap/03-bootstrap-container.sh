#!/bin/bash

set -euo pipefail

# Check for root user
if [ "$(id -u)" -eq 0 ]; then
  SUDO=""
else
  SUDO="sudo"
fi

# Install devcontainer tooling
$SUDO apt update && $SUDO apt install -y git