# Daily Check-In Workflow

This workflow guides the daily conversation with the user.

## Opening

"Good [morning/afternoon/evening]. What's on your mind today?"

## Context Review

Before asking questions, review:
- `context/current-focus.md` - What was the user working on?
- `context/open-questions.md` - Any unresolved items to follow up on?

If there are open questions from previous sessions, bring them up:
- "Last time you mentioned [X]. What happened with that?"

## Process Slack Captures

Check `data/captures.json` for unprocessed captures from Slack:

If there are captures:
1. List them: "I found [N] captures from Slack: [list them]"
2. For each capture:
   - **If type is "raw"** (unstructured message): Review with user to determine classification
     - Ask: "This looks like a [task/note/outcome]. Should I add it to [tasks/open-questions/outcomes]?"
     - Clarify domain if needed (Work, Personal, Personal Growth)
   - **If TASK**: Add to `data/tasks/tasks.json`
   - **If OUTCOME**: Add to `data/outcomes/outcomes.json`
   - **If NOTE**: Add to `context/open-questions.md` or appropriate context file
   - **If PROJECT**: Discuss with user about creating a project
3. Mark captures as processed (set `processed: true`)
4. Consider: Should captures.json be cleaned periodically? Or keep processed ones for history?

If no captures: Continue to core questions.

## Core Questions

Ask these in a conversational way (not like a form):

1. **What are you working on today?**
   - Listen for: New projects? Continuing existing work? One-off tasks?
   - Clarify: "Is this part of [existing project] or something new?"

2. **Any decisions or conclusions recently?**
   - Listen for: Outcomes to log
   - Prompt: "Should we capture that as an outcome?"

3. **Anything blocking you or unclear?**
   - Listen for: Open questions to track
   - Add to `context/open-questions.md`

4. **What's your current focus?**
   - Update `context/current-focus.md` with what matters today/this week

## Data Updates

Based on the conversation:
- Add new tasks to `data/tasks/tasks.json`
- Create new projects in `data/projects/` if needed
- Log outcomes to `data/outcomes/outcomes.json`
- Update current focus and open questions

## Closing

"Anything else you want to capture?"

Then: commit and push all changes.

## Tone

Keep it conversational, not interrogative. This should feel like talking to a thinking partner, not filling out a form.
