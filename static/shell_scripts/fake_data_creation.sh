#!/bin/bash

# Define arrays for fake data
# NAMES=("John Doe" "Jane Smith" "Michael Johnson" "Emily Brown" "Robert Williams")
# EMAILS=("john@example.com" "jane@example.com" "michael@example.com" "emily@example.com" "robert@example.com")
NAMES=("Michael Scott" "Jim Halpert" "Pam Beesly" "Kevin Malone")
EMAILS=("m.scott@dundermifflin.com" "j.halpert@dundermifflin.com" "p.beesly@dundermifflin.com" "k.malone@dundermifflin.com")

# Create users
echo "Creating users..."
for i in "${!EMAILS[@]}"; do
  email="${EMAILS[$i]}"
  name="${NAMES[$i]}"

  # Check if fake data already in db
  echo "Checking if fake data already in db.."
  sleep 1
  python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
try:
  user = User.objects.get(email="$email")
  if user:
    user.delete()
    print(f'user with email $email was in db. it is now deleted')
except User.DoesNotExist:
  print('User with email $email does not exist. It will be created')
EOF

  # Create user
  python manage.py create_users "$email" --password 'password123' --full_name "$name" --change_existing
done

# Create Relation object that bonds all users
echo "Creating relation between users..."
python manage.py create_users "${EMAILS[@]}" --relationbetween

# Create albums for 3 users
# echo "Creating albums for 3 users..."
# python manage.py create_albums 1 "john@example.com" --fill_photos 5 --access "all" --album_name "Album for everyone"
# python manage.py create_albums 1 "john@example.com" --fill_photos 3 --access "jane@example.com" "michael@example.com" "robert@example.com" --album_name "For my close friends"
# python manage.py create_albums 1 "jane@example.com" --fill_photos 4 --access "all" --album_name "Holidays 😊"
# python manage.py create_albums 3 "robert@example.com" --fill_photos 4 4 4 --access "john@example.com"

echo "Creating albums for our 'the office' characters.."
python manage.py create_albums 2 "m.scott@dundermifflin.com" --access "all" --album_name "Holidays" "Personal"
python manage.py create_albums 1 "j.halpert@dundermifflin.com" --access "p.beesly@dundermifflin.com" --album_name "Pam and I"
python manage.py create_albums 1 "k.malone@dundermifflin.com" --access "all" --album_name "Kevin"
