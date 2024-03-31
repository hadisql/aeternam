#!/bin/bash

############################################################
############# PREDEPLOYMENT : ERASING MEDIAFILES ###########
############################################################

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 [aeternam | aeternam-dev]"
    exit 1
fi

# Check if the provided argument is valid
if [ "$1" != "aeternam" ] && [ "$1" != "aeternam-dev" ]; then
    echo "Error: Invalid parameter. Please provide 'aeternam' or 'aeternam-dev'."
    exit 1
fi

parameter="$1"

echo "Pre-deployment script.."
echo "Trying to delete fake folders in mediafiles if present.."
sleep 1

# Define the directory path
directory="/var/lib/dokku/data/storage/$parameter/mediafiles"

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
sleep 1

############################################################
############# DEPLOYMENT : PUSHING DOKKU PROJECT ###########
############################################################

echo 'pushing the local script to dokku..'

if [ "$1" = "aeternam-dev" ]; then
  echo "Pushing to the dev project.."
  git push dokku-dev develop:develop
elif [ "$1" = "aeternam" ]; then
  echo "Pushing to the main project.."
  git push dokku main:master
fi

# Check if the push was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to push the project."
    exit 1
fi

echo '-----------------------------------'
sleep 1

#################################################################
############# POSTEPLOYMENT : COPYING MEDIAFILES BACK ###########
#################################################################

echo "giving -x permissions to fake_data shell scripts.."
ssh root@aeternam.hadisqalli.com "chmod +x /var/lib/dokku/data/storage/$parameter/staticfiles/shell_scripts/*"
ssh root@aeternam.hadisqalli.com "dokku enter $parameter web && cd static/shell_scripts && chmod +x ./emails_to_json.sh && ./emails_to_json.sh && python manage.py collectstatic --no-input"

echo '----- first step: syncing local fake data files with temp folder -----'
rsync -azP mediafiles/fake_profile_pictures/ root@aeternam.hadisqalli.com:/var/lib/dokku/data/storage/$parameter/temp/fake_profile_pictures
rsync -azP mediafiles/fake_photos/ root@aeternam.hadisqalli.com:/var/lib/dokku/data/storage/$parameter/temp/fake_photos
rsync -azP mediafiles/fake_albums/ root@aeternam.hadisqalli.com:/var/lib/dokku/data/storage/$parameter/temp/fake_albums


echo "----- second step: Copying fake data files from 'temp' folder.. -----"
ssh root@aeternam.hadisqalli.com "cp -rv /var/lib/dokku/data/storage/$parameter/temp/fake_* /var/lib/dokku/data/storage/$parameter/mediafiles"
