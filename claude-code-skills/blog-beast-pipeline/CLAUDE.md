# blog-beast-pipeline

Automated daily BLOG and BEAST pipeline. Paste raw OneNote notes into Claude Code and everything else happens automatically: BLOG processing, Coda write, BEAST pull, BEAST processing, Coda upsert, final report.

## Recommended Model

Run this pipeline with **Sonnet** at **normal effort**. The pipeline follows highly structured, rule-based instructions. Sonnet handles this efficiently. Opus is unnecessary and significantly slower.

## Trigger Phrases

The pipeline activates when the user says any of the following, followed by pasted raw daily work notes:

- `run pipeline`
- `run BLOG and BEAST`
- `run blog beast`
- `process my notes`
- `morning briefing`
- `run morning updates`
- `run BEAST`
- `run BLOG`
- `process today's notes`

Typical usage: the user types `run pipeline:` followed by the date header and pasted notes.

## Mode

MODE: PRODUCTION

CRITICAL EXECUTION RULES:
- Run the ENTIRE pipeline as one uninterrupted sequence.
- Do NOT output any text to the user until the Final Report in Step 6.
- Do NOT pause, ask for confirmation, or wait for input between steps.
- Process BLOG and BEAST internally. Run all scripts via Bash calls.
- The user should see ONLY the Final Report as output. Nothing else.
- The scripts handle retryable errors (SSL, connection, timeout, 429/502/503/504) internally with one automatic retry. If a script still fails after its internal retry, do not retry from Claude Code -- report the error in the Final Report.

Execution flow:
1. Process BLOG internally (no output)
2. Run blog_to_coda.py AND beast_from_coda.py via Bash (parallel if possible)
3. Process BEAST internally using the CSV output (no output)
4. Run beast_to_coda.py via Bash
5. Output the Final Report (this is the ONLY user-visible output)

---

## Pipeline Flow

When the user pastes raw daily work notes, execute these steps in order:

### Step 1: BLOG Processing
Process the pasted notes through the BLOG Processing Specification below. Output all seven sections plus the Coda field checklist in a single pass.

The date for the entry comes from the notes themselves (the day being documented), not from the system date. The user typically runs this the morning after the work day.


### Step 2: Write BLOG Entry to Coda
Construct a JSON object from the BLOG output with these keys:
- date: ISO format YYYY-MM-DD (from the date in the notes)
- reviewed_notes: Section 1 text
- polished_summary: Section 2 text
- executive_bullets: Section 3 text
- key_wins: Section 4 text
- blockers: Section 5 text
- category: Section 6 text (single category name)
- entry_type: "Daily"
- status: "Draft"

NEVER include Section 7 (Sensitive Items) in this JSON.

Write the JSON to a temp file using the Write tool, then run:
`python scripts/blog_to_coda.py --input <temp_file_path>`

The script strips markdown formatting to plain text for Coda (the API does not render markdown). Headings become UPPERCASE, bold markers are removed, dashes are preserved.


### Step 3: Extract BEAST Table from Coda
Run: `python scripts/beast_from_coda.py`

Capture the 12-column CSV output (stdout). This is the full To Do List with all rows including child rows. Due dates are converted from ISO to D Mon YYYY format for BEAST processing.


### Step 4: BEAST Processing
Process the extracted CSV plus the BLOG output from Step 1 through the BEAST Processing Specification below. Today's date for BEAST processing is the system date (the morning the pipeline runs).

Produce all four sections: Morning Briefing, Flags and Issues, Recommended Task Updates (with import CSV), and Today's Priority List.


### Step 5: Write BEAST Updates to Coda
Extract the import CSV block from the BEAST output (the block labeled "IMPORT CSV -- CHANGED AND NEW ROWS ONLY"). This is a 10-column CSV with header row.

Write the import CSV to a temp file using the Write tool, then run:
`python scripts/beast_to_coda.py --input <temp_file_path>`

The script validates field values, converts dates to ISO, skips child rows, and upserts using Task ID as the key column.


