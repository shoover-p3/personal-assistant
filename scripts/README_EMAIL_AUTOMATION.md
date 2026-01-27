# Research Email Automation

Automatically sends research findings via Gmail when research agents complete their runs.

## Quick Start

### 1. One-Time Setup (5 minutes)

Follow the setup guide: `scripts/GMAIL_SETUP.md`

**Summary:**
```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Follow Gmail_SETUP.md to:
# - Enable Gmail API in Google Cloud Console
# - Download credentials
# - Place in credentials/gmail_credentials.json
# - Run first-time authentication
```

### 2. Test Manual Send

After setup, test by manually sending the CKD research findings:

```bash
cd C:\Users\SHoover\personal-assistant
python scripts/send_research_email.py research_ckd_treatment
```

Expected output:
```
Authenticating with Gmail...
Converting findings to HTML...
Sending email: CKD Treatment Research Monitor - Update 2026-01-24
✓ Email sent successfully (Message ID: ...)
  Recipients: shane.b.hoover@gmail.com, buddyjbush@gmail.com
```

Check both inboxes for the formatted email with attachment.

## How It Works

### Email Format

**Subject:** `[Research Agent Name] - Update [Date]`
- Example: "CKD Treatment Research Monitor - Update 2026-01-27"

**Body:** HTML-formatted findings with:
- Styled headers and sections
- Clickable links
- Color-coded important information
- Professional layout

**Attachment:** Original `.md` file for archival

### Recipients

- shane.b.hoover@gmail.com (you)
- buddyjbush@gmail.com (Buddy)

### Trigger

Currently **manual** - after research agent runs:
```bash
python scripts/send_research_email.py research_ckd_treatment
```

**To make fully automatic:** Add to research agent completion workflow (see Integration section below).

## Integration with Research Agents

### Current Research Agents

1. **CKD Treatment Research** (`research_ckd_treatment`)
   - Runs every 3 days
   - Next run: 2026-01-27
   - Findings: `data/research-agents/research_ckd_treatment/findings.md`

### Making It Automatic

**Option A: Call from Claude during check-in**
When research agent completes, Claude calls:
```bash
python scripts/send_research_email.py research_ckd_treatment
```

**Option B: Windows Task Scheduler** (future enhancement)
Schedule script to run after research agent completes.

**Option C: GitHub Actions** (future enhancement)
Trigger email on findings.md file change.

### Adding New Research Agents

To email findings from a new research agent:

1. Ensure research agent has:
   - `config.json` with `findings_file` path
   - Valid findings markdown file
   - `schedule.last_run` date in config

2. Run email script with agent ID:
   ```bash
   python scripts/send_research_email.py <agent_id>
   ```

Example for a new "market_research" agent:
```bash
python scripts/send_research_email.py market_research
```

## Customization

### Change Recipients

Edit `scripts/send_research_email.py`:
```python
RECIPIENTS = ["shane.b.hoover@gmail.com", "buddyjbush@gmail.com", "new@email.com"]
```

### Change Email Styling

Edit HTML template in `markdown_to_html()` function in `send_research_email.py`.

### Change Subject Format

Edit subject line in `send_research_findings()` function:
```python
subject = f"{config['name']} - Update {run_date}"
```

## Troubleshooting

### "Credentials not found"
- Run Gmail setup: `scripts/GMAIL_SETUP.md`
- Verify: `credentials/gmail_credentials.json` exists

### "Token expired"
- Delete `credentials/gmail_token.json`
- Re-run script to re-authenticate

### "Research agent config not found"
- Check agent ID spelling
- Verify config exists: `data/research-agents/<agent_id>/config.json`

### Email not received
- Check spam folder
- Verify recipients in script
- Check Gmail API quota (shouldn't be an issue for low volume)

### Import errors
```bash
pip install -r scripts/requirements.txt
```

## Security

- All credentials stored in `credentials/` (git-ignored)
- OAuth tokens auto-refresh
- Can revoke access: [Google Account Permissions](https://myaccount.google.com/permissions)
- NEVER commit credentials to git

## Files

- `scripts/send_research_email.py` - Main email script
- `scripts/GMAIL_SETUP.md` - Setup instructions
- `scripts/requirements.txt` - Python dependencies
- `credentials/gmail_credentials.json` - OAuth client ID (you create)
- `credentials/gmail_token.json` - Access token (auto-generated)

## Future Enhancements

- [ ] Fully automated trigger on research agent completion
- [ ] Email digest format (multiple findings in one email)
- [ ] Unsubscribe/preferences management
- [ ] SMS notifications for high-priority findings
- [ ] Slack integration option
