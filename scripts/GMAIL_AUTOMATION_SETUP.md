# Gmail Automation Setup for GitHub Actions

## Overview
The research email automation needs Gmail API credentials stored as GitHub repository secrets.

## Setup Steps

### 1. Encode Credentials to Base64

From the personal-assistant directory, run:

```bash
# Encode gmail_credentials.json
base64 -w 0 credentials/gmail_credentials.json

# Encode gmail_token.json
base64 -w 0 credentials/gmail_token.json
```

Copy the output from each command.

### 2. Add to GitHub Secrets

1. Go to: https://github.com/shoover-p3/personal-assistant/settings/secrets/actions

2. Click "New repository secret"

3. Add two secrets:
   - Name: `GMAIL_CREDENTIALS_BASE64`
     Value: [paste the base64 output from gmail_credentials.json]

   - Name: `GMAIL_TOKEN_BASE64`
     Value: [paste the base64 output from gmail_token.json]

### 3. Test the Workflow

Once secrets are added, you can manually trigger the workflow:
1. Go to: https://github.com/shoover-p3/personal-assistant/actions
2. Select "Send Research Emails"
3. Click "Run workflow"

## How It Works

### Triggers
The email workflow runs automatically:
- **Daily at 9 AM UTC (4 AM EST)** - checks for unsent research emails
- **On push** - when research agent configs or findings are updated
- **Manual** - via GitHub Actions UI

### Process
1. Checks all active research agents
2. Compares `last_run` vs `email_sent_for_run` in config
3. Sends email for any runs that haven't been emailed
4. Updates config with `email_sent_for_run` date
5. Commits the update

### Email Content
- HTML formatted findings
- Includes full findings.md as attachment
- Sent to: shane.b.hoover@gmail.com, buddyjbush@gmail.com
- Subject: "[Agent Name] - Update [date]"

## Manual Email Send

To manually send an email for a research agent:

```bash
python scripts/send_research_email.py research_ckd_treatment
```

Or to check and send all pending:

```bash
python scripts/send-pending-research-emails.py
```

## Troubleshooting

### Email not sending
- Check GitHub Actions logs for errors
- Verify secrets are set correctly
- Ensure gmail_token.json hasn't expired (refresh by running locally)

### Token expired
If the token expires, run the email script locally once to refresh:
```bash
python scripts/send_research_email.py research_ckd_treatment
```
This will refresh the token, then re-encode and update the secret.
