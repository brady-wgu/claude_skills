---
name: activity-weekly
model: sonnet
effort: medium
description: >
  Generate Brady's weekly activity digest. ALWAYS use this skill when the user
  says "run weekly", "run my weekly", "weekly summary", "weekly digest",
  "weekly review", "summarize last week", or "what happened last week".
  Reads all Daily entries from the prior work week plus the live BEAST task list
  from Coda via MCP, generates a four-section weekly summary with integrity
  checks, and writes a Weekly entry to the Daily Log after human review.
---

# Activity Weekly

Generates a weekly digest by synthesizing all Daily entries from the prior work week, cross-referencing against the BEAST task list, performing a full To Do List audit, and writing a Weekly entry to the Coda Daily Log.

**THIS SKILL MUST READ AND ANALYZE THE FULL BEAST TABLE.** The BEAST task audit is not optional. Every weekly review includes a complete assessment of task health: overdue tasks, stale tasks, tasks that should be closed, tasks missing from blockers, and tasks due in the coming week.

---

## Recommended Model

Run with **Sonnet** at **medium effort**.

---

## AUTHOR CONTEXT

Brady Redfearn is a Senior Strategist in Program Development at Western Governors University (WGU).

Common acronyms: WGU, UPL, PD, LR, SDP, JFT, PES, BEAST, BLOG

---

## CODA SAFETY PROTOCOL

Read `references/coda-safety.md` for the full 5-constraint safety protocol and 7-step Write Safety Protocol. All constraints apply to this skill. No writes without explicit user confirmation.

---

## CODA SCHEMA REFERENCE

### Daily Log Table
- URI: `coda://docs/dHXfr0V468/tables/grid-ty2WGfh4qa`
- Columns: Date (`c-oiaBDBstH1`), Reviewed Notes (`c-DXM4h2B28G` canvas), Polished Summary (`c-FIWz6AEhwd`), Executive Bullets (`c-WSCAvrHbnz`), Key Wins (`c-QuKWx0lwGp`), Blockers (`c-bT-C79ocGH`), Category (`c-CA6Nwa3A2N` select), Status (`c-pR0VmtQ5AV` select), Entry Type (`c-7IZ-UJNjXG` select)

### BEAST Table
- URI: `coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x`
- Read all rows with `rowLimit: 100` + pagination. Extract `.name` from select refs, `.input` from dates.

---

## EXECUTION FLOW

### Step 1: Determine Target Week

Identify the prior complete work week (Monday through Friday). If today is Monday, the target is last week. If the user specifies a date range, use that instead.

### Step 2: Read Daily Entries for Target Week (internal, no output)

Call `table_rows_read` on the Daily Log:
```
table_rows_read(
  uri: "coda://docs/dHXfr0V468/tables/grid-ty2WGfh4qa",
  rowLimit: 100
)
```

Filter results in-skill: keep only rows where:
- Entry Type `.name` = "Daily"
- Date falls within the target Monday-Friday range

Extract text content from Slate JSON fields by traversing `root.children` and collecting `.text` values from each child's inner children array. Bold text has `"bold": true`. Bulleted items have `"style": "BulletedList"`.

Also check: does a prior Weekly entry exist (Entry Type = "Weekly" for the week before the target)? If yes, extract its Executive Bullets column (the "Looking Ahead" section) for the commitment tracking check.

### Step 3: Read BEAST Table (internal, no output)

Read all BEAST rows via MCP (same pagination pattern as activity-daily). Build the full task list with Task ID to Row ID mapping.

### Step 4: Generate Weekly Digest (internal, no output)

Produce four sections:

**Section 1: Week in Summary**
Narrative synthesis of the week. Include:
- The dominant workstream(s) and how focus shifted across the days
- Key meetings, decisions, or milestones
- Connections between daily activities that form a larger arc
- Reference specific Daily entries by date when relevant
- Professional tone, first person, no em dashes, no filler

**Section 2: Wins This Week**
Aggregate Key Wins from all Daily entries for the week. Deduplicate (same win mentioned on multiple days = one entry). Group by workstream/project where natural. One sentence per win.

If no wins across the entire week: `None logged.`

**Section 3: Looking Ahead**
Top 3 to 5 priorities for the coming week based on:
- BEAST tasks due in the coming week (by Due Date)
- High-priority BEAST tasks regardless of due date
- Momentum items from the current week's Daily entries (especially "Looking Ahead" sub-sections from Polished Summaries)
- Any unresolved blockers that need attention

Split into:
- **Next Week Priorities** (consequential items with rationale)
- **Continuing Background Tasks** (ongoing, lower-urgency items)

**Section 4: Blockers and Open Items**
Aggregate Blockers from all Daily entries for the week. Deduplicate. For each:
- The blocker text
- First appearance (which day)
- Current status: Resolved (if later Daily entries show resolution), Ongoing, or New

Flag any blocker that appeared on Monday and is still present on Friday with no progress note.

### Step 5: Run Integrity Checks (internal, no output)

See `references/integrity-checks.md` for full check definitions. Run these checks:

1. **Blocker Cross-Reference (Check 1):** Every blocker from all Daily entries matched against BEAST. Flag untracked blockers.
2. **Overdue Task Flag (Check 2):** All BEAST tasks past due date and not Done.
3. **Cadence Gap Detection (Check 3):** Every workday (Mon-Fri) in the target week should have a Daily entry. Flag missing days.
4. **Prior-Period Closure (Check 4):** If a prior Weekly exists, compare its "Looking Ahead" against this week's actual activity. Calculate commitment completion rate.
5. **Stale Task Detection (Check 8):** BEAST tasks with no Notes update in 14 days.

