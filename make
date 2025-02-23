#!/bin/bash
# Shell script that wraps Make to perform required setup.

if [ ! -e .venv ]; then
    python3.12 -m venv .venv
fi

. .venv/bin/activate
make "$@"
