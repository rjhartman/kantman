#!/usr/bin/env bash
set -euo pipefail

# Check for root user
if [ "$(id -u)" -eq 0 ]; then
  SUDO=""
else
  SUDO="sudo"
fi

# Install deps required for picamera Python packages.
# sudo apt install -y python3-libcamera python3-kms++ libcap-dev
$SUDO apt install -y python3-libcamera libcap-dev
