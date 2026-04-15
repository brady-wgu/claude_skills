---
name: activity-monthly
model: sonnet
effort: medium
description: >
  Generate Brady's monthly activity digest. ALWAYS use this skill when the user
  says "run monthly", "run my monthly", "monthly summary", "monthly digest",
  "monthly review", "summarize last month", or "what happened last month".
  Reads all Daily and Weekly entries from the prior month plus the BEAST task list
  and any prior Monthly Digest from Coda via MCP, generates a four-section monthly
  summary with integrity checks including blocker lifecycle and category trends,
  and writes a Monthly Digest entry to the Daily Log after human review.
  Also supports OneNote export reconciliation when a PDF is provided.
---

# Activity Monthly

Generates a monthly digest by synthesizing Daily and Weekly entries, performing a full BEAST task audit, tracking blocker lifecycles, and analyzing category distribution trends.

**THIS SKILL MUST READ AND ANALYZE THE FULL BEAST TABLE.** The BEAST task audit is not optional. Every monthly review includes a complete assessment of task health: overdue tasks, stale tasks, tasks that should be closed, tasks incorrectly left open, and a full BEAST health dashboard.

---

## Recommended Model

Run with **Sonnet** at **medium effort**.

---

## AUTHOR CONTEXT

Brady Redfearn is a Senior Strategist in Program Development at Western Governors University (WGU).

Common acronyms: WGU, UPL, PD, LR, SDP, JFT, PES, BEAST, BLOG

---

## CODA SAFETY PROTOCOL

Read `references/coda-safety.md` for the full protocol. All 5 constraints and the 7-step Write Safety Protocol apply.

---

## CODA SCHEMA REFERENCE

### Daily Log Table
- URI: `coda://docs/dHXfr0V468/tables/grid-ty2WGfh4qa`
- Full column list: see `references/coda-safety.md`

### BEAST Table
- URI: `coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x`

---

## EXECUTION FLOW

### Step 1: Determine Target Month

Identify the prior complete calendar month. If the user specifies a month, use that.

### Step 2: Read All Entries for Target Month (internal)

Call `table_rows_read` on Daily Log (paginate if needed). Filter in-skill:
- **Daily entries:** Entry Type = "Daily", Date within target month
- **Weekly entries:** Entry Type = "Weekly", Date within target month
- **Prior Monthly Digest:** Entry Type = "Monthly Digest" for the month before the target (if exists), to retrieve its "Looking Ahead" for closure checking

Extract text from Slate JSON fields by traversing `root.children`.

### Step 3: Read BEAST Table (MANDATORY — internal)

**THIS STEP IS NOT OPTIONAL.** Read ALL BEAST rows via MCP with pagination (`rowLimit: 100`, then `rowOffset: 100` if `hasMore`). Build the full task list with Task ID to Row ID mapping. Extract `.name` from select refs and `.input` from date fields.

### Step 4: Generate Monthly Digest (internal)

Produce four sections:

**Section 1: Month in Summary**
Narrative arc of the month. Include:
- Primary workstream focus and how it evolved week by week
- Key milestones, decisions, or turning points
- Reference Weekly summaries as structural anchors rather than re-reading every Daily
- Category distribution analysis: how many entries per category, shifts in focus
- Professional tone, first person, no em dashes, no filler

**Section 2: Wins This Month**
Aggregate from Weekly "Wins" sections, supplemented by Daily wins not captured in a Weekly. Deduplicate. Group by workstream/project. One sentence per win.

**Section 3: Looking Ahead**
Top 5 to 7 priorities for the coming month. Split into:
- **Next Month Priorities** (consequential items with rationale)
- **Continuing Background Tasks**

Base on: BEAST task due dates, priority levels, momentum from the current month, unresolved blockers.

**Section 4: Blockers and Open Items**
Split into three sub-sections:
- **Active Blockers** (with owner/dependency if known)
- **Untracked Gaps** (blockers with no BEAST task)
- **Resolved This Month** (for the record, with resolution date)

### Step 5: Run Integrity Checks (internal)

All Weekly checks (1-5, 8) plus:

6. **Blocker Lifecycle Report (Check 5):**
   - Blockers introduced this month (first appearance date)
   - Blockers resolved this month (resolution date, days to resolve)
   - Blockers persisting from prior month (age in days)
   - Average resolution velocity

7. **Category Distribution (Check 6):**
   - Table: Category | Entry Count | Percentage
   - Month-over-month comparison (if prior Monthly Digest exists)
   - Flag >60% concentration

