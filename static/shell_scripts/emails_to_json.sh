#!/bin/bash

echo "Importing demo users email list to json file"
# Retrieve Fake data from the creation script
creation_script_path="./fake_data_creation.sh"
if [ -f "$creation_script_path" ]; then
    # Extract variable values using grep
    NAMES_STR=$(grep '^NAMES=(' "$creation_script_path" | sed 's/)$//')
    EMAILS_STR=$(grep '^EMAILS=(' "$creation_script_path" | sed 's/)$//')

    # # Directly echo the extracted strings for debugging
    # echo "NAMES_STR: $NAMES_STR)"
    # echo "EMAILS_STR: $EMAILS_STR)"
    # # Eval the strings to recreate arrays
    eval "$NAMES_STR)"
    eval "$EMAILS_STR)"

    # # # Debugging: Print to verify arrays are correctly formed
    # echo "Extracted Names: ${NAMES[@]}"
    # echo "Extracted Emails: ${EMAILS[@]}"
else
    echo "Error: Script file not found"
fi

# Path to the JSON file
json_file="./emails.json"

# Create a JSON array
echo "[" > "$json_file"
for i in "${!EMAILS[@]}"; do
  echo "{\"email\": \"${EMAILS[$i]}\", \"name\": \"${NAMES[$i]}\"}" >> "$json_file"
  if [ $i -ne $((${#EMAILS[@]}-1)) ]; then
    echo "," >> "$json_file"
  fi
done
echo "]" >> "$json_file"
