#!/usr/bin/env python3
"""
Check research agents and send emails for any runs that haven't been emailed yet.
"""

import json
import subprocess
from pathlib import Path

def load_json(file_path):
    """Load JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(file_path, data):
    """Save JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def check_and_send_emails():
    """Check all research agents and send emails for unsent runs."""
    repo_root = Path(__file__).parent.parent
    research_agents_dir = repo_root / 'data' / 'research-agents'
    email_script = repo_root / 'scripts' / 'send_research_email.py'

    if not research_agents_dir.exists():
        print("No research agents directory found")
        return False

    any_sent = False

    # Check each research agent
    for agent_dir in research_agents_dir.iterdir():
        if not agent_dir.is_dir():
            continue

        config_file = agent_dir / 'config.json'
        if not config_file.exists():
            continue

        config = load_json(config_file)

        if config.get('status') != 'active':
            continue

        schedule = config.get('schedule', {})
        last_run = schedule.get('last_run')
        email_sent_for_run = schedule.get('email_sent_for_run')

        # If last_run exists but email hasn't been sent for it
        if last_run and last_run != email_sent_for_run:
            agent_id = config.get('agent_id')
            agent_name = config.get('name')

            print(f"Sending email for {agent_name} (run: {last_run})")

            # Run email script
            try:
                result = subprocess.run(
                    ['python', str(email_script), agent_id],
                    cwd=str(repo_root),
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                if result.returncode == 0:
                    print(f"  ✓ Email sent successfully")
                    print(result.stdout)

                    # Update config to mark email as sent
                    schedule['email_sent_for_run'] = last_run
                    save_json(config_file, config)
                    any_sent = True
                else:
                    print(f"  ✗ Email send failed")
                    print(result.stderr)

            except subprocess.TimeoutExpired:
                print(f"  ✗ Email send timed out")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        else:
            print(f"{config.get('name')}: No pending emails")

    return any_sent

if __name__ == '__main__':
    import sys

    emails_sent = check_and_send_emails()
    sys.exit(0 if not emails_sent else 0)  # Always exit 0 for workflow
