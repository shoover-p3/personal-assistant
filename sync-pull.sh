#!/bin/bash
# Pull latest changes from remote repository
# Run this script at the start of each work session

echo "Syncing with remote repository..."
git pull origin master

if [ $? -eq 0 ]; then
    echo "Successfully synced with remote"
else
    echo "Warning: Failed to pull from remote. Please check for conflicts."
    exit 1
fi
