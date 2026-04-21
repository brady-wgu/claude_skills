# Weekly BLOG Instructions

This file defines the synthesis rules for the Weekly BLOG entry. The weekly entry mirrors the daily seven-section structure plus one additional section (Integrity Audit) specific to the weekly cadence.

## Scope and voice

The weekly BLOG entry is a **retrospective rollup**, not a re-narration of each day. It synthesizes patterns, themes, and outcomes across the Mon-Fri window. It is written for two audiences: Brady himself (for continuity and course correction) and WGU leadership (via the downstream Executive View dashboard).

Voice is the same as the daily: senior professional tone, no em dashes, no AI clichés, DD MMM YYYY dates in prose (Coda column writes use `D Mon YYYY`), first-person when reflecting on the week's work.

Keep every section substantive but concise. The weekly is a synthesis, not a concatenation. If a section could be written by just pasting together daily entries, it is not doing its job.

## Input materials

By the time synthesis begins, you have:

- 0-5 Daily Log rows with Entry Type = Daily, dated within the window, each with Reviewed Notes, Polished Summary, Executive Bullets, Key Wins, Blockers, Category
- Full BEAST table state
- Audit findings from Stage 4 (not yet written anywhere)

Do not invent material. If a daily entry for Wed is missing, do not fabricate what happened Wednesday. Note the gap in Section 8.

## Section structure

Use exactly these eight section headers in this order. Each header uses the `##` markdown level.

```
## Section 1: Week in Review
## Section 2: Polished Weekly Summary
## Section 3: Executive Bullets
## Section 4: Key Wins
## Section 5: Blockers and Risks
## Section 6: Suggested Category
## Section 7: Sensitive Items
## Section 8: Integrity Audit
```

### Section 1: Week in Review

Narrative synthesis across the week. 4-8 paragraphs. This is the weekly equivalent of the daily's Reviewed Notes section — the raw, thinking-out-loud layer that downstream sections are distilled from.

Cover:

- What the week was about (the 1-3 dominant threads)
- How the week unfolded day by day at a high level (not a blow-by-blow, more like "early week focused on X; midweek pivoted to Y after Z happened")
- Shifts in direction, priority, or approach during the week
- How the week closed (momentum, unresolved questions, handoffs to next week)

Written in first person. Markdown allowed.

### Section 2: Polished Weekly Summary

A single leadership-ready paragraph, 4-6 sentences. Brady's PDO leadership should be able to read this and understand the week's shape without reading anything else.

No bullets. No headers within the paragraph. Just dense prose.

### Section 3: Executive Bullets

5-8 bullets, one line each. These appear in the Executive View dashboard and should stand alone without Section 2's context.

Format each bullet as a single sentence fragment leading with a strong verb: "Completed...", "Advanced...", "Escalated...", "Delivered...". Past tense, active voice.

### Section 4: Key Wins

Roll up the Key Wins sections from the week's daily entries, deduplicated and consolidated. Present as a bulleted list.

If two daily entries both claim the same win (e.g., Mon said "submitted JFT SDP scenario catalog v1.1" and Wed said "finalized scenario catalog"), collapse into one bullet with the final-state framing.

If a daily Key Win is trivial in the weekly context (e.g., "cleared inbox"), omit it unless it was notable for a specific reason.

3-8 bullets is typical. If the week was genuinely thin, fewer is honest and better than padding.

### Section 5: Blockers and Risks

Two sub-lists, both bulleted:

**Persistent blockers** — items that blocked work on multiple days or remain unresolved at week's end.

**Escalation candidates** — items that should be raised to leadership, external partners (Jellyfish, vendors), or cross-functional stakeholders in the coming week.

If a blocker from a prior week is still active, note that explicitly: "Week 3 of waiting on JFT response to the E010 scenario clarifications."

If there are no blockers, write `None` for each sub-list rather than omitting them.

### Section 6: Suggested Category

Single value from the 8 allowed Daily Log categories (see `coda-schema.md`). Pick the category that best represents the week's dominant theme. If two categories split the week roughly evenly, pick the one tied to the higher-priority work.

Write the value on its own line, exact case match. No prose explanation in the Coda column.

In the chat-visible preview, you may note the reasoning briefly (one sentence) so Brady can intervene if the choice is wrong, but do not include that reasoning in the Coda write.

### Section 7: Sensitive Items

Chat-only. Never written to Coda.

Use this section to surface anything that should stay out of the published Coda entry: personnel concerns, interpersonal friction, confidential leadership signals, anything Brady flagged in a daily Sensitive Items section. Aggregate and surface for Brady's awareness only.

If nothing applies, write `None`.

### Section 8: Integrity Audit

This section summarizes the findings from Stage 4's seven audit checks. Format:

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

<bulleted list of patterns detected that did not warrant a correction: category drift metrics, priority inversion, etc.>

### Daily Entry Coverage

<if any daily entries missing from the window, list missing dates; otherwise write "All five daily entries present.">
```

Keep each bullet tight — Task ID plus one sentence. The full diff Brady sees at the Stage 5 confirmation gate provides the detail; this section is the lasting record in Coda.

## Writing into the Blockers column

The Daily Log table has no column dedicated to the weekly integrity audit. Section 5 (Blockers) and Section 8 (Integrity Audit) are both written to `c-bT-C79ocGH`.

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

(etc.)
```

Brady's downstream Coda views can parse the `## Integrity Audit` heading to surface the audit separately if he adds a formula-driven column later.

## Checklist

Before declaring the synthesis complete, verify:

- [ ] All eight sections present with correct headers
- [ ] Section 6 value is one of the 8 allowed categories, case-exact
- [ ] Date used is the Friday of the review window in `D Mon YYYY` format
- [ ] No fabricated content for missing daily entries
- [ ] No em dashes anywhere in the prose
- [ ] No AI clichés ("dive into", "leverage", "unlock", "navigate", "journey", etc.)
- [ ] First-person voice in Sections 1, 2, 4, 5
- [ ] Past tense in Sections 3, 4
- [ ] Section 7 contents will not be written to Coda
- [ ] Section 8 audit counts match what was detected in Stage 4
