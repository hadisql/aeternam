#!/bin/bash

echo "Post-deployment script.."

echo "Trying to list app folder :" && ls /app && /app/staticfiles
echo "giving execution permission to fake_data_creation file.." && chmod +x "app/staticfiles/shell_scripts/fake_data_creation.sh"
echo "giving execution permission to fake_data_deletion file.." && chmod +x "app/staticfiles/shell_scripts/fake_data_deletion.sh"

echo "Copying mediafiles from temp to mediafiles folder.."
cp -rv /app/temp/fake_* /app/mediafiles
