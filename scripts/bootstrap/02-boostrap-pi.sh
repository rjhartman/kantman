#!/usr/bin/env bash
set -euo pipefail

# Check for root user
if [ "$(id -u)" -eq 0 ]; then
  SUDO=""
else
  SUDO="sudo"
fi

# Install deps required for picamera Python packages.
# Detect if running on a Raspberry Pi or not.
if [ -f /etc/os-release ]; then
  if [ "$(cat /etc/os-release)" == "raspbian" ]; then
    $SUDO apt install -y python3-libcamera python3-kms++ libcap-dev
  else
    $SUDO apt install -y python3-libcamera libcap-dev
  fi
fi
