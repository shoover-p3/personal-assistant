# Quick Reference Guide

This document contains frequently-needed guidance that's not essential for every session but more detailed than CLAUDE.md basics. For comprehensive edge cases and deep dives, see `docs/personal-assistant-mandate.md`.

---

## Classification Decision Trees

### Full Classification Logic

```
Does it require future action?
├─ YES: Is it a single step?
│  ├─ YES: TASK
│  └─ NO: Does it have multiple steps or span multiple sessions?
│     ├─ YES: PROJECT
│     └─ MAYBE: Ask user
└─ NO: Does it record something decided or learned?
   ├─ YES: OUTCOME
   └─ NO: Is it context for ongoing work?
      ├─ YES: NOTE (context files)
      └─ UNCERTAIN: Ask user "This could be a task or note. Which feels right?"
```

### Task vs. Project Decision

**Create TASK when:**
- Single action, clear completion
- Can be done in one session
- Doesn't require coordination of multiple pieces

**Create PROJECT when:**
- 3+ related tasks
- Work spanning >1 week
- Complex problem needing decomposition
- Recurring reference to same effort

**Ask user when:**
- 2 related tasks (might become project later)
- Unclear if work will expand
- User seems to be thinking through something

### Outcome vs. Task

**Common confusion:**
- User says: "I decided to use Python for this"
  - OUTCOME: "Decided to use Python" (decision made)
  - TASK: "Set up Python environment" (action needed)

**If both exist, create both:**
1. First log the OUTCOME (decision)
2. Then ask: "Should I create a task to implement this?"

---

## Capture Processing

### Detailed Workflow

For each item in captures.json where processed: false:

**Step 1: Present Clearly**
```
"From your Slack capture [timestamp]:
'[exact content]'

Should I add this as a task?"
```

**Step 2: Determine Classification**
Use decision tree above. If genuinely uncertain, ask ONE question:
- "Is this a task or just context to remember?"
- "Should this be its own project or part of [existing project]?"
- "Is this a decision you made or something you need to do?"

**Step 3: Execute Action**

For TASK:
```json
{
  "id": "task_XXX",
  "domain": "[infer or ask]",
  "content": "[cleaned up version]",
  "created": "[today]",
  "status": "open"
}
```

For OUTCOME:
```json
{
  "date": "[today]",
  "domain": "[infer or ask]",
  "content": "[what was decided/learned]"
}
```

For NOTE:
- Add to open-questions.md if it's a question
- Add to relevant project notes if project-specific
- Add to current-focus.md if it affects focus

For PROJECT:
- Create new project file
- Ask user for purpose if not obvious
- Link any related existing tasks

**Step 4: Mark Processed**
Update the capture in captures.json:
```json
{
  "timestamp": "...",
  "type": "raw",
  "domain": "...",
  "content": "...",
  "processed": true
}
```

**Step 5: Commit**
If processing multiple captures, batch commit:
"Process 5 Slack captures: 3 tasks, 1 outcome, 1 note"

### Batch Processing Strategy

**If >5 unprocessed captures:**
- Ask: "I see [N] captures. Go through all or just recent?"
- If "just recent": Start with most recent 5
- If "all": Process chronologically (oldest first)

**If capture is >3 days old:**
- Note age: "This is from [date], still relevant?"
- If user says no: Mark processed: true, don't create item

**If capture is time-sensitive:**
- Meeting, deadline, appointment
- Flag immediately: "This looks time-sensitive: [content]"
- Priority process regardless of batch

---

## Full Data Specifications

### Task Attributes

**Required:**
- `id`: Unique identifier (task_001, task_002, etc.)
- `domain`: "Work" | "Personal" | "Personal Growth"
- `content`: Clear, actionable description
- `created`: ISO date (YYYY-MM-DD)
- `status`: "open" | "completed" | "blocked" | "deferred" | "delegated"

**Optional:**
- `due`: ISO date
- `project_id`: Link to parent project
- `priority`: "high" | "medium" | "low"
- `context`: Additional notes
- `completed`: Date completed (if status=completed)
- `agent_id`: If delegated to agent

**Task Status Meanings:**
- **open**: Active, can work on now
- **completed**: Done (preserve in file)
- **blocked**: Waiting on external dependency
- **deferred**: Intentionally postponed
- **delegated**: Assigned to autonomous agent

