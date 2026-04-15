---
name: activity-annual
model: sonnet
effort: high
description: >
  Generate Brady's annual activity review. ALWAYS use this skill when the user
  says "run annual", "run my annual", "annual review", "annual summary",
  "year in review", "summarize last year", or "year-end review". Reads four
  Quarterly Reviews plus the BEAST task list and any prior Annual Review from
  Coda via MCP, generates a four-section annual review suitable for self-assessment
  or performance review, and writes an Annual Review entry to the Daily Log
  after human review.
---

# Activity Annual

Generates an annual review by synthesizing four Quarterly Reviews, performing a full BEAST task audit, producing a career narrative suitable for self-assessment or performance review, and analyzing year-long systemic patterns.

**THIS SKILL MUST READ AND ANALYZE THE FULL BEAST TABLE.** The BEAST task audit is not optional. Every annual review includes a complete year-end task health assessment, completion statistics, and cleanup recommendations.

---

## Recommended Model

Run with **Sonnet** at **high effort**. Annual reviews synthesize a full year of data and require strategic narrative depth.

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

### Step 1: Determine Target Year

Identify the prior complete calendar year. If the user specifies a year, use that.

### Step 2: Read Quarterly Reviews for Target Year (internal)

Call `table_rows_read` on Daily Log. Filter in-skill:
- **Quarterly Reviews:** Entry Type = "Quarterly Review", Date within the target year (4 entries expected)
- **Prior Annual Review:** Entry Type = "Annual Review" for the year before the target (if exists)

**Important:** Read ONLY Quarterly Reviews for the annual synthesis. Do NOT read Monthly Digests, Weekly, or Daily entries. The hierarchy ensures Quarterly Reviews already contain all synthesized content.

If fewer than 4 Quarterly Reviews exist, note the gap and work with available data. Flag missing quarters in integrity checks.

### Step 3: Read BEAST Table (MANDATORY — internal)

**THIS STEP IS NOT OPTIONAL.** Read ALL BEAST rows via MCP with pagination (`rowLimit: 100`, then `rowOffset: 100` if `hasMore`). Build the full task list. Extract `.name` from select refs and `.input` from date fields.

### Step 4: Generate Annual Review (internal)

Produce four sections:

**Section 1: Year in Summary**
Career narrative for the year. This section should be:
- Suitable for direct use in a self-assessment or performance review
- Identifies the 3-5 most significant contributions of the year
- Traces the strategic arc: how priorities evolved across quarters
- Notes career-defining moments, new responsibilities, or scope expansions
- Quantifies impact where possible (tasks completed, projects delivered, initiatives launched)
- Professional tone, first person, no em dashes, no filler

**Section 2: Key Accomplishments**
Grouped by initiative or workstream. For each:
- What was accomplished
- Why it mattered
- Quantified impact where available (count of deliverables, stakeholders served, problems resolved)

Identify the single most consequential accomplishment of the year.

**Section 3: Looking Ahead**
Strategic priorities for the coming year. Frame at the **career and initiative level**:
- What the priority is
- Why it matters for the coming year
- What success looks like at the annual scale

**Section 4: Systemic Observations**
Patterns, recurring challenges, and organizational insights accumulated over the year:
- Recurring blocker categories (what types of blockers appeared most often?)
- Organizational friction points (where did cross-team dependencies consistently slow work?)
- Seasonal workload patterns (were certain quarters heavier than others? Why?)
- Tool and process observations (what worked, what didn't)
- Recommendations for systemic improvement

### Step 5: Run Integrity Checks (internal)

1. **Prior-Year Closure:** Compare annual outcomes against prior year's goals (if prior Annual Review exists). Categorize: Completed, In Progress, Not Started, Dropped.

2. **Quarterly Coverage:** Flag any quarter that lacks a Quarterly Review.

3. **Year-Long Blocker Analysis:** Aggregate blocker data from all Quarterly Reviews. Identify patterns: most common blocker types, longest-running blockers, systemic vs one-time.

4. **BEAST Year-End Health:**
   - Total tasks created during the year (estimated from Note dates)
   - Total tasks completed
   - Tasks still open from the beginning of the year
   - Overall completion rate

5. **Workstream Health (Annual):** Same as quarterly Check 7 but aggregated across all 4 quarters.

### Step 5.5: BEAST Year-End Audit (MANDATORY — internal)

**THIS STEP IS NOT OPTIONAL.** Analyze the full BEAST table at the annual scale:

**A. Year-End Health Dashboard:**
- Total tasks created during the year (estimated from Note dates)
- Total tasks completed (Status = Done)
- Tasks still open from the beginning of the year
- Overall completion rate (completed / total)
- Average task lifespan (creation to completion)

**B. Year-Long Stale Tasks:**
Tasks open since the beginning of the year with no meaningful progress. These represent systematic neglect and need hard decisions: close as OBE, escalate, or recommit.

**C. Workstream Health (Annual):**
For each Project, aggregate across all 4 quarters:
- Total completed, total added, total stalled, net change
- Trajectory: "Growing", "Stable", "Declining", "Completed"

**D. Task Hygiene Recommendations:**
- Tasks with missing Due Dates
- Tasks with missing Notes
- Tasks with Status "Not started" for 90+ days
- Recommend bulk cleanup actions

### Step 6: Final Report + Write Confirmation

Present: Year in Summary, Key Accomplishments, Looking Ahead, Systemic Observations, **BEAST Year-End Audit Results**, all integrity check results, and write confirmation request.

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
      "[YYYY-12-31 last day of year]",
      "[Year in Summary as markdown]",
      "[Condensed annual overview]",
      "[Looking Ahead as markdown]",
      "[Key Accomplishments as markdown]",
      "[Systemic Observations as markdown]",
      "Admin",
      "Draft",
      "Annual Review"
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
| Last day of target year | Date | c-oiaBDBstH1 |
| Year in Summary | Reviewed Notes | c-DXM4h2B28G |
| Condensed annual overview | Polished Summary | c-FIWz6AEhwd |
| Looking Ahead | Executive Bullets | c-WSCAvrHbnz |
| Key Accomplishments | Key Wins | c-QuKWx0lwGp |
| Systemic Observations | Blockers | c-bT-C79ocGH |
| "Admin" | Category | c-CA6Nwa3A2N |
| "Draft" | Status | c-pR0VmtQ5AV |
| "Annual Review" | Entry Type | c-7IZ-UJNjXG |

---

## FORMATTING STANDARDS

| Setting | Value |
|---|---|
| Date format | DD MMM YYYY |
| Em dashes | Never |
| Tone | Professional, strategic first person suitable for performance review |
| Filler language | Never |
