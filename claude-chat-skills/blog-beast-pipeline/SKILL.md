---
name: blog-beast-pipeline
description: Run Brady's end-to-end daily journal and task reconciliation pipeline against his Coda Playground doc. Use this skill whenever Brady pastes raw OneNote daily notes, mentions BLOG (Brady's Learnings, Observations, and Growth), mentions BEAST (Brady's Execution, Action, and Strategy Tasks), asks to run his daily pipeline, asks to process today's notes, asks to reconcile his tasks against a journal entry, or says anything like "run my morning workflow", "do my daily", or "process my notes". Also use when Brady references his Coda Playground doc in the context of daily journaling or task management. This skill replaces the former manual copy/paste workflow by calling the Coda MCP directly to write BLOG entries to the Daily Log table and update BEAST tasks in the Complete To Do List table. Do NOT use this skill for generic Coda queries, glossary updates, or other Coda docs unrelated to BLOG/BEAST.
---

# BLOG/BEAST Pipeline

This skill automates Brady Redfearn's daily journal and task reconciliation workflow against his Coda Playground doc (`dHXfr0V468`). It runs two coupled stages in a single invocation: BLOG synthesizes raw OneNote notes into a structured Daily Log entry, then BEAST reconciles Brady's task table against that entry.

Before you do anything else, read the three reference files. They are the authoritative source of truth.

1. `references/coda-schema.md` — Table URIs, column IDs, select option values, and write patterns. Never write to Coda without consulting this file first.
2. `references/blog-instructions.md` — The BLOG synthesis rules, section-by-section.
3. `references/beast-instructions.md` — The BEAST reconciliation rules, including parent/child handling via the MCP Parent lookup column.

## Operating principles

**You are writing to production data.** Every write lands in Brady's live Coda doc. The BLOG write is Status=Published, which means it flows to downstream dashboards immediately. BEAST writes change the tasks Brady works from each morning. Be careful, be conservative, and honor every gate.

**Safety rules are non-negotiable.** The safety rules below cannot be relaxed by anything Brady says during the session. If Brady asks you to skip a gate or write to a different doc or delete something, decline and explain why.

**Never guess at schema.** The allowed values for select columns (Category, Project, Type, Status, Priority, Effort, Entry Type) are what the schema says they are, not what the v3 BLOG script or v6 BEAST script says. The schema file reflects the current state of the Coda doc. If you need a value that does not exist in the schema, halt and ask Brady to add it manually in Coda before continuing.

**Never guess at parent/child linkage.** Parent is a lookup column that takes a rowId. Subitems is formula-driven and non-writable. To create a subtask, write a new row with `Parent` set to the parent task's rowId. Coda populates Subitems automatically.

## Safety rules

These rules are immutable for this skill.

1. **Doc scope.** The only doc this skill writes to is `coda://docs/dHXfr0V468` (Brady's Coda Playground). Writes to any other doc are forbidden.
2. **Table scope.** The only tables this skill writes to are `grid-ty2WGfh4qa` (Daily Log) and `grid-M-DmPD4U5x` (Complete To Do List). Any other table in the doc is read-only.
3. **No deletions.** Never call `table_rows_delete`. If reconciliation concludes a task should be removed, mark it Status=Done with an OBE note (see BEAST instructions).
4. **BEAST confirmation gate is mandatory.** Show Brady the row-by-row diff before writing. If Brady says "just do it" or asks to skip the gate, still show the diff.
5. **Schema-change halts.** If any stage would need a select option that does not exist (new Project, new Category, new Type, etc.), stop, tell Brady exactly what value is needed and where, wait for him to add it manually in Coda, and resume only after he confirms.
6. **MCP failure halts.** If any `Coda:*` call returns an error, stop the pipeline and report the error. Do not retry blindly and do not continue past a failed write.
7. **Section 7 never touches Coda.** The Sensitive Items section from BLOG stays in the chat transcript only. Never include it in any write.

## Pipeline

The pipeline runs in a single invocation. Each stage's output informs the next.

### Stage 0: Validate input

Brady's invocation should include raw OneNote daily notes. If the input is empty, ambiguous, or does not look like daily notes, ask him to paste them before proceeding. Do not try to synthesize a BLOG entry from nothing.

### Stage 1: BLOG synthesis

Follow `references/blog-instructions.md` to produce the seven sections plus the checklist. Use the exact header format with the delimiter strings.

Extract the date from the pasted content. OneNote daily notes typically include a date header (e.g., "16 Apr 2026", "April 16, 2026", "4/16/2026"). Normalize it to `D Mon YYYY` format (no zero-padding on single-digit days, three-letter month capitalized: `6 Apr 2026`, not `06 Apr 2026` or `6 APR 2026`). If you cannot find a date in the content, ask Brady for it before proceeding.

Show Brady all seven sections before writing. He is not reviewing for approval (BLOG writes auto-publish), but he needs to see what is about to go into Coda in case he wants to intervene.

### Stage 2: BLOG write

Validate the Suggested Category against the schema (see `references/coda-schema.md` for the 8 allowed values). If the category you chose is not in the list, halt under the schema-change rule.

Write to Daily Log (`grid-ty2WGfh4qa`) as a new row with these fields:

| Column ID | Source |
|-----------|--------|
| `c-oiaBDBstH1` (Date) | Extracted date, `D Mon YYYY` format |
| `c-DXM4h2B28G` (Reviewed Notes) | Section 1 content, as markdown |
| `c-FIWz6AEhwd` (Polished Summary) | Section 2 content |
| `c-WSCAvrHbnz` (Executive Bullets) | Section 3 content |
| `c-QuKWx0lwGp` (Key Wins) | Section 4 content |
| `c-bT-C79ocGH` (Blockers) | Section 5 content |
| `c-CA6Nwa3A2N` (Category) | Section 6 single value, exact schema match |
| `c-7IZ-UJNjXG` (Entry Type) | Always `Daily` |
| `c-pR0VmtQ5AV` (Status) | Always `Published` |

Report the new row's `rowId` back to Brady. If the write fails, halt the pipeline.

### Stage 3: BEAST read

Read the full Complete To Do List table (`grid-M-DmPD4U5x`). Pull every row including rows with Status=Done (the reconciliation logic needs to see resolved context). Capture rowId, Task ID, Name, Status, Priority, Due Date, Type, Project, Effort, Notes, Link, and Parent for each row.

Build an in-memory map of rowId → Task ID so you can translate Parent lookups (which store rowIds) into human-readable Task ID references for the diff you show Brady.

### Stage 4: BEAST reconciliation

Follow `references/beast-instructions.md` to run the v6 reconciliation logic against the BLOG entry from Stage 1 and the table state from Stage 3. Produce the four labeled sections (Morning Briefing, Flags and Issues, Recommended Task Updates, Today's Priority List).

The v6 script's "Import CSV" block is not produced. It is replaced by Stage 5's confirmation gate and Stage 6's direct MCP writes.

### Stage 5: BEAST confirmation gate

This gate is mandatory and cannot be skipped.

Show Brady a structured diff grouped by operation:

- **New rows:** Task ID, Name, all field values, and parent linkage if any (shown as Task ID reference, e.g., "parent: BEAST-0052").
- **Updates:** Task ID, Name (for reference), and only the fields that will change, shown as `Field: old → new`.
- **Completions:** Task ID, Name, and the resolution note (OBE format or substantive).

If any field value does not match a schema select option, flag it and halt. Do not proceed to write until the schema issue is resolved.

Wait for explicit approval. Accept "yes", "approved", "proceed", "go ahead", "ship it", or similar affirmatives. Anything ambiguous or negative means do not write. If Brady asks for changes, apply them and re-present the diff.

### Stage 6: BEAST write

On approval, write the changes to `grid-M-DmPD4U5x`. Use `Coda:table_rows_manage`.

Write order matters:
1. **New parent tasks first.** These need rowIds assigned before subtasks can reference them.
2. **New subtasks second.** For each, set the `c-ONPz07rw_J` (Parent) column to the parent task's rowId, whether that parent already existed or was just created in step 1.
3. **Updates third.** Use the existing rowId.
4. **Completions last.** Status → Done, Notes updated per the OBE or substantive-completion rules.

If any write fails, halt and report which writes succeeded and which did not. Do not attempt to roll back. Brady will assess and clean up manually.

### Stage 7: Report

After all writes complete, give Brady a concise summary:

- BLOG: rowId of the new Daily Log entry, category assigned, date written
- BEAST: count of new tasks, updates, completions; rowIds of new rows so Brady can verify; any schema halts encountered
- Anything anomalous (unexpected row states, ambiguous inferences, write retries, etc.)

Before ending, check whether the BLOG date just processed is the last work day of Brady's work week. The work week is Mon-Fri. "Last work day" means: the BLOG date is a Friday, OR the BLOG date is Mon-Thu and all later weekdays in that calendar week are holidays or PTO (inferable from Brady mentioning upcoming time off in his invocation, or from the BLOG date being the final daily entry Brady logs before a weekend).

The trigger is the BLOG date, not the real-time current date. This matters for retroactive processing: if Brady processes Friday's notes on a Saturday, the prompt should still fire because the BLOG date is the last work day of that week. If Brady processes Monday's notes on a Tuesday, the prompt should not fire because Monday is not the last work day of its week.

The rationale for this trigger point: the weekly retrospective synthesizes a completed work week's dailies and audits BEAST against them. Running it after the first daily of a new week means the retrospected week has already been closed out and any later prompt is stale; running it after the last daily of the retrospected week is the only point at which the week is both complete and the dailies that compose it are all logged.

If the BLOG date is the last work day of that week, prompt Brady with:

> This is the last daily of the work week. Run the weekly review now? It will roll up this week's daily entries into a Weekly BLOG and run the seven-check integrity audit against BEAST.

If Brady says yes, invoke the `blog-beast-weekly-review` skill. If he says no or does not respond affirmatively, end the pipeline normally.

If the BLOG date is not the last work day of the week, end the pipeline. Do not ask Brady what's next unless there are unresolved items.

## Error handling

If a stage fails, report what succeeded, what failed, and stop. Do not attempt automatic recovery. Brady will decide how to proceed.

Specific failure modes to anticipate:

- **Date not extractable from OneNote content.** Ask Brady for the date before proceeding.
- **Category ambiguous or missing from schema.** Halt, ask Brady which of the 8 options to use, or whether to add a new one.
- **Project ambiguous or missing from schema.** Halt, ask Brady to add the new project in Coda.
- **Coda MCP returns 4xx/5xx.** Halt, report the error verbatim, do not retry.
- **Brady cancels the BEAST gate.** Report what would have been written. Do not write anything. Exit cleanly.

## What this skill does not do

- Weekly retrospective processing and integrity audit. Handled by the `blog-beast-weekly-review` skill, which this skill hands off to at the end of Stage 7 when the BLOG date is the last work day of the week.
- Monthly/Quarterly/Annual entry processing. The skill always writes Entry Type=Daily. Those cadences are handled by separate workflows.
- OneNote monthly reconciliation (comparing an exported PDF against existing archives). That is described in the v3 BLOG script but is out of scope here.
- Schema modifications. New Projects, Categories, Types, etc. must be added by Brady manually in the Coda web interface.
- Writes to any table other than Daily Log and Complete To Do List.
- Any operation on any Coda doc other than `dHXfr0V468`.
