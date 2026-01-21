@echo off
REM Pull latest changes from remote repository
REM Run this script at the start of each work session

echo Syncing with remote repository...
git pull origin master

if %errorlevel% equ 0 (
    echo Successfully synced with remote
) else (
    echo Warning: Failed to pull from remote. Please check for conflicts.
    exit /b 1
)
