# Slack Bot Deployment Instructions

This bot receives Slack messages and writes them to `data/captures.json` in GitHub.

## Prerequisites

1. Node.js installed
2. Cloudflare account (free tier is fine)

## Setup Steps

### 1. Install Wrangler CLI

```bash
npm install -g wrangler
```

### 2. Login to Cloudflare

```bash
wrangler login
```

This will open a browser for authentication.

### 3. Set Secrets

The worker needs two secret tokens:

```bash
wrangler secret put SLACK_BOT_TOKEN
# Paste your Slack bot token when prompted: xoxb-...

wrangler secret put GITHUB_TOKEN
# Paste your GitHub token when prompted: ghp_... or github_pat_...
```

### 4. Deploy

```bash
cd slack-bot
wrangler deploy
```

This will output a URL like: `https://personal-assistant-bot.your-subdomain.workers.dev`

### 5. Configure Slack Event Subscriptions

1. Go to https://api.slack.com/apps
2. Select your "Personal Captures" app
3. Click "Event Subscriptions" in sidebar
4. Enable Events: ON
5. Request URL: Paste the Cloudflare Worker URL from step 4
6. Wait for verification (should show "Verified ✓")
7. Under "Subscribe to bot events" add:
   - `message.im` (messages sent to bot via DM)
8. Click "Save Changes"
9. Slack will prompt to reinstall - click "Reinstall App"

## Usage

In your personal Slack workspace, DM the bot:

```
TASK Work: Schedule meeting with Eric
OUTCOME Personal Growth: Read for 30 minutes
NOTE Personal: Check mortgage rates
PROJECT Work: New trading system idea
```

Format: `TYPE Domain: content`

The bot will:
- Confirm the capture
- Write to GitHub `data/captures.json`
- Claude will process during next check-in

## Message Format

- **TYPE**: TASK, OUTCOME, NOTE, or PROJECT
- **Domain**: Work, Personal, or Personal Growth
- **Content**: What you want to capture

## Troubleshooting

- Check worker logs: `wrangler tail`
- Verify secrets are set: `wrangler secret list`
- Test deployment: `wrangler dev` (local testing)
