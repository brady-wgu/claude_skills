---
name: activity-daily
model: sonnet
effort: medium
description: >
  Run Brady's complete daily BLOG and BEAST pipeline via Coda MCP. ALWAYS use this
  skill when the user says "run pipeline", "run daily", "run BLOG and BEAST",
  "run blog beast", "process my notes", "morning briefing", "run morning updates",
  "run BEAST", "run BLOG", "process today's notes", or pastes raw daily work notes
  and asks to process them. Processes notes through a seven-section BLOG, reads the
  live BEAST table from Coda via MCP, produces a four-section BEAST briefing with
  task updates, performs a blocker-to-BEAST cross-reference, and writes all results
  to Coda via MCP after human review. Replaces the blog-beast-pipeline skill.
---

# Activity Daily

Unified BLOG + BEAST pipeline. Processes raw daily work notes end-to-end and synchronizes with Coda via MCP. No Python scripts, no temp files, no API keys.

**THIS SKILL HAS TWO EQUAL HALVES. BOTH ARE MANDATORY:**
1. **BLOG** — Process raw notes into a 7-section journal entry and write to the Daily Log
2. **BEAST** — Read the ENTIRE To Do List from Coda, analyze every task against the BLOG, flag problems, recommend updates, add new tasks, and write changes back

**Skipping BEAST processing is a critical failure.** The BEAST analysis is not optional, secondary, or "nice to have." It is half of this pipeline. If the Final Report does not contain a Morning Briefing, Flags and Issues, Recommended Task Updates, and Today's Priority List, the pipeline has not completed.

---

## Recommended Model

Run this pipeline with **Sonnet** at **medium effort**. The pipeline follows highly structured, rule-based instructions. Sonnet handles this efficiently. The `model: sonnet` and `effort: medium` frontmatter fields enforce this automatically when the skill is triggered.

---

## MODE: PRODUCTION

CRITICAL EXECUTION RULES:
- This pipeline has 6 steps. ALL 6 STEPS ARE MANDATORY. Do not skip any step.
- Step 1: Process BLOG (7 sections)
- Step 2: **Read the BEAST table from Coda via MCP** (MANDATORY — call table_rows_read)
- Step 3: **Process BEAST** (4 sections including task updates) (MANDATORY)
- Step 4: Blocker cross-reference
- Step 5: Final Report (the ONLY output the user sees — must include BOTH blog AND beast)
- Step 6: Execute writes after user confirmation
- Do NOT output any text to the user until the Final Report in Step 5.
- Do NOT skip Steps 2 and 3. The BEAST table MUST be read from Coda and processed.
- **EXCEPTION:** Coda writes ALWAYS require human confirmation. The Final Report includes a write confirmation request. No writes happen without explicit approval.

---

## AUTHOR CONTEXT

Brady Redfearn is a Senior Strategist in Program Development at Western Governors University (WGU). His title, team, and domain context are established. No need to prompt for context each session.

Common acronyms: WGU (Western Governors University), UPL (University Program Leader), PD (Program Development), LR (Learning Resources), SDP (Supplemental Digital Product), JFT (Jellyfish Technologies Ltd.), PES (Program Evaluation & Strategy), BEAST (Brady's Execution, Action, and Strategy Tasks), BLOG (Brady's Learnings, Observations, and Growth)

---

## CODA SAFETY PROTOCOL

Read `references/coda-safety.md` for the full safety protocol. Summary of the 5 non-negotiable constraints:

1. **Hard-code all write targets with read-first verification.** Never write to a URI from memory alone.
2. **Zero deletion capability.** Describe deletions for manual execution.
3. **Single-doc write scope.** Brady's Coda Playground (dHXfr0V468) only.
4. **All other Coda docs are read-only.**
5. **Global Admin mode.** Every write is irreversible and career-impacting.

The 7-step Write Safety Protocol applies to every `table_rows_manage` call. See `references/coda-safety.md` for the full protocol.

---

## CODA SCHEMA REFERENCE

### Doc
- Doc ID: dHXfr0V468
- Doc Name: Brady's Coda Playground

