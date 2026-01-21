# Git Sync Setup

This repository is configured to automatically sync between computers.

## How It Works

### Automatic Push After Commits
A `post-commit` git hook automatically pushes changes to the remote repository after every commit. You don't need to manually run `git push`.

### Session Start Pull
Before starting work, pull the latest changes using one of these methods:

#### Option 1: Run the sync script
- **Windows**: Double-click `sync-pull.bat` or run it from command line
- **Mac/Linux**: Run `./sync-pull.sh` from terminal

#### Option 2: Manual pull
```bash
git pull origin master
```

#### Option 3: Claude Code hook (Recommended)
Configure Claude Code to automatically run the sync script when starting a session by adding this to your Claude Code settings:

```json
{
  "hooks": {
    "on-session-start": "git pull origin master"
  }
}
```

## Workflow Between Computers

1. **On Computer A:**
   - Make changes to files
   - Commit changes: `git add . && git commit -m "Your message"`
   - Changes automatically push to GitHub

2. **On Computer B:**
   - Run `sync-pull.bat` (Windows) or `./sync-pull.sh` (Mac/Linux)
   - Or let Claude Code auto-pull if you configured the hook
   - Continue working with the latest changes

## Files

- `.git/hooks/post-commit` - Automatically pushes after commits
- `sync-pull.sh` - Shell script to pull latest changes
- `sync-pull.bat` - Windows batch script to pull latest changes
- `.gitignore` - Excludes `.claude/` and other local files from git

## Troubleshooting

If you encounter conflicts:
1. Commit or stash your local changes first
2. Run `git pull origin master`
3. Resolve any conflicts manually
4. Commit the resolved changes
