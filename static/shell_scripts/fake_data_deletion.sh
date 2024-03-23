#!/bin/bash

echo "Starting the user deletion script.."
sleep 2
echo "We retrieve the fake users list.."
sleep 1

# Retrieve Fake data from the creation script
creation_script_path="staticfiles/shell_scripts/fake_data_creation.sh"
if [ -f "$creation_script_path" ]; then
    # Extract variable values using grep
    names=$(grep '^NAMES=(' "$creation_script_path" | sed 's/NAMES=(//' | sed 's/)//')
    emails=$(grep '^EMAILS=(' "$creation_script_path" | sed 's/EMAILS=(//' | sed 's/)//')
    # Save extracted values as lists
    NAMES=($names)
    EMAILS=($emails)
    # Print
    echo "Names: $names"
    echo "Emails: $emails"
else
    echo "Error: Script file not found"
fi

# FAKE DATA DELETION
sleep 2
echo "Deletion of the fake users.."
sleep 1

for i in "${!EMAILS[@]}"; do
  email="${EMAILS[$i]}"
  python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

# Get the CustomUser model
User = get_user_model()
try:
  user = User.objects.get(email=$email)
  user.delete()
  print(f'User with email $email deleted successfully.')
except User.DoesNotExist:
  print(f'User with email $email does not exist.')
EOF
done
