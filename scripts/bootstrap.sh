#!/usr/bin/env bash

set -euo pipefail

# Install deps required for picamera Python packages.
sudo apt install -y python3-libcamera python3-kms++ libcap-dev

