# Coda Schema Reference

This file is the authoritative source for every Coda URI, column ID, and select option the skill uses. Consult it before every read or write. If the schema on this page conflicts with anything in the v3 BLOG script or v6 BEAST script, the schema on this page wins.

## Document

**Doc URI:** `coda://docs/dHXfr0V468`
**Name:** Brady's Coda Playground
**Only doc the skill writes to.** Writes to any other doc are forbidden.

## Write targets

These are the only two tables the skill writes to.

### Daily Log (BLOG destination)

- **Table URI:** `coda://docs/dHXfr0V468/tables/grid-ty2WGfh4qa`
- **Table ID:** `grid-ty2WGfh4qa`
- **Page:** Data Tables → Daily Log

### Complete To Do List (BEAST destination)

- **Table URI:** `coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x`
- **Table ID:** `grid-M-DmPD4U5x`
- **Page:** Data Tables → To Do List

Every other table in the doc is read-only as far as this skill is concerned, including user-facing views like "Current Drafts", "Executive View", "B.L.O.G. Feed", and "Current To Do List". Those are views and interfaces layered on top of the two write targets above. Do not write to them.

## Daily Log columns

Column order and IDs as they appear in `grid-ty2WGfh4qa`:

| Column | Column ID | Type | Writable | Notes |
|--------|-----------|------|----------|-------|
| Date | `c-oiaBDBstH1` | date (DAY_MONTH_TEXT_SHORT_YEAR) | yes | Display column. Write as `D Mon YYYY`, no zero-padding |
| Reviewed Notes | `c-DXM4h2B28G` | canvas | yes | Accepts markdown |
| Polished Summary | `c-FIWz6AEhwd` | text | yes | Accepts markdown |
| Executive Bullets | `c-WSCAvrHbnz` | text | yes | Accepts markdown |
| Key Wins | `c-QuKWx0lwGp` | text | yes | Accepts markdown |
| Blockers | `c-bT-C79ocGH` | text | yes | Accepts markdown |
| Category | `c-CA6Nwa3A2N` | select (single) | yes | See allowed values below |
| Entry Type | `c-7IZ-UJNjXG` | select (single) | yes | See allowed values below |
| Status | `c-pR0VmtQ5AV` | select (single) | yes | See allowed values below |

### Daily Log: Category (select, single)

Exact allowed values (case-sensitive):

- `Onboarding`
- `Initiative`
- `People & Network`
- `Team & Culture`
- `Definitions & Concepts`
- `Tools & Access`
- `Strategy`
- `Delivery`

The v3 BLOG script's category list (which includes UPL, Intake, Admin) is outdated. Use only the 8 values above. If none fit, halt and ask Brady.

### Daily Log: Entry Type (select, single)

Exact allowed values (case-sensitive), verified against Coda on 16 Apr 2026:

- `Daily`
- `Weekly`
- `Monthly`
- `Quarterly`
- `Annual`

This skill always writes `Daily`. Other values are produced by higher-cadence skills (weekly review, monthly digest, quarterly brief, annual review) and must match these option names exactly. Earlier schema drafts referenced `Monthly Digest`, `Quarterly Brief`, and `Annual Review`; those values do not exist in the Coda select list and will fail on write.

### Daily Log: Status (select, single)

Exact allowed values (case-sensitive):

- `Draft`
- `Published`

This skill always writes `Published`.

## Complete To Do List columns

Column order and IDs as they appear in `grid-M-DmPD4U5x`:

| Column | Column ID | Type | Writable | Notes |
|--------|-----------|------|----------|-------|
| Name | `c-MBRsPfbd6d` | text | yes | Display column |
| Status | `c-zH_C1i-smP` | select (single) | yes | See allowed values below |
| Priority | `c-g-kRN3Y2aS` | select (single) | yes | See allowed values below |
| Due Date | `c-NP39SR6C8D` | date (DAY_MONTH_TEXT_SHORT_YEAR) | yes | Write as `D Mon YYYY`, no zero-padding |
| Link | `c-wuGVeM0y7z` | url | yes | URL only |
| Type | `c-Z_PWA6_-Bb` | select (single) | yes | See allowed values below |
| Project | `c-W3gb8_ca2O` | select (single) | yes | See allowed values below |
| Effort | `c-RdNqDL9akn` | select (single) | yes | See allowed values below |
| Notes | `c-ioDsMHggmZ` | text | yes | Plain text |
| Parent | `c-ONPz07rw_J` | lookup (single) | yes | Takes rowId of parent task in same table |
| Subitems | `c-RRrt1LG5D9` | lookup (multiple, formula) | NO | Computed from Parent, never write |
| Task ID | `c-ImEDreEoEA` | text | yes | Format: `BEAST-XXXX` or `BEAST-XXXX.N` |

### To Do List: Status (select, single)

Exact allowed values (case-sensitive):

- `Not started`
- `In progress`
- `Done`
- `Blocked`

Note: `Not started` and `In progress` have lowercase second words. Not `Not Started` or `In Progress`.

### To Do List: Priority (select, single)

Exact allowed values (case-sensitive):

- `Low`
- `Medium`
- `High`

### To Do List: Type (select, single)

Exact allowed values (case-sensitive):

- `Action`
- `Meeting`
- `Research`
- `Deliverable`
- `Admin`

### To Do List: Project (select, single)

Exact allowed values (case-sensitive, preserve spaces and punctuation exactly):

- `JFT SDP`
- `Networking`
- `Team/Ops`
- `Onboarding`
- `Interactive Math Experiences`
- `BSHA (Bachelor of Science Healthcare Administration)`

The v6 BEAST script lists `Cicada` as a project. That project no longer exists. Cicada-era work now lives under `JFT SDP`. If reconciliation implies a new project name not in the list above, halt and ask Brady to add it in Coda first.

### To Do List: Effort (select, single)

Exact allowed values (case-sensitive, including the space):

- `30 min`
- `Half day`
- `Full day`
- `Multi-day`

## Parent/child task linkage

The BEAST table supports two levels of hierarchy. The v6 script's CSV-import workaround (manually setting parent relationships in the Coda UI after import) is obsolete for the MCP path. Use the Parent lookup column directly.

### How Parent works

- `c-ONPz07rw_J` (Parent) is a single-lookup column referencing rows in the same table (`grid-M-DmPD4U5x`).
- To assign a parent, write the parent row's **rowId** (e.g., `i-u2zIEX2RDZ`) to this column. Not the Task ID. Not the Name.
- `c-RRrt1LG5D9` (Subitems) is a formula-driven multi-lookup that Coda populates automatically from Parent. Never write to this column.

### Creating a new subtask under an existing parent

1. Look up the parent's rowId from the Stage 3 read (you have a rowId → Task ID map in memory).
2. Call `Coda:table_rows_manage` with:
   - All required fields (Name, Status, Priority, Due Date, Type, Project, Effort, Notes, Link)
   - Task ID as `BEAST-XXXX.N` where XXXX matches the parent's numeric part and N is the next sequential integer under that parent
   - `c-ONPz07rw_J` (Parent) set to the parent's rowId

### Creating a new parent and new subtasks in the same session

Order matters. You cannot reference a rowId that does not exist yet.

1. Write the parent row first. Capture its returned rowId.
2. Write each subtask, with `c-ONPz07rw_J` set to the newly captured parent rowId.

### Task ID assignment

- **New parent tasks:** Continue the `BEAST-XXXX` sequence from the highest existing numeric ID in the current table. Zero-pad to 4 digits.
- **New subtasks:** `BEAST-XXXX.N` where XXXX matches the parent and N starts at 1, incrementing per subtask in order of creation under that parent.
- **Existing subtasks with a BEAST-XXXX.N ID:** keep the existing ID permanently.
- **Existing subtasks without an ID:** assign one the first time they become the subject of an update or flag. Do not mass-assign IDs to all untagged subtasks at once unless there is a specific operational reason.

## MCP tool call patterns

### Reading the current Daily Log entries

```
Coda:table_rows_read
  uri: coda://docs/dHXfr0V468/tables/grid-ty2WGfh4qa
  filterFormula: thisRow.[Entry Type] = "Daily"
  rowLimit: 20
```

