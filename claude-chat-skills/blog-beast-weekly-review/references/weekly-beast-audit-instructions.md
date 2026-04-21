# Weekly BEAST Audit Instructions

This file defines the seven integrity audit checks the weekly review runs against the BEAST task table, plus the detection logic, outcome classification, and write behavior for each.

## Core principle

The weekly audit exists because daily reconciliation is reactive and present-focused. It catches things today. It does not systematically look backward for:

- Commitments made in prior days that never became tracked tasks
- Tasks that have been quietly sitting in the same state for too long
- Narrative completions that never got reflected in BEAST state
- Patterns in how work is being categorized or prioritized

The audit is not punitive. It is hygiene. Its goal is that nothing Brady committed to or completed is lost, and that BEAST accurately reflects the state of his work.

## Outcome classification

Every audit finding resolves to one of three outcomes:

**Auto-apply** — The audit has high confidence in both the detection and the correct resolution. A BEAST write is proposed (gated by the Stage 5 confirmation). The affected row gets a dated retroactive note.

**Flag** — The audit detects a likely issue but cannot safely determine the right action. Surfaced to Brady in Section 8 and in the Stage 5 diff under a "Flagged" header. No write is proposed. Brady handles manually.

**Observe** — The audit detects a pattern (category drift, priority inversion) rather than a specific row-level issue. Surfaced in Section 8 as an observation. No row-level write.

## The seven checks

### Check 1: Promised but not tracked

**Detection.** Scan each daily entry's Reviewed Notes, Polished Summary, Key Wins, and Blockers for commitment phrases:

- First-person future: "I'll...", "I will...", "I need to...", "I'm going to..."
- Next-step language: "next step is...", "follow-up is...", "action item:..."
- Assignment: "committed to...", "promised...", "owe..."

For each commitment phrase extracted, attempt to match it to an existing BEAST row by:

1. Exact or near-exact name match
2. Keyword overlap with Name or Notes fields (3+ content words)
3. Project + action verb alignment

If no match found, the commitment is promised-but-not-tracked.

**Outcome classification.**

- If the commitment is specific, time-bounded, and has clear scope → **Flag** (let Brady confirm before adding to BEAST, since auto-creating tasks from narrative is high-risk for false positives)
- If vague or aspirational ("should probably look into X") → **Observe** only, noted in Section 8

**Never auto-create BEAST rows from narrative extraction.** The false-positive risk is too high. Always flag for Brady.

### Check 2: Stalled tasks

**Detection.** Any BEAST row meeting all of the following:

- Status in {`Not started`, `In progress`, `Blocked`}
- Last modification date more than 5 working days ago (override configurable via invocation: "stalled threshold 7")
- Not a Parent row whose Subitems are actively moving (if child tasks updated within threshold, parent is not stalled)

If Coda's API response does not expose a reliable last-modification timestamp at the row level, fall back to: any row in the above statuses that was not mentioned in any daily entry's Reviewed Notes during the review window.

**Outcome classification.**

- `Blocked` status with external dependency noted in Notes → **Observe** (Brady knows; surfacing it anyway in Section 8)
- `Not started` or `In progress` with no recent mention → **Flag** (Brady decides: kill, defer, or escalate)
- No auto-applies for this check

### Check 3: Completed in narrative but still open in BEAST

**Detection.** Scan each daily entry's Key Wins and Polished Summary for completion language:

- "Completed...", "Finished...", "Submitted...", "Shipped...", "Delivered...", "Closed out..."
- "Done with...", "Wrapped...", "Signed off on..."

For each completion phrase, attempt to match to an existing BEAST row (same matching logic as Check 1). For matches where the BEAST row Status is not `Done`:

**Outcome classification.**

- Strong match (name similarity high, clear completion verb, no ambiguity) → **Auto-apply**: set Status = `Done`, append retroactive note
- Weak match or ambiguous completion ("made good progress on X" is not completion) → **Flag**

Auto-apply retroactive note format:

```
Retroactive completion via weekly review (<D Mon YYYY of review run>): Daily entry for <D Mon YYYY of completion> recorded this as completed. Status updated retroactively.
```

Preserve existing Notes content above the `---` separator per the SKILL.md Stage 7 pattern.

### Check 4: Missed due dates

**Detection.** Any BEAST row where:

- Due Date is before the start of the review window (i.e., due date passed before the week being reviewed even began, or passed during the week)
- Status is not `Done`

**Outcome classification.**