### Daily Log Table
- URI: `coda://docs/dHXfr0V468/tables/grid-ty2WGfh4qa`
- Columns:
  - Date: `c-oiaBDBstH1` (date)
  - Reviewed Notes: `c-DXM4h2B28G` (canvas -- accepts markdown strings for writes)
  - Polished Summary: `c-FIWz6AEhwd` (text)
  - Executive Bullets: `c-WSCAvrHbnz` (text)
  - Key Wins: `c-QuKWx0lwGp` (text)
  - Blockers: `c-bT-C79ocGH` (text)
  - Category: `c-CA6Nwa3A2N` (select)
  - Status: `c-pR0VmtQ5AV` (select)
  - Entry Type: `c-7IZ-UJNjXG` (select)

### Complete To Do List (BEAST) Table
- URI: `coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x`
- Columns:
  - Task ID: `c-ImEDreEoEA` (text)
  - Name: `c-MBRsPfbd6d` (text)
  - Status: `c-zH_C1i-smP` (select)
  - Priority: `c-g-kRN3Y2aS` (select)
  - Due Date: `c-NP39SR6C8D` (date)
  - Type: `c-Z_PWA6_-Bb` (select)
  - Project: `c-W3gb8_ca2O` (select)
  - Effort: `c-RdNqDL9akn` (select)
  - Notes: `c-ioDsMHggmZ` (text)
  - Link: `c-wuGVeM0y7z` (link)
  - Parent: `c-ONPz07rw_J` (lookup -- **NEVER WRITE**)
  - Subitems: `c-RRrt1LG5D9` (lookup -- **NEVER WRITE**)

---

## MCP DATA FORMAT NOTES

When reading from Coda via MCP, data returns in structured formats:

- **Select columns** return `{"name": "Done", "type": "ref", ...}`. Extract `.name` for display and comparison. For writes, pass the plain string (e.g., `"Done"`).
- **Date columns** return `{"type": "dt", "epoch": ..., "input": "4/13/2026"}`. Use `.input` for display. For writes, pass ISO format `"YYYY-MM-DD"`.
- **Rich text columns** (canvas, text with Slate) return nested Slate JSON: `{"root": {"children": [...]}, "type": "slate"}`. Traverse `root.children` to extract text. Each child has `.children[].text` for the content. For writes, pass markdown strings directly.
- **Plain text columns** (Notes, Task ID, Name) return simple strings.
- **The BEAST table has 162 rows.** Read with `rowLimit: 100`, then read again with `rowOffset: 100` to get the remainder.

---

## EXECUTION FLOW

When the user pastes raw daily work notes, execute these steps in order:

### Step 1: BLOG Processing (internal, no output)

Process the pasted notes through all seven BLOG sections plus the Coda field checklist in a single internal pass. Do not output anything to the user.

The date for the entry comes from the notes themselves (the day being documented), not from the system date. The user typically runs this the morning after the work day.

### Step 2: Read BEAST Table from Coda (MANDATORY — internal, no output)

**THIS STEP IS NOT OPTIONAL. You MUST call table_rows_read on the BEAST table.**

Call `table_rows_read` on the BEAST table via MCP:

```
table_rows_read(
  uri: "coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x",
  rowLimit: 100
)
```

If `hasMore` is true, call again with `rowOffset: 100` to get remaining rows. Combine all rows.

For each row, extract and store:
- **Row ID** (e.g., `i-K_YClpkwWq`) -- needed for update writes
- **Task ID** from `c-ImEDreEoEA` -- the BEAST-XXXX identifier
- **All field values**, extracting `.name` from select refs and `.input` from date fields
- Build a **Task ID to Row ID mapping** for the update step

Skip rows with no Task ID (child rows). Count child rows separately.

### Step 3: BEAST Processing (MANDATORY — internal, no output)

**THIS STEP IS NOT OPTIONAL. You MUST process the BEAST table and produce all 4 sections.**

Process the BEAST table data from Step 2 plus the BLOG output from Step 1 through the BEAST Processing Specification below. Today's date for BEAST processing is the system date (the morning the pipeline runs).

