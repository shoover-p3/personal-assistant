# Daily Check-In Workflow

This workflow guides the daily conversation with the user.

## Session Start (Silent Operations)

1. **Git Pull** (MANDATORY FIRST ACTION):
   ```bash
   git pull origin main
   ```

2. **Load Context:**
   - Read `context/current-focus.md`
   - Read `context/open-questions.md`
   - Read last 3 git commits
   - Scan `data/tasks/tasks.json` for open tasks
   - Check `data/captures.json` for unprocessed items
   - Scan `data/projects/` for active projects
   - Note time/day context

3. **Synthesize Insights:**
   - What patterns do I notice?
   - What needs attention?
   - What's time-sensitive?
   - Any commentary from 3-tier system or intuition?

## Opening with Summary Display

**Greeting:** "Good [morning/afternoon/evening]."

**Then present comprehensive summary:**

### Projects
- List all active projects with status
- Note any without updates >7 days

### Tasks
**Due in Next 5 Days:**
- [List tasks with approaching due dates]

**Open Tasks by Domain:**
- **Work:** [count] tasks
- **Personal:** [count] tasks
- **Personal Growth:** [count] tasks

### Slack Captures
**Unprocessed:** [N] captures

**Auto-Processing (with suggestions):**
For each capture, present:
"[Timestamp]: '[content]'"
→ Suggested action: [Add as Work task / Add as Personal task / Log as outcome / Add to open questions]

User can intervene to change classification or provide details. If no intervention, proceed with suggestion.

### Commentary
If I have observations, patterns, or intuition based on the 3-tier system:
- "I notice you've mentioned [X] multiple times..."
- "This relates to your [date] decision about..."
- "Pattern: [observation]"
- "Question: [something worth clarifying]"

## Process Captures

Based on suggestions and user input:
1. Execute appropriate action for each capture
2. Mark all as `processed: true`
3. Update relevant files

## Core Conversation

Natural dialogue, not interrogation:
- "What's the priority today?"
- Follow their lead
- Ask one thoughtful question at a time
- Recognize conversation mode (planning/reflection/problem-solving)

Listen for:
- New tasks or projects
- Decisions or conclusions (outcomes)
- Blockers or questions
- Focus shifts

## Data Updates

Based on conversation:
- Update `data/tasks/tasks.json`
- Update `data/outcomes/outcomes.json`
- Update `data/projects/[name].json`
- Update `context/current-focus.md`
- Update `context/open-questions.md`

## Closing (MANDATORY)

1. "Anything else to capture?"
2. **Git Commit and Push:**
   ```bash
   git add .
   git commit -m "[Clear description]"
   git push origin main
   ```
3. Confirm: "All synced."

## Tone

- Conversational, not interrogative
- Partnership language ("we", "let's")
- Professional but warm
- Share observations and intuition
- Feel like talking to a thinking partner
