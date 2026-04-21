# Monthly BLOG Instructions

This file defines the synthesis rules for the Monthly BLOG entry. The monthly entry mirrors the weekly eight-section structure but operates at a higher level of synthesis, covering roughly 20 daily entries and 4-5 weekly entries rolled into a single retrospective.

## Scope and voice

The monthly BLOG entry is a **thematic synthesis**, not a re-narration of each week. It surfaces patterns, inflection points, and second-order observations that would not be visible at daily or weekly cadences. It is written for three audiences: Brady himself (for continuity and strategic reflection), WGU leadership (via the downstream Executive View dashboard), and Brady's own quarterly and annual cadences (which will read the monthly entries as their input).

Voice is the same as daily and weekly: senior professional tone, no em dashes, no AI clichés, DD MMM YYYY dates in prose (Coda column writes use `D Mon YYYY`), first-person when reflecting on the month's work.

Keep every section substantive but concise. The monthly is a synthesis of syntheses. If a section could be written by just concatenating weekly entries, it is not doing its job. The monthly should surface things the weekly cadence did not: shifts in direction across weeks, patterns in how work was categorized or prioritized across the month, persistent themes vs one-off events.

## Input materials

By the time synthesis begins, you have:

- Roughly 15-22 Daily Log rows with Entry Type = Daily, dated within the target calendar month
- Roughly 3-5 Daily Log rows with Entry Type = Weekly, with Dates on Fridays of weeks overlapping the month
- Full BEAST table state
- Audit findings from Stage 5 (not yet written anywhere)

Do not invent material. If daily entries for certain days are missing, do not fabricate what happened. Note the gaps in Section 8.

## Section structure

Use exactly these eight section headers in this order. Each header uses the `##` markdown level.

```
## Section 1: Month in Review
## Section 2: Polished Monthly Summary
## Section 3: Executive Bullets
## Section 4: Key Wins
## Section 5: Blockers and Risks
## Section 6: Suggested Category
## Section 7: Sensitive Items
## Section 8: Integrity Audit
```

### Section 1: Month in Review

Week-by-week chronological recap. This is the monthly equivalent of the weekly's Week in Review section, organized by calendar week to preserve the month's natural rhythm.

List every week that overlaps the target month. For each week, use a `###` sub-heading in this format:

```
### Week of <Mon D> - <Fri D Mon YYYY> (in-scope: <day range or "full week">)
```

Examples for April 2026:

```
### Week of 30 Mar - 3 Apr 2026 (in-scope: 1-3 Apr)
### Week of 6 - 10 Apr 2026 (in-scope: full week)
### Week of 13 - 17 Apr 2026 (in-scope: full week)
### Week of 20 - 24 Apr 2026 (in-scope: full week)
### Week of 27 Apr - 1 May 2026 (in-scope: 27-30 Apr)
```

For each week's sub-section, write 1-3 paragraphs synthesizing what happened that week **using only the in-scope days**. Do not narrate activities that fell outside the month boundary, even if they are part of the same calendar week. For partial weeks, explicitly note when the week's narrative is truncated by the month boundary (e.g., "This week continued into May and will be fully covered in the May monthly retrospective.").

Preferred synthesis source for each week:
1. If a Weekly BLOG entry exists for that week, use it as the primary source, filtering to in-scope days only
2. If no Weekly BLOG entry exists, synthesize directly from the in-scope Daily entries for that week
3. Note in Section 8 any weeks where a Weekly BLOG was missing

After the week-by-week recap, add a `### Cross-Week Themes` sub-section with 1-2 paragraphs of synthesis **across** the weeks — what threads persisted, what shifted, what emerged or resolved.

Written in first person. Markdown allowed.

### Section 2: Polished Monthly Summary

A single leadership-ready paragraph, 6-10 sentences. Brady's PDO leadership should be able to read this and understand the month's shape without reading anything else.

No bullets. No headers within the paragraph. Just dense prose.

The monthly summary should be distinctly shaped — it covers strategic arcs, not just activity volume. A reader should come away with a clear answer to "what was this month about?"

### Section 3: Executive Bullets

6-10 bullets, one line each. These appear in the Executive View dashboard and should stand alone without Section 2's context.

Format each bullet as a single sentence fragment leading with a strong verb: "Completed...", "Advanced...", "Escalated...", "Delivered...", "Closed...", "Launched...". Past tense, active voice.

Monthly executive bullets should emphasize outcomes and milestones, not weekly activities. A bullet that could have appeared verbatim in a weekly entry is too granular for the monthly.

### Section 4: Key Wins

Roll up the Key Wins from the month's weekly entries (or from daily entries for weeks without a Weekly BLOG), deduplicated and elevated.

A win that appeared in two weekly entries (e.g., "started X" in week 1, "completed X" in week 3) collapses into one monthly bullet framed at the completion state.

A win that felt significant at the weekly cadence but is minor in monthly context may be omitted.