### Step 6: Final Report
Output a summary including:
- BLOG entry confirmation: date, category, row status
- BEAST updates confirmation: count of rows upserted, any new tasks created
- If new tasks were created: remind that Parent and Subitems must be manually assigned in Coda
- BEAST Section 2 (Flags and Issues): any items requiring attention
- BEAST Section 4 (Today's Priority List): the sequenced task list for the day
- BLOG Section 7 (Sensitive Items): ALWAYS display this section explicitly. These are never written to Coda. If items exist, call them out clearly. If none, state "None identified."

---

## Author Context

Brady Redfearn is a Senior Strategist in Program Development at Western Governors University (WGU). His title, team, and domain context are established. No need to prompt for context each session.

Common acronyms: WGU (Western Governors University), UPL (University Program Leader), PD (Program Development), LR (Learning Resources), SDP (Supplemental Digital Product), JFT (Just for Teachers), PES (Program Evaluation & Strategy), BEAST (Brady's Execution, Action, and Strategy Tasks), BLOG (Brady's Learnings, Observations, and Growth)

---

## Coda Schema Reference

### Doc
- Doc ID: dHXfr0V468
- Doc Name: Brady's Coda Playground

### Daily Log Table
- Table ID: grid-ty2WGfh4qa
- Columns:
  - Date: c-oiaBDBstH1 (date)
  - Reviewed Notes: c-DXM4h2B28G (canvas)
  - Polished Summary: c-FIWz6AEhwd (text)
  - Executive Bullets: c-WSCAvrHbnz (text)
  - Key Wins: c-QuKWx0lwGp (text)
  - Blockers: c-bT-C79ocGH (text)
  - Category: c-CA6Nwa3A2N (select)
  - Status: c-pR0VmtQ5AV (select)
  - Entry Type: c-7IZ-UJNjXG (select)

### Complete To Do List (BEAST) Table
- Table ID: grid-M-DmPD4U5x
- Columns:
  - Task ID: c-ImEDreEoEA (text)
  - Name: c-MBRsPfbd6d (text)
  - Status: c-zH_C1i-smP (select)
  - Priority: c-g-kRN3Y2aS (select)
  - Due Date: c-NP39SR6C8D (date)
  - Type: c-Z_PWA6_-Bb (select)
  - Project: c-W3gb8_ca2O (select)
  - Effort: c-RdNqDL9akn (select)
  - Notes: c-ioDsMHggmZ (text)
  - Link: c-wuGVeM0y7z (link)
  - Parent: c-ONPz07rw_J (lookup, manual assignment required)
  - Subitems: c-RRrt1LG5D9 (lookup, calculated display only, manual assignment required)

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

CRITICAL: Section 7 is NEVER written to Coda. It is displayed in the Claude Code terminal only.

### Usage Notes

- Sections 1 through 6: Map to corresponding Coda Daily Log columns
- Coda Field Checklist: Confirm Entry Type is Daily and move Status from Draft to Published after review
- Section 7: Displayed in terminal only. NEVER written to Coda under any circumstances
- Thin days are fine: If the notes are brief, produce proportionally brief output. Do not pad
- Multiple days at once: If the user pastes notes for more than one day, process each day as a separate complete output, clearly labeled with the date

### Formatting Standards

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

This specification processes two inputs -- a full BEAST CSV export and the BLOG entry from Step 1 -- and produces a structured four-section morning briefing plus a Coda import CSV containing only changed and new rows.

### Inputs

- **BEAST CSV** (required): Full Coda table export from beast_from_coda.py. Contains 12 columns: Task ID, Name, Status, Priority, Due Date, Type, Project, Effort, Notes, Link, Parent, Subitems.
- **BLOG entry** (required): The output from the BLOG processor in Step 1. This is the authoritative source for task status updates. BEAST records are only modified when BLOG evidence directly supports the change.
- **Today's date**: Use the system date automatically.

### Table Structure

The import CSV uses exactly these 10 columns in this order:

```
Task ID, Name, Status, Priority, Due Date, Type, Project, Effort, Notes, Link
```

Parent and Subitems are Coda-native hierarchy columns. They appear in every export but must NEVER be included in the import CSV. Coda manages them automatically. Note: Parent and Subitems require manual assignment in Coda after new tasks are created.

### Field Value Standards

All field values must match the exact spelling, capitalization, and punctuation shown below.

**Status** (exact values only):
- Not started
- In progress
- Done
- Blocked

**Priority** (exact values only):
- High
- Medium
- Low

**Effort** (exact values only):
- 30 min
- Half day
- Full day
- Multi-day

**Type** (exact values only):
- Action
- Meeting
- Research
- Deliverable
- Admin

**Project** -- treat as a proper noun. Use exact capitalization from the BEAST table. Never convert to all caps. Known project names:
- Cicada
- Networking
- Onboarding
- Team/Ops

Add new project names as they appear. Use exact spelling from the BLOG or BEAST table. Accept any non-empty string; warn if a value has not been seen before.

**Due Date** -- D Mon YYYY, no zero-padding on single-digit days.
Examples: 6 Mar 2026, 9 Mar 2026, 13 Mar 2026
Never write: 06 Mar 2026 or 09 Mar 2026
Note: When writing to Coda via beast_to_coda.py, dates are converted to ISO format (YYYY-MM-DD) for the API. The D Mon YYYY format is used in the BEAST processing output and import CSV only.

**Task ID** -- format: BEAST-XXXX with four-digit zero-padded number (e.g., BEAST-0027). New tasks continue the numeric sequence from the highest existing Task ID in the current export. Never use a temporary naming scheme.

### Child Row Rules

Parent tasks carry a BEAST-XXXX Task ID. Child rows nested under a parent have no Task ID.

- Do not assign Task IDs to child rows.
- Do not evaluate child rows for flags.
- Do not include child rows in the import CSV.
- The parent task row is the unit of tracking.

### Notes Standards

Every active task (Not started or In progress) must have substantive notes at all times. Notes must reflect current status, progress, blockers, and next actions.

Note format for datestamped entries:

```
BLOG DD MMM: [entry] | STATUS UPDATE DD MMM: [update]
```

New dated entries are prepended to existing notes, never overwriting prior history. Semicolons replace commas within CSV note fields to avoid parsing conflicts.

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

Duplicate Task ID rows in Coda exports are export artifacts. Flag as advisories in FLAGS AND ISSUES. Treat the second (Done) row with more recent note history as canonical. Do not re-import duplicates.

### Output Format

Produce output in exactly four labeled sections using this header format:

```
[one blank line]
**====================SECTION HEADER====================**
[one blank line]
```

Do not produce any output before the first section header. Do not add commentary after the final section.

### Section 1: Morning Briefing

**====================MORNING BRIEFING====================**

Write a short paragraph of three to four sentences summarizing the state of the BEAST list as of this morning. Cover: how many tasks are active (Not started or In progress), how many are overdue based on Due Date versus today's date, and any high-priority items that need immediate attention. State today's date explicitly. Professional tone. No em dashes. Format all dates as D Mon YYYY.

### Section 2: Flags and Issues

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

### Section 3: Recommended Task Updates

**====================RECOMMENDED TASK UPDATES====================**

Based on the BLOG entry, produce a list of recommended changes grounded in something explicitly stated or clearly implied in the BLOG, or in the contextual field reassessment logic above. Do not invent tasks or updates without basis in the source material.

For each recommendation:
- Task ID: existing ID for updates/completions; next available BEAST-XXXX for new tasks
- Action: Add, Update, or Complete
- Task Name: exact text to use or confirm in the Name field
- Field Changes: every column that needs to be set or updated, listed as Field: Value
- Reason: one sentence explaining what in the BLOG entry drives this recommendation

Group under three sub-labels: New Tasks to Add, Tasks to Update, and Tasks to Complete. If no recommendations apply to a group, write exactly: None.

After listing all recommendations, produce a ready-to-import CSV block. Label it clearly:

```
IMPORT CSV -- CHANGED AND NEW ROWS ONLY
```

Use the 10-column import order: Task ID, Name, Status, Priority, Due Date, Type, Project, Effort, Notes, Link. Include a header row. Do not include Parent, Subitems, or export-only columns. Do not include unchanged rows.

CSV formatting rules:
- Task names containing commas must be wrapped in double quotes
- Semicolons replace commas within note fields to avoid parsing conflicts

### Section 4: Today's Priority List

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
| Due Date format | D Mon YYYY, no zero-padding (e.g., 6 Mar 2026) |
| OBE note format | Prepend "OBE. Task Done.\n\n" to existing note; preserve original text |
| New Task ID format | Continue BEAST-XXXX sequence from highest existing ID in export |
| Child rows | No Task ID; excluded from all flag checks and import CSV |
| Project names | Proper nouns; exact capitalization; never all caps |
| Import CSV columns | 10 columns only: Task ID, Name, Status, Priority, Due Date, Type, Project, Effort, Notes, Link |
| Field reassessment | All fields on active tasks are subject to reassessment each morning |
| Parent / Subitems | Export-only columns; never include in import CSV; require manual assignment in Coda |
| Duplicate rows | Flag as advisory; treat second Done row as canonical; do not re-import |
| BLOG authority | BEAST records are only modified when BLOG evidence directly supports the change |
