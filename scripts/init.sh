#!/bin/bash

# Execute all bootstrap scripts
# shellcheck source=/dev/null
for file in "$PWD/scripts/bootstrap/"*.sh; do
    source "$file"
done