You MUST produce ALL four sections:
1. Morning Briefing — summary of task list health
2. Flags and Issues — every problem task flagged by type
3. Recommended Task Updates — specific changes to make, new tasks to create, tasks to complete
4. Today's Priority List — the 5-7 most important tasks for today

The Recommended Task Updates section is where you analyze the BLOG content against every active BEAST task and determine: which tasks should be updated (status, priority, notes, due dates), which tasks should be marked complete, and which NEW tasks should be created based on work described in the BLOG. This is the core intelligence of the BEAST processor.

For Section 3 (Recommended Task Updates), instead of producing a CSV import block, produce a structured MCP update payload:

**For existing task updates**, use the Task ID to Row ID mapping from Step 2:
```
{ rowNumberOrId: "[row ID]", updateCells: [{ columnId: "...", value: "..." }, ...] }
```

**For new tasks**, use the add action:
```
{ columns: ["c-ImEDreEoEA", "c-MBRsPfbd6d", ...], rows: [["BEAST-XXXX", "Task name", ...]] }
```

Convert all Due Dates to ISO format (YYYY-MM-DD) for writes. Keep D Mon YYYY in the display output.

### Step 4: Blocker-to-BEAST Cross-Reference (internal, no output)

Extract all unique blockers from BLOG Section 5. For each blocker, search the BEAST task list (from Step 2) for a matching task by keyword overlap in the Name or Notes fields.

For each unmatched blocker, prepare a flag:
- The blocker text
- "UNTRACKED: No corresponding BEAST task found"
- Recommendation to create a new BEAST task

Also check: if the BLOG mentions a stakeholder name combined with urgency language ("urgent", "ASAP", "deadline", "critical", "blocking"), check whether the related BEAST task has Priority = "High". If not, flag for upgrade.

### Step 5: Final Report + Write Confirmation (ONLY user-visible output)

This is the FIRST and ONLY output the user sees. Present everything in one structured report:

**Section A: BLOG Entry Summary**
- Date, suggested category
- Brief confirmation of what was processed

**Section B: BEAST Flags and Issues**
- Full output of BEAST Section 2

**Section C: BEAST Recommended Updates**
- Full output of BEAST Section 3 (human-readable format, not raw MCP payload)
- Show each task update: Task ID, Action (Add/Update/Complete), Field Changes, Reason

**Section D: Blocker Cross-Reference Results**
- Any untracked blockers flagged in Step 4
- Any priority upgrade signals

**Section E: Today's Priority List**
- Full output of BEAST Section 4

**Section F: Task Velocity**
- Tasks completed today: count
- Tasks created today: count
- Net delta

**Section G: Sensitive Items**
- Full output of BLOG Section 7. ALWAYS display explicitly. If none, state "None identified."
- Reminder: these are NEVER written to Coda.

**Section H: Write Confirmation Request**

Present the exact write operations that will be performed:

```
PROPOSED CODA WRITES (requires your confirmation):

1. BLOG ENTRY → Daily Log table
   - Date: [date]
   - Category: [category]
   - Entry Type: Daily
   - Status: Draft
   - [count] text fields populated

2. BEAST UPDATES → Complete To Do List table
   - [count] tasks to update
   - [count] new tasks to add
   - [list each task ID and action]

Type "yes" or "confirmed" to execute these writes.
Type "no" or "skip" to skip writes and keep the report only.
```

### Step 6: Execute Writes (only after confirmation)

On explicit confirmation from Brady, execute the writes following the 7-step Write Safety Protocol from `references/coda-safety.md`:

**BLOG Write to Daily Log:**

