# Monthly BEAST Audit Instructions

This file defines the ten integrity audit checks the monthly review runs against the BEAST task table, plus the detection logic, outcome classification, and write behavior for each.

## Core principle

The monthly audit exists because daily and weekly cadences are both forward-looking in character. Daily catches things today. Weekly catches things across the past Mon-Fri window. Neither systematically looks across a full calendar month for:

- Commitments that have persisted across multiple weekly audits without resolution
- Tasks stalled across the entire month rather than just the past week
- Project-level velocity imbalances (more work opened than closed)
- Gaps in weekly audit coverage that only become visible from Daily re-derivation

The monthly audit is not punitive. Like the weekly, it is hygiene. Its job is that nothing Brady committed to, stalled on, or completed is lost, and that BEAST accurately reflects the state of his work at month's end.

## Outcome classification

Every audit finding resolves to one of three outcomes:

**Auto-apply** — The audit has high confidence in both the detection and the correct resolution. A BEAST write is proposed (gated by the Stage 6 confirmation). The affected row gets a dated retroactive note.

**Flag** — The audit detects a likely issue but cannot safely determine the right action. Surfaced to Brady in Section 8 and in the Stage 6 diff under a "Flagged" header. No write is proposed. Brady handles manually.

**Observe** — The audit detects a pattern rather than a specific row-level issue. Surfaced in Section 8 as an observation. No row-level write.

## The ten checks

Checks 1-7 are carried from the weekly audit, scoped to the month instead of the week. Checks 8-10 are monthly-specific.

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

**Monthly cadence adjustment.** For items flagged by this check, cross-reference against the Weekly BLOG audit findings in Stage 2's data. If the same commitment was already flagged in a weekly audit and remains unmatched to BEAST, mark it as "Persistent: flagged in <N> weekly audits without resolution" — this moves the finding's severity up and may warrant stronger escalation language in Section 8.

**Outcome classification.**

- If the commitment is specific, time-bounded, and has clear scope → **Flag**
- If vague or aspirational → **Observe** only, noted in Section 8
- Never auto-create BEAST rows from narrative extraction.

### Check 2: Stalled tasks

**Detection.** Any BEAST row meeting all of the following:

- Status in {`Not started`, `In progress`, `Blocked`}
- Last modification date more than 5 working days ago (override configurable via invocation: "stalled threshold 7")
- Not a Parent row whose Subitems are actively moving

If Coda's API response does not expose a reliable last-modification timestamp at the row level, fall back to: any row in the above statuses that was not mentioned in any daily entry's Reviewed Notes during the review window.

**Outcome classification.**

- `Blocked` status with external dependency noted in Notes → **Observe**
- `Not started` or `In progress` with no recent mention → **Flag**
- No auto-applies for this check

Note: Check 2 and Check 8 have the same detection threshold (5 working days) but different scope. Check 2 covers any row that has been stalled at some point during the month. Check 8 covers rows that were stalled for the entire month (higher severity).

### Check 3: Completed in narrative but still open in BEAST

**Detection.** Scan each daily entry's Key Wins and Polished Summary for completion language:

- "Completed...", "Finished...", "Submitted...", "Shipped...", "Delivered...", "Closed out..."
- "Done with...", "Wrapped...", "Signed off on..."

For each completion phrase, attempt to match to an existing BEAST row. For matches where the BEAST row Status is not `Done`:

**Outcome classification.**

- Strong match (name similarity high, clear completion verb, no ambiguity) → **Auto-apply**: set Status = `Done`, append retroactive note
- Weak match or ambiguous completion → **Flag**

Auto-apply retroactive note format:

```
Retroactive completion via monthly review (<D Mon YYYY of review run>): Daily entry for <D Mon YYYY of completion> recorded this as completed. Status updated retroactively.
```

Preserve existing Notes content above the `---` separator per the SKILL.md Stage 8 pattern.

**Monthly cadence consideration.** If a completion was already auto-applied by a weekly audit earlier in the month, the monthly skill will see Status = `Done` and not re-flag it. No duplicate corrections.

### Check 4: Missed due dates