### Project Structure

**Required:**
- `id`: proj_[descriptor] (e.g., proj_flow_trade_system)
- `domain`: "Work" | "Personal" | "Personal Growth"
- `title`: Clear project name
- `purpose`: What this accomplishes
- `status`: "active" | "paused" | "completed" | "archived"
- `created`: ISO date
- `last_updated`: ISO date (update whenever touched)

**Recommended:**
- `actions`: Array of action items
- `outcomes`: Array of key decisions/learnings
- `open_questions`: Array of unresolved questions
- `notes`: Ongoing notes and challenges

**Optional:**
- `target_completion`: ISO date
- `links`: Object with arrays of related task IDs, outcome IDs, etc.

**Project Lifecycle:**
- **active**: Regular work happening
- **paused**: Temporarily set aside (note why in notes field)
- **completed**: Finished (preserve for reference)
- **archived**: Old/no longer relevant

### Outcome Attributes

**Required:**
- `date`: ISO date when decided/learned
- `domain`: "Work" | "Personal" | "Personal Growth"
- `content`: What was decided or learned

**Optional:**
- `context`: Why/how this came about
- `tags`: Array for categorization
- `project_id`: Link to relevant project

---

## Agent Management

### Creating Autonomous Agents

**When user says: "Handle this" or "Take care of [task]"**

**Step 1: Assess Suitability**

✅ **Good for agents:**
- Well-defined task with clear completion
- Clear success criteria
- Doesn't require constant user judgment
- Research, data gathering, code writing, document creation
- Data processing, file organization

❌ **Not for agents:**
- Requires subjective decisions
- Ambiguous requirements
- Needs real-time user input throughout
- Sensitive decisions

**Step 2: Create Agent File**

Location: `data/agents/agent_XXX.json`

```json
{
  "agent_id": "agent_001",
  "task_id": "task_123",
  "created": "2026-01-24T12:00:00Z",
  "status": "active",
  "type": "primary",
  "objective": "Clear description",
  "approach": "High-level strategy",
  "sub_agents": [],
  "progress": [
    {
      "timestamp": "2026-01-24T12:15:00Z",
      "update": "Started work",
      "status": "in_progress"
    }
  ],
  "blockers": [],
  "completion": null
}
```

**Step 3: Update Task**
- Change status to "delegated"
- Add agent_id to task

**Step 4: Begin Work**
Agent operates autonomously. Only surface to user for:
- Clarifying questions
- Blockers requiring user decision
- Completion

### Sub-Agent Creation

**Primary agent can spawn sub-agents when:**
- Distinct sub-task identified
- Parallel work would be more efficient
- Specialized capability needed

**Sub-agent structure:**
```json
{
  "agent_id": "agent_002",
  "parent_agent": "agent_001",
  "task_id": "task_123",
  "created": "2026-01-24T12:30:00Z",
  "status": "active",
  "type": "sub_agent",
  "objective": "Specific sub-task",
  "deliverable": "What this produces",
  "progress": [],
  "completion": null
}
```

### Agent Completion

**When agent completes:**

1. Finalize agent file (status: completed, completion timestamp)
2. Update task (status: completed, completed date)
3. Create outcome if significant learning
4. Move agent file to `data/agents/completed/`
5. Report to user:
   ```
   "Completed [task]: [brief summary]
   - [Key result 1]
   - [Key result 2]
   [Location of deliverables]
   
   Should I mark the task complete?"
   ```

### During Check-ins

If agents are active, briefly mention:
- "Agent working on [task] - [status]"
- Only elaborate if user asks
- Flag any blocked or needing input

---

## Research Agents

### Creating Research Agents

**When user says: "Create research agent for [topic]"**

**Step 1: Create Directory Structure**
```
data/research-agents/[agent-name]/
├── config.json
├── mandate.md
└── findings.json
```

**Step 2: Build Config with User**

Ask necessary questions:
- "How often should it run? (e.g., every 3 days, weekly)"
- "What are the key topics to monitor?"
- "Any specific trusted sources?"
- "What should it avoid?"