8. **BEAST Health Dashboard:**
   - Total active tasks (Not started + In progress)
   - Overdue tasks (count and %)
   - Tasks completed this month
   - Average task age (days since creation, estimated from earliest Note date)

9. **Cadence Checks:**
   - Weeks within the month that have no Weekly entry
   - Workdays within the month that have no Daily entry
   - Overall cadence compliance %

10. **Prior-Month Closure (Check 4):**
    - If prior Monthly Digest exists, compare its "Looking Ahead" against this month's activity
    - Commitment completion rate

### Step 5.5: BEAST Task Audit (MANDATORY — internal)

**THIS STEP IS NOT OPTIONAL.** Analyze the full BEAST table against the month's entries:

**A. Tasks That Should Be Closed:**
Scan all active BEAST tasks. Cross-reference against the month's Daily/Weekly entries. If evidence shows the task was completed during the month, recommend marking Done with a completion note.

**B. Tasks Incorrectly Left Open:**
Look for tasks whose Notes contain completion evidence (e.g., "Done", "Completed", "Delivered") but Status is still "In progress" or "Not started". Flag for closure.

**C. New Tasks to Create:**
Scan the month's "Looking Ahead" items and blocker lists for action items with no corresponding BEAST task. Recommend creation.

**D. Overdue Task Triage:**
For every overdue task, assess based on the month's activity: should it be rescheduled, escalated, deprioritized, or closed as OBE?

**E. Stale Task Cleanup:**
All BEAST tasks with no Notes update in 14+ days. Recommend: update, reschedule, deprioritize, or close.

**F. BEAST Health Dashboard:**
- Total active tasks
- Overdue count and %
- Completed this month
- Created this month
- Net change (completed - created)
- Oldest open task (by earliest Note date)

### Step 6: Final Report + Write Confirmation

Present: Month in Summary, Wins, Looking Ahead, Blockers, **BEAST Task Audit Results**, all integrity check results, and write confirmation request.

Write payload:
```
table_rows_manage(
  uri: "coda://docs/dHXfr0V468/tables/grid-ty2WGfh4qa",
  data: {
    action: "add",
    columns: [
      "c-oiaBDBstH1", "c-DXM4h2B28G", "c-FIWz6AEhwd", "c-WSCAvrHbnz",
      "c-QuKWx0lwGp", "c-bT-C79ocGH", "c-CA6Nwa3A2N", "c-pR0VmtQ5AV",
      "c-7IZ-UJNjXG"
    ],
    rows: [[
      "[YYYY-MM-DD last day of month]",
      "[Month in Summary as markdown]",
      "[Condensed monthly overview]",
      "[Looking Ahead as markdown]",
      "[Wins This Month as markdown]",
      "[Blockers and Open Items as markdown]",
      "Admin",
      "Draft",
      "Monthly Digest"
    ]]
  }
)
```

### Step 7: Execute Write (only after confirmation)

Follow the 7-step Write Safety Protocol. Verify by reading back.

---

## ONENOTE RECONCILIATION WORKFLOW

See `references/monthly-reconciliation.md` for the full process.

When the user uploads a PDF export from OneNote alongside the monthly digest request, run the reconciliation:

1. Parse the PDF for daily note entries
2. Cross-reference against Daily Log entries in Coda for the same period
3. Report:
   - Days with full match (no action)
   - Days with additional OneNote detail (review recommended)
   - Days completely missing from Daily Log (ACTION REQUIRED -- process through activity-daily)
   - Duplicate or contradictory content (REVIEW)
4. Summary: total days reviewed, aligned, requiring review, requiring processing

---

## COLUMN MAPPING

| Content | Column | Column ID |
|---|---|---|
| Last day of target month | Date | c-oiaBDBstH1 |
| Month in Summary | Reviewed Notes | c-DXM4h2B28G |
| Condensed monthly overview | Polished Summary | c-FIWz6AEhwd |
| Looking Ahead | Executive Bullets | c-WSCAvrHbnz |
| Wins This Month | Key Wins | c-QuKWx0lwGp |
| Blockers and Open Items | Blockers | c-bT-C79ocGH |
| "Admin" | Category | c-CA6Nwa3A2N |
| "Draft" | Status | c-pR0VmtQ5AV |
| "Monthly Digest" | Entry Type | c-7IZ-UJNjXG |

---

## FORMATTING STANDARDS

| Setting | Value |
|---|---|
| Date format | DD MMM YYYY |
| Em dashes | Never |
| Tone | Professional first person |
| Filler language | Never |