**Detection.** Any BEAST row where:

- Due Date is before the start of the review window (the first day of the target month) or during the month
- Status is not `Done`

**Outcome classification.**

- Row with movement during the window → **Observe**
- `Not started` with no movement → **Flag** as likely abandoned
- `In progress` or `Blocked` with no movement → **Flag** with suggestion to update due date or escalate

No auto-applies.

### Check 5: Orphaned subtasks

**Detection.** Any BEAST row where:

- The Parent (`c-ONPz07rw_J`) lookup references a rowId that either (a) does not exist in the current table, or (b) exists but has Status = `Done`

**Outcome classification.**

- Parent rowId does not exist → **Flag** as data integrity issue
- Parent is Done and subtask is also Done → **Observe** only
- Parent is Done but subtask is `Not started`, `In progress`, or `Blocked` → **Flag**

No auto-applies.

### Check 6: Category drift

**Detection.** Count the distribution of daily entry Categories across the full review window (the calendar month).

- Total daily entries with non-empty Category: N
- Entries with Category in {ambiguous, low-signal categories — currently `Delivery` and `Strategy` are broad catchalls}: M
- Entries with no Category or with a category that appears only once in the month: K

If (M + K) / N > 0.3, flag category drift.

Surface the actual category distribution in Section 8 regardless of threshold:

```
Monthly category distribution:
- Strategy: 8 days
- Delivery: 6 days
- Team & Culture: 3 days
- Uncategorized: 2 days
```

**Outcome classification.** Always **Observe**.

### Check 7: Priority inversion

**Detection.** Compare BEAST row activity across the full review window:

- `Priority = High` rows with no movement throughout the month: `H_stalled`
- `Priority = Low` rows that moved to `Done` during the month: `L_done`

