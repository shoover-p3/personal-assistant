"""
Research Findings Email Automation
Sends research agent findings via Gmail API with HTML formatting
"""

import os
import json
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
import markdown2

# Google API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Run: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client markdown2")
    exit(1)

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Email configuration
SENDER_EMAIL = "shane.b.hoover@gmail.com"
RECIPIENTS = ["shane.b.hoover@gmail.com", "buddyjbush@gmail.com"]

def get_gmail_credentials():
    """Authenticate and return Gmail API credentials"""
    creds = None
    token_path = Path(__file__).parent.parent / "credentials" / "gmail_token.json"
    credentials_path = Path(__file__).parent.parent / "credentials" / "gmail_credentials.json"

    # Token file stores user's access and refresh tokens
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                print(f"ERROR: Gmail credentials not found at {credentials_path}")
                print("Please follow setup instructions in scripts/GMAIL_SETUP.md")
                exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        token_path.parent.mkdir(exist_ok=True)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds

def markdown_to_html(md_content):
    """Convert markdown to styled HTML"""
    # Convert markdown to HTML
    html_body = markdown2.markdown(md_content, extras=["tables", "fenced-code-blocks"])

    # Wrap in styled HTML template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #34495e;
                margin-top: 30px;
                border-bottom: 2px solid #ecf0f1;
                padding-bottom: 8px;
            }}
            h3 {{
                color: #7f8c8d;
                margin-top: 20px;
            }}
            a {{
                color: #3498db;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            strong {{
                color: #e74c3c;
            }}
            code {{
                background-color: #f8f9fa;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }}
            ul {{
                padding-left: 20px;
            }}
            li {{
                margin: 8px 0;
            }}
            hr {{
                border: none;
                border-top: 1px solid #ecf0f1;
                margin: 30px 0;
            }}
            .footer {{
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ecf0f1;
                color: #7f8c8d;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            {html_body}
            <div class="footer">
                <p><em>Automated research digest from Personal Assistant System</em></p>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

def create_email_with_attachment(sender, recipients, subject, html_body, attachment_path):
    """Create email message with HTML body and attachment"""
    message = MIMEMultipart('alternative')
    message['From'] = sender
    message['To'] = ', '.join(recipients)
    message['Subject'] = subject

    # Attach HTML body
    html_part = MIMEText(html_body, 'html')
    message.attach(html_part)

    # Attach file
    if attachment_path and Path(attachment_path).exists():
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {Path(attachment_path).name}'
        )
        message.attach(part)

    # Encode message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_email(creds, sender, recipients, subject, html_body, attachment_path=None):
    """Send email via Gmail API"""
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = create_email_with_attachment(sender, recipients, subject, html_body, attachment_path)

        result = service.users().messages().send(userId='me', body=message).execute()
        print(f"[OK] Email sent successfully (Message ID: {result['id']})")
        print(f"  Recipients: {', '.join(recipients)}")
        return True

    except HttpError as error:
        print(f"[ERROR] Gmail API error: {error}")
        return False
    except Exception as error:
        print(f"[ERROR] Error sending email: {error}")
        return False

def send_research_findings(research_agent_id):
    """Send research findings for a specific agent"""
    # Load research agent config
    config_path = Path(__file__).parent.parent / "data" / "research-agents" / research_agent_id / "config.json"

    if not config_path.exists():
        print(f"[ERROR] Research agent config not found: {config_path}")
        return False

    with open(config_path, 'r') as f:
        config = json.load(f)

    # Load findings
    findings_path = Path(__file__).parent.parent / config['findings_file']

    if not findings_path.exists():
        print(f"[ERROR] Findings file not found: {findings_path}")
        return False

    with open(findings_path, 'r', encoding='utf-8') as f:
        findings_content = f.read()

    # Get Gmail credentials
    print("Authenticating with Gmail...")
    creds = get_gmail_credentials()

    # Convert markdown to HTML
    print("Converting findings to HTML...")
    html_body = markdown_to_html(findings_content)

    # Create subject line
    run_date = config['schedule']['last_run']
    subject = f"{config['name']} - Update {run_date}"

    # Send email
    print(f"Sending email: {subject}")
    success = send_email(
        creds=creds,
        sender=SENDER_EMAIL,
        recipients=RECIPIENTS,
        subject=subject,
        html_body=html_body,
        attachment_path=str(findings_path)
    )

    return success

def main():
    """Main entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python send_research_email.py <research_agent_id>")
        print("Example: python send_research_email.py research_ckd_treatment")
        sys.exit(1)

    research_agent_id = sys.argv[1]
    success = send_research_findings(research_agent_id)

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
