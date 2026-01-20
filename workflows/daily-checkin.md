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
