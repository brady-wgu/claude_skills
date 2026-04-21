# Reference: Pre-Flight Task ID Check

**Applies to:** `blog-beast-pipeline` and `blog-beast-weekly-review` skills (also applicable to any future skill that writes BEAST rows).

**Purpose:** Prevent Task ID collisions when adding new BEAST rows. Context from earlier in a session becomes stale the moment any other process (Brady, another Claude session, a Coda automation) writes to the BEAST table. Task IDs must be derived from the live table state at the moment of write, not from earlier reads.

**Incident this prevents:** On 16 Apr 2026, Claude assigned BEAST-0140 to a new MyOpenMath row based on an earlier max-ID read, not realizing Brady had added a different BEAST-0140 (Domain Driven Design course review) between reads. Resulted in two rows sharing the same Task ID. Corrected in-place but should have been prevented.

## The Rule

**Before every BEAST `add` operation, re-read the current maximum Task ID from the live table.** No exceptions, even if Claude just read the table seconds earlier.

## Implementation

### Step 1: Read max Task ID immediately before write

Call `Coda:table_rows_read` against the BEAST table with this filter and limit:

```
uri: coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x
filterFormula: StartsWith(thisRow.[Task ID], "BEAST-")
rowLimit: 5
filterColumnNames: ["Task ID"]
```

Sort descending on Task ID is not available via filter formula alone. Instead:

- Read with the filter above (all parent BEAST-#### tasks)
- Increase `rowLimit` to 50 if needed to ensure the current max is captured (BEAST table is sorted by Task ID descending by default in its default view, but the MCP read may not honor view sort order)
- Parse the returned Task IDs, extract the integer portion after `BEAST-`, and take the max

### Step 2: Exclude subtask IDs

Subtask Task IDs have the form `BEAST-0026.13` (parent.child). Only the parent integer matters for the max calculation. Split on `.` and take the first segment.

### Step 3: Compute next ID

```python
max_id = max(
    int(row["values"]["c-ImEDreEoEA"]["content"].split("-")[1].split(".")[0])
    for row in response["rows"]
    if row["values"]["c-ImEDreEoEA"]["content"].startswith("BEAST-")
)
next_id = f"BEAST-{max_id + 1:04d}"
```

### Step 4: Use next_id in the add operation

Pass `next_id` as the Task ID column value in the `Coda:table_rows_manage` add payload.

## When to skip this check

Never.

The check is cheap (one read, under a second) and the collision it prevents is expensive (requires a corrective update, creates audit noise, and can propagate if the duplicate ID gets referenced in other documents before the fix). Even if Claude just read the BEAST table earlier in the same Stage, re-read before writing.

## Subtask ID handling

If adding a subtask under an existing parent (e.g., adding a new person to the BEAST-0026 networking parent), the numbering rule is different:

- Read the parent row's `Subitems` array
- Find the max `.N` suffix among existing subtasks
- Assign `.N+1`

Subtasks do not collide with parent IDs because of the dot notation, so a parent max-ID read is not needed when adding a subtask.

## Verification after write

After any BEAST add, re-read the row by filter on the newly-assigned Task ID. Confirm:

1. Exactly one row exists with that Task ID (not two)
2. The values match what was intended

If the filter returns two rows, a collision happened despite the check (rare but possible if two writes hit the table within the same millisecond). Immediately update one of the rows to the next available ID and document the collision in the session report.

## Skill integration notes

This check should be invoked at:

- `blog-beast-pipeline` Stage 7 (BEAST Write), before every new task add
- `blog-beast-weekly-review` Stage 7 (BEAST Write), before every new task add
- Any future `blog-beast-monthly-review` or `blog-beast-quarterly-review` Stage 7 operations
- Any ad-hoc BEAST task creation requested mid-session

If the skill has a helper function for "add task to BEAST," the max-ID read should be inside that helper, not a responsibility of each caller.
