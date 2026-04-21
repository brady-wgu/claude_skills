# Reference: Sensitive Items Preservation

**Applies to:** `blog-beast-pipeline` and `blog-beast-weekly-review` skills. Also relevant to `blog-beast-monthly-review` and future quarterly/annual skills.

**Purpose:** Preserve Section 7 (Sensitive Items) content so it persists beyond the chat session. Section 7 is the highest-signal section of most reviews (strategic risks, stakeholder dynamics, soft-decline patterns, political observations) but it is chat-only by design. In the current skill design, it disappears when the conversation ends.

**Problem observed:** Across seven weekly reviews, substantive Section 7 content has been generated and discarded, including:

- Nathan-Scott stakeholder alignment gap (Week 3)
- No-feedback signal from 30 Mar leadership update (Week 6)
- Rachel Marcial zyBooks quality assessment as vendor-relationship language risk (Week 7)
- ChatGPT license soft-decline pattern from Mike (Week 7)
- Daryl Lee and Samantha Mosby "does not want to meet" relationship signals (Week 3)

None of these are appropriate for Coda (either because they are politically sensitive, because they reference individuals by name in ways that should not live in a shared tool, or because they are half-formed observations not suitable for team visibility). But losing them entirely is also wrong — they compound into pattern recognition over time.

## The Rule

At Stage 8 (Report), after the Weekly BLOG is written to Coda and the BEAST updates are complete, Claude produces a **separate chat-only artifact** formatted for paste into Brady's private doc.

### Artifact format

The artifact is a Markdown block formatted specifically for paste into OneNote's "00_Sensitive Items" page. The header includes the review window so entries stack chronologically when pasted at the top.

```markdown
## Sensitive Items — Week N (DD MMM YYYY through DD MMM YYYY)

*Generated DD MMM YYYY during blog-beast-weekly-review session. Not written to Coda.*

- [Item 1: full narrative observation]
- [Item 2: full narrative observation]
- [continues as needed]
```

Items should be full sentences or short paragraphs, not bullets of fragments. A reader six months later should be able to understand each item without additional context.

### Where this goes in the skill flow

Insert as Stage 8.5, between Stage 8 (Report) and skill completion:

1. Stage 8: Report to chat on what was written
2. **Stage 8.5: Sensitive Items artifact** — render the chat-only artifact
3. Skill completion

The artifact should be visually distinct from the regular report. Use a horizontal rule above and below, and explicit framing:

```
---

## Sensitive Items — Chat-Only Artifact

**This block is not written to Coda. Paste into your private "00_Sensitive Items" doc.**

[artifact content as specified above]

---
```

## What belongs in Sensitive Items

Items that belong in Section 7 and therefore in this artifact:

- Political or stakeholder-dynamic observations (alignment gaps, role tensions, soft-decline patterns)
- Relationship signals about specific individuals (unresponsive contacts, difficult working dynamics)
- Framing risks (language that is accurate but could damage a relationship if used verbatim in a deliverable)
- Meta-observations about the review process itself or about Brady's working patterns
- Early-stage observations that are not yet conclusions but are worth tracking across weeks
- Budget, contract, or compensation sensitivities
- Security concerns or credential-handling observations

Items that do NOT belong here (and should go in the regular Weekly BLOG instead):

- Factual commitments with owners and due dates (these go in BEAST)
- Neutral narrative about what happened (this goes in Section 1)
- Blockers that are public-facing and should be visible to leadership (Section 5)
- Win-and-loss summaries (Sections 3 and 4)

The test: if Brady would be uncomfortable with the item appearing in a doc his manager could read, it belongs in Sensitive Items. If he would not care, it belongs in the Coda write.

## Integration with the 00_Sensitive Items page

Brady created the "00_Sensitive Items" OneNote page on 12 Mar 2026 but it has not been kept up. The artifact format above is designed to enable a copy-paste workflow:

1. At the end of each weekly review, Brady sees the chat-only artifact
2. He selects the entire Markdown block, copies it
3. He pastes it at the top of the 00_Sensitive Items page
4. Done. No other manipulation needed.

The header date format (`Week N (DD MMM YYYY through DD MMM YYYY)`) allows chronological stacking with newest-on-top, matching Brady's OneNote daily journal convention.

## Integration with monthly and quarterly reviews

The monthly and quarterly review skills should pull from the 00_Sensitive Items page as optional input context when synthesizing cross-period patterns. However, since Brady has asked Claude not to fetch OneNote content programmatically (no Microsoft Graph API), this integration is manual:

- When running the monthly review, Brady can optionally paste the relevant month's Sensitive Items entries as additional context
- Claude uses them to inform pattern recognition across weeks
- Claude should never write Sensitive Items content back to Coda, regardless of which skill is running

## Alternative: If 00_Sensitive Items continues to be neglected

If Brady finds the copy-paste workflow is still being missed, a fallback is to render the Sensitive Items artifact as a downloadable `.md` file using the `create_file` tool. This gives Brady a concrete artifact he can file anywhere, not just OneNote. The file would be named `sensitive-items-YYYY-MM-DD.md` and saved to `/mnt/user-data/outputs/` for download.

Trade-off: files are more durable than chat blocks but add friction to the workflow. Start with the chat-only artifact and escalate to files only if the pattern shows the chat version is being lost.

## What should NEVER appear in this artifact

To protect Brady and the individuals mentioned, these are prohibited even in the chat-only artifact:

- Passwords, API keys, tokens, or any credential material
- Personally identifying information about students beyond what already exists in Coda
- Medical, financial, or legal details about named individuals
- Direct quotes attributed to a named individual unless Brady has already used that quote in a written form

The purpose of Sensitive Items is strategic observation, not gossip or evidence collection. If an item feels like it could be read back in a legal or HR context and cause harm, it does not belong in the artifact.