Priority inversion is flagged if `H_stalled > 0` AND `L_done > 2`. (Higher threshold than weekly's `L_done > 0` to account for natural quick-win volume in a longer window.)

**Outcome classification.** Always **Observe**. Report the counts and list the specific rows.

Example Section 8 entry:

```
Priority inversion detected for April 2026:
- 4 High-priority tasks had no movement this month (BEAST-0104, BEAST-0112, BEAST-0118.2, BEAST-0121)
- 12 Low-priority tasks were completed this month
```

### Check 8: Long-stalled tasks (monthly-specific)

**Detection.** Any BEAST row meeting all of the following:

- Status in {`Not started`, `In progress`, `Blocked`}
- Last modification date more than 5 working days ago AND before the start of the target month
- Not a Parent row whose Subitems moved during the month

This check is stricter than Check 2: it captures tasks that were stalled at the start of the month, remained stalled throughout, and are still stalled at month's end. The 5-working-day threshold is the same, but combined with the month-boundary check, this surfaces persistent stalls only.

**Outcome classification.**

- Any qualifying row → **Flag** with recommendation to either kill, defer with new Due Date, or escalate
- No auto-applies

In Section 8, list qualifying rows under a `**Long-stalled tasks**` heading with Task ID, Name, current Status, and the last mod date if available.

### Check 9: Project velocity drift (monthly-specific)

**Detection.** For each distinct `Project` value in BEAST, count:

- `opened_in_window`: rows where the row was created during the month (if creation timestamp available) OR rows with Status in {`Not started`, `In progress`, `Blocked`} that were first mentioned in a daily entry during the month
- `closed_in_window`: rows where Status transitioned to `Done` during the month

Calculate per-project velocity ratio: `closed / opened`.

Flag projects where:

- `opened_in_window >= 3` AND
- `closed_in_window / opened_in_window < 0.5`

This means a project added at least 3 new pieces of work during the month but closed fewer than half of them.

**Outcome classification.** Always **Observe**. Report per-project opened/closed counts in Section 8:

```
Monthly project velocity:
- JFT SDP: opened 7, closed 4, ratio 0.57 (OK)
- Calculus Vendors: opened 12, closed 3, ratio 0.25 (FLAGGED: opened-to-closed imbalance)
- Blog/Beast Automation: opened 4, closed 5, ratio 1.25 (net reduction)
- Document Style Skill: opened 2, closed 2, ratio 1.00 (steady state)
```

Projects with fewer than 3 openings in the month do not get a ratio printed (noise threshold).

### Check 10: Promise decay (monthly-specific)

**Detection.** Dual-source detection using both Weekly audit findings and Daily re-derivation:

**Source A — Weekly audits.** From Stage 2's Weekly BLOG data, parse each Weekly row's Blockers column for the `## Integrity Audit` section. Extract commitments listed in the `### Flagged for Manual Attention` and `### Auto-Applied Corrections` sub-sections across every Weekly in the month.

Build a commitment fingerprint set: {task description keywords, Project, first week flagged}.

For each commitment in the set:
- Check current BEAST state for a matching row (using the same matching logic as Check 1)
- If no matching BEAST row exists or the match exists but has Status in {`Not started`, `In progress`, `Blocked`} → commitment has decayed

**Source B — Daily re-derivation.** Independently run Check 1 logic across the full month's daily entries, producing a list of unresolved commitments derived from the narrative.

**Merge.**

- Items in Source A set that are still unresolved → **Confirmed promise decay**. Report in Section 8 with week-count: "Flagged in 3 of 4 weekly audits, still unresolved."
- Items in Source B set but NOT in Source A set → **Potential weekly audit coverage gap**. The Daily-derived signal caught something the weekly cadence missed. Report in Section 8 under a `**Weekly Audit Coverage Gaps**` sub-heading so Brady knows to sanity-check the weekly skill.
- Items in Source A set that now have a matching `Done` BEAST row → resolved, no action.

**Outcome classification.**

- Confirmed promise decay (Source A, unresolved across multiple weeks) → **Flag**
- Weekly audit coverage gap (Source B item missing from Source A) → **Flag** with coverage-gap labeling
- No auto-applies. Promise decay is always a judgment call — Brady decides whether to add the task, dismiss it, or escalate.

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
| 8. Long-stalled (monthly) | Never | Always | Never |
| 9. Project velocity drift | Never | Never | Always |
| 10. Promise decay | Never | Confirmed decay + coverage gaps | Never |

Only Check 3 produces auto-applied writes at the monthly cadence, same as weekly. All other checks either flag or observe. The monthly-specific checks (8-10) surface patterns that require Brady's judgment to act on.

## Confirmation gate presentation

When showing the Stage 6 diff, group corrections separately from normal BEAST operations:

```
=== New Tasks ===
(standard new-row format)

=== Updates ===
(standard field-diff format)

=== Completions ===
(standard OBE/substantive format)

=== Corrections (from monthly audit) ===
BEAST-0087 | "Submit JFT SDP scenario catalog v1.1 to PDO"
  Detected: Daily entry for 12 Apr 2026 recorded this as completed; BEAST still shows In progress.
  Changes:
    Status: In progress → Done
    Notes: <existing> + "Retroactive completion via monthly review (4 May 2026): ..."
```

Monthly-specific findings (Checks 8, 9, 10) do not appear in the diff because they produce flags and observations only, not writes. They are only reflected in the Monthly BLOG Section 8.

If Brady rejects a specific correction during the gate, drop just that correction and proceed with the others. Re-present the diff if the change is non-trivial.

## Error handling

- If Stage 3's BEAST read is incomplete (pagination error, partial table), halt the entire audit. Do not run checks against partial data.
- If Stage 1's daily entries are missing days, run the audit on the available data but note the gap in Section 8 — audit fidelity is lower when daily coverage is incomplete.
- If Stage 2's Weekly BLOG data is incomplete (missing Weekly entries for weeks overlapping the month), run Check 10 using Source B only and note in Section 8 that promise decay detection is reduced to Daily-derivation only for the affected weeks.
- If a row's Parent lookup points to a rowId not in the current read, re-read the missing rowId explicitly before flagging as orphaned.
- If Check 9 project counts require row-creation timestamps that Coda's API does not expose reliably, fall back to daily-entry first-mention heuristic and note the approximation in Section 8.
