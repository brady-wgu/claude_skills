# blog-beast-pipeline

Automated daily BLOG and BEAST pipeline. Paste raw OneNote notes into Claude Code and everything else happens automatically: BLOG processing, Coda write, BEAST pull, BEAST processing, Coda upsert, final report.

## Full Specification

The complete pipeline specification (processing rules, section formats, field standards, Coda schema) lives in one place:

**`plugin/skills/run-pipeline/SKILL.md`**

Both the Claude Code skill plugin and direct CLI usage follow the same spec. If you need to update pipeline behavior, edit SKILL.md only.

## Setup

See **`docs/SETUP.md`** for full installation instructions, including:
- Prerequisites (Python 3.10+, Coda API key)
- Running `python scripts/discover_config.py` to auto-configure table/column IDs
- Plugin installation for Claude Code
- Verification and troubleshooting

## Direct Use (Without Plugin)

If running the pipeline without the skill plugin installed, the same SKILL.md spec applies. Claude Code reads this CLAUDE.md on startup, which points to the spec. Trigger with any of:

`run pipeline`, `run BLOG and BEAST`, `process my notes`, `morning briefing`, `run morning updates`

## Key Files

| File | Purpose |
|------|---------|
| `plugin/skills/run-pipeline/SKILL.md` | Single source of truth for pipeline spec |
| `docs/SETUP.md` | Installation and setup guide |
| `scripts/discover_config.py` | Auto-discovers Coda table/column IDs |
| `scripts/pipeline_config.py` | Shared config loader for all scripts |
| `scripts/blog_to_coda.py` | Writes BLOG entry to Coda Daily Log |
| `scripts/beast_from_coda.py` | Pulls BEAST table from Coda as CSV |
| `scripts/beast_to_coda.py` | Upserts BEAST updates to Coda |
| `scripts/coda_client.py` | Low-level Coda API wrapper |
| `config.json` | Auto-generated schema config (gitignored) |
| `.env` | API credentials (gitignored) |
