#!/bin/bash

############################################################
############# PREDEPLOYMENT : ERASING MEDIAFILES ###########
############################################################

###### 1 : Building emails.json based on "fake_data_creation" script

# Set the path to emails.json
json_file="static/shell_scripts/emails.json"

# Check if emails.json exists
if [ -f "$json_file" ]; then
    # Get the initial checksum of the file
    initial_checksum=$(md5sum "$json_file" | awk '{ print $1 }')

    # Execute the script to generate/update emails.json
    chmod +x static/shell_scripts/emails_to_json.sh
    static/shell_scripts/emails_to_json.sh

    # Get the checksum of the file after execution
    final_checksum=$(md5sum "$json_file" | awk '{ print $1 }')

    # Compare the checksums to determine if the file was modified
    if [ "$initial_checksum" != "$final_checksum" ]; then
        current_date_time=$(date +"%Y-%m-%d %T")
        git commit -am "Demo emails update during predeployment - $current_date_time"
        # echo "Demo emails update during predeployment - $current_date_time"
    else
        echo "Warning: Failed to detect modifications to emails.json."
    fi
else
    # File doesn't exist, create it
    echo "Error: emails.json doesn't exist. Run \"emails_to_json.sh\" manually before executing this script."
    exit 1
fi

###### 2 : Check if deploy script passed with correct argument

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

###### 3 : Cleaning dokku mediafiles

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
echo '--------------------------------------------------------------------------------------'
echo '----------------- step 1 : predeployment done, mediafiles erased ---------------------'
echo '--------------------------------------------------------------------------------------'

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

echo '--------------------------------------------------------------------------------------'
echo '--------------------- step 2 : deployment done to $parameter -------------------------'
echo '--------------------------------------------------------------------------------------'
sleep 1

#################################################################
############# POSTEPLOYMENT : COPYING MEDIAFILES BACK ###########
#################################################################

echo "giving -x permissions to fake_data shell scripts.."
ssh root@aeternam.hadisqalli.com "chmod +x /var/lib/dokku/data/storage/$parameter/staticfiles/shell_scripts/*"

echo '----- first step: syncing local fake data files with temp folder -----'
rsync -azP mediafiles/fake_profile_pictures/ root@aeternam.hadisqalli.com:/var/lib/dokku/data/storage/$parameter/temp/fake_profile_pictures
rsync -azP mediafiles/fake_photos/ root@aeternam.hadisqalli.com:/var/lib/dokku/data/storage/$parameter/temp/fake_photos
rsync -azP mediafiles/fake_albums/ root@aeternam.hadisqalli.com:/var/lib/dokku/data/storage/$parameter/temp/fake_albums


echo "----- second step: Copying fake data files from 'temp' folder.. -----"
ssh root@aeternam.hadisqalli.com "cp -rv /var/lib/dokku/data/storage/$parameter/temp/fake_* /var/lib/dokku/data/storage/$parameter/mediafiles"

echo '--------------------------------------------------------------------------------------'
echo '-------------------------- step 3 : postdeployment done  -----------------------------'
echo '--------------------------------------------------------------------------------------'