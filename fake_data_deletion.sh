#!/bin/bash

echo "Starting the user deletion script.."
sleep 2
echo "Deletion of the fake users.."

python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

# Get the CustomUser model
User = get_user_model()

# Define the list of emails
emails = ["m.scott@dundermifflin.com", "j.halpert@dundermifflin.com", "p.beesly@dundermifflin.com", "k.malone@dundermifflin.com"]

# Iterate through the list of emails and delete users with matching emails
for email in emails:
    try:
        user = User.objects.get(email=email)
        user.delete()
        print(f"User with email {email} deleted successfully.")
    except User.DoesNotExist:
        print(f"User with email {email} does not exist.")
EOF
