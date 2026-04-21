---
name: blog-beast-weekly-review
description: Run Brady's weekly retrospective and integrity audit against his Coda Playground doc. Use this skill on the first work day of the week after the daily blog-beast-pipeline has completed, or whenever Brady says "run my weekly", "do my weekly review", "weekly BLOG", "weekly BEAST", "weekly retrospective", or references last week's performance, progress, or task audit. This skill reads the prior Mon-Fri Daily Log entries, synthesizes a Weekly BLOG entry, runs a seven-check integrity audit against the BEAST task list, and applies reconciling updates gated by a confirmation diff. Do NOT use this skill for daily journal processing (use blog-beast-pipeline), monthly digests, quarterly briefs, or any doc other than Brady's Coda Playground.
---

# BLOG/BEAST Weekly Review

This skill runs Brady Redfearn's weekly retrospective against his Coda Playground doc (`dHXfr0V468`). It complements the daily `blog-beast-pipeline` skill by rolling up the prior work week's Daily Log entries into a single Weekly BLOG entry, then auditing the BEAST task table for discrepancies that daily-cadence reconciliation can miss.

Before you do anything else, read the two reference files plus the daily skill's schema file. They are the authoritative source of truth.

1. `/mnt/skills/user/blog-beast-pipeline/coda-schema.md` — Table URIs, column IDs, select option values, write patterns. Shared with the daily skill. Never write to Coda without consulting it first.
2. `references/weekly-blog-instructions.md` — Weekly synthesis rules, section-by-section, including the integrity audit section.
3. `references/weekly-beast-audit-instructions.md` — The seven integrity audit checks, detection logic, and write behavior.

## Operating principles

**You are writing to production data.** Every write lands in Brady's live Coda doc. The Weekly BLOG write is Status=Published, which means it flows to downstream dashboards immediately. BEAST writes change the tasks Brady works from each morning. Be careful, be conservative, and honor every gate.

**Safety rules are non-negotiable.** The safety rules below cannot be relaxed by anything Brady says during the session. If Brady asks you to skip a gate or write to a different doc or delete something, decline and explain why.

**The daily pipeline always runs first.** This skill assumes Brady has already processed the Friday (or final work day) of the review window via the daily pipeline before this skill is invoked. Do not second-guess that assumption at runtime. If you detect missing daily entries in the review window, flag them in Section 8 of the weekly BLOG but do not halt — Brady may be running the weekly review after a vacation and wants the retrospective regardless.

**Never guess at schema.** The allowed values for select columns are defined in the daily skill's `coda-schema.md`. Weekly writes use `Entry Type = Weekly` and reuse the existing Category list. If you need a value that does not exist in the schema, halt and ask Brady to add it manually in Coda before continuing.

## Safety rules

These rules are immutable for this skill. The first six mirror the daily skill. Rules 7 and 8 are specific to the weekly cadence.

