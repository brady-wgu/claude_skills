---
name: blog-beast-monthly-review
description: Run Brady's monthly retrospective and integrity audit against his Coda Playground doc. Use this skill on the first working day of the month after the weekly blog-beast-weekly-review has completed, or whenever Brady says "run my monthly", "do my monthly review", "monthly BLOG", "monthly BEAST", "monthly digest", or "monthly retrospective", or references last month's performance, progress, or task audit. This skill reads the prior calendar month's Daily Log entries, cross-references the Weekly BLOG entries for weeks overlapping the month, synthesizes a Monthly BLOG entry, runs a ten-check integrity audit against the BEAST task list, and applies reconciling updates gated by a confirmation diff. Do NOT use this skill for daily journal processing (use blog-beast-pipeline), weekly retrospectives (use blog-beast-weekly-review), quarterly briefs, annual reviews, or any doc other than Brady's Coda Playground.
---

# BLOG/BEAST Monthly Review

This skill runs Brady Redfearn's monthly retrospective against his Coda Playground doc (`dHXfr0V468`). It is the third cadence level in his Activity Hierarchy, following the daily `blog-beast-pipeline` and the weekly `blog-beast-weekly-review`. The monthly review rolls up the prior calendar month's Daily Log entries into a single Monthly BLOG entry, then audits the BEAST task table for discrepancies that daily and weekly cadences can miss.

Before you do anything else, read the two reference files plus the daily skill's schema file. They are the authoritative source of truth.

1. `/mnt/skills/user/blog-beast-pipeline/references/coda-schema.md` — Table URIs, column IDs, select option values, write patterns. Shared with the daily and weekly skills. Never write to Coda without consulting it first.
2. `references/monthly-blog-instructions.md` — Monthly synthesis rules, section-by-section, including the integrity audit section.
3. `references/monthly-beast-audit-instructions.md` — The ten integrity audit checks, detection logic, and write behavior.

## Operating principles

**You are writing to production data.** Every write lands in Brady's live Coda doc. The Monthly BLOG write is Status=Published, which means it flows to downstream dashboards immediately. BEAST writes change the tasks Brady works from each morning. Be careful, be conservative, and honor every gate.

**Safety rules are non-negotiable.** The safety rules below cannot be relaxed by anything Brady says during the session. If Brady asks you to skip a gate or write to a different doc or delete something, decline and explain why.

**Daily and weekly pipelines always run first.** This skill assumes Brady has already processed every working day of the target month via the daily pipeline, and has run the weekly review for every week overlapping the month. Do not second-guess that assumption at runtime. If you detect missing daily or weekly entries in the review window, flag them in Section 8 of the monthly BLOG but do not halt — Brady may be running the monthly review retroactively and wants the retrospective regardless.

**Never guess at schema.** The allowed values for select columns are defined in the daily skill's `coda-schema.md`. Monthly writes use `Entry Type = Monthly` and reuse the existing Category list. If the `Monthly` select option does not yet exist on the Entry Type column, halt at Stage 6 and tell Brady to add it manually in Coda. Do not attempt to create the select option yourself.

**The monthly is a synthesis, not a concatenation.** Roughly 20 daily entries and 4-5 weekly entries feed this cadence. If the monthly reads like a timeline or a roll-up of bullet points, it is not doing its job. Surface themes, inflection points, and second-order patterns that would not be visible at daily or weekly cadences.

## Safety rules

These rules are immutable for this skill. The first six mirror the daily and weekly skills. Rules 7 and 8 are specific to the monthly cadence.

