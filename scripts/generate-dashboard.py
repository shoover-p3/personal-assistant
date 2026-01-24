#!/usr/bin/env python3
"""
Dashboard Generator for Personal Assistant
Generates a static HTML dashboard from tasks, projects, and captures data.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Paths
BASE_DIR = Path(__file__).parent.parent
TASKS_FILE = BASE_DIR / "data" / "tasks" / "tasks.json"
PROJECTS_DIR = BASE_DIR / "data" / "projects"
CAPTURES_FILE = BASE_DIR / "data" / "captures.json"
OUTPUT_FILE = BASE_DIR / "dashboard" / "index.html"


def load_tasks():
    """Load tasks from tasks.json"""
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [t for t in data.get('tasks', []) if t.get('status') == 'open']
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return []


def load_projects():
    """Load all project files"""
    projects = []
    try:
        for project_file in PROJECTS_DIR.glob("*.json"):
            with open(project_file, 'r', encoding='utf-8') as f:
                project = json.load(f)
                if project.get('status') == 'active':
                    projects.append(project)
    except Exception as e:
        print(f"Error loading projects: {e}")
    return projects


def load_captures():
    """Load captures from captures.json"""
    try:
        with open(CAPTURES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('captures', [])
    except Exception as e:
        print(f"Error loading captures: {e}")
        return []


def parse_date(date_str):
    """Parse date string to datetime object"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None


def days_until(date_str):
    """Calculate days until a date"""
    date = parse_date(date_str)
    if not date:
        return None
    delta = date - datetime.now()
    return delta.days


def days_since(date_str):
    """Calculate days since a date"""
    date = parse_date(date_str)
    if not date:
        return None
    delta = datetime.now() - date
    return delta.days


def generate_daily_brief(tasks, projects, captures):
    """Generate intelligent daily brief"""
    insights = []

    # Day of week
    today = datetime.now()
    day = today.strftime("%A, %B %d")
    insights.append(f"Today is {day}.")

    # Tasks due soon
    due_soon = []
    for task in tasks:
        if task.get('due'):
            days_left = days_until(task['due'])
            if days_left is not None and 0 <= days_left <= 5:
                due_soon.append(task)

    if due_soon:
        count = len(due_soon)
        plural = 's' if count > 1 else ''
        insights.append(f"{count} task{plural} due in next 5 days.")

    # Stale projects (no update in 7+ days)
    stale_projects = []
    for project in projects:
        last_updated = project.get('last_updated') or project.get('created')
        if last_updated:
            days = days_since(last_updated)
            if days and days > 7:
                stale_projects.append(project['title'])

    if stale_projects:
        if len(stale_projects) == 1:
            insights.append(f"Stale: {stale_projects[0]} (7+ days without updates).")
        else:
            names = ', '.join(stale_projects[:2])
            if len(stale_projects) > 2:
                names += f", +{len(stale_projects)-2} more"
            insights.append(f"Stale projects: {names}.")

    # Unprocessed captures
    unprocessed = [c for c in captures if not c.get('processed', False)]
    if unprocessed:
        count = len(unprocessed)
        plural = 's' if count > 1 else ''
        insights.append(f"{count} Slack capture{plural} waiting to process.")

    # Domain distribution insight
    domain_counts = defaultdict(int)
    for task in tasks:
        domain_counts[task.get('domain', 'Unknown')] += 1

    if domain_counts:
        max_domain = max(domain_counts, key=domain_counts.get)
        if domain_counts[max_domain] > 5:
            insights.append(f"{domain_counts[max_domain]} {max_domain} tasks open.")

    return " ".join(insights)


def group_tasks_by_domain(tasks):
    """Group tasks by domain"""
    grouped = defaultdict(list)
    for task in tasks:
        domain = task.get('domain', 'Unknown')
        grouped[domain].append(task)
    return grouped


def format_task_html(task):
    """Generate HTML for a single task"""
    due_info = ""
    due_class = ""

    if task.get('due'):
        days_left = days_until(task['due'])
        if days_left is not None:
            if days_left < 0:
                due_info = f'<span class="due-date overdue">Overdue by {abs(days_left)} days</span>'
                due_class = "urgent"
            elif days_left == 0:
                due_info = f'<span class="due-date urgent">Due today</span>'
                due_class = "urgent"
            elif days_left <= 5:
                due_info = f'<span class="due-date warning">Due in {days_left} days</span>'
                due_class = "warning"
            else:
                due_info = f'<span class="due-date">Due {task["due"]}</span>'

    content = task.get('content', '').replace('<', '&lt;').replace('>', '&gt;')

    return f'''
        <div class="task-card {due_class}">
            <p class="task-content">{content}</p>
            {due_info}
        </div>
    '''


def format_project_html(project):
    """Generate HTML for a single project"""
    title = project.get('title', 'Untitled')
    domain = project.get('domain', 'Unknown')
    purpose = project.get('purpose', '')
    last_updated = project.get('last_updated') or project.get('created', '')
    actions = project.get('actions', [])[:2]  # Next 2 actions

    actions_html = ""
    if actions:
        actions_items = "".join([f"<li>{action}</li>" for action in actions])
        actions_html = f'''
            <div class="next-actions">
                <h4>Next Actions:</h4>
                <ul>{actions_items}</ul>
            </div>
        '''

    return f'''
        <div class="project-card">
            <h3>{title}</h3>
            <span class="domain-tag">{domain}</span>
            <p class="purpose">{purpose}</p>
            <p class="last-updated">Updated: {last_updated}</p>
            {actions_html}
        </div>
    '''


