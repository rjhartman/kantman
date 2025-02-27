#!/bin/bash

# Execute all bootstrap scripts
for file in "$PWD/scripts/bootstrap/"*.sh; do
    echo "Executing $file"
    . "$file"
done

# Execute make tasks
# make python-deps
