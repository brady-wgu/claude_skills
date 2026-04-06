# blog-beast-automation

Automated daily BLOG and BEAST workflow with Coda.io integration, powered by Claude Code.

## What This Does

Collapses a multi-step manual workflow into a single interaction:

1. Paste raw daily work notes into Claude Code
2. BLOG processor produces a 7-section journal entry
3. Entry is written to the Coda Daily Log table
4. BEAST table is pulled from Coda
5. BEAST processor produces a 4-section morning briefing with task updates
6. Changed/new rows are upserted back to the Coda To Do List
7. Final report with priority list and any sensitive items

## Quick Start

1. Clone this repo
2. Copy `config.example.env` to `.env` and add your Coda API key
3. Install dependencies: `pip install -r requirements.txt`
4. Open Claude Code in this directory
5. Paste your daily notes

Claude Code reads `CLAUDE.md` and handles the rest.

## Project Structure

```
blog-beast-automation/
  CLAUDE.md              # Pipeline orchestration + BLOG/BEAST specs
  .env                   # Coda API key (gitignored)
  config.example.env     # Template for .env
  requirements.txt       # requests, python-dotenv
  scripts/
    coda_client.py       # Coda API wrapper (scoped to one doc)
    blog_to_coda.py      # Write BLOG entry to Daily Log table
    beast_from_coda.py   # Pull BEAST table as 12-column CSV
    beast_to_coda.py     # Upsert BEAST updates via Task ID
  docs/
    SETUP.md             # Detailed setup guide
```

## Pipeline Modes

Set in `CLAUDE.md`:

- **TEST**: Pauses after every step for review
- **PRODUCTION**: Runs the full pipeline without pausing

## Safety

- All Coda API calls are scoped to doc ID `dHXfr0V468` (hard-coded validation)
- Section 7 (Sensitive Items) is never written to Coda
- Parent/Subitems columns require manual assignment in Coda after new task creation
- The API key never appears in code or logs

## Dependencies

- Python 3.10+
- requests
- python-dotenv
- Claude Code (the LLM processor)
