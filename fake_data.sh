#!/bin/bash

# Define arrays for fake data
NAMES=("John Doe" "Jane Smith" "Michael Johnson" "Emily Brown" "Robert Williams")
EMAILS=("john@example.com" "jane@example.com" "michael@example.com" "emily@example.com" "robert@example.com")
ALBUM_DIRS=("0" "1" "2")

# Create 5 inactive users with random names and email as username
echo "Creating users..."
for i in "${!EMAILS[@]}"; do
  email="${EMAILS[$i]}"
  name="${NAMES[$i]}"

  # Create user
  python manage.py create_users "$email" --password 'password123' --full_name "$name" --change_existing
done

# Create Relation object that bonds all users
echo "Creating relation between users..."
python manage.py create_users "${EMAILS[@]}" --relationbetween

# Create albums for 3 users
echo "Creating albums for 3 users..."
python manage.py create_albums 1 "john@example.com" --fill_photos 5 --access "all" --album_name "Album for everyone"
python manage.py create_albums 1 "john@example.com" --fill_photos 3 --access "jane@example.com" "michael@example.com" "robert@example.com" --album_name "For my close friends"
python manage.py create_albums 1 "jane@example.com" --fill_photos 4 --access "all" --album_name "Holidays 😊"
python manage.py create_albums 3 "robert@example.com" --fill_photos 4 4 4 --access "john@example.com"
