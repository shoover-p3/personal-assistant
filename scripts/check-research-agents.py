#!/usr/bin/env python3
"""
Check if research agents are due to run and add notification to captures.
"""

import json
from datetime import datetime, timedelta
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

def check_research_agents():
    """Check all research agents and notify if any are due."""
    repo_root = Path(__file__).parent.parent
    research_agents_dir = repo_root / 'data' / 'research-agents'
    captures_file = repo_root / 'data' / 'captures.json'

    if not research_agents_dir.exists():
        print("No research agents directory found")
        return

    today = datetime.now().date()
    today_str = today.strftime('%Y-%m-%d')

    agents_due = []

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
        next_run_str = schedule.get('next_run')

        if not next_run_str:
            continue

        next_run = datetime.strptime(next_run_str, '%Y-%m-%d').date()

        # If today >= next_run, agent is due
        if today >= next_run:
            agents_due.append({
                'agent_id': config.get('agent_id'),
                'name': config.get('name'),
                'next_run': next_run_str
            })

    if not agents_due:
        print("No research agents due")
        return

    # Load captures and add notification
    captures = load_json(captures_file)

    for agent in agents_due:
        # Check if we already have an unprocessed notification for this agent
        existing = any(
            c.get('content', '').startswith(f"RESEARCH AGENT DUE: {agent['name']}")
            and not c.get('processed', False)
            for c in captures.get('captures', [])
        )

        if existing:
            print(f"Notification already exists for {agent['name']}")
            continue

        # Add capture notification
        capture = {
            'timestamp': datetime.now().isoformat(),
            'type': 'system',
            'domain': None,
            'content': f"RESEARCH AGENT DUE: {agent['name']} (scheduled for {agent['next_run']})",
            'processed': False
        }

        captures['captures'].append(capture)
        print(f"Added notification for {agent['name']}")

    save_json(captures_file, captures)

if __name__ == '__main__':
    check_research_agents()
