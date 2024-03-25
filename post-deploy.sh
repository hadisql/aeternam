#!/bin/bash

echo "Post-deployment script.."

chmod +x /var/lib/dokku/data/storage/aeternam-dev/staticfiles/shell_scripts/fake_data_creation.sh
chmod +x /var/lib/dokku/data/storage/aeternam-dev/staticfiles/shell_scripts/fake_data_deletion.sh

cp -rv /var/lib/dokku/data/storage/aeternam-dev/temp/fake_* /var/lib/dokku/data/storage/aeternam-dev/mediafiles