### Reading the full BEAST table

```
Coda:table_rows_read
  uri: coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x
  rowLimit: 100
  (paginate with rowOffset if totalRows > 100)
```

### Writing a new BLOG entry

```
Coda:table_rows_manage
  uri: coda://docs/dHXfr0V468/tables/grid-ty2WGfh4qa
  action: add (or whatever the manage tool expects; verify schema at runtime)
  rows: [
    {
      c-oiaBDBstH1: "16 Apr 2026",
      c-DXM4h2B28G: "<Section 1 markdown>",
      c-FIWz6AEhwd: "<Section 2 markdown>",
      c-WSCAvrHbnz: "<Section 3 markdown>",
      c-QuKWx0lwGp: "<Section 4 markdown>",
      c-bT-C79ocGH: "<Section 5 markdown>",
      c-CA6Nwa3A2N: "Strategy",
      c-7IZ-UJNjXG: "Daily",
      c-pR0VmtQ5AV: "Published"
    }
  ]
```

### Writing a new BEAST parent task

```
Coda:table_rows_manage
  uri: coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x
  rows: [
    {
      c-ImEDreEoEA: "BEAST-0165",
      c-MBRsPfbd6d: "Task name",
      c-zH_C1i-smP: "Not started",
      c-g-kRN3Y2aS: "High",
      c-NP39SR6C8D: "20 Apr 2026",
      c-Z_PWA6_-Bb: "Action",
      c-W3gb8_ca2O: "JFT SDP",
      c-RdNqDL9akn: "Half day",
      c-ioDsMHggmZ: "Task notes here",
      c-wuGVeM0y7z: ""
    }
  ]
```

### Writing a new BEAST subtask under an existing parent

```
Coda:table_rows_manage
  uri: coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x
  rows: [
    {
      c-ImEDreEoEA: "BEAST-0027.3",
      c-MBRsPfbd6d: "Subtask name",
      c-zH_C1i-smP: "Not started",
      c-g-kRN3Y2aS: "Medium",
      c-NP39SR6C8D: "18 Apr 2026",
      c-Z_PWA6_-Bb: "Meeting",
      c-W3gb8_ca2O: "Networking",
      c-RdNqDL9akn: "30 min",
      c-ioDsMHggmZ: "Subtask notes",
      c-wuGVeM0y7z: "",
      c-ONPz07rw_J: "i-u2zIEX2RDZ"
    }
  ]
```

### Updating an existing task

```
Coda:table_rows_manage
  uri: coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x
  rows: [
    {
      rowId: "i-existingRowId",
      c-zH_C1i-smP: "In progress",
      c-ioDsMHggmZ: "Updated notes reflecting current progress"
    }
  ]
```

Include only the fields that change when updating. Do not re-send unchanged fields.

### Marking a task Done with OBE resolution

```
Coda:table_rows_manage
  uri: coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x
  rows: [
    {
      rowId: "i-existingRowId",
      c-zH_C1i-smP: "Done",
      c-ioDsMHggmZ: "OBE. Task Done.\n\n<original notes preserved verbatim>"
    }
  ]
```

## Date format

All dates (Daily Log Date, BEAST Due Date) use the Coda `DAY_MONTH_TEXT_SHORT_YEAR` format, which Coda accepts as `D Mon YYYY` with:

- No zero-padding on single-digit days: `6 Apr 2026`, not `06 Apr 2026`
- Three-letter month, capitalized first letter only: `Apr`, not `APR` or `April`
- Four-digit year: `2026`

Brady's document style preference (DD MMM YYYY, all caps month) does not apply here. Coda's date parser is the constraint, and these are data fields not prose.

## Select value validation pattern

Before every write involving a select column, verify the value against the list in this file. If it does not match exactly, halt. Do not:

- Lowercase or uppercase to "normalize" (`not started` will not match `Not started`)
- Substitute a "closest match" (do not write `Team & Ops` when the column wants `Team/Ops`)
- Skip the field and write the row anyway

The skill's schema-change halt rule exists to keep the table clean. Use it.
