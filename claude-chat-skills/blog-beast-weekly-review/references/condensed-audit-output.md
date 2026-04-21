# Reference: Condensed Audit Output Format

**Applies to:** `blog-beast-weekly-review` skill primarily. Patterns generalize to `blog-beast-monthly-review` and any future quarterly/annual review skills.

**Purpose:** Reduce audit section verbosity when the seven-check integrity audit returns clean. After seven weekly reviews processed, only one legitimate flag has surfaced across all of them. The heavy subsection structure (Auto-Applied Corrections, Flagged for Manual Attention, Observations, Daily Entry Coverage) is overkill when every subsection reports "none."

**What this does not change:** When the audit finds actual content, the full structure is still used. Collapsing only happens when all findings are clean.

## The Rule

Section 8 of the Weekly BLOG synthesis has two rendering modes:

1. **Condensed mode** — used when the audit is clean across all seven checks
2. **Expanded mode** — used when any check surfaces a correction, flag, or material observation

### Condensed mode (all-clean)

Render Section 8 as a single summary line followed by the Daily Entry Coverage line:

```
### Section 8: Integrity Audit

All seven integrity checks clean. N of N in-window tasks Done; 0 auto-corrections, 0 flags, M note-only observations. Daily entry coverage: all five entries present.
```

Where:
- `N` is the count of in-window tasks that closed (e.g., 23)
- `M` is the count of note-only observations (e.g., 6)

**Critical:** Note-only observations are not reported in condensed mode beyond the count. If an observation is substantive enough to warrant the reader's attention, it is not a "note-only" observation and the audit should render in expanded mode.

### Expanded mode (any findings)

Render the full eight-subsection structure as currently specified in the skill:

- Audit Summary (counts)
- Auto-Applied Corrections (with details)
- Flagged for Manual Attention (with details)
- Observations (with details)
- Daily Entry Coverage (with details)

Only include subsections that have content. Empty subsections are omitted.

## Decision logic

At Stage 4 (Audit), after running all seven checks:

```python
auto_corrections = count_auto_corrections()
flags = count_flags()
observations = count_observations()
daily_coverage_complete = (entries_present == 5)

is_clean = (
    auto_corrections == 0
    and flags == 0
    and daily_coverage_complete
    and all(observation.is_note_only for observation in observations)
)

if is_clean:
    render_condensed_audit()
else:
    render_expanded_audit()
```

## What counts as "note-only"

Note-only observations are items the audit captures for record-keeping but that do not require reader action or reframe any conclusion:

- Retrospective audit context statements ("this review runs N weeks after the fact")
- Category distribution summaries with no drift finding
- "Stalled tasks: none" confirmations
- "Priority inversion: none" confirmations
- "Missed due dates: none" confirmations

Items that are NOT note-only (and therefore force expanded mode):

- Any category drift above 30%
- Any stalled High-priority task
- Any missed due date
- Any task flagged as untracked
- Any daily entry missing from the window
- Any narrative-to-BEAST mismatch
- Any schema-change halt condition

## Examples

### Good condensed audit (from a clean week)

```
### Section 8: Integrity Audit

All seven integrity checks clean. 23 of 23 in-window tasks Done; 0 auto-corrections, 0 flags, 5 note-only observations. Daily entry coverage: all five entries present.
```

### Good expanded audit (from Week 7, 40% drift)

```
### Section 8: Integrity Audit

### Audit Summary

- Auto-applied corrections: 0
- Flagged for manual attention: 0
- Observations (note-only): 6

### Observations

- Category distribution for the window: Initiative 3 days, Tools & Access 1 day, Delivery 1 day. (M+K)/N = 2 of 5, or 40 percent drift. This is above the 30 percent observation threshold and the highest drift ratio across the seven weeks processed. The drift is substantively accurate, 8 Apr was legitimately a Tools & Access day (pipeline rebuild) and 10 Apr was a Delivery continuation day with no new intake.
- Four new carry-forward tasks (BEAST-0116, 0120, 0121, 0131) are queued against 17 Apr due dates. This is the largest single-week accumulation of forward-dated work in the observed history and warrants a Week 8 triage.
- [additional observations as warranted]

### Daily Entry Coverage

All five daily entries present.
```

Note the expanded version only includes subsections that have content. Auto-Applied Corrections and Flagged for Manual Attention are omitted because both are zero.

## Skill integration notes

Update Stage 8 (Report) in the weekly-review skill to:

1. Determine `is_clean` using the logic above
2. If clean, render Section 8 as the single-line condensed format
3. If not clean, render Section 8 with only the subsections that have content
4. Either way, still write the full BLOG/BEAST integrity state to the Coda write as the Blockers column content

The Coda write in Stage 6 should use whichever format was selected for Section 8. The condensed format saves roughly 400 characters per clean week, which over a year compounds into meaningfully less Coda storage and significantly faster read operations when the monthly/quarterly skills pull weekly entries into their context windows.
