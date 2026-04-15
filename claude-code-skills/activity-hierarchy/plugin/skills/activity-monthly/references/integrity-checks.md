# Integrity Checks Reference

Standard audit procedures used by all Activity Hierarchy skills at the weekly level and above. The `activity-daily` skill uses only Check 1 (Blocker Cross-Reference). Higher-level skills progressively add more checks as indicated.

---

## Check 1: Blocker-to-BEAST Cross-Reference
**Used by:** Daily, Weekly, Monthly, Quarterly, Annual

Extract all unique blocker phrases from the source entries (BLOG Section 5 for daily, Blockers column for higher levels). For each blocker, search the BEAST task list for a matching task by keyword overlap in the Name or Notes fields.

**Output:** For each unmatched blocker:
- The blocker text
- "UNTRACKED: No corresponding BEAST task found"
- Recommendation: "Create a new BEAST task for this blocker?" or "Link to existing BEAST task [BEAST-XXXX]?"

---

## Check 2: Overdue Task Flag
**Used by:** Weekly, Monthly, Quarterly, Annual

List all BEAST tasks where:
- Due Date is earlier than today
- Status is NOT "Done" or "Cancelled"

**Output:** Bulleted list with Task ID, Name, Due Date, days overdue, current Status.

---

## Check 3: Cadence Gap Detection
**Used by:** Weekly, Monthly, Quarterly, Annual

Check whether all expected sub-period entries exist in the Daily Log:

| Skill Level | Checks For |
|---|---|
| Weekly | Every workday (Mon-Fri) in the target week has a Daily entry |
| Monthly | Every work week in the target month has a Weekly entry; every workday has a Daily entry |
| Quarterly | Every month in the quarter has a Monthly Digest |
| Annual | Every quarter in the year has a Quarterly Review |

**Output:** List of missing entries with dates and expected Entry Type.

---

## Check 4: Prior-Period Closure
**Used by:** Weekly, Monthly, Quarterly, Annual

Read the prior period's entry of the same type (e.g., for this week's Weekly, read last week's Weekly). Extract the "Looking Ahead" / "Executive Bullets" section. Compare each item against the current period's actual activity.

**Categorize each item as:**
- **Completed** - Clear evidence in the current period's entries that this was done
- **In Progress** - Partial evidence of work, not yet finished
- **Not Started** - No evidence of any work on this item
- **Dropped** - Explicitly deprioritized or superseded by other work

**Output:**
- Commitment completion rate: X/Y items addressed (Z%)
- List of items categorized as above
- Flag any "Not Started" items as requiring attention

---

## Check 5: Blocker Lifecycle Tracking
**Used by:** Monthly, Quarterly, Annual

For the target period, build a timeline of blockers:
- **Introduced:** First appearance of the blocker (date and source entry)
- **Resolved:** Date the blocker no longer appears in subsequent entries
- **Persisted:** Still present at the end of the period

**Output:**
- New blockers introduced this period: count and list
- Blockers resolved this period: count, list, average resolution time (days)
- Blockers persisting from prior period: count and list with age in days
- Resolution velocity: average days from introduction to resolution

---

## Check 6: Category Distribution Analysis
**Used by:** Monthly, Quarterly, Annual

Count the number of Daily entries per Category value for the target period. Calculate percentages.

**Output:**
- Table: Category | Entry Count | Percentage
- Dominant category (highest %) with flag if >60% concentration
- Shift analysis: compare against prior period's distribution (if available)
- Workstream balance assessment: is effort distributed appropriately?

---

## Check 7: Workstream Health Summary
**Used by:** Quarterly, Annual

For each Project value in the BEAST table, calculate:
- Tasks completed in the period (Status changed to "Done")
- Tasks still active (Status is "Not started" or "In progress")
- Tasks added during the period (by BLOG note dates)
- Tasks stalled (Status unchanged for >14 days with no Note updates)
- Net change (completed - added)

**Output:**
- Table: Project | Completed | Active | Added | Stalled | Net Change
- Health assessment per workstream: "Progressing", "Stalled", "Growing", "Winding Down"
- Flag any workstream with more stalled tasks than active tasks

---

## Check 8: Stale Task Detection
**Used by:** Weekly (14-day threshold), Monthly (14-day), Quarterly (30-day), Annual (30-day)

Flag BEAST tasks where:
- Status is "Not started" or "In progress"
- Notes field has no datestamped entry within the threshold period
- The task is not marked "Done" or "Cancelled"

**Output:** Bulleted list with Task ID, Name, last Note date (or "No notes"), days since last update.

---

## Check 9: Completion Velocity (Daily Enhancement)
**Used by:** Daily

After BEAST processing, count:
- Tasks completed today (Status changed to "Done" based on BLOG evidence)
- Tasks created today (new BEAST-XXXX tasks added)
- Net task delta (completed - created)

**Output:** One-line summary in the Final Report: "Task velocity: X completed, Y created, net delta Z"

---

## Check 10: Auto-Prioritization Signal (Daily Enhancement)
**Used by:** Daily

Scan BLOG Sections 1-3 for combinations of:
- A named stakeholder (person's name)
- Urgency language ("urgent", "ASAP", "deadline", "critical", "by end of day", "blocking")

If found, check whether the related BEAST task has Priority = "High". If not, flag for upgrade.

**Output:** "PRIORITY SIGNAL: [stakeholder name] + urgency language found for [topic]. Related BEAST task [BEAST-XXXX] is currently [Priority]. Recommend upgrade to High?"
