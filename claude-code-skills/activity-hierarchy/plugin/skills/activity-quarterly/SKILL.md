---
name: activity-quarterly
model: sonnet
effort: high
description: >
  Generate Brady's quarterly activity review. ALWAYS use this skill when the user
  says "run quarterly", "run my quarterly", "quarterly review", "quarterly summary",
  "summarize last quarter", or "Q1/Q2/Q3/Q4 review". Reads three Monthly Digests
  plus the BEAST task list and any prior Quarterly Review from Coda via MCP,
  generates a four-section quarterly review with integrity checks including
  workstream health analysis, and writes a Quarterly Review entry to the Daily
  Log after human review.
---

# Activity Quarterly

Generates a quarterly review by synthesizing three Monthly Digests, performing a full BEAST task audit, analyzing workstream health, and producing a strategic narrative.

**THIS SKILL MUST READ AND ANALYZE THE FULL BEAST TABLE.** The BEAST task audit is not optional. Every quarterly review includes a complete assessment: stale tasks, tasks open all quarter, workstream health matrix, and cleanup recommendations.

---

## Recommended Model

Run with **Sonnet** at **high effort**. Quarterly reviews synthesize 3 months of data and require more reasoning depth.

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

### BEAST Table
- URI: `coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x`

---

## EXECUTION FLOW

### Step 1: Determine Target Quarter

Identify the prior complete quarter:
- Q1: January - March
- Q2: April - June
- Q3: July - September
- Q4: October - December

If the user specifies a quarter, use that.

### Step 2: Read Monthly Digests for Target Quarter (internal)

Call `table_rows_read` on Daily Log. Filter in-skill:
- **Monthly Digests:** Entry Type = "Monthly Digest", Date within the target quarter (3 entries expected)
- **Prior Quarterly Review:** Entry Type = "Quarterly Review" for the quarter before the target (if exists)

Extract text from Slate JSON fields.

**Important:** Read ONLY Monthly Digests for the quarterly synthesis. Do NOT read individual Daily or Weekly entries. The whole point of the hierarchy is that Monthly Digests already contain the synthesized content.

If fewer than 3 Monthly Digests exist, note the gap and work with available data. Flag missing months in integrity checks.

### Step 3: Read BEAST Table (MANDATORY — internal)

**THIS STEP IS NOT OPTIONAL.** Read ALL BEAST rows via MCP with pagination (`rowLimit: 100`, then `rowOffset: 100` if `hasMore`). Build the full task list. Extract `.name` from select refs and `.input` from date fields.

### Step 4: Generate Quarterly Review (internal)

Produce four sections:

**Section 1: Quarter in Summary**
Strategic narrative of the quarter. Include:
- The 2-3 dominant workstreams and how they evolved month-over-month
- Significant pivots, new initiatives, or strategic shifts
- Month-over-month progression showing how focus evolved
- Key decisions or milestones that shaped the quarter's trajectory
- Suitable for use in a quarterly business review or stakeholder update
- Professional tone, first person, no em dashes, no filler

**Section 2: Wins This Quarter**
Aggregate from Monthly Digest wins. Group by workstream. Identify the single most consequential accomplishment of the quarter and explain why.

**Section 3: Looking Ahead**
Top 3 to 5 strategic priorities for the coming quarter. Frame at the **initiative level**, not the task level. Each priority should include:
- What the initiative is
- Why it matters this quarter
- What success looks like

**Section 4: Blockers and Systemic Issues**
Distinguish between:
- **Task-level blockers** still active from Monthly Digests
- **Systemic patterns** (e.g., recurring tool access delays, cross-team dependency bottlenecks, resource constraints that appeared in multiple months)

### Step 5: Run Integrity Checks (internal)

All Monthly checks (1-6, 8) plus:

7. **Workstream Health Matrix (Check 7):**
   For each Project value in BEAST:
   - Tasks completed this quarter
   - Tasks still active
   - Tasks added this quarter
   - Tasks stalled (no Status change or Note update in 30+ days)
   - Net change (completed - added)
   - Health: "Progressing", "Stalled", "Growing", "Winding Down"

8. **Quarter-long Stale Tasks:**
   BEAST tasks open for the entire quarter with no status change.

9. **Prior-Quarter Closure:**
   Compare quarterly outcomes against prior quarter's "Looking Ahead". Categorize: Completed, In Progress, Not Started, Dropped.

10. **Monthly Digest Coverage:**
    Flag any month in the quarter that has no Monthly Digest.

### Step 5.5: BEAST Task Audit (MANDATORY — internal)

**THIS STEP IS NOT OPTIONAL.** Analyze the full BEAST table at the quarterly scale:

**A. Quarter-Long Stale Tasks:**
Any BEAST task open for the entire quarter with no status change or note update in 30+ days. These need decisions: close, reschedule, or escalate.

**B. Tasks That Should Be Closed:**
Cross-reference Monthly Digest wins and completed items against active BEAST tasks. If a task's objective was achieved during the quarter, recommend closure.

**C. Orphaned Tasks:**
Tasks with no Project assignment, no Due Date, and no recent notes. Recommend: assign, defer, or close as OBE.

**D. Workstream Health Matrix:**
For each Project value in BEAST:
- Tasks completed this quarter
- Tasks still active
- Tasks added this quarter
- Tasks stalled (30+ days no update)
- Net change
- Health assessment: "Progressing", "Stalled", "Growing", "Winding Down"

**E. Overdue Triage:**
All overdue tasks with quarterly-level recommendations: bulk reschedule, deprioritize, or escalate.

### Step 6: Final Report + Write Confirmation

Present: Quarter in Summary, Wins, Looking Ahead, Systemic Issues, **BEAST Task Audit Results (including Workstream Health Matrix)**, all integrity check results, and write confirmation request.

Write payload follows the same pattern as other skills:
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
      "[YYYY-MM-DD last day of quarter]",
      "[Quarter in Summary as markdown]",
      "[Condensed quarterly overview]",
      "[Looking Ahead as markdown]",
      "[Wins This Quarter as markdown]",
      "[Blockers and Systemic Issues as markdown]",
      "Admin",
      "Draft",
      "Quarterly Review"
    ]]
  }
)
```

### Step 7: Execute Write (only after confirmation)

Follow the 7-step Write Safety Protocol. Verify by reading back.

---

## COLUMN MAPPING

| Content | Column | Column ID |
|---|---|---|
| Last day of target quarter | Date | c-oiaBDBstH1 |
| Quarter in Summary | Reviewed Notes | c-DXM4h2B28G |
| Condensed quarterly overview | Polished Summary | c-FIWz6AEhwd |
| Looking Ahead | Executive Bullets | c-WSCAvrHbnz |
| Wins This Quarter | Key Wins | c-QuKWx0lwGp |
| Blockers and Systemic Issues | Blockers | c-bT-C79ocGH |
| "Admin" | Category | c-CA6Nwa3A2N |
| "Draft" | Status | c-pR0VmtQ5AV |
| "Quarterly Review" | Entry Type | c-7IZ-UJNjXG |

---

## FORMATTING STANDARDS

| Setting | Value |
|---|---|
| Date format | DD MMM YYYY |
| Em dashes | Never |
| Tone | Professional, strategic first person |
| Filler language | Never |