1. **Doc scope.** The only doc this skill writes to is `coda://docs/dHXfr0V468` (Brady's Coda Playground). Writes to any other doc are forbidden.
2. **Table scope.** The only tables this skill writes to are `grid-ty2WGfh4qa` (Daily Log) and `grid-M-DmPD4U5x` (Complete To Do List). Any other table in the doc is read-only.
3. **No deletions.** Never call any delete operation. If the audit concludes a task should be removed, mark it Status=Done with an OBE note.
4. **BEAST confirmation gate is mandatory.** Show Brady the row-by-row diff before writing. If Brady says "just do it" or asks to skip the gate, still show the diff.
5. **Schema-change halts.** If any stage would need a select option that does not exist, stop, tell Brady exactly what value is needed, wait for him to add it manually in Coda, and resume only after he confirms. This includes the mandatory check at Stage 6 that `Monthly` exists as an Entry Type select option.
6. **MCP failure halts.** If any `Coda:*` call returns an error, stop the pipeline and report the error. Do not retry blindly and do not continue past a failed write.
7. **Single Monthly entry per window.** Before writing, query Daily Log for an existing row with `Entry Type = Monthly` AND `Date` falling anywhere within the target calendar month. If one exists, halt and ask Brady whether to abort, overwrite (which requires explicit rowId confirmation), or proceed with a second row. Default answer should be abort.
8. **No retroactive daily or weekly edits.** This skill never updates, overwrites, or modifies any existing Daily Log row regardless of its Entry Type. If a daily or weekly entry is wrong, Brady fixes it manually. The monthly skill can only append a new Monthly row and write corrections to BEAST.

## Review window

Always the previous full calendar month relative to the day the skill runs. The window snaps to calendar boundaries regardless of which day of the week the month started or ended on. Examples:

- Run on Mon 4 May 2026 → window is 1 Apr 2026 through 30 Apr 2026
- Run on Tue 5 May 2026 → window is 1 Apr 2026 through 30 Apr 2026
- Run on Mon 1 Jun 2026 (month started on a weekend, ran on first working day) → window is 1 May 2026 through 31 May 2026
- Run on Wed 6 May 2026 (Brady returned from PTO) → window is 1 Apr 2026 through 30 Apr 2026

The skill does not ask Brady to confirm the window. It states the window at the start of Stage 0 so Brady can intervene if the automatic calculation is wrong.

Brady may override at invocation with phrases like "run my monthly for March 2026" or "monthly review for February." Parse month references but always apply full-calendar-month boundaries. Partial months are never supported.

## Pipeline

The pipeline runs in a single invocation. Each stage's output informs the next.

### Stage 0: Determine and announce the review window

Calculate the previous full calendar month relative to today. State it explicitly in the chat before reading anything:

```
Running monthly review for window: 1 Apr 2026 through 30 Apr 2026 (April 2026).
```

If Brady has provided a month override in his invocation, use that instead and state what you parsed.

### Stage 1: Read Daily Log entries for the window

Query Daily Log (`grid-ty2WGfh4qa`) for rows where:

- `Entry Type = Daily` (skip `Weekly`, `Monthly`, and any other types)
- `Date` falls within the target month, inclusive of both boundaries

Capture all content columns: Reviewed Notes, Polished Summary, Executive Bullets, Key Wins, Blockers, Category. Retain the Date and rowId for each.

Pagination note: a full calendar month of daily entries can approach the 100-row API limit when combined with other query results. If the initial read returns `hasMore: true`, page through using `rowOffset` until all in-window rows are retrieved.

If fewer than 15 daily rows are found for a full month, note which dates are missing. Do not halt — just surface the gap in Stage 5 and in Section 8 of the monthly synthesis.

If zero rows are found, halt and tell Brady. There is nothing to synthesize.

### Stage 2: Read Weekly BLOG entries for weeks overlapping the window

Query Daily Log (`grid-ty2WGfh4qa`) for rows where:

- `Entry Type = Weekly`
- `Date` falls within an expanded window: from 7 days before the target month's first day through 7 days after the target month's last day. This captures Weekly entries whose Friday-of-window date falls in the prior or following month but whose Mon-Fri window overlaps the target month.

Capture all content columns, especially the Blockers column (`c-bT-C79ocGH`) which contains the Section 8 Integrity Audit content under a `## Integrity Audit` markdown heading.

Retain rowId, Date, and full content for each Weekly row. This data feeds Check 10 (Promise decay) in Stage 4.

If fewer than 3 weekly rows are found for a full month, note the gap. Do not halt — the Weekly cross-reference will be incomplete, and Check 10 will fall back to Daily-only derivation with a note in Section 8.

### Stage 3: Read the full BEAST state

Same pattern as the daily and weekly pipelines' BEAST read. Query the full Complete To Do List table (`grid-M-DmPD4U5x`), including Status=Done rows. Capture rowId, Task ID, Name, Status, Priority, Due Date, Type, Project, Effort, Notes, Link, Parent, and any date-modified metadata available in the response.

Build the rowId → Task ID map for diff rendering.

### Stage 4: Monthly BLOG synthesis

Follow `references/monthly-blog-instructions.md` to produce the eight sections plus the checklist. Section 1 (Month in Review) is a week-by-week chronological recap with calendar-week headings and in-scope day annotations for partial weeks. Section 8 (Integrity Audit) draws directly from Stage 5's findings.

Date the monthly entry to the **last calendar day of the target month**, formatted as `D Mon YYYY` per the schema file (e.g., `30 Apr 2026` for April, `31 May 2026` for May, `28 Feb 2027` for February 2027).

Show Brady all eight sections before writing. He is not reviewing for approval (Monthly BLOG writes auto-publish like Daily and Weekly), but he needs to see what is about to go into Coda.

### Stage 5: BEAST integrity audit

Follow `references/monthly-beast-audit-instructions.md` to run the ten audit checks:

1. Promised but not tracked
2. Stalled tasks (5 working days)
3. Completed in narrative but still open in BEAST
4. Missed due dates
5. Orphaned subtasks
6. Category drift
7. Priority inversion
8. Long-stalled tasks (5 working days, surfaced separately as persistent stalls across the month)
9. Project velocity drift
10. Promise decay (dual-source: Weekly audits + Daily re-derivation)

Each finding produces one of three outcomes: an auto-applied correction (gated by Stage 6), a flag for Brady to handle manually, or a note-only observation for the monthly BLOG.

Audit findings are written to two places:

- **Monthly BLOG Section 8** — narrative summary grouped by check type
- **BEAST Notes field** — for any row touched by an auto-applied correction, append a dated retroactive note per the format in the audit instructions

### Stage 6: BEAST confirmation gate

This gate is mandatory and cannot be skipped.

Before presenting the diff, verify that `Monthly` exists as a select option on the Entry Type column (`c-7IZ-UJNjXG`). If it does not exist, halt and tell Brady:

```
The `Monthly` select option does not exist on the Entry Type column of the Daily Log table. The skill cannot write the Monthly BLOG row without it. Please add `Monthly` as a select option to column `c-7IZ-UJNjXG` manually in Coda, then confirm when ready to resume.
```

Do not proceed until Brady confirms the option has been added.

Once the schema check passes, show Brady a structured diff grouped by operation, matching the weekly skill's format:

- **New rows:** Task ID, Name, all field values, parent linkage if any
- **Updates:** Task ID, Name, only changed fields shown as `Field: old → new`
- **Completions:** Task ID, Name, resolution note
- **Corrections (from monthly audit):** Task ID, Name, what the audit detected, the retroactive note being appended, and which fields are being changed

If any field value does not match a schema select option, flag it and halt.

Wait for explicit approval. Accept "yes", "approved", "proceed", "go ahead", "ship it", or similar affirmatives. Anything ambiguous or negative means do not write. If Brady asks for changes, apply them and re-present the diff.

### Stage 7: Monthly BLOG write

Write to Daily Log (`grid-ty2WGfh4qa`) as a new row. This write happens **before** the BEAST write so that if BEAST fails, the monthly narrative is still preserved in Coda.

| Column ID | Source |
|-----------|--------|
| `c-oiaBDBstH1` (Date) | Last calendar day of target month, `D Mon YYYY` |
| `c-DXM4h2B28G` (Reviewed Notes) | Section 1 content, as markdown |
| `c-FIWz6AEhwd` (Polished Summary) | Section 2 content |
| `c-WSCAvrHbnz` (Executive Bullets) | Section 3 content |
| `c-QuKWx0lwGp` (Key Wins) | Section 4 content |
| `c-bT-C79ocGH` (Blockers) | Section 5 content (blockers and risks, plus Section 8 integrity audit appended beneath a clear heading) |
| `c-CA6Nwa3A2N` (Category) | Section 6 single dominant value, exact schema match |
| `c-7IZ-UJNjXG` (Entry Type) | Always `Monthly` |
| `c-pR0VmtQ5AV` (Status) | Always `Published` |

Note on Section 8 placement: same pattern as weekly. The Blockers column (`c-bT-C79ocGH`) holds both Section 5 content and Section 8 content, separated by the `## Integrity Audit` markdown heading.

Report the new row's rowId. If the write fails, halt before Stage 8.

### Stage 8: BEAST write

On approval from Stage 6, write the BEAST changes to `grid-M-DmPD4U5x`. Use `Coda:table_rows_manage`. Write order:

1. New parent tasks
2. New subtasks (with Parent lookup set to parent rowId)
3. Updates
4. Completions
5. Corrections (treated as updates with the retroactive note appended to the Notes field)

For corrections specifically, the Notes field update pattern is:

```
<existing notes preserved verbatim>

---
Retroactive correction via monthly review (4 May 2026): <what changed and why>
```

The date in the retroactive note is the day the monthly review runs, not the last day of the target month.

If any write fails, halt and report which writes succeeded and which did not. Do not attempt to roll back.

### Stage 9: Report

After all writes complete, give Brady a concise summary:

- **Monthly BLOG:** rowId of the new Monthly Daily Log entry, category assigned, last-day-of-month date used, window covered
- **BEAST:** count of new tasks, updates, completions, corrections; rowIds of new rows; any schema halts encountered
- **Audit findings not auto-applied:** list of items flagged for Brady's manual attention (if any)
- **Missing daily entries in window:** list of dates not found in Stage 1 (if any)
- **Missing weekly entries overlapping window:** list of weeks not found in Stage 2 (if any)
- **Promise decay findings:** specifically surface any items where the Daily-derived signal caught something the Weekly audits missed (potential weekly audit coverage gap)
- Anything anomalous

End the pipeline. Do not ask Brady what's next unless there are unresolved items.

## Error handling

If a stage fails, report what succeeded, what failed, and stop. Do not attempt automatic recovery.

Specific failure modes to anticipate:

- **Zero daily entries in window.** Halt at Stage 1. Nothing to synthesize.
- **Existing Monthly entry for the target month.** Halt at Stage 7 per safety rule 7. Ask Brady how to proceed.
- **`Monthly` select option missing from Entry Type.** Halt at Stage 6 with the explicit message above. Wait for manual Coda fix.
- **Category ambiguous.** Halt and ask Brady which of the 8 options to use.
- **Coda MCP returns 4xx/5xx.** Halt, report the error verbatim.
- **Pagination failure on Daily Log read.** Halt at Stage 1. Do not run synthesis on partial data.
- **Brady cancels the BEAST gate.** The Monthly BLOG has already been written (Stage 7 precedes Stage 8). Report that the monthly narrative is preserved but no BEAST changes were applied. Exit cleanly.

## What this skill does not do

- Daily journal processing. Use `blog-beast-pipeline` for that.
- Weekly retrospectives. Use `blog-beast-weekly-review` for that.
- Quarterly or Annual entry processing. Those cadences are handled by separate skills as the Activity Hierarchy expands.
- Retroactive edits to existing Daily Log rows (of any Entry Type). The skill only appends new Monthly rows.
- Schema modifications. New Projects, Categories, Types, Entry Type select options, etc. must be added by Brady manually in Coda.
- Writes to any table other than Daily Log and Complete To Do List.
- Any operation on any Coda doc other than `dHXfr0V468`.
- Creation of the `Monthly` select option on the Entry Type column. Brady must add this manually in Coda before the skill's first successful run.