Create `config.json`:
```json
{
  "agent_id": "research_ckd_treatment",
  "name": "CKD Treatment Research Monitor",
  "created": "2026-01-24",
  "status": "active",
  "schedule": {
    "frequency": "every_3_days",
    "last_run": "2026-01-24T10:00:00Z",
    "next_run": "2026-01-27T10:00:00Z"
  },
  "topics": [
    "chronic kidney disease treatment",
    "CKD protocols",
    "CKD clinical trials"
  ],
  "sources": {
    "trusted_domains": [
      "pubmed.ncbi.nlm.nih.gov",
      "nejm.org"
    ],
    "trusted_substacks": [],
    "rss_feeds": [],
    "exclude_domains": []
  },
  "filters": {
    "avoid_ai_generated": true,
    "minimum_quality_signals": [
      "peer_reviewed",
      "clinical_trial"
    ],
    "date_range": "last_30_days",
    "language": "english"
  },
  "mandate_file": "data/research-agents/research_ckd_treatment/mandate.md"
}
```

**Step 3: Create Mandate File**

Help user define `mandate.md`:
- Mission statement
- What to look for
- What to ignore
- Quality criteria
- Source preferences
- Categorization system
- Special notes

**Step 4: Initialize Findings File**

Create `findings.json`:
```json
{
  "findings": [],
  "deduplication_index": {
    "url_hashes": [],
    "title_fingerprints": [],
    "content_signatures": []
  }
}
```

### During Check-ins

**If research agent has new findings:**
```
"[Agent Name] found [N] new items since last run:
- [Category]: [Title] (High relevance - peer-reviewed)
- [Category]: [Title]

Want to review now or add to reading list?"
```

**On demand:**
- "Show me recent [topic] research" → Display findings
- "Status of research agents" → List all agents with last run times

---

## Cross-Reference Intelligence

### How It Works

Maintain awareness of connections:
- Similar problems across projects
- Outcomes building on each other
- Questions answered by later work
- Patterns across domains

**Storage:** `data/cross-reference-index.json`

```json
{
  "concepts": {
    "lookahead_bias": {
      "outcomes": ["outcome_015", "outcome_032"],
      "projects": ["proj_flow_trade_system"]
    },
    "rebalancing_frequency": {
      "outcomes": ["outcome_015", "outcome_021"],
      "projects": ["proj_flow_trade_system", "proj_vixvol"]
    }
  },
  "instruments": {
    "treasury_futures": {
      "tasks": ["task_120"],
      "projects": ["proj_flow_trade_system"]
    }
  }
}
```

### When to Surface

**Always surface:**
- Direct contradictions: "This conflicts with your [date] decision"
- Solved problems: "You addressed this in [project] using [approach]"
- Repeated patterns: "This is the 3rd time [pattern]"

**Proactively suggest:**
- Related past work when starting project
- Alternative approaches from other domains
- Methodology that worked elsewhere

**Format:**
```
"Note: This relates to your [date] work on [project].
You concluded: [outcome]
Relevant because: [why it matters now]
Want me to pull up details?"
```

### Examples

**Preventing Re-work:**
```
User: "I need to figure out Treasury futures rollover"
Assistant: "You tackled rollover logic in Flow Trade System last month.
You decided to [approach]. Use the same here?"
```

**Catching Contradictions:**
```
User: "Let's test with daily rebalancing"
Assistant: "Quick note: In January you concluded daily rebalancing 
introduces lookahead bias for Treasury futures. Has something changed?"
```

**Pattern Recognition:**
```
During check-in: "I notice you've encountered 'entry signal quality' 
questions in three strategies. Worth developing a standard framework?"
```

---

## Outcome Synthesis

### What It Is

Periodically analyze accumulated outcomes to extract higher-level insights, decision-making principles, and frameworks.

### When to Synthesize

**Monthly (automatic):**
- During monthly review
- Analyze outcomes from past month
- Identify patterns or reinforced principles

**On-Demand:**
- User asks: "What have I learned about [topic]?"
- When starting similar project
- During major decisions

**Threshold-Based:**
- After 5+ outcomes on similar topic
- When clear pattern emerges (3+ similar approaches)
- When contradiction appears

### Synthesis Format

Create in `data/synthesis/frameworks/[topic].md`:

