#!/bin/bash

echo "Pre-deployment script.."
echo "Current location : " && pwd
sleep 1

echo "Trying to list mediafiles :" && sudo ls "/var/lib/dokku/data/storage/aeternam-dev/mediafiles"