A win that emerged only visible at monthly cadence (cumulative progress across multiple weeks that no single week would claim) should be surfaced explicitly.

4-10 bullets is typical. If the month was genuinely thin, fewer is honest and better than padding.

### Section 5: Blockers and Risks

Two sub-lists, both bulleted:

**Persistent blockers** — items that blocked work across multiple weeks or remain unresolved at month's end. If a blocker was surfaced in multiple Weekly BLOGs, explicitly note the duration: "Week 3 of 4 waiting on JFT response to E010 scenario clarifications" or "Persisted across all four weeks of April."

**Escalation candidates** — items that should be raised to leadership, external partners, or cross-functional stakeholders in the coming month. Monthly escalation candidates should be things the weekly cadence already tried to surface or that the cumulative monthly view makes newly visible.

If a blocker from a prior month is still active, note that explicitly.

If there are no blockers, write `None` for each sub-list rather than omitting them.

### Section 6: Suggested Category

Single dominant value from the 8 allowed Daily Log categories (see `coda-schema.md`). Pick the category that best represents the month's dominant theme.

For the monthly cadence, compute the category distribution across the month's Daily entries first, then select the category that either (a) has a plurality of Daily entries, or (b) if there's a close split, represents the higher-priority strategic work.

Write the value on its own line, exact case match. No prose explanation in the Coda column.

In the chat-visible preview, note the reasoning briefly (one sentence) so Brady can intervene if the choice is wrong, but do not include that reasoning in the Coda write.

### Section 7: Sensitive Items

Chat-only. Never written to Coda.

Use this section to surface anything that should stay out of the published Coda entry: personnel concerns, interpersonal friction, confidential leadership signals, anything Brady flagged in daily or weekly Sensitive Items sections. Aggregate and surface for Brady's awareness only.

If nothing applies, write `None`.

### Section 8: Integrity Audit

This section summarizes the findings from Stage 5's ten audit checks. Format:

```
### Audit Summary

- Auto-applied corrections: <count>
- Flagged for manual attention: <count>
- Observations (note-only): <count>

### Auto-Applied Corrections

<bulleted list, each entry: Task ID, one-line description of what was corrected>

### Flagged for Manual Attention

<bulleted list, each entry: Task ID or commitment phrase, one-line description of what needs your review>

### Observations

<bulleted list of patterns detected that did not warrant a correction>

### Monthly-Specific Findings

**Long-stalled tasks (Check 8):**
<list of tasks stalled for the entire month>

**Project velocity drift (Check 9):**
<per-project opened vs closed ratios, with flagged projects highlighted>

**Promise decay (Check 10):**
<commitments persisting across multiple weekly audits, plus any items where Daily-derived signal caught something the Weekly audits missed>

### Coverage Gaps

<if any daily entries missing from the window, list missing dates; if any weekly entries missing from weeks overlapping the window, list missing weeks; otherwise write "All daily and weekly entries present.">
```

Keep each bullet tight — Task ID plus one sentence. The full diff Brady sees at the Stage 6 confirmation gate provides the detail; this section is the lasting record in Coda.

## Writing into the Blockers column

The Daily Log table has no column dedicated to the monthly integrity audit. Section 5 (Blockers) and Section 8 (Integrity Audit) are both written to `c-bT-C79ocGH`.

Concatenate in this order, separated by a blank line:

```markdown
## Blockers and Risks

**Persistent blockers**
- ...

**Escalation candidates**
- ...

## Integrity Audit

### Audit Summary
...

### Auto-Applied Corrections
...

### Flagged for Manual Attention
...

### Observations
...

### Monthly-Specific Findings
...

### Coverage Gaps
...
```

Brady's downstream Coda views can parse the `## Integrity Audit` heading to surface the audit separately if he adds a formula-driven column later.

## Checklist

Before declaring the synthesis complete, verify:

- [ ] All eight sections present with correct headers
- [ ] Section 1 has a sub-heading for every week that overlaps the month, with correct in-scope annotations
- [ ] Section 1 ends with a `### Cross-Week Themes` sub-section
- [ ] Section 6 value is one of the 8 allowed categories, case-exact
- [ ] Date used is the last calendar day of the target month in `D Mon YYYY` format
- [ ] No fabricated content for missing daily or weekly entries
- [ ] No em dashes anywhere in the prose
- [ ] No AI clichés ("dive into", "leverage", "unlock", "navigate", "journey", "elevate", "orchestrate", etc.)
- [ ] First-person voice in Sections 1, 2, 4, 5
- [ ] Past tense in Sections 3, 4
- [ ] Section 7 contents will not be written to Coda
- [ ] Section 8 audit counts match what was detected in Stage 5
- [ ] Section 8 Monthly-Specific Findings sub-section is present
- [ ] Section 8 Coverage Gaps sub-section lists both daily and weekly missing entries (or confirms completeness)