```markdown
## [Topic] Framework
**Extracted from:** [N] outcomes between [dates]

**Your Principles:**
1. [Principle 1]
2. [Principle 2]

**Decision Criteria:**
- [Criterion 1]
- [Criterion 2]

**Open Questions:**
- [Question still unresolved]

**Confidence:** [High|Medium|Low]
```

### Integration with Work

**During decisions:**
```
User: "Should I use daily or monthly rebalancing?"
Assistant: "Based on your past work (5 similar decisions), you prefer 
month-end for Treasury futures to avoid lookahead bias. Apply that here?"
```

**During reviews:**
```
Monthly review includes: "This month you made 3 methodology decisions.
They reinforce your principle: [principle]."
```

---

## Periodic Reviews

### Weekly Review (Fridays)

**Trigger:** Friday during check-in, or user requests

**Contents:**
1. **Completed This Week:**
   - Tasks marked complete
   - Key outcomes/decisions
   - Projects that progressed

2. **Active Focus:**
   - Current focus status
   - Open tasks by domain
   - Active projects summary

3. **Attention Needed:**
   - Stale tasks (>14 days)
   - Unresolved questions (>7 days)
   - Upcoming due dates (next week)

4. **Patterns Observed:**
   - Which domains got attention
   - Recurring blockers
   - Progress on long-term work

**Format:** Conversational summary, not report. Focus on insights.

**Close:** "What should we focus on next week?"

### Monthly Review (First of Month)

**Trigger:** First session of new month, or user requests

**Contents:**
1. **Month in Review:**
   - Major accomplishments
   - Significant decisions/outcomes
   - Projects completed or advanced

2. **Active Portfolio:**
   - All active projects with status
   - Open questions needing resolution
   - Tasks carried forward (why?)

3. **Patterns & Insights:**
   - Domain balance
   - Common blockers
   - Completion trends
   - Growth areas

4. **Synthesis:**
   - New frameworks identified (from Outcome Synthesis)
   - Existing frameworks reinforced
   - Areas needing frameworks

5. **Looking Ahead:**
   - Next month focus?
   - Projects to pause/archive?
   - New initiatives?

**Format:** More comprehensive than weekly, still conversational.

### Stale Item Follow-ups

**During regular check-ins, surface:**

**Tasks:**
- Open >30 days: "Still relevant?"
- Open >60 days: "Should we close, defer, or break down?"
- Repeatedly deferred (>3 times): "Is something blocking it?"

**Questions:**
- Unresolved >14 days: "Making progress?"
- Unresolved >30 days: "Should we make this a task/project?"

**Projects:**
- No updates >21 days: "Still active?"
- No updates >60 days: "Pause or archive?"

**Approach:**
- Raise 1-2 stale items per check-in max
- Prioritize by current-focus context
- Frame as reminder, not criticism
- Accept user's decision without judgment

---

## Common Edge Cases

### Duplicate Detection

**When new item very similar to existing:**

1. Identify: "This looks similar to [existing]"
2. Show both: "Existing: [X], New: [Y]"
3. Ask: "Same thing or different?"
4. Action:
   - Same: Update existing, mark capture processed
   - Different: Add new, explain distinction

### Missing Context

**When user references something not in system:**

1. Acknowledge gap: "I don't see [X] in my records. Tell me more?"
2. If should exist: "Should this have been captured? Add it now."
3. Capture appropriately
4. If complex: Consider project file

### Conflicting Information

**New info contradicts existing:**

1. Task contradicts focus: "This conflicts with your current focus. Priority shift?"
2. New outcome contradicts old: "This supersedes your earlier decision, right?"
3. Duplicate with variations: "Similar to existing task. Same or different?"

**Rule:** Surface conflicts respectfully, don't assume which is correct.

### Circular Dependencies

**Task A blocks Task B, which blocks Task A:**

1. Recognize circle
2. Surface: "These block each other. Which needs to happen first?"
3. Help break cycle
4. Update statuses

### Scope Creep

**Project keeps expanding:**

1. Observe: "This has grown from [X] to [Y, Z, ...]"
2. Ask: "Split into multiple projects?"
3. Help define boundaries
4. Create sub-projects if needed

---

**For comprehensive edge cases, scaling considerations, and deep dives on any feature, see `docs/personal-assistant-mandate.md`.**
