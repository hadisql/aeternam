#!/bin/bash

# Define arrays for fake data
# NAMES=("John Doe" "Jane Smith" "Michael Johnson" "Emily Brown" "Robert Williams")
# EMAILS=("john@example.com" "jane@example.com" "michael@example.com" "emily@example.com" "robert@example.com")
NAMES=("Michael Scott" "Jim Halpert" "Pam Beesly" "Kevin Malone")
EMAILS=("m.scott@dundermifflin.com" "j.halpert@dundermifflin.com" "p.beesly@dundermifflin.com" "k.malone@dundermifflin.com")

# Create users
echo "Creating users from the office.."
for i in "${!EMAILS[@]}"; do
  EMAIL="${EMAILS[$i]}"
  NAME="${NAMES[$i]}"
  python manage.py create_user "$EMAIL" --password 'password123' --full_name "$NAME"
done

# Create Relation object that bonds all users
echo "Creating relation between users..."
for i in "${!EMAILS[@]}";do
  for ((j=i+1; j<${#EMAILS[@]}; j++)); do
      # incrementing j because the relation object is unique by pair (symmetry)
      echo "creating relation between ${NAMES[$i]} and ${NAMES[$j]}"
      python manage.py create_relation ${EMAILS[$i]} ${EMAILS[$j]}
  done
done

# Create albums for 3 users
# echo "Creating albums for 3 users..."
# python manage.py create_albums 1 "john@example.com" --fill_photos 5 --access "all" --album_name "Album for everyone"
# python manage.py create_albums 1 "john@example.com" --fill_photos 3 --access "jane@example.com" "michael@example.com" "robert@example.com" --album_name "For my close friends"
# python manage.py create_albums 1 "jane@example.com" --fill_photos 4 --access "all" --album_name "Holidays 😊"
# python manage.py create_albums 3 "robert@example.com" --fill_photos 4 4 4 --access "john@example.com"

echo "Creating albums for our 'the office' characters.."
# python manage.py create_albums 2 "m.scott@dundermifflin.com" --access "all" --album_name "Holidays" "Personal"
# python manage.py create_albums 1 "j.halpert@dundermifflin.com" --access "p.beesly@dundermifflin.com" --album_name "Pam and I"
# python manage.py create_albums 1 "k.malone@dundermifflin.com" --access "all" --album_name "Kevin"