1. READ: Call `table_rows_read` on Daily Log to verify table is accessible
2. VERIFY: Confirm column IDs match hard-coded schema
3. BUILD: Construct the payload:
```
table_rows_manage(
  uri: "coda://docs/dHXfr0V468/tables/grid-ty2WGfh4qa",
  data: {
    action: "add",
    columns: [
      "c-oiaBDBstH1",   // Date
      "c-DXM4h2B28G",   // Reviewed Notes
      "c-FIWz6AEhwd",   // Polished Summary
      "c-WSCAvrHbnz",   // Executive Bullets
      "c-QuKWx0lwGp",   // Key Wins
      "c-bT-C79ocGH",   // Blockers
      "c-CA6Nwa3A2N",   // Category
      "c-pR0VmtQ5AV",   // Status
      "c-7IZ-UJNjXG"    // Entry Type
    ],
    rows: [[
      "[ISO date from notes]",
      "[BLOG Section 1 as markdown]",
      "[BLOG Section 2 as markdown]",
      "[BLOG Section 3 as markdown]",
      "[BLOG Section 4 as markdown]",
      "[BLOG Section 5 as markdown]",
      "[BLOG Section 6 category name]",
      "Draft",
      "Daily"
    ]]
  }
)
```

CRITICAL: Section 7 (Sensitive Items) is NEVER included in any write payload.

4. (Already presented in Step 5)
5. (Already confirmed by user)
6. WRITE: Execute the `table_rows_manage` call
7. VERIFY: Read the new row back to confirm success

**BEAST Writes:**

For task **updates** (existing rows):
```
table_rows_manage(
  uri: "coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x",
  data: {
    action: "update",
    rows: [
      {
        rowNumberOrId: "[row ID from mapping]",
        updateCells: [
          { columnId: "[column ID]", value: "[new value]" },
          ...
        ]
      },
      ...
    ]
  }
)
```

For **new tasks** (new rows):
```
table_rows_manage(
  uri: "coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x",
  data: {
    action: "add",
    columns: [
      "c-ImEDreEoEA", "c-MBRsPfbd6d", "c-zH_C1i-smP", "c-g-kRN3Y2aS",
      "c-NP39SR6C8D", "c-Z_PWA6_-Bb", "c-W3gb8_ca2O", "c-RdNqDL9akn",
      "c-ioDsMHggmZ", "c-wuGVeM0y7z"
    ],
    rows: [["BEAST-XXXX", "Task name", "Not started", ...]]
  }
)
```

NEVER include Parent (`c-ONPz07rw_J`) or Subitems (`c-RRrt1LG5D9`) in any write.

After writes complete, output a brief confirmation:
- BLOG: "Daily Log entry created for [date] with Status: Draft"
- BEAST: "[N] tasks updated, [N] new tasks created"
- If new tasks were created: "Reminder: Parent and Subitems must be manually assigned in Coda"

If Brady says "no" or "skip" at the confirmation step, output: "Writes skipped. Report preserved above for reference." Do not write anything to Coda.

---

## BLOG PROCESSING SPECIFICATION

### Processing Rules

When the user pastes raw notes for one day, process them through all seven sections plus the checklist in a single pass. Do not ask clarifying questions mid-output unless the notes are completely unreadable. If something is ambiguous, make a reasonable inference and note it in Section 1.

### Section Header Format

Every section header must follow this exact format (downstream automation depends on it):

```
[one blank line]
**====================SECTION HEADER====================**
[one blank line]
```

### Section 1: Reviewed Notes

**====================REVIEWED NOTES====================**

Produce a cleaned version of the raw notes the user can paste directly into their workspace as the source record. Apply the minimum edits necessary to make the notes public-ready:

- Remove informality, venting, or unfiltered commentary about colleagues, teams, or departments that would be inappropriate in a professional context
- Remove language that could embarrass the author or any named or implied individuals
- Remove opinions or characterizations of people, roles, or organizations that are better left private
- Remove sensitive details: personnel matters, compensation, conflicts, or anything that reads as gossip or grievance
- Fix typos, expand shorthand, and normalize casual phrasing

Do not sanitize legitimate professional observations or strip useful context. The goal is professional discretion, not information loss. Preserve the original structure, voice, and level of detail. Format all dates as DD MMM YYYY.

### Section 2: Polished Summary

**====================POLISHED SUMMARY====================**

Write a thorough, professional journal entry in first person. Use only the sub-headers that are relevant from this list:

- Overview
- Organizational Context
- Key People
- Workstreams and Partnerships
- Working Definitions
- Tools and Access Pending
- Looking Ahead

Rules:
- Define all acronyms on first use
- Fix typos and expand shorthand but do not invent facts
- If any part of the raw notes is already written in polished prose, preserve it with light editing only
- No em dashes
- No filler language ("it is worth noting that", "in conclusion", etc.)
- Format all dates as DD MMM YYYY

### Section 3: Executive Bullets

**====================EXECUTIVE BULLETS====================**

Produce a structured briefing for a senior leader with 90 seconds to read it. Three labeled subsections only:

**Situation:** 2 to 3 bullets on what was learned or accomplished.
**Implications:** 1 to 2 bullets on strategic or operational meaning.
**Watch Items:** 1 to 2 bullets on open questions, risks, or follow-ups.

Each bullet is one concise sentence. Define acronyms on first use. No padding on thin days. Fewer bullets is always acceptable.

### Section 4: Key Wins

**====================KEY WINS====================**

A short bulleted list of wins, progress, clarity gained, or problems solved. One sentence per bullet. If none, write exactly: `None logged.`

### Section 5: Blockers

**====================BLOCKERS====================**

A short bulleted list of blockers, missing access, open questions, unresolved dependencies, or risks. One sentence per bullet. If none, write exactly: `None logged.`

### Section 6: Suggested Category

**====================SUGGESTED CATEGORY====================**

Recommend exactly one category from this list:
Onboarding, UPL, Intake, Initiative, People & Network, Team & Culture, Definitions & Concepts, Tools & Access, Strategy, Admin

### Coda Field Checklist

**====================CODA FIELD CHECKLIST====================**

- **Entry Type:** Daily
- **Status:** Draft (set to Published after review)

### Section 7: Sensitive Items (Private, Do Not Post)

**====================SENSITIVE ITEMS (DO NOT POST)====================**

Review the raw notes for any content that was removed or softened during the Reviewed Notes sanitization step AND that rises to the level of a substantive private matter the author may need to track or follow up on separately. This includes:

- Performance-related observations about specific individuals
- Personnel matters (hiring, departures tied to conduct, disciplinary actions)
- Policy changes driven by or targeting specific individuals' behavior
- Compensation or benefits details tied to named people
- Conflicts, grievances, or disputes that may require future action
- Any content the author may need for a private record but that does not belong in a shared workspace

For each item, briefly state:
1. What was removed or softened
2. Why it was flagged
3. Recommended follow-up action

Do NOT include items here that were simply informal language adjustments (e.g., softening a blunt phrasing or casual tone). Those belong in Section 1 and do not require separate tracking.

If no substantive sensitive items were identified, write exactly: `None identified.`

CRITICAL: Section 7 is NEVER written to Coda. It is displayed in the output only.

### BLOG Usage Notes

- Sections 1 through 6: Map to corresponding Coda Daily Log columns
- Coda Field Checklist: Confirm Entry Type is Daily and move Status from Draft to Published after review
- Section 7: Displayed in output only. NEVER written to Coda under any circumstances
- Thin days are fine: If the notes are brief, produce proportionally brief output. Do not pad
- Multiple days at once: If the user pastes notes for more than one day, process each day as a separate complete output, clearly labeled with the date

### BLOG Formatting Standards

| Setting | Value |
|---|---|
| Date format | DD MMM YYYY |
| Em dashes | Never |
| Acronyms | Define on first use in each section |
| Tone | Professional first person |
| Filler language | Never |
| Section headers | Exact format shown above |

---

## BEAST PROCESSING SPECIFICATION

BEAST = Brady's Execution, Action, and Strategy Tasks
BLOG = Brady's Learnings, Observations, and Growth

This specification processes two inputs -- the BEAST table data from Step 2 and the BLOG entry from Step 1 -- and produces a structured four-section morning briefing plus an MCP-ready update payload containing only changed and new rows.

### Inputs

