# Gmail API Setup for Research Email Automation

This guide walks you through setting up Gmail API access for automated research findings emails.

## Prerequisites

- Google account (shane.b.hoover@gmail.com)
- Python 3.7+
- Internet connection

## Setup Steps

### 1. Install Required Python Packages

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client markdown2
```

### 2. Enable Gmail API in Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing:
   - Click "Select a Project" at top
   - Click "New Project"
   - Name: "Personal Assistant Email"
   - Click "Create"

3. Enable Gmail API:
   - In the search bar, type "Gmail API"
   - Click "Gmail API"
   - Click "Enable"

### 3. Create OAuth 2.0 Credentials

1. Go to [Credentials page](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted to configure consent screen:
   - Click "Configure Consent Screen"
   - Select "External" (unless you have Google Workspace)
   - Click "Create"
   - Fill in:
     - App name: "Personal Assistant"
     - User support email: shane.b.hoover@gmail.com
     - Developer contact: shane.b.hoover@gmail.com
   - Click "Save and Continue"
   - Skip "Scopes" page (click "Save and Continue")
   - Add test users:
     - Click "Add Users"
     - Enter: shane.b.hoover@gmail.com
     - Click "Add"
   - Click "Save and Continue"
   - Click "Back to Dashboard"

4. Create OAuth Client ID:
   - Go back to Credentials page
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "Personal Assistant Desktop"
   - Click "Create"

5. Download credentials:
   - Click "Download JSON" (⬇ icon) next to your newly created OAuth client
   - Save the file

### 4. Save Credentials to Repository

1. Create credentials directory:
   ```bash
   mkdir C:\Users\SHoover\personal-assistant\credentials
   ```

2. Move downloaded JSON file:
   - Rename downloaded file to `gmail_credentials.json`
   - Move to: `C:\Users\SHoover\personal-assistant\credentials\gmail_credentials.json`

3. Update .gitignore (already done):
   ```
   credentials/
   ```

### 5. First-Time Authentication

1. Run the email script manually to authenticate:
   ```bash
   cd C:\Users\SHoover\personal-assistant
   python scripts/send_research_email.py research_ckd_treatment
   ```

2. Browser will open automatically:
   - Sign in to shane.b.hoover@gmail.com
   - Click "Continue" when warned app isn't verified (it's your own app)
   - Click "Allow" to grant permissions
   - You can close the browser window when done

3. Token saved:
   - A `gmail_token.json` file is created in `credentials/`
   - This stores your authentication for future runs
   - Token auto-refreshes, no need to re-authenticate

### 6. Test Email Send

After authentication completes, check that email was sent to both addresses.

## Troubleshooting

### "Access blocked: Personal Assistant hasn't completed verification"
- This happens because app is in testing mode
- Solution: Make sure you added shane.b.hoover@gmail.com as a test user (Step 3.3)
- Or: Click "Advanced" → "Go to Personal Assistant (unsafe)" (it's safe, it's your app)

### "Token has been expired or revoked"
- Delete `credentials/gmail_token.json`
- Re-run authentication (Step 5)

### "File not found: gmail_credentials.json"
- Verify file location: `C:\Users\SHoover\personal-assistant\credentials\gmail_credentials.json`
- Check file name is exactly `gmail_credentials.json` (not `credentials.json` or similar)

### Import errors
- Run: `pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client markdown2`
- Make sure you're using the correct Python environment

## Security Notes

- **credentials/** directory is in .gitignore - never commit credentials to git
- **gmail_credentials.json** - OAuth client ID (low risk if exposed, but keep private)
- **gmail_token.json** - Your access token (HIGH RISK if exposed - treat like a password)
- Tokens auto-expire and refresh - no manual maintenance needed
- You can revoke access anytime: [Google Account Permissions](https://myaccount.google.com/permissions)

## What Happens When Email Sends

1. Script reads research findings markdown file
2. Converts markdown to styled HTML
3. Authenticates with Gmail using saved token
4. Creates email with:
   - Subject: "[Research Agent Name] - Update [Date]"
   - Body: Formatted HTML findings
   - Attachment: Original .md file for archival
5. Sends to shane.b.hoover@gmail.com and buddyjbush@gmail.com
6. Logs success/failure

## Next Steps

After setup is complete:
- Email automation will run automatically when research agent completes
- No further action needed
- Check your inbox for research updates every 3 days
