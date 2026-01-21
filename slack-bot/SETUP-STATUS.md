# Slack Bot Setup Status

**Date:** 2026-01-21
**Status:** Deployment complete, but messaging blocked

## What's Working ✓

1. **Cloudflare Worker Deployed**
   - URL: `https://personal-assistant-bot.shane-b-hoover.workers.dev`
   - Secrets configured in Cloudflare (via `wrangler secret put`):
     - `SLACK_BOT_TOKEN`: ✓ Set (xoxb-...)
     - `GITHUB_TOKEN`: ✓ Set (github_pat_...)
   - Worker code deployed successfully

2. **Cloudflare Account**
   - Logged in as: shane.b.hoover@gmail.com
   - Account ID: acada9ffa09d1e74f4814a17f6ef513a
   - Workers.dev subdomain: shane-b-hoover.workers.dev

3. **Wrangler CLI Installed**
   - Version: 4.59.3
   - Authenticated and ready

## Current Issue ❌

**Problem:** When trying to send DM to bot in Slack, it says: "Sending messages to this app has been turned off."

## What We've Tried

### OAuth & Permissions
- Verified bot token scopes include:
  - `chat:write`
  - `im:history`
  - `im:read`
- Reinstalled app multiple times from OAuth & Permissions

### App Home Configuration
- **Messages Tab**: ON ✓
- **Home Tab**: Was OFF (didn't change this)
- Verified "Allow users to send Slash commands and messages from the messages tab" setting

### Event Subscriptions
- **Enabled**: Yes ✓
- **Request URL**: `https://personal-assistant-bot.shane-b-hoover.workers.dev` - **Verified ✓**
- **Bot Events Subscribed**:
  - `message.im` ✓
- **User Events**: None (not needed)

### Troubleshooting Attempts
1. Multiple reinstalls of the app to workspace
2. Removed and reinstalled app completely fresh
3. Verified all scopes were present
4. Checked Messages Tab was enabled
5. Confirmed Event Subscriptions were verified and saved

## Next Steps to Try

### Option 1: Check Interactivity Settings
1. Go to https://api.slack.com/apps → Your App
2. Click **"Interactivity & Shortcuts"** in sidebar
3. Check if there's a setting related to messages
4. May need to enable interactivity

### Option 2: Verify Bot User Exists
1. Go to **"App Home"**
2. Look at "Your App's Presence in Slack" section at top
3. Confirm bot user is configured with:
   - Display Name
   - Default Username
4. If no bot user exists, may need to add "Legacy Bot User"

### Option 3: Check App Installation in Workspace
1. In Slack workspace: Click workspace name → "Settings & administration" → "Manage apps"
2. Find the bot in installed apps list
3. Verify it shows as installed and active
4. Check what permissions are actually granted in the installation

### Option 4: Review Slack App Configuration Page
1. Look for any warnings or errors on the app dashboard
2. Check "Install App" section for any pending actions
3. Verify the workspace the app is installed to is correct

### Option 5: Create New Slack App (Last Resort)
If all else fails, may need to:
1. Create a brand new Slack app from scratch at https://api.slack.com/apps
2. Use "From scratch" option
3. Configure all settings fresh:
   - Add bot user
   - Set OAuth scopes: `chat:write`, `im:history`, `im:read`
   - Enable Event Subscriptions with Request URL
   - Subscribe to `message.im` bot event
   - Enable Messages Tab in App Home
4. Install to workspace
5. Update secrets in Cloudflare with new bot token:
   ```bash
   cd slack-bot
   echo "NEW_TOKEN" | wrangler secret put SLACK_BOT_TOKEN
   ```

## Test Plan (Once Working)

When the messaging issue is resolved:

1. **Test Basic Capture:**
   ```
   TASK Work: Test the personal assistant bot
   ```
   Expected: Bot replies with "✓ Captured: TASK in Work"

2. **Verify GitHub Write:**
   - Check `data/captures.json` in GitHub repo
   - Should see new entry with timestamp, type, domain, content

3. **Test All Message Types:**
   ```
   OUTCOME Personal Growth: Read for 30 minutes
   NOTE Personal: Check mortgage rates
   PROJECT Work: New trading system idea
   ```

4. **Test Invalid Format:**
   Send: "Just a regular message"
   Expected: Bot replies with format help message

## Useful Commands

```bash
# Check Cloudflare login status
wrangler whoami

# View deployed worker
wrangler deployments list

# View worker logs (live tail)
wrangler tail

# Update secrets
echo "NEW_TOKEN" | wrangler secret put SLACK_BOT_TOKEN
echo "NEW_TOKEN" | wrangler secret put GITHUB_TOKEN

# Redeploy worker (if code changes)
cd slack-bot
wrangler deploy
```

## Resources

- Slack App Dashboard: https://api.slack.com/apps
- Cloudflare Dashboard: https://dash.cloudflare.com/acada9ffa09d1e74f4814a17f6ef513a
- Worker URL: https://personal-assistant-bot.shane-b-hoover.workers.dev
- GitHub Repo: https://github.com/shoover-p3/personal-assistant
