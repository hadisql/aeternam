#!/bin/bash

echo "Pre-deployment script.."
echo "Current location : " && pwd
sleep 1

echo "Trying to list mediafiles :" && ls "/app/mediafiles"
echo "Trying to delete fake folders in mediafiles if present.."
sleep 1

# Define the directory path
directory="/app/mediafiles"

# Check if the directory exists
if [ -d "$directory" ]; then
    echo "Checking for folders starting with 'fake_' in $directory"

    # Find folders starting with 'fake_' and delete them recursively
    find "$directory" -type d -name 'fake_*' -exec rm -rf {} +

    echo "Folders starting with 'fake_' deleted"
else
    echo "Error: Directory $directory not found"
fi

echo "-----------------------------------"
