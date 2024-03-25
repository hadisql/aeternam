#!/bin/bash

echo "Post-deployment script.."

sudo chmod +x "/var/lib/dokku/data/storage/aeternam-dev/staticfiles/shell_scripts/fake_data_creation.sh"
sudo chmod +x "/var/lib/dokku/data/storage/aeternam-dev/staticfiles/shell_scripts/fake_data_deletion.sh"

sudo cp -rv /var/lib/dokku/data/storage/aeternam-dev/temp/fake_* /var/lib/dokku/data/storage/aeternam-dev/mediafiles
