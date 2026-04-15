# Activity Hierarchy: Setup Guide

## Prerequisites

- **Claude Code** (desktop app or CLI), version with skill/plugin support
- **Coda MCP Connector** enabled in your Claude Code configuration
- A **Coda document** with two tables matching the expected schema (see below)

## Step 1: Verify Coda MCP Connector

Open a Claude Code session and try:
```
Read a few rows from my Coda table
```

If Claude can access your Coda tables via MCP, you are ready. If not, enable the Coda MCP Connector in your Claude Code settings.

## Step 2: Verify Your Coda Tables

Your Coda document needs two tables:

### Daily Log Table
Used to store BLOG entries, weekly digests, monthly digests, quarterly reviews, and annual reviews.

Required columns:
| Column Name | Type | Purpose |
|---|---|---|
| Date | Date | Entry date |
| Reviewed Notes | Canvas | Full narrative content (Section 1 for daily, Summary for higher levels) |
| Polished Summary | Text | Condensed professional summary |
| Executive Bullets | Text | Structured briefing or "Looking Ahead" section |
| Key Wins | Text | Wins and accomplishments |
| Blockers | Text | Blockers and open items |
| Category | Select | Workstream category |
| Entry Type | Select | "Daily", "Weekly", "Monthly Digest", "Quarterly Review", "Annual Review" |
| Status | Select | "Draft" or "Published" |

### To Do List (BEAST) Table
Used for task management and cross-referencing.

Required columns:
| Column Name | Type | Purpose |
|---|---|---|
| Task ID | Text | Unique ID (format: BEAST-XXXX) |
| Name | Text | Task description |
| Status | Select | "Not started", "In progress", "Done", "Blocked" |
| Priority | Select | "High", "Medium", "Low" |
| Due Date | Date | Target completion date |
| Type | Select | "Action", "Meeting", "Research", "Deliverable", "Admin" |
| Project | Select | Workstream/project name |
| Effort | Select | "30 min", "Half day", "Full day", "Multi-day" |
| Notes | Text | Progress notes with dated entries |
| Link | Link | Reference URL (optional) |

## Step 3: Discover Your Column IDs

If you are Brady and using Brady's Coda Playground (doc ID dHXfr0V468), the column IDs are already hard-coded in the skills. Skip to Step 4.

For everyone else, you need to find your column IDs:

1. Open a Claude Code session with the Coda MCP Connector
2. Ask Claude to read your tables and list the column IDs:
   ```
   Read the schema of my Daily Log table at coda://docs/YOUR_DOC_ID/tables/YOUR_TABLE_ID
   ```
3. Update the column IDs in two places for each skill:
   - `references/coda-safety.md` (the hard-coded URI and column ID tables)
   - The SKILL.md itself (the CODA SCHEMA REFERENCE section and any inline column IDs in write payloads)

## Step 4: Add Entry Type Select Options

Your Daily Log table's Entry Type column needs these options:
- Daily
- Weekly
- Monthly Digest
- Quarterly Review
- Annual Review

If any are missing, add them manually in Coda before running the corresponding skill.

## Step 5: Install the Plugin

Copy the plugin directory to your Claude Code plugins folder:

**Windows:**
```
xcopy /E /I "plugin" "%USERPROFILE%\.claude\plugins\activity-hierarchy"
```

**Mac/Linux:**
```
cp -r plugin/ ~/.claude/plugins/activity-hierarchy/
```

Verify the installed structure looks like this:
```
~/.claude/plugins/activity-hierarchy/
  .claude-plugin/
    plugin.json
  skills/
    activity-daily/
      SKILL.md
      references/
        coda-safety.md
        field-standards.md
        integrity-checks.md
    activity-weekly/
      SKILL.md
      references/
        coda-safety.md
        integrity-checks.md
    activity-monthly/
      SKILL.md
      references/
        coda-safety.md
        integrity-checks.md
        monthly-reconciliation.md
    activity-quarterly/
      SKILL.md
      references/
        coda-safety.md
        integrity-checks.md
    activity-annual/
      SKILL.md
      references/
        coda-safety.md
        integrity-checks.md
```

**IMPORTANT:** The `.claude-plugin/` directory must be exactly ONE level deep. Do NOT nest it as `.claude-plugin/.claude-plugin/` or the plugin will not be discovered.

## Step 6: Verify Installation

1. **Close all Claude Code sessions** (the plugin is loaded at session start)
2. Open a new Claude Code session
3. Type `/activity-daily` and verify the skill is recognized
4. As a quick test, paste a short note like "Worked on project planning today" and confirm the skill processes it

## Step 7: First Real Run

Paste your actual daily work notes and say "run daily" or use `/activity-daily`. You should see:
- A 7-section BLOG entry
- A 4-section BEAST analysis (Morning Briefing, Flags, Recommended Updates, Priority List)
- A write confirmation request

Say "yes" to write to Coda, or "no" to keep the report without writing.

## Troubleshooting

### Skills not appearing after installation
- Verify `.claude-plugin/plugin.json` exists at the correct path (one level only)
- Restart Claude Code completely (close and reopen)
- Check that the `skills/` directory is at the same level as `.claude-plugin/`

### BEAST processing not running
- The skill MUST call `table_rows_read` on the BEAST table
- If you only see BLOG output with no task analysis, the MCP call may have failed
- Verify the BEAST table URI in `references/coda-safety.md` matches your actual table

### Write failures
- Ensure your Coda MCP Connector has write access to the target document
- Verify column IDs match your table schema
- Check that select column values (Status, Category, Entry Type) match exactly

### "No data found" for weekly/monthly/quarterly/annual
- These skills read from the Daily Log, not raw notes
- You need Daily entries before running Weekly, Weekly+Daily before Monthly, etc.
- The hierarchy builds progressively: start with daily, let data accumulate
