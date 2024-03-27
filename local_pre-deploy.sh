#!/bin/bash

echo "Pre-deployment script.."
echo "Trying to delete fake folders in mediafiles if present.."
sleep 1

# Define the directory path
directory="/var/lib/dokku/data/storage/aeternam-dev/mediafiles"

# Check if the directory exists
ssh root@aeternam.hadisqalli.com "
    if [ -d \"$directory\" ]; then
        echo 'Checking for folders starting with fake_ in $directory'
        # Find folders starting with 'fake_' and delete them recursively
        find \"$directory\" -type d -name 'fake_*' -exec rm -rfv {} +
        echo 'Folders starting with fake_ deleted'
    else
        echo 'Error: Directory $directory not found'
    fi
"
echo '-----------------------------------'
