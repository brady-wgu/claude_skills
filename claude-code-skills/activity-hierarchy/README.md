# Activity Hierarchy

A five-level automated activity management system built as Claude Code Skills. Each level reads from the level below, synthesizes the content, performs integrity audits against your task list, and writes a structured entry back to Coda.

```
Raw Notes --> /activity-daily --> Daily entries
                                      |
                        /activity-weekly --> Weekly entries
                                                |
                              /activity-monthly --> Monthly Digests
                                                        |
                                    /activity-quarterly --> Quarterly Reviews
                                                                |
                                          /activity-annual --> Annual Reviews
```

## The Five Skills

### /activity-daily
**Trigger:** "run daily", "run pipeline", "process my notes", "morning briefing"

Paste your raw work notes and this skill does everything:
- Processes notes into a 7-section BLOG (Reviewed Notes, Polished Summary, Executive Bullets, Key Wins, Blockers, Category, Sensitive Items)
- Reads your entire BEAST task list from Coda
- Analyzes every task against your notes: flags overdue tasks, recommends status changes, creates new tasks, marks completed work as done
- Produces a 4-section BEAST briefing (Morning Briefing, Flags and Issues, Recommended Task Updates, Today's Priority List)
- Cross-references your blockers against BEAST to catch untracked issues
- Writes the BLOG entry to Coda and updates your task list (after your confirmation)

### /activity-weekly
**Trigger:** "run weekly", "weekly summary", "weekly digest"

Reads all your Daily entries from the prior work week and produces:
- Week in Summary (narrative arc of the week)
- Wins This Week (deduplicated, grouped by workstream)
- Looking Ahead (priorities for next week based on task due dates and momentum)
- Blockers and Open Items (with lifecycle tracking)
- Full BEAST audit: tasks to close, tasks needing updates, new tasks to create, overdue triage, stale task cleanup, coming week preview
- Integrity checks: cadence compliance, commitment tracking vs last week's plan, workstream balance

### /activity-monthly
**Trigger:** "run monthly", "monthly digest", "monthly summary"

Reads all Daily and Weekly entries from the prior month and produces:
- Month in Summary (how focus evolved week by week)
- Wins This Month (from Weekly digests)
- Looking Ahead (5-7 priorities for next month)
- Blockers (lifecycle report: introduced, resolved, persisting)
- Full BEAST audit with health dashboard (active tasks, overdue %, completion rate)
- Category trend analysis (where your time is actually going)
- Optional: OneNote export reconciliation to catch gaps in your Daily Log

### /activity-quarterly
**Trigger:** "run quarterly", "quarterly review", "Q1/Q2/Q3/Q4 review"

Reads three Monthly Digests and produces:
- Quarter in Summary (strategic narrative)
- Wins This Quarter (most consequential accomplishment highlighted)
- Looking Ahead (initiative-level priorities, not task-level)
- Blockers and Systemic Issues (task-level vs organizational patterns)
- Workstream Health Matrix (per-project: completed, active, added, stalled, trajectory)
- Quarter-long stale task cleanup recommendations

### /activity-annual
**Trigger:** "run annual", "annual review", "year in review"

Reads four Quarterly Reviews and produces:
- Year in Summary (career narrative suitable for self-assessment or performance review)
- Key Accomplishments (grouped by initiative, quantified where possible)
- Looking Ahead (career-level strategic priorities)
- Systemic Observations (recurring patterns, organizational friction points, seasonal trends)
- Year-end BEAST health dashboard (completion rate, task lifespan, hygiene recommendations)

## What Makes This Different from a Simple Rollup

Every level performs **cross-checks** against your task list:
- Blockers in your notes are matched against BEAST tasks. Untracked blockers get flagged.
- "Looking Ahead" items from the prior period are compared against actual activity. Missed commitments get flagged.
- Overdue, stale, and incorrectly-open tasks are surfaced at every level.
- Workstream balance and category distribution are tracked to show where time is going.

## Prerequisites

1. **Claude Code** (desktop app or CLI) with the Coda MCP Connector enabled
2. A **Coda document** with two tables:
   - **Daily Log** table (for BLOG entries at all cadence levels)
   - **To Do List** table (for BEAST task management)
3. Column IDs in the skill files must match your Coda table schema (see Setup)

## Installation

See `docs/SETUP.md` for step-by-step instructions.

**Quick start (if you are Brady and column IDs already match):**
```
cp -r plugin/ ~/.claude/plugins/activity-hierarchy/
```
Restart Claude Code. Type `/activity-daily` to verify.

## Safety

All skills follow a strict 5-constraint Coda Safety Protocol:
1. Hard-coded write targets with read-first verification
2. Zero deletion capability (deletions described for manual execution)
3. Single-doc write scope (your Coda Playground only)
4. All other docs read-only
5. Human review gate before every write (no exceptions)

The Coda MCP Connector operates in Global Admin mode with no permission guardrails. Every write is treated as irreversible. See `references/coda-safety.md` in any skill for the full protocol.

## For Colleagues

To adapt these skills for your own Coda tables:
1. Create a Coda doc with a Daily Log table and a To Do List table
2. Run the column discovery process (see `docs/SETUP.md`)
3. Update the column IDs in `references/coda-safety.md` and each SKILL.md
4. Install the plugin to `~/.claude/plugins/activity-hierarchy/`
5. Start with `/activity-daily` to populate your Daily Log, then enable higher levels as data accumulates

The skills degrade gracefully: if no prior-period digest exists, the closure check is skipped. If no Weekly entries exist, the Monthly skill reads Daily entries directly.