- If the row has movement during the review window (appeared in daily Reviewed Notes or has recent mod timestamp) → **Observe** (work is in flight, just late)
- If no movement and status is `Not started` → **Flag** as likely abandoned, Brady decides
- If no movement and status is `In progress` or `Blocked` → **Flag** with suggestion to either update due date or escalate

No auto-applies. Missed due dates require judgment about whether to extend, drop, or escalate — never safe to auto-decide.

### Check 5: Orphaned subtasks

**Detection.** Any BEAST row where:

- The Parent (`c-ONPz07rw_J`) lookup references a rowId that either (a) does not exist in the current table, or (b) exists but has Status = `Done`

**Outcome classification.**

- Parent rowId does not exist (data integrity issue) → **Flag**, Brady resolves manually (likely a Coda migration artifact)
- Parent is Done and subtask is also Done → **Observe** only (clean state, just surfacing)
- Parent is Done but subtask is `Not started`, `In progress`, or `Blocked` → **Flag** (Brady decides: complete the subtask, reparent it, or cancel it)

No auto-applies.

### Check 6: Category drift

**Detection.** Count the distribution of daily entry Categories across the review window. Calculate:

- Total daily entries with non-empty Category: N
- Entries with Category in {ambiguous, low-signal categories — currently `Delivery` and `Strategy` are broad catchalls}: M
- Entries with no Category or with a category that appears only once in the week: K

If (M + K) / N > 0.3, flag category drift.

Also surface the actual category distribution in Section 8 regardless of threshold:

```
Category distribution:
- Strategy: 2 days
- Delivery: 2 days
- Team & Culture: 1 day
```

**Outcome classification.** Always **Observe**. Category choices are Brady's judgment call; the audit just surfaces the pattern.

### Check 7: Priority inversion

**Detection.** Compare BEAST row activity across the review window:

- `Priority = High` rows with no movement (no status change, no note update, no mention in daily entries): `H_stalled`
- `Priority = Low` rows that moved to `Done` during the window: `L_done`

Priority inversion is flagged if `H_stalled > 0` AND `L_done > 0`.

**Outcome classification.** Always **Observe**. The audit reports the counts and lists the specific rows, but does not recommend action. Brady decides whether the inversion was intentional (quick-wins strategy, blocked high-priority items) or a warning sign.

Example Section 8 entry:

```
Priority inversion detected:
- 3 High-priority tasks had no movement this week (BEAST-0104, BEAST-0112, BEAST-0118.2)
- 5 Low-priority tasks were completed this week
```

## Write behavior summary

| Check | Auto-apply | Flag | Observe |
|-------|-----------|------|---------|
| 1. Promised but not tracked | Never | Specific commitments | Vague commitments |
| 2. Stalled tasks | Never | Not started / In progress | Blocked with external dep |
| 3. Completed in narrative | Strong matches | Weak/ambiguous matches | Never |
| 4. Missed due dates | Never | No movement | With movement |
| 5. Orphaned subtasks | Never | Broken parent, Done parent + open child | Done parent + Done child |
| 6. Category drift | Never | Never | Always |
| 7. Priority inversion | Never | Never | Always |

Only Check 3 produces auto-applied writes. All other checks either flag or observe. This asymmetry is intentional: the audit's job is to surface, not to decide.

## Confirmation gate presentation

When showing the Stage 5 diff, group corrections separately from normal BEAST operations:

```
=== New Tasks ===
(standard new-row format)

=== Updates ===
(standard field-diff format)

=== Completions ===
(standard OBE/substantive format)

=== Corrections (from weekly audit) ===
BEAST-0087 | "Submit JFT SDP scenario catalog v1.1 to PDO"
  Detected: Daily entry for 27 Mar 2026 recorded this as completed; BEAST still shows In progress.
  Changes:
    Status: In progress → Done
    Notes: <existing> + "Retroactive completion via weekly review (20 Apr 2026): ..."
```

If Brady rejects a specific correction during the gate, drop just that correction and proceed with the others. Re-present the diff if the change is non-trivial.

## Error handling

- If Stage 2's BEAST read is incomplete (pagination error, partial table), halt the entire audit. Do not run checks against partial data.
- If Stage 1's daily entries are missing days, run the audit on the available data but note the gap in Section 8 — audit fidelity is lower when daily coverage is incomplete.
- If a row's Parent lookup points to a rowId not in the current read (possible with pagination), re-read the missing rowId explicitly before flagging as orphaned.
