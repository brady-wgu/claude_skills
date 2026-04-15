# BEAST Field Standards

All field values must match the exact spelling, capitalization, and punctuation shown below. These are the authoritative values for the BEAST (Complete To Do List) table. Any value not matching these standards is flagged as a warning.

---

## Status (exact values only)
- Not started
- In progress
- Done
- Blocked

## Priority (exact values only)
- High
- Medium
- Low

## Effort (exact values only)
- 30 min
- Half day
- Full day
- Multi-day

## Type (exact values only)
- Action
- Meeting
- Research
- Deliverable
- Admin

## Project
Treat as a proper noun. Use exact capitalization from the BEAST table. Never convert to all caps.

**Known project names (as of 14 APR 2026):**
- Cicada
- Networking
- Onboarding
- Team/Ops
- JFT SDP
- Learning Resources Analytics
- Math Supplemental Content

Add new project names as they appear in the BLOG or BEAST table. Use exact spelling. Accept any non-empty string but warn if a value has not been seen before.

## Task ID
Format: `BEAST-XXXX` with four-digit zero-padded number.
Examples: BEAST-0001, BEAST-0027, BEAST-0130

New tasks continue the numeric sequence from the highest existing Task ID in the current table read. Never use a temporary naming scheme. Never reuse a Task ID.

## Due Date
Format in BEAST processing output: `D Mon YYYY` (no zero-padding on single-digit days)
Examples: 6 Mar 2026, 9 Mar 2026, 13 Mar 2026
Never write: 06 Mar 2026 or 09 Mar 2026

Format for Coda MCP writes: ISO `YYYY-MM-DD`
Example: 2026-03-06, 2026-03-13

## Daily Log Entry Type Values
- "Daily" (from activity-daily)
- "Weekly" (from activity-weekly)
- "Monthly Digest" (from activity-monthly)
- "Quarterly Review" (from activity-quarterly)
- "Annual Review" (from activity-annual)

## Daily Log Category Values
- Onboarding
- UPL
- Intake
- Initiative
- People & Network
- Team & Culture
- Definitions & Concepts
- Tools & Access
- Strategy
- Admin

Higher-level entries (Weekly through Annual) always use "Admin".

## Daily Log Status Values
- Draft (default for all new entries)
- Published (set after review)

---

## Child Row Rules

Parent tasks carry a `BEAST-XXXX` Task ID. Child rows nested under a parent have no Task ID.

- Do not assign Task IDs to child rows
- Do not evaluate child rows for flags
- Do not include child rows in any write operation
- The parent task row is the unit of tracking

## Notes Standards

Every active task (Not started or In progress) must have substantive notes at all times. Notes must reflect current status, progress, blockers, and next actions.

**Datestamped entry format:**
```
BLOG DD MMM: [entry] | STATUS UPDATE DD MMM: [update]
```

New dated entries are prepended to existing notes, never overwriting prior history.

**OBE resolution for Done tasks with unfilled placeholders:**
If a Done task's Notes field still contains an unfilled placeholder beginning with "COMPLETION NOTE: Update this field with..." or "PROGRESS NOTE: Update this field with...", resolve as OBE:

```
OBE. Task Done.

[original note text preserved here unchanged]
```

Prepend the two-line header. Do not delete the original note text.

## Duplicate Row Rules

Duplicate Task ID rows in Coda reads are export artifacts. Flag as advisories. Treat the second (Done) row with more recent note history as canonical. Do not write duplicate rows.

## Contextual Field Reassessment

Every field on every active task is subject to reassessment each morning. The BEAST table should reflect current reality, not original assumptions. Apply human-level judgment. When recommending a field change not explicitly requested in the BLOG, briefly state the inference that supports it.

**Status reassessment:**
- In progress with no activity and BLOG implies stall: flag as Blocked or note the stall
- Not started with work clearly underway per BLOG: update to In progress
- Context implies task is no longer relevant: recommend Done or OBE with explanation

**Priority reassessment:**
- Low/Medium + BLOG describes urgency, stakeholder pressure, or blocking dependency: upgrade
- High + BLOG indicates deferral or deprioritization: downgrade

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