def generate_html(tasks, projects, daily_brief):
    """Generate complete HTML dashboard"""

    # Group tasks by domain
    grouped_tasks = group_tasks_by_domain(tasks)
    domains = ['Work', 'Personal', 'Personal Growth']

    # Generate tasks sections
    tasks_html = ""
    for domain in domains:
        domain_tasks = grouped_tasks.get(domain, [])
        if not domain_tasks and domain not in grouped_tasks:
            continue

        count = len(domain_tasks)
        tasks_cards = "".join([format_task_html(task) for task in domain_tasks])

        if not tasks_cards:
            tasks_cards = '<p class="empty-message">No open tasks</p>'

        tasks_html += f'''
            <div class="domain-section">
                <h3>{domain} <span class="count">({count})</span></h3>
                {tasks_cards}
            </div>
        '''

    # Generate projects section
    projects_html = ""
    if projects:
        for project in projects:
            projects_html += format_project_html(project)
    else:
        projects_html = '<p class="empty-message">No active projects</p>'

    # Complete HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>Personal Assistant Dashboard</title>
    <style>
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --text-primary: #c9d1d9;
            --text-secondary: #8b949e;
            --text-tertiary: #6e7681;
            --accent: #58a6ff;
            --urgent: #f85149;
            --warning: #d29922;
            --border: #30363d;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 16px;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .container {{
            width: 100%;
        }}

        h1 {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--text-primary);
        }}

        h2 {{
            font-size: 20px;
            font-weight: 600;
            margin-top: 32px;
            margin-bottom: 16px;
            color: var(--text-primary);
            border-bottom: 1px solid var(--border);
            padding-bottom: 8px;
        }}

        h3 {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 12px;
            color: var(--text-primary);
        }}

        h4 {{
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--text-secondary);
        }}

        .brief {{
            background-color: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 24px;
            font-size: 14px;
            line-height: 1.7;
            color: var(--text-secondary);
        }}

        .domain-section {{
            margin-bottom: 24px;
        }}

        .count {{
            font-size: 14px;
            font-weight: 400;
            color: var(--text-tertiary);
        }}

        .task-card {{
            background-color: var(--bg-secondary);
            border: 1px solid var(--border);
            border-left: 3px solid var(--border);
            border-radius: 6px;
            padding: 12px;
            margin-bottom: 8px;
            transition: border-color 0.2s ease;
        }}

        .task-card.warning {{
            border-left-color: var(--warning);
        }}

        .task-card.urgent {{
            border-left-color: var(--urgent);
        }}

        .task-content {{
            font-size: 14px;
            margin-bottom: 6px;
            color: var(--text-primary);
        }}

        .due-date {{
            font-size: 12px;
            color: var(--text-tertiary);
        }}

        .due-date.warning {{
            color: var(--warning);
            font-weight: 500;
        }}

        .due-date.urgent {{
            color: var(--urgent);
            font-weight: 500;
        }}

        .due-date.overdue {{
            color: var(--urgent);
            font-weight: 600;
        }}

        .project-card {{
            background-color: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 16px;
        }}

        .project-card h3 {{
            margin-bottom: 8px;
        }}

        .domain-tag {{
            display: inline-block;
            font-size: 12px;
            padding: 2px 8px;
            background-color: var(--bg-tertiary);
            color: var(--text-secondary);
            border-radius: 12px;
            margin-bottom: 8px;
        }}

        .purpose {{
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 8px;
            font-style: italic;
        }}

        .last-updated {{
            font-size: 12px;
            color: var(--text-tertiary);
            margin-bottom: 12px;
        }}

        .next-actions {{
            margin-top: 12px;
        }}

        .next-actions ul {{
            list-style: none;
            padding-left: 0;
        }}

        .next-actions li {{
            font-size: 14px;
            padding: 6px 0 6px 16px;
            position: relative;
            color: var(--text-primary);
        }}

        .next-actions li:before {{
            content: "→";
            position: absolute;
            left: 0;
            color: var(--accent);
        }}

        .empty-message {{
            font-size: 14px;
            color: var(--text-tertiary);
            font-style: italic;
            padding: 12px 0;
        }}

        @media (min-width: 768px) {{
            body {{
                padding: 24px;
            }}

            h1 {{
                font-size: 28px;
            }}

            h2 {{
                font-size: 22px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Personal Assistant</h1>

        <div class="brief">
            {daily_brief}
        </div>

        <section class="tasks">
            <h2>Tasks</h2>
            {tasks_html}
        </section>

        <section class="projects">
            <h2>Active Projects</h2>
            {projects_html}
        </section>
    </div>
</body>
</html>'''

    return html


def main():
    """Main execution"""
    print("Loading data...")
    tasks = load_tasks()
    projects = load_projects()
    captures = load_captures()

    print(f"Loaded {len(tasks)} open tasks, {len(projects)} active projects, {len(captures)} captures")

    print("Generating daily brief...")
    daily_brief = generate_daily_brief(tasks, projects, captures)

    print("Generating HTML...")
    html = generate_html(tasks, projects, daily_brief)

    print("Writing output...")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Dashboard generated successfully: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