- **BEAST table data** (required): Full table read via MCP from Step 2. All rows with Task IDs, plus child row count.
- **BLOG entry** (required): The output from the BLOG processor in Step 1. This is the authoritative source for task status updates. BEAST records are only modified when BLOG evidence directly supports the change.
- **Today's date**: Use the system date automatically.

### Field Value Standards

See `references/field-standards.md` for the complete field validation rules. Summary:

**Status:** "Not started", "In progress", "Done", "Blocked"
**Priority:** "High", "Medium", "Low"
**Effort:** "30 min", "Half day", "Full day", "Multi-day"
**Type:** "Action", "Meeting", "Research", "Deliverable", "Admin"
**Project:** Proper nouns, exact capitalization. Known: Cicada, Networking, Onboarding, Team/Ops, JFT SDP, Learning Resources Analytics, Math Supplemental Content
**Due Date:** D Mon YYYY in output display; YYYY-MM-DD for MCP writes
**Task ID:** BEAST-XXXX (four-digit zero-padded, continue from highest existing)

### Child Row Rules

Parent tasks carry a BEAST-XXXX Task ID. Child rows nested under a parent have no Task ID.

- Do not assign Task IDs to child rows.
- Do not evaluate child rows for flags.
- Do not include child rows in any write operation.
- The parent task row is the unit of tracking.

### Notes Standards

Every active task (Not started or In progress) must have substantive notes at all times. Notes must reflect current status, progress, blockers, and next actions.

Note format for datestamped entries:

```
BLOG DD MMM: [entry] | STATUS UPDATE DD MMM: [update]
```

New dated entries are prepended to existing notes, never overwriting prior history.

OBE resolution for Done tasks with unfilled placeholders:
If a Done task's Notes field still contains an unfilled placeholder beginning with "COMPLETION NOTE: Update this field with..." or "PROGRESS NOTE: Update this field with...", resolve as OBE using this format:

```
OBE. Task Done.

[original note text preserved here unchanged]
```

Prepend the two-line header to the existing note. Do not delete the original note text.

Substantive completion notes: If a Done task already has a meaningful completion record in Notes, do not alter it unless a specific update is recommended based on the BLOG entry.

### Contextual Field Reassessment

Every field on every active task is subject to reassessment each morning. The BEAST table should reflect current reality, not original assumptions. Apply human-level judgment to reassess whether existing field values still accurately reflect reality. When recommending a field change not explicitly requested in the BLOG, briefly state the inference that supports it in the Reason field.

**Status reassessment:**
- In progress with no activity and BLOG implies stall: flag as Blocked or note the stall
- Not started with work clearly underway per BLOG: update to In progress
- Context implies task is no longer relevant: recommend Done or OBE with explanation

**Priority reassessment:**
- Low/Medium + BLOG describes urgency, stakeholder pressure, or blocking dependency: upgrade Priority
- High + BLOG indicates deferral or deprioritization: downgrade Priority

**Due Date reassessment:**
- Overdue + BLOG implies rescheduling: set new Due Date based on BLOG evidence
- No Due Date + BLOG establishes clear target: add it
- Due Date no longer realistic per BLOG: recommend revised date with stated basis

**Effort reassessment:**
- Multi-day + BLOG shows quick completion or reduced scope: revise downward
- 30 min + BLOG reveals higher complexity: revise upward
- Cancelled or OBE: set to 30 min unless actual work invested warrants otherwise

**Type reassessment:**
- Research + BLOG shows concrete output now being produced: consider Deliverable
- Action + BLOG shows it is blocked on a conversation or decision: consider Meeting

**Project reassessment:**
- Task assigned to one project + BLOG clearly indicates work belongs to a different workstream: update Project and note the change

### Duplicate Row Rules

Duplicate Task ID rows in Coda reads are data artifacts. Flag as advisories in FLAGS AND ISSUES. Treat the second (Done) row with more recent note history as canonical. Do not write duplicate rows.

### BEAST Output Format

Produce output in exactly four labeled sections using this header format:

```
[one blank line]
**====================SECTION HEADER====================**
[one blank line]
```

