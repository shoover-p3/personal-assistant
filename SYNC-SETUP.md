# Git Sync Setup

This repository is configured to automatically sync between computers.

## How It Works

### Automatic Push After Commits
A `post-commit` git hook automatically pushes changes to the remote repository after every commit. You don't need to manually run `git push`.

### Automatic Pull at Session Start (Configured!)
Claude Code is configured to automatically pull the latest changes when you start a session. The `.claude/settings.local.json` file contains a `SessionStart` hook that runs `git pull origin master`.

**No manual action needed!** When you open Claude Code in this directory, it will automatically sync with the remote repository.

### Manual Pull Options (if needed)
If you need to manually pull changes:

#### Option 1: Run the sync script
- **Windows**: Double-click `sync-pull.bat` or run it from command line
- **Mac/Linux**: Run `./sync-pull.sh` from terminal

#### Option 2: Manual pull
```bash
git pull origin master
```

## Workflow Between Computers

1. **On Computer A (e.g., Laptop):**
   - Make changes to files
   - Commit changes: `git add . && git commit -m "Your message"`
   - Changes automatically push to GitHub ✓

2. **On Computer B (e.g., Work PC):**
   - Open Claude Code in the personal-assistant directory
   - Claude Code automatically pulls latest changes ✓
   - Continue working with synced files
   - Make changes, commit them
   - Changes automatically push to GitHub ✓

3. **Back on Computer A:**
   - Open Claude Code in the personal-assistant directory
   - Claude Code automatically pulls latest changes from Computer B ✓
   - Continue working seamlessly

## Files

- `.git/hooks/post-commit` - Automatically pushes after commits
- `.claude/settings.local.json` - Claude Code settings with SessionStart hook for auto-pull
- `sync-pull.sh` - Shell script to manually pull latest changes (rarely needed)
- `sync-pull.bat` - Windows batch script to manually pull latest changes (rarely needed)
- `.gitignore` - Excludes `.claude/` and other local files from git

## Troubleshooting

If you encounter conflicts:
1. Commit or stash your local changes first
2. Run `git pull origin master`
3. Resolve any conflicts manually
4. Commit the resolved changes