**Workstream Balance Scoring:**
Count Daily entries per Category for the week. Calculate percentages. Flag if >60% concentration in a single category.

**Blocker Age Tracking:**
For each ongoing blocker, calculate days since first appearance.

**Cadence Compliance Score:**
Percentage of workdays with a Daily entry: X/5 = Y%

### Step 5.5: BEAST Task Audit (MANDATORY — internal, no output)

**THIS STEP IS NOT OPTIONAL.** Analyze the full BEAST table against this week's Daily entries and produce actionable findings:

**A. Tasks That Should Be Closed:**
Scan all BEAST tasks with Status "In progress" or "Not started". For each, check if the week's Daily entries contain evidence that the task was completed. If so, recommend marking it Done with a completion note referencing the specific Daily entry date and evidence.

**B. Tasks That Need Note Updates:**
For any active BEAST task (Not started or In progress) that was referenced in a Daily entry this week, recommend prepending a dated note: `BLOG DD MMM: [summary of progress from the Daily entry]`

**C. New Tasks to Create:**
Scan the week's Daily entries for action items, commitments, follow-ups, or "Looking Ahead" items that have no corresponding BEAST task. Recommend creating new BEAST tasks with appropriate fields.

**D. Overdue Task Assessment:**
For every overdue BEAST task (Due Date < today, Status not Done), check if the week's Daily entries explain the delay. Recommend: reschedule with new Due Date, escalate priority, or mark blocked.

**E. Stale Task Assessment:**
For every BEAST task with no Notes update in 14+ days that is still active, flag it. Recommend: update notes with current status, reschedule, deprioritize, or close as OBE.

**F. Coming Week Preview:**
List all BEAST tasks due in the coming week (Monday through Friday after target week). Flag any that are High priority or have no notes.

### Step 6: Final Report + Write Confirmation (ONLY user-visible output)

Present everything in one structured report:

**A. Week in Summary** (full Section 1 output)
**B. Wins This Week** (full Section 2 output)
**C. Looking Ahead** (full Section 3 output)
**D. Blockers and Open Items** (full Section 4 output)

**E. BEAST Task Audit Results**
- Tasks recommended to close: [list with Task ID, Name, evidence]
- Tasks needing note updates: [list with Task ID, recommended note]
- New tasks to create: [list with proposed Name, Priority, Due Date, Project, Reason]
- Overdue tasks: [list with Task ID, Name, days overdue, recommendation]
- Stale tasks (14+ days): [list with Task ID, Name, last update, recommendation]
- Coming week preview: [list of tasks due next week]

**G. Integrity Check Results**
- Cadence compliance: X/5 workdays covered (Y%)
- Missing days: [list]
- Untracked blockers: [list or "None"]
- Commitment tracking (if prior Weekly exists): X/Y items addressed (Z%)
  - Completed: [list]
  - In Progress: [list]
  - Not Started: [list]
  - Dropped: [list]
- Workstream balance: [category distribution table]
- Blocker ages: [list with days]

**H. Write Confirmation**
```
PROPOSED CODA WRITE (requires your confirmation):

Weekly Entry → Daily Log table
- Date: [Friday of target week, ISO format]
- Entry Type: Weekly
- Status: Draft
- Category: Admin
- 5 text fields populated (Reviewed Notes, Polished Summary, Executive Bullets, Key Wins, Blockers)

Type "yes" to write. Type "no" to skip.
```

### Step 7: Execute Write (only after confirmation)

Follow the 7-step Write Safety Protocol:

```
table_rows_manage(
  uri: "coda://docs/dHXfr0V468/tables/grid-ty2WGfh4qa",
  data: {
    action: "add",
    columns: [
      "c-oiaBDBstH1",   // Date = Friday of target week
      "c-DXM4h2B28G",   // Reviewed Notes = Week in Summary (full narrative)
      "c-FIWz6AEhwd",   // Polished Summary = Condensed weekly overview
      "c-WSCAvrHbnz",   // Executive Bullets = Looking Ahead
      "c-QuKWx0lwGp",   // Key Wins = Wins This Week
      "c-bT-C79ocGH",   // Blockers = Blockers and Open Items
      "c-CA6Nwa3A2N",   // Category = "Admin"
      "c-pR0VmtQ5AV",   // Status = "Draft"
      "c-7IZ-UJNjXG"    // Entry Type = "Weekly"
    ],
    rows: [[
      "[YYYY-MM-DD Friday]",
      "[Week in Summary as markdown]",
      "[Condensed 2-3 paragraph overview]",
      "[Looking Ahead as markdown]",
      "[Wins This Week as markdown]",
      "[Blockers and Open Items as markdown]",
      "Admin",
      "Draft",
      "Weekly"
    ]]
  }
)
```

Verify the write by reading the new row back.

---

## COLUMN MAPPING REFERENCE

| Content | Column | Column ID |
|---|---|---|
| Friday of target week | Date | c-oiaBDBstH1 |
| Week in Summary (full narrative) | Reviewed Notes | c-DXM4h2B28G |
| Condensed weekly overview | Polished Summary | c-FIWz6AEhwd |
| Looking Ahead (next week) | Executive Bullets | c-WSCAvrHbnz |
| Wins This Week | Key Wins | c-QuKWx0lwGp |
| Blockers and Open Items | Blockers | c-bT-C79ocGH |
| "Admin" | Category | c-CA6Nwa3A2N |
| "Draft" | Status | c-pR0VmtQ5AV |
| "Weekly" | Entry Type | c-7IZ-UJNjXG |

---

## FORMATTING STANDARDS

| Setting | Value |
|---|---|
| Date format | DD MMM YYYY |
| Em dashes | Never |
| Acronyms | Define on first use |
| Tone | Professional first person |
| Filler language | Never |