Do not produce any output before the first section header. Do not add commentary after the final section.

### BEAST Section 1: Morning Briefing

**====================MORNING BRIEFING====================**

Write a short paragraph of three to four sentences summarizing the state of the BEAST list as of this morning. Cover: how many tasks are active (Not started or In progress), how many are overdue based on Due Date versus today's date, and any high-priority items that need immediate attention. State today's date explicitly. Professional tone. No em dashes. Format all dates as D Mon YYYY.

### BEAST Section 2: Flags and Issues

**====================FLAGS AND ISSUES====================**

A bulleted list of every named task (rows with a BEAST-XXXX Task ID) that has one or more of the following problems. Do not evaluate child rows. One bullet per flagged task. For each bullet: Task ID, task name, flag type, one-sentence explanation.

Flag types:
- OVERDUE: Due Date is earlier than today's date and Status is not Done
- MISSING NOTES: Notes field is empty or blank for any task regardless of status
- COMPLETED WITHOUT NOTES: Status is Done but Notes contains only the original setup note with no completion record
- COMPLETION NOTE PLACEHOLDER UNFILLED: Status is Done but Notes still contains "COMPLETION NOTE: Update this field with..."
- PROGRESS NOTE PLACEHOLDER UNFILLED: Status is In progress but Notes still contains "PROGRESS NOTE: Update this field with..."
- STALE IN PROGRESS: Status is In progress with no Due Date set
- HIGH PRIORITY NOT STARTED: Priority is High, Status is Not started, Due Date is at or before today
- MISSING DUE DATE: Status is Not started or In progress and Due Date is blank

If no flags are found, write exactly: `No flags identified.`

### BEAST Section 3: Recommended Task Updates

**====================RECOMMENDED TASK UPDATES====================**

Based on the BLOG entry, produce a list of recommended changes grounded in something explicitly stated or clearly implied in the BLOG, or in the contextual field reassessment logic above. Do not invent tasks or updates without basis in the source material.

For each recommendation:
- Task ID: existing ID for updates/completions; next available BEAST-XXXX for new tasks
- Action: Add, Update, or Complete
- Task Name: exact text to use or confirm in the Name field
- Field Changes: every column that needs to be set or updated, listed as Field: Value
- Reason: one sentence explaining what in the BLOG entry drives this recommendation

Group under three sub-labels: New Tasks to Add, Tasks to Update, and Tasks to Complete. If no recommendations apply to a group, write exactly: None.

### BEAST Section 4: Today's Priority List

**====================TODAY'S PRIORITY LIST====================**

A sequenced list of five to seven most important tasks to work on today, drawn from the full BEAST table after applying recommended updates. Sequence: overdue items first, then due today, then due this week, then by priority within each tier.

For each task:
```
[Task ID] [Task Name] -- [Project] -- [one clause of context explaining why it is on the list today]
```

### Standing Rules Summary

| Rule | Standard |
|---|---|
| Status capitalization | "Not started", "In progress", "Done", "Blocked" |
| Effort values | "30 min", "Half day", "Full day", "Multi-day" |
| Type values | "Action", "Meeting", "Research", "Deliverable", "Admin" |
| Due Date format | D Mon YYYY display; YYYY-MM-DD for MCP writes |
| OBE note format | Prepend "OBE. Task Done.\n\n" to existing note; preserve original text |
| New Task ID format | Continue BEAST-XXXX sequence from highest existing ID in table |
| Child rows | No Task ID; excluded from all flag checks and writes |
| Project names | Proper nouns; exact capitalization; never all caps |
| Field reassessment | All fields on active tasks are subject to reassessment each morning |
| Parent / Subitems | NEVER include in any write operation; require manual assignment in Coda |
| Duplicate rows | Flag as advisory; treat second Done row as canonical; do not write duplicates |
| BLOG authority | BEAST records are only modified when BLOG evidence directly supports the change |
| Sensitive Items | Section 7 is NEVER written to Coda under any circumstances |
| Write confirmation | ALL Coda writes require explicit human confirmation before execution |