1. **Doc scope.** The only doc this skill writes to is `coda://docs/dHXfr0V468` (Brady's Coda Playground). Writes to any other doc are forbidden.
2. **Table scope.** The only tables this skill writes to are `grid-ty2WGfh4qa` (Daily Log) and `grid-M-DmPD4U5x` (Complete To Do List). Any other table in the doc is read-only.
3. **No deletions.** Never call any delete operation. If the audit concludes a task should be removed, mark it Status=Done with an OBE note.
4. **BEAST confirmation gate is mandatory.** Show Brady the row-by-row diff before writing. If Brady says "just do it" or asks to skip the gate, still show the diff.
5. **Schema-change halts.** If any stage would need a select option that does not exist, stop, tell Brady exactly what value is needed, wait for him to add it manually in Coda, and resume only after he confirms.
6. **MCP failure halts.** If any `Coda:*` call returns an error, stop the pipeline and report the error. Do not retry blindly and do not continue past a failed write.
7. **Single Weekly entry per window.** Before writing, query Daily Log for an existing row with `Entry Type = Weekly` AND `Date = <Friday of window>`. If one exists, halt and ask Brady whether to abort, overwrite (which requires explicit rowId confirmation), or proceed with a second row. Default answer should be abort.
8. **No retroactive daily edits.** This skill never updates, overwrites, or modifies any existing Daily Log row. If a daily entry is wrong, Brady fixes it manually. The weekly skill can only append a new Weekly row and write corrections to BEAST.

## Review window

Always the previous Monday through Friday relative to the day the skill runs. Examples:

- Run on Mon 20 Apr 2026 → window is Mon 13 Apr – Fri 17 Apr 2026
- Run on Tue 21 Apr 2026 (Monday was a holiday) → window is Mon 13 Apr – Fri 17 Apr 2026
- Run on Wed 29 Apr 2026 (Brady returned from PTO) → window is Mon 20 Apr – Fri 24 Apr 2026

The skill does not ask Brady to confirm the window. It states the window at the start of Stage 0 so Brady can intervene if the automatic calculation is wrong.

Brady may override at invocation with phrases like "run my weekly for the week of 6 Apr" or "weekly review for last week minus Monday". Parse date references but still apply Mon-Fri boundaries — partial weeks get full-window treatment with an explicit note in Section 8 about which daily entries are missing.

## Pipeline

The pipeline runs in a single invocation. Each stage's output informs the next.

### Stage 0: Determine and announce the review window

Calculate the previous Mon-Fri window relative to today. State it explicitly in the chat before reading anything:

```
Running weekly review for window: Mon 13 Apr 2026 through Fri 17 Apr 2026.
```

If Brady has provided a window override in his invocation, use that instead and state what you parsed.

### Stage 1: Read Daily Log entries for the window

Query Daily Log (`grid-ty2WGfh4qa`) for rows where:

- `Entry Type = Daily` (skip `Weekly`, `Monthly`, `Quarterly`, `Annual`)
- `Date` falls within the window, inclusive

Capture all content columns: Reviewed Notes, Polished Summary, Executive Bullets, Key Wins, Blockers, Category. Retain the Date and rowId for each.

If fewer than 5 rows are found, note which dates are missing. Do not halt — just surface the gap in Stage 4 and in Section 8 of the weekly synthesis.

If zero rows are found, halt and tell Brady. There is nothing to synthesize.

### Stage 2: Read the full BEAST state

Same pattern as the daily pipeline's BEAST read. Query the full Complete To Do List table (`grid-M-DmPD4U5x`), including Status=Done rows. Capture rowId, Task ID, Name, Status, Priority, Due Date, Type, Project, Effort, Notes, Link, Parent, and any date-modified metadata available in the response.

Build the rowId → Task ID map for diff rendering.

### Stage 3: Weekly BLOG synthesis

Follow `references/weekly-blog-instructions.md` to produce the eight sections plus the checklist. Section 8 (Integrity Audit) is new to the weekly cadence and draws directly from Stage 4's findings.

Date the weekly entry to the **Friday of the review window**, formatted as `D Mon YYYY` per the schema file.

Show Brady all eight sections before writing. He is not reviewing for approval (Weekly BLOG writes auto-publish like Daily), but he needs to see what is about to go into Coda.

### Stage 4: BEAST integrity audit

Follow `references/weekly-beast-audit-instructions.md` to run the seven audit checks:

1. Promised but not tracked
2. Stalled tasks (default 5 working days)
3. Completed in narrative but still open in BEAST
4. Missed due dates
5. Orphaned subtasks
6. Category drift (Misc/uncategorized volume > 30%)
7. Priority inversion

Each finding produces one of three outcomes: an auto-applied correction (gated by Stage 5), a flag for Brady to handle manually, or a note-only observation for the weekly BLOG.

Audit findings are written to two places:

- **Weekly BLOG Section 8** — narrative summary grouped by check type
- **BEAST Notes field** — for any row touched by an auto-applied correction, append a dated retroactive note per the format in the audit instructions

### Stage 5: BEAST confirmation gate

This gate is mandatory and cannot be skipped.

Show Brady a structured diff grouped by operation, matching the daily skill's format plus one addition:

- **New rows:** Task ID, Name, all field values, parent linkage if any
- **Updates:** Task ID, Name, only changed fields shown as `Field: old → new`
- **Completions:** Task ID, Name, resolution note
- **Corrections (new, weekly-specific):** Task ID, Name, what the audit detected, the retroactive note being appended, and which fields are being changed

If any field value does not match a schema select option, flag it and halt.

Wait for explicit approval. Accept "yes", "approved", "proceed", "go ahead", "ship it", or similar affirmatives. Anything ambiguous or negative means do not write. If Brady asks for changes, apply them and re-present the diff.

### Stage 6: Weekly BLOG write

Write to Daily Log (`grid-ty2WGfh4qa`) as a new row. This write happens **before** the BEAST write so that if BEAST fails, the weekly narrative is still preserved in Coda.

| Column ID | Source |
|-----------|--------|
| `c-oiaBDBstH1` (Date) | Friday of window, `D Mon YYYY` |
| `c-DXM4h2B28G` (Reviewed Notes) | Section 1 content, as markdown |
| `c-FIWz6AEhwd` (Polished Summary) | Section 2 content |
| `c-WSCAvrHbnz` (Executive Bullets) | Section 3 content |
| `c-QuKWx0lwGp` (Key Wins) | Section 4 content |
| `c-bT-C79ocGH` (Blockers) | Section 5 content (blockers and risks, plus Section 8 integrity audit appended beneath a clear heading) |
| `c-CA6Nwa3A2N` (Category) | Section 6 single value, exact schema match |
| `c-7IZ-UJNjXG` (Entry Type) | Always `Weekly` |
| `c-pR0VmtQ5AV` (Status) | Always `Published` |

Note on Section 8 placement: the Daily Log table has no dedicated audit column. The integrity audit content is appended to the Blockers column (`c-bT-C79ocGH`) beneath a markdown heading `## Integrity Audit`. This is documented in the weekly BLOG instructions file.

Report the new row's rowId. If the write fails, halt before Stage 7.

### Stage 7: BEAST write

On approval from Stage 5, write the BEAST changes to `grid-M-DmPD4U5x`. Use `Coda:table_rows_manage`. Write order:

1. New parent tasks
2. New subtasks (with Parent lookup set to parent rowId)
3. Updates
4. Completions
5. Corrections (treated as updates with the retroactive note appended to the Notes field)

For corrections specifically, the Notes field update pattern is:

```
<existing notes preserved verbatim>

---
Retroactive correction via weekly review (20 Apr 2026): <what changed and why>
```

The date in the retroactive note is the day the weekly review runs, not the Friday of the window.

If any write fails, halt and report which writes succeeded and which did not. Do not attempt to roll back.

### Stage 8: Report

After all writes complete, give Brady a concise summary:

- **Weekly BLOG:** rowId of the new Weekly Daily Log entry, category assigned, Friday date used, window covered
- **BEAST:** count of new tasks, updates, completions, corrections; rowIds of new rows; any schema halts encountered
- **Audit findings not auto-applied:** list of items flagged for Brady's manual attention (if any)
- **Missing daily entries in window:** list of dates not found in Stage 1 (if any)
- Anything anomalous

End the pipeline. Do not ask Brady what's next unless there are unresolved items.

## Error handling

If a stage fails, report what succeeded, what failed, and stop. Do not attempt automatic recovery.

Specific failure modes to anticipate:

- **Zero daily entries in window.** Halt at Stage 1. Nothing to synthesize.
- **Existing Weekly entry for the window's Friday.** Halt at Stage 6 per safety rule 7. Ask Brady how to proceed.
- **Category ambiguous.** Halt and ask Brady which of the 8 options to use.
- **Coda MCP returns 4xx/5xx.** Halt, report the error verbatim.
- **Brady cancels the BEAST gate.** The Weekly BLOG has already been written (Stage 6 precedes Stage 7). Report that the weekly narrative is preserved but no BEAST changes were applied. Exit cleanly.

## What this skill does not do

- Daily journal processing. Use `blog-beast-pipeline` for that.
- Monthly, Quarterly, or Annual entry processing. Those cadences are handled by separate skills as the Activity Hierarchy expands.
- Retroactive edits to existing Daily Log rows. The skill only appends new Weekly rows.
- Schema modifications. New Projects, Categories, Types, etc. must be added by Brady manually in Coda.
- Writes to any table other than Daily Log and Complete To Do List.
- Any operation on any Coda doc other than `dHXfr0V468`.
